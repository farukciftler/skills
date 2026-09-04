# What "royalty-free" actually covers

This matters more for a music release than for a blog post, because cover art ships to
DSPs, gets fingerprinted, and ends up on merch. Getting it wrong surfaces months later as
a takedown or a claim.

## What the Pexels License grants

Free for commercial and non-commercial use. No attribution is legally required. Assets may
be modified. No fee, no per-use accounting.

## What it does not grant

These are the parts people miss:

1. **No model release.** Pexels does not guarantee that recognisable people in a frame
   consented to commercial use of their likeness. Putting an identifiable face on an album
   cover implies the person endorses or performs on the release — that is a personality-
   rights exposure independent of the image copyright. Treat any recognisable face as
   unusable for cover art unless the concept genuinely needs it and you accept the risk.

2. **No property or trademark release.** Logos, brand marks, instrument headstocks,
   microphone badges, screen contents, visible artwork, murals, tattoos, and distinctive
   architecture each carry rights the photographer never held and therefore could not pass
   on. A visible Neumann badge or Fender logo on a commercial cover is a trademark
   question, not a stock-photo question.

3. **Selling unaltered copies is prohibited.** Printing a Pexels photo on a poster,
   t-shirt, tote or vinyl sleeve *as the product* violates the licence. Using it as one
   component of a substantially new composition — treated, composited, typeset, halftoned —
   is fine. The `merch-print` preset exists to flag this, not to bless it.

4. **Do not replicate Pexels' core functionality.** Building a wallpaper app or an
   image-browser on top of the API breaches the API terms and gets keys revoked.

5. **Video audio is separate.** The audio bed on a Pexels clip is frequently not licensed
   under the same terms. Mute every clip and replace the audio.

## API Guidelines obligations

Distinct from the licence — these apply because the assets came through the API:

- Show a **prominent link to Pexels** wherever API-sourced content appears. Text is fine:
  "Photos provided by Pexels" linking to `https://www.pexels.com`.
- Credit the creator where possible: "Photo by John Doe on Pexels", linking to the photo
  page.
- Respect the rate limit: 200 requests/hour, 20,000/month by default. Working around it
  terminates access. Cache responses ~24h and normalise queries before hitting the API.

For a music release this cashes out as: put the Pexels link and creator credits in the
YouTube description, the release notes, and the site footer. Not on the cover art itself.

## Where AI-generated content complicates this

Pexels hosts some AI-generated submissions. For a release that will be distributed through
a DSP, an AI-generated cover may collide with the distributor's own AI-content policy even
when the Pexels licence is satisfied. Where a candidate looks synthetic — impossible
optics, garbled text in frame, over-smooth surfaces — flag it rather than assume it is
equivalent to a photograph.

## Practical clearance checklist before a cover ships

- No recognisable face, or a documented reason it is acceptable.
- No readable logo, brand mark, or third-party artwork in the cropped frame.
- The frame has been meaningfully transformed, not merely resized.
- Attribution recorded in `CREDITS.md` and copied into the release description.
- For video: audio stripped and replaced.
- The chosen frame reverse-image-searched, when the release is commercially significant,
  to check how heavily circulated it already is.

## Safer alternatives when a candidate fails clearance

- Re-run the search with `--exclude-people`.
- Move from "scene" to "texture": a macro of brass, tape, paper, concrete or fabric solves
  most cover briefs with zero clearance exposure.
- Use the frame as a treated background layer under original typography rather than as the
  image itself — which also satisfies the "substantially new composition" requirement.
