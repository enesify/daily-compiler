#!/usr/bin/env python3
"""Bütün sayılarda arar: başlık, kicker, deck, paragraflar, kısa haberler ve repo adları.

Kullanım:
  python3 tools/ara.py "Nvidia Huang"          # bütün kelimeler aynı haberde geçmeli
  python3 tools/ara.py "Shiro" --n 5           # en fazla 5 sonuç (varsayılan 10)

Çıktı en yeni sayıdan eskiye doğru: iç atıf adresi | kicker | başlık. Paragraf ya da kısa haberde
eşleştiyse eşleşen cümle de yazılır. İç atıf adresi kaynak listesinde aynen kullanılır
(`{"label": "13 Kasım sayısı: ...", "url": "#2026-11-13-is-1"}`).
"""
import argparse
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fold(t):
    return (t or "").replace("İ", "i").replace("I", "ı").lower().replace("’", "'")


def art_id(sec, i, a):
    return a.get("id") or f"{sec.get('id')}-{i + 1}"


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]


def items(d):
    """(çapa, kicker, başlık, metin) dörtlüleri. Kısa haberlerin ve repoların çapası yoktur (None): iç atıf sayıya verilir."""
    L = d.get("lead") or {}
    if L.get("headline"):
        yield "manset", L.get("kicker"), L["headline"], " ".join([L.get("deck") or ""] + (L.get("paragraphs") or []))
    for s in d.get("sections") or []:
        for i, a in enumerate(s.get("articles") or []):
            yield art_id(s, i, a), a.get("kicker"), a.get("headline") or "", " ".join(a.get("paragraphs") or [])
    for b in d.get("briefs") or []:
        yield None, f"Kısa · {b.get('tag')}", (b.get("text") or "")[:110], b.get("text") or ""
    for r in (d.get("repos") or {}).get("items") or []:
        yield None, "Repo", r.get("name") or "", r.get("why") or ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sorgu")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    words = fold(a.sorgu).split()
    issues = []
    for path in glob.glob(os.path.join(ROOT, "issues", "*.json")):
        if os.path.basename(path) != "index.json":
            issues.append(json.load(open(path, encoding="utf-8")))
    out = []
    for d in sorted(issues, key=lambda x: x["date"], reverse=True):
        for anchor, kicker, head, body in items(d):
            hay = fold(" ".join([kicker or "", head, body]))
            if not all(w in hay for w in words):
                continue
            line = f"#{d['date']}{'-' + anchor if anchor else ''} | {kicker or ''} | {head}"
            if not all(w in fold(head) for w in words):
                hit = next((s for s in sentences(body) if any(w in fold(s) for w in words)), "")
                if hit:
                    line += f"\n    … {hit[:200]}"
            out.append(line)
    print("\n".join(out[:a.n]) if out else "Eşleşme yok.")
    if len(out) > a.n:
        print(f"(+{len(out) - a.n} sonuç daha; --n ile artır)")


if __name__ == "__main__":
    main()
