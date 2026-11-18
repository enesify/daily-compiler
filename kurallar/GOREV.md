# The Daily Compiler · günlük sayı görevi

Bu dosya her sabah çalışan zamanlanmış görevin adımlarıdır. Görev bu dosyayı okuyup baştan sona uygular; zamanlanmış görevin kendi metni yalnızca buraya yönlendirir. Süreç değiştiğinde bu dosya, kurallarla aynı commit'te güncellenir.

Gazete https://dailycompiler.com adresinde, GitHub Pages ile `enesify/daily-compiler` reposunun `main` dalından yayımlanır.

## Sınırlar

- Yazım ve seçim kurallarının tamamı `kurallar/KURALLAR.md` dosyasındadır; yazmaya başlamadan önce baştan sona oku ve uygula. Alan adları ve biçim için örnek `kurallar/ornek.json`.
- Her sayının içeriği `issues/YYYY-MM-DD.json` dosyasıdır (tek doğruluk kaynağı); sayfalar `python3 build.py` ile bu dosyalardan üretilir.
- Yalnızca yeni `issues/<bugün>.json` ve `data/inceleme/<bugün>.json` dosyalarını eklersin, gerekiyorsa `data/modeller.json` dosyasını yenilersin ve `build.py`'yi çalıştırırsın. `build.py`, `assets/`, `kurallar/`, `tools/`, `CLAUDE.md` ve eski sayılara DOKUNMA. Bir kural yanlış, eksik ya da çelişkili görünüyorsa dosyayı değiştirme; en makul yorumu uygula ve son bildirimde belirt.
- Eski sayılar asla silinmez ve değiştirilmez. Önceki bir sayıda olgu hatası fark edersen (araştırırken, takip haberi yazarken ya da bir editör bulgusundan) bugünün sayısına `corrections` olarak ekle. Bugünün sayısındaki hatalar yayından önce düzeltilir; bunlar `corrections`'a girmez.
- Değişiklikleri doğrudan `main` dalına push et; `claude/` ile başlayan dal ya da pull request açma.
- Bu oturumda sen YAZARSIN; 4. adımda üç ayrı editör agent taslağı yayından önce denetler (`kurallar/EDITOR.md`).

## Verimli çalışma

Bunlar sonucu değiştirmez, yalnızca süreyi ve token kullanımını azaltır:

- **Paralel çağrı.** Birbirine bağlı olmayan aramaları (WebSearch) ve sayfa okumalarını (WebFetch) tek tek değil, aynı anda gönder; örneğin bir bölümün bütün aramalarını tek seferde, bir aramanın sonuçlarından okunacak sayfaları tek seferde.
- **Araştırma notu.** Okuduğun her kaynaktan kullanacağın olguları (rakam, tarih, isim, kısa alıntı) ve URL'yi `/tmp/dc/notlar.md` dosyasına kısaca yaz. Taslağı yazarken ve editör bulgularını düzeltirken önce bu notlara bak; aynı sayfayı yalnızca notta olmayan bir ayrıntı gerekiyorsa yeniden aç. Bu dosya editöre verilmez.
- **Taslağı yeniden yazma.** Taslak bir kez yazıldıktan sonra denetim aracının ve editörün bulgularını Edit aracıyla yalnızca ilgili alanı değiştirerek düzelt; dosyayı baştan yazma.
- Önceki sayıların tam metnini okuma; özet çıktısı yeterlidir. Son 3 sayıdan eski bir konu için `python3 tools/ara.py "<konu>"` ile arşivde ara (adres ve eşleşen cümleyi verir); yalnızca bir iç atıf ya da takip haberi için gerekiyorsa ilgili haberi aç.

## Adımlar

