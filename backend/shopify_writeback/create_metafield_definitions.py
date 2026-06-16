#!/usr/bin/env python3
"""
Create Paladio metafield definitions in Shopify via GraphQL Admin API
Run this once to set up all metafield definitions - then enriched data will be visible in product editor
"""
import requests
import time

from _config import STORE_URL, ACCESS_TOKEN, API_VERSION

GRAPHQL_URL = f"https://{STORE_URL}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# All Paladio metafield definitions to create
METAFIELD_DEFINITIONS = [
    # Category & Taxonomy
    {"name": "Enriched Category", "namespace": "paladio", "key": "category", "type": "single_line_text_field",
     "description": "AI-enriched Google Product Taxonomy category"},
    {"name": "Category Level 1", "namespace": "paladio", "key": "category_level_1", "type": "single_line_text_field",
     "description": "Top-level category (e.g., Apparel & Accessories)"},
    {"name": "Category Level 2", "namespace": "paladio", "key": "category_level_2", "type": "single_line_text_field",
     "description": "Second-level category (e.g., Clothing)"},
    {"name": "Category Level 3", "namespace": "paladio", "key": "category_level_3", "type": "single_line_text_field",
     "description": "Third-level category (e.g., Baby & Toddler Clothing)"},
    # Optimized Content
    {"name": "Optimized Title", "namespace": "paladio", "key": "optimized_title", "type": "single_line_text_field",
     "description": "AI-optimized product title for better conversions"},
    {"name": "Optimized Description", "namespace": "paladio", "key": "optimized_description", "type": "multi_line_text_field",
     "description": "AI-optimized product description"},
    # SEO
    {"name": "SEO Keywords", "namespace": "paladio", "key": "seo_keywords", "type": "json",
     "description": "AI-generated SEO keywords for search optimization"},
    {"name": "Title Keywords", "namespace": "paladio", "key": "title_keywords", "type": "json",
     "description": "Key product terms for title optimization"},
    {"name": "Description Sections", "namespace": "paladio", "key": "description_sections", "type": "json",
     "description": "Structured description sections for formatting"},
    # Attributes
    {"name": "Product Attributes", "namespace": "paladio", "key": "attributes", "type": "json",
     "description": "All enriched product attributes (brand, material, size, etc.)"},
    {"name": "Brand", "namespace": "paladio", "key": "brand", "type": "single_line_text_field",
     "description": "Product brand name"},
    {"name": "Material", "namespace": "paladio", "key": "material", "type": "single_line_text_field",
     "description": "Product material composition"},
    # Tax Compliance
    {"name": "Avalara Tax Code", "namespace": "paladio", "key": "avalara_tax_code", "type": "single_line_text_field",
     "description": "Tax code for automated tax calculation"},
    {"name": "Tax Category", "namespace": "paladio", "key": "tax_category", "type": "single_line_text_field",
     "description": "Product tax category"},
    # Product Flags
    {"name": "Is Bundle", "namespace": "paladio", "key": "is_bundle", "type": "boolean",
     "description": "Indicates if product is a bundle"},
    {"name": "Has Hazmat", "namespace": "paladio", "key": "has_hazmat", "type": "boolean",
     "description": "Indicates if product contains hazardous materials"},
    # FAQs
    {"name": "Product FAQs", "namespace": "paladio", "key": "faqs", "type": "json",
     "description": "AI-generated frequently asked questions and answers"},
]


def create_metafield_definition(definition: dict):
    """Create a single metafield definition via GraphQL"""
    
    mutation = """
    mutation metafieldDefinitionCreate($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
          id
          name
          namespace
          key
          type {
            name
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    
    variables = {
        "definition": {
            "name": definition["name"],
            "namespace": definition["namespace"],
            "key": definition["key"],
            "description": definition["description"],
            "type": definition["type"],
            "ownerType": "PRODUCT",
        }
    }
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json={"query": mutation, "variables": variables}
        )
        response.raise_for_status()
        data = response.json()
        
        result = data.get("data", {}).get("metafieldDefinitionCreate", {})
        user_errors = result.get("userErrors", [])
        
        if user_errors:
            error_msg = "; ".join(e.get("message", str(e)) for e in user_errors)
            return False, error_msg
        
        created = result.get("createdDefinition", {})
        return True, f"{created.get('namespace')}.{created.get('key')}"
        
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 70)
    print("CREATE PALADIO METAFIELD DEFINITIONS")
    print("=" * 70)
    print(f"\nStore: {STORE_URL}")
    print(f"Creating {len(METAFIELD_DEFINITIONS)} metafield definitions...\n")
    
    created = 0
    skipped = 0
    failed = 0
    
    for i, defn in enumerate(METAFIELD_DEFINITIONS, 1):
        success, msg = create_metafield_definition(defn)
        
        if success:
            # Check if it was actually created or already exists
            if "already exists" in msg.lower() or "duplicate" in msg.lower():
                print(f"  [{i:2d}] ⏭️  {defn['name']} - already exists")
                skipped += 1
            else:
                print(f"  [{i:2d}] ✅ {defn['name']} ({msg})")
                created += 1
        else:
            if "already exists" in msg.lower() or "taken" in msg.lower() or "duplicate" in msg.lower():
                print(f"  [{i:2d}] ⏭️  {defn['name']} - already exists")
                skipped += 1
            else:
                print(f"  [{i:2d}] ❌ {defn['name']}: {msg}")
                failed += 1
        
        time.sleep(0.5)  # Rate limiting
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Created: {created}")
    print(f"Already existed: {skipped}")
    print(f"Failed: {failed}")
    print("=" * 70)
    
    if created > 0 or skipped > 0:
        print("\n✨ Done! Go to any product in Shopify Admin and scroll down to see")
        print("   the Metafields section with your enriched Paladio data.")
    elif failed > 0:
        print("\n⚠️  Some definitions failed. You may need to create them manually")
        print("   in Settings → Custom data → Products → Add definition")


if __name__ == "__main__":
    main()
