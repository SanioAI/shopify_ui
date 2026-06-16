# Shopify App Store — Approval Readiness Checklist

**Purpose:** Track what Shopify reviewers expect and what you must complete before submission.  
**Official reference:** [Shopify App Store requirements](https://shopify.dev/docs/apps/launch/app-requirements-checklist) (keep this bookmarked; criteria change).

---

## Blockers (fix before review)

| Item | Why it matters | Status |
|------|----------------|--------|
| **OAuth per shop** | Apps cannot rely on hardcoded store URLs or Admin API tokens. Tokens must come from the install OAuth flow and be stored per merchant (encrypted at rest). | Review `api_server.py` / backend — replace dev credentials before production. |
| **HTTPS everywhere** | Production app URL, APIs, privacy policy, and support links must use HTTPS. | ⏳ |
| **Public Privacy Policy URL** | Required in the listing. Must describe what data you collect (products, metafields, emails from contact forms), AI processing, retention, subprocessors. | ⏳ |
| **Monitored support contact** | Email (or help desk) you list must be answered; Shopify expects reasonable response time. | `support@catalogagents.com` — confirm inbox works. |
| **App matches listing** | Screenshots and description must reflect the real app. No exaggerated claims. | ⏳ |

---

## 1. Technical (Shopify review)

- [ ] **Install / uninstall** — Clean install; uninstall removes webhooks, sessions, and optional app data per your policy.
- [ ] **Embedded admin experience** — Store-facing UI should load in Shopify Admin (embedded app) using [Shopify App Bridge](https://shopify.dev/docs/api/app-bridge) unless you have a documented exception for a standalone flow (confirm current pattern with Shopify Partner support if unsure).
- [ ] **Scopes** — Request only the [Admin API access scopes](https://shopify.dev/docs/api/usage/access-scopes) you need (`read_products`, `write_products`, metafields, etc.). Document why each scope exists in the listing.
- [ ] **No secrets in client or repo** — API keys, shared secrets, and tokens belong in server env vars / secrets manager, not in frontend or Git.
- [ ] **Error handling** — Clear messages when API fails; no raw stack traces to merchants.
- [ ] **Performance** — UI usable within a few seconds; avoid blocking the admin on long jobs (async jobs + status are fine).

---

## 2. Listing assets (Partners → App → Distribution)

- [ ] **App name** (≤30 characters) — e.g. *Catalog Agents - AI Enrichment*
- [ ] **Icon** — 1200×1200 PNG
- [ ] **Screenshots** — Typically 1600×900 or as required by current Partner UI; show real product UI
- [ ] **Short description** — Within character limits; accurate
- [ ] **Full description** — What the app does, pricing, support, limitations
- [ ] **Pricing section** — Align with what you charge. **Current product direction:**
  - Up to **25 SKUs free**
  - Up to **5,000 SKUs:** enrichment **$100/mo**, +compliance or +content **$150/mo**, **all three $200/mo**
  - Subscription requests via **approval flow** (contact form → contract → payment later) until Shopify Billing is wired
- [ ] **Privacy policy URL** — Public HTTPS page
- [ ] **Support URL or email** — Same as you monitor
- [ ] **App category** — e.g. Store design / products / marketing as fits

---

## 3. Legal & trust

- [ ] **Privacy policy** — Data you process (catalog data, enrichment outputs, form submissions), AI/third-party APIs, retention, merchant rights, contact.
- [ ] **Terms of Service** — Recommended: billing, cancellation, acceptable use, limitation of liability (lawyer or vetted template).
- [ ] **GDPR / regional** — If EU merchants: lawful basis, deletion requests, subprocessors list in privacy policy.

---

## 4. Billing (Shopify)

- [ ] **Partners account** — Tax and payout details complete if you charge through Shopify.
- [ ] **Shopify Billing API** — When you move from “approval + contract” to in-app charges, use [app charges](https://shopify.dev/docs/apps/billing) so billing is clear in the merchant’s Shopify invoice.
- [ ] **Until then** — Listing should honestly say how billing works (e.g. “Subscribe sends a request; we finalize plan and agreement separately”) so it matches the UI.

---

## 5. Support & documentation

- [ ] **Support email** active (e.g. support@catalogagents.com)
- [ ] **Optional:** Help center or FAQ URL (reduces review friction)

---

## 6. QA before “Submit for review”

- [ ] Test on a **development store** with a fresh install
- [ ] **Chrome** + **Safari** (embedded apps are sensitive to cookies / third-party context)
- [ ] **Mobile admin** — Basic usability if merchants use phones
- [ ] **Pricing page** — Subscribe opens contact/approval flow; copy matches listing
- [ ] No console errors on main flows

---

## 7. Relationship to other docs

| Document | Use |
|----------|-----|
| `APP_STORE_REQUIREMENTS.md` | Detailed breakdown, design brief, timeline |
| `DESIGN_ASSETS_BRIEF.md` | Icon and screenshot specs for designers |
| This checklist | **Go / no-go** before submission |

---

## Next steps (suggested order)

1. **Security** — Per-shop OAuth + remove hardcoded production credentials from backend.
2. **Legal** — Publish privacy policy (and terms) at stable HTTPS URLs.
3. **Assets** — Icon + screenshots that match the live UI and pricing.
4. **Listing** — Fill Partner Dashboard; paste URLs; align pricing text with **25 free / $100–$200** model.
5. **QA** — Run through the checklist above.
6. **Submit** — Allow ~5–10 business days for first review.

---

**Last updated:** April 2026  
