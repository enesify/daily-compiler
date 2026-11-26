# Bulgu kayıtları

Sabah görevinde taslağı yayından önce inceleyen üç editörün bulguları ve yazarın kararları (`YYYY-MM-DD.json`). Biçim ve alanlar: `kurallar/GOREV.md`, “Bulgu kaydı” bölümü. 18 Kasım 2026 kaydı, ayrı çalışan ilk inceleme görevinin deneme turudur (yayından sonra yapıldı).

Özet: `python3 tools/inceleme.py --ozet 14`. Açık kod bulguları: `python3 tools/inceleme.py --acik`; kodu düzelten oturum bulguya `"kapandi": "YYYY-AA-GG · <not>"` ekler.

`kacan.json`: günlük editörlerin kaçırıp kullanıcının (`kullanici`), harici bir incelemenin (`harici`) ya da haftalık görevin (`haftalik`) bulduğu sorunlar. Her kayıtta `neden`: `kural-yok` (kurallarda karşılığı yoktu), `ekran-yok` (sorun ekran.py'nin çekmediği bir ekrandaydı), `olcum-yok` (ölçülebilirdi ama ölçülmüyordu), `dikkat` (kural vardı, editör atladı), `kapsam-disi` (tek sayıya bakarak görülemez, site geneli). Özet: `python3 tools/inceleme.py --kacan 14`.
