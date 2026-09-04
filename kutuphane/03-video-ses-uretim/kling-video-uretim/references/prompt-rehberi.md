# Kling Prompt Rehberi — Mimari Render'dan Hareket

Kaynak: fal.ai Kling 3.0 / O1 / 2.6 prompt kılavuzları, Kling API şeması,
mimari görselleştirme stüdyolarının (visiomake, archivinci, renderai) saha
notları, 1 Eylül 2026. Kling'in kendi sitesi erişilemedi; oradan alıntı yok.
Prompt'lar **İngilizce** yazılır (model İngilizce eğitilmiş; Türkçe prompt
otomatik çevrilir ve kontrol kaybolur). Ekran metni ve açıklama Türkçe kalır.

## 1. Temel ilke: görsel sahneyi anlatır, prompt yalnızca hareketi

Image-to-video'da sahneyi yeniden tarif etmek zarar verir; model görselde
olmayan detay "ekler". Prompt = **ne hareket ediyor + kamera ne yapıyor +
ışık nasıl değişiyor**. 15–40 kelime, en fazla 60–100.

Sıra: önce sahne/ hareket, **kamera cümlesi en sonda** (Kling önce sahneyi
kurar, sonra kamerayı hareket ettirir).

**Tek hareket kuralı.** Bir klipte bir kamera hareketi. "Orbit + zoom" gibi
birleşik hareketler geometriyi büker.

**Hareketin sonu olsun.** "…then settles", "holds for the last second" —
yoksa model ikinci bir olay uydurur.

**Hız sözcüğü zorunlu.** `slow`, `very slow`, `gentle`, `steady`, `smooth
gimbal`. Yazılmazsa orta hız gelir; mimaride orta hız = bükülme.

**Işığı adıyla söyle.** "warm interior lights glowing through windows",
"blue-hour sky darkening", "last sunlight on the facade". "cinematic" tek
başına hiçbir şey yapmaz.

## 2. Kamera sözlüğü (Kling düz cümle anlar; köşeli komut Hailuo'ya özgü)

| Amaç | İfade | Mimaride not |
|---|---|---|
| Sabit | `static shot, locked-off camera, no camera movement` | Gökyüzü/ışık/su hareketiyle birlikte en güvenli seçenek |
| Yaklaşma | `slow push-in toward …`, `slow dolly in` | **En güvenilir hareket.** 5 sn |
| Optik zoom | `slow zoom in on the entrance` | Push-in'den daha az paralaks → daha az bükülme |
| Uzaklaşma | `slow pull-out to reveal …` | Kadraj dışını **uydurur** — mimaride kaçın, bitiş karesi yoksa kullanma |
| Yatay kayma | `slow dolly right, subtle parallax between foreground trees and the facade` | Kısa mesafe; ön plan ağaç varsa iyi çalışır |
| Tilt | `very slow tilt up along the facade from the entrance to the roofline` | 4–5 sn; dikey hatları vurgular — Moonstone kimliği dikeylikte |
| Crane | `slow crane down from the roofline to the entrance` | K1 açılışı için (katlar tek tek ışıklanır) |
| Orbit | `very slow orbit to the right, about 20 degrees, building stays centered` | **≤ 20–30°** / 5 sn; tam tur görünmeyen cepheyi uydurur |
| Drone | `slow aerial drone push-in with gentle descent` | Yükseklik değişimi az tutulur |
| Lens | `35mm`, `24mm wide`, `shallow depth of field` | Stil ipucu, kesin parametre değil |

## 3. Mimariyi sabit tutan ifadeler ve negatif prompt

Prompt'a eklenen sabitleyiciler (her mimari prompt'ta en az ikisi olsun):
`the building stays perfectly still and rigid` · `straight lines remain
straight` · `no people appear` · `no new objects appear` · `consistent color
grading` · `geometry stays rigid and sharp`.

**Varsayılan negatif** (betik boş bırakılınca bunu gönderir):
```
blur, distortion, warping, morphing, bending lines, warped windows, melting glass,
distorted architecture, extra buildings, people, pedestrians, cars, crowds, text,
logos, watermark, flicker, camera shake, fast camera, zoom out, low quality
```
Negatif prompt yumuşak bir eğilimdir, maske değil; yanlış kamera seçimini
kurtarmaz.

