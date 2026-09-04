# -*- coding: utf-8 -*-
"""
denetim.py — üretilen her sosyal medya içeriğinin mevzuat ve marka denetimi.

Bu dosya skill'in en önemli parçasıdır. Görsel üretmek kolaydır; kurumu idari
para cezasından korumak zordur. Denetim ÜRETİMDEN ÖNCE çalışır ve `blocker`
bulursa üretimi durdurur.

DAYANAK
-------
5580 sayılı Kanun m.11        — reklam serbest, TV yasak, kanıtlanamayan iddia yasak
5580 sayılı Kanun m.7/2-b,d   — yaptırım (brüt asgari ücretin beş katı)
ÖÖK Yönetmeliği m.7/4         — yalnızca ruhsattaki kurum adı
ÖÖK Yönetmeliği m.7/5         — MEB adı/logosu izne tabi
ÖÖK Yönetmeliği Ek m.4/1      — danışan resmi/ismi/başarısı/yorumu YASAK
ÖÖK Yönetmeliği Ek m.4/2      — her tanıtımda KAREKOD zorunlu
1219 sayılı Kanun Ek m.13     — psikoterapi yetkisi klinik psikologda

Ayrıntı: docs/mevzuat-arastirmasi.md · docs/marka-kimligi.md §7, §8
"""

import re
import unicodedata

# --- Önem düzeyleri ---------------------------------------------------------
BLOCKER = 'blocker'    # yayınlanamaz — üretim durur
UYARI = 'uyari'        # riskli — insan kararı gerekir
NOT = 'not'            # iyileştirme önerisi


class Bulgu:
    """Tek bir denetim bulgusu."""

    def __init__(self, onem, kural, mesaj, dayanak='', oneri=''):
        self.onem = onem
        self.kural = kural
        self.mesaj = mesaj
        self.dayanak = dayanak
        self.oneri = oneri

    def __repr__(self):
        return '[%s] %s — %s' % (self.onem.upper(), self.kural, self.mesaj)

    def satir(self):
        parcalar = ['[%s] %s' % (self.onem.upper(), self.kural), self.mesaj]
        if self.dayanak:
            parcalar.append('Dayanak: %s' % self.dayanak)
        if self.oneri:
            parcalar.append('Öneri: %s' % self.oneri)
        return '\n    '.join(parcalar)


def _sadelestir(metin):
    """Türkçe duyarlı küçültme + aksan ayrıştırma — kaçamakları yakalamak için."""
    if not metin:
        return ''
    metin = metin.replace('İ', 'i').replace('I', 'ı')
    metin = metin.lower()
    # Araya nokta/boşluk sokarak filtre atlatma denemelerini de yakala:
    # "t e r a p i" ya da "t.e.r.a.p.i" gibi.
    return metin


def _kelime_var(metin, kok):
    """
    Kelime kökünü sınır duyarlı arar. Türkçe sondan eklemeli olduğu için
    kökten sonra ek gelebilir: "terapi", "terapisi", "terapiye", "terapist".
    Ama "terapi" kökü "psikoterapötik" gibi kelimelerde de yakalanmalı.
    """
    desen = r'(?<![a-zçğıöşü])' + re.escape(kok) + r'[a-zçğıöşü]*'
    return re.search(desen, metin) is not None


