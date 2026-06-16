# The 10 Catalog Agents - Official List

**Last Updated**: February 12, 2026  
**Status**: Confirmed by Product Team

---

## Complete Agent List

These are the **10 agents** that will be available in the Shopify App:

### 1. **Hazmat Agent** ⚠️

**Purpose**: Detect hazardous materials and shipping restrictions

**What it does**:
- Identifies products containing hazardous materials (batteries, chemicals, aerosols, etc.)
- Flags shipping restrictions (air, ground, international)
- Provides compliance codes for carriers

**Output**:
- Hazmat classification (yes/no)
- Material type (lithium battery, flammable liquid, etc.)
- Shipping restrictions
- DOT/IATA compliance codes

**Pricing**: $0.01/product  
**Accuracy**: 90-95% (deterministic-first)  
**Use Case**: Shipping compliance, marketplace requirements, carrier integration

---

### 2. **Bundle Agent** 📦

**Purpose**: Detect multi-item bundles and product sets

**What it does**:
- Identifies if product is a bundle/set/pack
- Extracts bundle components
- Detects quantity multipliers ("6-pack", "set of 4")

**Output**:
- Is bundle: true/false
- Component items (if available)
- Quantity per bundle
- Bundle type (set, pack, kit, collection)

**Pricing**: $0.01/product  
**Accuracy**: 85-95% (deterministic-first)  
**Use Case**: Accurate pricing, inventory management, shipping calculations

---

### 3. **Taxonomy Agent** 🏷️

**Purpose**: Classify products into Google Product Taxonomy

**What it does**:
- Maps products to Google's 6,000+ category taxonomy
- Provides multi-level category hierarchy
- Assigns confidence scores

**Output**:
- Category path (e.g., "Apparel & Accessories > Jewelry > Necklaces")
- Category ID (Google taxonomy ID)
- Confidence score
- Alternative categories (if close match)

**Pricing**: $0.02/product  
**Accuracy**: 95%+ (80% deterministic, 20% LLM fallback)  
**Use Case**: SEO, marketplace compliance, product discoverability, Google Shopping

---

### 4. **Schema Agent** 🗂️

**Purpose**: Generate structured data (Schema.org) for products

**What it does**:
- Creates JSON-LD markup for rich snippets
- Generates category-specific schemas (Product, Offer, Review, etc.)
- Ensures Google compliance

**Output**:
- JSON-LD schema markup
- Product properties (name, description, price, availability)
- Offer details
- Review/rating schema (if applicable)

**Pricing**: $0.02/product  
**Accuracy**: 91%+ (category-specific schemas)  
**Use Case**: SEO, rich snippets in search results, Google Shopping

---

### 5. **Extraction Agent** 📋

**Purpose**: Extract structured attributes from product data

**What it does**:
- Identifies product attributes (material, size, color, weight, dimensions, etc.)
- Extracts values with confidence scores
- Standardizes attribute names

**Output**:
- List of key-value attribute pairs
- Data source (title, description, specs)
- Confidence score per attribute
- Alternative values (if multiple found)

**Pricing**: $0.03/product  
**Accuracy**: 70-85% (deterministic-first, LLM fallback)  
**Use Case**: Standardize product data, enable filtering/faceting, comparison shopping

---

### 6. **Enrichment Agent** 🌐

**Purpose**: Add missing product data from external sources

**What it does**:
- Pulls data from manufacturer websites (Tavily/Zyte)
- Adds missing dimensions, weights, specs
- Enriches images and technical details
- Routes to appropriate data connectors (Amazon, Google Shopping, manufacturer sites)

**Output**:
- Enhanced product attributes
- Additional images
- Technical specifications
- Data source URLs

**Pricing**: $0.04/product  
**Accuracy**: Medium (depends on source availability)  
**Use Case**: Complete missing data, reduce manual entry, improve product pages

---

### 7. **Content Agent** ✍️

**Purpose**: Generate optimized product titles and descriptions

**What it does**:
- Creates compelling product titles
- Generates detailed product descriptions
- Optimizes for readability and conversions
- Maintains brand voice

**Output**:
- Enhanced product title
- Full product description (multiple lengths: short, medium, long)
- Key features/benefits
- Technical specifications section

**Pricing**: $0.05/product  
**Accuracy**: 88%+ (AI-powered, human-reviewable)  
**Use Case**: Improve product pages, increase conversions, save content writing time

---

### 8. **SEO Agent** 🔍

**Purpose**: Generate SEO metadata (meta title, meta description, keywords)

**What it does**:
- Creates optimized meta titles (50-60 characters)
- Generates meta descriptions (150-160 characters)
- Suggests keywords
- Optimizes for search engines

**Output**:
- SEO meta title
- SEO meta description
- Primary keywords
- Secondary keywords
- URL slug suggestions

**Pricing**: $0.02/product  
**Accuracy**: 85%+ (SEO best practices)  
**Use Case**: Improve search rankings, increase organic traffic, Google Shopping optimization

---

### 9. **FAQ Generator Agent** ❓

**Purpose**: Generate frequently asked questions for products

