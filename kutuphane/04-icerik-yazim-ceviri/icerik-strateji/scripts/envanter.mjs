#!/usr/bin/env node
/**
 * İçerik envanteri — sıradaki işi öncelik sırasına dizer.
 *
 * Kullanım:
 *   node envanter.mjs                 tam rapor
 *   node envanter.mjs --sehir sam     tek kümeye odaklan
 *   node envanter.mjs --json          makine okunur çıktı
 *
 * Kaynak `content/` dizini: sunucuya hiç gitmiyor, veritabanına dokunmuyor,
 * saniyeler sürüyor. İçerik depoda dosya olarak yaşadığı için envanter de
 * dosyadan çıkıyor — bu, içeriği depoya taşımanın en somut kazancı.
 *
 * Betik yeni içerik **önermiyor**, eksik olanı gösteriyor. "Şu şehri ekle"
 * kararı insana ait; buradaki liste o kararın önündeki borcu sayıyor.
 */

import { readdir, readFile } from 'node:fs/promises';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const KOK = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const ICERIK = join(KOK, 'content');

/** Bir şehrin "çalışan küme" sayılması için asgari. Bkz. SKILL.md. */
const ASGARI_MEKAN = 3;
const ASGARI_ROTA = 1;
/** Rotanın iskeleti sayılan asgari durak. */
const ASGARI_DURAK = 3;

/**
 * Yürüyüş rotasında iki durak arası azami **yürünen** mesafe (km).
 *
 * Yürüyüş rotası okura "bunu yürüyerek yap" diyor; iki durak arası uzarsa
 * verilen söz tutulmuyor ve aradaki boşlukta anlatacak bir şey kalmıyor.
 */
const YURUYUS_AZAMI_KM = 1;

/**
 * Envanterin kullandığı **kuş uçuşu** eşiği — yukarıdaki kuralın vekili.
 *
 * Bu betiğin en değerli özelliği ağa hiç çıkmaması (bkz. dosya başı), o yüzden
 * gerçek yürüme mesafesi burada sorulamıyor. Kuş uçuşu ondan hep kısa: eski
 * şehir dokusunda ölçülen sapma çarpanı 1 km dolayında 1.16–1.35 arası
 * (Bab Şarkî→Azm 1.01→1.17; Halep Kalesi→Medine 0.66→0.89). En kötü çarpanla
 * 1 km'yi aşabilecek her bacağı yakalamak için eşik 0.75 km'ye çekildi.
 *
 * Yani bu eşik **fazladan uyarır, kaçırmaz**. Bulgu çıktığında karar gerçek
 * ölçümle verilir; nasıl ölçüleceği bulgunun eylem satırında yazıyor.
 */
const YURUYUS_KUS_UCUSU_ESIK_KM = 0.75;

const args = process.argv.slice(2);
const jsonCikti = args.includes('--json');
const sehirFiltresi = args.includes('--sehir') ? args[args.indexOf('--sehir') + 1] : null;

// ─── Okuma ──────────────────────────────────────────────────────────────────

async function klasorOku(ad) {
  const yol = join(ICERIK, ad);
  let dosyalar;
  try {
    dosyalar = await readdir(yol);
  } catch {
    return [];
  }

  const out = [];
  for (const dosya of dosyalar.filter((f) => f.endsWith('.json'))) {
    try {
      const kayit = JSON.parse(await readFile(join(yol, dosya), 'utf8'));
      kayit.__dosya = dosya.replace(/\.json$/, '');
      out.push(kayit);
    } catch (error) {
      console.error(`çözümlenemedi: ${ad}/${dosya} — ${error.message}`);
    }
  }
  return out;
}

const [sehirler, mekanlar, rotalar, yemekler] = await Promise.all([
  klasorOku('cities'),
  klasorOku('places'),
  klasorOku('routes'),
  klasorOku('food'),
]);

if (sehirler.length + mekanlar.length + rotalar.length + yemekler.length === 0) {
  console.error('content/ boş ya da bulunamadı.');
  process.exit(1);
}

