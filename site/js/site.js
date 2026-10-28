/* Page UI shared by every page: nav, reveals, counters, tilt, coverflow tracks, countdown, forms, page transitions. */
(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = matchMedia('(pointer: coarse)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const layoutChanged = () => document.dispatchEvent(new Event('kc:layout'));

  requestAnimationFrame(() => document.body.classList.add('ready'));

  /* ---------- Page transitions ---------- */
  const isInternal = a => a.host === location.host && /\.html$|\/$/.test(a.pathname) && !a.target && !a.hasAttribute('download');
  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    if (!isInternal(a) || (a.pathname === location.pathname && a.hash)) return;
    e.preventDefault();
    document.body.classList.add('leaving');
    document.dispatchEvent(new Event('kc:leave'));
    setTimeout(() => { location.href = a.href; }, reduceMotion ? 0 : 520);
  });
  addEventListener('pageshow', () => document.body.classList.remove('leaving'));

  /* ---------- Split titles into animated characters ---------- */
  $$('[data-split]').forEach(el => {
    let i = 0;
    const wrap = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType !== 3) return wrap(n);
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(word => {
          if (!word) return;
          if (/^\s+$/.test(word)) return frag.appendChild(document.createTextNode(' '));
          const w = document.createElement('span');
          w.className = 'w';
          [...word].forEach(c => {
            const s = document.createElement('span');
            s.className = 'ch';
            s.textContent = c;
            s.style.transitionDelay = (0.25 + i++ * 0.022) + 's';
            w.appendChild(s);
          });
          frag.appendChild(w);
        });
        n.replaceWith(frag);
      });
    };
    wrap(el);
  });

  /* ---------- Rail, reveals, counters ---------- */
  const stages = $$('main > [data-stage]');
  const rail = $('#rail');
  if (rail) {
    stages.forEach(s => {
      const a = document.createElement('a');
      a.href = '#' + s.id;
      a.setAttribute('aria-label', s.dataset.label || s.id);
      rail.appendChild(a);
    });
  }
  const dots = rail ? [...rail.children] : [];

  const countUp = el => {
    const to = +el.dataset.count, suffix = el.dataset.suffix || '';
    if (reduceMotion) { el.textContent = to + suffix; return; }
    const t0 = performance.now(), dur = 1600;
    const step = now => {
      const k = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))) + suffix;
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting || e.target.classList.contains('in')) return;
      e.target.classList.add('in');
      $$('[data-count]', e.target).forEach(countUp);
    });
  }, { threshold: 0.12 });
  $$('main > section, main section.sub-in').forEach(s => io.observe(s));

  /* ---------- Nav ---------- */
  const nav = $('#nav');
  const menuBtn = $('#menuBtn');
  menuBtn.addEventListener('click', () => menuBtn.setAttribute('aria-expanded', nav.classList.toggle('open')));

  /* ---------- Tilt ---------- */
  if (!isTouch && !reduceMotion) {
    $$('[data-tilt]').forEach(el => {
      const amt = +(el.dataset.tilt || 12);
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = `rotateY(${x * amt}deg) rotateX(${-y * amt}deg) translateZ(10px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
  }

  /* ---------- Pinned coverflow tracks ---------- */
  const tracks = $$('.pinned').map(section => {
    const track = $('.track', section);
    const scrub = $('.scrub i', section);
    const count = $('[data-count-label]', section);
    const all = [...track.children];
    const st = { section, track, scrub, all, visible: all };
    st.size = () => { section.style.height = `calc(100vh + ${Math.max(1, st.visible.length - 1) * 38}vh)`; };
    const filters = $('.filters', section);
    if (filters) {
      const apply = f => {
        $$('button', filters).forEach(b => b.setAttribute('aria-pressed', b.dataset.f === f));
        all.forEach(c => { c.style.display = (f === 'all' || c.dataset.cat === f) ? '' : 'none'; });
        st.visible = all.filter(c => c.style.display !== 'none');
        if (count) count.textContent = `${st.visible.length} event${st.visible.length === 1 ? '' : 's'} · Kuwait`;
        st.size();
        layoutChanged();
        update();
      };
      filters.addEventListener('click', e => {
        const b = e.target.closest('button');
        if (!b) return;
        apply(b.dataset.f);
        history.replaceState(null, '', b.dataset.f === 'all' ? location.pathname : `?category=${b.dataset.f}`);
      });
      const fromUrl = new URLSearchParams(location.search).get('category');
      if (fromUrl && $(`button[data-f="${fromUrl}"]`, filters)) st.initial = fromUrl;
      st.apply = apply;
    }
    st.size();
    return st;
  });

  const updateTrack = st => {
    const r = st.section.getBoundingClientRect();
    const span = r.height - innerHeight;
    const p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
    if (st.scrub) st.scrub.style.transform = `scaleX(${p})`;
    const v = st.visible;
    if (!v.length || r.bottom < -100 || r.top > innerHeight + 100) return;
    const first = v[0], last = v[v.length - 1];
    const a = first.offsetLeft + first.offsetWidth / 2;
    const b = last.offsetLeft + last.offsetWidth / 2;
    const x = a + (b - a) * p;
    st.track.style.transform = `translate3d(${innerWidth / 2 - x}px,0,0)`;
    const w = first.offsetWidth + 28;
    v.forEach(c => {
      const d = (c.offsetLeft + c.offsetWidth / 2 - x) / w;
      const ad = Math.min(Math.abs(d), 3);
      c.style.transform = reduceMotion ? '' : `translateZ(${-ad * 140}px) rotateY(${Math.max(-1, Math.min(1, d)) * -32}deg) scale(${1 - ad * 0.04})`;
      c.style.opacity = Math.max(0.25, 1 - ad * 0.28);
      c.style.zIndex = 10 - Math.round(ad);
    });
  };

  /* ---------- Scroll loop ---------- */
  const bar = $('#bar');
  const update = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
    nav.classList.toggle('solid', scrollY > 40);
    const mid = innerHeight / 2;
    let active = 0;
    stages.forEach((s, k) => { if (s.getBoundingClientRect().top <= mid) active = k; });
    dots.forEach((d, k) => d.classList.toggle('active', k === active));
    tracks.forEach(updateTrack);
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  tracks.forEach(st => st.initial && st.apply(st.initial));
  update();
  layoutChanged();

  /* ---------- Past events: label cards, replace countdown and booking link ---------- */
  const now = Date.now();
  $$('.ev[data-end]').forEach(c => {
    if (new Date(c.dataset.end).getTime() >= now) return;
    c.classList.add('past');
    const go = $('.go', c);
    if (go) go.textContent = 'Took place';
  });
  const cd = $('[data-countdown]');
  if (cd && new Date(cd.dataset.end).getTime() < now) {
    cd.outerHTML = '<p class="chip" style="margin:18px 0 0">This event has taken place</p>';
    const book = $('[data-book]');
    if (book) { book.href = 'events.html'; book.textContent = 'See upcoming events →'; }
  } else if (cd) {
    const target = new Date(cd.dataset.countdown).getTime();
    const cells = $$('b', cd);
    const tickCd = () => {
      let s = Math.max(0, Math.floor((target - Date.now()) / 1000));
      const parts = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
      parts.forEach((v, i) => { cells[i].textContent = String(v).padStart(2, '0'); });
    };
    tickCd();
    setInterval(tickCd, 1000);
  }

  /* ---------- Add to calendar (.ics) ---------- */
  $$('[data-ics]').forEach(a => {
    const d = JSON.parse(a.dataset.ics);
    const ics = [
      'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Knowledge Club//EN', 'BEGIN:VEVENT',
      `UID:${d.uid}@knowledgeclub.com`, `DTSTART;TZID=Asia/Kuwait:${d.start}`, `DTEND;TZID=Asia/Kuwait:${d.end}`,
      `SUMMARY:${d.title}`, `LOCATION:${d.location}`, `DESCRIPTION:${d.desc}`, 'END:VEVENT', 'END:VCALENDAR',
    ].join('\r\n');
    a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }));
  });

  /* ---------- Contact form → email ---------- */
  const contact = $('#contactForm');
  if (contact) {
    contact.addEventListener('submit', e => {
      e.preventDefault();
      const f = new FormData(contact);
      const body = `Name: ${f.get('name')}\nEmail: ${f.get('email')}\nPhone: ${f.get('phone')}\n\n${f.get('message')}`;
      location.href = `mailto:${contact.dataset.to}?subject=${encodeURIComponent(f.get('subject') || 'Knowledge Club enquiry')}&body=${encodeURIComponent(body)}`;
      $('#contactNote').textContent = 'Your email app should open with the message ready to send.';
    });
  }

  /* ---------- Membership form: posts to the existing Mailchimp list in a new tab ---------- */
  const join = $('#joinForm');
  if (join) {
    join.addEventListener('submit', () => {
      $('#joinNote').textContent = 'Thanks! Confirm your subscription in the tab that just opened.';
    });
  }
})();
