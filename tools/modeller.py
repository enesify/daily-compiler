#!/usr/bin/env python3
"""data/modeller.json dosyasını denetler (Modeller sayfasının ve sayı içindeki bandın verisi).

Kullanım:
    python3 tools/modeller.py            biçimi ve kuralları denetler; HATA varsa çıkış kodu 1, yayımlanmaz
    python3 tools/modeller.py --yas 7    ayrıca veri 7 günden eskiyse "GÜNCELLE" yazar (çıkış kodunu etkilemez)

Kurallar ve güncelleme adımları: .claude/skills/modeller-guncelle/SKILL.md
Bu betik yalnızca biçimi denetler; rakamların kaynaktaki tabloyla aynı olduğunu güncellemeyi yapan oturum doğrular.
"""
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "modeller.json")
BICIM = {"puan", "yuzde", "usd", "dk"}
errors, warns = [], []
E, W = errors.append, warns.append


def main():
    try:
        D = json.load(open(PATH, encoding="utf-8"))
    except Exception as e:
        print(f"HATA: data/modeller.json okunamadı: {e}")
        return 1
    try:
        upd = dt.date.fromisoformat(D.get("updated", ""))
        if upd > dt.date.today() + dt.timedelta(days=1):
            E(f"updated ileri bir tarih: {upd}")
    except ValueError:
        upd = None
        E("updated alanı YYYY-AA-GG biçiminde değil")
    src = D.get("sources") or {}
    for k, s in src.items():
        if not (s.get("name") and re.match(r"^https://", s.get("url") or "")):
            E(f"sources.{k}: name ve https ile başlayan url gerekli")
    met = D.get("metrics") or {}
    if not met:
        E("metrics boş")
    for k, m in met.items():
        for f in ("ad", "detay", "bicim", "iyi", "kaynak"):
            if not m.get(f):
                E(f"metrics.{k}: {f} eksik")
        if m.get("bicim") not in BICIM:
            E(f"metrics.{k}: bicim {sorted(BICIM)} içinden olmalı")
        if m.get("iyi") not in ("yuksek", "dusuk"):
            E(f"metrics.{k}: iyi 'yuksek' ya da 'dusuk' olmalı (liste bu yöne göre sıralanır)")
        if m.get("kaynak") not in src:
            E(f"metrics.{k}: kaynak '{m.get('kaynak')}' sources içinde yok")
    tabs = D.get("sekmeler") or []
    if not tabs:
        E("sekmeler boş (ilki sayı içindeki bantta kullanılan ölçüttür)")
    for k in tabs:
        if k not in met:
            E(f"sekmeler: '{k}' metrics içinde yok")
        elif not met[k].get("sekme"):
            E(f"metrics.{k}: sekmede görünecek kısa ad (sekme) eksik")
    models = D.get("models") or []
    if not 8 <= len(models) <= 14:
        E(f"model sayısı {len(models)}; kural gereği 8–14 arası olmalı (ilk 10 + en iyi 2 açık model)")
    names = set()
    for i, m in enumerate(models):
        w = f"models[{i}] ({m.get('ad')})"
        for f in ("ad", "kisa", "saglayici"):
            if not m.get(f):
                E(f"{w}: {f} eksik")
        if m.get("ad") in names:
            E(f"{w}: aynı model iki kez var (her modelin tek ayarı gösterilir)")
        names.add(m.get("ad"))
        if not isinstance(m.get("acik"), bool):
            E(f"{w}: acik true ya da false olmalı")
        if not isinstance(m.get("ayar"), str):
            E(f"{w}: ayar metin olmalı (ayarı olmayan modelde boş metin)")
        if len(m.get("kisa") or "") > 22:
            W(f"{w}: kisa ad 22 karakteri geçiyor; telefonda etiket taşabilir")
        for k in met:
            if k not in m:
                E(f"{w}: '{k}' alanı yok (ölçüm yoksa null yazılır)")
            elif m[k] is not None and (isinstance(m[k], bool) or not isinstance(m[k], (int, float)) or m[k] <= 0):
                E(f"{w}: '{k}' pozitif sayı ya da null olmalı")
    if models and tabs and tabs[0] in met:
        n = sum(1 for m in models if m.get(tabs[0]) is not None)
        if n < 5:
            E(f"bandın ölçütü '{tabs[0]}' için yalnızca {n} modelin ölçümü var; en az 5 gerekli")

    for w in warns:
        print("UYARI:", w)
    for e in errors:
        print("HATA:", e)
    if "--yas" in sys.argv and upd:
        try:
            lim = int(sys.argv[sys.argv.index("--yas") + 1])
        except (IndexError, ValueError):
            lim = 7
        age = (dt.date.today() - upd).days
        print(f"GÜNCELLE: veri {age} günlük (sınır {lim})" if age > lim else f"veri {age} günlük; güncelleme gerekmiyor")
    print(f"modeller.json: {len(models)} model, {len(met)} ölçüt · {len(errors)} hata, {len(warns)} uyarı")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
