# Shopify Writeback

Scripts to write enriched catalog data back to Shopify (metafields, title, description).

**Data source:** `../shopify_app/` (before-after (1).json, products (2).json)

## Scripts

| Script | Data Source | Purpose |
|--------|-------------|---------|
| `writeback_complete.py` | before-after (1).json | Full writeback: all metafields, title, description |
| `writeback_50_products.py` | products (2).json | Writeback: title, description, 4 metafields |
| `update_product_fields.py` | products (2).json | Update main fields + metafields (paladio namespace) |
| `create_metafield_definitions.py` | - | Create Paladio metafield definitions in Shopify |
| `show_before_after.py` | Shopify API | Compare original vs enriched data |
| `check_metafields.py` | Shopify API | Verify metafields on a product |
| `check_products.py` | products (2).json | Compare Shopify products vs enriched JSON |

## Run

```bash
cd shopify_writeback
python3 writeback_complete.py
# or
python3 writeback_50_products.py
```
