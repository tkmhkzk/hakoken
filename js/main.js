/* =========================================================
   箱建エンジニアリング — interactions
   ========================================================= */
(function () {
  'use strict';

  const header = document.getElementById('header');
  const menuToggle = document.getElementById('menuToggle');
  const gnav = document.getElementById('gnav');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header: scroll state + hide on scroll down ---------- */
  let lastY = window.scrollY;
  const onScroll = () => {
    const y = window.scrollY;
    header.classList.toggle('scrolled', y > 60);
    if (!document.body.classList.contains('nav-open')) {
      if (y > lastY && y > 400) header.classList.add('hide');
      else header.classList.remove('hide');
    }
    lastY = y;
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  const closeMenu = () => {
    document.body.classList.remove('nav-open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'メニューを開く');
  };
  menuToggle.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
  });
  gnav.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMenu));

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('[data-reveal]');
  // apply small stagger within shared parents
  document.querySelectorAll('.hero-actions').forEach(() => {});
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('in');
            obs.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in'));
  }

  /* ---------- Hero title lines: reveal on load ---------- */
  window.addEventListener('load', () => {
    const lines = document.querySelectorAll('.hero-title .line');
    lines.forEach((line, i) => {
      setTimeout(() => line.classList.add('in'), 200 + i * 140);
    });
  });

  /* ---------- Count-up stats ---------- */
  const counters = document.querySelectorAll('.count');
  const runCount = (el) => {
    const target = parseFloat(el.dataset.target || '0');
    const suffix = el.dataset.suffix || '';
    el.setAttribute('data-suffix', suffix);
    if (reduce) { el.textContent = target.toLocaleString(); return; }
    const dur = 1600;
    const start = performance.now();
    const ease = (t) => 1 - Math.pow(1 - t, 3);
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const val = Math.floor(ease(p) * target);
      el.textContent = val.toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString();
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((e) => {
          if (e.isIntersecting) { runCount(e.target); obs.unobserve(e.target); }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((c) => co.observe(c));
  } else {
    counters.forEach((c) => runCount(c));
  }

  /* ---------- Hero parallax (grid) ---------- */
  const heroGrid = document.querySelector('.hero-grid');
  if (heroGrid && !reduce) {
    let ticking = false;
    window.addEventListener(
      'scroll',
      () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const y = window.scrollY;
          if (y < window.innerHeight) {
            heroGrid.style.transform = `translateY(${y * 0.18}px) scale(1.05)`;
          }
          ticking = false;
        });
      },
      { passive: true }
    );
  }

  /* ---------- Nav active section highlight ---------- */
  const navLinks = Array.from(document.querySelectorAll('.gnav > ul a'));
  const sections = navLinks
    .map((a) => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const so = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const id = e.target.id;
            navLinks.forEach((a) =>
              a.classList.toggle('current', a.getAttribute('href') === '#' + id)
            );
          }
        });
      },
      { rootMargin: '-45% 0px -50% 0px' }
    );
    sections.forEach((s) => so.observe(s));
  }

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
