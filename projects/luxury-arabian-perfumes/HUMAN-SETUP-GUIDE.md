# AL MAJD — Human Setup Guide

**Complete step-by-step guide to get your luxury Arabian perfume dropshipping store operational.**

---

## 📋 Table of Contents

1. [Understanding Dropshipping](#1-understanding-dropshipping)
2. [Stripe Payment Setup](#2-stripe-payment-setup)
3. [Finding Suppliers](#3-finding-suppliers)
4. [Adding Product Images](#4-adding-product-images)
5. [Order Fulfillment Process](#5-order-fulfillment-process)
6. [Customer Service](#6-customer-service)
7. [Testing Before Launch](#7-testing-before-launch)
8. [Realistic Expectations](#8-realistic-expectations)

---

## 1. Understanding Dropshipping

### What is Dropshipping?

**You DON'T:**
- ❌ Buy inventory upfront
- ❌ Store products in your home
- ❌ Package or ship anything yourself
- ❌ Handle the products at all

**You DO:**
- ✅ Customer orders on your site (pays YOU €60)
- ✅ You order from AliExpress supplier (you pay them €12)
- ✅ Supplier ships directly to your customer
- ✅ You keep the difference (€48 minus Stripe fees = €46 profit)

### The Complete Flow

```
1. Customer discovers your site → browses products
   ↓
2. Customer adds to cart → checks out via Stripe
   ↓
3. Stripe charges their card → money goes to YOUR Stripe account
   ↓
4. You receive email notification → "New Order: Royal Rose Attar"
   ↓
5. You log into AliExpress → find the product from your supplier list
   ↓
6. You place order → enter CUSTOMER'S shipping address (not yours!)
   ↓
7. You pay supplier with your card → €12 charged
   ↓
8. Supplier processes order → ships from China/Dubai
   ↓
9. Customer receives package → 10-15 days later
   ↓
10. You keep profit → €46 per order (76% margin!)
```

### Time Investment

- **Per order:** 10-15 minutes (place supplier order, send tracking to customer)
- **Per day:** 30-60 minutes (check orders, respond to questions)
- **Per week:** 5-7 hours total (including social media posting)

### No Inventory = No Risk

- If you get 0 orders → you lose $0 (no inventory to discard)
- If you get 10 orders → you profit €460
- You only pay suppliers AFTER customers pay you

---

## 2. Stripe Payment Setup

Stripe is what processes customer credit card payments and deposits money into your bank account.

### Step 1: Create Stripe Account

1. Go to: **https://stripe.com**
2. Click **"Start now"** (top right)
3. Choose **"Accept online payments"**
4. Enter your details:
   - Email address
   - Full name
   - Country: **Portugal**
   - Business type: **Individual** (for now)
5. Verify your email
6. Complete business profile:
   - Business name: **AL MAJD** or your legal name
   - Website: Your Cloudflare Pages URL (e.g., `luxury-arabian-perfumes.pages.dev`)
   - Product description: **"Luxury Arabian perfumes and attars"**

### Step 2: Get Your API Keys

1. In Stripe dashboard, click **"Developers"** (top right)
2. Click **"API keys"** (left sidebar)
3. You'll see two modes:
   - **Test mode** (for testing — use fake cards)
   - **Live mode** (for real customers — real money)

**Start with TEST MODE:**

4. Copy your **Publishable key** (starts with `pk_test_`)
5. Copy your **Secret key** (starts with `sk_test_`)

**Keep the secret key SECRET** — never share it publicly!

### Step 3: Add Keys to Your Site

1. Open file: `projects/luxury-arabian-perfumes/site/js/cart.js`
2. Find this line (near the top):

```javascript
const STRIPE_PUBLISHABLE_KEY = 'pk_test_YOUR_STRIPE_KEY_HERE';
```

3. Replace with your actual test key:

```javascript
const STRIPE_PUBLISHABLE_KEY = 'pk_test_51Abc123DEF...'; // Your real key
```

4. Save the file

### Step 4: Create a Stripe Payment Link (Simplest Method)

**This is the easiest way to accept payments without a backend server:**

1. In Stripe dashboard, go to **"Payment Links"** (left sidebar)
2. Click **"+ New"** (top right)
3. Configure:
   - **Product name:** "AL MAJD Order" (generic — we'll show details in email)
   - **Price:** Leave as **customer chooses amount** OR set to €1 (you'll adjust manually)
   - **Currency:** EUR
   - **Success URL:** `https://luxury-arabian-perfumes.pages.dev/success.html`
   - **Cancel URL:** `https://luxury-arabian-perfumes.pages.dev/cancel.html`
4. Click **"Create link"**
5. Copy the payment link URL (looks like: `https://buy.stripe.com/test_abc123`)

6. Open `site/js/cart.js` again
7. Find this line:

```javascript
const STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/YOUR_PAYMENT_LINK';
```

8. Replace with your actual link:

```javascript
const STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/test_abc123def'; // Your real link
```

9. Save and redeploy: `wrangler pages deploy site`

### Step 5: Test the Checkout

1. Visit your live site
2. Add a product to cart
3. Click **"Finalizar Compra"**
4. You'll be redirected to Stripe's secure checkout page
5. Use a **test card:**
   - Card number: `4242 4242 4242 4242`
   - Expiry: Any future date (e.g., `12/28`)
   - CVC: Any 3 digits (e.g., `123`)
   - ZIP: Any 5 digits (e.g., `12345`)
6. Complete payment
7. You should see the success page
8. Check your Stripe dashboard → you'll see the test payment under **"Payments"**

**If this works: Your checkout is functional! ✅**

### Step 6: Switch to Live Mode (When Ready to Accept Real Money)

**Do this ONLY after testing is complete:**

1. In Stripe dashboard, toggle from **"Test mode"** to **"Live mode"** (top right)
2. Complete any required verification (Stripe may ask for ID, bank details)
3. Add your bank account:
   - Go to **"Settings"** → **"Bank accounts and scheduling"**
   - Add your IBAN (Portuguese bank account)
4. Get your **LIVE** API keys:
   - Go to **"Developers"** → **"API keys"**
   - Copy **Publishable key** (starts with `pk_live_`)
5. Create a **LIVE** Payment Link (same process as Step 4, but in live mode)
6. Update `site/js/cart.js` with LIVE keys and LIVE payment link
7. Redeploy: `wrangler pages deploy site`

**Now you can accept real payments and real money will go to your bank!**

### Stripe Fees

- **Per transaction:** 1.4% + €0.25 (European cards)
- **Example:** €60 order → Stripe takes €1.09 → you get €58.91

---

## 3. Finding Suppliers

You need to find actual products on AliExpress that match the luxury perfumes listed on your site.

### Step 1: Search AliExpress

1. Go to: **https://www.aliexpress.com**
2. Create an account (if you don't have one)
3. Search for each product type:
   - "Arabian oud oil"
   - "Attar perfume oil"
   - "Bakhoor incense"
   - "Arabic perfume"

### Step 2: Evaluate Suppliers

For each product, check:

✅ **Rating:** 4.5+ stars (minimum)
✅ **Orders:** 100+ orders (proven seller)
✅ **Price:** €4-15 per item (leaves room for profit)
✅ **Shipping:** Ships to Portugal, 10-20 day delivery
✅ **Photos:** High-quality product images (you can use these)
✅ **Reviews:** Positive reviews with photos

**Example good supplier:**
- Product: "3ml Oud Oil Roll-On"
- Price: €8.50
- Rating: 4.7 stars (2,340 orders)
- Shipping: Free, 12-18 days to Portugal
- Your selling price: €55 → **€46.50 profit per sale**

### Step 3: Document Your Suppliers

Create a spreadsheet (or use a text file):

```
Product Name | AliExpress URL | Supplier Cost | Your Price | Profit | Shipping Time
-------------|----------------|---------------|------------|--------|---------------
Oud Al Qamari | https://aliexpress.com/item/123 | €9.50 | €89 | €79.50 | 12-15 days
Royal Rose Attar | https://aliexpress.com/item/456 | €7.20 | €65 | €57.80 | 10-14 days
Musk Al Sultan | https://aliexpress.com/item/789 | €6.50 | €55 | €48.50 | 14-18 days
...
```

**Save this file:** `projects/luxury-arabian-perfumes/suppliers-list.md`

### Step 4: Order Samples (Optional but Recommended)

Before you start selling, order 1-2 products to yourself:

- **Why?** Verify quality, take your own photos, check shipping time
- **Cost:** €10-20 total
- **Benefit:** You can confidently sell knowing the product is good

**If a product is poor quality → remove it from your site immediately.**

### European Suppliers (Faster but More Expensive)

If you want 3-5 day shipping instead of 2-3 weeks:

- Search for suppliers in **Spain, France, UK** on Alibaba
- Expect to pay €20-40 per item (vs €5-15 from China)
- Your margins will be lower (€20-30 profit vs €40-50)
- But customers get products faster = fewer complaints

**Recommendation for launch:** Start with AliExpress (cheap, test demand). If you get lots of orders + complaints about shipping time, then switch to European suppliers.

---

## 4. Adding Product Images

Your site currently has placeholder icons (🌙, 🌹, etc.). You need real product photos.

### Option A: Use Supplier Images (Fast — 1 hour)

1. Find your products on AliExpress (see Section 3)
2. Right-click on product images → **"Save Image As..."**
3. Save them to: `projects/luxury-arabian-perfumes/site/images/products/`
4. Rename files to match product IDs:
   - `oud-al-qamari.jpg`
   - `royal-rose-attar.jpg`
   - `musk-al-sultan.jpg`
   - etc.
5. Update `site/js/products.js` — add `image` field:

```javascript
{
  id: "oud-al-qamari",
  name: "Oud Al Qamari",
  image: "images/products/oud-al-qamari.jpg", // ← Add this line
  category: "oud",
  volume: "12ml",
  price: 89,
  // ... rest of product data
}
```

6. Update `site/js/main.js` to show images instead of placeholders:

Find this section in `renderProducts()` function:

```javascript
<div class="product-img-placeholder">
  <div class="placeholder-icon">${product.icon}</div>
  <div class="placeholder-label">Al Majd</div>
</div>
```

Replace with:

```javascript
${product.image 
  ? `<img src="${product.image}" alt="${product.name}" class="product-img" />` 
  : `<div class="product-img-placeholder">
       <div class="placeholder-icon">${product.icon}</div>
       <div class="placeholder-label">Al Majd</div>
     </div>`
}
```

7. Redeploy: `wrangler pages deploy site`

### Option B: Use AI-Generated Images (Medium — 2 hours)

1. Use DALL-E, Midjourney, or Stable Diffusion
2. Prompt: "Luxury Arabian perfume bottle, oud oil, black and gold packaging, minimalist product photography, white background"
3. Generate 8-12 images (one per product)
4. Save to `site/images/products/`
5. Follow steps 5-7 from Option A

### Option C: Order Samples and Photograph (Slow — 1 week)

1. Order samples from AliExpress (€20-30 total)
2. Wait 2-3 weeks for delivery
3. Set up simple product photography (white background, good lighting)
4. Take photos with your phone (use portrait mode)
5. Edit (increase brightness, crop to square)
6. Save to `site/images/products/`
7. Follow steps 5-7 from Option A

**Recommendation:** Start with Option A (supplier images) to launch quickly. Upgrade to your own photos later if business takes off.

---

## 5. Order Fulfillment Process

**This is what you do when a customer places an order:**

### Step 1: Receive Order Notification

When a customer completes checkout on Stripe:

1. **Stripe sends you an email:** "Payment succeeded"
2. **Email contains:**
   - Customer name
   - Customer email
   - Amount paid (e.g., €89)
   - Payment ID

**NOTE:** The email WON'T tell you which product they ordered (limitation of simple Payment Links). You need to:

- Ask customer to email you their order details, OR
- Set up Stripe webhooks (more technical — skip for now)

**For now:** Add this note to your success page:

Edit `site/success.html`:

```html
<p>Por favor, envie-nos um email para <strong>ola@almajd.pt</strong> com:</p>
<ul>
  <li>Nome do produto que encomendou</li>
  <li>Morada de entrega completa</li>
  <li>Número de telefone (para a transportadora)</li>
</ul>
```

### Step 2: Confirm Order Details

Customer emails you: "Olá, acabei de encomendar o Oud Al Qamari, entrega para..."

You reply:

```
Obrigado pela sua encomenda!

Confirmamos:
- Produto: Oud Al Qamari (12ml)
- Preço: €89
- Morada: [repeat their address]

O seu perfume será enviado nas próximas 24-48 horas.
Tempo de entrega: 10-15 dias úteis (envio internacional premium).
Receberá um email com o número de rastreamento assim que for expedido.

Cumprimentos,
AL MAJD
```

### Step 3: Order from Supplier

1. Go to AliExpress
2. Find the product (use your supplier list from Section 3)
3. Add to cart
4. Click **"Buy Now"**
5. **CRITICAL:** Enter the CUSTOMER'S address, NOT yours:
   - Name: Customer's name
   - Address: Customer's address
   - Phone: Customer's phone
   - Leave a note: "Gift — no invoice" (so customer doesn't see AliExpress price)
6. Complete payment (you pay €9.50 with your card)
7. AliExpress gives you a tracking number (e.g., `AE123456789PT`)

### Step 4: Send Tracking to Customer

Email customer:

```
Olá,

O seu Oud Al Qamari foi expedido!

Rastreamento: AE123456789PT
Link: https://track24.net/en/tracking/AE123456789PT

Tempo estimado: 10-15 dias úteis.
Qualquer dúvida, estamos à disposição.

AL MAJD
```

### Step 5: Wait for Delivery

- Customer receives package in 10-15 days
- They (hopefully) love it
- You've made €79.50 profit (€89 - €9.50)

### Step 6: Follow Up (Optional but Recommended)

2 weeks after ordering, email customer:

```
Olá [Customer],

Esperamos que o seu Oud Al Qamari tenha chegado em perfeitas condições!

Se tiver alguma questão ou quiser explorar a nossa coleção completa,
estamos sempre disponíveis.

Obrigado por escolher AL MAJD.
```

This builds loyalty and encourages repeat orders.

---

## 6. Customer Service

### Common Questions & Your Answers

**Q: "Where is my order?"**
A: "O seu encomenda foi expedida no dia [date]. O rastreamento é [tracking]. Tempo de entrega: 10-15 dias úteis. Está atualmente em trânsito."

**Q: "It's been 3 weeks and nothing arrived!"**
A: Check tracking. If stuck in customs or lost:
1. Contact AliExpress supplier → ask for reshipment
2. If supplier refuses → refund the customer via Stripe
3. Apologize: "Pedimos desculpa pelo atraso. Reembolsamos o valor total e enviamos um novo perfume sem custo."

**Q: "The product is different from the photos!"**
A: (If true) → Full refund immediately + remove that product from site
(If not true) → Ask for photo proof, investigate with supplier

**Q: "Can I return it?"**
A: "Devido à natureza dos perfumes (produto de higiene pessoal), não aceitamos devoluções de produtos abertos. Se o produto chegou danificado, envie-nos fotos e reembolsamos totalmente."

**Q: "Do you have [specific perfume] not on your site?"**
A: "Podemos procurar para si! Envie-nos uma descrição do que procura e respondemos em 24 horas." (Then search AliExpress, quote them a price)

### Refund Process (Stripe)

If you need to refund a customer:

1. Go to Stripe dashboard
2. Click **"Payments"**
3. Find the customer's payment
4. Click **"⋯"** (three dots) → **"Refund payment"**
5. Choose: Full refund or partial refund
6. Confirm
7. Money is returned to customer's card in 5-10 days
8. Email customer: "Reembolso processado. Receberá o valor em 5-10 dias úteis."

**Refund policy:**
- Product never arrived → Full refund
- Product damaged → Full refund + offer to resend
- Customer changed mind (before shipping) → Full refund
- Customer changed mind (after shipping) → No refund (but you can offer 50% store credit to keep them happy)

---

## 7. Testing Before Launch

**DO NOT START MARKETING UNTIL YOU TEST EVERYTHING:**

### Pre-Launch Checklist

- [ ] **Stripe test mode works**
  - Add product to cart
  - Complete checkout with test card `4242 4242 4242 4242`
  - Payment shows in Stripe dashboard
  - Success page displays correctly

- [ ] **Site looks good on mobile**
  - Open site on your phone
  - Check all pages scroll correctly
  - Check cart works
  - Check checkout redirects properly

- [ ] **All links work**
  - Click every button
  - Click every nav link
  - Make sure no "404 Not Found" pages

- [ ] **Supplier list is complete**
  - You have AliExpress links for all 10 products
  - You've verified all suppliers ship to Portugal
  - You know the cost of each product

- [ ] **Product images are added**
  - No more placeholder icons
  - All products have real/AI-generated photos

- [ ] **Email is set up**
  - Create email: `ola@almajd.pt` (use Gmail forwarding or custom domain)
  - Test: Send yourself an email, make sure you receive it

- [ ] **You understand the full process**
  - Customer orders → Stripe charges → You order from AliExpress → Customer receives
  - You can do this in your sleep

**If ANY of the above are not checked → DO NOT launch. Fix them first.**

---

## 8. Realistic Expectations

### Timeline to First Sale

**With organic marketing (Instagram, TikTok):**
- **Week 1:** 50-100 Instagram followers, 50-100 website visits, **0-1 orders**
- **Week 2:** 150-200 followers, 150-200 visits, **1-2 orders**
- **Week 3-4:** 250-300 followers, 300-400 visits, **2-4 orders**
- **Month 2:** 500+ followers, 800+ visits, **8-12 orders**

**First order:** Expect it in 10-20 days (not day 1)

**With paid ads (Facebook/Instagram — if you add budget later):**
- **Day 1-3:** First orders can come immediately
- **Week 1:** 5-10 orders possible with €50 ad spend

### Revenue Projections (Organic Only)

**Month 1:**
- Orders: 3-5
- Revenue: €200-400
- Profit: €140-300 (after supplier costs + Stripe fees)

**Month 2:**
- Orders: 8-12
- Revenue: €500-800
- Profit: €380-600

**Month 3:**
- Orders: 15-25
- Revenue: €1000-1600
- Profit: €760-1200

**Month 6 (if scaling):**
- Orders: 40-60/month
- Revenue: €2500-4000
- Profit: €1900-3000

### Time Investment

**Week 1-2 (Setup):** 10-15 hours
- Learning the systems
- Setting up Stripe
- Finding suppliers
- Creating content

**Week 3+ (Maintenance):** 5-7 hours/week
- 30 min/day: Check orders, respond to questions
- 2-3 hours/week: Create Instagram/TikTok content (agents pre-write captions)
- Human just posts and engages

### What Success Looks Like

**After 30 days:**
- Site is live ✅
- Stripe is working ✅
- 3-5 orders completed ✅
- Customers are happy (no complaints) ✅
- You've made €200-300 profit ✅

**This validates the business model.** You can then:
- Add more products
- Increase content creation
- Consider paid ads (small budget)
- Scale to €1000+/month

### What Failure Looks Like

**After 30 days:**
- 0 orders
- <50 website visits
- Instagram has <100 followers
- No traction despite posting content

**Then:**
- Kill the project (God Agent decides)
- You've lost: $0 in inventory (because dropshipping)
- You've learned: Organic marketing for luxury goods, e-commerce setup
- Try a different project

---

## 🚀 You're Ready to Launch

**Next steps:**

1. **Complete Stripe setup** (Section 2) — 1 hour
2. **Find 5-8 suppliers on AliExpress** (Section 3) — 2 hours
3. **Add product images** (Section 4) — 1-2 hours
4. **Test the entire checkout flow** (Section 7) — 30 min
5. **Start posting on Instagram** (use content created by agents) — ongoing

**You have everything you need. Execute.**

---

**Questions? Email the project agent (report in task-log.md) or escalate to God Agent via human_task.**
