---
name: seo-expert
description: >-
  Use this skill when auditing, designing, or implementing SEO (Search Engine Optimization)
  for web applications, static websites, dynamic SPAs, or e-commerce sites.
  Enforces Technical SEO, Core Web Vitals, JSON-LD Schema Markup, OpenGraph metadata,
  semantic HTML hierarchy, crawlability, and AI/LLM search engine visibility.
---

# SEO Expert Skill (`seo-expert`)

This skill provides step-by-step guidance for conducting SEO audits, optimizing web pages, setting up structured data, and adhering to modern search engine and AI indexing standards.

---

## SEO Audit & Optimization Workflow

When asked to audit or optimize a codebase for SEO, execute the following steps:

### Step 1: Technical & Performance Foundation
1. **Core Web Vitals Assessment**:
   - **LCP (Largest Contentful Paint)**: < 2.0s. Check hero image preload, WebP/AVIF formats, and server response times.
   - **INP (Interaction to Next Paint)**: < 200ms. Check main-thread JS execution, long tasks, and event handler optimization.
   - **CLS (Cumulative Layout Shift)**: < 0.1. Ensure all images/embeds have explicit `width` and `height` dimensions.
2. **Crawlability & Indexability**:
   - Check `robots.txt` for crawl directives and AI bot permissions.
   - Verify self-referencing `<link rel="canonical" href="..." />` on every page.
   - Validate XML Sitemap format, `lastmod` timestamps, and inclusion of indexable pages only.
3. Refer to detailed guidelines in [references/technical-seo.md](references/technical-seo.md).

### Step 2: On-Page Meta & OpenGraph Tags
1. **Title Tag**: Must be unique per page, descriptive, < 60 characters, and front-load target intent.
2. **Meta Description**: Compelling preview copy between 120-155 characters that maximizes CTR.
3. **OpenGraph & Social Preview**:
   - `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`.
   - `og:image`: Standard **1200 x 630 px** (1.91:1 aspect ratio, < 1MB), with vital content within safe center 1080x600 px.
   - `twitter:card`: Set to `summary_large_image`.
4. Refer to detailed guidelines in [references/content-onpage.md](references/content-onpage.md).

### Step 3: Semantic HTML & E-E-A-T Content Structure
1. **Heading Hierarchy**: Exactly one `<h1>` per page, followed by logical `<h2>`, `<h3>` subheadings without skipping levels.
2. **Semantic Elements**: Use `<main>`, `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`, `<aside>`.
3. **Alt Text**: Descriptive, context-rich alt text on all non-decorative `<img>` tags.
4. **E-E-A-T Signals**: Visible author metadata, published/modified dates, credential links, and clear citations.

### Step 4: JSON-LD Structured Data (Schema Markup)
1. Inject valid `<script type="application/ld+json">` tags.
2. Always implement `Organization` schema on home/site root.
3. Implement context-specific schemas: `Article`, `Product`, `FAQPage`, `BreadcrumbList`, `WebSite` (with SearchAction).
4. Refer to reference templates in [references/schema-markup.md](references/schema-markup.md).

---

## Quick Verification Checklist

- [ ] Every page has a unique `<title>` (<60 chars) and meta description.
- [ ] Canonical URL tag `<link rel="canonical">` is present and self-referencing.
- [ ] OpenGraph image is 1200x630px and loads cleanly.
- [ ] JSON-LD schema parses cleanly with zero syntax or missing-property errors.
- [ ] Robots.txt allows search crawlers and does not block required CSS/JS.
- [ ] HTML headings use clean hierarchy (`h1` -> `h2` -> `h3`).
