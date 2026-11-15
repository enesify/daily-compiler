# The Daily Compiler · günlük sayı görevi

Bu dosya her sabah çalışan zamanlanmış görevin adımlarıdır. Görev bu dosyayı okuyup baştan sona uygular; zamanlanmış görevin kendi metni yalnızca buraya yönlendirir. Süreç değiştiğinde bu dosya, kurallarla aynı commit'te güncellenir.

Gazete https://dailycompiler.com adresinde, GitHub Pages ile `enesify/daily-compiler` reposunun `main` dalından yayımlanır.

## Sınırlar

- Yazım ve seçim kurallarının tamamı `kurallar/KURALLAR.md` dosyasındadır; yazmaya başlamadan önce baştan sona oku ve uygula. Alan adları ve biçim için örnek `kurallar/ornek.json`.
- Her sayının içeriği `issues/YYYY-MM-DD.json` dosyasıdır (tek doğruluk kaynağı); sayfalar `python3 build.py` ile bu dosyalardan üretilir.
- Yalnızca yeni `issues/<bugün>.json` dosyasını eklersin, gerekiyorsa `data/modeller.json` dosyasını yenilersin ve `build.py`'yi çalıştırırsın. `build.py`, `assets/`, `kurallar/`, `tools/`, `CLAUDE.md` ve eski sayılara DOKUNMA. Bir kural yanlış, eksik ya da çelişkili görünüyorsa dosyayı değiştirme; en makul yorumu uygula ve son bildirimde belirt.
- Eski sayılar asla silinmez ve değiştirilmez. Önceki bir sayıda olgu hatası fark edersen bugünün sayısına `corrections` olarak ekle.
- Değişiklikleri doğrudan `main` dalına push et; `claude/` ile başlayan dal ya da pull request açma.
- Bu oturumda sen YAZARSIN; 4. adımda ayrı bir EDİTÖR agent taslağı denetler.

## Verimli çalışma

Bunlar sonucu değiştirmez, yalnızca süreyi ve token kullanımını azaltır:

- **Paralel çağrı.** Birbirine bağlı olmayan aramaları (WebSearch) ve sayfa okumalarını (WebFetch) tek tek değil, aynı anda gönder; örneğin bir bölümün bütün aramalarını tek seferde, bir aramanın sonuçlarından okunacak sayfaları tek seferde.
- **Araştırma notu.** Okuduğun her kaynaktan kullanacağın olguları (rakam, tarih, isim, kısa alıntı) ve URL'yi `/tmp/dc/notlar.md` dosyasına kısaca yaz. Taslağı yazarken ve editör bulgularını düzeltirken önce bu notlara bak; aynı sayfayı yalnızca notta olmayan bir ayrıntı gerekiyorsa yeniden aç. Bu dosya editöre verilmez.
- **Taslağı yeniden yazma.** Taslak bir kez yazıldıktan sonra denetim aracının ve editörün bulgularını Edit aracıyla yalnızca ilgili alanı değiştirerek düzelt; dosyayı baştan yazma.
- Önceki sayıların tam metnini okuma; özet çıktısı yeterlidir. Yalnızca bir iç atıf ya da takip haberi için gerekiyorsa ilgili haberi aç.

## Adımlar

