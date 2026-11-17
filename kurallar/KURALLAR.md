# The Daily Compiler · yayın kuralları

Bu dosya gazetenin yazım ve seçim kurallarıdır. Yazar da editör de buna göre çalışır; yazar bu dosyayı değiştirmez.

Kurallar çatıştığında öncelik sırası: **doğruluk**, **okuyucu için önem**, **dil**, **biçim**. Uzunluk, sayı, ızgara ve alan kurallarının çoğunu `tools/kontrol.py` denetler; bunların sayıları 7. bölümdeki tabloda toplu olarak durur.

## 1. Okuyucu

Okuyucu, JVM ekosisteminde (Java, Maven, Spring Boot mikroservisleri) üretim sistemleri geliştiren ve ekibinde AI destekli geliştirme araçlarını kullanan deneyimli yazılımcılar ve teknik liderlerdir. Güvenlik açıkları, tooling kararları ve AI destekli geliştirme onlar için özellikle önemlidir.

Bu tanım seçimi ve önceliği yönlendiren bir mercektir; gazete herkese açıktır. Metinde belirli bir kişiye, şirkete ya da ekibe hitap etme. Okuyucuya her haberde şu soruların cevabını ver: ne değişti, beni etkiliyor mu, ne yapmalıyım ve ne zamana kadar.

## 2. Kaynak ve doğruluk (en önemli kurallar)

