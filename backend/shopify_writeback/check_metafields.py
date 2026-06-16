#!/usr/bin/env python3
"""
Quick script to check if metafields were written to a specific product
"""
import requests
import json

from _config import STORE_URL, ACCESS_TOKEN, API_VERSION

# Check both paladio (current) and sanio (legacy) namespaces
ENRICHED_NAMESPACES = ('paladio', 'sanio')

def check_product_metafields(product_title_search):
    """Check metafields for a specific product"""
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json"
    headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}
    params = {"limit": 250}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    products = response.json()['products']
    
    matching_product = None
    for product in products:
        if product_title_search.lower() in product['title'].lower():
            matching_product = product
            break
    
    if not matching_product:
        print(f"❌ Product not found: {product_title_search}")
        return
    
    print(f"\n✅ Found product: {matching_product['title']}")
    print(f"   Product ID: {matching_product['id']}")
    
    metafields_url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{matching_product['id']}/metafields.json"
    
    response = requests.get(metafields_url, headers=headers)
    response.raise_for_status()
    metafields = response.json()['metafields']
    
    print(f"\n📦 Total metafields: {len(metafields)}")
    
    enriched_metafields = [m for m in metafields if m['namespace'] in ENRICHED_NAMESPACES]
    
    if enriched_metafields:
        print(f"\n✨ Enriched Data ({len(enriched_metafields)} fields):")
        for mf in enriched_metafields:
            value = mf['value']
            if len(value) > 100:
                value = value[:100] + "..."
            print(f"\n   {mf['namespace']}.{mf['key']}:")
            print(f"   Type: {mf['type']}")
            print(f"   Value: {value}")
    else:
        print("\n❌ No paladio/sanio metafields found!")
        print("\nAll metafield namespaces found:")
        for mf in metafields:
            print(f"   - {mf['namespace']}.{mf['key']}")

if __name__ == "__main__":
    check_product_metafields("Maryland Baby Swaddle")
