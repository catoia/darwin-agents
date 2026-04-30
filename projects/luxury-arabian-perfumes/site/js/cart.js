/**
 * AL MAJD — Shopping Cart
 * localStorage-based cart with Stripe Checkout redirect
 */

const STRIPE_PUBLISHABLE_KEY = 'pk_test_YOUR_STRIPE_KEY_HERE';

// ── Cart State ────────────────────────────────────────────────────────────────
let cart = JSON.parse(localStorage.getItem('almajd_cart') || '[]');

function saveCart() {
  localStorage.setItem('almajd_cart', JSON.stringify(cart));
}

function getCartCount() {
  return cart.reduce((sum, item) => sum + item.qty, 0);
}

function getCartTotal() {
  return cart.reduce((sum, item) => sum + item.price * item.qty, 0);
}

// ── Cart Operations ───────────────────────────────────────────────────────────
function addToCart(productId, qty = 1) {
  const product = PRODUCTS.find(p => p.id === productId);
  if (!product) return;

  const existing = cart.find(i => i.id === productId);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({
      id: product.id,
      name: product.name,
      volume: product.volume,
      price: product.price,
      icon: product.icon,
      qty
    });
  }

  saveCart();
  updateCartUI();
  showCartDrawer();
  showAddedToast(product.name);
}

function removeFromCart(productId) {
  cart = cart.filter(i => i.id !== productId);
  saveCart();
  updateCartUI();
}

function updateQty(productId, delta) {
  const item = cart.find(i => i.id === productId);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    removeFromCart(productId);
    return;
  }
  saveCart();
  updateCartUI();
}

// ── UI Updates ────────────────────────────────────────────────────────────────
function updateCartUI() {
  const count = getCartCount();
  const total = getCartTotal();

  // Badge
  const badge = document.getElementById('cart-count');
  if (badge) {
    badge.textContent = count;
    badge.classList.toggle('visible', count > 0);
  }

  // Items list
  const itemsEl = document.getElementById('cart-items');
  const footerEl = document.getElementById('cart-footer');
  const totalEl  = document.getElementById('cart-total');

  if (!itemsEl) return;

  if (cart.length === 0) {
    itemsEl.innerHTML = '<p class="cart-empty">O seu carrinho está vazio.</p>';
    if (footerEl) footerEl.style.display = 'none';
    return;
  }

  itemsEl.innerHTML = cart.map(item => `
    <div class="cart-item" data-id="${item.id}">
      <div class="cart-item-img" style="background:#161616;display:flex;align-items:center;justify-content:center;font-size:1.8rem;">
        ${item.icon || '✦'}
      </div>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-vol">${item.volume}</div>
        <div class="cart-item-price">€${(item.price * item.qty).toFixed(2)}</div>
        <div class="cart-item-qty">
          <button onclick="updateQty('${item.id}', -1)" aria-label="Diminuir">−</button>
          <span>${item.qty}</span>
          <button onclick="updateQty('${item.id}', 1)" aria-label="Aumentar">+</button>
        </div>
      </div>
      <button class="cart-remove" onclick="removeFromCart('${item.id}')" aria-label="Remover">✕</button>
    </div>
  `).join('');

  if (footerEl) footerEl.style.display = 'flex';
  if (totalEl)  totalEl.textContent = `€${total.toFixed(2)}`;
}

// ── Cart Drawer ───────────────────────────────────────────────────────────────
function showCartDrawer() {
  const drawer  = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  if (drawer)  { drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); }
  if (overlay) overlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function hideCartDrawer() {
  const drawer  = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-overlay');
  if (drawer)  { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); }
  if (overlay) overlay.classList.remove('active');
  document.body.style.overflow = '';
}

// ── Toast Notification ────────────────────────────────────────────────────────
function showAddedToast(productName) {
  const existing = document.querySelector('.cart-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'cart-toast';
  toast.innerHTML = `<span>✦</span> "${productName}" adicionado ao carrinho`;
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '2rem',
    left: '50%',
    transform: 'translateX(-50%) translateY(10px)',
    background: '#1a1a1a',
    border: '1px solid rgba(201,168,76,0.3)',
    color: '#f8f5f0',
    padding: '0.8rem 1.6rem',
    fontSize: '0.78rem',
    letterSpacing: '0.08em',
    zIndex: '1000',
    opacity: '0',
    transition: 'all 0.3s ease',
    whiteSpace: 'nowrap',
    maxWidth: '90vw'
  });
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

// ── Stripe Checkout ───────────────────────────────────────────────────────────
async function initiateCheckout() {
  if (cart.length === 0) return;

  const btn = document.getElementById('checkout-btn');
  if (btn) {
    btn.textContent = 'A preparar checkout…';
    btn.disabled = true;
  }

  try {
    // Build line items for Stripe Checkout (server-side required for real keys)
    // For now, redirect to a pre-built Stripe Payment Link OR use Stripe.js
    // -----------------------------------------------------------------
    // OPTION A: Use Stripe Payment Links (simplest — no backend needed)
    //   Set STRIPE_PAYMENT_LINK below to your Payment Link URL
    // OPTION B: Use Stripe Checkout with backend (create-checkout-session)
    //   Uncomment the fetch() block below and set your backend URL
    // -----------------------------------------------------------------

    const STRIPE_PAYMENT_LINK = 'https://buy.stripe.com/YOUR_PAYMENT_LINK'; // <-- Set this

    // Encode cart as URL params so Stripe Payment Link page shows info
    const params = new URLSearchParams({
      prefilled_email: '',
      client_reference_id: `order_${Date.now()}`,
    });

    // For demo/test mode — redirect to the payment link
    // In production, swap this for a proper server-side session
    window.location.href = `${STRIPE_PAYMENT_LINK}?${params}`;

  } catch (err) {
    console.error('Checkout error:', err);
    if (btn) {
      btn.textContent = 'Finalizar Compra';
      btn.disabled = false;
    }
    alert('Erro ao iniciar o pagamento. Por favor tente novamente ou contacte-nos.');
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  updateCartUI();

  const cartBtn     = document.getElementById('cart-btn');
  const cartClose   = document.getElementById('cart-close');
  const cartOverlay = document.getElementById('cart-overlay');
  const checkoutBtn = document.getElementById('checkout-btn');

  if (cartBtn)     cartBtn.addEventListener('click', showCartDrawer);
  if (cartClose)   cartClose.addEventListener('click', hideCartDrawer);
  if (cartOverlay) cartOverlay.addEventListener('click', hideCartDrawer);
  if (checkoutBtn) checkoutBtn.addEventListener('click', initiateCheckout);

  // Keyboard close
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      hideCartDrawer();
      hideModal();
    }
  });
});

// Expose for inline handlers
window.addToCart     = addToCart;
window.removeFromCart = removeFromCart;
window.updateQty     = updateQty;
