// Standalone test/benchmark harness for PlatformerGen Core — runs WITHOUT Unity.
// Compile & run (Mono):   mcs -out:harness.exe tools/CoreHarness.cs $(find scripts/Runtime/Core -name '*.cs') && mono harness.exe [assetsDir]
// Compile & run (.NET):   put the same files in a console project, `dotnet run -- assetsDir`
// Modes: (none) = full test suite + generator stats;  "render <room|chunk|height|cave> <seed>";  "validate <file.txt>"
using System;
using System.Collections.Generic;
using System.IO;
using PlatformerGen;

public static class CoreHarness
{
    static int _fail;
    static MovementProfile P1 = MovementProfile.FromApex(3.2, 0.4, 8.0, bodyHeight: 1, fallGravityMultiplier: 1.6);

    public static int Main(string[] args)
    {
        string assets = args.Length > 0 && Directory.Exists(args[args.Length - 1]) ? args[args.Length - 1] : "assets";
        if (args.Length >= 3 && args[0] == "render") { Render(args[1], int.Parse(args[2]), assets); return 0; }
        if (args.Length >= 2 && args[0] == "validate") { ValidateFile(args[1]); return 0; }
        if (args.Length >= 2 && args[0] == "failures") { Failures(args[1], assets); return 0; }

        Console.WriteLine("Profile: " + P1);
        Console.WriteLine("Degraded (0.85): " + P1.Degraded(0.85));
        ValidatorCases();
        Determinism(assets);
        GeneratorStats(assets);
        Console.WriteLine(_fail == 0 ? "\nALL CHECKS PASSED" : "\n" + _fail + " CHECK(S) FAILED");
        return _fail == 0 ? 0 : 1;
    }

    static void Check(string name, bool cond, string detail = "")
    {
        Console.WriteLine((cond ? "  ok   " : "  FAIL ") + name + (cond || detail == "" ? "" : "\n" + detail));
        if (!cond) _fail++;
    }

    static ValidationReport V(string ascii, MovementProfile p = null, bool pit = true)
    {
        var g = AsciiLevel.Parse(ascii);
        return new ReachabilityValidator(p ?? P1, new ValidatorOptions { BottomIsPit = pit }).Validate(g);
    }

    static void ValidatorCases()
    {
        Console.WriteLine("\n== Validator cases ==");
        Check("flat walk", V(
"..........\n" +
"S........E\n" +
"##########").Passed);

        Check("gap 3 jumpable", V(
"..............\n" +
"..............\n" +
"S............E\n" +
"#####...######").Passed);

        Check("gap 8 NOT jumpable", !V(
"....................\n" +
"....................\n" +
"S..................E\n" +
"#####........#######").Passed);

        var r2 = V(
"..........\n" +
"..........\n" +
"........E.\n" +
"......####\n" +
"S.....####\n" +
"##########");
        Check("step up 2 reachable", r2.Passed, r2.ToString());

        var r4 = V(
"..........\n" +
"..........\n" +
"........E.\n" +
"......####\n" +
"......####\n" +
"......####\n" +
"S.....####\n" +
"##########");
        Check("step up 4 NOT reachable (jump 3.2 degraded to 2.72)", !r4.Passed, r4.ToString());

        var lad = V(
"..........\n" +
"........E.\n" +
"....H#####\n" +
"....H.....\n" +
"....H.....\n" +
"S...H.....\n" +
"##########");
        Check("ladder climb to ledge", lad.Passed, lad.ToString());

        var ow = V(
"..........\n" +
"....E.....\n" +
"...===....\n" +
"...S......\n" +
"##########");
        Check("jump up through one-way", ow.Passed, ow.ToString());

        var drop = V(
"..........\n" +
"....S.....\n" +
"#########.\n" +
"#...======\n" +
"#.........\n" +
"#E........\n" +
"##########", pit: false);
        Check("drop through one-way down", drop.Passed, drop.ToString());

        var spikes = V(
"............\n" +
"............\n" +
"............\n" +
"............\n" +
"S....^^....E\n" +
"############");
        Check("jump over 2 spikes", spikes.Passed, spikes.ToString());

        var closed = V(
"..........\n" +
"......###.\n" +
"S.....#E#.\n" +
"##########");
        Check("exit sealed in box NOT reachable", !closed.Passed);

        var tall = MovementProfile.FromApex(3.2, 0.4, 8.0, bodyHeight: 2);
        var tunnel = V(
"##########\n" +
"#........#\n" +
"#.######.#\n" +
"#S.......E\n" +
"##########", tall);
        Check("2-tall body can't fit 1-tile tunnel", !tunnel.Passed, tunnel.ToString());

        var fallDeath = MovementProfile.FromApex(3.2, 0.4, 8.0);
        fallDeath.MaxSafeFall = 3;
        var cliff = V(
"S.........\n" +
"####......\n" +
"####......\n" +
"####......\n" +
"####......\n" +
"####......\n" +
"####.....E\n" +
"##########", fallDeath, false);
        Check("MaxSafeFall=3 blocks 6-tile drop", !cliff.Passed, cliff.ToString());
    }