**What it does**:
- Creates relevant FAQs based on product type
- Generates answers using product data
- Formats for Schema.org FAQ markup

**Output**:
- 5-10 FAQ pairs (question + answer)
- JSON-LD FAQ schema
- FAQ categories (shipping, usage, specs, warranty, etc.)

**Pricing**: $0.02/product  
**Accuracy**: 82%+ (category-specific FAQs)  
**Use Case**: Reduce support inquiries, improve SEO (FAQ rich snippets), enhance product pages

---

### 10. **Compliance Agent** 📜

**Purpose**: Map products to tax codes and regulatory compliance

**What it does**:
- Maps to Avalara tax codes
- Identifies regulatory requirements
- Flags compliance issues
- Provides tax classification

**Output**:
- Avalara tax code
- Product category for tax purposes
- Regulatory flags (FDA, FCC, CPSC, etc.)
- Compliance notes

**Pricing**: $0.02/product  
**Accuracy**: 75-85% (deterministic-first, LLM fallback)  
**Use Case**: Tax automation, legal compliance, marketplace requirements, Avalara integration

---

## Agent Categories

### Data Quality (5 agents)
- Extraction Agent
- Bundle Agent
- Taxonomy Agent
- Schema Agent
- Enrichment Agent

### Content & SEO (3 agents)
- Content Agent
- SEO Agent
- FAQ Generator Agent

### Compliance (2 agents)
- Hazmat Agent
- Compliance Agent

---

## Pricing Summary

| Agent | Price per Product | Monthly Cost (224 products) |
|-------|-------------------|----------------------------|
| Hazmat | $0.01 | $2.24 |
| Bundle | $0.01 | $2.24 |
| Taxonomy | $0.02 | $4.48 |
| Schema | $0.02 | $4.48 |
| Extraction | $0.03 | $6.72 |
| Enrichment | $0.04 | $8.96 |
| Content | $0.05 | $11.20 |
| SEO | $0.02 | $4.48 |
| FAQ Generator | $0.02 | $4.48 |
| Compliance | $0.02 | $4.48 |
| **TOTAL** | **$0.24** | **$53.76/month** |

---

## Agent Dependencies

Some agents work better when combined:

**Recommended Combos**:
1. **SEO Boost**: Taxonomy + SEO + Schema + FAQ Generator
2. **Content Suite**: Content + SEO + FAQ Generator
3. **Data Foundation**: Extraction + Taxonomy + Bundle + Hazmat
4. **Compliance Pack**: Hazmat + Compliance
5. **Complete Package**: All 10 agents

---

## Agent Processing Order

Optimal sequence for best results:

```
1. Bundle Agent (detect if multi-item)
   ↓
2. Taxonomy Agent (categorize)
   ↓
3. Extraction Agent (get attributes)
   ↓
4. Enrichment Agent (add missing data)
   ↓
5. Schema Agent (structured data)
   ↓
6. Content Agent (title/description)
   ↓
7. SEO Agent (meta tags)
   ↓
8. FAQ Generator (questions/answers)
   ↓
9. Hazmat Agent (shipping restrictions)
   ↓
10. Compliance Agent (tax codes)
```

This order ensures each agent has maximum context from previous agents.

---

## Implementation Mapping

### Backend Modules (from Architecture)

| Agent | DSPy Pipeline/Module |
|-------|---------------------|
| Hazmat | `HazmatSegmentsAnalyzer` → `HazmatDetectionModule` |
| Bundle | `BundleSegmentsAnalyzer` → `BundleDetectionModule` |
| Taxonomy | `TaxonomySegmentsAnalyzer` → `TaxonomyPredictionModule` |
| Schema | `SchemaSegmentsAnalyzer` → `SchemaGenerationModule` |
| Extraction | `AttributeSegmentsAnalyzer` → `LLMExtractionModule` / `BatchLLMExtractionModule` |
| Enrichment | `EnrichmentSegmentsAnalyzer` → `ConnectorRoutingModule` + `DimensionPredictionModule` |
| Content | `ContentSegmentsAnalyzer` → `TitleGenerationModule` + `DescriptionGenerationModule` |
| SEO | `ContentSegmentsAnalyzer` → `SEOOptimizationModule` |
| FAQ Generator | `ContentSegmentsAnalyzer` → `FAQGenerationModule` |
| Compliance | `ComplianceSegmentsAnalyzer` → `AvalaraTaxMappingModule` / `BatchAvalaraTaxMappingModule` |

---

## UI Icons

For the Shopify App UI:

| Agent | Icon | Color |
|-------|------|-------|
| Hazmat | ⚠️ | Orange |
| Bundle | 📦 | Brown |
| Taxonomy | 🏷️ | Blue |
| Schema | 🗂️ | Gray |
| Extraction | 📋 | Green |
| Enrichment | 🌐 | Purple |
| Content | ✍️ | Indigo |
| SEO | 🔍 | Red |
| FAQ Generator | ❓ | Yellow |
| Compliance | 📜 | Blue-Gray |

---

**End of Document**
