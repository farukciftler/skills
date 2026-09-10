# Driving Unity from Claude (Unity CLI / pipeline / MCP)

Assumes the official Unity CLI (`unity`) and — for live control — `com.unity.pipeline` in the project. The
`unity-cli` skill of the Unity plugin is the full command reference; this file is the tilemap-specific playbook.

## Contents
1. Detect the situation · 2. Install the package into the project · 3. Assets & tiles · 4. Generate/validate/look loop
5. Tests & CI · 6. No Editor at all · 7. Troubleshooting

## 1. Detect the situation
```bash
unity --version                                   # CLI present?
cat <project>/ProjectSettings/ProjectVersion.txt  # Editor version
grep -E 'tilemap|pipeline|render-pipelines' <project>/Packages/manifest.json
unity status --format json                        # GUI Editor "ready"?  (headless batch Editors don't show here)
unity command --project-path <project>            # lists commands if a Pipeline server answers
unity pipeline list --format json                 # Safe Mode (compile errors) detection
```
- Live Editor reachable → drive it (sections 2–4). Never hand-edit scene/asset YAML while it's live.
- No `com.unity.pipeline` → `unity pipeline install --project-path <project>` (ask the user first; it edits manifest.json).
- Safe Mode → fix the `error CS####` lines from the Editor log first; nothing below works until it compiles.
- MCP instead of CLI: `unity mcp configure claude` exposes the same Editor commands as MCP tools; the `pgen_*`
  commands appear there too once registered.

