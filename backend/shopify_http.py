"""
Shopify Admin REST calls with 429 handling (Retry-After and exponential backoff).
All requests use HTTPS to *.myshopify.com.
"""
from __future__ import annotations

import random
import time
from typing import Any

import requests


def shopify_request(
    method: str,
    store_url: str,
    access_token: str,
    api_version: str,
    path: str,
    *,
    params: dict | None = None,
    json_body: Any = None,
    timeout: float = 30,
    max_retries: int = 6,
) -> requests.Response:
    """
    path must start with '/', e.g. '/products.json'.
    """
    if not path.startswith("/"):
        path = "/" + path
    url = f"https://{store_url}/admin/api/{api_version}{path}"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json",
    }
    last: requests.Response | None = None
    for attempt in range(max_retries):
        try:
            last = requests.request(
                method.upper(),
                url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=timeout,
            )
        except requests.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(min(2**attempt + random.uniform(0, 0.5), 60))
            continue

        if last.status_code == 429:
            ra = last.headers.get("Retry-After")
            if ra:
                try:
                    wait = float(ra)
                except ValueError:
                    wait = min(2**attempt + random.uniform(0, 1), 60)
            else:
                wait = min(2**attempt + random.uniform(0, 1), 60)
            time.sleep(wait)
            continue

        if last.status_code in (401, 403):
            err = requests.HTTPError(
                f"{last.status_code} {last.reason}: {last.text[:500]}",
                response=last,
            )
            raise err

        last.raise_for_status()
        return last

    if last is not None:
        last.raise_for_status()
    raise requests.HTTPError("Shopify request failed after retries")
