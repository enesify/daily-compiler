# The Daily Compiler · günlük inceleme görevi

Bu dosya, sabah yayımlanan sayıyı aynı gün inceleyen zamanlanmış görevin adımlarıdır (09.47, Europe/Istanbul). Görev bu dosyayı okuyup baştan sona uygular; zamanlanmış görevin kendi metni yalnızca buraya yönlendirir.

Görevin iki işi var:

1. **Onarım:** Günün sayısındaki hataları bulur ve düzeltilebilenleri hemen düzeltip yayımlar.
2. **Kayıt:** Her bulguyu, kök nedeniyle birlikte `data/inceleme/<bugün>.json` dosyasına yazar. Kurallar bu kayıtlara bakılarak haftalık olarak iyileştirilir; bu görev kurallara dokunmaz.

## Sınırlar

- Değiştirebileceğin dosyalar:
  - `issues/<bugün>.json`
  - yeni `data/inceleme/<bugün>.json`
  - `build.py`'nin ürettiği dosyalar
- Şunlara DOKUNMA: `kurallar/`, `tools/`, `build.py`, `assets/`, `CLAUDE.md`, `data/modeller.json` ve önceki günlerin sayıları. Bir kural ya da kod sorununu düzeltmek senin işin değil; bulguya yaz.
- Sayıyı yeniden yazma. Düzeltmeler en küçük değişiklikle yapılır (Edit aracıyla, yalnızca ilgili alan). Manşet seçimi, haber seçimi ve bölüm düzeni değişmez. Tek istisna: yanlış olduğu doğrulanan ve düzeltilemeyen bir haber çıkarılabilir. Çıkarırsan `size` değerlerini ve `calendar`/`pattern` ref'lerini güncelle.
- Bugünün sayısı yoksa (`issues/<bugün>.json` bulunamazsa) hiçbir şey yazma; PushNotification ile “İnceleme: bugünün sayısı yayımlanmamış” bildir ve dur.
- `data/inceleme/<bugün>.json` zaten varsa inceleme yapılmış demektir; dur.
- Doğrudan `main` dalına push et; dal ya da pull request açma.

## Adımlar

1. **Hazırlık.**
   - `git pull --ff-only origin main`.
   - Bugünün tarihini al: `TZ=Europe/Istanbul date +%F`.
   - `kurallar/KURALLAR.md`, `kurallar/TERIMLER.md` ve `kurallar/ATOLYE.md` dosyalarını oku, sonra `issues/<bugün>.json` dosyasını oku.
   - `python3 tools/kontrol.py issues/<bugün>.json` çalıştır; çıkan UYARI satırları da bulgudur.
   - `python3 build.py` ve ardından `python3 tools/ekran.py <bugün> --out /tmp/inc/ekran` çalıştır. Betiğin yazdığı taşma, JavaScript hatası ve kırık bağlantı satırları bulgudur.

2. **Üç bağımsız inceleme (paralel).** Agent aracıyla (subagent_type "general-purpose") üç agent'ı aynı anda başlat. Her birine yalnızca şunları ver:
   - görevi (aşağıda);
   - ilgili dosyaların tam yolları;
   - bulgularını yazacağı dosya: `/tmp/inc/<rol>.json`;
   - bu dosyadaki “Kayıt” bölümünün biçimi; agent `durum` alanını yazmaz.

   Sabah görevinin editör bulgularını ya da kendi kanaatini verme.

   - **Doğruluk.** Kaynakları WebFetch ile kendisi açar. Kapsam:
     - manşetin tamamı;
     - bütün `big` haberler, Güvenlik bölümü ve Atölye;
     - `stat`, grafik ve Takvim'deki her rakam ve tarih;
     - bunlara ek en az 6 haber.

     Her rakam, tarih, isim ve nitelendirme kaynakta açıkça yazıyor mu? Kaynağın çekincesi habere yansımış mı? Linkler açılıyor ve asıl kaynağa mı gidiyor? İç atıflar doğru habere mi gidiyor? Bağımsız sayfa okumalarını paralel yap. Puanı: `dogruluk`.
   - **Editoryal ve dil.** `kurallar/KURALLAR.md`, `kurallar/TERIMLER.md`, `kurallar/ATOLYE.md` ve sayının JSON'u. Bakacağı yerler:
     - okuyucu için seçim ve önem sırası (KURALLAR §1);
     - eksik bilgi ve “ne yapmalıyım” adımı;
     - etiketler;
     - haber cümlesi gibi yazılmış yorum;
     - tekrar ve dolgu;
     - Pratik çıkarım, why ve pattern kalitesi;
     - Atölye kuralları;
     - Türkçe: çeviri kokan cümle, sözlüğe aykırı terim, 25 kelimeyi aşan cümle, yanlış ek.

     Puanları: `icerik` (seçim, değer, editoryal kalite) ve `dil`.
   - **Tasarım.** `/tmp/inc/ekran/` altındaki bütün görüntüler (telefon, tablet, masaüstü) ve `tools/ekran.py` çıktısı. Görüntülere tek tek bakar; şunları arar:
     - hizalama ve boşluk dengesi;
     - erken kırılan ya da taşan satır;
     - emoji gibi çizilen karakter;
     - üst üste binme;
     - okunurluk ve kontrast;
     - aynı bileşenin farklı yerlerde farklı görünmesi;
     - telefonda dokunma hedefi.

     İçerikten kaynaklanan sorunu (çok uzun başlık, çok uzun repo adı) koddan kaynaklanandan ayırır. Puanı: `tasarim`.

   Her agent puanını 0-10 arası verir ve tek cümlelik gerekçe yazar (`gerekce`). Bulgu yoksa boş liste döner; sırf liste dolsun diye bulgu üretmez.

