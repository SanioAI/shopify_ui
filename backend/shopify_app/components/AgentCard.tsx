import React, { useState } from 'react';
import {
  Card,
  Badge,
  Button,
  Text,
  Box,
  InlineStack,
  BlockStack,
  Icon,
} from '@shopify/polaris';
import {
  CheckCircleIcon,
  CircleAlertIcon,
  CircleDisabledIcon,
} from '@shopify/polaris-icons';

export interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  pricePerProduct: number;
  estimatedMonthlyCost: number;
  status: 'active' | 'inactive' | 'trial';
  accuracy: number;
  category: 'seo' | 'data-quality' | 'compliance';
}

interface AgentCardProps {
  agent: Agent;
  totalProducts: number;
  onTry: (agentId: string) => void;
  onActivate: (agentId: string) => void;
  onViewDetails: (agentId: string) => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({
  agent,
  totalProducts,
  onTry,
  onActivate,
  onViewDetails,
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const getStatusBadge = () => {
    switch (agent.status) {
      case 'active':
        return (
          <Badge tone="success" icon={CheckCircleIcon}>
            Active
          </Badge>
        );
      case 'trial':
        return (
          <Badge tone="attention" icon={CircleAlertIcon}>
            Trial Mode
          </Badge>
        );
      case 'inactive':
      default:
        return (
          <Badge tone="info" icon={CircleDisabledIcon}>
            Inactive
          </Badge>
        );
    }
  };

  const getCategoryColor = () => {
    switch (agent.category) {
      case 'seo':
        return '#2E7D32'; // Green
      case 'data-quality':
        return '#1976D2'; // Blue
      case 'compliance':
        return '#F57C00'; // Orange
      default:
        return '#616161'; // Gray
    }
  };

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        transition: 'transform 0.2s',
        transform: isHovered ? 'translateY(-4px)' : 'translateY(0)',
      }}
    >
      <Card>
        <BlockStack gap="400">
          {/* Header with Icon and Status */}
          <InlineStack align="space-between" blockAlign="start">
            <InlineStack gap="200" blockAlign="center">
              <Box
                padding="200"
                background="bg-surface-secondary"
                borderRadius="200"
              >
                <Text as="span" variant="headingLg">
                  {agent.icon}
                </Text>
              </Box>
              <BlockStack gap="100">
                <Text as="h3" variant="headingMd" fontWeight="semibold">
                  {agent.name}
                </Text>
                <Box
                  padding="050"
                  paddingInlineStart="200"
                  paddingInlineEnd="200"
                  background="bg-surface-secondary"
                  borderRadius="100"
                >
                  <Text
                    as="span"
                    variant="bodySm"
                    tone="subdued"
                    fontWeight="medium"
                  >
                    {agent.category.replace('-', ' ').toUpperCase()}
                  </Text>
                </Box>
              </BlockStack>
            </InlineStack>
            {getStatusBadge()}
          </InlineStack>

          {/* Description */}
          <Text as="p" variant="bodyMd" tone="subdued">
            {agent.description}
          </Text>

          {/* Pricing */}
          <BlockStack gap="200">
            <InlineStack gap="100" blockAlign="baseline">
              <Text as="span" variant="bodyMd" tone="subdued">
                Pricing:
              </Text>
              <Text as="span" variant="bodyMd" fontWeight="semibold">
                ${agent.pricePerProduct.toFixed(3)}/product
              </Text>
            </InlineStack>
            <InlineStack gap="100" blockAlign="baseline">
              <Text as="span" variant="bodySm" tone="subdued">
                Est. Monthly:
              </Text>
              <Text as="span" variant="bodySm" fontWeight="semibold">
                ${agent.estimatedMonthlyCost.toFixed(2)}
              </Text>
              <Text as="span" variant="bodySm" tone="subdued">
                ({totalProducts} products)
              </Text>
            </InlineStack>
          </BlockStack>

          {/* Accuracy Badge */}
          <Box
            padding="200"
            background="bg-surface-secondary"
            borderRadius="200"
          >
            <InlineStack gap="200" blockAlign="center">
              <Text as="span" variant="bodySm" tone="subdued">
                Accuracy:
              </Text>
              <Box
                background="bg-fill-success"
                padding="025"
                paddingInlineStart="100"
                paddingInlineEnd="100"
                borderRadius="050"
              >
                <Text
                  as="span"
                  variant="bodySm"
                  fontWeight="semibold"
                  tone="success"
                >
                  {agent.accuracy}%
                </Text>
              </Box>
            </InlineStack>
          </Box>

          {/* Action Buttons */}
          <BlockStack gap="200">
            <InlineStack gap="200">
              <Button
                size="slim"
                onClick={() => onTry(agent.id)}
                disabled={agent.status === 'active'}
              >
                Try on 10 Products
              </Button>
              <Button
                size="slim"
                variant="primary"
                onClick={() => onActivate(agent.id)}
                disabled={agent.status === 'active'}
              >
                {agent.status === 'active' ? 'Activated' : 'Activate'}
              </Button>
            </InlineStack>
            <Button
              size="slim"
              variant="plain"
              onClick={() => onViewDetails(agent.id)}
              textAlign="left"
            >
              View Details →
            </Button>
          </BlockStack>
        </BlockStack>
      </Card>
    </div>
  );
};

// Example usage
export const AgentCardExample = () => {
  const exampleAgent: Agent = {
    id: 'taxonomy',
    name: 'Taxonomy Agent',
    icon: '🏷️',
    description: 'Classify products into 6000+ Google Product Taxonomy categories',
    pricePerProduct: 0.02,
    estimatedMonthlyCost: 4.48,
    status: 'inactive',
    accuracy: 95,
    category: 'data-quality',
  };

  return (
    <div style={{ maxWidth: '400px' }}>
      <AgentCard
        agent={exampleAgent}
        totalProducts={224}
        onTry={(id) => console.log('Try agent:', id)}
        onActivate={(id) => console.log('Activate agent:', id)}
        onViewDetails={(id) => console.log('View details:', id)}
      />
    </div>
  );
};
