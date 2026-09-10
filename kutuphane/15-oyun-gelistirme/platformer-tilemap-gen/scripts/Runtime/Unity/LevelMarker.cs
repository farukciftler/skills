using UnityEngine;

namespace PlatformerGen.Integration
{
    // Unity requires a MonoBehaviour to live in a file with the same name as the class.
    /// <summary>Tag on spawned (or hand-placed) entity GameObjects so levels can be read back and validated.</summary>
    public sealed class LevelMarker : MonoBehaviour
    {
        public Cell kind = Cell.Spawn;
    }
}
