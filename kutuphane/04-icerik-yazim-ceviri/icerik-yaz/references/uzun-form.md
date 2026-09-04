# Uzun Form İçeriğin Mimarisi ve Okuyucuyu Tutma Tekniği

**Araştırma tarihi:** 26 Ağustos 2026
**Amaç:** 2000+ kelimelik, şişirilmemiş, sonuna kadar okunan metin üretecek bir yazım kılavuzunun kanıt tabanı.

## Kanıt Seviyesi Etiketleri

Bu dosyada her iddia şu üç etiketten biriyle işaretlenmiştir:

- **[BİRİNCİL]** — Google'ın kendi dokümantasyonu, akademik/laboratuvar çalışması, kontrollü deney. Doğrudan dayanak var.
- **[KORELASYON]** — Büyük veri setinden çıkarılmış istatistiksel ilişki. Nedensellik kanıtlamaz, metodolojik sınırları var.
- **[FOLKLOR]** — SEO topluluğunun yaygın kabulü, ama arkasında yayınlanmış kanıt yok veya kanıt yanlış okunmuş. Uygulanabilir olabilir, ama "kanıtlanmış" diye sunulmamalı.

---

## 1. KONU OTORİTESİ (Topical Authority)

### Kavramın gerçek dayanağı

**Google'ın "topical authority" diye adlandırdığı bir sıralama sistemi yok.** Google'ın sıralama sistemleri listesinde, spam politikalarında veya Search Central dokümantasyonunda bu terim geçmez. Terim SEO topluluğunun ürünü. **[FOLKLOR]**

Ancak kavramın altında yatan üç ayrı, gerçek şey var:

**a) Google'ın "kapsamlılık" sorusu — [BİRİNCİL]**
Google'ın "Creating helpful, reliable, people-first content" dokümanında kendi kendine değerlendirme sorularından biri şudur:

> "Does the content provide a substantial, complete, or comprehensive description of the topic?"

Yani Google bir konunun *kapsamlı* ele alınmasını açıkça soruyor — ama bunu "site genelinde konu otoritesi" olarak değil, sayfa bazında içerik kalitesi olarak çerçeveliyor.
Kaynak: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

**b) 2024 Content Warehouse API sızıntısı — [KORELASYON / DOĞRULANMAMIŞ]**
Mart 2024'te GitHub'a düşen ve Mayıs 2024'te Rand Fishkin tarafından yayınlanan 2.500+ sayfalık, 14.014 API özniteliği içeren iç dokümantasyonda konu odaklılığıyla doğrudan ilgili iki alan var:

- `siteFocusScore`: "Number denoting how much a site is focused on one topic."
- `siteRadius`: "Measure of how far page_embeddings deviate from the site_embedding."

Yani Google, sayfa vektörlerini site vektörüyle karşılaştırıp "bu sayfa sitenin ana konusundan ne kadar uzakta" diye ölçen bir mekanizmaya sahip. Bu, "konu otoritesi" fikrinin bulunan en somut teknik izidir.

**Kritik uyarı:** Sızıntı ağırlık bilgisi içermiyor, hangi alanların aktif kullanıldığını söylemiyor, bazıları açıkça "deprecated" işaretli ve dokümandaki en yeni tarih Ağustos 2023. Bir alanın API'de var olması sıralamada kullanıldığını kanıtlamaz.
Kaynaklar: https://sparktoro.com/blog/an-anonymous-source-shared-thousands-of-leaked-google-search-api-documents-with-me-everyone-in-seo-should-see-them/ ve https://ipullrank.com/google-algo-leak

**c) İç bağlantı yoğunluğu — [KORELASYON]**
HubSpot'un 2015 iç testi (Anum Hussain, Cambria Davies): ilgili sayfalar arasına ne kadar çok iç bağlantı eklendiyse, o sayfalar SERP'te o kadar yükseldi ve o kadar çok gösterim aldı. HubSpot bu testin sayısal sonuçlarını (kesin sıralama/trafik rakamları) hiç yayınlamadı — sadece bir dağılım grafiği paylaştı. Pillar/cluster modelinin tüm popülerliği büyük ölçüde bu tek, sayısı açıklanmamış iç teste dayanıyor.
Kaynak: https://blog.hubspot.com/marketing/topic-clusters-seo (aynı sayfa, HubSpot'un kendi blog yeniden yapılandırmasının etkisi için de rakam vermiyor)

### Pillar / cluster modeli pratikte

Model şu: bir "pillar" (sütun) sayfa konuyu geniş ve yüzeysel kapsar; her alt başlık için ayrı bir "cluster" sayfası derinleşir; cluster'lar pillar'a, pillar da cluster'lara bağlanır.

Ahrefs'in kendi pillar sayfası ("Beginner's Guide to SEO") ~2.900 aylık organik ziyaret alıyor ve 649 farklı domainden backlink kazanmış — modelin işlediğine dair somut ama tek bir örnek. **[KORELASYON]**
Kaynak: https://ahrefs.com/blog/internal-links-for-seo/

### "Bir konuyu kapatmak" ne demek

Uygulanabilir tanım — folklorik değil, arama davranışına dayanan:

> Bir konuyu kapatmak = o konuda arama yapan birinin, sizin sayfanızı okuduktan sonra **başka bir sekme açmasına gerek kalmaması**.

Bunu bir kontrol listesine çevirin:
1. Sorunun tanımı ve neden önemli olduğu
2. Doğrudan cevap (ilk 100 kelimede)
3. Nasıl yapılır / mekanizma
4. En az iki gerçek örnek veya vaka
5. Ne zaman *işe yaramaz* — sınırlar, istisnalar
6. Karşı görüş veya yaygın yanlış
7. Sonraki adım / ilgili konuya bağlantı

Bu yedi maddeyi karşılamayan "kapsamlı rehber" aslında kapsamlı değil, sadece uzun.

### Konu dışına çıkmanın maliyeti — [KORELASYON]
Ahrefs, sızıntıdaki `siteFocusScore`/`siteRadius` alanlarından hareketle "konu dışı içerik yayınlamak otorite sinyalinizi aktif olarak sulandırabilir" sonucunu çıkarıyor. Bu bir çıkarım, doğrulanmış bir kural değil. Buna dayanan bir gerçek vaka: SEO danışmanı Jes Scholz'un emlak sektöründeki müşterisi makalelerinin %60'ını sildi ve kalan içerikte "tıklamalarda kayda değer bir artış" gördü.
Kaynak: https://ahrefs.com/blog/content-decay/

---

## 2. UZUNLUK MİTİ

### Google'ın resmi açıklamaları — [BİRİNCİL]

En net ve alıntılanabilir iki cümle, Google'ın kendi dokümantasyonundan:

**SEO Starter Guide:**
> "The length of the content alone doesn't matter for ranking purposes (there's no magical word count target, minimum or maximum, though you probably want to have at least one word)."

Kaynak: https://developers.google.com/search/docs/fundamentals/seo-starter-guide

**Creating Helpful Content — kaçınılması gereken davranışlar listesinde:**
> "Are you writing to a particular word count because you've heard or read that Google has a preferred word count? (No, we don't.)"

Kaynak: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

Yani kelime sayısı hedefi belirlemek, Google'ın kendi listesinde *kötü* içerik göstergesi olarak sayılıyor.

### Korelasyon çalışmaları ve metodolojik sorunları

**Backlinko / 11,8 milyon sonuç — [KORELASYON]**
En çok alıntılanan rakam buradan geliyor: "Google ilk 10 sonucunun ortalama kelime sayısı 1.447."

