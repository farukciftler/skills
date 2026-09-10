# Motora alma — Unity, RealityKit, Godot

## Format seçimi (indirmeden önce)

| Hedef | Tercih | Kabul | Kaçın |
|---|---|---|---|
| Unity | FBX (rig/anim), GLB (statik) | OBJ + texture | .blend (Blender kurulu değilse import olmaz) |
| RealityKit / iOS | USDZ | GLB → dönüştür | FBX (dönüşümde materyal kaybı) |
| Godot | GLB | .tres (ambientCG), FBX (4.x ufbx) | — |

Mobil bütçe: ekranda küçük görünen prop için 500–5k tri, 512–1k texture; Poly Haven/ambientCG'den 1k veya 2k çözünürlüğü indir, 8k'yı değil.

## Unity

- **glTF/GLB:** Package Manager → `com.unity.cloud.gltfast` (Unity glTFast). Sonra `.glb`'yi `Assets/` altına sürükle.
- **FBX:** doğrudan. Import ayarları: Scale Factor (Sketchfab modelleri sık sık 100x/0.01x gelir — prefab'da düzelt, mesh'te değil), Rig: Humanoid (Mixamo), Materials: Extract.
- **PBR materyal (ambientCG/Poly Haven):** Color → Base Map, NormalGL → Normal Map (ambientCG `_NormalGL` Unity ile uyumlu; `_NormalDX` DirectX — Y ters), Roughness → URP Lit Smoothness'a **ters çevrilerek** (1-roughness) ya da metallic/smoothness paketlenmiş haritaya; AO → Occlusion; Displacement çoğu zaman gereksiz.
- **HDRI:** `.hdr`/`.exr` → Texture Shape: Cube → Skybox/Cubemap materyali → Lighting > Environment.
- **Audio:** WAV kaynak; kısa SFX Decompress On Load, müzik Streaming + Vorbis.
- **Unity MCP bağlıysa:** import, prefab oluşturma, materyal atama ve klasör düzenini Editor'e yaptır; sonra `AssetDatabase.FindAssets` ile doğrula.
- Asset Store paketleri: Package Manager → My Assets (kullanıcı elle indirir/import eder).

## RealityKit / iOS (Swift, USDZ)

- Sketchfab download API USDZ verir; Poly Haven USD verir (USDZ'ye paketle).
- GLB/FBX → USDZ: Apple **Reality Converter** (sürükle-bırak, materyal düzeltme), Reality Composer Pro, veya Blender → File > Export > USD (`.usdz`).
- Dönüşüm sonrası kontrol: ölçek (RealityKit metre), eksen (Y-up), texture'ların pakete gömülü olması, PBR kanallarının doğru eşlenmesi.
- Uygulama boyutu: her USDZ texture'ı dahil taşır → 1k texture ile export et.
- Ses: `.caf`/`.m4a`; prosedürel ses tercih ediliyorsa `procedural-game-audio` skill'i.

## Godot 4

- GLB doğrudan sahneye; materyaller içe gelir.
- ambientCG pack'lerindeki `.tres` doğrudan StandardMaterial3D.
- HDRI: WorldEnvironment → Sky → PanoramaSkyMaterial.

## Dosya düzeni (her motor)

```
ThirdParty/
  PolyHaven/barrel_01/        (+ LICENSE.txt: "CC0 — polyhaven.com/a/barrel_01 — 2026-09-10")
  Sketchfab/<uid>_<slug>/     (+ LICENSE.txt: TASL satırı)
  Kenney/<pack>/              (pack'in kendi License.txt'si)
```

Her klasöre kaynak URL + lisans + indirme tarihi içeren `LICENSE.txt` koy; `credits.py` ledger'ı ile tutarlı olsun.
