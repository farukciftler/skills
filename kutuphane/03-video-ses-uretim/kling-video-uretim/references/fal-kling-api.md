# fal.ai × Kling — API Referansı

Doğrulama tarihi: **1 Eylül 2026**, fal.ai model sayfaları (`/api`, `/llms.txt`),
fal dokümanları ve `fal_client` Python kaynağı. fal fiyat ve şemaları sık
değiştiriyor; bir üretim gününden önce **fiyatı model sayfasından teyit et**.
`[?]` = doğrulanamadı.

## 1. Hangi uç nokta

Tam envanter `scripts/kling_video.py modeller` çıktısında. Karar tablosu:

| İş | Model | Neden |
|---|---|---|
| Yayın klibi (varsayılan) | `v3-pro` — `fal-ai/kling-video/v3/pro/image-to-video` | 1080p, 3–15 sn, bitiş karesi, negatif prompt, cfg; ailenin en iyi fizik/tutarlılığı |
| Prompt denemesi, kadraj kararı | `taslak` — `v2.5-turbo/standard` | 5 sn ≈ $0,21; 720p yeter, yayına gitmez |
| Bütçe daralınca yayın | `ekonomik` — `v2.5-turbo/pro` | $0,07/sn, 1080p; kaynak kompozisyonu ve ışığı iyi koruyor |
| İlk + son kare ile kesin kamera yolu | `o3-pro` ya da `o1` | Omni modeller ilk/son kare kontrolünde daha güçlü; negatif prompt yok |
| Web hero, büyük ekran | `v3-4k` | $0,42/sn; Reels için gereksiz |
| 6 plana kadar tek istekte çok çekim | `v3-pro` + `multi_prompt` | toplam ≤ 15 sn; `prompt` ile birlikte verilemez |

**Uç nokta şeması tuzakları**
- Başlangıç karesi alanı **uç noktaya göre değişir**: `start_image_url`
  (v3 pro/standard/4k, v3 turbo pro, v2.6 pro) · `image_url` (o3, v3 turbo
  standard, v2.5-turbo, v2.1, o1 değil — o1 `start_image_url`). Betik bunu
  tabloda tutuyor; elle istek kuruyorsan sayfaya bak.
- Bitiş karesi: `end_image_url` (v3, o3, o1, v2.6) · `tail_image_url` (v2.5-turbo pro).
- `duration` **string** (`"5"`). v3/o3: `"3"`–`"15"`; 2.x: `"5"`|`"10"`.
- `generate_audio` varsayılanı v3'te **true**, o3'te **false**. Mimari içerikte
  kapat: hem ucuz hem müzik post'ta eklenir. Betik varsayılan olarak kapatır.
- **`aspect_ratio` yok** — çıktı oranı girdi görselinden gelir. 9:16 istiyorsan
  görseli `hazirla.py` ile önce kırp.
- `seed` yok; `camera_control` v2.x/3.x I2V şemalarında yok `[?]` — kamera
  prompt'la ve bitiş karesiyle yönetilir.
- `cfg_scale` 0–1, varsayılan 0,5 (v3, v2.5-turbo, v2.1). v2.6 ve o3'te yok.
- `negative_prompt` varsayılanı `"blur, distort, and low quality"`; o3 ve
  v3 turbo standard'da alan yok.
