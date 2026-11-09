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


def article(ctx, a, aid):
    cls = f"s{a.get('size') or 4}" + (" big" if a.get("big") else "")
    k = f'<span class="kicker{" alert" if a.get("alert") else ""}">{caps_rich(a.get("kicker"))}</span>' if a.get("kicker") else ""
    pill = f'<span class="pill">{caps_rich(a.get("pill"))}</span>' if a.get("pill") else ""
    body = "".join(f"<p>{rich(p)}</p>" for p in a.get("paragraphs") or [])
    # stat: büyük haberlerde isteğe bağlı tek iri rakam {n, l}; grafik varsa basılmaz
    st = a.get("stat")
    stat = ""
    if a.get("big") and isinstance(st, dict) and st.get("n") and not chart(a.get("chart")):
        stat = f'<p class="stat"><span class="n">{esc(typo(st.get("n")))}</span><span class="l">{rich(st.get("l"))}</span></p>'
    # Telefonda küçük haberlerin metni üç satırda kesilir; site.js gerekirse bu düğmeyi gösterir
    more = "" if a.get("big") else '<button class="more" type="button" aria-expanded="false" hidden>Devamı</button>'
    return (f'<article class="{cls}" id="a-{esc(aid)}">{k}<h3>{pill}{rich(a.get("headline"))}</h3>{stat}'
            f'<div class="body">{body}</div>{more}{chart(a.get("chart"))}{sources(ctx, a.get("sources"))}</article>')


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


def masthead(ctx):
    return (f'<header class="mast"><h1><a href="{esc(ctx.href("index.html"))}"><span class="the">The</span>Daily Compiler</a></h1>'
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
<link rel="icon" href="{esc(ctx.href('assets/favicon.svg'))}" type="image/svg+xml">
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
               '<span class="the">The</span><span class="full">Daily Compiler</span><span class="mono">DC</span></a><div class="nav-links">' + "".join(
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
        out.append(
            f'<section class="lead" id="sec-manset"><div id="a-manset">'
            f'<span class="kicker{" alert" if L.get("alert") else ""}">{caps_rich(L.get("kicker") or "Manşet")}</span>'
            f'<h2>{rich(L.get("headline"))}</h2>'
            + (f'<p class="deck">{rich(L.get("deck"))}</p>' if L.get("deck") else "")
            + '<div class="cols">' + "".join(f"<p>{rich(p)}</p>" for p in L.get("paragraphs") or []) + "</div>"
            + chart(L.get("chart")) + sources(ctx, L.get("sources")) + f'</div><div class="lead-side">{box}{toc(secs)}</div></section>')

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
                f' <a href="{esc(u)}" target="_blank" rel="noopener" aria-label="Kaynak">↗</a>' if re.match(r"^https?://", u) else "")
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
<h3>Etiketler</h3>
<ul>
<li><b>İddia</b>: tek kaynağa dayanan ya da bağımsız olarak doğrulanmamış haber.</li>
<li><b>Şirket beyanı</b>: bir şirketin yalnızca kendisi hakkındaki ölçümü ya da açıklaması (kendi benchmark'ı, kendi vaka çalışması).</li>
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


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#18222B"/><text x="32" y="46" text-anchor="middle" font-family="Georgia,serif" font-size="40" font-weight="700" fill="#EEF0EC">D</text><text x="15" y="22" font-family="Georgia,serif" font-style="italic" font-size="11" fill="#5FB3B3">The</text></svg>"""


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
