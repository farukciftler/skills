#!/usr/bin/env node
/**
 * Görsel arama — çok kaynaklı, lisans süzgeçli.
 *
 * Kullanım:
 *   node gorsel-ara.mjs "Azm Palace Damascus"
 *   node gorsel-ara.mjs "Krak des Chevaliers" --count 6 --json
 *   node gorsel-ara.mjs "Umayyad Mosque" --strict umayyad
 *
 * Neden bu betik var: Pexels bu sitenin ihtiyacını karşılamıyor. Stok fotoğraf
 * bankalarında Suriye anıtlarının **yapıya özgü** karesi yok; "Bab Sharqi"
 * araması Kudüs'teki Şam Kapısı'nı döndürüyor. Oysa aynı anıtların künyeli,
 * lisanslı fotoğrafları kültürel miras arşivlerinde duruyor.
 *
 * ## Lisans kuralı — pazarlık edilemez
 *
 * Yalnızca **ticari kullanıma açık** lisanslar kabul ediliyor: CC0, kamu malı,
 * CC BY, CC BY-SA. NC (NonCommercial) ve ND (NoDerivatives) taşıyan her şey
 * reddediliyor.
 *
 * Sebebi somut: site bir markanın varlığı ve OTA tarafıyla aynı alan adını
 * paylaşıyor. NC lisanslı bir fotoğrafı burada yayımlamak hukuki risk. Bu
 * yüzden Oxford'un Manar al-Athar arşivi — Suriye için en zengin akademik
 * koleksiyon — bilinçli olarak kaynak listesinde yok: CC BY-NC-SA.
 *
 * ## Atıf zorunlu
 *
 * CC BY ve CC BY-SA atıf istiyor. Betik her sonuç için hazır bir `credit`
 * dizesi üretiyor; `wp-media.mjs --credit` ile doğrudan kullanılır ve ön yüz
 * onu galeri ile kahraman görselinin altında basıyor.
 */

const args = process.argv.slice(2);
const sorgu = args.find((a) => !a.startsWith('--'));
const jsonCikti = args.includes('--json');
const adet = args.includes('--count') ? Number(args[args.indexOf('--count') + 1]) : 6;
/** Sonucun başlığında geçmesi zorunlu terim — yanlış yapı eşleşmesini keser. */
const strict = args.includes('--strict') ? args[args.indexOf('--strict') + 1]?.toLowerCase() : null;

if (!sorgu) {
  console.error('Kullanım: gorsel-ara.mjs "arama terimi" [--count 6] [--strict terim] [--json]');
  process.exit(1);
}

const UA = 'ComeSyria/1.0 (https://comesyria.com; icerik@comesyria.com)';

/**
 * Lisans sıralaması: küçük sayı daha iyi.
 *
 * CC0 ve kamu malı en üstte çünkü atıf yükümlülüğü yok ve türev sorunu
 * çıkmıyor. CC BY-SA en altta: paylaşım-benzeri koşulu, görselde değişiklik
 * yapıldığında türevi de aynı lisansa bağlıyor.
 */
const LISANS_SIRA = {
  cc0: 0,
  pdm: 0,
  'public domain': 0,
  'by': 1,
  'by-sa': 2,
};

/** Ticari kullanıma kapalı olan her şey. */
function ticariUygun(lisans) {
  const l = (lisans || '').toLowerCase();
  if (!l) return false;
  if (l.includes('nc') || l.includes('noncommercial')) return false;
  if (l.includes('nd') || l.includes('noderiv')) return false;
  return true;
}

function lisansPuani(lisans) {
  const l = (lisans || '').toLowerCase();
  for (const [anahtar, puan] of Object.entries(LISANS_SIRA)) {
    if (l.includes(anahtar)) return puan;
  }
  return 3;
}


/**
 * Alaka puanı: sorgu sözcüklerinin kaçı başlıkta geçiyor (0–1).
 *
 * Kaba ama bu iş için yeterli — ve gerekli: kaynaklar sorguyla ilgisiz ama
 * lisansı temiz sonuçlar döndürebiliyor.
 */
function alakaPuani(baslik) {
  const b = (baslik || '').toLowerCase();
  const sozcukler = sorgu
    .toLowerCase()
    .split(/[^a-z0-9\u00c0-\u024f]+/)
    .filter((w) => w.length > 2);

  if (sozcukler.length === 0) return 1;
  const bulunan = sozcukler.filter((w) => b.includes(w)).length;

  return bulunan / sozcukler.length;
}