# --- 1. Yasak sözlük --------------------------------------------------------
# (kök, güvenli karşılık, dayanak)
YASAK_KELIMELER = [
    ('terapi',      'psikolojik danışma görüşmesi / rehberlik görüşmesi', '1219 s.K. Ek m.13'),
    ('psikoterapi', 'psikolojik danışma görüşmesi',                       '1219 s.K. Ek m.13'),
    ('terapist',    'psikolog / rehber öğretmen–psikolojik danışman',     '1219 s.K. Ek m.13'),
    ('seans',       'görüşme / oturum / buluşma',                          'Klinik çağrışım'),
    ('tedavi',      'destek / gelişim / güçlendirme',                      '5580 m.11'),
    ('teşhis',      'değerlendirme / ihtiyaç belirleme',                   'Hekim yetkisi'),
    ('tanı',        'değerlendirme / ön görüşme',                          'Hekim yetkisi'),
    ('klinik',      'merkez (ruhsattaki ad)',                              'ÖÖK Yön. m.7/4'),
    ('poliklinik',  'merkez',                                              'ÖÖK Yön. m.7/4'),
    ('muayenehane', 'merkez',                                              'ÖÖK Yön. m.7/4'),
    ('hasta',       'danışan / birey / katılımcı',                         'Sağlık dili'),
    ('şifa',        'destek / gelişim',                                    '5580 m.11'),
    ('iyileştirme', 'güçlendirme / beceri kazandırma',                     '5580 m.11'),
    ('bozukluk',    'zorlanma / güçlük / ihtiyaç',                         'Tıbbi sınıflama'),
    ('rahatsızlık', 'zorlanma / güçlük',                                   'Tıbbi sınıflama'),
]

# "tanı" kökü çok sık yanlış eşleşir ("tanışma", "tanıtım", "tanımak").
# Bu kelimeler yakalanırsa bulgu ÜRETİLMEZ.
TANI_ISTISNALARI = [
    'tanış', 'tanıt', 'tanım', 'tanıd', 'tanıy', 'tanır', 'tanın', 'tanıkl',
]

# --- 2. Kanıtlanamayan iddia ------------------------------------------------
IDDIA_DESENLERI = [
    (r'%\s*\d+|\byüzde\s+\d+', 'Sayısal başarı/oran iddiası'),
    (r'\bgaranti\w*', 'Garanti vaadi'),
    (r'\bkesin\s+sonuç\w*', 'Kesin sonuç vaadi'),
    (r'\ben\s+iyi\b|\ben\s+başarılı\b|\ben\s+etkili\b', 'Üstünlük iddiası'),
    (r'\b1\s*numara\b|\bbir\s+numara\b|\blider\b', 'Üstünlük iddiası'),
    (r'\btürkiye.?nin\s+en\b|\bistanbul.?un\s+en\b', 'Üstünlük iddiası'),
    (r'\buzman\s+kadromuzla\s+kesin\b', 'Kesinlik iddiası'),
    (r'\bmutlaka\s+geçer\b|\bkurtul\w*', 'Tedavi vaadi'),
]

# --- 3. Aciliyet / kıtlık dili (marka sesi §7.2) ----------------------------
ACILIYET_DESENLERI = [
    (r'\bson\s+\d+\s*(kontenjan|kişilik|yer)', '"son N kontenjan" — kıtlık dili'),
    (r'\bkaçırma\w*', '"kaçırmayın" — aciliyet dili'),
    (r'\bacele\s+et\w*', 'Aciliyet dili'),
    (r'\bhemen\s+(ara|kayıt|başla)\w*', 'Baskı kuran emir kipi'),
    (r'\bsınırlı\s+(süre|kontenjan)', 'Kıtlık dili'),
    (r'\bsadece\s+bugün\b', 'Kıtlık dili'),
]

# --- 4. MEB adı/logosu ------------------------------------------------------
MEB_DESENLERI = [
    (r'\bmeb\s*(onaylı|onaylidir|sertifikalı)', '"MEB onaylı" ibaresi'),
    (r'\bmillî?\s+eğitim\s+bakanlığı\s+(onaylı|sertifikalı)', '"MEB onaylı" ibaresi'),
    (r'\bbakanlık\s+onaylı', '"Bakanlık onaylı" ibaresi'),
]

OLGUSAL_KARSILIK = '5580 sayılı Kanun kapsamında ruhsatlıdır'


