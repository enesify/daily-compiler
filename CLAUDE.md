# The Daily Compiler · repo notları

- Yazım ve seçim kuralları `kurallar/KURALLAR.md`, editörün görevi `kurallar/EDITOR.md`, JSON biçim örneği `kurallar/ornek.json` dosyasındadır. Günlük sayıyı hazırlayan oturum bu dosyaları, `tools/`, `build.py` ve `assets/` altını değiştirmez; yalnızca yeni sayı dosyasını ekler ve gerektiğinde `data/modeller.json` dosyasını yeniler.
- `python3 tools/ozet.py --out <klasör>` yeni sayıdan önce gereken özeti verir (tarih, sıradaki numara, son 3 sayının başlıkları, olası açık uçlar). `python3 tools/kontrol.py <dosya>` bir sayı dosyasını ölçülebilir kurallara göre denetler; HATA çıkarsa yayımlanmaz.
- Modeller: `data/modeller.json`, `modeller.html` sayfasının ve her sayıdaki “Modeller” bandının verisidir. Sayıyı yayımlamadan önce `python3 tools/modeller.py --yas 7` çalıştırılır; çıktıda `GÜNCELLE` varsa ya da günün sayısında yeni bir model sürümü haberi varsa `.claude/skills/modeller-guncelle/SKILL.md` adımları uygulanır. `HATA` çıkarsa veri dosyası eski haline döndürülür; sayı yine yayımlanır.
- Her sayının içeriği `issues/YYYY-MM-DD.json` dosyasıdır. Sayfalar `python3 build.py` ile üretilir; üretilen dosyalar elle düzenlenmez.
- `build.py` her çalıştığında şu dosyaları yeniden yazar: `index.html`, `sayi/*.html`, `arsiv.html`, `hakkinda.html`, `modeller.html`, `feed.xml`, `issues/index.json`, `assets/favicon.svg`.
- Yeni bir sayı eklendiğinde şunların değişmesi BEKLENİR ve birlikte commit edilir: yeni `issues/<tarih>.json`, `issues/index.json`, `index.html`, `arsiv.html`, `feed.xml` ve `sayi/` altındaki sayfalar. `feed.xml` (RSS akışı) her yeni sayıda değişir; bu bir sorun değildir.
- `hakkinda.html`, `assets/modeller.js`, `assets/og.png`, `assets/apple-touch-icon.png`, `favicon.ico`, `assets/style.css`, `assets/site.js` yeni sayı eklenirken değişmez. `modeller.html` yalnızca `data/modeller.json` değiştiğinde değişir.
- `figures[]` öğelerindeki `ref` alanı (`"manset"` ya da `"<bölüm id>-<sıra>"`, ör. `"java-1"`) rakam kutusunu o habere link yapar; hedef yoksa kutu link olmadan basılır.
- Büyük haberlerde (`big: true`) isteğe bağlı `stat: {n, l}` alanı başlığın altına iri bir rakam basar; grafik varsa basılmaz.
- Haberlerde isteğe bağlı `why` alanı (tek cümle) “Neden önemli” etiketiyle metinden ayrı basılır. Sayının kökünde isteğe bağlı `pattern: {title, text, refs[]}` alanı manşetin altına “Günün örüntüsü” notu basar; `refs` haber çapalarıdır (`"java-2"` gibi).
- Bölümler JSON'daki `sections` dizisinden gelir; menü bu diziden kendiliğinden oluşur.
- `build.py` metne tipografik düzeltme uygular (kesme işareti ’, sayı aralıklarında kısa çizgi –); JSON'da düz `'` ve `-` yazılır.
- Sayfalar `assets/style.css` ve `assets/site.js` dosyalarını içerik özetiyle (`?v=...`) çağırır; bu dosyalar değişmedikçe özet de değişmez.
