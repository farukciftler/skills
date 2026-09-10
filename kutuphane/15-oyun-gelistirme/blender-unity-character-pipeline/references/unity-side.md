# Unity side reference

Read this when installing the importer scripts, importing/verifying a
character, wiring it into gameplay, or debugging anything that looks wrong
in Unity. Works with the official Unity plugin for Claude Code (Unity CLI +
`com.unity.pipeline` live-Editor control); falls back to batch mode or the
menu when no live Editor is reachable. For CLI mechanics (install, status,
Safe Mode recovery) defer to the `unity-cli` skill.

## 1. Install the scripts into the project (once)

Copy from this skill's `assets/unity/` into the project:

```
Assets/CharacterPipeline/Runtime/   CharacterAnimEvents.cs, CharacterSpeedDriver.cs, CharacterPipeline.Runtime.asmdef
Assets/CharacterPipeline/Editor/    CharacterManifest.cs, CharacterModelPostprocessor.cs, CharacterImporter.cs, CharacterPipeline.Editor.asmdef
Assets/CharacterPipeline/EditorCli/ CharacterPipelineCommands.cs, CharacterPipeline.Cli.asmdef
```

Why three assemblies: the CLI commands reference `Unity.Pipeline`. Their
asmdef has a `versionDefines` entry on `com.unity.pipeline` plus a
`defineConstraints` on the resulting symbol, so the assembly is simply not
compiled when the package is absent. A hard reference in a normal script
would be a compile error → Editor boots into **Safe Mode** → the Pipeline
server can't load → the agent is locked out. Never put `using
Unity.Pipeline...` outside that assembly.

After copying: if a live Editor is connected, `unity command recompile`
(poll `unity command recompile_status`), then `unity list` should show
`import_character` and `verify_character`. If the Pipeline package is
missing: `unity pipeline install --project-path <project>`.

## 2. Import & verify

Order matters (the importer handles it): manifest → model (creates Avatar)
→ clips (copy that Avatar) → generic root path (generic rigs) →
AnimatorController → prefab → verify.

| Situation | Command |
|---|---|
| Live Editor (`unity status` shows `ready`) | `unity command import_character --manifest /abs/Characters/Knight/exports/Knight.character.json` |
| Re-check only | `unity command verify_character --manifest <same path>` |
| No live Editor / CI | `unity run <project> -- -executeMethod CharacterPipeline.CharacterBatch.ImportFromCommandLine -manifest <abs path>` → exit 0/1, log line `CHARACTER_PIPELINE_REPORT {json}` (parse with `--format ndjson`) |
| Human in the loop | Menu **Tools → Character Pipeline → Import Manifest…** |

Both commands return a JSON report: `ok`, `avatar_valid`, `avatar_human`,
`measured_height_m`, `clips[]`, `issues[]`. Treat any issue as a failed gate.

Screenshot check after import: drop the prefab in a scene
(`unity command create_gameobject` / `eval` if exposed), then
`unity command screenshot --output ./shot.png --width 1280 --height 720`
and look at it. Play-mode check: `unity command editor_play`, set the
`Speed` parameter or fire a trigger via `eval`, screenshot again.

Re-export loop: re-run Blender export → re-run `import_character`. It is
idempotent (overwrites FBX, rebuilds controller, keeps the prefab GUID).

## 3. What the postprocessor enforces (and why)

Applies to any FBX sitting next to `<Name>.character.json`:

| Setting | Value | Reason |
|---|---|---|
| `useFileScale`, `globalScale` | true, 1 | Blender exported FBX_SCALE_ALL |
| `bakeAxisConversion` | true | converts axes in data, not via a −90° root rotation |
| `animationType` | Human / Generic (manifest) | |
| model: `avatarSetup` | CreateFromThisModel | T-pose rest from Blender |
| clips: `avatarSetup` + `sourceAvatar` | CopyFromOther = model avatar | clip files have no mesh |
| `skinWeights` | Standard (4) | Blender limited to 4 |
| `optimizeGameObjects` | false | sockets/bones stay reachable (turn on for crowds; expose sockets explicitly) |
| `materialImportMode` | model: ImportViaMaterialDescription, clips: None | |
| clip: name / loop | from manifest | take "Scene" → real clip name |
| clip: root motion | rotation & Y baked (Original); XZ baked only if in-place | see animation-craft §4 |
| clip: events | `OnAnimEvent(name)`, normalized time, DontRequireReceiver | single receiver component |
| `animationCompression` | Optimal | |
| `generateMeshLods` (6.2+) | manifest `mesh_lods` | |

`GetVersion()` is bumped whenever the logic changes → Unity reimports.

## 4. Generated assets

- `Name.controller`: float `Speed`; default state **Locomotion** = 1D blend
  tree of all looping clips at their real speeds (Idle 0, Walk 1.13, Run
  2.52…); one **trigger per one-shot clip** (`Attack`, `Hit`) with Any State
  → clip → back to Locomotion at 90%.
  Extend by hand or ask for layers (upper-body attack mask, additive hit).
  Death should become a terminal state (remove its exit transition).
- `Name.prefab`: prefab variant of the model, Animator (avatar + controller,
  `applyRootMotion` = any root-motion clip), `CharacterAnimEvents`.

## 5. Runtime usage

```csharp
// in-place locomotion: move with a CharacterController, feed real speed
gameObject.AddComponent<CharacterPipeline.CharacterSpeedDriver>();
// one-shots
animator.SetTrigger("Attack");
// gameplay events
GetComponent<CharacterPipeline.CharacterAnimEvents>().Fired += e => {
    if (e == "Hit") DealDamage();
    else if (e.StartsWith("Footstep")) PlayFootstep();
};
// equipment on sockets
var hand = transform.Find("RIG_Knight/Root/Hips/Spine/Chest/UpperChest/RightShoulder/RightUpperArm/RightLowerArm/RightHand/SKT_Hand_R");
// humanoid alternative: animator.GetBoneTransform(HumanBodyBones.RightHand)
```
Foot IK on uneven ground: enable **IK Pass** + `OnAnimatorIK` or the
Animation Rigging package (`com.unity.animation.rigging`, Two Bone IK
constraints on the legs) — install via `unity-package-management` skill.

Unity's "new animation system" preview was put on pause (Unite 2025
roadmap); Mecanim/Animator is the production target in 2026.

## 6. Troubleshooting (Unity)

| Symptom | Cause → fix |
|---|---|
| `unity command` can't connect, Editor is open | Safe Mode from compile errors → `unity pipeline list`, fix C#, restart (unity-cli skill) |
| `import_character` not listed | scripts not recompiled, or `com.unity.pipeline` missing → CLI asmdef skipped; use batch/menu or install package |
| Root child rotated −90° X / scale 100 | FBX not exported with FBX_SCALE_ALL, or postprocessor didn't run (manifest not next to FBX / wrong name) |
| Avatar invalid / red bones | bone names changed, missing required bone, A-pose too far from T, two root bones |
| Clip named "Scene", no loop | clip FBX not listed in manifest (`file` mismatch) → postprocessor skipped it |
| Clips play but character floats/sinks | origin not at feet in Blender; or Y root motion not baked |
| Character slides on ground (in-place) | Animator `Speed` ≠ real velocity; use `CharacterSpeedDriver` or match move speed to `speed_mps` |
| Character drifts/rotates over time (root motion) | rotation not baked; check clip `lockRootRotation` true |
| Humanoid clip looks different from Blender | expected small muscle-space differences; for exact playback use Generic |
| Sockets missing | `optimizeGameObjects` on, or socket bone exported non-deform |
| "AnimationEvent has no receiver" | prefab lacks `CharacterAnimEvents` (events use DontRequireReceiver, so only on custom setups) |
