import React, { useState, useEffect } from 'react';
import {
  Page,
  Layout,
  Card,
  Text,
  InlineStack,
  BlockStack,
  TextField,
  Button,
  Badge,
  Select,
  Grid,
  Checkbox,
  Banner,
} from '@shopify/polaris';
import { AgentCard, Agent } from '../components/AgentCard';
import { catalogAPI } from '../api/catalog-api';

const BACKEND_URL_KEY = 'catalog_backend_url';
const DEFAULT_BACKEND = 'http://localhost:5001';

// Mock data - replace with API calls
const MOCK_AGENTS: Agent[] = [
  {
    id: 'hazmat',
    name: 'Hazmat Agent',
    icon: '⚠️',
    description: 'Detect hazardous materials and shipping restrictions for compliance',
    pricePerProduct: 0.01,
    estimatedMonthlyCost: 2.24,
    status: 'inactive',
    accuracy: 93,
    category: 'compliance',
  },
  {
    id: 'bundle',
    name: 'Bundle Agent',
    icon: '📦',
    description: 'Detect multi-item bundles and product sets for accurate pricing',
    pricePerProduct: 0.01,
    estimatedMonthlyCost: 2.24,
    status: 'inactive',
    accuracy: 90,
    category: 'data-quality',
  },
  {
    id: 'taxonomy',
    name: 'Taxonomy Agent',
    icon: '🏷️',
    description: 'Classify products into 6000+ Google Product Taxonomy categories',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'active',
    accuracy: 95,
    category: 'data-quality',
  },
  {
    id: 'schema',
    name: 'Schema Agent',
    icon: '🗂️',
    description: 'Generate structured data (Schema.org) for rich snippets and SEO',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'inactive',
    accuracy: 91,
    category: 'seo',
  },
  {
    id: 'extraction',
    name: 'Extraction Agent',
    icon: '📋',
    description: 'Extract structured attributes (material, size, color, etc.) from product data',
    pricePerProduct: 0.03,
    estimatedMonthlyCost: 6.72,
    status: 'trial',
    accuracy: 85,
    category: 'data-quality',
  },
  {
    id: 'enrichment',
    name: 'Enrichment Agent',
    icon: '🌐',
    description: 'Add missing product data from manufacturer sites and external sources',
    pricePerProduct: 0.04,
    estimatedMonthlyCost: 8.96,
    status: 'inactive',
    accuracy: 78,
    category: 'data-quality',
  },
  {
    id: 'content',
    name: 'Content Agent',
    icon: '✍️',
    description: 'Generate optimized product titles and descriptions',
    pricePerProduct: 0.05,
    estimatedMonthlyCost: 11.2,
    status: 'inactive',
    accuracy: 88,
    category: 'seo',
  },
  {
    id: 'seo',
    name: 'SEO Agent',
    icon: '🔍',
    description: 'Generate SEO metadata (meta title, meta description, keywords)',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'inactive',
    accuracy: 85,
    category: 'seo',
  },
  {
    id: 'faq',
    name: 'FAQ Generator Agent',
    icon: '❓',
    description: 'Generate frequently asked questions and answers for products',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'inactive',
    accuracy: 82,
    category: 'seo',
  },
  {
    id: 'compliance',
    name: 'Compliance Agent',
    icon: '📜',
    description: 'Map products to tax codes (Avalara) and regulatory compliance',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'inactive',
    accuracy: 85,
    category: 'compliance',
  },
];

