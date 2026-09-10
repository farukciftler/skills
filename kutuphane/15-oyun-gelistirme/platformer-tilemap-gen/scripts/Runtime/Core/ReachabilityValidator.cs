using System;
using System.Collections.Generic;
using System.Text;

namespace PlatformerGen
{
    public enum MoveKind : byte { Start, Walk, Fall, Jump, Climb, DropThrough }

    [Serializable]
    public sealed class ValidationReport
    {
        public bool HasSpawn;
        public bool HasExit;
        public bool ExitReachable;
        public int StandableNodes;
        public int ReachableNodes;
        public double Coverage;          // reachable / standable
        public int PickupsTotal;
        public int PickupsReachable;
        public int PathLength;           // nodes on spawn->exit path
        public int JumpsOnPath;
        public int FallsOnPath;
        public string Profile;           // MovementProfile used (degraded)
        public List<Int2> Path = new List<Int2>();
        public List<string> Problems = new List<string>();

        public bool Passed { get { return HasSpawn && HasExit && ExitReachable; } }

        public override string ToString()
        {
            var sb = new StringBuilder();
            sb.Append(Passed ? "PASS" : "FAIL");
            sb.AppendFormat(" exitReachable={0} coverage={1:P0} ({2}/{3}) pickups={4}/{5} path={6} jumps={7} falls={8}",
                ExitReachable, Coverage, ReachableNodes, StandableNodes, PickupsReachable, PickupsTotal, PathLength, JumpsOnPath, FallsOnPath);
            foreach (var p in Problems) sb.Append("\n  - ").Append(p);
            return sb.ToString();
        }
    }

    [Serializable]
    public sealed class ValidatorOptions
    {
        public bool BottomIsPit = true;          // leaving the grid downward = death (bottomless pits)
        public double SafetyMargin = 0.85;       // validate with a degraded profile: no frame-perfect jumps required
        public int JumpHeightSamples = 0;        // 0 = auto (one per tile of jump height)
        public double SimulationSeconds = 4.0;   // per trajectory
        public double Hz = 60.0;
    }

    /// <summary>
    /// Physics-based playability check on a TileGrid. Builds a graph whose nodes are "places the
    /// character can rest" (standing on support or holding a ladder) and whose edges are simulated
    /// moves: walk, walk-off falls with air control, variable-height jumps with constant or delayed
    /// air control, ladder climbs and one-way drop-throughs. Then BFS from Spawn to Exit.
    ///
    /// It is intentionally conservative (degraded profile, no wall-jumps/dashes/double-jumps unless
    /// you extend it) — a PASS means an average player can finish, not just a TAS.
    /// </summary>
    public sealed class ReachabilityValidator
    {
        private readonly MovementProfile _p;
        private readonly ValidatorOptions _o;
        private TileGrid _g;

        public ReachabilityValidator(MovementProfile profile, ValidatorOptions options = null)
        {
            _o = options ?? new ValidatorOptions();
            _p = profile.Degraded(_o.SafetyMargin);
        }

        public MovementProfile EffectiveProfile { get { return _p; } }

        // ---------- cell queries ----------
        private enum Hit { Free, Block, Death }

        private Hit CellHit(int x, int y)
        {
            if (y < 0) return _o.BottomIsPit ? Hit.Death : Hit.Block;
            Cell c = _g.Get(x, y);
            if (!_g.InBounds(x, y)) return CellRules.IsSolid(c) ? Hit.Block : Hit.Free;
            if (CellRules.IsSolid(c)) return Hit.Block;
            if (c == Cell.Hazard) return Hit.Death;
            return Hit.Free;
        }

        private bool BodyFree(int x, int y)
        {
            for (int dy = 0; dy < _p.BodyHeight; dy++) if (CellHit(x, y + dy) != Hit.Free) return false;
            return true;
        }

