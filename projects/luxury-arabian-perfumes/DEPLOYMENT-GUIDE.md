# Deployment Guide: Luxury Arabian Perfumes Site

**Status:** Site ready to deploy ✅  
**Platform:** Cloudflare Pages (FREE hosting)  
**Estimated Time:** 5 minutes

---

## Option 1: Automated Deployment (Recommended)

This allows the agent to deploy automatically in future sessions.

### Step 1: Create Cloudflare API Token

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click **Create Token**
3. Use template: **Edit Cloudflare Workers** (includes Pages permissions)
4. Or create custom token with:
   - **Account** → **Cloudflare Pages** → **Edit**
5. Click **Continue to summary** → **Create Token**
6. **SAVE THE TOKEN** (shown only once)

### Step 2: Set Environment Variable

```bash
# Add to your shell profile (~/.zshrc or ~/.bash_profile)
export CLOUDFLARE_API_TOKEN="your-token-here"

# Reload shell
source ~/.zshrc  # or ~/.bash_profile
```

### Step 3: Deploy (automated)

```bash
cd /Users/nunocadete/darwin-agents/projects/luxury-arabian-perfumes
wrangler pages deploy site --project-name=luxury-arabian-perfumes
```

✅ Agent can now deploy automatically in future sessions.

---

## Option 2: Manual One-Time Deployment

If you prefer to deploy manually without setting up API token.

### Step 1: Login to Cloudflare

```bash
wrangler login
```

This opens your browser to authenticate. Click **Allow** to grant access.

### Step 2: Deploy the Site

```bash
cd /Users/nunocadete/darwin-agents/projects/luxury-arabian-perfumes
wrangler pages deploy site --project-name=luxury-arabian-perfumes
```

### Step 3: Get the Live URL

Wrangler will output:
```
✨ Deployment complete! Take a peek over at
   https://luxury-arabian-perfumes.pages.dev
```

### Step 4: Update Project Files

Copy the live URL and update:

**In `strategy.md`** (bottom of "Current Status" section):
```markdown
**Live URL:** https://luxury-arabian-perfumes.pages.dev
**Deployed:** 2026-04-30
```

**In `task-log.md`** (update the "[2026-04-30 12:00] URGENT: Deploy Site" entry):
```markdown
**Status:** ✅ DEPLOYED  
**Live URL:** https://luxury-arabian-perfumes.pages.dev
**Next Action:** Begin organic marketing (Instagram/TikTok content posting)
```

---

## What Gets Deployed

```
projects/luxury-arabian-perfumes/site/
├── index.html              (Main luxury e-commerce page)
├── css/
│   └── styles.css          (Black/gold/white luxury styling)
├── js/
│   ├── cart.js             (Shopping cart functionality)
│   ├── checkout.js         (Stripe payment integration)
│   └── products.js         (Product catalog)
├── success.html            (Payment success page)
├── cancel.html             (Payment cancelled page)
└── images/                 (Product images)
```

---

## After Deployment

**Immediate actions:**

1. **Test the site:**
   - Visit the live URL
   - Browse products
   - Test add-to-cart
   - Test checkout flow (use Stripe test mode)

2. **Configure Stripe (if not done):**
   - Get Stripe publishable key
   - Update `js/checkout.js` with your key
   - Test payment flow

3. **Update project files:**
   - Add live URL to strategy.md
   - Mark deployment complete in task-log.md
   - Update metrics.json with `status: "live"`

4. **Begin organic marketing:**
   - Start posting Instagram content (Day 1)
   - Post TikTok videos
   - Create Pinterest pins
   - Engage with target audience

---

## Troubleshooting

**Error: "Project not found"**
- First deployment creates the project automatically
- Cloudflare will assign: `luxury-arabian-perfumes.pages.dev`

**Error: "Authentication required"**
- Run: `wrangler login` (Option 2)
- Or set: `CLOUDFLARE_API_TOKEN` (Option 1)

**Error: "Invalid build directory"**
- Make sure you're in: `projects/luxury-arabian-perfumes/`
- Deploy from: `site/` subdirectory
- Command: `wrangler pages deploy site --project-name=luxury-arabian-perfumes`

**Need help?**
- Wrangler docs: https://developers.cloudflare.com/pages/platform/deploy-with-wrangler/
- Cloudflare Pages docs: https://developers.cloudflare.com/pages/

---

## Expected Result

✅ **Live URL:** `https://luxury-arabian-perfumes.pages.dev`  
✅ **SSL:** Automatic (Cloudflare provides free HTTPS)  
✅ **CDN:** Global edge network (fast worldwide)  
✅ **Cost:** $0 (Cloudflare Pages free tier)  
✅ **Deployment time:** ~30 seconds  

**The site will be live and ready for customers immediately after deployment.**
