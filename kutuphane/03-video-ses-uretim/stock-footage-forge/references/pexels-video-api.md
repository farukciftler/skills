# Pexels Video API — ölçülmüş gerçekler (araştırma: 2026-08-13, canlı API'ye karşı doğrulandı)

`pexels-media-scout` skill'i arama/puanlama/indirme işini zaten yapıyor — **video aramayı oradan sür**
(`--type video --preset reels-short`). Bu dosya, o skill'in üstünü örtmediği API gerçeklerini tutar.

## Endpoint'ler

- `GET https://api.pexels.com/videos/search` — `query`, `orientation` (landscape|portrait|square), `size`
  (large=4K, medium=FullHD, small=HD; **taban** çözünürlük filtresi, dosya boyutu değil), `locale`, `page`,
  `per_page` (maks 80). Auth: `Authorization: <KEY>` — "Bearer" öneki YOK.
- `GET .../videos/popular` — `min_width/min_height/min_duration/max_duration`. **`orientation` parametresi YOK**,
  istemci tarafında genişlik/yükseklikten filtrele.
- `orientation=portrait` **gerçek dikey master döndürüyor** (1080×1920, 2160×3840) — kırpılmış yatay değil.
  Shorts işinde her zaman bununla ara; yatay kaynağı dikeye kırpmak son çare.

## `video_files[]` — dosya seçimi

- **`quality` alanına DALLANMA.** Canlı ölçüm (418 dosya): `null`=251, sd=83, hd=66, uhd=18 — yeni girişlerde
  çoğunluk `null`. Boyuttan seç: `file_type=="video/mp4"` filtrele → tam `1080×1920` varsa onu, yoksa
  `≥1080×≥1920` en küçüğü, yoksa en büyüğü.
- `fps` tuhaf değerler alabiliyor: 23.98, 28.57, 29.94, 59.94... Aynı videonun farklı çözünürlükleri farklı
  fps taşıyabiliyor. Hat her klibi zaten CFR'a normalize ettiği için sorun değil — ama süre hesabını
  **ffprobe ile ölç**, API'nin `duration`'ı tam saniyeye yuvarlanmış.
- İndirme linki `videos.pexels.com/video-files/...` — **kimlik doğrulaması yok.** Ama Pexels hosting'i bir kez
  değiştirdi (Vimeo → kendi CDN'i, eski linkler öldü): **kalıcı kayda URL değil video `id` yaz**, gerekirse
  ID'den yeniden çöz.
- Belgelenmemiş ama canlıda var: her dosyada `size` (bayt) ve videoda `video_pictures[]` (15 eşit aralıklı
  önizleme karesi) — **bedava kontakt sayfası.** "Puan seçmez, göz seçer" kuralının video karşılığı:
  önizleme karelerini indirip BAK. `preview`/`image` URL'lerini parametreleriyle ve `User-Agent` başlığıyla
  çek — parametre kırpılırsa 403.

## Kota, künye, lisans

- Kota başlıkları otorite: bu projenin anahtarı `X-Ratelimit-Limit: 25000`/ay döndürüyor. Yanıtlar
  `cache-control: max-age=3600` taşıyor, scout'un 24 saatlik önbelleği sorunsuz.
- **Lisans künye istemiyor ama API Guidelines istiyor:** "prominent link to Pexels" zorunlu, fotoğrafçı
  künyesi kuvvetle isteniyor. Ev kuralıyla aynı: **Pexels bağlantısı + çekimci adı YouTube açıklamasına.**
  Scout'un yazdığı `CREDITS.md`/`credits.json` bunu hazır veriyor.
- Ticari kullanım ve değiştirme serbest; satılamaz (değiştirmeden), marka/kişi onayı ima edilemez,
  başka stok platformda dağıtılamaz. Model/mülk release GARANTİ EDİLMİYOR — insanlı/markalı kare
  scout'un bayraklarıyla elenir, ambient işlerde zaten `--exclude-people`.
- **Stok kliplerin kendi ses izi lisanslı DEĞİL** (scout `audio-track-not-licensed` bayrağı basar) —
  hat zaten tüm klip seslerini atıyor (`-an`), müzik tek ses kaynağı. Bu bayrak bu hatta bilgi, engel değil.

## Süre gerçeği

80 videoluk örneklem: min 3 sn, medyan ~20 sn, ortalama 26 sn, maks 180 sn; %64'ü 10–40 sn bandında.
Yani bir Short 3–6 klipten kurulur; tek klipten Short çıkarmayı planlama, kesit + kurgu planla.
`total_results` ~8000'de kapaklanmış görünüyor (belgesiz) — derin sayfalamaya güvenme.
