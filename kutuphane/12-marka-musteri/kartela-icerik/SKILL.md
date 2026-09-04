---
name: kartela-icerik
description: Kartela Psikoloji için Instagram gönderisi, karusel, hikaye ve Reels üretir — marka kimliğine ve MEB mevzuatına uygun, karekodlu, Türkçe seslendirmeli. Gönderi tasarla, afiş yap, duyuru görseli, etkinlik afişi, oyun grubu duyurusu, hikaye paylaşımı, karusel, reels, video, seslendirme, altyazı, sosyal medya içeriği, Instagram paylaşımı, post üret, story, açıklama metni, hashtag konularında kullan. Ayrıca hazır bir gönderiyi mevzuata göre denetlerken, yasak kelime kontrolü yaparken, karekod eksikliğini kontrol ederken kullan. Tetikleyiciler - instagram, gönderi, post, afiş, duyuru görseli, hikaye, story, karusel, reels, video üret, seslendirme, altyazı, sosyal medya, paylaşım, içerik takvimi.
---

# Kartela — Sosyal Medya İçerik Üretimi

Instagram gönderisi, karusel, hikaye ve Reels üretir. Her çıktı **önce mevzuat
denetiminden geçer**, sonra render edilir.

**Önce oku:** `docs/marka-kimligi.md` — özellikle §4 (renk), §5 (tipografi),
§7 (marka sesi), §8 (sosyal medya şablon sistemi).
**Mevzuat kısıtı için `rpdm-mevzuat` skill'i AYRICA geçerlidir.**

---

## Değişmez kurallar

Bunlar tartışmaya açık değildir; `denetim.py` çoğunu otomatik yakalar.

**Mevzuat — engelleyici:**
1. **Karekod her tanıtım materyalinde bulunur** (ÖÖK Yön. Ek m.4/2)
2. **Danışan resmi, ismi, başarısı, yorumu kullanılamaz** (Ek m.4/1) — veli rızası bu yasağı kaldırmaz
3. **Tanınabilir çocuk yüzü kullanılmaz** — danışan izlenimi yaratır
4. **"terapi, seans, tedavi, tanı, klinik, hasta" kelimeleri geçmez** (1219 s.K. Ek m.13)
5. **Ruhsat adı görünür** — "Özel … Rehberlik ve Psikolojik Danışma Merkezi" (m.7/4)
6. **MEB adı/logosu yok** — yerine "5580 sayılı Kanun kapsamında ruhsatlıdır" (m.7/5)
7. **Kanıtlanamayan iddia yok** — başarı oranı, garanti, "en iyi" (m.11)
8. **Televizyon mecrası yasak** (m.11)

**Marka — engelleyici:**
9. **Her gönderide fotoğraf bulunur.** Görselsiz gönderi üretilmez.
10. **Fotoğraf dikdörtgen blok olarak konmaz.** Daima en az iki kenardan taşar
    ve/veya maskeyle zemine erir. Beş yerleşim: `tam · alt · kemer · kose · yan`.
11. **Fotoğraf duotone ile palete çekilir.** Stok fotoğrafın kendi renkleri
    kompozisyona sızmaz.
12. **Aksan renkleri metin rengi olmaz** — yalnızca zemin ve dekoratif dolgu.
13. **Kartela şeridi tuvalde en fazla bir kez** — karuselde yalnızca kapakta.
14. **Ünlem, aciliyet ve kıtlık dili yok** — "son 3 kontenjan", "kaçırmayın" yasak.
15. **Emir kipi değil davet kipi** — "Randevu alın" değil "Yazmak isterseniz buradayız".

---

## Çalışma akışı

### 1. Brif yaz

`ornekler/` altındaki bir örneği kopyala. Alanlar:

| Alan | Zorunlu | Açıklama |
|---|---|---|
| `sablon` | ✅ | `t1-soz` · `t2-bilgi-kapak` · `t3-bilgi-ic` · `t4-duyuru` · `t5-mekan` · `h1-hikaye` |
| `gorsel` | ✅ | Depoya göreli yol. Yer tutucular: `website/frontend/public/gorseller/<kategori>/` |
| `yerlesim` | — | `tam · alt · kemer · kose · yan` (varsayılan `alt`) |
| `duotone` | — | `petrol · gul · mavi · sari · yumusak` (varsayılan `petrol`) |
| `zemin` | — | `z-beyaz · z-nane · z-gul · z-sari · z-mavi · z-petrol` |
| `baslik` | ✅ | Ana mesaj |
| `altmetin` | — | Destek cümlesi |
| `etiket` | — | Üst etiket (all-caps basılır) |
| `satirlar` | — | `[["Yaş","3–6"],["Gün","Cumartesi"]]` |
| `karekod_url` | ✅* | Karekodun işaret edeceği adres |
| `ruhsat_adi` | ✅ | Tam ruhsat adı |
| `aciklama` | — | Gönderi açıklaması → `aciklama.txt` |
| `etiketler` | — | Hashtag listesi |
| `kareler` | — | Karusel: her kare bir nesne; üst alanlar miras geçer |
| `tanitim` | — | `false` ise karekod aranmaz — gerekçesini brifte yaz |

