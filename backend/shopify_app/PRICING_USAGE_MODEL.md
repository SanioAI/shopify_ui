# Shopify App Pricing & Usage Model

**Last Updated**: February 12, 2026  
**Status**: Updated with Usage-Based Billing

---

## 🎯 Key Pricing Principle

**Charge based on USAGE, not just catalog size.**

### What We Track & Charge For:

1. **New Products** - When merchant adds new products
2. **Changed Products** - When existing products are updated and need re-processing
3. **Initial Catalog** - One-time processing of existing catalog

---

## 💰 Updated Pricing Model

### **Usage-Based Billing**

Instead of flat monthly rates, charge based on actual agent usage:

```
Price = (New Products × Agent Price) + (Changed Products × Agent Price)
```

**Example:**
- Merchant has 500 products initially
- Adds 20 new products in Month 1
- Updates 50 existing products in Month 1
- Has Taxonomy Agent enabled ($0.02/product)

**Billing:**
```
Initial Catalog: 500 products × $0.02 = $10.00 (one-time)
New Products:     20 products × $0.02 = $0.40
Changed Products: 50 products × $0.02 = $1.00
──────────────────────────────────────────────
Month 1 Total: $11.40
```

---

## 📊 Three Pricing Tiers (Updated)

### **Starter Plan** - $19/month base + usage

**Base Fee**: $19/month (platform access)

**Included:**
- Choose up to 3 agents
- 100 free product operations/month
- Basic support

**Usage Charges:**
- $0.01-$0.05 per product operation (depends on agent)
- New products: Full price
- Changed products: Full price
- Bulk initial import: 50% discount

**Best For:**
- Small stores (100-500 products)
- Low change frequency
- Testing the platform

---

### **Professional Plan** - $79/month base + usage

**Base Fee**: $79/month (platform access)

**Included:**
- Choose up to 7 agents
- 500 free product operations/month
- Priority support
- Advanced analytics

**Usage Charges:**
- $0.008-$0.04 per product operation (20% discount)
- New products: Full price
- Changed products: Full price
- Bulk initial import: 50% discount

**Best For:**
- Medium stores (500-5,000 products)
- Moderate change frequency
- Growing catalogs

---

### **Enterprise Plan** - $299/month base + usage

**Base Fee**: $299/month (platform access)

**Included:**
- All 10 agents
- 2,000 free product operations/month
- Dedicated support (phone + Slack)
- Custom integrations
- API access
- Volume discounts

**Usage Charges:**
- $0.006-$0.03 per product operation (40% discount)
- New products: Full price
- Changed products: Full price
- Bulk initial import: 50% discount

**Best For:**
- Large stores (5,000+ products)
- High change frequency
- Multiple stores/brands

---

## 📈 Usage Tracking Dashboard

### **New UI Component: Usage Dashboard**

Display in the main dashboard:

```
┌────────────────────────────────────────────────────────┐
│ Usage This Month                    [View Details →]   │
├────────────────────────────────────────────────────────┤
│                                                         │
│ ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│ │ 45         │  │ 128        │  │ 173        │        │
│ │ New        │  │ Changed    │  │ Total      │        │
│ │ Products   │  │ Products   │  │ Operations │        │
│ └────────────┘  └────────────┘  └────────────┘        │
│                                                         │
│ Included in plan: 500 operations                       │
│ Used: 173 / 500 (35%)                                  │
│ Remaining: 327 operations                              │
│                                                         │
│ Additional usage: $0.00                                │
│ (No overage charges this month)                        │
│                                                         │
├────────────────────────────────────────────────────────┤
│ Top Agents This Month:                                 │
│ • Taxonomy Agent: 173 operations                       │
│ • SEO Agent: 173 operations                            │
│ • Content Agent: 45 operations (new products only)     │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## 📋 Detailed Usage Breakdown Page

### **New Page: Usage & Billing**

```
┌──────────────────────────────────────────────────────────┐
│ Usage & Billing                          February 2026   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ MONTHLY SUMMARY                                           │
│                                                           │
│ Plan: Professional ($79/month)                            │
│ Included Operations: 500                                  │
│ Operations Used: 173                                      │
│ Additional Operations: 0                                  │
│                                                           │
│ Base Fee:        $79.00                                   │
│ Usage Charges:   $0.00                                    │
│ Total:           $79.00                                   │
│                                                           │
├──────────────────────────────────────────────────────────┤
│ PRODUCT ACTIVITY BREAKDOWN                                │
│                                                           │
│ Initial Catalog (Feb 1)                                   │
│ • 500 products × 3 agents = 1,500 operations              │
│ • Bulk import discount (50%): $60.00 → $30.00            │
│ • Status: ✅ Completed (one-time charge)                 │
│                                                           │
│ New Products (Feb 1-28)                                   │
│ • 45 products added                                       │
│ • 3 agents active = 135 operations                        │
│ • Cost: 135 × $0.01 avg = $1.35                          │
│ • Status: ✅ Included in plan                            │
│                                                           │
│ Changed Products (Feb 1-28)                               │
│ • 38 products updated (re-processed)                      │
│ • 3 agents active = 114 operations                        │
│ • Cost: 114 × $0.01 avg = $1.14                          │
│ • Status: ✅ Included in plan                            │
│                                                           │
│ Total Operations: 173 / 500 (35%)                         │
│                                                           │
├──────────────────────────────────────────────────────────┤
│ DAILY ACTIVITY (Last 7 Days)                             │
│                                                           │
│ Date     New  Changed  Total  Cost                       │
│ ──────────────────────────────────────                  │
│ Feb 21    2     5       7     $0.07 (included)           │
│ Feb 20    1     8       9     $0.09 (included)           │
│ Feb 19    0     3       3     $0.03 (included)           │
│ Feb 18    3     2       5     $0.05 (included)           │
│ Feb 17    5     6      11     $0.11 (included)           │
│ Feb 16    2     4       6     $0.06 (included)           │
│ Feb 15    1     2       3     $0.03 (included)           │
│                                                           │
├──────────────────────────────────────────────────────────┤
│ AGENT-SPECIFIC USAGE                                      │
│                                                           │
│ Agent            Operations  Cost     Status             │
│ ────────────────────────────────────────────────        │
│ Taxonomy          173       $3.46    Included            │
│ SEO               173       $3.46    Included            │
│ Content (new)      45       $2.25    Included            │
│                                                           │
│ Total            391        $9.17    Included in plan    │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 🔄 How We Track Changes

