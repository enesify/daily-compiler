// The Daily Compiler · Modeller sayfası: tek grafik, birkaç görünüm. Veri sayfaya gömülü JSON'dan (data/modeller.json) gelir.
// Grafik yalnızca ölçümü gösterir: yorum, çizgi ya da not yoktur.
// Bir ekseni ortak iki görünüm arasında noktalar yeni yerine kayar; ortak eksen yoksa grafik kısa bir solmayla değişir.
(function () {
  "use strict";
  var svg = document.getElementById("mdl-chart"), src = document.getElementById("mdl-veri");
  if (!svg || !src) return;
  var DATA; try { DATA = JSON.parse(src.textContent); } catch (e) { return; }
  var M = DATA.models, MET = DATA.metrics, VIEWS = DATA.views;
  var NS = "http://www.w3.org/2000/svg", $ = function (id) { return document.getElementById(id); };
  var el = function (t, a, par) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); if (par) par.appendChild(e); return e; };
  var tr = function (v, d) { return v.toFixed(d).replace(".", ","); };
  var FMT = {
    puan: { v: function (v) { return String(Math.round(v)); }, t: function (v) { return String(v); } },
    yuzde: { v: function (v) { return "%" + tr(v, 1); }, t: function (v) { return "%" + v; } },
    usd: { v: function (v) { return "$" + tr(v, 2); }, t: function (v) { return "$" + (v < 1 ? tr(v, 2) : v); } },
    dk: { v: function (v) { return tr(v, 1) + " dk"; }, t: function (v) { return String(v); } }
  };
  var fv = function (k, v) { return FMT[MET[k].bicim].v(v); }, ft = function (k, v) { return FMT[MET[k].bicim].t(v); };
  // eksen aralığı ve çentikler veriden hesaplanır (build.py m_scale ile aynı kural)
  Object.keys(MET).forEach(function (k) {
    var vs = M.map(function (m) { return m[k]; }).filter(function (v) { return v != null; }), lo = Math.min.apply(0, vs), hi = Math.max.apply(0, vs), t = [];
    if (MET[k].log) {
      var seq = []; for (var e = -3; e <= 6; e++) [1, 2, 5].forEach(function (s) { seq.push(+(s * Math.pow(10, e)).toPrecision(1)); });
      var a = seq.filter(function (s) { return s <= lo; }).pop(), b = seq.filter(function (s) { return s >= hi; })[0];
      t = seq.filter(function (s) { return s >= a && s <= b; }); MET[k].dom = [a, b];
    } else {
      var pad = (hi - (MET[k].sifir ? 0 : lo) || 1) * .06; lo = MET[k].sifir ? 0 : lo - pad; hi += pad;
      var raw = (hi - lo) / 5, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), step = [1, 2, 5, 10].filter(function (s) { return s * mag >= raw; })[0] * mag;
      var a2 = Math.floor(lo / step) * step, b2 = Math.ceil(hi / step) * step;
      for (var x = a2; x <= b2 + step / 1e6; x += step) t.push(+x.toPrecision(6)); MET[k].dom = [a2, b2];
    }
    MET[k].ticks = t;
  });
  // sağlayıcı renkleri: sitenin vurgu rengi (turkuaz) veriye verilmez
  var PAL = ["--l2", "--l3", "--l4", "--l7", "--l5", "--l6"];
  var provs = []; M.forEach(function (m) { if (provs.indexOf(m.saglayici) < 0) provs.push(m.saglayici); });
  var col = function (m) { return "var(" + PAL[Math.min(PAL.length - 1, provs.indexOf(m.saglayici))] + ")"; };
  var gAxis = $("mdl-axis"), gData = $("mdl-data"), missEl = $("mdl-miss"), srcEl = $("mdl-src");
  var legend = document.querySelectorAll("#mdl > .mdl-legend li[data-p]");
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion:reduce)").matches;
  var view = VIEWS[0], sel = null, G = {}, raf = 0, timers = [];
  var cvs = document.createElement("canvas").getContext("2d");

  var D = M.map(function (m, i) {
    var g = el("g", { "class": "dot", tabindex: 0, role: "button", "aria-label": m.ad }, $("mdl-dots"));
    el("circle", { r: 20, fill: "transparent" }, g);
    var ring = el("circle", { "class": "ring" }, g);
    var c = el(m.acik ? "path" : "circle", { "class": "c", fill: col(m) }, g);
    var t = el("text", { "class": "nm" }, $("mdl-labels"));
    el("tspan", {}, t).textContent = m.kisa || m.ad;
    var tv = el("tspan", { "class": "v", dx: 7 }, t);
    var d = { m: m, i: i, g: g, c: c, ring: ring, t: t, tv: tv, cur: null, from: null, to: null };
    var pick = function () { select(sel === d ? null : d); };
    g.addEventListener("click", pick);
    g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } });
    g.addEventListener("mouseenter", function () { if (!G.small) select(d); });
    return d;
  });
  svg.addEventListener("mouseleave", function () { if (!G.small) select(null); });

  function geom() {
    var W = svg.clientWidth || svg.parentNode.clientWidth, small = W < 600, H = small ? 420 : 500;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.style.height = H + "px";
    G = { W: W, H: H, small: small, L: small ? 40 : 54, R: small ? 12 : 22, T: small ? 22 : 26, axB: small ? 44 : 50,
          r: small ? 7 : 9, nf: small ? 12 : 14.5, fs: small ? 10.5 : 12.5 };
    G.pb = H - G.axB;
  }
  function sc(k, v, a, b) { var d = MET[k].dom; return MET[k].log ? a + (Math.log(v) - Math.log(d[0])) / (Math.log(d[1]) - Math.log(d[0])) * (b - a) : a + (v - d[0]) / (d[1] - d[0]) * (b - a); }
  function tw(s, size, mono) { cvs.font = (mono ? "400 " : "600 ") + size + "px " + (mono ? '"IBM Plex Mono",monospace' : '"IBM Plex Sans Condensed",Arial,sans-serif'); return cvs.measureText(s).width; }
  function ranked(k) { var s = MET[k].iyi === "dusuk" ? 1 : -1; return M.filter(function (m) { return m[k] != null; }).sort(function (a, b) { return s * (a[k] - b[k]); }); }
  function keys(v) { return v.rank ? [v.rank] : [v.x, v.y]; }
  function has(m, v) { return keys(v).every(function (k) { return m[k] != null; }); }

  function targets() {
    var order = view.rank ? ranked(view.rank) : null, rowH = (G.pb - G.T) / M.length;
    D.forEach(function (d) {
      var m = d.m, t = { op: 1, lab: 1, val: "" }, prev = d.cur;
      if (!has(m, view)) {   // ölçüm yok: nokta olduğu yerde söner, adı grafiğin altındaki satırda yazar
        t.op = 0; t.lab = 0; t.x = prev ? prev.x : G.L; t.y = prev ? prev.y : G.pb;
      } else if (view.rank) {
        t.x = sc(view.rank, m[view.rank], G.L, G.W - G.R - (G.small ? 112 : 190)); t.y = G.T + (order.indexOf(m) + .5) * rowH; t.val = fv(view.rank, m[view.rank]);
      } else {
        t.x = sc(view.x, m[view.x], G.L, G.W - G.R); t.y = sc(view.y, m[view.y], G.pb, G.T);
      }
      d.to = t;
    });
    placeLabels();
  }
  // etiket: önce sağ, sonra sol, üst, alt; hiçbiri boş değilse etiket basılmaz (adı dokununca ya da üzerine gelince görünür)
  function placeLabels() {
    var r = G.r, nf = G.nf, boxes = [];
    D.forEach(function (d) { if (d.to.op) boxes.push([d.to.x - r - 2, d.to.y - r - 2, 2 * r + 4, 2 * r + 4, d]); });
    D.slice().sort(function (a, b) { return a.to.y - b.to.y; }).forEach(function (d) {
      var t = d.to; t.lx = t.x; t.ly = t.y;
      if (!t.op) return;
      var w = tw(d.m.kisa || d.m.ad, nf) + (t.val ? 7 + tw(t.val, nf * .88, true) : 0), h = nf * 1.15, x = t.x, y = t.y;
      var o = r + 10;   // seçim halkası (r + 5) etiketin üstüne binmesin
      var c = view.rank ? [[x + o, y + nf * .36]] :
        [[x + o, y + nf * .36], [x - o - w, y + nf * .36], [x - w / 2, y - o], [x - w / 2, y + o + nf - 2],
         [x + r + 3, y - r - 3], [x - r - 3 - w, y - r - 3], [x + r + 3, y + r + nf], [x - r - 3 - w, y + r + nf]];
      var best = c[0], bestP = 1e9;
      c.forEach(function (p, ci) {
        var bx = [p[0] - 2, p[1] - nf, w + 4, h], pen = ci * .1;
        if (bx[0] < G.L + 2 || bx[0] + bx[2] > G.W - 2 || bx[1] < 2 || bx[1] + bx[3] > G.pb - 2) pen += 50;
        boxes.forEach(function (b) { if (b[4] !== d && bx[0] < b[0] + b[2] && bx[0] + bx[2] > b[0] && bx[1] < b[1] + b[3] && bx[1] + bx[3] > b[1]) pen += 10; });
        if (pen < bestP) { bestP = pen; best = p; }
      });
      t.lx = best[0]; t.ly = best[1];
      if (bestP >= 10) t.lab = 0; else boxes.push([t.lx - 2, t.ly - nf, w + 4, h, d]);
    });
  }
  function paint(d) {
    var s = d.cur;
    d.g.setAttribute("transform", "translate(" + s.x.toFixed(1) + "," + s.y.toFixed(1) + ")");
    d.g.style.opacity = s.op.toFixed(2); d.g.style.pointerEvents = s.op > .5 ? "" : "none";
    d.t.setAttribute("x", s.lx.toFixed(1)); d.t.setAttribute("y", s.ly.toFixed(1));
    d.t.style.opacity = (sel === d && s.op > .5 ? 1 : s.lab * s.op).toFixed(2);
  }
  function styleDots() {
    D.forEach(function (d) {
      var r = G.r, q = r * 1.22;
      if (d.m.acik) d.c.setAttribute("d", "M0 " + -q + "L" + q + " 0 0 " + q + " " + -q + " 0Z"); else d.c.setAttribute("r", r);
      d.ring.setAttribute("r", r + 5); d.t.setAttribute("font-size", G.nf);
      d.tv.textContent = d.to.val; d.tv.setAttribute("font-size", (G.nf * .88).toFixed(1));
    });
  }
  function axes() {
    gAxis.textContent = "";
    var L = G.L, R = G.W - G.R, T = G.T, pb = G.pb, fs = G.fs, ty = pb + fs + 9;
    var txt = function (x, y, s, cls, anc, size) { var e = el("text", { x: x, y: y, "class": cls, "text-anchor": anc || "start", "font-size": size || fs }, gAxis); e.textContent = s; };
    if (view.rank) {
      var k = view.rank, xr = R - (G.small ? 112 : 190), rowH = (pb - T) / M.length, list = ranked(k), pos = 0;
      MET[k].ticks.forEach(function (v) { var x = sc(k, v, L, xr); el("line", { x1: x, x2: x, y1: T, y2: pb, "class": "grid" }, gAxis); txt(x, ty, ft(k, v), "tick", "middle"); });
      list.forEach(function (m, i) {   // eşit puanlar aynı sırayı alır: 5, 5, 7
        if (!i || m[k] !== list[i - 1][k]) pos = i + 1;
        txt(L - 10, T + (i + .5) * rowH + fs * .36, String(pos), "tick", "end", fs + 1);
      });
      txt((L + xr) / 2, G.H - 6, MET[k].eksen, "axis", "middle", fs + .5);
    } else {
      MET[view.y].ticks.forEach(function (v) { var y = sc(view.y, v, pb, T); el("line", { x1: L, x2: R, y1: y, y2: y, "class": "grid" }, gAxis); txt(L - 7, y + fs * .36, ft(view.y, v), "tick", "end"); });
      MET[view.x].ticks.forEach(function (v) { var x = sc(view.x, v, L, R); el("line", { x1: x, x2: x, y1: T, y2: pb, "class": "grid" }, gAxis); txt(x, ty, ft(view.x, v), "tick", "middle"); });
      el("line", { x1: L, x2: R, y1: pb, y2: pb, "class": "base" }, gAxis);
      txt((L + R) / 2, G.H - 6, MET[view.x].eksen, "axis", "middle", fs + .5);
      txt(L, T - 9, "↑ " + MET[view.y].eksen, "axis", "start", fs + .5);
    }
    var groups = {}, order = [];
    M.forEach(function (m) {
      var k = (view.rank ? [view.rank] : [view.y, view.x]).filter(function (k) { return m[k] == null; })[0];
      if (!k) return;
      if (!groups[k]) { groups[k] = []; order.push(k); }
      groups[k].push(m.kisa || m.ad);
    });
    missEl.textContent = order.map(function (k) { return MET[k].ad + " ölçümü yok: " + groups[k].join(", "); }).join(" · ");
    srcEl.textContent = "Kaynak: ";
    var used = []; keys(view).forEach(function (k) { if (used.indexOf(MET[k].kaynak) < 0) used.push(MET[k].kaynak); });
    used.forEach(function (g, i) {
      if (i) srcEl.appendChild(document.createTextNode(", "));
      var a = document.createElement("a"); a.href = DATA.sources[g].url; a.target = "_blank"; a.rel = "noopener"; a.textContent = DATA.sources[g].name; srcEl.appendChild(a);
    });
    var d = DATA.updated.split("-"), AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
    srcEl.appendChild(document.createTextNode(" · " + (+d[2]) + " " + AY[+d[1] - 1] + " " + d[0]));
    Array.prototype.forEach.call(legend, function (li) {
      li.classList.toggle("off", !M.some(function (m) { return m.saglayici === li.getAttribute("data-p") && has(m, view); }));
    });
  }
  var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var copy = function (o) { var c = {}; for (var k in o) c[k] = o[k]; return c; };
  function still() { styleDots(); axes(); D.forEach(function (d) { d.cur = copy(d.to); paint(d); }); }
  function render(mode) {
    cancelAnimationFrame(raf); timers.forEach(clearTimeout); timers = [];
    gData.style.opacity = 1;
    geom(); targets();
    if (!mode || reduce || !D[0].cur) { still(); return; }
    if (mode === "fade") {   // ortak eksen yok: noktaların kayması yanlış bir ilişki anlatır
      gData.style.opacity = 0;
      timers.push(setTimeout(function () { still(); gData.style.opacity = 1; }, 160));
      return;
    }
    axes(); styleDots();   // eksenler hiç kaybolmaz: hedef görünümün eksenleri hemen çizilir
    D.forEach(function (d) { d.from = copy(d.cur); });
    var DUR = 600, STAG = 22, order = D.slice().sort(function (a, b) { return a.from.y - b.from.y; }), t0 = performance.now();
    var ks = ["x", "y", "lx", "ly", "lab", "op"];
    (function frame(now) {
      var done = true;
      order.forEach(function (d, i) {
        var t = Math.min(1, Math.max(0, (now - t0 - i * STAG) / DUR)), e = ease(t); if (t < 1) done = false;
        ks.forEach(function (k) { d.cur[k] = d.from[k] + (d.to[k] - d.from[k]) * e; }); paint(d);
      });
      if (!done) raf = requestAnimationFrame(frame); else D.forEach(function (d) { d.cur = copy(d.to); paint(d); });
    })(t0);
  }
  function select(d) {
    sel = d;
    D.forEach(function (o) { o.g.classList.toggle("sel", o === d); o.g.classList.toggle("dimmed", !!d && o !== d); if (o.cur) paint(o); });
    var r = $("mdl-read"); r.textContent = "";
    r.classList.toggle("hint", !d);
    if (!d) { if (G.small) r.textContent = "Ayrıntı için bir noktaya dokun."; return; }
    var m = d.m, add = function (tag, text, cls) { var e = document.createElement(tag); e.textContent = text; if (cls) e.className = cls; r.appendChild(e); return e; };
    add("b", m.ad);
    r.appendChild(document.createTextNode(" · " + m.saglayici + (m.ayar ? " · akıl yürütme ayarı: " + m.ayar : "") + (m.acik ? " · açık ağırlıklı" : "")));
    r.appendChild(document.createElement("br"));
    Object.keys(MET).forEach(function (k, i) {
      if (i) r.appendChild(document.createTextNode(" · "));
      var s = add("span", MET[k].ad + " ", "m"); var b = document.createElement("b"); b.textContent = m[k] == null ? "ölçüm yok" : fv(k, m[k]); s.appendChild(b);
    });
  }
  var box = $("mdl-views");
  VIEWS.forEach(function (v) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = v.label; b.setAttribute("aria-pressed", v === view);
    b.addEventListener("click", function () {
      if (v === view) return;
      var shared = !v.rank && !view.rank && (v.x === view.x || v.y === view.y);
      view = v;
      Array.prototype.forEach.call(box.children, function (o) { o.setAttribute("aria-pressed", o === b); });
      render(shared ? "slide" : "fade");
    });
    box.appendChild(b);
  });
  document.documentElement.classList.add("mdl-js");
  render(); select(null);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { render(); });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { render(); select(sel); }, 120); });
})();
