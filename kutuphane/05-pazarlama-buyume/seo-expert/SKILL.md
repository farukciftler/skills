---
name: seo-expert
description: Runs a deep, evidence-based SEO and AI-search (GEO/AEO) audit of a real website and turns it into a prioritized, fix-by-fix action plan with code-level recommendations. Use this whenever the user gives a URL or domain and wants it reviewed, audited, analyzed, improved, or benchmarked against competitors — and also for narrower asks like "why isn't this page ranking", "check my robots.txt / sitemap / canonical / schema / meta tags", "is my site visible in ChatGPT and AI Overviews", "run a technical SEO check", "write meta titles and descriptions", "plan content clusters", or any question about organic traffic drops, Core Web Vitals, structured data, keyword targeting, internal linking, or getting cited by AI answer engines. Trigger it even when the user just pastes a link with a vague ask like "take a look at this site", "bunu bir incele", "sitemi analiz et", or "buraya SEO açısından bak".
---

# SEO Expert

An SEO audit is only worth something if it is *grounded in what the site actually does*. The failure mode of AI-generated SEO advice is a generic checklist that could have been written without ever loading the page: "add meta descriptions, improve page speed, build backlinks." That output is worthless and the user can tell instantly.

So the whole design of this skill is: **fetch first, claim second.** Every finding must trace back to something observed in the site's own HTML, its robots.txt, a search result, or data the user supplied. If it can't be observed, it gets labeled as unverified — not asserted.

## Language of the deliverable

Write the report in whatever language the user is writing in. Keep the standard technical terms (canonical, hreflang, LCP, JSON-LD, schema, crawl budget) in English even in a Turkish report — that is how practitioners actually talk, and translating them makes the report harder to act on.

## Phase 0 — Scope before you crawl

Do not start fetching until the shape of the job is clear. Ask only what you actually need, in one short round (use the interactive options tool if available, otherwise 2-3 inline questions):

1. **The goal.** Ranking for specific commercial terms? Recovering from a traffic drop? Getting cited in AI answers? Pre-launch readiness? A migration post-mortem? The goal decides which phases get depth and which get a skim.
2. **Market and language.** Turkey/Turkish, multi-country, global English? This determines whether hreflang, local SEO, and TR-specific SERP behavior are in scope.
3. **Competitors.** Two or three real ones. If the user doesn't know, derive them in Phase 1 from who ranks for their core terms.
4. **Available data.** Do they have Google Search Console, Analytics, Ahrefs/Semrush exports, or a Screaming Frog crawl? If yes, ask them to paste or upload it — real GSC query data beats anything that can be inferred from the outside, and it changes the audit from "what looks wrong" to "what is actually costing you clicks."

If the user just wants a fast read ("quick look"), say so back and run Phases 1–2 plus a short version of 6. Don't silently downgrade a deep audit.

## Phase 1 — Reconnaissance

Goal: understand what this site *is* before judging it.

- **Fetch the homepage.** Read the raw HTML, not the rendered gist. Note the stack (Next.js, WordPress, Webflow, Shopify, custom), whether main content is present in the served HTML or injected by JavaScript, the title, meta description, canonical, hreflang cluster, viewport, and every JSON-LD block.
- **Fetch `/robots.txt` and `/sitemap.xml`.** These two files explain more failures than anything else on the list.
- **Enumerate what Google actually has.** Run `site:domain.com` searches — plus `site:domain.com/blog/`, `site:domain.com/urun/` and similar for major sections. This gives real indexed URLs you can then fetch, and the rough index size, and it surfaces junk that shouldn't be indexed (staging paths, tag archives, parameter URLs, PDFs).
- **Brand search.** Search the brand name alone. Does the site own its own name? Is there a Knowledge Panel-style entity presence, and what third-party sources (directories, review sites, LinkedIn, news) dominate?
- **Identify page templates.** Most sites have 4–8 templates: homepage, category, product/service, blog post, blog index, about/contact, landing pages. Problems are almost always template-level, not page-level, so fixing one template fixes hundreds of URLs. Sample 1–2 URLs per template for Phase 2.

**A note on fetching:** the fetch tool will only accept URLs that have appeared in the conversation — the user's URL, or ones returned by a search. If a direct path fetch is refused, run a search that surfaces the URL first, then fetch it. If a file genuinely can't be reached (robots.txt behind a WAF, for instance), ask the user to paste its contents rather than guessing what it says.

## Phase 2 — Technical audit

Read `references/01-technical.md` and work through it against the sampled pages. It covers crawlability and indexation, status codes and redirects, canonicalization, JavaScript rendering dependency, Core Web Vitals (including which parts you can and cannot verify from outside), mobile, HTTPS/security, internationalization, and site architecture.