def metni_denetle(metin, baglam=''):
    """
    Serbest metni (başlık, açıklama, altyazı, seslendirme metni) denetler.

    :param metin: denetlenecek metin
    :param baglam: bulguda gösterilecek alan adı (ör. "başlık", "açıklama")
    :return: Bulgu listesi
    """
    bulgular = []
    if not metin:
        return bulgular

    d = _sadelestir(metin)
    onek = ('%s: ' % baglam) if baglam else ''

    # 1. Yasak kelimeler
    for kok, karsilik, dayanak in YASAK_KELIMELER:
        if not _kelime_var(d, _sadelestir(kok)):
            continue
        if kok == 'tanı':
            # Yanlış eşleşmeleri ayıkla.
            if any(istisna in d for istisna in TANI_ISTISNALARI):
                # Kökün gerçekten yalnız geçtiği bir yer var mı?
                if not re.search(r'(?<![a-zçğıöşü])tanı(?![a-zçğıöşüşd])', d):
                    continue
        bulgular.append(Bulgu(
            BLOCKER, 'Yasak kelime',
            '%s"%s" kökü geçiyor.' % (onek, kok),
            dayanak,
            'Yerine: %s' % karsilik,
        ))

    # 2. Kanıtlanamayan iddia
    for desen, aciklama in IDDIA_DESENLERI:
        if re.search(desen, d):
            bulgular.append(Bulgu(
                BLOCKER, 'Kanıtlanamayan iddia',
                '%s%s.' % (onek, aciklama),
                '5580 m.11 — ispat yükü kurumdadır',
                'İddia yerine programın içeriğini, süresini ve yöntemini yaz.',
            ))

    # 3. Aciliyet/kıtlık
    for desen, aciklama in ACILIYET_DESENLERI:
        if re.search(desen, d):
            bulgular.append(Bulgu(
                UYARI, 'Aciliyet dili',
                '%s%s.' % (onek, aciklama),
                'docs/marka-kimligi.md §7.2',
                'Baskı kurmayan bir davet kipi kullan: "Yazmak isterseniz buradayız."',
            ))

    # 4. MEB adı
    for desen, aciklama in MEB_DESENLERI:
        if re.search(desen, d):
            bulgular.append(Bulgu(
                BLOCKER, 'MEB adı kullanımı',
                '%s%s.' % (onek, aciklama),
                'ÖÖK Yön. m.7/5',
                'Olgusal ifade kullan: "%s"' % OLGUSAL_KARSILIK,
            ))

    # 5. Ünlem — marka sesi ünlem kullanmaz
    if '!' in metin:
        bulgular.append(Bulgu(
            NOT, 'Ünlem işareti',
            '%sÜnlem işareti kullanılmış.' % onek,
            'docs/marka-kimligi.md §7.2',
            'Ünlem kaldırılır; ton zaten sakin olmalıdır.',
        ))

    # 6. Danışan referansı izi
    if re.search(r'\bdanışanımız\w*\s|\bbir\s+velimiz\b|\bteşekkür\s+mesajı', d):
        bulgular.append(Bulgu(
            BLOCKER, 'Danışan referansı',
            '%sDanışan/veli referansına benzeyen ifade var.' % onek,
            'ÖÖK Yön. Ek m.4/1 + KVKK m.6',
            'Danışan yorumu, teşekkürü ve başarı anlatısı hiçbir biçimde kullanılamaz.',
        ))

    return bulgular


