# Shopify App UI Development Plan

**Last Updated**: February 12, 2026  
**Owner**: Bindu Achalla  
**Status**: Planning Phase

---

## Table of Contents

1. [Overview](#overview)
2. [Catalog Agents Available](#catalog-agents-available)
3. [UI Components Required](#ui-components-required)
4. [Agent Configuration Interface](#agent-configuration-interface)
5. [Pricing Tiers](#pricing-tiers)
6. [Trial Mode Implementation](#trial-mode-implementation)
7. [Technical Architecture](#technical-architecture)
8. [API Integration Points](#api-integration-points)
9. [Implementation Phases](#implementation-phases)
10. [Wireframes](#wireframes)

---

## Overview

Build a Shopify app interface that allows merchants to:
- Select and configure catalog agents
- View pricing for each agent
- Try agents on 5-10 products before full activation
- View agent operation logs
- Manage product plans and subscriptions

### Key Requirements from Meeting
- **Agent Selection**: Dropdown with ~10 agents (configurable per client)
- **Pricing Visibility**: Show cost per agent upfront
- **Trial Mode**: Test on limited products (5-10) before activation
- **Logs Display**: Show agent operation results transparently
- **Backend Integration**: Connect to Soumya's catalog agent backend via Segment APIs

---

## Catalog Agents Available

Based on the catalog agentic system architecture, these are the **10 core agents** that should be exposed in the UI:

### 1. **Taxonomy Agent** 🏷️
- **Purpose**: Classify products into Google Product Taxonomy (6,000+ categories)
- **Output**: Category path (e.g., "Apparel > Jewelry > Necklaces")
- **Confidence**: High (deterministic-first reduces LLM calls by 80-90%)
- **Use Case**: Improve product discoverability, marketplace compliance

### 2. **Attribute Extraction Agent** 📋
- **Purpose**: Extract structured attributes (material, size, color, etc.)
- **Output**: Key-value pairs with confidence scores
- **Confidence**: Medium-High (70-85% deterministic accuracy)
- **Use Case**: Standardize product data, enable filtering/search

### 3. **Attribute Normalization Agent** ✅
- **Purpose**: Normalize attribute values to standard formats
- **Output**: Cleaned attributes (e.g., "5 lbs" → "5.0 pounds")
- **Confidence**: High (deterministic rules + LLM validation)
- **Use Case**: Data consistency, comparison shopping

### 4. **Bundle Detection Agent** 📦
- **Purpose**: Detect if product is a multi-item bundle or set
- **Output**: Boolean + bundle components
- **Confidence**: Very High (85-95% deterministic)
- **Use Case**: Accurate pricing, shipping calculations

### 5. **Hazmat Detection Agent** ⚠️
- **Purpose**: Identify hazardous materials (batteries, chemicals, etc.)
- **Output**: Hazmat classification + shipping restrictions
- **Confidence**: Very High (90-95% deterministic)
- **Use Case**: Shipping compliance, marketplace requirements

### 6. **Content Generation Agent** ✍️
- **Purpose**: Generate optimized product titles, descriptions, SEO metadata
- **Output**: Enhanced title, description, meta tags, FAQ
- **Confidence**: High (AI-powered, human-reviewable)
- **Use Case**: Improve SEO, increase conversions

### 7. **Schema Generation Agent** 🗂️
- **Purpose**: Create structured data schema for products
- **Output**: JSON-LD schema for rich snippets
- **Confidence**: High (category-specific schemas)
- **Use Case**: SEO, Google Shopping compatibility

### 8. **Enrichment Agent** 🌐
- **Purpose**: Add missing data (dimensions, images, specs) via external sources
- **Output**: Enhanced product data from manufacturer sites, APIs
- **Confidence**: Medium (depends on source availability)
- **Use Case**: Complete product information, reduce manual entry

### 9. **Compliance Agent** 📜
- **Purpose**: Map products to tax codes (Avalara), regulatory compliance
- **Output**: Tax codes, compliance flags
- **Confidence**: High (75-85% deterministic)
- **Use Case**: Tax automation, legal compliance

### 10. **Brand Compliance Agent** 🛡️
- **Purpose**: Verify brand authenticity, detect policy violations
- **Output**: Brand verification, policy flags
- **Confidence**: Medium-High (rule-based + AI)
- **Use Case**: Marketplace compliance, brand protection

---

## UI Components Required

### 1. **Agent Selection Dashboard** 🎛️

**Location**: Main app page after installation

**Components**:
- **Agent Cards Grid**: 3 columns, responsive
- **Search/Filter**: Filter by category (SEO, Data Quality, Compliance)
- **Bulk Actions**: "Enable All", "Trial All"

**Agent Card Layout**:
```
┌─────────────────────────────────────────┐
│ 🏷️ Taxonomy Agent           [Toggle]   │
│                                          │
│ Classify products into 6000+ categories  │
│                                          │
│ Pricing: $0.02/product                   │
│ Est. Monthly: $45 (for 224 products)     │
│                                          │
│ Status: ⚪ Not Active                    │
│                                          │
│ [Try on 10 Products] [Activate]          │
│ [View Details]                           │
└─────────────────────────────────────────┘
```

### 2. **Agent Details Modal** 📄

Opens when clicking "View Details"

**Sections**:
- **Description**: What it does, how it works
- **Sample Output**: Show example before/after
- **Pricing Breakdown**: Per-product cost, volume discounts
- **Performance Metrics**: Accuracy, speed, LLM usage
- **Configuration Options**: Confidence thresholds, data sources

**Example**:
```
┌─────────────────────────────────────────────────────────┐
│ 🏷️ Taxonomy Agent                         [Close ×]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ WHAT IT DOES                                             │
│ Automatically classifies products into Google's          │
│ standardized taxonomy (6000+ categories). Uses           │
│ deterministic analysis first (80% accuracy), then        │
│ AI fallback for complex cases.                           │
│                                                          │
│ SAMPLE OUTPUT                                            │
│ Before: "Blue diamond necklace"                          │
│ After:  "Jewelry & Accessories > Jewelry > Necklaces"   │
│                                                          │
│ PRICING                                                  │
│ • First 1,000 products:  $0.02/product                   │
│ • 1,001-10,000:          $0.015/product                  │
│ • 10,001+:               $0.01/product                   │
│                                                          │
│ YOUR ESTIMATE (224 products): $4.48/month                │
│                                                          │
│ PERFORMANCE                                              │
│ • Accuracy: 95%+                                         │
│ • Speed: ~1-2 sec/product                                │
│ • LLM Calls: 20% (80% deterministic)                     │
│                                                          │
│ [Try on 10 Products] [Activate Agent]                    │
└─────────────────────────────────────────────────────────┘
```

### 3. **Trial Mode Interface** 🧪

**Workflow**:
1. User clicks "Try on 10 Products"
2. Modal opens: "Select products or use random sample"
3. Progress bar during processing
4. Results comparison view

**Results View**:
```
┌─────────────────────────────────────────────────────────┐
│ Trial Results: Taxonomy Agent (10 products)              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ✅ 8/10 products successfully classified                 │
│ ⚠️  2/10 products need review                            │
│                                                          │
│ PRODUCT RESULTS:                                         │
│                                                          │
│ 1. Blue Diamond Necklace                                 │
│    Original: No category                                 │
│    New: Jewelry & Accessories > Necklaces                │
│    Confidence: 95%                                       │
│    [✓ Apply] [× Reject]                                  │
│                                                          │
│ 2. Diamond Tennis Bracelet                               │
│    Original: No category                                 │
│    New: Jewelry & Accessories > Bracelets                │
│    Confidence: 92%                                       │
│    [✓ Apply] [× Reject]                                  │
│                                                          │
│ ... (8 more products) ...                                │
│                                                          │
│ [Apply All] [Activate for All Products] [Cancel]         │
└─────────────────────────────────────────────────────────┘
```

### 4. **Agent Logs Viewer** 📊

**Features**:
- Real-time log streaming
- Filter by agent, status, timestamp
- Export to CSV
- Detailed error messages

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│ Agent Operation Logs                    [Export CSV]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Filters: [All Agents ▼] [All Status ▼] [Last 7 days ▼] │
│                                                          │
│ Timestamp         Agent          Product      Status     │
│ ────────────────────────────────────────────────────────│
│ 2026-02-12 14:32  Taxonomy      SKU-001      ✅ Success │
│ 2026-02-12 14:32  Attributes    SKU-001      ✅ Success │
│ 2026-02-12 14:33  Content       SKU-002      ⚠️  Warning│
│ 2026-02-12 14:33  Taxonomy      SKU-003      ❌ Failed  │
│                                                          │
│ [Click row for details]                                  │
│                                                          │
│ Showing 50 of 1,247 operations                           │
│ [Load More]                                              │
└─────────────────────────────────────────────────────────┘
```

### 5. **Pricing & Plans Page** 💳

**Features**:
- Compare pricing tiers (Starter, Pro, Enterprise)
- Calculate estimated costs based on catalog size
- Subscription management

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│ Choose Your Plan                                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  STARTER         PRO             ENTERPRISE              │
│  $49/month       $199/month      Custom                  │
│                                                          │
│  • 3 agents      • 7 agents      • All 10 agents        │
│  • 500 products  • 5,000 prod.   • Unlimited            │
│  • Basic support • Priority      • Dedicated support    │
│  • Email only    • Chat & Email  • Phone + Slack        │
│                                                          │
│  [Select]        [Select]        [Contact Sales]        │
│                                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Your Catalog: 224 products                               │
│ Recommended: Starter Plan                                │
│                                                          │
│ Estimated Monthly Cost: $49                              │
│ (Includes 3 agents of your choice)                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 6. **Product Tutorials Section** 📚

**Content**:
- Video walkthroughs for each agent
- Best practices guides
- FAQ
- Setup checklists

---

## Agent Configuration Interface

### Configuration Options per Agent

Each agent should have configurable parameters:

**Example: Taxonomy Agent Config**
```json
{
  "agent_id": "taxonomy",
  "enabled": true,
  "confidence_threshold": 0.75,
  "fallback_to_llm": true,
  "auto_apply": false,
  "notification_on_low_confidence": true,
  "batch_size": 50,
  "schedule": {
    "auto_run_on_new_products": true,
    "periodic_reprocess": false
  }
}
```

**UI for Configuration**:
```
┌─────────────────────────────────────────────┐
│ Configure: Taxonomy Agent         [Save]    │
├─────────────────────────────────────────────┤
│                                              │
│ Confidence Threshold: [========|---] 75%     │
│ Lower = more LLM calls, higher accuracy      │
│                                              │
│ ☑ Enable LLM fallback for low confidence    │
│ ☐ Auto-apply results (no review)            │
│ ☑ Notify me on low confidence results       │
│                                              │
│ Batch Processing                             │
│ Process in batches of: [50 ▼] products      │
│                                              │
│ Automation                                   │
│ ☑ Auto-run on new products                  │
│ ☐ Reprocess all products monthly            │
│                                              │
│ [Save Configuration]                         │
└─────────────────────────────────────────────┘
```

---

## Pricing Tiers

### Proposed Pricing Model

**Tier 1: Starter** - $49/month
- 3 agents (customer choice)
- Up to 500 products
- Basic support (email)
- Trial: 10 products per agent

**Tier 2: Professional** - $199/month
- 7 agents (customer choice)
- Up to 5,000 products
- Priority support (chat + email)
- Trial: 20 products per agent
- Advanced logs & analytics

**Tier 3: Enterprise** - Custom pricing
- All 10 agents
- Unlimited products
- Dedicated support (phone + Slack)
- Custom integrations
- API access
- SLA guarantees

### Per-Agent Pricing (À la carte)

If not using tier subscriptions:

| Agent | Price per Product | Volume Discount |
|-------|------------------|-----------------|
| Taxonomy | $0.02 | 50% off at 10K+ |
| Attributes | $0.03 | 50% off at 10K+ |
| Normalization | $0.01 | 50% off at 10K+ |
| Bundle Detection | $0.01 | 50% off at 10K+ |
| Hazmat | $0.01 | 50% off at 10K+ |
| Content Gen | $0.05 | 40% off at 10K+ |
| Schema | $0.02 | 50% off at 10K+ |
| Enrichment | $0.04 | 40% off at 10K+ |
| Compliance | $0.02 | 50% off at 10K+ |
| Brand Check | $0.02 | 50% off at 10K+ |

**Monthly Calculation for 224 products** (all agents):
- Taxonomy: $4.48
- Attributes: $6.72
- Normalization: $2.24
- Bundle: $2.24
- Hazmat: $2.24
- Content: $11.20
- Schema: $4.48
- Enrichment: $8.96
- Compliance: $4.48
- Brand: $4.48
- **Total**: ~$51.52/month

---

## Trial Mode Implementation

### User Flow

1. **Agent Selection**
   - User browses agent cards
   - Clicks "Try on 10 Products"

2. **Product Selection**
   ```
   Choose how to select products:
   • Random sample (10 products)
   • Manual selection (pick from list)
   • Smart selection (diverse sample)
   ```

3. **Processing**
   - Real-time progress bar
   - Estimated time display
   - Option to cancel

4. **Results Review**
   - Side-by-side comparison (before/after)
   - Confidence scores
   - Accept/reject per product

5. **Activation Decision**
   - Review trial results
   - See estimated monthly cost
   - Activate agent for all products

### Backend API Calls

**Trial Endpoint**:
```http
POST /api/agents/trial
{
  "agent_id": "taxonomy",
  "product_ids": ["9343074173172", "9343074238708", ...],
  "config": {
    "confidence_threshold": 0.75
  }
}

Response:
{
  "trial_id": "trial_abc123",
  "status": "processing",
  "estimated_completion": "2026-02-12T14:35:00Z"
}
```

**Poll for Results**:
```http
GET /api/agents/trial/trial_abc123

Response:
{
  "trial_id": "trial_abc123",
  "status": "completed",
  "results": [
    {
      "product_id": "9343074173172",
      "original": {...},
      "enriched": {...},
      "confidence": 0.95,
      "changes": [...]
    }
  ]
}
```

---

## Technical Architecture

### Tech Stack

**Frontend**:
- **Framework**: Shopify Polaris (React components)
- **Language**: TypeScript
- **State Management**: React Context + TanStack Query
- **Styling**: Polaris CSS + Tailwind
- **Build Tool**: Vite

**Backend** (handled by Soumya's team):
- Segment APIs for client/project/dataset registration
- Temporal workflows for catalog ingestion
- Catalog agent backend

**Your Responsibilities** (Frontend + Integration):
- Shopify app UI (Polaris components)
- Agent selection/configuration interfaces
- Trial mode implementation
- Pricing calculator
- Logs viewer
- API integration with Segment APIs

### Folder Structure

```
shopify_app/
├── frontend/                    # Shopify app frontend
│   ├── pages/
│   │   ├── Dashboard.tsx       # Main agent selection
│   │   ├── AgentDetails.tsx    # Agent detail modal
│   │   ├── TrialMode.tsx       # Trial interface
│   │   ├── Logs.tsx            # Agent logs viewer
│   │   ├── Pricing.tsx         # Plans & pricing
│   │   └── Settings.tsx        # App settings
│   ├── components/
│   │   ├── AgentCard.tsx       # Agent card component
│   │   ├── TrialResults.tsx    # Trial results view
│   │   ├── LogsTable.tsx       # Logs table
│   │   ├── PricingCalculator.tsx
│   │   └── ConfigEditor.tsx    # Agent config UI
│   ├── hooks/
│   │   ├── useAgents.ts        # Agent management
│   │   ├── useTrial.ts         # Trial mode logic
│   │   └── useSegmentAPI.ts    # Segment API integration
│   ├── services/
│   │   ├── segmentAPI.ts       # Segment API client
│   │   └── shopifyAPI.ts       # Shopify API client
│   └── types/
│       ├── agents.ts           # Agent type definitions
│       └── trial.ts            # Trial type definitions
├── backend/                     # Shopify app backend (Node/Python)
│   ├── api/
│   │   ├── agents.ts           # Agent CRUD
│   │   ├── trial.ts            # Trial endpoints
│   │   └── segment.ts          # Segment API proxy
│   └── webhooks/
│       └── shopify.ts          # Shopify webhooks
└── docs/
    ├── API.md                  # API documentation
    └── SETUP.md                # Setup instructions
```

---

## API Integration Points

### 1. Segment APIs (Soumya's Backend)

**Register Client**:
```http
POST /api/segment/clients
{
  "shopify_store_id": "paladio-3685",
  "store_url": "paladio-3685.myshopify.com",
  "plan": "starter"
}
```

**Create Project**:
```http
POST /api/segment/projects
{
  "client_id": "client_123",
  "project_name": "Main Catalog",
  "dataset_id": "dataset_456"
}
```

**Trigger Catalog Ingestion**:
```http
POST /api/segment/ingest
{
  "project_id": "project_789",
  "source": "shopify",
  "product_ids": ["9343074173172", ...]
}
```

### 2. Agent Management

**Get Available Agents**:
```http
GET /api/agents

Response:
[
  {
    "agent_id": "taxonomy",
    "name": "Taxonomy Agent",
    "description": "...",
    "pricing": {...},
    "enabled": false,
    "config": {...}
  }
]
```

**Enable Agent**:
```http
POST /api/agents/{agent_id}/enable
{
  "config": {...}
}
```

**Get Agent Logs**:
```http
GET /api/agents/{agent_id}/logs?limit=50&offset=0
```

---

## Implementation Phases

### Phase 1: Foundation 
- ✅ Set up Shopify app project (Polaris + TypeScript)
- ✅ Create basic dashboard layout
- ✅ Implement agent cards grid
- ✅ Build agent details modal
- ✅ Set up Segment API integration

### Phase 2: Agent Management 
- ⏳ Implement agent enable/disable toggles
- ⏳ Build configuration editor for each agent
- ⏳ Create pricing calculator
- ⏳ Integrate with backend agent APIs

### Phase 3: Trial Mode 
- ⏳ Build trial mode UI flow
- ⏳ Implement product selection interface
- ⏳ Create results comparison view
- ⏳ Add accept/reject functionality

### Phase 4: Logs & Analytics 
- ⏳ Build logs viewer with filtering
- ⏳ Add real-time log streaming
- ⏳ Create export functionality
- ⏳ Add analytics dashboard

### Phase 5: Pricing & Plans
- ⏳ Build pricing page
- ⏳ Implement plan selection
- ⏳ Add subscription management
- ⏳ Integrate Shopify billing API

### Phase 6: Polish & Launch 
- ⏳ Add tutorials/onboarding
- ⏳ Implement tooltips and help text
- ⏳ Performance optimization
- ⏳ Testing & bug fixes
- ⏳ Submit to Shopify App Store

---

## Wireframes

### Main Dashboard

```
┌───────────────────────────────────────────────────────────────────┐
│ 🛍️ Catalog Agents for Shopify          [Settings ⚙️] [Help ❓]   │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Your Catalog: 224 products                  Plan: Starter ($49)   │
│ Active Agents: 0/3                          [Upgrade to Pro]      │
│                                                                    │
├───────────────────────────────────────────────────────────────────┤
│ Filters: [All Categories ▼] [All Status ▼]        [Search...  🔍] │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐         │
│ │ 🏷️ Taxonomy    │ │ 📋 Attributes  │ │ ✅ Normalize   │         │
│ │                │ │                │ │                │         │
│ │ $0.02/product  │ │ $0.03/product  │ │ $0.01/product  │         │
│ │ Est: $4.48     │ │ Est: $6.72     │ │ Est: $2.24     │         │
│ │                │ │                │ │                │         │
│ │ ⚪ Inactive     │ │ ⚪ Inactive     │ │ ⚪ Inactive     │         │
│ │ [Try] [Enable] │ │ [Try] [Enable] │ │ [Try] [Enable] │         │
│ └────────────────┘ └────────────────┘ └────────────────┘         │
│                                                                    │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐         │
│ │ 📦 Bundles     │ │ ⚠️  Hazmat      │ │ ✍️  Content    │         │
│ │ ...            │ │ ...            │ │ ...            │         │
│ └────────────────┘ └────────────────┘ └────────────────┘         │
│                                                                    │
│ ... (4 more agent cards) ...                                      │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Review with Vamsi**: Get approval on agent list, pricing, UI design
2. **Wait for PRD**: Use Vamsi's PRD to finalize feature scope
3. **Set up project**: Initialize Shopify app with Polaris
4. **Build Phase 1**: Dashboard + agent cards
5. **Integrate Segment APIs**: Connect to Soumya's backend

---

## Questions for Vamsi

1. **Agent Selection**: Confirm which 10 agents to expose (vs. all 29 modules)
2. **Pricing Model**: Tier-based or à la carte or both?
3. **Trial Limits**: 5, 10, or 20 products for trial?
4. **Auto-apply**: Should agents auto-apply results or always require review?
5. **Webhooks**: Should we listen to Shopify product create/update webhooks?
6. **Backend API**: Is Segment API the correct integration point or different?

---

**End of Document**
