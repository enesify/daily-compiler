// The Daily Compiler · Modeller sayfası: tek grafik, birkaç görünüm. Veri sayfaya gömülü JSON'dan (data/modeller.json) gelir.
// Görünüm değişince her model yeni yerine kayar; ölçümü olmayan model alttaki “ölçüm yok” şeridine iner.
(function () {
  "use strict";
  var svg = document.getElementById("mdl-chart"), src = document.getElementById("mdl-veri");
  if (!svg || !src) return;
  var DATA; try { DATA = JSON.parse(src.textContent); } catch (e) { return; }
  var M = DATA.models, MET = DATA.metrics, VIEWS = DATA.views;
  var NS = "http://www.w3.org/2000/svg", $ = function (id) { return document.getElementById(id); };
  var el = function (t, a, par) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); if (par) par.appendChild(e); return e; };
  var tr = function (v, d) { return v.toFixed(d).replace(".", ","); };
  // değer ve eksen yazımı
  var FMT = {
    puan: { v: function (v) { return String(Math.round(v)); }, t: function (v) { return String(v); } },
    yuzde: { v: function (v) { return "%" + tr(v, 1); }, t: function (v) { return "%" + v; } },
    usd: { v: function (v) { return "$" + tr(v, 2); }, t: function (v) { return "$" + (v < 1 ? tr(v, 1) : v); } },
    dk: { v: function (v) { return tr(v, 1) + " dk"; }, t: function (v) { return String(v); } }
  };
  var fv = function (k, v) { return FMT[MET[k].bicim].v(v); }, ft = function (k, v) { return FMT[MET[k].bicim].t(v); };
  // eksen aralığı ve çentikler veriden hesaplanır
  Object.keys(MET).forEach(function (k) {
    var vs = M.map(function (m) { return m[k]; }).filter(function (v) { return v != null; }), lo = Math.min.apply(0, vs), hi = Math.max.apply(0, vs), t = [];
    if (MET[k].log) {
      var seq = []; for (var e = -3; e <= 6; e++) [1, 2, 5].forEach(function (s) { seq.push(+(s * Math.pow(10, e)).toPrecision(1)); });
      var a = seq.filter(function (s) { return s <= lo; }).pop(), b = seq.filter(function (s) { return s >= hi; })[0];
      t = seq.filter(function (s) { return s >= a && s <= b; }); MET[k].dom = [a, b];
    } else {
      var pad = (hi - lo || 1) * .06; lo -= pad; hi += pad;
      var raw = (hi - lo) / 4, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), step = [1, 2, 5, 10].filter(function (s) { return s * mag >= raw; })[0] * mag;
      var a2 = Math.floor(lo / step) * step, b2 = Math.ceil(hi / step) * step;
      for (var x = a2; x <= b2 + step / 1e6; x += step) t.push(+x.toPrecision(6)); MET[k].dom = [a2, b2];
    }
    MET[k].ticks = t;
  });
  var provs = []; M.forEach(function (m) { if (provs.indexOf(m.saglayici) < 0) provs.push(m.saglayici); });
  var col = function (m) { return "var(--l" + Math.min(6, provs.indexOf(m.saglayici) + 1) + ")"; };
  var gAxis = $("mdl-axis"), gNote = $("mdl-note"), fr = $("mdl-frontier"), under = $("mdl-under");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion:reduce)").matches;
  var view = VIEWS[0], sel = null, G = {}, raf = 0, timers = [];
  var cvs = document.createElement("canvas").getContext("2d");

  // kalıcı öğeler: her model için sap, nokta (açık modelde baklava), etiket
  var D = M.map(function (m, i) {
    var stem = el("line", { "class": "stem", stroke: col(m) }, $("mdl-stems"));
    var g = el("g", { "class": "dot", tabindex: 0, role: "button", "aria-label": m.ad }, $("mdl-dots"));
    el("circle", { r: 20, fill: "transparent" }, g);
    var ring = el("circle", { "class": "ring" }, g);
    var c = el(m.acik ? "path" : "circle", { "class": "c", stroke: col(m), fill: col(m) }, g);
    var t = el("text", { "class": "nm" }, $("mdl-labels"));
    el("tspan", {}, t).textContent = m.kisa || m.ad;
    var tv = el("tspan", { "class": "v", dx: 7 }, t);
    var d = { m: m, i: i, stem: stem, g: g, c: c, ring: ring, t: t, tv: tv, cur: null, from: null, to: null };
    var pick = function () { select(sel === d ? null : d); };
    g.addEventListener("click", pick);
    g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
    g.addEventListener("mouseenter", function () { if (!G.small) select(d); });
    return d;
  });
  svg.addEventListener("mouseleave", function () { if (!G.small) select(null); });

  function geom() {
    var W = svg.clientWidth || svg.parentNode.clientWidth, small = W < 600, H = small ? 450 : 540;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.style.height = H + "px";
    G = { W: W, H: H, small: small, L: small ? 40 : 54, R: small ? 12 : 22, T: small ? 22 : 26, axB: small ? 44 : 50, band: small ? 32 : 36,
          r: small ? 7.5 : 10, nf: small ? 12.5 : 15.5, fs: small ? 10.5 : 12.5 };
    G.pb = H - G.axB - G.band;           // çizim alanının altı
  }
  function sc(k, v, a, b) { var d = MET[k].dom; return MET[k].log ? a + (Math.log(v) - Math.log(d[0])) / (Math.log(d[1]) - Math.log(d[0])) * (b - a) : a + (v - d[0]) / (d[1] - d[0]) * (b - a); }
  function tw(s, size, mono) { cvs.font = (mono ? "400 " : "600 ") + size + "px " + (mono ? '"IBM Plex Mono",monospace' : '"IBM Plex Sans Condensed",Arial,sans-serif'); return cvs.measureText(s).width; }
  function ranked(k) { var s = MET[k].iyi === "dusuk" ? 1 : -1; return M.filter(function (m) { return m[k] != null; }).sort(function (a, b) { return s * (a[k] - b[k]); }); }

  // her modelin bu görünümdeki hedef konumu
  function targets() {
    var miss = 0, order = view.rank ? ranked(view.rank) : null;
    var nMiss = M.filter(function (m) { return view.rank ? m[view.rank] == null : (m[view.x] == null && m[view.y] != null) || m[view.x] == null; }).length;
    var gap = Math.min(170, (G.W - G.R - G.L - 190) / Math.max(1, nMiss));   // şeritteki modeller arası boşluk
    D.forEach(function (d) {
      var m = d.m, t = { miss: false, sx: 0, stem: 0, lab: 1, val: "" };
      if (view.rank) {
        var v = m[view.rank], rowH = (G.pb - G.T) / M.length;
        if (v == null) { t.miss = true; t.x = G.L + (G.small ? 78 : 92) + miss++ * gap; t.y = G.pb + G.band / 2; }
        else { t.x = sc(view.rank, v, G.L, G.W - G.R - (G.small ? 110 : 190)); t.y = G.T + (order.indexOf(m) + .5) * rowH; t.val = fv(view.rank, v); }
        t.sx = t.miss ? t.x : G.L;
      } else {
        var xv = m[view.x], yv = m[view.y];
        if (yv == null || xv == null) { t.miss = true; t.y = G.pb + G.band / 2; t.x = xv != null ? sc(view.x, xv, G.L, G.W - G.R) : G.L + (G.small ? 78 : 92) + miss++ * gap; }
        else { t.x = sc(view.x, xv, G.L, G.W - G.R); t.y = sc(view.y, yv, G.pb, G.T); }
        t.sx = t.x;
      }
      d.to = t;
    });
    placeLabels();
  }
  // sınır çizgisi: aynı ya da daha düşük maliyete (süreye) daha iyisi olmayan modeller
  function frontierSet() {
    if (!view.sinir) return [];
    var best = -Infinity, out = [];
    M.filter(function (m) { return m[view.x] != null && m[view.y] != null; }).sort(function (a, b) { return a[view.x] - b[view.x] || b[view.y] - a[view.y]; })
      .forEach(function (m) { if (m[view.y] > best) { out.push(m); best = m[view.y]; } });
    return out;
  }
  function placeLabels() {
    var r = G.r, nf = G.nf, boxes = [], F = frontierSet();
    D.forEach(function (d) { boxes.push([d.to.x - r - 2, d.to.y - r - 2, 2 * r + 4, 2 * r + 4, d]); });
    // sınır çizgisinin parçaları ve köşe notları da engel: etiket üstlerine binmesin
    if (F.length) {
      var R = G.W - G.R, px = function (m) { return sc(view.x, m[view.x], G.L, R); }, py = function (m) { return sc(view.y, m[view.y], G.pb, G.T); };
      F.forEach(function (m, i) { var x = px(m), y = py(m), nx = i + 1 < F.length ? px(F[i + 1]) : R, y0 = i ? py(F[i - 1]) : G.pb; boxes.push([x, y - 4, nx - x, 8, null]); boxes.push([x - 4, y, 8, y0 - y, null]); });
    }
    if (!view.rank) {
      var big = G.small ? 19 : 30, n = view.notlar || {};
      if (n.tl) boxes.push([G.L + 10, G.T + 6, big * .47 * n.tl.length, big + 6, null]);
      if (n.br) boxes.push([G.W - G.R - big * .72 * .45 * n.br.length - 10, G.pb - 14 - big * .72, big * .72 * .45 * n.br.length, big * .72 + 6, null]);
    }
    // telefonda yalnızca öndekiler etiketli; diğerleri dokununca
    var keep = null, nMissing = D.filter(function (d) { return d.to.miss; }).length;
    if (G.small && !view.rank) keep = F.concat(ranked(view.y).slice(0, 3));
    D.slice().sort(function (a, b) { return a.to.y - b.to.y; }).forEach(function (d) {
      var t = d.to, name = d.m.kisa || d.m.ad, w = tw(name, nf) + (t.val ? 7 + tw(t.val, nf * .88, true) : 0), h = nf * 1.15, x = t.x, y = t.y;
      t.lab = t.miss ? (G.small && nMissing > 2 ? 0 : 1) : (!keep || keep.indexOf(d.m) >= 0) ? 1 : 0;
      var c = view.rank && !t.miss ? [[x + r + 8, y + nf * .36]] :
        [[x + r + 6, y + nf * .36], [x - r - 6 - w, y + nf * .36], [x - w / 2, y - r - 6], [x - w / 2, y + r + nf + 1], [x + r + 3, y - r - 1], [x - r - 3 - w, y - r - 1], [x + r + 3, y + r + nf - 2], [x - r - 3 - w, y + r + nf - 2]];
      var bestC = c[0], bestP = 1e9;
      c.forEach(function (p, ci) {
        var bx = [p[0] - 2, p[1] - nf, w + 4, h], pen = ci * .1;
        if (bx[0] < 2 || bx[0] + bx[2] > G.W - 2) pen += 50;
        if (bx[1] < 2 || (!t.miss && bx[1] + bx[3] > G.pb + 2) || bx[1] + bx[3] > G.H - G.axB + 2) pen += 20;
        boxes.forEach(function (b) { if (b[4] !== d && bx[0] < b[0] + b[2] && bx[0] + bx[2] > b[0] && bx[1] < b[1] + b[3] && bx[1] + bx[3] > b[1]) pen += 10; });
        if (pen < bestP) { bestP = pen; bestC = p; }
      });
      t.lx = bestC[0]; t.ly = bestC[1];
      if (t.lab) boxes.push([t.lx - 2, t.ly - nf, w + 4, h, d]);
    });
  }
  function paint(d) {
    var s = d.cur;
    d.g.setAttribute("transform", "translate(" + s.x.toFixed(1) + "," + s.y.toFixed(1) + ")");
    d.t.setAttribute("x", s.lx.toFixed(1)); d.t.setAttribute("y", s.ly.toFixed(1));
    d.t.style.opacity = (sel === d ? 1 : s.lab).toFixed(2);
    d.stem.setAttribute("x1", s.sx.toFixed(1)); d.stem.setAttribute("x2", s.x.toFixed(1));
    d.stem.setAttribute("y1", s.y.toFixed(1)); d.stem.setAttribute("y2", s.y.toFixed(1));
    d.stem.style.opacity = (s.stem * .45).toFixed(2);
  }
  function styleDots() {
    D.forEach(function (d) {
      var r = G.r, q = r * 1.22;
      if (d.m.acik) d.c.setAttribute("d", "M0 " + -q + "L" + q + " 0 0 " + q + " " + -q + " 0Z"); else d.c.setAttribute("r", r);
      d.ring.setAttribute("r", r + 5); d.t.setAttribute("font-size", G.nf);
      d.c.setAttribute("fill", d.to.miss ? "var(--paper)" : col(d.m));
      d.tv.textContent = d.to.val; d.tv.setAttribute("font-size", (G.nf * .88).toFixed(1));
    });
  }
  function axes() {
    gAxis.textContent = ""; gNote.textContent = "";
    var L = G.L, R = G.W - G.R, T = G.T, pb = G.pb, fs = G.fs, ty = G.H - G.axB + 17;
    var txt = function (par, x, y, s, cls, anc, size) { var e = el("text", { x: x, y: y, "class": cls, "text-anchor": anc || "start", "font-size": size || fs }, par); e.textContent = s; return e; };
    if (view.rank) {
      var k = view.rank, xr = R - (G.small ? 110 : 190), rowH = (pb - T) / M.length;
      MET[k].ticks.forEach(function (v) { var x = sc(k, v, L, xr); el("line", { x1: x, x2: x, y1: T, y2: pb, "class": "grid" }, gAxis); txt(gAxis, x, ty, ft(k, v), "tick", "middle"); });
      ranked(k).forEach(function (m, i) { txt(gAxis, L - 12, T + (i + .5) * rowH + fs * .36, i + 1, "tick", "end", fs + 2); });
      el("line", { x1: L, x2: L, y1: T, y2: pb, "class": "base" }, gAxis);
      txt(gAxis, (L + xr) / 2, G.H - 7, MET[k].eksen, "axis", "middle", fs + .5);
    } else {
      MET[view.y].ticks.forEach(function (v) { var y = sc(view.y, v, pb, T); el("line", { x1: L, x2: R, y1: y, y2: y, "class": "grid" }, gAxis); txt(gAxis, L - 7, y + fs * .36, ft(view.y, v), "tick", "end"); });
      MET[view.x].ticks.forEach(function (v) { var x = sc(view.x, v, L, R); el("line", { x1: x, x2: x, y1: T, y2: pb, "class": "grid" }, gAxis); txt(gAxis, x, ty, ft(view.x, v), "tick", "middle"); });
      el("line", { x1: L, x2: R, y1: pb, y2: pb, "class": "base" }, gAxis);
      txt(gAxis, (L + R) / 2, G.H - 7, MET[view.x].eksen, "axis", "middle", fs + .5);
      txt(gAxis, L, T - 9, "↑ " + MET[view.y].eksen, "axis", "start", fs + .5);
      var big = G.small ? 19 : 30, n = view.notlar || {};
      if (n.tl) txt(gNote, L + 12, T + big + 6, n.tl, "say", "start", big);
      if (n.br) txt(gNote, R - 10, pb - 14, n.br, "say dim", "end", big * .72);
    }
    if (D.some(function (d) { return d.to.miss; })) {
      el("line", { x1: L, x2: R, y1: pb + G.band, y2: pb + G.band, "class": "grid", "stroke-dasharray": "3 4" }, gAxis);
      txt(gAxis, L, pb + G.band / 2 + fs * .36, "ölçüm yok", "tick", "start");
    }
  }
  function drawFrontier(animate) {
    var F = frontierSet();
    if (!F.length) { fr.setAttribute("d", ""); under.setAttribute("d", ""); return; }
    var R = G.W - G.R, pb = G.pb, d = "M" + sc(view.x, F[0][view.x], G.L, R).toFixed(1) + " " + pb;
    F.forEach(function (m, i) { d += "V" + sc(view.y, m[view.y], pb, G.T).toFixed(1) + "H" + (i + 1 < F.length ? sc(view.x, F[i + 1][view.x], G.L, R).toFixed(1) : R); });
    fr.setAttribute("d", d); under.setAttribute("d", d + "V" + pb + "Z");
    fr.style.transition = "none"; fr.style.opacity = 1;
    if (animate) {
      var len = fr.getTotalLength(); fr.style.strokeDasharray = len; fr.style.strokeDashoffset = len;
      fr.getBoundingClientRect();
      fr.style.transition = "stroke-dashoffset .7s cubic-bezier(.4,0,.2,1)"; fr.style.strokeDashoffset = 0;
    } else { fr.style.strokeDasharray = "none"; }
    under.classList.add("on");
  }
  var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var copy = function (o) { var c = {}; for (var k in o) c[k] = o[k]; return c; };
  function render(animate) {
    cancelAnimationFrame(raf); timers.forEach(clearTimeout); timers = [];
    geom(); targets();
    animate = animate && !reduce && D[0].cur;
    if (!animate) {
      styleDots(); axes(); gAxis.style.opacity = gNote.style.opacity = 1;
      D.forEach(function (d) { d.cur = copy(d.to); paint(d); }); drawFrontier(false); return;
    }
    // 1) eksen ve çizgi solar  2) noktalar yeni yerine kayar  3) eksen belirir, çizgi çizilir
    gAxis.style.opacity = gNote.style.opacity = 0; fr.style.transition = "opacity .18s"; fr.style.opacity = 0; under.classList.remove("on");
    timers.push(setTimeout(function () { axes(); gAxis.style.opacity = 1; gNote.style.opacity = 1; }, 230));
    styleDots();
    D.forEach(function (d) { d.from = copy(d.cur); });
    var DUR = 640, STAG = 28, order = D.slice().sort(function (a, b) { return a.from.y - b.from.y; }), t0 = performance.now();
    var keys = ["x", "y", "lx", "ly", "sx", "stem", "lab"];
    (function frame(now) {
      var done = true;
      order.forEach(function (d, i) {
        var t = Math.min(1, Math.max(0, (now - t0 - i * STAG) / DUR)), e = ease(t); if (t < 1) done = false;
        keys.forEach(function (k) { d.cur[k] = d.from[k] + (d.to[k] - d.from[k]) * e; }); paint(d);
      });
      if (!done) raf = requestAnimationFrame(frame);
      else { D.forEach(function (d) { d.cur = copy(d.to); paint(d); }); drawFrontier(true); }
    })(t0);
  }
  function select(d) {
    sel = d;
    D.forEach(function (o) { o.g.classList.toggle("sel", o === d); o.g.classList.toggle("dimmed", !!d && o !== d); if (o.cur) paint(o); });
    var r = $("mdl-read"); r.textContent = "";
    if (!d) { if (G.small) r.textContent = "Ayrıntı için bir noktaya dokun."; return; }
    var m = d.m, add = function (tag, text, cls) { var e = document.createElement(tag); e.textContent = text; if (cls) e.className = cls; r.appendChild(e); return e; };
    add("i", "", "sw").style.background = col(m);
    add("b", m.ad);
    r.appendChild(document.createTextNode(" · " + m.saglayici + (m.ayar ? " · ayar: " + m.ayar : "") + (m.acik ? " · açık model" : "")));
    r.appendChild(document.createElement("br"));
    Object.keys(MET).forEach(function (k, i) {
      if (i) r.appendChild(document.createTextNode(" · "));
      var s = add("span", MET[k].ad + ": ", "m"); var b = document.createElement("b"); b.textContent = m[k] == null ? "ölçüm bekleniyor" : fv(k, m[k]); s.appendChild(b);
    });
  }
  // görünüm düğmeleri
  var box = $("mdl-views"), q = $("mdl-q");
  VIEWS.forEach(function (v) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = v.label; b.setAttribute("aria-pressed", v === view);
    b.addEventListener("click", function () {
      if (v === view) return; view = v;
      Array.prototype.forEach.call(box.children, function (o) { o.setAttribute("aria-pressed", o === b); });
      q.classList.add("out"); setTimeout(function () { q.textContent = v.q; q.classList.remove("out"); }, reduce ? 0 : 200);
      render(true);
    });
    box.appendChild(b);
  });
  q.textContent = view.q;
  document.documentElement.classList.add("mdl-js");
  render(false); select(null);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { render(false); });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { render(false); select(sel); }, 120); });
})();
