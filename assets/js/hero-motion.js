/* ==========================================================================
   Hero motion pack (JS half) — animates the EXISTING hero, homepage only.
   1. Main card slowly crossfades through existing product photos
   2. Pointer parallax: the photo cluster tilts subtly toward the cursor
   No layout changes, no new assets; respects prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";

  var visual = document.querySelector(".hero__visual");
  var mainCard = document.querySelector(".hero-card--main");
  if (!visual || !mainCard) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  /* --- 1 · Showcase rotation (all photos already on the site/cached) ------ */
  var PHOTOS = [
    "assets/img/embroidery-1.webp",      /* current photo — stays first     */
    "assets/img/prod-tshirts.webp",
    "assets/img/prod-cuttingboards.webp",
    "assets/img/prod-laser-tumblers.webp"
  ];
  var HOLD_MS = 5200;

  var base = mainCard.querySelector("img");
  if (base) {
    var layers = PHOTOS.map(function (src, i) {
      if (i === 0) return base;                       /* reuse the existing img */
      var im = document.createElement("img");
      im.src = src; im.alt = ""; im.loading = "lazy"; im.decoding = "async";
      im.className = "hero-swap";
      mainCard.appendChild(im);
      return im;
    });
    var cur = 0;
    setInterval(function () {
      if (document.hidden) return;                    /* don't cycle unseen    */
      var next = (cur + 1) % layers.length;
      /* overlays fade in over the base; cycling back to 0 fades them all out */
      layers.forEach(function (el, i) {
        if (el !== base) el.classList.toggle("is-on", i === next);
      });
      cur = next;
    }, HOLD_MS);
  }

  /* --- 2 · Pointer parallax on the cluster -------------------------------- */
  var hero = document.querySelector(".hero");
  if (!hero || !window.requestAnimationFrame) return;
  var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;

  function tick() {
    cx += (tx - cx) * 0.12;
    cy += (ty - cy) * 0.12;
    visual.style.transform =
      "perspective(900px) rotateY(" + cx.toFixed(3) + "deg) rotateX(" + cy.toFixed(3) + "deg)";
    if (Math.abs(tx - cx) + Math.abs(ty - cy) > 0.01) raf = requestAnimationFrame(tick);
    else raf = null;
  }
  hero.addEventListener("pointermove", function (e) {
    var b = visual.getBoundingClientRect();
    var mx = (e.clientX - (b.left + b.width / 2)) / b.width;    /* -0.5 .. 0.5 */
    var my = (e.clientY - (b.top + b.height / 2)) / b.height;
    tx = mx * 4.5;                                              /* max ~2.2°   */
    ty = my * -3.5;
    if (!raf) raf = requestAnimationFrame(tick);
  });
  hero.addEventListener("pointerleave", function () {
    tx = ty = 0;
    if (!raf) raf = requestAnimationFrame(tick);
  });
})();
