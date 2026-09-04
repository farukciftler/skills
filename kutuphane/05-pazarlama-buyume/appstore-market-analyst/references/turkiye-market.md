# The Türkiye market

Turkish app-market data is thin and often stale. Much of what circulates in Turkish-language sources is recycled from a 2018 App Annie report. Flag the age of anything you cite here, and prefer live lookups for rankings and prices.

## Contents
- [Size and position](#size-and-position)
- [User behaviour](#user-behaviour)
- [What ranks in Türkiye](#what-ranks-in-türkiye)
- [The currency and pricing problem](#the-currency-and-pricing-problem)
- [Tax and regulation](#tax-and-regulation)
- [The Turkish games ecosystem](#the-turkish-games-ecosystem)
- [Strategy for a Türkiye-based developer](#strategy-for-a-türkiye-based-developer)
- [Building for Turkish users specifically](#building-for-turkish-users-specifically)

---

## Size and position

| Figure | Value | Source / date |
|---|---|---|
| Global rank, downloads | 8th | Adjust, end of 2024 |
| Annual downloads | 3.66B (2024); "over three billion" | Adjust / Business of Apps, 2024 |
| Total time in apps | 101.5B hours | Adjust, 2024 |
| Apps downloaded per user per year | 52 | Business of Apps, 2024 |
| Mobile app revenue projection | $1.65B by 2029 | Adjust |
| Mobile game revenue | $427.5M in 2025 — roughly half of Türkiye's total video game revenue | Adjust |
| Mobile game installs | +12% YoY 2024; +4% YoY H1 2025 | Adjust |
| Mobile game sessions | +8% 2024; +12% YoY H1 2025 | Adjust |
| Daily internet time | 7+ hours | 2024 |
| Mobile share of internet consumption | 60%+ | 2024 |

**Read this correctly: Türkiye is a top-10 market by volume and a small market by revenue.** 3.66B downloads against a projected $1.65B app revenue *by 2029* is the whole story. Engagement is high, spend per user is low.

Turkish gamers are noted by Adjust as materially less sticky than the global average — retention is a specific local weakness, not just a monetization one.

## User behaviour

- Android dominates unit share; iOS is a minority platform but skews higher-income and higher-spending. For a paid or subscription product, iOS is where the Turkish revenue is even though Android has the users.
- Heavy social and short-video consumption. Instagram has been the most-downloaded app; TikTok the top-grossing app; Temu a major recent entrant on downloads.
- Strong local commerce app usage — Trendyol, sahibinden, Getir-style categories, obilet/Etstur in travel, Martı in mobility.
- Price sensitivity is high and subscription fatigue is real. A ₺-denominated monthly subscription competes against a household budget in a high-inflation environment, not against a discretionary coffee.

## What ranks in Türkiye

Rankings move; treat any specific list as needing a live check. The stable shape:

- **Top grossing overall:** TikTok has held the top position; PUBG Mobile the top grossing game. Roblox and Candy Crush Saga also high-grossing.
- **Most downloaded:** Instagram, Temu, TikTok, WhatsApp, ChatGPT in the top tier.
- **Categories with real local players:** shopping (Trendyol, sahibinden), travel (obilet, Etstur), mobility (Martı), news (Mynet, Bundle), banking (all major banks with strong apps).

Live rankings: Similarweb `similarweb.com/top-apps/apple/turkey/`, Sensor Tower top charts with `country=TR`, AppBrain `appbrain.com/stats/appstore-rankings/`, 42matters Türkiye pages.

## The currency and pricing problem

This is the operationally important part for a developer.

**Türkiye sits at the bottom of Apple's global price tiers.** Apps, in-app purchases and Apple's own services are priced far below US equivalents — Apple Music around a tenth of US pricing, Apple Arcade similarly. The Turkish storefront is well known internationally as one of the cheapest, which is itself a signal of how low the tier assignment is.

**Consequences a developer must plan for:**

1. **A Turkish-storefront sale earns a fraction of a US sale.** Same tier position, different absolute revenue. Volume does not compensate.
2. **Apple's automatic FX-based price adjustments hit Türkiye repeatedly.** November 2025 saw a pricing update in Türkiye (alongside Poland and Switzerland) due to exchange rate changes. Expect these multiple times per year.
3. **Apple does NOT auto-adjust subscription prices.** This is the single most costly detail. FX moves, one-time purchase prices adjust, and your subscription silently keeps earning the old lira amount. **Check Turkish subscription pricing manually every quarter at minimum.** In a high-inflation market monthly spot-checks are the recommended discipline.
4. **Automatic conversion overshoots.** Apple's auto-conversion from a USD base tends to land Türkiye (like India, Brazil, Indonesia) at 2×–3× local affordability. If you set a US price and let Apple convert, your Turkish price is probably wrong in the direction of too expensive.
5. **The PPP correction:** target price ≈ (PPP_Türkiye / PPP_US) × base price, then round to a locally natural figure (₺449, ₺99, ₺199 read as prices; ₺437.63 does not).

Apple supports roughly 900 price points across 175 storefronts and 43–45 currencies. Türkiye is one storefront to set deliberately, not to leave on auto.

## Tax and regulation

| Item | Status |
|---|---|
| Digital services tax on App Store sales | **Reduced from 7.5% to 5% in January 2026** — a slight price decrease |
| Apple commission | 30% standard, 15% under the Small Business Program (under $1M annual proceeds) |
| Alternative payment steering | Rekabet Kurumu's 2023 decision permits directing users to alternative payment methods; in practice constrained by Apple's own policies and not a reliable plan for an indie app |
| Platform local-presence rules | Platforms with 10M+ daily active users in Türkiye must establish a local entity, not just a representative office |
| Content regulation | Amended internet regulations (2022 onward) increase platform liability for published content |

**For a Turkish developer's own tax position:** income from App Store sales is foreign-sourced revenue. There are Turkish exemption regimes relevant to some digital income (e.g. the GVK 20/B content-creator exemption) but their applicability to app revenue specifically is a question for an accountant, not for this skill. Flag it, don't advise on it.

**Development cost benchmarks in Türkiye** (from local agency sources, 2026): ₺60,000–₺1,500,000 typical range depending on complexity, with one source citing ₺50,000–₺3,000,000. Ongoing maintenance commonly estimated at ~20% of initial build cost annually. Treat these as agency pricing, not as what a solo developer's time is worth.

## The Turkish games ecosystem

The one part of the Turkish market that is globally significant.

- Games from Turkish studios reach 30M+ local players and hundreds of millions worldwide.
- **Dream Games (Royal Match)** is the flagship. Peak Games, Rollic, Gram Games and others built the precedent.
- The model is uniform and instructive: **build in Türkiye, monetize globally.** No successful Turkish game studio's revenue comes primarily from Turkish users.
- Local mobile game revenue of ~$427.5M (2025) is roughly half of Türkiye's total video game revenue — meaningful domestically, small globally.

This ecosystem produced deep local talent in UA, live-ops and monetization, which is a genuine advantage for a Türkiye-based developer building anything monetization-heavy.

## Strategy for a Türkiye-based developer

The pattern that works, and it is the same pattern the games industry already proved:

**1. Build in Türkiye, sell to NA/WE.** Median year-1 value per payer is $32 in North America against $14 in emerging markets. Ship English-first with quality English copy, price against the US tier, and treat Türkiye as one storefront among 175.

**2. Do not treat Türkiye as the primary market unless the product is inherently local.** Turkish-specific utilities, local commerce, local regulation-driven tools — those have a reason to be Türkiye-first. A general productivity or AI app does not.

**3. Localize into Turkish anyway.** It is cheap, it improves Turkish-storefront ASO, and Turkish users are engaged even when they spend little. Just don't build the business model on their spend.

**4. Price Türkiye separately and deliberately.** Low tier for conversion, reviewed quarterly, subscriptions checked manually.

**5. Exploit the cost asymmetry honestly.** A Turkish developer's cost base is low relative to NA/WE revenue. A product earning $2,000/month is marginal in San Francisco and meaningful in Istanbul. This is a real structural advantage in a market where most competitors need much larger outcomes to justify continuing.

**6. Use the Small Business Program.** 15% instead of 30% is a direct margin improvement, and as of iOS 27 it also gates free Private Cloud Compute access for Foundation Models apps under 2M lifetime first-time downloads.

## Building for Turkish users specifically

If the product genuinely targets Türkiye:

- **Payment friction is real.** Many users have limited card availability for App Store purchases; Apple Gift Card / balance top-up is a common path. Ultra-low entry price points convert better than they "should".
- **Annual over monthly.** A ₺ monthly subscription is a recurring decision in an inflationary environment; annual with a strong discount converts better and reduces churn exposure to FX moves.
- **Ad-supported is more viable than in NA/WE** relative to subscription — though Turkish eCPMs are well below global, so ad revenue per user is low in absolute terms. One local estimate puts pure-ad monthly revenue for a 1M-download app at $2,000–$5,000, against $20,000+ for the same app on a subscription model. Neither number is a benchmark; both illustrate the ratio.
- **Turkish language handling matters.** Agglutination breaks naive search and text processing; the dotted/dotless i (İ/ı) is a classic locale bug in case conversion; Turkish collation differs. Test with real Turkish input.
- **Ramadan, bayram and school calendar** drive real seasonality in engagement and spend across many categories.