1. **Hazırlık.** Repo kökünde olduğunu ve `git status`'un temiz olduğunu doğrula; `git pull --ff-only origin main` ile güncelle. `python3 tools/ozet.py --out /tmp/dc` çalıştır. Çıktı bugünün tarihini (Europe/Istanbul) ve dateLabel'ı, zaman penceresini, sıradaki number'ı, önceki manşeti, son 7 günün repolarını, takvim adaylarını, son sayıların Pratik çıkarım maddelerini, son 3 sayının başlıklarını (iç atıf adresleriyle) ve olası açık uçları verir; editör için `/tmp/dc/previous_headlines.txt` dosyasını yazar. Çıktı bugünün sayısının zaten var olduğunu söylüyorsa yeniden yazma, dur ve bildir.
2. **Kurallar.** `kurallar/KURALLAR.md` ve `kurallar/ornek.json` dosyalarını oku.
3. **Araştırma ve yazım.** Kurallara göre araştır ve taslağı `/tmp/dc/draft.json` olarak yaz. `python3 tools/kontrol.py /tmp/dc/draft.json` çalıştır: HATA satırlarının hepsini düzelt; UYARI satırlarını gözden geçir ve geçerli bir gerekçen yoksa düzelt. Hata kalmayana kadar tekrarla.
4. **Editör incelemesi (tek tur).** Agent aracıyla (subagent_type "general-purpose") ayrı bir EDİTÖR agent başlat. Ona yalnızca şunları ver: görevinin `kurallar/EDITOR.md`, kuralların `kurallar/KURALLAR.md` dosyasında olduğu (tam yollarıyla), taslağın `/tmp/dc/draft.json`, önceki başlıkların `/tmp/dc/previous_headlines.txt`, benchmark verisinin `data/modeller.json` olduğu (tam yoluyla), bulgularını `/tmp/dc/bulgular.json` dosyasına yazacağı ve bugünün tarihi. Kendi araştırma notlarını, kaynak özetlerini ya da “taslak bence iyi” gibi bir kanaati verme; editör kaynakları kendisi açmalı.
   - `/tmp/dc/bulgular.json` dosyasını oku. Tüm KRİTİK ve ÖNEMLİ bulguları düzelt (doğrulanamayan bilgiyi sil; gerekirse haberi çıkar ya da etiketle; çıkan haber ızgarayı bozuyorsa `size` değerlerini, calendar ve pattern ref'lerini güncelle). KÜÇÜK bulguları makulse düzelt. Katılmadığın bulguda kaynağı kendin açarak kontrol et.
   - Her bulgunun `karar` alanını doldur: `"düzeltildi"`, `"reddedildi: <kısa gerekçe>"` ya da `"küçük, bırakıldı"`.
   - Editörü ikinci kez çağırma. Tek istisna: manşet değiştiyse yalnızca yeni manşet için kısa bir ikinci kontrol.
5. **Yayın.**
   1. Son hali `issues/<bugün>.json` olarak yaz. `python3 tools/kontrol.py issues/<bugün>.json` hatasız geçmeli.
   2. Benchmark: `python3 tools/modeller.py --yas 7` çalıştır. Çıktıda `GÜNCELLE` varsa ya da bugünün sayısında yeni bir model sürümü haberi varsa `.claude/skills/modeller-guncelle/SKILL.md` adımlarını uygula. `HATA` çıkarsa `git checkout data/modeller.json` ile eski haline döndür; sayı yine yayımlanır.
   3. `python3 build.py` çalıştır. Hata verirse JSON'u düzelt ve tekrar çalıştır; `build.py`'yi değiştirme.
   4. `git status` ile yalnızca beklenen dosyaların değiştiğini doğrula: yeni `issues/<bugün>.json`, `issues/index.json`, `index.html`, `arsiv.html`, `feed.xml`, `sayi/` altındaki sayfalar; sayıda `corrections` varsa `hakkinda.html`; benchmark yenilendiyse `data/modeller.json` ve `benchmark.html`. Başka bir dosya değişmişse commit etme, nedenini araştır.
   5. Commit et; mesaj: `Sayı <number> · <dateLabel>` (ör. `Sayı 8 · Salı, 10 Kasım 2026`). Ardından `git push origin HEAD:main`. Push reddedilirse bir kez `git pull --rebase origin main`, `python3 build.py` ve tekrar push dene.
   6. Push yine başarısız olursa yayın yapılamamış demektir: PushNotification ile hemen bildir (hata mesajının özetiyle) ve hazırlanan JSON'u mesajda dosya olarak gönder.
6. **Bildirim.** `python3 tools/bulgular.py /tmp/dc/bulgular.json` editör özet satırını üretir. PushNotification ile kısa bir mesaj gönder: “The Daily Compiler · Sayı NNN hazır” + manşet başlığı + 2-3 öne çıkan başlık + editör özet satırı + benchmark güncellendiyse tek satır + `https://dailycompiler.com/sayi/<bugün>.html`. Kurallarda fark ettiğin bir sorun varsa tek cümleyle ekle. GitHub Pages yayını push'tan sonra birkaç dakika sürebilir.
