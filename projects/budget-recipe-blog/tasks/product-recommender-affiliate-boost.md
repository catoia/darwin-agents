# Task: Product Recommender - Boost Amazon Click-Through Rate

**Agent Type:** product-recommender  
**Priority:** CRITICAL  
**Deadline:** 48 hours  
**Spawned:** 2026-04-29

## Mission
Transform affiliate link placement from "buried at the bottom" to "impossible to miss". Every recipe page should have 8-12 relevant Amazon affiliate products strategically placed to maximize click-through rate.

## Current Problem
- Affiliate links exist but are minimal
- Links are buried at the bottom of pages
- 0 clicks tracked = 0 revenue
- Products are not contextually relevant or compelling

## Target: 8-12 Products Per Recipe

### Product Categories by Recipe Type

**Cooking Tools** (relevant to recipe method):
- Cast iron skillet for searing
- Non-stick pan for stir-fry
- Slow cooker for one-pot meals
- Instant Pot for pressure cooking
- Chef's knife, cutting board
- Measuring cups/spoons
- Mixing bowls
- Spatulas, tongs, ladles

**Ingredients** (bulk/pantry staples):
- Bulk rice (5lb bags)
- Pasta variety packs
- Canned goods (tomatoes, beans)
- Spice sets
- Olive oil, cooking spray
- Bouillon cubes, broth

**Storage & Meal Prep**:
- Glass meal prep containers
- Freezer bags
- Food saver systems
- Lunch boxes
- Portion control containers

**Serving & Presentation**:
- Serving bowls
- Dinner plates sets
- Utensils

**Cookbooks & Guides**:
- Budget cooking cookbooks
- Meal prep guides
- Slow cooker recipe books

## Placement Strategy

### 1. Top-of-Page Product Callout (ABOVE the fold)
Add a prominent section right after recipe intro:

```html
<div class="featured-products">
  <h3>🛒 Recommended for This Recipe</h3>
  <div class="product-grid">
    <a href="[amazon-link]" class="product-card" rel="nofollow sponsored">
      <strong>Cast Iron Skillet</strong>
      <span class="price">~$25</span>
    </a>
    <a href="[amazon-link]" class="product-card" rel="nofollow sponsored">
      <strong>Ground Meat Chopper</strong>
      <span class="price">~$10</span>
    </a>
  </div>
</div>
```

### 2. Inline Contextual Links (within instructions)
Add 2-3 inline product mentions in the recipe instructions:

```html
<p>Step 3: Use a <a href="[amazon-link]" class="inline-affiliate" rel="nofollow sponsored">ground meat chopper</a> to break up the beef perfectly while it cooks.</p>
```

### 3. Expanded "Tools & Equipment" Section (bottom)
Keep the bottom section but make it more detailed:
- Show 5-8 products with brief descriptions
- Use visual buttons/cards instead of plain text links
- Include price ranges
- Add "Why I recommend this" mini-reviews

### 4. NEW: "Kitchen Essentials" Dedicated Page
Create a new page: `public/kitchen-essentials.html`
- "Best Budget Kitchen Tools Under $50"
- Comparison tables (e.g., "Best Budget Chef Knives Compared")
- Honest reviews of products you "use"
- Link to this page from every recipe

## CSS Styling for Clickability

Add these classes to `public/css/style.css`:

```css
.cta-button {
  background: #ff9900; /* Amazon orange */
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  display: inline-block;
  margin: 5px;
}

.product-card {
  border: 2px solid #ff9900;
  padding: 15px;
  border-radius: 8px;
  background: #fff5e6;
  text-align: center;
  display: inline-block;
  margin: 10px;
}

.inline-affiliate {
  color: #ff9900;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}

.featured-products {
  background: #fffaf0;
  border-left: 4px solid #ff9900;
  padding: 20px;
  margin: 20px 0;
}
```

## Amazon Affiliate Link Format
ALL links must use proper Amazon Associates format:
```
https://www.amazon.com/dp/[ASIN]/ref=nosim?tag=nunodarwin-20
```

Tag: `nunodarwin-20` (already confirmed in existing pages)

## Product Research Process

For EACH recipe page:
1. Read the recipe carefully
2. Identify:
   - What cooking tool is needed? (pan, pot, knife, etc.)
   - What ingredients could be bought in bulk? (rice, pasta, spices)
   - What storage is needed? (meal prep containers)
3. Search Amazon for each product category
4. Pick 8-12 products with:
   - Good reviews (4+ stars)
   - Budget-friendly prices ($10-$40 range)
   - High relevance to the recipe

## Deliverables

1. **Updated ALL existing recipe pages** (10 pages) with:
   - Top-of-page featured products section
   - 2-3 inline affiliate links in instructions
   - Expanded bottom tools section
   - Visual button/card styling

2. **New page:** `public/kitchen-essentials.html`
   - Comprehensive buying guide
   - Comparison tables
   - 30+ product recommendations organized by category

3. **Updated CSS** with clickable affiliate link styles

4. **Product tracking spreadsheet** in `tasks/amazon-products.csv`:
   ```
   recipe_page,product_name,asin,category,placement,price
   budget-chicken-stir-fry.html,Cast Iron Skillet,B00006JSUB,cooking-tool,featured,$25
   ```

5. **Report in task-log.md** with:
   - Total products added per page
   - Placement strategy used
   - CSS improvements made
   - Estimated impact on CTR

## Success Criteria
✅ 8-12 products per recipe page  
✅ Featured products section ABOVE the fold on all pages  
✅ Inline affiliate links in recipe instructions  
✅ Visual styling makes links stand out (orange buttons, cards)  
✅ New "Kitchen Essentials" page created  
✅ All affiliate links use correct Amazon Associates tag  
✅ Product choices are contextually relevant and budget-appropriate

## Testing
Before completing:
- Click every affiliate link to verify it works
- Check that all links use `rel="nofollow sponsored"`
- Verify Amazon Associates tag: `nunodarwin-20`
- Test on mobile - are product cards readable?

## Notes
- Focus on BUDGET products ($10-$40 range) - stay on brand
- Authenticity matters - recommend products that actually help
- Don't be spammy - every product should have a reason to be there
- Track which products get clicks in Amazon Associates dashboard