/**
 * Tipten bağımsız denetimlerin gezdiği küme.
 *
 * `food` bu listeye eklenmeden önce envanterin kör noktasıydı: tip, REST
 * koleksiyonu ve JSON-LD dalı hazırdı ama envanter `content/food/` dizinini
 * hiç okumuyordu. Yemek kaydının dosya adı, kapak görseli, koordinatı ve
 * dil bütünlüğü hiçbir turda denetlenmiyordu — tam olarak bu betiğin
 * yakalaması gereken şeyler.
 */
const hepsi = [...sehirler, ...mekanlar, ...rotalar, ...yemekler];

const slugOf = (d) => d?.tr?.slug ?? '?';
const basligiOf = (d) => d?.tr?.title ?? slugOf(d);

// ─── Bulgular ───────────────────────────────────────────────────────────────

/** oncelik: küçük sayı = daha acil. Sıralama bunun üstünden yapılıyor. */
const bulgular = [];
const ekle = (oncelik, tur, hedef, mesaj, eylem) =>
  bulgular.push({ oncelik, tur, hedef, mesaj, eylem });

// Şehir başına mekan, rota ve yemek sayısı.
//
// Yemek `mekanSayisi`'na katılmıyor: çalışan küme eşiği (1 şehir + 3 mekan +
// 1 rota) mekanla ölçülüyor ve yemek kayıtlarını oraya saymak, üç mekanı
// olmayan bir şehri iki lokantayla "sağlıklı" gösterirdi.
const mekanSayisi = new Map();
const rotaSayisi = new Map();
const yemekSayisi = new Map();

for (const m of mekanlar) {
  if (m.city) mekanSayisi.set(m.city, (mekanSayisi.get(m.city) ?? 0) + 1);
}
for (const r of rotalar) {
  if (r.city) rotaSayisi.set(r.city, (rotaSayisi.get(r.city) ?? 0) + 1);
}
for (const y of yemekler) {
  if (y.city) yemekSayisi.set(y.city, (yemekSayisi.get(y.city) ?? 0) + 1);
}

// P0 — yetim kayıt: üretilmiş ama hiçbir şehir sayfasında görünmüyor.
for (const m of [...mekanlar, ...yemekler]) {
  if (!m.city) {
    ekle(0, 'yetim', slugOf(m), 'şehre bağlı değil', 'city alanına Türkçe şehir slug\'ı yaz');
  }
}

// P0 — dosya adı Türkçe slug'la eşleşmiyor.
//
// Dışa aktarma dosyaları **Türkçe slug'la** adlandırıyor. Elle farklı bir adla
// dosya oluşturulursa bir sonraki `--export` ikinci bir dosya üretiyor ve depo
// aynı kaydı iki kez taşıyor — biri kapak görselli, diğeri değil. Sessiz ve
// bulması zor bir hata; bir kez yaşandı.
for (const d of hepsi) {
  const slug = slugOf(d);
  if (d.__dosya && d.__dosya !== slug) {
    ekle(
      0,
      'dosya adı',
      d.__dosya,
      `Türkçe slug "${slug}" ile eşleşmiyor`,
      `dosyayı ${slug}.json olarak yeniden adlandır`,
    );
  }
}

// P1 — ölü hub, P5 — zayıf küme.
for (const s of sehirler) {
  const slug = slugOf(s);
  const m = mekanSayisi.get(slug) ?? 0;
  const r = rotaSayisi.get(slug) ?? 0;

  if (m < 2) {
    ekle(
      1,
      'ölü hub',
      slug,
      `${m} mekan, ${r} rota — "Bu şehirde" bölümü neredeyse boş`,
      `${ASGARI_MEKAN - m} mekan üret`,
    );
  } else if (m < ASGARI_MEKAN) {
    ekle(5, 'zayıf küme', slug, `${m} mekan`, `1 mekan daha ile sağlıklıya dönüyor`);
  }

  if (m >= 2 && r < ASGARI_ROTA) {
    ekle(5, 'rotasız küme', slug, `${m} mekan, rota yok`, 'mekanları bağlayan bir rota üret');
  }
}

// P2 — rota iskeleti.
for (const r of rotalar) {
  const durak = r.stops?.length ?? 0;
  if (durak < ASGARI_DURAK) {
    ekle(
      2,
      'kısa rota',
      slugOf(r),
      `${durak} durak (asgari ${ASGARI_DURAK})`,
      'güzergâh üzerindeki gerçek bir mekanı durak olarak ekle',
    );
  }
}

