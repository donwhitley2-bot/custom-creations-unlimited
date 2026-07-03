/* ==========================================================================
   Custom Creations Unlimited — Storefront (shop.html + order.html)
   Self-contained: no dependency on main.js internals, no backend required.
   --------------------------------------------------------------------------
   ⚙️  WHERE TO PLUG IN YOUR ACCOUNTS (this is the only block you need to edit)
   ========================================================================== */
const SHOP_CONFIG = {
  currency: "$",

  /* Stripe Payment Links — one per product id below.
     Create them in your Stripe Dashboard → Payment Links (no monthly fee,
     just ~2.9% + 30¢ per sale). Paste each URL here. While a value is left
     empty (""), that product falls back to the "email me a secure invoice"
     flow instead of instant card checkout. */
  stripeLinks: {
    "whiskey-glasses": "https://buy.stripe.com/4gM4gz3SB0h8fhZ3fHfrW00",
    "engraved-tumbler": "",
    "cutting-board": "",
    "coffee-mug": "",
    "crystal-award": "",
    "slate-coasters": ""
  },

  /* Where the customization details + uploaded artwork are sent when a
     customer places an order. Defaults to your existing Formspree endpoint.
     NOTE: file uploads require Formspree's paid tier (or another endpoint
     that accepts multipart/form-data). If the POST fails for any reason,
     the form automatically falls back to opening the customer's email app. */
  formEndpoint: "https://formspree.io/f/xykqkqao",
  notifyEmail: "info@ccucustom.com"
};

/* --------------------------------------------------------------------------
   PRODUCT CATALOG — single source of truth for the shop.
   Edit names / prices / images here. `personalize:true` shows the
   name/initial + artwork-upload fields on the order page.
   -------------------------------------------------------------------------- */
const PRODUCTS = [
  { id: "whiskey-glasses", name: "Personalized Whiskey Glasses", price: 42.99, unit: "set of 2",
    img: "assets/img/drinkware-3.webp", cat: "Drinkware",
    blurb: "A pair of heavy-base rocks glasses, laser-etched with the name, initial or monogram of your choice.",
    personalize: true },
  { id: "engraved-tumbler", name: "Engraved Stainless Tumbler", price: 27.99, unit: "each",
    img: "assets/img/prod-engravedtumblers.webp", cat: "Drinkware",
    blurb: "Double-wall insulated tumbler, deep-etched with your name or logo — dishwasher-safe and built to last.",
    personalize: true },
  { id: "cutting-board", name: "Custom Engraved Cutting Board", price: 39.99, unit: "each",
    img: "assets/img/prod-cuttingboards.webp", cat: "Kitchen",
    blurb: "Solid hardwood board engraved with a family name, monogram or custom artwork — a wedding & housewarming favorite.",
    personalize: true },
  { id: "coffee-mug", name: "Personalized Coffee Mug", price: 18.99, unit: "each",
    img: "assets/img/drinkware-1.webp", cat: "Drinkware",
    blurb: "Classic ceramic mug with an elegant etched or printed monogram in the color of your choice.",
    personalize: true },
  { id: "crystal-award", name: "Crystal Recognition Award", price: 59.99, unit: "each",
    img: "assets/img/prod-crystal.webp", cat: "Awards",
    blurb: "Premium optical-crystal award, laser-engraved with names, dates and your logo for standout recognition.",
    personalize: true },
  { id: "slate-coasters", name: "Engraved Slate Coaster Set", price: 24.99, unit: "set of 4",
    img: "assets/img/prod-slate.webp", cat: "Home",
    blurb: "Natural slate coasters with cork backing, engraved with a monogram, logo or short message.",
    personalize: true }
];

/* ========================================================================== */

