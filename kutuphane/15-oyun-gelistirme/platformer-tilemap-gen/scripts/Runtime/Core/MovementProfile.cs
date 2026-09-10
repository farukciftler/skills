using System;

namespace PlatformerGen
{
    /// <summary>
    /// The contract between the character controller and the level. Every procedural rule
    /// (max step, max gap, platform spacing) and the reachability validator derive from this.
    /// All values are in TILES (1 tile = 1 grid cell), never in Unity units.
    ///
    /// Build it from the real controller: read jumpHeight / timeToApex / runSpeed / gravityScale
    /// from the player script, convert units -> tiles with the Grid cellSize, then call FromApex().
    /// </summary>
    [Serializable]
    public sealed class MovementProfile
    {
        public double Gravity;            // tiles/s^2 while rising
        public double JumpVelocity;       // tiles/s initial upward velocity
        public double RunSpeed;           // tiles/s horizontal
        public double FallGravityMultiplier = 1.0; // >1 = snappier fall (typical 1.5–2.5)
        public int BodyHeight = 1;        // character height in tiles (1 = Spelunky-like, 2 = Celeste/Mario-big-like)
        public double BodyWidth = 0.8;    // collider width in tiles (slightly < 1 fits 1-tile gaps)
        public int MaxSafeFall = int.MaxValue; // tiles; falls longer than this count as death (fall damage games)
        public bool CanDropThroughOneWay = true;
        public bool CanClimbLadders = true;

        public double MaxJumpHeight { get { return JumpVelocity * JumpVelocity / (2.0 * Gravity); } }
        public double TimeToApex { get { return JumpVelocity / Gravity; } }

        /// <summary>Horizontal distance covered by a full jump landing at the same height.</summary>
        public double FlatJumpDistance
        {
            get
            {
                double tUp = TimeToApex;
                double tDown = Math.Sqrt(2.0 * MaxJumpHeight / (Gravity * FallGravityMultiplier));
                return RunSpeed * (tUp + tDown);
            }
        }

        /// <summary>Largest clear gap (in whole tiles) crossable on flat ground, accounting for body width.</summary>
        public int MaxGapTiles(double margin = 0.85)
        {
            return Math.Max(0, (int)Math.Floor(FlatJumpDistance * margin - BodyWidth));
        }

        /// <summary>Longest run of ground-level hazards (spikes) that can be jumped. Harder than a pit of the
        /// same width: over a pit the body may dip to ground level, over spikes it must stay a full tile higher.</summary>
        public int MaxHazardRunTiles(double margin = 0.85)
        {
            return Math.Max(1, MaxGapTiles(margin) - 1);
        }

        /// <summary>Largest step UP (whole tiles) reachable by a jump, with a safety margin.</summary>
        public int MaxStepUpTiles(double margin = 0.85)
        {
            return Math.Max(0, (int)Math.Floor(MaxJumpHeight * margin));
        }

        /// <summary>Designer-friendly construction: pick height and time-to-apex, derive physics.
        /// g = 2h/t^2, v0 = 2h/t. Typical "good feel": t = 0.3–0.45 s.</summary>
        public static MovementProfile FromApex(double jumpHeightTiles, double timeToApexSeconds, double runSpeedTilesPerSec,
                                               int bodyHeight = 1, double fallGravityMultiplier = 1.0)
        {
            if (jumpHeightTiles <= 0 || timeToApexSeconds <= 0) throw new ArgumentException("jump height and apex time must be > 0");
            var p = new MovementProfile();
            p.Gravity = 2.0 * jumpHeightTiles / (timeToApexSeconds * timeToApexSeconds);
            p.JumpVelocity = 2.0 * jumpHeightTiles / timeToApexSeconds;
            p.RunSpeed = runSpeedTilesPerSec;
            p.BodyHeight = Math.Max(1, bodyHeight);
            p.FallGravityMultiplier = Math.Max(0.1, fallGravityMultiplier);
            return p;
        }

        /// <summary>From Rigidbody2D-style numbers in Unity units: gravity = |Physics2D.gravity.y| * gravityScale,
        /// jumpVelocity = the velocity/impulse-derived launch speed, runSpeed = max horizontal speed. cellSize = Grid.cellSize.y.</summary>
        public static MovementProfile FromUnityUnits(double gravityUnits, double jumpVelocityUnits, double runSpeedUnits,
                                                     double cellSize, int bodyHeightTiles = 1, double fallGravityMultiplier = 1.0)
        {
            if (cellSize <= 0) throw new ArgumentException("cellSize must be > 0");
            var p = new MovementProfile();
            p.Gravity = gravityUnits / cellSize;
            p.JumpVelocity = jumpVelocityUnits / cellSize;
            p.RunSpeed = runSpeedUnits / cellSize;
            p.BodyHeight = Math.Max(1, bodyHeightTiles);
            p.FallGravityMultiplier = Math.Max(0.1, fallGravityMultiplier);
            return p;
        }

        /// <summary>A weaker copy used for validation, so levels never demand frame-perfect jumps.</summary>
        public MovementProfile Degraded(double factor)
        {
            var p = (MovementProfile)MemberwiseClone();
            // scale height by factor (v0 scales with sqrt), speed by factor
            p.JumpVelocity = JumpVelocity * Math.Sqrt(factor);
            p.RunSpeed = RunSpeed * factor;
            return p;
        }

        public override string ToString()
        {
            return string.Format("jumpH={0:0.00}t apex={1:0.00}s run={2:0.0}t/s flatJump={3:0.00}t maxGap={4}t maxStep={5}t body={6}",
                MaxJumpHeight, TimeToApex, RunSpeed, FlatJumpDistance, MaxGapTiles(), MaxStepUpTiles(), BodyHeight);
        }
    }
}
