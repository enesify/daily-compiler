# The Daily Compiler · yayın kuralları

Bu dosya gazetenin yazım ve seçim kurallarıdır. Yazar da editör de buradaki kurallara göre çalışır. Yazar bu dosyayı değiştirmez.

## 1. Okuyucu

Okuyucu, JVM ekosisteminde (Java, Maven, Spring Boot mikroservisleri) üretim sistemleri geliştiren ve ekibinde AI destekli geliştirme araçlarını kullanan deneyimli yazılımcılar ve teknik liderlerdir. Güvenlik açıkları, tooling kararları ve AI destekli geliştirme onlar için özellikle önemlidir.

Bu tanım haber seçimini ve önceliklendirmeyi yönlendiren bir mercektir. Gazete herkese açıktır: metinde belirli bir kişiye, şirkete ya da ekibe hitap etme. "Pratik çıkarım" maddelerini benzer işi yapan herhangi bir yazılım ekibinin uygulayabileceği biçimde yaz.

## 2. Araştırma

- Zaman penceresi: son 24 saat, en fazla 48 saat. Pazartesi sayılarında hafta sonu nedeniyle sınır 72 saattir (Cuma sabahından itibaren).
- Her bölüm için ayrı aramalar yap. Toplam WebSearch sayısı en az 15, en fazla 25'tir; 25 kesin üst sınırdır. Haber azsa daha fazla arama yapma, bölümleri kısa tut.
- WebFetch ile asıl kaynakları oku. Bir kaynak iki denemede 403, bot koruması ya da erişim hatası verirse o kaynağı bırak: aynı bilgiyi veren başka bir birincil kaynak ara, bulamazsan 5. bölümdeki "asıl kaynağa ulaşılamadı" kuralını uygula. Bot korumasını aşmaya çalışma (headless tarayıcı, arşiv servisleri vb. kullanma).
- Son 3 sayıda geçen haberleri tekrar etme. Gerçek bir yeni gelişme varsa onu öne çıkar ve önceki habere iç atıf ver (7. bölüm, İç atıflar).

## 3. Bölümler