1. **Hazırlık.** Repo kökünde olduğunu ve `git status`'un temiz olduğunu doğrula; `git pull --ff-only origin main` ile güncelle. `python3 tools/ozet.py --out /tmp/dc` çalıştır. Çıktı bugünün tarihini (Europe/Istanbul) ve dateLabel'ı, zaman penceresini, sıradaki number'ı, önceki manşeti, son 7 günün repolarını, takvim adaylarını, son sayıların Pratik çıkarım maddelerini, son 3 sayının başlıklarını (iç atıf adresleriyle) ve olası açık uçları verir; editör için `/tmp/dc/previous_headlines.txt` dosyasını yazar. Çıktı bugünün sayısının zaten var olduğunu söylüyorsa yeniden yazma, dur ve bildir.
2. **Kurallar.** `kurallar/KURALLAR.md`, `kurallar/ATOLYE.md`, `kurallar/TERIMLER.md` ve `kurallar/ornek.json` dosyalarını oku.
3. **Araştırma ve yazım.** Kurallara göre araştır. Seçtiğin her haberin konusunu (şirket, ürün ya da proje adı) `tools/ara.py` ile arşivde ara: daha önce yazıldıysa yeni gelişme olup olmadığına bak ve iç atıf ver. Haberler belli olduktan sonra Atölye konusunu seç: önce günün haberlerinde okuyucunun hemen kullanabileceği bir yöntem ara; yoksa özet çıktısındaki ATÖLYE bloğunun adaylarından birini al (son 45 günde işlenmemiş, az işlenen kategoriden). Atölye kaynaklarını da açıp oku; her adım bir kaynağa dayanmalı. Taslağı doğrudan `issues/<bugün>.json` olarak yaz (5. adıma kadar commit edilmez). `python3 tools/kontrol.py issues/<bugün>.json` çalıştır: HATA satırlarının hepsini düzelt; UYARI satırlarını gözden geçir ve geçerli bir gerekçen yoksa düzelt. Hata kalmayana kadar tekrarla.
4. **Yayından önce inceleme (tek tur, üç editör paralel).**
   1. `python3 build.py`, ardından `python3 tools/ekran.py <bugün> --out /tmp/dc/ekran` çalıştır. Sayfa yalnızca yerelde üretilir; henüz commit ve push yok. Betiğin yazdığı taşma, JavaScript hatası ve kırık bağlantı satırları bulgudur. Betik “ARAÇ YOK” derse tasarım editörünü başlatma ve bunu bildirimde belirt; Playwright ya da tarayıcı kurmaya ayrıca çalışma.
   2. Agent aracıyla (subagent_type "general-purpose") üç editörü **aynı anda** başlat: doğruluk, okur, tasarım. Her birine yalnızca şunları ver:
      - görevinin `kurallar/EDITOR.md` dosyasındaki kendi bölümü ve “Bulgu biçimi” bölümü olduğu (tam yoluyla);
      - taslak `issues/<bugün>.json` ve bugünün tarihi;
      - doğruluk ve okur editörüne `/tmp/dc/previous_headlines.txt`; doğruluk editörüne `data/modeller.json`; okur editörüne `kurallar/KURALLAR.md`, `kurallar/TERIMLER.md` ve `kurallar/ATOLYE.md`; tasarım editörüne `ekran.py` çıktısı ve `/tmp/dc/ekran/` (tam yollarıyla);
      - bulgularını yazacağı dosya: `/tmp/dc/bulgular-<rol>.json` (`dogruluk`, `okur`, `tasarim`).

      Kendi araştırma notlarını, kaynak özetlerini ya da “taslak bence iyi” gibi bir kanaati verme; editörler kaynakları kendileri açmalı.
   3. Üç bulgu dosyasını oku; aynı sorunu söyleyen bulguları birleştir. Tüm kritik ve önemli bulguları düzelt: doğrulanamayan bilgiyi sil, gerekirse haberi çıkar ya da etiketle; çıkan haber ızgarayı bozuyorsa `size` değerlerini, calendar ve pattern ref'lerini güncelle. Küçük bulguları makulse düzelt. Katılmadığın bulguda kaynağı kendin açarak kontrol et.
   4. Tasarım bulgusu içerikten geliyorsa (çok uzun başlık, elle kırılmış örnek satırları) taslakta düzelt. Koddan geliyorsa düzeltme; kayda `oneri` olarak yaz.
   5. Editörleri ikinci kez çağırma. Tek istisna: manşet değiştiyse yalnızca yeni manşet için doğruluk editörüne kısa bir ikinci kontrol.
   6. Düzeltmelerden sonra `python3 tools/kontrol.py issues/<bugün>.json` hatasız geçmeli. `python3 build.py` ve `python3 tools/ekran.py <bugün> --out /tmp/dc/ekran` yeni bir sorun göstermemeli.
   7. **Bulgu kaydı.** Bütün bulguları `data/inceleme/<bugün>.json` dosyasına yaz (biçim aşağıda, “Bulgu kaydı”). `python3 tools/inceleme.py data/inceleme/<bugün>.json` HATA vermemeli. Bu kayıt kuralların haftalık olarak iyileştirilmesinin ham verisidir; kök nedeni dürüst ve somut yaz.
