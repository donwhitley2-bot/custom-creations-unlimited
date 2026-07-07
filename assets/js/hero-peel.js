/* ==========================================================================
   "The Peel" — scroll-driven DTF transfer hero (vanilla Three.js, no build)
   --------------------------------------------------------------------------
   Progressive enhancement: the markup ships a static photo fallback.
   This script upgrades it to an interactive WebGL peel ONLY when:
     • the hero is near the viewport (IntersectionObserver lazy-load)
     • WebGL is available
     • the user hasn't asked for reduced motion
     • not a save-data connection, not a small/mobile viewport
   Otherwise it does nothing and the fallback photo simply stays.
   ========================================================================== */
(function () {
  "use strict";

  var peelBox = document.querySelector(".hero-peel");
  var stage = peelBox && peelBox.querySelector(".hero-peel__stage");
  var hero = document.querySelector(".hero--x");
  if (!peelBox || !stage || !hero) return;

  /* ---------- capability gates (fallback image stays if any fail) -------- */
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var conn = navigator.connection || {};
  if (conn.saveData) return;
  if (window.innerWidth < 820) return;
  try {
    var probe = document.createElement("canvas");
    if (!probe.getContext("webgl2") && !probe.getContext("webgl")) return;
  } catch (e) { return; }

  /* ---------- lazy-load three.min.js only when hero approaches ----------- */
  var loaded = false;
  var io = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting && !loaded) {
      loaded = true; io.disconnect();
      if (window.THREE) { init(); return; }
      var s = document.createElement("script");
      s.src = "assets/vendor/three.min.js";
      s.onload = init;               /* on error: fallback photo remains */
      document.head.appendChild(s);
    }
  }, { rootMargin: "240px" });
  io.observe(peelBox);

  /* ---------- scene ------------------------------------------------------ */
  function init() {
    var THREE = window.THREE;
    var W = 1.9, H = 1.06;                       /* garment plane, 16:9-ish */
    var RADIUS = 0.16;                           /* curl cylinder radius    */

    var renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    stage.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 10);
    camera.position.set(0, -0.03, 3.2);

    var group = new THREE.Group();
    group.rotation.x = -0.16;                    /* editorial top-down tilt */
    group.rotation.z = -0.05;
    scene.add(group);

    var loader = new THREE.TextureLoader();
    var tFabric = loader.load("assets/img/hero-fabric.webp");
    var tPrint = loader.load("assets/img/hero-print.webp");
    tFabric.wrapS = tFabric.wrapT = THREE.RepeatWrapping;

    var uniforms = {
      uFront: { value: 0.0 },                    /* peel line, 0=covered 1=done */
      tFabric: { value: tFabric },
      tPrint: { value: tPrint }
    };

    /* Garment: fabric with the gold print revealed behind the peel line */
    var garment = new THREE.Mesh(
      new THREE.PlaneGeometry(W, H),
      new THREE.ShaderMaterial({
        uniforms: uniforms,
        vertexShader:
          "varying vec2 vUv;\n" +
          "void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
        fragmentShader:
          "uniform sampler2D tFabric, tPrint; uniform float uFront; varying vec2 vUv;\n" +
          "void main(){\n" +
          "  vec3 fab = texture2D(tFabric, vUv * vec2(1.8, 1.0)).rgb * 1.06;\n" +
          "  float dTop = 1.0 - vUv.y;\n" +                                   /* 0 at top, 1 at bottom */
          "  float front = uFront * 1.79 - (vUv.x - 0.5) * 0.105;\n" +        /* matches film curl line */
          "  float revealed = 1.0 - smoothstep(front - 0.08, front, dTop);\n" +
          "  vec3 print = texture2D(tPrint, vUv).rgb;\n" +
          "  vec3 col = fab + print * revealed * 1.25;\n" +                   /* screen-ish: print bg is black */
          "  float band = exp(-pow((dTop - front) * 9.0, 2.0));\n" +          /* fresh-press glint at the edge */
          "  col += print * revealed * band * 0.4;\n" +
          "  gl_FragColor = vec4(col, 1.0);\n" +
          "}"
      })
    );
    group.add(garment);

    /* Film: high-segment plane curling around a moving cylinder */
    var film = new THREE.Mesh(
      new THREE.PlaneGeometry(W * 1.005, H * 1.02, 4, 140),
      new THREE.ShaderMaterial({
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide,
        uniforms: uniforms,
        vertexShader:
          "uniform float uFront; varying vec2 vUv; varying float vTheta;\n" +
          "const float R = " + RADIUS.toFixed(3) + ";\n" +
          "void main(){\n" +
          "  vUv = uv; vTheta = 0.0;\n" +
          "  vec3 p = position;\n" +
          "  float H2 = " + (H * 1.02 / 2).toFixed(4) + ";\n" +
          "  float yLine = H2 - uFront * (2.0 * H2 + 3.14159 * R + 0.35);\n" + /* travels top→past bottom */
          "  yLine += p.x * 0.06;\n" +                                          /* slight diagonal */
          "  float d = p.y - yLine;\n" +
          "  if (d > 0.0) {\n" +
          "    float theta = d / R;\n" +
          "    if (theta < 3.14159) { p.y = yLine + sin(theta) * R; p.z = (1.0 - cos(theta)) * R; vTheta = theta; }\n" +
          "    else { p.y = yLine - (d - 3.14159 * R); p.z = 2.0 * R; vTheta = 3.14159; }\n" +
          "  }\n" +
          "  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);\n" +
          "}",
        fragmentShader:
          "uniform sampler2D tPrint; uniform float uFront; varying vec2 vUv; varying float vTheta;\n" +
          "void main(){\n" +
          "  vec3 film = vec3(0.93, 0.90, 0.84);\n" +
          "  float deposited = step(0.001, vTheta);\n" +                 /* past the curl = ink left behind */
          "  vec3 ink = texture2D(tPrint, vUv).rgb * (1.0 - deposited) * 0.5;\n" +
          "  float glint = pow(max(sin(vTheta), 0.0), 6.0);\n" +          /* gold light along the curl */
          "  vec3 col = film * 0.32 + ink + vec3(0.83, 0.66, 0.38) * glint * 0.85;\n" +
          "  float alpha = 0.34 + glint * 0.5;\n" +
          "  gl_FragColor = vec4(col, alpha);\n" +
          "}"
      })
    );
    film.position.z = 0.012;
    group.add(film);

    peelBox.classList.add("is-webgl");

    /* ---------- drive: scroll scrubs the peel, pointer adds tilt --------- */
    var target = 0, current = 0, tiltX = 0, tiltY = 0, tTiltX = 0, tTiltY = 0;
    var playing = true, t0 = performance.now();

    function readScroll() {
      var r = hero.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      /* 0 when hero fully in view at top, 1 as it scrolls out */
      var p = (0 - r.top + vh * 0.12) / (r.height * 0.85);
      target = Math.max(0, Math.min(1, p));
    }
    window.addEventListener("scroll", readScroll, { passive: true });
    readScroll();

    peelBox.addEventListener("pointermove", function (e) {
      var b = peelBox.getBoundingClientRect();
      tTiltY = ((e.clientX - b.left) / b.width - 0.5) * 0.12;
      tTiltX = ((e.clientY - b.top) / b.height - 0.5) * -0.08;
    });
    peelBox.addEventListener("pointerleave", function () { tTiltX = tTiltY = 0; });

    function size() {
      var w = stage.clientWidth || 1, h = stage.clientHeight || 1;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    size();
    window.addEventListener("resize", size);

    /* pause rendering when tab hidden or hero far off-screen */
    var visIO = new IntersectionObserver(function (en) { playing = en[0].isIntersecting; }, {});
    visIO.observe(peelBox);
    document.addEventListener("visibilitychange", function () { playing = !document.hidden; });

    (function loop(now) {
      requestAnimationFrame(loop);
      if (!playing) return;
      var t = (now - t0) / 1000;
      var idle = 0.10 + Math.sin(t * 0.45) * 0.025;          /* gentle breathing before scroll */
      var goal = Math.max(idle, target);
      current += (goal - current) * 0.075;
      uniforms.uFront.value = current;
      tiltX += (tTiltX - tiltX) * 0.06;
      tiltY += (tTiltY - tiltY) * 0.06;
      group.rotation.x = -0.16 + tiltX;
      group.rotation.y = tiltY;
      renderer.render(scene, camera);
    })(t0);
  }
})();
