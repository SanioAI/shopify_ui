#!/usr/bin/env python3
"""
Update ACTUAL Shopify Product Fields with Enriched Data
- Updates Title, Description, and Product Type
- Also keeps metafields as backup
"""
import requests
import json
import time
import os
from typing import Dict, List, Optional

from _config import DATA_DIR, STORE_URL, ACCESS_TOKEN, API_VERSION

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_shopify_products() -> Dict[str, dict]:
    """Fetch all Shopify products and create a title->product map"""
    print("\n📥 Fetching Shopify products...")
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json"
    params = {"limit": 250}
    
    all_products = []
    
    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        all_products.extend(data['products'])
        
        # Check for pagination
        link_header = response.headers.get('Link', '')
        if 'rel="next"' in link_header:
            next_url = link_header.split(';')[0].strip('<>')
            url = next_url
            params = {}
        else:
            url = None
    
    print(f"✅ Found {len(all_products)} Shopify products")
    
    # Create title -> product map (normalized titles for matching)
    product_map = {}
    for product in all_products:
        # Store by normalized title for fuzzy matching
        normalized_title = product['title'].lower().strip()
        product_map[normalized_title] = product
    
    return product_map

def normalize_text(text: str) -> str:
    """Normalize text for matching"""
    return text.lower().strip()

def find_best_match(enriched_title: str, shopify_products: Dict[str, dict]) -> Optional[dict]:
    """Find best matching Shopify product for enriched title"""
    
    enriched_normalized = normalize_text(enriched_title)
    
    # Try exact match first
    if enriched_normalized in shopify_products:
        return shopify_products[enriched_normalized]
    
    # Try fuzzy match - extract key words
    stop_words = {'the', 'a', 'an', 'for', 'with', 'in', 'on', 'at', 'to', 'and', 'or', '-', '|', '&'}
    enriched_keywords = set(word for word in enriched_normalized.split() 
                           if word not in stop_words and len(word) > 2)
    
    best_match = None
    best_score = 0
    
    for shopify_title, product in shopify_products.items():
        shopify_keywords = set(word for word in shopify_title.split() 
                              if word not in stop_words and len(word) > 2)
        
        # Calculate overlap
        common_keywords = enriched_keywords & shopify_keywords
        if len(common_keywords) > 0:
            score = len(common_keywords) / max(len(enriched_keywords), len(shopify_keywords))
            
            if score > best_score:
                best_score = score
                best_match = product
    
    # Return if confidence is high enough
    if best_score > 0.4:
        return best_match
    
    return None

def update_product(product_id: int, enriched_data: dict) -> bool:
    """Update Shopify product with enriched data"""
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    
    # Prepare the update payload
    update_data = {
        "product": {
            "id": product_id,
            "title": enriched_data.get('optimized_title'),
            "body_html": f"<p>{enriched_data.get('optimized_description')}</p>",
            "product_type": enriched_data.get('category', '').split(' > ')[-1]  # Use last part of category
        }
    }
    
    try:
        response = requests.put(url, headers=HEADERS, json=update_data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def add_metafields(product_id: int, enriched_data: dict) -> bool:
    """Add enriched data as metafields (backup)"""
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
    
    metafields_to_add = [
        {
            "namespace": "paladio",
            "key": "category",
            "value": enriched_data.get('category', ''),
            "type": "single_line_text_field"
        },
        {
            "namespace": "paladio",
            "key": "optimized_title",
            "value": enriched_data.get('optimized_title', ''),
            "type": "single_line_text_field"
        },
        {
            "namespace": "paladio",
            "key": "optimized_description",
            "value": enriched_data.get('optimized_description', ''),
            "type": "multi_line_text_field"
        },
        {
            "namespace": "paladio",
            "key": "attributes",
            "value": json.dumps(enriched_data.get('attributes', {})),
            "type": "json"
        }
    ]
    
    success = True
    for metafield in metafields_to_add:
        try:
            response = requests.post(url, headers=HEADERS, json={"metafield": metafield})
            response.raise_for_status()
            time.sleep(0.3)  # Rate limiting
        except Exception as e:
            success = False
    
    return success

def main():
    print("=" * 80)
    print("UPDATE ACTUAL SHOPIFY PRODUCT FIELDS - 50 Products")
    print("=" * 80)
    
    # Load enriched data from shopify_app
    data_path = os.path.join(DATA_DIR, 'products (2).json')
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    enriched_products = data.get('items', [])
    print(f"\n📦 Loaded {len(enriched_products)} enriched products")
    
    # Get Shopify products
    shopify_products = get_shopify_products()
    
    print("\n" + "=" * 80)
    print("MATCHING & UPDATING PRODUCTS")
    print("=" * 80)
    
    matched = 0
    updated = 0
    failed = 0
    
    for i, enriched in enumerate(enriched_products, 1):
        if i % 10 == 1:
            print(f"\n[{i}/{len(enriched_products)}] Processing...")
        
        # Find matching Shopify product
        shopify_product = find_best_match(enriched.get('optimized_title', ''), shopify_products)
        
        if not shopify_product:
            print(f"  ⚠️ No match: {enriched.get('optimized_title', 'Unknown')[:60]}")
            failed += 1
            continue
        
        matched += 1
        
        # Update product fields
        success = update_product(shopify_product['id'], enriched)
        
        if success:
            # Also add metafields as backup
            add_metafields(shopify_product['id'], enriched)
            
            # Truncate title for display
            display_title = enriched.get('optimized_title', '')[:60] + '...'
            print(f"  ✅ {display_title}")
            updated += 1
            time.sleep(0.5)  # Rate limiting
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total enriched products: {len(enriched_products)}")
    print(f"Matched to Shopify: {matched}")
    print(f"Successfully updated: {updated}")
    print(f"Failed: {failed}")
    print("=" * 80)
    
    if updated > 0:
        print("\n✨ SUCCESS! Open your Shopify products to see the enriched data!")
        print("   - Title = Optimized Title")
        print("   - Description = Optimized Description")
        print("   - Product Type = Category")

if __name__ == "__main__":
    main()
