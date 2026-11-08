# The Daily Compiler

Her sabah otomatik hazırlanan, yazılım · yapay zeka · güvenlik gazetesi.

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

## Yeni sayı ekleme

```bash
cp yeni-sayi.json issues/2026-11-09.json
python3 build.py
git add -A && git commit -m "Sayı 007 · 9 Kasım 2026" && git push
```

Tasarım değiştiğinde `python3 build.py` tüm arşivi yeni tasarımla yeniden üretir.

## İç atıflar

Bir kaynağın `url` alanı `#YYYY-MM-DD-<bölüm id>-<sıra>` ise (ör. `#2026-11-07-is-4`), o sayıdaki habere link olur. Manşet için `#YYYY-MM-DD-manset`.

## Özel alan adı

Repo köküne alan adını içeren bir `CNAME` dosyası eklenir (ör. `compiler.ornek.com`); `build.py` canonical linkleri bu adresle üretir.
