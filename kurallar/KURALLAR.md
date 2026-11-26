# The Daily Compiler · yayın kuralları

Bu dosya gazetenin yazım ve seçim kurallarıdır. Yazar da editör de buna göre çalışır; yazar bu dosyayı değiştirmez.

Kurallar çatıştığında öncelik sırası: **doğruluk**, **okuyucu için önem**, **dil**, **biçim**. Ölçülebilir kurallar 7. bölümdedir.

## 1. Okuyucu

Okuyucu, farklı dillerde, farklı alanlarda ve farklı ölçekte yazılım geliştiren deneyimli yazılımcılar ve teknik liderlerdir; backend, frontend, mobil, veri, altyapı ya da gömülü sistemlerde çalışan herkes olabilir. Ortak noktaları, yapay zekâyı ve agent'ları işlerinde giderek daha çok kullanmaları ve teknik kararlar vermeleridir.

Öncelik sırası: (1) yapay zekâ ve yazılım geliştirme: modeller, AI destekli geliştirme araçları, agent'lar, geliştirme pratikleri; (2) okurun kullandığı dil, framework ve araçlardaki önemli değişiklikler; (3) güvenlik, kendi bölümünde; (4) sektör ve altyapı. Bir haberin önemi, kaç okuru ve ne kadar derinden etkilediğiyle ölçülür. Tek bir dile ya da framework'e özgü bir haber, o ekosistemi kullananlar için önemliyse kendi bölümünde yer alır, ama sayının geneline yön vermez; Java & Spring bölümü her sayıda yer alır ama gazetenin merceği değildir.

Gazete herkese açıktır. Metinde belirli bir kişiye, şirkete ya da ekibe hitap etme. Okuyucuya her haberde şu soruların cevabını ver: ne değişti, beni etkiliyor mu, ne yapmalıyım ve ne zamana kadar.

## 2. Kaynak ve doğruluk (en önemli kurallar)

