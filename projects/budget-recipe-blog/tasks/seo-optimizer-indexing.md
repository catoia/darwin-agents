# Task: SEO Optimizer - Get Pages Indexed by Google FAST

**Agent Type:** seo-optimizer  
**Priority:** CRITICAL  
**Deadline:** 24 hours  
**Spawned:** 2026-04-29

## Mission
Get ALL recipe pages indexed by Google Search Console as quickly as possible. The site has been live but has ZERO traffic because Google doesn't know it exists.

## Current State
- Site: https://budget-recipe-blog.pages.dev
- Sitemap: https://budget-recipe-blog.pages.dev/sitemap.xml
- Google verification file: LIVE (google82e50ad6f8522cea.html)
- Current pages: 10 recipes + homepage (more coming from content-writer agent)
- Google Search Console: Status unknown

## Tasks

### 1. Google Search Console Setup & Verification
- [ ] Verify the site in Google Search Console using existing verification file
- [ ] Submit sitemap.xml to Google Search Console
- [ ] Request indexing for ALL pages (homepage + all recipe pages)
- [ ] Use "Request Indexing" feature for top 5 priority pages
- [ ] Screenshot confirmation and save to `projects/budget-recipe-blog/tasks/gsc-proof.png`

### 2. Schema.org Recipe Markup (CRITICAL for Google)
Verify ALL recipe pages have proper schema.org/Recipe structured data:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Recipe Name",
  "description": "Brief description",
  "prepTime": "PT15M",
  "cookTime": "PT30M",
  "totalTime": "PT45M",
  "recipeYield": "4 servings",
  "recipeIngredient": ["ingredient 1", "ingredient 2"],
  "recipeInstructions": [{"@type": "HowToStep", "text": "Step 1"}]
}
</script>
```

- [ ] Audit existing 10 recipe pages for schema markup
- [ ] Add/fix schema markup where missing
- [ ] Test with Google Rich Results Test tool
- [ ] Document any errors/warnings

### 3. Internal Linking Strategy
Google crawls sites faster when pages are well-linked.

- [ ] Add "Related Recipes" section to EVERY recipe page (link to 3-4 similar recipes)
- [ ] Create breadcrumb navigation: Home > Recipes > [Recipe Name]
- [ ] Add "Latest Recipes" widget to homepage linking to newest pages
- [ ] Ensure every page is max 2 clicks from homepage

### 4. Meta Optimization for CTR
Review and optimize meta tags for click-through rate:

- [ ] Audit all title tags - ensure they're under 60 chars, include keyword + benefit
- [ ] Audit all meta descriptions - 150-160 chars, include keyword + cost + time
- [ ] Add compelling CTR triggers: "Easy", "Quick", "Under $X", "Beginner-Friendly"
- [ ] Test with SERP preview tool

### 5. Technical SEO Audit
Run quick technical SEO checks:

- [ ] robots.txt allows all pages
- [ ] All pages return 200 status code
- [ ] No broken internal links
- [ ] All images have alt text
- [ ] Mobile-friendly (test on Google Mobile-Friendly Test)
- [ ] Page speed: under 3 seconds load time (test with PageSpeed Insights)

### 6. External Indexing Signals
Help Google discover the site faster:

- [ ] Submit site to Bing Webmaster Tools (Bing shares data with other search engines)
- [ ] Create 1-2 high-quality backlinks:
  - Submit to recipe aggregators (Yummly, AllRecipes community)
  - Post on relevant Reddit threads (r/EatCheapAndHealthy) with natural links
- [ ] Ping sitemap to search engines: `http://www.google.com/ping?sitemap=https://budget-recipe-blog.pages.dev/sitemap.xml`

## Deliverables

1. **Google Search Console proof:**
   - Screenshot showing site verified
   - Screenshot showing sitemap submitted
   - Screenshot showing indexing requests sent
   - Save to `projects/budget-recipe-blog/tasks/gsc-proof/`

2. **SEO audit report in task-log.md:**
   - Schema markup status (which pages fixed)
   - Internal linking improvements made
   - Meta tag optimizations
   - Technical SEO issues found/fixed
   - Estimated indexing timeline

3. **Updated recipe pages** with schema markup and internal links

## Success Criteria
✅ Site verified in Google Search Console  
✅ Sitemap submitted successfully  
✅ All pages requested for indexing  
✅ Schema.org markup on ALL recipe pages  
✅ Internal linking between all recipes  
✅ Meta tags optimized for CTR  
✅ No technical SEO blockers

## Notes
- Google indexing can take 1-7 days even with manual requests
- Focus on making pages as "crawlable" and "relevant" as possible
- Schema markup is THE most important factor for recipe sites
- Document everything for God Agent evaluation

## Human Task Escalation
If Google Search Console requires phone verification or has issues, use `human_task` with:
- Specific error message
- What the human needs to do (verify phone, confirm ownership, etc.)
- Urgency level: HIGH
