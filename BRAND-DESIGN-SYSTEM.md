# Custom Creations Unlimited — Brand & Design System

> **Custom Creations Unlimited** — *Make Your Mark.*
> A premium custom-branding house: embroidery, custom apparel, promotional products,
> corporate awards, laser engraving and personalized gifts — all under one roof.

This document is the single source of truth for the brand. Every page should be built
against these tokens so the site stays consistent as it grows.

---

## 1. Brand strategy

| | |
|---|---|
| **Name** | Custom Creations Unlimited — a clear, descriptive name: the *total* set of branding solutions a business needs, under one roof. |
| **Tagline** | **Make Your Mark.** |
| **Positioning** | The one trusted partner for everything a brand puts its name on. |
| **Promise** | Premium craftsmanship, in-house, on time — with real human service. |
| **Personality** | Professional · Premium · Creative · Trusted · Modern · Easy to work with. |
| **Voice** | Confident, warm, precise. Short sentences. Benefit-first. Never gimmicky. |
| **Logo mark** | "CCU" monogram in a rounded obsidian square with a gold letterform. |

**Why it works:** the name says exactly what we do — one partner for *every* branded
product, from a single embroidered cap to a company-wide rollout. Plain-spoken and easy to
trust. The tagline *Make Your Mark.* ties it back to the craft: embroidery *stitches* a
mark, engraving *etches* one, awards *honor* one.

---

## 2. Color palette

The palette is **Obsidian ink + Champagne gold + Ivory** — a restrained luxury system.
Gold is an *accent*, never a flood. All values are defined as CSS custom properties in
`assets/css/styles.css` (`:root`) with a full dark-theme override (`[data-theme="dark"]`).

### Core
| Token | Hex | Use |
|---|---|---|
| `--ink-900` | `#0a0a0f` | Primary dark / footer / dark hero |
| `--ink-800` | `#101019` | Dark surfaces |
| `--ivory-50` | `#fbfaf6` | Light page background |
| `--ivory-100` | `#f7f4ee` | Soft sections |
| `--gold-500` | `#c8a24a` | **Primary accent** (light theme) |
| `--gold-400` | `#d4b066` | Primary accent (dark theme) |
| `--gold-300` | `#e3c988` | Light gold / gradients |
| `--rose` | `#e0a87e` | Warm gradient partner |

### Semantic (auto-swaps by theme)
`--bg`, `--bg-soft`, `--bg-elevated`, `--text`, `--text-muted`, `--line`, `--accent`,
`--on-accent`. **Always style with the semantic tokens**, not raw hex — that's what makes
dark mode work for free.

### Signature gradient
```
--grad-gold: linear-gradient(120deg, #e3c988, #c8a24a 45%, #e0a87e);
```
Used on primary CTAs, the logo accent, stat numbers, and icon chips.