// P2 — yürüyüş rotasında durak arası mesafe.
//
// Koordinatı olmayan durak sessizce atlanıyor: onun kendi bulgusu zaten P4'te
// açılıyor ve burada ikinci kez saymak listeyi gürültüye boğardı.
const mekanKoordinati = new Map(
  mekanlar
    .filter((m) => m.ortak?.lat != null && m.ortak?.lng != null)
    .map((m) => [slugOf(m), { lat: m.ortak.lat, lng: m.ortak.lng }]),
);

/** İki nokta arası kuş uçuşu mesafe (km). */
function kusUcusuKm(a, b) {
  const R = 6371;
  const rad = (d) => (d * Math.PI) / 180;
  const dLat = rad(b.lat - a.lat);
  const dLng = rad(b.lng - a.lng);
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.sin(dLng / 2) ** 2 * Math.cos(rad(a.lat)) * Math.cos(rad(b.lat));
  return 2 * R * Math.asin(Math.sqrt(h));
}

for (const r of rotalar) {
  if (r.ortak?.mode !== 'walking') continue;

  const duraklar = r.stops ?? [];
  for (let i = 0; i < duraklar.length - 1; i++) {
    const a = mekanKoordinati.get(duraklar[i].place);
    const b = mekanKoordinati.get(duraklar[i + 1].place);
    if (!a || !b) continue;

    const km = kusUcusuKm(a, b);
    if (km <= YURUYUS_KUS_UCUSU_ESIK_KM) continue;

    // Eşik bilinçli fazladan uyarıyor; karar gerçek ölçümle veriliyor.
    // Ölçüm yapıldıysa sonucu rota dosyasındaki `olculmus_bacaklar` taşır
    // (gorselsiz ile aynı kalıp: "bakıldı" ile "unutuldu" ayırt edilebilsin).
    // Sınırın altındaki ölçüm bulguyu kapatır; üstündeki ölçüm tahmine değil
    // bilgiye dayandığı için pazarlıksız bulgudur.
    const bacakAdi = `${duraklar[i].place} → ${duraklar[i + 1].place}`;
    const olculen = r.olculmus_bacaklar?.[bacakAdi];
    if (typeof olculen === 'number') {
      if (olculen <= YURUYUS_AZAMI_KM) continue;
      ekle(
        2,
        'uzun yürüyüş bacağı',
        slugOf(r),
        `${bacakAdi}: ölçülen ${olculen.toFixed(2)} km (azami ${YURUYUS_AZAMI_KM} km)`,
        'aradaki güzergâh üzerine bir durak ekle',
      );
      continue;
    }

    ekle(
      2,
      'uzun yürüyüş bacağı',
      slugOf(r),
      `${duraklar[i].place} → ${duraklar[i + 1].place}: kuş uçuşu ${km.toFixed(2)} km ` +
        `(yürünen mesafe bundan uzun; azami ${YURUYUS_AZAMI_KM} km)`,
      'aradaki güzergâh üzerine bir durak ekle; önce gerçek mesafeyi ölç: ' +
        'valhalla1.openstreetmap.de/route, costing "pedestrian"',
    );
  }
}

// P3/P4 — mekanın somut alanları. Mekan aramalarının cevabı tam olarak bunlar.
for (const m of mekanlar) {
  const f = m.tr?.fields ?? {};
  const slug = slugOf(m);

  if (!f.entry_fee) ekle(3, 'eksik alan', slug, 'entry_fee boş', 'somut yaz ya da "Değişken — girişte teyit et"');
  if (!f.opening_hours) ekle(3, 'eksik alan', slug, 'opening_hours boş', 'ziyaret saati ekle');
  if (m.ortak?.lat == null || m.ortak?.lng == null) {
    ekle(4, 'eksik alan', slug, 'koordinat yok', 'lat/lng ekle — GeoCoordinates buna bağlı');
  }
}

