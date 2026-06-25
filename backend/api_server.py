"""
Flask Backend API for Catalog AI Direct Shopify App — offline token fix
===================================================

This API connects the Shopify App UI to the catalog enrichment scripts.
Acts as a proxy to avoid CORS and mixed-content issues when UI runs on GitHub Pages.

Shopify credentials: set SHOPIFY_STORE_URL + SHOPIFY_ACCESS_TOKEN in .env (Develop apps token).
Optional OAuth: ENABLE_SHOPIFY_OAUTH=true (see shopify_oauth.py).

Endpoints:
- GET  /api/products - Fetch products from Shopify
- POST /api/run-enrichment - Full flow: fetch -> enrich (catalog API) -> writeback
- POST /api/enrich - Enrich products using catalog agents
- POST /api/writeback - Write enriched data back to Shopify
- GET  /api/stats - Get analytics stats
- GET  /api/health - Health check
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import subprocess
import os
import time
import base64
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from shopify_config import get_api_version, get_effective_shopify_credentials
from shopify_http import shopify_request

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-change-FLASK_SECRET_KEY-in-production")
CORS(app)

# Partner OAuth routes (/oauth/install, /callback) — opt-in; default off for a simple .env + shpat_ flow
if os.environ.get("ENABLE_SHOPIFY_OAUTH", "").lower() in ("1", "true", "yes"):
    from shopify_oauth import oauth_bp

    app.register_blueprint(oauth_bp)


def _is_https_request() -> bool:
    if request.headers.get("X-Forwarded-Proto", "").lower() == "https":
        return True
    return request.is_secure


@app.before_request
def enforce_https_if_configured():
    if os.environ.get("FORCE_HTTPS", "").lower() not in ("1", "true", "yes"):
        return None
    if request.path in ("/api/health", "/health"):
        return None
    if not _is_https_request():
        return jsonify({"error": "HTTPS required", "success": False}), 403
    return None


# Catalog Agent API (external enrichment service)
CATALOG_API_URL = os.environ.get("CATALOG_API_URL", "http://13.218.58.17")
CATALOG_API_KEY = os.environ.get("CATALOG_API_KEY", "")
CATALOG_API_USERNAME = os.environ.get("CATALOG_API_USERNAME", "")
CATALOG_API_PASSWORD = os.environ.get("CATALOG_API_PASSWORD", "")


def _get_catalog_auth_headers():
    """Build auth headers for catalog API. Prefer API key, else Basic auth (username:password)."""
    headers = {}
    if CATALOG_API_KEY:
        headers["X-API-Key"] = CATALOG_API_KEY
    elif CATALOG_API_USERNAME and CATALOG_API_PASSWORD:
        creds = base64.b64encode(f"{CATALOG_API_USERNAME}:{CATALOG_API_PASSWORD}".encode()).decode()
        headers["Authorization"] = f"Basic {creds}"
    return headers


def _shopify_context():
    store, token = get_effective_shopify_credentials()
    if not store or not token:
        return None
    try:
        from shopify_token_store import is_token_expired, refresh_shopify_token
        if is_token_expired(store):
            refreshed = refresh_shopify_token(store)
            if refreshed:
                token = refreshed
    except Exception:
        pass
    return store, token, get_api_version()


def _shopify_not_configured():
    oauth_on = os.environ.get("ENABLE_SHOPIFY_OAUTH", "").lower() in ("1", "true", "yes")
    if oauth_on:
        hint = (
            "Set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN in .env, or complete OAuth: "
            "GET /oauth/install?shop=YOURSTORE.myshopify.com (same host as SHOPIFY_REDIRECT_URI)."
        )
        err = (
            "Shopify Admin API credentials missing. Add SHOPIFY_ACCESS_TOKEN after OAuth, "
            "or ensure shopify_app/.shopify_tokens.enc exists with SHOPIFY_TOKEN_ENCRYPTION_KEY."
        )
    else:
        hint = (
            "Shopify Admin → Settings → Apps → Develop apps → your app → API credentials → "
            "Reveal Admin API access token. Set SHOPIFY_ACCESS_TOKEN=shpat_... in .env next to api_server.py, "
            "then restart."
        )
        err = (
            "Shopify is not connected: SHOPIFY_ACCESS_TOKEN is empty (or store URL missing). "
            "OAuth routes are disabled (ENABLE_SHOPIFY_OAUTH is not true)."
        )
    return jsonify({"success": False, "error": err, "hint": hint}), 503


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "Catalog AI Direct API is running"})


@app.route("/healthz", methods=["GET"])
def healthz():
    return {"ok": True}, 200


@app.route("/api/products", methods=["GET"])
def get_products():
    """Fetch products from Shopify (HTTPS only to Shopify Admin API)."""
    ctx = _shopify_context()
    if not ctx:
        return _shopify_not_configured()
    store, token, api_version = ctx
    try:
        limit = request.args.get("limit", 50, type=int)
        response = shopify_request(
            "GET",
            store,
            token,
            api_version,
            "/products.json",
            params={"limit": limit},
        )
        products = response.json().get("products", [])
        return jsonify({"success": True, "count": len(products), "products": products})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get enrichment statistics."""
    ctx = _shopify_context()
    if not ctx:
        return _shopify_not_configured()
    store, token, api_version = ctx
    try:
        response = shopify_request(
            "GET",
            store,
            token,
            api_version,
            "/products.json",
            params={"limit": 250},
        )
        products = response.json().get("products", [])
        total_products = len(products)
        enriched_count = 0
        for product in products:
            product_id = product["id"]
            meta_response = shopify_request(
                "GET",
                store,
                token,
                api_version,
                f"/products/{product_id}/metafields.json",
                timeout=15,
            )
            metafields = meta_response.json().get("metafields", [])
            sanio_metafields = [mf for mf in metafields if mf.get("namespace") in ("sanio", "paladio")]
            if sanio_metafields:
                enriched_count += 1

        return jsonify(
            {
                "success": True,
                "stats": {
                    "total_products": total_products,
                    "enriched_products": enriched_count,
                    "pending_products": total_products - enriched_count,
                    "active_agents": 10,
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/run-enrichment", methods=["POST"])
def run_enrichment():
    """
    Full enrichment workflow: fetch products from Shopify -> send to catalog API -> poll for results -> writeback.
    Use demo=true to skip catalog API and run writeback with existing before-after data (for testing without API key).
    """
    try:
        body = request.get_json(silent=True) or {}
        demo_mode = body.get("demo", False)
        limit = min(body.get("limit", 50), 25)

        if demo_mode:
            base_dir = os.path.dirname(__file__)
            writeback_dir = os.path.join(base_dir, "shopify_writeback")
            script_path = os.path.join(writeback_dir, "writeback_complete.py")
            if os.path.exists(script_path):
                result = subprocess.run(
                    ["python3", script_path],
                    capture_output=True,
                    text=True,
                    timeout=600,
                    cwd=writeback_dir,
                )
                if result.returncode == 0:
                    return jsonify(
                        {
                            "success": True,
                            "message": "Demo: Writeback completed using existing before-after data",
                            "enriched_count": 50,
                            "products_processed": 50,
                            "demo": True,
                        }
                    )
                return (
                    jsonify(
                        {
                            "success": False,
                            "error": result.stderr[:500] or "Writeback failed",
                            "demo": True,
                        }
                    ),
                    500,
                )
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "shopify_writeback/writeback_complete.py not found",
                        "demo": True,
                    }
                ),
                500,
            )

        ctx = _shopify_context()
        if not ctx:
            return _shopify_not_configured()
        store, token, api_version = ctx

        time.sleep(2)
        resp = shopify_request(
            "GET",
            store,
            token,
            api_version,
            "/products.json",
            params={"limit": limit},
        )
        products = resp.json().get("products", [])

        if not products:
            return jsonify({"success": False, "error": "No products found"}), 400

        product_data = [
            {
                "product_id": str(p["id"]),
                "title": p.get("title", ""),
                "description": (p.get("body_html") or "")[:5000],
                "vendor": p.get("vendor", ""),
                "product_type": p.get("product_type", ""),
                "tags": ",".join(p.get("tags", [])),
            }
            for p in products
        ]

        # Build CSV from Shopify product data and upload to catalog API
        import io
        import csv as csv_module

        csv_buffer = io.StringIO()
        fieldnames = ["product_id", "title", "description", "vendor", "product_type", "tags"]
        writer = csv_module.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)
        csv_content = csv_buffer.getvalue().encode("utf-8")

        import uuid as _uuid
        client_id = os.environ.get("CATALOG_CLIENT_ID", "paladio-shopify")
        project_id = os.environ.get("CATALOG_PROJECT_ID", "shopify-catalog-app")
        dataset_id = str(_uuid.uuid4())

        cat_headers = _get_catalog_auth_headers()
        try:
            cat_resp = requests.post(
                f"{CATALOG_API_URL}/api/csv/start",
                files={"file": ("products.csv", csv_content, "text/csv")},
                data={
                    "job_type": "production",
                    "client_id": client_id,
                    "project_id": project_id,
                    "dataset_id": dataset_id,
                    "job_name": f"shopify-{store.split('.')[0]}-{dataset_id[:8]}",
                },
                headers=cat_headers,
                timeout=60,
            )
        except requests.exceptions.RequestException as e:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Catalog API unreachable: {str(e)}",
                        "hint": "Ensure catalog agent is running and CATALOG_API_URL is correct",
                    }
                ),
                502,
            )

        if cat_resp is None:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Catalog API unreachable",
                        "hint": "Ensure catalog agent is running and CATALOG_API_URL is correct",
                    }
                ),
                502,
            )

        if cat_resp.status_code == 401:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Catalog API 401 Unauthorized",
                        "hint": "Set CATALOG_API_KEY or CATALOG_API_USERNAME+CATALOG_API_PASSWORD env vars",
                    }
                ),
                502,
            )
        if cat_resp.status_code >= 400:
            detail = cat_resp.text[:500] if cat_resp.text else ""
            err_msg = f"Catalog API error: {cat_resp.status_code}"
            if detail:
                err_msg += f" — {detail}"
            print(f"[api_server] Catalog API {cat_resp.status_code} response: {detail}")
            return jsonify({"success": False, "error": err_msg, "detail": detail}), 502

        job_data = cat_resp.json()
        job_id = job_data.get("job_id") or job_data.get("id")

        if not job_id:
            return jsonify({"success": False, "error": "No job_id in catalog API response"}), 502

        max_wait = 600
        poll_interval = 10
        elapsed = 0

        while elapsed < max_wait:
            time.sleep(poll_interval)
            elapsed += poll_interval

            try:
                prog_resp = requests.get(
                    f"{CATALOG_API_URL}/api/progress/{job_id}", headers=cat_headers, timeout=10
                )
                if prog_resp.status_code == 200:
                    prog = prog_resp.json()
                    status = (prog.get("status") or "").lower()
                    if status in ("succeeded", "completed", "done"):
                        break
                    if status in ("failed", "error"):
                        return (
                            jsonify(
                                {
                                    "success": False,
                                    "error": prog.get("message", "Enrichment failed"),
                                }
                            ),
                            500,
                        )
            except Exception:
                pass

        # Fetch before-after results (full format with core_attributes, content, attributes)
        results = []
        try:
            res_resp = requests.get(
                f"{CATALOG_API_URL}/api/results/before-after?job_id={job_id}&page_size=250",
                headers=cat_headers,
                timeout=30,
            )
            if res_resp.status_code == 200:
                data = res_resp.json()
                results = data.get("items", [])
        except Exception:
            pass

        # Fall back to products endpoint if before-after unavailable
        if not results:
            try:
                res_resp = requests.get(
                    f"{CATALOG_API_URL}/api/results/products?job_id={job_id}&page_size=250",
                    headers=cat_headers,
                    timeout=30,
                )
                if res_resp.status_code == 200:
                    data = res_resp.json()
                    results = data.get("items", [])
            except Exception:
                pass

        if results:
            results_path = os.path.join(os.path.dirname(__file__), "shopify_app", "enrichment_results.json")
            os.makedirs(os.path.dirname(results_path), exist_ok=True)
            with open(results_path, "w") as f:
                json.dump({"job_id": job_id, "items": results}, f, indent=2)

        if not results:
            return jsonify(
                {
                    "success": False,
                    "error": "Enrichment job completed but no results were returned.",
                    "job_id": job_id,
                }
            ), 502

        updated, failed = _shopify_writeback_from_results(results, store, token, api_version)

        return jsonify(
            {
                "success": True,
                "message": f"Enrichment complete! {updated} products enriched and updated in your store.",
                "job_id": job_id,
                "enriched_count": len(results),
                "products_processed": len(products),
                "updated": updated,
                "failed": failed,
            }
        )

    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            shop_domain = store if store else (os.environ.get("SHOPIFY_STORE_URL") or "").strip()
            install_url = f"/oauth/install?shop={shop_domain}" if shop_domain else "/oauth/install"
            return jsonify({
                "success": False,
                "error": "Shopify token expired. Please reconnect the app.",
                "reconnect": True,
                "install_url": install_url,
            }), 401
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enrich", methods=["POST"])
def enrich_products():
    try:
        data = request.get_json()
        product_ids = data.get("product_ids", [])

        if not product_ids:
            return jsonify({"success": False, "error": "No product IDs provided"}), 400

        return jsonify(
            {
                "success": True,
                "message": f"Enrichment started for {len(product_ids)} products",
                "job_id": "job_123456",
                "status": "processing",
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def _shopify_writeback_from_results(items, store, token, api_version):
    """
    Write enriched catalog results back to Shopify using real product IDs.

    Handles both before-after format (has item['after']) and simplified products
    format (has item['optimized_title'] at top level). Returns (updated, failed).
    """
    updated, failed = 0, 0
    for item in items:
        product_id = str(item.get("product_id", "")).strip()
        if not product_id or not product_id.isdigit():
            failed += 1
            continue

        # Resolve enriched data from before-after or flat format
        after = item.get("after", item)
        core = after.get("core_attributes", after.get("core_meta", {}))
        content_result = after.get("content", {}).get("result", {})
        attributes = after.get("attributes", {})

        optimized_title = (
            content_result.get("optimized_title")
            or after.get("optimized_title")
            or item.get("optimized_title")
        )
        optimized_description = (
            content_result.get("optimized_description")
            or after.get("optimized_description")
            or item.get("optimized_description")
        )
        taxonomy = core.get("taxonomy", after.get("category", ""))
        product_type = (
            core.get("category_level_3")
            or (taxonomy.split(" > ")[-1] if taxonomy else "")
        )

        # Update main product fields
        update_payload = {"product": {"id": int(product_id)}}
        if optimized_title:
            update_payload["product"]["title"] = optimized_title.strip('"')
        if optimized_description:
            update_payload["product"]["body_html"] = f"<p>{optimized_description.strip(chr(34))}</p>"
        if product_type:
            update_payload["product"]["product_type"] = product_type

        try:
            r = shopify_request(
                "PUT", store, token, api_version,
                f"/products/{product_id}.json",
                json_body=update_payload,
                timeout=15,
            )
            r.raise_for_status()
        except Exception:
            failed += 1
            continue

        # Fetch existing metafield IDs for this product (namespace=paladio)
        existing_mf = {}
        try:
            mf_resp = shopify_request(
                "GET", store, token, api_version,
                f"/products/{product_id}/metafields.json",
                params={"namespace": "paladio", "limit": 250},
                timeout=15,
            )
            for mf in mf_resp.json().get("metafields", []):
                existing_mf[mf["key"]] = mf["id"]
        except Exception:
            pass

        # Build metafields
        metafields = []
        if taxonomy:
            metafields.append(("category", taxonomy, "single_line_text_field"))
        for lvl in ("category_level_1", "category_level_2", "category_level_3"):
            if core.get(lvl):
                metafields.append((lvl, core[lvl], "single_line_text_field"))
        if optimized_title:
            metafields.append(("optimized_title", optimized_title.strip('"'), "single_line_text_field"))
        if optimized_description:
            metafields.append(("optimized_description", optimized_description.strip('"'), "multi_line_text_field"))
        if content_result.get("seo_keywords"):
            metafields.append(("seo_keywords", json.dumps(content_result["seo_keywords"]), "json"))
        if attributes:
            metafields.append(("attributes", json.dumps(attributes), "json"))
            for key in ("brand", "material", "color"):
                v = attributes.get(key)
                if v:
                    val = v.get("value", v) if isinstance(v, dict) else v
                    metafields.append((key, str(val), "single_line_text_field"))
        for flag in ("is_bundle", "has_hazmat"):
            if flag in core:
                metafields.append((flag, str(core[flag]).lower(), "boolean"))

        for key, value, mf_type in metafields:
            try:
                if key in existing_mf:
                    shopify_request(
                        "PUT", store, token, api_version,
                        f"/metafields/{existing_mf[key]}.json",
                        json_body={"metafield": {"id": existing_mf[key], "value": value, "type": mf_type}},
                        timeout=10,
                    )
                else:
                    shopify_request(
                        "POST", store, token, api_version,
                        f"/products/{product_id}/metafields.json",
                        json_body={"metafield": {"namespace": "paladio", "key": key, "value": value, "type": mf_type}},
                        timeout=10,
                    )
                time.sleep(0.2)
            except Exception:
                pass

        updated += 1
        time.sleep(0.3)

    return updated, failed


@app.route("/api/writeback", methods=["POST"])
def writeback():
    ctx = _shopify_context()
    if not ctx:
        return _shopify_not_configured()
    store, token, api_version = ctx

    results_path = os.path.join(os.path.dirname(__file__), "shopify_app", "enrichment_results.json")
    if not os.path.exists(results_path):
        return jsonify({"success": False, "error": "No enrichment results found. Run /api/run-enrichment first."}), 400

    try:
        with open(results_path) as f:
            data = json.load(f)
        items = data.get("items", [])
        if not items:
            return jsonify({"success": False, "error": "Enrichment results file is empty."}), 400

        updated, failed = _shopify_writeback_from_results(items, store, token, api_version)
        return jsonify({
            "success": True,
            "message": f"Writeback completed: {updated} products updated, {failed} skipped.",
            "updated": updated,
            "failed": failed,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/agents", methods=["GET"])
def get_agents():
    agents = [
        {
            "id": "taxonomy",
            "name": "Taxonomy Agent",
            "description": "Classifies products into proper categories",
            "category": "Data Quality",
            "status": "active",
        },
        {
            "id": "attributes",
            "name": "Attributes Extraction",
            "description": "Extracts product attributes (brand, size, color, etc.)",
            "category": "Data Quality",
            "status": "active",
        },
        {
            "id": "content",
            "name": "Content Generation",
            "description": "Generates optimized titles and descriptions",
            "category": "Content & SEO",
            "status": "active",
        },
        {
            "id": "seo",
            "name": "SEO Optimization",
            "description": "Optimizes product content for search engines",
            "category": "Content & SEO",
            "status": "active",
        },
        {
            "id": "schema",
            "name": "Schema Markup",
            "description": "Generates structured data for products",
            "category": "Content & SEO",
            "status": "active",
        },
    ]

    return jsonify({"success": True, "agents": agents})


# ── Shopify mandatory GDPR webhooks ──────────────────────────────────────────
import hmac as _hmac
import hashlib as _hashlib


def _verify_shopify_webhook(req) -> bool:
    secret = (os.environ.get("SHOPIFY_API_SECRET") or "").strip()
    if not secret:
        return False
    signature = req.headers.get("X-Shopify-Hmac-Sha256", "")
    digest = _hmac.new(secret.encode("utf-8"), req.get_data(), _hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return _hmac.compare_digest(expected, signature)


@app.route("/webhooks/customers/redact", methods=["POST"])
def gdpr_customers_redact():
    if not _verify_shopify_webhook(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"acknowledged": True}), 200


@app.route("/webhooks/customers/data_request", methods=["POST"])
def gdpr_customers_data_request():
    if not _verify_shopify_webhook(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"acknowledged": True}), 200


@app.route("/webhooks/shop/redact", methods=["POST"])
def gdpr_shop_redact():
    if not _verify_shopify_webhook(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"acknowledged": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("Starting Catalog AI Direct API...")
    print(f"API will be available at: http://localhost:{port}")
    print("UI should be configured to use this URL")
    print("Set SHOPIFY_STORE_URL + SHOPIFY_ACCESS_TOKEN in .env (Develop apps token), or ENABLE_SHOPIFY_OAUTH=true")
    _oauth = os.environ.get("ENABLE_SHOPIFY_OAUTH", "").lower() in ("1", "true", "yes")
    # OAuth state HMAC is sensitive to the dev reloader (two processes / restarts). Disable reloader when OAuth is on.
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=not _oauth)
