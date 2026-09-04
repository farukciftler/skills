# AI-driven app discovery (2026)

The honest framing to give clients: **app discovery is shifting from "keyword → ranked list" to
"intent → recommended action", on three fronts at once** — inside the stores (Apple's semantic search
and Tags, Google's Guided Search and Ask Play), inside general assistants (ChatGPT, Gemini,
Perplexity, Siri), and on the web that feeds them. Most published "AI ASO" advice is hypothesis
dressed as method. This file separates what has been measured from what has not.

---

## 1. What LLM assistants actually cite — the one methodologically transparent study

**AI App Discoverability Index, research run 19–20 March 2026.** 195 queries across 15 app categories
against ChatGPT, Claude, Gemini and Perplexity; 778 of 780 responses parsed; **4,265 app mentions,
1,230 unique apps.** **[measured]**

**Source mix of citations** (from Perplexity, the only platform exposing them; 1,285 URLs):

| Source type | Share |
|---|---|
| **Editorial content — listicles, reviews, roundups** | **62.4%** |
| **YouTube** | **14.2%** |
| **App store listings** | **9.5%** |
| Other | 13.9% |

Top cited domains were general-purpose review and comparison sites, not app stores.

**Other findings worth acting on:**
- **Visibility is fragmented per assistant.** Only **16.2% of apps appeared on all four platforms**;
  **54.8% appeared on only one.** Optimizing "for AI" generically is a category error — measure and
  work per assistant.
- **Query framing changes the answer set completely.** Adding a price qualifier moved free-app
  recommendations from **31.9% → 70.5% (+38.7 pp)**. Medium and narrow queries surfaced **64–66%
  niche apps** versus 34.3% for broad queries — long-tail qualified coverage is winnable in a way
  head terms are not.
- **Staleness is a live, exploitable problem.** Mint — shut down in March 2024 — was still recommended
  **21 times** across three platforms, often ranked first. Correcting stale web information about your
  own app, and being visibly current, is unusually high-leverage.
- **Power law.** The top 100 apps (8.1% of unique apps) took **38.1% of all mentions.**
- ⚠️ Presence of an `llms.txt` file correlated with **+22.9% mentions** — flagged by the author as
  exploratory, plausibly confounded ("sites that ship llms.txt are also better maintained"). Cheap
  enough to do; don't build a strategy on it.

**The single most actionable conclusion: ~62% of LLM app citations are editorial web content and only
~9.5% are store listings. Optimizing your App Store page has near-zero effect on whether ChatGPT
recommends you.** The lever is getting into "best X app" roundups on high-authority category sites and
onto YouTube. **That work is closer to digital PR and SEO than to ASO** — say so plainly rather than
selling AI visibility as an ASO deliverable.

Vendor tooling exists (AppTweak launched **AI Visibility for Apps** in April 2026, tracking how often
an app is recommended in AI answers and the user needs driving those recommendations), and 41% of app
marketers named monitoring AI recommendations their top priority. A homegrown version — run your target
queries weekly across models and log the mentions — is a legitimate substitute.

---

## 2. The stores are becoming LLM surfaces themselves

**Google Play [Google]:**
- **Ask Play** (I/O 2026) — a Gemini-powered chat on the listing that answers user questions, drawing
  from **your app description and key features**. ⚠️ Vendor claims it also reads your *website*, and
  that organic results get pushed to screen 4+ for conversational queries, are not Google-confirmed.
- **Guided Search** (rolling out since Sept 2025) — narrows broad queries into sub-queries and
  generates **highlight cards from listing metadata and reviews**.
- **Gemini app integration** — apps recommended and installed **without opening Play**.
- **Play Shorts** — a portrait short-form video feed for app promotion.
- Rollout is **English-language devices first; EEA significantly behind with no confirmed timeline.**

**Three ASO consequences that follow directly:**
1. **Your Play long description is now LLM input, not just human input and not just an index entry.**
   Write it as structured, factual capability documentation — front-load positioning, be explicit
   about what the app does *and does not* do, and cover pricing, platforms and use cases plainly. That
   also happens to be good for the keyword index, so there is no trade-off.
