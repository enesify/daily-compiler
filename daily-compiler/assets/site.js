// The Daily Compiler · küçük etkileşimler: kadran kaydırma/klavye, iç atıf vurgusu
(function () {
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
