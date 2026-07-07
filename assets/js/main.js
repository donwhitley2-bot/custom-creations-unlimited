/* =========================================================================
   MARQUE — homepage interactions
   Vanilla JS, no dependencies. Progressive enhancement, a11y-aware.
   ========================================================================= */
(function () {
  "use strict";
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Theme (light/dark) with persistence + system default ------- */
  var root = document.documentElement;
  var stored = localStorage.getItem("marque-theme");
  if (stored) {
    root.setAttribute("data-theme", stored);
  } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.setAttribute("data-theme", "dark");
  }
  var themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("marque-theme", next);
    });
  }

  /* ---------- Sticky header shadow ---------------------------------------- */
  var header = document.getElementById("header");
  var backToTop = document.getElementById("backToTop");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 20);
    if (backToTop) backToTop.classList.toggle("is-visible", y > 700);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReduced ? "auto" : "smooth" });
    });
  }

  /* ---------- Mobile navigation ------------------------------------------- */
  var navToggle = document.getElementById("navToggle");
  var mobileNav = document.getElementById("mobileNav");
  function closeMobile() {
    if (!mobileNav) return;
    mobileNav.classList.remove("is-open");
    mobileNav.setAttribute("aria-hidden", "true");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }
  if (navToggle && mobileNav) {
    navToggle.addEventListener("click", function () {
      var open = mobileNav.classList.toggle("is-open");
      mobileNav.setAttribute("aria-hidden", String(!open));
      navToggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    });
    mobileNav.querySelectorAll("a[href^='#']").forEach(function (a) {
      a.addEventListener("click", closeMobile);
    });
    // Sub-menu accordions
    mobileNav.querySelectorAll("[data-sub]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var panel = document.getElementById(btn.getAttribute("data-sub"));
        var open = panel.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", String(open));
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMobile();
    });
  }

  /* ---------- Scroll reveal (IntersectionObserver) ------------------------ */
  var revealEls = document.querySelectorAll("[data-reveal]");
  if (prefersReduced || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Animated counters ------------------------------------------- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    var dur = 1600, start = null;
    var isM = suffix.indexOf("M") !== -1;
    function fmt(v) {
      if (isM) return (v).toFixed(v < 10 ? 1 : 0);
      return Math.round(v).toLocaleString();
    }
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      el.textContent = fmt(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = fmt(target) + suffix;
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    if (prefersReduced || !("IntersectionObserver" in window)) {
      counters.forEach(function (el) {
        el.textContent = el.getAttribute("data-count") + (el.getAttribute("data-suffix") || "");
      });
    } else {
      var co = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { animateCount(entry.target); co.unobserve(entry.target); }
        });
      }, { threshold: 0.6 });
      counters.forEach(function (el) { co.observe(el); });
    }
  }

  /* ---------- Gallery filter ---------------------------------------------- */
  var filterBtns = document.querySelectorAll(".filter-btn");
  var galleryItems = document.querySelectorAll(".gallery-item, .post-card[data-cat]");
  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var filter = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
      galleryItems.forEach(function (item) {
        var show = filter === "all" || item.getAttribute("data-cat") === filter;
        item.classList.toggle("is-hidden", !show);
      });
    });
  });

  /* ---------- FAQ accordion ----------------------------------------------- */
  document.querySelectorAll(".faq-q").forEach(function (q) {
    q.addEventListener("click", function () {
      var item = q.closest(".faq-item");
      var answer = item.querySelector(".faq-a");
      var isOpen = item.classList.toggle("is-open");
      q.setAttribute("aria-expanded", String(isOpen));
      answer.style.maxHeight = isOpen ? answer.scrollHeight + "px" : null;
    });
  });

  /* ---------- Newsletter (front-end demo) --------------------------------- */
  var news = document.getElementById("newsletter");
  if (news) {
    news.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = news.querySelector("input[type=email]");
      var msg = document.getElementById("news-msg");
      if (input.checkValidity()) {
        news.reset();
        if (msg) msg.hidden = false;
      } else {
        input.reportValidity();
      }
    });
  }

  /* ---------- Lightbox (gallery pages) ------------------------------------ */
  var lightbox = document.getElementById("lightbox");
  if (lightbox) {
    var lbFrame = lightbox.querySelector(".lightbox__frame");
    var lbCat = lightbox.querySelector(".js-lb-cat");
    var lbTitle = lightbox.querySelector(".js-lb-title");
    var items = Array.prototype.slice.call(document.querySelectorAll(".gallery-item"));
    var current = 0;

    function lbRender(i) {
      var item = items[i];
      if (!item) return;
      var cat = item.getAttribute("data-cat-label") || "";
      var title = item.getAttribute("data-title") || "";
      var img = item.querySelector("img");
      if (img) {
        lbFrame.innerHTML = '<img class="ph-img" src="' + img.getAttribute("src") + '" alt="' + title + '">';
      } else {
        var ph = item.querySelector(".ph");
        var label = ph ? ph.getAttribute("data-label") : title;
        lbFrame.innerHTML = '<div class="ph" data-label="' + (label || title) + '"></div>';
      }
      if (lbCat) lbCat.textContent = cat;
      if (lbTitle) lbTitle.textContent = title;
      current = i;
    }
    function lbOpen(i) {
      lbRender(i);
      lightbox.classList.add("is-open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }
    function lbClose() {
      lightbox.classList.remove("is-open");
      lightbox.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
    function lbStep(d) {
      var visible = items.filter(function (it) { return !it.classList.contains("is-hidden"); });
      var pos = visible.indexOf(items[current]);
      var next = visible[(pos + d + visible.length) % visible.length];
      lbRender(items.indexOf(next));
    }
    items.forEach(function (item, i) {
      item.style.cursor = "zoom-in";
      item.setAttribute("tabindex", "0");
      item.setAttribute("role", "button");
      item.addEventListener("click", function () { lbOpen(i); });
      item.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); lbOpen(i); }
      });
    });
    lightbox.querySelectorAll("[data-lb-close]").forEach(function (b) { b.addEventListener("click", lbClose); });
    var prev = lightbox.querySelector(".lightbox__nav--prev");
    var next = lightbox.querySelector(".lightbox__nav--next");
    if (prev) prev.addEventListener("click", function () { lbStep(-1); });
    if (next) next.addEventListener("click", function () { lbStep(1); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lbClose(); });
    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("is-open")) return;
      if (e.key === "Escape") lbClose();
      if (e.key === "ArrowLeft") lbStep(-1);
      if (e.key === "ArrowRight") lbStep(1);
    });
  }

  /* ---------- File upload (drag/drop + filename) -------------------------- */
  document.querySelectorAll(".upload").forEach(function (zone) {
    var input = zone.querySelector("input[type=file]");
    var nameEl = zone.querySelector(".upload__name");
    if (!input) return;
    function showName() {
      if (input.files && input.files.length) {
        nameEl.textContent = input.files.length > 1
          ? input.files.length + " files selected"
          : input.files[0].name;
        nameEl.hidden = false;
      }
    }
    input.addEventListener("change", showName);
    ["dragover", "dragenter"].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add("is-drag"); });
    });
    ["dragleave", "drop"].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove("is-drag"); });
    });
    zone.addEventListener("drop", function (e) {
      if (e.dataTransfer && e.dataTransfer.files.length) { input.files = e.dataTransfer.files; showName(); }
    });
  });

  /* ---------- Quote / contact forms (Formspree w/ mailto fallback) -------- */
  // Wire a form to Formspree by setting its action to your endpoint, e.g.
  //   <form action="https://formspree.io/f/abcd1234" method="POST" ...>
  // Until then (or if the request fails) it falls back to composing an email.
  document.querySelectorAll("[data-mailto-form]").forEach(function (form) {
    function showSuccess() {
      // The success panel is usually a sibling of the form's card, not a child,
      // so search the nearest section (then the document) — not just the parent.
      var scope = form.closest("section") || document;
      var success = form.parentNode.querySelector(".form-success")
        || scope.querySelector(".form-success")
        || document.querySelector(".form-success");
      if (success) {
        form.style.display = "none";
        success.classList.add("is-shown");
        success.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "center" });
      }
      try { form.reset(); } catch (e) {}
    }
    function composeMailto() {
      var to = form.getAttribute("data-mailto") || "hello@marquebranding.com";
      var subject = form.getAttribute("data-subject") || "Website inquiry";
      var lines = [];
      form.querySelectorAll("input, select, textarea").forEach(function (el) {
        if (["file", "submit", "button", "hidden"].indexOf(el.type) !== -1) return;
        var label = (el.getAttribute("data-label") || el.name || "").trim();
        if (el.type === "checkbox" || el.type === "radio") {
          if (el.checked && !el.getAttribute("data-group") && label) lines.push(label + ": " + (el.value || "Yes"));
        } else if (el.value && label) {
          lines.push(label + ": " + el.value);
        }
      });
      var groups = {};
      form.querySelectorAll("input[type=checkbox]:checked, input[type=radio]:checked").forEach(function (el) {
        var g = el.getAttribute("data-group");
        if (g) { (groups[g] = groups[g] || []).push(el.value); }
      });
      Object.keys(groups).forEach(function (g) { lines.push(g + ": " + groups[g].join(", ")); });
      var body = encodeURIComponent("New request from the MARQUE website:\n\n" + lines.join("\n") +
        "\n\n(Note: please attach your logo file when sending.)");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + body;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var action = form.getAttribute("action") || "";
      var formspreeReady = /formspree\.io\/f\/(?!your-form-id\b)[A-Za-z0-9]+/.test(action);
      if (formspreeReady && window.fetch) {
        var btn = form.querySelector("[type=submit]");
        if (btn) { btn.disabled = true; btn.style.opacity = ".7"; }
        fetch(action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
          .then(function (r) { if (r.ok) showSuccess(); else composeMailto(); })
          .catch(composeMailto)
          .then(function () { if (btn) { btn.disabled = false; btn.style.opacity = ""; } });
      } else {
        composeMailto();
        showSuccess();
      }
    });
  });

  /* ---------- Tools menu password gate ------------------------------------ */
  (function () {
    var KEY = "ccuToolsAuth", PW = "JustLaserIt";
    function authed() { try { return sessionStorage.getItem(KEY) === "1"; } catch (e) { return false; } }
    document.querySelectorAll(".js-tools-link").forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (authed()) return;
        e.preventDefault();
        var pw = window.prompt("This area is password protected.\nEnter the Tools password:");
        if (pw === null) return;
        if (pw === PW) {
          try { sessionStorage.setItem(KEY, "1"); } catch (_) {}
          window.location.href = a.getAttribute("href");
        } else { window.alert("Incorrect password."); }
      });
    });
  })();

  /* ---------- Footer year -------------------------------------------------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
