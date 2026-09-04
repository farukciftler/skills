#!/usr/bin/env python3
"""Build and validate the iOS App Store 100-character keyword field.

Why this exists: the keyword field has a set of mechanical rules that are easy to state
and tedious to apply by hand -- words already in the title or subtitle are wasted, plurals
are handled automatically by Apple, stop words and generic terms are free, spaces after
commas cost characters, and competitor brands are a policy risk. Doing this by eye
reliably leaves 10-20 characters of unused budget on the table.

Usage
-----
  python3 keyword_field.py \
      --title "Loop: Habit Tracker" \
      --subtitle "Daily goals and streaks" \
      --keywords "habit,habits,routine,tracker,daily,goal,goals,streak,productivity,todo,app,free,reminder,checklist,self care,discipline,motivation" \
      --locale en-US

  # Just audit an existing field:
  python3 keyword_field.py --keywords "..." --title "..." --subtitle "..." --audit-only

Output: the packed field, character and byte counts, and a line-by-line report of every
term that was dropped and why -- so the reasoning can go straight into a deliverable.
"""

import argparse
import re
import sys
import unicodedata

# Indexed for free via the category, or explicitly discouraged by Apple.
GENERIC = {
    "app", "apps", "application", "free", "new", "best", "top", "good", "great",
    "iphone", "ipad", "ios", "apple", "mobile", "download", "online", "offline",
    "pro", "plus", "premium",
}

# English stop words. Apple names "the" and "to" explicitly; the rest follow the same logic.
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "by", "for",
    "with", "from", "up", "out", "is", "it", "as", "be", "are", "was", "your", "my",
    "you", "we", "i", "this", "that", "all", "any", "can", "will", "not", "no",
}

# A short list of very common app brands, as a nudge rather than a filter. Guideline 2.3.7
# prohibits competitor names in metadata; the consultant should decide, not the script.
COMMON_BRANDS = {
    "instagram", "facebook", "whatsapp", "tiktok", "snapchat", "youtube", "spotify",
    "netflix", "uber", "airbnb", "duolingo", "notion", "slack", "zoom", "telegram",
    "twitter", "linkedin", "pinterest", "reddit", "discord", "strava", "calm",
    "headspace", "revolut", "paypal", "venmo", "canva", "chatgpt", "gemini",
}


def normalize(word):
    return unicodedata.normalize("NFKC", word).strip().lower()


def singularize(word):
    """Rough English singular form.

    Apple treats singular and plural as duplicates and handles them automatically, so
    listing both is wasted budget. This is deliberately conservative -- it only strips
    endings it is confident about, because a false positive silently drops a real keyword.
    """
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith(("ses", "xes", "zes", "ches", "shes")):
        return word[:-2]
    if word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def tokenize_field(raw):
    """Split a keyword field on commas; keep multi-word phrases intact for reporting."""
    return [t.strip() for t in raw.split(",") if t.strip()]


def words_in(text):
    return {normalize(w) for w in re.findall(r"[^\s,\-_/|]+", text or "") if w}


