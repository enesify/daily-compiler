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
    // Menü sağa taşıyorsa ok göster; sona gelince gizle
    var more = nav.querySelector('.nav-more');
    var edge = function () { nav.classList.toggle('more', scroller.scrollLeft + scroller.clientWidth < scroller.scrollWidth - 4); };
    if (more && scroller !== nav) {
      scroller.addEventListener('scroll', edge, { passive: true }); addEventListener('resize', edge); edge();
      more.addEventListener('click', function () { scroller.scrollBy({ left: scroller.clientWidth * .6, behavior: 'smooth' }); });
    }
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
  // Telefonda haber metnini kes (küçük haber 3, büyük haber 8 satır); metin sığıyorsa düğme hiç görünmez
  var phone = window.matchMedia && matchMedia('(max-width: 560px)');
  function setOpen(art, open) {
    var b = art.querySelector('.more');
    art.classList.toggle('clamp', !open);
    if (b) { b.textContent = open ? 'Kapat' : 'Devamı'; b.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  }
  function clampAll() {
    if (!phone || !phone.matches) return;
    Array.prototype.forEach.call(document.querySelectorAll('article'), function (art) {
      var b = art.querySelector('.more'), body = art.querySelector('.body');
      if (!b || !body || b.dataset.ready) return;
      b.dataset.ready = '1';
      art.classList.add('clamp');
      if (body.scrollHeight <= body.clientHeight + 2) { art.classList.remove('clamp'); return; }
      b.hidden = false;
      b.addEventListener('click', function () { setOpen(art, art.classList.contains('clamp')); });
    });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(clampAll); else clampAll();
  if (phone && phone.addEventListener) phone.addEventListener('change', clampAll);

  function flash() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    if (!/^a-/.test(id)) return;
    var t = document.getElementById(id);
    if (!t) return;
    if (t.classList.contains('clamp')) setOpen(t, true);
    t.classList.remove('flash'); void t.offsetWidth; t.classList.add('flash');
  }
  window.addEventListener('hashchange', flash);
  flash();

  // Arşiv araması: sayıların haber başlıklarında, kısa haberlerde ve repo adlarında
  var veri = document.getElementById('arc-veri'), box = document.querySelector('.arc-search');
  if (veri && box) {
    var data = JSON.parse(veri.textContent), q = document.getElementById('arc-q'), none = box.querySelector('.arc-none');
    var fold = function (t) { return t.replace(/İ/g, 'i').replace(/I/g, 'ı').toLowerCase().replace(/[’']/g, "'"); };
    var rows = Array.prototype.slice.call(document.querySelectorAll('.arc-list li'));
    data.forEach(function (it, i) { it.li = rows[i]; it.f = it.a.map(function (x) { return fold(x[1]); }); });
    var esc = function (t) { return t.replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
    var run = function () {
      var words = fold(q.value.trim()).split(/\s+/).filter(Boolean), any = false;
      data.forEach(function (it) {
        var old = it.li && it.li.querySelector('.arc-hits');
        if (old) old.remove();
        if (!it.li) return;
        var hits = [];
        var lead = false;
        if (words.length) it.f.forEach(function (t, k) { if (words.every(function (w) { return t.indexOf(w) > -1; })) { if (it.a[k][0] === 'manset') lead = true; else hits.push(it.a[k]); } });
        var show = !words.length || lead || hits.length > 0;
        it.li.hidden = !show;
        if (show) any = true;
        if (hits.length) {
          var ul = document.createElement('ul');
          ul.className = 'arc-hits';
          ul.innerHTML = hits.slice(0, 4).map(function (x) {
            var t = x[1].length > 140 ? x[1].slice(0, 138) + '…' : x[1];
            return '<li><a href="' + it.h + (x[0] ? '#' + (x[0].indexOf('sec-') === 0 ? x[0] : 'a-' + x[0]) : '') + '">' + esc(t) + '</a></li>';
          }).join('') + (hits.length > 4 ? '<li class="more-hits">+' + (hits.length - 4) + '</li>' : '');
          it.li.appendChild(ul);
        }
      });
      Array.prototype.forEach.call(document.querySelectorAll('.arc-month'), function (m) {
        m.hidden = !m.querySelector('.arc-list > li:not([hidden])');
      });
      none.hidden = any;
    };
    box.hidden = false;
    q.addEventListener('input', run);
  }
})();