const money = (n) => SHOP_CONFIG.currency + Number(n).toFixed(2);
const findProduct = (id) => PRODUCTS.find((p) => p.id === id) || null;
const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/* ---------- SHOP GRID (shop.html) ---------------------------------------- */
function renderShopGrid() {
  const grid = document.getElementById("shopGrid");
  if (!grid) return;
  grid.innerHTML = PRODUCTS.map((p, i) => `
    <article class="product-card" data-reveal data-delay="${i % 3}">
      <a class="product-card__media" href="order.html?item=${encodeURIComponent(p.id)}" aria-label="Customize ${esc(p.name)}">
        <img src="${p.img}" alt="${esc(p.name)}" loading="lazy" decoding="async" />
        <span class="product-card__tag">${esc(p.cat)}</span>
      </a>
      <div class="product-card__body">
        <h3 class="product-card__name">${esc(p.name)}</h3>
        <p class="product-card__blurb">${esc(p.blurb)}</p>
        <div class="product-card__foot">
          <span class="price">${money(p.price)}<small>/ ${esc(p.unit)}</small></span>
          <a class="btn btn--gold" href="order.html?item=${encodeURIComponent(p.id)}">Customize &amp; Order</a>
        </div>
      </div>
    </article>`).join("");
}

/* ---------- ORDER PAGE (order.html) -------------------------------------- */
function renderOrderPage() {
  const root = document.getElementById("orderRoot");
  if (!root) return;

  const params = new URLSearchParams(window.location.search);
  const product = findProduct(params.get("item"));

  if (!product) {
    root.innerHTML = `
      <div class="order-empty">
        <h1>Product not found</h1>
        <p class="muted">That item isn't in our shop. Browse everything we make to order.</p>
        <a class="btn btn--gold btn--lg" href="shop.html">Back to the shop</a>
      </div>`;
    return;
  }

  const hasStripe = !!SHOP_CONFIG.stripeLinks[product.id];
  const payLabel = hasStripe
    ? `Continue to secure payment — ${money(product.price)}`
    : `Submit order — we'll email your invoice`;

  root.innerHTML = `
    <div class="order-layout">
      <aside class="order-summary" data-reveal>
        <div class="order-summary__media"><img src="${product.img}" alt="${esc(product.name)}" /></div>
        <span class="product-card__tag order-summary__tag">${esc(product.cat)}</span>
        <h1 class="order-summary__name">${esc(product.name)}</h1>
        <p class="order-summary__blurb">${esc(product.blurb)}</p>
        <div class="order-summary__price">${money(product.price)} <small>/ ${esc(product.unit)}</small></div>
        <ul class="order-summary__trust">
          <li>Free design proof before we produce</li>
          <li>Made in-house in Atlanta, GA</li>
          <li>Secure checkout — cards & Apple Pay</li>
        </ul>
      </aside>

      <div class="order-form-wrap" data-reveal data-delay="1">
        <form class="form order-form" id="orderForm" novalidate>
          <input type="hidden" name="Product" value="${esc(product.name)}" />
          <input type="hidden" name="Price" value="${money(product.price)}" />
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true" />

          <h2 class="order-form__step">1 · Personalize it</h2>
          ${product.personalize ? `
          <div class="field"><label for="o-perz">Name / initial / monogram to engrave <span class="req">*</span></label>
            <input class="input" id="o-perz" name="Personalization" placeholder="e.g. “MORRIS”, “A”, or “The Smith Family”" required /></div>
          <div class="field" style="margin-top:1.2rem"><span class="field-label">Reference photo or logo (optional)</span>
            <label class="upload"><input type="file" name="Artwork" accept="image/*,.pdf,.ai,.eps,.svg">
              <svg viewBox="0 0 24 24" fill="none"><path d="M12 16V4M7 9l5-5 5 5M5 20h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <strong>Click to upload</strong> or drag &amp; drop<br><span style="font-size:.8rem">PNG, JPG, PDF, AI, EPS or SVG</span>
              <span class="upload__name" hidden></span>
            </label>
            <span class="hint">Your artwork uploads securely with your order — we'll send a free proof before we produce anything.</span></div>
          ` : ""}
          <div class="field" style="margin-top:1.2rem"><label for="o-qty">Quantity <span class="req">*</span></label>
            <input class="input" type="number" min="1" value="1" id="o-qty" name="Quantity" required style="max-width:160px" /></div>

          <h2 class="order-form__step">2 · Your details</h2>
          <div class="form-row">
            <div class="field"><label for="o-name">Full name <span class="req">*</span></label><input class="input" id="o-name" name="Name" required /></div>
            <div class="field"><label for="o-email">Email <span class="req">*</span></label><input class="input" type="email" id="o-email" name="Email" required /></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="o-phone">Phone</label><input class="input" type="tel" id="o-phone" name="Phone" /></div>
            <div class="field"><label for="o-ship">Delivery</label>
              <select class="select" id="o-ship" name="Delivery"><option>Ship to me</option><option>Local pickup (Atlanta)</option></select></div>
          </div>

          <div id="shipFields">
            <h2 class="order-form__step">3 · Shipping address</h2>
            <div class="field"><label for="o-addr1">Street address <span class="req">*</span></label>
              <input class="input" id="o-addr1" name="Address" placeholder="123 Main St" autocomplete="address-line1" required /></div>
            <div class="field" style="margin-top:1rem"><label for="o-addr2">Apt / suite <span class="muted">(optional)</span></label>
              <input class="input" id="o-addr2" name="Address line 2" placeholder="Apartment, suite, unit" autocomplete="address-line2" /></div>
            <div class="form-row" style="margin-top:1rem">
              <div class="field"><label for="o-city">City <span class="req">*</span></label><input class="input" id="o-city" name="City" autocomplete="address-level2" required /></div>
              <div class="field"><label for="o-state">State <span class="req">*</span></label><input class="input" id="o-state" name="State" autocomplete="address-level1" required /></div>
            </div>
            <div class="form-row" style="margin-top:1rem">
              <div class="field"><label for="o-zip">ZIP code <span class="req">*</span></label><input class="input" id="o-zip" name="ZIP" inputmode="numeric" autocomplete="postal-code" required /></div>
              <div class="field"><label for="o-country">Country</label><input class="input" id="o-country" name="Country" value="United States" autocomplete="country-name" /></div>
            </div>
          </div>

          <div class="field" style="margin-top:1.4rem"><label for="o-notes">Notes / special instructions</label>
            <textarea class="textarea" id="o-notes" name="Notes" placeholder="Font preference, colors, spelling, event date…"></textarea></div>

          <button class="btn btn--gold btn--lg" type="submit" id="orderSubmit">
            ${payLabel}
            <svg viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <p class="muted" style="font-size:.82rem">Secure checkout via Stripe. We send a free proof before anything is produced.</p>
        </form>

        <div class="form-success order-success" hidden>
          <div class="form-success__icon"><svg viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
          <h2 class="order-success__head">Order details received!</h2>
          <p class="muted order-success__msg"></p>
          <div class="order-success__actions" style="margin-top:1.4rem"></div>
        </div>
      </div>
    </div>`;

  wireOrderForm(product, hasStripe);
}

