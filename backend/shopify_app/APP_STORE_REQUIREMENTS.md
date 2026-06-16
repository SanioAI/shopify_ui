# Requirements to Publish Catalog Agents to Shopify App Store

**Date**: February 20, 2026  
**App Name**: Catalog Agents (formerly "Catalog AI Direct")  
**Current Status**: Working in development - Ready for App Store submission preparation

**→ For a concise go/no-go list aligned with Shopify review (updated pricing & blockers), see [`MARKETPLACE_APPROVAL_CHECKLIST.md`](./MARKETPLACE_APPROVAL_CHECKLIST.md).**

---

## 📋 Current Status

### ✅ **What We Have (Completed)**
- [x] Working Shopify app with UI
- [x] App hosted on GitHub Pages: https://bindu-ai5.github.io/catalog-agents-ui/
- [x] Backend connector (reads/writes Shopify products)
- [x] 10 catalog agents defined with pricing
- [x] Tested successfully in development store
- [x] Complete planning documentation

### ⏳ **What We Need (To Publish)**

The items below are **REQUIRED** by Shopify before we can submit to the App Store.

---

## 🎨 1. Design Assets (UI Designer)

### **Required Files**

#### **A. App Icon** 🔴 CRITICAL
- **Size**: 1200 × 1200 pixels
- **Format**: PNG with transparent background
- **Style**: Professional, clean, recognizable at small sizes
- **Deadline**: 2 weeks

**What to tell designer:**
- Simple icon representing AI catalog enhancement
- Should work at 64×64px size
- 2-3 colors maximum
- No text in icon

---

#### **B. App Screenshots** 🔴 CRITICAL
- **Quantity**: 5-6 images
- **Size**: 1280 × 800 pixels (landscape)
- **Format**: PNG or JPG
- **Deadline**: 2 weeks

**Required Screenshots:**
1. **Dashboard** - Main agent selection screen
2. **Agent Details** - Close-up of agent card with pricing
3. **Trial Mode** - Before/after product enrichment
4. **Usage Dashboard** - Monthly usage tracking
5. **Logs Viewer** - Real-time operation logs
6. **Pricing Plans** (optional) - Plan comparison

**Requirements:**
- Add text annotations (e.g., "Choose from 10 AI Agents")
- Use actual UI with realistic data
- Clean, professional appearance
- Highlight key features

---

#### **C. App Banner** 🟡 RECOMMENDED
- **Size**: 1600 × 400 pixels
- **Format**: PNG or JPG
- **Content**: Logo + tagline + key benefit

---

### **Design Brief**
Full design requirements document created:
- **File**: `shopify_app/DESIGN_ASSETS_BRIEF.md`
- **Action**: Send this to UI designer
- **Cost Estimate**: $500-$1,500 (varies by designer)

---

## 📝 2. App Store Listing Content (Bindu)

### **A. App Name** 🔴 CRITICAL
```
Catalog Agents - AI Product Enrichment
```
(Max 30 characters)

**Status**: ✅ Decided

---

### **B. Tagline / Subtitle** 🔴 CRITICAL
```
Automatically enhance product data with 10 AI-powered agents
```
(Max 120 characters)

**Status**: ✅ Drafted

---

### **C. Short Description** 🔴 CRITICAL
```
Enrich your product catalog with AI. Automatically add taxonomy, 
SEO metadata, attributes, and compliance data. Try free on 10 products.
```
(Max 280 characters)

**Status**: ✅ Drafted

---

### **D. Full App Description** 🔴 CRITICAL

**Length**: 500-2000 characters

**Template provided in**: `shopify_app/DESIGN_ASSETS_BRIEF.md`

**Key sections to include:**
- What the app does
- Key benefits
- List of 10 agents
- Pricing information
- Perfect for (target customers)
- Free trial information

**Status**: ✅ Template drafted (needs minor edits)

**Action**: Review and finalize the description

---

### **E. Key Features List** 🔴 CRITICAL

**Required**: 5-10 bullet points

**Suggested:**
- 10 AI-powered catalog enhancement agents
- Try free on 10 products per agent
- Automatic processing of new/changed products
- Transparent usage-based pricing
- Real-time operation logs & analytics
- 95%+ accuracy with hybrid AI approach
- Shopify metafields integration
- Email notifications & alerts
- Export logs to CSV
- Priority support (Pro & Enterprise)

**Status**: ✅ Completed

---

## 📜 3. Legal Requirements (Legal/Compliance)

### **A. Privacy Policy** 🔴 CRITICAL

**Required by**: Shopify App Store

**Must Include:**
- What data you collect (product data, store info)
- How you use the data (AI processing, enrichment)
- How you store the data (security measures)
- Third-party services (if any)
- User rights (data access, deletion)
- Contact information