def build(title, subtitle, candidates, limit=100, keep_phrases=False):
    covered = set()
    for w in words_in(title) | words_in(subtitle):
        covered.add(singularize(w))

    kept, dropped = [], []
    seen = set()

    for term in candidates:
        norm = normalize(term)
        if not norm:
            continue

        # Apple permutes single words across title, subtitle and the keyword field into
        # multi-word queries, so phrases usually waste characters on a space.
        if " " in norm and not keep_phrases:
            parts = [p for p in norm.split() if p]
            for p in parts:
                candidates.append(p)
            dropped.append((term, "phrase split into single words (Apple permutes words itself)"))
            continue

        if len(norm) <= 2:
            dropped.append((term, "2 characters or fewer - Apple requires more than 2"))
            continue
        if norm in STOP_WORDS:
            dropped.append((term, "stop word - not indexed, wastes characters"))
            continue
        if norm in GENERIC:
            dropped.append((term, "generic/auto-indexed term - Apple indexes category and 'app' for free"))
            continue

        base = singularize(norm)
        if base in covered:
            reason = ("already in title/subtitle - indexing does not stack"
                      if base in words_in(title) | words_in(subtitle) or base in covered
                      else "duplicate")
            dropped.append((term, reason))
            continue
        if base in seen:
            dropped.append((term, "duplicate or plural of a term already included"))
            continue

        seen.add(base)
        kept.append((term.strip(), base))

    # Pack greedily in the given priority order, then try to backfill with anything short
    # enough to fit in the remainder -- unused budget is pure loss.
    field, packed, skipped_for_space = "", [], []
    for original, base in kept:
        token = original.strip()
        addition = token if not field else "," + token
        if len(field) + len(addition) <= limit:
            field += addition
            packed.append(token)
        else:
            skipped_for_space.append(token)

    for token in list(skipped_for_space):
        addition = "," + token
        if len(field) + len(addition) <= limit:
            field += addition
            packed.append(token)
            skipped_for_space.remove(token)

    brand_flags = [t for t in packed if normalize(t) in COMMON_BRANDS]
    return field, packed, dropped, skipped_for_space, brand_flags


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--keywords", required=True,
                   help="Comma-separated candidate keywords, highest priority first")
    p.add_argument("--title", default="", help="App name (30 chars) - words here are already indexed")
    p.add_argument("--subtitle", default="", help="Subtitle (30 chars) - words here are already indexed")
    p.add_argument("--limit", type=int, default=100, help="Character limit (default 100)")
    p.add_argument("--locale", default="en-US", help="Locale label for the report")
    p.add_argument("--keep-phrases", action="store_true",
                   help="Keep multi-word phrases instead of splitting them into single words")
    p.add_argument("--audit-only", action="store_true", help="Report only, don't repack")
    args = p.parse_args()

    candidates = tokenize_field(args.keywords)
    field, packed, dropped, no_space, brands = build(
        args.title, args.subtitle, candidates, args.limit, args.keep_phrases)

    print(f"\n=== iOS keyword field — {args.locale} ===")
    if args.title:
        print(f"Title    ({len(args.title):>2}/30): {args.title}")
    if args.subtitle:
        print(f"Subtitle ({len(args.subtitle):>2}/30): {args.subtitle}")

    if args.audit_only:
        print(f"\nSubmitted field ({len(args.keywords)} chars, "
              f"{len(args.keywords.encode('utf-8'))} bytes)")
    else:
        print(f"\nPacked field ({len(field)}/{args.limit} chars, "
              f"{len(field.encode('utf-8'))} bytes UTF-8):\n\n{field}\n")
        unused = args.limit - len(field)
        if unused > 0:
            print(f"⚠️  {unused} characters unused — unused budget is pure loss. "
                  f"Add long-tail terms until it is 0-2.")

    if len(field.encode("utf-8")) != len(field):
        print("\nℹ️  Non-ASCII characters present. Apple's version-metadata reference says the "
              "field is 100 *bytes*; the marketing page says 100 characters. Verify against "
              "the App Store Connect counter for this locale before submitting.")

    if brands:
        print("\n⚠️  Possible competitor brand names — Guideline 2.3.7 prohibits these in "
              "metadata. Apple may silently strip them; a rejection is possible:")
        for b in brands:
            print(f"      - {b}")

    if dropped:
        print(f"\nDropped ({len(dropped)}):")
        for term, reason in dropped:
            print(f"   - {term:<22} {reason}")

    if no_space:
        print(f"\nDidn't fit ({len(no_space)}) — candidates for a secondary locale's keyword "
              f"field (cross-localization) or a later iteration:")
        for t in no_space:
            print(f"   - {t}")

    print("\nReminders: no space after commas; single words, not phrases; never repeat a word "
          "across title/subtitle/keywords; plurals are automatic; keyword changes only take "
          "effect when a new version ships live.\n")


if __name__ == "__main__":
    sys.exit(main())
