# -*- coding: utf-8 -*-
"""
klip.py — Pexels stok videosunu marka klibine çevirir.

Reels gövdesi artık statik fotoğraf + Ken Burns değil, **gerçek video**dur.
Yalnızca kapanış karesi statiktir.

YAPILAN İŞLER
-------------
1. **Sessizleştirme** — Pexels lisansı klibin SES yatağını kapsamaz. Her klip
   `-an` ile sessizleştirilir; ses yalnızca kendi seslendirmemizden gelir.
2. **Normalizasyon** — her kaynak (dikey/kare/yatay, 24/25/30/60 fps) tek
   zincirle 1080×1920 · 30 fps · yuv420p · SAR 1:1 hâline gelir.
3. **Duotone** — fotoğraflardaki ile AYNI renk uçları. Stok videonun kendi
   rengi kompozisyona sızmaz; palet bozulmaz.
4. **Kırpma** — istenen saniyeden istenen süre kadar.

FFMPEG NOTLARI (bu makinede doğrulandı)
----------------------------------------
· `drawtext` YOK — metin PNG overlay ile bindirilir
· `lutrgb` VAR — duotone (gradient map) bununla yapılır
· `force_original_aspect_ratio=increase` + `crop` çifti HER kaynağı merkez-kırpar
· `setsar=1` atlanırsa concat/xfade sessizce bozulur
· `fps` FİLTRE olarak verilir (çıkış `-r` değil) — xfade CFR ister
· `settb=AVTB` xfade'in "timebase do not match" hatasının ilacı
· `format=yuv420p` zincirin SONUNDA
"""

import json
import os
import subprocess

GENISLIK = 1080
YUKSEKLIK = 1920
FPS = 30

# Duotone renk uçları — sablonlar/filtreler.svg.html ile BİREBİR aynı.
# (koyu_rgb, açık_rgb)
DUOTONE_UCLARI = {
    'petrol': ((10, 42, 54), (228, 239, 233)),    # #0A2A36 → #E4EFE9
    'gul':    ((74, 33, 41), (247, 234, 236)),    # #4A2129 → #F7EAEC
    'mavi':   ((15, 50, 62), (230, 242, 246)),    # #0F323E → #E6F2F6
    'sari':   ((56, 56, 26), (246, 245, 223)),    # #38381A → #F6F5DF
}

# BT.709 luminans ağırlıkları — SVG feColorMatrix ile aynı katsayılar.
GRI_MATRIS = ('colorchannelmixer='
              '0.2126:0.7152:0.0722:0:'
              '0.2126:0.7152:0.0722:0:'
              '0.2126:0.7152:0.0722')


def duotone_filtresi(ad):
    """
    Duotone filtre zincirini üretir (Photoshop'un Gradient Map karşılığı).

    Önce BT.709 luminansıyla gri tonlama, sonra `lutrgb` ile her parlaklık
    değerini iki renk arasında lineer eşleme:
        kanal = koyu + (açık − koyu) × val/255
    """
    if ad == 'yumusak':
        # Duotone değil: gerçek renkleri korur, doygunluğu düşürür,
        # gölgeleri kaldırır (mat film etkisi). Gerçek kurum çekimi için.
        return 'eq=saturation=0.55:contrast=0.94:brightness=0.03'

    if ad not in DUOTONE_UCLARI:
        ad = 'petrol'
    (kr, kg, kb), (ar, ag, ab) = DUOTONE_UCLARI[ad]

    lut = ("lutrgb="
           "r='%d+%d*val/255':"
           "g='%d+%d*val/255':"
           "b='%d+%d*val/255'"
           % (kr, ar - kr, kg, ag - kg, kb, ab - kb))
    return '%s,%s' % (GRI_MATRIS, lut)


def normalize_zinciri(duotone='petrol'):
    """Her kaynağı 1080×1920 · 30 fps · yuv420p hâline getiren tam zincir."""
    return ','.join([
        'scale=%d:%d:force_original_aspect_ratio=increase:flags=lanczos'
        % (GENISLIK, YUKSEKLIK),
        'crop=%d:%d' % (GENISLIK, YUKSEKLIK),
        'setsar=1',
        'fps=%d' % FPS,
        'settb=AVTB',
        duotone_filtresi(duotone),
        'format=yuv420p',           # zincirin SONUNDA
    ])


def sure_olc(yol):
    """ffprobe ile gerçek süreyi ölçer. Plandan alma — ölç."""
    cikti = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', str(yol)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(cikti or 0)


def hazirla(kaynak, cikti, sure, baslangic=0.0, duotone='petrol',
            kodlayici='libx264'):
    """
    Bir stok klibi marka klibine çevirir.

    :param sure: hedef süre (sn). Kaynak kısaysa kırpılır ve uyarı basılır.
    :param baslangic: kaynağın kaçıncı saniyesinden başlanacağı
    :param duotone: petrol · gul · mavi · sari · yumusak
    """
    gercek = sure_olc(kaynak)
    kullanilabilir = gercek - baslangic
    if kullanilabilir <= 0:
        raise ValueError('Başlangıç (%.1f sn) kaynak süresini (%.1f sn) aşıyor: %s'
                         % (baslangic, gercek, kaynak))
    if sure > kullanilabilir + 0.01:
        print('    ! %s: %.1f sn istendi, %.1f sn var — kırpıldı'
              % (os.path.basename(str(kaynak)), sure, kullanilabilir))
        sure = kullanilabilir

    komut = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-ss', '%.3f' % baslangic,
        '-i', str(kaynak),
        '-t', '%.3f' % sure,
        '-vf', normalize_zinciri(duotone),
        '-an',                       # LİSANS: stok klibin sesi kullanılamaz
    ]
    if kodlayici == 'libx264':
        komut += ['-c:v', 'libx264', '-crf', '18', '-preset', 'fast']
    else:
        komut += ['-c:v', 'h264_videotoolbox', '-b:v', '8M']
    komut += [
        '-profile:v', 'high',
        '-colorspace', 'bt709', '-color_primaries', 'bt709',
        '-color_trc', 'bt709', '-color_range', 'tv',
        '-x264-params', 'colorprim=bt709:transfer=bt709:colormatrix=bt709:range=tv',
        str(cikti),
    ]
    if kodlayici != 'libx264':
        komut = [p for p in komut if not p.startswith('colorprim=')]
        komut = [p for p in komut if p != '-x264-params']

    subprocess.run(komut, check=True, capture_output=True)

    olculen = sure_olc(cikti)
    return {'yol': str(cikti), 'sure': olculen, 'istenen': sure,
            'duotone': duotone, 'sessiz': True}


def manifest_oku(depo, kok='data/video'):
    """İndirilmiş klip manifestini okur."""
    yol = os.path.join(depo, kok, 'MANIFEST.json')
    if not os.path.exists(yol):
        return {'klipler': [], 'elenenler': []}
    with open(yol, encoding='utf-8') as f:
        return json.load(f)


def klip_bul(depo, kategori=None, sira=None, kok='data/video'):
    """
    Manifestten klip seçer.

    :param kategori: mekan · atolye · doga · malzeme
    :param sira: kategori içinde kaçıncı (0'dan). Verilmezse ilki.
    """
    manifest = manifest_oku(depo, kok)
    havuz = manifest['klipler']
    if kategori:
        havuz = [k for k in havuz if k['kategori'] == kategori]
    if not havuz:
        return None
    secim = havuz[(sira or 0) % len(havuz)]
    return os.path.join(depo, kok, secim['dosya'])
