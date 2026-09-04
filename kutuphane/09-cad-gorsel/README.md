# CAD & Görsel Üretim

Parametrik mobilya/CAD zinciri, markalı görsel hattı, stok görsel keşfi.

5 skill. Üst dizin: [../../README.md](../../README.md)

## `gorsel-uretim`

[SKILL.md](gorsel-uretim/SKILL.md)

Moonstone Residence için sosyal medya ve web görseli üretir — Instagram story/Reels karesi, feed ve carousel slaytı, OG görseli, sayı kartı, alıntı kartı, plan/veri kartı, web bölüm arka planı ve site için AVIF/WebP/JPEG varyantları. Markalı çerçeveyi, okunabilirlik katmanını, tipografiyi, altın ayracı, logoyu ve "Temsili görseldir" notunu doğru güvenli alan içinde yerleştirir; renk düzeltmesini Apple Silicon GPU'sunda Core Image ile yapar. Şu ifadeler geçtiğinde kullan: "görsel hazırla", "post tasarla", "story görseli", "kapak yap", "bu fotoğrafı markaya uyarla", "kırp", "boyutlandır", "renk düzelt", "logo bas", "carousel slaytı", "web için optimize et", "AVIF üret", "güvenli alanı kontrol et". Bir görsel dosyası üretilecek ya da var olan bir görsel Moonstone kimliğine uyarlanacaksa, araç adı hiç geçmese bile devreye gir. Görsel *bulmak* için `pexels-gorsel-bulucu`, hangi ölçü ve içeriğin gerektiği için `post-uretimi.md` / `story-uretimi.md`.

- **Ölçü:** 9.418 bayt · 6 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/moonstone/.claude/skills/gorsel-uretim

## `mobilya-cad`

[SKILL.md](mobilya-cad/SKILL.md)

Levha mobilya (suntalam/MDF dolap, ayakkabılık, gardırop, raf, TV ünitesi) tasarımını parametrik Python modelinden üretim ve sunum paketine çeviren zincir: build123d 3B (STEP/GLB/STL), ezdxf ölçülü teknik çizim (görünüş + kesit + antet, DXF/PDF/PNG), kesim listesi ve BOM (net/kesim ölçüsü, bant payı düşülmüş), donanım listesi, kenar bandı metrajı, giyotin nesting ve fire, parça başına CNC DXF (R12), Blender 5.2 render ve 8 sayfalık tasarım dosyası PDF. Kullanıcı "ayakkabılık", "dolap", "gardırop", "raf", "mobilya çiz", "3D model", "render", "teknik çizim", "kesit", "ölçülendir", "kesim listesi", "BOM", "kaç levha çıkar", "fire", "nesting", "kenar bandı", "DXF", "CNC", "malzeme listesi", "raf sarkar mı", "kaç çift alır", "askı sığar mı", "doku", "görsel" dediğinde ya da bir mobilya ölçülendirilir, malzeme/donanım seçilir veya üretime dosya hazırlanırken kullan. 32'lik sistem, minifix/menteşe delikleri, EN 312 P2 sehim, EN 14749 devrilme, askı derinliği ve desen yönü kuralları hesaplara gömülüdür.

- **Ölçü:** 18.267 bayt · 17 ek dosya · script içerir · referans dosyaları var
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
- **Kaynak:** ~/projects/reelsindustry/.claude/skills/pexels-media-scout, ~/projects/weftrecords/.claude/skills/pexels-media-scout

## `pexels-media-scout--weftrecords-gh`

[SKILL.md](pexels-media-scout--weftrecords-gh/SKILL.md)

Finds, scores, clearance-checks and downloads royalty-free Pexels photos and video for music deliverables — album covers, YouTube thumbnails and long-form backgrounds, lyric-video and Spotify Canvas beds, Reels/Shorts footage, press kits. Turns a vague or Turkish brief into queries that actually return usable frames, ranks candidates against the real spec (resolution headroom, crop survival, brand colour, text room, clip duration and loopability), flags model-release and trademark risk before anything ships, and writes attribution files. Use whenever someone needs stock visuals or B-roll for music, a cover image, a thumbnail or a video background, or mentions Pexels — including Turkish phrasings like "telifsiz görsel bul", "albüm kapağı için fotoğraf", "youtube thumbnail görseli", "arka plan videosu lazım", "stok video indir", "pexels api ile görsel çek", "ücretsiz stok fotoğraf". Trigger even when Pexels is never named — if the task is picking the right free image or clip for a deliverable, this applies.

- **Ölçü:** 7.441 bayt · 4 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/Documents/GitHub/weftrecords/.claude/skills/pexels-media-scout