Ama aynı çalışma şunu da söylüyor: kelime sayısı ile *sıralama pozisyonu* arasında doğrudan bir ilişki bulunamadı; kelime sayısı 1-10 pozisyonları arasında eşit dağılmış. Yazarların kendi ifadesi:

> "This being a correlation study, it's impossible for us to pinpoint why long-form content tends to appear on Google's first page."

Kaynak: https://backlinko.com/search-engine-ranking

**Metodolojik sorunlar — bu tür çalışmaların neden yanıltıcı olduğu:**

1. **Ters nedensellik.** Uzun içerik sıralamıyor; sıralayan konular (rehber, karşılaştırma, "nasıl yapılır") doğaları gereği uzun yazılıyor. Sorgu tipi hem uzunluğu hem sıralamayı belirliyor.
2. **Seçilim yanlılığı.** İlk 10'a giren siteler zaten yüksek otoriteli, bütçeli, editörlü siteler. Uzunluk, kaynak zenginliğinin bir *belirtisi*.
3. **Ortalama medyanı gizler.** "Ortalama 1.447 kelime" içinde 400 kelimelik tanım sayfaları ile 6.000 kelimelik rehberler aynı havuzda. Sorgu tipine göre ayrıştırılmadan ortalama anlamsız.
4. **Pozisyon içi dağılım düz.** Backlinko'nun kendi verisinde 1. ile 10. sıra arasında uzunluk farkı yok — bu, uzunluğun bir sıralama *kaldıracı* olmadığının en güçlü göstergesi.

**Sızıntıdan gelen ters yönlü kanıt — [DOĞRULANMAMIŞ ama dikkate değer]**
API dokümanında `numTokens` alanıyla ilgili not: Google indeksleme sırasında dokümanları "max cap"te kesiyor. Ayrıca `originalContentScore`: "7-bits, going from 0 to 127. Only pages with little content have this field." — yani kısa sayfalar özgünlük için ayrıca skorlanıyor. İkisi birlikte şunu ima ediyor: aşırı uzunluk sonuna eklenen kısımların hiç değerlendirilmemesine yol açabilir, kısa olmak ise otomatik ceza değil.
Kaynak: https://ipullrank.com/google-algo-leak

### Ne zaman uzun, ne zaman kısa — [BİRİNCİL]

Nielsen Norman Group'un "information foraging" (bilgi arayışı) hesabı bu soruya en iyi çerçeveyi veriyor. Okuyucu, harcadığı zamana karşılık aldığı fayda oranını optimize ediyor:

- **Kısa içerik (600 kelime / 3 dk):** saatte 105 fayda birimi
- **Uzun içerik (1.000 kelime / 5 dk):** saatte 100 fayda birimi
- **Uzmanlaşmış ihtiyacı olan okuyucu için uzun içerik:** saatte 167 fayda birimi
- **Karma strateji (kısa özet + derin kaynak birlikte):** saatte 181 fayda birimi — en yüksek

Nielsen'in editör kuralı:
> "A good editor should be able to cut 40% of the word count while removing only 30% of an article's value."

Kaynak: https://www.nngroup.com/articles/content-strategy-long-vs-short/

**Pratik karar kuralı:**

| Uzun yaz (2000+) | Kısa yaz (400-900) |
|---|---|
| Karar destekleyici sorgu ("X mi Y mi", "nasıl seçilir") | Tanım sorgusu ("X nedir") |
| Süreç/uygulama rehberi, adım adım | Tek bir gerçeğe cevap ("ne zaman açılıyor") |
| Tartışmalı konu, karşı görüş gerektiren | İşlemsel sorgu (satın alma, giriş) |
| Okuyucu zaten bağlı ve derinlik arıyor | Okuyucu acele ediyor, tek bilgi istiyor |
| Konuyu "kapatmak" stratejik hedefse | Konu zaten başka sayfada kapatılmışsa |

**Ve en önemlisi:** Google'ın spam politikalarında "scaled content abuse" tanımı — "many pages are generated for the primary purpose of manipulating search rankings and not helping users" — uzunluk için doldurma yapmanın doğrudan riskli tarafını gösteriyor.
Kaynak: https://developers.google.com/search/docs/essentials/spam-policies

---

## 3. YAPI DESENLERİ

Hangi yapı hangi arama amacına uyar — bu eşleştirme, uzun metnin en kritik mimari kararıdır.

### a) Ters Piramit (Inverted Pyramid) — [BİRİNCİL destekli]
En önemli bilgi (hatta sonuç) en başta; aşağı doğru detay incelir.

NN/g'nin web için gerekçesi: okuyucu dikkatle okumuyor, taramada herhangi bir noktada bırakabilir; ters piramitte **nerede bırakırsa bıraksın ana fikri almış olur**. Ayrıca metin herhangi bir noktadan kesilebilir, kritik bilgi kaybolmaz.
Kaynak: https://www.nngroup.com/articles/inverted-pyramid/

**Uygun olduğu amaç:** Bilgilendirici sorgu, haber, "X nedir/nasıl olur", öne çıkan snippet hedefi.

### b) PAS — Problem / Agitate / Solve
Sorunu tanımla → sorunun bedelini büyüt → çözümü sun. Kökeni doğrudan yanıt (direct response) reklamcılığı; Copyblogger'da Demian Farnworth tarafından popülerleştirildi.

Farnworth'un kendi örnek metni:
> "Insecure? You're not alone. Millions of people admit to being insecure. Yet, remain that way and you'll live a life in the shadows. A life on the fringe. Always wishing, never doing. Fortunately, there's an answer."

Kaynak: https://copyblogger.com/problem-agitate-solve/

**Uygun olduğu amaç:** Ticari araştırma, ikna edici sayfa, satış odaklı uzun metin. **Uygun olmadığı yer:** referans/dokümantasyon içeriği — orada "agitate" adımı okuyucuyu sinirlendirir.

### c) Hikaye → Analiz → Sonuç
Somut bir vaka ile aç, vakadan genel ilkeyi çıkar, uygulanabilir sonuca bağla. Gazetecilikte "feature lede + nut graf" yapısının uzun form karşılığı.

