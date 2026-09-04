# SEO doktrini — üç tipte de geçerli

Bu dosya ortak kuralları taşır. Tipe özgü olanlar `sehir.md`, `mekan.md`,
`rota.md` içinde.

## Sitenin hunideki yeri

Gezi aramaları dört aşamada ilerliyor: **ilham** (6–12 ay önce), **araştırma**
(3–6 ay), **karşılaştırma** (1–3 ay), **rezervasyon** (günler).

ComeSyria içerik sitesi **ilham ve araştırma** aşamalarına hizmet ediyor.
Rezervasyon comesyria.com'un OTA tarafının işi. Bu ayrım içeriği doğrudan
belirliyor:

- Fiyat karşılaştırması, "en iyi tur", "şimdi ayırt" dili **bu sitede yok.**
- Buradaki soru "gitmeye değer mi ve nasıl gidilir", "hangisi daha ucuz" değil.
- Her sayfa **tek bir arama niyetine** hizmet eder. İki niyeti tek sayfaya
  sıkıştırmak ikisini de zayıflatıyor.

## Hub & spoke

```
        şehir (hub)
       /     |     \
  mekan   mekan   rota (spoke)
```

- Şehir sayfası mekan ve rotalara **aşağı** bağlanır.
- Mekan ve rota şehre **yukarı** bağlanır (`city` alanı).
- Rota duraklara bağlanır (`stops`).

Bu iç bağlantı yapısı işin yarısı. Bağsız kayıt hem okurun yolunu kesiyor hem
tarayıcının derinliğe inmesini engelliyor. Sitede bu bağlar **alanlarla**
kuruluyor, gövdeye elle link yazarak değil — `city` ve `stops` doldurulursa ön
yüz bağlantıları kendi çiziyor.

## H2'ler soruyu karşılar

Başlık değil, **soru** mantığıyla kur. Okurun o tipte gerçekten sorduğu şeyler
tipin kendi dosyasında listeli.

Kötü: `Tarihçe` · `Genel Bilgiler` · `Sonuç`
İyi: `Ne zaman gidilir` · `Ne kadar sürer` · `Neyi kaçırma`

## Uzunluk

Üst sıradaki gezi sayfaları ortalama **~1.400 kelime**. Bu bir hedef değil bir
gösterge: konuyu tam kapsayan metin doğal olarak oraya yaklaşıyor. Kelime
saymak için cümle uzatma — boş cümle hem okuru hem sıralamayı düşürüyor.

Anahtar kelime yoğunluğu diye bir hedef **yok**. Aynı kelimeyi tekrar etmek
2010'ların tekniği; bugün konuyu tam kapsamak kazandırıyor.

## AEO — yapay zekâ aramasında alıntılanmak

2026'da trafiğin ciddi kısmı klasik mavi bağlantıdan değil, yapay zekâ
cevaplarından geliyor. Alıntılanan içeriğin ortak özellikleri:

1. **Çıkarılabilir olgu.** Paragrafın içine gömülmüş izlenim değil, tek başına
   doğru olan cümle. "Giriş 1500 SYP" alıntılanır; "makul bir ücret karşılığı
   gezilebiliyor" alıntılanmaz.
2. **Net yapı.** Soruyu karşılayan H2, altında doğrudan cevap. Cevap H2'nin
   hemen altındaki **ilk cümlede** olmalı, üçüncü paragrafta değil.
3. **Doğrulanabilirlik.** Tarih, ölçü, fiyat, saat. Belirsiz sıfat değil.
4. **Güncellik.** Eskimiş bilgi güveni bozuyor; fiyat ve saat değiştiyse kaydı
   güncelle.

Sitenin künye ızgarası (`entry_fee`, `opening_hours`, `duration`, `best_time`)
tam olarak bu işi yapıyor: **alıntılanabilir birim orası.** Doldurmak zorunlu.

## Yapısal veri

Ön yüz JSON-LD'yi alanlardan otomatik üretiyor (`web/src/lib/seo.tsx`). Senin
işin alanları doldurmak:

| Tip | Şema | Üreten alanlar |
| --- | --- | --- |
| `city` | `City` | `lat`, `lng` |
| `place` | `TouristAttraction` | `lat`, `lng`, `address`, `opening_hours`, `city` |
| `route` | `TouristTrip` + `itinerary` | `stops` |

Kurallar:

- **Koordinat dört ondalık basamak.** `36.1995` yeterli, `36.19` değil.
- **Şema alanları olgusal ve nötr kalır.** Kişisel izlenim gövde metnine ait,
  şemaya değil.
- Açıklama (özet) 150–160 karakter: hem meta açıklama hem şema açıklaması o.

## Üç dil, üç ayrı anahtar kelime

**Çeviri SEO'yu taşımıyor.** Aynı sayfanın üç dildeki başlığı üç ayrı sorguya
cevap verir:

| Dil | Tipik sorgu | Başlık buna göre |
| --- | --- | --- |
| tr | halep gezilecek yerler · halep kalesi giriş ücreti | Halep Kalesi |
| en | things to do in Aleppo · aleppo citadel opening hours | The Aleppo Citadel |
| ar | أماكن سياحية في حلب · قلعة حلب أوقات الزيارة | قلعة حلب |

Uygulaması:

- `title` ve `excerpt` **yeniden yazılır**, çevrilmez.
- `slug` her dilde o dilin okuru için türetilir.
- Gövde çevrilir ama **açıklama dozu değişir**: hedef dilin okurunun bilmediği
  şey açıklanır, bildiği şey açıklanmaz.

hreflang, kanonik ve site haritası bağlarını ön yüz otomatik kuruyor — tek
şartı çeviri bağının Polylang'de kurulmuş olması. `yayimla.php` bunu yapıyor.

## Kontrol listesi

Yayımlamadan önce, her dil için:

- [ ] Tek H1, marka adı yok
- [ ] Özet elle yazılmış, 150–160 karakter (Arapçada 125–155)
- [ ] İlk paragraf yazının tamamını özetliyor
- [ ] H2'ler okurun sorusunu karşılıyor
- [ ] Somut alanlar dolu (fiyat, saat, süre, koordinat)
- [ ] `city` bağı kurulu (mekan ve rota için)
- [ ] `stops` dolu (rota için)
- [ ] Kapak görseli var ve üç dilde aynı kimlik
- [ ] Slug her dilde farklı ve ASCII
- [ ] `denetle.mjs` temiz
