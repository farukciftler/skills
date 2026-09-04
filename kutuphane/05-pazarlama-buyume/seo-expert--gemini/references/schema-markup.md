# JSON-LD Schema Markup Reference

## 1. Organization Schema (Site Wide)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Brand Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/brand",
    "https://linkedin.com/company/brand",
    "https://github.com/brand"
  ]
}
```

## 2. Article / Blog Post Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Target Article Title",
  "description": "Short article summary for search engines and AI models.",
  "image": "https://example.com/og-image.jpg",
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-07-31T12:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "jobTitle": "SEO Specialist",
    "url": "https://example.com/authors/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Brand Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

## 3. Product Schema (E-Commerce)
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": ["https://example.com/product.jpg"],
  "description": "Detailed product description.",
  "sku": "PROD-123",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "49.99",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product-url"
  }
}
```

## 4. FAQ Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Technical SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Technical SEO involves optimizing web infrastructure so search engines and AI crawlers can efficiently crawl, render, and index pages."
      }
    }
  ]
}
```

## 5. BreadcrumbList Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://example.com/blog"
    }
  ]
}
```
