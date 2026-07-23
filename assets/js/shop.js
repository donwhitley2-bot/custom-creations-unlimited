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
    "slate-coasters": "",
    "tequila-tumbler": "https://buy.stripe.com/6oUbJ188Rd3U3zh4jLfrW01",
    "drink-straight-tumbler": "https://buy.stripe.com/3cI28r60J7JAgm3dUlfrW02",
    "haec-tumbler": "https://buy.stripe.com/fZu28r2Ox8NE9XF17zfrW03",
    "haec-mug": "https://buy.stripe.com/6oU28rgFn8NE1r93fHfrW04",
    "snakes-hiss": "https://buy.stripe.com/eVqaEXdtbd3UfhZaI9frW05",
    "drawstring-bag": "https://buy.stripe.com/4gMcN59cV9RIfhZ9E5frW06",
    "pray-on-it-hoodie": "https://buy.stripe.com/3cIcN59cV4xo2vdaI9frW07",
    "pray-on-it-tee": "https://buy.stripe.com/aFa9ATfBj7JA2vd3fHfrW08",
    "pray-pray-pray": "https://buy.stripe.com/aFa14n9cV4xoc5N17zfrW09",
    "waymaker": "https://buy.stripe.com/eVq9AT0Gp1lc7PxcQhfrW0a",
    "nope-not-today": "https://buy.stripe.com/cNibJ174NbZQedV03vfrW0b",
    "god-fidence": "https://buy.stripe.com/fZufZhfBjbZQ0n5g2tfrW0c"
  },

  /* Where the customization details + uploaded artwork are sent when a
     customer places an order. Defaults to your existing Formspree endpoint.
     NOTE: file uploads require Formspree's paid tier (or another endpoint
     that accepts multipart/form-data). If the POST fails for any reason,
     the form automatically falls back to opening the customer's email app. */
  formEndpoint: "https://formspree.io/f/mdaqdpao",   // dedicated "Shop" Formspree form (orders only)
  notifyEmail: "info@ccucustom.com"
};

/* --------------------------------------------------------------------------
   PRODUCT CATALOG — single source of truth for the shop.
   Edit names / prices / images here. `personalize:true` shows the
   name/initial + artwork-upload fields on the order page.
   -------------------------------------------------------------------------- */