        private bool IsStandable(int x, int y)
        {
            if (!_g.InBounds(x, y) || !BodyFree(x, y)) return false;
            Cell here = _g.Get(x, y);
            if (here == Cell.OneWay) return false;               // never "rest inside" a platform
            Cell below = _g.Get(x, y - 1);
            if (y > 0 && CellRules.IsSupport(below)) return true;
            if (y == 0 && !_o.BottomIsPit && CellRules.IsSolid(_g.OutOfBounds)) return true;
            if (_p.CanClimbLadders && (here == Cell.Ladder || (y > 0 && below == Cell.Ladder))) return true;
            return false;
        }

        // ---------- continuous trajectory simulation ----------
        private struct Landing { public bool Ok; public int X, Y; }

        /// <summary>Simulate from feet position (px,py) with velocity (vx,vy). Returns the resting node or !Ok on death/timeout.</summary>
        private Landing Simulate(double px, double py, double vx, double vy, bool delayedAirControl, double delayedVx)
        {
            double halfW = _p.BodyWidth * 0.5;
            double g = _p.Gravity;
            double dt = 1.0 / _o.Hz;
            double t = 0, maxY = py;
            bool apexPassed = false;
            int steps = (int)(_o.SimulationSeconds * _o.Hz);

            for (int s = 0; s < steps; s++, t += dt)
            {
                if (delayedAirControl && !apexPassed && vy <= 0) { apexPassed = true; vx = delayedVx; }
                double grav = vy > 0 ? g : g * _p.FallGravityMultiplier;
                int sub = Math.Max(1, (int)Math.Ceiling(Math.Max(Math.Abs(vx), Math.Abs(vy) + grav * dt) * dt / 0.2));
                double h = dt / sub;
                for (int k = 0; k < sub; k++)
                {
                    // --- X axis ---
                    if (vx != 0)
                    {
                        double nx = px + vx * h;
                        Hit hx = BoxHit(nx - halfW, nx + halfW, py, py + _p.BodyHeight);
                        if (hx == Hit.Death) return new Landing();
                        if (hx == Hit.Block)
                        {
                            // clamp against the wall
                            nx = vx > 0 ? Math.Floor(px + halfW + vx * h) - halfW - 1e-4 : Math.Ceiling(px - halfW + vx * h) + halfW + 1e-4;
                            if (BoxHit(nx - halfW, nx + halfW, py, py + _p.BodyHeight) != Hit.Free) nx = px;
                            vx = 0; if (delayedAirControl) delayedVx = 0;
                        }
                        px = nx;
                    }
                    // --- Y axis ---
                    vy -= (vy > 0 ? g : g * _p.FallGravityMultiplier) * h;
                    double ny = py + vy * h;
                    if (vy > 0)
                    {
                        Hit hy = BoxHit(px - halfW, px + halfW, ny, ny + _p.BodyHeight);
                        if (hy == Hit.Death) return new Landing();
                        if (hy == Hit.Block) { ny = Math.Floor(ny + _p.BodyHeight) - _p.BodyHeight - 1e-4; if (ny < py) ny = py; vy = 0; }
                    }
                    else
                    {
                        int boundary = (int)Math.Floor(py);
                        if (ny < boundary)
                        {
                            // crossing the top surface of row boundary-1
                            int landX;
                            if (FindSupport(px, halfW, boundary - 1, out landX))
                            {
                                if (maxY - boundary > _p.MaxSafeFall) return new Landing();
                                return new Landing { Ok = true, X = landX, Y = boundary };
                            }
                        }
                        Hit hy = BoxHit(px - halfW, px + halfW, ny, ny + _p.BodyHeight);
                        if (hy == Hit.Death) return new Landing();
                        if (hy == Hit.Block) return new Landing(); // should be caught by support check; treat as stuck
                        // ladder grab while falling/rising through a ladder cell (optional, conservative: only when falling)
                        if (_p.CanClimbLadders)
                        {
                            int cx = (int)Math.Floor(px), cy = (int)Math.Floor(ny + 0.5);
                            if (_g.Get(cx, cy) == Cell.Ladder && BodyFree(cx, cy)) return new Landing { Ok = true, X = cx, Y = cy };
                        }
                    }
                    py = ny;
                    if (py > maxY) maxY = py;
                    if (py < -2) return new Landing();
                }
            }
            return new Landing();
        }

