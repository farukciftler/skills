# 2D piksel-art platformer karakteri — zanaat + hat

## İçindekiler
1. Zanaat kuralları (boyut, palet, zamanlama, pivot)
2. Dört kaynak yolu (A prosedürel · B AI MCP · C Aseprite · D 3D→piksel)
3. Spec şeması (pixel_character.py)
4. Sheet kontratı ve QA kapısı
5. Unity'de ne kurulur (klipler, state machine, prefab)
6. Özel animasyon eklemek

---

## 1. Zanaat kuralları

**Boyut önce, sanat sonra.** Karakter yüksekliği (px) oyunun tile boyutuna ve referans çözünürlüğüne bağlıdır; üretim başladıktan sonra değiştirmek her şeyi yeniden çizdirir.

| Tile / PPU | Tipik karakter boyu | Not |
|---|---|---|
| 16 px | 20–28 px | Celeste/Shovel Knight ölçeği, 320×180 referans |
| 32 px | 36–56 px | daha fazla detay, 640×360 referans |

- Hücre (frame) boyutu **çift sayı** olmalı; tek sayıda pivot yarım piksele düşer → titreme.
- Tüm animasyonlar **aynı hücre boyutunu** paylaşır (saldırı yayı dahil). `pixel_character.py` bunu `"frame": {"auto": true}` ile tüm pozların birleşik sınırından hesaplar.
- **Pivot = ayak tabanı**, x ortada. `baseline` = karakterin en alt pikselinin (outline dahil) altındaki boş satır sayısı. Unity pivot y = baseline / frameHeight.
- Karakter **sağa bakar**; sola dönüş runtime'da `SpriteRenderer.flipX` ile (pivot etrafında aynalanır). İki yön ayrı çizilmez.
- Palet: karakter başına 12–20 renk; tüm kareler **tek palet** paylaşır (kare başına palet titrer). Arka plandan ayrışması için 1px koyu outline.
- Yarı saydam piksel yok (0 veya 255). Yumuşak kenar Unity'de hale yapar.

**Zamanlama kare sayısından önemlidir.** Pikselde tipik aralık 8–12 fps; eşit süreli kareler en yaygın acemi hatası. Varsayılanlar (ms):

| Anim | Kare | Süreler | Not |
|---|---|---|---|
| idle | 4 | 260/160/260/160 | nefes: gövde 1px iner, ayak sabit |
| walk | 6 | 110×6 | |
| run | 8 | 75×8 | öne eğik, kollar bükük |
| jump_rise | 2 | 70/110 | itiş + yükseliş |
| jump_apex | 1 | 150 | tepe asılı kalır |
| fall | 2 (loop) | 120/120 | |
| land | 3 | 50/90/150 | çarpma / squash / toparlanma |
| attack | 5 | 90/70/**50**/110/130 | anticipation → **strike (smear + OnAttackHit)** → follow → recover |
| hurt | 2 | 80/180 | hızlı; uzun hurt karakteri ağırlaştırır |
| death | 6 | … / 600 | son kare tutulur, `OnDeathFinished` |

Zıplama fazları ayrı kliplerdir; fizik karakteri taşır, sprite sadece pozu gösterir. Havadaki klipler `grounded:false` — QA onlarda ayak-zemin kontrolü yapmaz.

## 2. Dört kaynak yolu — hepsi aynı sheet kontratında biter

| Yol | Ne zaman | Kalite / tutarlılık |
|---|---|---|
| **A Prosedürel** (`pixel_character.py`) | varsayılan; bağımlılık yok; düşman varyantları; blockout | okunaklı, %100 tutarlı, "indie-minimal" |
| **B AI MCP** (PixelLab / Retro Diffusion vb.) + `frames_to_sheet.py` | kullanıcı bağlıysa ve daha detaylı görünüm isteniyorsa | detaylı ama kareler arası sapma olur → temizleme şart |
| **C Aseprite** (`sheet_to_aseprite.lua`) | kullanıcı elle cilalayacaksa | en yüksek kalite (insan eli) |
| **D 3D→piksel** (`render_frames.py --mode pixel` + `frames_to_sheet.py`) | 3D karakter zaten varsa, çok animasyon, çok yön | tutarlılık mükemmel (Dead Cells tekniği), stil 3D'den gelir |