const PRODUCTS = [
  { id: "whiskey-glasses", name: "Engraved Whiskey Glasses Cigar Holder", price: 42.99, unit: "set of 2",
    img: "assets/img/drinkware-3.webp?v=3", cat: "Drinkware",
    blurb: "A pair of heavy-base rocks glasses with a built-in cigar rest, laser-etched with the name, initial or monogram of your choice.",
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
    personalize: true },

  /* ---- Imported from the Crafty Creations Shopify catalog (made-to-order) ---- */
  { id: "god-fidence", name: "“God Fidence” Hoodie / Sweatshirt", price: 30, from: true, cat: "Apparel",
    img: "assets/img/shop-god-fidence.webp", options: "Hoodie / Sweatshirt · S–2XL · color",
    blurb: "Embroidered “God Fidence” faith design on a cozy hoodie or sweatshirt." },
  { id: "nope-not-today", name: "“NOPE Not Today” Hoodie / Sweatshirt", price: 20, from: true, cat: "Apparel",
    img: "assets/img/shop-nope-not-today.webp", options: "Hoodie / Sweatshirt / T-Shirt · S–2XL · color",
    blurb: "Embroidered “NOPE not today” design — pick your garment and size." },
  { id: "mom-life", name: "Mom Life Appliqué Hoodie / Sweatshirt", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-mom-life.webp", options: "Hoodie / Sweatshirt / Short Sleeve · S–2XL", personalize: true,
    blurb: "Appliqué “Mom Life” embroidery — add up to 4 kids’ names on the sleeve." },
  { id: "pray-on-it-hoodie", name: "“Pray On It, Pray Over It, Pray Through It” Hoodie", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-pray-on-it-hoodie.webp", options: "Hoodie / Sweatshirt · S–2XL · color",
    blurb: "Embroidered prayer design on a warm hoodie or sweatshirt." },
  { id: "pray-on-it-tee", name: "“Pray On It, Pray Over It, Pray Through It” T-Shirt", price: 15, from: true, cat: "Apparel",
    img: "assets/img/shop-pray-on-it-tee.webp", options: "Short / Long Sleeve · S–2XL",
    blurb: "Sublimation-printed prayer tee, made for everyday wear." },
  { id: "pray-pray-pray", name: "“Pray, Pray, Pray” Embroidered Hoodie / Sweatshirt", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-pray-pray-pray.webp", options: "Hoodie / Sweatshirt · S–2XL · color",
    blurb: "Beautifully embroidered “Pray, Pray, Pray” design." },
  { id: "waymaker", name: "“Waymaker, My God” Embroidered Hoodie / Sweatshirt", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-waymaker.webp", options: "Hoodie / Sweatshirt · S–2XL · color",
    blurb: "Professionally embroidered “Waymaker, My God” faith design." },
  { id: "tequila-tumbler", name: "“Save Water, Drink Tequila” 20oz Tumbler", price: 20, from: true, cat: "Drinkware",
    img: "assets/img/shop-tequila-tumbler.webp",
    blurb: "A durable 20oz tumbler wrap for the tequila lover." },
  { id: "drink-straight-tumbler", name: "Funny “Drink Straight” 20oz Tumbler", price: 20, from: true, cat: "Drinkware",
    img: "assets/img/shop-drink-straight-tumbler.webp",
    blurb: "A playful 20oz tumbler design for any beverage lover." },
  { id: "know-your-worth", name: "“Know Your Worth, Then Add Tax” T-Shirt", price: 20, from: true, cat: "Apparel",
    img: "assets/img/shop-know-your-worth.webp", options: "S–2XL",
    blurb: "A bold reminder to know your value — printed on a comfortable tee." },
  { id: "afro-woman", name: "Afro Woman Laser-Cut Wall Art", price: 40, from: true, cat: "Wood Art",
    img: "assets/img/shop-afro-woman.webp", options: "MDF or Original Wood Finish",
    blurb: "Intricately laser-cut wall art — a striking statement piece." },
  { id: "tree-woman", name: "Tree Woman Laser-Cut Wall Art", price: 40, from: true, cat: "Wood Art",
    img: "assets/img/shop-tree-woman.webp", options: "MDF or Original Wood Finish",
    blurb: "Precision laser-cut décor with beautiful, delicate detail." },
  { id: "in-love-couple", name: "In-Love Couple Laser-Cut Wall Art", price: 40, from: true, cat: "Wood Art",
    img: "assets/img/shop-in-love-couple.webp", options: "MDF or Original Wood Finish",
    blurb: "A romantic laser-cut piece — perfect for the home or as a gift." },
  { id: "kitchen-wall-art", name: "Kitchen Laser-Cut Wall Art", price: 60, from: true, cat: "Wood Art",
    img: "assets/img/shop-kitchen-wall-art.webp", options: "Original / Stained Oak / Stained Walnut",
    blurb: "Laser-cut from birch plywood and stained — durable, stylish kitchen décor." },
  { id: "jesus-forgives", name: "“Jesus Forgives” T-Shirt", price: 15, from: true, cat: "Apparel",
    img: "assets/img/shop-jesus-forgives.webp", options: "S–2XL",
    blurb: "A simple, powerful message on a comfortable everyday tee." },
  { id: "his-timing", name: "“His Timing, His Will, His Way” T-Shirt", price: 15, from: true, cat: "Apparel",
    img: "assets/img/shop-his-timing.webp", options: "S–2XL",
    blurb: "A reminder to trust the journey — soft, high-quality tee." },
  { id: "classy-hoodrat", name: "“Classy But Sometimes…” T-Shirt", price: 15, from: true, cat: "Apparel",
    img: "assets/img/shop-classy-hoodrat.webp", options: "S–2XL",
    blurb: "A fun, versatile statement tee with a wink of personality." },
  { id: "trusting-god", name: "“I’m Out Here Just Trusting God” Hoodie / Sweatshirt", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-trusting-god.webp", options: "Hoodie / Sweatshirt · S–2XL · color",
    blurb: "Warm, stylish and expertly embroidered with a message of faith." },
  { id: "nurse-life", name: "“Nurse Life” Embroidered Hoodie / Sweatshirt / Tee", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-nurse-life.webp", options: "Hoodie / Sweatshirt / Tee · S–2XL",
    blurb: "Show your passion for nursing with this embroidered design." },
  { id: "haec-tshirt", name: "H.A.E.C T-Shirt", price: 12.95, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-tshirt.webp", options: "Youth / Adult / PTO · S–2XL",
    blurb: "The High Achievers (H.A.E.C) tee — professional style and comfort." },
  { id: "haec-tote", name: "H.A.E.C Tote Bag", price: 12, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-tote.webp", options: "Natural / Black · PTO or Non-PTO",
    blurb: "A durable, spacious H.A.E.C tote for everyday carry." },
  { id: "haec-mug", name: "H.A.E.C 15oz Coffee Mug", price: 15, from: true, cat: "Drinkware",
    img: "assets/img/shop-haec-mug.webp",
    blurb: "A generous 15oz H.A.E.C mug to elevate your mornings." },
  { id: "haec-beanie", name: "H.A.E.C Embroidered Beanie", price: 15, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-beanie.webp", options: "Brown / Black · PTO or Student/Parent",
    blurb: "Stay warm in a soft, embroidered H.A.E.C beanie." },
  { id: "haec-toddler-tee", name: "H.A.E.C Toddler T-Shirt", price: 12.95, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-toddler-tee.webp", options: "White / Natural · 2T–5T",
    blurb: "The H.A.E.C design sized for the littlest high achievers." },
  { id: "custom-door-mat", name: "Custom Welcome Door Mat", price: 29.95, cat: "Home",
    img: "assets/img/shop-custom-door-mat.webp", personalize: true,
    blurb: "A 24\"×36\" doormat customized with your name, greeting or artwork." },
  { id: "custom-beanie", name: "Design Your Custom Embroidered Beanie", price: 20, from: true, cat: "Custom",
    img: "assets/img/shop-custom-beanie.webp", options: "Color: Red / White / Brown / Blue / Gray", personalize: true,
    blurb: "Your custom text embroidered on a beanie — choose color, font and thread." },
  { id: "custom-trucker-cap", name: "Design Your Custom “Flex Fit” Trucker Cap", price: 20, from: true, cat: "Custom",
    img: "assets/img/shop-custom-trucker-cap.webp", options: "Color: Green / White / Brown / Blue / Gray", personalize: true,
    blurb: "Design a personalized trucker cap that stands out at any event." },
  { id: "stay-humble", name: "“Stay Humble, Hustle Hard” Embroidered Tee / Hoodie", price: 25, from: true, cat: "Apparel",
    img: "assets/img/shop-stay-humble.webp", options: "Tee / Sweatshirt / Hoodie · S–2XL",
    blurb: "A powerful embroidered message to inspire the grind." },
  { id: "haec-adult-hoodie", name: "H.A.E.C Adult Sweatshirts & Hoodies", price: 22, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-adult-hoodie.webp", options: "Sweatshirt / Hoodie / Embroidered · PTO or Non-PTO · S–2XL",
    blurb: "Premium H.A.E.C sweatshirts and hoodies built for comfort." },
  { id: "haec-tumbler", name: "H.A.E.C 20oz Skinny Tumbler", price: 20, from: true, cat: "Drinkware",
    img: "assets/img/shop-haec-tumbler.webp",
    blurb: "A stainless 20oz skinny tumbler that keeps drinks at temperature." },
  { id: "drawstring-bag", name: "Sport Pack Drawstring Bag", price: 15, cat: "Apparel",
    img: "assets/img/shop-drawstring-bag.webp",
    blurb: "A lightweight, durable drawstring bag for athletes on the go." },
  { id: "uv-dtf-gang-sheet", name: "UV-DTF Gang Sheet (Custom Decals)", price: 10, from: true, cat: "Custom",
    img: "assets/img/shop-uv-dtf-gang-sheet.webp", options: "Sheet size: 11×16", personalize: true,
    blurb: "Build a custom UV-DTF adhesive decal gang sheet — upload your artwork." },
  { id: "haec-youth-hoodie", name: "H.A.E.C Youth / Toddler Sweatshirts & Hoodies", price: 16, from: true, cat: "Apparel",
    img: "assets/img/shop-haec-youth-hoodie.webp", options: "Sweatshirt / Hoodie / Embroidered · S–…",
    blurb: "The H.A.E.C line sized for youth and toddlers." },
  { id: "snakes-hiss", name: "“Snakes Don’t Hiss Anymore” T-Shirt", cat: "Apparel",
    img: "assets/img/shop-snakes-hiss.webp",
    blurb: "Bold cobra graphic — “Snakes don’t hiss anymore, they call you babe, bro or friend.”" }
];

