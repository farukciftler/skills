---
name: oyun-asset-kesif
description: Ücretsiz oyun asset'i (3D model, PBR texture/materyal, HDRI, 2D sprite, SFX, müzik, animasyon) bulan, lisansını ticari kullanım ve App Store açısından denetleyen, indirip Unity/RealityKit/Godot'a sokan ve CREDITS kaydı tutan uzman. Poly Haven, ambientCG, Poly Pizza, Sketchfab, Freesound API'lerini script ile tek seferde arar; Kenney, Quaternius, OpenGameArt, itch.io, Unity Asset Store free, Fab giveaway gibi API'siz kaynakları web aramasıyla tarar; asset MCP sunucularını (Sketchfab MCP, Poly Pizza MCP, Blender MCP, toplayıcı MCP'ler) kurar. Kullanıcı "free asset", "ücretsiz model/texture/ses", "CC0", "low poly model bul", "şu sahne için asset", "Asset Store'da bedava", "Sketchfab'dan indir", "HDRI lazım", "ses efekti bul", "müzik lazım", "lisansı uygun mu", "App Store'da kullanabilir miyim", "credits nasıl yazılır", "asset MCP" dediğinde; bir oyun sahnesi/prototip için görsel veya ses kaynağı gerektiğinde — "asset" kelimesi geçmese bile — kullan. Lisansı ASLA varsayma; her asset'in lisansını kaynağından oku.
---

# Oyun Asset Keşif

Amaç: "bedava" görünen ama ticari oyunda başa bela olacak asset'leri eleyip, gerçekten kullanılabilir olanı hızlıca bulmak, projeye sokmak ve atıf borcunu kayıt altına almak.

Temel ilke: **Önce lisans, sonra estetik.** Güzel ama lisansı uymayan asset sonuç listesine girmez; girerse kırmızı işaretle girer.

## 0. İhtiyacı netleştir (tek soru, gerekirse)

Konuşmada yoksa şunları çıkar; hepsini sormak zorunda değilsin, makul varsayım yapıp satır içinde belirt:

- **Tür:** 3D model / PBR materyal / HDRI / 2D sprite-UI / SFX / müzik / animasyon
- **Stil:** low-poly, stylized, realistic/scan, pixel art
- **Hedef:** Unity (hangi pipeline), RealityKit/USDZ (iOS), Godot, web
- **Dağıtım:** ticari mi? **App Store / Steam gibi DRM'li mağaza** mı? Açık kaynak mı? → lisans kapısını belirler
- **Bütçe:** poly/tri limiti, texture çözünürlüğü, dosya boyutu (mobil için önemli)

Dağıtım belirsizse **ticari + App Store** varsay (en sıkı durum); sonuçlar daha gevşek senaryoda da geçerli kalır.

## 1. Lisans kapısı — her sonuç için

Ayrıntılı matris ve credit şablonları: `references/licenses.md`. Kısa kural:

| Sınıf | Lisanslar | Karar |
|---|---|---|
| 🟢 Yeşil | CC0, Public Domain, Sonniss GDC, Fab Standard, Unity Asset Store EULA (free dahil), Mixamo, Pixabay Content License | Ticari + App Store serbest (EULA kısıtları: ham dosyayı yeniden dağıtma) |
| 🟡 Sarı | CC-BY 3.0/4.0, OGA-BY | Serbest ama **credit zorunlu**. CC-BY'nin anti-DRM maddesi App Store/Steam için tartışmalı → OGA-BY veya sanatçı feragati tercih et, CC-BY'yi uyarıyla sun |
| 🟠 Turuncu | CC-BY-SA, LGPL | Kapalı kaynak ticari oyunda riskli; sadece kullanıcı bilerek isterse |
| 🔴 Kırmızı | CC-BY-NC*, CC-BY-ND, GPL (App Store), "Editorial", lisanssız/belirsiz, "free for personal use" | Ticari projede önerme |

Kurallar:
- Lisansı **asset sayfasından/API alanından** oku; site genel beyanına güvenme (Sketchfab, OpenGameArt, itch.io, Freesound asset başına değişir).
- Pack içinde karışık lisans olabilir (OpenGameArt'ta sık); en kısıtlayıcıyı esas al.
- "AI ile üretilmiş/rip" şüphesi olan asset'i (ünlü oyunun modeli, marka, karakter) lisansı ne derse desin önerme.

## 2. Kaynak yönlendirme

Ayrıntılı API bilgisi, doğrulama tarihleri: `references/sources.md`.

| İhtiyaç | Önce | Sonra |
|---|---|---|
| Low-poly / stylized 3D | Poly Pizza (API), Kenney, Quaternius, KayKit | Sketchfab (lisans filtreli), itch.io |
| Realistic 3D prop | Poly Haven (API), Sketchfab | Smithsonian 3D (CC0), Fab free |
| PBR materyal / texture | ambientCG (API), Poly Haven (API) | — |
| HDRI / skybox | Poly Haven (API), ambientCG (API) | — |
| 2D sprite / UI / tileset | Kenney, OpenGameArt, itch.io | Unity Asset Store free |
| SFX | Kenney audio, Sonniss GDC bundle, Freesound (API) | OpenGameArt |
| Müzik | Kenney jingles, OpenGameArt (CC0 filtre), Pixabay Music | Incompetech (CC-BY → App Store notu) |
| İnsan animasyonu | Mixamo | Quaternius Universal Animation Library |
| Unity'ye özel paket/araç | Unity Asset Store (free filtresi) | — |

**API'li kaynaklar** → `scripts/asset_search.py` ile ara.
**API'siz kaynaklar** (Kenney, Quaternius, OpenGameArt, itch.io, Asset Store, Fab) → `web_search` / `web_fetch`; kullanıcıda Claude in Chrome varsa sayfada gezerek listele. URL kalıpları `references/sources.md`'de.

## 3. Arama — script

```bash
python scripts/asset_search.py "wooden barrel" --sources polyhaven,ambientcg,polypizza,sketchfab \
  --type model --commercial --appstore --limit 8 --out results.json
```

- Anahtarsız: `polyhaven`, `ambientcg`, `sketchfab` (arama). Anahtarlı: `polypizza` (`POLYPIZZA_API_KEY`), `freesound` (`FREESOUND_API_KEY`). Anahtar yoksa o kaynak atlanır ve çıktıda not düşülür — hata değildir.
- Çıktı normalize JSON: kaynak, id, başlık, lisans, lisans sınıfı, yazar, sayfa URL'si, thumbnail, indirme bilgisi, tri/format, hazır credit satırı.
- `--commercial` NC/ND'yi eler; `--appstore` CC-BY'ye DRM uyarısı ekler; `--green-only` sadece CC0/PD döndürür.
- Claude.ai sandbox'ında bu alan adları ağ izin listesinde olmayabilir; o durumda script'i kullanıcının makinesinde/Claude Code'da çalıştırmayı öner veya aynı sorguları `web_fetch` ile elle yap.

## 4. Sonuç sunumu

Her aday için tek satırlık özet + karar:

```
🟢 Wooden Barrel — Poly Haven — CC0 — 2.1k tri, glTF/FBX/USD, 4k texture
   Neden: stil uyuyor, mobil için 1k texture yeterli
   İndir: polyhaven.com/a/barrel_01 · Credit: gerekmez (nezaketen Poly Haven)
```

- En fazla 5-8 aday; en iyi 1-2'yi açıkça öner.
- Stil tutarlılığını uyar: farklı kaynaklardan karışık low-poly set görsel olarak dağılır; tek yazar/pack'ten gitmek genelde daha iyi.
- Mobil bütçeyi hesaba kat: 8k texture/100k tri'yi iOS için olduğu gibi önerme, LOD/çözünürlük seçimini belirt.

## 5. İndirme ve motora alma

Ayrıntı: `references/engine-import.md`.
- **Unity:** glTF/GLB için `com.unity.cloud.gltfast`; FBX doğrudan. Unity MCP bağlıysa (`unity mcp` / MCP for Unity) import + prefab + materyal atamasını Editor'de yaptır.
- **RealityKit / iOS:** USDZ hedefle. Sketchfab ve Poly Haven USD/USDZ verir; GLB → USDZ için Reality Converter veya Blender USD export.
- **Godot:** GLB doğrudan; ambientCG pack'lerinde `.tres` hazır gelir.
- Asset Store / Fab asset'lerini **public git reposuna koyma** — EULA ham dosyanın yeniden dağıtımını yasaklar; `.gitignore` + README'de "şu paketi kendin ekle" notu.

## 6. Kayıt — CREDITS ve ledger

Her indirilen asset `asset_ledger.json`'a girer; `CREDITS.md` oradan üretilir:

```bash
python scripts/credits.py add --from results.json --id polyhaven:barrel_01 --used-in "Level1/Props"
python scripts/credits.py render --out CREDITS.md
```

CC0 bile olsa kaydet: lisansı sonradan değişen asset'te "o tarihte CC0 idi" kanıtı ledger'dır (kaynak URL + tarih + lisans metni).

## 7. MCP ile otomasyon

Kullanıcı sürekli asset arayacaksa script yerine MCP kurmayı öner. Seçenekler, kurulum JSON'ları ve güvenlik notları: `references/mcp-servers.md`. Kısa özet:
- Unity içinde ara→import→prefab: **Poly Pizza Unity MCP**
- Sketchfab arama+indirme: **sketchfab-mcp-server**
- Blender üzerinden Poly Haven/Sketchfab: **Blender MCP**
- Çok kaynak tek yerde: **ASSETMCP**, **threenative-asset-mcp** (topluluk projeleri — kodu incelemeden çalıştırma)

## Sınırlar

- Asset Store ve Fab'ın herkese açık arama API'si yok; oralarda web araması + tarayıcı.
- Sketchfab tam indirme kullanıcı token'ı ister; üçüncü taraf uygulamada OAuth zorunlu.
- Freesound tam kalite indirme OAuth2 ister; token ile yalnızca preview (mp3/ogg) alınır — prototip için yeterli, final build için orijinali indir.
- Poly Pizza API ticari kullanımda ücretli olabilir (asset lisansından ayrı) — `references/sources.md`.
- Lisans hukuki danışmanlık değildir; yüksek bütçeli ticari projede şüpheli asset için sanatçıya yazılı izin önerilir.
- Karakter üretim pipeline'ı (Blender MCP ile sıfırdan) ayrı iştir; prosedürel ses isteniyorsa `procedural-game-audio` skill'ine devret.