/** HTML etiketlerini ve fazladan boşluğu temizler — extmetadata HTML dönüyor. */
function duz(html) {
  return String(html ?? '')
    .replace(/<[^>]*>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * JSON çeker, geçici hatalarda yeniden dener.
 *
 * Yeniden deneme sonradan eklendi ve gerekliydi: aynı sorgu turdan tura farklı
 * sonuç veriyordu. Sebep, hatanın sessizce yutulup "sonuç yok" sayılmasıydı —
 * arşiv API'leri ara sıra düşüyor ve tek denemede vazgeçmek, var olan görseli
 * yok saymak anlamına geliyordu.
 *
 * Bekleme katlanarak artıyor (0.6s, 1.2s): gönüllü altyapıyı zorlamamak için.
 */
async function getJson(url, deneme = 3) {
  for (let i = 0; i < deneme; i++) {
    try {
      const response = await fetch(url, {
        headers: { 'User-Agent': UA, Accept: 'application/json' },
        signal: AbortSignal.timeout(20000),
      });
      // 4xx kalıcı: yeniden denemek boşuna. 5xx ve ağ hatası geçici.
      if (response.status >= 400 && response.status < 500) return null;
      if (!response.ok) throw new Error(String(response.status));
      return await response.json();
    } catch {
      if (i === deneme - 1) return null;
      await new Promise((r) => setTimeout(r, 600 * (i + 1)));
    }
  }
  return null;
}

// ─── Kaynak 1: Wikimedia Commons ────────────────────────────────────────────
//
// Anıt fotoğrafında en isabetli kaynak: dosyalar yapı adıyla kategorilenmiş,
// yükleyen ve lisans künyede duruyor.

async function commons(terim = sorgu) {
  const url =
    'https://commons.wikimedia.org/w/api.php?action=query&format=json&origin=*' +
    `&generator=search&gsrsearch=${encodeURIComponent(terim)}&gsrnamespace=6&gsrlimit=${adet * 2}` +
    '&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=1600';

  const d = await getJson(url);
  const sayfalar = d?.query?.pages;
  if (!sayfalar) return [];

  return Object.values(sayfalar)
    .map((p) => {
      const ii = p.imageinfo?.[0];
      if (!ii) return null;
      const m = ii.extmetadata ?? {};

      const lisans = duz(m.LicenseShortName?.value) || duz(m.License?.value);
      const yazar = duz(m.Artist?.value) || 'bilinmiyor';

      return {
        kaynak: 'commons',
        baslik: p.title.replace(/^File:/, ''),
        indirme: ii.thumburl || ii.url,
        genislik: ii.width,
        yukseklik: ii.height,
        lisans,
        yazar,
        sayfa: ii.descriptionurl,
      };
    })
    .filter(Boolean);
}

// ─── Kaynak 2: Openverse ────────────────────────────────────────────────────
//
// Commons ve Flickr'ı birlikte tarıyor; asıl katkısı Flickr'daki CC içerik.
// `license_type=commercial` süzgeci sunucu tarafında uygulanıyor.

async function openverse() {
  const url =
    'https://api.openverse.org/v1/images/' +
    `?q=${encodeURIComponent(sorgu)}&license_type=commercial&page_size=${adet}`;

  const d = await getJson(url);
  if (!d?.results) return [];

  return d.results
    // Wikimedia kopyalarını ele: Openverse onlar için tam boy orijinali veriyor
    // (12 MB'a çıkabiliyor) ve indirme kırılganlaşıyor. Aynı dosyalar Commons
    // kaynağından zaten geliyor ve orada API'nin kendi ürettiği 1600 piksellik
    // `thumburl` var. Openverse'in asıl katkısı Flickr içeriği; onu koruyoruz.
    .filter((r) => r.source !== 'wikimedia')
    .map((r) => ({
    kaynak: `openverse:${r.source}`,
    baslik: duz(r.title) || '?',
    indirme: r.url,
    genislik: r.width,
    yukseklik: r.height,
    lisans: `${r.license}${r.license_version ? '-' + r.license_version : ''}`,
    yazar: r.creator || 'bilinmiyor',
    sayfa: r.foreign_landing_url,
  }));
}

// ─── Kaynak 3: Library of Congress ──────────────────────────────────────────
//
// Kamu malı tarihî fotoğraf. 20. yüzyıl başının Ortadoğu koleksiyonları burada
// ve Suriye kapsamı iyi. Bugünkü hâli göstermiyor — arşiv niteliğinde.

async function loc() {
  const url = `https://www.loc.gov/photos/?q=${encodeURIComponent(sorgu)}&fo=json&c=${adet}`;
  const d = await getJson(url);
  if (!d?.results) return [];

  return d.results
    .map((r) => {
      const img = Array.isArray(r.image_url) ? r.image_url[r.image_url.length - 1] : r.image_url;
      if (!img) return null;
      return {
        kaynak: 'loc',
        baslik: String(r.title ?? '?'),
        indirme: img.startsWith('http') ? img : `https:${img}`,
        genislik: 0,
        yukseklik: 0,
        lisans: 'public domain',
        yazar: String(r.contributor?.[0] ?? 'Library of Congress'),
        sayfa: r.url,
        tarihsel: true,
      };
    })
    .filter(Boolean);
}

// ─── Birleştir, süz, sırala ─────────────────────────────────────────────────

/**
 * Ham sonuçları süzer ve sıralar.
 *
 * Fonksiyona alınmasının sebebi geri çekilme: eleme SONRASI boş kalıp
 * kalmadığını bilmek gerekiyor. Önce ham listeye bakmak yanıltıyordu —
 * alakasız ama var olan sonuçlar geri çekilmeyi engelliyordu ve eleme
 * hepsini düşürünce elde hiçbir şey kalmıyordu.
 */
function suzVeSirala(ham) {
  const gorulen = new Set();

  return ham
    .filter((r) => {
      if (!r.indirme || !ticariUygun(r.lisans)) return false;
      const anahtar = r.baslik.toLowerCase().replace(/\W+/g, '');
      if (gorulen.has(anahtar)) return false;
      gorulen.add(anahtar);
      if (strict && !r.baslik.toLowerCase().includes(strict)) return false;
      return true;
    })
    .map((r) => ({
      ...r,
      alaka: alakaPuani(r.baslik),
      credit: `Fotoğraf: ${r.yazar} / ${r.kaynak.startsWith('commons') ? 'Wikimedia Commons' : r.kaynak === 'loc' ? 'Library of Congress' : r.kaynak} · ${r.lisans}`,
    }))
    // Sorgu sözcüklerinden hiçbiri başlıkta yoksa o kayıt başka bir şeyin
    // fotoğrafı; göstermek yanlış yapıyı sayfaya koymak demek.
    .filter((r) => r.alaka > 0)
    .sort((a, b) => {
      // Sıra bilinçli olarak ALAKA ile başlıyor. Önce lisansa göre sıralamak,
      // kamu malı bir 19. yüzyıl gazete gravürünü anıtın gerçek fotoğrafının
      // üstüne çıkarıyordu — lisansı en iyi olan, aradığın şey değil.
      if (b.alaka !== a.alaka) return b.alaka - a.alaka;
      // Tarihsel arşiv modern fotoğrafın altında: rehber bugünü göstermeli.
      if (Boolean(a.tarihsel) !== Boolean(b.tarihsel)) return a.tarihsel ? 1 : -1;
      const l = lisansPuani(a.lisans) - lisansPuani(b.lisans);
      if (l !== 0) return l;
      return b.genislik * b.yukseklik - a.genislik * a.yukseklik;
    })
    .slice(0, adet);
}

let sonuclar = suzVeSirala((await Promise.all([commons(), openverse(), loc()])).flat());

// Geri çekilme: eleme sonrası elde bir şey kalmadıysa sorguyu kısalt.
//
// Arşivler anıtları farklı adlandırıyor — Commons'ta "Damascus Tekkiye complex"
// var ama "Tekkiye Suleymaniye Damascus" hiçbir şey bulmuyor. İlk + son sözcük
// pratikte "anıt + şehir" oluyor ve arşivlerin dosya adlandırma kalıbı bu.
const sozcukler = sorgu.trim().split(/\s+/);
if (sonuclar.length === 0 && sozcukler.length > 2) {
  const kisa = `${sozcukler[0]} ${sozcukler[sozcukler.length - 1]}`;
  sonuclar = suzVeSirala(await commons(kisa));
}

if (jsonCikti) {
  console.log(JSON.stringify(sonuclar, null, 2));
  process.exit(0);
}

if (sonuclar.length === 0) {
  console.log(`\n"${sorgu}" için ticari kullanıma açık görsel bulunamadı.`);
  console.log('Görselsiz yayımla — yanlış yapının fotoğrafı görselsiz kayıttan kötü.\n');
  process.exit(0);
}

console.log(`\n"${sorgu}" — ${sonuclar.length} sonuç (ticari kullanıma açık)\n`);
for (const [i, r] of sonuclar.entries()) {
  const boyut = r.genislik ? `${r.genislik}x${r.yukseklik}` : 'boyut bilinmiyor';
  console.log(`${i + 1}. ${r.baslik.slice(0, 66)}`);
  console.log(`   ${r.kaynak} · ${r.lisans} · ${boyut}${r.tarihsel ? ' · TARİHSEL (bugünü göstermiyor)' : ''}`);
  console.log(`   credit: ${r.credit}`);
  console.log(`   ${r.indirme.slice(0, 100)}`);
  console.log(`   sayfa : ${r.sayfa ?? '-'}\n`);
}