**Uygun olduğu amaç:** Vaka çalışması, sektör analizi, tecrübe aktarımı (E-E-A-T'nin "Experience" ayağını en güçlü gösteren yapı).

### d) Kronolojik anlatı
Zaman çizgisi boyunca ilerler. **Uygun olduğu amaç:** "X'in tarihi", olay/kriz anlatısı, süreç kaydı, "biz nasıl yaptık" günlüğü. **Riski:** Ters piramide taban tabana zıt — ana bulgu sona düşer, tarama okurunu kaybeder. Çözüm: kronolojinin başına bir nut graf koyun.

### e) Karşılaştırma tablosu merkezli
Metin tabloyu kurar, tablo kararı verir, metin tablodaki her satırı açar.
**Uygun olduğu amaç:** "X vs Y", "en iyi N", araç/ürün seçimi. Bu sorgu tipinde tabloyu yukarı almak, metnin geri kalanını okumaya niyeti olmayan okuyucuya da değer verir.

### f) SSS (Sık Sorulanlar) bölümü
Metnin *sonunda*, ana akışa sığmayan ama arama hacmi olan yan soruları toplar. Uzun kuyruk sorguları ve snippet fırsatı için etkili. Semrush verisi: 10 kelimelik sorguların %55,5'i öne çıkan snippet tetikliyor (tek kelimelik sorgularda bu oran %4,3) — SSS bölümleri tam bu uzun sorgu bandını hedefler. **[KORELASYON]**
Kaynak: https://www.semrush.com/blog/featured-snippet/

**Uyarı — [FOLKLOR]:** "SSS şemasıyla SERP'te ekstra alan kaplama" taktiği artık büyük ölçüde geçersiz; Google FAQ rich result gösterimini 2023'te ciddi biçimde daralttı. SSS bölümünü okuyucu için yazın, şema için değil.

---

## 4. GİRİŞ PARAGRAFI

### İyi bir giriş ne yapar

Üç iş, bu sırayla:
1. **Cevabı verir veya vaadi netleştirir** (lede)
2. **Neden şimdi ve neden önemli olduğunu söyler** (nut graf)
3. **Metnin ne kapsadığını ima eder** (kapsam sözü)

### Gazetecilikten gelen kavramlar

**Lede:** Metnin ilk cümlesi/paragrafı. Beş N bir K'yı hızlıca cevaplar ve okuyucuyu tutar.

**Burying the lede:** Asıl haberi aşağı gömmek. Web'de bunun bedeli ölçülmüş: NN/g eye-tracking verisine göre sayfa görüntüleme süresinin **%42'den fazlası sayfanın üst %20'sinde**, **%65'ten fazlası üst %40'ında** geçiyor. Ana fikri 4. paragrafa gömerseniz, okuyucuların çoğu onu hiç görmez.
Kaynak: https://www.nngroup.com/articles/scrolling-and-attention/

**Nut graf (nutshell paragraph):** Lede'den sonra gelen, genellikle ikinci veya üçüncü paragraf. Hikâyeyi bağlama oturtur.
> "The nut graph tells audiences why the story is important and timely... explaining where the story is coming from, where it is going, and what is at stake." (Zamith, 2022)

Kaynak: https://en.wikipedia.org/wiki/Nut_graph

### Kaç kelime

Kanıta dayanan sınır: NN/g'ye göre kullanıcılar ortalama bir ziyarette metnin **en fazla %28'ini** okuyabiliyor, **%20 daha muhtemel**. Bir sayfanın bilgisinin yarısının okunması ancak **111 kelime veya altındaki** sayfalarda gerçekleşiyor.
Kaynak: https://www.nngroup.com/articles/how-little-do-users-read/

**Pratik kural:** Giriş bloğu 50-120 kelime. İlk cümle 15-20 kelimeyi geçmesin. Ana cevap ilk 100 kelime içinde tamamlanmış olsun.

### "Hadi başlayalım" tipi girişler neden kötü

Kötü giriş kalıpları ve neden başarısız oldukları:

| Kalıp | Sorun |
|---|---|
| "Günümüz dijital dünyasında..." | Sıfır bilgi. Okuyucunun zaten bildiği bir şeyi söylüyor. |
| "Bu yazıda X hakkında her şeyi öğreneceksiniz. Hadi başlayalım!" | Vaat var, teslimat yok. Cevabı erteliyor. |
| "X, birçok kişinin merak ettiği bir konudur." | Merakı doğrulamak bilgi değil. |
| Sözlük tanımıyla açmak | Okuyucu tanımı biliyor; bilmiyorsa bile bu snippet'te zaten var. |
| Kişisel uzun anekdot (nut graf'sız) | Klasik "burying the lede". |

**Kural:** Giriş paragrafından "Bu yazıda" ve "Hadi başlayalım" ifadelerini silin. Silince paragraf bilgi kaybediyorsa paragraf zaten iyiydi; kaybetmiyorsa paragraf boştu.

### Şablon: kanıta uygun giriş

```
[Cümle 1 — DOĞRUDAN CEVAP, 15-20 kelime, snippet'e uygun.]
[Cümle 2-3 — NUT GRAF: neden önemli, ne zaman geçerli, ne kadarlık bir fark yaratıyor. Sayı içersin.]
[Cümle 4 — KAPSAM: bu metnin neyi kanıtladığı ve neyi kanıtlamadığı.]
```

**Uygulanmış örnek:**

> Kelime sayısı bir sıralama faktörü değil; Google bunu kendi başlangıç rehberinde açıkça yazıyor. Buna rağmen ilk 10 sonucun ortalama uzunluğu 1.447 kelime — çünkü uzun yazılan konular ile sıralayan konular büyük ölçüde aynı konular. Aşağıda bu iki gerçeğin nasıl bir arada durduğunu, hangi sorgu tipinde uzun yazmanın işe yaradığını ve hangi durumda 600 kelimenin daha iyi performans verdiğini ölçülmüş verilerle ayırıyorum.

Bu giriş 71 kelime, ilk cümlede cevabı veriyor, ikinci cümlede karşı veriyi ve gerilimi kuruyor, üçüncüde kapsam sözü veriyor. "Hadi başlayalım" yok.

---

## 5. BAŞLIK HİYERARŞİSİ

### Google ne diyor — [BİRİNCİL]

Google'ın SEO Starter Guide'ı iki şeyi netleştiriyor:

> "no magical, ideal amount of headings a given page should have"

ve sıra konusunda:

> "from Google Search perspective, it doesn't matter if you're using them out of order"

Ama aynı doküman şunu tavsiye ediyor:
> "Break up long content into paragraphs and sections, and provide headings to help users navigate your pages."

Kaynak: https://developers.google.com/search/docs/fundamentals/seo-starter-guide

Yani: **H2/H3 sırası SEO için değil, erişilebilirlik ve okunabilirlik için önemli.** "H1 atlanırsa Google cezalandırır" iddiası **[FOLKLOR]**.

### Erişilebilirlik tarafı gerçek — [BİRİNCİL]

WebAIM'in ekran okuyucu kullanıcı anketinde, uzun bir sayfada bilgi ararken ilk yaptığı şey olarak **%71,6'sı "sayfadaki başlıklar arasında gezinmek"** diyor. Bu oran zaman içinde artmış ve baskın yöntem olmayı sürdürüyor.
Kaynak: https://webaim.org/projects/screenreadersurvey10/

WebAIM'in yapısal kuralı: sayfada tipik olarak tek `<h1>`, ve
> "it does not make sense to skip heading levels, such as from `<h2>` to `<h4>`, going down the page."

Kaynak: https://webaim.org/techniques/semanticstructure/

### İskelet testi

**Kural:** Yalnızca H2 ve H3'leri arka arkaya okuduğunuzda, metnin argümanı anlaşılmalı. Anlaşılmıyorsa başlıklar etiket, iskelet değil.

Kötü başlık dizisi (etiketler):
```
Giriş / Nedir? / Faydaları / Nasıl Yapılır / Sonuç
```
İyi başlık dizisi (iskelet):
```
Kelime sayısı sıralama faktörü değil — Google iki ayrı dokümanda bunu yazıyor
1.447 kelime rakamı nereden geliyor ve neden yanıltıcı
Uzun yazmanın gerçekten kazandırdığı üç sorgu tipi
600 kelimenin 2.000 kelimeyi yendiği durum
Doldurmanın ölçülmüş bedeli: okuyucu nerede bırakıyor
```

### Soru mu, ifade mi

- **Soru başlık** kullanın: sorgu doğrudan soru formundaysa ("neden", "nasıl", "-mi") ve snippet hedefliyorsanız. Semrush verisi: "why" sorularının %77,6'sı, "can" sorularının %72,4'ü snippet tetikliyor. **[KORELASYON]**
- **İfade başlık** kullanın: bölüm bir bulgu veya iddia sunuyorsa. İfade başlık iskelet testini geçer, soru başlık geçmez (soru bilgi taşımaz, cevabı taşımaz).
- **Karışık kullanın:** ana bölümlerde ifade (H2), SSS'de soru (H3).

NN/g'nin biçimlendirme kuralı: alt başlıklar ve madde işaretleri **"information-carrying words"** ile başlamalı — yani başlığın ilk 2-3 kelimesi ayırt edici olmalı, çünkü F deseninde okunacak tek kısım o.
Kaynak: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/

### İçindekiler listesi ne zaman işe yarar

- **Yarar:** 1.500+ kelime, referans niteliğinde, okuyucunun belirli bir bölüme atlamak isteyeceği içerik (dokümantasyon, uzun rehber, karşılaştırma).
- **Yaramaz:** anlatı yapısı, ikna metni, kronolojik hikâye — okuyucunun sırayla okuması gereken metinde içindekiler kaçış rampası olur.
- **Sıklık kuralı:** her 250-350 kelimede bir alt başlık. Bir başlık altında 400 kelimeden fazla kesintisiz metin varsa ya bölün ya kesin.

---

## 6. KISA CEVAP KUTULARI (Direct Answer)

### Google resmi olarak ne diyor — [BİRİNCİL]

İki resmi açıklama, iki farklı yanlış anlamayı düzeltiyor:

**Öne çıkan snippet için işaretleme yapılamaz.** Google'ın kendi dokümanı, "snippet için nasıl işaretleme yaparım" sorusuna verdiği cevap:
> "You can't."

ve seçim süreci:
> "Google systems determine whether a page would make a good featured snippet for a user's search request, and if so, elevates it."

Kaynak: https://developers.google.com/search/docs/appearance/featured-snippets

**AI Overviews için özel optimizasyon yok.**
> "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary."
> "You don't need to create new machine readable files, AI text files, or markup to appear in these features."

Tek teknik koşul:
> "To be eligible to be shown as a supporting link in AI Overviews or AI Mode, a page must be indexed and eligible to be shown in Google Search with a snippet."

Kaynak: https://developers.google.com/search/docs/appearance/ai-features

Yani "GEO/AEO optimizasyonu" adı altında satılan teknik kontrol listelerinin çoğu **[FOLKLOR]**.

### Ölçülmüş yapı — [KORELASYON]

Buna rağmen snippet'e giren metinlerin biçimsel ortak özellikleri ölçülmüş:

- **Uzunluk:** ~40-50 kelime / 250-300 karakter
- **Tip dağılımı:** paragraf %70, liste ~%26, tablo ~%3,4, video %4,6
- Kaynak: https://www.semrush.com/blog/featured-snippet/

- **Pozisyon:** Ahrefs'in ~2 milyon snippet incelemesinde, snippet'lerin yalnızca **%30,9'u** o sorguda 1. sırada olan sayfadan geliyor; ama Google'ın snippet'i **%99,58 oranında ilk 10'daki bir sayfadan** aldığı bulundu.
- Kaynak: https://ahrefs.com/blog/featured-snippets-study/

### Snippet'in gerçek trafik etkisi — [KORELASYON, karşı bulgu]

Bu, SEO folklorunun en çok atladığı veri: **öne çıkan snippet almak tıklama kaybettirebilir.**

Ahrefs'in ölçümü: snippet'li bir SERP'te snippet'in kendisi tıklamaların ~%8,6'sını, hemen altındaki ilk organik sonuç ~%19,6'sını alıyor. Snippet olmayan bir SERP'te 1. sıra ~%26 alıyor. Yani snippet, 1. sıradaki sayfanın tıklamasını yiyor.
Kaynak: https://ahrefs.com/blog/featured-snippets-study/

**AI Overviews etkisi:** Ahrefs'in 300.000 anahtar kelimelik (150.000 AI Overview'lu / 150.000 AI Overview'suz) Mart 2024 - Mart 2025 karşılaştırması: AI Overview varlığı, üst sıradaki sayfalar için **%34,5 CTR düşüşüyle** korele. Bilgilendirici sorgularda 1. sıra CTR'ı 0,073'ten 0,026'ya inmiş.
Kaynak: https://ahrefs.com/blog/ai-overviews-reduce-clicks/

**Stratejik sonuç:** Kısa cevap kutusu yazmanın gerekçesi "snippet kapmak" olmamalı — çünkü snippet net trafik kaybettirebilir. Gerekçe şu olmalı: **okuyucunun ilk 10 saniyede cevabı alıp kalmayı seçmesi.** Cevabı vermeyen metin zaten okunmuyor.

### Şablon: direct answer bloğu

```markdown
## [Soru, tam olarak sorulduğu haliyle]

[CEVAP CÜMLESİ — sorunun anahtar kelimelerini içerir, 15-25 kelime,
koşul veya "duruma göre değişir" ile başlamaz.]
[GEREKÇE — 2-3 cümle, bir sayı ve bir kaynak içerir, toplam 40-50 kelime.]

[Sonra: nüans, istisna, derinlik — snippet bloğunun DIŞINDA.]
```

**Uygulanmış örnek:**

> **Bir blog yazısı kaç kelime olmalı?**
> Sabit bir hedef yoktur; uzunluğu sorgu tipi belirler, kelime sayısı Google için sıralama faktörü değildir. Google'ın başlangıç rehberi bunu açıkça yazıyor: "there's no magical word count target, minimum or maximum". Pratikte tanım sorguları 400-900 kelimede, karar destekleyici rehberler 1.800-3.000 kelimede en iyi performansı veriyor.

Konum kuralı: bu blok ya girişin hemen ardında (ana sorgu için) ya da ilgili H2'nin hemen altında (alt sorgu için) olmalı. Bir "sonuç" bölümünde bekletilmemeli.

---

## 7. OKUYUCUYU TUTMA: ÖLÇÜLMÜŞ VERİ

### İnsanlar nerede bırakıyor — [BİRİNCİL/KORELASYON]

**Chartbeat scroll derinliği (Slate analizi, 2013):**
- %38 hiç etkileşime girmeden hemen ayrılıyor
- Kalanların %5'i hiç kaydırma yapmıyor
- **Medyan kaydırma derinliği: makalenin %50'si** (Slate'te), Chartbeat'in izlediği siteler genelinde %60
- Okuyucuların yalnızca **%25'i 1.600 pikselin ötesine** geçiyor
- Slate'te sürenin %86,2'si "fold" altında geçiyor (diğer sitelerde ~üçte iki)
- Josh Schwartz: "We generally see that higher-quality content causes people to scroll further"
- Ve kritik bulgu: **kaydırma derinliği ile paylaşım arasında çok zayıf ilişki var** — çok paylaşılan yazı okunmuş demek değil.

Kaynak: https://slate.com/technology/2013/06/how-people-read-online-why-you-wont-finish-this-article.html

**Chartbeat / Tony Haile (Time, 2014):**
- "**55% spent fewer than 15 seconds actively on a page**"
- Makalelerde her üç ziyaretçiden biri 15 saniyeden az okuyor
- 10.000 sosyal paylaşılan makale incelemesi: "there is no relationship whatsoever between the amount a piece of content is shared and the amount of attention an average reader will give that content"
- Ama: "if you can hold a visitor's attention for just three minutes they are **twice as likely to return** than if you only hold them for one minute"

Kaynak: https://time.com/12933/what-you-think-you-know-about-the-web-is-wrong/

Bu son bulgu uzun formun asıl iş gerekçesi: uzunluk sıralama getirmiyor ama **tutulan dikkat geri dönen okuyucu getiriyor.**

**NN/g dikkat dağılımı (2018, 120 katılımcı, 130.000+ göz sabitlemesi):**
- Sürenin **%57'si fold üstünde**
- İlk iki ekran dolusunda (2160px'e kadar) sürenin %74'ü
- Sayfanın üst %20'sinde sürenin %42'sinden fazlası
- Üst %40'ında %65'ten fazlası
- 2010'a göre iyileşme var: o zaman süre %80 fold üstündeydi

Kaynak: https://www.nngroup.com/articles/scrolling-and-attention/

### F deseni: hâlâ geçerli mi — [BİRİNCİL]

**Orijinal çalışma (2006):** 232 kullanıcı, binlerce sayfa. Bulgu: üstte yatay tarama, aşağıda daha kısa ikinci yatay tarama, solda dikey tarama.
Kaynak: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/

**11 yıl sonraki tekrar (2017):** Desen doğrulandı — "the F-shaped scanning pattern is alive and well in today's world — both on desktop and on mobile."

Ama en önemli nüans şu:
> "The F-pattern is the default pattern when there are no strong cues to attract the eyes towards meaningful information."

Yani **F deseni bir okuma tarzı değil, kötü biçimlendirmenin semptomu.** NN/g'nin ifadesiyle: "good web formatting reduces the impact of F-scanning."

NN/g'nin önerdiği düzeltmeler:
- En önemli noktaları **ilk iki paragrafa** koymak
- Bilgi taşıyan kelimelerle başlayan belirgin başlıklar
- Kritik terimleri **kalın** yapmak
- Madde ve numaralı listeler
- Gereksiz içeriği silmek
- İlke: "Do the work for the users instead of forcing them to exert effort and take bad shortcuts."

Kaynak: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/

### Biçimlendirmenin ölçülmüş etkisi — [BİRİNCİL, 1997 ama hâlâ en net deney]

NN/g'nin 5 versiyonlu kontrollü çalışması. Aynı bilgi, farklı yazım/sunum. Kullanılabilirlik iyileşmesi:

| Değişiklik | İyileşme |
|---|---|
| Özlü metin (concise) | **%58** |
| Taranabilir düzen (scannable) | **%47** |
| Nesnel dil (objective, pazarlama dilinden arındırılmış) | **%27** |
| Üçü birden | **%124** |

Ayrıca: kullanıcıların **%79'u her yeni sayfayı tarıyor; yalnızca %16'sı kelime kelime okuyor.**
Kaynak: https://www.nngroup.com/articles/how-users-read-on-the-web/

Dikkat: "nesnel dil %27 iyileştirdi" bulgusu, uzun form içeriğe doğrudan uygulanabilir — abartılı sıfatları ("inanılmaz derecede güçlü", "devrim niteliğinde") silmek ölçülmüş bir kazanç.

### Biçim kuralları (verilerden türetilmiş)

| Öğe | Kural | Dayanak |
|---|---|---|
| Paragraf uzunluğu | 2-4 cümle, 40-70 kelime | Tarama davranışı, F deseni |
| Alt başlık sıklığı | Her 250-350 kelimede bir | %71,6 başlıkla geziniyor |
| İlk 2 paragraf | Ana fikri taşımalı | %42 süre üst %20'de |
| Kalın kullanımı | Paragraf başına en fazla 1 ifade | Aşırısı hiçbir şeyi vurgulamaz |
| Liste | 5-7 madde; her madde bilgi taşıyan kelimeyle başlar | NN/g biçimlendirme |
| Cümle uzunluğu | Ortalama 15-20 kelime, ritim değişken | Okuma hızı ~250 wpm |
| Görsel/tablo | Her 500-700 kelimede bir kırılma | Fold altı dikkat düşüşü |

---

## 8. KANIT VE SOMUTLUK

Uzun metni sıkıcı olmaktan kurtaran şey uzunluğu değil, **birim kelime başına düşen yeni bilgi yoğunluğu**dur. Nielsen'in fayda/maliyet hesabı tam olarak bunu ölçüyor: okuyucu, harcadığı zamanın karşılığını alamadığında bırakıyor.

### Somutluk ölçeği

Aynı iddianın beş somutluk seviyesi:

| Seviye | Örnek | Değeri |
|---|---|---|
| 0 — Soyut | "Uzun içerik her zaman daha iyi sıralamaz." | Sıfır. Herkes söylüyor. |
| 1 — Nitel gerekçe | "Çünkü Google kelime sayısına bakmıyor." | Düşük. Doğrulanamaz. |
| 2 — Sayı | "İlk 10 sonucun ortalaması 1.447 kelime ama pozisyonlar arasında fark yok." | Orta. |
| 3 — Sayı + kaynak | "Backlinko'nun 11,8 milyon sonuç incelemesinde..." | Yüksek. |
| 4 — Sayı + kaynak + karşı görüş | "...ancak bu bir korelasyon çalışması; yazarlar 'impossible for us to pinpoint why' diyor." | En yüksek. |

**Kural:** 2000+ kelimelik bir metinde her H2 bölümü en az bir kez Seviye 3'e çıkmalı; metnin tamamında en az bir kez Seviye 4'e çıkmalı.

### Bir iddiayı kanıtlama biçimleri (etki sırasına göre)

1. **Kontrollü deney** — En güçlü. Örnek: Reboot Online'ın 5 aylık dış bağlantı deneyi (aşağıda, bölüm 9).
2. **Birinci el gözlem / kendi veriniz** — "Kendi 41 yazımızı güncelledik, medyan artış %X." Kimsede olmayan veri.
3. **Birincil kaynaktan doğrudan alıntı** — Google dokümanından *tam cümle*, parafraz değil.
4. **Büyük ölçekli korelasyon** — Metodolojik sınırı belirtilerek.
5. **Vaka çalışması** — Tek örnek; "kanıt" değil "örnek" diye sunulmalı.
6. **Uzman görüşü** — İsim, kurum, tarih olmadan değersiz.

### "Show, don't tell" pratiği

**Tell:** "Kötü girişler okuyucuyu kaçırır."
**Show:** "'Günümüz dijital dünyasında' ile başlayan bir giriş, okuyucunun ilk 15 saniyesini — Chartbeat'e göre ziyaretçilerin %55'inin sahip olduğu tüm süreyi — hiçbir bilgi vermeden tüketir."

Fark: ikincisi bir mekanizma gösteriyor ve ölçülmüş bir sayıya bağlıyor.

### Somutluk kontrol listesi

Her bölüm için sorun:
- [ ] Bu bölümde bir **sayı** var mı? (yüzde, adet, tarih, süre, para)
- [ ] Bir **isim** var mı? (kişi, kurum, ürün, çalışma adı)
- [ ] Bir **tarih** var mı? (bulgunun ne zaman geçerli olduğu)
- [ ] Bir **doğrudan alıntı** var mı? (parafraz değil)
- [ ] Bu iddianın **yanlış olabileceği bir durum** belirtilmiş mi?
- [ ] Bu paragrafı silsem okuyucu bir şey kaybeder mi? (Hayır ise silin.)

Son madde en önemlisi. "Şişirilmemiş uzun metin"in operasyonel tanımı budur: **her paragraf silinebilirlik testinden geçmiş metin.**

### Karşı görüş kullanmak

Karşı görüş, uzun formda iki iş yapar: metni inandırıcı kılar ve okuyucuyu ilerletir (gerilim yaratır). Yapı:

```
[İddia] → [En güçlü karşı argüman, dürüstçe] → [Karşı argümanın nerede geçerli olduğu]
→ [Yine de neden ana iddianın geçerli kaldığı, veya iddianın daraltılması]
```

Karşı argümanı zayıflatarak sunmak (straw man) okuyucunun güvenini tam da somutluk kazandığı yerde kaybettirir.

---

## 9. İÇ BAĞLANTI

### Kaç bağlantı, nereye

**Ahrefs'in önerisi:** makale başına **3-5 bağlamsal iç bağlantı** başlangıç noktası; içeriğin uzunluğuna göre ölçeklenir. Gerekçe: her bağlantı diğerlerinden geçen PageRank'i seyreltir. **[FOLKLOR + kısmi mekanizma]** — PageRank seyrelmesi gerçek bir mekanizma, ama "3-5" sayısı deneysel değil, sezgisel bir tavsiye.
Kaynak: https://ahrefs.com/blog/internal-links-for-seo/

Aynı sayfada John Mueller'a atfedilen ifade:
> "Internal linking is super critical for SEO. It's one of the biggest things you can do on a website to guide Google"

**Pratik kural (uzun form için):** her 400-500 kelimede en fazla 1 iç bağlantı; toplamda 2000 kelimelik yazıda 4-8 arası. Bağlantılar metnin *içine*, ilgili cümleye gömülmeli — sonda "İlgili yazılar" bloğuna yığılmamalı (o blok kaydırma derinliği %50 medyanının altında kalır, çoğu okuyucu görmez).

### Çapa metni (anchor text)

Google'ın resmi ifadesi — [BİRİNCİL]:
> "This text tells users and Google something about the page you're linking to. With appropriate anchor text, users and search engines can easily understand what your linked pages contain."

Kaynak: https://developers.google.com/search/docs/fundamentals/seo-starter-guide

Kurallar:
- **"Buraya tıklayın", "daha fazlası", "bu yazı"** kullanmayın — bilgi taşımıyor.
- Betimleyici olun: "e-posta segmentasyonu rehberimiz" gibi.
- **Çeşitlendirin:** aynı sayfaya farklı varyasyonlarla bağlanın; aynı çapa metnini onlarca kez tekrarlamak hem doğal durmaz hem tek anahtar kelimeye kilitler.
- Çapa metni bağlantı verilen sayfadaki H1 ile birebir aynı olmak zorunda değil, ama o sayfanın vaadini karşılamalı.

### Aşırı bağlantının zararı

İki ayrı zarar mekanizması:
1. **PageRank seyrelmesi** — mekanizma gerçek, etkisi ölçülmemiş.
2. **Okuma akışının kırılması** — her bağlantı okuyucuya bir "ayrılma kapısı" sunar. Uzun formda scroll derinliği medyanı zaten %50-60; ilk üçte birde çok sayıda bağlantı bu medyanı düşürür. Bu, ölçülmüş scroll verisinden çıkan pratik bir sonuç.

**Kural:** Girişte (ilk 200 kelime) hiç iç bağlantı vermeyin. Okuyucuyu önce metne bağlayın.

### Dış kaynağa bağlantı — kanıt var mı?

**Evet, kontrollü bir deney var — [BİRİNCİL].**

Reboot Online, Şubat 2016'da 5 aylık bir deney yürüttü:
- 10 yeni domain, aynı 300 kelimelik makale, uydurma bir ürün adı ("Phylandocic")
- 5 site otoriter kaynaklara (Oxford, Cambridge, Genome Research Institute) followed dış bağlantı verdi; 5 site hiç dış bağlantı vermedi
- Kontrol kelimesi ("Ancludixis") bağlantısız eklendi
- Domainler aynı anda kaydedildi, farklı IP'lerden gönderildi, günlük pozisyon takibi yapıldı

**Sonuç:** Dış bağlantı veren siteler tutarlı biçimde daha yüksek sıraladı. Etki sadece çapa metnindeki kelimede değil, sayfanın genelinde görüldü. Araştırmacıların sonucu: "outgoing relevant links to authoritative sites are considered in the algorithms and do have a positive impact on rankings."
Kaynak: https://www.rebootonline.com/blog/long-term-outgoing-link-experiment/

**Sınırları:** N=10, tek deney, 2016 tarihli, uydurma kelime üzerinde — rekabetsiz ortam. Yine de "PageRank'i dışarı sızdırma" (link hoarding) folklorunu doğrudan test eden ve çürüten nadir kontrollü çalışmalardan biri.

**Uygulanabilir sonuç:** Kanıt gerektiren her iddiada kaynağa doğrudan bağlantı verin. Bu hem okuyucu güveni hem — bu deneye göre — muhtemel bir sıralama faydası.

---

## 10. GÜNCELLEME (Content Refresh)

### Ne zaman güncellenir

**Güncelleyin:**
- Sayfa ilk 10'da ama düşüş trendinde (klasik "content decay")
- İçindeki veriler/ekran görüntüleri/fiyatlar eskimiş
- Arama amacı kaymış ama sizin açınız hâlâ yakın
- Rakipler daha kapsamlı sürüm yayınlamış

**Güncellemeyin — Ahrefs'in kriterleri [KORELASYON]:**
- Keyword Difficulty yüksekse (eşik olarak KD<40 öneriliyor): sorun içerik kalitesi değil, **bağlantı otoritesi açığı**. İçeriği güncellemek çözmez.
- Trafiği ve backlink'i düşük, düşük değerli anahtar kelimeler: güncellemek değil, **budamak** (prune) gerekir.
- Arama amacı içeriğinizin yaklaşımından tamamen kaymışsa: güncelleme değil, yeniden yazma veya yönlendirme.

Kaynak: https://ahrefs.com/blog/content-decay/

### Ölçülmüş sonuçlar — [KORELASYON, tekil vakalar]

Ahrefs'in kendi blogundan iki vaka:
- 2018 tarihli "link reclamation" yazısı Ağustos 2024'te baştan yazıldı ve yeniden yayınlandı: organik trafik **ikiye değil üçe katlandı (%302 artış)**.
- On-page SEO yazısı, Ağustos 2025 civarı güncellendi: **%36 organik trafik artışı**.

Ahrefs'in kendi uyarısı önemli: bu güncellemeler **anlamlı içerik değişikliği** içeriyordu, sadece yayın tarihi değiştirmek değil — "Google spent a lot of time refining how it handles [updates]".
Kaynak: https://ahrefs.com/blog/republishing-content/

Buffer'ın süreç otomasyonu vakası: tazeleme hızını dörde katladılar, "maliyetin çok altında %25 daha fazla makale" bitirdiler ve çoğu parçada "immediate, sustained upticks in traffic" gördüler.
Kaynak: https://ahrefs.com/blog/content-decay/

### Güncelleme tarihi göstermek — [BİRİNCİL]

Google'ın resmi rehberi tarihleri açıkça destekliyor. Önerdiği görünür format:
> "Posted Feb 4, 2019" veya "Last updated: Feb 14, 2018"

Ve yapısal veri: `datePublished` / `dateModified` (Article, BlogPosting, VideoObject).

**Google'ın açık uyarıları:**
> "Don't specify future dates, or the date of the action described on the page."
> "Make your dates and times consistent. Ensure that the date (and optional time and timezone) match between the equivalent user-visible and structured values."
> "Minimize the presence of other dates on the page"

Kaynak: https://developers.google.com/search/docs/appearance/publication-dates

**Sızıntıdan gelen destekleyici detay — [DOĞRULANMAMIŞ]:** Google üç ayrı tarih türü çıkarıyor: `bylineDate` ("date that will be shown in the snippets"), `syntacticDate` ("date explicitly mentioned in URL or document title"), `semanticDate` ("estimated date of content based on contents"). Bunlar arasındaki tutarsızlık zarar verebilir. Bu, Google'ın "tarihleri tutarlı tutun" resmi tavsiyesiyle birebir örtüşüyor — yani bu özel iddia iki bağımsız kaynaktan destek alıyor.
Kaynak: https://ipullrank.com/google-algo-leak

**Uyarı [FOLKLOR]:** "Tarihi değiştir, trafik gelsin" taktiği. Google `semanticDate`'i içerikten tahmin ediyor; içerik değişmeden tarih değiştirmek tutarsızlık yaratır. Ahrefs de bunu açıkça uyarıyor.

### Silme / birleştirme kararı

Karar ağacı:

```
Sayfa son 12 ayda anlamlı organik trafik aldı mı?
├─ Evet → Trend düşüyor mu?
│   ├─ Evet → GÜNCELLE (içeriği gerçekten değiştir, tarihi de güncelle)
│   └─ Hayır → DOKUNMA
└─ Hayır → Aynı konuda daha güçlü başka sayfan var mı?
    ├─ Evet → BİRLEŞTİR + 301 yönlendir (değerli bölümleri hedefe taşı)
    └─ Hayır → Backlink'i var mı?
        ├─ Evet → İlgili sayfaya 301
        └─ Hayır → SİL (410) veya noindex
```

Bu karar ağacının ampirik dayanağı zayıf ama mekanizması sağlam: birleştirme, dağınık iç bağlantı ve çakışan sinyalleri tek sayfada toplar; Jes Scholz vakası (%60 silme → tıklama artışı) bu yönde tek somut örnek.

---

## 11. YAZI SÜRECİ

### "Kill your darlings" — kaynağı düzeltelim

Bu söz Faulkner'a, Wilde'a, Stephen King'e, Chekhov'a, Eudora Welty'ye ve G.K. Chesterton'a atfedilir. **Hepsi yanlış.** Kaynak: Arthur Quiller-Couch, 1913-1914 Cambridge derslerinde ("On Style"), ve orijinal ifade "kill" değil, **"Murder your darlings"**.
Kaynak: https://slate.com/culture/2013/10/kill-your-darlings-writing-advice-what-writer-really-said-to-murder-your-babies.html

(Bu, bölüm 8'in kendi kuralının uygulanmış örneği: yaygın bir aktarımı düzeltmek, metne kimsede olmayan bir bilgi ekler.)

### Adım adım süreç (uzun form için)

**Adım 0 — Sorgu ve amaç tanımı (30 dk)**
Hedef sorguyu yazın. İlk 10 sonucu açın. Her birinin yapısını not edin (ters piramit mi, liste mi, karşılaştırma mı). **Amaç:** hangi yapının o sorgu için "kazanan format" olduğunu bulmak, sonra ondan daha iyisini yapmak — kopyalamak değil.

**Adım 1 — Sadece başlık iskeleti (45 dk)**
Metin yazmayın. Sadece H2/H3 yazın. Bitince **iskelet testini** uygulayın: sadece başlıkları okuyunca argüman anlaşılıyor mu? Anlaşılmıyorsa buradan geçmeyin. Bu adımda harcanan 45 dakika, sonraki 6 saatin yeniden yazımını önler.

**Adım 2 — Kanıt toplama, yazma değil (2-3 saat)**
Her H2'nin altına sadece kanıt notu düşün: sayı, kaynak URL, doğrudan alıntı. Kanıt bulunamayan H2'yi silin veya birleştirin. **Bu adım şişkinliği kaynağında önler:** kanıtı olmayan bölüm doldurma bölümüdür.

**Adım 3 — Kötü ilk taslak (tek oturum)**
Hızlı yazın, düzeltmeden. Girişi **en sona** bırakın — giriş, ancak metnin ne olduğu belli olunca yazılabilir. Hedefin %120'sini yazın; kesecek malzeme olsun.

**Adım 4 — Bekletme (minimum 12 saat, ideal 48)**
Taslağı kapatın. Bekletmenin işlevi: yazarın "ne demek istediğini" hatırlaması söner, geriye sayfada gerçekten yazan şey kalır. Kendi metnini okuyabilmenin tek yolu bu.

**Adım 5 — Kesme geçişi (hedef: %20-25 kısaltma)**
Nielsen'in kuralını hedef alın: kelimelerin %40'ını keserken değerin sadece %30'unu kaybedin. Kesim sırası:
1. Her paragrafın **ilk cümlesini** silmeyi deneyin — çoğu ısınma cümlesidir.
2. "Aslında, esasında, bilindiği üzere, unutmayın ki, önemle belirtmek gerekir ki" — sil.
3. "Çok, oldukça, son derece, gerçekten, inanılmaz" — sil (NN/g: nesnel dil %27 iyileştirme).
4. Aynı şeyi iki kez söyleyen paragrafları birleştirin.
5. Kanıtsız her genelleme: ya kanıt ekleyin ya silin.
6. **Darling testi:** en beğendiğiniz cümleyi işaretleyin. Okuyucuya bir şey öğretiyor mu, yoksa sizi mi gösteriyor? İkincisiyse silin.

**Adım 6 — Sesli okuma**
Metni baştan sona sesli okuyun. Tespit ettiği şeyler:
- Nefes almadan bitiremediğiniz cümle → çok uzun, bölün.
- Dilinizin takıldığı yer → cümle yapısı bozuk.
- Sıkıldığınız paragraf → okuyucu çoktan bıraktı.
- Aynı ritimli 3 ardışık cümle → monotonluk; birini kısaltın veya birleştirin.

Sesli okuma, sessiz okumanın atladığı ritim hatalarını yakalar; profesyonel redaksiyonun en düşük maliyetli, en yüksek getirili tek adımıdır.

**Adım 7 — Giriş ve direct answer bloğunu şimdi yazın**
Metnin gerçekte ne kanıtladığını artık biliyorsunuz. Bölüm 4 ve 6'daki şablonları uygulayın.

**Adım 8 — Tarama simülasyonu**
Metni %50 zoom'da açın, 20 saniye kaydırın. Bu sürede şunları görebiliyor musunuz: ana iddia, en çarpıcı sayı, tablo/liste, sonuç? Göremiyorsanız biçimlendirme yetersiz — bölüm 7'deki kurallara dönün.

**Adım 9 — Bağlantılar ve tarih**
İç bağlantıları yerleştirin (ilk 200 kelimede hiç, sonra her 400-500 kelimede en fazla 1). Her kanıt iddiasına dış kaynak bağlantısı verin. Yayın/güncelleme tarihini hem görünür hem yapısal veride, tutarlı biçimde koyun.

### Kelime bütçesi şablonu (2.400 kelimelik metin)

| Bölüm | Kelime | Oran |
|---|---|---|
| Giriş + direct answer | 120 | %5 |
| Bölüm 1 (temel/tanım + en güçlü kanıt) | 450 | %19 |
| Bölüm 2 (mekanizma / nasıl) | 550 | %23 |
| Bölüm 3 (uygulama / örnek / vaka) | 550 | %23 |
| Bölüm 4 (sınırlar, karşı görüş, ne zaman işe yaramaz) | 400 | %17 |
| SSS | 250 | %10 |
| Sonuç / sonraki adım | 80 | %3 |

Not: "Sonuç" bölümü %3'ten fazlaysa muhtemelen metni özetliyorsunuz. Ters piramitte ana fikir zaten başta verildi; sonda tekrar özetlemek okuyucuya yeni bilgi vermez. Sonuç bölümü ya **sonraki adım** vermeli ya hiç olmamalı.

---

## Özet: Folklor / Kanıt Ayrımı Tablosu

| İddia | Durum | Dayanak |
|---|---|---|
| Uzun içerik daha iyi sıralar | **FOLKLOR** | Google: "no magical word count target"; Backlinko'nun kendi verisinde 1-10 arası uzunluk farkı yok |
| İlk 10'un ortalaması 1.447 kelime | **KORELASYON** | Backlinko, 11,8M sonuç — ama nedensellik yok |
| Google'da "topical authority" adlı bir sistem var | **FOLKLOR** | Google dokümantasyonunda geçmiyor |
| Google site konu odaklılığını ölçebiliyor | **DOĞRULANMAMIŞ** | Sızıntıdaki `siteFocusScore` / `siteRadius` |
| Google kapsamlılığı soruyor | **BİRİNCİL** | "substantial, complete, or comprehensive description" |
| Öne çıkan snippet için işaretleme yapılabilir | **FOLKLOR** | Google: "You can't." |
| AI Overviews için özel optimizasyon gerekir | **FOLKLOR** | Google: "no additional requirements... nor other special optimizations necessary" |
| Snippet almak trafiği artırır | **KISMEN YANLIŞ** | Ahrefs: snippet %8,6 tıklama, altındaki sonuç %19,6 |
| AI Overviews tıklamayı düşürüyor | **KORELASYON** | Ahrefs, 300K anahtar kelime, %34,5 CTR düşüşü |
| H1 atlanırsa Google cezalandırır | **FOLKLOR** | Google: "it doesn't matter if you're using them out of order" |
| Başlık yapısı önemlidir | **BİRİNCİL** | WebAIM: ekran okuyucu kullanıcılarının %71,6'sı başlıkla geziniyor |
| F deseni geçersizleşti | **YANLIŞ** | NN/g 2017: "alive and well" — ama kötü biçimlendirmenin semptomu |
| İnsanlar uzun metni sonuna kadar okumuyor | **KANIT VAR** | Chartbeat: medyan scroll %50-60; %55 sayfada 15 sn'den az |
| Özlü + taranabilir + nesnel yazım işe yarar | **BİRİNCİL** | NN/g: sırasıyla %58, %47, %27; birlikte %124 iyileşme |
| Dış bağlantı vermek zarar verir (PageRank hoarding) | **ÇÜRÜTÜLDÜ** | Reboot Online 5 aylık kontrollü deney: dış bağlantı verenler daha yüksek sıraladı |
| Makale başına 3-5 iç bağlantı optimal | **FOLKLOR** | Ahrefs tavsiyesi, deneysel dayanak yok |
| İç bağlantı önemlidir | **KORELASYON + Google onayı** | HubSpot 2015 testi; Mueller: "super critical for SEO" |
| Sadece tarihi güncellemek trafik getirir | **FOLKLOR / RİSKLİ** | Google `semanticDate` tahmini; Ahrefs açıkça uyarıyor |
| Anlamlı güncelleme trafik getirir | **VAKA KANITI** | Ahrefs: %302 ve %36 artış (tekil vakalar) |
| "Kill your darlings" Faulkner'ın | **YANLIŞ** | Arthur Quiller-Couch, 1914, "Murder your darlings" |

---

## Tüm Kaynaklar

**Google birincil dokümantasyon**
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/appearance/featured-snippets
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/appearance/publication-dates
- https://developers.google.com/search/docs/essentials/spam-policies

**Kullanıcı davranışı araştırması (laboratuvar/eye-tracking)**
- https://www.nngroup.com/articles/how-users-read-on-the-web/
- https://www.nngroup.com/articles/how-little-do-users-read/
- https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/
- https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- https://www.nngroup.com/articles/scrolling-and-attention/
- https://www.nngroup.com/articles/inverted-pyramid/
- https://www.nngroup.com/articles/content-strategy-long-vs-short/
- https://webaim.org/projects/screenreadersurvey10/
- https://webaim.org/techniques/semanticstructure/

**Ölçüm / analitik verisi**
- https://slate.com/technology/2013/06/how-people-read-online-why-you-wont-finish-this-article.html
- https://time.com/12933/what-you-think-you-know-about-the-web-is-wrong/

**SEO korelasyon çalışmaları ve deneyler**
- https://backlinko.com/search-engine-ranking
- https://ahrefs.com/blog/featured-snippets-study/
- https://ahrefs.com/blog/ai-overviews-reduce-clicks/
- https://ahrefs.com/blog/internal-links-for-seo/
- https://ahrefs.com/blog/topical-authority/
- https://ahrefs.com/blog/content-decay/
- https://ahrefs.com/blog/republishing-content/
- https://www.semrush.com/blog/featured-snippet/
- https://blog.hubspot.com/marketing/topic-clusters-seo
- https://www.rebootonline.com/blog/long-term-outgoing-link-experiment/

**Google API sızıntısı (doğrulanmamış)**
- https://sparktoro.com/blog/an-anonymous-source-shared-thousands-of-leaked-google-search-api-documents-with-me-everyone-in-seo-should-see-them/
- https://ipullrank.com/google-algo-leak

**Yazım / gazetecilik**
- https://en.wikipedia.org/wiki/Nut_graph
- https://copyblogger.com/problem-agitate-solve/
- https://slate.com/culture/2013/10/kill-your-darlings-writing-advice-what-writer-really-said-to-murder-your-babies.html

---

## Araştırmanın Sınırları

Dürüstlük gereği kaydedilmeli:

1. **Web araması bütçesi bu oturumda tükendiği için** kaynaklar doğrudan URL getirme (WebFetch) ile toplandı. Bu, bilinen birincil kaynaklara ulaşmayı sağladı ama keşif kapsamını daralttı.
2. **John Mueller'ın "word count is not a ranking factor" tweet'i** SEO literatüründe çok alıntılanır; bu araştırmada doğrulanabilir bir arşiv sayfasından teyit edilemedi. Bu yüzden yerine Google'ın kendi dokümantasyonundaki iki eşdeğer ve daha güçlü ifade kullanıldı.
3. **HubSpot'un topic cluster testi** için sayısal sonuç hiçbir yerde yayınlanmamış — pillar/cluster modelinin ampirik temeli düşünüldüğünden zayıf.
4. **Reboot Online deneyi 2016 tarihli ve N=10.** Tekrarlanmamış. Sonucu yönlü kanıt olarak alın, kesin kural olarak değil.
5. **Chartbeat scroll verisi 2013-2014 tarihli.** Mobil ağırlığın artması bu rakamları değiştirmiş olabilir; NN/g'nin 2018 verisi (fold üstü payının %80'den %57'ye inmesi) davranışın zaman içinde değiştiğini gösteriyor.
6. **Featured snippet uzunluk verisi (40-50 kelime)** Semrush'un yayınladığı bir rehberden; ham metodoloji açıklanmamış — [KORELASYON] olarak alın.
