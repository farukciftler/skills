# CAD & Görsel Üretim

Parametrik mobilya/CAD zinciri, markalı görsel hattı, sunum tasarımı, stok görsel keşfi.

9 skill. Üst dizin: [../../README.md](../../README.md)

## `deck-studio`

[SKILL.md](deck-studio/SKILL.md)

Sunum tasarım stüdyosu — bir marka kimliği veya seçilmiş bir sanat yönetimi (art direction) üzerine kurulu, özel tipografili, kendi ürettiği illüstrasyon ve ürün mockup'larını içeren, jenerik AI şablonundan uzak .pptx desteleri üretir; mevcut desteleri de yeniden tasarlar ve denetler. Kullanıcı 'sunum hazırla', 'deck', 'pitch deck', 'yatırımcı sunumu', 'slayt', 'pptx', 'sunumu güzelleştir', 'şu desteyi yeniden tasarla', 'mockup ekle', 'illüstrasyon üret', 'marka kimliğine göre sunum', 'make me a deck', 'design these slides', 'redesign this presentation' dediğinde kullan. Bir teklif, rapor, strateji, lansman veya yatırımcı görüşmesi için slayt gerektiği anlaşıldığında — 'tasarım' kelimesi hiç geçmese bile — devreye gir. Sunuma girecek cihaz mockup'ı, arayüz ekranı, vektör illüstrasyon veya özel font gerektiğinde tek başına da kullan. Şablon doldurmaz; her deste için tek bir sanat yönetimi kararı verir, kilitler, her slaytta uygular.

- **Ölçü:** 10.093 bayt · 9 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `gorsel-uretim`

[SKILL.md](gorsel-uretim/SKILL.md)

Moonstone Residence için sosyal medya ve web görseli üretir — Instagram story/Reels karesi, feed ve carousel slaytı, OG görseli, sayı kartı, alıntı kartı, plan/veri kartı, web bölüm arka planı ve site için AVIF/WebP/JPEG varyantları. Markalı çerçeveyi, okunabilirlik katmanını, tipografiyi, altın ayracı, logoyu ve "Temsili görseldir" notunu doğru güvenli alan içinde yerleştirir; renk düzeltmesini Apple Silicon GPU'sunda Core Image ile yapar. Şu ifadeler geçtiğinde kullan: "görsel hazırla", "post tasarla", "story görseli", "kapak yap", "bu fotoğrafı markaya uyarla", "kırp", "boyutlandır", "renk düzelt", "logo bas", "carousel slaytı", "web için optimize et", "AVIF üret", "güvenli alanı kontrol et". Bir görsel dosyası üretilecek ya da var olan bir görsel Moonstone kimliğine uyarlanacaksa, araç adı hiç geçmese bile devreye gir. Görsel *bulmak* için `pexels-gorsel-bulucu`, hangi ölçü ve içeriğin gerektiği için `post-uretimi.md` / `story-uretimi.md`.

- **Ölçü:** 9.418 bayt · 6 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/moonstone/.claude/skills/gorsel-uretim

## `gorsel-uretim--moonstone-gh`

[SKILL.md](gorsel-uretim--moonstone-gh/SKILL.md)

Moonstone Residence için sosyal medya ve web görseli üretir — Instagram story/Reels karesi, feed ve carousel slaytı, OG görseli, sayı kartı, alıntı kartı, plan/veri kartı, web bölüm arka planı ve site için AVIF/WebP/JPEG varyantları. Markalı çerçeveyi, okunabilirlik katmanını, tipografiyi, altın ayracı, logoyu ve "Temsili görseldir" notunu doğru güvenli alan içinde yerleştirir; renk düzeltmesini Apple Silicon GPU'sunda Core Image ile yapar. Şu ifadeler geçtiğinde kullan: "görsel hazırla", "post tasarla", "story görseli", "kapak yap", "bu fotoğrafı markaya uyarla", "kırp", "boyutlandır", "renk düzelt", "logo bas", "carousel slaytı", "web için optimize et", "AVIF üret", "güvenli alanı kontrol et". Bir görsel dosyası üretilecek ya da var olan bir görsel Moonstone kimliğine uyarlanacaksa, araç adı hiç geçmese bile devreye gir. Görsel *bulmak* için `pexels-gorsel-bulucu`, hangi ölçü ve içeriğin gerektiği için `post-uretimi.md` / `story-uretimi.md`.

