---
name: kling-video-uretim
description: >
  Moonstone Residence için bir render ya da fotoğraftan fal.ai üzerinde Kling
  image-to-video ile kısa sinematik klip üretir ve bunu yayın Reels'ine
  çevirir: görseli okuyup çekim senaryosu yazar (kanca–gövde–kapanış, İngilizce
  Kling prompt'ları, Türkçe ekran metni, açıklama, etiket), görseli 9:16'ya
  hazırlar, fal kuyruğuna gönderir, klipleri künyesiyle indirir, marka
  katmanını (logo · tek satır başlık · "Temsili görseldir") güvenli alanda
  bindirir, ffmpeg/VideoToolbox ile birleştirip kapanış kartı ve müzik ekler.
  Şu ifadeler geçtiğinde kullan: "video üret", "hareketlendir", "render'ı
  videoya çevir", "Kling", "fal.ai", "image-to-video", "Reels videosu",
  "senaryo yaz", "bu fotoğraftan video", "drone hissi", "kamera hareketi",
  "klipleri birleştir", "video maliyeti". Kling ya da fal adı hiç geçmese bile
  bir görselden video üretilecekse devreye gir. Statik kare için
  `gorsel-uretim`, stok video için `pexels-gorsel-bulucu`, kural ve içerik için
  `moonstone-residence`.
---

# Kling Video Üretimi — fal.ai

Bu skill `gorsel-yon-referans.md` §7'deki **Rota C**'nin (mevcut render'dan
yapay zekâ ile hareket) üretim hattıdır: ara çözüm, 5–15 saniyelik yavaş
kamera hareketi ve geçiş kliplerinde iyi; tam tur videosu için 3D animasyon
(Rota A) hâlâ tek doğru yatırım. İş bölümü: **sen** görseli okur, senaryoyu ve
prompt'ları yazarsın, klipleri seçersin; **betikler** kırpma, API kuyruğu,
indirme, künye, katman ve montajı yapar.

Araştırma tarihi 1 Eylül 2026; fal fiyat ve şemaları için
`references/fal-kling-api.md`, prompt için `references/prompt-rehberi.md`,
senaryo kalıpları için `references/senaryo-sablonlari.md`, montaj / alternatif
model / hukuk için `references/post-produksiyon.md`.

## Kırmızı çizgiler — önce bunlar

1. **Metin ve logo AI karesine girmez.** Kling yazıyı bozar; marka katmanı
   post'ta `katman.py` ile biner. Karede ≤ 3 öğe (K4).
2. **Her klipte "Temsili görseldir" + açıklamada yapay zekâ beyanı** (K7).
   1 Ağustos 2026 yönetmelik değişikliği ve AB Madde 50 bunu zorunlu kılıyor
   (`post-produksiyon.md` §3). Instagram "Made with AI" açık.
3. **Kaynak kuralı:** katalog PDF'inden çıkarılmış ya da katalog türevi görsel
   **yayına gitmez** (`gorsel-yon-referans.md` §5). Şu an elimizdeki her raster
   katalog türevi → bunlarla üretilen her şey **taslaktır**; künyeye ve dosya
   adına `taslak` yaz. Ofis orijinali (`Mimari-Ofis-Talep-Listesi.md`) gelince
   aynı senaryo yeniden çalıştırılır.
4. **Uydurma yok.** Prompt'a olmayan manzara, peyzaj, malzeme; ekrana fiyat,
   teslim, mesafe, "yükseliyor" yazılmaz. İnsan varsa arkadan (K6); yapay
   figür gerçek sakin gibi sunulmaz.
5. **Anahtarlar** `~/.config/fal/key` ve `~/.config/elevenlabs/key` (600) ya da
   `FAL_KEY` / `ELEVENLABS_API_KEY`; depoya, sohbete,
   commit'e, künyeye girmez. Sohbette düz metin paylaşıldıysa söyle, fal
   panelinden yenilenmesini iste, öyle kullan.
6. **Para harcamadan önce maliyet.** `kling_video.py maliyet` ya da `--kuru`;
   ilk deneme `taslak` katmanında (5 sn ≈ $0,21), yayın `v3-pro` (≈ $0,56).

## Kurulum

```bash
mkdir -p ~/.config/fal && printf '%s' 'KEY_ID:KEY_SECRET' > ~/.config/fal/key && chmod 600 ~/.config/fal/key
python3 scripts/kling_video.py modeller     # bağlantı gerekmez; tabloyu basar
```

Ek paket yok: betikler standart kütüphane + Pillow (kurulu) + ffmpeg.
Fontlar `gorsel-uretim` ile ortak (Cormorant Garamond kurulu değilse Didot'ya düşer;
kurulum komutu o skill'de).

## İş akışı — tek komut

```bash
python3 scripts/uretim.py "Sosyal Medya Çıktıları/video/2026-09/senaryolar/S3-altta-sehir-ustte-huzur.json"
python3 scripts/uretim.py senaryo.json --taslak      # fal anahtarı yokken: Ken Burns klipleri
python3 scripts/uretim.py senaryo.json --adim ses    # tek aşama; çıktısı olan aşama atlanır
```

`hazirla → klipler (Kling toplu | taslak Ken Burns) → ses (ElevenLabs parçalı,
çekime hizalı + ambiyans) → altyazi → katman (ekran metinleri, logo kartı) →
montaj (bitir.py) → paket (kapak, açıklama+beyan, qc)`. Çıktı
`cikti_dizini/<ad>.mp4`, `kapak.png`, `aciklama.txt`, `<ad>.mp4.qc.json`.
Kling varyantları izlenip `secim` yazılmadan 1. varyant kullanılır — göz seçer.
Hazır dört senaryo: `Sosyal Medya Çıktıları/video/2026-09/senaryolar/`.

## Akış — aşamalar tek tek

### 0. Görseli oku, senaryoyu yaz

Görseli aç, `senaryo-sablonlari.md` §1'deki beş soruyu cevapla, uygun şablonu
seç (§3), `senaryo.json` yaz (`scripts/senaryo-ornek.json` örnek). Her çekim
için prompt `prompt-rehberi.md` §6'dan başlar; kurallar: tek kamera hareketi,
hız sözcüğü, en az iki sabitleyici ifade, kamera cümlesi en sonda, İngilizce.
Ekran metni ve açıklama Türkçe, `ton-ve-dil.md` sözlüğünden.

Kullanıcıya senaryoyu **üretimden önce** göster: çekim listesi, prompt'lar,
tahmini ücret, hangi kaynak görselin taslak sayıldığı.

### 1. Görseli hazırla

```bash
python3 scripts/hazirla.py cephe.jpg --oran 9:16 --odak center --out kaynak/cephe-9x16.jpg
```

Kling oranı **girdi görselinden** alır; 9:16 istiyorsan önce kırp. Betik sRGB'ye
çevirir, EXIF'i atar, kısa kenar/oran/boyut sınırlarını denetler. Kısa kenar
< 1.080 uyarısı gelirse üretim yine olur ama yumuşak çıkar — künyeye yaz.
Gündüz render'ı geldiyse önce `gorsel-uretim/scripts/aksam.py` (K1).

### 2. Üret

```bash
python3 scripts/kling_video.py maliyet senaryo.json            # önce ücret
python3 scripts/kling_video.py toplu senaryo.json --kuru       # istek gövdeleri
python3 scripts/kling_video.py toplu senaryo.json              # gönder, bekle, indir
```

Tek klip:

```bash
python3 scripts/kling_video.py uret --gorsel kaynak/cephe-9x16.jpg \
  --prompt "The building stays perfectly still and rigid ... slow push-in ..., then settles." \
  --model v3-pro --sure 5 --out cikti/cephe-yaklasma-1.mp4
```

Klip başına 2–6 dk. `--arka-plan` ile gönderip çık, `sonuc <request_id> --out …`
ile sonra al. Her klibin yanına `.json` künye (kaynak, prompt, model, request_id,
ücret) ve dizine `uretim-gunlugu.jsonl` yazılır. Kling seed vermiyor; `tekrar: 2`
ile iki varyant üret, iyisini seç (`prompt-rehberi.md` §7 ölçütleri).

Model seçimi: `v3-pro` varsayılan · `taslak` (v2.5-turbo standard) deneme ·
`ekonomik` (v2.5-turbo pro) bütçe · `o3-pro`/`o1` ilk+son kare kontrolü ·
`v3-4k` web hero. Tablo: `kling_video.py modeller`.

### 3. Marka katmanı

```bash
python3 scripts/katman.py --preset cross-9x16 --baslik "Ay taşının zarafeti, yaşamın en değerli hali" --out katman.png
python3 scripts/katman.py --preset cross-9x16 --tek-kelime "Prestij" --out katman.png
python3 scripts/katman.py --preset cross-9x16 --sadece-logo --out logo-kart.png
```

Şeffaf PNG: alt degrade (K3), Cormorant tek satır başlık alt üçte birde (K5),
logo sol üst, "Temsili görseldir" sağ altta; `cross-9x16` güvenli alanı
Instagram + TikTok'u tek sürümle kurtarır. `--guides` ile denetle.

### 4. Montaj

```bash
python3 scripts/bitir.py cikti/01-crane-inis-1.mp4 cikti/02-yaklasma-2.mp4 --preset reels \
  --katman katman.png --katman-baslangic 5 --kapanis logo-kart.png --bekle 1 \
  --muzik ambiyans.mp3 --platform instagram --out 01-marka-acilisi.mp4
```

Zincir: kırp/`--doldur bulanik` (siyah bant yerine bulanık kendi-dolgu) → `setsar`,
`fps=30`, `settb=AVTB` → xfade (ofset zincir üzerinden birikir) → `--bekle` →
katman (`enable` aralığı + alfa fade) → kapanış kartı **gövdeden sonra** → iki
geçişli loudnorm (Instagram −16 / YouTube-TikTok −14) → **libx264 crf 17 High
4.2** (Instagram yeniden kodlar; temiz kaynak kazanır) → bt709 etiketi →
QC (`akış hatasız`, süre ±0,3 sn, ölçü, `.qc.json`). `--hizli` VideoToolbox
önizleme; Instagram'a HEVC verilmez.

PNG/JPG girdi verilirse Ken Burns klibi olur (kat planı, eskiz): 2× çalışma
tuvali, en fazla %6 zoom / 9 sn, `--kb yukari,uzaklas` hareket listesi.
Denetim modları: `--guvenli-alan` (UI bantları kırmızı), `--dongu-kontrol`
(dikiş), `--kapak 1.0` (kapak karesi), `--son-kare` (zincirleme), `--dongu-xfade`
(kesintisiz döngü), `--derece` (kimlik derecelendirme dizesi).
Gerekçeler: `references/post-produksiyon.md` §1b.

### 4b. Seslendirme (yalnızca bilgi taşıyan içerikte)

```bash
python3 scripts/seslendir.py okunus "Tip 5, 3+1, net 96,54 m²."          # ne söyleneceğini gör
python3 scripts/seslendir.py uret "…" --ses bill --out vo.wav             # WAV + kelime zamanlaması
python3 scripts/altyazi.py vo.zamanlama.json --out-dir alt --baslangic 0.6 --toplam 15
python3 scripts/bitir.py … --seslendirme vo.wav --altyazi alt/altyazi.txt --muzik yatak.mp3
```

ElevenLabs `eleven_multilingual_v2`, anahtar `~/.config/elevenlabs/key`.
**Metin doğal ve jenerik:** rakam ve spec ekranda kalır, ses hissi taşır
("kimse metrekare demez"). Tonlama `--ton sakin|sicak|kanca` (stability/style/
speed) + noktalama + `<break time="0.4s" />`; `parcali` her çekime kendi tonuyla
ayrı sentez yapar. Sayı kaçınılmazsa yazıyla söylenir (`426 km` ölçülmüş felaket). Ses seçimi marka kararı: `deneme` ile 3–4 ses üret, Çise
Hanım seçsin. Mimari/yaşam Reels'i sessiz kalır (K8); seslendirme rehber,
süreç ve tip tanıtımı içindir. Açıklamaya `Seslendirme yapay zekâ ile
üretilmiştir.` Ayrıntı: `references/seslendirme.md`.

### 5. Kontrol ve teslim

`senaryo-sablonlari.md` §5 listesi. Teslimde: MP4 + açıklama metni + alt
metin + etiketler + künye. Her teslimden sonra "bunu daha iyi yapan şey" notu
— genelde cevap "mimari ofisten dikey akşam render'ı".

## Hangi durumda ne

| Durum | Yap |
|---|---|
| Cephe render'ı, akşam | Ş1/Ş2: crane iniş + push-in; sabit kamera ışık değişimi en güvenli |
| Cephe render'ı, gündüz | Önce `aksam.py`; ya da sabit kamera + "sky darkens, windows warm up" |
| Yatay render, dikey isteniyor | `hazirla.py --odak`; %60+ kayıp varsa ofisten dikey iste, üretme |
| Kat planı | AI değil, `bitir.py`/ffmpeg zoompan Ken Burns — Kling çizgiyi titretir |
| Havuz / iç mekân | Sabit kamera + su/perde/ışık hareketi; yaklaşma ikinci çekim |
| Spor salonu, hamam (`gecici-gorsel`) | Proje render'ı olduğu doğrulanmadan **üretme** |
| Kesin kamera yolu | Ofisten iki açı iste → `--bitis-gorsel` ile o3-pro/o1 |
| 15 sn+ tek plan | v3 `multi_prompt` (`--ekstra`) ya da son-kare zinciri; 10 sn tek klip kaymaya açık |
| Prompt tutmuyor | cfg 0,6–0,7; fazla hareket → 0,3–0,4; hâlâ olmuyorsa Veo 3.1 Fast ile A/B |

## Devir teslim

- **moonstone-residence** — K1–K8 kuralları, ton, veriler; çakışmada o kazanır.
- **gorsel-uretim** — `aksam.py` (gündüz→mavi saat), `frame.py` (fontlar, logo;
  `katman.py` bunu ithal eder), `grade.swift` (renk eşleme).
- **pexels-gorsel-bulucu** — ara kesit/b-roll stok video; proje yerine geçemez.

## Referans

- `references/fal-kling-api.md` — uç noktalar, alan adları, fiyat, kuyruk, hata, yardımcı modeller.
- `references/prompt-rehberi.md` — kamera sözlüğü, sabitleyiciler, negatif, 14 hazır prompt.
- `references/senaryo-sablonlari.md` — görsel okuma, senaryo.json, 10 şablon, kontrol listesi.
- `references/seslendirme.md` — ElevenLabs mekaniği, ses seçimi, ölçülmüş okunuş kuralları, konuşulan Türkçe, altyazı, miks, beyan.
- `references/post-produksiyon.md` — montaj zinciri, weftrecords/reelsindustry'den devralınan ölçülmüş kalıplar (§1b), alternatif modeller, hukuk.
