# Technical audit

Contents: [Crawlability](#1-crawlability) · [Indexation](#2-indexation) · [Status codes and redirects](#3-status-codes-and-redirects) · [Canonicalization](#4-canonicalization) · [JavaScript rendering](#5-javascript-rendering) · [Core Web Vitals](#6-core-web-vitals) · [Mobile](#7-mobile) · [Security](#8-security-and-protocol) · [Internationalization](#9-internationalization) · [Architecture](#10-site-architecture) · [Diagnosing a traffic drop](#11-diagnosing-a-traffic-drop)

Priority order when everything is broken at once: **indexation → rendering → canonicalization → Core Web Vitals → speed polish.** A page that isn't indexed cannot be slow-but-ranking; it simply doesn't exist. Don't hand someone a CLS fix while their staging subdomain is outranking production.

---

## 1. Crawlability

### robots.txt

Fetch it and read every line. The recurring disasters:

- `Disallow: /` left in place after a launch or migration. Catastrophic and surprisingly common.
- A wildcard `User-agent: *` block combined with an allowlist for only Googlebot and Bingbot — which silently excludes every AI crawler.
- Disallowed `/wp-content/`, `/assets/`, `/_next/`, or `/static/` paths that block CSS and JS. Google renders pages; blocking its own render resources produces a broken page in its eyes.
- Using `Disallow` when the intent was deindexing. A disallowed URL can still be indexed from external links, and Google can't read the `noindex` on a page it isn't allowed to fetch. Correct pattern: **allow crawling, apply `noindex`** — the opposite of most people's instinct.
- Missing `Sitemap:` line.

Note the crawler-specific rules and carry them into Phase 5 — the AI crawler section in `03-ai-search-geo.md` depends on what you find here.

### XML sitemap

Fetch it (and any child sitemaps in an index file). Check:

- Does it exist and is it referenced from robots.txt?
- Absolute URLs, HTTPS, matching the canonical host (no `www` mismatch).
- Only indexable, canonical, 200-status URLs. A sitemap full of redirects, 404s, and `noindex` pages is a trust signal problem, not just noise.
- `lastmod` reflecting real edits. Bulk-touching every `lastmod` to today's date on every deploy trains Google to ignore the field.
- Under 50,000 URLs / 50MB uncompressed per file.
- Sitemap URL count vs. `site:` result count — a large gap points at either crawl budget problems or mass exclusion.

### Crawl budget

Only matters at scale (roughly 10k+ URLs) or on sites generating infinite URL space. Look for faceted navigation producing parameter combinations, calendar archives, session IDs in URLs, and internal search result pages being crawled. On a 200-page brochure site, crawl budget is a non-issue — don't inflate it into a finding.

---

## 2. Indexation

You can't see Search Console from outside, so triangulate:

- `site:domain.com` for approximate index size.
- `site:domain.com "exact phrase from the page"` to test whether a specific page is known.
- Check the served HTML for `<meta name="robots">` and the `X-Robots-Tag` response header. A `noindex` accidentally shipped from staging to production is one of the highest-value findings you can make.
- Look for the pattern where a whole template carries `noindex, nofollow` — pagination, filtered views, author archives.

Then push the user to the real source: Search Console → Pages report, specifically the "Crawled – currently not indexed" and "Discovered – currently not indexed" buckets. Those two usually mean quality/duplication and crawl-budget problems respectively. Mark as `[NEEDS DATA]`.

**Things that should almost never be indexed:** internal search results, thin tag/archive pages, parameter duplicates, staging and dev subdomains, thank-you and cart pages, printer-friendly variants, PDFs that duplicate an HTML page.

---

## 3. Status codes and redirects

- HTTP → HTTPS: single 301, no chain.
- `www` and non-`www`: one canonical host, the other 301s to it. Check both directions, and with and without trailing slash. Four variants of the homepage all serving 200 is a real duplication problem.
- Redirect chains: each hop dilutes and slows. More than one hop is worth flagging; more than three is a defect.
- Soft 404s: a "product not found" page returning 200. Google indexes these as thin content.
- 302 used where 301 is meant. Temporary redirects that have been in place for two years are a signal error.
- After a migration: is the old URL map fully redirected to matching new URLs, or did everything get dumped onto the homepage? Bulk redirects to the homepage are treated as soft 404s and are the single most common cause of catastrophic post-migration traffic loss.

---

## 4. Canonicalization

For each sampled page check:

- Is there exactly one `<link rel="canonical">`? Two conflicting tags means Google picks one, probably not the one you wanted.
- Is it absolute, HTTPS, and self-referencing on the primary version?
- Does it point to a URL that returns 200 and is itself canonical? Chained canonicals get ignored.
- Does it contradict other signals — canonical says A, sitemap lists B, internal links point to C, hreflang references D? Conflicting signals are worse than no signals; Google resolves them unpredictably.
- Paginated series: each page self-canonical (not all pointing to page 1, which hides deep content).
- Are UTM and other tracking parameters generating indexed duplicates?

---

## 5. JavaScript rendering

This has become the highest-leverage technical check in 2026, because AI answer engines are much less patient renderers than Googlebot. Google will render JavaScript on a second pass; several AI crawlers largely won't. Content that only exists after hydration can be invisible to them entirely.

How to check from the raw fetched HTML:

- Is the main body copy present in the served source, or is there an empty `<div id="root">` / `<div id="__next">` and a bundle of scripts?
- Are H1 and title in the source, or written by client-side JS?
- Is the primary navigation in the source? If internal links only exist after hydration, link equity and discovery both suffer.
- Are JSON-LD blocks in the source or injected later? Injected schema is inconsistently picked up.

If the site is client-rendered, the recommendation is SSR or SSG for content routes — in Next.js terms, server components or `generateStaticParams` rather than a `useEffect` fetch; in Nuxt, SSR mode; for a pure SPA, prerendering for crawlers. Frame it as: *the content needs to exist in the first response.*

Also flag: content hidden behind tabs/accordions is fine for Google, but content that only loads on click via fetch is not indexed. Infinite scroll without paginated fallback URLs hides everything past the first screenful.

---

## 6. Core Web Vitals

Thresholds as of 2026 — unchanged, and each is measured at the **75th percentile of real Chrome users over a rolling 28-day window**:

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

INP replaced FID in March 2024. Any source still discussing FID is stale — say so if the user brings one.

**What you can and can't do here.** You cannot measure field CWV from a fetched HTML document. Mark the actual scores `[NEEDS DATA]` and point the user at PageSpeed Insights (which shows both CrUX field data and a Lighthouse lab run), Search Console's Core Web Vitals report, or a CrUX dashboard. What you *can* do is inspect the HTML for the causes, which is often more actionable than the score:

**LCP causes visible in source:**
- Hero image with no `fetchpriority="high"`, or lazy-loaded (`loading="lazy"` on the LCP element is a classic self-inflicted wound).
- No `<link rel="preload">` for the LCP image or critical font.
- Render-blocking CSS/JS in `<head>` without `defer`/`async`.
- Web fonts without `font-display: swap` and without preload.
- Unoptimized formats — large JPEG/PNG where AVIF or WebP would serve, no `srcset`/`sizes`.
- Third-party tags (chat widgets, tag managers, A/B testing snippets) loading synchronously before content.

**INP causes:** heavy JS bundles, long tasks over 50ms blocking the main thread, expensive event handlers, hydration cost on large component trees, unthrottled scroll/input listeners. INP is the most commonly failed of the three because it's an architecture problem, not a compression problem — you can't fix it by adding a plugin.

**CLS causes visible in source:** `<img>` and `<video>` without explicit `width`/`height` or `aspect-ratio`, ads and embeds without reserved space, banners and cookie notices injected above content, fonts swapping to a differently-metricked fallback, content shifted by late-loading components.

---

## 7. Mobile

Indexing is mobile-first, so the mobile rendering is the rendering that counts.

- `<meta name="viewport" content="width=device-width, initial-scale=1">` present.
- Parity: does the mobile version serve the same main content, headings, structured data, and internal links as desktop? Hiding content on mobile hides it from indexing.
- Tap targets sized and spaced for thumbs; text legible without zoom.
- No horizontal overflow.
- Intrusive interstitials on entry — full-screen popups that block content on arrival are an explicit demotion signal.

---

## 8. Security and protocol

- Valid HTTPS across all resources; no mixed content.
- HSTS where appropriate.
- HTTP/2 or HTTP/3.
- Sensible caching headers on static assets.
- CDN or WAF rules not blocking legitimate crawlers — check this specifically, because a Cloudflare bot-fight setting can silently override a permissive robots.txt. If organic traffic dropped off a cliff around a CDN change, this is the first suspect.

---

## 9. Internationalization

Relevant whenever the site serves more than one language or country — including a Turkish site with an English section.

- `hreflang` annotations reciprocal (if TR points at EN, EN must point back at TR). Non-reciprocal hreflang is ignored.
- `x-default` present for the fallback.
- Correct codes: `tr`, `tr-TR`, `en-GB`, `de-AT`. Language code alone is usually right unless targeting the same language in different markets. Note `en-UK` is invalid — the code is `en-GB`.
- Absolute URLs, self-referencing hreflang included, and each target returning 200.
- Consistent URL strategy: subdirectory (`/tr/`), subdomain, or ccTLD — pick one; mixing them confuses signal consolidation.
- Auto-redirecting by IP without an override traps both users and crawlers, which will mostly see the US version.

---

## 10. Site architecture

- Click depth: important pages within three clicks of the homepage. Anything deeper gets crawled less and ranks worse.
- URL structure: readable, lowercase, hyphenated, stable, shallow. Avoid dates in evergreen URLs. For Turkish sites, decide deliberately between transliterated ASCII slugs and UTF-8 slugs and stay consistent — mixing produces duplicate-looking URLs.
- Orphan pages: in the sitemap but not linked from anywhere. Find them by comparing sitemap URLs against internal links seen while crawling.
- Navigation is real `<a href>` markup, not JS click handlers. A `<div onclick>` is not a link.
- Breadcrumbs present and marked up (see `04-schema-2026.md`).
- Pagination uses real crawlable links with distinct URLs.

---

## 11. Diagnosing a traffic drop

When the brief is "our traffic fell," work down this list in order rather than auditing everything:

1. **When exactly?** Get the date from Analytics or Search Console. A cliff on one day means a technical or manual event; a slope over weeks means an algorithm update or competitive erosion.
2. **Clicks vs. impressions.** Impressions steady, clicks down → SERP feature change, AI Overviews absorbing the click, or title rewriting. Both down → ranking or indexation loss.
3. **Sitewide or a section?** Compare page groups. Section-specific drops point at a template change, a redirect, or a content quality issue in that cluster.
4. **Did the site change?** Deploys, redesigns, migrations, CMS updates, plugin changes, CDN or DNS changes, robots.txt edits. Correlate the date against the changelog.
5. **Manual action / security issue** in Search Console. Rare but decisive.
6. **Algorithm update?** Cross-check the date against the Google Search Status Dashboard and industry trackers. Confirmed 2026 core updates so far include March and May. Google's own advice is to wait until a rollout completes before drawing conclusions and to avoid reactive changes mid-rollout — repeat that advice.
7. **Competitive/SERP change.** Did the SERP itself change shape — new AI Overview, more ads, a new competitor?

Note that a decline in clicks with flat impressions has become the normal pattern in categories where AI Overviews now answer the question. That is not a site defect, and the correct response is a strategy shift (see `03-ai-search-geo.md`), not a technical fix. Say that plainly rather than manufacturing technical findings to explain it.
