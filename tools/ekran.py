#!/usr/bin/env python3
"""Bir sayının sayfasını üç ekran genişliğinde açar; bölüm bölüm ekran görüntüsü alır ve ölçülebilir tasarım sorunlarını yazar.

Kullanım:
    python3 tools/ekran.py 2026-11-18 --out /tmp/dc/ekran

Önce `python3 build.py` çalıştırılmış olmalı. Sistemdeki Chrome (/usr/bin/google-chrome), yoksa Playwright'ın kurulu Chromium'u
(PLAYWRIGHT_BROWSERS_PATH, ör. /opt/pw-browsers) kullanılır; Playwright yoksa betik kendisi kurar
(yalnızca Python paketi, ~10 sn; tarayıcı indirmez). Araç eksikse “ARAÇ YOK” satırı yazar ve 2 ile çıkar.
Çıktı: <out>/<genişlik>-<bölüm>.png dosyaları ve her genişlik için bir satır:
    telefon  hata yok            ya da
    telefon  TAŞMA 24px: pre.code (sec-atolye) · JS: ... · KESİK: .nm "..."
Görüntülere bakmak incelemenin işidir; bu betik yalnızca ölçülebilir olanı bulur: yatay taşma, taşan öğe, JavaScript hatası,
kırık iç bağlantı, yüklenemeyen dosya, satır sonunda bölünen kısa kod ya da kimlik (BÖLÜNEN), sayfa sonunda yanlış etkin
sekme (SEKME), son sayıda kadranın “Sonraki” adımı (KADRAN) ve telefonda katlama (KATLAMA: gizlenen kısım 4 satırdan kısa,
“Devamı” düğmesi “Neden önemli”/tablo/grafikten önce, düğme metni açmıyor). Telefonda katlamanın özeti ayrıca bir bilgi satırıdır.
"""
import argparse
import asyncio
import glob
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EKRANLAR = (("telefon", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
            ("tablet", dict(viewport={"width": 820, "height": 1180}, device_scale_factor=1)),
            ("masaustu", dict(viewport={"width": 1440, "height": 900}, device_scale_factor=1)))

OLC = r"""() => {
  const W = document.documentElement.clientWidth, out = {tasma: document.documentElement.scrollWidth - W, ogeler: [], kirik: []};
  const sec = el => (el.closest('section[id]') || {}).id || '';
  // Yatay kaydırılan şeritlerin (ör. eski sayılardaki rakam şeridi) içindeki öğeler ekran dışında olabilir; sorun değildir
  const kaydirmali = el => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
    const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll') return true; } return false; };
  for (const el of document.querySelectorAll('main *')) {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.left < -1) && !el.closest('pre') && !el.closest('.nav-links') && getComputedStyle(el).position !== 'fixed' && !kaydirmali(el))
      out.ogeler.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ' (' + sec(el) + ')');
  }
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    if (id && !document.getElementById(id)) out.kirik.push(a.getAttribute('href'));
  }
  out.ogeler = [...new Set(out.ogeler)].slice(0, 8);
  return out;
}"""

# Satır sonunda bölünmemesi gereken kısa kod ve kimlikler (code.nb, .nw): birden çok satır kutusu varsa bölünmüştür
BOLUNEN = r"""() => [...document.querySelectorAll('main code.nb, main .nw')]
  .filter(e => e.offsetParent && new Set([...e.getClientRects()].map(r => Math.round(r.top / 4))).size > 1)
  .map(e => '“' + e.textContent.trim().slice(0, 40) + '” (' + ((e.closest('section[id]') || {}).id || '') + ')').slice(0, 6)"""

# Telefonda katlama: her katlı haber açılıp kapatılır; görünen ve gizlenen kısım satır olarak ölçülür
KATLAMA = r"""async () => {
  const sonuc = {katli: 0, gorunen: [], gizlenen: [], sorun: []};
  const ad = a => a.id || ((a.querySelector('h2,h3') || {}).textContent || '').slice(0, 30);
  for (const art of [...document.querySelectorAll('article.clamp')]) {
    const body = art.querySelector('.body') || art, b = art.querySelector(':scope > .more, .more');
    if (!b) { sonuc.sorun.push('düğmesiz katlı haber: ' + ad(art)); continue; }
    const lh = parseFloat(getComputedStyle(body.querySelector('p') || body).lineHeight) || 24;
    const h1 = art.getBoundingClientRect().height;
    b.click(); await new Promise(r => setTimeout(r, 60));
    const h2 = art.getBoundingClientRect().height, acik = !art.classList.contains('clamp');
    b.click(); await new Promise(r => setTimeout(r, 30));
    sonuc.katli++;
    if (!acik || h2 <= h1) { sonuc.sorun.push('“Devamı” açmıyor: ' + ad(art)); continue; }
    const gor = Math.round(body.getBoundingClientRect().height / lh), giz = Math.round((h2 - h1) / lh);
    sonuc.gorunen.push(gor); sonuc.gizlenen.push(giz);
    if (giz < 4) sonuc.sorun.push(ad(art) + ' yalnızca ' + giz + ' satır gizliyor');
    for (let n = b.nextElementSibling; n; n = n.nextElementSibling)
      if (n.matches('.why, figure, .chart')) { sonuc.sorun.push('“Devamı” ' + n.className.split(' ')[0] + ' öncesinde: ' + ad(art)); break; }
  }
  return sonuc;
}"""

SEKME = r"""async () => {
  window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'}); await new Promise(r => setTimeout(r, 500));
  const l = [...document.querySelectorAll('nav.index a[href^="#"]')], son = l[l.length - 1];
  const on = document.querySelector('nav.index a[aria-current]');
  window.scrollTo({top: 0, behavior: 'instant'}); await new Promise(r => setTimeout(r, 200));
  return son && on !== son ? (on ? on.getAttribute('href') : 'hiçbiri') + ' etkin, beklenen ' + son.getAttribute('href') : '';
}"""

KADRAN = r"""(enSon) => {
  const off = document.querySelector('.dial-step.off'), sonraki = document.querySelector('a.dial-step[rel="next"]');
  if (enSon) {
    if (!off) return 'son sayıda soluk “Sonraki” adımı yok';
    const s = getComputedStyle(off);
    if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) return '“Sonraki” adımı gizli; kadranda boşluk kalır';
    if (+s.opacity > .6) return '“Sonraki” adımı soluk değil, tıklanabilir sanılır';
  } else if (!sonraki) return 'eski sayıda “Sonraki sayı” bağlantısı yok';
  return '';
}"""


def playwright_hazirla():
    """Playwright yoksa bir kez kurar (yaklaşık 10 sn; tarayıcı indirmez, sistemdeki Chrome kullanılır)."""
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        pass
    print("Playwright kuruluyor (pip, ~10 sn)…", file=sys.stderr)
    r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "playwright"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        print("ARAÇ YOK: playwright kurulamadı: " + r.stderr.strip()[-200:])
        return False
    return True


async def main(a):
    from playwright.async_api import async_playwright
    os.makedirs(a.out, exist_ok=True)
    port = 8800 + os.getpid() % 150
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    sorun_var = False
    try:
        en_son = json.load(open(os.path.join(ROOT, "issues", "index.json"), encoding="utf-8"))
        en_son = (en_son[0] if isinstance(en_son, list) else en_son["issues"][0])["date"] == a.tarih
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        en_son = False
    try:
        async with async_playwright() as p:
            kw = {"executable_path": a.chrome} if a.chrome else {}   # yoksa Playwright'ın kendi Chromium'u (PLAYWRIGHT_BROWSERS_PATH)
            b = await p.chromium.launch(args=["--no-sandbox"], **kw)
            for ad, kw in EKRANLAR:
                ctx = await b.new_context(**kw)
                pg = await ctx.new_page()
                js, yok = [], []
                pg.on("pageerror", lambda e: js.append(str(e)[:120]))
                pg.on("response", lambda r: yok.append(r.url.split(str(port))[-1]) if r.status >= 400 else None)
                await pg.goto(f"http://localhost:{port}/sayi/{a.tarih}.html", wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(600)
                katlama = await pg.evaluate(KATLAMA) if ad == "telefon" else None
                sekme = await pg.evaluate(SEKME)
                kadran = await pg.evaluate(KADRAN, en_son)
                # Telefonda katlanan metinler de görünsün diye “Devamı” açılır
                await pg.evaluate("document.querySelectorAll('.rest').forEach(e => e.classList.remove('rest'))")
                o = await pg.evaluate(OLC)
                bolunen = await pg.evaluate(BOLUNEN)
                # Görüntü yalnızca günden güne değişen bölümlerden alınır (başlık ve Benchmark bandı sabit bileşen)
                secs = ["section.lead", "section.cal-list"] + [f"#{i}" for i in await pg.evaluate(
                    "[...document.querySelectorAll('main section.sec[id]')].map(s => s.id)") if i != "sec-benchmark"]
                for sel in secs:
                    el = await pg.query_selector(sel)
                    if el and await el.is_visible():
                        isim = sel.replace("#", "").replace("section.", "").replace("header.", "")
                        await el.screenshot(path=os.path.join(a.out, f"{ad}-{isim}.png"))
                parca = []
                if o["tasma"] > 0:
                    parca.append(f"TAŞMA {o['tasma']}px: " + ", ".join(o["ogeler"]))
                elif o["ogeler"]:
                    parca.append("EKRAN DIŞI ÖĞE: " + ", ".join(o["ogeler"]))
                if js:
                    parca.append("JS: " + " | ".join(js[:3]))
                if yok:
                    parca.append("YÜKLENEMEDİ: " + ", ".join(sorted(set(yok))[:5]))
                if o["kirik"]:
                    parca.append("KIRIK İÇ BAĞLANTI: " + ", ".join(o["kirik"][:5]))
                if bolunen:
                    parca.append("BÖLÜNEN: " + ", ".join(bolunen))
                if sekme:
                    parca.append("SEKME: sayfa sonunda " + sekme)
                if kadran:
                    parca.append("KADRAN: " + kadran)
                if katlama and katlama["sorun"]:
                    parca.append("KATLAMA: " + "; ".join(katlama["sorun"][:5]))
                sorun_var |= bool(parca)
                print(f"{ad:9} " + (" · ".join(parca) if parca else "hata yok"))
                if katlama and katlama["gorunen"]:
                    g, z = katlama["gorunen"], katlama["gizlenen"]
                    print(f"{'':9} bilgi · katlama: {katlama['katli']} haber katlı; görünen {min(g)}–{max(g)} satır, gizlenen {min(z)}–{max(z)} satır")
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
    print(f"görüntüler: {a.out}")
    return 1 if sorun_var else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tarih")
    ap.add_argument("--out", default="/tmp/dc/ekran")
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    args = ap.parse_args()
    if not playwright_hazirla():
        sys.exit(2)
    if args.chrome and not os.path.exists(args.chrome):
        args.chrome = None
    if not args.chrome and not (glob.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium*"))
                                or glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium*"))):
        print("ARAÇ YOK: Chrome bulunamadı (/usr/bin/google-chrome yok, Playwright Chromium'u da yok); tasarım incelemesi ekran görüntüsü olmadan yapılamaz")
        sys.exit(2)
    sys.exit(asyncio.run(main(args)))