**cfg_scale.** 0–1, varsayılan 0,5. Model fazla hareket ekliyorsa düşür
(0,3–0,4); kamera komutunu dinlemiyorsa yükselt (0,6–0,7). Mimari için
0,5 ile başla, tek eksende değiştir.

## 4. Bilinen bozulmalar → çözüm

| Sorun | Neden | Çözüm |
|---|---|---|
| Doğramalar / çatı çizgisi "nefes alıyor" | Orbit, pull-out, uzun klip | Yalnızca push-in / zoom / kısa tilt; ≤ 30°; sabitleyici ifadeler |
| Camlar eriyor, yansıma titriyor | Cam + hareket | Hareketi azalt, `static shot` + çevre hareketi (bulut, ışık); daha az camlı açı seç |
| Zamanla kayma | 10 sn | **5 sn üret, iki 5'i birleştir**; bitiş karesiyle sabitle |
| İnsan / araba beliriyor | Kling "istenmeyen hareket ekler" | Negatif + "no people appear"; K6: yapay figür gerçek sakin gibi sunulmaz |
| Tabela / logo bozuluyor | Metin kararsız | Metni hareketli kareye koyma; logo ve yazı `katman.py` ile post'ta |
| Sonda doygunluk kayıyor | Bilinen davranış | `consistent color grading`; gerekirse `grade.swift` ile ilk kareye eşle |
| Ağaç / mermer "kaynıyor" | İnce doku + hareket | Hareketi azalt; upscale'i **sonra** yap; farklı seed için yeniden üret |
| Kenarlarda uydurma içerik | Pull-out / pan | Yalnızca görselin **içine** hareket et |

Kaynak görsel: uzun kenar ≥ 2.000 px ideal; kısa kenar < 1.080 ise Kling
büyütür ama yumuşar. Kat planı en zayıf girdi: çizgi titrer — plan
animasyonu için `bitir.py`/ffmpeg Ken Burns daha iyidir, AI değil.

## 5. İlk + son kare (ilk/son kare kontrolü)

`end_image_url` / `tail_image_url`: aynı sahnenin iki kamera konumunu ver,
model arasını yürür. **Kesin kamera yolu için en etkili yöntem** ve iki uçta
geometriyi sabitler. Kurallar: iki kare aynı ışık/saat; bakış açısı sıçraması
küçük (büyükse yürüme yerine morflama olur); prompt görünen değişimi anlatsın
("camera moves from the wide view to the entrance"). Mimari ofisten aynı
sahnenin iki açısı istenirse (`Mimari-Ofis-Talep-Listesi.md` madde 2) bu
mod kullanılır. Döngü için: başlangıç = bitiş görseli.

## 6. Moonstone için hazır prompt'lar

Her biri 5 sn, `v3-pro`, ses kapalı. `[…]` yerleri kadraja göre doldur.
Türkçe satır yalnızca ne olduğunu söyler, prompt'a girmez.

**P1 · Cephe, mavi saat, yaklaşma (Reels 01/02 açılış)**
> The building stays perfectly still and rigid, straight lines remain straight. Blue-hour sky darkens very gradually, warm interior lights glow brighter behind the glass, ground-floor shopfronts glow softly. Thin clouds drift slowly. No people, no cars, no text. Slow, steady push-in toward the entrance, 35mm, smooth gimbal, then settles.

**P2 · Cephe, sabit kamera, ışık değişimi (en güvenli)**
> Static locked-off camera, no camera movement. Sunset sky slowly shifts from orange to deep blue, apartment windows warm up one by one, faint reflections move on the glass balustrades. Geometry stays rigid and sharp. No people appear.

**P3 · Cephe, sokak seviyesinden tilt (dikeylik)**
> Camera at street level. Very slow tilt up along the facade from the illuminated ground-floor shops to the roofline over the full duration, tripod-smooth. Late golden light on the cladding, leaves on foreground trees move gently. The building stays rigid; straight lines remain straight. No people.

**P4 · Cephe, ön plan ağaçlı paralaks**
> Slow lateral dolly to the right with subtle parallax between the foreground trees and the facade; the building stays rigid and centered. Soft evening light, long shadows creep slowly. No new objects appear, no people, no cars.

