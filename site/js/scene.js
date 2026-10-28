/* Shared Three.js scene: the Knowledge Club emblem, a camera that flies one stop per [data-stage] section,
   pentagon shards along the path and an emblem portal at the end of every page. */
(() => {
  if (typeof THREE === 'undefined') return;

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = matchMedia('(pointer: coarse)').matches;
  const heroMode = document.body.dataset.emblem || 'hero';
  const stages = [...document.querySelectorAll('main > [data-stage]')];
  const N = Math.max(2, stages.length);

  const canvas = document.getElementById('scene');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(0x060818, 1);
  renderer.outputEncoding = THREE.sRGBEncoding;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060818, 0.02);
  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 400);

  scene.add(new THREE.HemisphereLight(0x9fb3ff, 0x1a0b2e, 0.6));
  const blueLight = new THREE.PointLight(0x3161f1, 3.2, 70);
  const pinkLight = new THREE.PointLight(0xff007a, 2.6, 70);
  const keyLight = new THREE.DirectionalLight(0xffffff, 0.9);
  keyLight.position.set(4, 6, 10);
  scene.add(blueLight, pinkLight, keyLight);

  /* ---------- Emblem geometry: circle + nested pentagons, each rotated 36° and inscribed in the last ---------- */
  const PENTA_K = Math.cos(Math.PI / 5);
  const pentagon = (r, rot, hole) => {
    const pts = [];
    for (let i = 0; i < 5; i++) {
      const a = Math.PI / 2 + rot + i * (Math.PI * 2 / 5);
      pts.push(new THREE.Vector2(Math.cos(a) * r, Math.sin(a) * r));
    }
    return hole ? pts.reverse() : pts;
  };
  const emblemShapes = R => {
    const shrink = 0.975;
    const outer = new THREE.Shape();
    outer.absarc(0, 0, R, 0, Math.PI * 2, false);
    outer.holes.push(new THREE.Path(pentagon(R * shrink, 0, true)));
    const shapes = [outer];
    let r = R * PENTA_K;
    for (let k = 0; k < 2; k++) {
      const s = new THREE.Shape(pentagon(r, Math.PI / 5));
      s.holes.push(new THREE.Path(pentagon(r * PENTA_K * shrink, 2 * Math.PI / 5, true)));
      shapes.push(s);
      r *= PENTA_K * PENTA_K;
    }
    return shapes;
  };
  const extrude = (shape, depth, R) => {
    const g = new THREE.ExtrudeGeometry(shape, {
      depth, bevelEnabled: true, bevelThickness: depth * 0.2, bevelSize: R * 0.01, bevelSegments: 2, curveSegments: 96,
    });
    g.center();
    return g;
  };

  /* The logo keeps its own colour: unlit pure white faces, light grey sides for depth. */
  const LOGO_WHITE = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const LOGO_SIDE = new THREE.MeshBasicMaterial({ color: 0xcfd3dd });

  const emblem = new THREE.Group();
  const layers = emblemShapes(5).map(s => {
    const m = new THREE.Mesh(extrude(s, 0.6, 5), [LOGO_WHITE, LOGO_SIDE]);
    emblem.add(m);
    return m;
  });
  if (heroMode !== 'none') scene.add(emblem);

  /* ---------- Camera path: one control point per stage ---------- */
  const pts = [];
  for (let i = 0; i < N; i++) {
    const side = i === 0 ? 0 : (i % 2 ? -1 : 1);
    pts.push(new THREE.Vector3(side * (4 + (i % 3)), (i % 2 ? 2.5 : -1.5) * (i ? 1 : 0), 18 - i * 34));
  }
  pts.push(pts[N - 1].clone().add(new THREE.Vector3(0, 0, -26)));
  const path = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.4);
  const SEG = pts.length - 1;
  const stageToT = s => Math.min(1, s / SEG);

  /* ---------- Pentagon shards ---------- */
  const SHARDS = Math.min(isTouch ? 140 : 300, 60 + N * 40);
  const shardShape = new THREE.Shape(pentagon(1, 0));
  shardShape.holes.push(new THREE.Path(pentagon(0.62, Math.PI / 5, true)));
  const shardGeo = new THREE.ExtrudeGeometry(shardShape, { depth: 0.18, bevelEnabled: false });
  shardGeo.center();
  const shards = new THREE.InstancedMesh(shardGeo, new THREE.MeshStandardMaterial({ metalness: 0.5, roughness: 0.35 }), SHARDS);
  const palette = [0x3161f1, 0x6188ff, 0xff007a, 0xf4f6ff, 0x3b1d82, 0x9fb3ff];
  const shardData = [];
  const dummy = new THREE.Object3D();
  const col = new THREE.Color();
  for (let i = 0; i < SHARDS; i++) {
    const p = path.getPointAt(0.03 + Math.random() * 0.97);
    const ang = Math.random() * Math.PI * 2;
    const rad = 8 + Math.random() * 16;
    shardData.push({
      base: new THREE.Vector3(p.x + Math.cos(ang) * rad, p.y + Math.sin(ang) * rad * 0.7, p.z + (Math.random() - 0.5) * 10),
      rot: new THREE.Euler(Math.random() * 6, Math.random() * 6, Math.random() * 6),
      spin: (Math.random() - 0.5) * 0.5,
      bob: Math.random() * Math.PI * 2,
      s: 0.3 + Math.random() * 0.9,
    });
    shards.setColorAt(i, col.set(palette[i % palette.length]));
  }
  scene.add(shards);

  /* ---------- Starfield ---------- */
  const STARS = isTouch ? 1600 : 3600;
  const depth = N * 34 + 80;
  const starPos = new Float32Array(STARS * 3);
  const starCol = new Float32Array(STARS * 3);
  for (let i = 0; i < STARS; i++) {
    starPos[i * 3] = (Math.random() - 0.5) * 170;
    starPos[i * 3 + 1] = (Math.random() - 0.5) * 120;
    starPos[i * 3 + 2] = 30 - Math.random() * depth;
    col.set(Math.random() < 0.18 ? 0xff5aa8 : Math.random() < 0.5 ? 0x9fb3ff : 0xffffff);
    starCol.set([col.r, col.g, col.b], i * 3);
  }
  const starGeo = new THREE.BufferGeometry();
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  starGeo.setAttribute('color', new THREE.BufferAttribute(starCol, 3));
  const stars = new THREE.Points(starGeo, new THREE.PointsMaterial({ size: 0.13, vertexColors: true, transparent: true, opacity: 0.85 }));
  scene.add(stars);

  /* ---------- Emblem portal (white outline) at the end of the page ---------- */
  const portal = new THREE.Group();
  emblemShapes(9).forEach(s => {
    portal.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(extrude(s, 0.1, 9), 20),
      new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 })
    ));
  });
  const end = path.getPointAt(1);
  portal.position.set(end.x, end.y, end.z - 18);
  scene.add(portal);

  /* ---------- Layout ---------- */
  let emblemX = 0, emblemY = 0, emblemS = 1;
  const resize = () => {
    const w = innerWidth, h = innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.fov = w < 760 ? 68 : 50;
    camera.updateProjectionMatrix();
    const wide = w / h > 1.1;
    const small = heroMode === 'corner';
    emblemX = wide ? (small ? 9 : 7.5) : 0;
    emblemY = wide ? (small ? 1 : 0) : 4.6;
    emblemS = (wide ? 1 : 0.7) * (small ? 0.75 : 1);
    emblem.scale.setScalar(emblemS);
  };
  addEventListener('resize', resize);
  resize();

  /* ---------- Scroll → stage ---------- */
  let offsets = [];
  const measure = () => { offsets = stages.map(s => s.getBoundingClientRect().top + scrollY); };
  measure();
  addEventListener('resize', measure);
  addEventListener('load', measure);
  document.addEventListener('kc:layout', measure);

  let stageTarget = 0;
  const readScroll = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    const y = scrollY;
    let i = 0;
    while (i < offsets.length - 1 && y >= offsets[i + 1]) i++;
    let frac = 0;
    if (i < offsets.length - 1) {
      const segEnd = Math.min(offsets[i + 1], max);
      frac = segEnd > offsets[i] ? (y - offsets[i]) / (segEnd - offsets[i]) : 1;
    } else if (max > offsets[i]) {
      frac = (y - offsets[i]) / (max - offsets[i]);
    }
    stageTarget = Math.min(N - 1 + 0.6, i + Math.min(1, Math.max(0, frac)) * (i < offsets.length - 1 ? 1 : 0.6));
  };
  addEventListener('scroll', readScroll, { passive: true });
  addEventListener('resize', readScroll);
  document.addEventListener('kc:layout', readScroll);
  readScroll();

  const mouse = new THREE.Vector2(), mouseS = new THREE.Vector2();
  addEventListener('pointermove', e => mouse.set(e.clientX / innerWidth - 0.5, e.clientY / innerHeight - 0.5));

  /* Page transition: rush forward through the portal */
  let warp = 0, warpTarget = 0;
  document.addEventListener('kc:leave', () => { warpTarget = 1; });
  addEventListener('pageshow', () => { warpTarget = 0; warp = 0; });

  /* ---------- Loop ---------- */
  const clock = new THREE.Clock();
  const look = new THREE.Vector3();
  const heroLook = new THREE.Vector3();
  let stage = stageTarget;
  const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

  const tick = () => {
    const t = reduceMotion ? 0 : clock.getElapsedTime();
    stage += (stageTarget - stage) * (reduceMotion ? 1 : 0.07);
    warp += (warpTarget - warp) * 0.12;
    mouseS.lerp(mouse, 0.05);

    const ct = Math.min(stageToT(stage), 0.999);
    const pos = path.getPointAt(ct);
    path.getPointAt(Math.min(ct + 0.03, 1), look);
    heroLook.set(emblemX * 0.45, emblemY * 0.35, 0);
    look.lerp(heroLook, 1 - smooth(0, 0.9, stage));
    camera.position.copy(pos);
    camera.position.x += mouseS.x * 2;
    camera.position.y += -mouseS.y * 1.5;
    camera.position.z -= warp * 14;
    camera.lookAt(look);
    camera.rotateZ(Math.sin(stage * 1.3) * 0.06 + warp * 0.5);
    if (Math.abs(camera.fov - (innerWidth < 760 ? 68 : 50) - warp * 30) > 0.05) {
      camera.fov = (innerWidth < 760 ? 68 : 50) + warp * 30;
      camera.updateProjectionMatrix();
    }

    blueLight.position.set(pos.x + 8, pos.y + 5, pos.z - 6);
    pinkLight.position.set(pos.x - 8, pos.y - 4, pos.z - 14);

    // Emblem: layers separate in depth and counter-rotate as you leave the hero
    const ex = smooth(0, 1.4, stage);
    emblem.position.set(emblemX, emblemY, 0);
    emblem.rotation.set(Math.sin(t * 0.4) * 0.12 + mouseS.y * 0.3 - ex * 0.5, Math.sin(t * 0.3) * 0.2 + mouseS.x * 0.5 + ex * 0.9, 0);
    layers.forEach((m, k) => {
      m.position.z = ex * k * 2.4;
      m.rotation.z = (k % 2 ? -1 : 1) * ex * (k + 1) * 0.8;
    });

    for (let i = 0; i < SHARDS; i++) {
      const d = shardData[i];
      dummy.position.copy(d.base);
      dummy.position.y += Math.sin(t * 0.6 + d.bob) * 0.6;
      dummy.rotation.set(d.rot.x + t * d.spin, d.rot.y + t * d.spin * 0.7 + stage * 0.5, d.rot.z);
      dummy.scale.setScalar(d.s);
      dummy.updateMatrix();
      shards.setMatrixAt(i, dummy.matrix);
    }
    shards.instanceMatrix.needsUpdate = true;

    stars.rotation.z = stage * 0.08;
    portal.rotation.z = t * 0.1;
    portal.children.forEach((l, k) => {
      l.rotation.z = (k % 2 ? -1 : 1) * t * 0.15 * (k + 1);
      l.position.z = smooth(N - 1.5, N - 0.5, stage) * k * 2;
    });

    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  };
  tick();
})();
