# Sektör Hattı — Bizimkiyle Karşılaştırma

AI destekli kısa video üretim hatlarının 2026'da nasıl kurulduğuna dair
araştırma, ve bizim hattımızın nerede durduğu. Amaç kopyalamak değil: neyin
bizde eksik olduğunu, neyin bize gerekmediğini ayırmak.

## İçindekiler
1. Standart hat şekli
2. Motion graphics: Remotion mu ffmpeg mi
3. Bizde olan / olmayan
4. Uyarlananlar
5. Bilerek almadıklarımız

---

## 1. Standart hat şekli

Bu alandaki hemen her proje aynı yedi adımı kuruyor:

```
Konu → LLM senaryo → TTS seslendirme → stok görsel eşleme
     → ALTYAZI → montaj (ffmpeg) → yayın
```

Yaygın yığın: **Claude/GPT** senaryo · **ElevenLabs** ses · **Pexels** stok ·
**Whisper/WhisperX** kelime zamanlaması · **ffmpeg** ya da **Remotion** montaj.
Orkestrasyon ya kod (Python/Node) ya da **n8n / Make** gibi düğüm tabanlı
araçlarla yapılıyor; hazır video API'leri (**Shotstack**, **Creatomate**)
montaj adımını dışarı veriyor.

Örnek projeler: `sumanreddy89/flow-youtube-faceless` (Claude + ElevenLabs +
Pexels + ffmpeg), `hassancs91/claude-faceless-shorts-creator` (Claude Code +
Remotion TSX + ElevenLabs + kelime-tam altyazı).

**Yaygın optimizasyon:** seslendirme üretilirken stok görseller paralel
indiriliyor.

## 2. Motion graphics: Remotion mu ffmpeg mi

**Remotion** React ile video yazmayı sağlıyor: bileşenler sahne oluyor,
`useCurrentFrame()` ve `interpolate()` ile animasyon kuruluyor, headless
Chromium her kareyi ekran görüntüsü alarak render ediyor. Tarayıcıda çalışan
her şey — CSS, SVG, web fontu — videoda çalışıyor.

**Maliyeti ağır.** Render süresi kare sayısı × piksel × React ağacının iş
yükü. Ölçülmüş bir örnek: 1080p 30 fps, 2 dakikalık 3×3 ızgara video, güçlü
bir makinede **15 dakikadan fazla**.

Bizim hat aynı işi başka türlü yapıyor: tipografi Pillow'da rasterleniyor,
ffmpeg yalnızca `overlay` yapıyor. **16 saniyelik bir Reels ~5,5 saniyede
render oluyor.**

| | Remotion | Bizim hat |
|---|---|---|
| Animasyon esnekliği | Çok yüksek (CSS/SVG/JS) | Orta (zoompan, xfade, fade, overlay) |
| Render hızı | Dakikalar | Saniyeler |
| Marka sistemi | React'te yeniden kurulur | `frame.py` zaten kurulu |
| Bağımlılık | Node + Chromium | Yok (Pillow + ffmpeg) |

**Karar: Remotion'a geçmiyoruz.** Bizim iş hacmimizde hız ve mevcut marka
altyapısı ağır basıyor. Ama sınır net: **karmaşık kinetik tipografi, veri
animasyonu ya da 3B benzeri sahneler gerekirse doğru araç Remotion.** O gün
gelirse bu dosyayı güncelle.

## 3. Bizde olan / olmayan

| Adım | Sektör | Bizde |
|---|---|---|
| Senaryo | LLM | ✓ marka kurallarına bağlı, `seslendirme-metni.md` |
| Seslendirme | ElevenLabs | ✓ + **ölçüm kapısı** (sektörde yok) |
| Türkçe okunuş düzeltme | — | ✓ (sektörde İngilizce odaklı, bu bize özgü) |
| Stok görsel | Pexels | ✓ + **hak denetimi ve kırmızı çizgi** |
| Müzik | telifli/AI servis | ✓ **prosedürel**, üçüncü taraf hakkı yok |
| **Altyazı** | Whisper kelime zamanı | **YOKTU → eklendi** |
| Montaj | ffmpeg / Remotion | ✓ ffmpeg, PNG bindirmeli |
| Yayın | API ile otomatik | ✗ elle |

## 4. Uyarlananlar

### Karaoke altyazı (`scripts/altyazi.py`)

En büyük eksikti. Sosyal videoların büyük çoğunluğu **sessiz** izleniyor;
altyazı tek başına en yüksek getirili ekleme.

Kelime zamanlaması zaten elimizdeydi — `soz_olcum.py` ASR denetimi için
ElevenLabs Scribe kullanıyor ve Scribe kelime bazlı zaman damgası döndürüyor.
Ayrı bir Whisper kurmaya gerek kalmadı.

Yöntem (ffmpeg'de `subtitles` olmadığı için): her **kelime durumu** için bir
alfa PNG rasterlenir, `concat` demuxer'ıyla **süreli görüntü dizisi** olarak
doğrudan ana filtre grafiğine girer. Ara dosya encode'u yok.

Öbekleme: en çok 4 kelime, en çok 2,2 sn, noktalamada ve 0,45 sn'den uzun
sessizlikte (nefes) kırılır.

```json
"altyazi": {"gecikme": 0.8, "boy": 44, "y": 1010}
```

**İki tuzak, ikisi de yaşandı:**

1. **Süreleri toplama, mutlak zamana bağla.** İlk sürümde her karenin süresi
   `bit − baş` olarak arka arkaya eklendi; kelimeler *arasındaki* boşluklar
   sayılmadığı için altyazı giderek sesin önüne geçti ve 8. saniyede bitti.
   Doğrusu: her olay kendi mutlak başlangıcına konur, süre bir sonraki olayın
   başlangıcından çıkarılır.
2. **`concat` demuxer son girdinin `duration` satırını yok sayar.** Son dosya
   bir kez daha `file` satırıyla tekrarlanmazsa son kare bir frame görünüp
   kayboluyor.

### Kinetik tipografi ilkesi

Araştırmanın kendi uyarısı: hareket **açıklığı artırıyorsa** güçlendirir,
yalnızca süsse rekabet eder. Metnin okunur kalması için aynı anda çok şey
hareket etmemeli ve göz okuyacak zamanı bulmalı. Ritim, **sesin veya müziğin
vuruşuna** oturmalı — bizde plakaların zamanlaması seslendirmeye göre
ayarlanıyor, altyazı ise kelime zamanına kilitli.

## 5. Bilerek almadıklarımız

- **Remotion** — bölüm 2. Hız ve mevcut marka altyapısı ağır bastı.
- **n8n / Make** — barındırılan bir bağımlılık ekliyor; betiklerimiz zaten
  çalışıyor ve depoda sürümleniyor.
- **Shotstack / Creatomate** — montajı dışarı vermek marka denetimini de
  dışarı vermek olurdu; `frame.py` kontrast ve güvenli alan denetimi yapıyor.
- **Otomatik yayın** — konut reklamında her kare insan onayından geçmeli.
  Mevzuat riski otomasyon kolaylığından ağır basıyor.
- **Trend konu API'si** — bu bir marka hesabı, trend kovalamıyor.
