#!/usr/bin/env python3
"""
Add 8-12 Amazon affiliate products per recipe page.
- Featured products section above fold
- Inline affiliate links in instructions
- Expanded tools section at bottom
- Update nav to include Kitchen Essentials
"""
import re
import os

BASE = "projects/budget-recipe-blog/public/recipes"

# ─── NAV SNIPPET ─────────────────────────────────────────────────────────────
NAV_OLD = '        <a href="/">Home</a>\n        <a href="/#recipes">Recipes</a>\n    </nav>'
NAV_NEW = '        <a href="/">Home</a>\n        <a href="/#recipes">Recipes</a>\n        <a href="/kitchen-essentials.html">🛒 Kitchen Essentials</a>\n    </nav>'

# ─── AFFILIATE DISCLAIMER ────────────────────────────────────────────────────
DISCLOSURE = '''            <div class="affiliate-disclosure">
                <strong>ℹ️ Affiliate Disclosure:</strong> This page contains Amazon affiliate links. We earn a small commission at no extra cost to you when you purchase through our links. We only recommend products we genuinely believe will help you cook on a budget.
            </div>'''

# ─── PER-PAGE PRODUCT DATA ───────────────────────────────────────────────────
PAGES = {
    "budget-chicken-recipes.html": {
        "intro_trigger": "These 10 recipes show you how to stretch affordable chicken into delicious family meals for under $15.",
        "featured": [
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
            ("🥩", "Nordic Ware Half Sheet Pan", "B000G0KJG4", "~$25", "★★★★★"),
            ("🌡️", "ThermoPro Meat Thermometer", "B01IHHLB3W", "~$12", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("🫙", "Pyrex 3-pc Glass Baking Set", "B00F23EDLK", "~$30", "★★★★★"),
        ],
        "inline_replacements": [
            ("large wok or skillet", 'large <a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a>'),
            ("large baking sheet", 'large <a href="https://www.amazon.com/dp/B000G0KJG4?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">half sheet pan</a>'),
            ("baking dish", '<a href="https://www.amazon.com/dp/B00F23EDLK?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">glass baking dish</a>'),
        ],
        "tools": [
            ("B07QQ8YTFW", "Cuisinart 12\" Nonstick Skillet", "~$38", "Non-stick surface releases food easily — perfect for searing chicken without sticking or burning."),
            ("B00004OCKQ", "OXO Good Grips 12\" Tongs", "~$12", "Flip and serve chicken safely. Spring-loaded, dishwasher safe, won't scratch pans."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Heat-resistant to 600°F. Great for sauces, basting, and scraping every last bit from pans."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Accurate measurements matter for marinades and sauces. Clear markings, easy pour spout."),
            ("B00FLYWNYQ", "Instant Pot Duo 6qt 7-in-1", "~$80", "Pressure-cook chicken from frozen in 15 min. Slow cooker, rice cooker, steamer all-in-one."),
            ("B00OGKJHQ0", "Budget Bytes Cookbook", "~$16", "80+ cheap, delicious recipes with cost-per-serving breakdowns. Perfect companion to this blog."),
        ],
    },
    "budget-ground-beef-recipes.html": {
        "intro_trigger": "These recipes show you how to stretch 1-2 pounds into hearty meals that feed your whole family for under $15.",
        "featured": [
            ("🥩", "Ground Meat Chopper Tool", "B00UXIO9U8", "~$10", "★★★★★"),
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("🫙", "Pyrex Glass Baking Dish Set", "B00F23EDLK", "~$30", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
        ],
        "inline_replacements": [
            ("large skillet", '<a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a>'),
            ("breaking it up as it cooks", 'breaking it up with a <a href="https://www.amazon.com/dp/B00UXIO9U8?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">ground meat chopper</a> as it cooks'),
            ("wok or large skillet", '<a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet or wok</a>'),
        ],
        "tools": [
            ("B00MVVIF0G", "Fat Separator Pitcher", "~$12", "Pour off excess fat from ground beef without losing the meat juices. Essential for healthier cooking."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Measure broth, sauces, and spices accurately. Stackable, clear markings, pour spout."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Scrape every last bit of sauce from pans. Heat safe to 600°F, dishwasher safe."),
            ("B00B4CJNVE", "OXO Good Grips Colander 5qt", "~$20", "Drain pasta, rinse beans, strain ground beef fat. Stable base, easy to handle."),
            ("B00RSBQRDC", "Barilla Pasta Variety 4-pack", "~$10", "Stock your pantry with spaghetti, penne, rotini, and rigatoni for quick ground beef meals."),
            ("B003HNLSLE", "Crock-Pot 6qt Slow Cooker", "~$35", "Make chili and bolognese while you're at work. Set it, forget it, come home to dinner."),
        ],
    },
    "budget-meal-prep-chicken.html": {
        "intro_trigger": None,  # will use first <p> after h1
        "featured": [
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("⚡", "Instant Pot Duo 6qt 7-in-1", "B00FLYWNYQ", "~$80", "★★★★★"),
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
            ("🥩", "Nordic Ware Half Sheet Pan", "B000G0KJG4", "~$25", "★★★★★"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
            ("🌡️", "ThermoPro Meat Thermometer", "B01IHHLB3W", "~$12", "★★★★★"),
        ],
        "inline_replacements": [
            ("large baking sheet", 'large <a href="https://www.amazon.com/dp/B000G0KJG4?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">half sheet pan</a>'),
            ("airtight containers", '<a href="https://www.amazon.com/dp/B01N6A5JZ7?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">airtight glass meal prep containers</a>'),
        ],
        "tools": [
            ("B074ZJ9PBN", "Rubbermaid Brilliance 10pc Set", "~$35", "Crystal-clear containers with 100% leak-proof lids. Stack perfectly in fridge, microwave safe."),
            ("B00NH7V9IU", "Ziploc Gallon Freezer Bags 30ct", "~$8", "Marinate, store, and freeze chicken portions. Heavy-duty, double zipper seal."),
            ("B0007GAWRS", "OXO Good Grips Food Scale", "~$50", "Portion control made easy. Weigh proteins and carbs accurately for macro tracking."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Move and serve chicken without tearing. Heat-resistant, flexible, dishwasher safe."),
            ("B077BQRLT3", "Meal Prep: Complete Guide", "~$15", "48 weekly meal prep plans with shopping lists. Saves hours and money every week."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Accurate sauces and marinades every time. Angled interior so you can read from above."),
        ],
    },
    "budget-slow-cooker-recipes.html": {
        "intro_trigger": None,
        "featured": [
            ("🍲", "Crock-Pot 6qt Slow Cooker", "B003HNLSLE", "~$35", "★★★★★"),
            ("⚡", "Instant Pot Duo 6qt 7-in-1", "B00FLYWNYQ", "~$80", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
            ("🌡️", "ThermoPro Meat Thermometer", "B01IHHLB3W", "~$12", "★★★★★"),
        ],
        "inline_replacements": [
            ("slow cooker", '<a href="https://www.amazon.com/dp/B003HNLSLE?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">slow cooker</a>'),
        ],
        "tools": [
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Essential for broths and sauces in slow cooker recipes. Stackable with easy-pour spout."),
            ("B00004OCKQ", "OXO Good Grips 12\" Tongs", "~$12", "Transfer meat in and out of your slow cooker safely. Spring-loaded, dishwasher safe."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Scrape out every last bit from your slow cooker insert. Heat safe, flexible."),
            ("B00RSBQRDC", "Barilla Pasta Variety 4-pack", "~$10", "Serve slow-cooker sauces over pasta. Keep all shapes stocked for busy weeknights."),
            ("B074ZJ9PBN", "Rubbermaid Brilliance 10pc Set", "~$35", "Slow cooker leftovers freeze and reheat perfectly in these leak-proof containers."),
            ("B009ICSJ8Y", "Slow Cooker Revolution Cookbook", "~$22", "400+ triple-tested slow cooker recipes from America's Test Kitchen. Worth every penny."),
        ],
    },
    "cheap-breakfast-meal-prep.html": {
        "intro_trigger": None,
        "featured": [
            ("🥩", "Nordic Ware Half Sheet Pan", "B000G0KJG4", "~$25", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("🥣", "OXO 3-pc Mixing Bowl Set", "B01FXN8DIS", "~$30", "★★★★★"),
            ("🍳", "Silicone Spatula Set (6pc)", "B07DNXKRMM", "~$15", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
        ],
        "inline_replacements": [
            ("baking sheet", '<a href="https://www.amazon.com/dp/B000G0KJG4?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">half sheet pan</a>'),
            ("mixing bowl", '<a href="https://www.amazon.com/dp/B01FXN8DIS?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">mixing bowl</a>'),
            ("airtight container", '<a href="https://www.amazon.com/dp/B01N6A5JZ7?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">airtight meal prep container</a>'),
        ],
        "tools": [
            ("B074ZJ9PBN", "Rubbermaid Brilliance 10pc Set", "~$35", "Keep prepped breakfasts fresh all week. Leak-proof lids, microwave and dishwasher safe."),
            ("B00NH7V9IU", "Ziploc Gallon Freezer Bags 30ct", "~$8", "Freeze individual breakfast portions for grab-and-go mornings. Double zipper seal."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Accurate measurements for consistent results every time you batch cook."),
            ("B00M4LVS14", "OXO Measuring Spoon Set", "~$12", "Get spice amounts right every time. Slim design fits in spice jars, stackable."),
            ("B07QQ8YTFW", "Cuisinart 12\" Nonstick Skillet", "~$38", "Perfect for scrambled eggs, pancakes, and breakfast hash. Non-stick for easy cleanup."),
            ("B077BQRLT3", "Meal Prep: Complete Guide", "~$15", "Breakfast meal prep strategies to save 5+ hours every week. Game-changer."),
        ],
    },
    "cheap-dinner-ideas-for-two.html": {
        "intro_trigger": None,
        "featured": [
            ("🍳", "Lodge 10\" Cast Iron Skillet", "B00006JSUB", "~$30", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("🥩", "Bamboo Cutting Board Set", "B08G22BJYC", "~$25", "★★★★☆"),
            ("🥣", "OXO 3-pc Mixing Bowl Set", "B01FXN8DIS", "~$30", "★★★★★"),
            ("🍳", "Silicone Spatula Set (6pc)", "B07DNXKRMM", "~$15", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
        ],
        "inline_replacements": [
            ("skillet over", '<a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a> over'),
            ("cutting board", '<a href="https://www.amazon.com/dp/B08G22BJYC?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cutting board</a>'),
        ],
        "tools": [
            ("B07QQ8YTFW", "Cuisinart 10\" Nonstick Skillet", "~$30", "Right size for two servings. Non-stick means less oil needed and easier cleanup."),
            ("B00004OCKQ", "OXO Good Grips 9\" Tongs", "~$10", "Flip proteins and toss vegetables with precision. Compact size perfect for cooking for two."),
            ("B0002IHMCU", "OXO Good Grips Can Opener", "~$12", "Opens any can smoothly. Essential for budget cooking with canned beans, tomatoes, tuna."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Half-portions need precise measuring. These nest and stack to save cabinet space."),
            ("B00M4LVS14", "OXO Measuring Spoon Set", "~$12", "Get seasoning right on smaller portions. Fits in spice jars, dishwasher safe."),
            ("B00KLTU47A", "Complete Cooking for Two Cookbook", "~$22", "250+ recipes scaled for 2 people. Every recipe has a cost breakdown. Perfect gift idea."),
        ],
    },
    "cheap-healthy-dinners.html": {
        "intro_trigger": None,
        "featured": [
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("🥩", "Bamboo Cutting Board Set", "B08G22BJYC", "~$25", "★★★★☆"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("🥩", "Nordic Ware Half Sheet Pan", "B000G0KJG4", "~$25", "★★★★★"),
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
        ],
        "inline_replacements": [
            ("sheet pan", '<a href="https://www.amazon.com/dp/B000G0KJG4?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">sheet pan</a>'),
            ("cast iron", '<a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a>'),
        ],
        "tools": [
            ("B07QQ8YTFW", "Cuisinart 12\" Nonstick Skillet", "~$38", "Cook with minimal oil for healthier meals. Heats evenly, easy cleanup, oven safe to 400°F."),
            ("B00004OCKQ", "OXO Good Grips 12\" Tongs", "~$12", "Toss salads, flip proteins, serve vegetables — the most-used tool in a healthy kitchen."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Low-fat cooking means you need every drop of sauce. Flexible spatulas scrape clean."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Portion control and accurate recipe measurements. The cornerstone of healthy cooking."),
            ("B00B4CJNVE", "OXO Good Grips Colander 5qt", "~$20", "Drain vegetables, rinse beans, strain pasta. A must-have for veggie-forward meals."),
            ("B00OGKJHQ0", "Budget Bytes Cookbook", "~$16", "100+ healthy recipes with full cost breakdowns. Eat well for under $5 per serving."),
        ],
    },
    "cheap-pasta-dishes-for-students.html": {
        "intro_trigger": "These pasta dishes are cheap, quick, and actually taste good.",
        "featured": [
            ("🍝", "Barilla Pasta Variety 4-pack", "B00RSBQRDC", "~$10", "★★★★★"),
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("🫙", "OXO Good Grips Colander 5qt", "B00B4CJNVE", "~$20", "★★★★★"),
            ("🥣", "OXO 3-pc Mixing Bowl Set", "B01FXN8DIS", "~$30", "★★★★★"),
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("🧀", "Box Grater Cuisipro 4-Sided", "B00000JJOP", "~$15", "★★★★★"),
        ],
        "inline_replacements": [
            ("large pot", '<a href="https://www.amazon.com/dp/B00B4CJNVE?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">large stockpot</a>'),
            ("fry bacon", 'fry bacon in a <a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a>'),
            ("Parmesan, grated", '<a href="https://www.amazon.com/dp/B00000JJOP?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">freshly grated Parmesan</a>'),
        ],
        "tools": [
            ("B07G1N1HVK", "Sistema Microwave Pasta Cooker", "~$12", "Cook pasta in the microwave — perfect for dorms. No stove needed, BPA-free."),
            ("B00006JSUB", "Lodge 12\" Cast Iron Skillet", "~$35", "Works on hot plates, gas, and electric. Sear bacon and sauté garlic perfectly."),
            ("B074ZJ9PBN", "Rubbermaid Brilliance 10pc Set", "~$35", "Store leftover pasta safely in the fridge. Leak-proof, clear, microwave safe."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Measure pasta water and sauce amounts accurately. Stackable, dorm-room friendly."),
            ("B00M4LVS14", "OXO Measuring Spoon Set", "~$12", "Season perfectly every time. Essential for carbonara and garlic pasta ratios."),
            ("B00OGKJHQ0", "Budget Bytes Cookbook", "~$16", "Over 100 cheap, student-friendly recipes including 20+ pasta dishes. Under $5/serving."),
        ],
    },
    "cheap-vegetarian-meals.html": {
        "intro_trigger": None,
        "featured": [
            ("🔪", "Victorinox 8\" Chef's Knife", "B0019WXIDO", "~$35", "★★★★★"),
            ("🥩", "Bamboo Cutting Board Set", "B08G22BJYC", "~$25", "★★★★☆"),
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
            ("⚡", "Instant Pot Duo 6qt 7-in-1", "B00FLYWNYQ", "~$80", "★★★★★"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
            ("🫙", "OXO Good Grips Colander 5qt", "B00B4CJNVE", "~$20", "★★★★★"),
        ],
        "inline_replacements": [
            ("large skillet", '<a href="https://www.amazon.com/dp/B00006JSUB?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cast iron skillet</a>'),
            ("cutting board", '<a href="https://www.amazon.com/dp/B08G22BJYC?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">cutting board</a>'),
        ],
        "tools": [
            ("B07QQ8YTFW", "Cuisinart 12\" Nonstick Skillet", "~$38", "Perfect for stir-fries and sautéed veggies. Even heat, easy cleanup, minimal oil needed."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Measure grains, legumes, and sauces accurately. Stackable, microwave-safe."),
            ("B01FXN8DIS", "OXO 3-pc Mixing Bowl Set", "~$30", "Toss salads, marinate tofu, mix dressings. Lids included for fridge storage."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Fold, stir, and scrape without scratching pans. Essential for tofu and bean dishes."),
            ("B01N6A5JZ7", "Glass Meal Prep Containers", "~$28", "Store pre-portioned vegetarian meals. Glass doesn't absorb smells like plastic."),
            ("B00B6Q3CPO", "Oh She Glows Cookbook", "~$20", "100+ plant-based recipes from scratch. Budget-friendly, crowd-pleasing, fully vegan."),
        ],
    },
    "easy-meal-prep-under-20.html": {
        "intro_trigger": None,
        "featured": [
            ("📦", "Glass Meal Prep Containers", "B01N6A5JZ7", "~$28", "★★★★☆"),
            ("⚡", "Instant Pot Duo 6qt 7-in-1", "B00FLYWNYQ", "~$80", "★★★★★"),
            ("🍳", "Lodge 12\" Cast Iron Skillet", "B00006JSUB", "~$35", "★★★★★"),
            ("⚖️", "OXO Digital Kitchen Scale", "B0007GAWRS", "~$50", "★★★★★"),
            ("🥩", "Nordic Ware Half Sheet Pan", "B000G0KJG4", "~$25", "★★★★★"),
            ("🌡️", "ThermoPro Meat Thermometer", "B01IHHLB3W", "~$12", "★★★★★"),
        ],
        "inline_replacements": [
            ("sheet pan", '<a href="https://www.amazon.com/dp/B000G0KJG4?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">sheet pan</a>'),
            ("meal prep container", '<a href="https://www.amazon.com/dp/B01N6A5JZ7?tag=nunodarwin-20" class="inline-affiliate" target="_blank" rel="nofollow sponsored">meal prep container</a>'),
        ],
        "tools": [
            ("B074ZJ9PBN", "Rubbermaid Brilliance 10pc Set", "~$35", "Crystal-clear so you always know what's inside. Leak-proof for commute-safe meal prep."),
            ("B00NH7V9IU", "Ziploc Gallon Freezer Bags 30ct", "~$8", "Freeze bulk-cooked proteins and grains. Label and date for foolproof meal prep."),
            ("B00B4CJNVE", "OXO Good Grips Colander 5qt", "~$20", "Drain grains, beans, and pasta quickly. Stable base, comfortable handles."),
            ("B0000CFT9Q", "OXO Measuring Cup Set", "~$15", "Consistent portions = consistent macros. Essential for any meal prep routine."),
            ("B07DNXKRMM", "Silicone Spatula Set (6pc)", "~$15", "Portion and serve without wasting food. Flexible enough to scrape containers clean."),
            ("B077BQRLT3", "Meal Prep: Complete Guide", "~$15", "48 weekly meal prep plans with shopping lists. The Bible of budget meal prep."),
        ],
    },
}


def build_featured_block(products):
    cards = ""
    for emoji, name, asin, price, stars in products:
        url = f"https://www.amazon.com/dp/{asin}?tag=nunodarwin-20"
        cards += f'''                    <a href="{url}" class="product-card" target="_blank" rel="nofollow sponsored">
                        <span class="product-emoji">{emoji}</span>
                        <strong>{name}</strong>
                        <span class="stars">{stars}</span>
                        <span class="price">{price}</span>
                    </a>\n'''
    return f'''
            <!-- FEATURED PRODUCTS - above fold -->
            <div class="featured-products">
                <h3>🛒 Recommended for This Recipe</h3>
                <p class="subtitle">Budget-friendly kitchen tools that make this recipe easier (all under $80)</p>
                <div class="product-grid">
{cards}                </div>
                <p style="margin-top:0.75rem;font-size:0.82rem;color:#999;">
                    <em>Amazon affiliate links — we earn a small commission at no extra cost to you.</em>
                </p>
            </div>'''


def build_tools_block(tools):
    cards = ""
    for asin, name, price, desc in tools:
        url = f"https://www.amazon.com/dp/{asin}?tag=nunodarwin-20"
        cards += f'''                    <div class="tool-card">
                        <span class="tool-name">{name}</span>
                        <span class="tool-desc">{desc}</span>
                        <div class="tool-price-row">
                            <span class="tool-price">{price}</span>
                            <a href="{url}" class="tool-btn" target="_blank" rel="nofollow sponsored">View on Amazon →</a>
                        </div>
                    </div>\n'''
    return f'''            <div class="affiliate-box" style="margin-top:2.5rem;">
                <h4>🔧 Complete Kitchen Toolkit for This Recipe</h4>
                <p style="margin-bottom:1rem;color:#555;">Everything you need to cook these recipes with confidence — all budget-friendly and highly rated on Amazon.</p>
                <div class="tools-grid">
{cards}                </div>
                <p style="margin-top:1.5rem;text-align:center;">
                    <a href="/kitchen-essentials.html" style="color:#cc7700;font-weight:700;font-size:1rem;">
                        → Browse the Full Kitchen Essentials Guide (30+ recommended products)
                    </a>
                </p>
            </div>'''


def update_page(filename, data):
    path = os.path.join(BASE, filename)
    with open(path, "r") as f:
        html = f.read()

    # 1. Update nav
    html = html.replace(NAV_OLD, NAV_NEW)

    # 2. Insert featured products after intro paragraph
    trigger = data.get("intro_trigger")
    featured_block = build_featured_block(data["featured"])
    if trigger and trigger in html:
        html = html.replace(trigger, trigger + "\n" + featured_block)
    else:
        # Find the first </p> after <article class="recipe-card">
        article_start = html.find('<article class="recipe-card">')
        if article_start == -1:
            article_start = html.find('<article')
        # Find 2nd </p> after article_start
        first_p_close = html.find("</p>", article_start)
        if first_p_close != -1:
            second_p_close = html.find("</p>", first_p_close + 1)
            if second_p_close != -1:
                insert_pos = second_p_close + 4
                html = html[:insert_pos] + "\n" + featured_block + html[insert_pos:]

    # 3. Inline replacements (replace first occurrence only)
    for old_text, new_text in data.get("inline_replacements", []):
        if old_text in html:
            html = html.replace(old_text, new_text, 1)

    # 4. Replace existing affiliate-box with expanded tools section
    old_box_start = html.find('<div class="affiliate-box">')
    old_box_end = html.find("</div>", old_box_start)
    # Find the actual closing div (may be nested - count levels)
    if old_box_start != -1:
        depth = 0
        i = old_box_start
        while i < len(html):
            if html[i:i+4] == "<div":
                depth += 1
            elif html[i:i+6] == "</div>":
                depth -= 1
                if depth == 0:
                    old_box_end = i + 6
                    break
            i += 1
        tools_block = build_tools_block(data["tools"])
        html = html[:old_box_start] + tools_block + html[old_box_end:]
    else:
        # No affiliate box — append before closing article tag
        tools_block = build_tools_block(data["tools"])
        html = html.replace("</article>", tools_block + "\n        </article>")

    with open(path, "w") as f:
        f.write(html)

    print(f"✅ Updated: {filename}")


def main():
    for filename, data in PAGES.items():
        try:
            update_page(filename, data)
        except Exception as e:
            print(f"❌ Error on {filename}: {e}")


if __name__ == "__main__":
    main()
