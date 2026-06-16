#!/usr/bin/env python3
"""Check what products are in Shopify and compare with enriched JSON"""

import requests
import json
import os

from _config import DATA_DIR, STORE_URL, ACCESS_TOKEN, API_VERSION

output = []

# Fetch Shopify products
url = f"https://{STORE_URL}/admin/api/{API_VERSION}/products.json?limit=250"
headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("Fetching products from Shopify...")
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

products = response.json().get('products', [])

output.append("="*80)
output.append(f"SHOPIFY PRODUCTS ({len(products)} total)")
output.append("="*80)
output.append("")

for i, p in enumerate(products, 1):
    output.append(f"{i}. ID: {p['id']}")
    output.append(f"   Title: {p['title']}")
    output.append(f"   SKU: {p.get('variants', [{}])[0].get('sku', 'N/A')}")
    output.append("")

# Load enriched JSON from shopify_app
output.append("")
output.append("="*80)
output.append("ENRICHED PRODUCTS FROM JSON")
output.append("="*80)
output.append("")

# Try products (2).json first
data_path = os.path.join(DATA_DIR, 'products (2).json')
if not os.path.exists(data_path):
    data_path = os.path.join(DATA_DIR, 'products.json')

with open(data_path, 'r') as f:
    data = json.load(f)
    
enriched = data.get('items', [])

for i, p in enumerate(enriched, 1):
    output.append(f"{i}. Title: {p.get('optimized_title', 'N/A')}")
    output.append(f"   Category: {p.get('category', 'N/A')}")
    output.append("")

# Write to file (in shopify_writeback folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, 'product_comparison.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(output))

print(f"✅ Output written to: {out_path}")
print(f"   Shopify products: {len(products)}")
print(f"   Enriched products: {len(enriched)}")
