# The Daily Compiler · editör görevleri

Sabah görevinde taslak yayımlanmadan önce üç editör aynı anda ve birbirinden bağımsız çalışır. Her biri yalnızca kendi bölümünü ve bu dosyanın sonundaki “Bulgu biçimi” bölümünü uygular:

- **Doğruluk editörü:** kaynakları açar; olgu, eksik bilgi, etiket ve Atölye kaynakları.
- **Okur editörü:** okur gözüyle seçim, önem, editoryal alanlar ve dil.
- **Tasarım editörü:** taslaktan üretilen sayfanın ekran görüntüleri.

Ortak kurallar:

- Metni yeniden yazma; repoya ve taslağa hiçbir şey yazma. Yazdığın tek dosya sana verilen bulgu dosyasıdır.
- Uzunluk, sayı, ızgara, alan biçimi, repo tekrarı, iç atıf hedefleri, yasak çeviriler (`tools/kontrol.py`) ile taşma, JavaScript hatası ve kırık iç bağlantı (`tools/ekran.py`) zaten ölçülür; bunlarla vakit harcama. Senin işin yargı gerektirenler.
- Birbirinden bağımsız sayfa okumalarını (WebFetch) ve görüntü okumalarını tek tek değil, aynı anda yap.
- Bulgu yoksa boş liste döndür; liste dolsun diye bulgu üretme.

## Doğruluk editörü

Taslak, önceki sayıların başlık ve çapaları (`previous_headlines.txt`) ve benchmark verisi (`data/modeller.json`) sana verilir. Bir kaynak iki denemede açılmazsa bulgu olarak not et ve geç; bot korumasını aşmaya çalışma.

### Kaynaktan doğrulama

Kaynak linklerini WebFetch ile açarak şunları doğrula:

- manşetin tamamı, Editörün önerileri maddeleri dahil;
- bütün büyük (`big`) haberler ve Güvenlik bölümünün bütün haberleri;
- Takvim'deki her tarih, Acil önlemler listesi, tüm grafikler, stat rakamları ve why satırlarındaki rakamlar;
- kicker'ında İddia ya da Şirket beyanı olan ya da olması gereken haberler;
- bunlara ek en az 6 haber.

Bir rakamın yönü (arttı/azaldı, daha sık/daha seyrek), bir özelliğin ad geçmişi ve kaynağa atfedilen çekinceler en sık yanlış çıkan ayrıntılardır; bunları özellikle kaynakla karşılaştır.

Her birinde sor:

- Her rakam, tarih, isim, ayrıntı ve nitelendirme kaynakta açıkça yazıyor mu? Kaynağın çekinceleri habere yansımış mı?
- Türetilmiş her rakamı (yüzde fark, oran, kat, “yaklaşık X ucuz”) girdilerinden kendin yeniden hesapla. Haberdeki benchmark değerleri `data/modeller.json` ile aynı mı; değilse metin ayar ya da sürüm farkını söylüyor mu?
- Linkler açılıyor mu, asıl kaynak mı? Takvim'deki `ref` tarihin geçtiği habere, `url` tarihin yazdığı kaynağa mı işaret ediyor? Önceki sayılara atıf yapılan yerde iç link var mı?

### Her haberde üç soru

Doğruladığın her haber için bu üç soruyu ayrı ayrı sor ve cevabı “evet” olanı bulgu yaz; bu üçü son haftalarda kural açık olduğu halde en sık kaçan hatalar:

1. Metinde kaynakta yazmayan bir ayrıntı, yöntem, sayı ya da nitelendirme var mı (“mantıklı” diye eklenmiş olanlar dahil)?
2. Güvenlik haberinde etkilenen, yaması olmayan ya da düzeltilmiş sürümlerden kaynakta yazdığı halde metne girmeyen var mı?
3. Editoryal alanlarda (why, Editörün önerileri, Atölye adımları) haber metninde ya da kaynakta olmayan yeni bir olgu var mı?

### Eksik bilgi

Okuyucu “ne değişti, beni etkiliyor mu, ne yapmalıyım, ne zamana kadar” sorularının cevabını alıyor mu? Özellikle:

- **Manşet ve büyük ürün haberleri:** bağımsız bir kaynakta bulunabilen önemli şart, sınır ya da yükümlülük (lisans, telemetri, destek yükümlülüğü, fiyat) eksik mi? Bunu kendin ara. Fiyat, son tarih, uyumluluk gibi pratik bilgi ilk paragrafta mı?
- **Güvenlik haberleri:** etkilenen ve yaması olmayan sürümler, giriş yolu, kontrol yöntemi ve düzeltilmiş sürümden kaynakta olduğu halde yazılmayan var mı? Aktif istismar ya da zehirlenmiş paket varken Acil önlemler boş mu? Geliştirici araçlarını (AI kodlama aracı ayarları, hook, MCP, IDE eklentisi, CI) hedef alan bulguda okurun bugün yapabileceği bir kontrol adımı var mı?
- Pencere içinde atlanmış büyük bir gelişme var mı: yaygın bir hizmetin saatler süren kesintisi, önemli bir model ya da araç sürümü?