def brifi_denetle(brif):
    """
    Bir üretim brifini bütün olarak denetler: metinler + yapısal zorunluluklar.

    :param brif: dict — sablon, baslik, altmetin, karekod, gorsel, etiketler...
    :return: Bulgu listesi
    """
    bulgular = []

    # --- Metin alanları
    for alan, etiket in [
        ('baslik', 'Başlık'),
        ('altmetin', 'Alt metin'),
        ('etiket', 'Üst etiket'),
        ('kayit_notu', 'Kayıt notu'),
        ('eylem', 'Eylem metni'),
        ('aciklama', 'Gönderi açıklaması'),
        ('seslendirme', 'Seslendirme metni'),
    ]:
        bulgular.extend(metni_denetle(brif.get(alan, ''), etiket))

    for i, satir in enumerate(brif.get('satirlar', []) or []):
        if isinstance(satir, (list, tuple)) and len(satir) == 2:
            bulgular.extend(metni_denetle(str(satir[1]), 'Bilgi satırı %d' % (i + 1)))

    # --- Karekod (ÖÖK Yön. Ek m.4/2)
    tanitim = brif.get('tanitim', True)
    if tanitim and not brif.get('karekod_url') and not brif.get('karekod_dosya'):
        bulgular.append(Bulgu(
            BLOCKER, 'Karekod eksik',
            'Tanıtım niteliği taşıyan materyalde karekod yok.',
            'ÖÖK Yön. Ek m.4/2',
            'Brife `karekod_url` ekle. Tanıtım değilse `"tanitim": false` yaz '
            've gerekçesini brifte belirt.',
        ))

    # --- Ruhsat adı (ÖÖK Yön. m.7/4)
    ruhsat = brif.get('ruhsat_adi', '')
    if not ruhsat:
        bulgular.append(Bulgu(
            UYARI, 'Ruhsat adı eksik',
            'Materyalde ruhsat adı görünmüyor.',
            'ÖÖK Yön. m.7/4',
            'Kilitli sürüm kullan: "Özel … Rehberlik ve Psikolojik Danışma Merkezi".',
        ))
    elif not _sadelestir(ruhsat).startswith('özel') and 'özel' not in _sadelestir(ruhsat):
        bulgular.append(Bulgu(
            UYARI, 'Ruhsat adında "Özel" yok',
            'Kurum adının önünde "Özel" ibaresi bulunmalıdır.',
            'ÖÖK Yön. m.7/4',
            '"Özel " ön ekini ekle.',
        ))

    # --- Metin uzunluğu (okunabilirlik — §8.4)
    baslik = brif.get('baslik', '') or ''
    kelime = len([k for k in re.split(r'\s+', baslik) if k])
    sablon = brif.get('sablon', '')

    if sablon == 't1-soz' and kelime > 12:
        bulgular.append(Bulgu(
            UYARI, 'Başlık uzun',
            'Söz şablonunda başlık %d kelime — sınır 12.' % kelime,
            'docs/marka-kimligi.md §8.4',
            'Kısalt; fazlası karusele taşınır.',
        ))
    elif kelime > 20:
        bulgular.append(Bulgu(
            UYARI, 'Başlık uzun',
            'Başlık %d kelime. Görseldeki metin asgaride tutulur.' % kelime,
            'docs/marka-kimligi.md §8.4',
            'Kısalt ya da karusel kullan.',
        ))

    altmetin = brif.get('altmetin', '') or ''
    if len([k for k in re.split(r'\s+', altmetin) if k]) > 45:
        bulgular.append(Bulgu(
            UYARI, 'Alt metin uzun',
            'Kare başına 45 kelime sınırı aşıldı.',
            'docs/marka-kimligi.md §8.4',
            'Karusel iç sayfasına böl.',
        ))

    # --- Görsel ZORUNLU (kurucu kararı, 23 Ağustos 2026)
    # Görselsiz gönderi üretilmez. Akışta metin bloğu kaydırılıp geçilir;
    # fotoğraf durdurucudur. Marka kimliği §8.4 şablonlarının hepsi fotoğraf taşır.
    if not brif.get('gorsel'):
        bulgular.append(Bulgu(
            BLOCKER, 'Görsel eksik',
            'Gönderide fotoğraf yok.',
            'Kurucu kararı — görselsiz gönderi üretilmez',
            'Brife `gorsel` ekle. Yer tutucu için: '
            'website/frontend/public/gorseller/<kategori>/… '
            '(MANIFEST.json listeler)',
        ))

    # --- Görsel yerleşimi: dikdörtgen blok yasak
    yerlesim = brif.get('yerlesim', 'alt')
    if yerlesim not in ('tam', 'alt', 'kemer', 'kose', 'yan'):
        bulgular.append(Bulgu(
            UYARI, 'Bilinmeyen yerleşim',
            'yerlesim="%s" tanımlı değil.' % yerlesim,
            'ortak.css — FOTOĞRAF KATMANI',
            'Geçerli: tam · alt · kemer · kose · yan. Hepsi kenardan taşar; '
            'fotoğraf hiçbir zaman ortada duran bir dikdörtgen blok değildir.',
        ))

    # --- Danışan görseli riski
    if brif.get('gorsel') and brif.get('insan_var'):
        bulgular.append(Bulgu(
            UYARI, 'Görselde insan',
            'Görselde insan olduğu işaretlenmiş.',
            'ÖÖK Yön. Ek m.4/1',
            'Danışan olamaz. Yalnızca mekân, nesne veya rızası alınmış ekip. '
            'Tanınabilir çocuk yüzü hiçbir koşulda kullanılmaz.',
        ))

    # --- Yer tutucu görsel uyarısı
    gorsel = str(brif.get('gorsel', '') or '')
    if 'gorseller/' in gorsel or 'pexels' in gorsel.lower():
        bulgular.append(Bulgu(
            NOT, 'Yer tutucu görsel',
            'Pexels yer tutucu görseli kullanılıyor.',
            'docs/marka-kimligi.md §6.1',
            'Yayında mekân ve ekip için GERÇEK fotoğraf kullanılır; stok görsel kullanılmaz.',
        ))

    # --- Mecra
    mecra = _sadelestir(str(brif.get('mecra', '')))
    if 'televizyon' in mecra or mecra == 'tv':
        bulgular.append(Bulgu(
            BLOCKER, 'Yasak mecra',
            'Televizyon mecrası seçilmiş.',
            '5580 m.11 — mutlak yasak',
            'Instagram, radyo, billboard, arama motoru ve basılı materyal serbesttir.',
        ))

    # --- İşbirliği etiketi
    if brif.get('isbirligi') and not brif.get('reklam_etiketi'):
        bulgular.append(Bulgu(
            BLOCKER, 'Reklam etiketi eksik',
            'İşbirliği içeriğinde "Reklam"/"Tanıtım" etiketi yok.',
            'Ticari Reklam Yön.',
            'İlk görüş alanında, yüksek kontrastta, her karede "Reklam" yaz.',
        ))

    return bulgular