        private Hit BoxHit(double left, double right, double bottom, double top)
        {
            int x0 = (int)Math.Floor(left), x1 = (int)Math.Floor(right - 1e-6);
            int y0 = (int)Math.Floor(bottom), y1 = (int)Math.Floor(top - 1e-6);
            Hit worst = Hit.Free;
            for (int y = y0; y <= y1; y++)
                for (int x = x0; x <= x1; x++)
                {
                    Hit h = CellHit(x, y);
                    if (h == Hit.Death) return Hit.Death;
                    if (h == Hit.Block) worst = Hit.Block;
                }
            return worst;
        }

        private bool FindSupport(double px, double halfW, int row, out int landX)
        {
            landX = 0;
            if (row < 0)
            {
                if (_o.BottomIsPit || !CellRules.IsSolid(_g.OutOfBounds)) return false;
                landX = (int)Math.Floor(px);
                return _g.InBounds(landX, 0) && BodyFree(landX, 0);
            }
            int x0 = (int)Math.Floor(px - halfW), x1 = (int)Math.Floor(px + halfW - 1e-6);
            int center = (int)Math.Floor(px);
            int best = int.MinValue; double bestD = double.MaxValue;
            for (int x = x0; x <= x1; x++)
            {
                Cell c = _g.Get(x, row);
                bool support = CellRules.IsSupport(c) || (_p.CanClimbLadders && c == Cell.Ladder && _g.Get(x, row + 1) != Cell.Ladder);
                if (!support || !_g.InBounds(x, row)) continue;
                if (!BodyFree(x, row + 1)) continue;
                double d = Math.Abs(x - center);
                if (d < bestD) { bestD = d; best = x; }
            }
            if (best == int.MinValue) return false;
            landX = best;
            return true;
        }

        // ---------- graph search ----------
        private struct Edge { public int X, Y; public MoveKind Kind; }

