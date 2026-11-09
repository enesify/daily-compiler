# The Daily Compiler · repo notları

- Her sayının içeriği `issues/YYYY-MM-DD.json` dosyasıdır. Sayfalar `python3 build.py` ile üretilir; üretilen dosyalar elle düzenlenmez.
- `build.py` her çalıştığında şu dosyaları yeniden yazar: `index.html`, `sayi/*.html`, `arsiv.html`, `hakkinda.html`, `feed.xml`, `issues/index.json`, `assets/favicon.svg`.
- Yeni bir sayı eklendiğinde şunların değişmesi BEKLENİR ve birlikte commit edilir: yeni `issues/<tarih>.json`, `issues/index.json`, `index.html`, `arsiv.html`, `feed.xml` ve `sayi/` altındaki sayfalar. `feed.xml` (RSS akışı) her yeni sayıda değişir; bu bir sorun değildir.
- `hakkinda.html`, `assets/og.png`, `assets/style.css`, `assets/site.js` yeni sayı eklenirken değişmez.
- `figures[]` öğelerindeki `ref` alanı (`"manset"` ya da `"<bölüm id>-<sıra>"`, ör. `"java-1"`) rakam kutusunu o habere link yapar; hedef yoksa kutu link olmadan basılır.
