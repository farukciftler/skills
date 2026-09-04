# Reels — Seslendirme, Altyazı, Video

Motor katmanı `src/icerik/` altındadır; ayrıntılı API için `src/icerik/README.md`.
Bu dosya **skill'in kullandığı akışı** anlatır.

## Tek komut

```bash
.venv-icerik/bin/python .claude/skills/kartela-icerik/reels.py brif.json
```

## Yapı — gövde video, kapanış statik

**Gövde gerçek videodur.** Pexels'ten inen dikey stok klipleri, markanın
duotone'uyla işlenmiş ve **sessizleştirilmiş** hâlde.
**Yalnızca kapanış karesi statiktir** — marka şablonuyla render edilen, logo,
tam ruhsat adı, karekod ve çağrı taşıyan kart.

Mesaj **yakılmış altyazıyla** taşınır; video kliplerinin üzerine ayrıca başlık
basılmaz. Instagram videoları sessiz izlenir, altyazı zaten zorunlu — ikinci
bir metin katmanı görüntüyü kalabalıklaştırır.

### Klip havuzu

```bash
python3 src/gorsel/video_indir.py --kategori hepsi --adet 5
```

Kategoriler: `mekan` · `atolye` · `doga` · `malzeme`.
Klipler `data/video/` altına iner, `MANIFEST.json` kaydeder.

**LİSANS — bağlayıcı:** Pexels Lisansı klibin **ses yatağını kapsamaz.**
`klip.py` her klibi `-an` ile sessizleştirir; ses yalnızca kendi
seslendirmemizden gelir. Tanınabilir kişiler için model izni garanti edilmez;
kadrajdaki logo ve marka ayrı haklara tabidir. Her üretim `KUNYE.md` yazar.

## Brif

```json
{
  "slug": "oyun-gruplari",
  "ruhsat_adi": "Özel Kartela Rehberlik ve Psikolojik Danışma Merkezi",
  "karekod_url": "https://kartelapsikoloji.com/kurumsal-bilgi",
  "seslendirme": "Anlatım metni. Türkçe, sakin, iddiasız.",

  "klipler": [
    { "kategori": "mekan", "sira": 0, "baslangic": 1, "sure": 5, "duotone": "petrol" },
    { "kategori": "doga",  "sira": 2, "baslangic": 2, "sure": 5, "duotone": "mavi" }
  ],

  "kapanis": {
    "zemin": "z-nane", "gorsel": "…", "yerlesim": "alt", "sure": 5,
    "etiket": "…", "baslik": "…", "altmetin": "…",
    "eylem": "Sormak için yazmanız yeterli."
  }
}
```

`baslangic` kaynağın kaçıncı saniyesinden başlanacağı — stok kliplerin ilk
saniyeleri genellikle en zayıf kadrajdır. `dosya` verilirse manifest yerine
doğrudan o dosya kullanılır.

**Kapanış karesi zorunludur.** Karekod ve ruhsat adı orada taşınır; olmadan
denetim engelleyici verir (ÖÖK Yön. Ek m.4/2 + m.7/4).

## Akış

1. **Denetim** — kapanış karesi metni + seslendirme metni ayrı ayrı.
   Sesli içerik de tanıtımdır; aynı yasaklar geçerlidir.
2. **Gövde** — stok klipler 1080×1920 · 30 fps · duotone · **sessiz** hâle getirilir
3. **Kapanış** — marka şablonu → PNG → sabit klip
4. **Birleştirme** — `xfade`, geçiş 0,5 sn (marka kuralı: 0,4–0,6 aralığına kırpılır)
5. **Seslendirme** — edge-tts, gerçek kelime zamanlaması
6. **Ses bindirme** — seslendirme videodan kısaysa **sessizlikle doldurulur**;
   kapanış karesi ekranda kalır (izleyici karekodu okusun diye)
7. **Altyazı** — yakılmış (burned-in)
8. **Doğrulama** + güvenli alan + döngü kontrol dosyaları

