# The Daily Compiler · Atölye

Atölye, haber değil uygulama bölümüdür. Her sayıda bir konu: yapay zekâyı ve agent'ları yazılım geliştirmede (ve araştırma ve analizde) verimli kullanmanın somut bir yolu. Okuyucu bölümü okuduktan sonra aynı gün bir şeyi farklı yapabilmelidir.

Bu dosya yazar ve editör için bağlayıcıdır; `KURALLAR.md`'deki kaynak ve dil kuralları bu bölüm için de geçerlidir.

## 1. Konu seçimi

1. **Haberle bağ önce gelir.** Günün haberlerinde okuyucunun hemen kullanabileceği bir özellik ya da yöntem varsa (yeni bir agent özelliği, yeni bir bağlam dosyası desteği, bir ekibin yayımladığı iş akışı), konu odur. O zaman `konu` alanı bankadaki en yakın konunun kimliği ya da `"haber"` olur; haber ise iç atıf verilir.
2. Yoksa **konu bankasından** seç (3. bölüm). `python3 tools/ozet.py` son 45 günde işlenen konuları ve kategori dağılımını gösterir. Son 45 günde işlenen konu tekrar seçilmez; son 7 sayıda en az işlenen kategoriden seçmeyi tercih et.
3. Haftada en az bir yazı kodlama dışı olur (araştırma ve analiz, ya da ekip süreçleri).
4. Konu dar ve somut olmalı: “Testlerde AI” değil, “Mevcut bir servise agent ile karakterizasyon testi yazdırmak”.

## 2. Kaynak

- **Her öneri bir kaynağa dayanır.** Atölye'de en sık yapılacak hata, modelin kendi kanaatini “en iyi uygulama” diye yazmasıdır. Yazıdaki her yöntem, adım ve uyarı en az bir kaynakta yazmalı; kaynağa atfet (“GitHub'ın Copilot belgeleri, talimatların kısa ve kendi başına anlaşılır cümleler olmasını öneriyor”).
- **Kaynak havuzu** (önce burada ara; başka kaynak da kullanılabilir, ama aynı ölçütle):
  - Araç üreticilerinin resmi belgeleri ve mühendislik yazıları: Anthropic (claude.com/blog, anthropic.com/engineering, docs.claude.com), OpenAI (platform.openai.com/docs, openai.com/index), GitHub (docs.github.com/copilot, github.blog), Google (ai.google.dev, developers.googleblog.com), JetBrains, Cursor, Sourcegraph, AWS, Microsoft (learn.microsoft.com).
  - Açık standartlar: agents.md, modelcontextprotocol.io.
  - Bağımsız yazarlar ve kurumlar: martinfowler.com (özellikle “Exploring Generative AI” dizisi), Thoughtworks Technology Radar, simonwillison.net, InfoQ, ACM Queue, IEEE Software.
  - Araştırma ve ölçüm: DORA raporları, METR, arXiv'deki deneysel çalışmalar (yöntemleri ve çekinceleriyle), büyük şirketlerin ölçüm içeren mühendislik blogları (Google, Meta, Uber, Shopify, Spotify, Netflix, Stripe).
  - Java ekosistemi: spring.io/blog, docs.spring.io, inside.java, foojay.io, JetBrains blogları.
- Forum, içerik toplayıcı ve SEO sitelerini birincil ya da güçlü bir kaynak varken kullanma.
- **Ölçüm dürüstlüğü.** Bir yöntemin işe yaradığına dair ölçüm varsa rakamı ve kimin ölçtüğünü yaz; yoksa “kanıtlanmış”, “kesin işe yarar” deme. Şirketin kendi ölçümü Şirket beyanı gibi atfedilir.
- **Tarih.** Araç davranışı hızla değişir. Bir araca özgü ayrıntıda kaynağın tarihine bak; 12 aydan eski bir belgeye dayanıyorsa güncel belgede hâlâ geçerli olduğunu doğrula.

## 3. Araç tarafsızlığı

