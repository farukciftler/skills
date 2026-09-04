---
name: turkce-anlati
description: |
  Dikey kısa video (Reels · Shorts · TikTok) için Türkçe anlatı metni yazar ve
  denetler. Metin KONUŞULMAK ve altyazı olarak OKUNMAK üzere yazılır; yazılı
  makale kuralları burada geçmez. Bir brifin `metin` alanını yazarken, mevcut
  bir metni doğallaştırırken, seslendirme öncesi denetlerken KULLAN.
  Tetikleyiciler, "anlatı metni yaz", "senaryo yaz", "voiceover metni",
  "seslendirme metni", "metni doğallaştır", "çeviri kokuyor", "Türkçesi kötü",
  "kültüre uygun yaz", "reels metni", "shorts senaryosu", "hook yaz".
  Yapay zekâ yazım kalıpları için `insanca` skill'i AYRICA geçerlidir; bu skill
  onun üstüne konuşulan dilin ve Türkiye kültürünün kısıtlarını ekler.
license: MIT
---

# Türkçe anlatı, konuşulan metin, okunan altyazı

Bu depodaki metin iki kez tüketiliyor: **kulakla** (TTS okur) ve **gözle**
(kelime kelime yanan altyazı). İkisinin kısıtları farklı ve ikisi de yazılı
makale kısıtlarından farklı. Bu skill o farkı yazıya döküyor.

**Önce oku:** `.claude/skills/insanca/SKILL.md`, yapay zekâ yazım kalıplarının
48 maddesi orada ve hepsi burada da geçerli. Bu dosya onu tekrar etmiyor,
üstüne konuşulan dilin ve kültürün kurallarını ekliyor.

---

## 0. Tek cümlede

**Söylendiği gibi yaz.** Gözle okunacak bir makale değil, sesli söylenecek bir
cümle kuruyorsun. Yazarken sesli oku; ağzın takılıyorsa metin yanlıştır.

---

## 1. Konuşulan dilin kısıtları

### 1.1 Nefes uzunluğu cümleyi belirler
**8-14 kelime.** Bunun üstü tek nefeste söylenmiyor; TTS söyler ama dinleyici
ipi kaybeder. Altı da zararlı: art arda üç kısa cümle telgraf gibi okunur.

Ritim değişken olmalı, insanca'nın "metronomik ritim" maddesi burada iki kat
geçerli, çünkü sesli okumada tekdüzelik yazılı metinden çok daha çabuk sırıtır.

### 1.2 Sesli okunmayan işaretler kullanılmaz
Parantez, noktalı virgül, uzun tire, kesme çizgisi, üç nokta, dipnot: hiçbiri
seste karşılığı olan şeyler değil. Parantez içine koyacağın şey ya cümledir ya
gereksizdir.

Virgül ve nokta kalır, onlar duraktır.

### 1.3 Türkçe fiil sondadır; kanca bunu bozar
Türkçede yük cümlenin sonuna düşer. Bu, **ilk iki saniye için felakettir**:
izleyici yüklemi duymadan kaydırır.

Kancada **devrik cümle** kur, yükü öne al:

> ❌ İstanbul'un altında dünyanın bilinen en uzun antik su hattı var.
> ✅ Dört yüz yirmi altı kilometre. İstanbul'un altındaki su hattı bu kadar uzun.

Gövdede kurallı cümleye dön; devrik cümle üst üste kullanılırsa yapmacık olur.

### 1.4 Zamir kullanma
Türkçe pro-drop: özne çekimde zaten var. "Sen bunu bilmiyorsun" değil
"bunu bilmiyorsun", hatta çoğu zaman ikinci tekil şahsa hiç girme.
Zamir bolluğu çeviri kokusunun en belirgin işaretidir.

### 1.5 Bir cümle bir fikir
Altyazı öbeği en çok 4 kelime; uzun bileşik cümle ekranda parçalanınca anlam
kopar. Bağlaçla iki fikri birbirine dikme, ikinci cümleyi aç.

---

## 2. Seslendirme motorunun ölçülmüş kısıtları

`motor/ses/okunus.py` bunları **otomatik** dönüştürüyor, brifte doğal yazabilirsin.
Ama neyin neden dönüştüğünü bil; dönüşmeyen bir biçim uydurursan hat sessizce
yanlış okur.

Ölçüm: ElevenLabs `bill` · `eleven_multilingual_v2` · faster-whisper `small`
geri-dönüşü · 2026-08-23.

| Yazım | Ölçülen sonuç |
|---|---|
| `426 km` | **2/2 felaket**, «dört yüz yüzyüz mülandı vatid hilet» |
| `426 kilometre` | **2/3 bozuk**, «4126», «4 düzli 26» |
| `dört yüz yirmi altı kilometre` | **2/2 doğru** |
| `%74'ü` | **1/2 bozuk**, «%50 kütüğü» |
| `yüzde yetmiş dördü` | doğru |
| `M.Ö. 5.` | bozuk, «Müvbeşinci» |
| `MÖ beşinci` | doğru |
| `II. Mehmet` | **yanlış sayı okundu**, «3. Mehmet» |
| `İkinci Mehmet` | doğru |
| `DSİ` · `İBB` | bozuk, «DSI», «EBB» |
| `Devlet Su İşleri` | doğru |
| `1453'te` · `3,5 milyon` · `TBMM` · `vb.` | **doğru, dokunma** |

