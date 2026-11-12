---
name: modeller-guncelle
description: The Daily Compiler'ın Modeller sayfasının verisini (data/modeller.json) bağımsız benchmark tablolarından yeniler. Yeni bir model çıktığında ya da tools/modeller.py "GÜNCELLE" dediğinde kullanılır.
---

# Modeller verisini güncelle

`data/modeller.json`, `modeller.html` sayfasının ve her sayıdaki “Modeller” bandının tek veri kaynağıdır. Grafik kodu (`assets/modeller.js`, `build.py`) bu dosyadan çizer; bu oturum koda dokunmaz, yalnızca veri dosyasını yeniler.

## Ne zaman

- `python3 tools/modeller.py --yas 7` çıktısında `GÜNCELLE` varsa, ya da
- bugünkü sayıda listedeki ya da listeye girebilecek bir modelin yeni sürüm haberi varsa.

İkisi de yoksa bu adımlar atlanır; tablo her gün değişmek zorunda değildir.

## Kaynaklar

| Anahtar | Tablo | Ölçütler |
|---|---|---|
| `aa` | https://artificialanalysis.ai/leaderboards/models | `zeka` (Intelligence Index), `maliyet` (Cost per Task, $), `sure` (Time per Task, dk) |
| `cursor` | https://cursor.com/evals | `kodlama` (Score, %), `kod_maliyet` (Cost / task, $) |

Yalnızca bu iki tablonun kendi sayfası okunur. Rakam başka bir siteden (derleme siteleri, haber, sosyal medya), şirketin kendi duyurusundan ya da hafızadan alınmaz. Tablo okunamıyorsa ya da satırlar eksik geliyorsa dosya **değiştirilmez**; eski veri eski tarihiyle kalır.

## Kurallar (editoryal seçim yoktur)

1. **Hangi modeller:** `aa` tablosunda zekâ endeksine göre ilk 10 farklı model. Listede en az 2 açık ağırlıklı model olmalıdır; ilk 10'da 2'den az varsa, eksik kalan kadar en yüksek puanlı açık model sona eklenir (toplam en çok 12 model). Aynı ailenin farklı adlı modelleri (ör. “Muse Wonder” ile “Muse Wonder Full”) ayrı modeldir.
2. **Hangi ayar:** Aynı modelin birden çok satırı varsa (max, xhigh, high…) zekâ endeksi en yüksek satır alınır; eşitlikte maliyeti düşük olan. Seçilen ayar `ayar` alanına küçük harfle yazılır (ayarı olmayan modelde boş metin).
3. **Kodlama:** `cursor` tablosunda aynı modelin **aynı ayarlı** satırı varsa `kodlama` ve `kod_maliyet` oradan alınır (“Extra High” = `xhigh`). Model ya da o ayar tabloda yoksa ikisi de `null` olur; başka ayarın ya da önceki sürümün rakamı yazılmaz.
4. **Eksik değer:** Tabloda “--” olan ya da hiç bulunmayan her değer `null`. Tahmin, yuvarlama ya da başka kaynaktan tamamlama yok.
5. **Sıra:** `models` dizisi zekâ endeksine göre büyükten küçüğe.
6. **Adlar:** `ad` tablodaki tam ad (ayar parantezi olmadan), `kisa` etikette görünecek ad (en çok 22 karakter; “Claude” ön eki atılır), `saglayici` şirket adı, `acik` açık ağırlıklı ise `true`.
7. Anthropic modelleri dahil hiçbir model kural dışında eklenmez, çıkarılmaz ya da öne alınmaz. Sayfaya “en iyi model” türü yorum eklenmez.

## Adımlar

1. İki tabloyu aç ve satırları oku. `aa` için ilk 60 satır yeterlidir; açık modelleri sayfanın “open weights” notundan ya da filtresinden doğrula.
2. Kurallara göre model listesini ve değerleri çıkar; `data/modeller.json` içinde yalnızca `updated`, `models` ve (kaynak sürümü değiştiyse) `sources.*.note` alanlarını yenile. `metrics` ve `views` olduğu gibi kalır.
3. Yazdığın her rakamı kaynak tablodaki satırla bir kez daha tek tek karşılaştır.
4. `python3 tools/modeller.py` çalıştır; `HATA` varsa düzelt, düzeltilemiyorsa değişikliği geri al (`git checkout data/modeller.json`).
5. `python3 build.py` ile siteyi üret. `data/modeller.json`, `modeller.html`, `index.html` ve `sayi/` sayfaları günün sayısıyla aynı commit'e girer.

## Yeni ölçüt eklemek (günlük oturumun işi değildir)

Yeni bir ölçüt ya da görünüm, ancak listedeki modellerin en az altısı için tablosu eksiksiz okunabilen bağımsız bir kaynak bulunduğunda eklenir: `sources` içine kaynak, `metrics` içine ölçüt (`bicim`: puan / yuzde / usd / dk; `iyi`: yuksek / dusuk; gerekirse `log`), `views` içine görünüm, her modele alan. Kod değişikliği gerekmez. Bu kararı gazetenin sahibi verir.
