# -*- coding: utf-8 -*-
"""
uret.py — brif dosyasından Instagram gönderisi / hikaye / karusel üretir.

    .venv-icerik/bin/python .claude/skills/kartela-icerik/uret.py brif.json
    .venv-icerik/bin/python .claude/skills/kartela-icerik/uret.py brif.json --denetim
    .venv-icerik/bin/python .claude/skills/kartela-icerik/uret.py brif.json --zorla

AKIŞ
----
1. Brif okunur
2. **Mevzuat ve marka denetimi** (denetim.py) — engelleyici bulgu varsa DURUR
3. Karekod üretilir (segno)
4. Şablon doldurulur, Playwright ile PNG'ye çevrilir
5. Çıktı `out/sosyal/<tarih>-<slug>/` altına yazılır, yanına denetim raporu

Denetim atlanmaz. `--zorla` yalnızca engelleyiciyi uyarıya indirir ve raporda
"ZORLANDI" damgası bırakır — kurucunun bilinçli kararı olmadan kullanılmaz.
"""

import argparse
import base64
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date

BURASI = os.path.dirname(os.path.abspath(__file__))
DEPO = os.path.abspath(os.path.join(BURASI, '..', '..', '..'))
SABLONLAR = os.path.join(BURASI, 'sablonlar')

sys.path.insert(0, BURASI)
import denetim  # noqa: E402


# --- Boyutlar ---------------------------------------------------------------
BOYUTLAR = {
    'gonderi': (1080, 1350),   # 4:5 — varsayılan
    'kare': (1080, 1080),
    'hikaye': (1080, 1920),    # 9:16
}

SABLON_BOYUTU = {
    't1-soz': 'gonderi',
    't2-bilgi-kapak': 'gonderi',
    't3-bilgi-ic': 'gonderi',
    't4-duyuru': 'gonderi',
    't5-mekan': 'gonderi',
    'h1-hikaye': 'hikaye',
}


# --- Mini şablon motoru -----------------------------------------------------
# Bağımlılık eklememek için: {{anahtar}} ve <!--#if anahtar-->…<!--#endif-->
def _kosullari_coz(sablon, veri):
    """Değeri boş olan <!--#if x--> bloklarını siler, dolu olanların işaretini kaldırır."""
    desen = re.compile(
        r'<!--#if\s+([a-z_0-9]+)-->(.*?)<!--#endif-->',
        re.DOTALL,
    )

    def degistir(eslesme):
        anahtar, govde = eslesme.group(1), eslesme.group(2)
        deger = veri.get(anahtar)
        if deger is None or deger == '' or deger == []:
            return ''
        return govde

    onceki = None
    # İç içe blokları çözmek için sabit noktaya kadar tekrarla.
    while onceki != sablon:
        onceki = sablon
        sablon = desen.sub(degistir, sablon)
    return sablon


def _kacir(metin):
    """HTML'e gömülecek metni güvenli hâle getirir."""
    return (str(metin)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))


def sablonu_doldur(sablon_metni, veri):
    """Şablonu doldurur. `_ham` ile biten anahtarlar kaçırılmaz (HTML parçası)."""
    cikti = _kosullari_coz(sablon_metni, veri)

    def degistir(eslesme):
        anahtar = eslesme.group(1)
        deger = veri.get(anahtar, '')
        if deger is None:
            return ''
        # HTML parçası olan anahtarlar kaçırılmaz — aksi hâlde etiketler
        # metin olarak basılır.
        if anahtar.endswith('_ham') or anahtar in ('karekod', 'satirlar', 'foto'):
            return str(deger)
        return _kacir(deger)

    return re.sub(r'\{\{\s*([a-z_0-9]+)\s*\}\}', degistir, cikti)


# --- Karekod ----------------------------------------------------------------
def karekod_uret(icerik, hedef_png):
    """
    Karekod üretir — ÖÖK Yön. Ek m.4/2 gereği her tanıtım materyalinde zorunlu.

    Petrol renginde, yüksek hata düzeltmeli (logo/kırpma toleransı için).
    """
    import segno
    kod = segno.make(icerik, error='h')
    kod.save(hedef_png, scale=12, border=2, dark='#005f7f', light='#ffffff')
    return hedef_png


