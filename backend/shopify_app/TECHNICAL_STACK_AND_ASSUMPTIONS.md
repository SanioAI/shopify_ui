# Technical Stack & Assumptions - Shopify App UI

**Date**: February 24, 2026  
**App Name**: Catalog Agents  
**Live URL**: https://bindu-ai5.github.io/catalog-agents-ui/

---

## 🔧 Technical Stack

### Frontend
- **HTML5** - Single page application
- **CSS3** - Custom styles + Shopify Polaris CDN
- **Vanilla JavaScript** - No frameworks, pure JS for interactivity
- **Shopify Polaris CSS** - `@shopify/polaris@12.0.0` (via CDN)

### Hosting & Deployment
- **GitHub Pages** - Free static hosting
- **Git** - Version control
- **Repository**: `bindu-ai5/shopify_ui`
- **Live URL**: `https://bindu-ai5.github.io/catalog-agents-ui/`

### Backend (Assumed/Not Yet Built)
- **Soumya's Segment APIs** - For agent execution
- **Shopify Admin API** - For reading/writing products
- **Webhooks** - For tracking new/changed products
- **Metafields** - For storing enriched data in Shopify

---

## 📋 Assumptions Made

### 1. Data & Integration
- ✅ Backend API exists (Soumya's segment APIs) to run agents
- ✅ Shopify store is already connected: `paladio-3685.myshopify.com`
- ✅ Access token available for Shopify Admin API
- ✅ Product data can be read via Shopify API
- ✅ Enriched data written back as metafields with `sanio` namespace

### 2. User Flow
- ✅ Merchants install app from Shopify Admin
- ✅ OAuth handled by Shopify (not built in current HTML)
- ✅ App loads as embedded iframe in Shopify Admin
- ✅ All data is mock/static (no real API calls yet)

### 3. Features (Current UI)
- ✅ Analytics data is **hardcoded** (142 products, $8.35/month, etc.)
- ✅ Buttons show alerts (not connected to real backend)
- ✅ Charts are **static** (no real data)
- ✅ Schedule settings don't persist (no database)
- ✅ "Run Now" button shows confirmation, doesn't actually run

### 4. Architecture
- ✅ **Single-page app** - All 4 pages in one HTML file
- ✅ **Client-side routing** - JavaScript toggles page visibility
- ✅ **No authentication** - Assumes Shopify OAuth handled externally
- ✅ **No state management** - No localStorage, no API calls
- ✅ **No build process** - Direct HTML file, no npm/webpack

### 5. Agent System
- ✅ 10 agents defined (Hazmat, Bundle, Taxonomy, Schema, Extraction, Enrichment, Content, SEO, FAQ Generator, Compliance)
- ✅ Agent logic runs on **backend** (not in UI)
- ✅ UI only **displays** agents and **triggers** execution
- ✅ Each agent has fixed pricing per product
- ✅ Agents write results to Shopify metafields

### 6. Deployment
- ✅ GitHub Pages serves static HTML
- ✅ No server-side rendering
- ✅ No API endpoints in this repo
- ✅ CORS not an issue (static content)
- ✅ Updates via `git push` (auto-deploys in 1-2 min)

### 7. Shopify Integration
- ✅ App registered in Shopify Partners Dashboard
- ✅ App URL points to GitHub Pages
- ✅ App embedded in Shopify Admin (not standalone)
- ✅ Uses Shopify's UI design system (Polaris)
- ✅ OAuth/billing handled by Shopify (not in code)

### 8. Future Backend Needs

When connecting to real backend, we'll need:

**API Endpoints:**
- `/api/agents/list` - Get available agents
- `/api/agents/activate` - Enable an agent
- `/api/agents/run` - Trigger enrichment
- `/api/analytics` - Get metrics (products enriched, costs, etc.)
- `/api/settings` - Save/load settings (schedule, preferences)

**Webhook Listener:**
- Listen for new/changed products from Shopify
- Trigger automatic enrichment based on settings

---

## 📊 Key Assumption Summary

| Assumption | Status | Notes |
|-----------|---------|-------|
| Backend API exists | ⏳ To be built | Soumya's segment APIs |
| Shopify store connected | ✅ Done | `paladio-3685.myshopify.com` |
| OAuth handled by Shopify | ✅ Assumed | Not in HTML code |
| Data is static/mock | ✅ Current | No real API calls yet |
| UI-only (no backend) | ✅ Current | Pure frontend app |
| GitHub Pages hosting | ✅ Done | Free, fast deployment |
| No database needed | ✅ Current | Settings don't persist |
| Agent execution is async | ✅ Assumed | Backend handles processing |

---

## 🎯 Summary

Built a **pure HTML/CSS/JS frontend** hosted on **GitHub Pages**, designed to look like a Shopify app, with **mock data** and **placeholder buttons**, ready to be connected to a real backend API later.

### Current State
- ✅ Professional UI with 4 pages (Dashboard, Analytics, Settings, Agents)
- ✅ Responsive design using Shopify Polaris
- ✅ Interactive elements (navigation, forms, buttons)
- ✅ Static charts and mock analytics data
- ✅ Live on GitHub Pages
- ✅ Accessible in Shopify Admin

### Next Steps
1. Connect to Soumya's backend APIs
2. Replace mock data with real API calls
3. Implement authentication/authorization
4. Add data persistence (settings, preferences)
5. Real-time updates via webhooks
6. Error handling and loading states

---

## 📁 File Structure

```
catalog-agents-ui/
├── index.html          ← Main app (621 lines)
│                         - Dashboard page
│                         - Analytics page (charts, metrics)
│                         - Settings page (run now/schedule)
│                         - Agents page (10 agents grid)
└── package.json        ← Minimal package file
```

---

## 🔗 Resources

- **Live App**: https://bindu-ai5.github.io/catalog-agents-ui/
- **Shopify Store**: paladio-3685.myshopify.com
- **Shopify Admin API**: 2024-01
- **GitHub Repo**: bindu-ai5/shopify_ui
- **Backend API**: http://54.211.133.171 (Soumya's catalog agent API)
