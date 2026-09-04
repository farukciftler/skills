# Donanım ve Araçlar

Bu skill'deki araç seçimleri bu makineye göre yapıldı. Makine değişirse
bu dosya güncellenmeli — özellikle Apple Silicon dışı bir makinede Core Image
ve VideoToolbox tavsiyeleri geçersizdir.

## Makine profili

| | |
|---|---|
| Model | MacBook Pro (Mac16,7) |
| Yonga | **Apple M4 Pro** |
| CPU | 14 çekirdek — 10 performans + 4 verim |
| GPU | 20 çekirdek, Metal 4 |
| Bellek | 24 GB birleşik |
| Disk | ~120 GB boş |
| İşletim sistemi | macOS (Darwin 25.5) |

Birleşik bellek şu yüzden önemli: CPU ile GPU arasında piksel kopyalama
maliyeti yok. Core Image üzerinden GPU'ya iş vermek küçük görsellerde bile
mantıklı; ayrık GPU'lu bir makinede aynı şey kopyalama maliyetinden dolayı
zarar ederdi.

## Kurulu araçlar

| Araç | Yol | Kullanım |
|---|---|---|
| `sips` | `/usr/bin/sips` | Ölçekleme, format çevirme, ICC. **AVIF yazabiliyor.** |
| `ffmpeg` / `ffprobe` | `/opt/homebrew/bin` | Video; `h264_videotoolbox`, `hevc_videotoolbox`, `prores_videotoolbox`, `libsvtav1`, `libx264` |
| `cwebp` | `/opt/homebrew/bin` | WebP yazma (sips WebP'yi yalnızca okuyor) |
| `rsvg-convert` | `/opt/homebrew/bin` | SVG → PNG; marka logoları ve ikon seti |
| `swift` / `swiftc` | `/usr/bin` | Core Image betikleri |
| Python 3 + Pillow 11.3 + NumPy 2.0 | `/usr/bin/python3` | `frame.py` |
| `node` | `/opt/homebrew/bin` | Gerekirse |
| `brew` | Homebrew 6.0.18 | Kurulum |

## Kurulu olmayanlar ve gerekip gerekmediği

| Araç | Gerekli mi | Not |
|---|---|---|
| ImageMagick | **Hayır** | Yaptığı işi sips + Pillow + Core Image karşılıyor |
| libvips | Şimdilik hayır | Binlerce dosyalık toplu işe çıkılırsa `brew install vips` en büyük hız kazancını verir |
| `avifenc` | **Hayır** | sips AVIF yazıyor |
| `exiftool` | Hayır | Meta veri denetimi gerekirse `brew install exiftool` |
| `pngquant` / `oxipng` | Hayır | PNG boyutu sorun olursa faydalı |
| OpenCV, scikit-image | Hayır | Akıllı kırpma/yüz algılama gerekirse Vision framework (Swift) daha uygun |

**Fontlar:** Cormorant Garamond ve Lora kurulu değil. Sistemde **Didot**,
Baskerville, Hoefler Text, Georgia, Times New Roman var. `frame.py` display
için Didot'ya, gövde için Georgia'ya düşüyor — ikisi de yüksek kaliteli
serif ve markaya yakın duruyor, ama birebir değil. Kurulum komutu SKILL.md'de.

## Ölçülmüş süreler

Bu makinede alınan gerçek değerler — başka bir makinede geçerli değil:

| İş | Süre |
|---|---|
| `swift grade.swift` tek 1200 px görsel (yorumlayıcı başlatma dahil) | ~0,8 sn |
| Aynı iş `swiftc -O` ile derlenmiş ikili | başlatma maliyeti ~0,02 sn'ye düşer |
| `frame.py` tek 1080×1920 kare | ~0,3 sn |
| `rsvg-convert` logo SVG → PNG | ~0,05 sn (sonuç önbelleğe alınıyor) |

Derlemenin anlamı şu: **20 dosyanın altında `swift` yeterli, üstünde derle.**
Yorumlayıcı başlatma maliyeti dosya başına ödenir.

## Paralel iş kalıbı

Performans çekirdeği sayısını kullan, toplam çekirdeği değil:

```bash
JOBS=$(sysctl -n hw.perflevel0.logicalcpu)   # bu makinede 10
ls *.jpg | xargs -P "$JOBS" -I{} komut {}
```

Verim çekirdeklerini de işe katmak (`-P 14`) bu tür yükte toplam süreyi
iyileştirmiyor; iş dağıtım maliyeti kazancı yiyor. 24 GB bellekte 10 eşzamanlı
Pillow işi rahat sığar — 4K'dan büyük kaynaklarla çalışılıyorsa `-P 6`'ya
düşür.

## Video kodlama

```bash
# donanım kodlayıcı — hızlı, CPU'yu boşta bırakır
ffmpeg -i in.mp4 -c:v hevc_videotoolbox -q:v 60 -tag:v hvc1 out.mp4
ffmpeg -i in.mp4 -c:v h264_videotoolbox -b:v 8M out.mp4

# kalite öncelikliyse yazılım kodlayıcı
ffmpeg -i in.mp4 -c:v libx264 -crf 18 -preset slow out.mp4
```

Sosyal medya yüklenen videoyu zaten yeniden kodluyor; `hevc_videotoolbox`
ile `libx264 -crf 18` arasındaki fark yayında görünmüyor. Arşiv ya da
web'de doğrudan servis edilecek video için yazılım kodlayıcı tercih edilir.

Sesi atmak (Pexels klipleri için zorunlu):
`ffmpeg -i in.mp4 -an -c:v copy out.mp4`

## Renk yönetimi

Sosyal medya için her şey **sRGB** olmalı. Bu ekran Display P3 — Preview ya da
ekran görüntüsü üzerinden çalışılırsa geniş gamut kayabilir. `grade.swift`
çıktıyı açıkça sRGB'ye yazıyor. Dışarıdan gelen bir görselde şüphe varsa:

```bash
sips --matchTo /System/Library/ColorSync/Profiles/sRGB\ Profile.icc girdi.jpg --out cikti.jpg
```

## Nereye dikkat

- **Retina ekran yanıltır.** 1080 px'lik bir kare ekranda küçük görünür ama
  telefonda tam ekrandır. Punto kararını ekranda değil, preset ölçüsünde ver.
- **PNG mi JPEG mi:** düz renk ve tipografi ağırlıklı kare → PNG; fotoğraf
  ağırlıklı → JPEG kalite 92. Instagram her ikisini de yeniden sıkıştırıyor,
  ama kaynağı temiz vermek bandinge karşı fark yaratıyor.
- **sips ile ölçeklemede** `-Z` uzun kenarı hedefler, `-z h w` tam boyut verir
  (oran bozar). Kırpma gerekiyorsa `frame.py` kullan, `cover()` doğru yapıyor.
