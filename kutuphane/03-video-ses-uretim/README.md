# Video & Ses Üretimi

Fizik ve ambient video hatları, müzik besteleme, plak etiketi, kanal yönetimi, prosedürel ses.

15 skill. Üst dizin: [../../README.md](../../README.md)

## `ambient-video-forge`

[SKILL.md](ambient-video-forge/SKILL.md)

Turns a still cover image plus an audio track into a long-form healing/ambient music video with layered procedural effects (rising smoke and incense plumes, drifting fog, dust motes, god rays, bokeh, starfields, water caustics, liquid warping of the artwork, bloom, grain, colour grading) in pure ffmpeg, no stock footage. Renders a short seamless loop and stream-copies it under the full track, so a 60-minute video costs minutes of CPU. Use whenever a video must be made from an album cover or still image, for a music track on YouTube, or with per-track variation across an album — "kapağı videoya çevir", "healing müzik videosu yap", "duman efekti ekle", "youtube için 1 saatlik video", "her parçaya farklı efekt", "ffmpeg ile duman/toz/ışık efekti", "lo-fi görsel yap", "sleep music videosu", "loop video hazırla", "spotify canvas". Trigger even when ffmpeg is never mentioned, if the deliverable is a video whose only footage is a still image plus effects. Pairs with retro-record-label and suno-composer.

- **Ölçü:** 9.829 bayt · 8 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/ambient-video-forge, ~/projects/reelsindustry/.claude/skills/ambient-video-forge, ~/projects/weftrecords/.claude/skills/ambient-video-forge, ~/Documents/GitHub/reelsindustry/.claude/skills/ambient-video-forge

## `chibi-character-factory`

[SKILL.md](chibi-character-factory/SKILL.md)

