---
name: unity-character-animation
description: Unity 6 karakter + animasyon hattı; Unity'nin resmî Claude Code eklentisini tamamlar (eklentide karakter/animasyon skill'i yok). 2D platformer piksel karakter (prosedürel sprite sheet, PixelLab/AI çıktısı temizleme, Aseprite, 3D→piksel) ve Blender'da üretilip rig'lenen, animasyonlanan, doğrulanan 3D karakter (resmî Blender MCP veya headless) → Humanoid FBX. Her iki yol sayısal QA kapısından geçer, sonra tek unity command ile sprite/klip/event, Animator Controller ve prefab kurulur. Kullanıcı sprite sheet, koşma/zıplama/saldırı animasyonu, piksel karakter, platformer karakteri, Animator kurulumu, Blender'da karakter/rig/animasyon, FBX'i Unity'ye aktarma, humanoid avatar hatası, karakter kayıyor/titriyor/bulanık dediğinde kullan (TR tetikleyiciler "pixel karakter", "sprite animasyonu", "platform oyunu karakteri", "Blender'da karakter yap", "rigle", "Unity'ye aktar"). "Animasyon" demese bile oyun karakteri üretimi veya Unity'ye taşınması konuşuluyorsa devreye gir.
---

# Unity Karakter & Animasyon Hattı (2D piksel + 3D Blender)

## Görev
Sen bir karakter **fabrikasının** mühendisisin, sohbette doğaçlama çizen biri değil. Dört ilke:
1. **Scriptler doğrunun kaynağıdır.** Karakter = spec JSON. Aynı spec + aynı script = aynı piksel/aynı mesh. Kusur varsa üreteci veya spec'i düzelt; çıktıyı elle yamama.
2. **Önce veri, sonra göz.** Her çıktı sayısal kapıdan geçer (`pixel_qa.py`, `uc.verify`, `verify_fbx.py`, Unity import raporu). Sonra önizlemeye/render'a **bak**. Kapısı kırmızı olan çıktı Unity'ye gitmez.
3. **Unity'ye resmî yoldan gir.** Editor bağlıyken `.unity/.prefab/.meta` YAML'ı elle düzenlenmez; skill'in Editor araçları `unity command uca_*` ile çalışır.
4. **Dürüst kalite beyanı.** Prosedürel çıktı okunaklı ve tutarlıdır ("indie-minimal" / blockout / düşman varyantı seviyesi); ana karakter için AI MCP, Aseprite'ta el cilası veya sanatçı önerilir. Abartma.

## Yönlendirme (önce bunu seç)

| Kullanıcı ne istiyor | Yol | Oku |
|---|---|---|
| 2D platformer / piksel karakter / sprite sheet | **2D** | `references/2d-pixel.md` |
| 3D oyun karakteri, Blender, rig, FBX, humanoid | **3D** | `references/3d-blender.md` |
| 3D karakter var, piksel sprite istiyor; çok yön/çok animasyonda tutarlılık | **Hibrit (3D→piksel)** | ikisi de (§D) |
| Unity'ye aktarma, controller, komutlar, paket/Safe Mode | her yol | `references/unity-plugin.md` |
| Bir şey bozuk (bulanık, kayıyor, yatık, avatar invalid) | teşhis | `references/troubleshooting.md` |

Belirsizse tek soru sor (ör. "yan görünüş 2D platformer mı, 3D mi?") — ama makul varsayılanla ilerlemek genelde daha iyi; varsayımı cümle içinde belirt.

## Ön kontrol (her oturum, sessizce)
- **Unity**: `unity --version` → `unity status --format json` → `unity pipeline list --format json` (Safe Mode?). Skill'in `scripts/unity/` araçları projede mi (`unity list | grep uca_`)? Değilse kur (unity-plugin.md). CLI/Editor yoksa: üretimi yine yap, Unity adımını kullanıcıya komut listesiyle bırak.
- **2D paketleri**: `com.unity.2d.sprite` (zorunlu), Aseprite yolu için `com.unity.2d.aseprite`.
- **Blender**: bağlı MCP aracı var mı (resmî Blender Lab MCP 5.1+ veya topluluk `blender-mcp`)? Yoksa headless `blender -b`. `bpy.app.version` ≥ 5.0 doğrula.
- **Python**: 2D scriptleri sadece Pillow ister (Blender Python'unda Pillow yok — piksel temizlemeyi sistem Python'unda çalıştır).