/* ==========================================================================
   APPAREL VARIANTS + FLAT PRICING
   Flat price by garment type × age (Youth/Adult). Color, Size and PTO are
   options that do NOT change the price. Values pulled from the Shopify store.
   ========================================================================== */
const PRICE_TABLE = {
  "T-Shirt":               { Youth: 14.95, Adult: 18.95 },
  "Sweatshirt":            { Youth: 16.95, Adult: 22.95 },
  "Hoodie":                { Youth: 18.95, Adult: 24.95 },
  "Embroidered Sweatshirt":{ Youth: 20.95, Adult: 28.95 },
  "Embroidered Hoodie":    { Youth: 22.95, Adult: 32.95 }
};

const SZ_ADULT_XS = ["XS", "S", "M", "L", "XL", "2XL", "3XL"];
const SZ_ADULT    = ["S", "M", "L", "XL", "2XL", "3XL"];
const SZ_TODDLER  = ["2T", "3T", "4T", "5T"];
const SZ_YOUTH    = ["2T", "3T", "4T", "5T", "S", "M", "L", "XL"];

/* Per-product option sets. `garments` = pickable (affects price); `garment` =
   fixed. `ages`/`age` drive Youth vs Adult pricing (default Adult). `flat` =
   single price (tote/beanie/bag). `pto` shows a PTO / Non-PTO selector. */
