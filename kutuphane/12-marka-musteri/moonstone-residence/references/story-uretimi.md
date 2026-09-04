# Story Üretimi

Instagram Hikâyeleri için mekanik, ölçü ve şablonlar. Marka kuralları için
`marka-kimligi.md`, dil için `ton-ve-dil.md`, kanal stratejisi için
`sosyal-medya.md`.

**Kanıt notu:** Bu dosyadaki benchmark rakamları sektör analiz araçlarının
2026 yayınlarından derlendi (`SEKTÖR` seviyesi — yön gösterir, bağımsız
doğrulanmadı). Kendi hesabınızın Insights verisi bunlardan sapabilir; ilk üç
ay sonunda kendi tabanınızı çıkarın ve bu rakamları bırakın.

## İçindekiler
1. Story'nin işi
2. Benchmark rakamları
3. Dizi mimarisi: kaç kare, ne kadar süre
4. Kare anatomisi ve güvenli alan
5. Sticker mekaniği
6. Anlatı kalıpları
7. Moonstone story şablonları
8. Öne çıkanlar (highlights) mimarisi
9. Haftalık ritim
10. Ölçüm ve yayın sonrası okuma

---

## 1. Story'nin işi

Feed marka kurar, Reels yeni insan getirir, **Story eldeki insanı harekete
geçirir.** Moonstone'da story'nin üç somut görevi var:

1. **Şantiyeyi canlı tutmak** — takipçi projeyi ilerliyor görmeli.
2. **Soru toplamak** — soru kutusundan gelen her soru bir sonraki içeriktir ve
   satış ekibi için bedava pazar araştırmasıdır.
3. **DM başlatmak** — story'den gelen DM, bu segmentte en sıcak lead kanalı.
   Türkiye'de WhatsApp %90 ile bir numaralı uygulama; story → DM → WhatsApp
   zinciri Moonstone'un ana dönüşüm yoludur.

Story satış yapmaz, **satış konuşmasını başlatır.** Her diziyi bu gözle kur.

## 2. Benchmark rakamları

| Ölçüt | Referans aralık |
|---|---|
| Tamamlama oranı (completion) | ~%70 genel; küçük hesaplarda %90+ |
| Çıkış oranı — 1. kare | ~%23,8 (en yüksek kayıp burada) |
| Çıkış oranı — 2. kare | ~%20,5 |
| Çıkış oranı — 3. kare | ~%18,5 |
| Çıkış oranı — 4–9. kare | ~%13–16 |
| İleri kaydırma (tap forward) | görselde %56–66, videoda %50–62 |
| Geri dönüş (tap back) | ~%4,5 — **yüksekse iyi işarettir**, insan bir şeyi tekrar okumuş |
| Sticker etkileşimi | erişimin %15–25'i; %25 üstü çok iyi |
| Bağlantı tıklaması | ortalama ~%1,2; iyi aralık %3–8 |
| Yanıt (reply) oranı | erişimin %1–3'ü |
| Erişim oranı — 1K–5K takipçili hesap | takipçinin %9,5–10,4'ü |
| Erişim oranı — 5K–10K | %3,5–4,2 |

**Bunun pratik anlamı:** İzleyicinin dörtte biri **birinci karede** düşüyor.
Yani ilk kare bir kapak değil, bir kancadır. "MOONSTONE RESIDENCE" yazan bir
logo karesiyle başlamak, izleyicinin %24'ünü doğrudan atmaktır.

Yeni bir hesapta erişim oranının takipçinin %10'u civarında olması normaldir —
500 takipçide 50 kişi görür. Bu düşük değil, tabandır. Rakam değil, **oran**
ve **trend** izlenir.

## 3. Dizi mimarisi: kaç kare, ne kadar süre

- **Erişim hedefliyorsan:** 6–13 kare.
- **Tamamlama hedefliyorsan:** 7 kare veya altı.
- **Anlatı için tatlı nokta:** 3–5 kare. Bağlı bir hikâye insanı ileri
  kaydırtıyor; kopuk kareler kaydırtmıyor, çıkartıyor.
- **Kare başına süre:** 5–10 saniye en yüksek tamamlamayı veriyor. 15 saniyeyi
  geçen kare belirgin biçimde kaybettiriyor.
