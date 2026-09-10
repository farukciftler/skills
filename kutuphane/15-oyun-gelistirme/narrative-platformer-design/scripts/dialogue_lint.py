#!/usr/bin/env python3
"""
dialogue_lint.py - flag fake-sounding, AI-flavored, expository or non-native
patterns in game dialogue, plus surface problems (line length, monologues).

Input formats (auto-detected):
  * Plain / screenplay text:   SPEAKER: line of dialogue
  * Yarn-style:                title:/---/=== headers, <<commands>>, -> options ignored
  * JSON:                      [{"speaker": "...", "text": "..."}]
                               or {"lines": [...]}
                               or [{"scene_id": ..., "lines": [...]}, ...]
Lines in [brackets] or (parentheses) are treated as stage directions and skipped.

Usage:
  python3 dialogue_lint.py script.txt [--max-chars 90] [--formal ROBOT --formal SAGE]
                                      [--json] [--strict]

Severity: HIGH = fix before shipping, MED = fix unless deliberate, LOW = review.
These are heuristics. A flag is a question, not a verdict.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------- rules ----

AI_VOCAB = [
    "delve", "tapestry", "testament", "intricate", "pivotal", "crucial", "vibrant",
    "meticulous", "underscore", "underscores", "showcase", "foster", "bolster",
    "enduring", "garner", "interplay", "realm", "beacon", "symphony", "embark",
    "unwavering", "multifaceted", "myriad", "plethora", "profound", "resonate",
    "resonates", "ethereal", "navigate the", "navigating the", "landscape of",
]
AI_TRANSITIONS = ["additionally", "furthermore", "moreover", "nevertheless",
                  "ultimately", "in conclusion", "it is important to note",
                  "it's important to note", "indeed,"]
THEME_STATEMENTS = [
    r"\b(maybe|perhaps)\b.{0,40}\b(the real|was never about|all along)\b",
    r"\bwas never (really )?about\b",
    r"\bthe (real|true) (treasure|journey|enemy|challenge)\b",
    r"\bit'?s not about the destination\b",
    r"\bi'?ve (grown|changed) so much\b",
]
EXPOSITION = [
    r"\bas you (already )?know\b", r"\bas we both know\b", r"\blike i told you\b",
    r"\bremember when we\b", r"\byou know that (the|our)\b", r"\bas i said before\b",
]
EMOTION_NAMING = re.compile(
    r"\b(i\s*(am|'m)\s*(feeling\s+)?(so\s+|very\s+|really\s+)?|i\s+feel\s+(so\s+|very\s+|really\s+)?)"
    r"(sad|scared|afraid|angry|happy|lonely|anxious|worried|lost|hopeless|frightened|terrified|nervous|depressed|overwhelmed)\b",
    re.I)
THERAPY = ["set boundaries", "that's valid", "that is valid", "i hear you", "my trauma",
           "process this", "process my", "toxic", "self-care", "healing journey",
           "safe space", "emotional labor", "hold space"]
GENERIC_CHEER = ["you've got this", "you got this", "i believe in you", "never give up",
                 "we can do this together", "together we can", "you can do it"]
NOT_X_BUT_Y = [r"\bnot just\b.{1,60}\bbut\b", r"\bit'?s not (just )?(a|an|the)?\s?\w+[,.]? it'?s\b",
               r"\bnot about\b.{1,40}\bit'?s about\b", r"\bmore than just\b"]
DESCRIBE_VISIBLE = [r"^\s*(wow[,!]?\s*)?look(,| at) (that|a|the|this)\b", r"\bcan you see (that|the)\b"]
UNCONTRACTED = [r"\bI am\b", r"\bdo not\b", r"\bdoes not\b", r"\bcannot\b", r"\bit is\b",
                r"\byou are\b", r"\bwe are\b", r"\bthey are\b", r"\bI will\b", r"\bI have not\b",
                r"\bis not\b", r"\bare not\b", r"\bthat is\b", r"\blet us\b", r"\bwill not\b",
                r"\bI would\b", r"\bdid not\b"]
ESL = [
    (r"\b(open|close) the (light|lights|lamp)\b", "turn on / turn off the light"),
    (r"\blos(e|t) the (bus|train|ferry)\b", "miss the bus"),
    (r"\bi am agree\b", "I agree"),
    (r"\binformations\b", "information / info"),
    (r"\badvices\b", "advice"),
    (r"\b(am|is|are|'m|'s|'re) \w+ing (here |there )?since\b", "present perfect: I've been ...ing since"),
    (r"\bsince \d+ (minutes|hours|days|weeks|months|years)\b", "for N hours (not since)"),
    (r"\bwaiting (us|me|you|him|her|them)\b", "waiting for us"),
    (r"\bvery very\b", "one stronger word (freezing, starving...)"),
    (r"\bpull(ed)? a (photo|picture)\b", "take a photo"),
    (r"\bsee a dream\b", "have a dream"),
    (r"\bgive (you )?(a|my) word\b", "promise"),
    (r"\bclose the phone\b", "hang up"),
    (r"\buntil tomorrow\b.*\b(finish|done|ready)\b|\b(finish|done|ready)\b.*\buntil tomorrow\b", "by tomorrow"),
    (r"^\s*is (very |so |really )?(cold|hot|dark|late|far|dangerous)\b", "missing subject: It's ..."),
    (r"\bhow are you\?\s*i'?m fine,? thank you", "textbook exchange"),
    (r"\b(am|is|are|'m|'s|'re)( not)? (seeing|knowing|understanding|wanting|liking|needing|believing|remembering|hearing)\b",
     "stative verb in continuous: I can't see / I don't know"),
]
TRIPLET = re.compile(r"\b(\w{3,}), (\w{3,}),? and (\w{3,})\b", re.I)

SEV_ORDER = {"HIGH": 0, "MED": 1, "LOW": 2}

# -------------------------------------------------------------- parsing ----

LINE_RE = re.compile(r"^\s*([A-Za-z][\w .'\-]{0,30}?)\s*:\s*(.+)$")
SKIP_PREFIXES = ("title:", "tags:", "position:", "colorid:", "---", "===", "<<", "->", "//", "#", "~", "*", "+", "=")


def parse_text(raw):
    lines = []
    for n, line in enumerate(raw.splitlines(), 1):
        s = line.strip()
        if not s or s.lower().startswith(SKIP_PREFIXES):
            continue
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("(") and s.endswith(")")):
            continue
        s = re.sub(r"<<.*?>>", "", s)          # inline yarn commands
        s = re.sub(r"#\w[\w:]*", "", s).strip()  # yarn line tags
        s = re.sub(r"\s*\[[^\]]*\]\s*$", "", s)  # trailing stage direction
        m = LINE_RE.match(s)
        if m:
            speaker, text = m.group(1).strip(), m.group(2).strip()
            if speaker.lower() in ("http", "https"):
                continue
            lines.append({"n": n, "speaker": speaker, "text": text})
    return lines


def parse_json(raw):
    data = json.loads(raw)
    out, counter = [], 0

    def take(items):
        nonlocal counter
        for it in items:
            if isinstance(it, dict) and "lines" in it:
                take(it["lines"])
            elif isinstance(it, dict) and "text" in it:
                counter += 1
                out.append({"n": it.get("id", counter), "speaker": it.get("speaker", "?"),
                            "text": str(it["text"])})
    if isinstance(data, dict):
        take(data.get("lines", [data]))
    elif isinstance(data, list):
        take(data)
    return out


def load(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if raw.lstrip().startswith(("[", "{")):
        try:
            return parse_json(raw)
        except json.JSONDecodeError:
            pass
    return parse_text(raw)

# --------------------------------------------------------------- checks ----


def lint(lines, max_chars=90, formal=()):
    findings = []
    formal = {f.lower() for f in formal}
    cast = {l["speaker"] for l in lines if l["speaker"] != "?"}
    cast_names = {c.split()[0].capitalize() for c in cast if len(c) > 1}

    def add(sev, l, rule, hint):
        findings.append({"sev": sev, "line": l["n"], "speaker": l["speaker"],
                         "text": l["text"][:110], "rule": rule, "hint": hint})

    for l in lines:
        t, tl = l["text"], l["text"].lower()
        L = len(t)
        if L > max_chars * 1.5:
            add("HIGH", l, f"too long ({L} chars)", f"split into bubbles <= {max_chars}")
        elif L > max_chars:
            add("MED", l, f"long ({L} chars)", f"target <= {max_chars}")
        for w in AI_VOCAB:
            if re.search(r"\b" + re.escape(w) + r"\b", tl):
                add("HIGH", l, f"AI vocabulary: '{w}'", "use a plain, concrete word")
        for w in AI_TRANSITIONS:
            if tl.startswith(w) or f" {w} " in f" {tl} ":
                add("MED", l, f"essay transition: '{w}'", "people say: also / and / but / anyway")
        for p in THEME_STATEMENTS:
            if re.search(p, tl):
                add("HIGH", l, "theme stated out loud", "cut; let the player infer it")
                break
        for p in EXPOSITION:
            if re.search(p, tl):
                add("HIGH", l, "'As you know, Bob' exposition", "move info to world / argument / newcomer")
                break
        if EMOTION_NAMING.search(t):
            add("MED", l, "emotion announced", "leak it: deflection, action, specific detail")
        for w in THERAPY:
            if w in tl:
                add("MED", l, f"therapy-speak: '{w}'", "wrong register for most game worlds")
        for w in GENERIC_CHEER:
            if w in tl:
                add("LOW", l, f"generic reassurance: '{w}'", "something only THIS character would say")
        for p in NOT_X_BUT_Y:
            if re.search(p, tl):
                add("MED", l, "'not X but Y' construction", "say the real thing once, plainly")
                break
        for p in DESCRIBE_VISIBLE:
            if re.search(p, tl):
                add("LOW", l, "describes what the player can see", "react instead of describe")
        dashes = t.count("\u2014") + t.count(" -- ")
        stripped = t.rstrip()
        trailing = stripped.endswith("\u2014") or stripped.endswith("--")
        if dashes - (1 if trailing else 0) > 0:
            add("LOW", l, "em dash mid-line", "keep em dashes for interruptions; else comma/period")
        m = TRIPLET.search(t)
        if m:
            add("LOW", l, f"triplet: '{m.group(0)}'", "one precise detail beats three generic ones")
        if l["speaker"].lower() not in formal:
            hits = [p for p in UNCONTRACTED if re.search(p, t)]
            if hits:
                ex = re.search(hits[0], t).group(0)
                add("LOW", l, f"uncontracted '{ex}'", "contract, or add speaker to --formal if deliberate")
        for p, fix in ESL:
            if re.search(p, tl):
                add("MED", l, "non-native pattern", fix)

    # ---- script-level checks
    n = len(lines)
    if n:
        # name overuse
        name_lines = [l for l in lines
                      if any(re.search(r"\b" + re.escape(nm) + r"\b", l["text"])
                             for nm in cast_names if nm.lower() != l["speaker"].split()[0].lower())]
        if n >= 6 and len(name_lines) / n > 0.25:
            findings.append({"sev": "MED", "line": "-", "speaker": "*",
                             "text": f"{len(name_lines)}/{n} lines address someone by name",
                             "rule": "name overuse", "hint": "real people rarely say each other's names"})
        # exclamation density
        excl = sum(1 for l in lines if l["text"].rstrip().endswith("!"))
        if n >= 6 and excl / n > 0.2:
            findings.append({"sev": "LOW", "line": "-", "speaker": "*",
                             "text": f"{excl}/{n} lines end with '!'",
                             "rule": "exclamation inflation", "hint": "cap at 1-2 per scene"})
        # repeated openers
        openers = Counter(re.sub(r"[^\w']", "", l["text"].split()[0]).lower()
                          for l in lines if l["text"].split())
        if n >= 8:
            w, c = openers.most_common(1)[0]
            if c / n > 0.25:
                findings.append({"sev": "LOW", "line": "-", "speaker": "*",
                                 "text": f"'{w}' opens {c}/{n} lines",
                                 "rule": "repetitive openers", "hint": "vary sentence starts"})
        # monologues
        run_sp, run_len, run_start = None, 0, None
        for l in lines + [{"speaker": None, "n": None, "text": ""}]:
            if l["speaker"] == run_sp:
                run_len += 1
            else:
                if run_sp and run_len >= 4:
                    findings.append({"sev": "MED", "line": run_start, "speaker": run_sp,
                                     "text": f"{run_len} consecutive lines",
                                     "rule": "monologue", "hint": "break with a reaction, action or interruption"})
                run_sp, run_len, run_start = l["speaker"], 1, l["n"]
        # sameness of length (symmetry)
        if n >= 8:
            lens = [len(l["text"]) for l in lines]
            mean = sum(lens) / n
            var = sum((x - mean) ** 2 for x in lens) / n
            if mean > 25 and (var ** 0.5) / mean < 0.25:
                findings.append({"sev": "LOW", "line": "-", "speaker": "*",
                                 "text": f"line lengths very uniform (mean {mean:.0f})",
                                 "rule": "symmetrical rhythm", "hint": "mix fragments with longer lines"})
    def line_key(v):
        return (0, int(v), "") if str(v).isdigit() else (1, 0, str(v))
    findings.sort(key=lambda f: (SEV_ORDER[f["sev"]], line_key(f["line"])))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--max-chars", type=int, default=90)
    ap.add_argument("--formal", action="append", default=[], help="speaker who deliberately avoids contractions")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any HIGH finding")
    a = ap.parse_args()

    lines = load(a.path)
    if not lines:
        print("No dialogue lines found. Expected 'SPEAKER: text' or JSON with speaker/text.")
        sys.exit(2)
    findings = lint(lines, a.max_chars, a.formal)

    if a.json:
        print(json.dumps({"lines": len(lines), "findings": findings}, indent=2))
    else:
        counts = Counter(f["sev"] for f in findings)
        speakers = Counter(l["speaker"] for l in lines)
        print(f"Parsed {len(lines)} lines, {len(speakers)} speakers: "
              + ", ".join(f"{s}({c})" for s, c in speakers.most_common()))
        print(f"Findings: HIGH {counts.get('HIGH', 0)} | MED {counts.get('MED', 0)} | LOW {counts.get('LOW', 0)}\n")
        by = defaultdict(list)
        for f in findings:
            by[f["sev"]].append(f)
        for sev in ("HIGH", "MED", "LOW"):
            if by[sev]:
                print(f"== {sev} ==")
                for f in by[sev]:
                    print(f"  L{f['line']:<5} {f['speaker'][:10]:<10} {f['rule']}")
                    print(f"         \"{f['text']}\"")
                    print(f"         -> {f['hint']}")
                print()
        if not findings:
            print("Clean. Still do the read-aloud pass.")
    if a.strict and any(f["sev"] == "HIGH" for f in findings):
        sys.exit(1)


if __name__ == "__main__":
    main()