### Etiket ve eşit muamele

- Kırmızı (`alert`) yalnızca aktif istismar, zehirlenmiş paket ya da kimlik doğrulamasız RCE haberinde mi?
- Eksik İddia ya da Şirket beyanı etiketi; İddia haberinde kesin kipte başlık; başlığa girmiş şirket iddiası.
- Tek ve ikincil kaynağa dayanan bölüm haberi.
- Anthropic ve Claude haberlerine farklı ölçüt; karşılaştırmada bir modelin (Claude dahil) rakam yerine sıfatla geçilmesi.

### Atölye kaynakları

Atölye kuralları `kurallar/ATOLYE.md` dosyasındadır. Atölye'nin bütün kaynaklarını aç ve şunlara bak:

- Her adım, uyarı ve rakam kaynaklardan birinde yazıyor mu? Kaynakta olmayan “en iyi uygulama” kanaati var mı?
- Örnek blok doğru mu: komutlar ve dosya yolları o araç için geçerli mi, sözdizimi bozuk mu, çalıştırıldığında zarar verebilecek ya da gizli bilgi isteyen bir satır var mı?
- Ölçüm yokken “kanıtlanmış” deniyor mu; bir araca övgü sıfatı var mı?
- Araca özgü ayrıntı güncel mi (12 aydan eski kaynakta özellikle)?
- Rakamların ölçüm koşulu (kim ölçtü, hangi ayarda) kaynaktaki gibi korunmuş mu?

Puanın: `dogruluk`.

## Okur editörü

Taslak, `kurallar/KURALLAR.md`, `kurallar/TERIMLER.md`, `kurallar/ATOLYE.md` ve `previous_headlines.txt` sana verilir. Kaynak açmazsın; tek istisna, bir cümle kendi içinde ya da başka bir haberle çelişiyorsa o cümlenin kaynağı (en çok 3 sayfa).

### Seçim ve önem

- Manşet kurala uyuyor mu: AI/LLM, aynı şirket ya da ürün ailesi art arda ikinci kez değil, güvenlik temalı manşet art arda ikinci kez değil.
- Son 3 sayıyla tekrar (Takip haberleri hariç), pencere dışı haber.
- Öncelik ve yer dağılımı: büyük haberler okuyucunun işine en çok dokunanlara mı gitmiş; Java & Spring'de JVM dışı haber ya da haber varken okuma yazısı; şirket ağırlığı ve bölüm dışı güvenlik sınırı.

### Dil ve editoryal alanlar

- Haber cümlesi gibi yazılmış yorum; düz çeviri, aynı olgunun iki kez söylenmesi, dolgu cümlesi, terim tutarsızlığı, `kurallar/TERIMLER.md` sözlüğüne aykırı terim (yazılımcının İngilizce kullandığı bir terimin Türkçeleştirilmesi ya da yerleşik Türkçesi olanın İngilizce bırakılması), açıklanmamış ya da yanlış açıklanmış jargon, alanın yanlış terimi; sözlükte olmasa da yazılımcının İngilizce kullandığı bir terimin Türkçe karşılıkla yazılması (betik, el sıkışma, damıtma, ortanca gibi) ve şirket, ürün ya da özellik adının çevrilmesi. Terim bulgusunda doğru terimi ve sözlüğe eklenmesi gerekip gerekmediğini yaz; metinde belirli bir kişiye ya da şirkete hitap.
- Editörün önerilerinde genel ya da önceki sayılardan tekrar eden madde; metinde olmayan yeni bir olgu getiren madde.
- why satırında abartı, haberdeki olgulara dayanmayan çıkarım ya da şirket açıklamasının tekrarı.
- Repolarda ikinci cümle “neden şimdi”yi söylüyor mu, `lang` kaynakta görülmüş mü.
- 25 kelimeyi aşan cümle, çeviri kokan cümle, yanlış ek, belirsiz gönderim (“bu”, “daha az” neyi niteliyor?).
- “Açıklanmadı / belirtmiyor” cümleleri: okurun kararını etkilemeyen eksiklik yazılmış mı, haber böyle bir cümleyle mi bitiyor? Kararı etkileyen bir eksiklik sonucuyla birlikte söylenmiş mi?
- Bir paragrafta birikmiş karşılaştırmalı rakamlar tabloya ya da grafiğe taşınabilir mi? Acil önlemler, sayının uyarı taşıyan bütün açıklarını ciddiyet sırasıyla kapsıyor mu?

### Terim taraması

