---
name: stock-footage-forge
description: Builds YouTube Shorts (9:16, 1080x1920) and full music videos (16:9) by cutting royalty-free Pexels STOCK VIDEO clips to an existing music track — center-crop/fps normalization, xfade assembly, bar-aligned audio segment with two-pass -14 LUFS loudnorm, safe-area title card, fast h264_videotoolbox render. Use whenever a music release needs a vertical Short, a Reel/TikTok, a promo clip cut from stock footage, or a music video whose footage is real video (not a still cover with effects — that is ambient-video-forge). Trigger on "shorts yap", "shorts üret", "dikey video", "reels", "tiktok videosu", "stok videodan klip", "pexels videolarından video", "müzik videosu kur", "tanıtım klibi", "9:16", and whenever a track needs promotion on the Shorts feed. Pairs with pexels-media-scout (finds the clips) and healing-audio-youtube-seo (titles the upload).
---

# Stock Footage Forge

Stok video + mevcut müzik → Shorts ya da müzik videosu. `ambient-video-forge`
tek kareden efektle video üretir; **bu skill gerçek çekimden kurgu yapar.**
İkisi rakip değil: uzun albüm videosu forge'un işi, o videonun Shorts tanıtımı
bunun işi.

## Karar sırası — render'dan önce

1. **Kurgu iddiası olmadan kurgu yok.** Yayının brief'indeki tek değişken,
   Short'un da kurgusudur. WR-034'te iddia "iki kaynak ayırt edilemez hâle
   gelir" → kurgu iki çöl dünyasını dönüşümlü kesip soyut kum dokusunda
   birleştirir. Rastgele güzel klipler dizmek, YouTube'un 2025 "inauthentic
   content" politikasının tam tarif ettiği şey — hem demonetize riski hem
   kimliksiz iş. Kurguyu yazmadan klip arama.
2. **Segment ölçülür, baştan alınmaz.** İzleyici ~1.7 saniyede kaydırıyor;
   Short parçanın en güçlü ânında AÇILIR. WAV üstünde RMS zarfı çıkar
   (saniyelik pencere yeter), en yoğun bloğu bul, `audio_start`'ı oraya koy.
   Parçanın intro'su Short'un intro'su değildir.
3. **Süre: 20–35 sn, asla 60 sn üstü.** 60 sn üstü telif iddialı Short küresel
   bloklanıyor; kısa klipte %izlenme ve tekrar (algoritmanın ödüllendirdiği
   iki sinyal) kolay. `bpm` alanını doldur — script toplamı tam bar sayısına
   yuvarlar, döngü başa döndüğünde vuruş oturur.
4. **Klipler `pexels-media-scout` ile bulunur** (`--type video --preset
   reels-short`), elle Google'dan değil. O skill'in üç kuralı burada da
   geçerli: puan seçmez göz seçer (kontakt sayfası kur, BAK), konumu
   belirsiz kare kimlik demiri olmaz, insanlı/markalı kare elenir.
   API gerçekleri: `references/pexels-video-api.md` — özellikle
   `orientation=portrait` (gerçek dikey master), `quality` alanına güvenme,
   ID sakla URL saklama.

## Kurulum

```bash
# 1) Klipleri bul ve indir (pexels-media-scout)
python3 .claude/skills/pexels-media-scout/scripts/pexels_scout.py search \
  --type video --preset reels-short -q "..." -q "..." \
  --color "<yayının vurgu rengi>" --exclude-people --limit 18 --out /tmp/sl.json
# önizlemeleri indir, kontakt sayfası kur, GÖZLE seç, sonra download --pick ...

# 2) Başlık kartı (sanatçı paletiyle; atlanabilir ama akış sessiz izleniyor —
#    ilk kareden görünen tek satır bağlam, jenerik altyazıdan iyi çalışıyor)
python3 .claude/skills/stock-footage-forge/scripts/make_title_card.py \
  --title "TWO DESERTS, ONE THROAT" --sub "TAIGA SAHEL" \
  --ink "#E7DCC2" --accent "#B4622C" --out title.png

# 3) Manifest yaz (şema script başında) ve kur
python3 .claude/skills/stock-footage-forge/scripts/build_stock_video.py \
  manifest.json --dry-run     # önce komutu GÖR
python3 .claude/skills/stock-footage-forge/scripts/build_stock_video.py manifest.json
```