- **Günde kaç dizi:** Moonstone ölçeğinde günde **bir dizi** yeterli. Az ama
  iyi üretilmiş kare, çok ama özensiz kareden iyi sonuç veriyor.

Moonstone için varsayılan: **4–6 kare, kare başına 6–8 saniye, günde bir dizi.**

## 4. Kare anatomisi ve güvenli alan

Tuval **1080×1920 px (9:16)**. Instagram kendi arayüzünü üstüne bindiriyor:

```
┌─────────────────────────────┐  0
│  ÜST 250 px — İLERLEME       │   Instagram: ilerleme çubuğu,
│  ÇUBUĞU VE PROFİL            │   profil adı, kapatma düğmesi
├─────────────────────────────┤  250
│                             │
│                             │
│      GÜVENLİ ALAN           │   Başlık, metin, logo, veri
│      1080 × 1420            │   buraya. Kenarlardan en az
│                             │   65 px içeride kal.
│                             │
│   [ sticker: orta-alt ]     │   Etkileşim öğesi buraya —
│                             │   başparmakla ulaşılabilir
├─────────────────────────────┤  1670
│  ALT 250 px — YANIT ALANI    │   Instagram: yanıt kutusu,
│  VE DÜĞMELER                │   paylaş/beğen düğmeleri
└─────────────────────────────┘  1920
```

**Kare tasarım kuralları (marka uyumlu):**

- Zemin: lacivert `#040C1D` ya da tam kanama render + üstüne
  `linear-gradient(to top, rgba(4,12,29,.85), transparent)` okunabilirlik katmanı.
- Başlık: Cormorant Garamond, 64–96 px, harf aralığı `0.04em`, beyaz.
- Gövde/veri: Lora ya da IBM Plex benzeri nötr sans, 34–44 px.
- Vurgu: altın `#B8992F` — koyu zeminde güvenli (7,1:1 kontrast). Açık zeminde
  metin rengi olarak kullanma.
- Logo: sağ üstte, güvenli alanın içinde, küçük. Her karede değil, **ilk ve
  son karede** yeterli.
- Render kullanılan her karede küçük ve okunur **"Temsili görseldir"** notu.

## 5. Sticker mekaniği

En yüksek erişimli hesaplar **neredeyse her kareye bir sticker koyuyor** —
süs olsun diye değil, insana kaydırmak yerine yapacak bir şey verdiği için.
Sticker erişimin %15–25'ini etkileşime çeviriyor.

| Sticker | Ne zaman | Moonstone örneği |
|---|---|---|
| **Anket (2 seçenek)** | En düşük eşikli etkileşim; tek dokunuş | "2+1 mi, 3+1 mi?" · "Kiler şart mı, lüks mü?" |
| **Soru kutusu** | İçerik fikri toplamak, satışa veri getirmek | "Proje hakkında en çok neyi merak ediyorsunuz?" |
| **Kaydırıcı (emoji slider)** | Estetik tepkisi ölçmek | Cephe render'ı + "Bu cephe kaç puan?" |
| **Test (quiz)** | Bilgi vermek + oynatmak | "Tip 5'in salonu kaç m²? → 28 / 32 / 36" (doğru: 36,05) |
| **Bağlantı** | Siteye/plan sayfasına taşımak | "Tüm daire planları" → ilgili sayfa |
| **Geri sayım** | Gerçek bir tarih varsa | Satış ofisi açılışı, canlı yayın. **Sahte aciliyet için kullanma.** |
| **Konum** | Her yerel içerikte | Tuzla / satış ofisi konumu |
| **Bahsetme** | Ayhanlar hesabını etiketlemek | Erişimi ikiye böler, kurumsal güveni taşır |

**Kural:** Bir karede en fazla bir etkileşim sticker'ı. İki anket üst üste
konursa ikisi de tıklanmıyor.

**Soru kutusundan gelen her soru üç şeye dönüşür:** bir story yanıtı, bir SSS
maddesi (siteye), bir carousel fikri. Soru toplamayı haftalık alışkanlık yap.

## 6. Anlatı kalıpları

