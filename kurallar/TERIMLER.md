# Terim sözlüğü

Okuyucu Türk yazılımcı. Ölçüt, terimin sözlük karşılığı değil, bir yazılım ekibinin toplantıda, PR yorumunda ya da Slack'te kullandığı kelimedir. Bir kavram sayı boyunca tek terimle yazılır. Sözlükte olmayan bir terimde de aynı ölçüt geçerlidir: Türkçesi yerleşik değilse İngilizce kalır, karşılık uydurulmaz.

Türkçe ek İngilizce terime kesme işaretiyle gelir: secret'lar, branch'te, endpoint'i, event adları.

## İngilizce kalır

secret, token, runtime, event, branch, merge, pull request, commit, workflow, pipeline, endpoint, backend, frontend, control plane, data plane, framework, adapter, plugin, extension (ürün adı olarak: Copilot Extensions, VS Code extension), hook, skill, harness, sandbox, breaking change, deprecated, release candidate, heap dump, thread dump, allocation, garbage collector (GC), transcript (agent ya da sohbet dökümü), log, loglama, trace, rollout, checkpoint, alignment, fine-tuning, inference, context window, prompt, benchmark, trust store, keystore, container, cluster (altyapıda), load balancer, rate limit, feature flag, stealth (şirket için), redaksiyon (redaction).

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
