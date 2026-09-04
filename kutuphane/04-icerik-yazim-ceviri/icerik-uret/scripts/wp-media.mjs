#!/usr/bin/env node
/**
 * Bir görseli indirip WordPress medya kitaplığına yükler.
 *
 * Kullanım:
 *   node wp-media.mjs <indirme-adresi> --alt "betimleyici metin" [--credit "Fotoğraf: ..."]
 *
 * Çıktı: { id, url } — `id` doğrudan `featured_media` ya da galeri dizisine
 * yazılabilir.
 *
 * Kimlik doğrulama WordPress uygulama parolasıyla (Application Password) yapılır;
 * yönetici parolası hiçbir yerde kullanılmaz.
 */

function flag(name, fallback = '') {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : process.argv[index + 1];
}

const source = process.argv[2];
const alt = flag('alt');
const credit = flag('credit');

if (!source || source.startsWith('--')) {
  console.error('Kullanım: wp-media.mjs <indirme-adresi> --alt "metin" [--credit "..."]');
  process.exit(1);
}

if (!alt) {
  // Uyarı değil hata: alt metni olmayan görsel hem erişilebilirliği hem de
  // görsel aramasını sessizce bozuyor, sonradan fark edilmesi zor.
  console.error('--alt zorunlu. Ekran okuyucu ve görsel araması için tek kaynak bu.');
  process.exit(1);
}

const base = apiBase();
const user = requireEnv('WP_ADMIN_USER');
const password = requireEnv('WP_ADMIN_APP_PASSWORD');

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

const auth = 'Basic ' + Buffer.from(`${user}:${password}`).toString('base64');

// 1. Kaynağı indir.
const download = await fetch(source);
if (!download.ok) {
  console.error(`Görsel indirilemedi: ${download.status}`);
  process.exit(1);
}

const bytes = Buffer.from(await download.arrayBuffer());
const type = download.headers.get('content-type') ?? 'image/jpeg';
const extension = type.includes('png') ? 'png' : type.includes('webp') ? 'webp' : 'jpg';

// Dosya adı alt metninden türetiliyor: medya kitaplığında "pexels-12345.jpg"
// yığını yerine aranabilir adlar oluşuyor ve dosya adı da bir SEO sinyali.
const name =
  alt
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[çğıöşü]/g, (ch) => ({ ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u' })[ch])
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60) || 'gorsel';

// 2. Yükle.
const upload = await fetch(`${base}/wp-json/wp/v2/media`, {
  method: 'POST',
  headers: {
    ...PROXY_HEADERS,
    Authorization: auth,
    'Content-Type': type,
    'Content-Disposition': `attachment; filename="${name}.${extension}"`,
  },
  body: bytes,
});

if (!upload.ok) {
  console.error(`Yükleme başarısız ${upload.status}: ${await upload.text()}`);
  process.exit(1);
}

const media = await upload.json();

// 3. Alt metni ve atfı yaz. Yükleme uçları bunları gövdede kabul etmiyor,
//    ayrı bir güncelleme gerekiyor.
const patch = await fetch(`${base}/wp-json/wp/v2/media/${media.id}`, {
  method: 'POST',
  headers: { ...PROXY_HEADERS, Authorization: auth, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    alt_text: alt,
    title: alt.slice(0, 100),
    ...(credit ? { meta: { cs_credit: credit } } : {}),
  }),
});

if (!patch.ok) {
  console.error(`Alt metni yazılamadı ${patch.status}: ${await patch.text()}`);
  process.exit(1);
}

console.log(JSON.stringify({ id: media.id, url: media.source_url, alt }, null, 2));
