# Task: Content Writer - Generate 20 New Recipe Pages

**Agent Type:** content-writer  
**Priority:** CRITICAL  
**Deadline:** 48 hours  
**Spawned:** 2026-04-29

## Mission
Generate 20 NEW budget recipe pages targeting long-tail keywords. These recipes must be:
- SEO-optimized for specific search queries
- Following the existing recipe template format
- Ready for immediate deployment
- Including Amazon affiliate link placeholders

## Target Keywords (Long-Tail Focus)
1. "chicken breast recipes under $5"
2. "vegetarian meals for students"
3. "cheap pasta dishes for family"
4. "budget meal prep for beginners"
5. "easy rice recipes under $10"
6. "affordable slow cooker meals"
7. "cheap healthy lunches for work"
8. "budget breakfast ideas for kids"
9. "inexpensive fish recipes"
10. "cheap vegan dinner ideas"
11. "budget friendly casseroles"
12. "easy cheap soup recipes"
13. "affordable taco recipes"
14. "budget stir fry meals"
15. "cheap salad recipes filling"
16. "budget pizza recipes at home"
17. "inexpensive sandwich ideas"
18. "cheap egg recipes dinner"
19. "budget friendly pasta bake"
20. "easy cheap desserts under $5"

## Recipe Page Requirements

### Structure (follow existing template in public/recipes/)
1. **HTML head:** Title, meta description, schema.org Recipe markup
2. **Hero section:** Recipe title, brief description, cost estimate
3. **Ingredients list:** Itemized with quantities
4. **Instructions:** Step-by-step numbered list
5. **Nutrition info:** Estimated calories, protein, carbs
6. **Amazon affiliate section:** Products placeholder (will be filled by product-recommender agent)

### SEO Requirements
- Title tag: "[Recipe Name] - Budget Recipe Under $[X]"
- Meta description: 150-160 chars, include keyword + cost + time
- H1: Main recipe title
- H2s: "Ingredients", "Instructions", "Tips", "Recommended Products"
- Internal links: Link to 2-3 related recipes from existing pages
- Alt text on images (use placeholder images for now)

### Content Quality
- Authentic voice: practical, helpful, not overly promotional
- Cost breakdown: Show why it's budget-friendly
- Prep time + cook time clearly stated
- Tips section: substitutions, storage, meal prep ideas
- 800-1200 words per recipe (enough for SEO, not bloated)

## File Format
Save each recipe as: `public/recipes/[keyword-slug].html`

Example: `public/recipes/chicken-breast-recipes-under-5.html`

## Deliverables
1. 20 HTML recipe pages in `public/recipes/`
2. Updated `public/sitemap.xml` to include all new pages
3. Updated `public/index.html` to link to new recipes in featured section
4. Report in `task-log.md` with:
   - List of all 20 recipes created
   - Keywords targeted
   - Any issues encountered
   - Estimated time to complete

## Notes
- Use the existing recipe template as reference (`public/recipes/budget-chicken-stir-fry.html`)
- Leave Amazon affiliate product sections as placeholders - product-recommender agent will fill them
- Focus on SPEED - 20 recipes in 48h means ~2.5 hours per recipe max
- Quality over perfection - these can be refined later based on traffic data

## Success Criteria
✅ 20 new recipe pages deployed  
✅ All pages follow SEO template  
✅ Sitemap updated  
✅ Internal linking between recipes  
✅ Ready for immediate Cloudflare deployment