def karekod_html(png_yolu):
    """Karekodu base64 olarak gömer — render sırasında dosya yolu sorunu olmasın."""
    if not png_yolu or not os.path.exists(png_yolu):
        return ('<div class="karekod eksik">KAREKOD<br>EKSİK</div>')
    with open(png_yolu, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return '<div class="karekod"><img src="data:image/png;base64,%s" alt=""></div>' % b64


# --- Bilgi satırları --------------------------------------------------------
def satirlar_html(satirlar):
    """[[etiket, değer], …] → <div class="satir"><dt>…</dt><dd>…</dd></div>"""
    if not satirlar:
        return ''
    parcalar = []
    for satir in satirlar:
        if not isinstance(satir, (list, tuple)) or len(satir) != 2:
            continue
        parcalar.append(
            '<div class="satir"><dt>%s</dt><dd>%s</dd></div>'
            % (_kacir(satir[0]), _kacir(satir[1]))
        )
    return '\n      '.join(parcalar)


# --- Görsel -----------------------------------------------------------------
def filtreleri_enjekte(html):
    """SVG duotone/grain filtrelerini <body>'den hemen sonra ekler."""
    yol = os.path.join(SABLONLAR, 'filtreler.svg.html')
    with open(yol, encoding='utf-8') as f:
        defs = f.read()
    return html.replace('<body>', '<body>\n' + defs, 1)


# --- Fotoğraf katmanı -------------------------------------------------------
YERLESIMLER = {
    'tam': 'foto-tam',
    'alt': 'foto-alt',
    'kemer': 'foto-kemer',
    'kose': 'foto-kose',
    'yan': 'foto-yan',
}

DUOTONELAR = {
    'petrol': 'dt-petrol',
    'gul': 'dt-gul',
    'mavi': 'dt-mavi',
    'sari': 'dt-sari',
    'kartela': 'dt-kartela',
    'yumusak': 'dt-yumusak',
    'kartela': 'dt-kartela',   # tri-tone — aynı tuvalde şerit kullanma
}

# Zemin sınıfından erime rengi — .foto-alt kullanıldığında fotoğrafın üst
# kenarı bu renge erir, böylece sert dikdörtgen kenar oluşmaz.
ZEMIN_RENGI = {
    'z-beyaz': '#ffffff',
    'z-nane': '#e4efe9',
    'z-gul': '#f7eaec',
    'z-sari': '#f6f5df',
    'z-mavi': '#e6f2f6',
    'z-petrol': '#005f7f',
}


# Zemin → duotone eşlemesi.
#
# ARAŞTIRMA BULGUSU (en değerli tek kural): fotoğrafın "sayfaya yapıştırılmış
# blok" görünmesini bitiren şey kenar yumuşatmak DEĞİL, duotone'un **açık
# ucunu zemin rengiyle birebir aynı yapmaktır**. Fotoğrafın en açık pikselleri
# zeminle aynı renk olunca nerede bittiği gözle ayırt edilemez; maskeyle
# birleşince fotoğraf kâğıda basılmış gibi durur.
#
# Filtre uçları bu yüzden zemin token'larıyla birebir eşlenmiştir:
#   dt-petrol açık uç #E4EFE9 = --mint      = z-nane
#   dt-gul    açık uç #F7EAEC = --tint-rose = z-gul
#   dt-mavi   açık uç #E6F2F6 = --tint-sky  = z-mavi
#   dt-sari   açık uç #F6F5DF = --tint-yellow = z-sari
ZEMIN_DUOTONU = {
    'z-nane': 'petrol',
    'z-gul': 'gul',
    'z-mavi': 'mavi',
    'z-sari': 'sari',
    'z-beyaz': 'petrol',
    'z-petrol': 'petrol',
}


def foto_html(brif):
    """
    Fotoğraf katmanını üretir.

    Fotoğraf ASLA dikdörtgen blok olarak konmaz: her yerleşim en az iki kenardan
    taşar ya da maskeyle zemine erir (ortak.css — FOTOĞRAF KATMANI, kural 2).
    """
    kaynak = gorsel_html_yolu(brif.get('gorsel'))
    if not kaynak:
        return ''

    yerlesim = YERLESIMLER.get(brif.get('yerlesim', 'alt'), 'foto-alt')

    # Duotone verilmediyse ZEMİNDEN türetilir — açık uç zeminle aynı olur ve
    # fotoğrafın kenarı görünmez biçimde erir (yukarıdaki gerekçe).
    duotone_adi = brif.get('duotone') or ZEMIN_DUOTONU.get(
        brif.get('zemin', 'z-nane'), 'petrol')
    duotone = DUOTONELAR.get(duotone_adi, 'dt-petrol')
    grain = ' grain' if brif.get('grain', True) else ''

    siniflar = 'foto-kap %s %s%s' % (yerlesim, duotone, grain)
    parcalar = ['<div class="%s"><img src="%s" alt=""></div>' % (siniflar, kaynak)]

    # Perde — metin fotoğrafın üstündeyse okunabilirliği garanti eder.
    perde = brif.get('perde')
    if perde is None:
        perde = 'alt' if yerlesim in ('foto-tam',) else ('erime' if yerlesim == 'foto-alt' else '')

    renk = ZEMIN_RENGI.get(brif.get('zemin', 'z-nane'), '#e4efe9')

    if perde == 'alt':
        parcalar.append('<div class="perde-alt"></div>')
    elif perde == 'tam':
        parcalar.append('<div class="perde-tam"></div>')
    elif perde == 'erime':
        # Üstte zemine erir…
        parcalar.append(
            '<div class="perde-erime" style="--erime-renk:%s"></div>' % renk)
        # …altta logo ve karekodun oturduğu bandı korur.
        parcalar.append(
            '<div class="perde-altbar" style="--erime-renk:%s"></div>' % renk)

    return '\n  '.join(parcalar)


def gorsel_html_yolu(yol):
    """Görseli base64 gömer — Playwright'ın dosya erişimine bağımlı kalmayalım."""
    if not yol:
        return ''
    mutlak = yol if os.path.isabs(yol) else os.path.join(DEPO, yol)
    if not os.path.exists(mutlak):
        print('  ! Görsel bulunamadı, atlanıyor: %s' % yol)
        return ''
    uzanti = os.path.splitext(mutlak)[1].lower().lstrip('.')
    mime = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp'}.get(uzanti, 'jpeg')
    with open(mutlak, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return 'data:image/%s;base64,%s' % (mime, b64)


# --- Render -----------------------------------------------------------------
def png_uret(html_metni, hedef_png, genislik, yukseklik, olcek=2):
    """
    HTML'i PNG'ye çevirir.

    Geçici dosya `sablonlar/` içine yazılır: ortak.css ve yerel yazı tipleri
    göreli yolla çözülsün diye. Render bitince silinir.
    """
    from playwright.sync_api import sync_playwright

    gecici = tempfile.NamedTemporaryFile(
        mode='w', suffix='.html', dir=SABLONLAR, delete=False, encoding='utf-8'
    )
    try:
        gecici.write(html_metni)
        gecici.close()

        with sync_playwright() as p:
            tarayici = p.chromium.launch()
            sayfa = tarayici.new_page(
                viewport={'width': genislik, 'height': yukseklik},
                device_scale_factor=olcek,
            )
            sayfa.goto('file://' + gecici.name)
            # Yerel yazı tipleri yüklensin — font-display:block ile zaten bekler.
            sayfa.wait_for_timeout(350)
            try:
                sayfa.evaluate('document.fonts.ready')
            except Exception:
                pass
            sayfa.wait_for_timeout(150)
            sayfa.screenshot(path=hedef_png, clip={
                'x': 0, 'y': 0, 'width': genislik, 'height': yukseklik,
            })
            tarayici.close()
    finally:
        if os.path.exists(gecici.name):
            os.unlink(gecici.name)

    return hedef_png


# --- Tek kare üretimi -------------------------------------------------------
def kare_uret(brif, hedef_klasor, sira=None, karekod_png=None):
    """Bir brif sözlüğünden tek bir PNG üretir."""
    sablon_adi = brif.get('sablon', 't2-bilgi-kapak')
    sablon_yolu = os.path.join(SABLONLAR, '%s.html' % sablon_adi)
    if not os.path.exists(sablon_yolu):
        raise SystemExit('Şablon yok: %s' % sablon_yolu)

    with open(sablon_yolu, encoding='utf-8') as f:
        sablon_metni = f.read()

    boyut_adi = brif.get('boyut') or SABLON_BOYUTU.get(sablon_adi, 'gonderi')
    genislik, yukseklik = BOYUTLAR[boyut_adi]

    veri = dict(brif)
    veri['boyut'] = 'hikaye' if boyut_adi == 'hikaye' else ('kare' if boyut_adi == 'kare' else '')
    veri['zemin'] = brif.get('zemin', 'z-nane')
    veri['karekod'] = karekod_html(karekod_png) if brif.get('tanitim', True) else ''
    veri['satirlar'] = satirlar_html(brif.get('satirlar'))
    veri['foto'] = foto_html(brif)

    # Metin fotoğrafın üstünde mi duruyor? Yalnızca tam zemin ve alt taşmada
    # metin fotoğrafla örtüşür; diğer yerleşimlerde metin zeminde kalır.
    yerlesim = brif.get('yerlesim', 'alt')
    veri['uzeri'] = 'uzeri' if (brif.get('gorsel') and yerlesim == 'tam') else ''

    html = sablonu_doldur(sablon_metni, veri)
    html = filtreleri_enjekte(html)

    ad = brif.get('dosya') or ('%02d-%s' % (sira, sablon_adi) if sira is not None else sablon_adi)
    hedef = os.path.join(hedef_klasor, '%s.png' % ad)
    png_uret(html, hedef, genislik, yukseklik, olcek=brif.get('olcek', 2))
    return hedef


# --- Ana akış ---------------------------------------------------------------
def calistir(brif_yolu, yalnizca_denetim=False, zorla=False):
    with open(brif_yolu, encoding='utf-8') as f:
        brif = json.load(f)

    # Karusel mi tek kare mi?
    kareler = brif.get('kareler')
    if kareler:
        # Ortak alanlar her kareye miras geçer.
        ortak = {k: v for k, v in brif.items() if k != 'kareler'}
        birimler = []
        for kare in kareler:
            birlesik = dict(ortak)
            birlesik.update(kare)
            birimler.append(birlesik)
    else:
        birimler = [brif]

    # --- 1. DENETİM (atlanmaz)
    print('\n=== Mevzuat ve marka denetimi ===')
    tum_bulgular = []
    for i, birim in enumerate(birimler):
        bulgular = denetim.brifi_denetle(birim)
        if len(birimler) > 1:
            print('\n  --- Kare %d/%d' % (i + 1, len(birimler)))
        engel = denetim.yazdir(bulgular)
        tum_bulgular.extend(bulgular)

    ozet = denetim.ozet(tum_bulgular)
    engelleyici_var = ozet[denetim.BLOCKER] > 0

    if engelleyici_var and not zorla:
        print('\n✗ ÜRETİM DURDURULDU — %d engelleyici bulgu var.' % ozet[denetim.BLOCKER])
        print('  Metni düzeltip tekrar çalıştırın. Bilinçli bir karar veriyorsanız --zorla.')
        return 2

    if yalnizca_denetim:
        print('\n(yalnızca denetim — üretim yapılmadı)')
        return 1 if engelleyici_var else 0

    # --- 2. Çıktı klasörü
    slug = brif.get('slug') or re.sub(r'[^a-z0-9]+', '-', (brif.get('baslik') or 'icerik').lower())[:40].strip('-')
    klasor = os.path.join(DEPO, 'out', 'sosyal', '%s-%s' % (date.today().isoformat(), slug))
    os.makedirs(klasor, exist_ok=True)

    # --- 3. Karekod
    karekod_png = None
    if brif.get('karekod_dosya'):
        karekod_png = os.path.join(DEPO, brif['karekod_dosya'])
    elif brif.get('karekod_url'):
        karekod_png = karekod_uret(brif['karekod_url'], os.path.join(klasor, 'karekod.png'))
        print('\n✓ Karekod üretildi: %s' % brif['karekod_url'])

    # --- 4. Render
    print('\n=== Render ===')
    uretilenler = []
    for i, birim in enumerate(birimler):
        sira = (i + 1) if len(birimler) > 1 else None
        yol = kare_uret(birim, klasor, sira=sira, karekod_png=karekod_png)
        boyut = os.path.getsize(yol) // 1024
        print('  ✓ %s  (%d KB)' % (os.path.basename(yol), boyut))
        uretilenler.append(yol)

    # --- 5. Açıklama metni ve rapor
    if brif.get('aciklama'):
        with open(os.path.join(klasor, 'aciklama.txt'), 'w', encoding='utf-8') as f:
            f.write(brif['aciklama'].strip() + '\n')
            if brif.get('etiketler'):
                f.write('\n' + ' '.join('#' + e.lstrip('#') for e in brif['etiketler']) + '\n')

    with open(os.path.join(klasor, 'denetim-raporu.txt'), 'w', encoding='utf-8') as f:
        f.write('Kartela içerik denetim raporu\n')
        f.write('Tarih: %s\n' % date.today().isoformat())
        f.write('Brif: %s\n' % os.path.basename(brif_yolu))
        if engelleyici_var and zorla:
            f.write('\n*** ZORLANDI — engelleyici bulgulara rağmen üretildi ***\n')
        f.write('\nÖzet: %d engelleyici · %d uyarı · %d not\n\n'
                % (ozet[denetim.BLOCKER], ozet[denetim.UYARI], ozet[denetim.NOT]))
        for b in tum_bulgular:
            f.write(b.satir() + '\n\n')
        if not tum_bulgular:
            f.write('Bulgu yok.\n')

    print('\n✓ Çıktı: %s' % klasor)
    print('  %d görsel · denetim-raporu.txt%s'
          % (len(uretilenler), ' · aciklama.txt' if brif.get('aciklama') else ''))
    return 0


def main():
    ayristirici = argparse.ArgumentParser(
        description='Kartela sosyal medya içerik üretimi (gönderi · hikaye · karusel)')
    ayristirici.add_argument('brif', help='Brif JSON dosyası')
    ayristirici.add_argument('--denetim', action='store_true',
                             help='Yalnızca denetle, üretme')
    ayristirici.add_argument('--zorla', action='store_true',
                             help='Engelleyici bulgulara rağmen üret (raporda damgalanır)')
    args = ayristirici.parse_args()
    sys.exit(calistir(args.brif, args.denetim, args.zorla))


if __name__ == '__main__':
    main()
