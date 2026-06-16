"""
Per-shop OAuth access tokens: Supabase (recommended for production) or encrypted local file.

Supabase (set both):
  SUPABASE_URL
  SUPABASE_SERVICE_ROLE_KEY  — use the service role only on the server; never in the browser.
  Create the table: run shopify_app/supabase_shopify_oauth_tokens.sql in the Supabase SQL editor.

File fallback (no Supabase env):
  SHOPIFY_TOKEN_ENCRYPTION_KEY  +  pip install cryptography
  Data file: shopify_app/.shopify_tokens.enc (gitignored)
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent / "shopify_app"
_TOKEN_FILE = _DATA_DIR / ".shopify_tokens.enc"
_TABLE = "shopify_oauth_tokens"

_supabase: Any = None


def _supabase_env_ok() -> bool:
    u = (os.environ.get("SUPABASE_URL") or "").strip()
    k = (os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
    return bool(u and k)


def _get_supabase():
    global _supabase
    if not _supabase_env_ok():
        return None
    if _supabase is not None:
        return _supabase
    try:
        from supabase import create_client
    except ImportError as e:
        raise RuntimeError(
            "Supabase is configured (SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY) but "
            "the supabase package is not installed. Run: pip install supabase"
        ) from e
    _supabase = create_client(
        os.environ["SUPABASE_URL"].strip(),
        os.environ["SUPABASE_SERVICE_ROLE_KEY"].strip(),
    )
    return _supabase


def _fernet():
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        return None
    key = os.environ.get("SHOPIFY_TOKEN_ENCRYPTION_KEY", "").strip()
    if not key:
        return None
    return Fernet(key.encode())


def _read_raw() -> dict[str, str]:
    f = _fernet()
    if not f or not _TOKEN_FILE.exists():
        return {}
    try:
        return json.loads(f.decrypt(_TOKEN_FILE.read_bytes()).decode())
    except Exception:
        return {}


def _write_raw(data: dict[str, str]) -> None:
    f = _fernet()
    if not f:
        raise RuntimeError(
            "Set SHOPIFY_TOKEN_ENCRYPTION_KEY and install cryptography to store OAuth tokens."
        )
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _TOKEN_FILE.write_bytes(f.encrypt(json.dumps(data).encode()))


def save_token(
    shop: str,
    token: str,
    refresh_token: str | None = None,
    expires_in: int | None = None,
) -> None:
    shop = shop.strip().lower()
    client = _get_supabase()
    if client is not None:
        ts = datetime.now(timezone.utc)
        row: dict[str, Any] = {
            "shop": shop,
            "access_token": token,
            "updated_at": ts.isoformat(),
        }
        if refresh_token:
            row["refresh_token"] = refresh_token
        if expires_in:
            row["expires_at"] = (ts + timedelta(seconds=int(expires_in))).isoformat()
        client.table(_TABLE).upsert(row).execute()
        return
    data = _read_raw()
    data[shop] = token
    _write_raw(data)


def load_token_for_shop(shop: str) -> str | None:
    shop = shop.strip().lower()
    client = _get_supabase()
    if client is not None:
        res = client.table(_TABLE).select("access_token").eq("shop", shop).limit(1).execute()
        rows = res.data or []
        if not rows:
            return None
        return rows[0].get("access_token")
    return _read_raw().get(shop)


def load_full_token_for_shop(shop: str) -> dict | None:
    """Return full token row: access_token, refresh_token, expires_at."""
    shop = shop.strip().lower()
    client = _get_supabase()
    if client is None:
        token = _read_raw().get(shop)
        return {"access_token": token} if token else None
    res = (
        client.table(_TABLE)
        .select("access_token, refresh_token, expires_at")
        .eq("shop", shop)
        .limit(1)
        .execute()
    )
    rows = res.data or []
    return rows[0] if rows else None


def load_first_shop_token() -> tuple[str | None, str | None]:
    client = _get_supabase()
    if client is not None:
        res = client.table(_TABLE).select("shop, access_token").order("updated_at", desc=True).limit(1).execute()
        rows = res.data or []
        if not rows:
            return None, None
        r = rows[0]
        return r.get("shop"), r.get("access_token")
    data = _read_raw()
    if not data:
        return None, None
    s = next(iter(data.keys()))
    return s, data[s]


def refresh_shopify_token(shop: str) -> str | None:
    """Exchange the stored refresh_token for a new access_token. Returns new token or None."""
    import requests as _requests

    row = load_full_token_for_shop(shop)
    if not row or not row.get("refresh_token"):
        return None

    client_id = (os.environ.get("SHOPIFY_API_KEY") or "").strip()
    client_secret = (os.environ.get("SHOPIFY_API_SECRET") or "").strip()
    if not client_id or not client_secret:
        return None

    try:
        resp = _requests.post(
            f"https://{shop}/admin/oauth/access_token",
            json={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": row["refresh_token"],
            },
            headers={"Accept": "application/json"},
            timeout=30,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        new_token = data.get("access_token")
        if new_token:
            save_token(
                shop,
                new_token,
                refresh_token=data.get("refresh_token"),
                expires_in=data.get("expires_in"),
            )
        return new_token
    except Exception:
        return None


def is_token_expired(shop: str) -> bool:
    """True if the stored token has an expires_at that is within 5 minutes of now."""
    row = load_full_token_for_shop(shop)
    if not row or not row.get("expires_at"):
        return False
    try:
        expires_at = datetime.fromisoformat(row["expires_at"].replace("Z", "+00:00"))
        return datetime.now(timezone.utc) >= expires_at - timedelta(minutes=5)
    except Exception:
        return False