## Videoda duotone

Fotoğraflardaki ile **birebir aynı renk uçları**, ffmpeg ile:
BT.709 luminansıyla gri tonlama (`colorchannelmixer`) → gradient map (`lutrgb`).

```
colorchannelmixer=0.2126:0.7152:0.0722:0:… , lutrgb=r='koyu+fark*val/255':…
```

`yumusak` duotone değildir — gerçek kurum çekimi için doygunluk düşürme.

## Seslendirme

## KARAR — ses `tr-TR-EmelNeural` **[B]**

**Kurucu, ses örneklerini dinleyerek `tr-TR-EmelNeural`'ı seçti**
(23 Ağustos 2026). Türkçe fonetiği iyi bulundu. Bu ses **varsayılandır ve
değiştirilmez**; alternatif motorlar yalnızca yedek ve lisans yolu meselesidir.

Kritik nokta: **Azure anahtarı alınması bu kararı bozmaz.** Azure *aynı Emel
sesini* sunar — yalnızca hukuken temiz bir kanaldan. Ses değişmez, yalnızca
lisans belirsizliği ortadan kalkar.

---

**Motor zinciri: `azure` (anahtar varsa) → `edge` → `supertonic` → `say`.**

Ölçüm yöntemi: ASR geri-dönüş testi (üret → Whisper ile deşifre et → özgün
metinle karşılaştır). "Fonetik WER" ı/i, ğ, ö/ü yüklü cümlelerde.

| Motor / ses | Fonetik WER | Zamanlama | Ticari lisans |
|---|---|---|---|
| **edge `tr-TR-EmelNeural`** | **%0** | gerçek (WordBoundary) | ⚠️ **belirsiz** |
| edge `tr-TR-AhmetNeural` | %0 | gerçek | ⚠️ belirsiz |
| **supertonic `F5`** | **%0** | Whisper hizalama | ✅ MIT + OpenRAIL-M |
| macOS `say` Yelda | %6,7 | Whisper hizalama | ✅ |
| ~~piper `tr_TR-dfki`~~ | — | — | ❌ **CC-BY-NC-SA** |
| edge çok dilli sesler | **%100** | gerçek | ⚠️ |

### İki lisans sorunu — ikisi de çözüldü

**1. `piper` ticari kullanıma KAPALI.** `tr_TR-dfki-medium` veri seti
CC-BY-NC-SA-4.0. Ruhsatlı bir kurumun tanıtım videosunda **kullanılamaz**.
Zincirden çıkarıldı; yerine `supertonic` geldi (MIT, çevrimdışı, %0 hata,
385 MB). Açıkça `--motor piper` denirse hâlâ çalışır — kullanmayın.

**2. `edge-tts` ticari kullanımı belirsiz.** Geliştiricisinin ifadesi:
*"This library is meant for personal use"*. Microsoft'un yayımlanmış izni yok.

**Çözüm — Azure ücretsiz F0 anahtarı.** `AZURE_SPEECH_KEY` ve
`AZURE_SPEECH_REGION` tanımlandığı anda zincir kendiliğinden oraya geçer,
kodda değişiklik gerekmez. **Aylık 500.000 karakter ücretsiz** — bizim
hacmimiz (~50.000/ay) kotanın onda biri. Aynı Emel sesi, hukuken temiz.

### Çok dilli sesler Türkçe konuşamıyor

Azure dokümanı `en-US-AvaMultilingualNeural` gibi seslerin tr-TR desteklediğini
söylüyor; **test bunu çürüttü.** "Yağmurluğunu giy" → *"Jagmer Lagunu Jai"*.
Türkçe imlayı Almanca/İngilizce fonetiğiyle okuyorlar. Uluslararası kelimeler
düzgün çıktığı için yüzeysel denemede iyi sanılabilir — **kullanmayın.**

### Kelime zamanlaması

