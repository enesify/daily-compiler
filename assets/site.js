// The Daily Compiler · küçük etkileşimler: tema düğmesi, bölüm menüsü vurgusu, kadran kaydırma/klavye, iç atıf vurgusu
(function () {
  // Tema: varsayılan sistem ayarı; seçim sistemle aynıysa kayıt silinir ve yine sistem izlenir
  var btn = document.getElementById('theme-toggle');
  if (btn && window.matchMedia) {
    var root = document.documentElement, mq = matchMedia('(prefers-color-scheme: dark)');
    var eff = function () { return root.getAttribute('data-theme') || (mq.matches ? 'dark' : 'light'); };
    var paint = function () {
      var dark = eff() === 'dark';
      var label = dark ? 'Açık temaya geç' : 'Koyu temaya geç';
      btn.setAttribute('aria-label', label); btn.title = label;
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    };
    btn.hidden = false; paint();
    btn.addEventListener('click', function () {
      var next = eff() === 'dark' ? 'light' : 'dark', sys = mq.matches ? 'dark' : 'light';
      try {
        if (next === sys) { root.removeAttribute('data-theme'); localStorage.removeItem('dc-theme'); }
        else { root.setAttribute('data-theme', next); localStorage.setItem('dc-theme', next); }
      } catch (e) { root.setAttribute('data-theme', next); }
      paint();
    });
    if (mq.addEventListener) mq.addEventListener('change', paint);
  }

  // Bölüm menüsü: görünen bölümü vurgula, menü kayıyorsa o linki görünür tut
  var nav = document.querySelector('nav.index');
  if (nav && 'IntersectionObserver' in window) {
    var links = {}, active = null, scroller = nav.querySelector('.nav-links') || nav;
    // Menü üste yapıştığında küçük logoyu göster
    var sentinel = document.querySelector('.nav-sentinel');
    if (sentinel) {
      new IntersectionObserver(function (es) {
        var e = es[es.length - 1];
        nav.classList.toggle('stuck', !e.isIntersecting && e.boundingClientRect.top < 1);
      }).observe(sentinel);
    }
    Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var mark = function (id) {
      var a = links[id];
      if (!a || a === active) return;
      if (active) active.removeAttribute('aria-current');
      a.setAttribute('aria-current', 'true'); active = a;
      if (scroller.scrollWidth > scroller.clientWidth) {
        var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
        scroller.scrollTo({ left: a.offsetLeft - scroller.clientWidth / 2 + a.offsetWidth / 2, behavior: reduce ? 'auto' : 'smooth' });
      }
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: '-15% 0px -75% 0px' });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  var dial = document.getElementById('archive');
  if (dial) {
    var track = dial.querySelector('.dial-track');
    var cur = dial.querySelector('.tick[aria-current="page"]');
    if (track && cur) {
      var r = track.getBoundingClientRect(), c = cur.getBoundingClientRect();
      track.scrollLeft += c.left - r.left - r.width / 2 + c.width / 2;
    }
    var prev = dial.querySelector('a.dial-step[rel="prev"]');
    var next = dial.querySelector('a.dial-step[rel="next"]');
    document.addEventListener('keydown', function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
      var t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.key === 'ArrowLeft' && prev) { location.href = prev.href; }
      if (e.key === 'ArrowRight' && next) { location.href = next.href; }
    });
    var head = dial.querySelector('.dial-head'), sx = null, sy = null;
    if (head) {
      head.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
      head.addEventListener('touchend', function (e) {
        if (sx === null) return;
        var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy; sx = null;
        if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) {
          var a = dx > 0 ? prev : next; if (a) location.href = a.href;
        }
      }, { passive: true });
    }
  }
  function flash() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    if (!/^a-/.test(id)) return;
    var t = document.getElementById(id);
    if (!t) return;
    t.classList.remove('flash'); void t.offsetWidth; t.classList.add('flash');
  }
  window.addEventListener('hashchange', flash);
  flash();
})();
