// Registers the importers as Unity CLI commands (Unity's official Claude Code plugin / com.unity.pipeline).
// Compiled ONLY when com.unity.pipeline is installed (UCA_PIPELINE comes from UCA.Editor.asmdef versionDefines),
// so a project without the package never drops into Safe Mode because of this file.
//   unity command recompile  ->  unity list | grep uca_  ->  unity command uca_pixel_import --sheet ...
#if UCA_PIPELINE
using Unity.Pipeline.Commands;

namespace UCA.Editor
{
    public static class UcaCliCommands
    {
        [CliCommand("uca_pixel_import", "Import a uca-sheet/1 pixel character: Point-filtered sprites, sliced frames, AnimationClips with events, platformer Animator Controller, prefab (Rigidbody2D + capsule + driver). Idempotent.")]
        public static string PixelImport(
            [CliArg("sheet", "Project-relative path to <name>_sheet.json (the PNG must sit next to it)")] string sheet,
            [CliArg("out", "Output folder for clips/controller (default: <sheet dir>/Animations)")] string @out = "",
            [CliArg("ppu", "Pixels per unit override (0 = use the sheet's ppu)")] string ppu = "0",
            [CliArg("prefab", "true/false: create the prefab")] string prefab = "true",
            [CliArg("physics", "true/false: add Rigidbody2D, CapsuleCollider2D and PlatformerAnimatorDriver")] string physics = "true")
        {
            int.TryParse(ppu, out int p);
            return PixelCharacterImporter.Run(sheet, @out, p, prefab != "false", physics != "false");
        }

        [CliCommand("uca_3d_import", "Import a uca-3d/1 manifest + FBX: explicit Humanoid avatar, in-place looped clips with events, palette material, locomotion blend-tree controller, prefab with CharacterController. Reports avatar validity, root rotation, height, facing.")]
        public static string Import3D(
            [CliArg("manifest", "Project-relative path to <name>.manifest.json (FBX and palette PNG next to it)")] string manifest,
            [CliArg("out", "Output folder for material/controller (default: <manifest dir>/Animations)")] string @out = "",
            [CliArg("prefab", "true/false: create the prefab")] string prefab = "true",
            [CliArg("controller", "true/false: build the Animator Controller")] string controller = "true")
        {
            return Character3DImporter.Run(manifest, @out, prefab != "false", controller != "false");
        }
    }
}
#endif