**Options:**
1. **Hire lawyer** ($500-$2,000) - Recommended
2. **Use template** (Free) - Risky
   - Templates available at: https://getterms.io/ or https://termsfeed.com/
3. **Privacy policy generators** ($50-$200)

**Hosting**: Must be hosted at public URL (e.g., https://catalogagents.com/privacy)

**Status**: ⏳ **NOT STARTED - PRIORITY**

**Deadline**: Before submission

---

### **B. Terms of Service** 🟡 RECOMMENDED

**Not required by Shopify but recommended**

**Must Include:**
- Usage terms
- Billing terms
- Cancellation policy
- Liability limitations
- Intellectual property

**Status**: ⏳ Not started

---

## 📧 4. Support & Contact (Immediate)

### **A. Support Email** 🔴 CRITICAL

**Required**: Professional support email

**Options:**
- support@catalogagents.com (need domain)
- support@sanio.ai (if you have this domain)
- catalogagents.support@gmail.com (temporary)

**Requirements:**
- Must be monitored daily
- Response time: <24 hours (Shopify standard)

**Status**: ⏳ **NEED TO SET UP**

**Action**: 
1. Decide on email address
2. Set up email forwarding
3. Create response templates

---

### **B. Documentation** 🟡 RECOMMENDED

**Optional but helpful:**
- Getting started guide
- FAQ
- Tutorial videos
- API documentation (for developers)

**Status**: ⏳ Not started (can add later)

---

## 💳 5. Billing Setup (Shopify Partners)

### **A. Configure Billing** 🔴 CRITICAL

**In Shopify Partners Dashboard:**
1. Set up billing plans:
   - Starter: $19/month base
   - Professional: $79/month base
   - Enterprise: $299/month base
2. Configure usage charges (per-operation pricing)
3. Add trial period (if offering free trial)

**Status**: ⏳ **NOT CONFIGURED**

**Deadline**: Before submission

---

### **B. Bank Account / Payment** 🔴 CRITICAL

**Required**: Connect bank account for payouts

**In Partners Dashboard:**
- Add banking information
- Tax information (W-9 or W-8BEN)
- PayPal or Stripe (for payouts)

**Status**: ⏳ Not set up

---

## 🧪 6. Testing Requirements (QA)

### **A. Functionality Testing** 🔴 CRITICAL

**Must test:**
- [ ] App installation works
- [ ] App uninstallation works (clean data removal)
- [ ] All 10 agents display correctly
- [ ] Buttons work (or show appropriate messages)
- [ ] Pricing displays correctly
- [ ] Usage tracking works
- [ ] Mobile responsive design
- [ ] Works in different browsers (Chrome, Safari, Firefox)

**Status**: ⏳ Partial (basic testing done, need comprehensive QA)

---

### **B. Performance Testing** 🟡 RECOMMENDED

**Check:**
- Page load time (<3 seconds)
- No console errors
- Works with large product catalogs (1000+ products)

**Status**: ⏳ Not done

---

## 🔒 7. Security & Compliance (Technical)

### **A. OAuth & Authentication** 🔴 CRITICAL

**Shopify Requirements:**
- Use Shopify OAuth (not API keys)
- Secure token storage
- HTTPS only (already done with GitHub Pages ✅)

**Status**: ✅ Using Shopify App OAuth

---

### **B. GDPR Compliance** 🔴 CRITICAL

**If serving EU customers:**
- Data processing agreement
- Right to data deletion
- Cookie consent
- Privacy policy compliance

**Status**: ⏳ Need to implement

---

## 📱 8. App Store Submission Checklist

### **Before You Can Submit:**

- [ ] **Design Assets**
  - [ ] App icon (1200×1200px)
  - [ ] 5-6 screenshots (1280×800px)
  - [ ] App banner (optional)

- [ ] **Content**
  - [ ] App name finalized
  - [ ] App description written
  - [ ] Key features list
  - [ ] Pricing details

- [ ] **Legal**
  - [ ] Privacy policy URL
  - [ ] Terms of service (optional)

- [ ] **Support**
  - [ ] Support email set up
  - [ ] Support contact monitored

- [ ] **Technical**
  - [ ] App fully functional
  - [ ] Tested in development store
  - [ ] No critical bugs
  - [ ] Mobile responsive

- [ ] **Billing**
  - [ ] Pricing plans configured in Partners Dashboard
  - [ ] Bank account connected

---

## 🚀 Submission Process

### **Step 1: Complete Checklist Above**

All items must be ✅ before submission.

---

### **Step 2: Fill Out App Listing**

1. Go to: https://partners.shopify.com/
2. Find your app: "Catalog AI Direct"
3. Click "App Store Listing" tab
4. Fill out all fields:
   - App name
   - Subtitle
   - Description
   - Key features
   - Upload icon
   - Upload screenshots
   - Add privacy policy URL
   - Add support contact
   - Select categories
   - Add pricing information

---

### **Step 3: Submit for Review**

1. Review all information
2. Click "Submit for Review"
3. Shopify reviews (5-10 business days)
4. They will:
   - Test app installation
   - Check functionality
   - Review content
   - Verify compliance

---

### **Step 4: Respond to Feedback**

**If Approved:**
- App goes live in App Store
- Available at: https://apps.shopify.com/catalog-agents

**If Rejected:**
- Shopify provides feedback
- Fix issues
- Resubmit

---

## ⏱️ Timeline Estimate

| Task | Owner | Time | Status |
|------|-------|------|--------|
| Design Assets | UI Designer | 2 weeks | ⏳ Not started |
| Privacy Policy | Legal/Bindu | 3-5 days | ⏳ Not started |
| Content Finalization | Bindu | 1 day | ⏳ 80% done |
| Support Email Setup | Bindu | 1 hour | ⏳ Not started |
| Billing Configuration | Bindu | 2 hours | ⏳ Not started |
| Comprehensive Testing | Bindu/QA | 3 days | ⏳ Partial |
| App Store Listing | Bindu | 2 hours | ⏳ Not started |
| Shopify Review | Shopify | 5-10 days | ⏳ N/A |

**Total Estimated Time**: 3-4 weeks

---

## 💰 Cost Estimate

| Item | Cost | Required |
|------|------|----------|
| Design Assets (logo, screenshots) | $500-$1,500 | ✅ Required |
| Privacy Policy (lawyer) | $500-$2,000 | ✅ Required |
| Domain (catalogagents.com) | $10-$20/year | 🟡 Optional |
| Hosting | $0 (GitHub Pages) | ✅ Already free |
| Shopify Partner Account | $0 (free) | ✅ Already done |

**Minimum Total**: $1,000-$3,500

---

## 🎯 Immediate Action Items

### **Priority 1: Legal** (CRITICAL PATH)
1. [ ] Draft privacy policy (or hire lawyer)
2. [ ] Host privacy policy at public URL
3. [ ] Review Shopify's privacy requirements

### **Priority 2: Design** (CRITICAL PATH)
1. [ ] Send design brief to UI designer
2. [ ] Get quote and timeline
3. [ ] Approve design concepts

### **Priority 3: Support**
1. [ ] Set up support email
2. [ ] Create email templates
3. [ ] Assign team member to monitor

### **Priority 4: Configuration**
1. [ ] Configure billing plans in Partners Dashboard
2. [ ] Connect bank account
3. [ ] Test billing flow

### **Priority 5: Testing**
1. [ ] Complete comprehensive QA testing
2. [ ] Fix any bugs found
3. [ ] Test on mobile devices

---

## ❓ Questions to Answer Before Submission

1. **Domain**: Do we buy catalogagents.com domain?
2. **Privacy Policy**: Hire lawyer or use template?
3. **Support**: Who will handle support emails?
4. **Pricing**: Final approval on $19/$79/$299 pricing?
5. **Launch Date**: When do we want to go live?
6. **Beta Testing**: Should we do beta with select merchants first?

---

## 📞 Who Does What

| Task | Owner | Status |
|------|-------|--------|
| Design Assets | **UI Designer** | ⏳ Waiting to assign |
| Privacy Policy | **Legal/Bindu** | ⏳ Need decision |
| Content Writing | **Bindu** | ⏳ 80% complete |
| Support Setup | **Bindu** | ⏳ To do |
| Billing Config | **Bindu** | ⏳ To do |
| Testing | **Bindu/QA** | ⏳ Partial |
| App Submission | **Bindu** | ⏳ After all complete |
| Vamsi Approval | **Vamsi** | ⏳ Waiting (FOR_VAMSI.md) |

---

## 📝 Summary

### **What's Done** ✅
- App works in development
- UI deployed and live
- Backend tested
- Planning complete

### **What's Needed** ⏳
- Design assets (logo, screenshots)
- Privacy policy
- Support email setup
- Billing configuration
- Comprehensive testing
- App Store listing submission

### **Timeline**: 3-4 weeks from now

### **Cost**: $1,000-$3,500

### **Next Step**: Wait for Vamsi's approval, then start design assets

---

**Status**: Ready for next phase once Vamsi approves the plan! 🚀

---

**Created**: February 20, 2026  
**Last Updated**: February 20, 2026  
**Document Owner**: Bindu Achalla
