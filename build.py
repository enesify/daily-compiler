#!/usr/bin/env python3
"""The Daily Compiler · statik site üretici.

issues/*.json  →  index.html (son sayı), sayi/YYYY-MM-DD.html, arsiv.html, hakkinda.html, feed.xml
Kullanım:  python3 build.py
Bağımlılık yok (yalnızca Python 3 standart kütüphanesi).
"""
import datetime as dt
import glob
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = "The Daily Compiler"
TAGLINE_B = "Yazılım · Yapay Zeka · LLM"
TAGLINE = "Her sabah, son 24–48 saatin özeti"
STRIP_DAYS = 14  # kadran şeridinde gösterilen takvim günü

MONTHS = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
MONTHS_LONG = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
DAYS_SHORT = ["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"]
DAYS_3 = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

# ---------------------------------------------------------------- yardımcılar
esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)


def d_of(iso):
    return dt.date.fromisoformat(iso)


def short_date(iso):
    d = d_of(iso)
    return f"{d.day} {MONTHS[d.month - 1]}"


def long_date(iso):
    d = d_of(iso)
    return f"{DAYS[d.weekday()]}, {d.day} {MONTHS_LONG[d.month - 1]} {d.year}"


def asset(ctx, rel):
    """assets/ dosyası için içerik özetli adres: dosya değişince tarayıcı önbelleği kendiliğinden yenilenir."""
    try:
        v = hashlib.sha1(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]
    except OSError:
        return ctx.href(rel)
    return f"{ctx.href(rel)}?v={v}"


WJ = "\u2060"  # word joiner: sayı aralığı satır sonunda bölünmesin


def typo(text):
    """Tipografik düzeltmeler: kesme işareti (Code'da → Code’da) ve sayı/saat aralıklarında kısa çizgi (16:00–18:00).
    CVE numaraları ve ISO tarihler (2026-11-07) gibi çok tireli diziler aralık sayılmaz."""
    s = str(text or "")
    s = re.sub(r"(?<=[\w)”])'(?=\w)", "’", s)
    s = re.sub(r"(?<![\w\-/.,:])(%?\d+(?:[.,:]\d+)*)-(%?\d+(?:[.,:]\d+)*)(?![\w\-/])",
               lambda m: f"{m.group(1)}{WJ}–{WJ}{m.group(2)}", s)
    return s


def _text(p, i):
    """rich() içindeki düz metin parçası; koddan hemen sonra gelen ek kesmesi de düzeltilir (`x`'e → ’e)."""
    p = typo(p)
    return "’" + p[1:] if i and re.match(r"'\w", p) else p


def plain(text):
    """Düz metin alanları (title, og, feed) için backtick işaretlerini at."""
    return typo(text).replace("`", "")


def num3(n):
    return str(n or "").zfill(3)


def rich(text):
    """`backtick` → <code>, gerisi kaçışlı metin."""
    parts = re.split(r"`([^`]+)`", str(text or ""))
    return "".join(f"<code>{esc(p)}</code>" if i % 2 else esc(_text(p, i)) for i, p in enumerate(parts) if p)


# Büyük harf: Türkçe kelimelerde i→İ, İngilizce terim/özel isimlerde i→I (SPRING, GITHUB)
EN = set(("spring java maven linux firefox openai github gitlab copilot kimi gemini intel hibernate kotlin quarkus "
          "kubernetes pypi alpine debian chromium windows android ios xcode intellij jetbrains rails wordpress siemens "
          "crowdstrike mistral tencent deepseek notion perplexity nothing zipline siltronic pipeline build preview weights "
          "weight tooling cli ide exploit exploitgym spec kit policy pricing fintech vibe coding commit git diff review "
          "findings vision terminal-bench swe-bench langchain4j micronaut graalvm openjdk jdk jakarta tomcat jenkins redis "
          "milvus qdrant ollama vllm sglang daybreak astra sol cyber firebase lockdown mode kill switch fiddler dreadnode "
          "nebius iren nscale pierre conductor cognition devin cursor windsurf antigravity bedrock agentcore azure aws "
          "vertex lambda tpu tpus inference coding agentic big tech high speed highspeed claude-code ai-native ci cd devops "
          "sonar sonarqube jacoco surefire figma eclipse skill skills anthropic combinator microsoft local first cisco "
          "driven change insight insights pi vite vitest prisma sqlite ollama mini lite fine tuning edition engine engines it").split())


def tr_upper(s):
    return s.replace("i", "İ").replace("ı", "I").upper()


def word_up(w):
    m = re.match(r"^([^'’]*)(['’].*)?$", w, re.S)
    base, suf = m.group(1), m.group(2) or ""
    if "i" not in base:
        return tr_upper(base) + tr_upper(suf)
    key = re.sub(r"[^a-z0-9.\-]", "", base.lower())
    en = (not re.search(r"[çğıöşüİÇĞÖŞÜ]", base)) and (
        key in EN or re.search(r"[a-z][A-Z]", base) or re.search(r"[wxq]", base, re.I)
        or re.search(r"ing$", base, re.I) or re.search(r"\d", base))
    return (base.upper() if en else tr_upper(base)) + tr_upper(suf)


def caps(s):
    toks = re.split(r"(\s+|[&·/()–—,:;+\-])", str(s or ""))
    return "".join(word_up(t) if t and not t.isspace() else t for t in toks)


def caps_rich(text):
    """Büyük harfe çevrilecek alanlar: kod parçaları korunur."""
    parts = re.split(r"`([^`]+)`", str(text or ""))
    return "".join(f"<code>{esc(p)}</code>" if i % 2 else esc(caps(_text(p, i))) for i, p in enumerate(parts) if p)


