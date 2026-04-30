/**
 * AL MAJD — Main JS
 * Product rendering, modals, filters, animations
 */

// ── Product Rendering ─────────────────────────────────────────────────────────
function renderProducts(filter = 'all') {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  const filtered = filter === 'all'
    ? PRODUCTS
    : PRODUCTS.filter(p => p.category === filter);

  grid.innerHTML = filtered.map(product => `
    <article class="product-card fade-in" data-category="${product.category}" data-id="${product.id}">
      <div class="product-img-wrap" onclick="openModal('${product.id}')">
        ${product.image ? `<img src="${product.image}" alt="${product.name}" class="product-img" loading="lazy" />` : `<div class="product-img-placeholder"><div class="placeholder-icon">${product.icon}</div><div class="placeholder-label">Al Majd</div></div>`}
        ${product.badge ? `<div class="product-badge">${product.badge}</div>` : ''}
      </div>
      <div class="product-info">
        <div class="product-category">${categoryLabel(product.category)}</div>
        <h3 class="product-name">${product.name}</h3>
        <div class="product-volume">${product.volume}</div>
        <div class="product-notes">${product.shortNotes}</div>
        <div class="product-footer">
          <div>
            <span class="product-price">€${product.price}</span>
            ${product.oldPrice ? `<span class="product-old-price">€${product.oldPrice}</span>` : ''}
          </div>
          <button
            class="add-to-cart-btn"
            onclick="event.stopPropagation(); addToCart('${product.id}')"
            aria-label="Adicionar ${product.name} ao carrinho"
          >
            Adicionar
          </button>
        </div>
      </div>
    </article>
  `).join('');

  // Trigger fade-in animations
  requestAnimationFrame(() => {
    grid.querySelectorAll('.fade-in').forEach((el, i) => {
      setTimeout(() => el.classList.add('visible'), i * 80);
    });
  });
}

function categoryLabel(cat) {
  const labels = {
    oud:     'Óleo de Oud',
    attar:   'Attar Puro',
    bakhoor: 'Bakhoor',
    rose:    'Rosa Oriental'
  };
  return labels[cat] || cat;
}

// ── Filters ───────────────────────────────────────────────────────────────────
function initFilters() {
  const btns = document.querySelectorAll('.filter-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;

      const grid = document.getElementById('products-grid');
      if (grid) {
        grid.style.opacity = '0';
        grid.style.transform = 'translateY(8px)';
        grid.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        setTimeout(() => {
          renderProducts(filter);
          grid.style.opacity = '1';
          grid.style.transform = 'none';
        }, 200);
      }
    });
  });
}

// ── Product Modal ─────────────────────────────────────────────────────────────
function openModal(productId) {
  const product = PRODUCTS.find(p => p.id === productId);
  if (!product) return;

  const modal   = document.getElementById('product-modal');
  const overlay = document.getElementById('modal-overlay');
  const content = document.getElementById('modal-content');

  content.innerHTML = `
    <div class="modal-grid">
      <div class="modal-img">
        ${product.image ? `<img src="${product.image}" alt="${product.name}" class="modal-product-img" />` : `<div class="modal-img-placeholder">${product.icon}</div>`}
      </div>
      <div class="modal-details">
        <div class="modal-category">${categoryLabel(product.category)}</div>
        <h2 class="modal-name">${product.name}</h2>
        <div class="modal-volume">${product.volume}</div>
        <p class="modal-desc">${product.description}</p>

        <div>
          <div class="modal-notes-label">Notas de Perfume</div>
          <div class="modal-notes-text">
            <strong>Topo:</strong> ${product.notes.topo}<br />
            <strong>Coração:</strong> ${product.notes.meio}<br />
            <strong>Fundo:</strong> ${product.notes.base}
          </div>
        </div>

        <div class="modal-price">
          €${product.price}
          ${product.oldPrice ? `<span class="product-old-price" style="font-size:1rem">€${product.oldPrice}</span>` : ''}
        </div>

        <div class="modal-actions">
          <button
            class="btn btn-primary"
            onclick="addToCart('${product.id}'); hideModal();"
          >
            Adicionar ao Carrinho
          </button>
          <button class="btn btn-ghost" onclick="hideModal()">Continuar a Ver</button>
        </div>
      </div>
    </div>
  `;

  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function hideModal() {
  const modal   = document.getElementById('product-modal');
  const overlay = document.getElementById('modal-overlay');
  if (modal)   { modal.classList.remove('open'); modal.setAttribute('aria-hidden', 'true'); }
  if (overlay) overlay.classList.remove('active');
  document.body.style.overflow = '';
}

window.openModal = openModal;
window.hideModal = hideModal;

// ── Scroll Animations ─────────────────────────────────────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll(
    '.pillar, .ingredient, .testimonial, .story-text, .story-visual'
  ).forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });
}

// ── Header Scroll Effect ──────────────────────────────────────────────────────
function initHeader() {
  const header = document.getElementById('site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
      header.style.background = 'rgba(5,5,5,0.98)';
    } else {
      header.style.background = 'rgba(10,10,10,0.95)';
    }
  }, { passive: true });
}

// ── Mobile Nav ────────────────────────────────────────────────────────────────
function initMobileNav() {
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  // Close on link click
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });
}

// ── Newsletter Form ───────────────────────────────────────────────────────────
function initNewsletter() {
  const form = document.getElementById('newsletter-form');
  if (!form) return;

  form.addEventListener('submit', e => {
    e.preventDefault();
    const input = form.querySelector('input[type="email"]');
    const email = input?.value;
    if (!email) return;

    // TODO: Connect to your email provider (Mailchimp, Brevo, etc.)
    // For now, show success message
    form.innerHTML = `
      <p style="color:var(--gold);font-size:0.8rem;letter-spacing:0.1em;">
        ✦ Subscrito com sucesso
      </p>
    `;
  });
}

// ── Modal Overlay Click ───────────────────────────────────────────────────────
function initModalClose() {
  const overlay = document.getElementById('modal-overlay');
  const closeBtn = document.getElementById('modal-close');
  if (overlay) overlay.addEventListener('click', hideModal);
  if (closeBtn) closeBtn.addEventListener('click', hideModal);
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  renderProducts();
  initFilters();
  initScrollAnimations();
  initHeader();
  initMobileNav();
  initNewsletter();
  initModalClose();
});
