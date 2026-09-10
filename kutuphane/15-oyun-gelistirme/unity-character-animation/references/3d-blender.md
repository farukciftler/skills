# 3D karakter — Blender'da üret, rigle, animasyonla, doğrula → Unity Humanoid

## İçindekiler
1. Blender bağlantısı (resmî MCP · topluluk MCP · headless)
2. MCP oturum protokolü
3. Konvansiyonlar ve spec
4. Aşamalar ve kapılar
5. Klip yazma (dünya-ekseni delta tablosu + otomatik planting)
6. FBX export presetleri ve dosya doğrulaması
7. Unity'de ne kurulur
8. Blender 5.x API tuzakları (hepsi bu hatta gerçekten yaşandı)
9. Dış kaynaklı mesh (Meshy/Tripo/Hunyuan/kullanıcı modeli)

---

## 1. Blender bağlantısı

| Yol | Gereksinim | Not |
|---|---|---|
| **Resmî Blender Lab MCP** | Blender **5.1+**, add-on + MCP bundle | Blender geliştiricileri tarafından; `execute_blender_code` (canlı), `execute_blender_code_for_cli` (arka plan süreç), `get_blendfile_summary_datablocks`. **Korumasız kod çalıştırır** — kaydedilmemiş sahneyi riske atma. |
| Topluluk `blender-mcp` (ahujasid) | add-on + `uvx blender-mcp` | `execute_blender_code`, `get_scene_info`, viewport screenshot; Poly Haven/Sketchfab/Hyper3D/Hunyuan3D entegrasyonları |
| **Headless** | `blender` PATH'te | MCP limiti yok (zaman aşımı/yanıt boyutu). **Tam yeniden üretim için tercih et.** |

Hangi araç bağlıysa onu kullan; bağlı değilse ve kullanıcının makinesinde Blender varsa headless komut ver. Kütüphane (`uca_character.py`) üç yolda da aynıdır.

## 2. MCP oturum protokolü
1. **Isınma çağrısı**: önce zararsız okuma (`bpy.app.version_string`, obje listesi). İlk çağrı el sıkışma yarışıyla düşebilir → bir kez tekrar.
2. **Sürüm**: ≥5.0 bekle (slotted action/channelbag API). 4.4–4.5 çoğunlukla çalışır, <4.4 çalışmaz — söyle, tahmin etme.
3. **Kaydet**: yıkıcı işlem öncesi .blend kaydedilmiş olsun veya boş sahnede çalış.
4. **Tek istemci**: Claude Desktop ve Claude Code aynı anda bağlıysa çağrılar gizemli şekilde zaman aşımına düşer.
5. **Parçala**: build → animate → verify → export ayrı çağrılar. Mega-script gönderme.

MCP'de yükleme deseni:
```python
import sys, importlib; sys.path.insert(0, r"<SKILL>/scripts/blender")
import uca_character as uc; importlib.reload(uc)
spec = uc.load_spec(r"<proje>/art/hero.json")
uc.build(spec)
```
```python
print(uc.animate(spec))
```
```python
import json; print(json.dumps(uc.verify(spec), indent=1))
```
```python
print(uc.export(spec, r"<proje>/Assets/Characters/Hero"))
```
Headless tek komut: `blender -b --factory-startup --python scripts/blender/pipeline.py -- hero.json --out <klasör> --save-blend`

## 3. Konvansiyonlar ve spec
- 1 BU = 1 m, Z yukarı, karakter **-Y'ye bakar**, sol taraf +X, ayaklar z=0'da, orijin ayak ortası.
- Bind pose = **T-pose** (Unity Humanoid avatar oluşturma bunu bekler).
- Kemik adları = Unity `HumanBodyBones` adları (Hips, Spine, Chest, Neck, Head, LeftShoulder, LeftUpperArm, LeftLowerArm, LeftHand, LeftUpperLeg, LeftLowerLeg, LeftFoot, LeftToes, sağ taraf aynısı) + `Root` (orijinde, deform değil). 21 humanoid kemik; zorunlu 15'in hepsi var. Eşleme Unity'de **açıkça** yapılır, automap'e bırakılmaz.
- **Rigid parça skinning**: her parça tek kemiğe 1.0 ağırlıkla. Ağırlık boyama hata sınıfını tamamen yok eder; mankeni tarzında eklem topları (`style: "mannequin"`) dikiş boşluklarını gizler.
- Tek materyal `MAT_<name>`, 64×64 palet atlası (8px hücre, **Closest** interpolasyon), UV'ler hücre merkezine çökertilir.
- Klipler **yerinde** (in-place): kök ilerlemez; oyunu CharacterController taşır, root motion kapalı.