`*` `tanitim: false` değilse zorunlu.

### 2. Denetle

```bash
.venv-icerik/bin/python .claude/skills/kartela-icerik/uret.py brif.json --denetim
```

Engelleyici bulgu varsa **metni düzelt**, denetimi zorlama.

### 3. Üret

```bash
.venv-icerik/bin/python .claude/skills/kartela-icerik/uret.py brif.json
```

Çıktı: `out/sosyal/<tarih>-<slug>/` — PNG'ler, `karekod.png`,
`aciklama.txt`, `denetim-raporu.txt`.

### 4. Reels (video)

```bash
.venv-icerik/bin/python .claude/skills/kartela-icerik/reels.py brif.json
```

**Gövde gerçek videodur** (Pexels dikey klipleri, duotone'lu, sessizleştirilmiş);
**yalnızca kapanış karesi statiktir** ve karekod ile ruhsat adını orada taşır.

Klip havuzu: `python3 src/gorsel/video_indir.py --kategori hepsi --adet 5`

**Seslendirme sesi `tr-TR-EmelNeural`** — kurucu dinleyerek seçti, değiştirilmez.

**Arka plan müziği prosedüreldir** (`src/icerik/muzik.py`) ve her Reels'te
bulunur. Stok/AI müzik kullanılmaz: prosedürel üretimde üçüncü taraf hakkı
yoktur. Dor modu, vurmalı yok, konuşma bandı oyulmuş. Brifte `muzik` ve
`muzik_seviye` ile ayarlanır.

Motor `src/icerik/` altında: `seslendirme.py` (TTS + kelime zamanlaması),
`kare.py` (HTML→PNG), `video.py` (hareket, geçiş, ses, altyazı, encode);
`klip.py` stok videoyu marka klibine çevirir. Ayrıntı: `references/reels.md`.

---

## Şablon seçimi

| Ne söylüyorsun | Şablon | Yerleşim önerisi |
|---|---|---|
| Tek bir fikir, ≤12 kelime | `t1-soz` | `kose` veya `yan` |
| Karusel kapağı, konu başlığı | `t2-bilgi-kapak` | `alt` veya `kemer` |
| Karusel iç sayfası, numaralı adım | `t3-bilgi-ic` | `yan` (metin nefes alsın) |
| Program/etkinlik duyurusu, tarih-saat-yaş | `t4-duyuru` | `alt` |
| Mekân, ekip, atmosfer | `t5-mekan` | `tam` + perde |
| Hikaye | `h1-hikaye` | `tam` veya `alt` |

**Duotone seçimi:** petrol = sakin/kurumsal · gül kurusu = sıcak/aile ·
açık mavi = bilgi/süreç · sarı = oyun/atölye/çocuk ·
`yumusak` = **gerçek mekân ve ekip fotoğrafı** (renkleri korur, yalnız sakinleştirir).

---

## Metin yazarken

Kelime karşılıkları ve güvenli kalıplar: `references/metin-kaliplari.md`.

Kısa kural: **mekân ve yöntem anlatılır, etki iddia edilmez.**
"Sanat terapisi" değil "Sanat Atölyesi". "Seans" değil "görüşme".
"Kaygıya son" değil "Akademik kaygıyla başa çıkma becerileri".

Her başvuru çağrısında eşiği düşüren cümle bulunur:
*"Karar vermek zorunda değilsiniz. Sadece sormak için de yazabilirsiniz."*

---

## Görsel seçimi

Yer tutucular `website/frontend/public/gorseller/` altında, `MANIFEST.json`
listeler. Yeni indirme:

```bash
python3 src/gorsel/indir.py --kategori mekan --adet 8
```

**Yer tutucu görseller yalnızca taslak içindir.** Yayında mekân ve ekip için
**gerçek fotoğraf** kullanılır (`docs/marka-kimligi.md` §6.1). `denetim.py`
Pexels yolu gördüğünde not düşer.

Seçim kuralı: tanınabilir çocuk yüzü yok · klinik sahne yok · çaresiz/depresif
poz yok · "mutlu aile" klişesi yok. Nesne, detay, el, mekân, doku tercih edilir.

---

## Referanslar

| Konu | Dosya |
|---|---|
| Şablon anatomileri, yerleşim ve duotone kararları | `references/sablonlar.md` |
| Güvenli metin kalıpları, başlık, açıklama, hashtag | `references/metin-kaliplari.md` |
| Reels: seslendirme, altyazı, encode, güvenli alan | `references/reels.md` |
| Yayın öncesi kontrol listesi | `references/kontrol-listesi.md` |

---

## Çıktı üslubu

Türkçe yaz. Bir tasarım kararını "güzel görünüyor" diye savunma — hangi kurala
ya da hangi ziyaretçi sorusuna bağlandığını söyle. Mevzuata takılan bir fikir
çıkarsa **kısıtı söyle ve çalışan alternatifi yaz**; sadece "olmaz" deme.
