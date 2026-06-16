# Step-by-Step Guide: Create Metafield Definitions in Shopify

## ✅ Updated for Paladio

All metafields now use the **`paladio`** namespace (your company name).

---

## 📋 Quick Reference - Metafields to Create

| # | Name | Namespace | Key | Type |
|---|------|-----------|-----|------|
| 1 | Enriched Category | paladio | category | Single line text |
| 2 | SEO Keywords | paladio | seo_keywords | JSON |
| 3 | Product Attributes | paladio | attributes | JSON |
| 4 | Product FAQs | paladio | faqs | JSON |
| 5 | Avalara Tax Code | paladio | avalara_tax_code | Single line text |
| 6 | Tax Category | paladio | tax_category | Single line text |
| 7 | Title Keywords | paladio | title_keywords | JSON |
| 8 | Description Sections | paladio | description_sections | JSON |

---

## 📝 Step-by-Step Instructions

### **Step 1: Access Shopify Settings**

1. Open your **Shopify Admin**
2. Scroll down the **left sidebar**
3. Click **"Settings"** at the bottom (gear icon ⚙️)

---

### **Step 2: Go to Custom Data**

1. In Settings, click **"Custom data"**
   - (Or **"Metafields"** in older versions)
2. Click **"Products"**

---

### **Step 3: Create Metafield #1 - Enriched Category**

1. Click **"Add definition"**
2. Fill in:

```
Name: Enriched Category

Namespace: paladio
Key: category

Description: AI-enriched product category taxonomy

Type: Single line text
```

3. Click **"Save"**

---

### **Step 4: Create Metafield #2 - SEO Keywords**

1. Click **"Add definition"** again
2. Fill in:

```
Name: SEO Keywords

Namespace: paladio
Key: seo_keywords

Description: AI-generated SEO keywords

Type: JSON
```

3. Click **"Save"**

---

### **Step 5: Create Metafield #3 - Product Attributes**

```
Name: Product Attributes

Namespace: paladio
Key: attributes

Description: Enriched product attributes (brand, material, etc.)

Type: JSON
```

Click **"Save"**

---

### **Step 6: Create Metafield #4 - Product FAQs**

```
Name: Product FAQs

Namespace: paladio
Key: faqs

Description: AI-generated frequently asked questions

Type: JSON
```

Click **"Save"**

---

### **Step 7: Create Metafield #5 - Avalara Tax Code**

```
Name: Avalara Tax Code

Namespace: paladio
Key: avalara_tax_code

Description: Tax code for automated tax calculation

Type: Single line text
```

Click **"Save"**

---

### **Step 8: Create Metafield #6 - Tax Category**

```
Name: Tax Category

Namespace: paladio
Key: tax_category

Description: Product tax category

Type: Single line text
```

Click **"Save"**

---

### **Step 9: Create Metafield #7 - Title Keywords**

```
Name: Title Keywords

Namespace: paladio
Key: title_keywords

Description: Key product terms for optimization

Type: JSON
```

Click **"Save"**

---

### **Step 10: Create Metafield #8 - Description Sections**

```
Name: Description Sections

Namespace: paladio
Key: description_sections

Description: Structured description sections

Type: JSON
```

Click **"Save"**

---

## ✅ Verify Your Metafields

1. Go to **Products** in left sidebar
2. Click on **"Colorado Baby Onesie"** or **"Sway True Wireless Headphones"**
3. **Scroll all the way down**
4. Look for **"Metafields"** section
5. Click to expand it
6. You should see all your **paladio** metafields with data!

Example of what you'll see:

```
Metafields
├─ Enriched Category: "Apparel & Accessories > Clothing > Baby & Toddler Clothing"
├─ SEO Keywords: ["Colorado baby onesie", "3-6 months snapsuit", ...]
├─ Product Attributes: {"brand": "Little", "material": "USA cotton", ...}
├─ Product FAQs: [{"question": "What material...", "answer": "..."}]
├─ Avalara Tax Code: "P0000000"
├─ Tax Category: "Clothing"
└─ Title Keywords: ["Colorado", "Baby Onesie", "Cotton", ...]
```

---

## 🎯 Important Notes

- **All metafields use namespace `paladio`** (not sanio)
- Each metafield must be created individually
- Once created, they will auto-populate on all products that have the data
- Metafields are visible in admin but hidden from customers unless you add them to your theme

---

## 🚀 Next Steps

After creating all metafields, you can:

1. **View enriched data** in product editor
2. **Display on storefront** using Liquid code (see SHOPIFY_METAFIELD_GUIDE.md)
3. **Run the full writeback** for all 50 products (remove test limit from script)

---

**Need help? Check the detailed guide:** `SHOPIFY_METAFIELD_GUIDE.md`