## 2. Install the package into the project
Copy files (plain filesystem ops — scripts aren't scene YAML):
```bash
SKILL=<abs path to platformer-tilemap-gen>; P=<project>
mkdir -p "$P/Assets/PlatformerGen/Generated"
cp -r "$SKILL/scripts/Runtime"         "$P/Assets/PlatformerGen/Runtime"
cp -r "$SKILL/scripts/Editor"          "$P/Assets/PlatformerGen/Editor"
cp -r "$SKILL/scripts/Editor.Pipeline" "$P/Assets/PlatformerGen/Editor.Pipeline"
cp -r "$SKILL/scripts/Tests.Editor"    "$P/Assets/PlatformerGen/Tests"
cp "$SKILL"/assets/*.txt               "$P/Assets/PlatformerGen/Generated/"
```
Then recompile and confirm registration:
```bash
unity command recompile --project-path "$P"
unity command recompile_status --project-path "$P"      # poll until completed
unity list --project-path "$P" --format json | grep pgen_   # pgen_setup, pgen_defaults, pgen_generate, pgen_validate, pgen_ascii, pgen_sweep
```
If `pgen_*` are missing but the project compiled: the pipeline package is absent (the Editor.Pipeline assembly is
compiled only with it) — the menu `Tools > PlatformerGen` still works, and `eval` can call `PlatformerGenOps` directly.

## 3. Assets & tiles
```bash
unity command pgen_defaults --project-path "$P"          # TileLegend + Config_RoomGrid + Config_ChunkStitch
unity command pgen_setup    --project-path "$P"          # Grid + 5 tilemaps + colliders in the active scene
```
Find tile assets and wire the legend (eval runs C# in the Editor; availability depends on the pipeline version —
check `unity command` output; if absent, write a tiny Editor script with a `[MenuItem]` or `[CliCommand]` instead):
```bash
unity command eval 'return string.Join("\n", System.Linq.Enumerable.Select(UnityEditor.AssetDatabase.FindAssets("t:TileBase"), g => UnityEditor.AssetDatabase.GUIDToAssetPath(g)));' --project-path "$P"

unity command eval '
var L = UnityEditor.AssetDatabase.LoadAssetAtPath<PlatformerGen.Integration.TileLegend>("Assets/PlatformerGen/Generated/TileLegend.asset");
System.Func<string, UnityEngine.Tilemaps.TileBase> T = p => UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.Tilemaps.TileBase>(p);
L.Find(PlatformerGen.Cell.Solid).tile  = T("Assets/Tiles/Ground_RuleTile.asset");
L.Find(PlatformerGen.Cell.OneWay).tile = T("Assets/Tiles/Platform.asset");
L.Find(PlatformerGen.Cell.Hazard).tile = T("Assets/Tiles/Spikes.asset");
L.Find(PlatformerGen.Cell.Ladder).tile = T("Assets/Tiles/Ladder.asset");
UnityEditor.EditorUtility.SetDirty(L); UnityEditor.AssetDatabase.SaveAssets();
return string.Join(";", L.MissingAssignments());' --project-path "$P"
```
No RuleTile yet? Use the Unity plugin skills `sprite-segment-3x3grid` + `tilemap-ruletile-createfromsegment` on the
user's tileset sprites, then point `Solid` at the result.
Set the movement profile on the config the same way (`cfg.jumpHeightTiles = ...; SetDirty; SaveAssets`) using numbers
read from the player controller.

## 4. Generate / validate / look loop
```bash
C=Assets/PlatformerGen/Generated/Config_RoomGrid.asset
unity command pgen_generate --config $C --seed 7 --project-path "$P" --format json   # writes scene, returns ReportDto JSON
unity command screenshot --output /tmp/level_7.png --width 1920 --height 1080 --project-path "$P"
unity command pgen_sweep --config $C --count 100 --project-path "$P"                  # tuning: firstTryPassRate > 0.9
unity command pgen_generate --config $C --seed 7 --dry_run true --project-path "$P"   # validate only, scene untouched
unity command pgen_validate --config $C --project-path "$P"                           # validate what's painted now
unity command pgen_ascii --project-path "$P"                                          # scene -> ASCII for reasoning/diffs
unity command save_scene --project-path "$P"
```
Look at the screenshot every time tiles/legend/rendering changed: ASCII proves reachability; only pixels prove that
RuleTiles resolved, spikes face the right way, sorting and camera are right. Frame the level first if needed
(e.g. eval: move Main Camera to the level centre, set orthographicSize to fit).
Report to the user: config + seed, pass/coverage/jumps, screenshot, and anything in `problems`.

## 5. Tests & CI
```bash
unity test "$P" --mode EditMode --report-format junit --output ./pgen-tests.xml --timeout 600   # exit 6 = failures
unity run "$P" --command pgen_sweep --format ndjson -- --config $C --count 200                  # one-shot, no warm Editor
```

## 6. No Editor at all (still useful)
Everything in Core runs under plain Mono/.NET, so levels, templates and the validator can be developed before Unity
is even open:
```bash
cd <skill>; mcs -out:/tmp/h.exe tools/CoreHarness.cs $(find scripts/Runtime/Core -name '*.cs')
mono /tmp/h.exe assets                    # full suite: validator cases, determinism, 100-seed stats per generator
mono /tmp/h.exe render room 7 assets      # one level + room layout + overlay
mono /tmp/h.exe failures chunk assets     # first failing seeds with overlays (tuning)
mono /tmp/h.exe validate my_level.txt     # any ASCII level
```
(`apt-get install mono-mcs mono-runtime` if missing; with dotnet, put the same files in a console project.)
When the harness profile differs from the game, edit `P1` at the top of `CoreHarness.cs`.

## 7. Troubleshooting
| Symptom | Fix |
|---|---|
| `pgen_generate` → "TileLegend incomplete" | assign Solid/OneWay/Hazard/Ladder tiles (section 3) |
| Level written but invisible | tiles have no sprite, wrong sorting layer, camera elsewhere → screenshot + select Ground tilemap |
| Player falls through | Rigidbody2D on player, layers in Physics2D matrix, composite has geometry (pgen writes Manual→Generate) |
| Snags on flat ground | a tilemap lost its `compositeOperation = Merge` (re-run `pgen_setup`) |
| One-way solid from below | `usedByEffector` must be on the **CompositeCollider2D**, effector `useOneWay` on |
| Lines between tiles | atlas + padding, point filter, pixel-perfect camera (`2d-pixel-perfect` skill) |
| Commands time out after edits | domain reload / compile — poll `recompile_status`, check Safe Mode |
