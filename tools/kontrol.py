#!/usr/bin/env python3
"""Bir sayı dosyasını (taslak ya da son hali) kurallar/KURALLAR.md'deki ölçülebilir kurallara göre denetler.

Kullanım:
    python3 tools/kontrol.py /tmp/dc/draft.json
    python3 tools/kontrol.py issues/2026-11-12.json

HATA satırları düzeltilmeden yayımlanmaz (çıkış kodu 1). UYARI satırları gözden geçirilir; gerekçesi varsa bırakılabilir.
Bu betik yalnızca biçim ve ölçüleri denetler; doğruluğu ve dili editör denetler.
"""
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = "Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık"
errors, warns = [], []
E = errors.append
W = warns.append


def words(text):
    return len(str(text or "").split())


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ“`])", str(text or "")) if s.strip()]


def strings(x, path=""):
    """JSON içindeki bütün metinleri (yol, değer) olarak dolaş."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(x, str):
        yield path, x


def check_sources(where, srcs, dates):
    if not srcs:
        E(f"{where}: kaynak yok")
    for s in srcs or []:
        u = (s or {}).get("url") or ""
        if u.startswith("#"):
            check_ref_link(where, u, dates)
        elif not re.match(r"^https?://", u):
            E(f"{where}: geçersiz kaynak adresi: {u!r}")


def check_ref_link(where, u, dates):
    m = re.match(r"^#(\d{4}-\d{2}-\d{2})-(.+)$", u)
    if not m:
        E(f"{where}: iç atıf biçimi yanlış: {u}")
        return
    d, anchor = m.groups()
    if d not in dates:
        E(f"{where}: iç atıf hedefi yok: issues/{d}.json")
    elif anchor not in dates[d]:
        E(f"{where}: iç atıf {u} o sayıda yok (geçerli çapalar: {', '.join(sorted(dates[d]))})")


def check_chart(where, c):
    items = c.get("items") or []
    if not c.get("title"):
        E(f"{where}: grafikte title yok")
    if not 2 <= len(items) <= 5:
        E(f"{where}: grafikte {len(items)} çubuk var (2-5 olmalı)")
    for it in items:
        if not isinstance(it.get("value"), (int, float)) or it.get("value") < 0:
            E(f"{where}: grafik değeri sayı ve >= 0 olmalı: {it.get('label')}")
        if not it.get("display"):
            E(f"{where}: grafik öğesinde display yok: {it.get('label')}")
    if sum(1 for it in items if it.get("highlight")) > 1:
        W(f"{where}: grafikte birden fazla highlight var")


def check_prose(where, paras, big):
    text = " ".join(paras or [])
    first = (sentences(text) or [""])[0]
    if re.search(rf"\b\d{{1,2}} ({MONTHS})", " ".join(first.split()[:6])):
        W(f"{where}: ilk cümle tarihli duyuru kalıbıyla açılıyor: “{first[:70]}…”")
    for s in sentences(text):
        n = words(s)
        if n > 32:
            W(f"{where}: {n} kelimelik cümle: “{s[:70]}…”")
        if s.count(";") > 1:
            W(f"{where}: cümlede birden fazla noktalı virgül: “{s[:70]}…”")
    if big:
        for i, p in enumerate(paras or []):
            if words(p) > 80:
                W(f"{where}: {i + 1}. paragraf {words(p)} kelime (en fazla 80)")
    elif len(paras or []) > 1:
        W(f"{where}: küçük haber {len(paras)} paragraf (tek paragraf olmalı)")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except (OSError, ValueError) as e:
        sys.exit(f"HATA: dosya okunamadı ya da geçerli JSON değil: {e}")

    # Önceki sayılar: numara ve iç atıf hedefleri
    dates, numbers, prev = {}, [], {}
    for p in glob.glob(os.path.join(ROOT, "issues", "*.json")):
        if os.path.basename(p) == "index.json" or os.path.abspath(p) == os.path.abspath(path):
            continue
        with open(p, encoding="utf-8") as f:
            o = json.load(f)
        if o.get("date") == d.get("date"):
            continue
        numbers.append(o.get("number") or 0)
        a = {"manset"}
        for s in o.get("sections") or []:
            for i, art in enumerate(s.get("articles") or []):
                a.add(str(art.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}"))
        dates[o["date"]] = a
        prev[o["date"]] = o

    # Üst alanlar
    for k in ("date", "number", "dateLabel", "readingMinutes", "lead", "sections", "repos", "briefs"):
        if k not in d:
            E(f"üst alan eksik: {k}")
    if "_not" in d:
        E("_not alanı örnek dosyaya aittir, sayıda yer almaz")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d.get("date") or "")):
        E(f"date biçimi YYYY-MM-DD olmalı: {d.get('date')!r}")
    if numbers and d.get("number") != max(numbers) + 1:
        E(f"number {d.get('number')} yanlış; {max(numbers) + 1} olmalı")

    # Metin geneli
    for where, s in strings(d):
        if where.endswith(".url"):
            continue
        if "«" in s or "»" in s:
            E(f"{where}: « » kullanılmış, Türkçe tırnak “ ” olmalı")
        if '"' in s:
            E(f"{where}: düz çift tırnak kullanılmış, Türkçe tırnak “ ” olmalı")
        if "’" in s:
            W(f"{where}: kıvrık kesme işareti yazılmış; düz ' yaz, sayfa kendisi çevirir")

    # Çapalar
    secs = d.get("sections") or []
    L = d.get("lead") or {}
    anchors = {"manset": L}
    for s in secs:
        for i, a in enumerate(s.get("articles") or []):
            anchors[str(a.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}")] = a

    # Manşet
    if len(L.get("headline") or "") > 80:
        E(f"manşet başlığı {len(L['headline'])} karakter (en fazla 80)")
    for k in ("kicker", "headline", "deck", "paragraphs", "sources", "box"):
        if not L.get(k):
            E(f"lead.{k} eksik")
    if len(L.get("paragraphs") or []) != 4:
        W(f"manşet {len(L.get('paragraphs') or [])} paragraf (4 beklenir)")
    if L.get("why"):
        W("manşette why yazılmaz; Pratik çıkarım kutusu var")
    box = L.get("box") or {}
    if not 3 <= len(box.get("items") or []) <= 4:
        W(f"Pratik çıkarım kutusunda {len(box.get('items') or [])} madde var (3-4 beklenir)")
    check_prose("manşet", L.get("paragraphs"), True)
    check_sources("manşet", L.get("sources"), dates)
    charts = 1 if L.get("chart") else 0
    if L.get("chart"):
        check_chart("manşet", L["chart"])

    # Bölümler
    stats = 0
    for s in secs:
        sid = s.get("id") or "bolum"
        if not s.get("id") or not s.get("title"):
            E(f"bölümde id ya da title eksik: {s.get('title') or s.get('id')}")
        if re.search(r"kısa bölüm", s.get("subtitle") or "", re.I):
            E(f"{sid}: subtitle'da “Kısa bölüm” notu var")
        arts = s.get("articles") or []
        patch = s.get("patch")
        if patch is not None:
            if sid != "guvenlik":
                E(f"{sid}: patch (Bugün yamala) yalnızca Güvenlik bölümünde olur")
            if not 1 <= len(patch) <= 3:
                E(f"{sid}.patch {len(patch)} madde (1-3 olmalı; yoksa alanı yazma)")
            for i, m in enumerate(patch):
                if not m.get("text"):
                    E(f"{sid}.patch[{i}]: text eksik")
                elif len(m["text"]) > 110:
                    E(f"{sid}.patch[{i}]: {len(m['text'])} karakter (en fazla 110)")
                if not re.match(r"^https://", m.get("url") or ""):
                    E(f"{sid}.patch[{i}]: url https ile başlamalı")
        lo, hi = {"ai": (6, 8), "guvenlik": (3, 4)}.get(sid, (2, 3))
        if not lo <= len(arts) <= hi:
            (E if sid == "guvenlik" and len(arts) > hi else W)(f"{sid}: {len(arts)} haber var ({lo}-{hi} beklenir)")
        row = []
        for i, a in enumerate(arts):
            where = f"{sid}-{i + 1}"
            size, big = a.get("size"), bool(a.get("big"))
            if size not in (4, 6, 8):
                E(f"{where}: size 4, 6 ya da 8 olmalı: {size!r}")
                size = 4
            for k in ("kicker", "headline", "paragraphs"):
                if not a.get(k):
                    E(f"{where}: {k} eksik")
            if sid == "guvenlik":
                if big or size == 8:
                    E(f"{where}: Güvenlik bölümünde büyük ya da 8 kolonluk haber olmaz (3 haber 4+4+4, 4 haber 6+6)")
                n = words(" ".join(a.get("paragraphs") or []))
                if n > 100:
                    W(f"{where}: güvenlik haberi {n} kelime (60-90 beklenir)")
            limit = 60 if size == 4 else 70
            if len(a.get("headline") or "") > limit:
                E(f"{where}: başlık {len(a['headline'])} karakter (en fazla {limit}): {a['headline']}")
            kick = (a.get("kicker") or "").split(" · ")[0].replace("İ", "i").lower()
            if kick == "iddia" and not re.search(r":|iddia", a.get("headline") or "", re.I):
                W(f"{where}: İddia haberinin başlığında kaynak ya da “iddia” yok: {a.get('headline')}")
            if big and not a.get("why"):
                E(f"{where}: büyük haberde why yok")
            if a.get("why"):
                if words(a["why"]) > 25:
                    E(f"{where}: why {words(a['why'])} kelime (en fazla 25)")
                if re.match(r"\s*neden önemli", a["why"], re.I):
                    E(f"{where}: why “Neden önemli” ile başlıyor; etiketi sayfa ekler")
            st = a.get("stat")
            if st:
                stats += 1
                if not big:
                    E(f"{where}: stat yalnızca büyük haberde olur")
                if a.get("chart"):
                    E(f"{where}: aynı haberde hem stat hem chart var")
                if len(str(st.get("n") or "")) > 10:
                    E(f"{where}: stat.n {len(str(st.get('n')))} karakter (en fazla 10)")
                if len(str(st.get("l") or "")) > 80:
                    E(f"{where}: stat.l {len(str(st.get('l')))} karakter (en fazla 80)")
            if a.get("chart"):
                charts += 1
                check_chart(where, a["chart"])
            check_prose(where, a.get("paragraphs"), big)
            check_sources(where, a.get("sources"), dates)
            row.append((where, size, words(" ".join(a.get("paragraphs") or [])), big))
            total = sum(r[1] for r in row)
            if total == 12:
                sizes = [r[1] for r in row]
                ws = [r[2] for r in row]
                if sizes == [8, 4]:
                    ratio = ws[1] / ws[0] if ws[0] else 0
                    msg = f"{row[0][0]} + {row[1][0]}: 4 kolonluk haber büyük haberin %{ratio * 100:.0f}'i ({ws[1]}/{ws[0]} kelime; hedef %40-60)"
                    if not 0.30 <= ratio <= 0.75:
                        E(msg)
                    elif not 0.40 <= ratio <= 0.60:
                        W(msg)
                    if not 160 <= ws[0] <= 220:
                        W(f"{row[0][0]}: büyük haber {ws[0]} kelime (160-220 beklenir)")
                elif len(set(sizes)) == 1:
                    if max(ws) - min(ws) > 20:
                        W(f"{'+'.join(r[0] for r in row)}: kelime farkı {max(ws) - min(ws)} ({ws}; en fazla 20)")
                else:
                    E(f"{sid}: satır {sizes} biçiminde; 8+4, 6+6 ya da 4+4+4 olmalı")
                row = []
            elif total > 12:
                E(f"{sid}: size değerleri satırı taşırıyor ({[r[1] for r in row]}); 8+4, 6+6 ya da 4+4+4 olmalı")
                row = []
        if row:
            E(f"{sid}: son satır dolmuyor ({[r[1] for r in row]}); toplam 12 olmalı")
    if stats > 3:
        E(f"{stats} stat var (bir sayıda en fazla 3)")
    if charts > 3:
        E(f"{charts} grafik var (bir sayıda en fazla 3)")

    # Takvim
    if d.get("figures"):
        W("figures artık kullanılmıyor; sayının başında Takvim (calendar) basılır")
    cal = d.get("calendar")
    if cal is not None:
        if not 2 <= len(cal) <= 5:
            E(f"calendar {len(cal)} öğe (2-5 olmalı; en az 2 uygun tarih yoksa alanı yazma)")
        try:
            today = datetime.date.fromisoformat(d.get("date"))
        except (TypeError, ValueError):
            today = None
        last = None
        for i, c in enumerate(cal):
            w = f"calendar[{i}]"
            try:
                cd = datetime.date.fromisoformat(str(c.get("date")))
            except ValueError:
                E(f"{w}: date biçimi YYYY-MM-DD olmalı: {c.get('date')!r}")
                continue
            if today and not 0 <= (cd - today).days <= 30:
                E(f"{w}: {cd} sayı tarihinden itibaren 0-30 gün içinde olmalı")
            if last and cd < last:
                W(f"{w}: öğeler tarih sırasında değil (sayfa yine de sıralar)")
            last = cd
            t = c.get("text") or ""
            if not t:
                E(f"{w}: text eksik")
            elif len(t) > 60:
                E(f"{w}: text {len(t)} karakter (en fazla 60): {t}")
            if re.search(r"\b(yakında|bekleniyor|muhtemelen|önemli)\b", t, re.I):
                W(f"{w}: kesin olmayan ya da yorum içeren ifade: {t}")
            r, u = c.get("ref"), c.get("url")
            if not r and not u:
                E(f"{w}: ref ya da url gerekli")
            if r and r not in anchors:
                E(f"{w}: ref {r!r} bu sayıda yok (geçerli: {', '.join(anchors)})")
            if u and not re.match(r"^https://", u):
                E(f"{w}: url https ile başlamalı")

    # Düzeltmeler
    for i, c in enumerate(d.get("corrections") or []):
        w = f"corrections[{i}]"
        cd, r = c.get("date"), c.get("ref")
        if cd not in dates:
            E(f"{w}: {cd!r} tarihli önceki sayı yok")
        elif r not in dates[cd]:
            E(f"{w}: {cd} sayısında {r!r} çapası yok")
        if not c.get("text"):
            E(f"{w}: text eksik")
        elif words(c["text"]) > 50:
            W(f"{w}: {words(c['text'])} kelime (tek iki cümle beklenir)")

    # Yalnızca Anthropic kaynaklı öne çıkarma
    def only_anthropic(a):
        us = [x.get("url") or "" for x in a.get("sources") or []]
        return us and all(re.search(r"(anthropic\.com|claude\.(ai|com))", u) for u in us)
    for where, a in [("manşet", L)] + [(k, v) for k, v in anchors.items() if k != "manset"]:
        if only_anthropic(a) and (where == "manşet" or a.get("big") or a.get("stat") or a.get("chart")):
            E(f"{where}: yalnızca Anthropic kaynaklı haber manşet, büyük haber, stat ya da chart olamaz")

    # Manşet: aynı şirket art arda
    older = [k for k in prev if k < str(d.get("date"))]
    if older:
        p = prev[max(older)]
        pk = ((p.get("lead") or {}).get("headline") or "").split()[:1]
        if pk and pk == (L.get("headline") or "").split()[:1]:
            W(f"manşet önceki sayınınkiyle aynı kelimeyle açılıyor ({pk[0]}); aynı şirket art arda manşet olmaz")

    # Günün örüntüsü
    P = d.get("pattern")
    if P is not None:
        if len(P.get("title") or "") > 60:
            E(f"pattern.title {len(P['title'])} karakter (en fazla 60)")
        if not 30 <= words(P.get("text")) <= 60:
            E(f"pattern.text {words(P.get('text'))} kelime (30-60 olmalı)")
        pr = P.get("refs") or []
        if len(pr) < 3:
            E(f"pattern.refs {len(pr)} adet (en az 3 olmalı)")
        for r in pr:
            if r not in anchors:
                E(f"pattern.refs: {r!r} bu sayıda yok")

    # Repolar
    items = (d.get("repos") or {}).get("items") or []
    if not 6 <= len(items) <= 8:
        E(f"repolar {len(items)} adet (6-8 olmalı)")
    owners = {}
    for r in items:
        name = r.get("name") or "?"
        for k in ("name", "url", "stars", "cat", "why", "meta"):
            if not r.get(k):
                E(f"repo {name}: {k} eksik")
        if not isinstance(r.get("starsValue"), (int, float)):
            E(f"repo {name}: starsValue sayı olmalı")
        if len(sentences(r.get("why"))) < 2:
            W(f"repo {name}: why tek cümle; ikinci cümle neden şimdi gündemde olduğunu söylemeli")
        want = f"{r['lang']} · {r.get('cat')}" if r.get("lang") else r.get("cat")
        if r.get("meta") != want:
            E(f"repo {name}: meta {r.get('meta')!r} olmalıydı {want!r}")
        owners.setdefault(name.split("/")[0].lower(), []).append(name)
    for o, names in owners.items():
        if len(names) > 1:
            E(f"aynı kuruluştan birden fazla repo: {', '.join(names)}")
    try:
        today = datetime.date.fromisoformat(d.get("date"))
    except (TypeError, ValueError):
        today = None
    seen = {}
    for pd, o in prev.items():
        if today and 0 < (today - datetime.date.fromisoformat(pd)).days <= 7:
            for r in (o.get("repos") or {}).get("items") or []:
                seen.setdefault((r.get("name") or "").lower(), pd)
    for r in items:
        n = (r.get("name") or "").lower()
        if n in seen:
            E(f"repo {r.get('name')}: {seen[n]} sayısında yer aldı (7 gün içinde tekrar olmaz)")
    if items and not any((r.get("lang") or "") in ("Java", "Kotlin", "Scala", "Groovy") for r in items):
        W("repolarda JVM reposu yok; trending listelerinde varsa en az biri girer")

    # Kısa Kısa
    briefs = d.get("briefs") or []
    if not 6 <= len(briefs) <= 10:
        E(f"Kısa Kısa {len(briefs)} haber (6-10 olmalı)")
    for i, b in enumerate(briefs):
        if not b.get("tag") or not b.get("text"):
            E(f"briefs[{i}]: tag ya da text eksik")
        u = b.get("url") or ""
        if u.startswith("#"):
            check_ref_link(f"briefs[{i}]", u, dates)
        elif not re.match(r"^https?://", u):
            E(f"briefs[{i}]: geçersiz adres: {u!r}")
        if len(sentences(b.get("text"))) > 3:
            W(f"briefs[{i}]: {len(sentences(b.get('text')))} cümle (tek-iki cümle beklenir)")

    total_words = sum(words(v) for k, v in strings(d) if not k.endswith(".url"))
    for m in errors:
        print("HATA  ", m)
    for m in warns:
        print("UYARI ", m)
    print(f"\n{len(errors)} hata, {len(warns)} uyarı · yaklaşık {total_words} kelime (~{total_words / 200:.0f} dk okuma)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