### A — Prosedürel
```bash
python scripts/pixel/pixel_character.py spec.json --out build/Ranger          # tümü
python scripts/pixel/pixel_character.py spec.json --out build/Ranger --anims attack   # hızlı iterasyon
python scripts/pixel/pixel_qa.py build/Ranger/Ranger_sheet.json
```
Çıktı: `Ranger_sheet.png`, `Ranger_sheet.json`, `preview/<anim>.gif` (6x, zemin çizgili), `preview/contact_sheet.png`. **Contact sheet'e mutlaka bak.** Poz sorunu → `poses_for()` tablosunu düzelt, pikseli elle yamama.

### B — AI MCP + temizleme
AI araçları: PixelLab MCP (`claude mcp add pixellab https://api.pixellab.ai/mcp -t http -H "Authorization: Bearer …"` — anahtar kullanıcıya ait; ücretli). Kareleri anim adıyla klasörle:
```
ai_out/knight/idle/00.png … ; ai_out/knight/run/00.png …
python scripts/pixel/frames_to_sheet.py --dir ai_out/knight --name Knight --out build/Knight --colors 16 --grid auto --outline
python scripts/pixel/pixel_qa.py build/Knight/Knight_sheet.json
```
`--grid auto` büyütülmüş "sahte piksel"i bulur (1–8x doğrulandı) ve blok **modu** rengiyle küçültür (ortalama yeni renk icat eder). `--palette palette.json` ile oyunun paletine kilitle. Rapordaki `notSnapped` satırları 2px'den büyük ayak kaymalarıdır — gizlenmez, kaynak kareyi yeniden ürettir.