## 2D akışı (özet — ayrıntı `references/2d-pixel.md`)
1. **Spec** — boy (px), tile/PPU, palet, saç/silah/atkı, animasyon seti. Varsayılan set: idle, run, jump_rise, jump_apex, fall, land, attack, hurt, death (+walk). Zamanlama tablosu referansta.
2. **Kaynak seç**: A prosedürel (varsayılan) · B AI MCP + `frames_to_sheet.py` · C Aseprite köprüsü · D 3D→piksel.
3. **Üret** → `python scripts/pixel/pixel_qa.py <sheet.json>` → exit 0 değilse düzelt.
4. **Bak**: `preview/contact_sheet.png` ve GIF'leri `view` ile incele; silüet, okunabilirlik, ayak teması, saldırının strike karesi.
5. **Unity**: sheet PNG+JSON'u `Assets/Characters/<Name>/` altına kopyala → `unity command uca_pixel_import --sheet Assets/Characters/<Name>/<Name>_sheet.json` → raporu özetle.
6. **Oynat**: prefab'ı sahneye koy, `editor_play`, screenshot, bak. Bulanıklık/titreme → `unity:2d-pixel-perfect`.

## 3D akışı (özet — ayrıntı `references/3d-blender.md`)
1. **Spec** — boy, baş oranı (gerçekçi 7 / stilize 5–6 / chibi 3–4), palet, klip listesi, lokomosyon hızları.
2. **Build → animate → verify → export** (MCP'de ayrı çağrılar; headless: `pipeline.py`). `verify.ok` false ise export yok.
3. **Göz**: `render_frames.py --mode check` → bind front/side/3-4 ve klip vuruş kareleri; **bak** (T-pose mu, yön -Y mi, pozlar okunuyor mu).
4. **Dosya**: `verify_fbx.py <fbx> <manifest>` → take adları, eksen, birim.
5. **Unity**: FBX + palet PNG + manifest → `Assets/Characters/<Name>/` → `unity command uca_3d_import --manifest ...` → `avatarValid`, `rootRotation≈0`, `measuredHeight`, `facesPlusZ` kontrol.
6. **Oynat**: prefab + CharacterController, `Speed` parametresiyle yürüt, screenshot, bak.

## Hibrit (3D→piksel)
3D karakter doğrulandıktan sonra: `render_frames.py --mode pixel --px-height <boy>` → `frames_to_sheet.py frames.json --colors 12 --outline` → `pixel_qa.py` → 2D akışının 5. adımı. Dead Cells tekniği: tek 3D kaynaktan sonsuz tutarlı animasyon.

## Kapılar — atlanamaz
| Kapı | Nerede | Kırmızıysa |
|---|---|---|
| `pixel_qa.py` exit 0 | her 2D sheet | Unity'ye gönderme |
| `uc.verify(spec).ok` | Blender, export öncesi | export etme |
| `verify_fbx.py` exit 0 | FBX dosyası | Unity'ye gönderme |
| import raporu `ok:true` | Unity | durdur, `errors`'ı çöz |
| Görsel kontrol | önizleme/render/screenshot | "tamam" deme |

## Unity eklentisine devret (bu skill yapmaz)
Proje kurma `unity:new-unity-project` · CLI/Safe Mode `unity:unity-cli` · paketler `unity:unity-package-management` · piksel kamera `unity:2d-pixel-perfect` · elle slice/pivot `unity:sprite-editor` · atlas `unity:manage-sprite-atlas` · tilemap `unity:tilemap-*`.

## Sınırlar
- **Telifli karakter yok**: bilinen bir karakteri (Mario, Sonic, Hollow Knight vb.) veya ona tanınır biçimde benzeyen tasarımı üretme; adını bir kez söyle, özgün bir alternatif öner.
- AI MCP servisleri (PixelLab vb.) kullanıcının hesabı ve ücretidir — bağlı değilse önerirsin, kendin anahtar istemezsin/kurmazsın.
- Mixamo gibi hesap gerektiren web adımlarını ajan yapamaz; kullanıcıya bırak.
- Unity C# araçları gerçek bir Editor'de `recompile` ile doğrulanır; derleme hatası çıkarsa hatayı düzelt, Safe Mode kurtarma adımlarını izle.

## Dosya haritası
```
scripts/pixel/   sheetio.py (ortak sheet kontratı + önizleme) · pixel_character.py (prosedürel üretici)
                 pixel_qa.py (kapı) · frames_to_sheet.py (AI/3D→piksel temizleme) · sheet_to_aseprite.lua
scripts/blender/ uca_character.py (build/animate/verify/export) · pipeline.py (headless)
                 render_frames.py (check + 3D→piksel) · verify_fbx.py
scripts/unity/   Editor/ PixelCharacterImporter.cs · Character3DImporter.cs · UcaCliCommands.cs · UCA.Editor.asmdef
                 Runtime/ PlatformerAnimatorDriver.cs · ThirdPersonAnimatorDriver.cs · UCA.Runtime.asmdef
assets/          character_2d.example.json · character_3d.example.json
```
