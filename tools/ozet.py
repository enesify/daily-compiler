#!/usr/bin/env python3
"""Yeni sayıya başlamadan önce gereken özet: tarih, sıradaki sayı numarası, son sayıların başlıkları ve açık uçlar.

Kullanım:
    python3 tools/ozet.py                 # özeti ekrana yazar
    python3 tools/ozet.py --out /tmp/dc   # ayrıca /tmp/dc/previous_headlines.txt dosyasını yazar (editör için)

Son sayıların tam metnini okumaya gerek bırakmaz; şema için kurallar/ornek.json'a bakılır.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
# Sonucu henüz belli olmayan konulara işaret eden ifadeler
OPEN = re.compile(r"henüz|bekleniyor|beklenen|planlan|başlayacak|yayımlanacak|açıklanmadı|açıklamadı|doğrulanmadı|"
                  r"tarih verilmedi|sürecek|itibaren|son tarih|preview|release candidate|\bRC\d?\b|canary", re.I)


def load():
    issues = []
    for path in sorted(glob.glob(os.path.join(ROOT, "issues", "*.json"))):
        if os.path.basename(path) == "index.json":
            continue
        with open(path, encoding="utf-8") as f:
            issues.append(json.load(f))
    return sorted(issues, key=lambda d: d["date"])


def anchors(issue):
    """(çapa, bölüm adı, kicker, başlık, paragraflar) listesi."""
    out = []
    L = issue.get("lead") or {}
    if L.get("headline"):
        out.append(("manset", "Manşet", L.get("kicker") or "", L["headline"], L.get("paragraphs") or []))
    for s in issue.get("sections") or []:
        for i, a in enumerate(s.get("articles") or []):
            aid = str(a.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}")
            out.append((aid, s.get("title") or "", a.get("kicker") or "", a.get("headline") or "", a.get("paragraphs") or []))
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ“`])", text) if s.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3, help="kaç önceki sayı özetlensin (varsayılan 3)")
    ap.add_argument("--out", help="previous_headlines.txt dosyasının yazılacağı klasör")
    args = ap.parse_args()

    now = datetime.datetime.now(ZoneInfo("Europe/Istanbul"))
    today = now.date().isoformat()
    issues = load()
    last = issues[-args.n:]
    lines = []
    p = lines.append

    p(f"BUGÜN: {today} · dateLabel: \"{DAYS[now.weekday()]}, {now.day} {MONTHS[now.month - 1]} {now.year}\"")
    window = "72 saat (Pazartesi)" if now.weekday() == 0 else "48 saat"
    p(f"ZAMAN PENCERESİ: {window}")
    if any(d["date"] == today for d in issues):
        p(f"!! issues/{today}.json ZATEN VAR: yeniden yazma, dur ve bildir.")
    p(f"SIRADAKİ number: {max((d.get('number') or 0) for d in issues) + 1 if issues else 1}")
    p("")

    head = []
    for d in reversed(last):
        head.append(f"== {d['date']} · Sayı {d.get('number')} ==")
        for aid, sec, kicker, title, _ in anchors(d):
            head.append(f"#{d['date']}-{aid} | {sec} | {kicker} | {title}")
        for b in d.get("briefs") or []:
            head.append(f"(kısa) {b.get('tag')}: {(b.get('text') or '')[:150]}")
        head.append("")
    if issues:
        L = issues[-1].get("lead") or {}
        p(f"ÖNCEKİ MANŞET (aynı şirket art arda manşet olmaz): {L.get('kicker')} | {L.get('headline')}")
    t0 = now.date()
    recent = []
    for d in issues:
        if 0 < (t0 - datetime.date.fromisoformat(d["date"])).days <= 7:
            recent += [r.get("name") for r in (d.get("repos") or {}).get("items") or []]
    if recent:
        p("SON 7 GÜNÜN REPOLARI (tekrar girmez): " + ", ".join(sorted(set(recent))))
    upcoming = {}
    for d in issues[-5:]:
        for c in d.get("calendar") or []:
            if str(c.get("date")) >= today:
                upcoming[(c.get("date"), c.get("text"))] = (d["date"], c.get("ref"), c.get("url"))
    if upcoming:
        p("ÖNCEKİ TAKVİMLERDE HÂLÂ GELECEKTE KALAN TARİHLER (önemini koruyorsa yeniden girebilir; ref yerine url gerekir):")
        for (cd, t), (src, r, u) in sorted(upcoming.items()):
            p(f"  {cd} | {t} | {u or f'#{src}-{r}'}")
    # Önceki sayıların metninde geçen ileri tarihler (Takvim adayı)
    AY = {"Ocak":1,"Şubat":2,"Mart":3,"Nisan":4,"Mayıs":5,"Haziran":6,"Temmuz":7,"Ağustos":8,"Eylül":9,"Ekim":10,"Kasım":11,"Aralık":12}
    rx = re.compile(r"\b(\d{1,2}) (" + "|".join(AY) + r")(?:'?\w*)?(?: (\d{4}))?")
    fut = {}
    for d in issues[-5:]:
        y0 = int(d["date"][:4])
        def walk(o, where):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k not in ("url", "sources"):
                        walk(v, where)
            elif isinstance(o, list):
                for v in o:
                    walk(v, where)
            elif isinstance(o, str):
                for m in rx.finditer(o):
                    try:
                        dt = datetime.date(int(m.group(3) or y0), AY[m.group(2)], int(m.group(1)))
                    except ValueError:
                        continue
                    if 0 < (dt - t0).days <= 30:
                        i = max(0, m.start() - 70)
                        fut.setdefault(dt, f"{d['date']}: …{o[i:m.end() + 50]}…")
        walk({k: v for k, v in d.items() if k in ("lead", "sections", "briefs")}, d["date"])
    if fut:
        p("ÖNCEKİ SAYILARIN METNİNDE GEÇEN İLERİ TARİHLER (Takvim'e alınmalı ya da neden alınmadığı bilinmeli):")
        for dt in sorted(fut):
            p(f"  {dt} | {fut[dt][:200]}")
    pr = []
    for d in last:
        for x in ((d.get("lead") or {}).get("box") or {}).get("items") or []:
            pr.append(f"  {d['date']}: {x[:140]}")
    if pr:
        p("SON SAYILARIN PRATİK ÇIKARIM MADDELERİ (tekrar edilmez):")
        lines.extend(pr)
    p("")
    p("SON SAYILARIN HABERLERİ (iç atıf adresi | bölüm | kicker | başlık):")
    lines.extend(head)

    p("OLASI AÇIK UÇLAR (anahtar kelimeye göre seçilmiş cümleler; hepsi açık uç değildir, kendin değerlendir):")
    for d in reversed(last):
        for aid, _, _, title, paras in anchors(d):
            for s in sentences(" ".join(paras)):
                if OPEN.search(s):
                    p(f"#{d['date']}-{aid} | {title[:50]} | {s[:260]}")
        for b in d.get("briefs") or []:
            if OPEN.search(b.get("text") or ""):
                p(f"{d['date']} (kısa) {b.get('tag')}: {(b.get('text') or '')[:260]}")

    print("\n".join(lines))
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, "previous_headlines.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(head) + "\n")
        print(f"\nYazıldı: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