5. **Yayın.**
   1. `issues/<bugün>.json` son halindedir; `python3 tools/kontrol.py issues/<bugün>.json` hatasız geçmeli.
   2. Benchmark: `python3 tools/modeller.py --yas 7` çalıştır. Çıktıda `GÜNCELLE` varsa ya da bugünün sayısında yeni bir model sürümü haberi varsa `.claude/skills/modeller-guncelle/SKILL.md` adımlarını uygula. `HATA` çıkarsa `git checkout data/modeller.json` ile eski haline döndür; sayı yine yayımlanır.
   3. `python3 build.py` çalıştır. Hata verirse JSON'u düzelt ve tekrar çalıştır; `build.py`'yi değiştirme.
   4. `git status` ile yalnızca beklenen dosyaların değiştiğini doğrula: yeni `issues/<bugün>.json`, yeni `data/inceleme/<bugün>.json`, `issues/index.json`, `index.html`, `arsiv.html`, `feed.xml`, `sayi/` altındaki sayfalar, `arama/<ay>.json`; sayıda `corrections` varsa `hakkinda.html`; benchmark yenilendiyse `data/modeller.json` ve `benchmark.html`. Başka bir dosya değişmişse commit etme, nedenini araştır.
   5. Commit et; mesaj: `Sayı <number> · <dateLabel>` (ör. `Sayı 8 · Salı, 10 Kasım 2026`). Ardından `git push origin HEAD:main`. Push reddedilirse bir kez `git pull --rebase origin main`, `python3 build.py` ve tekrar push dene.
   6. Push yine başarısız olursa yayın yapılamamış demektir: PushNotification ile hemen bildir (hata mesajının özetiyle) ve hazırlanan JSON'u mesajda dosya olarak gönder.
6. **Bildirim.** `python3 tools/inceleme.py data/inceleme/<bugün>.json` editör özet satırını üretir. PushNotification ile kısa bir mesaj gönder: “The Daily Compiler · Sayı NNN hazır” + manşet başlığı + 2-3 öne çıkan başlık + editör özet satırı + benchmark güncellendiyse tek satır + `https://dailycompiler.com/sayi/<bugün>.html`. Kurallarda fark ettiğin bir sorun varsa tek cümleyle ekle. GitHub Pages yayını push'tan sonra birkaç dakika sürebilir.

## Bulgu kaydı

`data/inceleme/<bugün>.json`:

```json
{
  "tarih": "2026-11-19",
  "sayi": 17,
  "puan": {"icerik": 7.5, "dogruluk": 8, "dil": 7, "tasarim": 8},
  "gerekce": {"icerik": "…", "dogruluk": "…", "dil": "…", "tasarim": "…"},
  "dogrulanan": 18,
  "bulgular": [
    {
      "id": "b1",
      "kategori": "terim",
      "onem": "kucuk",
      "konum": "java-1 · <başlık> ya da JSON yolu",
      "sorun": "“dallarda” yazılmış",
      "kanit": "kurallar/TERIMLER.md: branch İngilizce kalır",
      "durum": "duzeltildi",
      "kok": "denetlenebilir",
      "kural": "TERIMLER.md yasak çeviriler tablosunda “dallarda” biçimi yok; kalıp genişletilmeli",
      "not": ""
    }
  ]
}
```

- `puan`, `gerekce`, `dogrulanan`: editörlerin dosyalarından olduğu gibi alınır. Puanlar taslağın düzeltilmeden önceki halini ölçer; yazarın kalitesini izlemek için. Tasarım editörü çalışmadıysa `puan.tasarim` `null` olur.
- Editör bulgularının alanları (`kategori`, `onem`, `konum`, `sorun`, `kanit`) aynen alınır; `ekran.py` ve `kontrol.py`'nin UYARI satırları da `teknik` ya da ilgili kategoride bulgu olarak eklenir.
- `durum`:
  - `duzeltildi`: taslakta düzelttin.
  - `oneri`: taslakta düzeltilemeyen sorun (kod, tasarım altyapısı, kural).
  - `birakildi`: küçük ve tartışmalı; gerekçesi `not` alanında.
  - `reddedildi`: kaynağı kendin açıp bulgunun yanlış olduğunu gördün; gerekçesi `not` alanında.
  - `duzeltme-listesinde`: önceki bir sayıdaki olgu hatası; bugünün sayısına `corrections` olarak eklendi.

  Kritik doğruluk ve kaynak bulguları yalnızca `duzeltildi` ya da `reddedildi` olabilir.
- `kok` (bulgunun neden ortaya çıktığı):
  - `yok`: kurallar doğru ve açık, o gün hata yapıldı.
  - `denetlenebilir`: `tools/kontrol.py` ya da `tools/ekran.py` bunu yakalayabilirdi.
  - `belirsiz`: ilgili kural var ama farklı yorumlanabiliyor.
  - `uygulanmadi`: kural açık ama uygulanmamış; yanlış adımda ya da gözden kaçacak bir yerde olabilir.
  - `eksik`: bu durumu kapsayan kural yok.
  - `kod`: sorun `build.py`, CSS ya da JavaScript'te.

  `yok` dışındaki her bulguda `kural` alanına hangi dosyanın hangi bölümü olduğunu ve neyin eksik ya da belirsiz olduğunu tek cümleyle yaz.