- Yöntemi mümkünse araçtan bağımsız anlat; örnekleri farklı araçlara yay (Claude Code, Codex, GitHub Copilot, Cursor, Gemini CLI, JetBrains Junie vb.).
- Bir araca özgü bir özellik anlatılıyorsa, öteki yaygın araçlarda karşılığı varsa tek cümleyle an.
- Bu bir kota değildir. Okuyucu için faydası yüksek bir konu tek bir araca (Claude dahil) özgüyse o araçla yazılır; art arda aynı araçla ilgili önemli konular gelebilir. Ölçüt okuyucunun kazancıdır.
- Gazeteyi Claude yazdığı için Claude ile ilgili yazılarda övgü sıfatı kullanma ve sınırları da yaz; haberlerdeki eşit muamele ilkesi burada da geçerlidir.

## 4. Yapı ve dil

- **Başlık** yapılacak işi söyler: “Agent'lar için proje talimat dosyası: kısa, somut, katmanlı”. En fazla 80 karakter.
- **Giriş** (`intro`, 1-2 cümle): sorun ve okuyucunun kazancı.
- **Ne zaman** (`when`, 1-2 cümle): yöntemin işe yaradığı ve yaramadığı durum.
- **Adımlar** (`steps`, 3-6 madde): her biri uygulanabilir tek bir eylem; gerekiyorsa kısa açıklama. Her adım kaynağa dayanır.
- **Örnek** (`example`, isteğe bağlı ama beklenen): kopyalanıp uyarlanabilecek kısa bir blok (talimat dosyası, prompt, yapılandırma, komut, kod). En fazla 25 satır. Okuyucu kitlesine uygun olarak mümkünse Java/Spring/Maven bağlamında. Örnek uydurma bir projeye aitse “örnek” olduğu açıktır; gerçek bir proje adı ya da gerçekmiş gibi görünen sonuç rakamı yazma. Gizli bilgi (anahtar, parola, iç adres) yazma; çalıştırıldığında zarar verebilecek komut (silme, zorla push, üretim ortamına yazma) koyma.
- **Sık yapılan hata** (`pitfall`, 1-2 cümle): kaynakta geçen bir hata ya da sınır.
- **Kaynaklar**: 1-4 link; ilk link yöntemin birincil kaynağı.
- **Uzunluk:** intro, when, steps ve pitfall birlikte 250-550 kelime (örnek blok sayılmaz). Konu küçükse kısa tut; dolgu yazma.
- Dil: haberlerdeki gibi kısa cümle, emir kipiyle adımlar (“Dosyayı repo köküne koyun”). Okuyucuya “siz” diye hitap edilir.

## 5. Konu bankası

Kimlik `kategori-konu` biçimindedir; `atolye.konu` alanına yazılır. Bu liste ayda bir gözden geçirilir; tükenen kategoriye yeni konular eklenir.

### agent · Agentic geliştirme
- `agent-talimat-dosyasi`: AGENTS.md/CLAUDE.md gibi proje talimat dosyası: ne yazılır, ne yazılmaz
- `agent-talimat-katman`: Çok modüllü projede katmanlı talimat dosyaları (kök, modül, kişisel)
- `agent-gorev-tanimi`: Agent'a iyi görev tanımı: hedef, kapsam, kabul ölçütü, yasaklar
- `agent-once-plan`: Önce plan, sonra kod: agent'a planı yazdırıp onaylatmak
- `agent-kucuk-adim`: Büyük işi agent için küçük, doğrulanabilir adımlara bölmek
- `agent-test-dongusu`: Agent'ın kendi testini çalıştırıp düzelttiği döngü (testi önce yazdırmak)
- `agent-baglam-yonetimi`: Uzun oturumda bağlamı taze tutmak: temizleme, özetleme, yeni oturum
- `agent-alt-agent`: Alt agent'larla araştırma ve doğrulamayı ana işten ayırmak
- `agent-paralel`: Birden çok agent'ı paralel çalıştırmak: ayrı çalışma ağaçları (git worktree)
- `agent-izinler`: Agent izinleri: hangi komutlara onay gerekir, sandbox, ağ erişimi
- `agent-hooks`: Hook'larla zorunlu kontroller (biçimlendirme, lint, yasaklı dosya)
- `agent-ozel-komut`: Tekrarlanan işler için özel komutlar ve beceriler (skills)
- `agent-mcp`: MCP sunucusu bağlamak: ne zaman değer katar, güvenlik riski nedir
- `agent-kod-tabani-kesif`: Yabancı bir kod tabanını agent ile tanımak: soru listesi ve harita
- `agent-hata-ayiklama`: Agent ile hata ayıklama: yeniden üretme, hipotez, kanıt
- `agent-refactor`: Agent ile güvenli refactor: önce karakterizasyon testleri
- `agent-migrasyon`: Agent ile büyük ölçekli migrasyon (ör. Spring Boot sürüm geçişi, Jakarta)
- `agent-headless`: Agent'ı CI'da başsız çalıştırmak: sınırlar ve çıktı biçimi
- `agent-maliyet`: Agent maliyetini kontrol etmek: model seçimi, bağlam boyutu, önbellek
- `agent-model-secimi`: Hangi iş için hangi model ve akıl yürütme seviyesi
- `agent-ciktiyi-dogrulama`: Agent çıktısını doğrulamak: neye güvenilir, neye bakılmalı
- `agent-yarim-is`: Agent'ın yarım bıraktığı ya da “tamamladım” dediği işi yakalamak
- `agent-prompt-kaliplari`: Kodlama için işe yarayan prompt kalıpları (örnek, kısıt, çıktı biçimi)
- `agent-ekip-kurallari`: Ekipte agent kullanım kuralları: ne serbest, ne onaylı
- `agent-dokumantasyon`: Agent'a güncel kütüphane belgesi vermek (eski API uydurmasını önlemek)
- `agent-ekran-goruntusu`: Arayüz işinde agent'a görsel hedef ve ekran görüntüsüyle doğrulama
- `agent-bellek`: Agent belleği ve kalıcı notlar: ne saklanır, ne saklanmaz
- `agent-uzun-gorev`: Saatler süren görevler: ilerleme dosyası, ara kontrol noktaları

