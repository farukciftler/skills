# Senaryo Şablonları — Fotoğraftan Reels'e

Bu dosya, bir render/fotoğraf geldiğinde **senaryo** üretmenin kalıbıdır.
Senaryo = çekim listesi (her çekim: kaynak görsel, Kling prompt'u, süre,
model) + ekran metni + açıklama + etiket. Kural kaynakları:
`gorsel-yon-referans.md` (K1–K8), `post-uretimi.md` §3 (kanca, yapı),
`ton-ve-dil.md` (dil), `Sosyal Medya/Moonstone-Acilis-Yayini-Uretim-Brifleri.md`
(9 gönderi). Prompt sözlüğü `prompt-rehberi.md`.

## 1. Görseli okumak — senaryo yazmadan önce

Gelen görsele bak ve şu beşi yaz; senaryo bunlardan çıkar:

| Soru | Cevap ne belirler |
|---|---|
| **Ne var?** cephe / iç mekân / havuz / plan / teras / drone | Şablon (§3) |
| **Işık saati?** öğle / gün batımı / mavi saat / gece | K1: gündüzse `aksam.py` ya da sabit kamera + "sky darkens"; render akşamsa doğrudan |
| **Oran ve çözünürlük?** | 9:16'ya kırpınca ne kaybolur → `hazirla.py --odak`; kısa kenar < 1.080 ise "yumuşak çıkar" uyarısı |
| **Kadrajda ne hareket edebilir?** gökyüzü, cam yansıması, su, ağaç, perde, vitrin ışığı | Prompt'un "çevre hareketi" cümlesi |
| **Kaynak nereden?** katalog türevi mi, ofis orijinali mi | §5 kuralı: katalog türevi **yayına gitmez**, test için kullanılır |

Kaynak katalog türeviyse senaryoyu yine yaz, üret, ama çıktıyı "taslak —
ofis kaynağı gelince yeniden üretilecek" diye işaretle.

## 2. Senaryo dosyası (`senaryo.json`)

```json
{
  "baslik": "01 · Marka açılışı",
  "format": "reels", "hedef_sure_sn": 10,
  "cikti_dizini": "Sosyal Medya Çıktıları/video/2026-09/01-marka-acilisi",
  "varsayilan": { "model": "v3-pro", "sure": 5, "cfg": 0.5, "ses": false, "tekrar": 2 },
  "cekimler": [
    { "ad": "01-crane-inis", "gorsel": "kaynak/cephe-9x16.jpg",
      "prompt": "Slow crane down from the roofline toward the entrance ...",
      "rol": "kanca", "ekran_metni": "" },
    { "ad": "02-yaklasma", "gorsel": "kaynak/cephe-9x16.jpg",
      "prompt": "The building stays perfectly still and rigid ... slow push-in ...",
      "rol": "govde", "ekran_metni": "Ay taşının zarafeti, yaşamın en değerli hali" }
  ],
  "kapanis": { "kart": "logo", "sure": 2.5 },
  "ekran_metni": "Ay taşının zarafeti, yaşamın en değerli hali",
  "aciklama": "…", "etiketler": ["#moonstoneresidence", "#tuzla", "#aydıntepe", "#rezidans", "#mimari"],
  "alt_metin": "Mavi saatte aydınlatılmış Moonstone Residence cephesi, temsili render.",
  "montaj": "bitir.py 01-crane-inis-1.mp4 02-yaklasma-2.mp4 --katman katman.png --kapanis logo-kart.png --bekle 1"
}
```

`kling_video.py toplu` yalnızca `varsayilan` + `cekimler` alanlarını okur;
diğerleri montaj ve yayın için insan/Claude notudur. `tekrar: 2` = her çekim
iki varyant (dosya adı `-1`, `-2`).

## 3. Şablonlar — görsel tipine göre

Her şablon: **kanca (0–2 sn) → gövde → kapanış**. Süre 10–20 sn = 2–4 çekim ×
5 sn + kapanış kartı 2,5 sn. Çekim başına prompt `prompt-rehberi.md` §6'dan.

### Ş1 · Cephe (tek render) — "Marka açılışı" (brief 01, 10 sn)
| # | Rol | Prompt | Ekran |
|---|---|---|---|
| 1 | Kanca | P7 crane iniş, katlar ışıklanır | — |
| 2 | Gövde | P1 yaklaşma, vitrinler kadraja girer | tek satır slogan (alt üçte bir) |
| K | Kapanış | `--bekle 1` + logo kartı 2,5 sn | — |
Ses: sessiz-derin ambiyans. CTA yok. Katman 2. çekimde girer (`--katman-baslangic 5`).

### Ş2 · Cephe (tek render) — "Proje genel görünümü" (brief 02, 15 sn)
1 P6 drone yaklaşımı (kanca) · 2 P4 paralaks ya da P5 mikro-orbit · 3 P2 sabit
kamera ışık değişimi (dinlenme) · K logo. Ekran: `Değerli bir yaşamın yeni adresi`.

