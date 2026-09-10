using System;
using System.IO;
using UnityEngine;

namespace CharacterPipeline
{
    // Mirrors <Name>.character.json written by char_lib.stage_export (schema blender-unity-character/1).
    // Field names are snake_case on purpose: JsonUtility maps them 1:1.
    [Serializable] public class ManifestEvent { public string name; public int frame; }

    [Serializable]
    public class ManifestClip
    {
        public string name;
        public string file;
        public int frames;
        public int fps = 30;
        public bool loop;
        public bool root_motion;
        public float speed_mps;
        public ManifestEvent[] events = new ManifestEvent[0];
        public string state;
    }

    [Serializable]
    public class CharacterManifest
    {
        public string schema;
        public string name;
        public string rig_type = "humanoid";   // humanoid | generic
        public float height_m;
        public int fps = 30;
        public string model;
        public ManifestClip[] clips = new ManifestClip[0];
        public string unity_folder;
        public string root_bone = "Root";
        public string[] sockets = new string[0];   // SKT_* bones for equipment
        public bool mesh_lods;                  // Unity 6.2+: generate Mesh LODs on import

        public bool IsHumanoid => rig_type == null || rig_type.ToLowerInvariant() != "generic";

        public static CharacterManifest Load(string path)
        {
            var m = JsonUtility.FromJson<CharacterManifest>(File.ReadAllText(path));
            if (m == null || string.IsNullOrEmpty(m.name))
                throw new InvalidDataException($"Not a character manifest: {path}");
            if (string.IsNullOrEmpty(m.unity_folder)) m.unity_folder = $"Assets/Characters/{m.name}";
            return m;
        }

        /// <summary>Manifest that governs an asset path (Name.fbx or Name@Clip.fbx), or null.</summary>
        public static CharacterManifest ForAsset(string assetPath, out string manifestPath)
        {
            manifestPath = null;
            if (!assetPath.EndsWith(".fbx", StringComparison.OrdinalIgnoreCase)) return null;
            var dir = Path.GetDirectoryName(assetPath)?.Replace('\\', '/');
            var baseName = Path.GetFileNameWithoutExtension(assetPath);
            var charName = baseName.Split('@')[0];
            var candidate = $"{dir}/{charName}.character.json";
            if (!File.Exists(candidate)) return null;
            manifestPath = candidate;
            try { return Load(candidate); } catch { return null; }
        }

        public ManifestClip ClipForFile(string assetPath)
        {
            var file = Path.GetFileName(assetPath);
            foreach (var c in clips) if (string.Equals(c.file, file, StringComparison.OrdinalIgnoreCase)) return c;
            return null;
        }

        public string ModelAssetPath => $"{unity_folder}/{model}";
    }
}
