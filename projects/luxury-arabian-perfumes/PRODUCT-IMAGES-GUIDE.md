# Product Images Guide

## Current Status

The site currently uses **placeholder icons** (🌙, 🌹, ✦, etc.) instead of real product photos.

**This needs to be fixed before marketing launch.**

---

## Quick Fix Options

### Option 1: Use AliExpress Supplier Images (FASTEST - 1 hour)

**Best for immediate launch.**

1. Find your products on AliExpress (see HUMAN-SETUP-GUIDE.md Section 3)
2. Right-click product images → "Save Image As..."
3. Save to: `site/images/products/`
4. Rename to match product IDs:
   ```
   oud-al-qamari.jpg
   royal-rose-attar.jpg
   musk-al-sultan.jpg
   oudh-cambodi-noir.jpg
   bakhoor-al-oud.jpg
   amber-al-sharq.jpg
   white-oud-medina.jpg
   rose-taif-pure.jpg
   oud-malaki.jpg
   mabkhara-set.jpg
   ```

5. Update `site/js/products.js` to reference images:

   For each product, add an `image` field:

   ```javascript
   {
     id: "oud-al-qamari",
     name: "Oud Al Qamari",
     image: "images/products/oud-al-qamari.jpg", // ← ADD THIS LINE
     category: "oud",
     volume: "12ml",
     price: 89,
     // ... rest unchanged
   }
   ```

6. Update `site/js/main.js` to display images:

   Find the `renderProducts()` function, locate this block:

   ```javascript
   <div class="product-img-placeholder">
     <div class="placeholder-icon">${product.icon}</div>
     <div class="placeholder-label">Al Majd</div>
   </div>
   ```

   Replace with:

   ```javascript
   ${product.image 
     ? `<img src="${product.image}" alt="${product.name}" class="product-img" loading="lazy" />` 
     : `<div class="product-img-placeholder">
          <div class="placeholder-icon">${product.icon}</div>
          <div class="placeholder-label">Al Majd</div>
        </div>`
   }
   ```

   Do the same in the modal rendering section (`openModal()` function).

7. Redeploy:
   ```bash
   cd projects/luxury-arabian-perfumes
   wrangler pages deploy site
   ```

**Total time: 1 hour**

---

### Option 2: AI-Generated Images (BETTER QUALITY - 2-3 hours)

**Use if you want unique, luxury-looking images without waiting for physical samples.**

1. Use AI image generator:
   - **DALL-E 3** (via ChatGPT Plus): Best quality
   - **Midjourney**: Professional results
   - **Stable Diffusion**: Free but requires setup
   - **Bing Image Creator**: Free, decent quality

2. Prompt template:
   ```
   Luxury Arabian perfume bottle, [TYPE] oil, elegant black and gold packaging,
   minimalist product photography, clean white background, professional lighting,
   high-end cosmetics, premium quality, 8K resolution
   ```

   Examples:
   - "Luxury Arabian oud oil bottle, 12ml, elegant black glass with gold Arabic calligraphy..."
   - "Premium attar perfume bottle with rose design, luxury Middle Eastern fragrance..."
   - "Wooden bakhoor incense box, luxury Islamic home fragrance, black and gold..."

3. Generate 10 images (one per product)

4. Download as JPG/PNG, save to `site/images/products/`

5. Follow steps 5-7 from Option 1

**Total time: 2-3 hours**

---

### Option 3: Order Samples + Photograph (BEST QUALITY - 2-3 weeks)

**Only do this if business is validated and you're scaling.**

1. Order 3-5 sample products from AliExpress (€15-30 total)
2. Wait 2-3 weeks for delivery
3. Set up simple product photography:
   - White poster board background (€5 from stationery store)
   - Natural window light or cheap ring light (€15-25)
   - Smartphone camera (use portrait mode)
4. Take photos:
   - Multiple angles per product
   - Close-ups of bottles, labels, packaging
   - Lifestyle shots (hand holding bottle, on marble surface, etc.)
5. Edit photos:
   - Use free tools: Canva, Photopea, GIMP
   - Increase brightness, adjust contrast
   - Crop to square (1:1 ratio)
   - Export as JPG (1200x1200px)
6. Save to `site/images/products/`
7. Follow steps 5-7 from Option 1

**Total time: 2-3 weeks (mostly waiting), 3-4 hours active work**

---

## Temporary Solution (Current)

**The placeholders are styled to look premium**, but they're not sellable images.

**DO NOT START MARKETING until you have at least Option 1 (supplier images) implemented.**

---

## Image Requirements

### Technical Specs
- **Format:** JPG or PNG
- **Size:** 800x800px minimum (1200x1200px ideal)
- **Aspect ratio:** 1:1 (square)
- **File size:** <500KB per image
- **Background:** White, transparent, or luxury (black/gold)

### Aesthetic
- ✅ High-quality, sharp, well-lit
- ✅ Shows product clearly (bottle shape, label, cap)
- ✅ Professional/luxury feel (matches AL MAJD brand)
- ✅ Consistent style across all products
- ❌ No watermarks
- ❌ No other products visible
- ❌ No distracting backgrounds

---

## Next Steps

1. **Choose an option** based on urgency:
   - Need to launch THIS WEEK? → Option 1 (supplier images)
   - Want to launch professionally? → Option 2 (AI images)
   - Already validated, scaling? → Option 3 (own photos)

2. **Implement** (follow steps above)

3. **Test** on mobile and desktop (images load correctly, look good)

4. **Deploy** updated site

5. **Then and only then** start marketing (Instagram, etc.)

---

**Questions? Check task-log.md or HUMAN-SETUP-GUIDE.md**