Bir dizi, bağımsız karelerin toplamı değil. Üç kalıp Moonstone'un içeriğinin
neredeyse tamamını karşılar:

**A · Kanca → Gerilim → Ödül** (3–4 kare)
Bir merak uyandır, cevabı geciktir, ver. Ürün ve bilgi içerikleri için.
> K1: "Salonu, evin yarısından büyük." · K2: Tip 2 planı, ölçüler görünür ·
> K3: "22,25 m² salon + mutfak. Net 40,49 m²." · K4: Bağlantı sticker'ı.

**Kancayı olumlu kur.** "40 m²'de yaşanır mı?" tipi yeterlilik soruları
okuyucuya olumsuz cevabı da hediye eder; aynı bilgiyi doğrulanabilir bir oran
olarak vermek hem daha güçlü hem daha dürüst. Bkz. `olumlu-dil.md`.

**B · Süreç** (4–6 kare)
Bir işin başından sonuna. Şantiye içeriğinin doğal biçimi.
> K1: "Bu sabah 7. kat." · K2–4: kalıp, beton, ekip · K5: geniş plan ·
> K6: anket "Sizce kaç ayda tamamlanır?"

**C · Karşılaştırma** (3 kare)
İki şeyi yan yana koy, izleyiciye seçtir.
> K1: "Tip 1 mi Tip 3 mü?" · K2: iki planın yan yana ölçüleri ·
> K3: anket + "Detaylı tablo profildeki bağlantıda."

Üçünde de **son kare bir sonraki adımı söyler.** Adım her zaman satış olmak
zorunda değil — "yarın devamı" da bir adımdır ve ertesi gün izlenmeyi artırır.

## 7. Moonstone story şablonları

Bunlar doğrudan üretilebilir. Veriler `proje-verileri.md`'den; hiçbiri
uydurma değil.

**1 · Şantiye günlüğü** (haftada 2, sabah)
`K1` Tarih + kat bilgisi, canlı çekim, altyazı: "24 Ağustos · 7. kat"
`K2` Yakın detay — demir, kalıp, beton yüzeyi
`K3` Geniş plan, cephenin bugünkü hali
`K4` Anket: "Sizce cephe hangi ayda kapanır?"

**2 · Daire tipi turu** (haftada 1)
`K1` Kanca: "36 m² salon nasıl duruyor?"
`K2` Tip 5 planı, salon vurgulu
`K3` Mahal listesi: ebeveyn banyosu, kiler, 7,11 m² hol
`K4` "10. katta, geniş teraslı." + bağlantı sticker'ı

**3 · Sayı kartı** (haftada 1)
Tek kare, koyu zemin, büyük altın rakam: `3.000 m²` / `6 daire tipi` /
`40,49 – 96,54 m² net`. Sticker: kaydırıcı ya da soru kutusu.

**4 · Sosyal alan** (2 haftada 1)
`K1` "3. bodrumda ne var?" `K2` Kapalı havuz `K3` Spor salonu
`K4` Hamam-sauna-masaj `K5` Anket: "Hangisini en çok kullanırsınız?"

**5 · Soru toplama** (haftada 1, akşam)
Tek kare, sade lacivert zemin, soru kutusu: "Moonstone hakkında en çok neyi
merak ediyorsunuz?" — gelen soruları ertesi gün ayrı karelerde yanıtla.

**6 · Cevap dizisi** (soru toplamanın ertesi günü)
Her karede bir soru + kısa net cevap. Fiyat sorulduysa: "Fiyat ve ödeme
seçenekleri için satış ofisimizden bilgi alabilirsiniz" + WhatsApp bağlantısı.
**Fiyat rakamı yazma** — doğrulanmış veri yok.

**7 · Kurumsal kimlik** (ayda 1)
Mockup klasöründeki gerçek görseller — kartvizit, cepli dosya, flama.
"Ayhanlar Mimarlık Yapı ve İnşaat güvencesiyle." Marka gücünü ucuza taşır.

**8 · Mimari detay** (haftada 1)
Render'dan tek bir detay: cam yüzey, dikey hat, ışık. Cormorant başlık:
"Işık, iç mekânın malzemesidir." Sticker: kaydırıcı.

