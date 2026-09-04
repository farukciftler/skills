#!/usr/bin/env node
/**
 * Bir kaydı çeviri fişi olarak çeker.
 *
 * Kullanım:
 *   node cek.mjs --type place --slug halep-kalesi --lang tr
 *   node cek.mjs --id 42
 *
 * Çıktı iki bloğa ayrılmış bir JSON: `cevrilecek` ve `sabit`. Ayrım kasıtlı —
 * koordinat, süre, mesafe ve fiyat gibi alanlar çeviride en sık kaybolan ya da
 * bozulan veriler. Fişte ayrı durunca kopyalanacakları belli oluyor.
 *
 * Yayımlama bu betiğin işi değil: `icerik-uret/scripts/wp-post.mjs` kullanılır.
 */

const args = process.argv.slice(2);

function flag(name) {
  const index = args.indexOf(`--${name}`);
  return index === -1 ? null : args[index + 1];
}

const id = flag('id');
const type = flag('type');
const slug = flag('slug');
const lang = flag('lang') ?? 'tr';

if (!id && !(type && slug)) {
  console.error('Kullanım: cek.mjs --type <tip> --slug <slug> [--lang tr] | --id <id>');
  process.exit(1);
}

/** WordPress içerik tipi → REST koleksiyon adı. */
const REST_BASE = { post: 'posts', city: 'cities', place: 'places', route: 'routes' };

/**
 * İç adres tercih edilir: betik sunucunun içinden çalışıyor, nginx ve TLS
 * katmanını dolaşmasının faydası yok. `icerik-uret` betikleriyle aynı kural.
 */
function apiBase() {
  const value = process.env.WP_ADMIN_API_URL || process.env.WP_URL;
  if (!value) {
    console.error('WP_ADMIN_API_URL ya da WP_URL tanımlı değil.');
    process.exit(1);
  }
  return value.replace(/\/$/, '');
}

const base = apiBase();

/**
 * Çeviride aynen kopyalanacak alanlar.
 *
 * Sayısal olan her şey ve koordinatlar. `entry_fee` ve `opening_hours` listede
 * yok çünkü içlerinde hem sabit sayı hem çevrilecek kelime var ("1500 SYP",
 * "pazartesi kapalı") — onlar `cevrilecek` tarafında, uyarısıyla birlikte.
 */
const SABIT_ALANLAR = ['lat', 'lng', 'duration', 'distance', 'population'];

/** Çevrilmeyip hedef dilde yeniden türetilecek alanlar. */
const YENIDEN_TURETILIR = ['slug', 'excerpt', 'subtitle'];

async function main() {
  const url = id
    ? `${base}/wp-json/wp/v2/${REST_BASE[type] ?? 'posts'}/${id}`
    : `${base}/wp-json/wp/v2/${REST_BASE[type]}?slug=${encodeURIComponent(slug)}&lang=${lang}&per_page=1`;

  const response = await fetch(url, {
    headers: {
      Accept: 'application/json',
      // İç adrese giden istek düz HTTP; WordPress'in kendini https sanması için
      // nginx'in ürettiği başlık elle ekleniyor.
      'X-Forwarded-Proto': 'https',
    },
  });

  if (!response.ok) {
    console.error(`WordPress ${response.status} döndü: ${url}`);
    process.exit(1);
  }

  const payload = await response.json();
  const record = Array.isArray(payload) ? payload[0] : payload;

  if (!record) {
    console.error('Kayıt bulunamadı.');
    process.exit(1);
  }

  const fields = record.cs?.fields ?? {};

  const cevrilecek = {
    title: record.title?.rendered ?? '',
    content: record.content?.rendered ?? '',
    tips: fields.tips ?? [],
    highlights: fields.highlights ?? [],
    address: fields.address ?? null,
    period: fields.period ?? null,
    best_time: fields.best_time ?? null,
    best_season: fields.best_season ?? null,
    // Bu ikisinde sayı aynen kalır, çevresindeki kelime çevrilir.
    entry_fee: fields.entry_fee ?? null,
    opening_hours: fields.opening_hours ?? null,
  };

  const sabit = Object.fromEntries(
    SABIT_ALANLAR.filter((key) => fields[key] !== null && fields[key] !== undefined).map((key) => [
      key,
      fields[key],
    ]),
  );

  // Görsel kimlikleri de sabit: çeviri aynı fotoğrafı kullanır. Polylang'de
  // medya çevirisi kapalı olduğu için bir ek bütün dillerde ortak — aynı
  // kimlik her dilde aynı dosyayı veriyor. Kopyalamayı unutmak sessizce
  // kapaksız bir çeviri sayfası bırakıyor.
  if (record.featured_media) {
    sabit.featured_media = record.featured_media;
  }
  if (fields.gallery?.length) {
    sabit.gallery = fields.gallery.map((image) => image.id);
  }

  // Rota durakları ve şehir bağı kimlik taşıyor. Çeviri kaydı **hedef dildeki**
  // kimliklere bağlanmalı; kaynağınkini kopyalamak mekanı yanlış dile bağlar.
  const bagliKayitlar = {};
  if (fields.city) {
    bagliKayitlar.city = { kaynak_id: fields.city.id, kaynak_slug: fields.city.slug };
  }
  if (fields.stops?.length) {
    bagliKayitlar.stops = fields.stops.map((stop) => ({
      kaynak_id: stop.place.id,
      kaynak_slug: stop.place.slug,
      note: stop.note,
    }));
  }

  const fis = {
    _yonerge:
      'cevrilecek bloğunu hedef dilde YENİDEN YAZ. sabit bloğunu olduğu gibi kopyala. ' +
      'yeniden_turetilir alanları çevrilmez, hedef dilin okuru için baştan yazılır. ' +
      'bagli_kayitlar içindeki kimlikler HEDEF DİLDEKİ karşılıklarıyla değiştirilmeli.',

    kaynak: {
      id: record.id,
      type: record.type,
      slug: record.slug,
      lang: record.cs?.lang ?? lang,
    },

    mevcut_ceviriler: record.cs?.translations ?? {},

    cevrilecek,
    sabit,

    yeniden_turetilir: Object.fromEntries(
      YENIDEN_TURETILIR.map((key) => [
        key,
        key === 'slug' ? record.slug : key === 'excerpt' ? stripTags(record.excerpt?.rendered ?? '') : fields[key] ?? null,
      ]),
    ),

    bagli_kayitlar: bagliKayitlar,

    gorsel: record.cs?.image
      ? { id: record.cs.image.id, mevcut_alt: record.cs.image.alt }
      : null,
  };

  console.log(JSON.stringify(fis, null, 2));
}

function stripTags(html) {
  return html
    .replace(/<[^>]*>/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
