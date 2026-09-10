# Lisans matrisi ve credit şablonları

Hukuki danışmanlık değildir. Amaç: ticari indie oyunda (özellikle App Store) sık yapılan hataları yakalamak.

## Matris

| Lisans | Ticari | Değiştirme | Credit | App Store / Steam (DRM) | Kapalı kaynak | Sınıf |
|---|---|---|---|---|---|---|
| CC0 1.0 / Public Domain | ✅ | ✅ | ❌ (nezaket) | ✅ | ✅ | 🟢 |
| Unity Asset Store EULA | ✅ | ✅ | ❌ | ✅ | ✅ (ham dosya dağıtma yok) | 🟢 |
| Fab Standard License | ✅ | ✅ | ❌ | ✅ | ✅ (ham dosya dağıtma yok) | 🟢 |
| Sonniss GDC | ✅ | ✅ | ❌ | ✅ | ✅ (tek başına paketleme, AI eğitimi yok) | 🟢 |
| Pixabay Content License | ✅ | ✅ | ❌ | ✅ | ✅ (tek başına dağıtma yok) | 🟢 |
| Mixamo | ✅ | ✅ | ❌ | ✅ | ✅ | 🟢 |
| OGA-BY 3.0 / 4.0 | ✅ | ✅ | ✅ | ✅ (DRM kısıtı yok) | ✅ | 🟡 |
| CC-BY 3.0 / 4.0 | ✅ | ✅ | ✅ | ⚠️ anti-DRM maddesi | ✅ | 🟡 |
| CC-BY-SA 3.0 / 4.0 | ✅ | ✅ (türev de SA) | ✅ | ⚠️ DRM + SA | ⚠️ asset türevleri SA kalır | 🟠 |
| LGPL | ✅ | ✅ (değişiklik açılır) | ✅ | ⚠️ | ✅ | 🟠 |
| GPL 2/3 | ✅ | ✅ | ✅ | ❌ App Store şartlarıyla uyumsuz kabul edilir | ❌ | 🔴 |
| CC-BY-NC* | ❌ | — | — | — | — | 🔴 |
| CC-BY-ND | ✅ | ❌ (oyuna gömmek türev sayılabilir) | ✅ | — | — | 🔴 |
| "Personal use only", "Editorial", lisans yok | ❌ | — | — | — | — | 🔴 |

## CC-BY ve App Store — neden sarı-uyarı

CC-BY 4.0 (ve 3.0) lisans sahibinin haklarını kısıtlayan "etkili teknolojik önlem" (DRM) uygulamayı yasaklar. App Store (FairPlay) ve Steam DRM içerir. Creative Commons bu platformları 4.0 tartışmasında örnek olarak anmış ama maddeyi kaldırmamıştır. Pratikte:
- Topluluk görüşü bölünmüş; birçok oyun CC-BY asset'le yayında ve bilinen yaptırım örneği azdır — ama risk sıfır değildir.
- **Güvenli yollar, sırasıyla:** (1) aynı asset'in CC0/OGA-BY sürümü varsa onu seç, (2) sanatçıdan yazılı anti-DRM feragati iste (OpenGameArt'ta birçok sanatçı açıkça veriyor), (3) eşdeğer CC0 asset bul.
- Kullanıcıya karar bırakırken bunu tek cümleyle söyle; tekrarlama.

## Credit satırı şablonları

CC-BY / OGA-BY için TASL: **T**itle, **A**uthor, **S**ource, **L**icense.

```
"Wooden Barrel" by jane_doe (https://sketchfab.com/3d-models/...) — CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
"Door Creak" by user123 on Freesound (https://freesound.org/s/12345/) — CC BY 4.0
"Forest Tileset" by Artist (https://opengameart.org/content/...) — OGA-BY 3.0
Değiştirildiyse sona: "— modified (recolored, decimated)"
```

Nereye: oyun içi Credits ekranı (zorunlu erişilebilir yer) + repo'da `CREDITS.md`. App Store açıklamasına gerek yok ama oyun içinden ulaşılabilir olmalı.

CC0 için isteğe bağlı: `Assets by Kenney (kenney.nl), Poly Haven (polyhaven.com), ambientCG (ambientcg.com) — CC0`.

Sketchfab ek şartı: yazar kullanıcı adı + Sketchfab model linki. Poly Haven canlı API'si ürün içinde kullanılıyorsa (runtime asset tarayıcısı gibi) "Powered by Poly Haven" görünür olmalı.

## Kırmızı bayraklar (lisans ne derse desin önerme)

- Bilinen oyun/film karakteri, marka logosu, ünlü araç tasarımı (Sketchfab'da fan art çok; CC lisansı yüklemeyi yapanın hakkı yoksa geçersiz)
- "Ripped", "extracted from", "fan model" ifadeleri
- Yazarın başka hiçbir işi olmayan, lisansı açıklamayla çelişen pack
- Açıklamada "AI generated" + belirsiz eğitim verisi — ticari projede kullanıcıya not düş
