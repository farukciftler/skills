# Kaynaklar — erişim, API, lisans

Doğrulama tarihi: **10 Eylül 2026**. API'ler değişir; bir istek beklenmedik şekil dönerse önce bu dosyadaki linkten dokümantasyonu yeniden kontrol et.

İçindekiler: API'li (Poly Haven · ambientCG · Poly Pizza · Sketchfab · Freesound) → API'siz (Kenney · Quaternius/KayKit · OpenGameArt · itch.io · Unity Asset Store · Fab · Sonniss · Mixamo · Smithsonian · Openverse · müzik)

---

## API'li kaynaklar

### Poly Haven — HDRI, texture, model — CC0
- Base: `https://api.polyhaven.com` · Docs: https://polyhaven.com/our-api (OpenAPI: api.polyhaven.com/api-docs/swagger.json)
- **Anahtar yok.** Her istekte **benzersiz `User-Agent` zorunlu** (ör. `FarukAssetSearch/1.0`).
- `GET /assets?type=hdris|textures|models|all&categories=a,b` → `{id: {name, description, category, tags[], attributes{}, thumbnail_url, max_resolution, polycount (model), authors{}, download_count, type(0=HDRI,1=tex,2=model)}}`
- `GET /categories/{type}` → kategori: adet
- `GET /files/{id}` → çözünürlük→format→`{url,size,md5}`; model/texture'da blend/gltf/fbx/usd ve bağımlı texture listesi
- **Keyword araması yok** → tümünü çek, `name/tags/category/description` üzerinde istemci tarafında filtrele.
- API kullanım şartı (18 Tem 2026 itibarıyla): ticari dahil herkese ücretsiz; canlı API'yi ürün içinde kullanıyorsan kullanıcıya "Powered by Poly Haven" benzeri atıf. Bu **API servisinin** şartı; asset'ler CC0. Kendi oyunun için indirip gömdüğünde asset'ler için credit gerekmez. (GitHub'daki eski ToS metni "non-commercial" diyebilir; polyhaven.com/our-api günceldir.)

