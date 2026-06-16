#!/usr/bin/env python3
"""
Show before/after comparison of enriched products in Shopify
"""

import requests
import json

from _config import STORE_URL, ACCESS_TOKEN, API_VERSION

# Check both paladio (current) and sanio (legacy) namespaces
ENRICHED_NAMESPACES = ('paladio', 'sanio')

def get_product_with_metafields(product_id):
    """Fetch a product with all its metafields."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        product = response.json().get('product', {})
        
        meta_url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
        meta_response = requests.get(meta_url, headers=headers, timeout=30)
        meta_response.raise_for_status()
        metafields = meta_response.json().get('metafields', [])
        
        enriched_metafields = [mf for mf in metafields if mf['namespace'] in ENRICHED_NAMESPACES]
        
        return product, enriched_metafields
        
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        return None, []

def get_all_enriched_products():
    """Get all products that have paladio or sanio metafields."""
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json?limit=250"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        products = response.json().get('products', [])
        
        enriched = []
        
        print("🔍 Checking for enriched products...")
        for product in products:
            product_id = product['id']
            
            meta_url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
            meta_response = requests.get(meta_url, headers=headers, timeout=30)
            
            if meta_response.status_code == 200:
                metafields = meta_response.json().get('metafields', [])
                enriched_mf = [mf for mf in metafields if mf['namespace'] in ENRICHED_NAMESPACES]
                
                if enriched_mf:
                    enriched.append((product, enriched_mf))
        
        return enriched
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def display_before_after(product, metafields):
    """Display before/after for a product."""
    print(f"\n{'='*80}")
    print(f"PRODUCT: {product['title']}")
    print(f"{'='*80}")
    
    print(f"\n📦 BEFORE (Original):")
    print(f"   Title: {product['title']}")
    print(f"   Description: {product['body_html'][:100] if product.get('body_html') else 'None'}...")
    print(f"   Product Type: {product.get('product_type', 'None')}")
    print(f"   Vendor: {product.get('vendor', 'None')}")
    
    print(f"\n✨ AFTER (Enriched Metafields):")
    for mf in metafields:
        key = mf['key']
        value = mf['value']
        
        if len(str(value)) > 100:
            value_display = str(value)[:100] + "..."
        else:
            value_display = value
        
        print(f"   {mf['namespace']}.{key}: {value_display}")

def main():
    print(f"\n{'='*80}")
    print("BEFORE & AFTER - Enriched Products Comparison")
    print(f"{'='*80}\n")
    
    enriched_products = get_all_enriched_products()
    
    if not enriched_products:
        print("\n❌ No enriched products found!")
        print("   Run the writeback script first: python3 writeback_50_products.py\n")
        return
    
    print(f"\n✅ Found {len(enriched_products)} enriched products!\n")
    
    for product, metafields in enriched_products:
        display_before_after(product, metafields)
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total enriched products: {len(enriched_products)}")
    
    metafield_counts = {}
    for _, metafields in enriched_products:
        for mf in metafields:
            key = f"{mf['namespace']}.{mf['key']}"
            metafield_counts[key] = metafield_counts.get(key, 0) + 1
    
    print(f"\nMetafield breakdown:")
    for key, count in sorted(metafield_counts.items()):
        print(f"  - {key}: {count} products")
    
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