Dil kontrolünden ayrı, ayrı bir adım olarak yap: taslaktaki her teknik terimi bölüm bölüm çıkar (başlık, deck, metin, why, Editörün önerileri, etiketler, tablo başlıkları, Atölye, repolar, Kısa Kısa) ve her biri için sor: Türk bir yazılımcı bunu PR yorumunda ya da Slack'te nasıl yazar? Türkçe karşılığı yerleşik değilse (betik, akıl yürütme, kod golfü gibi) ya da bir şirket, ürün, özellik, plan veya ayar adı çevrilmişse bulgudur. Emin olmadığın terimi de `kucuk` bulgu olarak yaz. Aynı kavramın sayı içinde iki farklı terimle yazılması da bulgudur.

### Atölye okunurluğu

- Okuyucu bugün uygulayabilir mi, yoksa yazı genel tavsiye mi? Adımların ilk cümlesi kısa bir buyruk mu?
- Rakamların ölçeği ve neyi ölçtüğü yazıyor mu? Uygulamaya bir şey katmayan deney anekdotu var mı?

Puanların: `icerik` (seçim, değer, editoryal kalite) ve `dil`.

## Tasarım editörü

`kurallar/TASARIM.md`, `tools/ekran.py` çıktısı ve `/tmp/dc/ekran/` altındaki görüntüler (telefon dikey, telefon yatay, tablet ve masaüstü) sana verilir. Betik bölünen kod, uzun satır, sayfa sonu sekmesi, kadran ve telefondaki katlamayı zaten ölçer. Ölçülebilir kusur aramakla yetinme: görüntüye bir okur gözüyle bak ve `kurallar/TASARIM.md` ilkelerine (seyreklik, tutarlılık, renge dayanmayan ayrım, yönlendirme, dolgu) aykırı olanı da bulgu olarak yaz. `/tmp/dc/acik-kod.txt` henüz düzeltilmemiş kod bulgularıdır; bunları yeniden yazma. Görüntülere tek tek bak:

- hizalama ve boşluk dengesi; erken kırılan, taşan ya da tek kelimesi alt satıra düşen satır;
- satır içi kodun ya da bağlantı okunun kendi içinden bölünmesi;
- emoji gibi çizilen karakter, düz kalan tırnak ya da kesme işareti, yanlış kısa çizgi;
- üst üste binme; okunurluk ve kontrast;
- aynı bileşenin farklı yerlerde farklı görünmesi;
- telefonda dokunma hedefi;
- dolgu başlık ya da etiket, yanıltıcı bağlantı metni, gözden kaçan önemli bağlantı;
- yalnızca renkle yapılmış ayrım, aynı satırda yan yana duran iki farklı bileşen.

Sorunun içerikten mi (çok uzun başlık, elle kırılmış örnek satırları) yoksa koddan mı geldiğini ayır; içerikten geliyorsa taslakta nasıl düzeltileceğini öner. Puanın: `tasarim`.

## Bulgu biçimi

Bulgularını sana verilen dosyaya (`/tmp/dc/bulgular-<rol>.json`) yaz:

```json
{"rol": "dogruluk",
 "puan": {"dogruluk": 7.5},
 "gerekce": {"dogruluk": "Tek cümle."},
 "dogrulanan": 18,
 "bulgular": [
  {"kategori": "dogruluk", "onem": "kritik", "konum": "ai-4 · <haber başlığı> ya da JSON yolu",
   "sorun": "...", "kanit": "Kaynakta ne yazıyor; URL (ya da görüntü dosyası)", "oneri": "..."}
 ]}
```

- `puan`: taslağın senin alanındaki kalitesi, 0-10. 9, okurun hiçbir düzeltme istemeyeceği bir sayıdır. Ölçek her gün aynıdır.
- `dogrulanan`: yalnızca doğruluk editörü; kaynağını açarak doğruladığın haber sayısı.
- `kategori`: `dogruluk`, `kaynak`, `eksik-bilgi`, `etiket`, `secim`, `editoryal`, `dil`, `terim`, `atolye`, `tasarim` ya da `teknik`.
- `onem`:
  - `kritik`: yanlış, kaynaksız ya da kaynağın söylediğini aşan bilgi.
  - `onemli`: yeniden hesapta tutmayan rakam; okuyucunun karar vermesi için gereken eksik bilgi; eksik etiket ya da İddia haberinde kesin kipte başlık; eşit muamele ihlali; tekrar ya da pencere dışı haber; dayanaksız why; kaynak kalitesi; önceliklendirme; belirgin tasarım bozukluğu.
  - `kucuk`: dil ve biçim.
- Önem sırasına göre yaz. `durum`, `kok` ve `kural` alanlarını yazma; onları yazar doldurur.

Dosyayı yazdıktan sonra cevabında yalnızca bulgu sayılarını ve dosya yolunu söyle.
