---
name: masifico-video-uretim
description: Masifico'nun gerçekçi ürün videosu operatörü. Blender rigid body fizik simülasyonu (kule istifleme, devrilme, yuvarlanan araba; kayın için friction/bounciness sabitleri, küçük nesne ölçek tuzağı), kamera animasyonu kalıpları, EEVEE Next / Cycles Metal çift motor stratejisi, M2 Pro render süreleri, AgX renk yönetimi, ffmpeg bt709 encode, contact-log tabanlı ahşap foley senkronu, 9:16 sosyal format kuralları (hook, safe area, altyazı, süre bantları) ve 2026 AI video araç sınırları için tek kaynak. Kullanıcı "video al", "reels üret", "animasyon render", "fizik simülasyonu", "devrilme videosu", "araba gitsin", "slow motion", "ASMR video", "TikTok/Etsy videosu", "ürün videosu" dediğinde; bir SKU'nun hareketli içeriği planlanır veya üretilirken; ya da render/encode/ses senkronu sorunu çözülürken bu skill kullanılır. Derin kaynak docs/arastirma/gercekci-video-render-arastirma-v1.md; skill oradaki değerleri uygulama reçetesine indirir.
---

# Masifico Video Üretim Operatörü

Amaç: CAD modelden (build123d STEP/STL/GLB) gerçek çekimden ayırt edilmesi zor, deterministik
olarak tekrar üretilebilir video çıkarmak. Repo kültürü videoya aynen taşınır: üret (fizik bake) →
render (başsız CLI) → encode (ffmpeg) → denetle, tek script zinciri; beğenilen take'in kimliği
cache + seed'dir. Değerlerin kaynağı `docs/arastirma/gercekci-video-render-arastirma-v1.md`.

## 1 · Altın kurallar

1. **Ürün pikselleri yalnız CAD render'dan veya gerçek çekimden gelir.** AI video (Veo 3.1,
   Kling 3.0, Runway Gen-4/Aleph) yalnız atmosfer, geçiş ve arka plan katmanı; AI üretimli
   karede ürün görünüyorsa video REDDEDİLİR (geometri ve marka rengi kareler arası kayar,
   olmayan ürün göstermek dürüstlük sorunudur). Sora 2'nin 7 ayda kapanması tek sağlayıcıya
   iş akışı kurmama dersidir.
2. **Deterministik üretim:** sabit seed başlangıç koşulları + bake edilmiş cache + kontak logu =
   take kimliği. Seed ve sürüm çıktı adına/künyeye yazılır; 9:16 ve 16:9 aynı cache'ten çıkar.
3. **Çift motor:** günlük sosyal içerik EEVEE Next (4-10 sn/kare), haftalık hero Cycles Metal
   (30-90 sn/kare). M2 Pro'da 6 sn reels: EEVEE 15-25 dk, Cycles 1,5-4 saat. Shader'lar ortak.
4. **Doğrudan videoya render alınmaz;** önce kare dizisi (PNG/EXR), sonra ffmpeg.
5. Satış kilidi dili video açıklamalarında da korunur.

## 2 · Fizik reçetesi (Bullet)

- **Ölçek tuzağı:** Bullet 20 cm altında stabil değil; ürünler 42-160 mm. Sahne **5-10 kat
  büyütülmüş** kurulur (ağır çekim hissi premiuma yarar); gerçek tempo istenirse gravity ×ölçek.
  DOF, ışık boyutu ve gravity AYNI çarpanla ölçeklenir yoksa maket hissi doğar; çarpan tek sabitte tutulur.
- STL importtan sonra mutlaka Apply Scale (Ctrl-A).
- **Collision shape:** DT-10 taşları Convex Hull · KB-24 blokları Box, silindirleri Cylinder
  (lokal Z = silindir ekseni) · AR-07 tekerleri Cylinder. Mesh shape kullanılmaz.
- **Kayın sabitleri:** friction blok-blok 0,45-0,55, blok-masa 0,5-0,6, halı 0,7+;
  bounciness istif/kule 0-0,05, tek çarpma vurgusu 0,1-0,3. Kütle: Calculate Mass (Wood, ~720 kg/m³).
  Damping translation 0,04-0,1, rotation 0,1-0,2.
- **World:** istif sahnesinde Substeps 30-60, Solver Iterations 20-50, **Split Impulse KAPALI**
  (tek çarpmada açık). Start Deactivated = "önce duruyor, sonra yıkılıyor" senaryosu.
- **Sanat hileleri:** Animated checkbox (taşları elle kondur, son taşta fiziğe bırak);
  ters oynatma ("bloklar kendiliğinden diziliyor"). Passive zemine keyframe verirken Animated işaretle.