// P3/P4 — yemek kaydının somut alanları.
//
// Yemekte künye ızgarası mekandan farklı: giriş ücreti anlamsız, "ne yenir" ve
// "ne kadar tutar" ise sayfanın en çok işe yarayan iki satırı. `kind` ayrıca
// JSON-LD alt tipini seçiyor (seo.tsx); listede olmayan bir değer sessizce
// `Restaurant`a düşüyor ve dondurmacı lokanta olarak işaretleniyor.
const YEMEK_TURLERI = ['restaurant', 'cafe', 'bakery', 'icecream', 'sweets'];

for (const y of yemekler) {
  const f = y.tr?.fields ?? {};
  const slug = slugOf(y);

  if (!f.signature) ekle(3, 'eksik alan', slug, 'signature boş', 'ne yenir — adıyla yaz');
  if (!f.price_range) ekle(3, 'eksik alan', slug, 'price_range boş', 'kişi başı aralık ya da "Değişken — sorup öğren"');
  if (!f.opening_hours) ekle(3, 'eksik alan', slug, 'opening_hours boş', 'açılış saati ekle');

  if (f.entry_fee) {
    ekle(3, 'fazla alan', slug, 'entry_fee dolu', 'yeme içmede giriş ücreti yok — boşalt, price_range kullan');
  }

  const kind = y.ortak?.kind;
  if (!kind) {
    ekle(3, 'eksik alan', slug, 'kind boş', `ortak.kind yaz: ${YEMEK_TURLERI.join(' / ')}`);
  } else if (!YEMEK_TURLERI.includes(kind)) {
    ekle(
      3,
      'geçersiz alan',
      slug,
      `kind "${kind}" listede yok`,
      `${YEMEK_TURLERI.join(' / ')} — başka değer JSON-LD'de sessizce Restaurant oluyor`,
    );
  }

  if (y.ortak?.lat == null || y.ortak?.lng == null) {
    ekle(4, 'eksik alan', slug, 'koordinat yok', 'lat/lng ekle — GeoCoordinates buna bağlı');
  }
}

// P6 — kapak görseli.
//
// `gorselsiz` alanı gerekçe taşıyorsa kayıt atlanır. Yanlış fotoğraf
// fotoğrafsızdan kötü olduğu için "arandı, doğrulanamadı" geçerli bir sonuç;
// her turda yeniden listelenmesi gerçek eksikleri gürültüye boğuyordu.
// Gerekçe zorunlu: boş bir bayrak, unutulmuş kayıtla bilinçli kararı
// birbirinden ayırt edilemez yapardı.
for (const d of hepsi) {
  if (d.featured_media) continue;
  if (typeof d.gorselsiz === 'string' && d.gorselsiz.trim()) continue;
  if (d.gorselsiz !== undefined) {
    ekle(6, 'görsel', slugOf(d), 'gorselsiz alanı gerekçesiz', 'gerekçe yaz ya da alanı kaldır');
    continue;
  }
  ekle(6, 'görsel', slugOf(d), 'kapak görseli yok', 'gorsel-ara.mjs ile ara; doğrulanamıyorsa gorselsiz alanına gerekçe yaz');
}

// Dil bütünlüğü — üç dilden biri eksikse hreflang bölünüyor.
for (const d of hepsi) {
  const eksik = ['tr', 'en', 'ar'].filter((l) => !d[l]);
  if (eksik.length) {
    ekle(1, 'eksik dil', slugOf(d), `${eksik.join(', ')} yok`, 'ceviri becerisiyle tamamla');
  }
}

// ─── Çıktı ──────────────────────────────────────────────────────────────────

const suzulmus = sehirFiltresi
  ? bulgular.filter((b) => b.hedef === sehirFiltresi || mekanSlugSehri(b.hedef) === sehirFiltresi)
  : bulgular;

function mekanSlugSehri(slug) {
  const m =
    mekanlar.find((x) => slugOf(x) === slug) ??
    rotalar.find((x) => slugOf(x) === slug) ??
    yemekler.find((x) => slugOf(x) === slug);
  return m?.city ?? null;
}

suzulmus.sort((a, b) => a.oncelik - b.oncelik || a.tur.localeCompare(b.tur));