Script ne yapıyor: her klibi ffprobe ile ölçüp `scale=W:H:force_original_
aspect_ratio=increase,crop,setsar=1,fps,settb=AVTB,format=yuv420p` zincirinden
geçirir (yatay/dikey/kare her kaynak tek zincirle), xfade offset'lerini ölçülen
sürelerden hesaplar, ses kesitini **iki geçişli** loudnorm ile −14 LUFS'a
çeker (tek geçiş müzikte pompalar), bt709 etiketleriyle videotoolbox'a kodlar
ve çıkışın süresini **ölçerek** doğrular. Gerekçeler ve elle müdahale için:
`references/ffmpeg-pipeline.md`.

## Görsel kurallar

- **Metin güvenli kutuda:** 1080×1920'de ortalanmış ~880×1150 px — üst 192,
  alt 480, sağ 108 px Shorts arayüzü tarafından kaplı. `make_title_card.py`
  varsayılanı bunun içinde durur; kartı elle yaparsan bu kutudan çıkma.
- **Kadraj:** varsayılan merkez-kırpma. Konu merkezde değilse klibe
  `"crop_x"` yaz; otomatik reframe yok, karar göze ait.
- **Koyu/yavaş gradyanlı sahnede** videotoolbox bantlar — manifest'te
  `"encoder": "libx264"` seç; ≤60 sn işte fark saniyeler.
- Kapak ASLA Short'un görüntüsü olmaz (kanal kuralı); görüntü her zaman
  çekimden gelir.

## Yayın ve kayıt

- **Shorts sınıflandırması otomatik:** dikey oran + ≤180 sn = Short. Ayrı
  yükleme düğmesi yok. Başlık anahtar kelime taşısın (Shorts araması büyüyor),
  3–5 hashtag **açıklamada**. Ayrıntı: `references/youtube-shorts.md`.
- **İlgili video bağlantısı huninin kendisi:** Short'u albüm videosuna
  bağla (Studio → related video). Sabitlenmiş yorum + açıklama bağlantısı da.
- **Künye:** Pexels linki + çekimci adları açıklamaya (scout'un `CREDITS.md`'si
  hazır veriyor) + evin AI künye satırı. Stok kliplerin kendi ses izi lisanslı
  değil — hat zaten tüm klip seslerini atıyor, müzik tek ses.
- **Kayıt:** render `assets.csv`'ye (`asset_type=shorts_video`), yayın
  `publishing.csv`'ye, kapanış işleri `channel_log.csv`'ye. Seçilen VE elenen
  klipler gerekçeyle brief'e — pexels-media-scout bölümündeki gibi.

## Tuzaklar (yaşanmışlar)

| Tuzak | Gerçek |
|---|---|
| Pexels önizlemesi 403 veriyor | `preview` URL'sini **parametreleriyle** ve `User-Agent` başlığıyla çek; parametre kırpma |
| `trim=duration=` bitiş zamanı sanmak | `duration` ÇIKIŞ süresidir; `start`tan itibaren sayar |
| Skorun en iyi 6'sını indirmek | WR-034'te skor 84 alan klipler arasında ATV kalabalığı ve tabela vardı — göz elemeden indirme yok |
| Uzun fade-out | döngüde video "ölüp yeniden doğuyor"; 0.3 sn eşit fade kullan |
| `quality=="hd"` filtresi | yeni Pexels dosyalarının %60'ında quality `null` — boyuttan seç |
