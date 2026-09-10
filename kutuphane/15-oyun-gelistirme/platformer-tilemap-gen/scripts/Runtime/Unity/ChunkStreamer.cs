using System.Collections.Generic;
using UnityEngine;

namespace PlatformerGen.Integration
{
    /// <summary>
    /// Endless runner / infinite side-scroller: streams ChunkStream segments ahead of the camera and
    /// clears them behind it. Segment i is a pure function of (seed, i, previous exit height), so a
    /// replay with the same seed reproduces the same world. Config.algorithm must be ChunkStitch.
    /// Colliders: each append rebuilds the layer composites once. If that shows in the profiler on
    /// low-end devices, raise segmentsAhead and append during calm moments, or split into per-segment Tilemaps.
    /// </summary>
    public sealed class ChunkStreamer : MonoBehaviour
    {
        public LevelGenConfig config;
        public LevelLayers layers;
        public Transform follow;                 // usually the camera or player
        public int seed = 1;
        public int segmentsAhead = 3;
        public float unloadBehindTiles = 40f;
        [Tooltip("Tiles over which difficulty ramps from start to end, then stays at end.")]
        public float rampLengthTiles = 1500f;

        private ChunkStream _stream;
        private readonly Queue<BoundsInt> _live = new Queue<BoundsInt>();
        private float _cell = 1f;

        private void Start()
        {
            var gen = config.CreateGenerator() as ChunkStitchGenerator;
            if (gen == null) { Debug.LogError("[PlatformerGen] ChunkStreamer needs algorithm = ChunkStitch", this); enabled = false; return; }
            _stream = gen.CreateStream(new Rng(seed));
            _cell = layers.ground.layoutGrid.cellSize.x;
            for (int i = 0; i < segmentsAhead; i++) Append();
        }

        private void Update()
        {
            if (_stream == null || follow == null) return;
            float followTile = follow.position.x / _cell;
            // keep segmentsAhead worth of content in front
            while (_stream.NextX - followTile < segmentsAhead * 12) Append();
            // unload behind
            while (_live.Count > 0 && _live.Peek().xMax < followTile - unloadBehindTiles)
                TilemapLevelWriter.ClearRegion(layers, _live.Dequeue());
        }

        private void Append()
        {
            var seg = _stream.Next(Mathf.Clamp01(_stream.NextX / rampLengthTiles));
            var origin = new Vector3Int(seg.X, 0, 0);
            TilemapLevelWriter.Write(seg.Grid, layers, config.legend, origin, new WriteOptions { clearFirst = false });
            _live.Enqueue(new BoundsInt(seg.X, 0, 0, seg.Grid.Width, seg.Grid.Height, 1));
        }
    }
}
