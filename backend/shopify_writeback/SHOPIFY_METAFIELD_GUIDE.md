# Shopify Metafield Definitions for Enriched Product Data

## Overview
This guide shows you how to create metafield definitions in Shopify to store all enriched product data from your Catalog AI system.

**IMPORTANT: All metafields use the namespace `paladio` (your company name)**

---

## How to Create Metafield Definitions in Shopify

1. Go to **Shopify Admin** → **Settings** (bottom left)
2. Click **"Custom data"** (or "Metafields" in older versions)
3. Click **"Products"**
4. Click **"Add definition"** for each metafield below

---

## Metafield Definitions to Create

### 1. CATEGORY & TAXONOMY

#### **Enriched Category**
- **Name**: `Enriched Category`
- **Namespace and key**: `paladio.category`
- **Type**: `Single line text`
- **Description**: `AI-enriched Google Product Taxonomy category`

#### **Category Level 1**
- **Name**: `Category Level 1`
- **Namespace and key**: `paladio.category_level_1`
- **Type**: `Single line text`
- **Description**: `Top-level category (e.g., Apparel & Accessories)`

#### **Category Level 2**
- **Name**: `Category Level 2`
- **Namespace and key**: `paladio.category_level_2`
- **Type**: `Single line text`
- **Description**: `Second-level category (e.g., Clothing)`

#### **Category Level 3**
- **Name**: `Category Level 3`
- **Namespace and key**: `paladio.category_level_3`
- **Type**: `Single line text`
- **Description**: `Third-level category (e.g., Baby & Toddler Clothing)`

---

### 2. OPTIMIZED CONTENT

#### **Optimized Title**
- **Name**: `Optimized Title`
- **Namespace and key**: `paladio.optimized_title`
- **Type**: `Single line text`
- **Description**: `AI-optimized product title for better conversions`

#### **Optimized Description**
- **Name**: `Optimized Description`
- **Namespace and key**: `paladio.optimized_description`
- **Type**: `Multi-line text`
- **Description**: `AI-optimized product description`

---

### 3. SEO FIELDS

#### **SEO Keywords**
- **Name**: `SEO Keywords`
- **Namespace and key**: `paladio.seo_keywords`
- **Type**: `List.Single line text` (or `JSON` if list not available)
- **Description**: `AI-generated SEO keywords for search optimization`

#### **Title Keywords**
- **Name**: `Title Keywords`
- **Namespace and key**: `paladio.title_keywords`
- **Type**: `List.Single line text` (or `JSON`)
- **Description**: `Key product terms for title optimization`

#### **Description Sections**
- **Name**: `Description Sections`
- **Namespace and key**: `paladio.description_sections`
- **Type**: `Multi-line text` (or `JSON`)
- **Description**: `Structured description sections for formatting`

---

### 4. PRODUCT ATTRIBUTES

#### **Product Attributes**
- **Name**: `Product Attributes`
- **Namespace and key**: `paladio.attributes`
- **Type**: `JSON`
- **Description**: `All enriched product attributes (brand, material, size, etc.)`

#### **Brand**
- **Name**: `Brand`
- **Namespace and key**: `paladio.brand`
- **Type**: `Single line text`
- **Description**: `Product brand name`

#### **Material**
- **Name**: `Material`
- **Namespace and key**: `paladio.material`
- **Type**: `Single line text`
- **Description**: `Product material composition`

---

### 5. TAX COMPLIANCE

#### **Avalara Tax Code**
- **Name**: `Avalara Tax Code`
- **Namespace and key**: `paladio.avalara_tax_code`
- **Type**: `Single line text`
- **Description**: `Tax code for automated tax calculation`

#### **Tax Category**
- **Name**: `Tax Category`
- **Namespace and key**: `paladio.tax_category`
- **Type**: `Single line text`
- **Description**: `Product tax category`

---

### 6. PRODUCT FLAGS

#### **Is Bundle**
- **Name**: `Is Bundle`
- **Namespace and key**: `paladio.is_bundle`
- **Type**: `True or False`
- **Description**: `Indicates if product is a bundle`

#### **Has Hazmat**
- **Name**: `Has Hazmat`
- **Namespace and key**: `paladio.has_hazmat`
- **Type**: `True or False`
- **Description**: `Indicates if product contains hazardous materials`

---

### 7. FAQs

#### **Product FAQs**
- **Name**: `Product FAQs`
- **Namespace and key**: `paladio.faqs`
- **Type**: `JSON`
- **Description**: `AI-generated frequently asked questions and answers`

---

## Priority Order for Creation

If you're short on time, create these **essential metafields first**:

1. ✅ `paladio.category` - Category taxonomy
2. ✅ `paladio.optimized_title` - Better titles
3. ✅ `paladio.optimized_description` - Better descriptions
4. ✅ `paladio.seo_keywords` - SEO optimization
5. ✅ `paladio.attributes` - Product specs
6. ✅ `paladio.faqs` - Customer questions
7. ✅ `paladio.avalara_tax_code` - Tax compliance

---

## After Creating Definitions

Once you create these metafield definitions:

1. **Refresh your product page** in Shopify Admin
2. **Scroll to the "Metafields" section** at the bottom
3. You should now see all the enriched data fields populated!

---

## Using Metafields in Your Theme

To display metafields on your storefront, add this Liquid code to your theme:

```liquid
{% if product.metafields.paladio.optimized_description %}
  <div class="enriched-description">
    {{ product.metafields.paladio.optimized_description }}
  </div>
{% endif %}

{% if product.metafields.paladio.seo_keywords %}
  <meta name="keywords" content="{{ product.metafields.paladio.seo_keywords }}">
{% endif %}

{% if product.metafields.paladio.faqs %}
  <div class="product-faqs">
    <h3>Frequently Asked Questions</h3>
    {% assign faqs = product.metafields.paladio.faqs | parse_json %}
    {% for faq in faqs %}
      <div class="faq-item">
        <h4>{{ faq.question }}</h4>
        <p>{{ faq.answer }}</p>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

---

## Notes

- Some metafield types (like `List.Single line text`) may not be available on all Shopify plans
- If unavailable, use `JSON` type instead and parse in your theme
- Metafields are stored per product and don't affect performance
- You can edit metafield values manually in the product editor after creation