Zamanlama vermeyen motorlarda (`supertonic`, `say`) faster-whisper ile
zorlanmış hizalama yapılır. Ölçülen doğruluk: ortalama **66 ms** sapma,
kelimelerin %82'si <100 ms. Reels altyazısı için fazlasıyla yeterli.
`small` modeli `large-v3`'ten daha isabetli (bilinen zaman damgası kayması).

Rapor sözlüğünde `zamanlama_kaynagi` alanı hangi yolun kullanıldığını söyler.
`tahmini: true` çıkarsa altyazı senkronu yayına gitmeden gözle kontrol edilir.

### Denenmemiş güçlü aday

`tr-TR-Elif:MAI-Voice-2` — Azure'un yeni sesi, `caring · empathy ·
encouraging · reflective` stillerini destekliyor. Kaygılı bir veliye hitap
eden marka tonunun aradığı register tam bu. **Anahtar olmadığı için test
edilemedi.** Anahtar geldiğinde ilk denenecek şey budur.

Ses **−16 LUFS**'a normalize edilir (konuşma standardı; müzik −14).

**Türkçe metin yazarken:** kısaltma kullanma ("RPDM" değil tam ad), rakamları
yazıyla yaz ("20-28 ay" yerine "yirmi ile yirmi sekiz ay" daha doğru okunur),
noktalama koy — altyazı bölünmesi noktalamaya bağlıdır.

## Altyazı — zorunludur

Instagram videoları büyük ölçüde **sessiz izlenir**. Altyazısız Reels üretilmez.

**Teknik not:** bu makinedeki ffmpeg'de `drawtext`, `subtitles` ve `ass`
filtreleri **yok** (Homebrew derlemesi libass/libfreetype'sız). Altyazı bu
yüzden Playwright'ta marka fontuyla dizilip saydam PNG olarak zamanlı
`overlay=…:enable='between(t,a,b)'` ile yakılır. Yan fayda gerçek: Türkçe
diakritikler ve marka tipografisi tam kontrolde.

Stil: beyaz `#FFFFFF` metin, petrol `#005F7F` %92 opak kutu — kontrast 7,13:1.

Bölme kuralı: cümle sonu (`. ! ? : ;`) **her zaman** böler; virgül en az iki
kelime birikmişse böler.

## Arka plan müziği — prosedürel

**Her Reels'te arka plan müziği vardır ve prosedürel üretilir.**
`src/icerik/muzik.py`, numpy ile toplamsal sentez.

### Neden prosedürel

Stok müzik ve AI müzik servisleri (Suno vb.) telif, lisans ve "yapay zekâ
üretimi beyanı" sorunları taşır. Ruhsatlı bir kurumun tanıtım materyalinde bu
riskler gereksizdir. **Prosedürel üretimde üçüncü taraf hakkı yoktur** —
dalga formu koddaki matematikle doğar. Tohum verildiği için aynı brif her
zaman aynı müziği üretir.

### Müzikal kararlar — hepsi marka kuralına bağlı

| Karar | Gerekçe |
|---|---|
| **Dor modu** (varsayılan) | Minör üçlü sıcak ve düşünceli; yükseltilmiş altılı Aeolian'ın melankolisini kırar. Ne hüzünlü ne satış diline kaçan parlaklıkta. |
| **Vurmalı YOK** | Ritim aciliyet üretir; marka sesi aciliyet dilini yasaklar (§7.2). Nabız yoksa dinleyici sıkıştırılmaz. |
| **Akor başına 8–12 sn** | Bir cümle boyunca müzikte "olay" olmaz; dikkat konuşmada kalır. |
| **Pes kök (55–110 Hz)** | Konuşma temel frekansının (Emel ≈ 207 Hz) altında kalır, maskelemez. |
| **1–3 kHz oyulur** (−6 dB) | Ünsüz anlaşılabilirliğinin yaşadığı bant. Ölçüldü: konuşma bandı, müziğin gövdesinin **45 dB altında**. |
| **3–4 sn atak, uzun kuyruk** | İrkiltici hiçbir olay olmaz. |

