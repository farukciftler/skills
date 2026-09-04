# SEO

Hedef: Tuzla ve çevresinde konut/ticari alan arayan kişiyi organik olarak
yakalamak, marka aramalarında tam hakimiyet kurmak ve portalların yanında
kendi kanalımızı kurmak.

## İçindekiler
1. Gerçekçi çerçeve
2. Anahtar kelime evreni
3. Sayfa-anahtar kelime eşlemesi
4. Teknik SEO
5. Yapısal veri (schema.org)
6. Yerel SEO
7. Portal stratejisi
8. İçerik planı
9. Ölçüm ve raporlama

---

## 1. Gerçekçi çerçeve

Üç şeyi baştan söyle:

**Marka araması bizim.** "moonstone residence", "moonstone tuzla" gibi
aramalarda birinci olmak kolay ve zorunludur. Site yayına girer girmez bu
sağlanır. Bugün site olmadığı için bu trafik **kayıp** — katalog dağıtılmış,
insanlar markayı aratıyor ve karşılarına hiçbir şey çıkmıyor. En acil iş bu.

**Genel aramalar zor ve yavaş.** "tuzla satılık daire" gibi sorgularda
sahibinden.com, emlakjet, hepsiemlak gibi portallar oturmuş durumda. Tek proje
sitesiyle onları geçmek 6–12 aylık bir iştir ve her zaman kazanılmaz. Kullanıcıya
bunu net söyle; "3 ayda ilk sıraya çıkarız" diyen kimseye inanmasın.

**Kazanılabilir yer uzun kuyruktur.** "aydıntepe tuzla rezidans", "tuzla 1+1
rezidans daire", "tuzla ticari dükkân kiralık" gibi spesifik ve niyeti yüksek
sorgular. Rekabet düşük, dönüşüm yüksek. Strateji buraya odaklanır.

## 2. Anahtar kelime evreni

Aşağıdaki liste niyet mantığıyla kurulmuştur. **Arama hacmi rakamı yazma** —
elimizde araç verisi yok; hacimler Google Keyword Planner / Ahrefs ile
doğrulanmadan rapora girmemeli.

**Marka (öncelik 1 — hemen kazanılır)**
moonstone residence · moonstone residence tuzla · moonstone residence fiyat ·
moonstone residence daire planları · moonstone residence kat planı ·
ayhanlar mimarlık · ayhanlar yapı inşaat · moonstone tuzla proje

**Yerel + ürün (öncelik 2 — asıl savaş alanı)**
tuzla rezidans · tuzla yeni proje · tuzla satılık rezidans · aydıntepe tuzla
satılık daire · tuzla aydıntepe rezidans · tuzla 1+1 daire · tuzla 2+1 satılık
daire · tuzla 3+1 rezidans · tuzla teraslı daire · tuzla havuzlu site ·
tuzla spor salonlu rezidans

**Ticari (ayrı ve değerli — rakip az)**
tuzla satılık dükkan · tuzla ticari alan · aydıntepe kiralık dükkan ·
tuzla cadde üstü dükkan · tuzla yatırımlık dükkan

**Bilgi amaçlı (blog için)**
tuzla yaşamak nasıl · aydıntepe tuzla hakkında · rezidans mı site mi ·
net brüt metrekare farkı · kat irtifakı nedir · konut kredisi hesaplama ·
1+1 daire yatırım mantıklı mı · rezidans aidatı ne kadar olur

**Uzun kuyruk kalıpları** — bunları çoğaltarak blog ve SSS üret:
`tuzla [oda tipi] [özellik] daire`, `aydıntepe [ihtiyaç]`, `[proje adı] [soru]`

## 3. Sayfa-anahtar kelime eşlemesi

Her sayfa **tek bir birincil** anahtar kelimeye sahip olsun; iki sayfa aynı
kelimeyi hedeflerse birbirini yer (yamyamlık).

| Sayfa | Birincil | Başlık etiketi (≤ 60 karakter) |
|---|---|---|
| `/` | moonstone residence | `Moonstone Residence \| Tuzla Aydıntepe'de Yeni Yaşam` |
| `/proje` | moonstone residence proje detayları | `Proje Detayları \| Moonstone Residence Tuzla` |
| `/daire-planlari` | tuzla rezidans daire planları | `Daire Planları ve m² Bilgileri \| Moonstone Residence` |
| `/sosyal-alanlar` | tuzla havuzlu rezidans | `Havuz, Spor Salonu ve Spa \| Moonstone Residence` |
| `/ticari-alanlar` | tuzla satılık dükkan | `3.000 m² Ticari Alan \| Moonstone Residence Tuzla` |
| `/lokasyon` | aydıntepe tuzla rezidans | `Lokasyon ve Ulaşım \| Moonstone Residence Tuzla` |
| `/insaat-sureci` | moonstone residence inşaat durumu | `İnşaat Süreci ve Güncel Durum \| Moonstone Residence` |
| `/hakkimizda` | ayhanlar mimarlık yapı inşaat | `Ayhanlar Mimarlık Yapı ve İnşaat \| Moonstone Residence` |
| `/iletisim` | moonstone residence satış ofisi | `İletişim ve Satış Ofisi \| Moonstone Residence Tuzla` |

