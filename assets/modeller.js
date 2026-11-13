// The Daily Compiler · Modeller sayfası: ölçüt sekmeleri ve sıralı liste. Veri sayfaya gömülü JSON'dan (data/modeller.json) gelir.
// Ölçüt değişince satırlar yeni sıralarına kayar, çubuklar ve rakamlar yeni değerlerine akar.
// Satıra dokununca o modelin bütün ölçümleri açılır. Yorum yok: yalnızca ölçüm, sıra ve kaynak.
(function () {
  "use strict";
  var list = document.getElementById("mdl-list"), src = document.getElementById("mdl-veri");
  if (!list || !src) return;
  var D; try { D = JSON.parse(src.textContent); } catch (e) { return; }
  var M = D.models, MET = D.metrics, KEYS = Object.keys(MET), TABS = D.sekmeler;
  var $ = function (id) { return document.getElementById(id); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion:reduce)").matches;
  var tr = function (v, d) { return v.toFixed(d).replace(".", ","); };
  var esc = function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;"); };
  var FMT = {   // build.py M_FMT ile aynı yazım
    puan: function (v) { return String(Math.round(v)); },
    yuzde: function (v) { return "%" + tr(v, 1); },
    usd: function (v) { return "$" + tr(v, 2); },
    dk: function (v) { return tr(v, 1) + " dk"; }
  };
  var f = function (k, v) { return FMT[MET[k].bicim](v); };
  var MAX = {};
  KEYS.forEach(function (k) { MAX[k] = Math.max.apply(0, M.map(function (m) { return m[k] || 0; })); });
  var pct = function (k, v) { return (v / MAX[k] * 100).toFixed(2) + "%"; };   // çubuklar sıfırdan başlar
  var AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
  var dp = D.updated.split("-"), DATE = (+dp[2]) + " " + AY[+dp[1] - 1] + " " + dp[0];
  function caption(k) {
    var s = D.sources[MET[k].kaynak], cap = $("mdl-cap");
    cap.textContent = MET[k].ad + ", " + (MET[k].iyi === "yuksek" ? "yüksekten düşüğe" : "düşükten yükseğe") + " · Kaynak: ";
    var a = document.createElement("a"); a.href = s.url; a.target = "_blank"; a.rel = "noopener"; a.textContent = s.name;
    cap.appendChild(a); cap.appendChild(document.createTextNode(" · " + DATE));
  }
  function tween(el, from, to, k, delay) {   // rakam yeni değerine akar
    if (reduce || from == null) { el.textContent = f(k, to); return; }
    var t0 = performance.now() + delay;
    (function step(now) {
      var t = Math.max(0, Math.min(1, (now - t0) / 550)), e = 1 - Math.pow(1 - t, 3);
      el.textContent = f(k, from + (to - from) * e);
      if (t < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  var key = TABS[0], open = null;
  var rows = M.map(function (m) {
    var r = document.createElement("div"); r.className = "mrow"; r.tabIndex = 0; r.setAttribute("role", "button"); r.setAttribute("aria-expanded", "false");
    r.innerHTML = '<span class="rk"></span><span class="nm">' + esc(m.ad) + "<small>" + esc(m.saglayici) + (m.ayar ? " · " + esc(m.ayar) : "") + (m.acik ? " · açık ağırlıklı" : "") +
      '</small></span><span class="mbar"><i></i></span><span class="val"></span>' +
      '<span class="chev" aria-hidden="true"><svg viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"/></svg></span><div class="det">' +
      KEYS.map(function (k) {
        var v = m[k];
        return '<div data-k="' + k + '"' + (v == null ? ' class="na"' : "") + ' title="' + esc(MET[k].ad) + '">' + esc(MET[k].detay) +
          '<span class="mb"><i style="width:' + (v == null ? 0 : pct(k, v)) + '"></i></span><b>' + (v == null ? "–" : f(k, v)) + "</b></div>";
      }).join("") + "</div>";
    var o = { m: m, el: r, val: r.querySelector(".val"), bar: r.querySelector(".mbar i"), rk: r.querySelector(".rk"), shown: null };
    var toggle = function () { open = open === o ? null : o; layout(false); };
    r.addEventListener("click", toggle);
    r.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
    list.appendChild(r);
    return o;
  });
  var tabs = $("mdl-tabs");
  TABS.forEach(function (k) {
    var b = document.createElement("button"); b.type = "button"; b.textContent = MET[k].sekme; b.setAttribute("data-k", k);
    b.addEventListener("click", function () { setKey(k, true); });
    tabs.appendChild(b);
  });
  tabs.addEventListener("keydown", function (e) {   // sekmeler arasında ok tuşlarıyla gezinme
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    var i = (TABS.indexOf(key) + (e.key === "ArrowRight" ? 1 : -1) + TABS.length) % TABS.length;
    setKey(TABS[i], true); tabs.children[i].focus(); e.preventDefault();
  });
  function setKey(k, fromUser, first) {
    if (TABS.indexOf(k) < 0) k = TABS[0];
    var changed = !first && k !== key; key = k;
    Array.prototype.forEach.call(tabs.children, function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-k") === k); });
    if (fromUser && location.hash !== "#" + k) { try { history.replaceState(null, "", "#" + k); } catch (e) { location.hash = k; } }
    layout(changed);
  }
  function layout(changed) {
    var k = key, up = MET[k].iyi === "yuksek";
    caption(k);
    var have = rows.filter(function (o) { return o.m[k] != null; });
    have.sort(function (a, b) { return up ? b.m[k] - a.m[k] : a.m[k] - b.m[k]; });
    var y = 0, pos = 0;
    have.forEach(function (o, i) {
      if (!i || o.m[k] !== have[i - 1].m[k]) pos = i + 1;   // eşit değerler aynı sırayı alır
      var delay = changed && !reduce ? i * 22 : 0;            // satırlar yukarıdan aşağı dalga halinde
      o.rk.textContent = pos;
      o.el.classList.remove("gone"); o.el.removeAttribute("aria-hidden"); o.el.tabIndex = 0;
      o.el.classList.toggle("open", open === o); o.el.setAttribute("aria-expanded", open === o);
      Array.prototype.forEach.call(o.el.querySelectorAll(".det div"), function (d) { d.classList.toggle("on", d.getAttribute("data-k") === k); });
      o.el.style.transitionDelay = delay + "ms"; o.bar.style.transitionDelay = delay + "ms";
      o.el.style.transform = "translateY(" + y + "px)";
      y += o.el.offsetHeight;
      o.bar.style.width = pct(k, o.m[k]);
      if (changed || o.shown == null) tween(o.val, o.shown, o.m[k], k, delay);
      o.shown = o.m[k];
    });
    rows.forEach(function (o) {   // bu ölçütte ölçümü olmayan model listede yer almaz; açıksa ölçümü olan ölçüte dönünce yine açık gelir
      if (have.indexOf(o) >= 0) return;
      o.el.classList.add("gone"); o.el.setAttribute("aria-hidden", "true"); o.el.tabIndex = -1;
      o.el.style.transitionDelay = "0ms"; o.el.style.transform = "translateY(" + y + "px)"; o.shown = null;
    });
    list.style.height = y + "px";
    if (changed && open && have.indexOf(open) >= 0) {   // açık satır ekrandan çıkıyorsa sayfa onu izler
      setTimeout(function () {
        var r = open.el.getBoundingClientRect(), top = tabs.parentNode.getBoundingClientRect().bottom + 8;
        if (r.top < top || r.bottom > innerHeight - 8) scrollBy({ top: r.top - top - 40, behavior: reduce ? "auto" : "smooth" });
      }, 620);
    }
  }

  $("mdl-static").hidden = true; list.hidden = false;
  setKey(location.hash.slice(1) || TABS[0], false, true);   // açılışta hareket yok
  addEventListener("hashchange", function () { setKey(location.hash.slice(1), false); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(false); });
  var rt; addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { layout(false); }, 120); });
})();