- **Kaynakta yazmayan yazılmaz.** Haber metninde (başlık, deck, paragraflar, Takvim, Acil önlemler, stat, grafik, kısa haberler, repolar) kaynağında açıkça yazmayan hiçbir ayrıntı, yöntem, sayı ya da nitelendirme olmaz. “Mantıklı” diye ekleme; emin değilsen yazma. İstisnalar: kısa jargon açıklamaları (genel bilinen tanım) ve editoryal alanlar (Editörün önerileri, why). Editoryal alanlar da yeni olgu getirmez.
- **Asıl kaynak.** Her haberde en az bir gerçek link; uydurma link yok. Asıl kaynağı ver: resmi duyuru, advisory, makale, sürüm notu, birincil haber. Toplayıcı siteler (aiweekly.co, Releasebot vb.) yalnızca haberi bulmak içindir; forum ve SEO sitelerini daha iyisi varken kullanma. Haber başına en fazla 4 kaynak: önce birincil, sonra en güçlü bağımsız. Asıl kaynağa ulaşamadıysan haberi atla ya da “İddia” etiketiyle Kısa Kısa'ya yaz.
- **Etiketler.** Tek kaynaklı ve doğrulanmamış iddia: kicker “İddia · Konu”; başlık kesin olgu gibi yazılmaz, kaynağa atfedilir (“Sentra: Qubole üzerinden müşteri AWS hesaplarına girildi”). Bir şirketin yalnızca kendisi hakkındaki ölçüm ve beyanı (kendi benchmark'ı, kendi tasarrufu, kendi vaka çalışması): kicker “Şirket beyanı · Konu”; başlıktaki ölçüm şirkete atfedilir.
- **Bağımsız kaynakta şartlar.** Manşet ya da büyük haber olacak bir ürün duyurusunda, hangi şirketten olursa olsun, en az bir bağımsız kaynakta şartları, sınırları ve eleştirileri ara (lisans, veri ve telemetri, fiyat); duyuruyu yalnızca aktaran yazı bağımsız sayılmaz. Bulduğun önemli şart habere girer.
- **Rakamlar.** Rakamları kaynakta yazdığı gibi ver. Türetilmiş bir rakamı (yüzde fark, oran, “kat”) kendin hesaplıyorsan girdileri kaynaktan al, hesabı iki kez yap, yuvarlarken “yaklaşık” de; kaynağın hesabını kullanıyorsan ona atfet. Aynı rakam sayı boyunca ve önceki sayılarla tutarlı olmalı. Benchmark sayfasındaki (`data/modeller.json`) bir ölçümü haberde veriyorsan değer aynı olmalı; kaynak başka bir ayarın ya da sürümün sonucunu veriyorsa bunu yaz.
- **Eşit muamele.** Bu gazeteyi Anthropic'in Claude modeli yazıyor. Anthropic ve Claude haberlerine diğer şirketlerle aynı etiketleri, çekinceleri ve ölçütleri uygula; övgü sıfatı kullanma. Modelleri ya da ürünleri karşılaştırırken her birine aynı rakamı ver; hiçbirini (Claude dahil) rakamsız “en pahalısı”, “en iyisi” gibi bir ifadeyle geçme.
- **Çekince ve yorum.** Kaynağın kendi çekincesi (tekrar üretilemedi, tartışmalı) habere yazılır. Kendi yorumunu haber cümlesi gibi yazma; yorum yalnızca editoryal alanlarda olur. Kaynaktan 15 kelimeyi aşan alıntı yapma. Siyasi konularda yorum katma.

## 3. Araştırma

- **Pencere:** son 24 saat, en fazla 48 saat; Pazartesi sayılarında 72 saat (Cuma sabahından itibaren). Pencere birincil kaynağın tarihiyle ölçülür (sürüm notu, etiket, duyuru), toplayıcıda ya da Hacker News'te görüldüğü günle değil. Java okuma yazıları ve Takip haberleri bu sınırın dışındadır.
- **Arama:** her bölüm için ayrı arama; toplam 15-25 WebSearch (25 üst sınır), en az üçte biri yapay zekâ için ve farklı açılardan (model, araştırma, benchmark, agent, düzenleme); Güvenlik için 2-3 arama yeter.
- **Okuma:** asıl kaynakları WebFetch ile oku. İki denemede açılmayan kaynağı bırak, aynı bilgiyi veren başka bir birincil kaynak ara; bot korumasını aşmaya çalışma.
- **Tekrar:** son 3 sayıda geçen haberi tekrar etme. Gerçek bir yeni gelişme varsa onu yaz ve önceki habere iç atıf ver.
- **Arşiv:** özet yalnızca son 3 sayıyı gösterir. Bir konunun daha önce işlenip işlenmediğini `python3 tools/ara.py "<şirket ya da konu>"` ile bütün arşivde ara; çıktıdaki adres iç atıfta aynen kullanılır. Daha eski sayıda işlenmiş bir konu da yeni bir gelişme olmadan tekrar yazılmaz.
- **Açık uçlar:** özet çıktısı son sayılarda sonucu henüz belli olmayan konuları ve ileri tarihleri listeler. Tarihi pencereye düşenler için toplam en fazla 3 arama ayır. Birincil kaynakta yeni bir olgu (sonuç, yama durumu, istismar, yeni sürüm) varsa “Takip” etiketiyle Kısa Kısa'ya ya da ilgili bölüme yaz ve iç atıf ver; yoksa yazma. Takip haberi tekrar sayılmaz.
- **Takvim için** ayrı arama yapma: okuduğun kaynaklarda geçen ileri tarihleri ve özet çıktısındaki tarihleri değerlendir (6. bölüm).

## 4. Bölümler

**Manşet.** Günün en önemli ve en çok eylem gerektiren yapay zekâ ya da yazılım geliştirme gelişmesi: model sürümleri, AI kodlama araçları ve agent harness'larında önemli değişiklikler, ekiplerin AI kullanımını etkileyen araştırma ve benchmark'lar, fiyat, limit ve politika değişiklikleri. Manşete değer bir gelişme yoksa bu alandaki en güçlü haberi manşet yap; abartma.

- Güvenlik haberleri manşete çıkmaz. İstisna: ana konusu bir AI aracı ya da AI destekli geliştirme pratiği olan güvenlik haberi; ama güvenlik temalı manşet art arda iki sayıda olmaz.
- Aynı şirket ya da ürün ailesi (Gemini, GPT, Claude gibi) art arda iki sayıda manşet olmaz; o gün en güçlü haber yine o şirketinse bölümün büyük haberi yap. Önceki manşet özet çıktısında görünür.
- Başlık doğrulanabilir bir olguyla açılır (fiyat, sürüm, erişim, bağımsız ölçüm); şirketin kendi ölçümü başlığa girmez. En önemli pratik bilgi (fiyat, uyumluluk, son tarih, kimin etkilendiği) deck'te ya da ilk paragrafta olur.
- Manşetin yanında Editörün önerileri kutusu olur (6. bölüm).

**Yapay Zekâ & LLM** (`ai`). Gazetenin ana bölümü: model sürümleri, benchmark'lar, araştırmalar, agent'lar ve agent altyapısı, açık modeller, AI düzenlemeleri ve politika değişiklikleri. Pencere içinde yeterli gerçek haber yoksa daha az yaz; dolgu koyma.

**Şirketler & Altyapı** (`is`). Yatırımlar, birleşmeler, çipler, veri merkezleri. Bir yatırım ya da birleşme okura bir araç, altyapı ya da pazar kararı açısından bir şey söylemiyorsa Kısa Kısa'ya gider; 6-8 kolon almaz.

**Geliştirme & Araçlar** (`gelistirme`). AI kodlama araçları, agent harness'ları, CLI'lar, dil ve framework haberleri.

**Java & Spring** (`java`). Yalnızca JVM ekosistemi: JDK, Spring, Maven, Hibernate, Maven Central ve JVM bağımlılıklarını etkileyen tedarik zinciri haberleri. AI kütüphaneleri ancak Java/Kotlin API'si ise girer (LangChain4j ve Spring AI evet; Python LangChain Geliştirme & Araçlar'a gider). Önce şu kaynaklara bak, tek tek proje araması yapma; başka projeleri ancak bunlarda bir ipucu varsa ara:

