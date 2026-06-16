/**
 * Catalog Agent API Client
 * Connects the Shopify app to api_server.py (which proxies to catalog agents API).
 *
 * Usage:
 * 1. Set backend URL: catalogAPI.setBackendUrl('http://localhost:5001')
 * 2. Call runEnrichment() when user clicks "Run enrichment"
 */

/** Default: Paladio catalog backend. Override with VITE_API_BASE_URL env var. */
const DEFAULT_BACKEND = (import.meta as any).env?.VITE_API_BASE_URL?.replace('/api', '') || 'https://catalog.paladio.ai';

export interface RunEnrichmentOptions {
  limit?: number;
  demo?: boolean;
}

export interface RunEnrichmentResult {
  success: boolean;
  message?: string;
  enriched_count?: number;
  products_processed?: number;
  error?: string;
  demo?: boolean;
}

export interface HealthResult {
  status: string;
  message: string;
}

export interface StatsResult {
  success: boolean;
  stats?: {
    total_products?: number;
    enriched_count?: number;
  };
}

export class CatalogAPI {
  private backendUrl: string | null = null;

  setBackendUrl(url: string | null) {
    this.backendUrl = url;
  }

  getBackendUrl(): string | null {
    return this.backendUrl;
  }

  /** Test connection to backend */
  async testConnection(): Promise<{ ok: boolean; message: string }> {
    const url = this.backendUrl || DEFAULT_BACKEND;
    try {
      const resp = await fetch(`${url.replace(/\/$/, '')}/api/health`);
      const data: HealthResult = await resp.json();
      return { ok: resp.ok, message: data.message || data.status };
    } catch (err) {
      return {
        ok: false,
        message: err instanceof Error ? err.message : 'Connection failed',
      };
    }
  }

  /** Get catalog stats (product count, etc.) */
  async getStats(): Promise<StatsResult> {
    const url = this.backendUrl || DEFAULT_BACKEND;
    try {
      const resp = await fetch(`${url.replace(/\/$/, '')}/api/stats`);
      return await resp.json();
    } catch (err) {
      return { success: false };
    }
  }

  /** Run full enrichment: fetch products → catalog API → writeback to Shopify */
  async runEnrichment(
    options: RunEnrichmentOptions = {},
    onProgress?: (step: string, message: string) => void
  ): Promise<RunEnrichmentResult> {
    const url = this.backendUrl || DEFAULT_BACKEND;
    const base = url.replace(/\/$/, '');
    const body = {
      limit: Math.min(options.limit ?? 50, 25),
      demo: !!options.demo,
    };

    onProgress?.('start', body.demo ? 'Running in demo mode...' : 'Starting enrichment...');

    try {
      const resp = await fetch(`${base}/api/run-enrichment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data: RunEnrichmentResult = await resp.json();

      if (!resp.ok) {
        onProgress?.('error', data.error || `Error ${resp.status}`);
        return { success: false, error: data.error };
      }

      const count = data.enriched_count ?? data.products_processed ?? 0;
      const msg = data.demo
        ? 'Demo complete! Writeback ran with existing data.'
        : `Enrichment complete! ${count} products processed.`;
      onProgress?.('complete', msg);

      return { success: true, ...data };
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Request failed';
      onProgress?.('error', msg);
      return { success: false, error: msg };
    }
  }
}

export const catalogAPI = new CatalogAPI();
