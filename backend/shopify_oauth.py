"""
Shopify OAuth 2.0 install and callback for custom/public apps.

Register the same redirect URL in Partner Dashboard as SHOPIFY_REDIRECT_URI (HTTPS in production).

State is HMAC-signed (no Flask session). Payload is base64url so | is not in query strings.

Routes:
  GET /oauth/install?shop=yourstore.myshopify.com
  GET /oauth/callback?code=...&shop=...&state=...
  GET /oauth/self-test  — verify signing works on this machine (no Shopify call)
"""
from __future__ import annotations

import base64
import hashlib
import html
import hmac
import threading
import time
import urllib.parse

import requests
from flask import Blueprint, jsonify, redirect, request

from shopify_config import (
    get_api_version,
    get_oauth_client_id,
    get_oauth_client_secret,
    get_oauth_redirect_uri,
    get_oauth_state_signing_secret,
    get_scopes,
    normalize_shop_domain,
    oauth_skip_state_verify,
)
from shopify_token_store import save_token

_PALADIO_METAFIELD_DEFINITIONS = [
    ("Enriched Category", "paladio", "category", "single_line_text_field", "AI-enriched Google Product Taxonomy category"),
    ("Category Level 1", "paladio", "category_level_1", "single_line_text_field", "Top-level category"),
    ("Category Level 2", "paladio", "category_level_2", "single_line_text_field", "Second-level category"),
    ("Category Level 3", "paladio", "category_level_3", "single_line_text_field", "Third-level category"),
    ("Optimized Title", "paladio", "optimized_title", "single_line_text_field", "AI-optimized product title"),
    ("Optimized Description", "paladio", "optimized_description", "multi_line_text_field", "AI-optimized product description"),
    ("SEO Keywords", "paladio", "seo_keywords", "json", "AI-generated SEO keywords"),
    ("Product Attributes", "paladio", "attributes", "json", "All enriched product attributes"),
    ("Brand", "paladio", "brand", "single_line_text_field", "Product brand name"),
    ("Material", "paladio", "material", "single_line_text_field", "Product material composition"),
    ("Avalara Tax Code", "paladio", "avalara_tax_code", "single_line_text_field", "Tax code for automated tax calculation"),
    ("Tax Category", "paladio", "tax_category", "single_line_text_field", "Product tax category"),
    ("Is Bundle", "paladio", "is_bundle", "boolean", "Indicates if product is a bundle"),
    ("Has Hazmat", "paladio", "has_hazmat", "boolean", "Indicates if product contains hazardous materials"),
    ("Product FAQs", "paladio", "faqs", "json", "AI-generated FAQs"),
]

_GRAPHQL_CREATE_METAFIELD = """
mutation metafieldDefinitionCreate($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition { id name }
    userErrors { field message }
  }
}
"""


def _create_paladio_metafields_bg(shop: str, token: str, api_version: str) -> None:
    """Create all paladio.* metafield definitions. Safe to call multiple times (skips existing)."""
    url = f"https://{shop}/admin/api/{api_version}/graphql.json"
    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}
    for name, namespace, key, mf_type, description in _PALADIO_METAFIELD_DEFINITIONS:
        try:
            resp = requests.post(url, headers=headers, json={
                "query": _GRAPHQL_CREATE_METAFIELD,
                "variables": {"definition": {
                    "name": name, "namespace": namespace, "key": key,
                    "type": mf_type, "description": description, "ownerType": "PRODUCT",
                }},
            }, timeout=15)
            resp.raise_for_status()
        except Exception:
            pass
        time.sleep(0.3)


oauth_bp = Blueprint("shopify_oauth", __name__, url_prefix="/oauth")


def _encode_oauth_state_inner(inner: str) -> str:
    return base64.urlsafe_b64encode(inner.encode()).decode().rstrip("=")


def _decode_oauth_state_param(state_param: str) -> str | None:
    if not state_param or not state_param.strip():
        return None
    s = state_param.strip()
    pad = (4 - len(s) % 4) % 4
    try:
        return base64.urlsafe_b64decode(s + "=" * pad).decode()
    except Exception:
        return None


