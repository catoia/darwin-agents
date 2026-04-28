# Budget Recipe Blog - Deployment & Setup Guide

## ✅ What's Ready

- ✅ Homepage with 10 recipe cards
- ✅ 10 SEO-optimized recipe pages targeting long-tail keywords
- ✅ Amazon affiliate link placeholders (need actual Associate ID)
- ✅ Sitemap.xml for Google Search Console
- ✅ robots.txt
- ✅ Clean, mobile-responsive design

## 🚀 Deployment Status

✅ **DEPLOYED:** https://budget-recipe-blog.pages.dev

Deployed on: 2026-04-28
Cloudflare Project: budget-recipe-blog
Status: Live and accessible

### Deploy Again (if needed)

If you need to redeploy after content updates

### Option 1: Deploy via Wrangler CLI

```bash
# Set environment variables
export CLOUDFLARE_API_TOKEN="your-api-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id-here"

# Deploy using npx (no installation needed)
npx wrangler pages deploy public --project-name=budget-recipe-blog
```

### Option 2: Deploy via Cloudflare Dashboard

1. Go to https://dash.cloudflare.com
2. Click "Workers & Pages" > "Create application" > "Pages" > "Connect to Git"
3. Or upload the `public/` folder directly
4. Project name: `budget-recipe-blog`
5. Build output directory: `/public`

The site will be live at: `https://budget-recipe-blog.pages.dev`

## 💰 Monetization Setup

### 1. Google AdSense (Priority: HIGH)

**What you need to do:**
1. Go to https://www.google.com/adsense/start/
2. Sign up with your Google account
3. Add your site URL: `https://budget-recipe-blog.pages.dev`
4. Add the AdSense code snippet to the `<head>` section of all pages
5. Wait for approval (typically 1-2 weeks)

**Once approved**, the agent will add ad placements to recipe pages automatically.

### 2. Amazon Associates (Priority: HIGH)

**What you need to do:**
1. Go to https://affiliate-program.amazon.com/
2. Sign up for Amazon Associates
3. Get your Associate ID (format: `yourname-20`)
4. Replace `budgetrecipe-20` in all recipe pages with your actual ID

**Find all affiliate links:**
```bash
grep -r "tag=budgetrecipe-20" public/
```

**Replace with your ID:**
```bash
# After you have your Associate ID, run:
find public/ -name "*.html" -exec sed -i '' 's/budgetrecipe-20/YOUR-ACTUAL-ID-20/g' {} +
```

## 📊 Google Search Console Setup

Once the site is deployed:

1. Go to https://search.google.com/search-console
2. Add property: `https://budget-recipe-blog.pages.dev`
3. Verify ownership (Cloudflare handles DNS verification automatically)
4. Submit sitemap: `https://budget-recipe-blog.pages.dev/sitemap.xml`
5. Request indexing for the homepage and top 3-5 recipe pages

## 🎯 Target Keywords

These pages are optimized for:
- "cheap dinner ideas for two"
- "budget chicken recipes"
- "easy meal prep under $20"
- "cheap pasta dishes for students"
- "budget meal prep chicken"
- "cheap healthy dinners"
- "budget ground beef recipes"
- "cheap vegetarian meals"
- "budget slow cooker recipes"
- "cheap breakfast meal prep"

## 📈 What Happens Next

After deployment, the Project Agent will:
1. Monitor Google Search Console for indexing and impressions
2. Add AdSense ad units once approved
3. Track Amazon affiliate clicks and conversions
4. A/B test different CTAs and ad placements
5. Expand content to top-performing keywords
6. Update metrics.json daily with traffic and revenue data

## 💵 Revenue Expectations

**Week 1-2:** $0 (indexing phase, AdSense pending approval)
**Week 3-4:** $5-15 (first impressions, early affiliate clicks)
**Week 5-6:** $30-50 (growing traffic, AdSense approved)
**Target by Week 6:** $200 revenue (combined AdSense + Amazon)

Success depends on:
- Google indexing speed (submit to Search Console to accelerate)
- AdSense approval time (1-2 weeks typical)
- Amazon affiliate conversion rate (2-5% typical)
- Content quality and SEO optimization (already solid ✅)