**Meta açıklama kalıbı** (150–160 karakter, eylem içeren):
`Tuzla Aydıntepe'de 1+1'den 3+1'e rezidans daireleri, 3.000 m² ticari alan, havuz ve spa. Daire planlarını inceleyin, satış ofisinden randevu alın.`

Her sayfada **tek H1**, alt bölümler H2/H3 hiyerarşisinde. H1 marka sloganı
olabilir ama anahtar kelimeyi de taşımalı.

## 4. Teknik SEO

- **Kanonik URL** her sayfada tanımlı. `www` ve HTTPS tek biçimde 301'lenmiş.
- **`robots.txt`** ve **XML site haritası**; site haritası Search Console'a
  gönderilmiş. Görsel site haritası da ekle — render'lar Google Görseller'den
  trafik getirir.
- **`lang="tr"`**, `<meta charset="utf-8">`.
- Sayfalama, filtreleme veya URL parametresi kullanılıyorsa (daire tipi filtresi)
  ya `noindex` ver ya kanoniği ana sayfaya bağla; ince içerikli yüzlerce URL
  üretme.
- **404 sayfası** markalı ve navigasyonlu olsun.
- Core Web Vitals hedefleri `web-ui-ux.md` bölüm 7'de; Google bunları sıralama
  sinyali olarak kullanıyor ve bu sitede en büyük risk görsel ağırlığı.
- **Görsel SEO:** dosya adları anlamlı (`moonstone-residence-tuzla-cephe-render.avif`,
  `IMG_2831.jpg` değil), `alt` metinleri tanımlayıcı ve doğal.
- **İç bağlantı:** her daire tipi sayfasından lokasyon ve iletişime, blogdan
  ilgili ürün sayfasına bağlan. Yetim sayfa bırakma.
- **Sayfa hızı** ölçümü PageSpeed Insights alan verisiyle (lab değil) takip
  edilsin.

## 5. Yapısal veri (schema.org)

Konut projeleri için doğru işaretleme rakiplerin çoğunda yok — ucuz bir avantaj.
JSON-LD olarak `<head>`'e koy.