- **Ölçü:** 11.636 bayt · 13 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/moonstone/.claude/skills/gorsel-uretim

## `mobilya-cad`

[SKILL.md](mobilya-cad/SKILL.md)

Levha mobilya (suntalam/MDF dolap, ayakkabılık, gardırop, raf, TV ünitesi) tasarımını parametrik Python modelinden üretim ve sunum paketine çeviren zincir: build123d 3B (STEP/GLB/STL), ezdxf ölçülü teknik çizim (görünüş + kesit + antet, DXF/PDF/PNG), kesim listesi ve BOM (net/kesim ölçüsü, bant payı düşülmüş), donanım listesi, kenar bandı metrajı, giyotin nesting ve fire, parça başına CNC DXF (R12), Blender 5.2 render ve 8 sayfalık tasarım dosyası PDF. Kullanıcı "ayakkabılık", "dolap", "gardırop", "raf", "mobilya çiz", "3D model", "render", "teknik çizim", "kesit", "ölçülendir", "kesim listesi", "BOM", "kaç levha çıkar", "fire", "nesting", "kenar bandı", "DXF", "CNC", "malzeme listesi", "raf sarkar mı", "kaç çift alır", "askı sığar mı", "doku", "görsel" dediğinde ya da bir mobilya ölçülendirilir, malzeme/donanım seçilir veya üretime dosya hazırlanırken kullan. 32'lik sistem, minifix/menteşe delikleri, EN 312 P2 sehim, EN 14749 devrilme, askı derinliği ve desen yönü kuralları hesaplara gömülüdür.

- **Ölçü:** 18.267 bayt · 17 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/mobilya/.claude/skills/mobilya-cad

## `mobilya-cad--mobilya-gh`

[SKILL.md](mobilya-cad--mobilya-gh/SKILL.md)

Levha mobilya (suntalam/MDF dolap, ayakkabılık, gardırop, raf ünitesi, TV ünitesi, mutfak modülü) tasarımını uçtan uca üretim paketine çeviren mühendislik zinciri — parametrik 3B katı model (build123d → STEP/GLB/STL), ölçülendirilmiş teknik çizim (ezdxf → görünüş + kesit + antet, DXF/PDF/PNG), kesim listesi ve BOM (net/kesim ölçüsü, bant payı düşülmüş), kenar bandı metrajı, giyotin kesim optimizasyonu ve fire raporu, parça başına CNC DXF (R12), ve Blender 5.2 ile foto-gerçekçi render, PBR doku/mesh texture, USDZ/GLB çıktısı. Kullanıcı "ayakkabılık", "dolap", "gardırop", "raf", "mobilya çiz", "3D model", "render", "teknik çizim", "kesit", "görünüş", "ölçülendir", "kesim listesi", "parça listesi", "BOM", "kaç levha çıkar", "fire", "yerleşim/nesting", "kenar bandı", "DXF", "CNC dosyası", "malzeme listesi", "raf sarkar mı", "kaç çift alır", "texture", "kaplama", "doku", "mesh", "görsel/sunum" dediğinde; bir mobilya ölçülendirilirken, malzeme/donanım seçilirken, üretime gönderilecek dosya hazırlanırken veya ürün görseli istendiğinde bu skill'i kullan. 32'lik sistem, minifix/kavela/menteşe delik tabloları, EN 312 P2 sehim limitleri, EN 14749 devrilme eşiği, kenar bandı payı ve desen yönü kuralları hesaplara gömülüdür.

- **Ölçü:** 13.453 bayt · 12 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/mobilya/.claude/skills/mobilya-cad

## `pexels-gorsel-bulucu`

[SKILL.md](pexels-gorsel-bulucu/SKILL.md)

Moonstone Residence için telifsiz Pexels fotoğrafı ve videosu bulur, puanlar, hak/izin riskini denetler ve künyesiyle birlikte indirir. Blog kapağı, site bölüm arka planı, OG görseli, sosyal medya zemini, doku/malzeme plakası, Reels ara kesiti ve Tuzla/İstanbul çevre içeriği için kullanılır. Türkçe ya da muğlak bir brief'i gerçekten sonuç veren İngilizce sorgulara çevirir; adayları teslim edilecek ölçüye göre (çözünürlük payı, kırpma dayanıklılığı, marka rengi, metin için sessiz alan, klip süresi) sıralar. Şu ifadeler geçtiğinde kullan: "telifsiz görsel", "stok fotoğraf", "arka plan görseli", "blog kapağı", "doku bul", "Pexels", "ücretsiz görsel", "b-roll", "video arka plan", "banner görseli". Pexels adı hiç geçmese bile, bir teslimat için hazır görsel seçilecekse devreye gir. **Proje render'ının yerine geçecek görsel aramak için KULLANILMAZ** — o sınır aşağıda.

