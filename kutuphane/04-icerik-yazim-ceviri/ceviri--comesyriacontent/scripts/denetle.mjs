#!/usr/bin/env node
/**
 * Çeviri denetimi.
 *
 * Kullanım:
 *   node denetle.mjs kaynak.json ceviri.json
 *   node denetle.mjs --lang en --metin "serbest metin"
 *
 * İki iş yapıyor:
 *
 *   SADAKAT   Kaynaktaki sayı, fiyat ve saat çeviride duruyor mu; yazının
 *             iskeleti (H2, madde, bağlantı) korunmuş mu.
 *   TİKLİK    Hedef dile göre bilinen yapay zekâ kalıpları, cümle uzunluğu
 *             tekdüzeliği, bağlaç yoğunluğu.
 *
 * Betiğin okuyamadığı şey metnin kendisi. Temiz rapor "iyi çeviri" demek değil,
 * "bilinen hatalar yok" demek. Ölçüt hâlâ yüksek sesle okumak.
 *
 * Çıkış kodu: bulgu varsa 1, temizse 0.
 */

import { readFile } from 'node:fs/promises';

// ─── Kalıp listeleri ────────────────────────────────────────────────────────

/**
 * Yasak kalıplar. Her biri metni anında makine yapan, gerçek yazının
 * kullanmadığı ifadeler. Kaynakları: references/*.md
 */