### Brifte kullanımı

```json
"muzik": true,                                    // varsayılan — prosedürel
"muzik": false,                                   // müziksiz
"muzik": { "kok": "F2", "mod": "lidyen", "tohum": 7 },
"muzik": "data/muzik/hazir.wav",                  // ⚠️ telifi AYRICA denetlenmeli
"muzik_seviye": -18                               // dB, konuşmaya göre
```

Modlar: `dor` (varsayılan) · `aeol` (daha hüzünlü) · `lidyen` (umutlu) ·
`pentatonik` (en yumuşak, çelişkisiz).

Tohum verilmezse **slug'dan türetilir** — aynı içerik her zaman aynı müziği alır.

### Seviye

Modül varsayılanı −24 dB konuşmanın 22 dB altına düşürüyordu; telefon
hoparlöründe duyulmuyordu. **−18 dB** varsayılan yapıldı: ölçülen ayrım
16 dB — fark edilir bir yatak, ünsüzleri örtmez.

Bu **dinleyerek ayarlanacak** bir değerdir; `muzik_seviye` ile değiştirilir.

### Ölçülen denge (örnek üretim)

| Ne | Seviye |
|---|---|
| Genel | −16,2 LUFS (Instagram konuşma standardı) |
| Konuşma bölümleri | −20,3 dB |
| Konuşma boşlukları (yalnız müzik) | −36,6 dB |

## Encode

**Varsayılan `libx264 -crf 18 -preset fast`.** Ölçüm VideoToolbox'ı çürüttü:

| Kodlayıcı | Uçtan uca | Dosya | Bit hızı |
|---|---|---|---|
| **libx264** | **26,2 sn** | **2,6 MB** | **1,07 Mbit/sn** |
| h264_videotoolbox | 27,4 sn | 12,7 MB | 5,31 Mbit/sn |

Donanım kodlayıcı bu iş yükünde hızlı bile değil (darboğaz PNG/Chromium) ve
4,9× büyük. Ayrıca koyu, yavaş gradyanlı sahnelerde **bantlıyor** — Kartela'nın
mat paleti tam bu risk sınıfı. `kodlayici='onizleme'` VideoToolbox'a geçer.

Çıktı: 1080×1920 · 30 fps · yuv420p · bt709 · AAC 48 kHz stereo · `+faststart`.

## Güvenli alan — bir mevzuat hatası yakalandı

Instagram arayüzü **üst 200 px, alt 480 px, yan 100 px**'i örtebilir.

İlk sürümde karekod ve ruhsat adı alttan 150 px'teydi — yani **görünmeyen**
bir karekod. Görünmeyen karekod ÖÖK Yön. Ek m.4/2 açısından yok hükmündedir.
Künye 720 px'e, altyazı 520 px'e taşındı.

**Her Reels'te `kontrol-guvenli-alan.mp4` gözle kontrol edilir.** Kırmızı
alandaki hiçbir şeye güvenilmez. Bu dosya **yayınlanmaz**, atılır.

## Döngü

`kontrol-dongu.mp4` klibi kendine ekler; orta noktadaki dikişe bakılır.
Görünür bir sıçrama varsa ya son kare ilk kareye yaklaştırılır ya da net bir
bitişe geçilir. **Çapraz geçişle düzeltilmez** — kurgu hatası gibi okunur.

## Kontrol listesi

- [ ] Seslendirme metni denetimden geçti
- [ ] Altyazı var ve senkron (`tahmini: true` değilse)
- [ ] Karekod güvenli alanın **içinde** ve okunuyor
- [ ] Ruhsat adı tam — kısaltma değil
- [ ] Süre 15–60 sn
- [ ] `dogrula` → `uygun: true`
- [ ] `kontrol-guvenli-alan.mp4` gözle bakıldı
- [ ] Arka müzik kullanıldıysa **telif durumu ayrıca denetlendi** (modül lisans kontrolü yapmaz)
