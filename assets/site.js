// The Daily Compiler · küçük etkileşimler: tema düğmesi, bölüm menüsü vurgusu, kadran kaydırma/klavye, iç atıf vurgusu
(function () {
  // Arşiv, Hakkında ve Benchmark sayfalarında başlığın solunda bugünün tarihi (İstanbul saati)
  var today = document.querySelector('.mast-date[data-today]');
  if (today) {
    try {
      var now = new Date(), o = { timeZone: 'Europe/Istanbul' };
      var d = new Intl.DateTimeFormat('tr-TR', Object.assign({ day: 'numeric', month: 'long', year: 'numeric' }, o)).format(now);
      var w = new Intl.DateTimeFormat('tr-TR', Object.assign({ weekday: 'long' }, o)).format(now);
      var b = document.createElement('b'); b.textContent = d;
      today.appendChild(b); today.appendChild(document.createTextNode(w));
    } catch (e) {}
  }

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
    // Sağda devamı varsa ok ve solma, solda kaydırılmış kısım varsa soldan solma
    var edge = function () {
      // Okun yer açmak için eklediği sağ boşluk ölçüme katılmaz (yoksa ok kendini açık tutar)
      var pr = nav.classList.contains('has-more') ? parseFloat(getComputedStyle(scroller).paddingRight) || 0 : 0;
      nav.classList.toggle('has-more', scroller.scrollLeft + scroller.clientWidth < scroller.scrollWidth - pr - 4);
      nav.classList.toggle('has-less', scroller.scrollLeft > 4);
    };
    if (more && scroller !== nav) {
      scroller.addEventListener('scroll', edge, { passive: true }); addEventListener('resize', edge); edge();
      // Yapışınca logo menüye girer ve menünün genişliği değişir: geçiş bitince de yeniden ölç
      var brand = nav.querySelector('.nav-brand');
      if (brand) brand.addEventListener('transitionend', function (e) { if (e.propertyName === 'max-width') edge(); });
      more.addEventListener('click', function () { scroller.scrollBy({ left: scroller.clientWidth * .6, behavior: 'smooth' }); });
    }
    // Menü üste yapıştığında küçük logoyu göster
    var sentinel = document.querySelector('.nav-sentinel');
    if (sentinel) {
      new IntersectionObserver(function (es) {
        var e = es[es.length - 1];
        nav.classList.toggle('stuck', !e.isIntersecting && e.boundingClientRect.top < 1);
        if (typeof edge === 'function') edge();
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
  // Telefonda haber metnini kes: küçük haberde ~3, büyük haberde ~8 satırdan sonraki ilk uygun cümle sonunda.
  // Metin sığıyorsa düğme hiç görünmez.
  var phone = window.matchMedia && matchMedia('(max-width: 560px)');
  // Kesme noktası: hedef satırdan önceki son cümle sonu; o çok erkense (hedefin %60'ından önce) bir sonraki cümle sonu
  function cutAt(body, lines) {
    var p = body.querySelector('p') || body, lh = parseFloat(getComputedStyle(p).lineHeight) || 24;
    var top = body.getBoundingClientRect().top, limit = top + lines * lh + 4;
    var w = document.createTreeWalker(body, NodeFilter.SHOW_TEXT), r = document.createRange(), n, m, rx, ends = [];
    while ((n = w.nextNode())) {
      if (n.parentNode.closest('.rest')) continue;
      rx = /[.!?…][”"’)]*(?=\s|$)/g;
      while ((m = rx.exec(n.data))) {
        r.setStart(n, m.index); r.setEnd(n, m.index + 1);
        var rc = r.getClientRects();
        if (rc.length) ends.push({ n: n, i: m.index + m[0].length, y: rc[rc.length - 1].bottom });
      }
    }
    if (!ends.length) return null;
    var k = -1;
    ends.forEach(function (e, j) { if (e.y <= limit) k = j; });
    if (k < 0) k = 0;
    else if (ends[k].y < top + lines * lh * .6 && ends[k + 1] && ends[k + 1].y <= top + (lines * 2 + 1) * lh) k++;
    return ends[k] === ends[ends.length - 1] ? null : ends[k];
  }
  // Kesme noktasından sonraki her şeyi .rest ile işaretle (paragraf yapısı bozulmaz)
  function markRest(body, cut) {
    var rest = cut.n.splitText(cut.i), node = rest;
    var wrap = function (x) {
      if (x.nodeType === 3) { if (!x.data.trim() && x !== rest) return; var sp = document.createElement('span'); sp.className = 'rest'; x.parentNode.insertBefore(sp, x); sp.appendChild(x); }
      else if (x.nodeType === 1) x.classList.add('rest');
    };
    while (node && node !== body) {
      var next = node.nextSibling;
      if (node === rest) wrap(node);
      for (var x = next; x; ) { var nx = x.nextSibling; wrap(x); x = nx; }
      node = node.parentNode === body ? null : node.parentNode;
    }
  }
  var reduceMotion = function () { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; };
  function setOpen(art, open) {
    var b = art.querySelector('.more');
    art.classList.toggle('clamp', !open);
    if (b) { b.textContent = open ? 'Kapat' : 'Devamı'; b.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  }
  function clampAll() {
    if (!phone || !phone.matches) return;
    // Manşet ~6, büyük haber ~8, küçük haber ~3 satırdan sonraki cümle sonunda kesilir
    Array.prototype.forEach.call(document.querySelectorAll('article, #a-manset'), function (art) {
      var b = art.querySelector('.more'), body = art.querySelector('.body, .cols');
      if (!b || !body || b.dataset.ready) return;
      b.dataset.ready = '1';
      var cut = cutAt(body, art.id === 'a-manset' ? 6 : art.classList.contains('big') ? 8 : 3);
      if (!cut) return;
      markRest(body, cut);
      art.classList.add('clamp');
      b.hidden = false;
      b.addEventListener('click', function () {
        var opening = art.classList.contains('clamp');
        setOpen(art, opening);
        // Kapatınca haberin başı ekranın üstünde kaldıysa okur haberin başına döner
        if (!opening && art.getBoundingClientRect().top < 0) art.scrollIntoView({ block: 'start', behavior: reduceMotion() ? 'auto' : 'smooth' });
      });
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
    var data = JSON.parse(veri.textContent), q = document.getElementById('arc-q'), count = box.querySelector('.arc-count');
    var fold = function (t) { return t.replace(/İ/g, 'i').replace(/I/g, 'ı').toLowerCase().replace(/[’']/g, "'"); };
    var rows = Array.prototype.slice.call(document.querySelectorAll('.arc-list li'));
    data.forEach(function (it, i) { it.li = rows[i]; it.f = it.a.map(function (x) { return fold(x[1]); }); if (it.li) { it.head = it.li.querySelector(':scope > a'); it.html = it.head.innerHTML; } });
    var esc = function (t) { return t.replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
    // Eşleşen kelimeleri <mark> ile sar: metin düğümlerinde aranır, iç biçim (code vb.) korunur
    var mark = function (el, words) {
      var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], n;
      while ((n = w.nextNode())) nodes.push(n);
      nodes.forEach(function (node) {
        var f = fold(node.data), rs = [];
        if (f.length !== node.data.length) return;
        words.forEach(function (wd) { var i = f.indexOf(wd); while (i > -1) { rs.push([i, i + wd.length]); i = f.indexOf(wd, i + wd.length); } });
        if (!rs.length) return;
        rs.sort(function (a, b) { return a[0] - b[0]; });
        var frag = document.createDocumentFragment(), at = 0;
        rs.forEach(function (r) {
          if (r[0] < at) { if (r[1] > at) r[0] = at; else return; }
          frag.appendChild(document.createTextNode(node.data.slice(at, r[0])));
          var m = document.createElement('mark'); m.textContent = node.data.slice(r[0], r[1]); frag.appendChild(m); at = r[1];
        });
        frag.appendChild(document.createTextNode(node.data.slice(at)));
        node.parentNode.replaceChild(frag, node);
      });
    };
    var run = function () {
      var words = fold(q.value.trim()).split(/\s+/).filter(Boolean), nIss = 0, nHit = 0;
      data.forEach(function (it) {
        var old = it.li && it.li.querySelector('.arc-hits');
        if (old) old.remove();
        if (!it.li) return;
        var hits = [];
        var lead = false;
        if (words.length) it.f.forEach(function (t, k) { if (words.every(function (w) { return t.indexOf(w) > -1; })) { if (it.a[k][0] === 'manset') lead = true; else hits.push(it.a[k]); } });
        var show = !words.length || lead || hits.length > 0;
        it.li.hidden = !show;
        // Manşet eşleşmiyorsa soluk: okur eşleşmenin alttaki satırlarda olduğunu görür
        it.head.innerHTML = it.html;
        it.li.classList.toggle('dim', words.length > 0 && !lead);
        if (lead) mark(it.head, words);
        if (words.length && show) { nIss++; nHit += hits.length + (lead ? 1 : 0); }
        if (hits.length) {
          var ul = document.createElement('ul');
          ul.className = 'arc-hits';
          ul.innerHTML = hits.slice(0, 4).map(function (x) {
            var t = x[1].length > 140 ? x[1].slice(0, 138) + '…' : x[1];
            return '<li><a href="' + it.h + (x[0] ? '#' + (x[0].indexOf('sec-') === 0 ? x[0] : 'a-' + x[0]) : '') + '">' + esc(t) + '</a></li>';
          }).join('') + (hits.length > 4 ? '<li class="more-hits">+' + (hits.length - 4) + '</li>' : '');
          it.li.appendChild(ul);
          Array.prototype.forEach.call(ul.querySelectorAll('a'), function (a) { mark(a, words); });
        }
      });
      Array.prototype.forEach.call(document.querySelectorAll('.arc-month'), function (m) {
        m.hidden = !m.querySelector('.arc-list > li:not([hidden])');
      });
      count.textContent = !words.length ? '' : nHit ? nIss + ' sayıda ' + nHit + ' sonuç' : 'Bu aramayla eşleşen haber yok.';
    };
    box.hidden = false;
    q.addEventListener('input', run);
  }
})();
