# YouTube Shorts — ölçülmüş gerçekler (araştırma: 2026-08-13)

Kaynaklı tam rapor bu dosyanın sonunda; burası hattı süren özet.

## Teknik sınırlar

| Parametre | Değer |
|---|---|
| Tuval | **1080×1920, 9:16** (4K dikey kabul ediliyor, gerek yok) |
| Shorts sayılma şartı | kare-veya-dikey oran **ve** ≤ 180 sn — ayrı bir "Short olarak yükle" düğmesi YOK |
| Maks süre | 180 sn (2024-10-15'ten beri) — ama **≤ 60 sn kal**: 60 sn üstü telif iddialı Short **küresel bloklanıyor**; 60 sn altı yalnız para kaybediyor |
| Hedef süre (müzik) | **20–35 sn**, kaynaklar 15–30 vs 30–60 diye bölünüyor; ödüllendirilen şey ortalama %izlenme + tekrar — kısa klipte ikisi de kolay |
| Encode | MP4 faststart, H.264 High, **8–12 Mbps @1080 (30fps), 12 Mbps @60fps**, BT.709, 4:2:0, AAC-LC 48 kHz 384 kbps |
| Ses seviyesi | YouTube ≈ **−14 LUFS'a yalnız KISAR**, yükseltmez. Master ≈ −14 LUFS int., ≤ −1 dBTP. Sessiz ambient master Shorts akışında komşularından kısık kalır — Shorts kesitinde −14'e normalize et |

## Güvenli alan (1080×1920)

Google'ın tek resmî rakamı (Shorts reklam spec'i): **üst %10 (~192 px), alt %25 (~480 px), sağ %10 (~108 px)** kaplı.
Üçüncü taraf ölçümleri biraz daha sıkı. Sağlam kural: **tüm metin/logo, ortalanmış ~880×1150 px kutuda** —
kenarlardan ≥100 px, üstten ≥200 px, alttan ≥480 px. Alt ~40 px'te ilerleme çubuğu var. Kadraj merkezi hiçbir zaman örtülmüyor.

## Ne işliyor

- **Kanca 0. saniyede.** İzleyici ~1.7 sn'de kaydırma kararı veriyor. Parçanın en güçlü ânı Short'un 0:00'ında başlar — şarkının intro'su değil. Nakaratı/en yoğun dokuyu kes, oradan başlat.
- **Döngü birinci sınıf strateji.** Shorts otomatik başa sarıyor ve tekrar izlenme ağır basıyor. Son kare ≈ ilk kare, ses barda kesilmiş → dikişsiz döngü. Uzun fade-out YAPMA: döngüde video "ölüp yeniden doğuyor" hissi veriyor ve retention'ı vuruyor. 0.3 sn'lik eşit fade'ler nefes gibi okunuyor.
- **Metin ilk kareden itibaren, tek satır, merkeze yakın.** Çoğu izleyici ilk anda sessiz izliyor; enstrümantal müzikte bağlam satırı ("140 → 44 BPM, yalnızca aşağı") jenerik altyazıdan iyi performans veriyor.
- **En iyi segment kullanılır** — 3 dakikalık parça 6–12 Short verir. Ambient'te "nakarat"ın karşılığı: kimliğin en yoğun ânı (çalgı girişi, en tanınır motif).

## Metadata ve dağıtım

- `#shorts` etiketi sınıflandırma için GEREKMİYOR (oran+süre belirliyor). Hashtag dağıtımı artırmıyor; 3–5 tanesi **açıklamada** (başlıkta değil) dursun.
- Shorts algoritması uzun formdan ayrı: küçük tohum kitle → sinyaller iyiyse genişletme. Feed organik izlenmenin %60+'ı; arama küçük ama büyüyor (2026'da Shorts arama filtresi geldi) — başlık artık anahtar kelime taşısın.
- **İlgili video bağlantısı = huninin kendisi.** Short'a TEK video iliştirilebilir (Studio'da, yükleme akışında ya da düzenlemede); kanal adının altında tıklanır kapsül olarak görünür. Gelişmiş özellik erişimi ister; hedef herkese açık/liste dışı olmalı. **Her Short, albüm videosuna bağlanır** — ayrıca sabitlenmiş yorum + açıklama bağlantısı.
- Belgelenmiş taktik: **çok Short → tek uzun video** ("flooding") — trafiği tek hedefe toplar.

## Para ve politika

- Shorts geliri havuz modeli; kendi müziğin = "no music track" durumu (Shorts Audio Library lisanslı parça kullanmıyorsun), bölüşüm yok. Shorts RPM ~$0.01–0.10/1K — Shorts keşif aracı, gelir kalemi değil.
- **2025-07-15 "inauthentic content" politikası:** şablonlaşmış, insan katkısız seri AI içerik demonetize edilebiliyor. Salt stok-görüntü+müzik derlemesi kanonik "düşük emek" deseni — **karşı önlem tam bizim sistem:** sanatçı başına ayrı kimlik, yayına özel kurgu iddiası, künye satırı, insan seçimi (kontakt sayfası kuralı).
- Suno kaynaklı müzik Content ID'ye alınmıyor (2025 ortası itibarıyla) — kendi Short'unu kendi dağıtımcın claim'lemez; ama üçüncü taraf kopyalamaya karşı otomatik koruma da yok.

## Açık/belirsiz noktalar

1. Shorts oynatıcısının mobil feed'de −14 LUFS normalizasyonu uyguladığı doğrulanamadı (izleme sayfasıyla aynı varsay).
2. Güvenli alan pikselleri cihaza/uygulama sürümüne göre oynuyor — %10/%25/%10 tek resmî rakam.
3. İdeal süre verisi çelişkili (15–30 vs 30–60 kampı) — varsayılan 20–35 sn, ölçümle oyna.
4. Huni dönüşüm rakamları (%2–4) satıcı beyanı, denetlenmiş veri değil.
