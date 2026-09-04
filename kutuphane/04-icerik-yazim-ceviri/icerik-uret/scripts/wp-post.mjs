#!/usr/bin/env node
/**
 * Bir içerik kaydını oluşturur ya da günceller.
 *
 * Kullanım:
 *   node wp-post.mjs icerik.json [--translation-of <id>]
 *
 * JSON şeması için ornek-icerik.json dosyasına bak. Aynı slug ikinci kez
 * gönderilirse yeni kayıt açılmaz, mevcut kayıt güncellenir — betiği tekrar
 * çalıştırmak kopya üretmemeli.
 */

import { readFile } from 'node:fs/promises';

const file = process.argv[2];
if (!file || file.startsWith('--')) {
  console.error('Kullanım: wp-post.mjs icerik.json [--translation-of <id>]');
  process.exit(1);
}

const translationOfIndex = process.argv.indexOf('--translation-of');
const translationOf = translationOfIndex === -1 ? null : Number(process.argv[translationOfIndex + 1]);

const base = apiBase();
const auth =
  'Basic ' +
  Buffer.from(`${requireEnv('WP_ADMIN_USER')}:${requireEnv('WP_ADMIN_APP_PASSWORD')}`).toString('base64');

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    console.error(`${name} tanımlı değil. Sunucudaki .env dosyasından yükle.`);
    process.exit(1);
  }
  return value;
}

/**
 * WordPress'in API adresi.
 *
 * Genel adres (`WP_URL`) yerine iç adres tercih ediliyor: betikler sunucunun
 * içinden çalışıyor, nginx ve TLS katmanını dolaşmalarının bir faydası yok ve
 * alt alan adının DNS'i hazır olmadan da çalışmaları gerekiyor.
 */
function apiBase() {
  const value = process.env.WP_ADMIN_API_URL || process.env.WP_URL;
  if (!value) {
    console.error('WP_ADMIN_API_URL ya da WP_URL tanımlı değil.');
    process.exit(1);
  }
  return value.replace(/\/$/, '');
}

/**
 * İç adrese giden istekler düz HTTP.
 *
 * WordPress uygulama parolalarını yalnızca SSL üzerinden kabul ediyor ve
 * 127.0.0.1'e giden istek `is_ssl()` testini geçemiyor. nginx'in üretimde
 * eklediği başlık burada elle ekleniyor; konteyner zaten yalnızca localhost'tan
 * erişilebilir olduğu için bu bir güvenlik gevşetmesi değil.
 */
const PROXY_HEADERS = { 'X-Forwarded-Proto': 'https' };

const doc = JSON.parse(await readFile(file, 'utf8'));

for (const key of ['type', 'slug', 'title', 'excerpt', 'content', 'lang']) {
  if (!doc[key]) {
    console.error(`Eksik alan: ${key}`);
    process.exit(1);
  }
}

/** İçerik tipi → REST koleksiyonu. */
const REST_BASE = { post: 'posts', city: 'cities', place: 'places', route: 'routes' };
const collection = REST_BASE[doc.type];

if (!collection) {
  console.error(`Bilinmeyen tip: ${doc.type}. Geçerli: ${Object.keys(REST_BASE).join(', ')}`);
  process.exit(1);
}

async function api(path, init = {}) {
  const response = await fetch(`${base}/wp-json${path}`, {
    ...init,
    headers: { ...PROXY_HEADERS, Authorization: auth, 'Content-Type': 'application/json', ...(init.headers ?? {}) },
  });

  if (!response.ok) {
    throw new Error(`${init.method ?? 'GET'} ${path} → ${response.status}: ${await response.text()}`);
  }

  return response.json();
}

// Aynı slug daha önce yayımlandıysa güncelle. `status=any` gerekli: taslak
// hâldeki bir kayıt varsayılan sorguda görünmüyor ve betik onun üstüne ikinci
// bir kayıt açıyordu.
const existing = await api(
  `/wp/v2/${collection}?slug=${encodeURIComponent(doc.slug)}&status=any&per_page=1`,
);

const payload = {
  slug: doc.slug,
  title: doc.title,
  excerpt: doc.excerpt,
  content: doc.content,
  status: doc.status ?? 'publish',
  ...(doc.featured_media ? { featured_media: doc.featured_media } : {}),
  // Alanlar `cs_` önekiyle kaydediliyor; JSON'da önek yazılmıyor ki şema
  // dosyasıyla birebir aynı görünsün.
  meta: Object.fromEntries(Object.entries(doc.fields ?? {}).map(([key, value]) => [`cs_${key}`, value])),
};

const record = existing.length
  ? await api(`/wp/v2/${collection}/${existing[0].id}`, { method: 'POST', body: JSON.stringify(payload) })
  : await api(`/wp/v2/${collection}`, { method: 'POST', body: JSON.stringify(payload) });

// Dil ve çeviri bağı REST üzerinden kurulamıyor (Polylang ücretsiz sürümü bu
// uçları açmıyor), bu yüzden sunucuda wp-cli ile tamamlanması gereken komut
// çıktıya yazılıyor.
const followUp = [
  `docker exec comesyriacontent-wp wp eval 'pll_set_post_language(${record.id}, "${doc.lang}");' --allow-root`,
];

if (translationOf) {
  followUp.push(
    `docker exec comesyriacontent-wp wp eval '$s = pll_get_post_translations(${translationOf}); ` +
      `$s[pll_get_post_language(${translationOf})] = ${translationOf}; $s["${doc.lang}"] = ${record.id}; ` +
      `pll_save_post_translations($s);' --allow-root`,
  );
}

console.log(
  JSON.stringify(
    {
      id: record.id,
      slug: record.slug,
      link: record.link,
      updated: existing.length > 0,
      followUp,
    },
    null,
    2,
  ),
);