### **Product Change Detection**

Monitor these events via Shopify webhooks:

1. **`products/create`** → New Product
   - Track as "New Product"
   - Full agent processing
   - Full price

2. **`products/update`** → Changed Product
   - Compare with previous version
   - Detect significant changes:
     - Title changed
     - Description changed
     - Images added/removed
     - Variants changed
     - Price changed
     - Tags changed
   - Re-run agents only if significant
   - Full price

### **Change Significance Detection**

```javascript
// Pseudo-code for change detection
function isSignificantChange(oldProduct, newProduct) {
  const significantFields = [
    'title',
    'body_html',
    'images',
    'variants',
    'tags',
    'product_type',
    'vendor'
  ];
  
  for (const field of significantFields) {
    if (hasChanged(oldProduct[field], newProduct[field])) {
      return true;
    }
  }
  
  return false;
}
```

**Only charge for significant changes** (not minor updates like inventory counts).

---

## 📊 Per-Client Metrics (Backend Tracking)

### **What We Store in Database**

```sql
-- Client usage table
CREATE TABLE client_usage (
  id UUID PRIMARY KEY,
  client_id UUID NOT NULL,
  month DATE NOT NULL,
  
  -- Product counts
  initial_catalog_size INT,
  new_products_count INT,
  changed_products_count INT,
  total_operations INT,
  
  -- Per-agent usage
  agent_operations JSONB, -- { "taxonomy": 173, "seo": 173, ... }
  
  -- Billing
  base_fee DECIMAL(10,2),
  usage_charges DECIMAL(10,2),
  total_amount DECIMAL(10,2),
  
  -- Timestamps
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  
  UNIQUE(client_id, month)
);

-- Daily product activity log
CREATE TABLE product_activity_log (
  id UUID PRIMARY KEY,
  client_id UUID NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  activity_type VARCHAR(50), -- 'new', 'changed', 'deleted'
  
  -- Change details
  changed_fields JSONB, -- { "title": true, "description": true, ... }
  significance_score DECIMAL(3,2), -- 0.0 - 1.0
  
  -- Agent processing
  agents_run JSONB, -- ["taxonomy", "seo", "content"]
  operations_count INT,
  
  -- Timestamps
  occurred_at TIMESTAMP,
  processed_at TIMESTAMP,
  
  INDEX(client_id, occurred_at)
);
```

---

## 🎯 Updated Agent Pricing

### **Per-Operation Pricing**

| Agent | Starter | Professional | Enterprise |
|-------|---------|--------------|------------|
| Hazmat | $0.01 | $0.008 | $0.006 |
| Bundle | $0.01 | $0.008 | $0.006 |
| Taxonomy | $0.02 | $0.016 | $0.012 |
| Schema | $0.02 | $0.016 | $0.012 |
| Extraction | $0.03 | $0.024 | $0.018 |
| Enrichment | $0.04 | $0.032 | $0.024 |
| Content | $0.05 | $0.04 | $0.03 |
| SEO | $0.02 | $0.016 | $0.012 |
| FAQ | $0.02 | $0.016 | $0.012 |
| Compliance | $0.02 | $0.016 | $0.012 |