Spec (`assets/character_3d.example.json`):
```json
{"name": "Hero", "height": 1.8, "headRatio": 6.5, "build": 1.0, "style": "mannequin", "segments": 8,
 "triBudget": 6000, "fps": 30,
 "palette": {"skin": "#e0ac8a", "shirt": "#3b5dc9", "pants": "#333c57", "shoes": "#5a3a28", "hair": "#3b2a20", "accent": "#ef7d57", "joint": "#29366f"},
 "clips": ["Idle","Walk","Run","Jump_Start","Jump_Air","Jump_Land","Attack","Hurt","Death"],
 "locomotion": {"walkSpeed": 1.6, "runSpeed": 4.5},
 "export": {"preset": "bake_axis"}}
```
`headRatio`: 7–7.5 gerçekçi, 5–6 stilize, 3–4 chibi. `locomotion` hızları blend tree eşikleridir (klibin tasarlandığı m/s) — oyunun gerçek hareket hızlarıyla eşleşmezse ayak kayar.

## 4. Aşamalar ve kapılar

| Aşama | Fonksiyon | Kapı |
|---|---|---|
| 1 build | `uc.build(spec)` | tri, kemik sayısı döner |
| 2 animate | `uc.animate(spec)` | her klip = aynı adlı Action, tek slot |
| 3 verify | `uc.verify(spec)` | **ok:false → export yok** |
| 4 export | `uc.export(spec, out)` | FBX + `<name>_Palette.png` + `<name>.manifest.json` |
| 5 dosya | `verify_fbx.py` | take adları, GlobalSettings eksen/birim, yeniden içe aktarma |
| 6 göz | `render_frames.py --mode check` | bind front/side/3-4 + klip vuruş kareleri — **bak** |

`verify` kontrolleri: 21 humanoid kemik, tri bütçesi, boy ±%2, ayak z≈0, ağırlıksız vertex yok, kemiksiz vertex group yok, -Y yönü, palet boş değil, eksik klip yok, loop dikişi (ilk=son poz), **zemin delinmesi** (her kare, havadakiler dahil), Idle/Walk'ta iki ayak birden havada mı, Attack'ta **ölçülmüş** darbe karesi (sağ elin en ileri noktası; yazılan tahmin değil).

## 5. Klip yazma
`clip_library()` tabloları **dünya ekseni deltası** kullanır; `_pose_to_local` bunları hiyerarşide zincirler (W_b = D_b · W_parent, yerel q_b = R_b⁻¹ · W_parent⁻¹ · W_b · R_b). Böylece kolu indirip sonra dirseği "dünya X etrafında" bükmek sezgisel olarak doğru çıkar. Anlamsal yardımcılar:
- `arms(l_down, r_down, l_swing, r_swing, l_elbow, r_elbow)` — T-pozdan indirme, öne sallama +, dirsek öne bükme +
- `legs(l_swing, r_swing, l_knee, r_knee, l_foot, r_foot, l_spread, r_spread)` — uyluk öne +, diz bükme +
- `torso(lean, twist, chest_lean, chest_twist, head, head_turn, hips_lean, hips_twist)` — öne eğilme +
- anahtar: `(kare, pose(...), (x, y, lift))` — `lift` sadece ek kaldırma.

**Otomatik planting**: yerdeki kliplerde her anahtar pozdan sonra Hips dikeyde kaydırılır ki en alçak nokta bind-pozdaki gibi zemine otursun; ardından `_fix_between_keys` her kareyi tarar, interpolasyonun zemine gömdüğü karelerde Hips'i yukarı iter. Çömelme yüksekliğini elle ayarlamak (ayakların gömülmesinin 1 numaralı sebebi) gereksiz. Havadaki klipler: meta `{"plant": "up", "airborne": True}` — sadece yukarı iter (toplanmış bacak zeminin/pivotun altına sarkmaz; 3D→piksel yolunda QA'nın `feet` hatasını bu önler), asla aşağı çekmez.

Yeni klip (ör. `Roll`, `Climb`): tabloya ekle → `spec.clips`'e ekle → verify → controller'a elle bağla (importer uyarır).

## 6. FBX export
| Preset | Blender | Unity `bakeAxisConversion` | Sonuç |
|---|---|---|---|
| `bake_axis` (varsayılan) | Forward **-Y**, Up **Z**, Apply Scalings **FBX All**, Apply Transform **kapalı** | **true** | kök dönmesi 0, ölçek 1, +Z'ye bakar |
| `legacy` | Forward -Z, Up Y, FBX All | false | kökte (-90,0,0) — Humanoid için zararsız, Generic için çirkin |