### sdlc · SDLC, test ve kod incelemesi
- `sdlc-karakterizasyon-testi`: Eski koda karakterizasyon testi yazdırmak
- `sdlc-test-verisi`: Gerçekçi test verisi ve fixture üretmek
- `sdlc-mutasyon-testi`: Mutasyon testiyle AI'ın yazdığı testlerin gücünü ölçmek (PIT)
- `sdlc-entegrasyon-testi`: Testcontainers ile entegrasyon testlerini agent'a yazdırmak
- `sdlc-kod-inceleme-ai`: AI kod incelemesi: neyi yakalar, neyi kaçırır, nasıl ayarlanır
- `sdlc-pr-aciklamasi`: PR açıklaması ve commit mesajını AI ile yazmak (ve sınırları)
- `sdlc-buyuk-pr`: AI'ın ürettiği büyük PR'ları incelenebilir parçalara bölmek
- `sdlc-gereksinim`: Gereksinimden kabul ölçütü ve test senaryosu çıkarmak
- `sdlc-spec-odakli`: Spesifikasyon odaklı geliştirme: önce spec, sonra agent
- `sdlc-flaky-test`: Kararsız (flaky) testleri AI ile teşhis etmek
- `sdlc-log-analizi`: Hata loglarını ve stack trace'leri AI ile çözümlemek
- `sdlc-performans`: Performans sorununu profil çıktısıyla AI'a analiz ettirmek
- `sdlc-teknik-borc`: Teknik borç envanteri çıkarmak ve önceliklendirmek
- `sdlc-dokumantasyon`: Koddan güncel dokümantasyon ve diyagram üretmek
- `sdlc-adr`: Mimari karar kayıtlarını (ADR) AI ile yazmak ve agent'a okutmak
- `sdlc-olay-sonrasi`: Olay sonrası inceleme (postmortem) taslağı: zaman çizelgesi ve kök neden
- `sdlc-onboarding`: Yeni ekip üyesinin kod tabanına alışmasını AI ile hızlandırmak
- `sdlc-ai-kod-kalitesi`: AI'ın ürettiği kodun kalite ve bakım riskleri (ölçümler)
- `sdlc-olcum`: AI kullanımının ekip verimine etkisini ölçmek (DORA, çevrim süresi)