**P5 · Cephe, mikro-orbit**
> Very slow orbit to the right, about 20 degrees over the full duration, keeping the building centered and rigid, smooth gimbal. Sunset clouds drift slowly, interior lights glow. Straight lines remain straight. No people, no cars.

**P6 · Drone yaklaşımı (Reels 02 kancası)**
> Slow aerial drone push-in from a high wide view toward the residence with a gentle descent, camera tilting down slightly, smooth. Sky stays calm, evening light glints softly on the glass. Buildings remain rigid and sharp. No people, no cars.

**P7 · Crane iniş — katlar ışıklanır (Reels 01 kancası)**
> Slow crane down from the roofline toward the entrance over the full duration, smooth. As the camera descends, the apartment windows light up floor by floor with warm light, blue-hour sky above. The building stays perfectly still and rigid. No people.

**P8 · Kapalı havuz (Reels 06)**
> Static camera, no camera movement. Water surface ripples gently, light caustics move slowly across the pool floor and the ceiling, soft steam near the surface. Walls, loungers and plants stay perfectly still. No people appear.

**P9 · Havuz, yavaş yaklaşma**
> Slow, steady push-in along the length of the pool toward the far glass wall, eye level, smooth gimbal. Water ripples gently, reflections shimmer softly. Architecture stays rigid, straight lines remain straight. No people.

**P10 · Salon / iç mekân (render gelince)**
> Slow dolly-in toward the window, 35mm, gimbal-smooth. Sheer curtains move very gently, evening light shifts slowly across the floor. Furniture and walls stay perfectly still. No people.

**P11 · Teras, manzaraya çıkış (Reels 09 kapanışı)**
> Camera holds still for a moment, then slowly pushes toward the terrace railing and the evening city view. Sunset sky glows, distant lights twinkle softly, rigid architecture, straight lines remain straight. No people.

**P12 · Koridor / lobi**
> Slow forward push along the corridor's perspective lines, smooth steadicam, no bob. Ceiling lights stay steady, reflections on the floor remain calm. No people.

**P13 · Ticari zemin kat (Reels 03 gövdesi)**
> Slow lateral dolly along the illuminated ground-floor shopfronts at street level, smooth. Warm light spills from the glass, gentle reflections on the pavement. Building stays rigid, no people, no cars, no signage text.

**P14 · Kapanış öncesi sakin kare**
> Static shot, locked-off camera. Very subtle drift of thin clouds across the blue-hour sky, interior lights glow steadily, nothing else moves. Rigid geometry, no people.

## 7. Üretim disiplini

- Her çekim için **2 varyant** üret (aynı prompt, farklı çıktı); en iyi kareyi seç.
  Kling seed vermiyor; tekrar = yeni deneme.
- Önce `taslak` katmanında 1 varyant: kadraj ve hareket doğru mu? Sonra `v3-pro`.
- Seçim ölçütü: doğramalar düz kaldı mı · cam eridi mi · insan/araba belirdi mi ·
  son yarım saniyede renk kaydı mı · hareket sonunda durdu mu.
- Kabul edilen klibin künyesi (`.json`) klibin yanında durur: kaynak render,
  prompt, model sürümü, request_id. İleride bir alıcı "bu görüntü gerçek miydi"
  derse dosya oradadır.

## Kaynaklar
blog.fal.ai/kling-3-0-prompting-guide · fal.ai/learn/devs/kling-o1-prompt-guide ·
fal.ai/learn/devs/kling-2-6-pro-prompt-guide · veed.io/learn/kling-ai-prompting-guide ·
atlascloud.ai/blog/guides/kling-ai-video-prompt-guide · glif.app/use-cases/kling-3-prompting-guide ·
prompt-architects.com/blog/25-30-cinematic-camera-prompts-for-veo3-and-kling ·
visiomake.com/en/blog/runway-vs-kling-vs-pika-architecture-renders ·
visiomake.com/en/blog/ai-architecture-walkthrough-video-from-still-renders-2026 ·
archivinci.com/architecture-ai-tools/ai-image-to-video · renderai.app/blog/video-ai-models-for-architects-designers-marketers ·
queststudio.io/blog/reduce-flicker-melting-artifacts · github.com/aself101/kling-api (resmî şema aynası).