def build_oauth_state(shop: str) -> str:
    shop = normalize_shop_domain(shop)
    ts = str(int(time.time()))
    msg = f"{shop}|{ts}"
    secret = get_oauth_state_signing_secret()
    if not secret:
        raise RuntimeError(
            "Set FLASK_SECRET_KEY (or SHOPIFY_API_SECRET) in .env next to api_server.py, then restart."
        )
    sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()[:32]
    inner = f"{msg}|{sig}"
    return _encode_oauth_state_inner(inner)


def _normalize_oauth_state_param(state_param: str | None) -> str | None:
    """
    Shopify redirects with `state` in the query string. Some proxies/browsers alter
    encoding; unquote and fix space→+ so base64 matches what we sent on /install.
    """
    if not state_param:
        return None
    s = state_param.strip()
    s = urllib.parse.unquote(s)
    s = s.replace(" ", "+")
    return s


def verify_oauth_state_detail(
    state_param: str | None, shop: str, *, force_verify: bool = False
) -> tuple[bool, str]:
    """
    Returns (ok, message). If not ok, message explains why (for debugging 400 pages).
    """
    if not force_verify and oauth_skip_state_verify():
        return True, "ok (OAUTH_SKIP_STATE_VERIFY)"

    shop = normalize_shop_domain(shop)
    state_param = _normalize_oauth_state_param(state_param)
    if not state_param:
        return False, "missing state"

    if "|" in state_param:
        raw = state_param
    else:
        decoded = _decode_oauth_state_param(state_param)
        raw = decoded if decoded and "|" in decoded else state_param

    if "|" not in raw:
        return False, "state has no valid payload (decode/parse)"
    parts = raw.rsplit("|", 2)
    if len(parts) != 3:
        return False, f"state has {len(parts)} parts, expected 3"
    shop_p, ts, sig = parts
    shop_p = normalize_shop_domain(shop_p)
    if shop_p != shop:
        return (
            False,
            "shop_mismatch: /oauth/install was started for a different shop than the OAuth "
            f"callback. state_shop={shop_p!r} callback_shop={shop!r}. Use the same store, e.g. "
            f"http://127.0.0.1:5001/oauth/install?shop={shop}",
        )
    try:
        if abs(int(time.time()) - int(ts)) > 3600:
            return False, "state older than 1 hour — start again from /oauth/install"
    except ValueError:
        return False, "invalid timestamp in state"
    secret = get_oauth_state_signing_secret()
    if not secret:
        return False, "no signing secret (FLASK_SECRET_KEY or SHOPIFY_API_SECRET)"
    msg = f"{shop_p}|{ts}"
    expected = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()[:32]
    if not hmac.compare_digest(sig, expected):
        return (
            False,
            "HMAC mismatch (wrong FLASK_SECRET_KEY between install and callback, or state was corrupted in transit). "
            "Restart api_server, run install again, or for local only set OAUTH_SKIP_STATE_VERIFY=true",
        )
    return True, "ok"


def verify_oauth_state(state_param: str | None, shop: str, *, force_verify: bool = False) -> bool:
    """force_verify=True ignores OAUTH_SKIP_STATE_VERIFY (for /oauth/self-test)."""
    ok, _ = verify_oauth_state_detail(state_param, shop, force_verify=force_verify)
    return ok


@oauth_bp.route("/install")
def oauth_install():
    shop_raw = (request.args.get("shop") or "").strip()
    shop = normalize_shop_domain(shop_raw)
    if not shop.endswith(".myshopify.com"):
        return jsonify({"error": "Missing or invalid shop (expected *.myshopify.com)"}), 400

    client_id = get_oauth_client_id()
    redirect_uri = get_oauth_redirect_uri()
    if not client_id or not redirect_uri:
        return jsonify(
            {
                "error": "Configure SHOPIFY_API_KEY and SHOPIFY_REDIRECT_URI",
            }
        ), 500

    try:
        state = build_oauth_state(shop)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    params = {
        "client_id": client_id,
        "scope": get_scopes(),
        "redirect_uri": redirect_uri,
        "state": state,
    }
    auth_url = f"https://{shop}/admin/oauth/authorize?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@oauth_bp.route("/callback")