export const AgentDashboard: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const [totalProducts, setTotalProducts] = useState(224);
  const [backendUrl, setBackendUrl] = useState(() =>
    typeof window !== 'undefined' ? localStorage.getItem(BACKEND_URL_KEY) || DEFAULT_BACKEND : DEFAULT_BACKEND
  );
  const [demoMode, setDemoMode] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [runMessage, setRunMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Initialize backend URL and load stats
  useEffect(() => {
    const url = backendUrl || DEFAULT_BACKEND;
    catalogAPI.setBackendUrl(url);
    if (typeof window !== 'undefined') {
      localStorage.setItem(BACKEND_URL_KEY, url);
    }
    catalogAPI.getStats().then((res) => {
      if (res.success && res.stats?.total_products != null) {
        setTotalProducts(res.stats.total_products);
      }
    });
  }, [backendUrl]);

  const handleSaveBackendUrl = () => {
    const url = backendUrl?.trim() || DEFAULT_BACKEND;
    setBackendUrl(url);
    catalogAPI.setBackendUrl(url);
    if (typeof window !== 'undefined') {
      localStorage.setItem(BACKEND_URL_KEY, url);
    }
  };

  const handleTestConnection = async () => {
    setConnectionStatus('Testing...');
    const { ok, message } = await catalogAPI.testConnection();
    setConnectionStatus(ok ? `✓ ${message}` : `✗ ${message}`);
  };

  const handleRunEnrichment = async () => {
    setIsRunning(true);
    setRunMessage(null);
    try {
      const result = await catalogAPI.runEnrichment(
        { limit: 25, demo: demoMode },
        (step, msg) => console.log(`[${step}] ${msg}`)
      );
      if (result.success) {
        setRunMessage({
          type: 'success',
          text: result.message || 'Enrichment completed! Products updated in Shopify.',
        });
        catalogAPI.getStats().then((res) => {
          if (res.success && res.stats?.total_products != null) {
            setTotalProducts(res.stats.total_products);
          }
        });
      } else {
        setRunMessage({ type: 'error', text: result.error || 'Enrichment failed' });
      }
    } catch (err) {
      setRunMessage({
        type: 'error',
        text: err instanceof Error ? err.message : 'Request failed. Is api_server.py running?',
      });
    } finally {
      setIsRunning(false);
    }
  };
  const activePlan = 'Starter';
  const maxAgents = 3;
  const activeAgentCount = MOCK_AGENTS.filter((a) => a.status === 'active').length;

  // Filter agents
  const filteredAgents = MOCK_AGENTS.filter((agent) => {
    const matchesSearch =
      searchQuery === '' ||
      agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory =
      categoryFilter === 'all' || agent.category === categoryFilter;

    const matchesStatus =
      statusFilter === 'all' || agent.status === statusFilter;

    return matchesSearch && matchesCategory && matchesStatus;
  });

  // Calculate total estimated cost
  const totalEstimatedCost = MOCK_AGENTS.reduce(
    (sum, agent) => (agent.status === 'active' ? sum + agent.estimatedMonthlyCost : sum),
    0
  );

  const handleTryAgent = (agentId: string) => {
    console.log('Try agent:', agentId);
    // TODO: Open trial modal
  };

  const handleActivateAgent = (agentId: string) => {
    console.log('Activate agent:', agentId);
    // TODO: Call API to activate agent
  };

  const handleViewDetails = (agentId: string) => {
    console.log('View details:', agentId);
    // TODO: Open agent details modal
  };

  return (
    <Page
      title="Catalog Agents"
      subtitle={`Enhance your product catalog with AI-powered agents`}
      primaryAction={{
        content: 'Run Enrichment',
        onAction: handleRunEnrichment,
        loading: isRunning,
      }}
      secondaryActions={[
        {
          content: 'View Logs',
          onAction: () => console.log('View logs'),
        },
        {
          content: 'Help',
          onAction: () => console.log('Help'),
        },
      ]}
    >
      <Layout>
        {/* Backend connection & Run enrichment */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd">
                Connect to Catalog Agents Backend
              </Text>
              <Text as="p" variant="bodyMd" tone="subdued">
                The backend (api_server.py) fetches your Shopify products, sends them to the catalog API for enrichment, then writes results back to Shopify.
              </Text>
              <InlineStack gap="200" blockAlign="center">
                <div style={{ flex: 1, minWidth: 200 }}>
                  <TextField
                    label="Backend URL"
                    value={backendUrl}
                    onChange={setBackendUrl}
                    placeholder="http://localhost:5001"
                    autoComplete="off"
                  />
                </div>
                <Button onClick={handleSaveBackendUrl}>Save</Button>
                <Button variant="secondary" onClick={handleTestConnection}>
                  Test Connection
                </Button>
              </InlineStack>
              {connectionStatus && (
                <Text as="p" variant="bodySm" tone="subdued">
                  {connectionStatus}
                </Text>
              )}
              <Checkbox
                label="Demo mode — Use existing enriched data (no catalog API key needed)"
                checked={demoMode}
                onChange={setDemoMode}
              />
              <InlineStack gap="200">
                <Button variant="primary" onClick={handleRunEnrichment} loading={isRunning}>
                  Run All Active Agents Now
                </Button>
              </InlineStack>
              {runMessage && (
                <Banner tone={runMessage.type === 'success' ? 'success' : 'critical'} onDismiss={() => setRunMessage(null)}>
                  {runMessage.text}
                </Banner>
              )}
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Overview Cards */}
        <Layout.Section>
          <InlineStack gap="400">
            <Card>
              <BlockStack gap="200">
                <Text as="h3" variant="headingSm" tone="subdued">
                  Your Catalog
                </Text>
                <Text as="p" variant="heading2xl" fontWeight="bold">
                  {totalProducts}
                </Text>
                <Text as="p" variant="bodySm" tone="subdued">
                  products
                </Text>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="200">
                <Text as="h3" variant="headingSm" tone="subdued">
                  Active Agents
                </Text>
                <InlineStack gap="100" blockAlign="baseline">
                  <Text as="p" variant="heading2xl" fontWeight="bold">
                    {activeAgentCount}
                  </Text>
                  <Text as="p" variant="headingMd" tone="subdued">
                    / {maxAgents}
                  </Text>
                </InlineStack>
                <Text as="p" variant="bodySm" tone="subdued">
                  {activePlan} Plan
                </Text>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="200">
                <Text as="h3" variant="headingSm" tone="subdued">
                  Estimated Cost
                </Text>
                <Text as="p" variant="heading2xl" fontWeight="bold">
                  ${totalEstimatedCost.toFixed(2)}
                </Text>
                <Text as="p" variant="bodySm" tone="subdued">
                  per month
                </Text>
              </BlockStack>
            </Card>

            <Card>
              <BlockStack gap="200">
                <Text as="h3" variant="headingSm" tone="subdued">
                  Current Plan
                </Text>
                <Badge tone="success">{activePlan}</Badge>
                <Button size="slim" variant="plain">
                  Upgrade to Pro →
                </Button>
              </BlockStack>
            </Card>
          </InlineStack>
        </Layout.Section>

        {/* Filters */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <InlineStack gap="400" align="space-between">
                <div style={{ flexGrow: 1 }}>
                  <TextField
                    label=""
                    value={searchQuery}
                    onChange={setSearchQuery}
                    placeholder="Search agents..."
                    autoComplete="off"
                    clearButton
                    onClearButtonClick={() => setSearchQuery('')}
                  />
                </div>
                <Select
                  label="Category"
                  options={[
                    { label: 'All Categories', value: 'all' },
                    { label: 'Data Quality', value: 'data-quality' },
                    { label: 'SEO', value: 'seo' },
                    { label: 'Compliance', value: 'compliance' },
                  ]}
                  value={categoryFilter}
                  onChange={setCategoryFilter}
                />
                <Select
                  label="Status"
                  options={[
                    { label: 'All Status', value: 'all' },
                    { label: 'Active', value: 'active' },
                    { label: 'Trial', value: 'trial' },
                    { label: 'Inactive', value: 'inactive' },
                  ]}
                  value={statusFilter}
                  onChange={setStatusFilter}
                />
              </InlineStack>
            </BlockStack>
          </Card>
        </Layout.Section>

        {/* Agent Cards Grid */}
        <Layout.Section>
          <Grid>
            {filteredAgents.map((agent) => (
              <Grid.Cell key={agent.id} columnSpan={{ xs: 6, sm: 6, md: 4, lg: 4, xl: 4 }}>
                <AgentCard
                  agent={agent}
                  totalProducts={totalProducts}
                  onTry={handleTryAgent}
                  onActivate={handleActivateAgent}
                  onViewDetails={handleViewDetails}
                />
              </Grid.Cell>
            ))}
          </Grid>

          {filteredAgents.length === 0 && (
            <Card>
              <BlockStack gap="400" inlineAlign="center">
                <Text as="p" variant="bodyMd" tone="subdued">
                  No agents found matching your filters.
                </Text>
                <Button
                  onClick={() => {
                    setSearchQuery('');
                    setCategoryFilter('all');
                    setStatusFilter('all');
                  }}
                >
                  Clear Filters
                </Button>
              </BlockStack>
            </Card>
          )}
        </Layout.Section>

        {/* Quick Actions */}
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd">
                Quick Actions
              </Text>
              <InlineStack gap="200">
                <Button>View Agent Logs</Button>
                <Button>Download Report</Button>
                <Button>Schedule Demo</Button>
              </InlineStack>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
};

export default AgentDashboard;
