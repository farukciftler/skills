# Asset MCP sunucuları

Doğrulama: 10 Eylül 2026. Hepsi yerel çalışır (stdio); Claude Code, Claude Desktop, Cursor gibi istemcilerle. Claude.ai web sohbeti kullanıcının makinesindeki MCP'ye erişemez.

**Güvenlik:** Topluluk MCP'leri kullanıcının makinesinde kod çalıştırır. Kurmadan önce repo'yu incele (yıldız, son commit, ne indirdiği, nereye yazdığı). Blender/Unity köprüleri keyfi Python/C# çalıştırabilir — sadece güvenilen projelerde aç. API anahtarlarını `env` bloğunda tut, repoya commit etme.

## Seçim tablosu

| İhtiyaç | MCP | Anahtar |
|---|---|---|
| Unity içinde low-poly ara→import→prefab→credit | Poly Pizza Unity MCP | Poly Pizza |
| Genel Poly Pizza araması (motor bağımsız) | MatthewHallCom/Poly-Pizza-MCP | Poly Pizza |
| Sketchfab ara + glTF/GLB/USDZ indir | sketchfab-mcp-server | Sketchfab API token |
| Blender'a Poly Haven/Sketchfab asset'i çek, düzenle, export | ahujasid/blender-mcp | Sketchfab için token |
| Çok kaynak + lisans kontrolü + CREDITS | ASSETMCP / threenative-asset-mcp | Kaynağa göre |
| Unity Editor'ü sür (import, prefab, materyal) | Unity CLI `unity mcp` veya MCP for Unity | — |

## Poly Pizza — Unity entegre (topluluk, lobehub: had0yun-poly-pizza-mcp)
Arama, toplu import, prefab üretimi, önbellek, CC-BY modeller için credit dosyası.
```json
{ "mcpServers": { "poly-pizza": {
  "command": "node", "args": ["/path/to/poly-pizza-mcp/dist/index.js"],
  "env": { "POLY_PIZZA_API_KEY": "...", "UNITY_PROJECT_PATH": "/path/to/UnityProject" } } } }
```
Araçlar: `search_models`, `search_and_batch_import`, `get_popular`. Unity glTF desteği için glTFast gerekebilir.

## Poly Pizza — genel (github.com/MatthewHallCom/Poly-Pizza-MCP)
```json
{ "mcpServers": { "polypizza": {
  "command": "node", "args": ["/path/to/polypizza-mcp/dist/index.js"],
  "env": { "POLYPIZZA_AUTH_TOKEN": "..." } } } }
```
Araçlar: `get_model`, `get_list`, `search_models` (kategori/lisans/animasyon filtresi), `search_models_by_keyword`, `get_user`. Token yoksa sunucu başlamaz.

## Sketchfab (npm: sketchfab-mcp-server)
```json
{ "mcpServers": { "sketchfab": {
  "command": "node", "args": ["/path/to/build/index.js", "--api-key", "..."] } } }
```
veya `SKETCHFAB_API_KEY` env. Araçlar: arama (query, tags, categories, `downloadable`, limit 1–24), model detayı, indirme (gltf/glb/usdz/source, `outputPath`). Lisans filtresi araçta yoksa sonuçta `license` alanını kendin kontrol et.

## Blender MCP (ahujasid/blender-mcp)
Blender eklentisi + `uvx blender-mcp`. Eklenti panelinden **PolyHaven** ve **Sketchfab** entegrasyonlarını aç (kapalıyken araçlar hata döner). Araçlar: `get_polyhaven_categories`, `search_polyhaven_assets(asset_type, categories)`, Poly Haven indir/uygula, Sketchfab ara/indir. Asset'i Blender'da decimate/retopo/rescale edip Unity'ye FBX/GLB, iOS'a USDZ export etmek için ideal.

## Toplayıcılar (topluluk)
- **ASSETMCP** (glama: evonar543/ASSETMCP, Python): Kenney, OpenGameArt, Quaternius, Poly Haven, ambientCG, Openverse, itch.io, Godot Asset Library, GitHub, yerel klasör aramaları; normalize sonuç; indirmeden önce lisans kontrolü; `ASSET_MANIFEST.json`; `CREDITS.md`. Opsiyonel Blender köprüsü keyfi Python çalıştırır.
- **threenative-asset-mcp** (glama: jonit-dev): Fab (varsayılan free), Poly Haven, ambientCG, Smithsonian 3D, Sketchfab + küratörlü oyun sesi kataloğu (Sonniss, Kenney, Freesound, OpenGameArt, Pixabay, Mixkit...). Doğrudan indirme sadece lisansı bilinen sabit URL'li paketlerde.

Toplayıcı MCP'ler yeni ve küçük projeler: sonuçlarını bu skill'in lisans kapısından yine geçir; "license: safe" etiketine körü körüne güvenme.

## Unity Editor tarafı
- Resmî: Unity CLI (`com.unity.pipeline` paketi) → `unity mcp configure claude-code`. Proje içi asset aramak için `unity command eval` ile `AssetDatabase.FindAssets("t:Material wood")`.
- MCP for Unity (CoplayDev): Package Manager git URL `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`; asset yönetimi, sahne, script.
- IvanMurzak/Unity-MCP: `assets-find`, `assets-find-built-in` hazır araçlar.

İndirilen dosyayı `Assets/ThirdParty/<Kaynak>/<AssetAdı>/` altına koy; ledger'daki `used_in` alanı prefab yolunu tutsun.
