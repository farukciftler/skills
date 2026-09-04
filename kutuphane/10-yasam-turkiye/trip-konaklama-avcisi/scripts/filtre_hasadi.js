/* Trip.com filtre kodlarini liste sayfasindan yeniden hasat eder.
 *
 * Ne zaman: references/filtre-kodlari.md eskidiginde, ya da yeni bir sehrin
 * landmark/semt id'leri gerektiginde. Trip.com bu kodlari haber vermeden degistirebilir.
 *
 * Kullanim: herhangi bir /hotels/list?... sayfasi YUKLENDIKTEN sonra calistir.
 * Once tum "Daha Fazla Goster" dugmelerini acar, sonra bolum bolum doker.
 *
 * Cikti: {bolum, ogeler:[[baslik, filterID, urlTokeni]]}
 * filterID -> token cevrimi icin references/url-grameri.md §2.
 */
(async () => {
  const bekle = (ms) => new Promise((r) => setTimeout(r, ms));

  // 1. Katlanmis filtreleri ac
  let acilan = 0;
  for (const e of document.querySelectorAll('.filter-main-items *')) {
    if (e.children.length === 0 && /^(Show More|Daha Fazla Göster)$/.test(e.textContent.trim())) {
      try { e.click(); acilan++; } catch (_) {}
    }
  }
  await bekle(900);

  // 2. Her filtre ogesinin filterID'sini React fiber'dan oku
  const fid = (el) => {
    const k = Object.keys(el).find((x) => x.startsWith('__reactFiber'));
    if (!k) return null;
    let f = el[k];
    for (let i = 0; i < 10 && f; i++) {
      const p = f.memoizedProps;
      if (p && p.item && p.item.filterID) return p.item.filterID;
      f = f.return;
    }
    return null;
  };

  // 'type|value' -> 'type~value*type*value' (TAG_ oneki ilk yarida kalir)
  const token = (id) => {
    const p = id.split('|');
    const kuyruk = p.slice(1).join('~');
    const deger = p.slice(1).map((x) => (x.startsWith('TAG_') ? x.slice(4) : x)).join('~');
    return `${p[0]}~${kuyruk}*${p[0]}*${deger}`;
  };

  const bolumler = [];
  for (const c of document.querySelectorAll('.filter-container')) {
    const baslik =
      (c.querySelector('.filter-item-title-text') || {}).innerText ||
      c.innerText.slice(0, 24);
    const ogeler = [];
    for (const l of c.querySelectorAll('label[for]')) {
      const id = fid(l);
      if (!id) continue;
      // Yildiz gibi bazi ogelerin metni bostur; for niteligi yedek etiket olur
      const baslik2 = l.textContent.trim() || `(${l.getAttribute('for')})`;
      ogeler.push([baslik2, id, token(id)]);
    }
    if (ogeler.length) bolumler.push({ bolum: baslik.trim(), ogeler });
  }

  return JSON.stringify({
    hasatZamani: new Date().toISOString(),
    sehir: new URLSearchParams(location.search).get('cityId'),
    acilanKatlanmisBolum: acilan,
    not: 'Landmark/semt ve marka listeleri SEHRE OZELDIR; digerleri sehirden bagimsizdir.',
    bolumler,
  });
})();
