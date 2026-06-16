#!/usr/bin/env python3
"""
Write 50 enriched products from products (2).json to Shopify
- Updates main product fields: title, description, product type
- Writes all data to paladio metafields
"""

import requests
import json
import time
import os

from _config import DATA_DIR, STORE_URL, ACCESS_TOKEN, API_VERSION

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_shopify_products():
    """Fetch all products from Shopify."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json"
    params = {"limit": 250}
    all_products = []
    
    try:
        while url:
            response = requests.get(url, headers=HEADERS, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            all_products.extend(data.get('products', []))
            
            link = response.headers.get('Link', '')
            if 'rel="next"' in link:
                url = link.split(';')[0].strip('<>')
                params = {}
            else:
                url = None
        
        return {p['title'].lower(): p for p in all_products}
    except Exception as e:
        print(f"❌ Error fetching products: {e}")
        return {}

def find_best_match(enriched_title, shopify_products):
    """Find best matching Shopify product by keyword overlap."""
    enriched_lower = enriched_title.lower()
    
    stop_words = {'the', 'a', 'an', 'for', 'with', 'in', 'on', 'at', 'to', 'and', 'or', '-', '|', '&'}
    keywords = set(w for w in enriched_lower.split() if len(w) > 2 and w not in stop_words)
    
    best_match = None
    best_score = 0
    
    for shopify_title_lower, product in shopify_products.items():
        shopify_keywords = set(w for w in shopify_title_lower.split() if len(w) > 2 and w not in stop_words)
        common = keywords & shopify_keywords
        if len(common) > 0:
            score = len(common) / max(len(keywords), len(shopify_keywords))
            if score > best_score:
                best_score = score
                best_match = product
    
    return best_match if best_score > 0.4 else None

def update_product_main_fields(product_id, enriched):
    """Update main product title, description, and product type."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    
    product_type = enriched.get('category', '').split(' > ')[-1] if enriched.get('category') else ''
    
    payload = {
        "product": {
            "id": product_id,
            "title": enriched.get('optimized_title', ''),
            "body_html": f"<p>{enriched.get('optimized_description', '')}</p>",
            "product_type": product_type
        }
    }
    
    try:
        response = requests.put(url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"   ❌ Update error: {e}")
        return False

def write_metafield(product_id, namespace, key, value, value_type="single_line_text_field"):
    """Write a metafield to Shopify."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
    
    payload = {
        "metafield": {
            "namespace": namespace,
            "key": key,
            "value": value,
            "type": value_type
        }
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        return False

def write_metafields(product_id, enriched):
    """Write all enriched data as paladio metafields."""
    written = 0
    
    if enriched.get('category'):
        if write_metafield(product_id, "paladio", "category", enriched["category"]):
            written += 1
        time.sleep(0.3)
    
    if enriched.get('optimized_title'):
        if write_metafield(product_id, "paladio", "optimized_title", enriched["optimized_title"]):
            written += 1
        time.sleep(0.3)
    
    if enriched.get('optimized_description'):
        if write_metafield(product_id, "paladio", "optimized_description", enriched["optimized_description"], "multi_line_text_field"):
            written += 1
        time.sleep(0.3)
    
    if enriched.get('attributes'):
        attrs_json = json.dumps(enriched["attributes"])
        if write_metafield(product_id, "paladio", "attributes", attrs_json, "json"):
            written += 1
        time.sleep(0.3)
    
    return written

def main():
    print(f"\n{'='*80}")
    print("SHOPIFY WRITEBACK - 50 Products (Title + Metafields)")
    print(f"{'='*80}\n")
    
    # Load enriched data from shopify_app
    data_path = os.path.join(DATA_DIR, 'products (2).json')
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    enriched_products = data.get('items', [])
    print(f"📦 Loaded {len(enriched_products)} enriched products\n")
    
    # Fetch Shopify products
    print("📥 Fetching Shopify products...")
    shopify_products = get_shopify_products()
    print(f"✅ Found {len(shopify_products)} Shopify products\n")
    
    print(f"{'='*80}")
    print("MATCHING & WRITING BACK")
    print(f"{'='*80}\n")
    
    matched_count = 0
    success_count = 0
    
    for i, enriched in enumerate(enriched_products, 1):
        enriched_title = enriched.get('optimized_title', 'Unknown')
        
        if i % 10 == 1 or i == len(enriched_products):
            print(f"\n[{i}/{len(enriched_products)}] Processing...")
        
        match = find_best_match(enriched_title, shopify_products)
        
        if not match:
            print(f"  ❌ No match: {enriched_title[:55]}...")
            continue
        
        matched_count += 1
        product_id = match['id']
        
        # 1. Update main product fields (title, description, product type)
        main_ok = update_product_main_fields(product_id, enriched)
        time.sleep(0.5)
        
        # 2. Write metafields
        metafield_count = write_metafields(product_id, enriched)
        time.sleep(0.5)
        
        if main_ok and metafield_count > 0:
            success_count += 1
            display = enriched_title[:55] + '...' if len(enriched_title) > 55 else enriched_title
            print(f"  ✅ {display} (title + {metafield_count} metafields)")
        else:
            print(f"  ⚠️ Partial: {enriched_title[:50]}...")
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total enriched products: {len(enriched_products)}")
    print(f"Matched to Shopify: {matched_count}")
    print(f"Successfully written: {success_count}")
    print(f"Failed to match: {len(enriched_products) - matched_count}")
    print(f"{'='*80}\n")
    
    if success_count > 0:
        print("✨ Done! Products updated with:")
        print("   • Title = optimized title")
        print("   • Description = optimized description")
        print("   • Product type = category")
        print("   • Metafields: paladio.category, paladio.optimized_title, paladio.optimized_description, paladio.attributes")

if __name__ == "__main__":
    main()
