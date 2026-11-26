# Terim sözlüğü

Okuyucu Türk yazılımcı. Ölçüt, terimin sözlük karşılığı değil, bir yazılım ekibinin toplantıda, PR yorumunda ya da Slack'te kullandığı kelimedir. Bir kavram sayı boyunca tek terimle yazılır. Sözlükte olmayan bir terimde de aynı ölçüt geçerlidir: Türkçesi yerleşik değilse İngilizce kalır, karşılık uydurulmaz.

Türkçe ek İngilizce terime kesme işaretiyle gelir: secret'lar, branch'te, endpoint'i, event adları.

Şirket, ürün, özellik, plan, rol ve ayar adları kaynaktaki gibi yazılır, çevrilmez: 1Password'de Vault, GitHub'da Organization ve Member, Cloudflare'de Search for Agents. Gerekirse ilk geçtiği yerde parantez içinde kısaca açıklanır.

## İngilizce kalır

secret, token, runtime, event, branch, merge, pull request, commit, workflow, pipeline, endpoint, backend, frontend, control plane, data plane, framework, adapter, plugin, extension (ürün adı olarak: Copilot Extensions, VS Code extension), hook, skill, harness, sandbox, breaking change, deprecated, release candidate, heap dump, thread dump, allocation, garbage collector (GC), transcript (agent ya da sohbet dökümü), log, loglama, trace, rollout, checkpoint, alignment, speech-to-speech, read-your-writes, fine-tuning, inference, context window, prompt, benchmark, trust store, keystore, container, cluster (altyapıda), load balancer, rate limit, feature flag, stealth (şirket için), redaksiyon (redaction), handshake, header (HTTP ve protokol başlığı), script, stateless, stateful, full precision, judge (LLM judge, judge model), CTF (capture the flag), distillation, chunking (chunk'lara ayırmak), embedding, vault (parola yöneticisinde), sampling, warm-up, recursive self-improvement, medyan, reasoning (reasoning seviyesi, reasoning metni), pretraining, registry, code golf.

## Türkçesi yerleşik, Türkçe yazılır

açık (vulnerability), yama, istismar, aktif istismar, uzaktan kod çalıştırma, kimlik doğrulama, yetki, arka kapı, tedarik zinciri, bellek sızıntısı, bellek (agent belleği dahil), önbellek, bağımlılık, sürüm, güncelleme, yükseltme, ortam değişkeni, alt sorgu, sorgu, sunucu, istemci, dosya, dizin, depolama, veri merkezi, yapılandırma, kök neden analizi, sınıflandırıcı, değerlendirme, parametre, ağırlıklar (model), eğitim (model), bağlam, araç, oturum, izin, kural.

## Yasak çeviriler

Sol sütundaki kalıp `tools/kontrol.py` tarafından uyarı olarak yakalanır. Bağlam gerçekten başka bir anlam taşıyorsa (“o anı” gibi) uyarı yok sayılabilir.

| Kalıp | Yerine |
|---|---|
| `\bsır(lar|rı|ları|ların|rını|ra|lara)?\b` | secret |
| `\bçalışma zamanı(nı|nın|na|nda)?\b` | runtime |
| `\bolay ad(ı|ları)\b` | event adı |
| `\bdal(da|dan|ı|ın|lar|larda|lara|ları|ında)\b` | branch |
| `\bbirleştirme(si|leri|ler)\b` | merge (pull request için) |
| `\biş akış(ı|ları|larının|larını|larında)\b` | workflow |
| `\buç nokta(sı|lar|ları|sının)?\b` | endpoint |
| `\barka uç(u|lar)?\b` | backend |
| `\bkontrol düzlem(i|ini)\b` | control plane |
| `\bçatı(sı|lar)?\b` | framework |
| `\buyarlayıcı(sı|lar)?\b` | adapter |
| `\bkırıcı değişiklik(ler)?\b` | breaking change |
| `\bkullanımdan düşürül\w*` | deprecated (deprecate edilen) |
| `\b(heap|thread) döküm\w*` | heap dump, thread dump |
| `\bayırma(sı|lar)?\b` | allocation |
| `\bkayıt (tutma|kodu|düzeni)\b` | loglama, log kodu |
| `\bhizalama\w*` | alignment |
| `\bkarart\w*` | redaksiyon (redaction) |
| `\banı(lar|ları|ların|ya|yı|sı|nın)?\b` | bellek kaydı (agent belleğinde) |
| `\bemekli\w*` | arşive kaldırılan (Apache Attic), desteği sona eren |
| `\bgizlilikten çık\w*` | stealth moddan çıkan |
| `\bistem(ler|i|leri)?\b` | prompt |
| `\bince ayar\w*` | fine-tuning |
| `\bçıkarım (maliyet|hız|sunucu)\w*` | inference maliyeti, hızı, sunucusu |
| `\bel sıkışma\w*` | handshake |
| `\bbetik\w*|\bbetiğ\w*` | script |
| `\bdurumsuz\b` | stateless |
| `\btam hassasiyet\w*` | full precision |
| `\bhakem(i|den|lendi|le)?\b|\bhakem model\w*` | judge, judge model |
| `\bbayrak yakala\w*` | CTF (capture the flag) |
| `\bdamıtma\w*` | distillation |
| `\bparçalama hatt\w*|\bparçalayıp\b` | chunking, chunk'lara ayırıp |
| `\bortanca\w*` | medyan |
| `\bısınma koşu\w*` | warm-up koşusu |
| `\bözyinelemeli kendini geliştir\w*` | recursive self-improvement |
| `\bakıl yürüt\w*` | reasoning |
| `\bön eğitim\w*` | pretraining |
| `\bbeceri(ler|leri|si)?\b` | skill |
| `\bkayıt defter\w*` | registry |
| `\beklenti(si|ye|ler|leri|nin)?\b` | plugin ya da extension |
| `\bkod golf\w*` | code golf |