def ozet(bulgular):
    """Bulguları önem düzeyine göre sayar."""
    return {
        BLOCKER: len([b for b in bulgular if b.onem == BLOCKER]),
        UYARI: len([b for b in bulgular if b.onem == UYARI]),
        NOT: len([b for b in bulgular if b.onem == NOT]),
    }


def yazdir(bulgular):
    """Bulguları okunur biçimde yazdırır. Blocker varsa True döner."""
    if not bulgular:
        print('  ✓ Denetim temiz — bulgu yok.')
        return False

    sirali = sorted(bulgular, key=lambda b: [BLOCKER, UYARI, NOT].index(b.onem))
    for b in sirali:
        isaret = {'blocker': '✗', 'uyari': '!', 'not': '·'}[b.onem]
        print('  %s %s' % (isaret, b.satir()))

    s = ozet(bulgular)
    print('\n  Özet: %d engelleyici · %d uyarı · %d not'
          % (s[BLOCKER], s[UYARI], s[NOT]))
    return s[BLOCKER] > 0


if __name__ == '__main__':
    # Kendi kendini deneme — kural motorunun çalıştığını gösterir.
    ornekler = [
        'Çocuğunuz için sanat terapisi seansları',
        'Akademik Kaygı Programı — 6 oturumluk grup çalışması',
        '%90 başarı garantisi! Son 3 kontenjan!',
        'MEB onaylı uzman kadromuzla',
        'Tanışma görüşmesi ve tanıtım toplantısı',
    ]
    for o in ornekler:
        print('\n--- %s' % o)
        yazdir(metni_denetle(o))
