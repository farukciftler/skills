# Report and prioritization

## Prioritization rubric

Score each finding on impact, confidence, and effort, then assign a priority. The point is to make the ranking defensible rather than to produce a precise number — the user should be able to see why item three is above item four.

- **Impact** (1–5): how much organic visibility, traffic, or revenue this plausibly moves.
- **Confidence** (1–5): how sure you are, both that the problem is real and that the fix addresses it. A `[VERIFIED]` finding with a well-understood mechanism scores 5; an `[INFERRED]` one scores 2–3.
- **Effort** (1–5, where 1 is trivial): a config change is 1; a rewrite of the rendering architecture is 5.

| Priority | Meaning | Typical examples |
|---|---|---|
| **P0** | Actively costing visibility right now. Fix this week. | `noindex` in production, `Disallow: /`, broken canonicals across a template, mass 404s after a migration, retrieval crawlers blocked at the CDN |
| **P1** | High impact, achievable in weeks. | Client-side-only main content, missing/duplicate titles sitewide, LCP in the poor band, no `Organization` schema, cannibalization on money terms |
| **P2** | Real gains, needs planning or a content cycle. | Cluster build-out, internal linking programme, E-E-A-T upgrades, hreflang implementation, answer-first rewrites |
| **P3** | Worth doing, low urgency. | Open Graph tags, alt text cleanup, `llms.txt`, minor copy polish |

Two rules that keep this honest: **cap P0 at around five items** — if everything is critical, nothing is — and **put at least two quick wins near the top**, since early completed items are what keep an audit from dying in a backlog.

---

## Report template

Use this structure. Adapt section depth to the brief, but keep the order — it goes from "what should I do" to "here's why," which is the order a decision-maker reads in.

```markdown
# SEO Audit — [domain]
[date] · Scope: [what was examined, how many pages, which templates]

## 1. Executive summary
Three to five sentences. The state of the site, the single biggest opportunity,
and the expected direction if the P0/P1 items are done. Written for someone
who will read only this section.

**Health snapshot**
| Area | State | Note |
|---|---|---|
| Crawl & indexation | 🔴 / 🟡 / 🟢 | one line |
| Rendering & speed | | |
| On-page & content | | |
| Structured data | | |
| AI search visibility | | |
| Authority & entity | | |

## 2. Priority actions
The table someone can work from. Ordered, not grouped by category.

| # | Priority | Finding | Impact | Effort | Owner |
|---|---|---|---|---|---|
| 1 | P0 | … | High | 1h | Dev |

## 3. Findings in detail
One block per finding, in priority order:

### [P0] Short title of the problem
**Status:** [VERIFIED] / [INFERRED] / [NEEDS DATA]
**Where:** the URL(s), or "all pages under /blog/"
**Observed:** the actual evidence — the tag, the directive, the response code
**Why it matters:** the business consequence in plain language
**Fix:** exact code or copy to paste
**Verify:** how to confirm it worked, and roughly when to expect movement

## 4. AI search visibility
The citation-share table from the query testing, then the diagnosis.

| Question tested | Cited sources | Your site | Winning format |
|---|---|---|---|

## 5. Competitor delta
What two or three competitors have that this site doesn't, on the queries
that matter. Structural, not a tag-by-tag comparison.

## 6. Content roadmap
Prioritized list of pages to create, update, consolidate, or remove.
Each with: target query, intent, page type, working title, key subtopics,
internal links in/out.

## 7. 90-day plan
Weeks 1–2, 3–6, 7–12. Grouped by owner (Dev / Content / Marketing) so the
work can be handed out rather than re-triaged.

## 8. Measurement
Baseline metrics recorded today, the KPIs to track, and the review cadence.

## 9. What couldn't be checked
Everything marked [NEEDS DATA], with the tool that would answer it.
This section builds trust rather than undermining it — it shows the rest
of the report is grounded.
```

---

## Writing the findings

**Be specific to this site.** "Your H1 on /cozumler/ is the company slogan rather than the page subject" is a finding. "Make sure H1s are optimized" is filler. If a finding could be copy-pasted into another site's audit unchanged, cut it or make it specific.

**Show the fix, don't describe it.** Give the corrected title tag with its character count, the JSON-LD block with real values, the robots.txt lines, the `<link rel="preload">` tag. Descriptions of fixes get deferred; pasteable fixes get shipped.

**Name the consequence, not the rule.** "This violates best practice" is weak. "Google is choosing its own titles for these pages, so you don't control what appears in the result" is a reason to act.

**Group template-level issues.** If 340 product pages share a broken canonical, that is one finding about one template, not 340 findings. Say how many URLs it affects — that's what conveys the scale.

**Be honest about what's already good.** If the technical foundation is solid, say so and move the weight of the report to content and AI visibility. Manufacturing problems to justify length is the fastest way to lose a technical reader.

---

## KPI framework

Set the baseline in the report so the next review has something to compare against.

**Traditional search**
- Impressions, clicks, CTR, average position (Search Console) — segmented by page group, not just sitewide
- Indexed page count and the "crawled but not indexed" bucket
- Core Web Vitals pass rate at the 75th percentile
- Rankings for the defined target set

**AI search**
- Citation share across the tested query set — re-run monthly
- Referral traffic from AI assistant domains, tracked separately
- AI crawler hits in server or CDN logs
- Branded search volume as an entity-strength proxy

**Business**
- Organic conversions and assisted conversions
- Revenue or pipeline attributed to organic
- Cost per acquisition versus paid channels

**Expectation setting, to state plainly in the report:** technical fixes show up in days to weeks once recrawled. Content and authority work compounds over three to twelve months. Core update recoveries typically wait for a subsequent update. Nobody can guarantee a ranking, and anyone who does is either guessing or lying — say the first half of that sentence in the report and keep the second half to yourself.