### mimari · Mimari ve tasarım
- `mimari-alternatif`: Tasarım alternatiflerini AI ile karşılaştırmak (karar matrisi)
- `mimari-api-tasarimi`: API sözleşmesini (OpenAPI) önce yazıp agent'a uygulatmak
- `mimari-domain-modeli`: Domain modelini ve sınırlı bağlamları AI ile keşfetmek
- `mimari-diyagram`: Kod ve konuşmadan diyagram üretmek (Mermaid, C4)
- `mimari-ai-ozellik`: Ürüne AI özelliği eklemek: RAG, araç kullanımı, değerlendirme
- `mimari-llm-entegrasyon`: Java'dan LLM çağırmak: Spring AI ve LangChain4j ile temel desen
- `mimari-yapilandirilmis-cikti`: LLM'den yapılandırılmış çıktı (JSON şema, tip güvenliği)
- `mimari-eval`: LLM özelliği için değerlendirme (eval) seti kurmak
- `mimari-rag`: RAG'de parçalama, arama ve kaynak gösterme kararları
- `mimari-agent-mimarisi`: Kendi agent'ını kurarken iş akışı mı, agent mı: karar ölçütleri
- `mimari-modulerlik`: Kod tabanını agent'lar için daha anlaşılır yapmak (modül sınırları)
- `mimari-guvenilirlik`: LLM çağrılarında zaman aşımı, yeniden deneme ve yedek model

### cicd · CI/CD, güvenlik ve işletim
- `cicd-ai-pipeline`: CI'da AI adımı: inceleme, test önerisi, sürüm notu
- `cicd-surum-notu`: Commit geçmişinden sürüm notu üretmek
- `cicd-bagimlilik`: Bağımlılık güncellemelerini agent ile yönetmek (Dependabot/Renovate ile)
- `cicd-guvenlik-acigi`: Güvenlik açığı uyarılarını AI ile önceliklendirmek ve yamalamak
- `cicd-prompt-injection`: Agent'larda prompt injection riski: repo, issue ve web içeriği
- `cicd-gizli-bilgi`: Agent'ların gizli bilgiye erişimini sınırlamak
- `cicd-tedarik-zinciri`: AI'ın önerdiği paketler: uydurma paket adları (slopsquatting)
- `cicd-iac`: Altyapı kodunu (Terraform, Helm) AI ile yazmak ve doğrulamak
- `cicd-gozlemlenebilirlik`: Alarm ve dashboard tanımlarını AI ile üretmek
- `cicd-olay-mudahale`: Olay anında AI: log, metrik ve runbook ile teşhis
- `cicd-maliyet-izleme`: Ekipte AI kullanım maliyetini izlemek ve bütçelemek
- `cicd-veri-gizliligi`: Şirket kodunu AI araçlarına verirken veri ve lisans kuralları
- `cicd-lisans`: AI'ın ürettiği kodda lisans ve telif riski

### ekip · Ekip ve süreç
- `ekip-kural-belgesi`: Ekip için AI kullanım politikası: kısa ve uygulanabilir
- `ekip-paylasim`: Ekipte prompt, talimat ve becerileri paylaşmak (repoda tutmak)
- `ekip-egitim`: Ekibe agentic geliştirmeyi öğretmek: eşli çalışma ve örnek görevler
- `ekip-toplanti`: Toplantı notu ve karar kaydını AI ile çıkarmak
- `ekip-gorev-bolme`: Epik ve hikâyeleri AI ile bölmek ve tahminlemek
- `ekip-yazisma`: Teknik yazışma: RFC, tasarım belgesi ve geri bildirim

### arastirma · Araştırma ve analiz
- `arastirma-derin-arastirma`: Derin araştırma araçlarını doğru kullanmak: soru, kapsam, doğrulama
- `arastirma-kaynak-dogrulama`: AI çıktısındaki iddiaları ve kaynakları doğrulamak
- `arastirma-teknoloji-secimi`: Teknoloji seçimi için karşılaştırma raporu hazırlamak
- `arastirma-makale-okuma`: Akademik makaleyi AI ile okumak: yöntem, sonuç, sınırlar
- `arastirma-veri-analizi`: AI ile veri analizi: hesabı kodda yaptırmak, sonucu doğrulamak
- `arastirma-sql`: Doğal dilden SQL: şema vermek ve sonucu doğrulamak
- `arastirma-log-veri`: Büyük log ve CSV dosyalarını AI ile özetlemek
- `arastirma-rakip-analizi`: Ürün ve rakip analizi: kaynaklı tablo çıkarmak
- `arastirma-ozet`: Uzun belge ve toplantı kaydını kayıpsız özetlemek
- `arastirma-sunum`: Analiz sonucunu karar vericiye sunmak: grafik ve tek sayfa özet
- `arastirma-halusinasyon`: Halüsinasyonu azaltmak: kaynak isteme, alıntı, belirsizlik