    static string Load(string assets, string file) { return File.ReadAllText(Path.Combine(assets, file)); }

    static IGridGenerator Make(string kind, string assets)
    {
        switch (kind)
        {
            case "room":
                return RoomGridGenerator.FromText(Load(assets, "room-templates.txt"), 10, 8);
            case "chunk":
                return new ChunkStitchGenerator(P1, ChunkTemplate.FromText(Load(assets, "chunk-templates.txt"))) { TargetWidth = 140 };
            case "height":
                return new HeightmapGenerator(P1) { Width = 150, Height = 28 };
            case "cave":
                return new CaveGenerator(P1) { Width = 60, Height = 36 };
        }
        throw new ArgumentException(kind);
    }

    static ValidatorOptions OptsFor(string kind) { return new ValidatorOptions { BottomIsPit = kind == "chunk" || kind == "height" }; }

    static void Determinism(string assets)
    {
        Console.WriteLine("\n== Determinism ==");
        foreach (var k in new[] { "room", "chunk", "height", "cave" })
        {
            string a = AsciiLevel.Render(Make(k, assets).Generate(new Rng(42)));
            string b = AsciiLevel.Render(Make(k, assets).Generate(new Rng(42)));
            string c = AsciiLevel.Render(Make(k, assets).Generate(new Rng(43)));
            Check(k + ": same seed => identical, different seed => different", a == b && a != c);
        }
    }

    static void GeneratorStats(string assets)
    {
        Console.WriteLine("\n== Generator stats (100 seeds each) ==");
        foreach (var k in new[] { "room", "chunk", "height", "cave" })
        {
            var gen = Make(k, assets);
            var opts = OptsFor(k);
            var sw = System.Diagnostics.Stopwatch.StartNew();
            double first = GenerationPipeline.FirstTryPassRate(gen, P1, 100, opts);
            int totalAttempts = 0, passed = 0;
            for (int s = 0; s < 100; s++)
            {
                var res = GenerationPipeline.Run(gen, s, P1, opts, 30);
                totalAttempts += res.Attempts; if (res.Report.Passed) passed++;
            }
            sw.Stop();
            Console.WriteLine(string.Format("  {0,-7} firstTry={1:P0}  finalPass={2}/100  avgAttempts={3:0.00}  {4:0}ms total",
                k, first, passed, totalAttempts / 100.0, sw.Elapsed.TotalMilliseconds));
            Check(k + " final pass rate >= 98%", passed >= 98);
        }
    }

    static void Render(string kind, int seed, string assets)
    {
        var gen = Make(kind, assets);
        var res = GenerationPipeline.Run(gen, seed, P1, OptsFor(kind), 30);
        var v = new ReachabilityValidator(P1, OptsFor(kind));
        var rep = v.Validate(res.Grid);
        Console.WriteLine(gen.Name + " seed=" + seed + " attempts=" + res.Attempts + " " + res.Milliseconds.ToString("0") + "ms");
        var rg = gen as RoomGridGenerator;
        if (rg != null) Console.WriteLine(rg.DescribeLastLayout());
        var cg = gen as ChunkStitchGenerator;
        if (cg != null) Console.WriteLine(string.Join(" | ", cg.LastLabels.ToArray()));
        Console.WriteLine(v.RenderOverlay(res.Grid, rep));
        Console.WriteLine(rep);
    }

    static void Failures(string kind, string assets)
    {
        var gen = Make(kind, assets);
        var v = new ReachabilityValidator(P1, OptsFor(kind));
        int shown = 0;
        for (int s = 0; s < 100 && shown < 3; s++)
        {
            var g = gen.Generate(new Rng(s).Derive(0));
            var rep = v.Validate(g);
            if (rep.Passed) continue;
            shown++;
            Console.WriteLine("seed " + s + ": " + rep);
            var cg = gen as ChunkStitchGenerator;
            if (cg != null) Console.WriteLine(string.Join(" | ", cg.LastLabels.ToArray()));
            Console.WriteLine(v.RenderOverlay(g, rep));
        }
    }

    static void ValidateFile(string path)
    {
        var g = AsciiLevel.Parse(File.ReadAllText(path), new Rng(1));
        var v = new ReachabilityValidator(P1);
        var rep = v.Validate(g);
        Console.WriteLine(v.RenderOverlay(g, rep));
        Console.WriteLine(rep);
    }
}
