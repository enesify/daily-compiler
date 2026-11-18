#!/usr/bin/env python3
"""Bir sayının sayfasını üç ekran genişliğinde açar; bölüm bölüm ekran görüntüsü alır ve ölçülebilir tasarım sorunlarını yazar.

Kullanım:
    python3 tools/ekran.py 2026-11-18 --out /tmp/inc/ekran

Önce `python3 build.py` çalıştırılmış olmalı. Sistemdeki Chrome kullanılır (/usr/bin/google-chrome); Playwright yoksa betik kendisi kurar
(yalnızca Python paketi, ~10 sn; tarayıcı indirmez). Araç eksikse “ARAÇ YOK” satırı yazar ve 2 ile çıkar.
Çıktı: <out>/<genişlik>-<bölüm>.png dosyaları ve her genişlik için bir satır:
    telefon  hata yok            ya da
    telefon  TAŞMA 24px: pre.code (sec-atolye) · JS: ... · KESİK: .nm "..."
Görüntülere bakmak incelemenin işidir; bu betik yalnızca ölçülebilir olanı bulur (yatay taşma, taşan öğe, JavaScript hatası,
kırık iç bağlantı, yüklenemeyen dosya).
"""
import argparse
import asyncio
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
  for (const el of document.querySelectorAll('main *')) {
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.left < -1) && !el.closest('pre') && !el.closest('.nav-links') && getComputedStyle(el).position !== 'fixed')
      out.ogeler.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ' (' + sec(el) + ')');
  }
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    if (id && !document.getElementById(id)) out.kirik.push(a.getAttribute('href'));
  }
  out.ogeler = [...new Set(out.ogeler)].slice(0, 8);
  return out;
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
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=a.chrome, args=["--no-sandbox"])
            for ad, kw in EKRANLAR:
                ctx = await b.new_context(**kw)
                pg = await ctx.new_page()
                js, yok = [], []
                pg.on("pageerror", lambda e: js.append(str(e)[:120]))
                pg.on("response", lambda r: yok.append(r.url.split(str(port))[-1]) if r.status >= 400 else None)
                await pg.goto(f"http://localhost:{port}/sayi/{a.tarih}.html", wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                await pg.wait_for_timeout(600)
                # Telefonda katlanan metinler de görünsün diye “Devamı” açılır
                await pg.evaluate("document.querySelectorAll('.rest').forEach(e => e.classList.remove('rest'))")
                o = await pg.evaluate(OLC)
                # Görüntü yalnızca telefon ve masaüstü için, yalnızca günden güne değişen bölümlerden alınır
                # (başlık ve Benchmark bandı sabit bileşen); tablet yalnızca ölçülür.
                secs = [] if ad == "tablet" else ["section.lead", "section.cal-list"] + [f"#{i}" for i in await pg.evaluate(
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
                sorun_var |= bool(parca)
                print(f"{ad:9} " + (" · ".join(parca) if parca else "hata yok"))
                await ctx.close()
            await b.close()
    finally:
        srv.terminate()
    print(f"görüntüler: {a.out}")
    return 1 if sorun_var else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("tarih")
    ap.add_argument("--out", default="/tmp/inc/ekran")
    ap.add_argument("--chrome", default="/usr/bin/google-chrome")
    args = ap.parse_args()
    if not os.path.exists(args.chrome):
        print(f"ARAÇ YOK: Chrome bulunamadı ({args.chrome}); tasarım incelemesi ekran görüntüsü olmadan yapılamaz")
        sys.exit(2)
    if not playwright_hazirla():
        sys.exit(2)
    sys.exit(asyncio.run(main(args)))
