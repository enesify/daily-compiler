# The Daily Compiler

Her sabah otomatik hazırlanan, yazılım · yapay zekâ · güvenlik gazetesi.

## Yapı

| Yol | Ne |
| --- | --- |
| `issues/YYYY-MM-DD.json` | Her sayının içeriği (tek doğruluk kaynağı) |
| `build.py` | JSON'lardan statik sayfaları üretir (yalnızca Python 3, bağımlılık yok) |
| `assets/style.css`, `assets/site.js` | Tasarım ve küçük etkileşimler |
| `index.html` | Son sayı (üretilir) |
| `sayi/YYYY-MM-DD.html` | Tek tek sayılar (üretilir) |
| `arsiv.html` | Ay ay tüm sayılar (üretilir) |
| `issues/index.json` | Sayı listesi (üretilir) |
| `feed.xml` | Atom/RSS akışı, son 30 sayı (üretilir; her yeni sayıda değişir) |
| `hakkinda.html` | Gazetenin nasıl hazırlandığı ve etiketler (üretilir; metni `build.py` içinde) |
| `assets/og.png` | Paylaşım kartı görseli (sabit) |

## Yeni sayı ekleme

```bash
cp yeni-sayi.json issues/2026-11-09.json
python3 build.py
git add -A && git commit -m "Sayı 007 · 9 Kasım 2026" && git push
```

Tasarım değiştiğinde `python3 build.py` tüm arşivi yeni tasarımla yeniden üretir.

## İç atıflar

Bir kaynağın `url` alanı `#YYYY-MM-DD-<bölüm id>-<sıra>` ise (ör. `#2026-11-07-is-4`), o sayıdaki habere link olur. Manşet için `#YYYY-MM-DD-manset`.

## Kurallar ve araçlar

| Yol | Ne |
|---|---|
| `kurallar/KURALLAR.md` | Yazım ve seçim kuralları (okuyucu, bölümler, uzunluk, kaynak, dil, JSON alanları) |
| `kurallar/EDITOR.md` | Editör agent'ın görevi |
| `kurallar/ornek.json` | JSON biçim örneği |
| `tools/ozet.py` | Yeni sayıdan önce: tarih, sıradaki numara, son sayıların başlıkları, açık uçlar |
| `tools/kontrol.py` | Bir sayı dosyasını ölçülebilir kurallara göre denetler |
| `tools/modeller.py` | `data/modeller.json` dosyasını (Benchmark sayfasının verisi) denetler; `--yas 7` ile güncelleme gerekip gerekmediğini söyler |
| `.claude/skills/modeller-guncelle/` | Benchmark verisinin hangi tablolardan, hangi kurallarla yenileneceği |

Kurallar değişecekse bu dosyalar düzenlenir; zamanlanmış görevin prompt'u yalnızca iş akışını içerir.

## Takvim, Bugün yamala, düzeltmeler

- `calendar[]` (`{date, text, ref?, url?}`): sayının başında önümüzdeki 30 günün tarihleri. `ref` bu sayıdaki habere, `url` dış kaynağa link verir. Sayı tarihinden önceki öğeler basılmaz. Eski sayılardaki `figures[]` rakam şeridi olarak basılmaya devam eder; yeni sayılarda yazılmaz.
- Güvenlik bölümündeki `patch[]` (`{text, url}`, 1-3 madde) bölümün başına “Bugün yamala” listesi basar.
- `corrections[]` (`{date, ref, text}`) sayının sonunda “Düzeltme” bölümü olarak basılır; bütün düzeltmeler Hakkında sayfasında da listelenir.
- Arşiv sayfası haber başlıklarında, kısa haberlerde ve repo adlarında arama yapar (veri sayfaya gömülüdür).

## İri rakam

Büyük haberlerde (`big: true`) `stat: {"n": "%65-80", "l": "açıklama"}` alanı başlığın altına iri bir rakam basar; haberde grafik varsa basılmaz.

## Tipografi

`build.py` metinde düz kesme işaretini `’`, sayı ve saat aralıklarındaki tireyi `–` yapar (CVE numaraları ve ISO tarihler hariç); kod parçalarına ve linklere dokunmaz. JSON'da düz `'` ve `-` yazmaya devam edilir.

## Tema

Sayfa sistemin açık/koyu ayarını izler; masthead'deki düğmeyle yapılan seçim tarayıcıda (`localStorage`, `dc-theme`) saklanır.

## Özel alan adı

Repo köküne alan adını içeren bir `CNAME` dosyası eklenir (ör. `compiler.ornek.com`); `build.py` canonical linkleri bu adresle üretir.