# ---------------------------------------------------------------- veri
def load_issues():
    out = []
    for f in glob.glob(os.path.join(ROOT, "issues", "*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:  # bozuk dosya tüm siteyi düşürmesin
            print(f"UYARI: {f} okunamadı: {e}", file=sys.stderr)
            continue
        if isinstance(d, dict) and re.match(r"^\d{4}-\d{2}-\d{2}$", str(d.get("date", ""))):
            out.append(d)
    out.sort(key=lambda d: d["date"], reverse=True)
    return out


def issue_path(date):
    return f"sayi/{date}.html"


class Ctx:
    def __init__(self, issues, depth):
        self.issues = issues
        self.by_date = {i["date"]: i for i in issues}
        self.pre = "../" * depth if depth else ""

    def href(self, path):
        return self.pre + path


# ---------------------------------------------------------------- bileşenler
def ref_link(ctx, label, url):
    m = re.match(r"^#?(\d{4}-\d{2}-\d{2})(?:-([a-z0-9-]+))?$", url or "", re.I)
    if not m or m.group(1) not in ctx.by_date:
        return f'<span class="ref-gone" title="Bu sayı bulunamadı">{esc(label)}</span>'
    date, anchor = m.group(1), m.group(2)
    h = ctx.href(issue_path(date)) + (f"#a-{anchor}" if anchor else "")
    return f'<a class="ref" href="{esc(h)}" title="{esc(short_date(date))} sayısındaki habere git">↩ {esc(plain(label))}</a>'


def ext_link(label, url):
    if re.match(r"^https?://", url or "", re.I):
        return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(typo(label))}</a>'
    return esc(typo(label))


def sources(ctx, lst):
    if not lst:
        return ""
    items = [ref_link(ctx, s.get("label"), s.get("url")) if str(s.get("url", "")).startswith("#")
             else ext_link(s.get("label"), s.get("url")) for s in lst]
    pre = "Kaynaklar: " if len(lst) > 1 else "Kaynak: "
    return f'<p class="src">{pre}{" · ".join(items)}</p>'


def chart(c):
    if not isinstance(c, dict) or not isinstance(c.get("items"), list):
        return ""
    items = []
    for x in c["items"][:8]:
        try:
            v = float(x.get("value"))
        except Exception:
            continue
        if isinstance(x.get("label"), str) and v >= 0:
            items.append((x, v))
    if len(items) < 2:
        return ""
    mx = max(v for _, v in items) or 1
    rows = []
    for x, v in items:
        shown = str(x["display"]) if x.get("display") is not None else str(x.get("value"))
        hl = " hl" if x.get("highlight") else ""
        rows.append(
            f'<div class="brow{hl}" role="img" aria-label="{esc(x["label"])}: {esc(shown)}" title="{esc(x["label"])}: {esc(shown)}">'
            f'<span class="bl">{esc(x["label"])}</span><div class="btrack"><div class="bar" style="width:{v / mx * 100:.2f}%"></div></div>'
            f'<span class="bv">{esc(shown)}</span></div>')
    cap = f"<figcaption>{caps_rich(c.get('title'))}</figcaption>" if c.get("title") else ""
    note = f'<p class="cnote">{rich(c.get("note"))}</p>' if c.get("note") else ""
    return f'<figure class="chart">{cap}{"".join(rows)}{note}</figure>'


PROVENANCE = {"iddia": "claim", "şirket beyanı": "company"}


def kicker(text, alert=False, default=None):
    """Üst başlık. Baştaki “İddia” / “Şirket beyanı” kaynak etiketi konu etiketinden ayrılır ve çerçeveli basılır."""
    text = str(text or default or "")
    if not text:
        return ""
    parts = [p.strip() for p in text.split(" · ")]
    key = parts[0].replace("İ", "i").replace("I", "ı").lower()
    prov = ""
    if key in PROVENANCE:
        prov = f'<span class="prov prov-{PROVENANCE[key]}">{esc(caps(parts[0]))}</span>'
        parts = parts[1:]
    rest = caps_rich(" · ".join(parts)) if parts else ""
    return f'<span class="kicker{" alert" if alert else ""}">{prov}{rest}</span>'


def article(ctx, a, aid):
    cls = f"s{a.get('size') or 4}" + (" big" if a.get("big") else "")
    k = kicker(a.get("kicker"), a.get("alert"))
    pill = f'<span class="pill">{caps_rich(a.get("pill"))}</span>' if a.get("pill") else ""
    body = "".join(f"<p>{rich(p)}</p>" for p in a.get("paragraphs") or [])
    # stat: büyük haberlerde isteğe bağlı tek iri rakam {n, l}; grafik varsa basılmaz
    st = a.get("stat")
    stat = ""
    if a.get("big") and isinstance(st, dict) and st.get("n") and not chart(a.get("chart")):
        stat = f'<p class="stat"><span class="n">{esc(typo(st.get("n")))}</span><span class="l">{rich(st.get("l"))}</span></p>'
    # Telefonda küçük haberlerin metni üç satırda kesilir; site.js gerekirse bu düğmeyi gösterir
    more = '<button class="more" type="button" aria-expanded="false" hidden>Devamı</button>'
    # why: tek cümlelik editoryal “Neden önemli” notu; metinden ayrı ve etiketli basılır
    why = f'<p class="why"><b>{esc(caps("Neden önemli"))}</b>{rich(a.get("why"))}</p>' if a.get("why") else ""
    return (f'<article class="{cls}" id="a-{esc(aid)}">{k}<h3>{pill}{rich(a.get("headline"))}</h3>{stat}'
            f'<div class="body">{body}</div>{more}{why}{chart(a.get("chart"))}{sources(ctx, a.get("sources"))}</article>')


def pattern(cur):
    """Günün örüntüsü: birkaç haberin ortak noktasını adlandıran isteğe bağlı editoryal not {title, text, refs[]}."""
    P = cur.get("pattern")
    if not isinstance(P, dict) or not P.get("text"):
        return ""
    heads = {"manset": (cur.get("lead") or {}).get("headline")}
    for s in cur.get("sections") or []:
        for i, a in enumerate(s.get("articles") or []):
            heads[art_id(s, i, a)] = a.get("headline")
    links = []
    for r in P.get("refs") or []:
        r = str(r).lstrip("#")
        r = r[2:] if r.startswith("a-") else r
        if heads.get(r):
            links.append(f'<a href="#a-{esc(r)}">{rich(heads[r])}</a>')
    rel = f'<p class="src">İlgili haberler: {" · ".join(links)}</p>' if links else ""
    title = f'<h3>{rich(P.get("title"))}</h3>' if P.get("title") else ""
    return (f'<aside class="pattern" aria-label="Günün örüntüsü"><div><span class="kicker">{esc(caps("Günün örüntüsü"))}</span>{title}</div>'
            f'<div><p>{rich(P.get("text"))}</p>{rel}<p class="note">Bu not editoryal bir gözlemdir, haberin parçası değildir.</p></div></aside>')


def art_id(s, i, a):
    return str(a.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}")


def section_articles(ctx, s):
    return "".join(article(ctx, a, art_id(s, i, a)) for i, a in enumerate(s.get("articles") or []))


def dial(ctx, cur):
    issues = ctx.issues
    idx = next(i for i, x in enumerate(issues) if x["date"] == cur["date"])
    older = issues[idx + 1] if idx + 1 < len(issues) else None
    newer = issues[idx - 1] if idx > 0 else None

    def step(it, sym, lbl_has, lbl_none, rel):
        if it:
            return (f'<a class="dial-step" rel="{rel}" href="{esc(ctx.href(issue_path(it["date"])))}" '
                    f'aria-label="{esc(lbl_has + ": " + long_date(it["date"]))}">{sym}</a>')
        return f'<span class="dial-step" aria-label="{esc(lbl_none)}">{sym}</span>'

    meta = f'Sayı {num3(cur.get("number"))} · '
    meta += '<span class="latest">Son sayı</span>' if idx == 0 else f'{idx} sayı önce'
    meta += (f'<span class="opt"> · ≈ {cur.get("readingMinutes") or 15} dk okuma</span>'
             f' · <a href="{esc(ctx.href("arsiv.html"))}">Arşiv</a>')

    # Şerit: en yeni sayıya kadar son STRIP_DAYS takvim günü; eski bir sayı açıksa ona ortalanır
    latest, oldest, c = d_of(issues[0]["date"]), d_of(issues[-1]["date"]), d_of(cur["date"])
    end = min(latest, c + dt.timedelta(days=STRIP_DAYS // 2)) if c < latest - dt.timedelta(days=STRIP_DAYS - 1) else latest
    start = max(oldest, end - dt.timedelta(days=STRIP_DAYS - 1))
    ticks = []
    d = start
    while d <= end:
        iso = d.isoformat()
        it = ctx.by_date.get(iso)
        lbl = f"{d.day} {MONTHS_LONG[d.month - 1]}" + (f" · Sayı {num3(it.get('number'))}" if it else " · sayı yok")
        inner = f'<span class="stem"></span><span class="d">{d.day}</span><span class="w">{caps(DAYS_SHORT[d.weekday()])}</span>'
        ms = " mstart" if d.day == 1 and d != start else ""
        if it:
            cur_attr = ' aria-current="page"' if iso == cur["date"] else ""
            ticks.append(f'<a class="tick has{ms}" role="listitem" href="{esc(ctx.href(issue_path(iso)))}" '
                         f'title="{esc(lbl)}" aria-label="{esc(lbl)}"{cur_attr}>{inner}</a>')
        else:
            ticks.append(f'<span class="tick none{ms}" role="listitem" title="{esc(lbl)}" aria-label="{esc(lbl)}">{inner}</span>')
        d += dt.timedelta(days=1)

    return (f'<nav class="dial" id="archive" aria-label="Sayı arşivi"><div class="dial-head">'
            f'{step(older, "‹", "Önceki sayı", "Daha eski sayı yok", "prev")}'
            f'<div class="dial-now"><span class="dial-date">{esc(cur.get("dateLabel") or long_date(cur["date"]))}</span>'
            f'<span class="dial-meta">{caps_meta(meta)}</span></div>'
            f'{step(newer, "›", "Sonraki sayı", "Daha yeni sayı yok", "next")}</div>'
            f'<div class="dial-track"><div class="ticks" role="list">{"".join(ticks)}</div></div></nav>')


def caps_meta(s):
    """dial-meta: etiketlerin dışındaki metni büyük harfe çevir."""
    return re.sub(r"(>|^)([^<]+)", lambda m: m.group(1) + caps(m.group(2)), s)


# Logo: Grenze Gotisch'ten çizim olarak üretildi (yazı tipi yüklenmez, her cihazda aynı görünür).
# "the" parçası turkuaz ve ince, isim koyu ve kalın basılır. full = tam isimlik, mono = telefondaki yapışan menü için "The DC".
LOGO = {"full": {"the": "M22.4 29.8Q20.5 29.8 19.2 32Q18 34.2 17.3 37.5Q16.6 40.8 16.4 44.3Q16.1 47.8 16.1 50.4Q16.1 56.4 17.2 61.7Q18.4 67 21.2 70.2Q24 73.5 28.9 73.5L41.9 73.4V78.6Q40.6 79 37.9 79.4Q35.2 79.8 32.2 80.2Q29.3 80.5 27.1 80.7Q24.8 80.9 24.2 80.9Q18.2 80.9 14.2 76.9Q10.2 72.9 8.2 66.3Q6.2 59.7 6.2 52.1Q6.2 46.9 7 43.5Q7.7 40 9.2 36.7Q9.9 35.6 11.4 33.9Q13 32.2 15.3 30.7Q17.6 29.2 20.4 28.7ZM45.4 20.9 43.4 28.7Q41.2 29.5 38.8 30.1Q36.4 30.8 34.2 31.1Q32 31.5 30.2 31.5Q27.7 31.5 26.2 31Q24.7 30.5 23.3 30Q21.9 29.5 19.6 29.5Q19 29.5 18.4 29.5Q17.7 29.6 17.1 29.8L16.9 29.2L1.3 27.5L3.2 18Q9.7 18.8 15.1 19.6Q20.4 20.5 24.3 21Q28.2 21.5 30.1 21.5Q31.5 21.5 33.5 21.3Q35.4 21.2 38.1 20.7Q40.8 20.3 44.2 19.6ZM22.6 73.7V25.3H27.8V68Q27.8 68.6 27.3 70.2Q26.8 71.7 25.7 73.7Z M47.9 20.7V17Q47.9 17 48.8 16.8Q49.6 16.7 50.9 16.4Q52.1 16.2 53.4 15.9Q54.7 15.7 55.7 15.5Q56.7 15.4 57 15.4Q57.3 15.4 58.1 16.1Q59 16.8 59.8 17.5Q60.5 18.3 60.5 18.7L60 41.3L60.5 41.4Q61.8 40.4 63.4 39.2Q65.1 38 66.7 36.9Q68.2 35.8 69.3 35Q70.4 34.3 70.5 34.3Q75.1 34.3 78.3 35.8Q81.5 37.3 83.2 41Q84.9 44.7 84.9 51.2V77.2Q84.9 80.2 83.8 83.6Q82.7 86.9 80.7 89.7Q78.6 92.5 75.6 93.9L72.7 91.5Q74.1 89.2 74.8 86.8Q75.4 84.5 75.6 82.2Q75.8 79.8 75.8 77.6V51.2Q75.8 46.4 74.7 44.5Q73.5 42.5 72.2 42.1Q70.8 41.8 70 41.8Q69.6 41.8 67.6 42.6Q65.6 43.4 63.5 44.3Q61.4 45.2 60.5 45.6V74.1L63.9 75.6V79.3Q63.9 79.3 62.7 79.5Q61.4 79.8 59.7 80.1Q57.9 80.4 56.5 80.7Q55 80.9 54.7 80.9Q54.4 80.9 53.6 80.2Q52.8 79.5 52.1 78.7Q51.4 77.9 51.4 77.6V22.1Z M103.4 58.1Q103.4 64.6 105.2 68Q106.9 71.4 109.1 72.6Q111.3 73.8 112.7 73.8Q113.1 73.8 114.6 73.8Q116.1 73.7 118.1 73.6Q120.1 73.5 122.1 73.4Q124.1 73.3 125.6 73.3V77.4Q123.8 78 121.5 78.6Q119.2 79.2 116.9 79.7Q114.6 80.2 112.8 80.6Q111.1 80.9 110.4 80.9Q106.3 80.9 102.5 78.7Q98.7 76.4 96.2 71.8Q93.8 67.1 93.8 59.9Q93.8 54.9 94.5 50.7Q95.2 46.5 96.2 44.6Q97 43.4 99 41.6Q101.1 39.9 103.5 38.2Q106 36.6 108.1 35.4Q110.2 34.3 111.2 34.3Q116.7 34.3 120.2 36.1Q123.6 37.9 125.3 42.8Q127 47.8 127 57.4L99 60.3V56.5L117.3 53.5Q117.3 47.4 116 43.8Q114.7 40.3 110.4 40.3Q109.6 40.3 108.7 40.4Q107.7 40.5 106.6 41Q105.2 41.7 104.3 46.3Q103.4 51 103.4 58.1Z", "main": "M155.3 24.7V19.8Q156.8 19.6 159 19.3Q161.2 19 163.5 18.8Q165.7 18.5 167.4 18.4Q169 18.3 169.4 18.4Q170.1 18.5 171 19.3Q171.9 20.2 172.5 21.1Q173.2 22 173.3 22.4V71.8L188.9 74.7Q190.1 74.9 190.9 74.3Q191.7 73.8 192.3 72.4Q193 71.1 193.4 69.2Q194.2 65.7 194.5 60.4Q194.7 55.2 194.7 48.8Q194.7 43.7 194.2 39.2Q193.7 34.7 192.6 31.4Q191.6 28.1 190 26.2Q188.5 24.4 186.4 24.6L180.6 25L181.8 18.3H186.8Q190.6 18.3 194.3 19.7Q198 21.2 201 24.6Q204 28 205.9 33.7Q207.7 39.5 207.7 48.1Q207.7 54.3 207.1 59Q206.5 63.7 205.4 67.4Q205.1 68.3 203.6 70Q202.1 71.7 199.9 73.6Q197.7 75.5 195.4 77.2Q193.1 78.8 191 79.9Q189 81 187.8 81Q183.9 81 180 80.9Q176 80.7 172.2 80.4Q168.5 80.1 165 79.5Q164.4 79.4 163.5 78.6Q162.6 77.8 161.8 76.9Q161.1 75.9 161 75.5V26.5ZM180.4 18.3H183.4V68.9Q183.4 69.5 182.8 71Q182.2 72.6 181.1 74.6H178.1V25.9Q178.1 24.9 178.8 22.8Q179.5 20.7 180.4 18.3Z M228.3 81Q223.3 81 220.2 79.2Q217 77.4 215.5 74.3Q213.9 71.2 213.9 67.4Q213.9 65.1 214.4 62.6Q215 60.1 216.1 57.8L226 62Q225.7 63 225.5 64.2Q225.3 65.5 225.3 66.8Q225.3 69.1 226.2 70.8Q227 72.4 229.7 72.4Q230.4 72.4 231.8 71.7Q233.3 71.1 235.2 70.1Q237.1 69.1 239 68.1V73.1Q236.9 74.7 234.6 76.5Q232.2 78.4 230.4 79.7Q228.7 81 228.3 81ZM216.1 57.8 238 54.9V60.1L224.8 63ZM217 41.7 218.9 34.1Q222.3 33.8 225.4 33.7Q228.5 33.7 231.4 33.7Q234.3 33.7 236.9 34Q238.4 34.2 240.4 35.7Q242.4 37.3 244.4 39.5Q246.3 41.6 247.6 43.8Q248.9 46 248.9 47.5V73L252.7 74.5V79.2Q250.5 79.6 248 80Q245.5 80.4 243.6 80.7Q241.7 81 241.1 81Q240.8 81 240 80.3Q239.1 79.6 238.4 78.7Q237.6 77.8 237.6 77.4V73.4L237.2 72.4V49.5Q237.2 46.4 236.2 45Q235.1 43.6 232.5 43.5Q231 43.3 228.6 43.3Q226.2 43.3 223.4 43.4Q220.7 43.5 218.4 43.6Z M265.2 81Q264.9 81 263.8 80.2Q262.7 79.3 261.8 78.4Q260.8 77.5 260.8 77.1V41.5L257 40.2V35.5Q257 35.5 258.6 35.2Q260.1 34.9 262.3 34.6Q264.5 34.2 266.3 33.9Q268.1 33.7 268.5 33.7Q268.9 33.7 269.8 34.5Q270.8 35.3 271.6 36.2Q272.5 37.2 272.5 37.7V73.3L276.2 74.4V79.1Q276.2 79.1 274.7 79.4Q273.2 79.7 271.2 80.1Q269.1 80.4 267.4 80.7Q265.6 81 265.2 81ZM259.8 17.8Q259.8 17.5 260.8 16.7Q261.9 15.8 263.3 14.7Q264.6 13.6 265.8 12.9Q266.9 12.1 267.1 12.1Q267.6 12.1 268.7 13Q269.8 13.9 271 15.2Q272.2 16.5 273.1 17.7Q273.9 18.8 273.8 19.3L273.3 21.6Q273.2 22 272.2 22.9Q271.2 23.7 269.9 24.7Q268.6 25.7 267.4 26.5Q266.3 27.2 266 27.2Q265.5 27.2 264.4 26.3Q263.3 25.3 262.1 24Q261 22.7 260.2 21.6Q259.4 20.5 259.4 20.1Z M288.7 81Q288.4 81 287.5 80.3Q286.5 79.5 285.7 78.6Q284.8 77.7 284.8 77.4V22.8L281 21.3V16.6Q281 16.6 282.1 16.4Q283.2 16.3 284.8 16Q286.5 15.7 288.2 15.4Q290 15.1 291.3 15Q292.6 14.8 292.9 14.8Q293.3 14.8 294.1 15.6Q295 16.3 295.7 17.2Q296.5 18 296.5 18.4V72.9L300.2 74.4V79.1Q300.2 79.1 298.6 79.4Q297 79.7 294.9 80.1Q292.8 80.4 291 80.7Q289.2 81 288.7 81Z M320.5 98.3Q320.2 98.3 319.5 97.2Q318.8 96.1 318.2 94.9Q317.7 93.7 317.7 93.4L322.3 79.9Q321.1 80 320.1 80.2Q319.1 80.3 318.8 80.3Q318.6 80.3 317.8 79.9Q317 79.4 317 79.4L306.8 41.5L302.7 40.3V35.3Q302.7 35.3 304.2 35Q305.7 34.8 307.8 34.5Q309.9 34.2 311.6 33.9Q313.3 33.7 313.6 33.7Q313.9 33.7 314.9 34.3Q315.9 34.9 316.9 35.7Q317.8 36.5 317.9 37L323.1 60L324.8 70.3H325.8L333.4 41L327.2 40.2V34.6Q327.2 34.6 328.5 34.5Q329.8 34.5 331.7 34.3Q333.7 34.1 335.7 34Q337.8 33.8 339.2 33.7Q340.7 33.7 340.9 33.7Q341.3 33.7 342 34.4Q342.8 35.2 343.4 36.2Q344.1 37.2 344 37.7L330.8 79.4L328.2 90.5L332.6 92.3L332.5 96.8Q332.5 96.8 330.9 97Q329.2 97.3 326.9 97.5Q324.7 97.8 322.8 98Q320.9 98.3 320.5 98.3Z M379.6 26.6Q379.2 30 378.8 33.3Q378.3 36.6 378.1 40.4Q377.9 44.1 377.9 48.9Q377.9 58.1 379.4 63.1Q381 68 383.7 69.9Q386.4 71.8 389.8 71.8L404 71.7V78.6Q402.6 79 399.7 79.4Q396.9 79.9 393.8 80.2Q390.7 80.6 388.3 80.8Q386 81 385.4 81Q379.6 81 374.9 78Q370.2 74.9 367.5 68.5Q364.8 62.1 364.8 52Q364.8 45.6 365.7 40.3Q366.5 35 367.8 31.7Q369.1 30 371.4 27.9Q373.7 25.9 376.3 24ZM383.7 72V26.1Q383.7 25.2 384.4 23.1Q385.1 21 386 18.6L389 18.7V66.3Q389 66.9 388.4 68.4Q387.8 70 386.7 72ZM404.1 38.5H397.6L396.3 27.5Q395.2 27.2 393.6 26.8Q391.9 26.5 390.4 26.2Q388.8 26 387.9 26Q386.9 26 386.3 26Q385.6 26.1 385.1 26.2L386 18.6Q386.5 18.4 386.8 18.3Q387.2 18.3 387.6 18.3Q389.2 18.3 392.3 18.5Q395.4 18.8 399 19.1Q402.5 19.4 405.3 19.8Z M433.3 81Q422.5 81 416.8 75.8Q411.1 70.5 411.1 59.3Q411.1 54.8 411.9 50.6Q412.6 46.4 413.6 44.4Q414.5 43.2 416.8 41.3Q419 39.5 421.8 37.8Q424.5 36.1 426.8 34.9Q429.1 33.7 430.1 33.7Q440.9 33.7 446.3 39.2Q451.8 44.8 451.8 55Q451.8 60 451.1 64.2Q450.3 68.4 449.4 70.7Q448.6 71.8 446.4 73.5Q444.2 75.2 441.5 77Q438.8 78.7 436.5 79.9Q434.2 81 433.3 81ZM433.6 74.5Q433.9 74.4 435 73.9Q436 73.5 437 73Q437.9 72.5 437.9 72.5Q438.4 70.2 438.9 66.4Q439.4 62.6 439.4 56.4Q439.4 51.8 438.4 48.2Q437.4 44.5 435.2 42.4Q433.1 40.2 429.7 40.2Q428.9 40.2 428.1 40.3Q427.3 40.5 426.4 40.8Q425.2 41.4 424.4 45.9Q423.5 50.4 423.5 57.9Q423.5 64.6 425.1 68.2Q426.6 71.9 428.9 73.2Q431.3 74.5 433.6 74.5Z M465.4 81Q465 81 464.1 80.3Q463.2 79.5 462.3 78.6Q461.4 77.7 461.4 77.4V41.8L457.6 40.3V35.5Q457.6 35.5 459.2 35.2Q460.8 35 463 34.6Q465.1 34.2 467 33.9Q468.8 33.7 469.3 33.7Q469.6 33.7 470.4 34.4Q471.2 35.2 472 36.1Q472.7 37 472.7 37.4V40.6Q473.8 39.6 475.2 38.4Q476.6 37.2 478 36.2Q479.3 35.1 480.3 34.4Q481.3 33.7 481.4 33.7Q486.3 33.7 489.9 35.2Q493.4 36.8 495 40.6Q496.1 39.6 497.5 38.4Q498.8 37.2 500 36.2Q501.3 35.1 502.2 34.4Q503.1 33.7 503.3 33.7Q508.5 33.7 512.1 35.1Q515.7 36.5 517.6 40.1Q519.6 43.6 519.6 49.8V72.9L523.2 74.4V79.1Q523.2 79.1 521.7 79.4Q520.1 79.7 518 80.1Q515.8 80.4 514.1 80.7Q512.3 81 511.9 81Q511.6 81 510.6 80.3Q509.6 79.5 508.7 78.6Q507.9 77.7 507.9 77.4V49.9Q507.9 47.1 507.3 45.6Q506.6 44.1 505.7 43.4Q504.8 42.8 504 42.7Q503.2 42.5 502.7 42.5Q502.5 42.5 501.5 43Q500.6 43.4 499.5 44Q498.4 44.6 497.5 45.1Q496.6 45.6 496.4 45.7V72.9L499.9 74.4V79.1Q499.9 79.1 498.3 79.4Q496.8 79.7 494.7 80.1Q492.6 80.4 490.8 80.7Q489.1 81 488.7 81Q488.4 81 487.4 80.3Q486.4 79.5 485.5 78.6Q484.7 77.7 484.7 77.4V49.9Q484.7 46.2 483.7 44.7Q482.8 43.1 481.6 42.8Q480.4 42.5 479.8 42.5Q479.5 42.5 478.6 43Q477.6 43.4 476.4 44Q475.2 44.6 474.3 45.1Q473.4 45.6 473.1 45.7V72.9L476.6 74.4V79.1Q476.6 79.1 475.1 79.4Q473.5 79.7 471.4 80.1Q469.3 80.4 467.6 80.7Q465.8 81 465.4 81Z M553.1 33.7Q557.6 33.7 561.4 36.1Q565.1 38.6 567.3 43.4Q569.5 48.2 569.5 55.4Q569.5 60.3 568.8 64.4Q568.1 68.5 567.1 70.7Q566.2 71.9 564 73.6Q561.7 75.3 559.1 77Q556.5 78.7 554.2 79.9Q551.9 81 551 81Q550.2 81 548.2 80.8Q546.2 80.5 543.6 80.1V89.9L547.7 91.5V96.4Q546.7 96.7 544.8 97Q543 97.3 540.9 97.6Q538.9 97.9 537.3 98.1Q535.8 98.3 535.3 98.3Q535 98.3 534.1 97.5Q533.3 96.7 532.5 95.9Q531.7 95 531.7 94.6L532.3 77.9V41.7L528.5 40.2V35.5Q529.5 35.3 531.3 35Q533 34.7 534.8 34.4Q536.7 34.1 538.1 33.9Q539.5 33.7 539.9 33.7Q540.3 33.7 541.1 34.4Q542 35.2 542.8 36.1Q543.5 36.9 543.5 37.3V40.7Q545.1 39.4 547.3 37.8Q549.4 36.2 551.2 34.9Q552.9 33.7 553.1 33.7ZM551.6 42.4Q551.3 42.4 549.9 43Q548.5 43.6 546.9 44.4Q545.2 45.2 544 45.8V72.2Q545.4 72.8 547.4 73.5Q549.5 74.1 551.3 74.4Q553.2 74.8 553.9 74.6Q554.9 74.3 555.6 72.5Q556.3 70.7 556.7 66.9Q557.1 63.1 557.1 56.7Q557.1 51.9 556.1 48.7Q555.2 45.6 553.9 44Q552.6 42.4 551.6 42.4Z M583.6 81Q583.3 81 582.2 80.2Q581.1 79.3 580.2 78.4Q579.2 77.5 579.2 77.1V41.5L575.4 40.2V35.5Q575.4 35.5 577 35.2Q578.5 34.9 580.7 34.6Q582.9 34.2 584.7 33.9Q586.5 33.7 586.9 33.7Q587.3 33.7 588.2 34.5Q589.2 35.3 590 36.2Q590.9 37.2 590.9 37.7V73.3L594.6 74.4V79.1Q594.6 79.1 593.1 79.4Q591.6 79.7 589.6 80.1Q587.5 80.4 585.8 80.7Q584 81 583.6 81ZM578.2 17.8Q578.2 17.5 579.2 16.7Q580.3 15.8 581.7 14.7Q583 13.6 584.2 12.9Q585.3 12.1 585.5 12.1Q586 12.1 587.1 13Q588.2 13.9 589.4 15.2Q590.6 16.5 591.5 17.7Q592.3 18.8 592.2 19.3L591.7 21.6Q591.6 22 590.6 22.9Q589.6 23.7 588.3 24.7Q587 25.7 585.8 26.5Q584.7 27.2 584.4 27.2Q583.9 27.2 582.8 26.3Q581.7 25.3 580.5 24Q579.4 22.7 578.6 21.6Q577.8 20.5 577.8 20.1Z M607.1 81Q606.8 81 605.9 80.3Q604.9 79.5 604.1 78.6Q603.2 77.7 603.2 77.4V22.8L599.4 21.3V16.6Q599.4 16.6 600.5 16.4Q601.6 16.3 603.2 16Q604.9 15.7 606.6 15.4Q608.4 15.1 609.7 15Q611 14.8 611.3 14.8Q611.7 14.8 612.5 15.6Q613.4 16.3 614.1 17.2Q614.9 18 614.9 18.4V72.9L618.6 74.4V79.1Q618.6 79.1 617 79.4Q615.4 79.7 613.3 80.1Q611.2 80.4 609.4 80.7Q607.6 81 607.1 81Z M636.6 58.3Q636.6 63.7 638 66.8Q639.4 69.9 641.3 71.1Q643.2 72.4 644.8 72.4Q645.1 72.4 646.7 72.3Q648.3 72.3 650.6 72.2Q652.8 72.1 655 72Q657.2 71.9 658.7 71.8V76.8Q657.1 77.4 654.6 78.1Q652.2 78.8 649.7 79.4Q647.1 80.1 645.1 80.6Q643.1 81 642.3 81Q637.4 81 633.3 78.6Q629.3 76.2 626.8 71.5Q624.4 66.8 624.4 59.8Q624.4 54.9 625.2 50.6Q625.9 46.3 626.9 44.2Q627.8 43 630 41.3Q632.3 39.5 635 37.8Q637.7 36 640 34.8Q642.3 33.7 643.4 33.7Q649 33.7 652.8 35.6Q656.5 37.5 658.4 42.6Q660.2 47.8 660.2 57.5L631.6 60.5V55.7L648.4 52.7Q648.5 47.1 647.3 43.8Q646.2 40.5 642.9 40.3Q642.2 40.2 641.3 40.2Q640.3 40.2 639.5 40.6Q638.2 41.3 637.4 46Q636.6 50.7 636.6 58.3Z M673.4 81Q673 81 672.1 80.3Q671.2 79.5 670.3 78.6Q669.4 77.7 669.4 77.4V41.5L665.6 40.2V35.5Q665.6 35.5 667.2 35.2Q668.7 34.9 670.8 34.6Q672.9 34.2 674.6 33.9Q676.4 33.7 676.8 33.7Q677.2 33.7 678.1 34.5Q679.1 35.3 680 36.3Q680.8 37.3 680.8 37.6L680.7 41.7Q682 40.3 683.3 38.9Q684.6 37.5 685.7 36.3Q686.9 35.1 687.7 34.4Q688.5 33.7 688.8 33.7Q690.3 33.7 692.5 34.2Q694.6 34.7 695.8 35.1Q696 35.6 696.3 36.8Q696.6 38.1 696.6 38.9Q696.6 39.4 696.2 40.6Q695.7 41.7 695.1 43Q694.4 44.3 693.9 45.3Q693.3 46.2 693.1 46.3Q692.6 46.1 691.6 45.6Q690.5 45.2 689.4 44.9Q688.2 44.5 687.3 44.5Q687 44.5 686.3 44.7Q685.6 45 684.7 45.4Q683.8 45.7 682.9 46.2Q682 46.6 681.1 47.1V72.3L686.9 73.9V79Q686.9 79 685.7 79.2Q684.5 79.4 682.6 79.7Q680.7 80 678.7 80.3Q676.7 80.6 675.2 80.8Q673.8 81 673.4 81Z", "x0": 0.3, "w": 697.3, "y0": 11.1, "h": 88.2}, "mono": {"the": "M22.4 29.8Q20.5 29.8 19.2 32Q18 34.2 17.3 37.5Q16.6 40.8 16.4 44.3Q16.1 47.8 16.1 50.4Q16.1 56.4 17.2 61.7Q18.4 67 21.2 70.2Q24 73.5 28.9 73.5L41.9 73.4V78.6Q40.6 79 37.9 79.4Q35.2 79.8 32.2 80.2Q29.3 80.5 27.1 80.7Q24.8 80.9 24.2 80.9Q18.2 80.9 14.2 76.9Q10.2 72.9 8.2 66.3Q6.2 59.7 6.2 52.1Q6.2 46.9 7 43.5Q7.7 40 9.2 36.7Q9.9 35.6 11.4 33.9Q13 32.2 15.3 30.7Q17.6 29.2 20.4 28.7ZM45.4 20.9 43.4 28.7Q41.2 29.5 38.8 30.1Q36.4 30.8 34.2 31.1Q32 31.5 30.2 31.5Q27.7 31.5 26.2 31Q24.7 30.5 23.3 30Q21.9 29.5 19.6 29.5Q19 29.5 18.4 29.5Q17.7 29.6 17.1 29.8L16.9 29.2L1.3 27.5L3.2 18Q9.7 18.8 15.1 19.6Q20.4 20.5 24.3 21Q28.2 21.5 30.1 21.5Q31.5 21.5 33.5 21.3Q35.4 21.2 38.1 20.7Q40.8 20.3 44.2 19.6ZM22.6 73.7V25.3H27.8V68Q27.8 68.6 27.3 70.2Q26.8 71.7 25.7 73.7Z M47.9 20.7V17Q47.9 17 48.8 16.8Q49.6 16.7 50.9 16.4Q52.1 16.2 53.4 15.9Q54.7 15.7 55.7 15.5Q56.7 15.4 57 15.4Q57.3 15.4 58.1 16.1Q59 16.8 59.8 17.5Q60.5 18.3 60.5 18.7L60 41.3L60.5 41.4Q61.8 40.4 63.4 39.2Q65.1 38 66.7 36.9Q68.2 35.8 69.3 35Q70.4 34.3 70.5 34.3Q75.1 34.3 78.3 35.8Q81.5 37.3 83.2 41Q84.9 44.7 84.9 51.2V77.2Q84.9 80.2 83.8 83.6Q82.7 86.9 80.7 89.7Q78.6 92.5 75.6 93.9L72.7 91.5Q74.1 89.2 74.8 86.8Q75.4 84.5 75.6 82.2Q75.8 79.8 75.8 77.6V51.2Q75.8 46.4 74.7 44.5Q73.5 42.5 72.2 42.1Q70.8 41.8 70 41.8Q69.6 41.8 67.6 42.6Q65.6 43.4 63.5 44.3Q61.4 45.2 60.5 45.6V74.1L63.9 75.6V79.3Q63.9 79.3 62.7 79.5Q61.4 79.8 59.7 80.1Q57.9 80.4 56.5 80.7Q55 80.9 54.7 80.9Q54.4 80.9 53.6 80.2Q52.8 79.5 52.1 78.7Q51.4 77.9 51.4 77.6V22.1Z M103.4 58.1Q103.4 64.6 105.2 68Q106.9 71.4 109.1 72.6Q111.3 73.8 112.7 73.8Q113.1 73.8 114.6 73.8Q116.1 73.7 118.1 73.6Q120.1 73.5 122.1 73.4Q124.1 73.3 125.6 73.3V77.4Q123.8 78 121.5 78.6Q119.2 79.2 116.9 79.7Q114.6 80.2 112.8 80.6Q111.1 80.9 110.4 80.9Q106.3 80.9 102.5 78.7Q98.7 76.4 96.2 71.8Q93.8 67.1 93.8 59.9Q93.8 54.9 94.5 50.7Q95.2 46.5 96.2 44.6Q97 43.4 99 41.6Q101.1 39.9 103.5 38.2Q106 36.6 108.1 35.4Q110.2 34.3 111.2 34.3Q116.7 34.3 120.2 36.1Q123.6 37.9 125.3 42.8Q127 47.8 127 57.4L99 60.3V56.5L117.3 53.5Q117.3 47.4 116 43.8Q114.7 40.3 110.4 40.3Q109.6 40.3 108.7 40.4Q107.7 40.5 106.6 41Q105.2 41.7 104.3 46.3Q103.4 51 103.4 58.1Z", "main": "M155.3 24.7V19.8Q156.8 19.6 159 19.3Q161.2 19 163.5 18.8Q165.7 18.5 167.4 18.4Q169 18.3 169.4 18.4Q170.1 18.5 171 19.3Q171.9 20.2 172.5 21.1Q173.2 22 173.3 22.4V71.8L188.9 74.7Q190.1 74.9 190.9 74.3Q191.7 73.8 192.3 72.4Q193 71.1 193.4 69.2Q194.2 65.7 194.5 60.4Q194.7 55.2 194.7 48.8Q194.7 43.7 194.2 39.2Q193.7 34.7 192.6 31.4Q191.6 28.1 190 26.2Q188.5 24.4 186.4 24.6L180.6 25L181.8 18.3H186.8Q190.6 18.3 194.3 19.7Q198 21.2 201 24.6Q204 28 205.9 33.7Q207.7 39.5 207.7 48.1Q207.7 54.3 207.1 59Q206.5 63.7 205.4 67.4Q205.1 68.3 203.6 70Q202.1 71.7 199.9 73.6Q197.7 75.5 195.4 77.2Q193.1 78.8 191 79.9Q189 81 187.8 81Q183.9 81 180 80.9Q176 80.7 172.2 80.4Q168.5 80.1 165 79.5Q164.4 79.4 163.5 78.6Q162.6 77.8 161.8 76.9Q161.1 75.9 161 75.5V26.5ZM180.4 18.3H183.4V68.9Q183.4 69.5 182.8 71Q182.2 72.6 181.1 74.6H178.1V25.9Q178.1 24.9 178.8 22.8Q179.5 20.7 180.4 18.3Z M228.9 26.6Q228.5 30 228.1 33.3Q227.6 36.6 227.4 40.4Q227.2 44.1 227.2 48.9Q227.2 58.1 228.7 63.1Q230.3 68 233 69.9Q235.7 71.8 239.1 71.8L253.3 71.7V78.6Q251.9 79 249 79.4Q246.2 79.9 243.1 80.2Q240 80.6 237.6 80.8Q235.3 81 234.7 81Q228.9 81 224.2 78Q219.5 74.9 216.8 68.5Q214.1 62.1 214.1 52Q214.1 45.6 215 40.3Q215.8 35 217.1 31.7Q218.4 30 220.7 27.9Q223 25.9 225.6 24ZM233 72V26.1Q233 25.2 233.7 23.1Q234.4 21 235.3 18.6L238.3 18.7V66.3Q238.3 66.9 237.7 68.4Q237.1 70 236 72ZM253.4 38.5H246.9L245.6 27.5Q244.5 27.2 242.9 26.8Q241.2 26.5 239.7 26.2Q238.1 26 237.2 26Q236.2 26 235.6 26Q234.9 26.1 234.4 26.2L235.3 18.6Q235.8 18.4 236.1 18.3Q236.5 18.3 236.9 18.3Q238.5 18.3 241.6 18.5Q244.7 18.8 248.3 19.1Q251.8 19.4 254.6 19.8Z", "x0": 0.3, "w": 255.3, "y0": 11.1, "h": 88.2}}


def logo(kind, cls=""):
    g = LOGO[kind]
    c = ("logo " + cls).strip()
    return (f'<svg class="{c}" viewBox="{g["x0"]} {g["y0"]} {g["w"]} {g["h"]}" role="img" aria-label="{SITE_NAME}">'
            f'<path class="the" d="{g["the"]}"/><path d="{g["main"]}"/></svg>')


def masthead(ctx):
    return (f'<header class="mast"><h1><a href="{esc(ctx.href("index.html"))}">{logo("full")}</a></h1>'
            f'<div class="tag"><span class="tag-t"><b>{esc(TAGLINE_B)}</b>{esc(TAGLINE)}</span>'
            f'<button class="theme" type="button" id="theme-toggle" aria-label="Açık/koyu temayı değiştir" '
            f'title="Açık/koyu tema" hidden><span class="ico" aria-hidden="true"></span></button></div></header>')


def footer(ctx):
    return ('<footer><span>The Daily Compiler · Her sabah yayımlanır · '
            f'<a href="{esc(ctx.href("arsiv.html"))}">Arşiv</a> · <a href="{esc(ctx.href("feed.xml"))}">RSS</a> · '
            f'<a href="{esc(ctx.href("hakkinda.html"))}">Hakkında</a></span>'
            '<span>Haberler yapay zeka tarafından kaynaklardan özetlenir ve ayrı bir yapay zeka editörce denetlenir; '
            f'hata olabilir, kaynak linklerine bakın. <a href="{esc(ctx.href("hakkinda.html"))}">Nasıl hazırlanıyor?</a></span></footer>')


# Sayfa boyanmadan önce kayıtlı tema seçimini uygula (yanıp sönmeyi önler)
THEME_BOOT = ("<script>try{var t=localStorage.getItem('dc-theme');"
              "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")


def page(ctx, title, desc, body, canonical=None, og_title=None, og_url=None, base="", published=None):
    can = f'<link rel="canonical" href="{esc(canonical)}">' if canonical else ""
    og = ""
    if og_url or canonical:
        og += f'<meta property="og:url" content="{esc(og_url or canonical)}">\n'
    if base:
        og += (f'<meta property="og:image" content="{esc(base)}assets/og.png">\n'
               '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
               '<meta name="twitter:card" content="summary_large_image">\n')
    if published:
        og += f'<meta property="article:published_time" content="{esc(published)}">\n'
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:locale" content="tr_TR">
{og}<meta name="color-scheme" content="light dark">
{THEME_BOOT}
{can}
<link rel="alternate" type="application/atom+xml" title="{esc(SITE_NAME)}" href="{esc(ctx.href('feed.xml'))}">
<link rel="icon" href="{esc(ctx.href('favicon.ico'))}" sizes="32x32">
<link rel="icon" href="{esc(ctx.href('assets/favicon.svg'))}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{esc(ctx.href('assets/apple-touch-icon.png'))}">
<meta name="theme-color" content="#EEF0EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#151B20" media="(prefers-color-scheme: dark)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,500&family=IBM+Plex+Sans+Condensed:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{esc(asset(ctx, 'assets/style.css'))}">
</head>
<body>
<div class="wrap" lang="tr">
{masthead(ctx)}
{body}
{footer(ctx)}
</div>
<script src="{esc(asset(ctx, 'assets/site.js'))}" defer></script>
</body>
</html>
"""


def render_issue(ctx, cur):
    secs = cur.get("sections") or []
    nav_items = [("manset", "Manşet")] + [(s.get("id"), s.get("title")) for s in secs]
    if cur.get("repos"):
        nav_items.append(("repolar", "GitHub Repoları"))
    if cur.get("briefs"):
        nav_items.append(("kisa", "Kısa Kısa"))
    out = [dial(ctx, cur)]
    out.append('<main id="issue">')
    # Menü üste yapışınca solunda küçük logo belirir (site.js, .nav-sentinel görünümden çıkınca "stuck" sınıfını ekler)
    out.append('<div class="nav-sentinel" aria-hidden="true"></div><nav class="index" aria-label="Bölümler">'
               f'<a class="nav-brand" href="{esc(ctx.href("index.html"))}" tabindex="-1" aria-hidden="true">'
               f'{logo("full", "full")}{logo("mono", "mono")}</a><div class="nav-links">' + "".join(
        f'<a href="#sec-{esc(i)}">{esc(caps(t))}</a>' for i, t in nav_items) + "</div></nav>")

    figs = cur.get("figures") or []
    if figs:
        # ref: "manset" ya da "<bölüm id>-<sıra>" (haberin kendi id'si varsa o); hedef bu sayıda yoksa kutu link olmaz
        targets = {"manset"} if cur.get("lead") else set()
        for s in secs:
            for i, a in enumerate(s.get("articles") or []):
                targets.add(str(a.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}"))
        cells = []
        for f in figs:
            inner = f'<span class="n">{esc(f.get("n"))}</span><span class="l">{rich(f.get("l"))}</span>'
            ref = str(f.get("ref") or "").lstrip("#")
            ref = ref[2:] if ref.startswith("a-") else ref
            if ref in targets:
                cells.append(f'<a class="fig" href="#a-{esc(ref)}">{inner}</a>')
            else:
                cells.append(f'<div class="fig">{inner}</div>')
        out.append('<section class="figs-wrap" aria-label="Günün rakamları"><span class="kicker">'
                   + esc(caps("Günün rakamları")) + '</span><div class="figs">' + "".join(cells) + "</div></section>")

    L = cur.get("lead")
    if L:
        box = ""
        if L.get("box"):
            B = L["box"]
            box = (f'<aside class="box"><span class="kicker">{caps_rich(B.get("kicker") or "Pratik çıkarım")}</span>'
                   f'<h3>{rich(B.get("title"))}</h3><ol>' + "".join(f"<li>{rich(t)}</li>" for t in B.get("items") or []) + "</ol>"
                   + (f'<p class="note">{esc(B.get("note"))}</p>' if B.get("note") else "") + "</aside>")
        # Manşet grafiği dar ekranda metnin altında, geniş ekranda sağ sütunda durur: iki kopya basılır, biri CSS ile gizlenir
        lead_chart = chart(L.get("chart"))
        lc = lambda cls: f'<div class="{cls}">{lead_chart}</div>' if lead_chart else ""
        out.append(
            f'<section class="lead" id="sec-manset"><div id="a-manset">'
            f'{kicker(L.get("kicker"), L.get("alert"), "Manşet")}'
            f'<h2>{rich(L.get("headline"))}</h2>'
            + (f'<p class="deck">{rich(L.get("deck"))}</p>' if L.get("deck") else "")
            + '<div class="cols">' + "".join(f"<p>{rich(p)}</p>" for p in L.get("paragraphs") or []) + "</div>"
            + lc("lc-main") + sources(ctx, L.get("sources")) + f'</div><div class="lead-side">{box}{lc("lc-side")}{toc(secs)}</div></section>')

    out.append(pattern(cur))

    for s in secs:
        sid = s.get("id") or "bolum"
        arts = section_articles(ctx, s)
        sub = f'<p>{rich(s.get("subtitle"))}</p>' if s.get("subtitle") else ""
        out.append(f'<section class="sec" id="sec-{esc(sid)}"><div class="sec-h"><h2>{esc(typo(s.get("title")))}</h2>{sub}</div>'
                   f'<div class="grid">{arts}</div></section>')

    R = cur.get("repos")
    if R and R.get("items"):
        cards = []
        for r in R["items"]:
            name = (f'<a class="name" href="{esc(r.get("url"))}" target="_blank" rel="noopener">{esc(r.get("name"))}</a>'
                    if re.match(r"^https?://", r.get("url") or "") else f'<span class="name">{esc(r.get("name"))}</span>')
            meta = r.get("meta") or " · ".join(x for x in [r.get("lang"), r.get("cat")] if x)
            cards.append(f'<div class="repo">{name}<span class="stars">{"★ " + esc(r["stars"]) if r.get("stars") else ""}</span>'
                         f'<p class="why">{rich(r.get("why"))}</p>' + (f'<span class="meta">{caps_rich(meta)}</span>' if meta else "") + "</div>")
        sub = R.get("subtitle") or "Trending listelerinden seçme · yıldız sayıları kaynak tarihindeki değerlerdir"
        out.append(f'<section class="sec" id="sec-repolar"><div class="sec-h"><h2>Öne Çıkan GitHub Repoları</h2><p>{rich(sub)}</p></div>'
                   f'<div class="repos">{"".join(cards)}</div>{sources(ctx, R.get("sources"))}</section>')

    briefs = cur.get("briefs") or []
    if briefs:
        ps = []
        for b in briefs:
            u = b.get("url") or ""
            tail = (" " + ref_link(ctx, "önceki sayı", u)) if u.startswith("#") else (
                f'\u00a0<a href="{esc(u)}" target="_blank" rel="noopener" aria-label="Kaynak">↗</a>' if re.match(r"^https?://", u) else "")
            ps.append(f'<p><b>{caps_rich(b.get("tag"))}</b>{rich(b.get("text"))}{tail}</p>')
        out.append(f'<section class="sec" id="sec-kisa"><div class="sec-h"><h2>Kısa Kısa</h2></div><div class="briefs">{"".join(ps)}</div></section>')
    out.append(end_nav(ctx, cur))
    out.append("</main>")
    return "\n".join(out)


def toc(secs):
    """Manşetin yanında, kutunun altında: her bölümün ilk haberi (yalnızca geniş ekranda görünür)."""
    items = []
    for s in secs:
        A = s.get("articles") or []
        if A and A[0].get("headline"):
            items.append(f'<li><a href="#a-{esc(art_id(s, 0, A[0]))}"><span class="ts">{esc(caps(s.get("title")))}</span>'
                         f'<span class="th">{rich(A[0].get("headline"))}</span></a></li>')
    if not items:
        return ""
    return f'<nav class="toc" aria-label="Bu sayıda"><span class="kicker">{esc(caps("Bu sayıda"))}</span><ol>{"".join(items)}</ol></nav>'


def end_nav(ctx, cur):
    """Sayı sonu: önceki/sonraki sayının manşeti ve başa dönüş."""
    issues = ctx.issues
    idx = next(i for i, x in enumerate(issues) if x["date"] == cur["date"])
    older = issues[idx + 1] if idx + 1 < len(issues) else None
    newer = issues[idx - 1] if idx > 0 else None

    def cell(it, cls, label):
        if not it:
            return f'<span class="{cls}"></span>'
        head = (it.get("lead") or {}).get("headline") or long_date(it["date"])
        return (f'<a class="{cls}" href="{esc(ctx.href(issue_path(it["date"])))}"><span class="kicker">{esc(caps(label + " · " + short_date(it["date"])))}</span>'
                f'<span class="en-h">{rich(head)}</span></a>')

    right = cell(newer, "en-next", "Sonraki sayı") if newer else (
        f'<a class="en-next" href="{esc(ctx.href("arsiv.html"))}"><span class="kicker">{esc(caps("Arşiv"))}</span>'
        '<span class="en-h">Tüm sayılar</span></a>')
    return (f'<nav class="endnav" aria-label="Sayı sonu">{cell(older, "en-prev", "Önceki sayı")}'
            f'<a class="en-top" href="#" aria-label="Sayfanın başına dön">↑ {esc(caps("Başa dön"))}</a>{right}</nav>')


def render_archive(ctx):
    months = {}
    for it in ctx.issues:
        d = d_of(it["date"])
        months.setdefault((d.year, d.month), []).append(it)
    blocks = []
    for (y, m), items in months.items():
        lis = "".join(
            f'<li><span class="ad">{esc(DAYS_3[d_of(i["date"]).weekday()] + ", " + short_date(i["date"]))}</span>'
            f'<a href="{esc(ctx.href(issue_path(i["date"])))}">{rich((i.get("lead") or {}).get("headline") or long_date(i["date"]))}</a>'
            f'<span class="an">{esc(caps("Sayı " + num3(i.get("number"))))}</span></li>' for i in items)
        blocks.append(f'<section class="arc-month"><h2>{MONTHS_LONG[m - 1]} {y}</h2><ul class="arc-list">{lis}</ul></section>')
    return f'<main id="issue" class="arc">{"".join(blocks)}</main>'


def render_about(ctx):
    return f"""<main id="issue" class="about">
<h2>Hakkında</h2>
<p>The Daily Compiler; yazılım, yapay zeka ve güvenlik haberlerini her sabah tek sayfada toplayan günlük bir gazetedir. Kişisel, ticari olmayan bir projedir; reklam ya da sponsorlu içerik yoktur.</p>
<h3>Nasıl hazırlanıyor?</h3>
<p>Her sayı otomatik olarak, bir yapay zeka modeli (Anthropic Claude) tarafından hazırlanır. Model son 24–48 saatin haberlerini tarar (Pazartesi sayılarında hafta sonunu da kapsar), asıl kaynakları okur ve haberleri kendi cümleleriyle özetler. Ardından ayrı bir yapay zeka “editör”, taslağı kaynak linklerini yeniden açarak denetler; doğrulanamayan bilgi çıkarılır ya da etiketlenir.</p>
<p>Sayılar yayımlanmadan önce bir insan tarafından tek tek okunmaz. Bu yüzden hata olabilir: bir haber sizin için önemliyse, altındaki kaynak linkinden asıl metne bakın.</p>
<p>Gazeteyi yazan model Anthropic’in ürünü olduğu için Anthropic ve Claude haberlerinde bir çıkar çatışması vardır. Bu haberlere de diğer şirketlerle aynı etiketler ve çekinceler uygulanır; bir şirket, manşet dışında bir sayıda en fazla iki haber ve bir kısa haberle yer alır.</p>
<h3>Etiketler</h3>
<ul>
<li><span class="prov prov-claim">İDDİA</span> tek kaynağa dayanan ya da bağımsız olarak doğrulanmamış haber.</li>
<li><span class="prov prov-company">ŞİRKET BEYANI</span> bir şirketin yalnızca kendisi hakkındaki ölçümü ya da açıklaması (kendi benchmark’ı, kendi vaka çalışması).</li>
<li><b>Pratik çıkarım</b>: manşetin yanındaki kutu editoryal öneridir, haberin parçası değildir.</li>
<li><b>↩ ile başlayan kaynaklar</b>: önceki bir sayıdaki habere iç atıftır.</li>
</ul>
<h3>Takip</h3>
<p>Yeni sayılar her sabah yayımlanır; tüm sayılar <a href="{esc(ctx.href("arsiv.html"))}">arşivde</a> kalır. Bir okuyucu uygulamasıyla izlemek için <a href="{esc(ctx.href("feed.xml"))}">RSS akışını</a> kullanabilirsiniz.</p>
</main>"""


def render_feed(issues, base):
    """Atom akışı: son 30 sayı. Zaman damgaları sayı tarihinden türetilir (yeniden üretim dosyayı değiştirmesin)."""
    x = lambda t: html.escape(plain(t), quote=False)
    stamp = lambda iso: f"{iso}T07:11:00+03:00"
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="tr">',
           f"<title>{x(SITE_NAME)}</title>", f"<subtitle>{x(TAGLINE_B)} · {x(TAGLINE)}</subtitle>",
           f'<link href="{esc(base)}"/>', f'<link rel="self" type="application/atom+xml" href="{esc(base)}feed.xml"/>',
           f"<id>{esc(base)}</id>", f"<updated>{stamp(issues[0]['date'])}</updated>",
           f"<author><name>{x(SITE_NAME)}</name></author>"]
    for it in issues[:30]:
        L = it.get("lead") or {}
        url = base + issue_path(it["date"])
        label = it.get("dateLabel") or long_date(it["date"])
        heads = [(L.get("headline"), "manset")] if L.get("headline") else []
        for s in it.get("sections") or []:
            for i, a in enumerate(s.get("articles") or []):
                heads.append((a.get("headline"), str(a.get("id") or f"{s.get('id') or 'bolum'}-{i + 1}")))
        body = (f"<p>{x(L.get('deck'))}</p>" if L.get("deck") else "") + "<ul>" + "".join(
            f'<li><a href="{esc(url)}#a-{esc(aid)}">{x(h)}</a></li>' for h, aid in heads if h) + "</ul>"
        out += ["<entry>", f"<title>{x(L.get('headline') or label)}</title>", f'<link href="{esc(url)}"/>',
                f"<id>{esc(url)}</id>", f"<updated>{stamp(it['date'])}</updated>",
                f"<summary>{x('Sayı ' + num3(it.get('number')) + ' · ' + label + (' · ' + L['deck'] if L.get('deck') else ''))}</summary>",
                f'<content type="html">{html.escape(body, quote=False)}</content>', "</entry>"]
    out.append("</feed>")
    return "\n".join(out) + "\n"


# Sekme ikonu: logodaki "D" (çizim olarak; yazı tipine bağlı değil) ve masthead çizgisine gönderme yapan turkuaz çizgi.
# Koyu temada renkler tersine döner. favicon.ico ve assets/apple-touch-icon.png aynı çizimin sabit kopyalarıdır.
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><style>.b{fill:#18222B}.f{fill:#EEF0EC}.a{fill:#5FB3B3}@media (prefers-color-scheme:dark){.b{fill:#EEF0EC}.f{fill:#18222B}.a{fill:#0F5E63}}</style><rect class="b" width="64" height="64" rx="10"/><path class="f" d="M17.4 14.59V11.84Q18.25 11.72 19.47 11.57Q20.7 11.42 21.95 11.28Q23.2 11.14 24.13 11.07Q25.05 11 25.29 11.04Q25.68 11.13 26.16 11.59Q26.64 12.05 27.01 12.57Q27.38 13.09 27.43 13.32V40.87L36.16 42.49Q36.78 42.59 37.24 42.26Q37.7 41.94 38.06 41.2Q38.41 40.46 38.64 39.4Q39.09 37.45 39.24 34.51Q39.38 31.58 39.38 28.02Q39.38 25.17 39.09 22.67Q38.79 20.17 38.21 18.31Q37.63 16.45 36.77 15.43Q35.91 14.4 34.75 14.51L31.5 14.76L32.2 11H34.94Q37.06 11 39.13 11.81Q41.2 12.62 42.89 14.51Q44.58 16.4 45.59 19.61Q46.6 22.81 46.6 27.62Q46.6 31.07 46.29 33.7Q45.98 36.34 45.35 38.39Q45.17 38.92 44.34 39.84Q43.51 40.77 42.29 41.83Q41.07 42.89 39.76 43.83Q38.46 44.77 37.33 45.39Q36.19 46 35.52 46Q33.36 46 31.15 45.92Q28.94 45.83 26.84 45.64Q24.74 45.45 22.8 45.16Q22.45 45.09 21.95 44.64Q21.45 44.2 21.04 43.68Q20.63 43.16 20.59 42.92V15.61ZM31.4 11H33.06V39.23Q33.06 39.56 32.72 40.43Q32.39 41.29 31.78 42.41H30.12V15.26Q30.12 14.71 30.51 13.53Q30.91 12.35 31.4 11Z"/><rect class="a" x="13" y="52" width="38" height="4"/></svg>"""


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    issues = load_issues()
    if not issues:
        sys.exit("issues/ klasöründe sayı yok")
    base = ""
    if os.path.exists(os.path.join(ROOT, "CNAME")):
        base = "https://" + open(os.path.join(ROOT, "CNAME")).read().strip() + "/"
    # eski sayfaları temizle (silinmiş bir JSON'un sayfası kalmasın)
    for f in glob.glob(os.path.join(ROOT, "sayi", "*.html")):
        os.remove(f)
    for it in issues:
        ctx = Ctx(issues, 1)
        L = it.get("lead") or {}
        label = it.get("dateLabel") or long_date(it["date"])
        head = plain(L.get("headline"))
        # Sekme ve paylaşım başlığı: önce manşet, sonra gazete adı ve tarih
        title = f"{head} · {SITE_NAME}, {short_date(it['date'])}" if head else f"{SITE_NAME} · {label}"
        desc = plain(L.get("deck")) or head or TAGLINE
        write(issue_path(it["date"]), page(ctx, title, desc, render_issue(ctx, it),
                                           base + issue_path(it["date"]) if base else None,
                                           og_title=head or title, base=base, published=f"{it['date']}T07:11:00+03:00"))
    latest = issues[0]
    ctx = Ctx(issues, 0)
    L = latest.get("lead") or {}
    head = plain(L.get("headline"))
    write("index.html", page(ctx, f"{SITE_NAME} · {TAGLINE_B}", plain(L.get("deck")) or head or TAGLINE,
                             render_issue(ctx, latest), base + issue_path(latest["date"]) if base else None,
                             og_title=f"{SITE_NAME} · {head}" if head else SITE_NAME, og_url=base or None, base=base))
    write("arsiv.html", page(ctx, f"Arşiv · {SITE_NAME}", "Tüm sayılar", render_archive(ctx),
                             base + "arsiv.html" if base else None, base=base))
    write("hakkinda.html", page(ctx, f"Hakkında · {SITE_NAME}", "The Daily Compiler nasıl hazırlanıyor, etiketler ne anlama geliyor",
                                render_about(ctx), base + "hakkinda.html" if base else None, base=base))
    if base:
        write("feed.xml", render_feed(issues, base))
    write("assets/favicon.svg", FAVICON)
    # sayı listesi (otomasyon ve iç atıf kontrolü için)
    write("issues/index.json", json.dumps(
        [{"date": i["date"], "number": i.get("number"), "headline": (i.get("lead") or {}).get("headline")} for i in issues],
        ensure_ascii=False, indent=1))
    print(f"{len(issues)} sayı üretildi · son sayı {latest['date']}")


if __name__ == "__main__":
    main()
