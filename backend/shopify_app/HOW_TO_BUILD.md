# How to Build the Shopify App - Complete Guide

**App Name**: Catalog Agents  
**Tech Stack**: Shopify CLI + Remix + React + TypeScript + Polaris  
**Timeline**: 12 weeks (but can start with MVP in 4 weeks)

---

## 📋 Overview

You'll build a **Shopify App** that runs inside the Shopify Admin dashboard. Merchants install it, configure agents, and see enriched product data.

---

## 🎯 Phase 0: Prerequisites (Before Starting)

### **1. Install Required Software**

```bash
# Check if you have Node.js (v18+)
node --version

# If not installed, download from: https://nodejs.org/

# Check if you have npm
npm --version

# Install Shopify CLI
npm install -g @shopify/cli

# Verify installation
shopify version
```

### **2. Create Shopify Partner Account**

1. Go to: https://partners.shopify.com/
2. Sign up (free)
3. Verify email
4. Complete profile

### **3. Create Development Store** (for testing)

1. In Partners Dashboard → Stores
2. Click "Add store" → "Development store"
3. Name it: "Catalog Agents Test"
4. Select: "Test an app or theme"
5. Create store

### **4. Set Up Version Control**

```bash
# If you don't have Git installed
# Download from: https://git-scm.com/

# Verify Git is installed
git --version

# Create GitHub account if you don't have one
# https://github.com/
```

---

## 🚀 Phase 1: Create the App (Week 1)

### **Step 1: Initialize Shopify App**

```bash
# Navigate to your workspace
cd ~/Desktop/Transfer/OneDrive/Desktop/sanio.ai/catalog_agents_plugins/

# Create new Shopify app
shopify app init

# Follow the prompts:
# ✓ App name: catalog-agents
# ✓ Template: Remix (recommended)
# ✓ Language: TypeScript
```

**This creates:**
```
catalog-agents/
├── app/                  # Frontend (Remix)
│   ├── routes/           # Pages
│   └── components/       # UI components
├── extensions/           # Shopify extensions
├── shopify.app.toml      # App config
└── package.json
```

### **Step 2: Configure the App**

Edit `shopify.app.toml`:

```toml
# App info
name = "Catalog Agents"
client_id = "YOUR_CLIENT_ID"  # Auto-generated
application_url = "https://app.catalogagents.com"  # Placeholder for now

# Scopes (what permissions the app needs)
scopes = "read_products,write_products,read_orders"

[webhooks]
api_version = "2024-01"

[[webhooks.subscriptions]]
topics = ["products/create", "products/update"]
uri = "/api/webhooks/products"
```

### **Step 3: Install Dependencies**

```bash
cd catalog-agents

# Install Shopify Polaris (UI library)
npm install @shopify/polaris @shopify/polaris-icons

# Install additional dependencies
npm install @tanstack/react-query axios

# Install dev dependencies
npm install -D @types/react @types/node
```

### **Step 4: Start Development Server**

```bash
# Start Shopify dev server
shopify app dev

# This will:
# 1. Start local server (port 3000)
# 2. Create a tunnel URL (e.g., https://abc123.trycloudflare.com)
# 3. Open your development store
# 4. Install the app automatically

# Output will show:
# > Your app is running at https://abc123.trycloudflare.com
# > Preview your app: https://admin.shopify.com/store/your-store/apps/catalog-agents
```

**Leave this running in Terminal 1.**

---

## 🎨 Phase 2: Build the UI (Week 2-4)

### **Step 1: Set Up Project Structure**

```bash
# In a new terminal (Terminal 2)
cd catalog-agents/app

# Create folder structure
mkdir -p components services hooks types utils
```

**Final structure:**
```
catalog-agents/app/
├── routes/
│   ├── app._index.tsx         # Dashboard (main page)
│   ├── app.agents.tsx          # Agent management
│   ├── app.trial.tsx           # Trial mode
│   ├── app.logs.tsx            # Logs viewer
│   ├── app.usage.tsx           # Usage & billing
│   └── app.settings.tsx        # Settings
├── components/
│   ├── AgentCard.tsx           # Agent card component
│   ├── TrialModal.tsx          # Trial modal
│   ├── LogsTable.tsx           # Logs table
│   └── UsageDashboard.tsx      # Usage metrics
├── services/
│   ├── agentAPI.ts             # Agent management API
│   ├── shopifyAPI.ts           # Shopify API calls
│   └── segmentAPI.ts           # Backend API (Soumya's)
├── hooks/
│   ├── useAgents.ts            # Agent state
│   └── useTrial.ts             # Trial mode logic
└── types/
    ├── agents.ts               # Type definitions
    └── trial.ts
```