- **Ölçü:** 7.639 bayt · 4 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/moonstone/.claude/skills/pexels-gorsel-bulucu

## `pexels-media-scout`

[SKILL.md](pexels-media-scout/SKILL.md)

Finds, scores, clearance-checks and downloads royalty-free Pexels photos and video for music deliverables — album covers, YouTube thumbnails and long-form backgrounds, lyric-video and Spotify Canvas beds, Reels/Shorts footage, press kits. Turns a vague or Turkish brief into queries that actually return usable frames, ranks candidates against the real spec (resolution headroom, crop survival, brand colour, text room, clip duration and loopability), flags model-release and trademark risk before anything ships, and writes attribution files. Use whenever someone needs stock visuals or B-roll for music, a cover image, a thumbnail or a video background, or mentions Pexels — including Turkish phrasings like "telifsiz görsel bul", "albüm kapağı için fotoğraf", "youtube thumbnail görseli", "arka plan videosu lazım", "stok video indir", "pexels api ile görsel çek", "ücretsiz stok fotoğraf". Trigger even when Pexels is never named — if the task is picking the right free image or clip for a deliverable, this applies.

- **Ölçü:** 7.441 bayt · 4 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/projects/reelsindustry/.claude/skills/pexels-media-scout, ~/projects/weftrecords/.claude/skills/pexels-media-scout, ~/Documents/GitHub/reelsindustry/.claude/skills/pexels-media-scout

## `pexels-media-scout--weftrecords-gh`

[SKILL.md](pexels-media-scout--weftrecords-gh/SKILL.md)

Finds, scores, clearance-checks and downloads royalty-free Pexels photos and video for music deliverables — album covers, YouTube thumbnails and long-form backgrounds, lyric-video and Spotify Canvas beds, Reels/Shorts footage, press kits. Turns a vague or Turkish brief into queries that actually return usable frames, ranks candidates against the real spec (resolution headroom, crop survival, brand colour, text room, clip duration and loopability), flags model-release and trademark risk before anything ships, and writes attribution files. Use whenever someone needs stock visuals or B-roll for music, a cover image, a thumbnail or a video background, or mentions Pexels — including Turkish phrasings like "telifsiz görsel bul", "albüm kapağı için fotoğraf", "youtube thumbnail görseli", "arka plan videosu lazım", "stok video indir", "pexels api ile görsel çek", "ücretsiz stok fotoğraf". Trigger even when Pexels is never named — if the task is picking the right free image or clip for a deliverable, this applies.

- **Ölçü:** 7.441 bayt · 4 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/pexels-media-scout, claude.ai senkronu (efemer önbellek)

## `post-forge`

[SKILL.md](post-forge/SKILL.md)

Designs and RENDERS finished social post visuals — Instagram feed posts (4:5, 1:1), Stories frames, Instagram carousels and LinkedIn document carousels — as pixel-exact HTML/SVG exported to PNG and PDF. Builds custom SVG illustration, hand-drawn charts and product mockups (phone frame, laptop, browser window, isometric app screens, floating UI cards) instead of stock templates, locked to a brand design system. Use whenever the deliverable is the IMAGE, not the caption — "instagram postu tasarla", "post görseli üret", "carousel hazırla", "LinkedIn carousel", "şu ekranı telefon mockup'ında göster", "özel SVG çiz", "bu postlar birbirine benziyor, farklılaştır", "screenshot'u güzelleştir", "story görseli", "metrik kartı tasarla". Trigger even when the user only says "post" but points at a screenshot, a product screen, a metric or a design system, and for redesign or de-templating of existing visuals. Hand caption copy to trend-setter; this skill owns the pixels.

- **Ölçü:** 11.147 bayt · 11 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** github:farukciftler/pipsworn → .claude/skills/post-forge, ~/Documents/GitHub/pipsworn/.claude/skills/post-forge, claude.ai senkronu (efemer önbellek)

