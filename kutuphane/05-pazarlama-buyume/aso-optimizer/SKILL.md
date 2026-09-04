---
name: aso-optimizer
description: >-
  Use this skill when auditing, writing, or optimizing mobile application store listings for Apple App Store (App Store Connect) and Google Play Store.
  Enforces 2026 ASO standards: exact character limits, semantic keyword placement, screenshot OCR text indexing, Custom Product Pages (CPPs), App Events, conversion rate optimization (CRO), and post-install retention signals.
---

# ASO Optimizer Skill (`aso-optimizer`)

This skill provides step-by-step guidance for conducting ASO audits, writing optimized store metadata (iOS & Android), designing high-converting visual assets, and setting up Custom Product Pages and App Events.

---

## ASO Optimization & Listing Workflow

### Step 1: Platform-Specific Metadata Optimization

#### iOS App Store (App Store Connect)
1. **App Name (Max 30 chars)**: Core title + primary keyword. High weighting.
2. **Subtitle (Max 30 chars)**: Secondary intent keywords. High weighting.
3. **Keyword Field (Max 100 bytes)**:
   - Hidden field. Comma-separated, NO spaces (`keyword1,keyword2,keyword3`).
   - Do NOT duplicate words already used in App Name, Subtitle, or primary category.
   - Omit plurals if singular is present; avoid generic terms ("free", "app").
4. **Promotional Text (Max 170 chars)**: Non-indexed, but updateable without app build submission.
5. **Long Description (Max 4,000 chars)**: Not indexed for iOS keyword search, but essential for CRO and conversion.

#### Google Play Store (Google Play Console)
1. **App Title (Max 30 chars)**: Core brand + primary keyword. Highest search weighting.
2. **Short Description (Max 80 chars)**: High-level pitch and keyword density. Substantial search weighting.
3. **Long Description (Max 4,000 chars)**: **Fully indexed by Google's semantic algorithm**.
   - Aim for 2% - 3% natural keyword density for primary clusters.
   - Include bulleted feature highlights and clear value propositions.
   - Avoid keyword stuffing (triggers spam suppression penalties).

---

### Step 2: Visual Asset & OCR Optimization
1. **Icon**: Simple, high-contrast, visually distinct focal point. Avoid cluttered text.
2. **Screenshots & Apple OCR**:
   - **2026 Update**: Apple's optical character recognition (OCR) indexes text inside screenshots. Use searchable, high-intent caption text.
   - **First 3 Screenshots**: Crucial for conversion (viewed in search results without scrolling).
   - Use bold caption headers, high-contrast device mockups, and localized messaging.
3. **App Trailer / Promo Video**: First 3-5 seconds must hook the user; auto-plays on mute.

---

### Step 3: Segmentation via Custom Product Pages (CPPs)
1. **Custom Product Pages (iOS CPPs / Google Custom Store Listings)**:
   - Create tailored store listings mapped to distinct ad campaign themes or target audience personas.
   - **2026 Organic Discovery**: Align CPP visual messaging with organic search intent clusters.
2. **A/B Testing**: Run Store Listing Experiments on Google Play and Product Page Optimization (PPO) on iOS.

---

### Step 4: Engagement & Event Strategy
1. **In-App Events (iOS) & Promotional Content (Android)**:
   - Schedule time-sensitive events (e.g., seasonal sales, content drops, live challenges).
   - Events appear in search results, editorial tabs, and recommendation feeds, re-engaging lapsed users.
2. **In-App Purchases (IAP) Display**:
   - Give IAP items descriptive titles and icons to rank directly in search results.

---

## ASO Audit Checklist

- [ ] iOS App Name is <= 30 characters and contains main keyword.
- [ ] iOS Subtitle is <= 30 characters with zero word overlap from App Name.
- [ ] iOS Keyword Field is <= 100 bytes, comma-separated with NO spaces.
- [ ] Google Play Title is <= 30 characters.
- [ ] Google Play Short Description is <= 80 characters.
- [ ] Google Play Long Description contains natural keyword density (2-3%) without spam.
- [ ] Screenshot text uses high-contrast typography readable by Apple OCR.
- [ ] In-App Events / Promotional Content configured for peak engagement periods.
