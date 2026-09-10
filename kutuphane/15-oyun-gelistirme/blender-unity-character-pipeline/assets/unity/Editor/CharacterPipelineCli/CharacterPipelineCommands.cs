#if HAS_UNITY_PIPELINE
using Unity.Pipeline.Commands;   // [CliCommand]/[CliArg] - assembly Unity.Pipeline (com.unity.pipeline)

namespace CharacterPipeline
{
    // Compiled ONLY when com.unity.pipeline is installed (asmdef versionDefines +
    // defineConstraints), so a project without the package never breaks into Safe Mode.
    public static class CharacterPipelineCommands
    {
        // unity command import_character --manifest /abs/path/Knight.character.json
        [CliCommand("import_character", "Import a Blender character manifest: copy FBX files, avatar, clips, controller, prefab",
                    MainThreadRequired = true)]
        public static string ImportCharacter([CliArg("manifest", "Absolute path to <Name>.character.json")] string manifest)
            => CharacterImporter.Import(manifest);

        // unity command verify_character --manifest /abs/path/Knight.character.json
        [CliCommand("verify_character", "Verify an imported character against its manifest (avatar, clips, scale, axes)",
                    MainThreadRequired = true)]
        public static string VerifyCharacter([CliArg("manifest", "Path to <Name>.character.json")] string manifest)
            => CharacterImporter.Verify(manifest);
    }
}
#endif