function wireOrderForm(product, hasStripe) {
  const form = document.getElementById("orderForm");
  const successPanel = document.querySelector(".order-success");
  const submitBtn = document.getElementById("orderSubmit");
  if (!form) return;

  // Show/hide the shipping address based on the Delivery choice. Required must be
  // toggled off when hidden, or the browser blocks submit on an unfocusable field.
  const deliverySel = document.getElementById("o-ship");
  const shipFields = document.getElementById("shipFields");
  const shipReq = shipFields ? shipFields.querySelectorAll("#o-addr1, #o-city, #o-state, #o-zip") : [];
  const syncShipping = () => {
    if (!deliverySel || !shipFields) return;
    const pickup = /pickup/i.test(deliverySel.value);
    shipFields.hidden = pickup;
    shipReq.forEach((el) => { el.required = !pickup; el.disabled = pickup; });
  };
  if (deliverySel) { deliverySel.addEventListener("change", syncShipping); syncShipping(); }

  const showSuccess = () => {
    form.hidden = true;
    successPanel.hidden = false;
    const msg = successPanel.querySelector(".order-success__msg");
    const actions = successPanel.querySelector(".order-success__actions");
    const stripeUrl = SHOP_CONFIG.stripeLinks[product.id];
    if (stripeUrl) {
      msg.textContent = "Your customization is saved. Click below to pay securely by card — we'll email a free proof before we produce anything.";
      actions.innerHTML =
        `<a class="btn btn--gold btn--lg" href="${stripeUrl}">Pay ${money(product.price)} securely</a>
         <a class="btn btn--ghost btn--lg" href="shop.html">Keep shopping</a>`;
    } else {
      msg.textContent = "Thanks! We've got your details and will email you a secure payment invoice (usually within one business day), along with a free proof to approve.";
      actions.innerHTML = `<a class="btn btn--gold btn--lg" href="shop.html">Keep shopping</a>`;
    }
    successPanel.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  const mailtoFallback = () => {
    const get = (n) => { const el = form.elements[n]; return el ? el.value : ""; };
    const lines = [
      "New online order", "",
      "Product: " + product.name,
      "Price: " + money(product.price),
      "Quantity: " + get("Quantity"),
      product.personalize ? "Personalization: " + get("Personalization") : "",
      "Delivery: " + get("Delivery"),
      "Notes: " + get("Notes"), "",
      "Name: " + get("Name"),
      "Email: " + get("Email"),
      "Phone: " + get("Phone"),
      "", "(Please attach your reference artwork to this email.)"
    ].filter(Boolean);
    const href = "mailto:" + SHOP_CONFIG.notifyEmail +
      "?subject=" + encodeURIComponent("Online order: " + product.name) +
      "&body=" + encodeURIComponent(lines.join("\n"));
    window.location.href = href;
    showSuccess();
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (form.elements["_gotcha"] && form.elements["_gotcha"].value) return; // honeypot

    submitBtn.disabled = true;
    submitBtn.classList.add("is-loading");

    const stripeUrl = SHOP_CONFIG.stripeLinks[product.id];

    // Best-effort: record the customization details before payment.
    // Uses a timeout so a slow/blocked endpoint can never strand the customer.
    let sent = false;
    if (SHOP_CONFIG.formEndpoint) {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 7000);
      try {
        const fd = new FormData(form);
        fd.append("_orderpage", window.location.href);
        const res = await fetch(SHOP_CONFIG.formEndpoint, {
          method: "POST", body: fd, headers: { Accept: "application/json" }, signal: ctrl.signal
        });
        sent = res.ok;
      } catch (_) { sent = false; }
      finally { clearTimeout(timer); }
    }

    // If this product has a Stripe link, go straight to secure card checkout.
    if (stripeUrl) {
      window.location.href = stripeUrl;   // navigating away; leave button in loading state
      return;
    }

    // No Stripe link yet → fall back to the "email me an invoice" flow.
    submitBtn.disabled = false;
    submitBtn.classList.remove("is-loading");
    if (sent) showSuccess();
    else mailtoFallback();
  });
}