def oauth_callback():
    shop_raw = request.args.get("shop") or ""
    shop = normalize_shop_domain(shop_raw)
    code = request.args.get("code")
    state = request.args.get("state")
    err = request.args.get("error")

    if err:
        return (
            _callback_page(
                ok=False,
                title="OAuth error",
                body=request.args.get("error_description") or err,
            ),
            400,
        )

    if not shop.endswith(".myshopify.com") or not code:
        return (
            _callback_page(
                ok=False,
                title="Missing parameters",
                body=f"shop={shop_raw!r} code={'set' if code else 'missing'}",
            ),
            400,
        )

    st_ok, st_reason = verify_oauth_state_detail(state, shop)
    if not st_ok:
        decoded = _decode_oauth_state_param(state or "") if state and "|" not in state else None
        hint = (
            "\n\nOther tips:\n"
            "1) /oauth/self-test — if build_verify_ok is false, fix FLASK_SECRET_KEY.\n"
            "2) Local only: OAUTH_SKIP_STATE_VERIFY=true in .env (never in production).\n"
            "3) Use 127.0.0.1 consistently in redirect URI and in the browser (not localhost).\n"
            "4) Start install and finish within one hour, same browser session."
        )
        return (
            _callback_page(
                ok=False,
                title="Invalid OAuth state",
                body=(
                    f"Reason: {st_reason}\n\n"
                    f"shop_param={shop_raw!r} normalized={shop!r}\n"
                    f"state_len={len(state or '')}\n"
                    f"decoded_ok={bool(decoded and '|' in decoded)}"
                    f"{hint}"
                ),
            ),
            400,
        )

    client_id = get_oauth_client_id()
    client_secret = get_oauth_client_secret()
    redirect_uri = get_oauth_redirect_uri()
    if not all([client_id, client_secret, redirect_uri]):
        return jsonify({"error": "OAuth client not fully configured"}), 500

    token_url = f"https://{shop}/admin/oauth/access_token"
    resp = requests.post(
        token_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        },
        headers={"Accept": "application/json"},
        timeout=30,
    )
    if resp.status_code >= 400:
        return (
            _callback_page(
                ok=False,
                title="Token exchange failed",
                body=resp.text[:800],
            ),
            resp.status_code,
        )

    data = resp.json()
    access_token = data.get("access_token")
    if not access_token:
        return _callback_page(ok=False, title="No access token", body=str(data)[:500]), 502

    refresh_token = data.get("refresh_token")
    expires_in = data.get("expires_in")

    try:
        save_token(shop, access_token, refresh_token=refresh_token, expires_in=expires_in)
    except Exception as e:
        return (
            _callback_page(
                ok=False,
                title="Could not save token",
                body=str(e),
            ),
            500,
        )

    # Create paladio.* metafield definitions in background (safe to re-run, skips existing)
    threading.Thread(
        target=_create_paladio_metafields_bg,
        args=(shop, access_token, get_api_version()),
        daemon=True,
    ).start()

    # Redirect merchant into the embedded app UI
    shop_name = shop.replace(".myshopify.com", "")
    client_id = get_oauth_client_id()
    app_url = f"https://admin.shopify.com/store/{shop_name}/apps/{client_id}"
    return redirect(app_url)


def _callback_page(ok: bool, title: str, body: str) -> str:
    color = "#008060" if ok else "#d82c0d"
    safe_title = html.escape(title)
    safe_body = html.escape(body)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{safe_title}</title></head>
<body style="font-family: system-ui; padding: 2rem; max-width: 560px;">
  <h1 style="color: {color};">{safe_title}</h1>
  <pre style="white-space: pre-wrap; background: #f6f6f7; padding: 1rem; border-radius: 8px;">{safe_body}</pre>
</body></html>"""


@oauth_bp.route("/scopes")
def oauth_scopes_documentation():
    return jsonify({"scopes": get_scopes().split(","), "api_version": get_api_version()})


@oauth_bp.route("/self-test")
def oauth_self_test():
    """Verify HMAC state signing works (same process as real OAuth)."""
    shop = "test-shop.myshopify.com"
    try:
        st = build_oauth_state(shop)
        ok = verify_oauth_state(st, shop, force_verify=True)
        skip = oauth_skip_state_verify()
        secret_set = bool(get_oauth_state_signing_secret())
        return jsonify(
            {
                "build_verify_ok": ok,
                "skip_state_verify_env": skip,
                "signing_secret_configured": secret_set,
                "shop": shop,
            }
        )
    except RuntimeError as e:
        return jsonify({"error": str(e), "build_verify_ok": False}), 500