const YASAK = {
  // JS'in `\w` ve `\b` sınıfları Türkçe harfleri tanımıyor: `\w*mektedir`
  // "sürmektedir"i "rmektedir" diye yakalıyor ve rapor kırık görünüyor. Bu
  // yüzden Türkçe kalıplar `\p{L}` ile ve `u` bayrağıyla yazılıyor; kelime
  // sınırı yerine harf-olmayan bağlam (`(?<![\p{L}])`) kullanılıyor.
  tr: [
    [/[\p{L}]*mektedir/giu, 'Bürokratik Türkçe: -mektedir → -yor'],
    [/[\p{L}]*maktadır/giu, 'Bürokratik Türkçe: -maktadır → -yor'],
    [/yer al(makta|ıyor)[\p{L}]*/giu, '"yer almaktadır" → "var", "duruyor"'],
    [/bulunmakta[\p{L}]*/giu, '"bulunmaktadır" → "var"'],
    [/gerçekleştir[\p{L}]*/giu, '"gerçekleştirmek" → yapmak, kurmak, düzenlemek'],
    [/sahip ol(an|duğu|makta)[\p{L}]*/giu, 'İngilizce calque: "sahip olmak" → "...-si var"'],
    [/söz konusu/giu, 'Resmî yazışma dili'],
    [/önem (arz|taşı)[\p{L}]*/giu, '"önem arz etmektedir" → "önemli"'],
    [/bunun yanı sıra|buna ek olarak/giu, 'Gereksiz bağlaç — sil'],
    [/deneyimi? yaşa[\p{L}]*/giu, '"deneyim yaşamak" → görmek, gezmek, denemek'],
    [
      /(?<![\p{L}])(eşsiz|büyüleyici|unutulmaz|muhteşem)(?![\p{L}])/giu,
      'Turizm sloganı — somut bilgi yaz',
    ],
    [/(?<![\p{L}])kalbinde(?![\p{L}])/giu, '"...-in kalbinde" → "ortasında", "göbeğinde"'],
  ],
  en: [
    [/\bnestled\b/gi, 'Gezi metni çöplüğü'],
    [/\bhidden gem\b/gi, 'Gezi metni çöplüğü'],
    [/\bmust[- ](visit|see)\b/gi, 'Gezi metni çöplüğü'],
    [/\bbreathtaking\b|\bstunning\b/gi, 'Gezi metni çöplüğü'],
    [/\bvibrant\b|\bbustling\b/gi, 'Gezi metni çöplüğü'],
    [/\bquaint\b|\bcharming\b|\bpicturesque\b/gi, 'Gezi metni çöplüğü'],
    [/\bsteeped in history\b/gi, 'Gezi metni çöplüğü'],
    [/\brich (cultural )?(heritage|history|tapestry)\b/gi, 'Boş övgü — hangi tarih?'],
    [/\bboasts\b/gi, '"boasts" → "has", ya da somut bilgi'],
    [/\ba testament to\b/gi, 'Gezi metni çöplüğü'],
    [/\bwhether you(\'re| are)\b/gi, 'Okuru kategorize etme'],
    [/\boff the beaten path\b/gi, 'Gezi metni çöplüğü'],
    [/\b(gateway|jewel|crown jewel) (to|of)\b/gi, 'Gezi metni çöplüğü'],
    [/\bunforgettable\b|\bonce[- ]in[- ]a[- ]lifetime\b/gi, 'Gezi metni çöplüğü'],
    [/\b(moreover|furthermore|additionally)\b/gi, 'Yapay zekâ bağlacı — sil'],
    [/\bit is worth noting\b/gi, 'Yastık ifade — sil'],
    [/\bin conclusion\b|\bto sum up\b/gi, 'Yazı zaten bitiyor — sil'],
    [/\bserves as a\b/gi, '"serves as a" → "is"'],
    [/\bplays a (crucial|key|vital) role\b/gi, 'Ne yaptığını yaz'],
    [/\bnot only\b[^.]{0,60}\bbut also\b/gi, 'Basit bağlaç ya da iki cümle'],
    // Amerikanizmler
    [/\b(downtown|sidewalk|vacation|gotten|reach out|touch base)\b/gi, 'Amerikanizm — küresel İngilizce değil'],
  ],
  ar: [
    [/علاوة على ذلك/g, 'Yapay zekâ bağlacı — sil'],
    [/بالإضافة إلى ذلك/g, 'Yapay zekâ bağlacı — sil'],
    [/من الجدير بالذكر/g, 'Yastık ifade — sil'],
    [/تجدر الإشارة/g, 'Yastık ifade — sil'],
    [/في الختام/g, '"Sonuç olarak" — sil'],
    [/يُعتبر من أهم|يعتبر من أهم/g, 'Kalıplaşmış övgü — somut bilgi yaz'],
    [/تاريخ عريق/g, 'Boş övgü ikilisi'],
    [/ثقافة غنية/g, 'Boş övgü ikilisi'],
    // Mısır / Körfez sızıntısı
    [/دلوقتي/g, 'Mısır ağzı — Şamîsi: هلق'],
    [/\bإيه\b/g, 'Mısır ağzı — Şamîsi: شو'],
    [/عايز/g, 'Mısır ağzı — Şamîsi: بدي'],
    [/كويس/g, 'Mısır ağzı — Şamîsi: منيح'],
    // "منذ ذلك الحين" fasih Arapçada "o zamandan beri" demek; yasaklanan
    // Körfez kullanımı tek başına duran ve "şimdi" anlamına gelen الحين.
    [/(?<!ذلك )(?<!ذاك )الحين/g, 'Körfez ağzı — Şamîsi: هلق'],
    [/\bوش\b/g, 'Körfez ağzı — Şamîsi: شو'],
    [/سوريا(?!ت)/g, 'Bu sitede Suriye: سورية'],
    // Ağıt tonu
    [/ما تبقى من|أطلال|ذكريات ضائعة/g, 'Ağıt tonu — marka sesi bunu reddediyor'],
  ],
};

/** Bağlaç yoğunluğu ölçülen kalıplar. */
const BAGLAC = {
  tr: /\b(ayrıca|bununla birlikte|dolayısıyla|bu nedenle|ancak|fakat)\b/gi,
  en: /\b(however|therefore|moreover|furthermore|additionally|thus|hence)\b/gi,
  ar: /(كما أن|لذلك|بالتالي|غير أن|إلا أن|ومع ذلك)/g,
};

/** Özet uzunluğu hedefi — Arapça aynı anlamı daha az karakterle taşıyor. */
const OZET_HEDEF = { tr: [150, 165], en: [150, 165], ar: [125, 155] };

// ─── Rapor ──────────────────────────────────────────────────────────────────

const bulgular = [];
const ekle = (seviye, baslik, ayrinti) => bulgular.push({ seviye, baslik, ayrinti });

// ─── Yardımcılar ────────────────────────────────────────────────────────────

const stripTags = (html) => String(html ?? '').replace(/<[^>]*>/g, ' ');

/** Arap-Hint rakamlarını Latin'e çevirir — sadakat karşılaştırması için. */
function normalizeDigits(text) {
  return String(text ?? '').replace(/[٠-٩]/g, (d) => String(d.charCodeAt(0) - 0x0660));
}

/**
 * Metindeki anlamlı sayılar.
 *
 * Saatler önce ve bütün olarak alınıyor: "09:00" iki ayrı sayı sayılırsa hem
 * rapor gürültülü çıkıyor hem de çeviride saat biçimi değişmişse ("9am") üç
 * ayrı yanlış hata üretiyor. Saat olarak tüketilen rakamlar ikinci taramaya
 * girmiyor.
 */
function sayilar(text) {
  const clean = normalizeDigits(stripTags(text));

  const saatler = clean.match(/\d{1,2}:\d{2}/g) ?? [];
  const kalan = clean.replace(/\d{1,2}:\d{2}/g, ' ');
  const digerleri = kalan.match(/\d+(?:[.,]\d+)?/g) ?? [];

  return [...new Set([...saatler, ...digerleri])];
}

function etiketSay(html, etiket) {
  const matches = String(html ?? '').match(new RegExp(`<${etiket}[\\s>]`, 'gi'));
  return matches ? matches.length : 0;
}

/** Cümlelere böler. Arapça kendi soru işaretini ve virgülünü kullanıyor. */
function cumleler(text, lang) {
  const clean = stripTags(text).replace(/\s+/g, ' ').trim();
  if (!clean) return [];
  const sinir = lang === 'ar' ? /[.؟!]+/ : /[.?!]+/;
  return clean
    .split(sinir)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

const kelimeSay = (cumle) => cumle.split(/\s+/).filter(Boolean).length;

// ─── Yüzyıl ─────────────────────────────────────────────────────────────────

/**
 * Yüzyıl sayı sadakatinin istisnası — ama muafiyeti değil.
 *
 * Arapçada yüzyıl rakamla değil sıra sayısıyla yazılıyor: "18. yüzyıl" karşılığı
 * "القرن الثامن عشر". Bu doğru Arapça ve sitenin yerleşik üslubu (on sekiz
 * kayıt böyle). Düz rakam araması bunu "sayı düştü" diye HATA veriyordu; oysa
 * okur bilgiyi eksiksiz görüyor. Kaybolan fiyatla eş tutulacak bir şey değil.
 *
 * Rakama çevirmek yanlış çözümdü: on sekiz kaydın üslubunu bozardı. Ölçüm asıl
 * sorunu da gösterdi — düz arama yüzyılları **tesadüfen** geçiriyordu.
 * krak-des-chevaliers'ın Arapçası denetimi yalnızca "1271" tarihi "12" dizisini
 * içerdiği için geçiyor; yüzyıl gerçekten yazılmasa da geçerdi. Yani kural
 * hiç uygulanmıyordu.
 *
 * Bu yüzden istisna yüzyılı atlamıyor, **doğruluyor**: hedef dilde yüzyıl
 * sözcüğünün yanında ya rakam ya da o dilin sıra sayısı duruyor mu. Yüzyıl
 * gerçekten düşmüşse hata olarak kalıyor.
 */
const YUZYIL_SOZCUGU = {
  tr: /yüzyıl/giu,
  en: /centur(?:y|ies)/gi,
  ar: /قرن|قرون/g,
};

/**
 * Sıra sayıları. Arapçada `قرن` eril, o yüzden eril biçimler; `العشرين` ve
 * `العشرون` ikisi de geçerli (cümledeki i'raba göre değişiyor).
 *
 * Onluk tuzağı: "الثاني" hem 2 hem de 12'nin ("الثاني عشر") başlangıcı. 1–10
 * arası biçimler bu yüzden ardından `عشر` gelmediğinde sayılıyor — yoksa
 * kaynaktaki 2, hedefteki 12'yle eşleşip sessizce geçerdi. İngilizcede aynı
 * tuzak yok ("eighth" ile "eighteenth" ayrı diziler) ama sözcük sınırı yine de
 * konuyor.
 */
const SIRA_SAYISI = {
  tr: {},
  en: {
    1: ['first'], 2: ['second'], 3: ['third'], 4: ['fourth'], 5: ['fifth'],
    6: ['sixth'], 7: ['seventh'], 8: ['eighth'], 9: ['ninth'], 10: ['tenth'],
    11: ['eleventh'], 12: ['twelfth'], 13: ['thirteenth'], 14: ['fourteenth'],
    15: ['fifteenth'], 16: ['sixteenth'], 17: ['seventeenth'], 18: ['eighteenth'],
    19: ['nineteenth'], 20: ['twentieth'], 21: ['twenty-first'],
  },
  ar: {
    1: ['الأول'], 2: ['الثاني'], 3: ['الثالث'], 4: ['الرابع'], 5: ['الخامس'],
    6: ['السادس'], 7: ['السابع'], 8: ['الثامن'], 9: ['التاسع'], 10: ['العاشر'],
    11: ['الحادي عشر'], 12: ['الثاني عشر'], 13: ['الثالث عشر'],
    14: ['الرابع عشر'], 15: ['الخامس عشر'], 16: ['السادس عشر'],
    17: ['السابع عشر'], 18: ['الثامن عشر'], 19: ['التاسع عشر'],
    20: ['العشرين', 'العشرون'], 21: ['الحادي والعشرين', 'الحادي والعشرون'],
  },
};

/** Kaynak metinde yüzyıl olarak anılan sayılar. Kaynak her zaman Türkçe. */
function kaynakYuzyillar(kaynakMetin) {
  const clean = normalizeDigits(stripTags(kaynakMetin));
  const eslesme = clean.match(/\d+\s*\.\s*yüzyıl/giu) ?? [];
  return new Set(eslesme.map((m) => m.match(/\d+/)[0]));
}

/**
 * Hedef metinde `n`. yüzyıl gerçekten ifade edilmiş mi.
 *
 * Yüzyıl sözcüğünün çevresine bakılıyor, metnin tamamına değil: Türkçe ve
 * Arapça sayıyı önüne ("القرن الثامن عشر", "18. yüzyıl"), İngilizce de önüne
 * ("18th century") koyuyor, ama Arapçada aralık "بين القرنين 15 و13" diye
 * sözcükten sonra da gelebiliyor. İki yöne de bakmak bu yüzden.
 */
function yuzyilVar(ceviriMetinNorm, n, lang) {
  const sozcuk = YUZYIL_SOZCUGU[lang];
  if (!sozcuk) return false;

  const sayi = Number(n);
  const biçimler = SIRA_SAYISI[lang]?.[sayi] ?? [];
  const onlukAlti = lang === 'ar' && sayi >= 1 && sayi <= 10;

  for (const eslesme of ceviriMetinNorm.matchAll(sozcuk)) {
    const bas = Math.max(0, eslesme.index - 40);
    const pencere = ceviriMetinNorm.slice(bas, eslesme.index + eslesme[0].length + 40);

    // Rakamla yazılmış: "القرن 19", "18th century", "18. yüzyıl".
    if (new RegExp(`(?<![0-9])${n}(?![0-9])`).test(pencere)) return true;

    // Sıra sayısıyla yazılmış.
    for (const biçim of biçimler) {
      const kalip = onlukAlti
        ? new RegExp(`${biçim}(?!\\s*عشر)`)
        : new RegExp(lang === 'ar' ? biçim : `\\b${biçim}\\b`, 'i');
      if (kalip.test(pencere)) return true;
    }
  }

  return false;
}

// ─── Denetimler ─────────────────────────────────────────────────────────────

/**
 * Sayı sadakati.
 *
 * Çeviride en sık ve en pahalı kayıp bu: fiyat ya da saat düşerse okur bilgiyi
 * hiç görmüyor. İki haneli ve üstü sayılar hata, tek haneliler uyarı — tek
 * rakam çoğu zaman cümle içinde eriyip başka türlü ifade edilebiliyor.
 *
 * Yüzyıllar ayrı yoldan gidiyor; gerekçesi `yuzyilVar` başında. Düşen yüzyıl
 * tek haneli olsa bile HATA: "eriyip başka türlü ifade edilmiş olabilir"
 * gerekçesi burada geçmiyor, çünkü o başka biçimlere `yuzyilVar` zaten baktı.
 * Rapora ayrı satır olarak giriyor — "3 yok" demek yerine hangi yüzyılın
 * düştüğünü söylemek düzeltmeyi kısaltıyor.
 */
function sadakatSayilar(kaynakMetin, ceviriMetin, lang) {
  const kaynakSet = sayilar(kaynakMetin);
  const ceviriMetinNorm = normalizeDigits(stripTags(ceviriMetin));
  const yuzyillar = kaynakYuzyillar(kaynakMetin);

  const eksikYuzyil = [...yuzyillar].filter((n) => !yuzyilVar(ceviriMetinNorm, n, lang));
  const eksik = kaynakSet.filter((n) => !yuzyillar.has(n) && !ceviriMetinNorm.includes(n));

  if (eksikYuzyil.length) {
    ekle(
      'HATA',
      'Kaynaktaki yüzyıl çeviride geçmiyor',
      `${eksikYuzyil.map((n) => `${n}.`).join(', ')} — hedef dilde rakamla ya da ` +
        'sıra sayısıyla yaz (18th century / القرن الثامن عشر).',
    );
  }
  if (eksik.length === 0) return;

  const ciddi = eksik.filter((n) => n.replace(/[.,]/g, '').length >= 2);
  const hafif = eksik.filter((n) => n.replace(/[.,]/g, '').length < 2);

  if (ciddi.length) {
    ekle('HATA', 'Kaynaktaki sayılar çeviride yok', ciddi.join(', '));
  }
  if (hafif.length) {
    ekle('UYARI', 'Tek haneli sayılar çeviride görünmüyor', hafif.join(', '));
  }
}

/** Yazının iskeleti korunmuş mu. */
function sadakatYapi(kaynakHtml, ceviriHtml) {
  for (const etiket of ['h2', 'h3', 'li', 'a']) {
    const k = etiketSay(kaynakHtml, etiket);
    const c = etiketSay(ceviriHtml, etiket);
    if (k !== c) {
      ekle(
        etiket === 'a' ? 'UYARI' : 'HATA',
        `<${etiket}> sayısı tutmuyor`,
        `kaynak ${k}, çeviri ${c}`,
      );
    }
  }
}

/** Hedef dile göre yasak kalıplar. */
function tiklikler(metin, lang) {
  const duz = stripTags(metin);
  for (const [kalip, aciklama] of YASAK[lang] ?? []) {
    const eslesme = duz.match(kalip);
    if (eslesme) {
      ekle('HATA', `Yapay zekâ kalıbı: "${[...new Set(eslesme)].join('", "')}"`, aciklama);
    }
  }
}

/**
 * Cümle uzunluğu tekdüzeliği.
 *
 * Makine hep 15–25 kelimelik cümle yazıyor; insan yazısında dört kelimelik de
 * kırk kelimelik de var. Standart sapma ortalamanın %35'inin altındaysa ritim
 * düz demektir. Eşik ampirik: iyi yazılmış metinlerde bu oran genelde 0.45+.
 */
function ritim(metin, lang) {
  const liste = cumleler(metin, lang);
  if (liste.length < 5) return;

  const uzunluk = liste.map(kelimeSay);
  const ortalama = uzunluk.reduce((a, b) => a + b, 0) / uzunluk.length;
  const sapma = Math.sqrt(
    uzunluk.reduce((acc, n) => acc + (n - ortalama) ** 2, 0) / uzunluk.length,
  );
  const oran = sapma / ortalama;

  if (oran < 0.35) {
    ekle(
      'UYARI',
      'Cümle uzunlukları tekdüze',
      `ortalama ${ortalama.toFixed(1)} kelime, sapma/ortalama ${oran.toFixed(2)} ` +
        '(0.35 altı makine ritmi). Araya kısa cümle koy.',
    );
  }

  const uzun = liste.filter((c) => kelimeSay(c) > 40);
  if (uzun.length) {
    ekle('UYARI', `${uzun.length} cümle 40 kelimeden uzun`, `ilki: "${uzun[0].slice(0, 70)}…"`);
  }
}

/** Bağlaç yoğunluğu. */
function baglacYogunlugu(metin, lang) {
  const liste = cumleler(metin, lang);
  if (liste.length < 4) return;

  const sayi = (stripTags(metin).match(BAGLAC[lang]) ?? []).length;
  const oran = sayi / liste.length;

  if (oran > 0.3) {
    ekle(
      'UYARI',
      'Bağlaç yoğunluğu yüksek',
      `${liste.length} cümlede ${sayi} bağlaç. İlişki çoğu zaman zaten belli; söylemek zayıflatıyor.`,
    );
  }
}

/** Arapçaya özgü teknik kontroller. */
function arapcaTeknik(metin) {
  const duz = stripTags(metin);

  if (/[٠-٩]/.test(duz)) {
    ekle(
      'HATA',
      'Arap-Hint rakamı kullanılmış (١٢٣)',
      'Ön yüz Latin rakam basıyor (ar-u-nu-latn). Gövdede de Latin rakam yaz.',
    );
  }

  // Arapça metinde Latin noktalama, kopyala-yapıştır çevirinin izi.
  const arapcaVar = /[؀-ۿ]/.test(duz);
  if (arapcaVar && /\?/.test(duz)) {
    ekle('UYARI', 'Latin soru işareti (?) kullanılmış', 'Arapçası: ؟');
  }
  if (arapcaVar && /,/.test(duz)) {
    ekle('UYARI', 'Latin virgül (,) kullanılmış', 'Arapçası: ،');
  }
}

/** Alan düzeyi kontroller: slug, özet, başlık. */
function alanlar(kaynak, ceviri) {
  const lang = ceviri.lang;

  if (kaynak.slug && ceviri.slug && kaynak.slug === ceviri.slug) {
    ekle(
      'HATA',
      'Slug kopyalanmış',
      `"${ceviri.slug}" her iki dilde aynı. Hedef dilin okuru için yeniden türet (sam / damascus / dimashq).`,
    );
  }

  if (ceviri.slug && !/^[a-z0-9-]+$/.test(ceviri.slug)) {
    ekle('HATA', 'Slug ASCII değil', `"${ceviri.slug}" — küçük harf, rakam ve tire kullan.`);
  }

  if (ceviri.excerpt) {
    const uzunluk = ceviri.excerpt.length;
    const [alt, ust] = OZET_HEDEF[lang] ?? OZET_HEDEF.tr;
    if (uzunluk < alt || uzunluk > ust) {
      ekle(
        uzunluk > ust + 30 || uzunluk < alt - 40 ? 'HATA' : 'UYARI',
        'Özet uzunluğu hedef dışında',
        `${uzunluk} karakter, hedef ${alt}–${ust} (${lang}).`,
      );
    }
  } else {
    ekle('HATA', 'Özet boş', 'Meta açıklama buradan geliyor; boşsa gövdeden rastgele cümle seçiliyor.');
  }

  if (ceviri.title && /ComeSyria/i.test(ceviri.title)) {
    ekle('HATA', 'Başlıkta marka adı var', 'Ön yüz "%s · ComeSyria" şablonunu kendisi uyguluyor.');
  }

  // Birebir kopya — çeviri yapılmamış.
  // (medya kontrolü ayrı fonksiyonda; bkz. medya())
  const k = stripTags(kaynak.content ?? '').replace(/\s+/g, ' ').trim();
  const c = stripTags(ceviri.content ?? '').replace(/\s+/g, ' ').trim();
  if (k && c && k === c) {
    ekle('HATA', 'Gövde kaynakla birebir aynı', 'Çeviri yapılmamış.');
  }
}

/**
 * Görsel sadakati.
 *
 * Çeviri kaynakla aynı fotoğrafı kullanır ve bunu aynı ek kimliğini kopyalayarak
 * yapar — Polylang'de medya çevirisi kapalı olduğu için bir ek bütün dillerde
 * ortak. Kimliği kopyalamayı unutmak sessiz bir hata: kayıt sorunsuz
 * yayımlanıyor ama çeviri sayfası kapaksız kalıyor.
 *
 * `alt` kasten denetlenmiyor. Alt metin ekin üstünde duruyor, yani diller
 * arasında paylaşılıyor; çeviride yazılan bir alt kaynağınkini ezer.
 */
function medya(sabit, ceviri) {
  const kaynakKapak = sabit?.featured_media ?? null;
  const ceviriKapak = ceviri.featured_media ?? null;

  if (kaynakKapak && !ceviriKapak) {
    ekle(
      'HATA',
      'Çeviride kapak görseli yok',
      `Kaynakta featured_media=${kaynakKapak}. Aynı kimliği kopyala — çeviri aynı fotoğrafı kullanır.`,
    );
  } else if (kaynakKapak && ceviriKapak && kaynakKapak !== ceviriKapak) {
    ekle(
      'UYARI',
      'Kapak görseli kaynaktan farklı',
      `kaynak ${kaynakKapak}, çeviri ${ceviriKapak}. Kasıtlı değilse aynı kimliği kullan.`,
    );
  }

  const kaynakGaleri = sabit?.gallery ?? [];
  const ceviriGaleri = ceviri.fields?.gallery ?? [];

  if (kaynakGaleri.length && ceviriGaleri.length !== kaynakGaleri.length) {
    ekle(
      'HATA',
      'Galeri görselleri eksik',
      `kaynak ${kaynakGaleri.length} görsel, çeviri ${ceviriGaleri.length}. Kimlikleri aynen kopyala.`,
    );
  }

  if (ceviri.fields?.alt || ceviri.alt) {
    ekle(
      'UYARI',
      'Çeviride alt metni yazılmış',
      'Alt metin ek üzerinde ve diller arasında ortak; buraya yazmak kaynağınkini eziyor.',
    );
  }
}

// ─── Giriş ──────────────────────────────────────────────────────────────────

function bayrak(name) {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? null : process.argv[index + 1];
}

async function main() {
  const serbestMetin = bayrak('metin');

  if (serbestMetin) {
    const lang = bayrak('lang') ?? 'tr';
    tiklikler(serbestMetin, lang);
    ritim(serbestMetin, lang);
    baglacYogunlugu(serbestMetin, lang);
    if (lang === 'ar') arapcaTeknik(serbestMetin);
    return rapor(lang);
  }

  const [kaynakDosya, ceviriDosya] = process.argv.slice(2).filter((a) => !a.startsWith('--'));

  if (!kaynakDosya || !ceviriDosya) {
    console.error('Kullanım: denetle.mjs kaynak.json ceviri.json  |  --lang en --metin "..."');
    process.exit(1);
  }

  const kaynak = JSON.parse(await readFile(kaynakDosya, 'utf8'));
  const ceviri = JSON.parse(await readFile(ceviriDosya, 'utf8'));

  // Fiş biçiminde geldiyse (cek.mjs çıktısı) gövdeyi oradan al.
  const kaynakIcerik = kaynak.cevrilecek ?? kaynak;
  const lang = ceviri.lang ?? 'tr';

  if (!YASAK[lang]) {
    console.error(`Bilinmeyen dil: ${lang}. Beklenen: tr, en, ar.`);
    process.exit(1);
  }

  // Kaynak ve hedef aynı dildeyse karşılaştırmanın hiçbir maddesi anlamlı
  // değil — slug zaten aynı, kalıplar zaten kaynağın kalıpları. Bunu sessizce
  // "slug kopyalanmış" diye raporlamak yanıltıyor.
  const kaynakLang = kaynak.kaynak?.lang ?? kaynak.lang;
  if (kaynakLang && kaynakLang === lang) {
    console.error(
      `Kaynak ve çeviri aynı dilde (${lang}). Çeviri dosyasının "lang" alanını kontrol et.`,
    );
    process.exit(1);
  }

  const kaynakHepsi = [kaynakIcerik.content, kaynakIcerik.entry_fee, kaynakIcerik.opening_hours]
    .filter(Boolean)
    .join(' ');
  const ceviriHepsi = [ceviri.content, ceviri.fields?.entry_fee, ceviri.fields?.opening_hours]
    .filter(Boolean)
    .join(' ');

  sadakatSayilar(kaynakHepsi, ceviriHepsi, lang);
  sadakatYapi(kaynakIcerik.content, ceviri.content);
  medya(kaynak.sabit, ceviri);
  alanlar({ slug: kaynak.kaynak?.slug ?? kaynak.slug, content: kaynakIcerik.content }, ceviri);
  tiklikler([ceviri.title, ceviri.excerpt, ceviri.content].filter(Boolean).join(' '), lang);
  ritim(ceviri.content, lang);
  baglacYogunlugu(ceviri.content, lang);
  if (lang === 'ar') arapcaTeknik([ceviri.title, ceviri.excerpt, ceviri.content].filter(Boolean).join(' '));

  rapor(lang);
}

function rapor(lang) {
  const hatalar = bulgular.filter((b) => b.seviye === 'HATA');
  const uyarilar = bulgular.filter((b) => b.seviye === 'UYARI');

  console.log(`\nÇeviri denetimi — hedef dil: ${lang}\n${'─'.repeat(60)}`);

  if (bulgular.length === 0) {
    console.log('Bulgu yok.\n');
    console.log('Not: betik kalıp tanıyor, metni okuyamıyor. Temiz rapor iyi');
    console.log('çeviri demek değil. Son ölçüt hâlâ yüksek sesle okumak.\n');
    process.exit(0);
  }

  for (const grup of [hatalar, uyarilar]) {
    for (const b of grup) {
      console.log(`\n[${b.seviye}] ${b.baslik}`);
      console.log(`         ${b.ayrinti}`);
    }
  }

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`${hatalar.length} hata, ${uyarilar.length} uyarı.\n`);

  process.exit(hatalar.length > 0 ? 1 : 0);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