### Contrast
Body text on background meets **WCAG 2.2 AA**. Gold is used for large text, borders and
fills — not for small body copy on light backgrounds (it wouldn't pass), which is why
links use `--accent-strong` (`--gold-700`) in light mode.

---

## 3. Typography

Two families, loaded from Google Fonts in `index.html`.

| Role | Font | Notes |
|---|---|---|
| **Display / headings** | **Fraunces** (serif, optical) | Luxury editorial feel; weights 400–700, italic for emphasis. |
| **Body / UI** | **Inter** (sans) | Highly legible at all sizes; weights 400–700. |

### Type scale (fluid, `clamp()`)
| Token | Range |
|---|---|
| `--fs-h1` | 2.75 → 5.75 rem |
| `--fs-h2` | 2 → 3.5 rem |
| `--fs-h3` | 1.4 → 1.9 rem |
| `--fs-lead` | 1.25 rem |
| `--fs-body` | 1.06 rem |

Headings: `letter-spacing: -0.015em`, `line-height: 1.04`. Body `line-height: 1.65`.
Eyebrows: Inter, uppercase, `letter-spacing: .18em`, gold.

---

## 4. Shape, elevation & motion

- **Radii:** `--radius-sm 12px` · `--radius 18px` · `--radius-lg 28px` · `--radius-xl 36px` · `--pill 999px`.
- **Shadows:** soft, layered (`--shadow-xs … --shadow-lg`, plus a gold glow `--shadow-gold`). Never hard/black.
- **Glassmorphism:** sticky header, hero badge and gallery tags use `backdrop-filter: blur()` over `--surface-glass`.
- **Easing:** `--ease`, `--ease-out` (cubic-bezier). Default duration `--dur .5s`.
- **Motion respects `prefers-reduced-motion`** — all transitions/animations collapse to instant.

---

## 5. Component library (in `styles.css`)

| Component | Class | Notes |
|---|---|---|
| Buttons | `.btn` + `.btn--gold / --primary / --ghost / --light / --lg / --block` | Pill, lift-on-hover. |
| Arrow link | `.link-arrow` | Animated arrow. |
| Header / nav | `.site-header`, `.nav-link`, `.mega` | Glass on scroll, hover mega-menu. |
| Mobile nav | `.mobile-nav` | Slide-in panel w/ sub-accordions. |
| Hero | `.hero`, `.hero-card`, `.hero-badge` | Layered collage + floating glass badge. |
| Marquee | `.marquee` | Infinite client logo strip, pauses on hover. |
| Service card | `.service-card` | Media + icon + CTA. |
| Feature card | `.feature` | Icon + copy (Why Us). |
| Stats | `.stats`, `.stat__num[data-count]` | Animated counters on scroll. |
| Process | `.process-step` | Numbered, connected steps. |
| Gallery | `.gallery-grid`, `.gallery-item`, `.filter-btn` | Filterable masonry-style grid. |
| Industries | `.industry-chip` | Icon chips. |
| Testimonials | `.testi-card` | Quote + avatar. |
| FAQ | `.faq-item`, `.faq-q`, `.faq-a` | Accessible accordion. |
| CTA banner | `.cta-banner` | Dark gradient conversion block. |
| Contact / map | `.contact-strip`, `.map-wrap` | Info rows + embedded Google Map. |
| Footer | `.site-footer` | 4-col + newsletter + social. |
| Floating actions | `.floating .fab`, `.back-to-top` | Sticky call + quote, pulse ring. |
| Promo bar | `.promo-bar` | Urgency banner. |
| Placeholder media | `.ph[data-label]` | Elegant gradient stand-in until real photos are dropped in. |
| Reveal | `[data-reveal]` `[data-delay]` | Scroll-in animation via IntersectionObserver. |

---

## 6. Imagery direction

Replace the `.ph` placeholders with **professional, well-lit photography**:
- Real products on clean or richly textured backgrounds (close-up stitching, engraving sparks, crystal awards catching light).
- Warm, editorial color grade that complements gold + ivory.
- Consistent aspect ratios (cards 16:11, hero collage square/4:5).
- Always set descriptive `alt` text (the placeholders already carry labels to guide this).

Recommended pipeline: store originals, export **WebP/AVIF** at 1×/2×, lazy-load
(`loading="lazy"`) everything below the fold. See README for the Cloudinary note.

---

## 7. Accessibility (WCAG 2.2)

- Semantic landmarks (`header`/`main`/`footer`/`nav`), one `<h1>`, ordered headings.
- Skip-link, visible `:focus-visible` rings, `aria-expanded` on every toggle.
- Color-independent meaning; AA contrast on text.
- Reduced-motion honored; all interactive elements keyboard-operable.
- Map iframe + decorative SVGs labeled/`aria-hidden` appropriately.

---

## 8. Using the system on new pages

1. Link the same `styles.css` + `main.js`.
2. Reuse the header/footer markup verbatim (keeps nav consistent).
3. Compose pages from existing components; avoid one-off CSS.
4. New colors → add a token, never a raw hex in markup.
5. Wrap new sections in `<section class="section">` + `.container` and add `data-reveal`.