3. **Değerlendir ve düzelt.**
   - Bulguları birleştir ve aynı olanları tek bulguya indir.
   - Kritik ve önemli bulgularda emin değilsen kaynağı kendin aç. Yanlış çıkan bulguyu kayda yazma.
   - Her bulguya `durum` ver:
     - **`duzeltildi`:** sayıda düzelttin. Bunlar şunlardır:
       - terim ve dil;
       - yazım;
       - kırık link (doğru adresi kaynaktan doğrulayarak);
       - eksik İddia ya da Şirket beyanı etiketi;
       - kaynağın verdiği bir kontrol adımının eklenmesi;
       - belirsiz cümle;
       - kaynakla çelişen rakam: bunda düzeltme okura da bildirilir, aşağıya bak.
     - **`duzeltme-listesinde`:** okurun ilk yayında yanlış bir olgu okuduğu durum. Metni düzelt ve sayının `corrections` alanına aynı gün için bir kayıt ekle: `{"date": "<bugün>", "ref": "<çapa>", "text": "İlk yayımlanan metinde … yazıyordu; doğrusu …"}`. Olgu hatasını sessizce düzeltme. Üslup düzeltmesi bu listeye girmez.
     - **`oneri`:** sayıda düzeltilemeyen ya da düzeltilmemesi gereken sorun. Örnekler: kod veya tasarım, seçim hatası (haberi değiştirmek yasak), kural sorunu.
     - **`birakildi`:** küçük ve tartışmalı; gerekçesini `not` alanına yaz.
   - Kritik doğruluk ve kaynak bulguları `oneri` ya da `birakildi` olarak bırakılamaz.

4. **Kök neden.** Her bulgu için `kok` alanını doldur. Bu alan haftalık kural iyileştirmesinin ham verisidir; dürüst ve somut yaz:
   - `yok`: kurallar doğru ve açık, yazar o gün hata yaptı. Tek seferlik hataların çoğu buradadır.
   - `denetlenebilir`: `tools/kontrol.py` ya da `tools/ekran.py` bunu yakalayabilirdi. Örnek: yasak çeviri, taşan öğe, eksik alan.
   - `belirsiz`: ilgili kural var ama farklı yorumlanabiliyor.
   - `uygulanmadi`: kural açık ama sabah görevi uygulamamış. Kural yanlış adımda ya da gözden kaçacak bir yerde olabilir.
   - `eksik`: bu durumu kapsayan kural yok.
   - `kod`: sorun `build.py`, CSS ya da JavaScript'te.

   `yok` dışındaki her bulguda `kural` alanına hangi dosyanın hangi bölümü olduğunu ve neyin eksik ya da belirsiz olduğunu tek cümleyle yaz.

5. **Yayın.**
   1. Düzeltme yaptıysan:
      - `python3 tools/kontrol.py issues/<bugün>.json` hatasız geçmeli.
      - `python3 build.py` çalıştır.
      - `python3 tools/ekran.py <bugün>` yeni bir sorun göstermemeli.
   2. Kaydı `data/inceleme/<bugün>.json` olarak yaz. `python3 tools/inceleme.py data/inceleme/<bugün>.json` HATA vermemeli.
   3. `git status` ile yalnızca beklenen dosyaların değiştiğini doğrula:
      - kayıt dosyası;
      - düzeltme yaptıysan `issues/<bugün>.json`, `index.html`, `sayi/` altındaki sayfalar, `arama/<ay>.json`, `feed.xml`, `issues/index.json`;
      - `corrections` eklediysen `hakkinda.html`.
   4. Commit et. Mesaj: `İnceleme · Sayı <number> · <dateLabel>`. Ardından `git push origin HEAD:main`. Push reddedilirse bir kez `git pull --rebase origin main`, `python3 build.py` ve tekrar push dene.

6. **Bildirim.** PushNotification ile tek mesaj gönder:
   - `python3 tools/inceleme.py data/inceleme/<bugün>.json` çıktısındaki satır;
   - en önemli 2-3 düzeltme, kısa;
   - kritik bir bulgu varsa onun tek cümlelik özeti.

   Bulgu yoksa yalnızca puan satırı yeter.

## Kayıt

`data/inceleme/<bugün>.json`:

```json
{
  "tarih": "2026-11-18",
  "sayi": 16,
  "puan": {"icerik": 7.5, "dogruluk": 8, "dil": 7, "tasarim": 8},
  "gerekce": {"icerik": "…", "dogruluk": "…", "dil": "…", "tasarim": "…"},
  "dogrulanan": 14,
  "bulgular": [
    {
      "id": "b1",
      "kategori": "terim",
      "onem": "kucuk",
      "konum": "sections[3].articles[0].paragraphs[0]",
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

Alanlar:

- `kategori`: `dogruluk`, `kaynak`, `eksik-bilgi`, `secim`, `dil`, `terim`, `editoryal`, `atolye`, `tasarim` ya da `teknik` (build, link, araç).
- `onem`:
  - `kritik`: okura yanlış ya da kaynaksız bilgi.
  - `onemli`: etiket, eksik adım, seçim, belirgin tasarım bozukluğu.
  - `kucuk`: dil ve biçim.
- `konum`: JSON yolu ya da ekran ve bölüm (`telefon · sec-atolye`).
- `kanit`: kaynakta ne yazdığı ve URL'si; ya da görüntü dosyasının adı.
- `puan`: 0-10. Ölçek bütün günlerde aynıdır: 9, okurun hiçbir düzeltme istemeyeceği bir sayıdır.
