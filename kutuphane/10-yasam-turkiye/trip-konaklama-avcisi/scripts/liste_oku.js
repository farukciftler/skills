/* Trip.com liste sayfasindan yapilandirilmis aday listesi cikarir.
 *
 * Kullanim: sayfa YUKLENDIKTEN sonra bu dosyanin icerigini tarayicida calistir
 * (javascript_tool / DevTools konsolu). JSON string doner.
 *
 * Metin kazimaz: her otel kartinin React prop'larindaki card.hotelInfo / card.roomInfo
 * nesnelerini okur. Bicim degisirse references/tarayici-okuma.md §2'ye bak.
 */
(() => {
  const CARD_SEL = '.hotel-list .list-item';

  // Kartin ICINDEKI bir dugumden basla, fiber uzerinden YUKARI yuru.
  // Kartin kok elemanindan yukari yurumek ise yaramaz: prop'lar ic dugumlerde.
  const cardOf = (item) => {
    for (const d of item.querySelectorAll('*')) {
      const k = Object.keys(d).find((x) => x.startsWith('__reactFiber'));
      if (!k) continue;
      let f = d[k];
      for (let i = 0; i < 10 && f; i++) {
        const p = f.memoizedProps;
        if (p && p.card && p.card.hotelInfo) return p.card;
        f = f.return;
      }
    }
    return null;
  };

  // "The British Museum 210 m uzaklikta" / "210m walk from ..." / "1,2 km" -> metre
  const metre = (s) => {
    if (!s) return null;
    const m = s.match(/([\d.,]+)\s*(km|kilometre|m|metre)\b/i);
    if (!m) return null;
    const ham = m[1];
    if (/^k/i.test(m[2])) {
      // km: binlik ayraci nokta, ondalik virgul olabilir
      return Math.round(parseFloat(ham.replace(/\./g, '').replace(',', '.')) * 1000);
    }
    // metre: ayraclari at, tam sayi
    return Math.round(parseFloat(ham.replace(/[.,]/g, '')));
  };

  // 4,8 km/sa = 80 m/dk. Yavaslatan kosullar icin references/mesafe-ve-konum.md §2.
  const dakika = (m) => (m == null ? null : Math.round(m / 80));

  const sayi = (s) => {
    if (s == null) return null;
    const m = String(s).replace(/[^\d.,]/g, '');
    if (!m) return null;
    // TR bicimi: 5.788 -> 5788 ; 6,3 -> 6.3
    return parseFloat(m.replace(/\./g, '').replace(',', '.'));
  };

  // Turkce nokta li I tuzagi: JS'de /i/ bayragi "Ucretsiz Iptal" icindeki U+0130'yi
  // "i" ile eslestirmez. Once aksanlari soy, sonra kucult, sonra eslestir.
  const norm = (s) =>
    String(s || '')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/\u0131/g, 'i')
      .toLowerCase();

  const etiketler = (r) => {
    const t = (r && r.roomTags) || {};
    return []
      .concat(t.advantageTags || [], t.promotionTags || [], t.discountTags || [])
      .map((x) => x && x.tagTitle)
      .filter(Boolean);
  };

  // Kaliplar norm() ciktisina (aksansiz, kucuk harf) uygulanir.
  const ORTAK = /ortak banyo|shared bath|shared facilit|ortak tuvalet|shared toilet/;
  const OZEL = /en[- ]?suite|ozel banyo|private bath|mustakil banyo/;
  const IPTAL = /ucretsiz iptal|free cancel/;

  const satirlar = [];
  for (const item of document.querySelectorAll(CARD_SEL)) {
    const c = cardOf(item);
    if (!c) continue;
    const h = c.hotelInfo || {};
    const r = (c.roomInfo || {})[0] || {};
    const pos = h.positionInfo || {};
    const koord = (pos.mapCoordinate || []).find((x) => x.coordinateType === 1) ||
                  (pos.mapCoordinate || [])[0] || {};
    const oda = (r.summary || {}).physicsName || '';
    const m = metre(pos.positionDesc);

    satirlar.push({
      id: (h.summary || {}).hotelId,
      ad: (h.nameInfo || {}).name,
      tur: (h.hotelCategory || {}).categoryName,
      yildiz: (h.hotelStar || {}).star,
      puan: sayi((h.commentInfo || {}).commentScore),
      yorumSayisi: sayi((h.commentInfo || {}).commenterNumber),
      konumMetni: pos.positionDesc || null,
      mesafeM: m,
      yurumeDk: dakika(m),
      semt: (pos.zoneNames || [])[0] || null,
      lat: koord.latitude || null,
      lon: koord.longitude || null,
      oda: oda || null,
      yatak: ((r.bedInfo || {}).contentList || [])[0] || null,
      gecelik: (r.priceInfo || {}).displayPrice || null,
      gecelikSayi: sayi((r.priceInfo || {}).displayPrice),
      toplamMetni: ((r.priceInfo || {}).priceExplanation || '').split('\n')[0] || null,
      odemeTipi: (r.payInfo || {}).payType,
      etiketler: etiketler(r),
      // Kart duzeyinde on eleme; KESIN DEGIL, detay sayfasinda dogrula:
      ucretsizIptalRozeti: etiketler(r).some((t) => IPTAL.test(norm(t))),
      banyoIpucu: ORTAK.test(norm(oda)) ? 'ORTAK' : (OZEL.test(norm(oda)) ? 'OZEL' : 'BELIRSIZ'),
      detayUrl: null, // asagida doldurulur
    });
  }

  // Detay linkleri: minimal bicim (buyuk/kucuk harf tuzagina dikkat: checkIn/checkOut)
  const q = new URLSearchParams(location.search);
  const alan = location.hostname;
  for (const s of satirlar) {
    if (!s.id) continue;
    s.detayUrl = `https://${alan}/hotels/detail/?cityId=${q.get('cityId') || ''}` +
      `&hotelId=${s.id}&checkIn=${q.get('checkin') || ''}&checkOut=${q.get('checkout') || ''}` +
      `&adult=${q.get('adult') || '2'}&children=${q.get('children') || '0'}` +
      `&crn=${q.get('crn') || '1'}&curr=${q.get('curr') || 'TRY'}`;
  }

  const govde = document.body.innerText;
  const bulunan = (govde.match(/([\d.,]+)\s*(?:konaklama yeri bulundu|properties found)/) || [])[1];
  const cipler = (() => {
    const i = govde.search(/konaklama yeri bulundu|properties found/);
    return i < 0 ? [] : govde.slice(i, i + 200).split('\n').slice(1, 9)
      .filter((x) => x && !/Filtreleri Temizle|Clear Filters|Haritada|Show on Map/.test(x));
  })();

  return JSON.stringify({
    okumaZamani: new Date().toISOString(),
    url: location.href,
    filtredenGecenToplam: bulunan || null,
    uygulananFiltreCipleri: cipler,
    okunanKartSayisi: satirlar.length,
    not: 'okunanKartSayisi < filtredenGecenToplam ise sayfa kaydirilmali (tarayici-okuma.md §3)',
    adaylar: satirlar,
  });
})();
