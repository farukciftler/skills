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

---

# Emlak ve inşaat için ek risk katmanı (Moonstone)

Yukarıdakiler telif ve kişilik hakkı riskidir. Bir konut projesinde bunların
üstüne **reklam mevzuatı riski** biner ve pratikte daha sık başa dert olan
budur.

## Yanıltıcı temsil — asıl risk

Türkiye'de konut reklamı 6502 sayılı Tüketicinin Korunması Hakkında Kanun ve
Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği'ne tabidir. Stok görsel
burada iki şekilde sorun yaratır:

1. **Ürünü yanlış temsil etmek.** Başka bir binanın cephesi, başka bir dairenin
   salonu, başka bir tesisin havuzu Moonstone'un yerine geçemez. Alıcı satın
   alma kararını gördüğü görsele dayandırıyorsa, o görselin projeye ait olması
   gerekir.
2. **Çevreyi yanlış temsil etmek.** Tuzla Aydıntepe'ye ait olmayan bir sahil,
   manzara ya da sokak, proje çevresi gibi sunulamaz.

Bu ikisi tazminat ve idari para cezasının yanı sıra sözleşme uyuşmazlığına da
konu olur — ve marka güveni açısından telafisi en pahalı hatadır.

## Karar testi

Her aday görselde tek soru:

> **Bu görseli gören biri, Moonstone Residence'ı gördüğünü sanabilir mi?**

- **Evet / belki** → kullanma.
- **Hayır, açıkça genel bir görsel** → kullanılabilir, ama bağlam da doğru olsun.

Bağlamın kendisi de temsil üretir: doğru bir doku fotoğrafı, "Tip 5 salonu"
başlığının altına konursa yanıltıcı hale gelir. Görsel + başlık + yerleştirme
birlikte değerlendirilir.

## Güvenli / riskli kullanım tablosu

| Kullanım | Durum |
|---|---|
| Doku ve malzeme plakası (beton, mermer, ahşap, cam, kâğıt) | **Güvenli** — tanınabilir yer, kişi, marka yok |
| Site bölüm arka planı, üzerine koyu katman + tipografi | **Güvenli** |
| Blog kapağı (kredi, net/brüt, yatırım rehberi) | **Güvenli** |
| Soyut gece göğü / hilal / ay taşı görselleri | **Güvenli** — marka anlatısıyla uyumlu |
| Sunum ve teklif belgelerinde bölüm ayracı | **Güvenli** |
| Genel iç mekân atmosferi, "örnek görüntü" ibaresiyle rehber içerikte | **Dikkatli** — daire tipiyle ilişkilendirilmemeli |
| Şantiye fotoğrafı, rehber içerikte konu anlatımı olarak | **Dikkatli** — Moonstone şantiyesi sanılmamalı |
| Tanınabilir bina cephesi | **Riskli** — hem marka/mimari hakkı hem yanıltıcı temsil |
| İç mekân fotoğrafı, daire tipi anlatımının içinde | **Yasak** |
| Havuz / spor salonu / spa fotoğrafı, sosyal alan anlatımında | **Yasak** |
| Başka bir şehrin manzarası, lokasyon anlatımında | **Yasak** |
| Stok görsel + üzerine proje adı, ürün iletişiminde | **Yasak** |

## Ek işaretleme kuralı

- Proje render'ları zaten **"Temsili görseldir"** notu taşır. Stok görsel
  kullanılan yerde bu not **yetmez** — çünkü görsel projeyi temsil etmiyor,
  hiç ilgisi yok. Orada gereken şey görselin ürün gibi okunmamasıdır.
- Blog ve rehber içeriğinde stok görsel kullanıldığında künye Pexels
  bağlantısıyla birlikte yazının sonunda ya da site altbilgisinde bulunmalı.

## Yayın öncesi ek kontrol

- [ ] Karar testi geçildi mi? ("Moonstone sanılabilir mi?")
- [ ] Görselin yanındaki başlık ve metin, görseli ürünle ilişkilendiriyor mu?
- [ ] Tanınabilir bina, plaka, logo, yüz var mı?
- [ ] Konum iddiası içeren bir yere konuluyor mu?
- [ ] Künye `CREDITS.md`'ye yazıldı ve yayınlanacak yere taşınacak mı?
