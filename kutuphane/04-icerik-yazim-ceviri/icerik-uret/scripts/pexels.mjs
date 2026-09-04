#!/usr/bin/env node
/**
 * Pexels görsel arama.
 *
 * Kullanım:
 *   node pexels.mjs "damascus old city courtyard" --count 5 [--orientation landscape]
 *
 * Çıktı: her satırda bir aday, JSON dizisi olarak. Ölçüler ve fotoğrafçı adı
 * birlikte geliyor ki seçim yaparken kaliteyi de atfı da görebilesin.
 *
 * Anahtar ortamdan okunur (PEXELS_API_KEY). Depoya yazılmaz.
 */

const API = 'https://api.pexels.com/v1/search';

function parseArgs(argv) {
  const query = argv.find((arg) => !arg.startsWith('--'));
  const flag = (name, fallback) => {
    const index = argv.indexOf(`--${name}`);
    return index === -1 ? fallback : argv[index + 1];
  };

  return {
    query,
    count: Number(flag('count', 6)),
    orientation: flag('orientation', 'landscape'),
  };
}

const { query, count, orientation } = parseArgs(process.argv.slice(2));

if (!query) {
  console.error('Kullanım: pexels.mjs "arama terimi" [--count 6] [--orientation landscape|portrait|square]');
  process.exit(1);
}

const key = process.env.PEXELS_API_KEY;
if (!key) {
  console.error('PEXELS_API_KEY tanımlı değil. Sunucudaki .env dosyasından yükle:');
  console.error('  export $(grep PEXELS_API_KEY /root/projects/comesyriacontent/.env | xargs)');
  process.exit(1);
}

const params = new URLSearchParams({
  query,
  per_page: String(Math.min(Math.max(count, 1), 30)),
  orientation,
});

const response = await fetch(`${API}?${params}`, { headers: { Authorization: key } });

if (!response.ok) {
  console.error(`Pexels ${response.status}: ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();

if (!data.photos?.length) {
  // Sessizce boş dizi dönmek yerine uyarmak önemli: aramanın sonuçsuz kaldığını
  // görmeyen bir akış, kayda yanlış bir görsel iliştirmeye çok yakın.
  console.error(`"${query}" için sonuç yok. Daha somut bir İngilizce terim dene.`);
  console.log('[]');
  process.exit(0);
}

const results = data.photos.map((photo) => ({
  id: photo.id,
  // Orijinal yerine `large2x` (~1880px): kapak görseli için fazlasıyla yeterli,
  // orijinaller 5000px'e çıkıp yüklemeyi gereksiz yavaşlatıyor.
  download: photo.src.large2x,
  width: photo.width,
  height: photo.height,
  photographer: photo.photographer,
  credit: `Fotoğraf: ${photo.photographer} / Pexels`,
  alt: photo.alt || '',
  page: photo.url,
}));

console.log(JSON.stringify(results, null, 2));
