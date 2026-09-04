# Technical SEO & Crawl Governance Reference

## Core Web Vitals (2026 Standards)
- **LCP (< 2.0s)**: Preload critical hero assets (`<link rel="preload" as="image" href="...">`), deliver images in modern formats (AVIF/WebP), optimize server time & CDN routing.
- **INP (< 200ms)**: Reduce main-thread blocking JavaScript, split long tasks (>50ms) using `requestIdleCallback` or Web Workers, streamline DOM event handlers.
- **CLS (< 0.1)**: Assign explicit `width` and `height` attributes to all images/videos/embeds, utilize CSS `aspect-ratio`, avoid injecting layout-shifting dynamic DOM nodes above the fold.

## Robots.txt Governance
```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /checkout/

# XML Sitemap Location
Sitemap: https://example.com/sitemap.xml
```

## XML Sitemap Standard
- Only include indexable, 200 OK canonical URLs.
- Remove 301/302 redirects, 404/410 errors, and `noindex` pages.
- Provide accurate `<lastmod>` ISO 8601 timestamps to signal content freshness.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-07-31T12:00:00+00:00</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

## Canonicalization & Status Codes
- Every indexable page MUST have a self-referencing canonical link: `<link rel="canonical" href="https://example.com/canonical-path" />`.
- Maintain clean status code responses: 200 OK for live content, 301 for permanent redirects, 404/410 for deleted assets.
