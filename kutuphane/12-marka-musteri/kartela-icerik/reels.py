# -*- coding: utf-8 -*-
"""
reels.py — brif dosyasından Instagram Reels üretir.

    .venv-icerik/bin/python .claude/skills/kartela-icerik/reels.py brif.json

YAPI (kurucu kararı, 23 Ağustos 2026)
--------------------------------------
**Gövde gerçek videodur** — Pexels'ten inen dikey stok klipleri, markanın
duotone'uyla işlenmiş ve sessizleştirilmiş hâlde.
**Yalnızca kapanış karesi statiktir** — marka şablonuyla render edilen, logo,
tam ruhsat adı, karekod ve çağrı taşıyan kart.

Mesaj **yakılmış altyazıyla** taşınır; video kliplerinin üzerine başlık metni
basılmaz. Instagram videoları sessiz izlenir, altyazı zaten zorunludur —
ikinci bir metin katmanı görüntüyü kalabalıklaştırır.

AKIŞ
----
1. Brif okunur, **mevzuat denetiminden geçirilir** (engelleyici varsa durur)
2. Stok klipler işlenir: 1080×1920 · 30 fps · duotone · SESSİZ
3. Kapanış karesi marka şablonuyla PNG olarak render edilir → klibe çevrilir
4. Klipler yumuşak geçişle birleştirilir
5. Türkçe seslendirme üretilir
6. Ses bindirilir (seslendirme uzunsa kapanış karesi donar), altyazı yakılır
7. `dogrula` + güvenli alan + döngü kontrol dosyaları
"""

import argparse
import json
import os
import sys
from datetime import date

BURASI = os.path.dirname(os.path.abspath(__file__))
DEPO = os.path.abspath(os.path.join(BURASI, '..', '..', '..'))

sys.path.insert(0, BURASI)
sys.path.insert(0, DEPO)

import denetim              # noqa: E402
import klip as klip_modulu  # noqa: E402
import uret                 # noqa: E402
from src.icerik import muzik as muzik_modulu, seslendirme, video   # noqa: E402


GECIS_SURE = 0.5          # marka kuralı: 0,4–0,6 sn
KLIP_SURESI = 5.0
KAPANIS_SURESI = 4.0


def _tohum(metin):
    """
    Slug'dan kararlı bir tohum üretir.

    Aynı içerik her zaman aynı müziği alsın diye — yeniden üretildiğinde
    müzik değişmez. Python'un `hash()`'i süreçler arası kararsızdır (PYTHONHASHSEED),
    bu yüzden FNV-1a kullanılıyor.
    """
    karma = 0x811c9dc5
    for karakter in str(metin):
        karma ^= ord(karakter)
        karma = (karma * 0x01000193) & 0xFFFFFFFF
    return karma % 10000


def muzik_hazirla(brif, sure, klasor):
    """
    Arka plan müziğini hazırlar.

    Brifteki `muzik` alanı:
      · yok / true  → prosedürel üretim, tohum slug'dan türetilir
      · false       → müziksiz
      · "yol/x.wav" → hazır dosya (telifi AYRICA denetlenmeli)
      · {…}         → prosedürel, ayarlar elle verilir

    Prosedürel üretim varsayılandır: üçüncü taraf hakkı yoktur, telif denetimi
    gerektirmez ve aynı brif her zaman aynı müziği verir.
    """
    ayar = brif.get('muzik', True)

    if ayar is False:
        return None, None

    if isinstance(ayar, str):
        yol = ayar if os.path.isabs(ayar) else os.path.join(DEPO, ayar)
        if not os.path.exists(yol):
            print('  ! müzik dosyası bulunamadı: %s — müziksiz devam' % ayar)
            return None, None
        print('  ! hazır müzik dosyası kullanılıyor — TELİF DURUMU AYRICA '
              'DENETLENMELİDİR (modül lisans kontrolü yapmaz)')
        return yol, {'kaynak': 'hazır dosya', 'telif': 'denetlenmedi'}

    secenekler = ayar if isinstance(ayar, dict) else {}
    tohum = secenekler.get('tohum', _tohum(brif.get('slug', 'kartela')))

    hedef = os.path.join(klasor, 'fon-muzik.wav')
    bilgi = muzik_modulu.uret(
        sure=sure + 0.5,                      # birleştirme payı
        cikti_yolu=hedef,
        tohum=tohum,
        kok=secenekler.get('kok', 'D2'),
        mod=secenekler.get('mod', 'dor'),
        akor_suresi=float(secenekler.get('akor_suresi', 10.0)),
    )
    return hedef, bilgi


