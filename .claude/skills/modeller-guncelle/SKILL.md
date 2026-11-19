---
name: modeller-guncelle
description: The Daily Compiler'ın Benchmark sayfasının verisini (data/modeller.json) bağımsız benchmark tablolarından yeniler. Yeni bir model çıktığında ya da tools/modeller.py "GÜNCELLE" dediğinde kullanılır.
---

# Benchmark verisini güncelle

`data/modeller.json`, `benchmark.html` sayfasının ve her sayıdaki “Benchmark” bandının tek veri kaynağıdır. Liste kodu (`assets/modeller.js`, `build.py`) bu dosyadan üretilir; bu oturum koda dokunmaz, yalnızca veri dosyasını yeniler.

## Ne zaman

- `python3 tools/modeller.py --yas 7` çıktısında `GÜNCELLE` varsa (veri eskiyse ya da ana listede 20'den az model varsa), ya da
- bugünkü sayıda listedeki ya da listeye girebilecek bir modelin yeni sürüm haberi varsa.

İkisi de yoksa bu adımlar atlanır; tablo her gün değişmek zorunda değildir.

## Kaynaklar

| Anahtar | Tablo | Ölçütler |
|---|---|---|
| `aa` | https://artificialanalysis.ai/leaderboards/models | `zeka` (Intelligence Index), `maliyet` (Cost per Task, $), `sure` (Time per Task, dk) |
| `cursor` | https://cursor.com/evals | `kodlama` (Score, %), `kod_maliyet` (Cost / task, $) |

Yalnızca bu iki tablonun kendi sayfası okunur. Rakam başka bir siteden (derleme siteleri, haber, sosyal medya), şirketin kendi duyurusundan ya da hafızadan alınmaz. Tablo okunamıyorsa ya da satırlar eksik geliyorsa dosya **değiştirilmez**; eski veri eski tarihiyle kalır.

## Kurallar (editoryal seçim yoktur)

Her sekme ilk `ilk` (şu an 20) modeli gösterir. Veri iki listeden oluşur:

1. **Ana liste (Zekâ, Maliyet, Süre sekmeleri):** `aa` tablosunda zekâ endeksine göre ilk 20 farklı model. Listede en az 2 açık ağırlıklı model olmalıdır; ilk 20'de 2'den az varsa, eksik kalan kadar sondaki kapalı model çıkarılır ve yerine en yüksek puanlı açık model girer (liste yine 20). Aynı ailenin farklı adlı modelleri (ör. “Muse Wonder” ile “Muse Wonder Full”) ayrı modeldir. Maliyet ve Süre sekmeleri zekâ sırasındaki ilk 20 modeli kendi ölçütlerine göre sıralar; tablonun en ucuz ya da en hızlı modelleri ayrıca eklenmez. Ana listedeki bir modelin maliyet ya da süresi tabloda yoksa (“--”), o sekmenin 20'ye tamamlanması için zekâ sırasındaki bir sonraki model (21., gerekirse 22.) `"yalniz": ["maliyet", "sure"]` alanıyla eklenir (yalnızca eksik olan sekme(ler) yazılır); bu model Zekâ sekmesinde görünmez.
2. **Hangi ayar:** Aynı modelin birden çok satırı varsa (max, xhigh, high…) zekâ endeksi en yüksek satır alınır; eşitlikte maliyeti düşük olan. Seçilen ayar `ayar` alanına küçük harfle yazılır (ayarı olmayan modelde boş metin).
3. **Kodlama sekmesi:** `cursor` tablosunda ilk 20 farklı model. Ana listedeki bir modelin `kodlama` ve `kod_maliyet` değeri, `cursor` tablosundaki **aynı ayarlı** satırdan alınır (“Extra High” = `xhigh`). Aynı ayarlı satır yoksa ama model tabloda başka ayarla varsa, o modelin en yüksek puanlı satırı alınır ve ayarı `kod_ayar` alanına küçük harfle yazılır (sayfa “kodlamada xhigh” diye gösterir). Model tabloda hiç yoksa ikisi de `null`; önceki sürümün rakamı yazılmaz. Ana listede olmayan bir model, `cursor` tablosundaki en yüksek puanlı satırıyla ve `"yalniz": "kodlama"` alanıyla eklenir: `ayar` o satırın ayarı, `kodlama` ve `kod_maliyet` o satırdan, diğer ölçütleri `null`. Kodlama sekmesi bütün modelleri puana göre sıralayıp ilk 20'yi gösterir; `cursor` tablosunun ilk 20 farklı modelinin her biri ya ana listede ya `yalniz` olarak dosyada olmalıdır.
4. **Eksik sekme:** `tools/modeller.py` bir sekmede 20'den az model görürse `GÜNCELLE` der. Kaynak tablosunda gerçekten yeterli satır yoksa (ör. CursorBench'te 20'den az model), dosyanın köküne `"eksik_onaylandi": "<updated ile aynı tarih>"` yazılır; uyarı aynı veri için tekrar `GÜNCELLE` demez.
5. **Eksik değer:** Tabloda “--” olan ya da hiç bulunmayan her değer `null`. Tahmin, yuvarlama ya da başka kaynaktan tamamlama yok.
6. **Sıra:** `models` dizisinde önce ana liste zekâ endeksine göre büyükten küçüğe, sonra `yalniz` modeller kodlama puanına göre.
7. **Adlar:** `ad` tablodaki tam ad (ayar parantezi olmadan), `kisa` sayı içindeki bantta görünecek ad (en çok 22 karakter; “Claude” ön eki atılır), `saglayici` şirket adı, `acik` açık ağırlıklı ise `true`.
8. Anthropic modelleri dahil hiçbir model kural dışında eklenmez, çıkarılmaz ya da öne alınmaz. Sayfaya “en iyi model” türü yorum eklenmez.

## Adımlar

1. İki tabloyu aç ve satırları oku. `aa` için ilk 80 satır, `cursor` için bütün tablo okunur; açık modelleri sayfanın “open weights” notundan ya da filtresinden doğrula.
2. Kurallara göre model listesini ve değerleri çıkar; `data/modeller.json` içinde yalnızca `updated`, `models` ve (kaynak sürümü değiştiyse) `sources.*.note` alanlarını yenile. `metrics` ve `sekmeler` olduğu gibi kalır.
3. Yazdığın her rakamı kaynak tablodaki satırla bir kez daha tek tek karşılaştır.
4. `python3 tools/modeller.py` çalıştır; `HATA` varsa düzelt, düzeltilemiyorsa değişikliği geri al (`git checkout data/modeller.json`).
5. `python3 build.py` ile siteyi üret. `data/modeller.json`, `benchmark.html`, `index.html` ve `sayi/` sayfaları günün sayısıyla aynı commit'e girer.

## Yeni ölçüt eklemek (günlük oturumun işi değildir)

Yeni bir ölçüt, ancak listedeki modellerin en az altısı için tablosu eksiksiz okunabilen bağımsız bir kaynak bulunduğunda eklenir: `sources` içine kaynak, `metrics` içine ölçüt (`ad`: tam ad; `detay`: açılan satırdaki kısa ad; `bicim`: puan / yuzde / usd / dk; `iyi`: yuksek / dusuk, liste bu yöne göre sıralanır; sekmede görünecekse `sekme`: kısa ad), sekme olacaksa `sekmeler` dizisine anahtarı (ilki sayı içindeki bandın ölçütüdür), her modele alan. Kod değişikliği gerekmez. Bu kararı gazetenin sahibi verir.