        private void Expand(int x, int y, List<Edge> outEdges)
        {
            outEdges.Clear();
            double s = _p.RunSpeed;
            // walk / walk-off
            for (int dir = -1; dir <= 1; dir += 2)
            {
                int nx = x + dir;
                if (IsStandable(nx, y)) { outEdges.Add(new Edge { X = nx, Y = y, Kind = MoveKind.Walk }); continue; }
                if (!_g.InBounds(nx, y) || !BodyFree(nx, y)) continue;
                double[] drifts = { 0, 0.5, 1.0, -0.5 };
                foreach (double d in drifts)
                    AddLanding(Simulate(nx + 0.5, y, dir * s * d, 0, false, 0), MoveKind.Fall, outEdges);
            }
            // jumps (variable height x air control variants)
            int samples = _o.JumpHeightSamples > 0 ? _o.JumpHeightSamples : Math.Max(1, (int)Math.Ceiling(_p.MaxJumpHeight));
            // Players take off from anywhere on a tile — usually its edge. Besides the tile centre we also
            // launch from the leading edge (body overhanging the next column if that column is free).
            double edge = 0.5 - 0.02;
            double leftStart = BoxHit(x + 0.5 - edge - _p.BodyWidth * 0.5, x + 0.5 - edge + _p.BodyWidth * 0.5, y, y + _p.BodyHeight) == Hit.Free ? x + 0.5 - edge : x + 0.5;
            double rightStart = BoxHit(x + 0.5 + edge - _p.BodyWidth * 0.5, x + 0.5 + edge + _p.BodyWidth * 0.5, y, y + _p.BodyHeight) == Hit.Free ? x + 0.5 + edge : x + 0.5;
            for (int i = 1; i <= samples; i++)
            {
                double hgt = _p.MaxJumpHeight * i / samples;
                double vy = Math.Sqrt(2 * _p.Gravity * hgt);
                double[] vxs = { -s, -s * 0.5, 0, s * 0.5, s };
                foreach (double vx in vxs)
                {
                    AddLanding(Simulate(x + 0.5, y, vx, vy, false, 0), MoveKind.Jump, outEdges);
                    if (vx > 0 && rightStart != x + 0.5) AddLanding(Simulate(rightStart, y, vx, vy, false, 0), MoveKind.Jump, outEdges);
                    if (vx < 0 && leftStart != x + 0.5) AddLanding(Simulate(leftStart, y, vx, vy, false, 0), MoveKind.Jump, outEdges);
                }
                AddLanding(Simulate(x + 0.5, y, 0, vy, true, s), MoveKind.Jump, outEdges);
                AddLanding(Simulate(x + 0.5, y, 0, vy, true, -s), MoveKind.Jump, outEdges);
            }
            // ladders
            if (_p.CanClimbLadders)
            {
                Cell here = _g.Get(x, y), above = _g.Get(x, y + 1), below = _g.Get(x, y - 1);
                if ((here == Cell.Ladder || above == Cell.Ladder) && BodyFree(x, y + 1) && (above == Cell.Ladder || IsStandable(x, y + 1)))
                    outEdges.Add(new Edge { X = x, Y = y + 1, Kind = MoveKind.Climb });
                if (below == Cell.Ladder && BodyFree(x, y - 1))
                    outEdges.Add(new Edge { X = x, Y = y - 1, Kind = MoveKind.Climb });
            }
            // drop through one-way
            if (_p.CanDropThroughOneWay && _g.Get(x, y - 1) == Cell.OneWay)
            {
                double[] vxs = { 0, s * 0.5, -s * 0.5 };
                foreach (double vx in vxs) AddLanding(Simulate(x + 0.5, y - 1 + 1e-3, vx, 0, false, 0), MoveKind.DropThrough, outEdges);
            }
        }

        private void AddLanding(Landing l, MoveKind kind, List<Edge> edges)
        {
            if (!l.Ok) return;
            if (!IsStandable(l.X, l.Y) && !(_g.Get(l.X, l.Y) == Cell.Ladder)) return;
            edges.Add(new Edge { X = l.X, Y = l.Y, Kind = kind });
        }