### **Step 2: Create the Main Dashboard**

Create `app/routes/app._index.tsx`:

```typescript
import { useState } from 'react';
import {
  Page,
  Layout,
  Card,
  Text,
  Grid,
  InlineStack,
  BlockStack,
} from '@shopify/polaris';
import { AgentCard } from '../components/AgentCard';

export default function Index() {
  const [agents, setAgents] = useState([
    {
      id: 'taxonomy',
      name: 'Taxonomy Agent',
      icon: '🏷️',
      description: 'Classify products into 6000+ categories',
      pricePerProduct: 0.02,
      status: 'inactive',
      accuracy: 95,
    },
    // ... add other 9 agents
  ]);

  return (
    <Page title="Catalog Agents" subtitle="Enhance your product catalog with AI">
      <Layout>
        <Layout.Section>
          <Card>
            <InlineStack gap="400">
              <BlockStack gap="200">
                <Text as="h3" variant="headingSm">Your Catalog</Text>
                <Text as="p" variant="heading2xl">224</Text>
                <Text as="p" variant="bodySm">products</Text>
              </BlockStack>
              {/* Add more stats */}
            </InlineStack>
          </Card>
        </Layout.Section>

        <Layout.Section>
          <Grid columns={3}>
            {agents.map((agent) => (
              <Grid.Cell key={agent.id}>
                <AgentCard
                  agent={agent}
                  onTry={(id) => console.log('Try', id)}
                  onActivate={(id) => console.log('Activate', id)}
                />
              </Grid.Cell>
            ))}
          </Grid>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

### **Step 3: Copy Agent Card Component**

Copy the `AgentCard.tsx` component I created earlier to:
```
catalog-agents/app/components/AgentCard.tsx
```

### **Step 4: Test Locally**

With `shopify app dev` still running, visit:
```
https://admin.shopify.com/store/your-store/apps/catalog-agents
```

You should see your dashboard!

---

## 🔗 Phase 3: Connect to Backend (Week 5-6)

### **Step 1: Create API Service**

Create `app/services/agentAPI.ts`:

```typescript
const API_BASE = process.env.BACKEND_API_URL || 'http://your-backend-url';