/* ---------- reveal + upload wiring for dynamically injected content -------
   main.js binds [data-reveal] and .upload at page load, before this script
   injects the shop markup — so we re-wire our own nodes here. -------------- */
function revealize(scope) {
  const els = (scope || document).querySelectorAll("[data-reveal]:not(.is-in)");
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) {
    els.forEach((el) => el.classList.add("is-in"));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  els.forEach((el) => io.observe(el));
}

function wireUploads(scope) {
  (scope || document).querySelectorAll(".upload").forEach((zone) => {
    const input = zone.querySelector("input[type=file]");
    const nameEl = zone.querySelector(".upload__name");
    if (!input || zone.dataset.wired) return;
    zone.dataset.wired = "1";
    const showName = () => {
      if (!input.files || !input.files.length) { nameEl.hidden = true; return; }
      nameEl.textContent = input.files.length > 1
        ? input.files.length + " files selected"
        : input.files[0].name;
      nameEl.hidden = false;
    };
    input.addEventListener("change", showName);
    ["dragenter", "dragover"].forEach((ev) =>
      zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add("is-drag"); }));
    ["dragleave", "drop"].forEach((ev) =>
      zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove("is-drag"); }));
    zone.addEventListener("drop", (e) => {
      if (e.dataTransfer && e.dataTransfer.files.length) { input.files = e.dataTransfer.files; showName(); }
    });
  });
}

/* ---------- boot ---------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  renderShopGrid();
  renderOrderPage();
  revealize(document);
  wireUploads(document);
});