- **Kaynakta yazmayan yazılmaz.** Haber metninde (başlık, deck, paragraflar, Takvim, Bugün yamala, stat, grafik, kısa haberler, repolar) kaynağında açıkça yazmayan hiçbir ayrıntı, yöntem, sayı ya da nitelendirme olmaz. “Mantıklı” diye ekleme; emin değilsen yazma. İstisnalar: kısa jargon açıklamaları (genel bilinen tanım) ve editoryal alanlar (Pratik çıkarım, why, pattern). Editoryal alanlar da yeni olgu getirmez.
- **Asıl kaynak.** Her haberde en az bir gerçek kaynak linki olur; uydurma link yok. Linklerde asıl kaynağı ver: resmi duyuru, advisory, makale, sürüm notu, birincil haber. Özet ve toplayıcı siteler (aiweekly.co, theneuron.ai, Releasebot vb.) yalnızca haberi bulmak içindir. Haber başına en fazla 4 kaynak: önce birincil, sonra en güçlü bağımsız kaynak. Forum, toplayıcı ve SEO sitelerini daha iyisi varken kullanma. Asıl kaynağa ulaşamadıysan haberi atla ya da “İddia” etiketiyle Kısa Kısa'ya yaz.
- **Etiketler.** Tek kaynaklı ve doğrulanmamış iddia: kicker “İddia · Konu”; başlık kesin olgu gibi yazılmaz, kaynağa atfedilir (“Sentra: Qubole üzerinden müşteri AWS hesaplarına girildi”). Bir şirketin yalnızca kendisi hakkındaki ölçüm ve beyanı (kendi benchmark'ı, kendi tasarrufu, kendi vaka çalışması): kicker “Şirket beyanı · Konu”; başlıktaki ölçüm şirkete atfedilir.
- **Bağımsız kaynakta şartlar.** Ürün ya da hizmet duyurusu manşet veya büyük haber olacaksa, hangi şirketten olursa olsun, duyuru dışında en az bir bağımsız kaynakta şartları, sınırları ve eleştirileri ara: lisans ve kullanım şartları, veri ve telemetri, destek yükümlülükleri, fiyat. Duyuruyu yalnızca aktaran yazı bağımsız kaynak sayılmaz. Bulduğun önemli şart habere girer.
- **Rakamlar.** Rakamları kaynakta yazdığı gibi ver. Yüzde fark, oran, “kat” gibi türetilmiş bir rakamı sen hesaplıyorsan girdileri kaynaktan al, hesabı iki kez yap, yuvarlarken “yaklaşık” de. Kaynağın hesabını kullanıyorsan ona atfet ve kendi girdilerinle çelişmediğini kontrol et. Aynı rakam sayı boyunca ve önceki sayılarla tutarlı olmalı. Benchmark sayfasındaki (`data/modeller.json`) bir ölçümü haberde veriyorsan değer aynı olmalı; kaynak başka bir ayarın ya da sürümün sonucunu veriyorsa bunu yaz.
- **Eşit muamele.** Bu gazeteyi Anthropic'in Claude modeli yazıyor. Anthropic ve Claude haberlerine diğer şirketlerle aynı etiketleri, çekinceleri ve ölçütleri uygula; övgü sıfatı kullanma. Modelleri ya da ürünleri karşılaştırırken her birine aynı rakamı ver; hiçbirini (Claude dahil) rakamsız “en pahalısı”, “en iyisi” gibi bir ifadeyle geçme.
- **Çekince ve yorum.** Kaynağın kendi çekincesi (tekrar üretilemedi, tartışmalı) habere yazılır. Kendi yorumunu haber cümlesi gibi yazma; yorum yalnızca editoryal alanlarda olur. Kaynaktan 15 kelimeyi aşan alıntı yapma. Siyasi konularda yorum katma.

## 3. Araştırma

- **Pencere:** son 24 saat, en fazla 48 saat; Pazartesi sayılarında 72 saat (Cuma sabahından itibaren). Java okuma yazıları ve Takip haberleri bu sınırın dışındadır.
- **Arama:** her bölüm için ayrı arama; toplam 15-25 WebSearch (25 kesin üst sınır), en az üçte biri Yapay Zekâ & LLM için ve farklı açılardan (model sürümleri, araştırma, benchmark, agent'lar, düzenleme); Güvenlik için 2-3 arama yeter. Haber azsa daha fazla arama yapma, bölümü kısa tut.
- **Paralel:** birbirinden bağımsız aramaları ve sayfa okumalarını aynı anda gönder.
- **Okuma:** asıl kaynakları WebFetch ile oku. İki denemede 403, bot koruması ya da erişim hatası veren kaynağı bırak, aynı bilgiyi veren başka bir birincil kaynak ara. Bot korumasını aşmaya çalışma (headless tarayıcı, arşiv servisleri vb.).
- **Tekrar:** son 3 sayıda geçen haberi tekrar etme. Gerçek bir yeni gelişme varsa onu yaz ve önceki habere iç atıf ver.
- **Arşiv:** özet yalnızca son 3 sayıyı gösterir. Bir konunun daha önce işlenip işlenmediğini `python3 tools/ara.py "<şirket ya da konu>"` ile bütün arşivde ara; çıktıdaki adres iç atıfta aynen kullanılır. Daha eski sayıda işlenmiş bir konu da yeni bir gelişme olmadan tekrar yazılmaz.
- **Açık uçlar:** özet çıktısı son sayılarda sonucu henüz belli olmayan konuları ve ileri tarihleri listeler. Tarihi pencereye düşenler için toplam en fazla 3 arama ayır. Birincil kaynakta bir sonuç varsa “Takip” etiketiyle Kısa Kısa'ya ya da ilgili bölüme yaz ve iç atıf ver; sonuç yoksa yazma. Takip haberi tekrar sayılmaz.
- **Takvim için** ayrı arama yapma: okuduğun kaynaklarda geçen ileri tarihleri ve özet çıktısındaki tarihleri değerlendir (6. bölüm).

## 4. Bölümler

**Manşet.** Bu okuyucu için günün en önemli ve en çok eylem gerektiren AI/LLM gelişmesi: model sürümleri, AI kodlama araçları ve agent harness'larında önemli değişiklikler, ekiplerin AI kullanımını etkileyen araştırma ve benchmark'lar, fiyat, limit ve politika değişiklikleri. Manşete değer bir gelişme yoksa en güçlü AI/LLM haberini manşet yap; abartma.

- Güvenlik haberleri manşete çıkmaz. İstisna: ana konusu bir AI aracı ya da AI destekli geliştirme pratiği olan güvenlik haberi; ama güvenlik temalı manşet art arda iki sayıda olmaz.
- Aynı şirket ya da ürün ailesi (Gemini, GPT, Claude gibi) art arda iki sayıda manşet olmaz; o gün en güçlü haber yine o şirketinse bölümün büyük haberi yap. Önceki manşet özet çıktısında görünür.
- Başlık bağımsız ya da doğrulanabilir bir olguyla açılır (fiyat, sürüm, erişim, bağımsız ölçüm); şirketin kendi ölçümü ya da hız iddiası başlığa girmez.
- Okuyucu için en önemli pratik bilgi (fiyat, uyumluluk, son tarih, kimin etkilendiği, rakiplerle karşılaştırma) deck'te ya da ilk paragrafta olur.
- Manşetin yanında Pratik çıkarım kutusu olur (6. bölüm).

**Yapay Zekâ & LLM** (`ai`). Gazetenin ana bölümü: model sürümleri, benchmark'lar, araştırmalar, agent'lar ve agent altyapısı, açık modeller, AI düzenlemeleri ve politika değişiklikleri. Pencere içinde yeterli gerçek haber yoksa daha az yaz; dolgu koyma.

**Şirketler & Altyapı** (`is`). Yatırımlar, birleşmeler, çipler, veri merkezleri.

**Geliştirme & Araçlar** (`gelistirme`). AI kodlama araçları, agent harness'ları, CLI'lar, dil ve framework haberleri.

**Java & Spring** (`java`). Yalnızca JVM ekosistemi: JDK, Spring, Maven, Hibernate, Maven Central ve JVM bağımlılıklarını etkileyen tedarik zinciri haberleri. AI kütüphaneleri ancak Java/Kotlin API'si ise girer (LangChain4j ve Spring AI evet; Python LangChain Geliştirme & Araçlar'a gider). Önce şu kaynaklara bak, tek tek proje araması yapma; başka projeleri ancak bunlarda bir ipucu varsa ara:

- https://spring.io/blog, https://github.com/spring-projects/spring-boot/releases, https://github.com/spring-projects/spring-framework/releases
- https://feed.infoq.com/java/news/ (InfoQ Java ve Spring özetleri), https://inside.java/, https://foojay.io/today/
- https://openjdk.org/projects/jdk/, https://openjdk.org/jeps/0 (JEP durumları), https://jdk.java.net/ (erken erişim ve GA yapıları)
- https://www.openwall.com/lists/oss-security/ (Java/Apache güvenlik duyuruları)

Pencere içinde haber yoksa bunu gizleme ve dolgu koyma: son 7 günde yayımlanmış, önceki sayılarda geçmemiş en fazla 1 pratik yazıyı “Okuma · Konu” kicker'ıyla koy. Haber varken okuma yazısı koyma.

**Güvenlik** (`guvenlik`). Küçük bir bölüm: aktif istismarlar, kritik CVE'ler, tedarik zinciri saldırıları (özellikle Java/JVM, npm/Maven, AI tooling) arasından bu okuyucunun en çok harekete geçmesi gerekenler. Haftalar önce düzeltilmiş, aciliyeti olmayan açıkları koyma. Güvenlik gazetenin ana konusu değildir: bölüm dışında bir sayıda en fazla 1 haber ve 2 kısa haber güvenlik temalı olabilir (Java & Spring'e giren bir açık bu 1 habere sayılır).