### C — Aseprite köprüsü
```bash
aseprite -b --script-param sheet=Ranger_sheet.png --script-param meta=Ranger_sheet.json \
            --script-param out=Ranger.aseprite --script scripts/pixel/sheet_to_aseprite.lua
```
Anim başına bir tag, kare süreleri, loop (`repeats`), `event:OnAttackHit` cel user data. Unity'de `com.unity.2d.aseprite` → Import Mode **Animated Sprite**, Pivot Alignment **Custom** (x 0.5, y = baseline/h), PPU, Filter Point. İçe aktarıcının ürettiği Animator Controller salt okunurdur; düzenlenebilir istenirse Inspector'da **Export Animation Assets**. Platformer state machine gerekiyorsa en sağlam yol: cilalanmış kareleri tag klasörlerine çıkar ve aynı hattan geçir:
```bash
aseprite -b Ranger.aseprite --save-as "polished/{tag}/{tagframe}.png"
python scripts/pixel/frames_to_sheet.py --dir polished --name Ranger --out build/Ranger --colors 20
```
(`frames_to_sheet` dosyaları doğal sırayla okur: 2 < 10. Süreler anim varsayılanlarından gelir; gerekirse JSON'da `durationMs` düzelt.)

### D — 3D→piksel
```bash
blender -b Hero.blend --python scripts/blender/render_frames.py -- --name Hero --mode pixel --px-height 40 --out build/HeroPx --clips Idle,Run,Attack,Death
python scripts/pixel/frames_to_sheet.py build/HeroPx/frames.json --out build/HeroPx/sheet --colors 12 --outline
```
Workbench düz ışık + AA kapalı; kamera -X'ten bakar → karakter ekranda sağa bakar. `--step` ile kare seçimi (varsayılan ~12 fps). Idle gibi yavaş kliplerde `--step 8` (aksi halde 24 kare nefes çıkar). Kopya kareler süreleri toplanarak birleştirilir.

## 3. Spec şeması (pixel_character.py)
```json
{
  "name": "Ranger",
  "frame": {"auto": true, "baseline": 2},        // veya {"w":48,"h":40,"baseline":2}
  "ppu": 16,
  "outline": "full",                              // full | selective | none
  "body": {"height": 24, "head": 1.0, "build": 1.0,
           "hair": "short", "weapon": "sword", "scarf": true},  // hair: short|long|hood|spiky|none ; weapon: sword|staff|none
  "palette": {"cloth": "#3b5dc9", "cloth_shade": "#29366f", "accent": "#ef7d57", "...": "..."},
  "animations": {"walk": false, "attack": {"ms": [80,60,40,100,120]}},   // false = çıkar; ms/loop/grounded override
  "stateHints": {"runSpeed": 3.5, "apexBand": 1.2}                        // controller eşikleri (birim/sn)
}
```
Palet anahtarları: outline, skin(_shade), hair(_shade), cloth(_shade), pants(_shade), boots(_shade), accent, eye, weapon(_shade), smear.
Silüet ayrışması renkten değil **şekilden** gelir: saç tipi, silah, atkı, `head`/`build` oranları. Düşman varyantı = aynı spec, farklı palet + oran.

## 4. Sheet kontratı ve QA
`uca-sheet/1` (bkz. `scripts/pixel/sheetio.py` başlığı): anim başına bir satır, üst-sol koordinat, kare başına `durationMs`, `events`, `loop`, `grounded`, `pivot`, `ppu`, `stateHints`.

`pixel_qa.py` — **her yolun çıktısında koş**, exit 1 = dur:
- E `alpha` yarı saydam · E `clip` hücre kenarına değiyor · E `feet` yerdeki klipte ayak baseline'da değil · E `empty`
- W `colors` · W `orphans` tek piksel gürültü · W `dupe` · W `loopseam` · W `volume` idle alanı %12'den fazla oynuyor · W `pivot`

## 5. Unity'de ne kurulur (`uca_pixel_import`)
- Texture: Sprite/Multiple, **Point**, mipmap yok, sıkıştırma yok, Clamp, NPOT yok, FullRect mesh.
- Slicing: Sprite Editor data provider, capability kontrollü (resmî Safe Core Pattern); isimler `<Name>_<anim>_<ii>`; yeniden koşunca **sprite ID'leri korunur**.
- Klipler: `SpriteRenderer.m_Sprite` PPtr eğrisi, kare başına gerçek süre, son kareyi tutan kapanış anahtarı, loopTime, event'ler.
- Controller (tüm geçişler süre 0, pikselde blend yok):
```
idle ⇄ walk ⇄ run          (Speed > 0.1 / > runSpeed)
ground → jump_rise          (!Grounded && VelY > 0.1)
ground → fall               (!Grounded && VelY < -0.1)   kenardan düşme
jump_rise → jump_apex       (VelY < apexBand) → fall (VelY < -apexBand)
air → land (Grounded) → idle (exit 1) | run (Speed>0.1, exit 0.5)
AnyState → death (Dead) > hurt (Hurt && !Dead) > attack (Attack && !Dead) → idle (exit 1)
```
- Prefab: SpriteRenderer + Animator + Rigidbody2D (Interpolate, dönme kilitli, Continuous) + CapsuleCollider2D (idle opak sınırından) + `UCA.PlatformerAnimatorDriver` (hız/zemin/flip okur; `TriggerAttack/TriggerHurt/SetDead`; `onAttackHit/onDeathFinished` UnityEvent).

## 6. Özel animasyon (wall_slide, dash, crouch…)
1. `pixel_character.py` → `poses_for()` içine yeni isim + poz tablosu, `DEFAULT_ANIMS`'e süre/loop/grounded.
2. QA → import. Importer bilinmeyen state'i ekler ama geçiş kurmaz ve `warnings`'te söyler → geçişi kullanıcının oyun mantığına göre (ör. `WallSlide` bool parametresi) ekle.
