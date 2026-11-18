#!/usr/bin/env python3
"""Günlük inceleme kaydını (data/inceleme/YYYY-MM-DD.json) denetler, bildirim satırını üretir ve kayıtları özetler.

Kullanım:
    python3 tools/inceleme.py data/inceleme/2026-11-18.json   kaydı denetler, bildirim satırını yazar (sorun varsa çıkış kodu 1)
    python3 tools/inceleme.py --ozet 14                       son 14 günün kayıtlarını özetler (haftalık kural analizi için)

Kayıt biçimi ve alanların anlamı: kurallar/INCELEME.md, “Kayıt” bölümü.
"""
import datetime as dt
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "data", "inceleme")
KATEGORI = ("dogruluk", "kaynak", "eksik-bilgi", "secim", "dil", "terim", "editoryal", "atolye", "tasarim", "teknik")
ONEM = ("kritik", "onemli", "kucuk")
DURUM = ("duzeltildi", "duzeltme-listesinde", "oneri", "birakildi")
KOK = ("yok", "denetlenebilir", "belirsiz", "uygulanmadi", "eksik", "kod")
PUAN = ("icerik", "dil", "tasarim")


def denetle(d, yol):
    s = []
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d.get("tarih", ""))):
        s.append("tarih YYYY-AA-GG biçiminde değil")
    elif os.path.basename(yol) != f"{d['tarih']}.json":
        s.append("dosya adı tarihle aynı olmalı")
    if not isinstance(d.get("sayi"), int):
        s.append("sayi (sayı numarası) tam sayı olmalı")
    p = d.get("puan") or {}
    for k in PUAN:
        v = p.get(k)
        if k == "tasarim" and v is None:   # ekran aracı çalışmadıysa
            continue
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            s.append(f"puan.{k} 0-10 arası sayı olmalı")
    ids = set()
    for i, b in enumerate(d.get("bulgular") or []):
        w = f"bulgular[{i}]"
        for f, izin in (("kategori", KATEGORI), ("onem", ONEM), ("durum", DURUM), ("kok", KOK)):
            if b.get(f) not in izin:
                s.append(f"{w}.{f} {b.get(f)!r}; şunlardan biri olmalı: {', '.join(izin)}")
        for f in ("konum", "sorun", "kanit"):
            if not str(b.get(f) or "").strip():
                s.append(f"{w}.{f} boş")
        if b.get("kok") not in (None, "yok") and not str(b.get("kural") or "").strip():
            s.append(f"{w}: kok '{b.get('kok')}' ise kural alanı (hangi kural ya da dosya, ne eksik) yazılmalı")
        if b.get("onem") == "kritik" and b.get("kategori") in ("dogruluk", "kaynak") and b.get("durum") not in ("duzeltildi", "duzeltme-listesinde"):
            s.append(f"{w}: kritik doğruluk bulgusu düzeltilmeden bırakılamaz")
        if b.get("id") in ids:
            s.append(f"{w}: id tekrar ediyor")
        ids.add(b.get("id"))
    return s


def satir(d):
    bs = d.get("bulgular") or []
    o = Counter(b.get("onem") for b in bs)
    st = Counter(b.get("durum") for b in bs)
    kural = sum(1 for b in bs if b.get("kok") not in (None, "yok"))
    p = d.get("puan") or {}
    vs = [p[k] for k in PUAN if isinstance(p.get(k), (int, float))]
    ort = sum(vs) / len(vs) if vs else 0
    return (f"İnceleme · Sayı {d.get('sayi')}: {ort:.1f}/10 (içerik {p.get('icerik')}, "
            f"dil {p.get('dil')}, tasarım {p.get('tasarim')}) · "
            f"{o['kritik']} kritik, {o['onemli']} önemli, {o['kucuk']} küçük bulgu · "
            f"{st['duzeltildi'] + st['duzeltme-listesinde']} düzeltildi, {st['oneri']} öneri · {kural} kural sinyali")


def ozet(gun):
    son = dt.date.today() - dt.timedelta(days=gun)
    kay = []
    for f in sorted(glob.glob(os.path.join(DIR, "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
            if dt.date.fromisoformat(d["tarih"]) > son:
                kay.append(d)
        except (ValueError, KeyError, OSError):
            print(f"UYARI: {os.path.basename(f)} okunamadı", file=sys.stderr)
    if not kay:
        print(f"Son {gun} günde inceleme kaydı yok.")
        return
    print(f"Son {gun} gün · {len(kay)} kayıt ({kay[0]['tarih']} – {kay[-1]['tarih']})")
    print("\nPuanlar (içerik / dil / tasarım):")
    for d in kay:
        p = d.get("puan") or {}
        print(f"  {d['tarih']}  " + " / ".join(str(p.get(k, '?')) for k in PUAN))
    gr = defaultdict(list)
    for d in kay:
        for b in d.get("bulgular") or []:
            gr[(b.get("kategori"), b.get("kok"))].append((d["tarih"], b))
    print("\nKategori × kök neden (sayı adedi · bulgu adedi):")
    for (kat, kok), lst in sorted(gr.items(), key=lambda x: (-len({t for t, _ in x[1]}), -len(x[1]))):
        gunler = sorted({t for t, _ in lst})
        isaret = "  ← tekrar ediyor" if kok != "yok" and len(gunler) >= 3 else ""
        print(f"  {kat:12} {kok:14} {len(gunler)} sayı · {len(lst)} bulgu{isaret}")
        if kok != "yok":
            for t, b in lst[:4]:
                print(f"      {t} {b.get('konum')}: {str(b.get('sorun'))[:110]}  [kural: {str(b.get('kural') or '')[:60]}]")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--ozet":
        ozet(int(sys.argv[2]))
        return 0
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    yol = sys.argv[1]
    d = json.load(open(yol, encoding="utf-8"))
    s = denetle(d, yol)
    print(satir(d))
    for x in s:
        print("HATA: " + x, file=sys.stderr)
    return 1 if s else 0


if __name__ == "__main__":
    sys.exit(main())