**Manşet.** Günün bu okuyucu için en önemli ve en çok eylem gerektiren AI/LLM gelişmesi (yalnızca genel olarak en büyük haber değil). Örnekler: model sürümleri, AI kodlama araçları ve agent harness'larındaki önemli değişiklikler, ekiplerin AI kullanımını etkileyen araştırma ve benchmark'lar, fiyat/limit/politika değişiklikleri. Güvenlik haberleri (CVE'ler, ihlaller, tedarik zinciri saldırıları) manşete çıkmaz, Güvenlik bölümünde 8 kolonluk büyük haber olur. İstisna: ana konusu bir AI aracı ya da AI destekli geliştirme pratiği olan güvenlik haberleri (ör. bir AI kodlama aracının sırları sızdırması) manşet olabilir. Pencere içinde manşete değer bir AI/LLM gelişmesi yoksa en güçlü AI/LLM haberini manşet yap; uydurma ya da abartma. Manşetin yanında "Pratik çıkarım" kutusu olur: benzer işi yapan bir yazılım ekibi için 3-4 somut madde.

**Yapay Zeka & LLM** (id `ai`). Model sürümleri, benchmark'lar, araştırmalar.

**Şirketler & Altyapı** (id `is`). Yatırımlar, birleşmeler, çipler, veri merkezleri.

**Geliştirme & Araçlar** (id `gelistirme`). AI kodlama araçları, agent harness'ları, CLI'lar, dil/framework haberleri.

**Java & Spring** (id `java`). JDK, Spring, Maven, Hibernate, LangChain4j vb. Pencere içinde yeni sürüm ya da haber yoksa bunu gizleme: subtitle'ı "Son 48 saatte yeni sürüm yok · haftanın okumaları" gibi açıkça yaz, yalnızca son 7 günden ve önceki sayılarda geçmemiş pratik yazıları koy, kısa tut. Uydurma. Sürüm ve haberleri önce şu kaynaklardan kontrol et, tek tek proje araması yapma:

- https://spring.io/blog
- https://feed.infoq.com/java/news/ (InfoQ Java ve Spring haftalık özetleri)
- https://openjdk.org/projects/jdk/ (aktif JDK sürüm sayfası ve JEP listesi)
- https://inside.java/
- https://www.openwall.com/lists/oss-security/ (Java/Apache güvenlik duyuruları için günlük dizin)

Bunlar dışındaki projeleri ancak bu kaynaklarda bir ipucu varsa ara.

**Güvenlik** (id `guvenlik`). Aktif istismarlar, kritik CVE'ler, tedarik zinciri saldırıları (özellikle Java/JVM, npm/Maven, AI tooling). Haftalar önce düzeltilmiş, aciliyeti olmayan açıkları büyük haber yapma.

Açık haberleri için (hangi bölümde ya da Kısa Kısa'da olursa olsun):

- Düşük önemdeki açıkları yalnızca Java/JVM, build ve CI araçları ya da AI tooling'i etkiliyorsa ve okuyucunun yapması gereken bir şey varsa yaz. Yer doldurmak için açık haberi koyma.
- Kimin etkilendiğini (ürün, sürüm aralığı, hangi yapılandırma) ve ne yapılacağını (yükseltilecek sürüm ya da geçici önlem) söyle; Kısa Kısa'da tek cümleyle. Kaynakta yoksa olmadığını belirt.

**Öne Çıkan GitHub Repoları.** 6-8 repo; GitHub trending, trendshift.io, günlük trending listeleri gibi kaynaklardan.

- Repolar trending listesinin sıralamasından seçilir; "Featured" ya da sponsorlu alanlardaki repoları seçme.
- Her biri için iki cümle: ilki reponun ne olduğunu, ikincisi neden şimdi gündemde olduğunu (yeni sürüm, yeni özellik, bir duyuru) söyler.
- Neden yükseldiği kaynakta görünmeyen, yıllardır bilinen genel amaçlı projeleri yalnızca listeyi doldurmak için seçme; 6 iyi repo 8 vasat repodan iyidir. Aynı kuruluştan en fazla 1 repo al.
- `stars` metni kaynaktaki hassasiyette yazılır: tam sayı görünüyorsa Türkçe binlik ayıracıyla "1.932", kaynak yuvarlanmış "13.4k" veriyorsa "13,4 bin". `starsValue` alanına aynı değeri sayı olarak yaz (13,4 bin → 13400). Mümkünse güncel değeri repo sayfasından al.
- `lang` ve `cat` alanlarını ayrı doldur, `meta` alanını bunlardan oluştur ("Rust · Kategori"; dil yoksa yalnızca kategori). Dili kaynakta (repo sayfası, README, topic etiketi) açıkça görmediysen tahmin etme, `lang` alanını hiç yazma.
- Telif açısından şüpheli projeleri (ör. ticari oyun emülatörleri, recomp) seçme.

**Kısa Kısa.** 6-10 tek-iki cümlelik haber. Okuyucuya değer katmayan tüketici ürünü ya da magazin haberlerini koyma; sayıyı doldurmak için haber ekleme.

**Subtitle.** Her bölümün subtitle'ı yalnızca o bölümdeki haberleri özetler; "Kısa bölüm" gibi bir not yazma. Tek istisna Java & Spring'deki "yeni sürüm yok" notudur.

## 4. Uzunluk ve yerleşim

- Toplam içerik yaklaşık 15 dakikalık okuma olmalı: manşet 4 paragraf, bölüm başına 2-4 haber.
- Yer dağılımını okuyucunun önceliklerine göre yap: 8 kolonluk büyük haberler okuyucunun işine en çok dokunan haberlere gitsin; genel piyasa/finans haberleri ve küçük sürüm notları 4 kolonla yetinsin.
- Izgara 12 kolonludur. Her bölümde `size` değerleri satırları tam dolduracak şekilde seçilir: 8+4, 6+6 ya da 4+4+4. İlk haber genelde `big: true` olur.

**Uzunluk dengesi.** Sayfa aynı satırdaki haberleri eşit yüksekliğe uzatır; biri diğerinden çok uzunsa kısa olanın altında büyük bir boşluk kalır. 8 kolonluk büyük haber iki sütuna dizildiği için aynı metin 4 kolonluk haberin yarısı kadar yer tutar. Bu yüzden:

- 8 kolonluk büyük haber 160-220 kelime, 2-3 paragraf.
- Onunla aynı satırdaki 4 kolonluk haber bunun yaklaşık yarısı: 80-110 kelime, tek paragraf.
- 6+6 satırlarında iki haber 80-110 kelime ve birbirine yakın (fark en fazla 20 kelime). 4+4+4 satırlarında da üç haber yakın uzunlukta.
- Bir haber bu ölçüye sığmıyorsa metni kısaltmak yerine `size` değerini ya da satırdaki eşini değiştir.

**Paragraf uzunluğu.** Manşette ve büyük haberlerde paragraf başına en fazla 80 kelime; daha uzun paragrafı konunun değiştiği yerde ikiye böl. 4 ve 6 kolonluk haberler tek paragraf kalır.

**Başlık uzunluğu.** Manşet başlığı en fazla 80 karakter, haber başlıkları en fazla 70 karakter, 4 kolonluk haberlerde en fazla 60 karakter (boşluklar dahil). Başlık haberin tek ana olgusunu söyler; başlığa sığmayan rakam, tarih ve ikinci olguyu manşette deck'e, haberlerde ilk cümleye taşı. Sayfa manşeti çok büyük puntoyla basar ve başlık paylaşım kartlarında da görünür.

## 5. Kaynak ve doğruluk (en önemli kurallar)

- Haber metninde (headline, deck, paragraphs, figures, stat, chart, briefs, repolar) kaynağında açıkça yazmayan hiçbir ayrıntı, yöntem, sayı ya da nitelendirme yazma. Bilmediğin bir şeyi "mantıklı" diye ekleme; emin değilsen yazma. İki istisna var: 6. bölümdeki kısa jargon açıklamaları (genel bilinen tanım) ve editoryal alanlar (Pratik çıkarım, why, pattern). Editoryal alanlar da yeni olgu içermez.
- Özet/aggregator siteleri (aiweekly.co, theneuron.ai, techstartups roundup'ları, Releasebot vb.) yalnızca haberi ve asıl kaynağı bulmak için kullan. Linklerde asıl kaynağı (resmi duyuru, birincil haber, GitHub issue ya da sürüm notu) ver. Asıl kaynağa ulaşamadıysan haberi atla ya da kicker'ı "İddia" ile işaretleyip metinde asıl kaynağa ulaşılamadığını söyle.
- Tek kaynaklı ve doğrulanmamış iddiaları kicker'ın başına "İddia" ekleyerek işaretle. Bir şirketin yalnızca kendisi hakkındaki ölçüm ve beyanlarını (kendi benchmark'ı, kendi maliyet tasarrufu, kendi vaka çalışması) kicker'ın başında "Şirket beyanı" ile işaretle. Biçim: "İddia · Konu", "Şirket beyanı · Konu".
- Kaynakta bildirenin kendi çekincesi varsa (tekrar üretilemedi, tartışmalı vb.) bunu habere yaz.
- Kendi yorumunu haber cümlesi gibi yazma. Editoryal yorum yalnızca "Pratik çıkarım" kutusunda, haberlerin why alanında ve pattern notunda olabilir; paragraphs içinde yorum olmaz.
- Her haberde en az bir kaynak linki olsun (gerçek URL, uydurma link yok). Rakamları kaynakta yazdığı gibi ver. Kaynaklardan 15 kelimeyi aşan alıntı yapma. Siyasi konularda yorum katma.

## 6. Haber dili

Türkçe yaz; teknik terimler İngilizce kalabilir (context window, release candidate, sandbox vb.). Her haberi kendi cümlelerinle özetle. Satır içi kod, komut ve dosya adlarını `backtick` içine al. Metin içi tırnak ve alıntılar için Türkçe tırnak “ ” kullan; « » veya düz " kullanma. Düz kesme işareti ' ve tire - yaz; tipografik biçimlerini sayfa kendisi üretir.

- **Giriş cümlesi** haberin sonucunu söyler: ne değişti, ne bulundu, ne bozuldu. Tarihle ya da “X şirketi … duyurdu” kalıbıyla açma; tarihi ve duyuranı cümlenin sonuna ya da ikinci cümleye koy. Aynı sayıda iki haber aynı kalıpla açılmasın. İddia ve Şirket beyanı haberlerinde kaynak yine ilk cümlede anılır (“X'e göre” ya da cümle sonunda); yasak olan atıf değil, tarihli duyuru kalıbıdır.
- **Kısa cümle kur.** Bir cümlede en fazla bir noktalı virgül; 25 kelimeyi aşan cümleyi böl. Bir cümlede ikiden fazla karşılaştırma ya da rakam çifti sıralama.
- **Rakam seç, rakam yığma.** Okuyucunun karar vermesine yarayan iki üç rakamı ver, gerisini kaynağa bırak. Grafikteki rakamların hepsini metinde tek tek sıralama; metin grafiğin ne gösterdiğini söylesin ve en fazla ana rakamı ansın. figures ve stat rakamları ise ilgili haberin metninde bir kez geçer.
- **Terimler.** Bir kavram için sayı boyunca tek terim kullan (aynı sayıda hem “istem” hem “prompt” olmaz). Yerleşik Türkçe karşılığı olmayan terimi İngilizce bırak; karşılık uydurma (“skalarlaştırma”, “sınıfı örneklemek” gibi). İngilizce deyimi kelime kelime çevirme: “in the wild” için “sahada istismar” ya da “aktif istismar”, “instantiate” için “nesnesini oluşturmak”.
- **Jargon.** Okuyucu deneyimli bir yazılımcıdır ama her alt alanın uzmanı değildir. Yaygın olmayan bir ürün, protokol, benchmark ya da kısaltmayı ilk geçtiği yerde üç-sekiz kelimeyle açıkla (ör. “Kerberos'un bilet dağıtım sunucusu KDC”). Açıklama kaynakta yazan ya da genel olarak bilinen bir tanım olmalı; emin değilsen açıklama uydurma, terimi çıkar ya da kaynağın ifadesiyle ver. Java, Docker, CVE, RAG, MCP gibi bu okuyucunun bildiği terimleri açıklama.
- **Başlık kipi.** İddia etiketli ya da tek kaynaklı haberin başlığı kesin olgu gibi yazılmaz; başlıkta kaynak ya da “iddia” yer alır (ör. “Sentra: Qubole üzerinden müşteri AWS hesaplarına girildi”). Şirket beyanı haberlerinde başlıktaki ölçüm ya da üstünlük şirkete atfedilir.

## 7. İçerik kurgusu

- **Şirket ağırlığı.** Bir şirket (ürünleriyle birlikte) bir sayıda manşet dışında en fazla 2 haber ve 1 kısa haberle yer alır; aynı günün birden çok duyurusunu tek haberde birleştir. Başka bir konunun haberinde şirketin yalnızca adının geçmesi (ör. bir açığı bulan araç olarak) ve repo listesi bu sınıra girmez. Bu gazeteyi Anthropic'in Claude modeli yazıyor: Anthropic ve Claude haberlerinde diğer şirketlere uyguladığın etiketleri, çekinceleri ve ölçütleri aynen uygula, övgü sıfatı kullanma, rakip ürünleri aynı ayrıntıda ver.
- **Neden önemli (`why`).** Bölümlerdeki her büyük haberde zorunlu, diğer haberlerde isteğe bağlı tek cümle (en fazla 25 kelime). Manşette why yazılmaz; orada "Pratik çıkarım" kutusu var. Haberin bu okuyucu kitlesi için sonucunu söyler: kim etkilenir, neyi değiştirir, ne zaman harekete geçmeli. Sayfa bunu “Neden önemli” etiketiyle metinden ayrı basar; cümleyi bu sözle başlatma. Yalnızca haberde yazan olgulardan çıkan sonucu söyler, yeni olgu ya da rakam getirmez; tahmin, abartı ve “önemli bir adım” gibi içi boş ifadeler yazma. Söyleyecek somut bir şey yoksa küçük haberde boş bırak. why cümlesi uzunluk dengesi kelime sayılarına dahil değildir.
- **Süreklilik (açık uçlar).** Son 3 sayıda sonucu henüz belli olmayan konular vardır: tarihi verilmiş gelecek olaylar (kesinti, geçiş, GA, son tarih) ve “henüz açıklanmadı”, “düzeltme bekleniyor” denen haberler. Tarihi pencereye düşenler için toplam en fazla 3 arama ayır. Birincil kaynakta bir sonuç varsa “Takip” etiketiyle Kısa Kısa'ya ya da ilgili bölüme yaz ve önceki habere iç atıf ver; sonuç yoksa yazma, tahmin yürütme. Takip haberi tekrar sayılmaz.
- **Günün örüntüsü (`pattern`, isteğe bağlı).** Yalnızca bu sayıdaki en az üç haber aynı olguyu paylaşıyorsa ve bu ortaklık her birinin kendi kaynağında açıkça yazıyorsa ekle (ör. üç ayrı güvenlik duyurusunun da açıkların yapay zeka araçlarıyla bulunduğunu belirtmesi). Ortaklığı adlandır ve haberleri say; nedensellik kurma, gelecek tahmini yapma. Zorlama bağlantı kurmaktansa hiç yazma; çoğu gün örüntü olmaz.

## 8. JSON alanları

Alan adları ve biçim için `kurallar/ornek.json` dosyasına bak; o dosya yalnızca yapıyı gösterir, içindeki metinler ve uzunluklar örnek değildir.

- `date` (YYYY-MM-DD), `number` (önceki en büyük number + 1), `dateLabel` ("Çarşamba, 4 Kasım 2026" biçimi), `readingMinutes` (15).
- `figures`: tam 5 adet `{n, l, ref}`; günün çarpıcı rakamları.
- `pattern` (isteğe bağlı): `{title, text, refs[]}`.
- `lead`: `{kicker, alert, headline, deck, paragraphs[], chart?, sources[{label, url}], box{kicker, title, items[], note}}`.
- `sections[]`: `{id, title, subtitle, articles[]}`; haber: `{size: 4|6|8, big?, kicker, alert?, pill?, headline, stat?, paragraphs[], why?, chart?, sources[]}`.
- `repos`: `{subtitle, items[{name, url, stars, starsValue, lang?, cat, why, meta}], sources[]}`.
- `briefs[]`: `{tag, text, url}`.

**Çapalar.** Bir haberin bu sayıdaki çapası: manşet için `manset`, bölüm haberleri için `<bölüm id>-<sıra>` (sıra, bölümün `articles` dizisindeki 1'den başlayan konum; ör. `java` bölümünün ilk haberi → `java-1`). Haberin kendi `id` alanı varsa sıra yerine o kullanılır.

**Rakam şeridi (`figures`).** Sayfa her rakam kutusunu, rakamın geçtiği habere link yapar; `ref` alanına o haberin çapasını yaz. Her rakam bu sayıdaki bir haberde aynen geçmeli; mümkünse 5 rakamı en az 3 farklı habere dağıt. Rakam yalnızca Kısa Kısa ya da repolarda geçiyorsa `ref` yazma. Haber sırasını değiştirirsen ref'leri güncelle.

**İri rakam (`stat`, isteğe bağlı).** Yalnızca `big: true` haberlerde. Biçim: `{"n": "%65-80", "l": "rakamın neyi ölçtüğünü söyleyen kısa açıklama"}`. Sayfa bunu başlığın altında iri puntoyla basar. `n` en fazla 10 karakterlik tek bir rakam ya da aralık, `l` en fazla 80 karakter; rakam kaynakta yazmalı ve haberin ana olgusu olmalı. Bir sayıda en fazla 3 stat; chart olan habere stat koyma, figures'taki bir rakamı stat olarak tekrar etme. Uygun rakam yoksa hiç koyma.

**`pattern` biçimi.** `{"title": "en fazla 60 karakter", "text": "30-60 kelime", "refs": ["guvenlik-2", "java-2", "java-3"]}`; `refs` ilgili haberlerin çapalarıdır, en az 3 tane.

**İç atıflar.** Önceki bir sayıdaki habere atıf yaptığında, o haberin kaynak listesine ek bir kaynak koy: `{"label": "Dünkü sayı: <o haberin kısa başlığı>", "url": "#YYYY-MM-DD-<çapa>"}` (ör. 7 Kasım sayısında `is` bölümünün 4. haberi → `#2026-11-07-is-4`; önceki sayının manşeti → `#YYYY-MM-DD-manset`). Atıf dünkü sayıya değilse etiket "7 Kasım sayısı: ..." biçiminde olsun. Hedefin `issues/` klasöründe gerçekten var olduğunu ve doğru habere işaret ettiğini kontrol et. Kısa Kısa'da `url` alanı aynı biçimde iç link olabilir. Metinde “dünkü sayıda andığımız” gibi bir atıf yapıyorsan iç linki mutlaka ekle.

**Grafikler (`chart`, isteğe bağlı).** Sayfa chart alanını yatay çubuk grafik olarak çizer. Biçim: `{"title": "Ölçü ve birim, ör. ExploitGym başarı oranı (%)", "note"?: "kısa not ya da kaynak uyarısı", "items": [{"label": "...", "value": sayı (>= 0, ham değer), "display": "%48,5 gibi Türkçe biçimli metin", "highlight"?: true}]}`.

- Grafik az ve anlamlı olmalı: bir sayıda 0-3 grafik; zorlama grafik koymaktansa hiç koymamak daha iyidir.
- Grafik yalnızca haberin ANA iddiasını tek bakışta gösteren bir karşılaştırma ise eklenir: aynı şeyin önce/sonra hali (build süresi 18→9 dk), aynı ölçütte rakip ya da önceki sürüm (model A ve B'nin aynı benchmark skoru), aynı görevin iki koşuldaki sonucu.
- Şunları yapma: farklı türden şeyleri aynı grafikte karıştırma (endeksler ile tek tek hisseler, şirketler ile ülkeler); haberin ana konusu olmayan yan rakamları çizme; paragraftaki rakamları sadece listelemek için grafik yapma; farklı ürün kademelerini (ör. standart/highspeed fiyatı) karşılaştırmak gibi okuyucuya yeni bir şey söylemeyen grafikler.
- Her grafik için kendine sor: “Bu çubukların boyu arasındaki fark, haberin söylediği şeyin kendisi mi?” Cevap hayırsa grafik koyma.
- Rakamlar kaynakta açıkça yazmalı ve aynı birimde olmalı (2-5 çubuk); hiçbir değeri tahmin etme, türetme veya uydurma. Şirketin kendi ölçümüyse `note` alanında belirt. Negatif değişimlerde `value` mutlak değer, `display` "−%5,5" olsun. Haberin ana öznesi olan tek çubuğa `highlight: true` ver.