- Prompt sınırı 2.500 karakter.
- Görsel: jpg/jpeg/png (webp/avif API'de `[?]`), ≤ 50 MB (o1: ≤ 10 MB),
  kısa kenar ≥ 300 px, oran 1:2,5 – 2,5:1.

## 2. Fiyat (saniye başı, USD; 10 sn = 2 × 5 sn, doğrusal)

| Model | ses kapalı | ses açık | 5 sn (ses kapalı) |
|---|---|---|---|
| v3 pro | 0,112 | 0,168 | 0,56 |
| v3 standard | 0,084 | 0,126 | 0,42 |
| v3 turbo pro | 0,14 | 0,14 | 0,70 |
| v3 turbo standard | 0,112 | — | 0,56 |
| v3 4k | 0,42 | 0,42 | 2,10 |
| o3 pro | 0,112 | 0,14 | 0,56 |
| o3 standard | 0,084 | 0,112 | 0,42 |
| v2.6 pro | 0,07 | 0,14 | 0,35 |
| v2.5-turbo pro | 0,07 | — | 0,35 |
| v2.5-turbo standard | 0,042 | — | 0,21 |
| v2.1 pro / standard / master | 0,09 / 0,05 / 0,28 | — | 0,45 / 0,25 / 1,40 |
| o1 | 0,084–0,112 | — | ~0,56 |

Bütçe kalıbı: bir Reels için **3 çekim × 2 varyant × 5 sn v3-pro ≈ $3,40**;
önce taslak katmanında kadraj denemesi (**6 × $0,21 ≈ $1,26**), sonra
seçilenleri v3-pro'da. `kling_video.py maliyet senaryo.json` gitmeden söyler.

## 3. Mekanik

**Kimlik.** `Authorization: Key <key_id:key_secret>`. Anahtar `FAL_KEY` ya da
`~/.config/fal/key` (600). Depoya, sohbete, commit'e girmez.

**Kuyruk (betiğin kullandığı yol).**
1. `POST https://queue.fal.run/{model-id}` gövde = model girdisi →
   `{request_id, status_url, response_url, cancel_url, queue_position}`
2. `GET {status_url}?logs=1` → `IN_QUEUE` (queue_position) · `IN_PROGRESS`
   (logs) · `COMPLETED` (metrics.inference_time)
3. `GET {response_url}` → `{"video": {"url", "content_type", "file_name", "file_size"}}`
4. İptal: `PUT {cancel_url}`.
Durum/sonuç URL'leri yanıtın içinden kullanılır; alt yollu modellerde elle
kurmak (`…/v3/pro/image-to-video/requests/…`) yanlış olabilir, kök uygulama
yolu (`fal-ai/kling-video/requests/…`) gerekir. Betik `durum`/`sonuc`
komutlarında ikisini de dener.

**Webhook.** Gönderime `?fal_webhook=https://…` ekle; `status: OK|ERROR`,
`payload`. İmza ED25519, JWKS `https://rest.fal.ai/.well-known/jwks.json`.
Bu makinede sunucu yok; `--arka-plan` + `sonuc` yeterli.

**Yükleme.** `POST https://rest.fal.ai/storage/auth/token?storage_type=fal-cdn-v3`
→ `{token, token_type, base_url}`; sonra `POST {base_url}/files/upload`
(`Authorization: {token_type} {token}`, `Content-Type`, `X-Fal-File-Name`) →
`{access_url}`. Yedek: `POST /storage/upload/initiate?storage_type=gcs` →
`{upload_url, file_url}`, `PUT upload_url`. Son çare: `data:` URI (kabul
ediliyor, büyük dosyada yavaş). Betik üçünü sırayla dener.

**Eşzamanlılık.** Yeni hesapta 2 eşzamanlı `IN_PROGRESS`; kuyruktakiler
sayılmaz, düşürülmez. `toplu` komutu hepsini gönderir, kuyruk sıralar. v3 için
hesap başına 1 `[?]`.

**Çıktı ömrü.** Sonuç dosyası fal CDN'de; varsayılan saklama süresi
belirtilmemiş `[?]` — betik **hemen indirir**. İstek/yanıt JSON'u 30 gün.

**Hata tipleri.** `content_policy_violation` (422, tekrar deneme yok —
prompt'taki insan/marka/metin ifadesi ya da görsel), `image_too_large/small`
(422), `concurrent_requests_limit` (429), `generation_timeout` (504),
`downstream_service_error` (400). Betik 429/5xx'te üstel bekleme ile 5 deneme.

**Süre.** Ölçülen/ilan edilen: o3 standard ~95 sn (5 sn klip), v3 pro ~2 dk
(5 sn), 10–15 sn kliplerde 5 dk+. v2.1 pro ~5 dk. Planlama: **klip başına
2–6 dk**; `toplu` çalıştırıp başka işe geç.

**Çıktı.** MP4, 1080p (pro katmanları), 720p (standard), 4K (4k). FPS fal'da
yazmıyor `[?]`; Kling spesifikasyonu 30 fps. `bitir.py` 30 fps'e sabitler.

## 4. Yardımcı uç noktalar (`kling_video.py calistir <endpoint> --json '…'`)

| İş | Uç nokta | Girdi | Ücret |
|---|---|---|---|
| Upscale + 60 fps (zamansal tutarlı) | `fal-ai/topaz/upscale/video` | `video_url`, `upscale_factor` 2, `model` Proteus, `target_fps` 60 (isteğe) | $0,02/sn 720→1080p; 60 fps ×2 |
| Ucuz upscale | `fal-ai/seedvr/upscale/video` | `video_url`, `target_resolution` 1080p | ~$0,25 / 5 sn 1080p |
| Kare ara değerleme | `fal-ai/rife/video` | `video_url`, `num_frames` 1, `loop` | $0,0013/işlem sn |
| Uzatma (Kling'de yok) | son kareyi al → yeni klip (`bitir.py --son-kare`) | — | — |
| Alternatif I2V A/B | `fal-ai/veo3.1/fast/image-to-video`, `bytedance/seedance-2.0/fast/image-to-video`, `fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video` | model sayfasına bak | $0,10–0,24/sn |

fal'da **Kling extend yok**; `multi_prompt` (≤15 sn) ya da son-kare zinciri.

## 5. Ham örnek (curl)

```bash
curl -X POST "https://queue.fal.run/fal-ai/kling-video/v3/pro/image-to-video" \
  -H "Authorization: Key $FAL_KEY" -H "Content-Type: application/json" \
  -d '{"start_image_url":"https://…/cephe-9x16.jpg",
       "prompt":"Slow, steady push-in toward the entrance…",
       "duration":"5","generate_audio":false,"cfg_scale":0.5,
       "negative_prompt":"blur, distortion, warping, people, cars, text"}'
```

## Kaynaklar
fal model sayfaları: `fal.ai/models/fal-ai/kling-video/{v3,o3,v2.6,v2.5-turbo,v2.1,o1}/…/image-to-video`
(`/api`, `/llms.txt`) · `fal.ai/docs/documentation/model-apis/inference/{queue,webhooks,synchronous}` ·
`…/concurrency-limits` · `…/media-expiration` · `fal.ai/docs/model-apis/errors` ·
`github.com/fal-ai/fal/projects/fal_client` (client.py) · `blog.fal.ai/kling-3-0-is-now-available-on-fal/` ·
`fal.ai/models/fal-ai/topaz/upscale/video`, `…/seedvr/upscale/video`, `…/rife/video`.
