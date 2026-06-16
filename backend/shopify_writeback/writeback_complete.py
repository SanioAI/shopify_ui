#!/usr/bin/env python3
"""
Complete Enriched Data Writeback to Shopify
- Updates product title, description, and product type
- Writes ALL enriched fields as metafields (category, SEO, attributes, FAQs, tax, etc.)
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
    
    # Create title -> product map
    product_map = {}
    for product in all_products:
        normalized_title = product['title'].lower().strip()
        product_map[normalized_title] = product
    
    return product_map

def normalize_text(text: str) -> str:
    """Normalize text for matching"""
    return text.lower().strip()

def find_best_match(original_title: str, shopify_products: Dict[str, dict]) -> Optional[dict]:
    """Find matching Shopify product by original title"""
    
    title_normalized = normalize_text(original_title)
    
    # Try exact match
    if title_normalized in shopify_products:
        return shopify_products[title_normalized]
    
    # Fuzzy match
    stop_words = {'the', 'a', 'an', 'for', 'with', 'in', 'on', 'at', 'to', 'and', 'or', '-', '|', '&'}
    keywords = set(word for word in title_normalized.split() 
                  if word not in stop_words and len(word) > 2)
    
    best_match = None
    best_score = 0
    
    for shopify_title, product in shopify_products.items():
        shopify_keywords = set(word for word in shopify_title.split() 
                              if word not in stop_words and len(word) > 2)
        
        common = keywords & shopify_keywords
        if len(common) > 0:
            score = len(common) / max(len(keywords), len(shopify_keywords))
            
            if score > best_score:
                best_score = score
                best_match = product
    
    if best_score > 0.5:
        return best_match
    
    return None

def update_product_main_fields(product_id: int, enriched_data: dict) -> bool:
    """Update main product fields (title, description, type)"""
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    
    content_result = enriched_data.get('content', {}).get('result', {})
    core_attributes = enriched_data.get('core_attributes', {})
    
    optimized_title = content_result.get('optimized_title', enriched_data.get('title'))
    optimized_description = content_result.get('optimized_description', '')
    
    # Use category level 3 as product type
    product_type = core_attributes.get('category_level_3', 
                                      core_attributes.get('taxonomy', '').split(' > ')[-1] if core_attributes.get('taxonomy') else '')
    
    update_data = {
        "product": {
            "id": product_id,
            "title": optimized_title,
            "body_html": f"<p>{optimized_description}</p>",
            "product_type": product_type
        }
    }
    
    try:
        response = requests.put(url, headers=HEADERS, json=update_data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"   ❌ Error updating main fields: {str(e)}")
        return False

def add_all_metafields(product_id: int, enriched_data: dict) -> int:
    """Add ALL enriched data as metafields"""
    
    url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
    
    core_attributes = enriched_data.get('core_attributes', {})
    attributes = enriched_data.get('attributes', {})
    tax_compliance = enriched_data.get('tax_compliance', {})
    content_result = enriched_data.get('content', {}).get('result', {})
    
    metafields = []
    
    # 1. CATEGORY & TAXONOMY
    if core_attributes.get('taxonomy'):
        metafields.append({
            "namespace": "paladio",
            "key": "category",
            "value": core_attributes['taxonomy'],
            "type": "single_line_text_field"
        })
    
    if core_attributes.get('category_level_1'):
        metafields.append({
            "namespace": "paladio",
            "key": "category_level_1",
            "value": core_attributes['category_level_1'],
            "type": "single_line_text_field"
        })
    
    if core_attributes.get('category_level_2'):
        metafields.append({
            "namespace": "paladio",
            "key": "category_level_2",
            "value": core_attributes['category_level_2'],
            "type": "single_line_text_field"
        })
    
    if core_attributes.get('category_level_3'):
        metafields.append({
            "namespace": "paladio",
            "key": "category_level_3",
            "value": core_attributes['category_level_3'],
            "type": "single_line_text_field"
        })
    
    # 2. OPTIMIZED CONTENT
    if content_result.get('optimized_title'):
        metafields.append({
            "namespace": "paladio",
            "key": "optimized_title",
            "value": content_result['optimized_title'],
            "type": "single_line_text_field"
        })
    
    if content_result.get('optimized_description'):
        metafields.append({
            "namespace": "paladio",
            "key": "optimized_description",
            "value": content_result['optimized_description'],
            "type": "multi_line_text_field"
        })
    
    # 3. SEO FIELDS
    if content_result.get('seo_keywords'):
        metafields.append({
            "namespace": "paladio",
            "key": "seo_keywords",
            "value": json.dumps(content_result['seo_keywords']),
            "type": "json"
        })
    
    if content_result.get('title_keywords'):
        metafields.append({
            "namespace": "paladio",
            "key": "title_keywords",
            "value": json.dumps(content_result['title_keywords']),
            "type": "json"
        })
    
    if content_result.get('description_sections'):
        metafields.append({
            "namespace": "paladio",
            "key": "description_sections",
            "value": json.dumps(content_result['description_sections']),
            "type": "json"
        })
    
    # 4. PRODUCT ATTRIBUTES
    if attributes:
        metafields.append({
            "namespace": "paladio",
            "key": "attributes",
            "value": json.dumps(attributes),
            "type": "json"
        })
        
        # Individual attribute fields
        if attributes.get('brand'):
            metafields.append({
                "namespace": "paladio",
                "key": "brand",
                "value": str(attributes['brand']),
                "type": "single_line_text_field"
            })
        
        if attributes.get('material'):
            metafields.append({
                "namespace": "paladio",
                "key": "material",
                "value": str(attributes['material']),
                "type": "single_line_text_field"
            })
    
    # 5. TAX COMPLIANCE
    if tax_compliance.get('avalara_tax_code'):
        metafields.append({
            "namespace": "paladio",
            "key": "avalara_tax_code",
            "value": tax_compliance['avalara_tax_code'],
            "type": "single_line_text_field"
        })
    
    if tax_compliance.get('tax_category'):
        metafields.append({
            "namespace": "paladio",
            "key": "tax_category",
            "value": tax_compliance['tax_category'],
            "type": "single_line_text_field"
        })
    
    # 6. PRODUCT FLAGS
    if 'is_bundle' in core_attributes:
        metafields.append({
            "namespace": "paladio",
            "key": "is_bundle",
            "value": str(core_attributes['is_bundle']).lower(),
            "type": "boolean"
        })
    
    if 'has_hazmat' in core_attributes:
        metafields.append({
            "namespace": "paladio",
            "key": "has_hazmat",
            "value": str(core_attributes['has_hazmat']).lower(),
            "type": "boolean"
        })
    
    # 7. FAQs
    if content_result.get('faqs'):
        metafields.append({
            "namespace": "paladio",
            "key": "faqs",
            "value": json.dumps(content_result['faqs']),
            "type": "json"
        })
    
    # Write all metafields
    success_count = 0
    for metafield in metafields:
        try:
            response = requests.post(url, headers=HEADERS, json={"metafield": metafield})
            response.raise_for_status()
            success_count += 1
            time.sleep(0.3)  # Rate limiting
        except Exception as e:
            pass  # Continue with other metafields
    
    return success_count

def main():
    print("=" * 80)
    print("COMPLETE ENRICHED DATA WRITEBACK - 50 Products")
    print("=" * 80)
    
    # Load enriched data from before-after JSON (in shopify_app)
    data_path = os.path.join(DATA_DIR, 'before-after (1).json')
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    enriched_products = data.get('items', [])
    print(f"\n📦 Loaded {len(enriched_products)} enriched products")
    
    # Get Shopify products
    shopify_products = get_shopify_products()
    
    print("\n" + "=" * 80)
    print("MATCHING & WRITING ALL ENRICHED DATA")
    print("=" * 80)
    
    matched = 0
    updated = 0
    failed = 0
    total_metafields = 0
    
    for i, item in enumerate(enriched_products, 1):
        if i % 10 == 1:
            print(f"\n[{i}/{len(enriched_products)}] Processing...")
        
        # Get original title from "before" data
        original_title = item.get('before', {}).get('title', '')
        enriched_data = item.get('after', {})
        
        if not original_title:
            print(f"  ⚠️ No original title found")
            failed += 1
            continue
        
        # Find matching Shopify product
        shopify_product = find_best_match(original_title, shopify_products)
        
        if not shopify_product:
            display_title = original_title[:60] + '...' if len(original_title) > 60 else original_title
            print(f"  ⚠️ No match: {display_title}")
            failed += 1
            continue
        
        matched += 1
        
        # Update main product fields
        main_success = update_product_main_fields(shopify_product['id'], enriched_data)
        
        # Add ALL metafields
        metafield_count = add_all_metafields(shopify_product['id'], enriched_data)
        total_metafields += metafield_count
        
        if main_success and metafield_count > 0:
            content_result = enriched_data.get('content', {}).get('result', {})
            display_title = content_result.get('optimized_title', original_title)[:55] + '...'
            print(f"  ✅ {display_title} ({metafield_count} metafields)")
            updated += 1
            time.sleep(0.5)
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total enriched products: {len(enriched_products)}")
    print(f"Matched to Shopify: {matched}")
    print(f"Successfully updated: {updated}")
    print(f"Total metafields written: {total_metafields}")
    print(f"Failed: {failed}")
    print("=" * 80)
    
    if updated > 0:
        print("\n✨ SUCCESS! Your products now have:")
        print("   ✅ Updated titles & descriptions")
        print("   ✅ Category taxonomy")
        print("   ✅ SEO keywords")
        print("   ✅ Product attributes")
        print("   ✅ FAQs")
        print("   ✅ Tax compliance codes")
        print("\nNext steps:")
        print("   1. Follow shopify_writeback/SHOPIFY_METAFIELD_GUIDE.md to create metafield definitions")
        print("   2. Refresh your Shopify product pages to see all enriched data")

if __name__ == "__main__":
    main()