2. **Consistency between your listing and your website matters more**, since Ask Play (and general
   assistants) draw on both. Aligning feature naming across the two is low-cost and low-risk.
3. **Reviews feed the summary and highlight cards.** Review sentiment became a *representation* input,
   not only a ranking and conversion input.

**App Store [Apple]:**
- **App Store Tags** — LLM-generated from your metadata, human-reviewed, deselectable in App Store
  Connect (see `app-store-ios.md` §8). This is the mechanism by which your non-indexed description
  finally affects discovery.
- **Semantic / natural-language search** since iOS 18.1, with a further multi-intent shift in June 2025
  — favours conversational long-tail phrasing and semantic clusters over isolated head terms.
- **App Intents are becoming a discovery surface.** Apple's guidance is to expose functionality through
  App Intents as discovery shifts *"away from traditional app browsing toward intent-based
  interactions, where users focus on outcomes rather than navigation."* ⚠️ The conversational-Siri
  rollout timeline (2026–2027) has slipped repeatedly.

---

## 3. Web / "app SEO" now does double duty

- **Google indexes both Play and App Store product pages**, so a store page can rank in web search
  without a website at all.
- ⚠️ Figures for search-engine-driven app discovery ("one in four users", "~40% of global users") come
  from different studies measuring different things and are not reconcilable — use them to argue that
  the channel is significant, not to size it.
- **The compounding argument, and the real 2026 change:** since ~62% of LLM app citations are editorial
  web content, a "best budgeting app 2026" listicle placement is simultaneously an SEO asset, an
  AI-visibility asset and a referral-traffic asset. **This is the biggest expansion of ASO's scope in
  years, and it sits outside the app stores.**
- **Tactics that hold up:** use-case landing pages rather than one generic homepage; structured data;
  **Smart App Banners** on iOS Safari and web install prompts on Android; deep links so a search result
  opens the app if installed and the store page if not; **web-to-app banners with deferred deep
  linking** so the user lands on the right in-app screen after install.
- ⚠️ **Web-to-app economics improved after the 2024–2025 anti-steering rulings** (external purchase
  links), which changes the calculus on sending traffic to your own site rather than straight to the
  store — but the regulatory position is jurisdiction-specific and still moving. Verify current
  entitlement rules before building on it.

---

## 4. App Clips — an honest assessment

15 MB cap. Discovery surfaces: App Clip Codes, QR codes, NFC tags, Safari Smart Banners, Apple Maps
action buttons, Messages links. The value proposition inverts the funnel — value delivered before
install, so the install decision comes from someone who already succeeded at a task.

⚠️ **No published adoption or conversion data exists**, and there were no App Clips announcements at
WWDC 2026. Vendors calling them "underrated" is marketing language for low adoption.

**Verdict:** worth building **only with a physical-world or link-shared intent moment** — restaurant
ordering, scooter unlock, event check-in, parking, in-store try-on, a shared document. For a
general-purpose app with no physical touchpoint, App Clips are a distraction with no evidence base.
Do not rank this above creative testing or review management.

---

## 5. What is and is not evidenced — say this out loud

**Evidenced (from the March 2026 index):**
1. Editorial placement dominates LLM citations (62.4%).
2. YouTube is #2 (14.2%).
3. Store listings are only 9.5% — ASO alone does not buy AI visibility.
4. Optimize per-assistant; over half of apps appear on only one.
5. Price and specificity qualifiers reshape results entirely — build coverage for qualified long-tail
   queries, not just head terms.
6. Freshness is a defensible edge, because assistants demonstrably recommend dead apps.

**Not evidenced:** any causal ranking factor for LLM app recommendations; any measured install volume
attributable to AI assistants; any ROI figure for "AI visibility" work; any claim that a specific
metadata format improves LLM recommendation. **Every vendor "AI ASO checklist" currently circulating
is hypothesis, not finding.**

**So measure it yourself:** run a weekly prompt panel (your target queries across the major
assistants, logged), and track branded-search lift plus direct/unattributed install volume as
proxies. That converts an unfalsifiable pitch into an actual experiment — which is the whole value of
having a consultant.
