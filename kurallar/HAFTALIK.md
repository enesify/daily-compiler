# Haftalık iyileştirme görevi

Haftada bir çalışır. Amacı günlük sayıyı hazırlayan görevin (`kurallar/GOREV.md`) ve editörlerinin kaçırdığını bulmak, tekrar eden hataların kökünü kurallarda ve kodda kapatmak. Günlük sayıların içeriğine dokunmaz.

## Değiştirilmeyecek kararlar

Bunlar yayıncının verdiği kararlardır; bulgular aksini gösterse bile değiştirilmez, gerekiyorsa raporda öneri olarak yazılır:

- Manşet yapay zekâ ya da yazılım geliştirme haberidir; güvenlik manşete zorlanmaz.
- Bir şirkete günlük haber sınırı yoktur. “Günün örüntüsü” bölümü yoktur.
- Okur kitlesi çeşitlidir; seçim tek bir teknoloji yığınına göre daraltılmaz. Java & Spring bölümü her sayıda kalır.
- Puanlama ve ölçek tartışması park edildi; puan ölçeği değiştirilmez.
- “zekâ” şapkalı yazılır. Grafiklerde yorum, kalabalık ve eksik değer açıklaması yoktur.
- `kurallar/TASARIM.md` ilkeleri.

## Adımlar

1. **Hazırlık.** `git pull --ff-only origin main`; `git status` temiz olmalı. Çalışma klasörü `/tmp/hf`.
2. **Veri.** Şunları çalıştır ve çıktıları sakla:
   - `python3 tools/inceleme.py --ozet 14` (tekrar eden kategori ve kök nedenler);
   - `python3 tools/inceleme.py --acik` (açık kod bulguları);
   - `python3 tools/inceleme.py --kacan 14` (günlük editörlerin kaçırdıkları).
3. **Site geneli inceleme.** Agent aracıyla (subagent_type "general-purpose") iki inceleyiciyi aynı anda başlat:
   - **Tasarım koordinatörü:** `kurallar/TASARIM.md` ilkeleriyle siteyi baştan sona gezer: `index.html`, son üç sayı, `arsiv.html`, `benchmark.html`, `hakkinda.html`, `404.html`. Dört ekranda (390, 844 yatay, 820, 1440 px), açık ve karanlık temada bakar; yerel sunucu `python3 -m http.server` ve Playwright ile. Tek sayıda görülemeyen sorunları arar: bileşenler arası tutarsızlık, eskimiş metin, gözden kaçan bağlantı, dolgu, renge dayanan ayrım.
   - **Dil editörü:** Son yedi sayının bütün metnini `kurallar/TERIMLER.md` ölçütüyle tarar: çevrilmiş İngilizce terimler, çevrilmiş şirket, ürün ya da özellik adları, sayılar arası terim tutarsızlığı.

   İkisi de bulgularını `kurallar/EDITOR.md` “Bulgu biçimi”nde `/tmp/hf/bulgular-<rol>.json` dosyasına yazar; dosya değiştirmez.
4. **Kurallar.** Tekrar eden kök nedenler (en az üç sayıda) ve `kacan.json` kayıtları için ilgili kural dosyasında en küçük değişikliği yap:
   - Her değişikliğin kanıtı bir bulgu ya da kaçan kayıt olmalı.
   - Kural dosyaları büyümesin: eklediğin kadar sadeleştir, `kurallar/KURALLAR.md` kelime sayısını önce ve sonra raporla.
   - Yeni bir yasak çeviri `kurallar/TERIMLER.md` tablosuna eklenir.
5. **Kod.** Açık kod bulgularını ve site geneli bulgulardan küçük ve geri alınabilir olanları düzelt (`build.py`, `assets/`, `tools/`).
   - Görünümü belirgin biçimde değiştiren tasarım kararlarını uygulama; raporda öneri olarak yaz. Bunlar yayıncının onayıyla yapılır.
   - Düzeltme sonrası şunlar temiz olmalı:
     - `python3 build.py` (Python 3.11 ile de);
     - son üç sayı için `python3 tools/ekran.py <tarih>`;
     - son üç sayı için `python3 tools/kontrol.py issues/<tarih>.json`.
   - Kapatılan bulguya `"kapandi": "<tarih> · <kısa not>"` ekle.
   - Günlük editörlerin kaçırdığı her sorunu `data/inceleme/kacan.json`'a `bulan: "haftalik"` ve kök nedeniyle kaydet.
6. **Rapor.** `data/inceleme/haftalik/<tarih>.md` dosyasına yaz:
   - ne değişti (kural ve kod, dosya dosya);
   - onay bekleyen öneriler;
   - kaçan sorunların neden dağılımı ve geçen haftaya göre değişimi.
7. **Yayın.** Değişiklikleri tek commit'te gönder: mesaj `Haftalık iyileştirme · <tarih>`. Commit trailer'ları `CLAUDE.md`'deki düzene uyar. Ardından `main`'e push et.

## Sınırlar

- `issues/*.json` içeriğine, zamanlanmış görevlere ve `CHANGELOG.md` etiketlerine dokunma.
- Dosya silme; bir kuralı kaldırman gerekiyorsa gerekçesini rapora yaz.
- Bir adım başarısız olursa geri al ve raporda belirt; yarım değişiklik push edilmez.
