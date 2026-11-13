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
| `tools/modeller.py` | `data/modeller.json` dosyasını (Modeller sayfasının verisi) denetler; `--yas 7` ile güncelleme gerekip gerekmediğini söyler |
| `.claude/skills/modeller-guncelle/` | Modeller verisinin hangi tablolardan, hangi kurallarla yenileneceği |

Kurallar değişecekse bu dosyalar düzenlenir; zamanlanmış görevin prompt'u yalnızca iş akışını içerir.

## Rakam şeridi

`figures[]` öğesine `ref` alanı eklenirse (`"manset"` ya da `"<bölüm id>-<sıra>"`, ör. `"java-1"`), rakam kutusu o habere link olur. Hedef o sayıda yoksa kutu link olmadan basılır.

## İri rakam

Büyük haberlerde (`big: true`) `stat: {"n": "%65-80", "l": "açıklama"}` alanı başlığın altına iri bir rakam basar; haberde grafik varsa basılmaz.

## Tipografi

`build.py` metinde düz kesme işaretini `’`, sayı ve saat aralıklarındaki tireyi `–` yapar (CVE numaraları ve ISO tarihler hariç); kod parçalarına ve linklere dokunmaz. JSON'da düz `'` ve `-` yazmaya devam edilir.

## Tema

Sayfa sistemin açık/koyu ayarını izler; masthead'deki düğmeyle yapılan seçim tarayıcıda (`localStorage`, `dc-theme`) saklanır.

## Özel alan adı

Repo köküne alan adını içeren bir `CNAME` dosyası eklenir (ör. `compiler.ornek.com`); `build.py` canonical linkleri bu adresle üretir.