- Her açık haberinde, hangi bölümde olursa olsun, “etkileniyor muyum, ne yapmalıyım” sorusunun cevabı olur: etkilenen ve yaması olmayan sürümler, giriş yolu ya da önkoşul, nasıl kontrol edileceği (sürüm komutu, IOC, kilit dosyasında aranacak paket), düzeltilmiş sürüm ya da geçici çözüm. Kaynakta biri yoksa “kaynak belirtmiyor” de. Kısa Kısa'da kimin etkilendiği ve ne yapılacağı tek cümleyle.
- Geliştirici araçlarını hedef alan bulgularda (AI kodlama araçlarının ayar, hook, MCP ya da talimat dosyaları; IDE eklentileri; CI yapılandırması; paket yöneticisi betikleri) okurun bugün yapabileceği en az bir kontrol adımı yazılır: hangi dosyaya ya da ayara bakılacağı, değişikliğin nasıl fark edileceği (“repolardaki `.claude/settings.json` ve hook değişikliklerini kod incelemesine dahil edin”). Adım kaynaktan ya da aracın resmi belgesinden gelir. Okurun kullandığı araçları doğrudan hedef alan böyle bir bulgu, bölümün en önemli haberiyse bölümün başına konur.
- Düşük önemdeki açığı yalnızca Java/JVM, build ve CI araçlarını ya da AI tooling'i etkiliyorsa ve okuyucunun yapacağı bir şey varsa yaz.
- **Bugün yamala** (`patch`, isteğe bağlı): bölümün başında 1-3 madde. Yalnızca pencere içinde aktif istismar edildiği bildirilen (CISA KEV'e eklenen ya da üreticinin “istismar ediliyor” dediği) açıklar ve zehirlenmiş paketler. Her madde tek satır: ürün ve etkilenen sürüm, ne yapılacağı. Kaynak: CISA KEV kataloğu, üretici ya da paket kayıt defteri duyurusu. Aynı açık bölümde haber olarak da yazıldıysa listeye girmez. Ölçüt tutmuyorsa alanı yazma.

**Öne Çıkan GitHub Repoları.** GitHub trending, trendshift.io gibi trending listelerinin sıralamasından; “Featured” ya da sponsorlu alanlardan değil.

- Her repo için iki cümle: ne olduğu ve neden şimdi gündemde olduğu (yeni sürüm, yeni özellik, duyuru). Neden yükseldiği görünmeyen, yıllardır bilinen projeleri liste dolsun diye seçme; 6 iyi repo 8 vasat repodan iyidir.
- Aynı kuruluştan en fazla 1 repo. Son 7 günde yer almış repo (aynı kuruluşun benzer adlı reposu dahil) tekrar girmez; liste özet çıktısında. Trending listelerinde bir JVM reposu (Java, Kotlin, Scala, Groovy) varsa en az biri girer. Telif açısından şüpheli projeleri (ticari oyun emülatörleri, recomp) seçme.
- `stars` mümkünse repo sayfasındaki güncel değer, kaynaktaki hassasiyette: tam sayı “1.932”, yuvarlanmış “13,4 bin”; `starsValue` aynı değerin sayısı (13400). `lang` yalnızca kaynakta açıkça görüldüyse; `meta` = “Dil · Kategori” (dil yoksa yalnızca kategori).

**Atölye.** Her sayıda bir uygulama yazısı: yapay zekâyı ve agent'ları yazılım geliştirmede, araştırma ve analizde verimli kullanmanın somut bir yolu. Konu seçimi, kaynak, yapı ve konu bankası `kurallar/ATOLYE.md` dosyasındadır; bu dosyadaki kaynak ve dil kuralları Atölye için de geçerlidir.

**Kısa Kısa.** Tek-iki cümlelik haberler. Tek ve ikincil kaynağa dayanan bir gelişme ancak burada, “İddia” ile başlayarak yer alabilir. Yaygın kullanılan bir hizmetin (bulut, Microsoft 365, GitHub, büyük model API'leri) pencere içindeki saatler süren kesintisi atlanmaz, en azından burada yer alır; link status sayfasındaki olay kaydına verilir. Tüketici ürünü ve magazin haberlerini, sayıyı doldurmak için haber koyma.

**Yer dağılımı.** 8 kolonluk büyük haberler okuyucunun işine en çok dokunan haberlere gider; genel piyasa ve finans haberleri ve küçük sürüm notları 4 kolonla yetinir. Bir şirket (ürünleriyle birlikte) manşet dışında en fazla 2 haber ve 1 kısa haberle yer alır; aynı günün duyurularını tek haberde birleştir. Başka bir haberde adının geçmesi ve repo listesi bu sınıra girmez.

## 5. Haber dili

Türkçe yaz; yerleşik karşılığı olmayan teknik terimler İngilizce kalır (context window, release candidate, sandbox). Her haberi kendi cümlelerinle özetle.

- **Giriş cümlesi** sonucu söyler: ne değişti, ne bulundu, ne bozuldu. Tarihle ya da “X şirketi … duyurdu” kalıbıyla açma; tarih ve duyuran cümle sonuna ya da ikinci cümleye gider. İddia ve Şirket beyanı haberlerinde kaynak yine ilk cümlede anılır (“X'e göre”). Aynı sayıda iki haber aynı kalıpla açılmaz.
- **Kısa cümle.** 25 kelimeyi aşan cümleyi böl; bir cümlede en fazla bir noktalı virgül ve en fazla iki karşılaştırma ya da rakam çifti.
- **Rakam seç.** Karar vermeye yarayan iki üç rakamı ver, gerisini kaynağa bırak. Grafikteki rakamları metinde tek tek sıralama; stat rakamı metinde bir kez geçer.
- **Terim.** Bir kavrama sayı boyunca tek terim (aynı sayıda hem “istem” hem “prompt” olmaz). Karşılık uydurma; İngilizce kalıbı kelime kelime çevirme (“in the wild” → “aktif istismar”, “instantiate” → “nesnesini oluşturmak”). Alanın kendi terimini kullan (DNA için “baz çifti”).
- **Dolgu ve tekrar yok.** Aynı olguyu bir haberde iki kez söyleme. “Bir dizi iyileştirme”, “rutin sürüm işleri” gibi bilgi taşımayan cümle yazma; söyleyecek şey kalmadıysa haberi bitir.
- **Jargon.** Yaygın olmayan bir ürün, protokol, benchmark ya da kısaltmayı ilk geçtiği yerde üç-sekiz kelimeyle açıkla (“Kerberos'un bilet dağıtım sunucusu KDC”); açıklama kaynakta yazan ya da genel bilinen bir tanım olmalı. Java, Docker, CVE, RAG, MCP gibi terimleri açıklama.
- **Yazım.** Satır içi kod, komut ve dosya adları `backtick` içinde. Tırnak “ ”; « » ve düz " kullanma. Düz kesme işareti ' ve tire - yaz; tipografik biçimlerini sayfa üretir. “Zekâ” her yerde şapkalı: yapay zekâ, zekâ endeksi.
- **Başlık** haberin tek ana olgusunu söyler; sığmayan rakam, tarih ve ikinci olgu manşette deck'e, haberlerde ilk cümleye gider.

## 6. Editoryal alanlar ve özel kutular

- **Pratik çıkarım** (manşet kutusu, 3-4 madde). Benzer işi yapan herhangi bir yazılım ekibinin uygulayabileceği somut eylemler: hangi sürüm, ayar, komut, son tarih ya da karşılaştırma (“`thinking: high` ile `xhigh`'ı aynı görev setinde 20 koşuda karşılaştırın; 1 Aralık'taki fiyat artışından önce bitirin”). Her habere uyan genel madde (“kendi görev setinizde ölçün”, “takip edin”, “değerlendirin”) ve önceki üç sayının maddelerini tekrar eden madde yazılmaz; liste özet çıktısında.
- **Neden önemli** (`why`). Bölümlerin büyük haberlerinde beklenir, diğerlerinde isteğe bağlı; manşette yazılmaz. Tek cümle: bu okuyucu için sonuç (kim etkilenir, neyi değiştirir, ne zaman harekete geçmeli). Yalnızca haberdeki olgulardan çıkar; yeni olgu, tahmin, abartı, “önemli bir adım” gibi boş ifade ve şirketin kendi açıklamasının tekrarı olmaz. Somut sonuç yoksa yazma. “Neden önemli” sözüyle başlama; etiketi sayfa ekler.
- **Takvim** (`calendar`, isteğe bağlı). Önümüzdeki 30 günün okuyucuyu ilgilendiren tarihleri: GA ve sürüm, fiyat ve limit değişikliği, servis kapanışı, son tarih, bilanço günü, önemli konferans açılışı. Öncelik bilanço, GA, fiyat değişikliği ve son tarihlerde. Tarih kaynakta açıkça yazmalı; “yakında”, “bekleniyor” ya da tahmini tarih girmez. Tarih bu sayıdaki bir haberde geçiyorsa `ref` o haberin çapası, geçmiyorsa `url` kaynağın linki. `text` olayın kendisi, yorum ve sıfat yok (“Gemini 4 Carbon ve Argon fiyatı iki katına çıkıyor”). Özet çıktısındaki önceki takvim öğeleri ve önceki sayıların metninde geçen ileri tarihler önemini koruyorsa girer; tarihi değiştiyse yeni kaynağıyla. En az 2 uygun tarih yoksa alanı yazma.
- **Düzeltme** (`corrections`, isteğe bağlı). Önceki bir sayıda olgu hatası fark edersen bu sayıya ekle: hatalı sayının tarihi, o sayıdaki çapa ve tek iki cümleyle neyin yanlış yazıldığı ve doğrusu. Üslup değişikliği düzeltme değildir; düzeltmeyi yumuşatma. Eski sayının dosyasını değiştirme.
- **İri rakam** (`stat`, isteğe bağlı). Yalnızca büyük haberde, grafik yoksa; haberin ana olgusu olan ve kaynakta yazan tek rakam ya da aralık. Uygun rakam yoksa koyma.
- **Grafik** (`chart`, isteğe bağlı). Yalnızca haberin ana iddiasını tek bakışta gösteren bir karşılaştırma: aynı şeyin önce ve sonrası, aynı ölçütte rakipler ya da sürümler, aynı görevin iki koşulu. Kendine sor: “Çubukların boyu arasındaki fark, haberin söylediği şeyin kendisi mi?” Değilse koyma. Farklı türden şeyleri karıştırma, yan rakamları ve paragraftaki rakamları çizme. Değerler kaynakta açıkça yazmalı ve aynı birimde olmalı; tahmin ya da türetme yok. Şirketin kendi ölçümüyse `note`'ta belirt. Haberin ana öznesi olan tek çubuğa `highlight`. Negatif değişimde `value` mutlak değer, `display` “−%5,5”.
- **Günün örüntüsü** (`pattern`, isteğe bağlı). Yalnızca bu sayıdaki en az üç haber aynı olguyu paylaşıyor ve bu ortaklık her birinin kendi kaynağında açıkça yazıyorsa. Ortaklığı adlandır ve haberleri say; nedensellik ve tahmin yok. Çoğu gün örüntü olmaz.
- **İç atıf.** Önceki bir sayıdaki habere atıfta kaynak listesine `{"label": "Dünkü sayı: <kısa başlık>", "url": "#YYYY-MM-DD-<çapa>"}` ekle (dünkü değilse “7 Kasım sayısı: …”). Metinde “dünkü sayıda andığımız” gibi bir atıf varsa iç link zorunlu. Kısa Kısa'da `url` aynı biçimde iç link olabilir.

## 7. Ölçüler

`tools/kontrol.py` bunları denetler; HATA yayını durdurur, UYARI gözden geçirilir.

| Öğe | Ölçü |
|---|---|
| Toplam | yaklaşık 12-15 dakikalık okuma (Atölye dahil) |
| Manşet | 4 paragraf; başlık en fazla 80 karakter; Pratik çıkarım 3-4 madde |
| Yapay Zekâ & LLM | 6-8 haber; ilk satır 8+4, sonra 6+6 ya da 4+4+4 |
| Diğer haber bölümleri | 2-3 haber |
| Güvenlik | 3-4 haber, her biri 60-90 kelime tek paragraf; büyük haber yok (4+4+4 ya da 6+6) |
| Izgara | 12 kolon; satırlar 8+4, 6+6 ya da 4+4+4; ilk haber genelde `big: true` |
| Büyük haber (8 kolon) | 160-220 kelime, 2-3 paragraf; aynı satırdaki 4 kolonluk haber 80-110 kelime |
| 6+6 ve 4+4+4 satırları | 80-110 kelime, satırdaki haberler arasında en fazla 20 kelime fark; tek paragraf |
| Paragraf | manşette ve büyük haberde en fazla 80 kelime |
| Başlık | haberlerde en fazla 70, 4 kolonluk haberde en fazla 60 karakter |
| why | tek cümle, en fazla 25 kelime; uzunluk dengesine sayılmaz |
| stat | sayıda en fazla 3; `n` en fazla 10, `l` en fazla 80 karakter |
| Grafik | sayıda en fazla 3; 2-5 çubuk |
| Takvim | 2-5 öğe; 0-30 gün ileride; `text` en fazla 60 karakter |
| Bugün yamala | 1-3 madde, her biri en fazla 110 karakter |
| pattern | başlık en fazla 60 karakter, metin 30-60 kelime, en az 3 ref |
| Atölye | 250-550 kelime (örnek blok hariç); 3-6 adım; örnek en fazla 25 satır; 1-4 kaynak |
| Repolar | 6-8 |
| Kısa Kısa | 6-10 |
| Kaynak | haber başına 1-4 link |

Bir haber ölçüsüne sığmıyorsa metni zorla kısaltmak yerine `size` değerini ya da satırdaki eşini değiştir.

## 8. JSON alanları

Alan adları ve biçim `kurallar/ornek.json` dosyasındadır; oradaki metinler ve uzunluklar örnek değildir.

- `date` (YYYY-MM-DD), `number` (önceki en büyük + 1), `dateLabel` (“Çarşamba, 4 Kasım 2026”), `readingMinutes` (sayfa okuma süresini kendisi hesaplar; alan biçim için yazılır).
- `lead`: `{kicker, alert, headline, deck, paragraphs[], chart?, sources[{label, url}], box{kicker, title, items[], note}}`. Kaynak `label`'ında “·” kullanma (“Hugging Face blog: llama.cpp v1.0.0”); sayfa kaynakları “·” ile ayırır.
- `sections[]`: `{id, title, subtitle?, patch?, articles[]}`; haber: `{size: 4|6|8, big?, kicker, alert?, pill?, headline, stat?, paragraphs[], why?, chart?, sources[]}`. Bölüm `subtitle`'ı sayfada basılmaz, yazmak zorunlu değildir. `patch` yalnızca Güvenlik'te: `[{text, url}]`.
- `repos`: `{subtitle, items[{name, url, stars, starsValue, lang?, cat, why, meta}], sources[]}`.
- `atolye`: `{konu, kicker, title, intro, when, steps[], example{label, lang, code}, pitfall, sources[]}`; `konu` konu bankasındaki kimlik ya da `"haber"`.
- `briefs[]`: `{tag, text, url}`.
- İsteğe bağlı: `calendar[{date, text, ref?, url?}]`, `corrections[{date, ref, text}]`, `pattern{title, text, refs[]}`. `figures` artık yazılmaz.
- `stat`: `{"n": "%65-80", "l": "rakamın neyi ölçtüğü"}`. `chart`: `{"title": "Ölçü ve birim", "note"?: "...", "items": [{"label", "value": sayı >= 0, "display": "%48,5", "highlight"?: true}]}`.

**Çapalar.** Manşet `manset`; bölüm haberleri `<bölüm id>-<sıra>` (sıra `articles` dizisinde 1'den başlar: `java` bölümünün ilk haberi `java-1`). Haberin kendi `id` alanı varsa o kullanılır.
