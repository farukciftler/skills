using NUnit.Framework;
using UnityEngine;
using UnityEngine.Tilemaps;
using PlatformerGen.Integration;

namespace PlatformerGen.Tests
{
    // Run: unity test <project> --mode EditMode --report-format junit --output results.xml
    public class PlatformerGenTests
    {
        private static readonly MovementProfile P = MovementProfile.FromApex(3.2, 0.4, 8.0, 1, 1.6);

        [Test]
        public void Validator_FlatLevel_Passes()
        {
            var g = AsciiLevel.Parse("..........\n..........\nS........E\n##########");
            Assert.IsTrue(new ReachabilityValidator(P).Validate(g).Passed);
        }

        [Test]
        public void Validator_WideGap_Fails()
        {
            var g = AsciiLevel.Parse("....................\n....................\nS..................E\n#####........#######");
            Assert.IsFalse(new ReachabilityValidator(P).Validate(g).Passed);
        }

        [Test]
        public void Generators_AreDeterministic()
        {
            var a = new HeightmapGenerator(P).Generate(new Rng(7));
            var b = new HeightmapGenerator(P).Generate(new Rng(7));
            Assert.AreEqual(AsciiLevel.Render(a), AsciiLevel.Render(b));
        }

        [Test]
        public void Heightmap_PassesAcross20Seeds()
        {
            var opts = new ValidatorOptions { BottomIsPit = true };
            for (int s = 0; s < 20; s++)
                Assert.IsTrue(GenerationPipeline.Run(new HeightmapGenerator(P), s, P, opts, 10).Report.Passed, "seed " + s);
        }

        [Test]
        public void Writer_Reader_RoundTrip()
        {
            var gridGo = new GameObject("TestGrid", typeof(Grid));
            try
            {
                var layers = LevelLayers.EnsureOn(gridGo.GetComponent<Grid>());
                var legend = ScriptableObject.CreateInstance<TileLegend>();
                legend.Find(Cell.Solid).tile = ScriptableObject.CreateInstance<Tile>();
                legend.Find(Cell.OneWay).tile = ScriptableObject.CreateInstance<Tile>();
                legend.Find(Cell.Hazard).tile = ScriptableObject.CreateInstance<Tile>();
                legend.Find(Cell.Ladder).tile = ScriptableObject.CreateInstance<Tile>();

                string level = "S....E\n.=H.^.\n######";
                var src = AsciiLevel.Parse(level);
                var ws = TilemapLevelWriter.Write(src, layers, legend, Vector3Int.zero);
                Assert.AreEqual(9, ws.tilesWritten); // 6 solid + one-way + ladder + hazard (S/E are entities, not tiles)
                Vector3Int origin;
                var back = TilemapLevelReader.Read(layers, legend, out origin);
                Assert.AreEqual(Vector3Int.zero, origin);
                Assert.AreEqual(AsciiLevel.Render(src), AsciiLevel.Render(back));
            }
            finally { Object.DestroyImmediate(gridGo); }
        }
    }
}