**9 · Satış ofisi** (2 haftada 1)
`K1` Ofisin içi `K2` Maket/plan masası `K3` Konum sticker'ı + yol tarifi
`K4` "Randevusuz da gelebilirsiniz." + WhatsApp

**10 · Yerel içerik** (2 haftada 1) `[DOĞRULA: mesafeler]`
Aydıntepe/Tuzla'dan gerçek bir kare — sahil, çarşı, ulaşım. Konum sticker'ı
zorunlu. Bu içerik yerel keşfi besler ve projeyi bir yere oturtur.

## 8. Öne çıkanlar (highlights) mimarisi

Öne çıkanlar profilin kalıcı vitrini — yeni gelen kişi önce oraya bakar.
Kapak görselleri **`Icon Çalışması/Icon-gold/` setinden** yapılsın; ikonlar
zaten hazır ve markanın kendi malı.

| Öne çıkan | İkon | İçerik |
|---|---|---|
| Daire Planları | Proje Detayları | Altı tipin ayrı ayrı kareleri |
| Sosyal Alanlar | Yaşam Tarzı | Havuz, spor salonu, spa |
| İnşaat | İnşaat Süreci | Aylık ilerleme, kronolojik |
| Ticari Alan | Projelerimiz | 3.000 m², dükkân m²'leri, yatırımcı dili |
| Lokasyon | Lokasyon | Konum, ulaşım, çevre |
| Sıkça Sorulanlar | Hakkımızda | Soru kutusundan gelen gerçek sorular |
| İletişim | İletişim | Adres, telefon, WhatsApp, çalışma saatleri |

Sıra önemli: soldan sağa **Daire Planları → Sosyal Alanlar → İnşaat**.
En çok bakılan üç şey bunlar.

Öne çıkanlar **ölü arşiv olmamalı** — inşaat öne çıkanına her ay yeni kare
eklenir, eskisi silinmez (kronoloji güven üretir).

## 9. Haftalık ritim

| Gün | İçerik |
|---|---|
| Pazartesi | Şantiye günlüğü (dizi B) |
| Salı | Mimari detay (tek kare + kaydırıcı) |
| Çarşamba | Daire tipi turu (dizi A) |
| Perşembe | Şantiye günlüğü ya da sosyal alan |
| Cuma | Soru toplama (tek kare, akşam) |
| Cumartesi | Cevap dizisi |
| Pazar | Sayı kartı ya da yerel içerik |

Türkiye için paylaşım saatleri `SEKTÖR`: gün içi **10:00–15:00** en dengeli
aralık; **Pazar 21:00** haftanın etkileşim zirvesi; Reels için **20:00–23:00**.
İlk 30–60 dakikadaki etkileşim dağıtımı belirliyor. Bunlar başlangıç
noktasıdır — ikinci aydan itibaren kendi Insights verinize göre ayarlayın.

## 10. Ölçüm ve yayın sonrası okuma

Instagram Insights'ta bakılacaklar ve nasıl okunacağı:

- **Kare bazlı çıkış (exits):** Hangi karede insan kaçıyor? 1. karede yüksek
  çıkış = kanca zayıf. Ortada ani sıçrama = o kare sıkıcı ya da okunmuyor.
- **İleri kaydırma (forward taps):** Yüksekse kare çok uzun ya da içerik ince.
- **Geri dönüş (back taps):** **İyi sinyal.** İnsan bir şeyi tekrar okumuş —
  genelde plan, m² ya da sayı kartı. Hangi karelerin geri döndürdüğünü not al,
  o tür içeriği çoğalt.
- **Sticker etkileşimi:** %15'in altındaysa sticker ya yanlış yerde (güvenli
  alan dışında) ya da soru ilgi çekmiyor.
- **Yanıt ve DM sayısı:** Asıl metrik bu. Görüntülenme değil, **başlayan
  konuşma sayısı** raporlanır.
- **Bağlantı tıklaması:** %1,2 ortalama; %3'ün altındaysa bağlantı karesi
  yeterince değer vaat etmiyor.

Aylık raporda ilk satır şu olmalı: *"Story'den gelen DM ve WhatsApp
görüşmesi sayısı."* Görüntülenme sayısı en altta, bağlam olarak yer alır.