**Bulk Initial Import:** 50% discount on first-time catalog processing

---

## 📈 Example Billing Scenarios

### **Scenario 1: Small Jewelry Store (Starter Plan)**

**Initial Setup:**
- 224 existing products
- Activates: Taxonomy, SEO, Schema (3 agents)

**Month 1:**
```
Initial Import:
  224 products × 3 agents = 672 operations
  672 × $0.015 avg = $10.08
  Bulk discount (50%): $5.04 (one-time)

New Products:
  12 new products × 3 agents = 36 operations
  36 × $0.015 avg = $0.54

Changed Products:
  8 products updated × 3 agents = 24 operations
  24 × $0.015 avg = $0.36

Total Operations: 60 (within 100 free)
Base Fee: $19.00
Usage Charges: $0.00 (within allowance)
One-time Import: $5.04

Month 1 Total: $24.04
```

**Month 2:**
```
New Products: 5 × 3 = 15 operations
Changed Products: 3 × 3 = 9 operations
Total: 24 operations (within 100 free)

Month 2 Total: $19.00 (base fee only)
```

---

### **Scenario 2: Medium Fashion Store (Professional Plan)**

**Initial Setup:**
- 2,500 existing products
- Activates: Taxonomy, SEO, Schema, Content, Extraction (5 agents)

**Month 1:**
```
Initial Import:
  2,500 products × 5 agents = 12,500 operations
  12,500 × $0.02 avg = $250.00
  Bulk discount (50%): $125.00 (one-time)

New Products (Season Launch):
  150 new products × 5 agents = 750 operations
  750 × $0.02 avg = $15.00

Changed Products:
  80 products updated × 5 agents = 400 operations
  400 × $0.02 avg = $8.00

Total Operations: 1,150
Included in plan: 500
Overage: 650 operations
Overage charges: 650 × $0.02 = $13.00

Base Fee: $79.00
Usage Charges: $13.00
One-time Import: $125.00

Month 1 Total: $217.00
```

**Month 2 (Normal):**
```
New Products: 30 × 5 = 150 operations
Changed Products: 60 × 5 = 300 operations
Total: 450 operations (within 500 free)

Month 2 Total: $79.00 (base fee only)
```

---

### **Scenario 3: Large Electronics Store (Enterprise Plan)**

**Initial Setup:**
- 10,000 existing products
- Activates: All 10 agents

**Month 1:**
```
Initial Import:
  10,000 products × 10 agents = 100,000 operations
  100,000 × $0.018 avg = $1,800.00
  Bulk discount (50%): $900.00 (one-time)

New Products:
  200 new products × 10 agents = 2,000 operations
  Included in plan: 2,000 free

Changed Products:
  500 products updated × 10 agents = 5,000 operations
  Overage: 5,000 operations
  5,000 × $0.018 avg = $90.00

Base Fee: $299.00
Usage Charges: $90.00
One-time Import: $900.00

Month 1 Total: $1,289.00
```

**Month 2 (Normal):**
```
New Products: 80 × 10 = 800 operations
Changed Products: 120 × 10 = 1,200 operations
Total: 2,000 operations (exactly at limit)

Month 2 Total: $299.00 (base fee only)
```

---

## 🔔 Usage Alerts & Notifications

### **Email Notifications**

Send to merchants:

1. **Approaching Limit** (at 80% of included operations)
   ```
   Subject: You've used 80% of your monthly operations
   
   Hi [Merchant],
   
   You've used 400 of your 500 included operations this month.
   
   Current usage:
   - New products: 45
   - Changed products: 80
   - Total operations: 400
   
   If you exceed 500 operations, additional operations will be
   charged at $0.016/operation.
   
   View detailed usage: [Link]
   ```

2. **Exceeded Limit** (when overage occurs)
   ```
   Subject: Additional usage charges this month
   
   Hi [Merchant],
   
   You've exceeded your plan's included operations.
   
   Plan: Professional ($79/month, 500 operations included)
   Total usage: 650 operations
   Overage: 150 operations
   Additional charges: $2.40
   
   Your next invoice will be $81.40.
   
   Consider upgrading to Enterprise for higher limits.
   ```

3. **Monthly Summary** (end of month)
   ```
   Subject: Your February usage summary
   
   Hi [Merchant],
   
   Here's your usage summary for February:
   
   - New products added: 45
   - Products updated: 128
   - Total operations: 650
   - Base fee: $79.00
   - Additional usage: $2.40
   - Total: $81.40
   
   Download invoice: [Link]
   View detailed breakdown: [Link]
   ```

---

## 📊 API Endpoints for Usage Tracking

### **Get Monthly Usage**