export const agentAPI = {
  // Get all available agents
  async getAgents() {
    const response = await fetch(`${API_BASE}/api/agents`);
    if (!response.ok) throw new Error('Failed to fetch agents');
    return response.json();
  },

  // Enable an agent
  async enableAgent(agentId: string, config: any) {
    const response = await fetch(`${API_BASE}/api/agents/${agentId}/enable`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ config }),
    });
    if (!response.ok) throw new Error('Failed to enable agent');
    return response.json();
  },

  // Start trial mode
  async startTrial(agentId: string, productIds: string[]) {
    const response = await fetch(`${API_BASE}/api/agents/trial`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent_id: agentId, product_ids: productIds }),
    });
    if (!response.ok) throw new Error('Failed to start trial');
    return response.json();
  },

  // Get trial results
  async getTrialResults(trialId: string) {
    const response = await fetch(`${API_BASE}/api/agents/trial/${trialId}`);
    if (!response.ok) throw new Error('Failed to fetch trial results');
    return response.json();
  },

  // Get agent logs
  async getLogs(agentId?: string, limit = 50) {
    const url = agentId
      ? `${API_BASE}/api/agents/${agentId}/logs?limit=${limit}`
      : `${API_BASE}/api/agents/logs?limit=${limit}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch logs');
    return response.json();
  },
};
```

### **Step 2: Use TanStack Query for Data Fetching**

Update `app/routes/app._index.tsx`:

```typescript
import { useQuery } from '@tanstack/react-query';
import { agentAPI } from '../services/agentAPI';

export default function Index() {
  const { data: agents, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: agentAPI.getAgents,
  });

  if (isLoading) return <Spinner />;

  return (
    <Page title="Catalog Agents">
      {/* Render agents */}
    </Page>
  );
}
```

### **Step 3: Set Up Environment Variables**

Create `.env`:

```bash
# Backend API (Soumya's)
BACKEND_API_URL=http://your-backend-url
BACKEND_API_KEY=your-api-key

# Shopify (auto-filled by Shopify CLI)
SHOPIFY_API_KEY=your-shopify-api-key
SHOPIFY_API_SECRET=your-shopify-api-secret
```

---

## 🧪 Phase 4: Testing (Week 7-8)

### **Test in Development Store**

1. **Install the app** in your dev store (done automatically by `shopify app dev`)
2. **Test all features**:
   - Agent selection
   - Trial mode
   - Logs viewer
   - Usage tracking

### **Test with Real Data**

Use your Shopify store (paladio-3685):
1. Connect to your real store
2. Test with your 224 products
3. Verify metafields are written correctly

---

## 🚀 Phase 5: Deployment (Week 9-10)

### **Option A: Deploy to Vercel** (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# ✓ Project name: catalog-agents
# ✓ Framework: Remix
# ✓ Deploy

# You'll get a URL like:
# https://catalog-agents.vercel.app
```

### **Option B: Deploy to Railway**

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project"
4. Select your GitHub repo
5. Railway auto-detects Remix
6. Click "Deploy"
7. Get URL: `https://catalog-agents.up.railway.app`

### **Update App URL in Dev Dashboard**

1. Go to https://partners.shopify.com/
2. Find your app
3. Go to Configuration
4. Update "App URL" to your production URL
5. Save

---

## 📱 Phase 6: Submit to Shopify App Store (Week 11-12)

### **Step 1: Prepare Assets**

- [ ] App icon (1200×1200px)
- [ ] 5-6 screenshots
- [ ] App description
- [ ] Privacy policy
- [ ] Support email

### **Step 2: Submit App**

1. In Partners Dashboard → Apps → Your App
2. Click "Submit for Review"
3. Fill out listing details
4. Upload assets
5. Submit

Shopify reviews in 5-10 business days.

---

## 🛠️ Development Commands

```bash
# Start dev server
shopify app dev

# Build for production
npm run build

# Deploy to Vercel
vercel --prod

# View logs
shopify app logs

# Update app config
shopify app config push

# Generate new page
shopify app generate page
```

---

## 📚 Resources

### **Shopify Documentation**
- App development: https://shopify.dev/docs/apps
- Polaris components: https://polaris.shopify.com/
- App Bridge: https://shopify.dev/docs/api/app-bridge

### **Remix Documentation**
- Remix docs: https://remix.run/docs
- Tutorials: https://remix.run/docs/en/main/tutorials

### **Our Documentation**
- UI Plan: `shopify_app/SHOPIFY_APP_UI_PLAN.md`
- Agents List: `shopify_app/AGENTS_LIST.md`
- Setup Checklist: `shopify_app/SETUP_CHECKLIST.md`

---

## 🎯 MVP (Minimum Viable Product) - 4 Weeks

If you want to launch faster, build this first:

### **Week 1: Setup + Dashboard**
- [ ] Create app with Shopify CLI
- [ ] Build main dashboard
- [ ] Display 10 agent cards (hardcoded data)

### **Week 2: Agent Management**
- [ ] Enable/disable agents
- [ ] Basic configuration
- [ ] Connect to backend API

### **Week 3: Trial Mode**
- [ ] "Try on 10 Products" feature
- [ ] Show before/after results
- [ ] Activation flow

### **Week 4: Deployment**
- [ ] Deploy to Vercel
- [ ] Test in production
- [ ] Submit to App Store

**Skip for MVP:**
- Logs viewer (add later)
- Usage tracking (add later)
- Advanced analytics (add later)

---

## ❓ Troubleshooting

### **"shopify: command not found"**
```bash
npm install -g @shopify/cli
```

### **"Cannot connect to development store"**
- Check if dev server is running (`shopify app dev`)
- Verify store URL in `shopify.app.toml`

### **"Module not found"**
```bash
npm install
```

### **Changes not reflecting**
- Restart dev server
- Clear browser cache
- Check for TypeScript errors

---

## 🎉 Summary

### **Complete Process:**
1. ✅ Install prerequisites (Node.js, Shopify CLI)
2. ✅ Create Shopify Partner account
3. ✅ Run `shopify app init` to create app
4. ✅ Build UI with React + Polaris
5. ✅ Connect to backend APIs (Soumya's)
6. ✅ Test in development store
7. ✅ Deploy to Vercel/Railway
8. ✅ Submit to Shopify App Store

### **Total Timeline:**
- **MVP**: 4 weeks
- **Complete**: 12 weeks

### **Next Steps:**
1. Install Node.js and Shopify CLI
2. Run `shopify app init`
3. Start building the dashboard
4. Copy the AgentCard component I created

---

**Ready to start? Let me know if you need help with any specific step!** 🚀
