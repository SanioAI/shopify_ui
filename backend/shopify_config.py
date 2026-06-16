"""
Shopify app configuration from environment (no secrets in source).

OAuth install URL scopes: set SHOPIFY_SCOPES to the minimal set your app needs.
Default matches product + listing access used by catalog enrichment.
"""
from __future__ import annotations

import os
from pathlib import Path

# Load .env next to this file so FLASK_SECRET_KEY etc. load even if cwd is wrong.
_ENV_FILE = Path(__file__).resolve().parent / ".env"
try:
    from dotenv import load_dotenv

    load_dotenv(_ENV_FILE)
except ImportError:
    pass


def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()


def get_api_version() -> str:
    return _env("SHOPIFY_API_VERSION", "2026-01")


def get_scopes() -> str:
    # Minimal for typical catalog work: products read/write; listings if you sync sales channels.
    # Tighten in Partner Dashboard to match and remove unused scopes before App Store review.
    return _env(
        "SHOPIFY_SCOPES",
        "read_products,write_products,read_product_listings,write_product_listings",
    )


def get_oauth_client_id() -> str:
    return _env("SHOPIFY_API_KEY")


def get_oauth_client_secret() -> str:
    return _env("SHOPIFY_API_SECRET")


def get_oauth_redirect_uri() -> str:
    return _env("SHOPIFY_REDIRECT_URI")


def get_oauth_state_signing_secret() -> str:
    """Same secret used to sign OAuth state (must match between /install and /callback)."""
    return _env("FLASK_SECRET_KEY") or _env("SHOPIFY_API_SECRET")


def normalize_shop_domain(shop: str) -> str:
    """Shopify may send shop as full domain or handle only."""
    s = (shop or "").strip().lower()
    if not s:
        return ""
    if s.endswith(".myshopify.com"):
        return s
    if "." not in s:
        return f"{s}.myshopify.com"
    return s


def oauth_skip_state_verify() -> bool:
    """Local dev only. Never enable in production."""
    return _env("OAUTH_SKIP_STATE_VERIFY").lower() in ("1", "true", "yes")


def get_effective_shopify_credentials() -> tuple[str | None, str | None]:
    """
    Resolve store URL and Admin API access token.

    Order: SHOPIFY_STORE_URL + SHOPIFY_ACCESS_TOKEN (env),
    then encrypted token file from OAuth (shopify_token_store).
    """
    store = _env("SHOPIFY_STORE_URL")
    token = _env("SHOPIFY_ACCESS_TOKEN")
    if store and token:
        return store, token
    try:
        from shopify_token_store import load_first_shop_token, load_token_for_shop

        if store:
            t = load_token_for_shop(store)
            if t:
                return store, t
        s, t = load_first_shop_token()
        if s and t:
            return s, t
    except Exception:
        pass
    return None, None
