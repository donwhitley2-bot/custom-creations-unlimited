/* ==========================================================================
   Custom Creations Unlimited — Hero "The Seal" (Three.js + GSAP)
   - Lazy, capability-gated WebGL. Static poster stays for reduced-motion,
     no-WebGL, or small screens (balanced performance).
   - Does not touch any existing functional code.
   ========================================================================== */
import * as THREE from "three";

const hero = document.querySelector(".hero-x");
const canvas = hero && hero.querySelector(".hero-x__canvas");
const gsap = window.gsap;
const ScrollTrigger = window.ScrollTrigger;
if (gsap && ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- copy entrance (works even without WebGL) ---------------------- */
function animateCopy() {
  if (!gsap || reduce) return;
  const items = hero.querySelectorAll("[data-hx]");
  gsap.set(items, { opacity: 0, y: 26 });
  gsap.to(items, {
    opacity: 1, y: 0, duration: 1, ease: "power3.out",
    stagger: 0.09, delay: 0.15
  });
}

/* ---------- capability gate ---------------------------------------------- */
function webglOK() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
  } catch (e) { return false; }
}
const canRun3D = canvas && webglOK() && !reduce && window.innerWidth >= 768
  && !(navigator.deviceMemory && navigator.deviceMemory <= 2);

animateCopy();

if (!canRun3D) {
  // Poster stays visible; nothing else to do.
} else {
  init3D();
}

function init3D() {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0, 3.6);

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: "high-performance" });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const loader = new THREE.TextureLoader();
  const sealTex = loader.load("assets/img/seal.png", (t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; });

  // Environment (navy studio) → realistic gold reflections
  const pmrem = new THREE.PMREMGenerator(renderer);
  loader.load("assets/img/hero-env.jpg", (env) => {
    env.mapping = THREE.EquirectangularReflectionMapping;
    const rt = pmrem.fromEquirectangular(env);
    scene.environment = rt.texture;
    env.dispose(); pmrem.dispose();
  });

  // Medallion (coin): caps show the seal, edge is brushed gold
  const geo = new THREE.CylinderGeometry(1, 1, 0.12, 96, 1);
  geo.rotateX(Math.PI / 2);
  const capMat = new THREE.MeshStandardMaterial({
    map: sealTex, bumpMap: sealTex, bumpScale: 0.02,
    metalness: 0.9, roughness: 0.33, envMapIntensity: 1.15, color: 0xffffff
  });
  const edgeMat = new THREE.MeshStandardMaterial({ color: 0xc9a24f, metalness: 1, roughness: 0.38, envMapIntensity: 1.0 });
  const medal = new THREE.Mesh(geo, [edgeMat, capMat, capMat]);
  const group = new THREE.Group();
  group.add(medal);
  scene.add(group);

  // Lights (envmap does most; a drifting key light adds life)
  scene.add(new THREE.AmbientLight(0x24304f, 0.6));
  const key = new THREE.DirectionalLight(0xffe8bf, 2.2); key.position.set(2, 2.4, 3); scene.add(key);
  const rim = new THREE.DirectionalLight(0x9fb4ff, 1.1); rim.position.set(-3, -1, 1.5); scene.add(rim);

  // Layout / sizing
  let W = 0, H = 0;
  function layout() {
    const r = hero.getBoundingClientRect();
    W = r.width; H = r.height;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
    // push the seal to the right on wide layouts, centered when stacked
    const wide = window.innerWidth >= 900;
    group.position.x = wide ? 1.05 : 0;
    group.scale.setScalar(wide ? 1 : 0.86);
  }
  layout();
  window.addEventListener("resize", layout);

  // Pointer parallax
  const pointer = { x: 0, y: 0 };
  window.addEventListener("pointermove", (e) => {
    pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.y = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });

  // Scroll choreography: rotate + recede as the hero scrolls away
  const scroll = { spin: 0, y: 0, z: 0 };
  if (gsap && ScrollTrigger) {
    gsap.to(scroll, {
      spin: Math.PI * 1.1, y: 0.35, z: -0.8,
      ease: "none",
      scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: 1 }
    });
  }

  // Render loop, paused when hero is offscreen
  let visible = true, raf = 0;
  new IntersectionObserver((ents) => {
    visible = ents[0].isIntersecting;
    if (visible && !raf) loop();
  }, { threshold: 0 }).observe(hero);

  const clock = new THREE.Clock();
  let ry = 0, rx = 0;
  function loop() {
    raf = requestAnimationFrame(loop);
    if (!visible) { cancelAnimationFrame(raf); raf = 0; return; }
    const t = clock.getElapsedTime();
    // base slow spin + pointer tilt + scroll spin
    ry += (pointer.x * 0.5 - ry) * 0.04;
    rx += (-pointer.y * 0.32 - rx) * 0.04;
    group.rotation.y = t * 0.28 + scroll.spin + ry;
    group.rotation.x = rx + Math.sin(t * 0.6) * 0.03;
    group.position.y = Math.sin(t * 0.8) * 0.05 + scroll.y;
    group.position.z = scroll.z;
    // subtle light drift
    key.position.x = Math.cos(t * 0.4) * 2.4;
    key.position.y = 1.8 + Math.sin(t * 0.5) * 0.8;
    renderer.render(scene, camera);
  }

  // reveal
  requestAnimationFrame(() => { hero.classList.add("is-webgl"); loop(); });
}