        /// <summary>Validate a grid. Spawn/Exit come from markers; override with explicit positions if you have none.</summary>
        public ValidationReport Validate(TileGrid grid, Int2? spawnOverride = null, Int2? exitOverride = null)
        {
            _g = grid;
            var rep = new ValidationReport { Profile = _p.ToString() };

            var spawns = grid.FindAll(Cell.Spawn);
            var exits = grid.FindAll(Cell.Exit);
            if (spawnOverride.HasValue) { spawns.Clear(); spawns.Add(spawnOverride.Value); }
            if (exitOverride.HasValue) { exits.Clear(); exits.Add(exitOverride.Value); }
            rep.HasSpawn = spawns.Count > 0;
            rep.HasExit = exits.Count > 0;
            if (!rep.HasSpawn) rep.Problems.Add("No Spawn marker (S).");
            if (!rep.HasExit) rep.Problems.Add("No Exit marker (E).");
            if (spawns.Count > 1) rep.Problems.Add("Multiple Spawn markers; using the first.");

            int W = grid.Width, Hh = grid.Height;
            for (int y = 0; y < Hh; y++) for (int x = 0; x < W; x++) if (IsStandable(x, y)) rep.StandableNodes++;

            var visited = new bool[W * Hh];
            var parent = new int[W * Hh];
            var kind = new MoveKind[W * Hh];
            for (int i = 0; i < parent.Length; i++) parent[i] = -1;
            var q = new Queue<int>();

            if (rep.HasSpawn)
            {
                Int2 sp = spawns[0];
                int sx = sp.x, sy = sp.y;
                if (!IsStandable(sx, sy))
                {
                    var l = Simulate(sx + 0.5, sy, 0, 0, false, 0);
                    if (l.Ok) { sx = l.X; sy = l.Y; }
                    else rep.Problems.Add("Spawn " + sp + " is not a resting position and falls to death/nowhere.");
                }
                if (grid.InBounds(sx, sy) && (IsStandable(sx, sy)))
                {
                    int si = grid.Index(sx, sy);
                    visited[si] = true; kind[si] = MoveKind.Start; q.Enqueue(si);
                }
            }

            var exitSet = new HashSet<int>();
            foreach (var e in exits)
                for (int dy = 0; dy < _p.BodyHeight; dy++)
                    if (grid.InBounds(e.x, e.y - dy)) exitSet.Add(grid.Index(e.x, e.y - dy));

            var edges = new List<Edge>(64);
            int goal = -1;
            while (q.Count > 0)
            {
                int cur = q.Dequeue();
                rep.ReachableNodes++;
                if (goal < 0 && exitSet.Contains(cur)) goal = cur;
                Expand(cur % W, cur / W, edges);
                foreach (var ed in edges)
                {
                    int ni = grid.Index(ed.X, ed.Y);
                    if (visited[ni]) continue;
                    visited[ni] = true; parent[ni] = cur; kind[ni] = ed.Kind;
                    q.Enqueue(ni);
                }
            }

            rep.ExitReachable = goal >= 0;
            rep.Coverage = rep.StandableNodes > 0 ? (double)rep.ReachableNodes / rep.StandableNodes : 0;
            if (rep.HasExit && rep.HasSpawn && !rep.ExitReachable) rep.Problems.Add("Exit is NOT reachable from Spawn with the (degraded) movement profile.");

            if (goal >= 0)
            {
                var path = new List<Int2>();
                for (int n = goal; n >= 0; n = parent[n])
                {
                    path.Add(new Int2(n % W, n / W));
                    if (kind[n] == MoveKind.Jump) rep.JumpsOnPath++;
                    if (kind[n] == MoveKind.Fall || kind[n] == MoveKind.DropThrough) rep.FallsOnPath++;
                }
                path.Reverse();
                rep.Path = path;
                rep.PathLength = path.Count;
            }

            foreach (var pk in grid.FindAll(Cell.Pickup))
            {
                rep.PickupsTotal++;
                bool got = false;
                for (int dy = 0; dy < _p.BodyHeight && !got; dy++)
                    if (grid.InBounds(pk.x, pk.y - dy) && visited[grid.Index(pk.x, pk.y - dy)]) got = true;
                if (got) rep.PickupsReachable++;
            }
            if (rep.PickupsTotal > rep.PickupsReachable) rep.Problems.Add((rep.PickupsTotal - rep.PickupsReachable) + " pickup(s) unreachable.");

            _lastVisited = visited; _lastW = W;
            return rep;
        }

        private bool[] _lastVisited; private int _lastW;

        /// <summary>After Validate(): was this node reachable? Useful for overlays and for placing Exit at the farthest reachable spot.</summary>
        public bool WasReachable(int x, int y)
        {
            if (_lastVisited == null || _g == null || !_g.InBounds(x, y)) return false;
            return _lastVisited[y * _lastW + x];
        }

        /// <summary>ASCII debug overlay: '*' = path, '+' = other reachable resting spots.</summary>
        public string RenderOverlay(TileGrid grid, ValidationReport rep)
        {
            var onPath = new HashSet<Int2>(rep.Path);
            return AsciiLevel.Render(grid, (x, y) =>
            {
                Cell c = grid.Get(x, y);
                if (c != Cell.Empty && c != Cell.Ladder) return null;
                if (onPath.Contains(new Int2(x, y))) return '*';
                if (WasReachable(x, y)) return '+';
                return null;
            });
        }
    }
}
