# Content and on-page

Contents: [Intent](#1-search-intent) · [Titles and meta](#2-titles-and-meta-descriptions) · [Headings and body](#3-headings-and-body-structure) · [Images](#4-images-and-media) · [Thin and duplicate](#5-thin-duplicate-and-cannibalizing-content) · [E-E-A-T](#6-e-e-a-t) · [Topical authority](#7-topical-authority-and-clusters) · [Internal linking](#8-internal-linking) · [Content gaps](#9-content-gap-analysis) · [Local](#10-local-seo) · [Off-page](#11-off-page)

---

## 1. Search intent

The most common reason a well-optimized page doesn't rank is that it answers a different question than the one being asked. Before critiquing a page's tags, check whether its *format* matches the SERP.

For each target query, run the search and look at what's actually ranking. If the first page is dominated by comparison listicles and the user has a product page, no amount of on-page work will fix that — they need a different page type. Classify the intent as informational, commercial investigation, transactional, or navigational, and check the page type against it.

Also read the SERP for what Google thinks the query means: People Also Ask boxes reveal the subquestions to cover, the presence of an AI Overview tells you the click is likely to be absorbed, and the ranking pages' formats (video, tool, calculator, guide) show what "satisfying" looks like here.

---

## 2. Titles and meta descriptions

**Title tag.** One per page, unique. Roughly 50–60 characters before truncation, though the real limit is pixel width. Primary term near the front, brand at the end if it earns its place. Written for the click, not for a keyword-density score. Google rewrites titles it considers unhelpful — a title that's just a keyword stuffed list invites rewriting, which means losing control of the snippet.

Check for: duplicated titles across templates (a strong sign of a template bug), missing titles, titles that are just the brand name, and titles generated from a field that's empty on half the pages.

**Meta description.** Not a ranking factor, but it is the ad copy for the result. Around 150–160 characters, with the value proposition and a reason to click. Missing descriptions mean Google pulls an arbitrary passage. On a large site with thousands of product pages, templated descriptions with distinct variables beat both hand-writing and leaving them blank.

When rewriting titles and meta for the user, write actual copy for their actual pages — with character counts — not instructions on how to write copy.

**Open Graph and Twitter cards.** Not organic ranking factors but they govern how shared links appear, which affects the social and referral channel. Cheap to fix; group them as a P3 batch.

---

## 3. Headings and body structure

- Exactly one H1, matching the page's actual subject. Not the site logo alt, not the nav.
- Logical H2/H3 nesting without skipped levels. Headings should read as an outline of the page if extracted alone — this is exactly how AI systems chunk content.
- Descriptive headings ("How pricing works for teams under 50") beat clever ones ("The good stuff"). They are the retrieval handles.
- Short paragraphs. Two to four sentences. This is not a style preference in 2026 — extraction systems lift discrete passages, and a 200-word block is a worse candidate than three tight ones.
- The answer to the page's core question appears in the first 100–150 words, before the setup and the brand story. Both readers and answer engines reward getting to the point.
- Tables, definition lists, and numbered steps where the content is genuinely structured. Highly extractable and genuinely more readable.

---

## 4. Images and media

- Descriptive `alt` text that would make sense read aloud. Empty `alt=""` is correct for decorative images; missing `alt` is not the same thing.
- Descriptive filenames (`kurumsal-finops-panosu.webp`, not `IMG_4471.jpg`).
- Modern formats (AVIF/WebP), responsive `srcset`, explicit dimensions.
- Video: transcripts and a `VideoObject` where relevant. Transcripts are the only way the content becomes text-searchable and quotable.

---

## 5. Thin, duplicate, and cannibalizing content

- **Thin pages**: pages that exist for a keyword rather than a reader. Location pages differing only in the city name, tag archives with two posts, near-empty category pages. The choice per page is improve, consolidate, or remove — and "remove with a 301 to the closest relevant page" is a legitimate, underused answer.
- **Duplicate content**: same copy on multiple URLs, boilerplate manufacturer product descriptions, printer variants, HTTP/HTTPS/www variants.
- **Cannibalization**: several pages competing for one query, splitting signals so none rank. Detect it with `site:domain.com "target phrase"` — if four pages come back and they're all trying to be the answer, that's the finding. Fix by consolidating into one strong page and redirecting the rest, or by differentiating them onto genuinely distinct queries.
- **Content decay**: pages that used to rank and have gone stale. Refreshing a decaying page with real updates usually outperforms writing a new one. Requires GSC data — mark `[NEEDS DATA]`.

---

## 6. E-E-A-T

Experience, Expertise, Authoritativeness, Trust. Not a score Google computes; a framework its quality raters use and its systems approximate. It matters most for YMYL topics — health, finance, legal, safety — and a FinOps or fintech site sits closer to that end than a general blog does.

What's checkable on the page:

- **Named authors** with real bios, credentials, and their own author pages — not "Admin" or "Editorial Team."
- **First-hand experience** in the writing: original screenshots, our-own-data, "we tested this across 40 deployments." This is the single hardest thing for a competitor or a language model to replicate, and in 2026 it is the main differentiator between content that gets cited and content that gets summarized away.
- **Citations to primary sources**, with outbound links. Linking out does not leak ranking power in any way that matters; it builds credibility.
- **Dates**: published and meaningfully updated. Fake "updated today" stamps on unchanged content are a trust problem.
- **Trust infrastructure**: real physical address, phone, company registration details, privacy policy, terms, refund policy, visible contact routes. For a Turkish company: `Mersis` number, `ticaret sicil` details, and a KVKK notice are ordinary trust signals in that market.
- **Third-party corroboration**: reviews, press mentions, certifications, customer logos with substance behind them.

---

## 7. Topical authority and clusters

Google is not evaluating pages in isolation; it's evaluating whether the site is a credible source on a subject. The mechanism people use for this is the pillar-and-cluster structure: one comprehensive hub page for the topic, and a set of supporting pages each covering one subtopic in depth, with bidirectional internal links between hub and spokes.

For the audit:

1. Map what the site currently covers — group all URLs by topic.
2. Identify which topics have a hub, which have orphaned spokes with no hub, and which have a hub with no supporting depth.
3. Compare against competitors' coverage of the same topic space. The gaps are the content roadmap.
4. Check that cluster pages actually link to each other and to the hub. A cluster that isn't linked is not a cluster; it's a pile of posts.

Be honest about timelines. Cluster strategies compound over 3–12 months. Anyone promising faster is selling something.

---

## 8. Internal linking

Underrated, free, and entirely within the user's control.

- Do the money pages have meaningful inbound internal links from relevant content, or are they only reachable from the nav?
- Anchor text: descriptive and varied. "Read more" and "click here" pass no topical signal.
- Orphan pages with zero internal links.
- Excessive links in body copy diluting each one — no fixed number, but a paragraph with eight links is doing nothing for any of them.
- Cross-cluster links only where there's a genuine relationship. Random interlinking muddies topical signals.
- Footer link dumps: low value, and if the count is large it looks manipulative.

Deliverable: a concrete list of "add a link from page A to page B with anchor text C." That's a task someone can execute this afternoon, which makes it one of the highest-completion-rate recommendations in any audit.

---

## 9. Content gap analysis

Without paid tools you can still do a real version of this:

1. Take the site's core topics.
2. For each, run the searches a buyer would run and record who ranks.
3. Read the People Also Ask questions — free, direct evidence of the subquestions.
4. Fetch the top-ranking competitor pages and note what they cover that the user's page doesn't.
5. Where the user has GSC data, the highest-value gap is usually queries where they already rank positions 5–15 — existing relevance, one push from real traffic. Ask for that export.

Output a prioritized content roadmap: target query, intent, page type, working title, primary subtopics to cover, internal links in and out, and which existing page it replaces or supports.

---

## 10. Local SEO

In scope when the business has a physical location or serves a defined area.

- Google Business Profile: claimed, categorized correctly, complete, with recent photos, posts, Q&A, and an active review flow.
- NAP consistency — name, address, phone identical everywhere on the web. In Turkey that includes the ordinary directory set alongside Google.
- `LocalBusiness` schema matching the profile exactly.
- Location pages with genuinely local content, not templated city-swaps.
- Embedded map, transit and parking notes, local landmarks — the things that prove the location is real.

---

## 11. Off-page

You can't audit a backlink profile from outside, so scope this honestly.

What you *can* do: search the brand name and see who mentions it, check whether the site owns branded search, look at whether they appear in the industry's obvious listicles and directories, and note the "best X" articles in their category that don't mention them — every one of those is a concrete outreach target, and in 2026 those same listicles are heavily used by AI answer engines.

What you can't: link counts, authority metrics, toxic-link assessment. Mark `[NEEDS DATA]` and name Ahrefs/Semrush/Moz plus GSC's own links report (free, and the only one that's Google's actual data).

Recommend earned links — original research, data studies, tools, expert commentary, digital PR — and refuse to help with paid link schemes or PBNs, explaining the manual-action risk rather than just declining.