## Phase 3 — On-page and content

Read `references/02-content-onpage.md`. Covers title/meta/heading quality against real SERP competition, search intent alignment, thin and duplicate content, E-E-A-T signals, topical authority and cluster structure, internal linking, and content gaps versus competitors.

## Phase 4 — Structured data

Read `references/04-schema-2026.md`. Extract every JSON-LD block from the sampled pages and validate it by hand: type correctness, required properties, entity linking via `@id` and `sameAs`, and — the one people miss — whether the markup matches what a visitor actually sees on the page. This file also carries the 2026 reality of which schema types still earn rich results and which have been retired.

## Phase 5 — AI search visibility (GEO/AEO)

Read `references/03-ai-search-geo.md`. This is the phase that separates a 2026 audit from a 2019 one, and it's the phase where an AI agent has an unusual advantage: **you can run the queries yourself.**

Take 8–12 questions a real buyer would ask in this category — not keywords, questions — and search them. Record who gets cited, what format the cited passage takes, and whether the user's site appears at all. That produces an actual citation-share baseline instead of speculation. Then diagnose why: crawler access, answer-first structure, entity clarity, third-party corroboration.

## Phase 6 — Competitor delta

Run an abbreviated Phases 1–5 against two or three competitors. You are not writing them an audit; you are answering one question: **what do they have that the user doesn't, on the queries that matter?** Look for structural advantages (content depth, schema coverage, site speed, entity presence, citation share) rather than cataloguing their meta tags.

## Phase 7 — Report

Read `references/05-report-and-priority.md` for the exact deliverable structure and the prioritization rubric. Short version: findings ranked P0–P3 by impact × confidence ÷ effort, each with evidence, business consequence, and a copy-pasteable fix.

## Evidence discipline

These rules are the difference between a useful audit and an expensive-sounding one.

**Every finding carries four things:** the URL where you saw it, what you observed (short verbatim excerpt from the source — a tag, a directive, a heading), why it costs the business something, and the exact fix as code or copy the user can paste.

**Never invent numbers.** No made-up domain authority, traffic estimates, keyword volumes, backlink counts, or "you'll gain 40% traffic." If a number matters and you can't observe it, say which tool produces it and what to look for there.

**Separate observed from inferred from unverifiable.** Mark each finding:
- `[VERIFIED]` — you fetched it and read it.
- `[INFERRED]` — a reasonable conclusion from evidence, stated as such ("the served HTML contains no body copy, which suggests client-side rendering; confirm with the URL Inspection tool").
- `[NEEDS DATA]` — genuinely outside what you can see: CrUX field data, Search Console impressions, backlink profiles, actual rankings, conversion data. Name the tool and the specific report.

**Absence of evidence is not evidence.** If a search doesn't surface a page, that is not proof it's deindexed — it may be a search-provider artifact. Say "did not appear in the searches I ran," not "is not indexed."

**Don't pad.** Twelve real findings beat forty generic ones. If the technical foundation is clean, say it's clean and spend the space on content and AI visibility instead. A short honest audit is a good audit.

**Prefer primary sources.** Google's Search Central documentation and web.dev outrank agency blog posts when they disagree. If you cite an industry statistic, attribute it and treat it as directional, not fact. Where SEO opinion is genuinely divided (llms.txt is the current example), present both sides and the cost of each choice rather than picking one and sounding certain.

## What this skill will not do

Turn down black-hat requests and explain the risk instead: private blog networks and paid link schemes, cloaking or serving different content to crawlers than to users, scaled auto-generated content produced to game rankings, fake reviews or fabricated author bios, scraping competitors' content, and negative SEO against a competitor. These carry real manual-action and reputational risk, and the honest version of expertise is saying so.

Also, if the user asks for a guarantee — "will this get me to number one" — the honest answer is that no one can promise a ranking. Give the expected direction, the realistic time horizon (technical fixes: weeks; content and authority: 3–12 months), and what would falsify the hypothesis.

## Reference files

Read the relevant file at the start of its phase; don't try to hold all of them at once.

| File | Read it for |
|---|---|
| `references/01-technical.md` | Crawl, index, redirects, canonical, JS rendering, Core Web Vitals, mobile, hreflang, architecture |
| `references/02-content-onpage.md` | Titles/meta, intent, thin content, E-E-A-T, topical authority, internal linking, content gaps |
| `references/03-ai-search-geo.md` | AI crawler access, citation testing, answer-first writing, entity strategy, llms.txt |
| `references/04-schema-2026.md` | Which schema still earns rich results in 2026, JSON-LD templates, validation, entity graph |
| `references/05-report-and-priority.md` | Report template, P0–P3 rubric, roadmap format, KPI framework |