**Her sayfada — kuruluş:**

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Moonstone Residence",
  "legalName": "Ayhanlar Mimarlık, Yapı İnşaat Ltd. Şti.",
  "parentOrganization": {
    "@type": "Organization",
    "name": "Ayhanlar Mimarlık, Yapı İnşaat Ltd. Şti."
  },
  "url": "https://www.moonstoneresidence.com",
  "telephone": "+90-212-530-30-20",
  "email": "info@moonstoneresidence.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Aydıntepe Mah, Yeşildere Cad, Harbiye Sok No: 17",
    "addressLocality": "Tuzla",
    "addressRegion": "İstanbul",
    "addressCountry": "TR"
  },
  "areaServed": "Tuzla, İstanbul"
}
```

**Daire tipi sayfalarında — her tip için:**

```json
{
  "@context": "https://schema.org",
  "@type": "Apartment",
  "name": "Moonstone Residence Tip 5 · 3+1",
  "numberOfRooms": 4,
  "numberOfBedrooms": 3,
  "numberOfBathroomsTotal": 2,
  "floorSize": { "@type": "QuantitativeValue", "value": 96.54, "unitCode": "MTK" },
  "petsAllowed": null
}
```

`floorSize` olarak **net** m² kullan; brüt'ü ayrı bir `additionalProperty`
olarak ver. Fiyat bilgisi netleşmeden `Offer`/`price` alanı **ekleme** —
yanlış fiyat işaretlemesi hem güven hem mevzuat sorunudur.

Ayrıca: `BreadcrumbList` (tüm alt sayfalar), `FAQPage` (SSS bölümü olan
sayfalar), `ImageObject` (galeri).

## 6. Yerel SEO

Tuzla gibi ilçe bazlı aramada **Google Business Profile** çoğu zaman siteden
daha çok lead getirir. Sırasıyla:

1. **Google Business Profile aç ve doğrula** — satış ofisi adresiyle
   (Aydıntepe Mah, Yeşildere Cad, Harbiye Sok No: 17, Tuzla). Kategori:
   "Emlak geliştiricisi" / "İnşaat şirketi". Doğrulama kartla gelir, süreç
   1–2 hafta; **bugün başlatılmalı.**
2. Profili doldur: çalışma saatleri, telefon, web, hizmet alanı, açıklama
   (marka diliyle), en az 20 fotoğraf (render + saha + kimlik görselleri).
3. **Google Posts**'u haftada bir kullan — inşaat ilerlemesi doğal içerik.
4. **Yorum stratejisi:** ziyaret eden her müşteriden yorum iste; her yoruma
   markanın sesiyle yanıt ver. Yorum sayısı yerel sıralamanın en güçlü
   sinyallerinden.
5. **NAP tutarlılığı:** ad, adres, telefon her yerde birebir aynı yazılsın —
   site, GBP, portallar, sosyal medya, dizinler. Farklı yazımlar sinyali böler.
6. Apple Haritalar ve Yandex Haritalar kayıtlarını da aç (Türkiye'de Yandex
   trafiği azımsanmaz).

## 7. Portal stratejisi

Portallar rakip değil, dağıtım kanalıdır — ve organik aramada zaten üst
sıradalar. Sektör verisi, konut alıcısının karar öncesi **önce portala**
gittiğini, proje sitesinin ikinci durak olduğunu gösteriyor. Doğru kullanım:
**portalda görün, siteye taşı.** Portal ilanları site yayına girmeden de
açılabilir — bugün yapılabilecek en hızlı iş budur.

- **sahibinden.com**, **emlakjet**, **hepsiemlak**, **zingat** — her tip için
  ayrı ilan, gerçek m², gerçek görsel, ilan metninde marka adı ve site adresi.
- İlan başlığı kalıbı: `Moonstone Residence Tuzla Aydıntepe 2+1 Net 65 m² Teraslı`
  — proje adı önde, çünkü marka aramasını da yakalar.
- Portal ilanlarındaki görselleri site galerisiyle **aynı** tut; farklı görsel
  güven kırar.
- Portal lead'lerini de aynı CRM'e düşür ki lead başına maliyet karşılaştırması
  yapılabilsin.
- Ticari alanlar için ayrı ilan kategorisi kullan (satılık/kiralık işyeri) —
  farklı bir alıcı kitlesi.

## 8. İçerik planı

Blog süs değil; uzun kuyruk aramaları ve otoriteyi buradan kazanıyoruz. Ayda
2–4 yazı yeterli ama **düzenli** olmalı. Her yazı bir soruya cevap versin ve
sonunda ilgili ürün sayfasına bağlansın.

İlk 12 yazı önerisi (öncelik sırasıyla):

1. Tuzla Aydıntepe'de yaşamak: ulaşım, çevre, günlük hayat `[DOĞRULA]`
2. Net m² ile brüt m² arasındaki fark nedir, hangisine bakmalı
3. Rezidans mı site mi: aidat, hizmet ve yaşam farkları
4. 1+1 daire yatırımı mantıklı mı — kira getirisi nasıl hesaplanır
5. Kat irtifakı, kat mülkiyeti ve iskân: alıcı için ne anlama gelir
6. Ticari alan yatırımı: dükkân alırken bakılacak 8 kriter
7. Moonstone Residence daire tipleri karşılaştırması (ürün içeriği)
8. İnşaat süreci: Moonstone Residence'ta bu ay ne yapıldı (aylık dizi)
9. Havuzlu ve spor salonlu bir binada yaşamak neyi değiştirir
10. Konut kredisiyle alım: adım adım süreç
11. Tuzla'da okul, sağlık ve alışveriş rehberi `[DOĞRULA]`
12. Ayhanlar Mimarlık Yapı ve İnşaat: yapım anlayışı ve referanslar `[DOĞRULA]`

**Başlık dili ile kreatif dili ayrıdır.** Blog başlığı, SSS ve meta açıklama
**sorgunun kendi dilinde** yazılır — soru biçiminde olabilir, çünkü amaç
eşleşmektir ("1+1 daire yatırım mantıklı mı?"). Aynı yazıyı duyuran Instagram
karesi, ilan başlığı ve site kahraman alanı ise **her zaman olumlu** kalır.
Sorunun cevabı yazının ilk paragrafında ve olumlu olsun; "küçüktür ama…" diye
başlayan bir yazı, hedeflediği endişeyi pekiştirir. Ayrıntı: `olumlu-dil.md`
bölüm 5.

Yazı uzunluğu 800–1500 kelime, en az 2 özgün görsel, H2/H3 yapısı, sonunda
tek net çağrı. Yapay zekâ ile üretilmiş genel içerik yığmak bu segmentte işe
yaramaz — Google yararlı içerik güncellemeleriyle bunu eliyor ve marka
prestijine zarar veriyor. Her yazının içinde **kimsenin bilmediği bir gerçek**
olsun (gerçek mesafe, gerçek m², sahadan bir fotoğraf).

## 9. Ölçüm ve raporlama

**Aylık rapor iskeleti:**

1. Organik oturum ve organik lead sayısı (ikisi birlikte, ayrı ayrı anlamsız)
2. Marka vs. marka dışı arama trafiği ayrımı
3. İlk 10'a giren anahtar kelime sayısı ve hareket edenler
4. Google Business Profile: arama görüntülenmesi, yol tarifi, telefon araması
5. En çok lead getiren 5 sayfa
6. Core Web Vitals durumu
7. Gelecek ay yapılacaklar — 3 madde, fazlası dağıtır

Search Console'da **sorgu bazlı** takip yap; GA4 anahtar kelime vermez.
İlk 3 ayda hedef sıralama değil **indekslenme ve marka hakimiyeti** olmalı;
gerçek organik büyüme 4. aydan sonra konuşulur. Kullanıcıya bu takvimi baştan
ver, sonradan hayal kırıklığı olmasın.
