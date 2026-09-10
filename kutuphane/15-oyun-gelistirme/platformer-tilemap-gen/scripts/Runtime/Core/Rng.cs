using System;
using System.Collections.Generic;

namespace PlatformerGen
{
    /// <summary>
    /// Deterministic, platform-independent RNG (SplitMix64). Same seed => same level on every
    /// platform, Unity version and .NET runtime. Never use UnityEngine.Random for level generation:
    /// it is global state that any other script can advance, which silently breaks seed replay.
    /// Use Derive(salt) to get independent sub-streams (per chunk, per room, per pass) so that
    /// changing one pass does not reshuffle the others.
    /// </summary>
    public sealed class Rng
    {
        private ulong _state;
        public readonly ulong Seed;

        public Rng(ulong seed) { Seed = seed; _state = seed; }
        public Rng(int seed) : this((ulong)(uint)seed * 0x9E3779B97F4A7C15UL + 0x632BE59BD9B4E019UL) { }

        public ulong NextULong()
        {
            ulong z = (_state += 0x9E3779B97F4A7C15UL);
            z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9UL;
            z = (z ^ (z >> 27)) * 0x94D049BB133111EBUL;
            return z ^ (z >> 31);
        }

        /// <summary>[0, max)</summary>
        public int Next(int max)
        {
            if (max <= 0) return 0;
            return (int)(NextULong() % (ulong)max);
        }

        /// <summary>[min, maxExclusive)</summary>
        public int Range(int min, int maxExclusive) { return min + Next(Math.Max(1, maxExclusive - min)); }

        /// <summary>[0,1)</summary>
        public double NextDouble() { return (NextULong() >> 11) * (1.0 / 9007199254740992.0); }

        public bool Chance(double p) { return NextDouble() < p; }

        public T Pick<T>(IList<T> list) { return list[Next(list.Count)]; }

        public T PickWeighted<T>(IList<T> items, Func<T, double> weight)
        {
            double total = 0;
            for (int i = 0; i < items.Count; i++) total += Math.Max(0, weight(items[i]));
            if (total <= 0) return items[Next(items.Count)];
            double r = NextDouble() * total;
            for (int i = 0; i < items.Count; i++)
            {
                r -= Math.Max(0, weight(items[i]));
                if (r < 0) return items[i];
            }
            return items[items.Count - 1];
        }

        public void Shuffle<T>(IList<T> list)
        {
            for (int i = list.Count - 1; i > 0; i--)
            {
                int j = Next(i + 1);
                T t = list[i]; list[i] = list[j]; list[j] = t;
            }
        }

        /// <summary>Independent child stream. Derive(chunkIndex) is stable regardless of how much the parent was used.</summary>
        public Rng Derive(long salt)
        {
            ulong h = Seed ^ ((ulong)salt * 0xD1B54A32D192ED03UL);
            h ^= h >> 33; h *= 0xFF51AFD7ED558CCDUL; h ^= h >> 33; h *= 0xC4CEB9FE1A85EC53UL; h ^= h >> 33;
            return new Rng(h);
        }

        public static int HashString(string s)
        {
            unchecked
            {
                int h = (int)2166136261;
                for (int i = 0; i < s.Length; i++) { h ^= s[i]; h *= 16777619; }
                return h;
            }
        }
    }
}