Production pipeline for building low-poly chibi game characters using Claude + Blender MCP only (no third-party generators), from parametric base mesh to a rigged, socketed, animated, USDZ-exported RealityKit asset for a turn-based iOS diorama game. Use this skill whenever the user works on game characters or drives Blender through MCP — creating or modifying a character, base mesh, armature/rig, equipment sockets, palette or materials, verification renders, silhouette tests, animations, USDZ/GLB export, or the factory scripts (build_character.py, characters/*.json). Trigger even for small requests like "make the hands bigger", "add a new enemy variant", "the export looks wrong in RealityKit", and whenever Warrior, Trickster, or enemies for the D&D-style iOS game are mentioned.

- **Ölçü:** 23.326 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `headless-reel-forge`

[SKILL.md](headless-reel-forge/SKILL.md)

Mass-produces 9:16 vertical physics Reels/Shorts/TikToks with no window, no editor and no display attached — a Rust rigid-body simulator (rapier) writes a motion cache, a headless Bevy/wgpu renderer replays it on Metal straight into ffmpeg, and impact audio is synthesised offline from the contact log. Use when the deliverable is a physics-driven short-form video or its machinery, and especially when the current pipeline is too slow, needs a window open, or forces a full render before you can tell whether a roll was any good. Trigger on "fizik motoruyla video üret", "arkaplanda video üretsin", "Godot çok yavaş", "simülasyon çok uzun sürüyor", "headless render", "GPU ile video üret", "toplu reels üret", "seed taraması", "prosedürel ses", "çarpışma sesi sentezle", "pencere açmadan render", "9:16 dikey video otomatik" — and whenever someone asks which engine to use for automated physics video, or how to render without opening an editor.

- **Ölçü:** 10.722 bayt · 12 ek dosya · referans dosyaları var
- **Kaynak:** ~/.claude/skills/headless-reel-forge, ~/.gemini/config/plugins/kirkit-skills/.claude/skills/headless-reel-forge, ~/.gemini/config/plugins/kirkit-skills/skills/headless-reel-forge, ~/projects/kirkit/data/skills/skills/headless-reel-forge

## `headless-reel-forge--instagram-reels`

[SKILL.md](headless-reel-forge--instagram-reels/SKILL.md)

Mass-produces 9:16 vertical physics Reels/Shorts/TikToks with no window, no editor and no display attached — a Rust rigid-body simulator (rapier) writes a motion cache, a headless Bevy/wgpu renderer replays it on Metal straight into ffmpeg, and impact audio is synthesised offline from the contact log. Use when the deliverable is a physics-driven short-form video or its machinery, and especially when the current pipeline is too slow, needs a window open, or forces a full render before you can tell whether a roll was any good. Trigger on "fizik motoruyla video üret", "arkaplanda video üretsin", "Godot çok yavaş", "simülasyon çok uzun sürüyor", "headless render", "GPU ile video üret", "toplu reels üret", "seed taraması", "prosedürel ses", "çarpışma sesi sentezle", "pencere açmadan render", "9:16 dikey video otomatik" — and whenever someone asks which engine to use for automated physics video, or how to render without opening an editor.

- **Ölçü:** 10.722 bayt · 17 ek dosya · referans dosyaları var
- **Kaynak:** ~/projects/instagram-reels/docs/headless-reel-forge

## `healing-audio-youtube-seo`

[SKILL.md](healing-audio-youtube-seo/SKILL.md)

Names and optimises functional-audio releases for YouTube — healing music, 432 Hz / 528 Hz / solfeggio, binaural and delta beds, sleep, meditation, study, spa, reiki, lo-fi, ambient — covering the track name, the search title, description, chapters, tags, hashtags, playlist and series architecture, plus the claim and duplication gates that keep a Suno-fed catalogue monetisable. Use whenever a track or long-form upload needs a title or rename, a batch needs a naming system, or titles need auditing for truncation, health-claim risk, false duration or templated repetition. Trigger on "şarkı ismi ne olsun", "youtube başlığı yaz", "432 hz videosuna isim", "healing music kanalı", "başlık optimizasyonu", "hangi keyword'ü hedefleyelim", "bu isim aratılır mı", "AI diye demonetize olur muyum", "seri isimlendirmesi", "playlist ismi", "uzun format başlığı". Use it even when someone only says "isim bul" or "başlık" about a music upload — on YouTube the name IS the distribution.

- **Ölçü:** 10.730 bayt · 7 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/healing-audio-youtube-seo, ~/projects/reelsindustry/.claude/skills/healing-audio-youtube-seo, ~/projects/weftrecords/.claude/skills/healing-audio-youtube-seo, ~/Documents/GitHub/reelsindustry/.claude/skills/healing-audio-youtube-seo

## `kling-video-uretim`

[SKILL.md](kling-video-uretim/SKILL.md)

Moonstone Residence için bir render ya da fotoğraftan fal.ai üzerinde Kling image-to-video ile kısa sinematik klip üretir ve bunu yayın Reels'ine çevirir: görseli okuyup çekim senaryosu yazar (kanca–gövde–kapanış, İngilizce Kling prompt'ları, Türkçe ekran metni, açıklama, etiket), görseli 9:16'ya hazırlar, fal kuyruğuna gönderir, klipleri künyesiyle indirir, marka katmanını (logo · tek satır başlık · "Temsili görseldir") güvenli alanda bindirir, ffmpeg/VideoToolbox ile birleştirip kapanış kartı ve müzik ekler. Şu ifadeler geçtiğinde kullan: "video üret", "hareketlendir", "render'ı videoya çevir", "Kling", "fal.ai", "image-to-video", "Reels videosu", "senaryo yaz", "bu fotoğraftan video", "drone hissi", "kamera hareketi", "klipleri birleştir", "video maliyeti". Kling ya da fal adı hiç geçmese bile bir görselden video üretilecekse devreye gir. Statik kare için `gorsel-uretim`, stok video için `pexels-gorsel-bulucu`, kural ve içerik için `moonstone-residence`.

- **Ölçü:** 11.143 bayt · 13 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/moonstone/.claude/skills/kling-video-uretim

## `physics-reel-forge`

[SKILL.md](physics-reel-forge/SKILL.md)

Builds and runs a rigid-body physics pipeline that mass-produces 9:16 vertical "satisfying physics" Reels/Shorts/TikToks on Apple Silicon — falling cubes, jointed chains whipping over a pivot, dominoes, ball-pit fills, tower collapses — via Godot+Jolt on Metal, deterministic Movie Maker capture, impulse-driven impact audio and VideoToolbox encoding. Use whenever the deliverable is a physics-driven short-form video or its machinery — scene recipes, chain tuning, seed sweeps, batch rendering, render speed, safe-zone framing, seamless loops, impact sound, export settings. Trigger on "fizik motoruyla video üret", "düşen küpler videosu", "zincir simülasyonu", "satisfying physics reels", "toplu video üret", "seed varyasyonu", "render çok yavaş", "9:16 dikey render", "çarpışma sesi ekle", "Godot ile video çıkar", "loop olacak video" — even when the user only says "viral video üretmek istiyorum" but the mechanism is a simulation, or asks whether to use Godot, Blender, Rapier or a custom Metal engine for this genre.

- **Ölçü:** 11.460 bayt · 10 ek dosya · referans dosyaları var
- **Kaynak:** ~/projects/instagram-reels/docs/physics-reel-forge, ~/Documents/GitHub/instagram-reels/docs/physics-reel-forge

## `procedural-game-audio`

[SKILL.md](procedural-game-audio/SKILL.md)

Build procedural (rule-generated, zero-asset) music and SFX engines for Apple-ecosystem apps — iOS/macOS/visionOS games and apps — using pure AVFoundation (AVAudioSourceNode), with a real-time-safe three-layer architecture (synth → sample-accurate clock → composer), adaptive intensity-driven themes, non-overlapping SFX, ducking, and crossfades. Use this skill whenever the user mentions procedural music, adaptive/dynamic game music, "prosedürel müzik", synthesizing audio without asset files, AVAudioSourceNode, AVAudioEngine render callbacks, chiptune/ambient generation in Swift, an AudioKit-vs-native decision, background music for a game, sound effects that "shouldn't overlap", or is debugging audio crackle, clicks, AudioConverter -302 errors, or "IOWorkLoop skipping cycle due to overload" — even if they don't say "procedural". Also use it when reviewing or extending an existing AVAudioSourceNode-based engine for real-time safety.

- **Ölçü:** 9.646 bayt · 1 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek), ~/Documents/GitHub/pipsworn/.claude/skills/procedural-game-audio, ~/Documents/GitHub/dietrying/.claude/skills/procedural-game-audio

## `retro-record-label`

[SKILL.md](retro-record-label/SKILL.md)

A full retro record label in one skill — names the release, art-directs and RENDERS period-accurate album covers at 3000×3000 (procedural plates or the user's own photo, run through halftone/duotone/riso/VHS/xerox treatments), then writes the globally optimised English release metadata — YouTube title, description, tags, hashtags and chapters, plus DSP-legal track and album titles. Use whenever someone needs cover art, an album or song name, or release copy — "albüm kapağı yap", "retro kapak tasarla", "şarkı ismi bul", "albüm ismi öner", "youtube açıklaması yaz", "single çıkaracağım", "kapak alternatifleri üret", "plak kapağı", "70ler tarzı kapak", "spotify kapak boyutu", "bu şarkıyı nasıl adlandırayım", "keyword'leri optimize et". Trigger even when the request covers only one department (just the name, just the cover, just the description), and whenever a track from suno-composer needs packaging for release.

- **Ölçü:** 9.897 bayt · 13 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/retro-record-label, ~/projects/weftrecords/.claude/skills/retro-record-label

## `shorts-strategy`

[SKILL.md](shorts-strategy/SKILL.md)

Format seçimi ve yayın temposu kuralları — yeni bir video/seri fikri değerlendirilirken veya yayın planlanırken uygula

- **Ölçü:** 2.630 bayt · 0 ek dosya
- **Kaynak:** ~/projects/instagram-reels/.claude/skills/shorts-strategy

## `stock-footage-forge`

[SKILL.md](stock-footage-forge/SKILL.md)

Builds YouTube Shorts (9:16, 1080x1920) and full music videos (16:9) by cutting royalty-free Pexels STOCK VIDEO clips to an existing music track — center-crop/fps normalization, xfade assembly, bar-aligned audio segment with two-pass -14 LUFS loudnorm, safe-area title card, fast h264_videotoolbox render. Use whenever a music release needs a vertical Short, a Reel/TikTok, a promo clip cut from stock footage, or a music video whose footage is real video (not a still cover with effects — that is ambient-video-forge). Trigger on "shorts yap", "shorts üret", "dikey video", "reels", "tiktok videosu", "stok videodan klip", "pexels videolarından video", "müzik videosu kur", "tanıtım klibi", "9:16", and whenever a track needs promotion on the Shorts feed. Pairs with pexels-media-scout (finds the clips) and healing-audio-youtube-seo (titles the upload).

- **Ölçü:** 6.085 bayt · 5 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/projects/reelsindustry/.claude/skills/stock-footage-forge, ~/projects/weftrecords/.claude/skills/stock-footage-forge, ~/Documents/GitHub/reelsindustry/.claude/skills/stock-footage-forge

## `suno-composer`

[SKILL.md](suno-composer/SKILL.md)

Composes a song as a trained musician would — key/mode, tempo, meter, harmonic plan, form with bar counts, arrangement and vocal tessitura — then translates those decisions into a Suno-ready Style field, Exclude field and metatagged lyrics. Use this whenever someone wants a song, a Suno prompt, a style/song description, lyrics for an AI music tool, an instrumental bed, a jingle, an intro theme, game or app background music, or wants an existing prompt diagnosed ("why does my Suno track sound generic / rushed / wrong genre / like AI"). Trigger on Turkish phrasings too — "şarkı yaz", "suno prompt'u üret", "song description hazırla", "beste yap", "müzik promptu", "jingle lazım", "oyunuma müzik", "şu prompt neden kötü çıkıyor", "enstrümantal parça", "sözlerini de yaz". Use it even when the person never says "Suno" — if the deliverable is a text description that some model turns into music, this applies.

- **Ölçü:** 10.678 bayt · 3 ek dosya · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/suno-composer, ~/projects/weftrecords/.claude/skills/suno-composer

## `weft-channel`

[SKILL.md](weft-channel/SKILL.md)

Weft Records YouTube kanalını yükleme SONRASINDA yönetir — Studio analitiklerini okumak, sayıları kataloğa yazmak, topluluk (Community) duyurusu geçmek, oynatma listesi/bitiş ekranı/sabitlenmiş yorum kurmak, yorumları yanıtlamak, kanal açıklaması ve anahtar kelimelerini güncellemek, düşük performansta başlık/thumbnail müdahalesine karar vermek. Kanal işleri Chrome eklentisiyle studio.youtube.com üzerinden sürülür. Tetikleyiciler: "kanala bak", "analitik", "youtube studio", "kaç görüntüleme", "views ölç", "CTR", "duyuru geç", "community post", "topluluk gönderisi", "oynatma listesi", "playlist", "bitiş ekranı", "sabitlenmiş yorum", "yorumlara bak", "abone", "kanal açıklaması", "başlığı değiştir", "thumbnail değiştir", "video yayınlandı sonra ne yapacağız", "+30 gün ölçümü". Bir video YouTube'a yüklendikten sonraki HER iş bu skill'e aittir.

- **Ölçü:** 8.107 bayt · 8 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/projects/reelsindustry/.claude/skills/weft-channel, ~/projects/weftrecords/.claude/skills/weft-channel, ~/Documents/GitHub/reelsindustry/.claude/skills/weft-channel

## `weft-channel--weftrecords-gh`

[SKILL.md](weft-channel--weftrecords-gh/SKILL.md)

Weft Records YouTube kanalını yükleme SONRASINDA yönetir — Studio analitiklerini okumak, sayıları kataloğa yazmak, topluluk (Community) duyurusu geçmek, oynatma listesi/bitiş ekranı/sabitlenmiş yorum kurmak, yorumları yanıtlamak, kanal açıklaması ve anahtar kelimelerini güncellemek, düşük performansta başlık/thumbnail müdahalesine karar vermek. Kanal işleri Chrome eklentisiyle studio.youtube.com üzerinden sürülür. Tetikleyiciler: "kanala bak", "analitik", "youtube studio", "kaç görüntüleme", "views ölç", "CTR", "duyuru geç", "community post", "topluluk gönderisi", "oynatma listesi", "playlist", "bitiş ekranı", "sabitlenmiş yorum", "yorumlara bak", "abone", "kanal açıklaması", "başlığı değiştir", "thumbnail değiştir", "video yayınlandı sonra ne yapacağız", "+30 gün ölçümü". Bir video YouTube'a yüklendikten sonraki HER iş bu skill'e aittir.

- **Ölçü:** 8.107 bayt · 8 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/weft-channel

## `weft-release`

[SKILL.md](weft-release/SKILL.md)

Weft Records etiketinin uçtan uca yayın hattını yürütür — yeni sanatçı kimliği açma, yayın brief'i, Suno bestesi, retro kapak, yayın metadata'sı ve katalog kaydı. Bu repoda müzik, sanatçı, albüm, kapak, prompt veya katalog ile ilgili HER iş bu skill ile başlar. Tetikleyiciler: "yeni sanatçı", "yeni albüm aç", "WR-0NN", "şarkı üretelim", "kapak yap", "prompt logla", "kataloğa ekle", "yayına hazırla", "roster", "bu sanatçının tarzı", "albüm çıkaralım", "metadata yaz", "excel'i güncelle". Sanatçı kimliğinin şeridini korumak ve her üretim denemesini loglamak bu skill'in birincil görevidir.

- **Ölçü:** 3.763 bayt · 0 ek dosya
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/weft-release, ~/projects/weftrecords/.claude/skills/weft-release

