# Sürüm notları

Etiketler yalnızca sitenin kodu, tasarımı ve sabah görevinin kuralları değiştiğinde atılır; günlük sayılar etiketlenmez (onların sayı numarası vardır).

- **Büyük sürüm (v2.0):** sayı dosyasının biçimini ya da kuralları temelden değiştiren işler
- **Ara sürüm (v1.1):** yeni özellik ya da tasarım değişikliği
- **Düzeltme (v1.0.1):** hata düzeltmeleri

## v1.1 · 17 Kasım 2026

### Yeni bölüm: Atölye
- Her sayıda bir uygulama yazısı: yapay zekâyı ve agent'ları yazılım geliştirmede (SDLC, mimari, agentic geliştirme, CI/CD), araştırma ve analizde kullanmanın somut bir yolu; 2-3 dakikalık okuma
- Masaüstünde solda giriş, “Ne zaman” ve numaralı adımlar (ilk cümle kalın), sağda kopyalanabilir örnek blok, sık yapılan hata ve kaynaklar; telefonda tek sütun, “Devamı” ile açılır
- Kopyalama düğmesi tema düğmesiyle aynı çizgi ikon; kopyalanınca onay işaretine döner
- Kurallar `kurallar/ATOLYE.md`: konu seçimi (önce günün haberi, yoksa konu bankası), her önerinin kaynağa dayanması, ölçüm dürüstlüğü, esnek araç tarafsızlığı, 6 kategoride 89 konuluk banka
- Denetim: `tools/kontrol.py` alanları, uzunluğu, 45 gün içinde konu tekrarını, örnekte zararlı komut ya da gizli bilgiyi denetler; `tools/ozet.py` son 45 günün konularını ve aday konuları verir; editör Atölye'nin kaynaklarını ve örneğini ayrıca doğrular

## v1.0 · 16 Kasım 2026

Gazetenin ilk tutarlı sürümü. 3 Kasım'daki ilk sayıdan bu yana yapılan işler; değerlendirme puanları: okuyucu 7,3/10 (Sayı 12-13), tasarım 7,5/10.

### Sayı sayfası
- Fraunces italik logo, solda tarih; tema düğmesi; yapışkan bölüm menüsü (masaüstünde tam logo, telefonda bitişik DC), kaydırma oku ve iki yanda solma
- Sayılar arası gezinme: yalnızca önceki / sonraki sayı; telefonda kaydırarak geçiş
- Manşet, Pratik çıkarım, Bu sayıda listesi ve Takvim; telefonda manşet ilk ekranda, haberler cümle sonunda kesilip “Devamı” ile açılır
- 12 sütunlu haber ızgarası; “Neden önemli”, iri rakam, grafik, Günün örüntüsü; Güvenlik'te “Bugün yamala”; sayı sonunda Düzeltme
- Kaynaklar: beş ve fazlasında ilk üçü görünür, iç atıflar ↩ ile önceki sayıdaki habere gider

### Diğer sayfalar
- Benchmark: bağımsız ölçümlerle sıralı liste, ölçüt sekmeleri, kayan satır animasyonu, satır açınca bütün ölçütler; her sayının sonunda ilk beş bandı
- Arşiv: ay ay liste ve arama (veri ay ay ayrı dosyalarda, ilk aramada yüklenir)
- Hakkında: yöntem, etiketler, çıkar çatışması, düzeltmeler listesi
- RSS akışı, paylaşım kartı, favicon ve iPhone/Android simgesi (bitişik DC)

### Altyapı
- Yazı tipleri sitenin kendi sunucusundan; spot italiği 17 KB alt küme
- Erişilebilirlik: içeriğe geç linki, dokunmatikte 44 px hedefler, kontrast, hareket azaltma
- Telefonda kesme ve Benchmark yerleşiminde toplu ölçüm; açılışta düzen kayması yok

### Sabah görevi
- Adımlar `kurallar/GOREV.md`, kurallar `kurallar/KURALLAR.md`, editör görevi `kurallar/EDITOR.md`
- Araçlar: `ozet.py` (son sayıların özeti, takvim adayları, açık uçlar), `kontrol.py` (ölçülebilir kurallar), `ara.py` (bütün arşivde arama), `bulgular.py` (editör bulguları ve bildirim özeti), `modeller.py` (benchmark verisi)
- Yazar ve ayrı bir editör ajanı; paralel arama, araştırma notu, biçimli editör bulguları