```http
GET /api/usage/monthly?month=2026-02

Response:
{
  "client_id": "client_abc123",
  "month": "2026-02",
  "plan": "professional",
  "usage": {
    "new_products": 45,
    "changed_products": 128,
    "total_operations": 650,
    "operations_by_agent": {
      "taxonomy": 173,
      "seo": 173,
      "content": 45,
      "extraction": 173,
      "schema": 86
    }
  },
  "billing": {
    "base_fee": 79.00,
    "included_operations": 500,
    "overage_operations": 150,
    "overage_charges": 2.40,
    "total": 81.40
  }
}
```

### **Get Daily Activity**

```http
GET /api/usage/daily?start_date=2026-02-15&end_date=2026-02-21

Response:
{
  "daily_activity": [
    {
      "date": "2026-02-21",
      "new_products": 2,
      "changed_products": 5,
      "total_operations": 21,
      "cost": 0.336
    },
    {
      "date": "2026-02-20",
      "new_products": 1,
      "changed_products": 8,
      "total_operations": 27,
      "cost": 0.432
    }
  ]
}
```

### **Get Product Activity Log**

```http
GET /api/usage/products?limit=50&offset=0

Response:
{
  "total": 173,
  "products": [
    {
      "product_id": "9343074173172",
      "activity_type": "changed",
      "changed_at": "2026-02-21T14:32:00Z",
      "changed_fields": ["title", "description"],
      "agents_run": ["taxonomy", "seo", "content"],
      "operations": 3,
      "cost": 0.048
    }
  ]
}
```

---

## 🎯 Key Implementation Points

### **1. Webhook Handling**

```javascript
// Handle Shopify product webhooks
app.post('/webhooks/products/create', async (req, res) => {
  const product = req.body;
  
  // Track as new product
  await trackProductActivity({
    client_id: getClientFromShop(req.headers['x-shopify-shop-domain']),
    product_id: product.id,
    activity_type: 'new',
    product_data: product
  });
  
  // Trigger agent processing
  await triggerAgentProcessing({
    product_id: product.id,
    agents: getEnabledAgents(client_id),
    priority: 'high'
  });
  
  res.status(200).send('OK');
});

app.post('/webhooks/products/update', async (req, res) => {
  const newProduct = req.body;
  const oldProduct = await getProductFromCache(newProduct.id);
  
  // Check if change is significant
  if (isSignificantChange(oldProduct, newProduct)) {
    await trackProductActivity({
      client_id: getClientFromShop(req.headers['x-shopify-shop-domain']),
      product_id: newProduct.id,
      activity_type: 'changed',
      changed_fields: detectChangedFields(oldProduct, newProduct),
      product_data: newProduct
    });
    
    // Trigger agent re-processing
    await triggerAgentProcessing({
      product_id: newProduct.id,
      agents: getEnabledAgents(client_id),
      priority: 'normal'
    });
  }
  
  res.status(200).send('OK');
});
```

### **2. Billing Integration**

```javascript
// Calculate monthly bill
async function calculateMonthlyBill(client_id, month) {
  const usage = await getMonthlyUsage(client_id, month);
  const plan = await getClientPlan(client_id);
  
  const baseFee = plan.base_fee;
  const includedOps = plan.included_operations;
  const pricePerOp = plan.price_per_operation;
  
  const totalOps = usage.new_products + usage.changed_products;
  const overageOps = Math.max(0, totalOps - includedOps);
  const overageCharges = overageOps * pricePerOp;
  
  return {
    base_fee: baseFee,
    usage_charges: overageCharges,
    total: baseFee + overageCharges
  };
}

// Charge via Shopify Billing API
async function chargeClient(client_id, amount, description) {
  const shop = await getShopDomain(client_id);
  
  const charge = await shopify.recurringApplicationCharge.create({
    name: `Catalog Agents - ${description}`,
    price: amount,
    return_url: `https://your-app.com/billing/callback`,
    test: process.env.NODE_ENV === 'development'
  });
  
  return charge;
}
```

---

## 📋 Summary

### **Key Changes to Pricing Model:**

1. ✅ **Base fee + usage** (not flat monthly)
2. ✅ **Track new products separately** (full charge)
3. ✅ **Track changed products separately** (full charge)
4. ✅ **Initial catalog discount** (50% off bulk import)
5. ✅ **Include free operations** (100/500/2000 per tier)
6. ✅ **Usage dashboard** (show metrics to merchant)
7. ✅ **Daily activity log** (transparency)
8. ✅ **Email alerts** (approaching limit, exceeded, monthly summary)
9. ✅ **Webhooks for real-time tracking** (products/create, products/update)
10. ✅ **Smart change detection** (only charge for significant changes)

---

**This model is MUCH better for your business!** 📈

It ensures you get paid fairly for:
- Initial catalog processing
- Each new product added
- Each product that changes and needs re-processing

**End of Document**