"Apply Transform" (experimental) **kullanma** — Blender kendi uyarısında armatür/animasyonla bozuk olduğunu söyler. Diğer sabit ayarlar: Add Leaf Bones **kapalı**, deform-only **kapalı** (Root kalsın), All Actions **açık**, NLA Strips **kapalı**, Force Start/End Keying açık, Simplify 0, doku gömülmez (palet PNG yanında gider). Parametreler operatörden **introspect** edilir; bilinmeyen argüman atılır ve `dropped_args` olarak raporlanır.

`verify_fbx.py`:
```bash
blender -b --factory-startup --python scripts/blender/verify_fbx.py -- Hero.fbx Hero.manifest.json
```
Take adları `RIG_Hero|Idle` biçimindedir — Unity klip adını buradan alır; importer `|` önekini atar. `UpAxis=2` (bake_axis), `UnitScaleFactor=100` (Unity "1m (File)", ölçek 1) beklenir.

## 7. Unity'de ne kurulur (`uca_3d_import`)
1. ModelImporter: ölçek 1, dosya ölçeği, preset'e göre `bakeAxisConversion`, Humanoid + CreateFromThisModel.
2. **Açık avatar eşlemesi**: manifestteki `humanList` → `HumanTrait.BoneName`; skeleton içe aktarılan T-pose hiyerarşiden. Avatar `isValid && isHuman` değilse hata.
3. Klipler: önek temizleme, loopTime, root rotation/Y/XZ **bake into pose** (yerinde), `OnAttackHit` (normalize zaman = ölçülmüş darbe karesi / kare sayısı), `OnDeathFinished`.
4. Palet dokusu Point/mipmap yok; pipeline'a uygun Lit materyal (URP/HDRP/Standard) oluşturulur ve FBX materyaline **remap** edilir.
5. Controller: `Locomotion` 1D blend tree (Speed: Idle 0 · Walk walkSpeed · Run runSpeed), Jump_Start → Jump_Air → Jump_Land, AnyState → Death > Hurt > Attack; kısa fixed-duration geçişler (3D'de blend doğru, pikselde yanlış).
6. Prefab (model varyantı): Animator (avatar, root motion kapalı) + CharacterController (manifest kapsülü) + `UCA.ThirdPersonAnimatorDriver`.
7. Rapor: `avatarValid`, `rootRotation` (bake_axis'te 0 beklenir), `measuredHeight` (±%5), `facesPlusZ`.

## 8. Blender 5.x API tuzakları (bu hatta yakalananlar)
- `action.fcurves` / `action.groups` **5.0'da kaldırıldı** → `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot).fcurves`. Pose-bone `keyframe_insert` hâlâ çalışır ve slotu kendisi oluşturur.
- Generated image'da `colorspace_settings.name` atamak buffer'ı **sıfırlar** → renk uzayını piksellerden ÖNCE ata; byte image `pixels[]` doğrudan sRGB değerdir; `img.pack()` yoksa .blend'e kaydedilmez. (Belirti: siyah karakter. `verify` artık boş paleti yakalar.)
- Kamera hizalama: `to_track_quat("-Z", "Y")` — up ekseni track ekseniyle aynı olursa (`"Z"`) kamera yan yatar ve her poz yanlış görünür.
- Son değerlendirilen kare pozu kemiklerde kalır: bind render/export öncesi pose'u sıfırla (`_reset_pose`).
- FBX "All Actions" eski sürümlerde çok slotlu action'larda sadece ilk slotu yazıyordu → her klip tek slotlu ayrı Action (bu hat böyle üretir).
- Operatör kwarg'ları sürümler arasında değişir → introspect et, körlemesine kwarg geçme.

## 9. Dış kaynaklı mesh
Kullanıcı kendi modelini veya AI 3D çıktısını (Meshy/Tripo/Hunyuan MCP) getirirse: bu hattın rig/animasyon/export/Unity kısmı yine geçerli, fakat build aşaması yerine:
1. Modeli T-poza, -Y yönüne, ayak z=0'a, 1 BU = 1 m ölçeğe getir; dönüşümleri uygula.
2. `bone_table(spec)` iskeletini modelin eklem yüksekliklerine göre ayarla (spec `height`/`headRatio`/`build` ile başla, gerekirse tabloyu ölç).
3. Organik mesh için `parent_set(type='ARMATURE_AUTO')` (otomatik ağırlık) — bone-heat uyarısı = mesh sorunu (içe dönük/örtüşen geometri), elle boyamaya kaçma.
4. `animate → verify → export` aynı. Tri bütçesini spec'te yükselt; decimate gerekirse Blender'da yap.
Mixamo'ya otomatik rig için kullanıcının hesabıyla elle yükleme gerekir — ajan bunu yapamaz; yaparsa gelen FBX'i Blender'da bu konvansiyonlara çevir (kemik adları farklıdır: `humanList`'i ona göre yaz).