- **Tekerlekli araç (AR-07):** aks/teker dönüşü keyframe ile sürülür ya da hinge constraint;
  gövde Active + Convex Hull. Bake → Bake To Keyframes (motion blur ve ses script'i için şart).

## 3 · Kamera ve gerçekçilik

- Kalıplar: orbit (Empty pivot, Linear + Cyclic modifier = kusursuz loop; 30-60° yay yeter),
  dolly/push-in (Track To açık), macro slide (85-105 mm, DOF Focus Object = Empty, raking ışık
  10-30°). Fizik sahnesinde kamera sabit; hareket sakin planlara. 25 fps, tek harekette tek fikir.
- Gerçekçiliğin üç sıçraması: **kenar pahı** (0,5-2 mm; STL'de yoksa Cycles Bevel node r 0,5-1,
  samples 8-16) · **roughness varyasyonu** (sabit roughness = "render gibi durma"nın 1 numaralı
  sebebi; imperfection map %10-30, parmak izi maskesi roughness'ı 0,05-0,1 düşürür, zımpara/bez
  izi yönlü desen) · **motion blur 180°** (Cycles Shutter 0,5, Position Center; fizik bake şart).
- DOF gerçek lens tablosuyla: full-frame 50-85 mm f/2.8-5.6, konu 0,4-0,8 m; post'ta gaussian
  blur ile DOF taklidi yasak. Albedo 30-240 sRGB bandı; nokta ışık yerine gerçek boyutlu area.
- **Renk:** AgX (Filmic'in Notorious Six kusuru kiremit #CE4F1F'i bozar). Render EXR linear →
  AgX grade → Rec.709 teslim. Palet AgX altında bir kez test kartıyla doğrulanır; kiremit/petrol
  tonlarında %5-10 saturation telafisi grade preset'i olur. Standard transform asla.
- **Flicker:** Use Animated Seed açık, OIDN High/Accurate/Albedo+Normal, threshold 0,005-0,01,
  yeterli sample (256-1024). Cycles'ta temporal denoiser yok; kalan titreme kompozitte.

## 4 · Render ve encode sabitleri

- Cycles animasyon: Adaptive threshold 0,01-0,02, Max Samples 256-512 (1080p), Light Tree açık,
  Persistent Data açık (statik sahnede ~10 kat), GPU Compute Metal.
- Başsız: `blender -b sahne.blend -E CYCLES -o //kareler/kare_#### -F PNG -s 1 -e 125 -a -- --cycles-device METAL`
- Sosyal H.264 (ASWF): `ffmpeg -r 25 -i kare_%04d.png -pix_fmt yuv420p10le -vf "scale=in_color_matrix=bt709:out_color_matrix=bt709" -c:v libx264 -preset slower -crf 18 -movflags faststart out.mp4`
  **bt709 scale filtresi zorunlu** (yoksa bt601'e düşer, marka rengi kayar).
- Arşiv: `prores_ks -profile:v 3` (422 HQ); alfa gerekirse 4444. Ses: `-c:a aac -b:a 256k -shortest`.

## 5 · Ses (foley + senkron)

- En doğru kaynak kendi ürünü: 48 kHz, sessiz oda, keçe zemin, darbe tipi başına 8-10 varyasyon
  (tık, tok, sürtme, kaskad). Lisans sorunu sıfır + TikTok işletme hesabının trend müzik yasağını
  orijinal ses avantaja çevirir. Freesound'da CC0 filtreli yedekler raporda listeli; BBC arşivi ticari değil.
- Senkron: bake edilmiş animasyonun hız-delta analizi (Bake-Collisions-To-Sounds eklentisi veya
  f-curve script'i) → (kare, nesne, şiddet) JSON → VSE/ffmpeg. Varyasyon: rastgele örnek + ±1-2
  yarım ton pitch + ±2 dB. Kule yıkılışında 3-4 belirgin darbe + tek kaskad kaydı; altına hafif oda tonu.
- Kayıt yoksa modal sentez: 2-5 sönümlü sinüzoid (örn. 700/1400/2800 Hz, decay 30-80 ms) + kısa gürültü.

## 6 · Format ve içerik kuralları (9:16, 2026)

- Master 1080×1920 MP4 H.264; kritik içerik **840×1300 merkez blokta** (üç platformun safe
  area'sını birden temizler); logo üst 220 px'in altında. Reels akışta ~4:5 kırpar, dikey merkeze kur.
- Süre bandı 15-30 sn en yüksek tutundurma; hook ilk 2-2,5 saniyede tamam (ilk 3 sn'de %50-60
  izleyici düşer); en çarpıcı kare (devrilme anı) AÇILIŞ karesi olur, sona saklanmaz.
- Gömülü altyazı her videoda (%15-25 retention farkı; izleyicinin %60+'ı sessiz izler).
  Kesme temposu 2-4 sn; son başa bağlanan loop dağıtımı büyütür.
- Etsy: 5-15 sn kesit, ses tamamen silinir (%100 görsel anlatım), 1080 px+, listing başına 1 video.
- Format matrisi (rapor §21): slow-mo devrilme+loop · ASMR dizme (hands-only) · stop motion
  (12 fps) · unboxing · atölye perde arkası · ebeveyn eğitimi (Lovevery modeli) · challenge
  tohumu ("kaç taş dizebilirsin", Grimm's topluluk modeli). Çocuk yüzü değil çocuk eli.

## 7 · Teslim öncesi denetçi listesi

Shutter 0,5 (180°) mi · AgX ve aynı grade tüm planlarda mı · DOF lens tablosuyla uyumlu mu ·
animated seed açık mıydı · encode komutunda bt709 filtresi var mı · CG planlarda grain match
var mı · seed + sürüm künyede mi · AI karede ürün görünüyor mu (görünüyorsa RED) ·
satış kilidi ibaresi açıklamada mı. Denetçi geçmeden video yayınlanmaz.

## 8 · Zincirdeki yeri

`masifico-urun-gorsel` sahne/materyal reçetesini kurar (aynı GLB, aynı kayın shader'ı) →
**bu skill** hareket, ses ve dağıtım katmanını ekler. Alternatif headless hat (rapier + Bevy +
kontak log ses sentezi) için `headless-reel-forge` skill'i; determinizm kuralları rapor §12.
