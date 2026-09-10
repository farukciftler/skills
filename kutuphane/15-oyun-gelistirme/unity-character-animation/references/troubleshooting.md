# Sorun giderme — belirti → sebep → düzeltme

## 2D
| Belirti | Sebep | Düzeltme |
|---|---|---|
| Sprite bulanık | Bilinear filtre / mipmap / AA | importer zaten Point+mipmapsiz yapar; hâlâ bulanıksa AA/kamera → `unity:2d-pixel-perfect` |
| Karakter yürürken 1px titriyor | Tek sayılı hücre, pivot yarım pikselde, fizik interpolasyonu yok | çift hücre; QA `pivot` uyarısı; Rigidbody2D Interpolate (prefab'da açık); kamera LateUpdate |
| Ayak zeminde yüzüyor/gömülüyor | baseline ile collider/pivot uyuşmuyor | QA `feet` hatası ilk bakılacak yer; pivot y = baseline/h; collider altı pivotta |
| Sola dönünce karakter kayıyor | Pivot x merkezde değil | sheet simetrik kırpılır (pivot 0.5); elle kırpılmış sheet'i `frames_to_sheet` ile yeniden üret |
| Son kare hiç görünmüyor | Kapanış anahtarı yok | importer ekler; elle yapılan kliplerde son kareyi süresi kadar tutan anahtar ekle |
| Saldırı iki kez tetikleniyor | AnyState self-transition | importer `canTransitionToSelf=false`; özel geçişlerde de kapat |
| Havada idle oynuyor | Grounded yanlış (ground layer maskesi) | `PlatformerAnimatorDriver.groundLayers`; collider Rigidbody2D'ye bağlı mı |
| Zıplama başında idle'a geri titriyor | İlk karede cast hâlâ zemine değiyor | normal: bir kare sonra düzelir; rahatsız ederse `groundProbe` küçült |
| `uca_pixel_import` "com.unity.2d.sprite is missing" | paket yok | `unity:unity-package-management` ile ekle, recompile |
| AI sheet'te renk sayısı patlıyor | kare başına palet / gürültü | `frames_to_sheet --colors 16` veya `--palette` ile oyun paletine kilitle |
| AI kareleri blok gibi değil | büyütülmüş sahte piksel | `--grid auto` (1–8x doğrulandı); tespit 1 dönerse `--grid N` ver |

## 3D
| Belirti | Sebep | Düzeltme |
|---|---|---|
| Unity'de model -90° yatık | preset/bakeAxis uyuşmazlığı | manifest `exportPreset` ile importer ayarı eşleşir; rapor `rootRotation` ≠ 0 ise preset değiştir |
| Model 100x büyük/küçük | Apply Scalings yanlış | FBX All + useFileScale; `verify_fbx` UnitScaleFactor=100 |
| "Avatar invalid" / kırmızı kemikler | eşleme veya T-pose yok | manifest `humanList` bone adları modelde mi; bind pose T-pose mu |
| Animasyonlar Unity'de yok | action'lar kaydedilmedi / NLA karışıklığı | fake user + All Actions; `verify_fbx` take listesine bak |
| Klip adları `RIG_Hero|Idle` | Blender take adlandırması | importer `|` önekini atar; elle import ettiysen clipAnimations'da yeniden adlandır |
| Karakter yürürken ileri kayıyor | root motion açık / bake into pose kapalı | importer bake-into-pose + `applyRootMotion=false`; hareketi CharacterController yapar |
| Ayaklar kayıyor (ice skating) | blend tree eşiği ≠ gerçek hız | `locomotion.walkSpeed/runSpeed` = oyunun hızları; ya da klip hızını ayarla |
| Karakter siyah (Blender) | palet buffer'ı sıfırlandı / pack yok | 3d-blender.md §8; `verify` "palette texture is blank" |
| Karakter Unity'de mor | shader bulunamadı (pipeline) | importer pipeline'a göre seçer; özel pipeline'da materyal shader'ını elle ata |
| Uzuv zemine giriyor | interpolasyon | `verify` yakalar; `_fix_between_keys` yetmezse anahtar ekle |
| MCP çağrısı zaman aşımı | uzun iş tek çağrıda / iki istemci | aşamalara böl; tek istemci; tam üretimde headless |

## Unity bağlantısı
| Belirti | Sebep | Düzeltme |
|---|---|---|
| `unity command` bağlanamıyor | Safe Mode (derleme hatası) | `unity pipeline list` → log'dan `error CS` → kaynağı düzelt → PID ile yeniden başlat (`unity:unity-cli`) |
| `uca_*` komutları listede yok | recompile edilmedi / pipeline yok | `unity command recompile` → `recompile_status`; `UCA_PIPELINE` versionDefine'ı pipeline paketi yoksa tanımlanmaz → `eval` yedeğini kullan |
| eval CS0246/CS0210 | `using` yazıldı / tip nitelenmedi | statement bloğu: tam nitelikli `UCA.Editor.PixelCharacterImporter.Run(...)` |
