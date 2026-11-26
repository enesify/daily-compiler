#!/usr/bin/env python3
"""Sabah görevinin bulgu kaydını (data/inceleme/YYYY-MM-DD.json) denetler, bildirim satırını üretir ve kayıtları özetler.

Kullanım:
    python3 tools/inceleme.py data/inceleme/2026-11-18.json   kaydı denetler, bildirim satırını yazar (sorun varsa çıkış kodu 1)
    python3 tools/inceleme.py --ozet 14                       son 14 günün kayıtlarını özetler (haftalık kural analizi için)
    python3 tools/inceleme.py --acik                          açık kod bulgularını listeler
    python3 tools/inceleme.py --kacan 14                      günlük editörlerin kaçırdığı sorunları özetler (kacan.json)

Kod bulgusu (kok “kod”, durum “oneri”): sabah oturumu kodu değiştiremediği için kayıtta kalır. Düzelten oturum bulguya
"kapandi": "YYYY-MM-DD · <commit ya da kısa not>" alanını ekler; o zamana dek bulgu açık sayılır ve bildirim satırında görünür.

Kayıt biçimi ve alanların anlamı: kurallar/GOREV.md, “Bulgu kaydı” bölümü.
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
KATEGORI = ("dogruluk", "kaynak", "eksik-bilgi", "etiket", "secim", "dil", "terim", "editoryal", "atolye", "tasarim", "teknik")
ONEM = ("kritik", "onemli", "kucuk")
DURUM = ("duzeltildi", "duzeltme-listesinde", "oneri", "birakildi", "reddedildi")
KOK = ("yok", "denetlenebilir", "belirsiz", "uygulanmadi", "eksik", "kod")
PUAN = ("icerik", "dogruluk", "dil", "tasarim")


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
        if k == "tasarim" and v is None:   # ekran aracı çalışmadıysa tasarım editörü çalışmaz
            continue
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            s.append(f"puan.{k} 0-10 arası sayı olmalı")
    if d.get("dogrulanan") is not None and not isinstance(d.get("dogrulanan"), int):
        s.append("dogrulanan tam sayı olmalı")
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
        if b.get("onem") == "kritik" and b.get("kategori") in ("dogruluk", "kaynak") and b.get("durum") not in ("duzeltildi", "reddedildi", "duzeltme-listesinde"):
            s.append(f"{w}: kritik doğruluk bulgusu yalnızca düzeltilir ya da kaynağa bakılarak reddedilir")
        if b.get("id") in ids:
            s.append(f"{w}: id tekrar ediyor")
        ids.add(b.get("id"))
    return s


def acik_kod():
    """Bütün kayıtlarda kapanmamış kod bulguları: [(tarih, bulgu)]."""
    out = []
    for f in sorted(glob.glob(os.path.join(DIR, "2*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for b in d.get("bulgular") or []:
            if b.get("kok") == "kod" and b.get("durum") == "oneri" and not b.get("kapandi"):
                out.append((d.get("tarih"), b))
    return out


def satir(d):
    bs = d.get("bulgular") or []
    o = Counter(b.get("onem") for b in bs)
    st = Counter(b.get("durum") for b in bs)
    kural = sum(1 for b in bs if b.get("kok") not in (None, "yok"))
    p = d.get("puan") or {}
    vs = [p[k] for k in PUAN if isinstance(p.get(k), (int, float))]
    ort = sum(vs) / len(vs) if vs else 0
    dg = f"{d['dogrulanan']} haber doğrulandı · " if isinstance(d.get("dogrulanan"), int) else ""
    return (f"Editörler: taslak {ort:.1f}/10 (içerik {p.get('icerik')}, doğruluk {p.get('dogruluk')}, "
            f"dil {p.get('dil')}, tasarım {p.get('tasarim') if p.get('tasarim') is not None else '–'}) · {dg}"
            f"{o['kritik']} kritik, {o['onemli']} önemli, {o['kucuk']} küçük bulgu · "
            f"{st['duzeltildi'] + st['duzeltme-listesinde']} düzeltildi, {st['reddedildi']} reddedildi, {st['oneri']} öneri · {kural} kural sinyali"
            f"{f' · {n} açık kod bulgusu' if (n := len(acik_kod())) else ''}")


def ozet(gun):
    son = dt.date.today() - dt.timedelta(days=gun)
    kay = []
    for f in sorted(glob.glob(os.path.join(DIR, "2*.json"))):
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
    print("\nPuanlar (içerik / doğruluk / dil / tasarım):")
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


KACAN = os.path.join(DIR, "kacan.json")
NEDEN = ("kural-yok", "ekran-yok", "olcum-yok", "dikkat", "kapsam-disi")
BULAN = ("kullanici", "harici", "haftalik")


def kacan(gun):
    """Günlük editörlerin kaçırdığı sorunlar: neden ve kategoriye göre sayılar, son kayıtlar."""
    try:
        lst = json.load(open(KACAN, encoding="utf-8"))["kayitlar"]
    except (OSError, ValueError, KeyError):
        print("kacan.json okunamadı")
        return 1
    hata = [f"{i}: {k}" for i, r in enumerate(lst) for k, izin in (("neden", NEDEN), ("bulan", BULAN))
            if r.get(k) not in izin]
    for h in hata:
        print("HATA  kacan.json " + h)
    son = dt.date.today() - dt.timedelta(days=gun)
    lst = [r for r in lst if dt.date.fromisoformat(r["tarih"]) > son]
    print(f"Son {gun} gün · {len(lst)} kaçan sorun")
    for alan in ("neden", "kategori", "bulan"):
        say = defaultdict(int)
        for r in lst:
            say[r.get(alan)] += 1
        print(f"  {alan:9} " + " · ".join(f"{k} {n}" for k, n in sorted(say.items(), key=lambda x: -x[1])))
    for r in lst[-8:]:
        print(f"  {r['tarih']} [{r['kategori']}/{r['neden']}] {r['sorun'][:110]}")
    return 1 if hata else 0


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--kacan":
        return kacan(int(sys.argv[2]))
    if sys.argv[1:] == ["--acik"]:
        lst = acik_kod()
        print(f"{len(lst)} açık kod bulgusu" + (":" if lst else ""))
        for t, b in lst:
            print(f"  {t} {b.get('id')} [{b.get('kategori')}] {b.get('konum')}: {str(b.get('sorun'))[:120]}")
        return 0
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