### ambientCG — PBR materyal, HDRI, decal, bazı 3D — CC0
- **API v3** (Şubat 2026'dan beri önerilen): `GET https://ambientcg.com/api/v3/assets`
  - `q` (AND'lenen kelimeler), `type` = `material|hdri|substance|decal|atlas|3d-model|plain-image|brush|terrain|hdri-element` (virgül = OR), `sort` = `popular|latest|downloads|oldest|random|alphabet`, `limit` 1–500 (varsayılan 100), `offset`, `id`, `date`
  - `include` = `title,url,tags,thumbnails,previews,downloads,maps,dimensions,technique,...` — **include vermezsen sadece `id` döner**
  - Yanıt: `{totalResults, nextPageHttp, currentPageHttp, assets:[{id, ...include alanları}]}`
  - Site arama parametreleri API ile birebir: ambientcg.com/list?type=material&q=sand → aynı query string.
- v2 (`/api/v2/full_json`) hâlâ çalışıyor ama yeni iş için v3.
- Anahtar yok. Asset sayfası: `https://ambientcg.com/view?id={id}`. Pack'lerde `.tres` (Godot), `.usdc`, `.blend`, `.mtlx` (OpenPBR) var.
- Docs: https://docs.ambientcg.com/api/v3/assets/

### Poly Pizza — low-poly 3D — CC0 + CC-BY karışık
- Base: `https://api.poly.pizza/v1/` · Header: `X-Auth-Token: <key>` (hesap açıp poly.pizza/settings/api)
- `GET /search/{keyword}` · `GET /model/{id}` · `GET /user/{username}` · `GET /popular` · liste/collection uç noktaları
- Yanıt alanları (topluluk dokümanlarından; büyük/küçük harf farklı gelebilir — script toleranslı): `ID, Title, Creator{Username}, Thumbnail, Download (glb), Licence, Tags, Tri Count/TriangleCount, Animated`
- Arama filtreleri (`limit`, `animated`, tri aralığı, kategori, lisans) topluluk wrapper'larında geçiyor — **resmî doküman sayfasında doğrula** (poly.pizza/docs/api).
- ⚠️ Site, API'yi "hobi için ücretsiz, ticari kullanımda kullandıkça öde" olarak duyurmuştu (eski basın sayfası). Bu API erişim ücreti, asset lisansı değil; ticari ürün içine canlı API gömülecekse güncel şartı kontrol et. Kendi oyunun için arayıp elle indirmek sorun değil.
- Lisans model başına: CC0 veya CC-BY → her sonucu tek tek sınıfla.

### Sketchfab — her tarz 3D — CC lisansları (asset başına)
- Arama: `GET https://api.sketchfab.com/v3/search?type=models&q=...&downloadable=true` — anahtarsız çalışır.
  - Faydalı parametreler: `license` (slug: `cc0`, `by`, `by-sa`, `by-nd`, `by-nc`, `by-nc-sa`, `by-nc-nd`), `max_face_count`, `animated`, `rigged`, `pbr_type`, `categories`, `sort_by` (`-likeCount`, `-viewCount`, `-publishedAt`), `count` (≤24), `cursor`. Slug/parametre adları Data API docs'ta doğrulanmalı: https://docs.sketchfab.com/data-api/v3/index.html#/search
  - Sonuç: `uid, name, viewerUrl, user{username, profileUrl}, license{label/slug}, faceCount, vertexCount, animationCount, isDownloadable, thumbnails.images[]`
- İndirme: `GET /v3/models/{uid}/download` → **kimlik doğrulama zorunlu**. Kişisel kullanım: `Authorization: Token <API token>` (sketchfab.com/settings/password). Üçüncü taraf uygulama: OAuth2 + son kullanıcı Sketchfab girişi zorunlu.
  - Dönen link geçici (kısa ömürlü imzalı URL) → **cache'leme**, hemen indir.
  - API üzerinden formatlar: glTF, GLB, USDZ (FBX/OBJ kaynak dosyalar API'de yok; sitede elle).
- Lisans şartı: CC-BY ailesinde yazar + Sketchfab kaynak linki; oyun içinde kullanıcıya erişilebilir credit.
- "Downloadable" ≠ ticari: NC/ND modeller de indirilebilir → `--commercial` filtresi şart.

### Freesound — SFX, ambiyans — CC0 / CC-BY / CC-BY-NC (asset başına)
- API anahtarı: https://freesound.org/apiv2/apply · Parametre: `token=<key>`
- **Arama uç noktası: `GET https://freesound.org/apiv2/search/`** (`/apiv2/search/text/` Kasım 2025'te deprecate; hâlâ redirect ediyor)
  - `query`, `filter` (Solr: `license:"Creative Commons 0"`, `duration:[0 TO 5]`, `tag:loop`, `avg_rating:[4 TO 5]`), `fields=id,name,username,license,duration,previews,url,tags`, `page_size`, `sort`
  - `license` alanı URL döner (ör. `http://creativecommons.org/publicdomain/zero/1.0/`) → script eşler
- Preview (mp3/ogg) token ile iner; **orijinal kalite indirme OAuth2 ister**. Prototip için preview, final build için orijinali sitede indir.
- Resmî Python istemcisi: `pip install git+https://github.com/MTG/freesound-python`

---

## API'siz kaynaklar (web_search / web_fetch / Claude in Chrome)

### Kenney — 2D/3D/UI/audio — CC0
- kenney.nl/assets · pack bazlı zip. API yok; kenney.nl/assets/{pack-slug} sayfası. Poly Pizza'da da Kenney modelleri var (`/user/Kenney`) → API ile tek model çekilebilir.
- Credit gerekmez; nezaketen "Kenney (kenney.nl)".

### Quaternius / KayKit — stylized low-poly model + animasyon — CC0 (pack sayfasında teyit et)
- quaternius.com, kaylousberg.itch.io. Pack bazlı. Quaternius modelleri Poly Pizza'da da aranabilir.

### OpenGameArt — her şey — karışık lisans
- API yok. Gelişmiş arama URL'si: `https://opengameart.org/art-search-advanced?keys={q}` + tür ve lisans filtreleri (formdan seçip URL'yi kopyala).
- Lisanslar: CC0, OGA-BY 3.0/4.0, CC-BY 3.0/4.0, CC-BY-SA, GPL/LGPL. **Birden fazla lisans listelenmişse** kullanıcı en uygun olanı seçebilir (ör. "OGA-BY 3.0, CC0" → CC0).
- OGA-BY = CC-BY'nin DRM kısıtı kaldırılmış hali → App Store için CC-BY'den güvenli.

### itch.io — 2D/3D/audio — karışık
- Filtre URL kalıpları: `https://itch.io/game-assets/free`, `.../free/tag-3d`, `.../free/tag-low-poly`, `.../free/tag-music`, lisans: `https://itch.io/game-assets/assets-cc0`, `.../assets-cc4-by`
- "Free" ≠ lisanslı: çok pack özel lisansla gelir ("ticari serbest, yeniden satma yok" gibi) → sayfadaki lisans metnini oku.

### Unity Asset Store — free paketler — Asset Store EULA
- Herkese açık arama API'si yok. Sitede "Free Assets" filtresi; `web_search "site:assetstore.unity.com free <konu>"` iyi çalışır.
- EULA: non-restricted asset'ler başka motorlarda da kullanılabilir; ham dosyayı yeniden dağıtamaz/çıkarılabilir bırakamazsın, UGC'de para kazanamazsın. **Public repoya koyma.** "Restricted" veya "Extension Asset" etiketi varsa sayfadaki özel şartı oku.
- Import: Package Manager → My Assets (elle, kullanıcı yapar).

### Fab (Epic) — free + haftalık/iki haftalık giveaway
- Fab Standard License: her motor/araçta kullanım serbest. Megascans 2025'ten itibaren büyük ölçüde ücretli; bir kısmı free kalır.
- Giveaway'ler süreli: "sahip ol" dersen kalıcı. Güncel liste için `web_search "Fab free assets this week"`.
- Unreal dışı motorlarda format FBX/GLB olan asset'leri seç.

### Sonniss GDC Game Audio Bundle — SFX — royalty-free
- Yıllık, onlarca GB. Ticari, atıfsız, sınırsız proje. Yasak: sesleri tek başına yeniden paketleme/satma ve AI eğitimi. Geçmiş yılların bundle'ları da indirilebilir.

### Mixamo (Adobe) — rig + insansı animasyon — ücretsiz, oyunlarda royalty-free
- API yok; Adobe hesabıyla elle. Karakteri yükle → otomatik rig → animasyon indir (FBX). Humanoid Unity rig'ine uyar.

### Smithsonian Open Access 3D — tarihi objeler — CC0 (asset başına "CC0" etiketi olanlar)
### Openverse — CC görseller/ses araması (API var: api.openverse.org) — fotoğraf/texture referansı için; oyun sprite'ı için nadiren uygun.

### Müzik
- **Kenney Music Jingles** (CC0), **OpenGameArt** (CC0 filtresi), **Pixabay Music** (Pixabay Content License — ticari, atıfsız; müzik tek başına yeniden dağıtılamaz).
- **Incompetech / Kevin MacLeod**: CC-BY 4.0, sabit credit satırı → App Store'da CC-BY DRM notu geçerli; lisans satın alarak atıfsız sürüm alınabilir.
