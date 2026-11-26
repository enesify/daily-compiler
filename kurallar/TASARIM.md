# Tasarım ilkeleri

The Daily Compiler bir gazete: sakin, editoryal, tipografiyle konuşan bir sayfa. Bu dosya tasarım editörünün (`kurallar/EDITOR.md`) ve haftalık tasarım incelemesinin ölçütüdür. Bir ekran görüntüsü teknik olarak kusursuz olsa da bu ilkelere aykırıysa bulgudur.

## Dil

- Görsel yok; tek istisna 404 sayfasındaki çizgi çizim (yayıncı onaylı). Kimlik tipografi, ince çizgiler, kâğıt zemin ve tek vurgu rengiyle (petrol) kurulur. Emoji, stok görsel, gölge, gradyan ve süs öğesi kullanılmaz; ikonlar sitenin çizgi ikonlarıdır.
- Yazı tipleri: başlık ve metin Newsreader, etiketler IBM Plex Sans Condensed, kod IBM Plex Mono. Etiket büyük harf ve harf aralıklı, metin serif.
- Hareket yalnızca okurun bir eylemine yanıt olarak (açma, kopyalama onayı) kullanılır.

## Seyreklik ve tutarlılık

- Vurgu (çerçeve, zemin, renk, kalın) yalnızca seyrek öğede kullanılır; her haberde tekrarlanan bileşen sade kalır. Her habere uygulanan bir vurgu uyarının etkisini yok eder.
- Aynı türde bilgi her yerde aynı bileşenle gösterilir. Aynı satırda iki farklı bileşen (ör. kutulu ve kutusuz etiket) yan yana durmaz.
- Numaralı listeler (Editörün önerileri, Atölye adımları) aynı numara bileşenini kullanır: kod yazısıyla, ince petrol çerçeveli “01”. Yeni bir numaralı liste de bunu kullanır.
- Yeni bir öğe gerekmeden önce sitede aynı işi yapan bir kalıp aranır (“Devamı”, sayfa sonu gezinmesi, kaynak satırı).

## Ayrım ve erişilebilirlik

- Bir ayrım yalnızca renge ya da ince bir işarete dayanmaz; biçim (italik, büyük harf), konum ya da sözcük de ayırır. Gri tonlamada da okunur olmalı.
- Kırmızı yalnızca acil güvenlik haberindedir.
- Telefonda dokunma hedefi en az 44 px; metin ile zemin arasında yeterli kontrast.

## Okuma

- Satır uzunluğu metin sütununu ve yaklaşık 80 karakteri geçmez; yatay telefon ve tablette de. Liste, kutu ve tablo metin sütunundan geniş olmaz.
- Kod, kimlik (CVE, GHSA), sürümlü ad (GPT-6.2), repo adı ve tarih (8 Aralık) satır sonunda bölünmez; bağlantı oku son sözcükten ayrılmaz.
- Büyük harfe çevrilen İngilizce özel adlar noktasız I ile yazılır (MITEL, GITHUB).
- Grafik ve tablolarda yorum, süs ve eksik değer açıklaması yok; bileşenler birbirine benzer.

## Yönlendirme

- Önemli bir bağlantı görünür olur ve ne açacağını söyler; kaynak satırı ya da kapanış çizgisi gibi “bölüm bitti” işaretinin altında kalmaz.
- Bağlantı ve etiket metni yanıltmaz: “tamamı” denmez, gerçekte olmayan bir sayı yazılmaz.
- Okur bir öğeye dokununca ne olacağını tahmin edebilmeli (sayfa değişiyor mu, içerik yerinde mi açılıyor?).

## Dolgu

- Anlam taşımayan başlık, etiket ve açıklama yazılmaz (“Bugün yapılacaklar”, “Bu kutu editoryal öneridir”). Etiketin adı ne olduğunu söyler, buyurmaz.
- Aynı bilgi iki yerde verilmez (altbilgi ve Hakkında gibi). İstisna: 404 sayfasındaki bağlantılar, yolunu kaybeden okura ikinci bir yol olarak kalır.

## Ekranlar

Her inceleme şu ekranlarda yapılır: telefon dikey (390 px), telefon yatay (844 px), tablet (820 px), masaüstü (1440 px). Site açık ve karanlık temada aynı ilkelere uyar.
