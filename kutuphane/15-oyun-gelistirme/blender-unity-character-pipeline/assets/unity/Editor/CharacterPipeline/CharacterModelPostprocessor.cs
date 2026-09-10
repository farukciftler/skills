using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEngine;

namespace CharacterPipeline
{
    /// <summary>
    /// Enforces pipeline import settings for any FBX that sits next to a
    /// <Name>.character.json manifest. Runs on every (re)import, so settings
    /// can't drift when someone re-exports from Blender.
    /// </summary>
    public class CharacterModelPostprocessor : AssetPostprocessor
    {
        public override uint GetVersion() => 3;   // bump when logic changes -> forces reimport

        void OnPreprocessModel()
        {
            var m = CharacterManifest.ForAsset(assetPath, out _);
            if (m == null) return;
            var mi = (ModelImporter)assetImporter;
            var clip = m.ClipForFile(assetPath);
            bool isModel = clip == null;

            // Scale / axes: Blender exported with FBX_SCALE_ALL, -Z fwd, Y up.
            mi.globalScale = 1f;
            mi.useFileScale = true;
            mi.bakeAxisConversion = true;     // no -90 X on the root transform
            mi.importBlendShapes = true;
            mi.skinWeights = ModelImporterSkinWeights.Standard; // 4 bones/vertex (Blender limited to 4)
            mi.optimizeGameObjects = false;   // keep bones reachable for sockets/IK
            mi.materialImportMode = isModel ? ModelImporterMaterialImportMode.ImportViaMaterialDescription
                                            : ModelImporterMaterialImportMode.None;
            mi.importCameras = false;
            mi.importLights = false;
#if UNITY_6000_2_OR_NEWER
            if (isModel) mi.generateMeshLods = m.mesh_lods;
#endif
            mi.animationType = m.IsHumanoid ? ModelImporterAnimationType.Human
                                            : ModelImporterAnimationType.Generic;
            if (isModel)
            {
                mi.avatarSetup = ModelImporterAvatarSetup.CreateFromThisModel;
                mi.importAnimation = false;
            }
            else
            {
                mi.importAnimation = true;
                mi.animationCompression = ModelImporterAnimationCompression.Optimal;
                mi.resampleCurves = true;
                var avatar = AssetDatabase.LoadAllAssetsAtPath(m.ModelAssetPath).OfType<Avatar>().FirstOrDefault();
                if (avatar != null)
                {
                    mi.avatarSetup = ModelImporterAvatarSetup.CopyFromOther;
                    mi.sourceAvatar = avatar;
                }
                else
                {
                    // Model not imported yet: CharacterImporter re-imports clips after the model.
                    mi.avatarSetup = ModelImporterAvatarSetup.CreateFromThisModel;
                }
            }
        }

        void OnPreprocessAnimation()
        {
            var m = CharacterManifest.ForAsset(assetPath, out _);
            if (m == null) return;
            var clip = m.ClipForFile(assetPath);
            if (clip == null) return;
            var mi = (ModelImporter)assetImporter;
            var defaults = mi.defaultClipAnimations;
            if (defaults == null || defaults.Length == 0) return;

            var src = defaults[0];                 // Blender writes one take per file ("Scene")
            var c = new ModelImporterClipAnimation
            {
                name = clip.name,
                takeName = src.takeName,
                firstFrame = src.firstFrame,
                lastFrame = src.lastFrame,
                loopTime = clip.loop,
                loopPose = clip.loop,
                // Rotation: always baked (clips are authored facing forward).
                lockRootRotation = true,
                keepOriginalOrientation = true,
                // Height: baked, original -> pelvis bob stays in the pose.
                lockRootHeightY = true,
                keepOriginalPositionY = true,
                // XZ: baked for in-place clips; free for root-motion clips.
                lockRootPositionXZ = !clip.root_motion,
                keepOriginalPositionXZ = true,
                events = BuildEvents(clip),
            };
            mi.clipAnimations = new[] { c };
        }

        static AnimationEvent[] BuildEvents(ManifestClip clip)
        {
            var list = new List<AnimationEvent>();
            if (clip.events == null || clip.frames <= 0) return list.ToArray();
            foreach (var e in clip.events)
                list.Add(new AnimationEvent
                {
                    functionName = "OnAnimEvent",   // CharacterAnimEvents receiver
                    stringParameter = e.name,
                    time = Mathf.Clamp01(e.frame / (float)clip.frames),  // normalized in importer settings
                    messageOptions = SendMessageOptions.DontRequireReceiver,
                });
            return list.ToArray();
        }
    }
}