def calistir(brif_yolu, zorla=False):
    with open(brif_yolu, encoding='utf-8') as f:
        brif = json.load(f)

    klipler_brifi = brif.get('klipler') or []
    kapanis = brif.get('kapanis')

    if not klipler_brifi:
        print('✗ Brifte `klipler` yok. Reels gövdesi video kliplerinden kurulur.')
        return 2

    # --- 1. Denetim
    print('\n=== Mevzuat ve marka denetimi ===')
    tum = []

    if not kapanis:
        tum.append(denetim.Bulgu(
            denetim.BLOCKER, 'Kapanış karesi yok',
            'Reels\'te kapanış karesi bulunmuyor.',
            'ÖÖK Yön. Ek m.4/2 + m.7/4',
            'Karekod ve ruhsat adı kapanış karesinde taşınır; olmadan '
            'tanıtım materyali eksiktir. Brife `kapanis` ekle.',
        ))
        denetim.yazdir([tum[-1]])
    else:
        kapanis_brifi = dict(kapanis)
        kapanis_brifi.setdefault('ruhsat_adi', brif.get('ruhsat_adi', ''))
        kapanis_brifi.setdefault('karekod_url', brif.get('karekod_url', ''))
        kapanis_brifi.setdefault('sablon', 'h1-hikaye')
        kapanis_brifi['boyut'] = 'hikaye'
        print('\n  --- Kapanış karesi')
        b = denetim.brifi_denetle(kapanis_brifi)
        denetim.yazdir(b)
        tum.extend(b)

    seslendirme_metni = brif.get('seslendirme', '')
    if seslendirme_metni:
        print('\n  --- Seslendirme metni')
        s_b = denetim.metni_denetle(seslendirme_metni, 'Seslendirme')
        denetim.yazdir(s_b)
        tum.extend(s_b)
    else:
        print('\n  ! Seslendirme metni yok — sessiz ve altyazısız Reels.')

    ozet = denetim.ozet(tum)
    if ozet[denetim.BLOCKER] > 0 and not zorla:
        print('\n✗ ÜRETİM DURDURULDU — %d engelleyici bulgu.' % ozet[denetim.BLOCKER])
        return 2

    # --- 2. Klasörler
    slug = brif.get('slug', 'reels')
    klasor = os.path.join(DEPO, 'out', 'sosyal',
                          '%s-%s-reels' % (date.today().isoformat(), slug))
    calisma = os.path.join(klasor, 'calisma')
    os.makedirs(calisma, exist_ok=True)

    # --- 3. Karekod
    karekod_png = None
    if brif.get('karekod_url'):
        karekod_png = uret.karekod_uret(
            brif['karekod_url'], os.path.join(klasor, 'karekod.png'))
        print('\n✓ Karekod üretildi')

    # --- 4. Gövde: stok klipler → marka klipleri
    print('\n=== Gövde (Pexels video → duotone, sessiz) ===')
    parcalar = []
    kunye = []
    manifest = klip_modulu.manifest_oku(DEPO)

    for i, k in enumerate(klipler_brifi):
        kaynak = k.get('dosya')
        if kaynak:
            kaynak = os.path.join(DEPO, kaynak)
        else:
            kaynak = klip_modulu.klip_bul(DEPO, k.get('kategori'), k.get('sira', i))
        if not kaynak or not os.path.exists(kaynak):
            print('  ! klip bulunamadı (kategori=%s sira=%s) — atlanıyor'
                  % (k.get('kategori'), k.get('sira')))
            continue

        hedef = os.path.join(calisma, 'govde-%02d.mp4' % (i + 1))
        bilgi = klip_modulu.hazirla(
            kaynak, hedef,
            sure=float(k.get('sure', KLIP_SURESI)),
            baslangic=float(k.get('baslangic', 0)),
            duotone=k.get('duotone', 'petrol'))
        print('  ✓ govde-%02d.mp4  %.1f sn  duotone=%s  %s'
              % (i + 1, bilgi['sure'], bilgi['duotone'], os.path.basename(kaynak)))
        parcalar.append(hedef)

        # Künye — Pexels lisansı atıf istemez ama kaydını tutuyoruz.
        for kayit in manifest.get('klipler', []):
            if os.path.basename(kayit['dosya']) == os.path.basename(kaynak):
                kunye.append(kayit)
                break

    if not parcalar:
        print('\n✗ Hiç klip hazırlanamadı. `python3 src/gorsel/video_indir.py` çalıştırın.')
        return 2

    # --- 5. Kapanış karesi: statik marka kartı
    if kapanis:
        print('\n=== Kapanış karesi (statik marka kartı) ===')
        kapanis_brifi['dosya'] = 'kapanis'
        png = uret.kare_uret(kapanis_brifi, calisma, karekod_png=karekod_png)
        print('  ✓ %s' % os.path.basename(png))

        kapanis_klip = os.path.join(calisma, 'kapanis.mp4')
        video.kare_klip(png, float(kapanis.get('sure', KAPANIS_SURESI)), kapanis_klip)
        print('  ✓ kapanis.mp4  %.1f sn' % float(kapanis.get('sure', KAPANIS_SURESI)))
        parcalar.append(kapanis_klip)

    # --- 6. Birleştir
    print('\n=== Birleştirme ===')
    birlesik = os.path.join(calisma, 'birlesik.mp4')
    bilgi = video.birlestir(parcalar, birlesik, gecis_sure=GECIS_SURE)
    print('  ✓ %.2f sn (%d parça)' % (bilgi.get('sure', 0), len(parcalar)))

    son = birlesik

    # --- 7. Seslendirme + altyazı
    if seslendirme_metni:
        print('\n=== Seslendirme ===')
        wav = os.path.join(calisma, 'anlatim.wav')
        ses_bilgi = seslendirme.seslendir(
            seslendirme_metni, wav,
            ses=brif.get('ses', 'tr-TR-EmelNeural'),
            hiz=brif.get('hiz', '+0%'))
        print('  ✓ %s · %.2f sn%s' % (
            ses_bilgi.get('motor', '?'), ses_bilgi.get('sure', 0),
            '' if not ses_bilgi.get('tahmini') else '  (zamanlama TAHMİNİ)'))

        # Seslendirme videodan KISA ise video kesilmemeli — kapanış karesinin
        # sessizce ekranda kalması istenen davranıştır (izleyici karekodu
        # okusun diye). Bu yüzden ses, video uzunluğuna kadar sessizlikle
        # doldurulur. Altyazı zamanlamaları sonda pad edildiği için bozulmaz.
        video_suresi = klip_modulu.sure_olc(son)
        ses_suresi = float(ses_bilgi.get('sure', 0))
        if video_suresi > ses_suresi + 0.05:
            import subprocess
            dolgulu = os.path.join(calisma, 'anlatim-dolgulu.wav')
            subprocess.run([
                'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                '-i', wav,
                '-af', 'apad=whole_dur=%.3f' % video_suresi,
                '-ar', '48000', '-ac', '1', dolgulu,
            ], check=True, capture_output=True)
            print('  ✓ ses %.2f → %.2f sn sessizlikle dolduruldu '
                  '(kapanış karesi ekranda kalsın)' % (ses_suresi, video_suresi))
            wav_bindirilecek = dolgulu
        else:
            wav_bindirilecek = wav

        # --- Arka plan müziği (prosedürel)
        print('\n=== Arka plan müziği ===')
        muzik_yolu, muzik_bilgi = muzik_hazirla(brif, video_suresi, calisma)
        if muzik_bilgi and muzik_bilgi.get('kaynak') != 'hazır dosya':
            print('  ✓ prosedürel · %s/%s · tohum=%d · akor %.0f sn'
                  % (muzik_bilgi['kok'], muzik_bilgi['mod'],
                     muzik_bilgi['tohum'], muzik_bilgi['akor_suresi']))
            print('    telif: üçüncü taraf hakkı yok · seviye %.0f dB'
                  % float(brif.get('muzik_seviye', -18.0)))
        elif not muzik_yolu:
            print('  (müziksiz)')

        # Müzik seviyesi: modül varsayılanı −24 dB, konuşmanın 22 dB altına
        # düşürüyordu — telefon hoparlöründe duyulmuyor. Prosedürel müziğimiz
        # zaten konuşma bandından oyulmuş ve vurmalı içermiyor, bu yüzden
        # biraz yukarıda durabilir. −18 dB ≈ konuşmanın 17 dB altı: fark
        # edilir bir yatak, ama ünsüzleri örtmez. Brifte `muzik_seviye` ile
        # değiştirilebilir (dinleyerek ayarlanacak bir değerdir).
        seviye = float(brif.get('muzik_seviye', -18.0))

        sesli = os.path.join(calisma, 'sesli.mp4')
        video.ses_bindir(son, wav_bindirilecek, sesli, muzik=muzik_yolu,
                         muzik_seviye=seviye, video_uzat=True)
        son = sesli

        print('\n=== Altyazı (yakılmış) ===')
        altyazili = os.path.join(calisma, 'altyazili.mp4')
        video.altyazi_bindir(son, wav + '.json', altyazili)
        son = altyazili
        print('  ✓ bindirildi')

    # --- 8. Son dosya + doğrulama
    hedef = os.path.join(klasor, '%s-reels.mp4' % slug)
    os.replace(son, hedef)

    print('\n=== Doğrulama ===')
    rapor = video.dogrula(hedef)
    for anahtar in ('genislik', 'yukseklik', 'fps', 'sure', 'ses_var', 'uygun'):
        if anahtar in rapor:
            print('  %-10s %s' % (anahtar, rapor[anahtar]))
    for uyari in rapor.get('uyarilar', []):
        print('  ! %s' % uyari)

    # --- 9. Kontrol dosyaları (atılacak — yayınlanmaz)
    print('\n=== Kontrol dosyaları ===')
    try:
        video.guvenli_alan(hedef, os.path.join(klasor, 'kontrol-guvenli-alan.mp4'))
        video.dongu_kontrol(hedef, os.path.join(klasor, 'kontrol-dongu.mp4'))
        print('  ✓ kontrol-guvenli-alan.mp4 · kontrol-dongu.mp4')
    except Exception as hata:
        print('  ! kontrol dosyaları üretilemedi: %s' % hata)

    # --- 10. Künye ve rapor
    with open(os.path.join(klasor, 'KUNYE.md'), 'w', encoding='utf-8') as f:
        f.write('# Kullanılan stok klipler\n\n')
        f.write('Pexels Lisansı — atıf zorunlu değildir, kayıt için tutulur.\n\n')
        for k in kunye:
            f.write('- **%s** · %s · [Pexels](%s)\n'
                    % (os.path.basename(k['dosya']), k.get('fotografci', '—'),
                       k.get('pexels_url', '')))
        f.write('\n## Pexels Lisansının KAPSAMADIKLARI\n\n')
        f.write('- **Klibin ses yatağı lisanslı değildir** — bu üretimde tüm '
                'klipler sessizleştirildi; ses yalnızca kendi seslendirmemizdir.\n')
        f.write('- Tanınabilir kişiler için model izni garanti edilmez.\n')
        f.write('- Kadrajdaki logo, sanat eseri ve markalar ayrı haklara tabidir.\n')
        f.write('- Klibi olduğu gibi satmak yasaktır.\n\n')
        f.write('**Yer tutucudur.** Yayında mekân ve ekip için gerçek çekim '
                'kullanılır (docs/marka-kimligi.md §6.1).\n')

    with open(os.path.join(klasor, 'denetim-raporu.txt'), 'w', encoding='utf-8') as f:
        f.write('Kartela Reels denetim raporu\nTarih: %s\n\n' % date.today().isoformat())
        if ozet[denetim.BLOCKER] and zorla:
            f.write('*** ZORLANDI ***\n\n')
        f.write('Özet: %d engelleyici · %d uyarı · %d not\n\n'
                % (ozet[denetim.BLOCKER], ozet[denetim.UYARI], ozet[denetim.NOT]))
        for b in tum:
            f.write(b.satir() + '\n\n')
        if not tum:
            f.write('Bulgu yok.\n')

    if brif.get('aciklama'):
        with open(os.path.join(klasor, 'aciklama.txt'), 'w', encoding='utf-8') as f:
            f.write(brif['aciklama'].strip() + '\n')
            if brif.get('etiketler'):
                f.write('\n' + ' '.join('#' + e.lstrip('#')
                                        for e in brif['etiketler']) + '\n')

    print('\n✓ Çıktı: %s' % hedef)
    print('  KUNYE.md · denetim-raporu.txt · kontrol dosyaları')
    return 0 if rapor.get('uygun', True) else 1


def main():
    a = argparse.ArgumentParser(description='Kartela Reels üretimi')
    a.add_argument('brif')
    a.add_argument('--zorla', action='store_true')
    args = a.parse_args()
    sys.exit(calistir(args.brif, args.zorla))


if __name__ == '__main__':
    main()