### Ş3 · Cephe — "Mimari detay" tek görsel yerine 5 sn sessiz klip (brief 05)
Tek çekim P3 tilt (dikeylik). Ekran `Dikey ve yatay hatların dengesi`. Logo
sol üst. Kapanış kartı yok; `--bekle 1`.

### Ş4 · Konum (brief 03, 20 sn) — harita kısmı AI değil
Harita animasyonu `bitir.py` dışında (Keynote/After Effects ya da ffmpeg
zoompan). AI yalnızca 3. çekim: P1 ya da P13 ticari zemin kat. Ekran:
`Aydıntepe'de, Tuzla'nın içinde`. Ulaşım süresi yazılmaz `[DOĞRULA]`.

### Ş5 · Yaşam — havuz · spor · hamam (brief 06, 20 sn)
1 P8 havuz sabit kamera, su kostikleri (kanca; üst metin `Bunların üçü de aynı
katta.`) · 2 P9 havuz yaklaşma · 3 spor/hamam **yalnızca proje render'ıysa**
(sitedeki `gecici-gorsel` dosyaları örnek fotoğraf olabilir — `[DOĞRULA]`,
değilse bu çekim üretilmez) · K logo. İnsan yok (K6).

### Ş6 · Süreç (brief 08, 25 sn) — büyük kısmı AI değil
Eskiz → plan → kesit → render üst üste bindirme ffmpeg/Keynote işi. AI
yalnızca son çekim: P2 sabit kamera mavi saat. Ekran `Bir proje kâğıttan
nasıl doğar?`. "yükseliyor / şantiye / temel" yok.

### Ş7 · Manifesto (brief 09, 15 sn) — iç mekân render'ı gerektirir
1 P10 salon yaklaşma (ışık kapıdan düşer) · 2 P12 koridor · 3 P11 teras
manzara · K logo. Ekran iki satır aralıklı: `Yeni bir ev.` … `Yeni bir
başlangıç.` (iki `katman.py` çıktısı, `--katman-baslangic/--katman-bitis`
ile iki montaj geçişi ya da iki ayrı bitir.py turu). **İç mekân render'ı
elimizde yok**; ofisten gelince.

### Ş8 · Tek kelime (referans @yapay.co "PRESTİJ")
Herhangi bir cephe klibi + `katman.py --tek-kelime "Prestij"`. Sessiz, CTA yok.
Kelime seçenekleri ton sözlüğünden: Zarafet · Prestij · Huzur · Değer.
"Lüks", "Fırsat" **yok**.

### Ş9 · Story 5 sn (dikey, sticker payı)
Tek çekim, `ig-story` güvenli alanı (üst/alt 250). Katman yok ya da yalnızca
logo; metin ve sticker Instagram'da eklenir (`story-uretimi.md`).

### Ş10 · Web hero (16:9, döngü)
`hazirla.py --oran 16:9`, P2 ya da P14 sabit kamera + çevre hareketi,
başlangıç = bitiş görseli (kesintisiz döngü), `bitir.py --preset web`
sessiz, `libx264`. Üstüne site kendi tipografisini koyar.

## 4. Ekran metni ve açıklama kalıbı

- Ekran metni **tek satır**, katalog/ton sözlüğünden (`Ay taşının zarafeti,
  yaşamın en değerli hali` · `Değerli bir yaşamın yeni adresi` · `Yeni nesil
  yaşam alanları.` · `Işık, iç mekânın malzemesidir.`). Rakam, telefon, fiyat,
  "son daireler" **yok**.
- Açıklama: kanca (≤ 60 kr) → bağlam (1 cümle) → fayda (1 cümle) → adım
  (isteğe bağlı, tek) → `Temsili görseldir; görseller yapay zekâ desteğiyle
  hareketlendirilmiştir.` → 3–5 etiket (marka · yerel · kategori · konu · kurumsal).
- Alt metin ≤ 125 karakter, görseli tarif eder.
- Konum etiketi: Aydıntepe, Tuzla.

## 5. Yayın öncesi kontrol (K1–K8 + bu skill)

- [ ] Kaynak görsel ofis orijinali mi? Katalog türeviyse "taslak" damgası var mı?
- [ ] Işık akşam/mavi saat mi?
- [ ] Her çekimde tek kamera hareketi, hız sözcüğü, sabitleyici ifade var mı?
- [ ] Doğramalar düz, cam erimemiş, insan/araba belirmemiş mi? (iki varyanttan iyisi seçildi mi?)
- [ ] Metin ve logo AI karesine değil, `katman.py` ile bindi mi? Güvenli alan içinde mi?
- [ ] Karede ≤ 3 öğe; "Temsili görseldir" okunur mu?
- [ ] Açıklamada yapay zekâ beyanı satırı var mı? Instagram "Made with AI" açık mı?
- [ ] Künye `.json` klibin yanında mı? `uretim-gunlugu.jsonl` güncel mi?
- [ ] Doğrulanmamış veri yok mu? (fiyat, teslim, mesafe, daire sayısı, "yükseliyor")
