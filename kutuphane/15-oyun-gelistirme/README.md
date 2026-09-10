# Oyun Geliştirme

2D/3D oyun üretimi: pixel ve Blender karakter animasyonu, Unity aktarımı, anlatı tasarımı, ücretsiz asset keşfi ve lisans denetimi.

4 skill. Üst dizin: [../../README.md](../../README.md)

## `blender-unity-character-pipeline`

[SKILL.md](blender-unity-character-pipeline/SKILL.md)

Build game-ready 3D characters and their animations in Blender (driven via Blender MCP or headless bpy) and land them in Unity through the official Unity plugin/CLI - humanoid T-pose rig with Unity bone names, procedural blockout or user/AI mesh fitting, skinning, IK-driven walk/run cycles with zero foot slide, idle, pose-to-pose attacks/hit reacts, animation events, per-clip FBX export, round-trip verification, then Unity avatar, clip settings, blend-tree Animator Controller and prefab via `unity command import_character`. Use whenever the user wants to create, rig, skin or animate a 3D game character, make a walk/run/idle/attack animation, export Blender to Unity, fix FBX scale/rotation/avatar/root-motion problems, or retarget humanoid clips - including Turkish requests like "karakter oluştur", "animasyon yap", "yürüme animasyonu", "rig et", "Blender'dan Unity'ye aktar", "karakteri Unity'e al", "3D oyun karakteri". Not for 2D sprites or RealityKit/USDZ chibi (chibi-character-factory).

- **Ölçü:** 11.304 bayt · 17 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `narrative-platformer-design`

[SKILL.md](narrative-platformer-design/SKILL.md)

Narrative designer + game writer for story-driven 2D platformers (Celeste / Inside / Gris / Hollow Knight / Ori tier). Builds the story out of the core verbs (mechanics-as-metaphor), chapter and level structure, beat charts that sync story beats with difficulty and flow, human-sounding English dialogue (subtext, voice bibles, barks, reactive lines, speech-bubble limits), wordless/environmental storytelling, storyboards and in-engine animatic specs; audits existing scripts with bundled lint tools for AI-tells, exposition and pacing breaks. Use whenever the user writes or designs story, characters, dialogue, cutscenes, level pacing or storyboards for a 2D platformer, metroidvania or side-scroller, even if they only say 'hikaye yaz', 'diyalogları doğal yap', 'senaryo', 'bölüm akışı', 'storyboard hazırla', 'oyun kurgusu', 'sürükleyici olsun', 'AI gibi durmasın', 'NPC konuşması', 'cutscene', 'beat chart', or paste a script to review.

- **Ölçü:** 13.252 bayt · 14 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `oyun-asset-kesif`

[SKILL.md](oyun-asset-kesif/SKILL.md)

Ücretsiz oyun asset'i (3D model, PBR texture/materyal, HDRI, 2D sprite, SFX, müzik, animasyon) bulan, lisansını ticari kullanım ve App Store açısından denetleyen, indirip Unity/RealityKit/Godot'a sokan ve CREDITS kaydı tutan uzman. Poly Haven, ambientCG, Poly Pizza, Sketchfab, Freesound API'lerini script ile tek seferde arar; Kenney, Quaternius, OpenGameArt, itch.io, Unity Asset Store free, Fab giveaway gibi API'siz kaynakları web aramasıyla tarar; asset MCP sunucularını (Sketchfab MCP, Poly Pizza MCP, Blender MCP, toplayıcı MCP'ler) kurar. Kullanıcı "free asset", "ücretsiz model/texture/ses", "CC0", "low poly model bul", "şu sahne için asset", "Asset Store'da bedava", "Sketchfab'dan indir", "HDRI lazım", "ses efekti bul", "müzik lazım", "lisansı uygun mu", "App Store'da kullanabilir miyim", "credits nasıl yazılır", "asset MCP" dediğinde; bir oyun sahnesi/prototip için görsel veya ses kaynağı gerektiğinde — "asset" kelimesi geçmese bile — kullan. Lisansı ASLA varsayma; her asset'in lisansını kaynağından oku.

- **Ölçü:** 8.007 bayt · 6 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `pixel-platformer-animator`

[SKILL.md](pixel-platformer-animator/SKILL.md)

Creates pixel-art character sprite animations for 2D platformer games and wires them into Unity 6 — generates a full side-view animation set (idle, run, jump, apex, fall, land, crouch, wall slide, dash, attack, hurt, death) as a validated sprite sheet with per-frame timing and events, or takes the user's own Aseprite/PNG art, then imports it through the official Unity plugin workflow (unity-cli eval) into sliced sprites, AnimationClips, a platformer Animator Controller, a runtime driver and a ready prefab. Use whenever the user wants a player/enemy sprite, sprite sheet, run cycle, jump or attack animation, Animator setup for a platformer, or asks why a pixel character floats, jitters, blurs, slides when flipping or skips frames — even if they never say "animation". Trigger on Turkish phrasings like "pixel karakter", "sprite animasyonu", "koşma animasyonu", "platform oyunu karakteri", "sprite sheet oluştur", "Animator kur", "karakter zıplamıyor gibi görünüyor".

- **Ölçü:** 7.423 bayt · 11 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