const VARIANTS = {
  "god-fidence":       { colors: ["Black","Brown","Natural","Blue","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "nope-not-today":    { colors: ["Black","Natural","Blue","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "mom-life":          { colors: ["White","Tan"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "pray-on-it-hoodie": { colors: ["Brown","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "pray-on-it-tee":    { colors: ["Black","White"], sizes: SZ_ADULT_XS, garments: ["Short Sleeve","Long Sleeve"], flat: 19.95 },
  "pray-pray-pray":    { colors: ["Black","Brown","Natural","Blue","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "waymaker":          { colors: ["Black","Brown","Natural","Blue","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"], flat: 28.95 },
  "know-your-worth":   { colors: ["White","Pink","Natural"], sizes: SZ_ADULT_XS, garment: "T-Shirt" },
  "jesus-forgives":    { colors: ["White"], sizes: SZ_ADULT_XS, garment: "T-Shirt" },
  "his-timing":        { colors: ["White","Blue","Black"], sizes: SZ_ADULT_XS, garment: "T-Shirt" },
  "classy-hoodrat":    { colors: ["White"], sizes: SZ_ADULT_XS, garment: "T-Shirt" },
  "trusting-god":      { colors: ["Black","Gray","White","Orange"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt"] },
  "nurse-life":        { colors: ["Black","Gray","White"], sizes: SZ_ADULT_XS, garments: ["Hoodie","Sweatshirt","T-Shirt"] },
  "stay-humble":       { colors: ["White","Black","Blue","Red"], sizes: SZ_ADULT, garments: ["T-Shirt","Sweatshirt","Hoodie"] },
  "haec-tshirt":       { colors: ["White","Natural","Black"], sizes: SZ_ADULT, garment: "T-Shirt", ages: ["Adult","Youth"], pto: true },
  "haec-toddler-tee":  { colors: ["White","Natural","Black"], sizes: SZ_TODDLER, garment: "T-Shirt", age: "Youth" },
  "haec-adult-hoodie": { colors: ["Black","White","Natural"], sizes: SZ_ADULT, garments: ["Sweatshirt","Hoodie","Embroidered Sweatshirt","Embroidered Hoodie"], pto: true },
  "haec-youth-hoodie": { colors: ["Black","White","Natural"], sizes: SZ_YOUTH, garments: ["Sweatshirt","Hoodie","Embroidered Sweatshirt","Embroidered Hoodie"], age: "Youth" },
  "haec-beanie":       { colors: ["Brown","Black"], flat: 12.95, pto: true },
  "haec-tote":         { colors: ["Natural","Black"], flat: 15, pto: true },
  "snakes-hiss":       { colors: ["Black"], sizes: SZ_ADULT, garment: "T-Shirt", flat: 20.95 }
};

function garmentKey(label) {
  const s = String(label).toLowerCase();
  if (s.includes("embroider") && s.includes("hood")) return "Embroidered Hoodie";
  if (s.includes("embroider") && s.includes("sweat")) return "Embroidered Sweatshirt";
  if (s.includes("hood")) return "Hoodie";
  if (s.includes("sweat")) return "Sweatshirt";
  return "T-Shirt"; // tee, short/long sleeve, etc.
}
function variantPrice(v, sel) {
  sel = sel || {};
  if (v.flat != null) return v.flat;
  const gLabel = sel.garment || (v.garments ? v.garments[0] : v.garment) || "T-Shirt";
  const gk = garmentKey(gLabel);
  if (v.prices) return v.prices[gk] != null ? v.prices[gk] : Object.values(v.prices)[0];
  const age = sel.age || v.age || (v.ages ? v.ages[0] : "Adult");
  const row = PRICE_TABLE[gk] || PRICE_TABLE["T-Shirt"];
  return row[age] != null ? row[age] : row.Adult;
}
function variantMinPrice(v) {
  if (v.flat != null) return v.flat;
  if (v.prices) return Math.min.apply(null, Object.values(v.prices));
  const gLabels = v.garments || [v.garment || "T-Shirt"];
  const ages = v.ages || [v.age || "Adult"];
  let min = Infinity;
  gLabels.forEach((gl) => ages.forEach((a) => {
    const p = (PRICE_TABLE[garmentKey(gl)] || {})[a];
    if (p != null) min = Math.min(min, p);
  }));
  return min === Infinity ? 0 : min;
}
/* true when the price varies (garment/age choice, or differing custom prices) → show "from" */
function variantIsFrom(v) {
  if (v.flat != null) return false;
  if (v.prices) return new Set(Object.values(v.prices)).size > 1;
  return !!(v.garments || v.ages);
}

/* Build the Style/Age/Color/Size/PTO <select> fields for an apparel product. */
function variantSelectsHTML(v) {
  const field = (label, name, values, req, first) =>
    `<div class="field"${first ? "" : ' style="margin-top:1.2rem"'}>` +
      `<label for="o-${name.toLowerCase()}">${label}${req ? ' <span class="req">*</span>' : ""}</label>` +
      `<select class="select" id="o-${name.toLowerCase()}" name="${name}"${req ? " required" : ""}>` +
      values.map((x) => `<option>${esc(x)}</option>`).join("") +
      `</select></div>`;
  const out = [];
  if (v.garments) out.push(field("Style", "Garment", v.garments, true, out.length === 0));
  if (v.ages)     out.push(field("Age", "Age", v.ages, true, out.length === 0));
  if (v.colors)   out.push(field("Color", "Color", v.colors, true, out.length === 0));
  if (v.sizes)    out.push(field("Size", "Size", v.sizes, true, out.length === 0));
  if (v.pto)      out.push(field("Membership", "PTO", ["PTO", "Non-PTO"], false, out.length === 0));
  return out.join("");
}

/* ========================================================================== */

const money = (n) => SHOP_CONFIG.currency + Number(n).toFixed(2);
const findProduct = (id) => PRODUCTS.find((p) => p.id === id) || null;
const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/* ---------- SHOP GRID (shop.html) ---------------------------------------- */
function renderShopGrid() {
  const grid = document.getElementById("shopGrid");
  if (!grid) return;
  grid.innerHTML = PRODUCTS.map((p, i) => {
    const v = VARIANTS[p.id];
    const price = v ? variantMinPrice(v) : p.price;
    const showFrom = v ? variantIsFrom(v) : false;   // non-variant items are single-price
    // "Set" item with a Stripe link (no variants/options/personalization) → buy now,
    // straight to Stripe checkout, skipping the order form entirely.
    const stripeUrl = SHOP_CONFIG.stripeLinks[p.id];
    const directBuy = !!stripeUrl && !v && !p.personalize && !p.options;
    const href = directBuy ? stripeUrl : `order.html?item=${encodeURIComponent(p.id)}`;
    const btnLabel = directBuy ? "Buy now" : ((showFrom || v || p.from) ? "Order" : "Customize &amp; Order");
    return `
    <article class="product-card" data-cat="${esc(p.cat)}" data-reveal data-delay="${i % 3}">
      <a class="product-card__media" href="${href}" aria-label="${directBuy ? "Buy" : "Customize"} ${esc(p.name)}">
        <img src="${p.img}" alt="${esc(p.name)}" loading="lazy" decoding="async" />
        <span class="product-card__tag">${esc(p.cat)}</span>
      </a>
      <div class="product-card__body">
        <h3 class="product-card__name">${esc(p.name)}</h3>
        <p class="product-card__blurb">${esc(p.blurb)}</p>
        <div class="product-card__foot">
          <span class="price">${showFrom ? '<small class="price__from">from</small> ' : ''}${money(price)}${p.unit ? `<small>/ ${esc(p.unit)}</small>` : ''}</span>
          <a class="btn btn--gold" href="${href}">${btnLabel}</a>
        </div>
      </div>
    </article>`;
  }).join("");
  renderShopFilters(grid);
}

/* ---------- Category filter pills (injected above the grid) --------------- */
function renderShopFilters(grid) {
  if (document.getElementById("shopFilters")) return;   // don't double-insert
  const ORDER = ["Apparel", "Drinkware", "Wood Art", "Awards", "Kitchen", "Home", "Custom"];
  const cats = [...new Set(PRODUCTS.map((p) => p.cat))]
    .sort((a, b) => ((ORDER.indexOf(a) + 1) || 99) - ((ORDER.indexOf(b) + 1) || 99));
  const bar = document.createElement("div");
  bar.className = "shop-filters";
  bar.id = "shopFilters";
  bar.setAttribute("role", "tablist");
  bar.setAttribute("aria-label", "Filter products by category");
  bar.innerHTML =
    `<button class="filter-btn is-active" data-filter="all">All</button>` +
    cats.map((c) => `<button class="filter-btn" data-filter="${esc(c)}">${esc(c)}</button>`).join("");
  grid.parentNode.insertBefore(bar, grid);

  bar.addEventListener("click", (e) => {
    const btn = e.target.closest(".filter-btn");
    if (!btn) return;
    bar.querySelectorAll(".filter-btn").forEach((b) => b.classList.toggle("is-active", b === btn));
    const f = btn.dataset.filter;
    grid.querySelectorAll(".product-card").forEach((card) => {
      card.style.display = (f === "all" || card.dataset.cat === f) ? "" : "none";
    });
  });
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

  const v = VARIANTS[product.id];
  const initPrice = v ? variantPrice(v, {}) : product.price;
  const hasStripe = !!SHOP_CONFIG.stripeLinks[product.id];
  const payLabel = hasStripe
    ? `Continue to secure payment — ${money(initPrice)}`
    : `Submit order — we'll email your invoice`;

  root.innerHTML = `
    <div class="order-layout">
      <aside class="order-summary" data-reveal>
        <div class="order-summary__media"><img src="${product.img}" alt="${esc(product.name)}" /></div>
        <span class="product-card__tag order-summary__tag">${esc(product.cat)}</span>
        <h1 class="order-summary__name">${esc(product.name)}</h1>
        <p class="order-summary__blurb">${esc(product.blurb)}</p>
        <div class="order-summary__price">${v ? `<span class="js-vprice">${money(initPrice)}</span>` : `${product.from ? '<small style="font-size:.55em;color:var(--text-faint);font-weight:500">from</small> ' : ''}${money(product.price)}${product.unit ? ` <small>/ ${esc(product.unit)}</small>` : ''}`}</div>
        <ul class="order-summary__trust">
          <li>Free design proof before we produce</li>
          <li>Made in-house in Atlanta, GA</li>
          <li>Secure checkout — cards & Apple Pay</li>
        </ul>
      </aside>

      <div class="order-form-wrap" data-reveal data-delay="1">
        <form class="form order-form" id="orderForm" novalidate>
          <input type="hidden" name="_subject" value="🛒 New online order: ${esc(product.name)}" />
          <input type="hidden" name="Product" value="${esc(product.name)}" />
          <input type="hidden" name="Price" value="${money(initPrice)}" />
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true" />

          <h2 class="order-form__step">1 · ${(v || product.options) ? "Your options" : (product.personalize ? "Personalize it" : "Order details")}</h2>
          ${v ? variantSelectsHTML(v) : (product.options ? `
          <div class="field"><label for="o-opts">Size, color &amp; style <span class="req">*</span></label>
            <input class="input" id="o-opts" name="Options" placeholder="${esc(product.options)}" required />
            <span class="hint">Available: ${esc(product.options)}</span></div>
          ` : "")}
          ${product.personalize ? `
          <div class="field"${product.options ? ' style="margin-top:1.2rem"' : ''}><label for="o-perz">Name / text to personalize <span class="req">*</span></label>
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
            <h2 class="order-form__step">3 · Shipping address <span class="muted" style="font-size:.72rem;font-weight:400;letter-spacing:0;text-transform:none">— optional, we'll confirm it on your invoice</span></h2>
            <div class="field"><label for="o-addr1">Street address</label>
              <input class="input" id="o-addr1" name="Address" placeholder="123 Main St" autocomplete="address-line1" /></div>
            <div class="field" style="margin-top:1rem"><label for="o-addr2">Apt / suite</label>
              <input class="input" id="o-addr2" name="Address line 2" placeholder="Apartment, suite, unit" autocomplete="address-line2" /></div>
            <div class="form-row" style="margin-top:1rem">
              <div class="field"><label for="o-city">City</label><input class="input" id="o-city" name="City" autocomplete="address-level2" /></div>
              <div class="field"><label for="o-state">State</label><input class="input" id="o-state" name="State" autocomplete="address-level1" /></div>
            </div>
            <div class="form-row" style="margin-top:1rem">
              <div class="field"><label for="o-zip">ZIP code</label><input class="input" id="o-zip" name="ZIP" inputmode="numeric" autocomplete="postal-code" /></div>
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

  // Live flat-pricing: recompute when the Style (garment) or Age select changes.
  const v = VARIANTS[product.id];
  if (v && v.flat == null) {
    const priceEl = document.querySelector(".order-summary__price .js-vprice");
    const priceInput = form.elements["Price"];
    const gSel = form.elements["Garment"];
    const aSel = form.elements["Age"];
    const updatePrice = () => {
      const p = variantPrice(v, { garment: gSel && gSel.value, age: aSel && aSel.value });
      if (priceEl) priceEl.textContent = money(p);
      if (priceInput) priceInput.value = money(p);
    };
    [gSel, aSel].forEach((s) => s && s.addEventListener("change", updatePrice));
    updatePrice();
  }

  // Show/hide the shipping address based on the Delivery choice. Required must be
  // toggled off when hidden, or the browser blocks submit on an unfocusable field.
  const deliverySel = document.getElementById("o-ship");
  const shipFields = document.getElementById("shipFields");
  const shipReq = shipFields ? shipFields.querySelectorAll("#o-addr1, #o-city, #o-state, #o-zip") : [];
  const syncShipping = () => {
    if (!deliverySel || !shipFields) return;
    const pickup = /pickup/i.test(deliverySel.value);
    shipFields.hidden = pickup;
    shipReq.forEach((el) => { el.disabled = pickup; });  // optional fields; just exclude on pickup
  };
  if (deliverySel) { deliverySel.addEventListener("change", syncShipping); syncShipping(); }

  const showSuccess = () => {
    form.style.display = "none";
    successPanel.hidden = false;
    successPanel.classList.add("is-shown");   // .form-success is display:none until this
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
