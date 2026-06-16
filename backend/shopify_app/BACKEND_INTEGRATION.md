# Shopify App → Backend Integration

The shopify_app UI is now connected to the catalog agents backend. When customers use the app, they can run enrichment directly.

## How It Works

```
Shopify App (AgentDashboard)  →  api_server.py  →  Catalog Agents API ([http://13.218.58.17](http://13.218.58.17/docs))
         ↓                              ↓
    User clicks                    Fetches products from Shopify
    "Run Enrichment"               Sends to catalog API
                                   Writes enriched data back via shopify_writeback
```

## Setup

### 1. Start the backend

```bash
cd catalog-agentic-system-dependencyinjection
python3 api_server.py
```

The backend runs on **http://localhost:5001** by default (port 5001 avoids macOS AirPlay on 5000).

### 2. Configure the app

When the app loads, it uses `http://localhost:5001` as the default backend URL. You can change it in the "Connect to Catalog Agents Backend" section:

- **Backend URL**: Where api_server.py is running (e.g. `http://localhost:5001` or your deployed URL)
- **Demo mode**: Check this to use existing before-after data (no catalog API key needed)

### 3. Run enrichment

Click **"Run All Active Agents Now"** or the primary **"Run Enrichment"** button. The backend will:

1. Fetch products from Shopify (using credentials in api_server.py)
2. Send them to the catalog API for enrichment
3. Run writeback to push enriched data back to Shopify

## Files Added

| File | Purpose |
|------|---------|
| `api/catalog-api.ts` | API client – test connection, get stats, run enrichment |
| `pages/AgentDashboard.tsx` | Updated with backend URL config, Run enrichment button, connection status |

## For Production

- Deploy `api_server.py` to a server (e.g. AWS, Heroku)
- Set `CATALOG_API_KEY` env var if the catalog API requires auth
- Update the app's backend URL to your deployed API URL
- For multi-tenant: api_server will need to accept store credentials per request (from Shopify OAuth)
