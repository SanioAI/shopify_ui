-- Run in Supabase: SQL Editor → New query → paste → Run
-- Stores per-shop Admin API access tokens (OAuth). Used only with SUPABASE_SERVICE_ROLE_KEY on the server.

create table if not exists public.shopify_oauth_tokens (
  shop text primary key,
  access_token text not null,
  updated_at timestamptz not null default now()
);

-- No access for anonymous/authenticated users; only the service role (backend) should use this project key.
alter table public.shopify_oauth_tokens enable row level security;

-- Intentionally no policy for public roles — only service role bypasses RLS and can read/write.

create index if not exists shopify_oauth_tokens_updated_at_idx
  on public.shopify_oauth_tokens (updated_at desc);

comment on table public.shopify_oauth_tokens is 'Shopify OAuth access tokens; server-side only.';
