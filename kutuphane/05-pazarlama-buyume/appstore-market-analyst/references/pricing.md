# Pricing: model, price point, and the premium tail

## Contents
- [Choosing a monetization model](#choosing-a-monetization-model)
- [Apple's price tier mechanics](#apples-price-tier-mechanics)
- [Setting the base price](#setting-the-base-price)
- [Localizing price](#localizing-price)
- [Subscription design](#subscription-design)
- [Paid-upfront: when it still works](#paid-upfront-when-it-still-works)
- [The premium tail: $100–$999 apps](#the-premium-tail-100999-apps)
- [Net revenue math](#net-revenue-math)
- [Price maintenance discipline](#price-maintenance-discipline)

---

## Choosing a monetization model

| Model | Works when | Fails when |
|---|---|---|
| **Subscription, hard paywall** | Ongoing value, recurring use, the value is legible in the first 30 seconds | The value only becomes apparent after use — the wall blocks the demonstration |
| **Subscription, freemium** | Free tier is genuinely useful and creates a habit; upgrade is a natural ceiling | Free tier is good enough forever, or too crippled to build a habit |
| **Paid upfront** | Professional/vertical tool, a buyer who expenses it, a game port with a name, or a deliberate quality signal | Mass-market consumer anything |
| **One-time IAP / lifetime unlock** | Utility with a finite value proposition; also as an option alongside subscription | You need funding for ongoing server or model costs |
| **Consumable IAP** | Games, credit-based AI features | Non-game utilities — reads as nickel-and-diming |
| **Ads** | Very high session frequency, mass audience, low willingness to pay | Anything premium-positioned, or any audience under ~100k MAU |
| **Free, monetized elsewhere** | The app supports a business that earns off-platform | You expected the app itself to be the business |

**The conversion data:** hard paywalls convert at a **10.7% median D35 trial-to-paid** rate against **2.1% for freemium** — roughly 5×. But freemium gets far more people in the door. The decision is really about whether your value is *demonstrable before use* (wall it) or *only apparent through use* (freemium it).

**Hybrid is normal.** Subscription plus a lifetime option plus a small consumable tier is common and does not confuse people when the tiers map to genuinely different user intents.

## Apple's price tier mechanics

- Roughly **900 price points across 175 storefronts and 43–45 currencies.**
- Increments: **$0.10 below $10, $0.50 from $10–$50, $1.00 above $50.**
- Top standard tier is **$999.99**; higher prices require requesting special access from Apple.
- You can set prices **per storefront**, or pick a base storefront and let Apple auto-convert.
- **Apple auto-adjusts one-time prices** for tax and FX changes. **Apple does NOT auto-adjust subscription prices** — ever. This is the most consequential asymmetry in the system.
- Apple runs multiple pricing/tax adjustment rounds per year. January 2026 alone changed tax handling in nine countries (Kazakhstan VAT up, Türkiye digital sales tax down 7.5%→5%, Zimbabwe VAT up, Ghana levy removed, Mauritius new 15% VAT, Bulgaria switched BGN→EUR).

## Setting the base price

Work from the US price as the base, then localize.

**Anchor to what the alternative costs the buyer, not to your development cost.** A tool that replaces a $30/month SaaS subscription can charge meaningfully; a tool that replaces "doing it manually in Notes" cannot, regardless of how hard it was to build.

**Common ceilings by shape (US pricing, indicative):**

| Shape | Typical range |
|---|---|
| Consumer utility subscription | $2.99–$9.99/month, $19.99–$59.99/year |
| Prosumer / creative tool | $9.99–$29.99/month |
| B2B mobile tool, paid upfront | $49–$149 — converts better than free-with-subscription when the buyer is a decision-maker |
| Consumer paid upfront | $2.99–$9.99, and the market for this is small |
| Game, paid upfront | $2.99–$9.99 mobile-native; $19.99+ for console/PC ports |
| Professional vertical tool | $99–$999 — see the premium tail below |

**Launch positioning:** entering at 20–40% below an established incumbent is the standard play for a professional tool. For a new consumer subscription, an attractive entry price matters disproportionately when you run paid acquisition without trials — it determines how fast growth loops can scale.

**Do not launch cheap intending to raise later.** Existing subscribers are grandfathered or must be asked to consent, and raising a price is much harder than lowering one. Launch at the price you want and discount tactically.

## Localizing price

Auto-conversion from a US base **overshoots local affordability by 2×–3× in Türkiye, India, Brazil and Indonesia**, and lands 10–25% *below* US equivalent in the UK and Germany once VAT is accounted for.

The correction:

```
target_price ≈ (PPP_country / PPP_base) × base_price
```

Then round to a locally natural number — ₺449, ₹499, R$49.90. Prices that look like conversion artifacts read as foreign and convert worse.

**Which markets to set manually:** the US and your top three revenue markets always; plus any high-inflation market you sell in (Türkiye, Argentina). Leaving 170 storefronts on auto is fine. Leaving Türkiye on auto is not.

**Review cadence:** stable markets (US, UK, EU) annually. High-inflation markets monthly to quarterly.

## Subscription design

**Trial length.** Longer trials do not linearly improve conversion; the relationship is well documented and non-obvious. Test rather than assuming a 7-day default is right.

**Monthly vs annual.** Annual reduces churn exposure and improves LTV per payer but raises the commitment barrier. In high-inflation currencies annual also protects you from FX drift — which is a Türkiye-specific argument for pushing annual harder there than elsewhere.

**Year 2+ renewals drop to 15% commission.** This is a real reason to optimise for retention over acquisition once you have a base.

**Offer types worth using and usually neglected:** introductory offers, promotional offers for lapsed users, win-back offers, and offer codes for partnerships and press. These are free levers already built into StoreKit.

**Paywall placement is the highest-leverage experiment you can run**, ahead of price itself. Onboarding-embedded paywalls, post-value-moment paywalls, and settings-only paywalls produce dramatically different conversion for the same product and price. Reported figures of ~42.5% trial-to-paid with optimised onboarding versus a 2–5% general free-to-paid median show the size of the spread.

## Paid-upfront: when it still works

Paid apps are ~5.2% of the App Store and declining. In several categories they are under 2% of listings. But the model is not dead — it is concentrated.

It works when:
- **The buyer expenses it.** Licensed professionals — dentists, pilots, architects, piano technicians, musicians — treat a $200 app as a business tool.
- **Enterprise procurement is the channel.** $400 per seat is routine in that context and price is not the friction.
- **Price is a quality signal to an enthusiast community.** Golfers, traders, hobbyists with expensive hobbies.
- **It screens out consumer impulse buyers**, which is often the intent — high-priced tools have lower support load per unit of revenue.
- **The app is a port of a known game.**

Reported figure worth citing carefully: the top 1% of paid apps by revenue earn a median of roughly $18,000/month, while a comparable freemium app in the same category needs 10–20× more downloads to match. Source is App Store data published by Apple (2024) as reported by an agency — verify before leaning on it.

## The premium tail: $100–$999 apps

The pattern is consistent and instructive.

**Top of the mainstream range as of 2026: roughly $999.99** — `roc.Kasse` (a certified point-of-sale system for German retail, complying with KassenSichV fiscal law) and `CyberTuner` (professional piano tuning) are the standard examples.

**What they all share:**
- A **licensed or certified professional** as the buyer
- **Regulatory or certification cost** baked into the product (fiscal compliance, medical reference, aviation)
- **Replacement of physical equipment or a workflow that costs far more** — a $999 piano tuning app replaces a several-thousand-dollar device
- **A small, identifiable, reachable audience** — you can name the buyer's profession
- **Ongoing support and update obligations** the price funds

**Categories where they cluster:** point-of-sale and fiscal compliance, medical and dental reference, aviation, CAD and engineering, music/instrument technology, legal reference, forex and trading tools.

**Games essentially never reach these prices.** High upfront prices are a professional-tools phenomenon.

**Can you build one?** The honest test: can you name the profession, estimate how many of them exist, and identify how you would reach them without app store search? If not, this is not your model. The premium tail is a distribution problem disguised as a pricing decision.

## Net revenue math

Work it through explicitly rather than quoting gross:

```
List price
  − local tax/VAT (varies by storefront; Türkiye DST now 5%)
  = proceeds base
  − Apple commission (30%, or 15% under Small Business Program / year-2+ renewals)
  = your proceeds
  − payment/FX/withdrawal costs
  − RevenueCat or similar (if used)
  = net
```

**Enroll in the Small Business Program if you're under $1M annual proceeds.** 30%→15% is a doubling of margin, and since iOS 27 it also gates free Private Cloud Compute access for Foundation Models apps under 2M lifetime first-time downloads.

**China note:** 25% standard / 12% Small Business since March 2026.

## Price maintenance discipline

A short checklist to run quarterly:

1. Check Apple's developer news for pricing and tax announcements since last review.
2. **Verify subscription prices in high-inflation storefronts** — they never auto-adjust.
3. Compare your Türkiye price against a PPP-derived target and against local competitor pricing.
4. Check that Google Play prices in the same countries are still aligned — a tax change on one store does not fix the other.
5. Confirm your top three revenue markets are set manually, not on auto-conversion.

For more than two apps this becomes a spreadsheet problem; tools exist (Mirava, PricePush, RevenueCat's pricing features) that automate the sweep.