- https://spring.io/blog, https://github.com/spring-projects/spring-boot/releases, https://github.com/spring-projects/spring-framework/releases
- https://feed.infoq.com/java/news/ (InfoQ Java ve Spring özetleri), https://inside.java/, https://foojay.io/today/
- https://openjdk.org/projects/jdk/, https://openjdk.org/jeps/0 (JEP durumları), https://jdk.java.net/ (erken erişim ve GA yapıları)
- https://www.openwall.com/lists/oss-security/ (Java/Apache güvenlik duyuruları)

Pencere içinde haber yoksa bunu gizleme ve dolgu koyma: son 7 günde yayımlanmış, önceki sayılarda geçmemiş en fazla 1 pratik yazıyı “Okuma · Konu” kicker'ıyla koy. Haber varken okuma yazısı koyma.

**Güvenlik** (`guvenlik`). Küçük bir bölüm: aktif istismarlar, kritik CVE'ler, tedarik zinciri saldırıları (yaygın kullanılan diller, framework'ler, paket ekosistemleri, CI ve AI tooling) arasından okurun en çok harekete geçmesi gerekenler. Haftalar önce düzeltilmiş, aciliyeti olmayan açıkları koyma. Güvenlik gazetenin ana konusu değildir: bölüm dışında bir sayıda en fazla 1 haber ve 2 kısa haber güvenlik temalı olabilir (Java & Spring'e giren bir açık bu 1 habere sayılır).

- Her açık haberinde, hangi bölümde olursa olsun, “etkileniyor muyum, ne yapmalıyım” sorusunun cevabı olur: etkilenen ve yaması olmayan sürümler, giriş yolu ya da önkoşul, nasıl kontrol edileceği (sürüm komutu, IOC, kilit dosyasında aranacak paket), düzeltilmiş sürüm ya da geçici çözüm. Kaynakta olmayan bir bilgiyi yalnızca okurun kararını değiştiriyorsa ve sonucuyla birlikte söyle (“IOC yayımlanmadı; ele geçirilip geçirilmediğinizi bu duyurudan anlayamazsınız”); haberi “açıklanmadı / belirtmiyor” cümlesiyle bitirme. Kısa Kısa'da kimin etkilendiği ve ne yapılacağı tek cümleyle.
- Geliştirici araçlarını hedef alan bulgularda (AI kodlama araçlarının ayar, hook, MCP ya da talimat dosyaları; IDE eklentileri; CI; paket yöneticisi betikleri) okurun bugün yapabileceği en az bir kontrol adımı yazılır (“repolardaki `.claude/settings.json` ve hook değişikliklerini kod incelemesine dahil edin”); adım kaynaktan ya da aracın resmi belgesinden gelir.
- Düşük önemdeki açığı yalnızca yaygın kullanılan runtime, build ve CI araçlarını ya da AI tooling'i etkiliyorsa ve okuyucunun yapacağı bir şey varsa yaz.
- **Kırmızı** (`alert: true`): yalnızca aktif istismar edildiği bildirilen açık, zehirlenmiş paket ya da kimlik doğrulamasız RCE haberinde; bu ölçüt bölüm ne olursa olsun geçerli. Okurdan eylem beklemeyen olay, takip ve kimlik doğrulama gerektiren açık petrol kalır.
- **Acil önlemler** (`patch`, isteğe bağlı): bölümün başında 1-3 madde; sayının (her bölümün) uyarı taşıyan bütün açıklarından seçilir: pencere içinde aktif istismar edildiği bildirilen açıklar (CISA KEV ya da üretici), zehirlenmiş paketler ve yaygın kullanılan yazılımda kimlik doğrulama gerektirmeyen uzaktan kod çalıştırma (yaması ya da geçici çözümü çıkmış). Sıra, ciddiyet ve etkilenen kitlenin genişliğine göredir; CISA son tarihi sıralama ölçütü değil, ek bilgidir. Her madde tek satır: ürün ve etkilenen sürüm, ne yapılacağı. Açık bu sayıda haber olarak da yazıldıysa madde `ref` ile o habere bağlanır; değilse `url` birincil duyuruya (CISA KEV, üretici, paket kayıt defteri). Ölçüt tutmuyorsa alanı yazma.

**Öne Çıkan GitHub Repoları.** GitHub trending, trendshift.io gibi trending listelerinin sıralamasından; “Featured” ya da sponsorlu alanlardan değil.

- Her repo için iki cümle: ne olduğu ve neden şimdi gündemde olduğu. “Neden şimdi” bir olaydır (yeni sürüm, duyuru, bir haberde anılma); trending sırası ve yıldız sayısı değildir. Olayı bulunamayan repoyu seçme; 6 iyi repo 8 vasat repodan iyidir.
- Aynı kuruluştan en fazla 1 repo. Son 7 günde yer almış repo (aynı kuruluşun benzer adlı reposu dahil) tekrar girmez; liste özet çıktısında. Trending listelerinde bir JVM reposu (Java, Kotlin, Scala, Groovy) varsa en az biri girer. Telif açısından şüpheli projeleri (ticari oyun emülatörleri, recomp) seçme.
- `stars` mümkünse repo sayfasındaki güncel değer, kaynaktaki hassasiyette: tam sayı “1.932”, yuvarlanmış “13,4 bin”; `starsValue` aynı değerin sayısı (13400). `lang` yalnızca kaynakta açıkça görüldüyse; `meta` = “Dil · Kategori” (dil yoksa yalnızca kategori).

**Atölye.** Her sayıda bir uygulama yazısı: yapay zekâyı ve agent'ları yazılım geliştirmede, araştırma ve analizde verimli kullanmanın somut bir yolu. Konu seçimi, kaynak, yapı ve konu bankası `kurallar/ATOLYE.md` dosyasındadır; bu dosyadaki kaynak ve dil kuralları Atölye için de geçerlidir.

**Kısa Kısa.** Tek-iki cümlelik haberler. Tek ve ikincil kaynağa dayanan bir gelişme ancak burada, “İddia” ile başlayarak yer alabilir. Yaygın bir hizmetin (bulut, GitHub, büyük model API'leri) saatler süren kesintisi en azından burada yer alır; link status sayfasındaki olay kaydına verilir. Tüketici ürünü, magazin ve dolgu haberi koyma.

**Yer dağılımı.** 8 kolonluk büyük haberler okuyucunun işine en çok dokunan haberlere gider; genel piyasa ve finans haberleri ve küçük sürüm notları 4 kolonla yetinir. Bir şirket (ürünleriyle birlikte) manşet dışında en fazla 2 haber ve 1 kısa haberle yer alır; aynı günün duyurularını tek haberde birleştir. Başka bir haberde adının geçmesi ve repo listesi bu sınıra girmez.

## 5. Haber dili

Türkçe yaz; yerleşik karşılığı olmayan teknik terimler İngilizce kalır (context window, release candidate, sandbox). Hangi terimin İngilizce kalacağı, hangisinin Türkçe yazılacağı ve yasak çeviriler `kurallar/TERIMLER.md` dosyasındadır; ölçüt, Türk yazılımcının işte kullandığı kelimedir (secret, runtime, branch, endpoint; ama yama, açık, bellek sızıntısı). Her haberi kendi cümlelerinle özetle.

- **Giriş cümlesi** sonucu söyler: ne değişti, ne bulundu, ne bozuldu. Tarihle ya da “X şirketi … duyurdu” kalıbıyla açma; tarih ve duyuran cümle sonuna ya da ikinci cümleye gider. İddia ve Şirket beyanı haberlerinde kaynak yine ilk cümlede anılır (“X'e göre”). Aynı sayıda iki haber aynı kalıpla açılmaz.
- **Kısa cümle.** 25 kelimeyi aşan cümleyi böl; bir cümlede en fazla bir noktalı virgül ve en fazla iki karşılaştırma ya da rakam çifti.
- **Rakam seç.** Karar vermeye yarayan iki üç rakamı ver. Aynı ölçütte birkaç model, sürüm ya da koşulun rakamları birikiyorsa onları grafiğe (`chart`) ya da tabloya (`table`) taşı, metinde tek cümlelik bir yargı bırak (“kodlamada fark yok, maliyet yarıya indi”); grafikteki rakamları metinde tek tek sıralama. Stat rakamı metinde bir kez geçer.
- **Terim.** Bir kavrama sayı boyunca tek terim (aynı sayıda hem “istem” hem “prompt” olmaz). Karşılık uydurma; İngilizce kalıbı kelime kelime çevirme (“in the wild” → “aktif istismar”, “instantiate” → “nesnesini oluşturmak”). Alanın kendi terimini kullan (DNA için “baz çifti”).
- **Dolgu ve tekrar yok.** Aynı olguyu bir haberde iki kez söyleme; önceki sayılarda verilmiş bir uyarıyı yeni bilgi olmadan tekrarlama. “Bir dizi iyileştirme”, “rutin sürüm işleri” gibi bilgi taşımayan cümle yazma; söyleyecek şey kalmadıysa haberi bitir.
- **Jargon.** Yaygın olmayan bir ürün, protokol, benchmark ya da kısaltmayı ilk geçtiği yerde üç-sekiz kelimeyle açıkla (“Kerberos'un bilet dağıtım sunucusu KDC”); açıklama kaynakta yazan ya da genel bilinen bir tanım olmalı. Java, Docker, CVE, RAG, MCP gibi terimleri açıklama.
- **Yazım.** Satır içi kod, komut ve dosya adları `backtick` içinde. Tırnak “ ”; « » ve düz " kullanma. Düz kesme işareti ' ve tire - yaz; tipografik biçimlerini sayfa üretir. “Zekâ” her yerde şapkalı: yapay zekâ, zekâ endeksi.
- **Başlık** haberin tek ana olgusunu söyler; sığmayan rakam, tarih ve ikinci olgu manşette deck'e, haberlerde ilk cümleye gider.

## 6. Editoryal alanlar ve özel kutular

- **Editörün önerileri** (manşet kutusu, 3-4 madde; sayfadaki etiketi kod yazar; kutuya ayrıca başlık ya da `kicker` yazılmaz). Herhangi bir yazılım ekibinin uygulayabileceği somut eylemler: sürüm, ayar, komut, son tarih ya da karşılaştırma (“`thinking: high` ile `xhigh`'ı aynı görev setinde 20 koşuda karşılaştırın; 1 Aralık'taki fiyat artışından önce bitirin”). Metinde olmayan olgu, her habere uyan genel madde (“takip edin”, “değerlendirin”) ve önceki üç sayının maddelerini (özet çıktısında) tekrar eden madde yazılmaz.
- **Neden önemli** (`why`). Bölümlerin büyük haberlerinde beklenir, diğerlerinde isteğe bağlı; manşette yazılmaz. Tek cümle: bu okuyucu için sonuç (kim etkilenir, neyi değiştirir, ne zaman harekete geçmeli). Yalnızca haberdeki olgulardan çıkar; yeni olgu, tahmin, “önemli bir adım” gibi boş ifade ve şirket açıklamasının tekrarı olmaz; somut sonuç yoksa yazma. “Neden önemli” sözüyle başlama; etiketi sayfa ekler.
- **Takvim** (`calendar`, isteğe bağlı). Önümüzdeki 30 günün tarihleri: GA ve sürüm, fiyat ve limit değişikliği, servis kapanışı, son tarih, bilanço, önemli konferans. Tarih kaynakta açıkça yazmalı; “yakında” ya da tahmini tarih girmez. Bu sayıdaki bir haberde geçiyorsa `ref` o haberin çapası, değilse `url` kaynağın linki. `text` olayın kendisi, yorumsuz (“Gemini 4 Carbon ve Argon fiyatı iki katına çıkıyor”). Özet çıktısındaki önceki tarihler önemini koruyorsa girer. En az 2 tarih yoksa alanı yazma.
- **Düzeltme** (`corrections`, isteğe bağlı). Önceki bir sayıdaki olgu hatası: hatalı sayının tarihi, çapa ve bir iki cümleyle neyin yanlış yazıldığı ve doğrusu. Üslup değişikliği düzeltme değildir; düzeltmeyi yumuşatma. Eski sayının dosyasını değiştirme.
- **İri rakam** (`stat`, isteğe bağlı). Yalnızca büyük haberde, grafik yoksa; haberin ana olgusu olan ve kaynakta yazan tek rakam ya da aralık. Uygun rakam yoksa koyma.
- **Tablo** (`table`, isteğe bağlı). Grafiğin tek boyutu yetmediğinde: birkaç öğenin (model, sürüm, dağıtım) birkaç ölçütte karşılaştırması ya da yama durumu (dağıtım, düzeltilmiş sürüm). 2-6 satır, 2-5 sütun; ilk sütun öğenin adı. Değerler kaynakta yazdığı gibi; boş hücre “–”. Yorum, renk ve sıralama iddiası yok; bir haberde grafik ya da tablodan yalnızca biri.
- **Grafik** (`chart`, isteğe bağlı). Yalnızca haberin ana iddiasını tek bakışta gösteren bir karşılaştırma: aynı şeyin önce ve sonrası, aynı ölçütte rakipler ya da sürümler, aynı görevin iki koşulu. Çubukların boyu arasındaki fark haberin söylediği şeyin kendisi değilse koyma; farklı türden şeyleri ve yan rakamları çizme. Değerler kaynakta yazmalı ve aynı birimde olmalı; tahmin ya da türetme yok. Şirketin kendi ölçümüyse `note`'ta belirt. Haberin ana öznesi olan tek çubuğa `highlight`. Negatif değişimde `value` mutlak değer, `display` “−%5,5”.
- **İç atıf.** Önceki bir sayıdaki habere atıfta kaynak listesine `{"label": "Dünkü sayı: <kısa başlık>", "url": "#YYYY-MM-DD-<çapa>"}` ekle (dünkü değilse “7 Kasım sayısı: …”). Metinde “dünkü sayıda andığımız” gibi bir atıf varsa iç link zorunlu. Kısa haberin çapası `kisa-<sıra>`; Takip kısasında `url` yeni olgunun kaynağı, önceki habere atıf `ref`.

## 7. Ölçüler

`tools/kontrol.py` bunları denetler; HATA yayını durdurur, UYARI gözden geçirilir.

| Öğe | Ölçü |
|---|---|
| Toplam | yaklaşık 12-15 dakikalık okuma (Atölye dahil) |
| Manşet | 4 paragraf; başlık en fazla 80 karakter; Editörün önerileri 3-4 madde |
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
| Acil önlemler | 1-3 madde, her biri en fazla 110 karakter |
| Atölye | 250-550 kelime (örnek blok hariç); 3-6 adım; örnek en fazla 25 satır; 1-4 kaynak |
| Repolar | 6-8 |
| Kısa Kısa | 6-10 |
| Kaynak | haber başına 1-4 link |

Bir haber ölçüsüne sığmıyorsa metni zorla kısaltmak yerine `size` değerini ya da satırdaki eşini değiştir.

## 8. JSON alanları

Alan adları ve biçim `kurallar/ornek.json` dosyasındadır; oradaki metinler ve uzunluklar örnek değildir.

- `date` (YYYY-MM-DD), `number` (önceki en büyük + 1), `dateLabel` (“Çarşamba, 4 Kasım 2026”), `readingMinutes` (sayfa okuma süresini kendisi hesaplar; alan biçim için yazılır).
- `lead`: `{kicker, alert, headline, deck, paragraphs[], chart?, table?, sources[{label, url}], box{items[]}}`. Kaynak `label`'ında “·” kullanma (“Hugging Face blog: llama.cpp v1.0.0”); sayfa kaynakları “·” ile ayırır.
- `sections[]`: `{id, title, subtitle?, patch?, articles[]}`; haber: `{size: 4|6|8, big?, kicker, alert?, pill?, headline, stat?, paragraphs[], why?, chart?, table?, sources[]}`; `patch[{text, ref?, url?}]`. Bölüm `subtitle`'ı sayfada basılmaz, yazmak zorunlu değildir. `patch` yalnızca Güvenlik'te: `[{text, url}]`.
- `repos`: `{subtitle, items[{name, url, stars, starsValue, lang?, cat, why, meta}], sources[]}`.
- `atolye`: `{konu, kicker, title, intro, when, steps[], example{label, lang, code}, pitfall, sources[]}`; `konu` konu bankasındaki kimlik ya da `"haber"`.
- `briefs[]`: `{tag, text, url, ref?}`.
- İsteğe bağlı: `calendar[{date, text, ref?, url?}]`, `corrections[{date, ref, text}]`. `figures` artık yazılmaz.
- `stat`: `{"n": "%65-80", "l": "rakamın neyi ölçtüğü"}`. `chart`: `{"title": "Ölçü ve birim", "note"?: "...", "items": [{"label", "value": sayı >= 0, "display": "%48,5", "highlight"?: true}]}`. `table`: `{"title": "Ne karşılaştırılıyor", "cols": ["Model", "SWE-bench", "Fiyat ($/M)"], "rows": [["GPT-6.2", "%71,2", "2,50"], {"cells": ["…"], "highlight": true}], "note"?: "..."}`.

**Çapalar.** Manşet `manset`; bölüm haberleri `<bölüm id>-<sıra>` (sıra `articles` dizisinde 1'den başlar: `java` bölümünün ilk haberi `java-1`). Haberin kendi `id` alanı varsa o kullanılır.