**Kural:** kısaltma birim (km, kg, sn…) ve `%` simgesi metne hiç girmez.
Roma rakamı yazıyla yazılır. Yıl ve ondalık rakamla kalır.

> Not: `İBB` bozuk okunuyor ama `TBMM` doğru, fark **İ harfi**. Türkçeye özgü
> harfleri taşıyan kısaltmalar açık yazılır.

---

## 3. Türkiye kültürüne uyum

### 3.1 Yerel adı kullan, çevirisini değil
`Constantinople` → **Konstantinopolis** (dönem adı) ya da **İstanbul**.
`Valens Aqueduct` → **Bozdoğan Kemeri**. `Basilica Cistern` → **Yerebatan Sarnıcı**.
Stok kütüphanesi İngilizce diye metin de İngilizce ada kaymasın.

### 3.2 Tarihî kişiyi halkın bildiği adla an
`II. Mehmet` teknik olarak doğru; **Fatih Sultan Mehmet** tanınır.
`Justinianus I` yerine **Justinianus**. Ansiklopedi künyesi değil anlatı yazıyorsun.

### 3.3 Ölçü ve biçim
Metrik sistem, her zaman. Ondalık **virgül** (3,5), binlik **nokta** (1.400).
Tarih **gün ay yıl**. Para **TL**; yabancı para geçiyorsa kur tarihini söyle.

### 3.4 Zorlama yerlilik yapma
Çay, mahalle, dolmuş, bakkal metne kendiliğinden giriyorsa iyi; iliştiriliyorsa
sırıtır. Aynısı deyimler için: **150-250 kelimede en çok bir deyim**
(`insanca/references/deyimler.md`). Deyim yığını samimiyet değil, gürültü.

### 3.5 Çevrilmiş deyim kullanma
"Günün sonunda", "bardağın dolu tarafı", "masaya yatırmak" gibi İngilizceden
kalıplanmış ifadeler çeviri kokusunun taşıyıcısıdır. Türkçede karşılığı varsa
onu kullan, yoksa düz söyle.

### 3.6 Hassas konularda iddia etme, aktar
Din, etnik köken, siyaset ve yakın tarih geçiyorsa: kaynağı söyle, yorumu
izleyiciye bırak. Bu kanal iddiaya dayanıyor; iddianın **kaynağı** olmalı.
Kaynak yoksa o cümle yazılmaz.

---

## 4. Bu depoya özgü kısıtlar

- **`kimlik.yaml → asla_yapmaz`** listesi metinde **makineyle** denetleniyor
  (`motor/kimlik.py:YASAK_DESEN`). Ünlem, aciliyet, kıtlık, clickbait soru,
  emir kipi, garanti, listicle sayacı, biri geçerse üretim TTS'e girmeden durur.
- **Cümle sayısı iskeletin rol sayısını karşılamalı.** Varsayılan iskeletler
  4 rollü (`motor/varyasyon.py:ISKELETLER`), yani `metin` 4 cümle olmalı.
- **Kapanış rolü çağrıdır ama emir değildir.** "Abone ol" yasak; kapanış
  iddiayı bağlar, izleyiciden bir şey istemez.
- **İlk cümlede somut im bulunsun**, rakam, ölçü birimi ya da özel ad.
  `motor/puanlama/olcumler.py:kanca` bunu sayıyor ve eşiği geçmeyen çekim
  render'a girmiyor.

---

## 5. Çalışma sırası

1. **İddiayı tek cümle yaz.** Taşımıyorsa metin de taşımaz.
2. **İskeleti seç** (`veri-once`, `sahne-once`, `karsit`, `soru-cevap`,
   `kronoloji`, `tek-nesne`) ve rol başına bir cümle yaz.
3. **Sesli oku.** Takılan yeri düzelt, ölçüt kulak, göz değil.
4. **`insanca` denetimini uygula**, 48 kalıp + 17 akış kuralı.
5. **§2 tablosuna göre gözden geçir.** Otomatik dönüşüm var ama uydurma biçim
   (örn. `426 klm`) dönüşmez.
6. **§3'e göre yerelleştir**, adlar, ölçüler, kaynak.
7. Brife yaz, `python -m motor cekim` çalıştır, `kanca` puanına bak.

---

## Kaynaklar

- `.claude/skills/insanca/`, Tahir Yıldız, MIT. 48 yapay zekâ yazım kalıbı,
  17 akış kuralı, deyim sözlüğü.
- `references/olcumler.md`, bu depodaki TTS ölçümlerinin ham kaydı.
- `docs/ffmpeg-hatti.md`, altyazı öbekleme ve güvenli alan kısıtları.
