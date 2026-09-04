# AI search visibility (GEO / AEO)

Contents: [Framing](#framing) · [Crawler access](#1-crawler-access-the-single-biggest-blocker) · [Citation testing](#2-citation-testing-run-it-yourself) · [Retrievability](#3-retrievability) · [Answer-first content](#4-answer-first-content-structure) · [Entity strategy](#5-entity-strategy) · [Third-party presence](#6-third-party-presence) · [llms.txt](#7-llmstxt-the-honest-answer) · [Measurement](#8-measurement)

## Framing

The terminology is unsettled — GEO (Generative Engine Optimization), AEO (Answer Engine Optimization), LLMO, "AI SEO" all describe the same work. Use whichever term the user used and don't lecture them about it.

The important framing, and the one to give the user: **this is a layer on top of SEO, not a replacement for it.** Google's own position is that its AI features run on the same ranking systems and require no special optimization, and the documentation says plainly that there are no additional technical requirements to appear in AI Overviews or AI Mode beyond being indexed and eligible for a snippet. Independent studies keep finding that the sites cited by AI answers are heavily drawn from pages that already rank well in conventional search — though the estimates vary widely between studies, so treat any specific percentage as directional rather than settled.

What that means practically: a site with broken indexation will not be fixed by GEO tactics. Do the technical work first. Then optimize for extractability.

What genuinely changes: the goal shifts from *a ranked link* to *a cited passage*. Users increasingly get the answer without a click, so success is measured in citation share and brand mention, and the traffic that does arrive is lower-volume and higher-intent. Say this to the user explicitly — it reframes what "success" means and prevents them from reading a click decline as pure failure.

---

## 1. Crawler access — the single biggest blocker

Most AI providers now run **two separate crawlers**, and conflating them is the most common and most expensive mistake in this whole area:

| Purpose | Examples | Blocking it means |
|---|---|---|
| **Training** — feeds model weights | `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `CCBot` | The model has no background knowledge of the brand |
| **Search / retrieval** — fetches live pages to answer and cite | `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | **No citations, ever** — this is the one that costs visibility |
| **User-triggered fetch** — a user clicked a link | `ChatGPT-User`, `Claude-User` | The user's own request fails |

Countless sites blanket-blocked AI bots during the 2023–24 wave of concern and never revisited it. If the goal is AI visibility, **the retrieval crawlers must be allowed** — blocking `GPTBot` while allowing `OAI-SearchBot` is a perfectly coherent position (no training use, still citable), and it is often exactly what a business actually wants.

Two more things to check:
- Blocking `Google-Extended` does **not** affect Googlebot or organic rankings; they're separate. Correct the misconception if the user raises it.
- The CDN can override the intent. Cloudflare's bot-management settings and similar WAF rules block AI crawlers at the edge regardless of what robots.txt says. If robots.txt looks permissive but the site is absent from AI answers, check the CDN configuration — this is a genuinely common and invisible failure.

A workable baseline to give the user, adapted to their training-data stance:

```
# Retrieval / answer engines — allow these to stay citable
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

# User-triggered fetches
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

# Training crawlers — decide deliberately; Allow: / if comfortable
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: *
Allow: /
Disallow: /sepet/
Disallow: /hesabim/
Disallow: /*?s=

Sitemap: https://example.com/sitemap.xml
```

Caveat honestly: robots.txt is a voluntary standard (RFC 9309), not enforcement. Compliance among declared crawlers is generally good; user-triggered fetchers and undeclared scrapers frequently ignore it. If the user's goal is actually to *prevent* access rather than to signal a preference, that requires WAF-level blocking, and you should say so instead of pretending robots.txt does it.

---

## 2. Citation testing — run it yourself

This is where an AI agent doing the audit can produce something a static checklist can't. Don't theorize about AI visibility; measure it.

**Method:**

1. Write 8–12 questions a real prospective customer would type — natural language, not keywords. Cover the funnel: category-defining ("what is FinOps"), comparison ("best cloud cost tools for mid-size companies"), evaluative ("is X worth it"), and problem-first ("how do I cut AWS spend without losing performance"). Include Turkish-language versions if the market is Turkey; citation behavior differs by language and the gap is often larger there.
2. Search each one and record: which domains get cited, what the cited passage looks like (a definition? a table row? a step list? a statistic?), and whether the user's site appears at all.
3. Build a citation-share table: query, cited sources, user's site present Y/N, format of the winning passage.

**Also account for query fan-out.** Answer engines decompose a complex question into several narrower sub-queries and retrieve for each independently. So a page can win the broad question by owning several of its parts. When a target question is complex, break it into its likely sub-questions and check coverage for each — the gaps there are the content brief.

This table is usually the most persuasive artifact in the whole report, because it turns "you should think about AI search" into "here are eleven questions where three competitors get cited and you don't."

---

## 3. Retrievability

For a passage to be cited, it has to be cleanly fetchable and cleanly extractable:

- **Server-rendered main content.** Covered in `01-technical.md` §5 and it matters more here. Several AI crawlers execute little or no JavaScript. Content that appears only after hydration may as well not exist.
- **Fast, stable 200 responses.** Retrieval happens under a latency budget; slow or flaky origins get dropped.
- **No redirect chains** on content URLs.
- **Not gated.** Content behind a login, an email wall, or an aggressive interstitial can't be cited.
- **Clean HTML semantics.** `<article>`, `<h1>`–`<h3>`, `<table>`, `<ol>` — real markup gives the extractor structure. A page built from nested `<div>`s with CSS-only visual hierarchy has none.
- **Text, not images.** Data locked in a screenshot or an infographic is invisible. Put the numbers in a table and use the image alongside.

---

## 4. Answer-first content structure

The patterns that correlate with getting quoted:

- **Lead with the answer.** A direct, self-contained 40–60 word answer immediately under the heading, then the depth. The passage has to make sense lifted out of context, so it should not begin with "As we mentioned above" or depend on the previous paragraph.
- **One question per heading**, phrased the way people ask it. The heading is the retrieval key.
- **Short paragraphs**, two to four sentences.
- **Specificity beats fluency.** Concrete numbers, dates, named tools, versions, prices, and measurements are far more citable than smooth generalities. Research into what raises citation rates keeps landing on the same cluster: verifiable statistics, quotations from named sources, and explicit citations to primary sources. Treat the specific reported lift figures as directional, but the direction is well-supported.
- **Attribute claims.** "According to Google's Search Central documentation…" with a link. Cited content cites.
- **Comparison tables** for anything vs. anything. They are lifted almost verbatim into answers.
- **Numbered steps** for procedures.
- **A definition block** for the category term, written so it stands alone.
- **Freshness.** Visible, real update dates. Answer engines skew toward recent sources on anything time-sensitive.
- **Consistency across the site.** Contradicting yourself between the pricing page and a blog post lowers confidence in both.

What *doesn't* work: keyword stuffing (models don't count keywords), thin AI-generated filler (it's the exact thing recent core updates target), and walls of undifferentiated prose.

---

## 5. Entity strategy

Answer engines reason about entities — the company, its products, its people — rather than strings. Make the entity unambiguous:

- **One canonical name**, used identically everywhere. If the brand appears as "Cloud4Next", "Cloud 4 Next" and "C4N" across the web, that's three weak entities instead of one strong one.
- **An entity home page** — a real About page stating what the company is, what it does, where it operates, when it was founded, who runs it.
- **`Organization` schema with `sameAs`** pointing to every authoritative profile: LinkedIn, Crunchbase, GitHub, X, Wikidata if applicable. This is the machine-readable statement that all these profiles are the same entity. See `04-schema-2026.md`.
- **Consistent descriptions** across LinkedIn, directories, app stores, and press. Contradictory self-descriptions produce a fuzzy entity.
- **Named people** with `Person` schema and consistent bios — expertise attaches to people, and models track them.
- **Explicit relationships**: what category the product belongs to, what it integrates with, who it competes with. Say these things in plain text on the site; don't leave the model to infer them.

---

## 6. Third-party presence

Answer engines lean heavily on aggregators, listicles, review platforms, and community discussion — a brand's own site is one voice among many, and often not the decisive one.

So the off-site work is a real part of the strategy:

- Get included in the "best X" and "top N alternatives" articles in the category. Identify them by running the comparison queries from §2 and listing every source cited. Each one is a concrete outreach target.
- Category review platforms (G2, Capterra, Trustpilot, and the sector-relevant local equivalents) — claimed profiles, current information, an active review flow.
- Wikipedia/Wikidata where notability is genuine; never fabricate it.
- Community presence where the audience actually is (Reddit, Stack Overflow, sector forums, LinkedIn), participating honestly. Astroturfing is both against platform rules and easy to detect — don't recommend it.
- Original research and data. A study with numbers nobody else has is the most reliably cited artifact type there is, because it can't be synthesized from existing sources.

---

## 7. llms.txt — the honest answer

A proposed markdown file at `/llms.txt` listing a site's key content for language models.

Where things actually stand: Google has stated on the record that it does not support it and does not plan to, with Google staff comparing it to the old keywords meta tag; no major answer engine has publicly confirmed using it for ranking or citation; and crawler-log studies report negligible request volume against it. Meanwhile Google's own Lighthouse tooling checks for it, which has produced visible mixed messaging between Google teams.

So: **it is cheap, harmless, and currently unproven.** The right recommendation is to say exactly that, put it at P3 if the user wants to hedge on an emerging standard, and be clear it should not displace an hour spent on robots.txt, server-rendering, or content structure. Do not present it as a requirement — that's how you lose credibility with a technical audience.

If they want one anyway, the format is a markdown H1 with the site name, a blockquote summary, and sections of annotated links to the most important pages.

---

## 8. Measurement

Set up the baseline so progress is provable:

- **Referral traffic from AI sources.** Analytics segment for `chatgpt.com`, `perplexity.ai`, `claude.ai`, `copilot.microsoft.com`, `gemini.google.com`. Usually small volume, notably higher engagement and conversion — worth reporting separately rather than losing inside "Referral."
- **Server-log or CDN monitoring of AI crawler user-agents** — confirms they're actually reaching the site, which is the thing robots.txt only *requests*.
- **Repeated citation testing.** Re-run the §2 query set monthly and track the share. Manual and slightly tedious, but it's real data the user owns.
- **Branded search volume**, as a proxy for entity strength.
- Commercial trackers exist (Semrush and Ahrefs both ship AI-visibility features, plus a crop of dedicated tools). Mention them as options; don't endorse one.

Timeline to set expectations: retrieval-based engines can reflect structural changes within weeks; anything depending on training data or entity recognition takes far longer. Don't promise a fast turnaround.