if (jsonCikti) {
  console.log(
    JSON.stringify(
      {
        ozet: {
          sehir: sehirler.length,
          mekan: mekanlar.length,
          rota: rotalar.length,
          yemek: yemekler.length,
          bulgu: suzulmus.length,
        },
        kumeler: sehirler.map((s) => ({
          slug: slugOf(s),
          mekan: mekanSayisi.get(slugOf(s)) ?? 0,
          rota: rotaSayisi.get(slugOf(s)) ?? 0,
          yemek: yemekSayisi.get(slugOf(s)) ?? 0,
          saglikli:
            (mekanSayisi.get(slugOf(s)) ?? 0) >= ASGARI_MEKAN &&
            (rotaSayisi.get(slugOf(s)) ?? 0) >= ASGARI_ROTA,
        })),
        bulgular: suzulmus,
      },
      null,
      2,
    ),
  );
  process.exit(0);
}

// ANSI kacislari terminal disinda bosaltiliyor: `--json` ciktisi ya da
// `| less` gibi borulanmis kullanimda renk kodu gurultuden baska bir sey degil.
const renkli = process.stdout.isTTY;
const esc = (kod) => (renkli ? `\u001b[${kod}m` : '');
const K = { kirmizi: esc(31), sari: esc(33), yesil: esc(32), gri: esc(90), sifir: esc(0) };

console.log(`\nComeSyria içerik envanteri\n${'─'.repeat(64)}`);
console.log(
  `${sehirler.length} şehir · ${mekanlar.length} mekan · ${rotalar.length} rota · ` +
    `${yemekler.length} yemek\n`,
);

// Küme sağlığı tablosu — stratejinin tek bakışta görüldüğü yer.
//
// Yemek sütunu sağlık hesabına girmiyor, yalnızca gösteriliyor: hangi kümenin
// yeme içmede tamamen boş olduğu buradan görülüyor.
console.log('KÜMELER');
console.log(
  `  ${'şehir'.padEnd(14)}${'mekan'.padStart(6)}${'rota'.padStart(6)}${'yemek'.padStart(7)}   durum`,
);
for (const s of sehirler) {
  const slug = slugOf(s);
  if (sehirFiltresi && slug !== sehirFiltresi) continue;

  const m = mekanSayisi.get(slug) ?? 0;
  const r = rotaSayisi.get(slug) ?? 0;
  const y = yemekSayisi.get(slug) ?? 0;
  const saglikli = m >= ASGARI_MEKAN && r >= ASGARI_ROTA;
  const durum = m < 2 ? `${K.kirmizi}ölü hub${K.sifir}` : saglikli ? `${K.yesil}sağlıklı${K.sifir}` : `${K.sari}zayıf${K.sifir}`;

  console.log(
    `  ${slug.padEnd(14)}${String(m).padStart(6)}${String(r).padStart(6)}${String(y).padStart(7)}   ${durum}`,
  );
}

const saglikliSayi = sehirler.filter(
  (s) => (mekanSayisi.get(slugOf(s)) ?? 0) >= ASGARI_MEKAN && (rotaSayisi.get(slugOf(s)) ?? 0) >= ASGARI_ROTA,
).length;

console.log(
  `\n  ${saglikliSayi}/${sehirler.length} küme çalışıyor.` +
    (saglikliSayi < sehirler.length
      ? ` ${K.sari}Yeni şehir açmadan önce bunlar kapanmalı.${K.sifir}`
      : ` ${K.yesil}Yeni şehir açılabilir.${K.sifir}`),
);

if (suzulmus.length === 0) {
  console.log(`\n${K.yesil}Bulgu yok.${K.sifir}\n`);
  process.exit(0);
}

console.log(`\nYAPILACAKLAR (${suzulmus.length})`);

let sonOncelik = -1;
for (const b of suzulmus) {
  if (b.oncelik !== sonOncelik) {
    console.log(`\n  ${K.gri}── P${b.oncelik} ──${K.sifir}`);
    sonOncelik = b.oncelik;
  }
  console.log(`  ${b.tur.padEnd(13)} ${b.hedef.padEnd(32)} ${b.mesaj}`);
  console.log(`  ${' '.repeat(13)} ${K.gri}→ ${b.eylem}${K.sifir}`);
}

console.log(
  `\n${'─'.repeat(64)}\n` +
    `Üstteki madde açıkken alttakine geçme. Yeni şehir bu listede yok —\n` +
    `liste boşalana kadar sırası gelmiyor.\n`,
);
