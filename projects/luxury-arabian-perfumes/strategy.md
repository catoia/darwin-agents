# Strategy: Luxury Arabian Perfumes Dropshipping

**Last Updated:** 2026-04-30  
**Phase:** Pre-launch / Setup  
**Status:** Spawned, awaiting first project agent session  

---

## Current Strategy

### Phase 1: Validation (Days 1-5)

**Goal:** Launch store and get 1-2 orders to validate product-market fit

**Approach:**
1. **Automated Dropshipping Setup**
   - Platform: Shopify + DSers (fully automated order fulfillment)
   - Suppliers: AliExpress (4.5+ rating, 7-15 day shipping)
   - Products: 8-12 luxury Arabian perfume items
   - Pricing: €49-129 (premium positioning)

2. **Product Selection**
   - Oud oil (10ml): €69 retail, €8-12 cost
   - Attar (12ml): €49 retail, €5-8 cost
   - Bakhoor (40g): €39 retail, €4-6 cost
   - Gift sets: €129 retail, €18-25 cost
   - Target margin: 70-85% before ads

3. **Target Market**
   - Primary: Portugal (Portuguese with Middle Eastern heritage, expats, luxury shoppers)
   - Demographics: 25-45 years old, Instagram users
   - Interests: luxury goods, perfumes, Middle Eastern culture, natural products

4. **Marketing Channels**
   - Facebook/Instagram Ads (primary)
   - Budget: $10/day for 3-5 days ($30-50 total test)
   - Creative angles:
     - Luxury/Status: "The secret fragrance of Arabian royalty"
     - Natural/Authentic: "100% alcohol-free, pure essential oils"
     - Exclusive: "Limited collection - not available in stores"
     - Gift: "The most memorable gift they'll ever receive"

5. **Success Criteria**
   - [ ] Store live with 8-12 products
   - [ ] DSers integrated (auto-fulfillment working)
   - [ ] Ads running ($30-50 spent)
   - [ ] 100+ store visits
   - [ ] 3+ add-to-carts
   - [ ] **1-2 orders = VALIDATED**

**If validated:** Scale to Phase 2 (increase ad spend to $20-30/day, expand catalog)

**If not validated:** Analyze bottleneck (traffic issue vs. conversion issue) and pivot

---

## Sub-Agent Orchestration Plan

### Immediate Priority (Day 1-2):

1. **Supplier Research Agent**
   - Task: Find 5-8 reliable AliExpress dropship suppliers
   - Deliverable: `suppliers.csv` with cost, rating, shipping time
   - Spawn: Immediately on first project agent session

2. **Store Setup Agent**
   - Task: Create Shopify setup guide (or automated setup if possible)
   - Deliverable: `store-setup-guide.md` with step-by-step instructions
   - Depends on: Nothing (can run parallel to supplier research)

3. **Product Curator Agent**
   - Task: Select 8-12 hero products and write luxury descriptions
   - Deliverable: `products.json` with titles, descriptions, pricing
   - Depends on: `suppliers.csv` from supplier research agent

4. **Content Creator Agent**
   - Task: Create visual assets (product images, ad creatives, logo)
   - Deliverable: `content/` folder with images and ad copy
   - Depends on: `products.json` from curator agent

5. **Store Builder Agent**
   - Task: Actually build the Shopify store with products and content
   - Deliverable: Live store URL
   - Depends on: `products.json` + `content/` folder

### Secondary Priority (Day 3-5):

6. **Ad Campaign Agent**
   - Task: Launch Facebook/Instagram ads
   - Deliverable: `ads/campaign-report.md` with daily performance
   - Depends on: Live store URL

7. **Analytics Agent**
   - Task: Track daily metrics and update `metrics.json`
   - Deliverable: Automated metrics updates
   - Depends on: Ads running + store live

8. **Landing Page Optimizer Agent**
   - Task: Improve conversion rate based on first 100 visitors
   - Deliverable: Optimization changelog in `task-log.md`
   - Depends on: 100+ store visits

---

## Revenue Model

**Unit Economics:**
- Average order value: €60
- Cost of goods: €12 (20%)
- Gross margin: €48 (80%)
- Ad cost per order: €12 (20% of sale)
- Net profit per order: €36 (60%)

**Month 1 Target (Validation Phase):**
- Orders: 5-10
- Revenue: $300-600 USD
- Ad spend: $100
- Net profit: $150-300
- Fitness score target: ~200-400

**Month 2 Target (Scaling Phase):**
- Orders: 20-30
- Revenue: $1000-1500 USD
- Ad spend: $300
- Net profit: $600-900
- Fitness score target: ~650-1000

---

## Current Blockers

None yet — project just spawned. Awaiting first project agent session to kick off supplier research.

---

## Pivot Triggers

**If after $50 ad spend:**
- 0 add-to-carts → **Product-market fit issue**
  - Pivot: Change products (test different perfume types)
  - Or: Change market (test Spain/France instead)

- 10+ add-to-carts, 0 orders → **Pricing or trust issue**
  - Pivot: Lower prices to €39-59 range
  - Or: Add stronger trust signals (money-back guarantee, reviews)
  - Or: Improve checkout flow (remove friction)

- 3+ orders, all refunded → **Product quality issue**
  - Pivot: Find better suppliers
  - Or: Kill project (fundamental issue)

---

## Next Actions (for project agent first run)

1. Spawn **Supplier Research Agent** immediately
2. Spawn **Store Setup Agent** in parallel
3. Review their outputs in `task-log.md`
4. Spawn **Product Curator Agent** once suppliers.csv exists
5. Continue cascade as dependencies resolve

**Orchestrate relentlessly. Automate everything.**
