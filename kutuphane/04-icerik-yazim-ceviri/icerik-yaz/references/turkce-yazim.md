# Türkçe İçerikte SEO ve Doğal Yazım — Araştırma Notları

Hazırlanma tarihi: 26 Ağustos 2026
Amaç: Türkçe ve İngilizce içerik üreten bir yazım kılavuzuna girdi oluşturmak.

**Kaynak işaretleme kuralı:** Her iddianın yanında URL verilmiştir. Doğrulanabilir kaynak bulunamayan, dilbilimsel akıl yürütmeye veya gözleme dayanan bölümler **[KAYNAKSIZ — gerekçelendirilmiş gözlem]** etiketiyle işaretlenmiştir.

---

## 1. TÜRKÇE'NİN YAPISI VE ARAMA MOTORU

### 1.1 Sorunun kökeni: tek kök, yüzlerce yüzey biçimi

Türkçe sondan eklemeli (agglutinative) bir dildir; kök sabit kalır, anlam ve dilbilgisi ilişkileri üst üste binen eklerle kurulur. `ev + ler + iniz + de` → *evlerinizde*. Ünlü uyumu nedeniyle aynı ek birden çok yüzey biçimine sahiptir (`-de / -da / -te / -ta`).
Kaynak: https://en.wikipedia.org/wiki/Turkish_language , https://tr.wikipedia.org/wiki/T%C3%BCrk%C3%A7e

Bunun ölçeği hesaplama dilbiliminde iyi belgelenmiştir. Oflazer'in Türkçe için iki düzeyli (two-level) morfolojik betimlemesi, yaklaşık 23.000 köklük bir sözlük üzerine 22 fonolojik kural ve isim/fiil paradigmaları için sonlu durumlu makineler kurar — yani biçim üretimi kural tabanlı olarak sonsuza yakındır.
Kaynak: https://doi.org/10.1093/llc/9.2.137

Eklemeli dillerde konuşma tanıma üzerine yapılan çalışma durumu açıkça özetler: "Eklemeli dillerde tüm ilgili kelimeleri kapsayacak kelime tabanlı bir sözlük kurmak pratikte imkânsızdır... bu durum **milyonlarca farklı ama yine de sık kullanılan kelime biçimine** yol açar."
Kaynak: https://doi.org/10.3115/1220835.1220897

**SEO açısından sonuç:** İngilizce'de "wooden toy" ve "wooden toys" iki biçimdir. Türkçe'de *ahşap oyuncak* ekseninde gerçek kullanımda karşılaşılan biçimler şunlardır: ahşap oyuncak, ahşap oyuncaklar, ahşap oyuncağı, ahşap oyuncakları, ahşap oyuncakların, ahşap oyuncaklarda, ahşap oyuncaktan, ahşap oyuncaklı, ahşap oyuncakçı, ahşap oyuncakçılık... Bir sayfada "tam eşleşme" hedeflemek matematiksel olarak anlamsızdır; hedeflenecek biçim sayısı tek bir sayfanın taşıyabileceğinden fazladır.

### 1.2 Arama motoru Türkçe'de kök buluyor mu? — Kanıtlar

**Kanıt 1 — Google'ın kendi beyanı (eş anlamlı sistemi).** Google, sorgu anlama katmanını şöyle tarif eder: "yazım hatalarını tanıyıp düzeltmek gibi görece basit adımlardan, kullandığınız kelimelerin tam olarak geçmediği belgeleri bile bulmamızı sağlayan gelişmiş eş anlamlı sistemimize kadar uzanır." Ve ölçek verir: "Bu sistemin geliştirilmesi beş yıldan fazla sürdü ve **diller genelinde aramaların %30'undan fazlasında** sonuçları belirgin biçimde iyileştiriyor."
Kaynak: https://www.google.com/search/howsearchworks/how-search-works/ranking-results/

**Kanıt 2 — Google Ads "close variants" tanımı.** Google Ads dokümantasyonu yakın varyasyonları şöyle tanımlar: "Close variants can include **singular and plural forms, acronyms, stem words**, misspellings, **abbreviations, accents**, and variants of your keyword terms that have the same meaning." Burada "stem words" ve "accents" ifadeleri kritiktir: Google reklam eşleştirmesinde açıkça kök ve aksan normalizasyonu yaptığını söyler. Organik arama tarafı da aynı dilsel altyapıyı kullanır.
Kaynak: https://support.google.com/google-ads/answer/2472708

**Kanıt 3 — BERT ve dilden dile aktarım.** Google, BERT'i aramaya getirirken "bir dilden öğrendiklerini diğerlerine uygulayabildiklerini" ve öne çıkan snippet'lerde Korece, Hintçe, Portekizce gibi dillerde iyileşme gördüklerini bildirdi. Yani Google'ın dil anlama katmanı İngilizce'ye özgü değildir.
Kaynak: https://blog.google/products/search/search-language-understanding-bert/

**Kanıt 4 — Türkçe bilgi erişimi literatürü.** Can ve arkadaşlarının 408.305 belge ve 72 sorgudan oluşan büyük ölçekli Türkçe test koleksiyonuyla yaptığı çalışma, "basit bir kelime kırpma (word truncation) yaklaşımının, dile bağımlı külliyat istatistikleri kullanan kırpmanın ve ayrıntılı bir lemmatizer tabanlı kök bulucunun **Türkçe bilgi erişiminde benzer erişim etkinliği sağladığını**" gösterir. Yani Türkçe'de kök bulma çalışır; hatta ilk 5-6 harfe kırpmak bile ciddi kazanç verir.
Kaynak: https://doi.org/10.1002/asi.20750

**Kanıt 5 — Tokenizasyon araştırması.** "Impact of Tokenization on Language Models: An Analysis for Turkish" (2023) çalışması, morfolojik düzeyde tokenizasyonun Türkçe'de fiili standart (BPE/WordPiece) yöntemlerle yarışabilir performans verdiğini gösterir — modern dil modelleri Türkçe'yi zaten alt kelime parçalarına ayırarak işler.
Kaynak: https://doi.org/10.1145/3578707

**Pratik sonuç:** Google Türkçe'de büyük olasılıkla saf sözlükbilimsel bir "stemmer" değil, alt kelime tokenizasyonu + eş anlamlı genişletme + dil modeli anlama katmanı kullanır. Kullanıcı açısından etkisi aynıdır: *ahşap oyuncak* için sıralanan bir sayfa, *ahşap oyuncaklar* sorgusunda da sıralanır. Google'ın her çekimli biçimi ayrı hedeflemenizi beklediğine dair hiçbir resmî kanıt yoktur; aksine "aynı kelime veya ifadeleri doğal olmayan bir sonuç ortaya çıkacak kadar sık tekrarlamak" açıkça spam politikası ihlalidir.
Kaynak: https://developers.google.com/search/docs/essentials/spam-policies

### 1.3 "Tam eşleşme" takıntısının Türkçe'de yarattığı bozuk cümleler

Türkçe'de anahtar kelimeyi çekimsiz kök hâlinde cümleye sokmaya çalışmak, İngilizce'de olmayan bir gramer hasarı üretir. Çünkü Türkçe'de belirtili nesne, tamlama ve iyelik ekleri zorunludur; onları düşürmek cümleyi bozar.

| Yanlış (anahtar kelime zorlaması) | Doğru (doğal Türkçe) |
|---|---|
| "Ahşap oyuncak satın almak isteyenler ahşap oyuncak modellerimizi inceleyebilir." | "Ahşap oyuncak arıyorsanız modellerimize göz atın." |
| "Ahşap oyuncak fiyatları için ahşap oyuncak sayfamızı ziyaret edin." | "Fiyatları ürün sayfasında bulabilirsiniz." |
| "Çocuk ahşap oyuncak oynamayı sever." (nesne eki düşmüş) | "Çocuklar ahşap oyuncaklarla oynamayı sever." |
| "İstanbul ahşap oyuncak mağaza" (başlık olarak) | "İstanbul'da ahşap oyuncak mağazası" |
| "En iyi ahşap oyuncak markası ahşap oyuncak üretiminde önde." | "Ahşap oyuncak üretiminde önde gelen markalardan biriyiz." |

**[KAYNAKSIZ — gerekçelendirilmiş gözlem]** Türkçe'de "ahşap oyuncak fiyat" gibi eksiz kalıplar yalnızca *sorgu dilinde* doğaldır (insanlar arama kutusuna telgraf üslubuyla yazar); *metin dilinde* değildir. Metinde bu kalıbı kullanmak, sayfanın makine tarafından üretildiği izlenimini güçlendirir.

### 1.4 Türkçe'de arama hacmi araştırması nasıl yapılır

Google Anahtar Kelime Planlayıcı aylık ortalama arama tahminlerini yakın varyasyonları gruplayarak sunar (bkz. yukarıdaki "close variants" tanımı) — ancak gruplama şeffaf değildir ve Türkçe'de eklerin nasıl toplandığı belgelenmemiştir.
Kaynak: https://support.google.com/google-ads/answer/7337243 , https://support.google.com/google-ads/answer/2472708

Pratik yöntem:

1. **Kök öbeği belirle, ek varyantlarını ayrı ayrı sorgula.** "ahşap oyuncak", "ahşap oyuncaklar", "ahşap oyuncak fiyatları", "ahşap oyuncak modelleri". Eğer araç ikisine de aynı hacmi veriyorsa gruplama yapıyor demektir; farklı hacim veriyorsa gruplama yapmıyordur ve toplam talebi görmek için hepsini toplamanız gerekir.
2. **Türkçe karakterli ve karaktersiz biçimleri ayrı ayrı ölç.** "ahşap oyuncak" ve "ahsap oyuncak". (Bkz. 2.2)
3. **Eklerin hacim dağılımı hakkında genel örüntü [KAYNAKSIZ — gerekçelendirilmiş gözlem]:** Ticari sorgularda çoğul + iyelik biçimi ("... modelleri", "... fiyatları", "... çeşitleri") genellikle yalın kökten daha yüksek hacim taşır, çünkü kullanıcı bir liste bekler. Bilgi amaçlı sorgularda ise yalın kök baskındır ("ahşap oyuncak nedir", "ahşap oyuncak nasıl yapılır").
4. **Araç yerine Google'ın kendi sinyallerini kullan:** Autocomplete önerileri, "İlgili aramalar", "Kullanıcılar şunları da soruyor" blokları Türkçe'de nicel araçlardan daha güvenilir örüntü verir — çünkü doğrudan gerçek sorgu dağılımından türer. **[KAYNAKSIZ — gerekçelendirilmiş gözlem]**
5. **Search Console sorgu raporu nihai kaynaktır.** Türkçe'de bir sayfanın hangi çekimli biçimlerde göründüğünü yalnızca burada gerçek veriyle görürsünüz.

**Yazım kılavuzuna girecek kural:** Bir konu için tek bir "anahtar kelime" değil, **bir kök öbeği** hedefle. O öbeği metinde 2-4 kez, **her seferinde cümlenin gerektirdiği ekle** kullan. Aynı eki tekrarlama.

---

## 2. TÜRKÇE ARAMA DAVRANIŞI

### 2.1 Pazar ve cihaz gerçekleri

- **Arama motoru payı (Temmuz 2026, Türkiye):** Google %80,5 — Yandex %17,5 — Bing %0,97 — Yahoo %0,6 — DuckDuckGo %0,33.
  Kaynak: https://gs.statcounter.com/search-engine-market-share/all/turkey
  **Not:** Yandex'in %17,5'lik payı Türkiye'yi Avrupa'da olağandışı kılar; İngilizce SEO kaynaklarının "Google = arama" varsayımı Türkiye'de her altı aramadan birini ıskalar.
- **Cihaz dağılımı (Temmuz 2026, Türkiye):** Mobil %74,08 — Masaüstü %25,33 — Tablet %0,58.
  Kaynak: https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet/turkey
- **Kullanıcı tabanı (Digital 2026 Turkey):** 77,5 milyon internet kullanıcısı (nüfusun %88,3'ü); 81,9 milyon mobil bağlantı (nüfusun %93,3'ü); 62,3 milyon sosyal medya kimliği.
  Kaynak: https://datareportal.com/reports/digital-2026-turkey

**Yazma açısından sonucu:** Okurun dörtte üçü metni dar bir ekranda okuyor. Türkçe zaten kelime başına daha çok karakter taşıdığından (ekler nedeniyle), uzun cümle mobilde İngilizce'ye göre daha fazla satır kaplar. Paragraf uzunluğu ve cümle uzunluğu Türkçe'de İngilizce'den daha sıkı tutulmalıdır. **[KAYNAKSIZ — gerekçelendirilmiş çıkarım]**

### 2.2 Türkçe karakter kullanmadan arama

Bu, Türkçe'ye özgü ve ölçülmüş bir olgudur. "Effects of diacritics on Turkish information retrieval" çalışması şunu bulur: "İstatistiksel analiz, belgeler ve sorgular farklı harf biçimleri içerdiğinde — belgeler aksanlı harflerden, sorgular standart Latin harflerinden oluştuğunda ve tersi — **erişim performansının anlamlı biçimde düştüğünü** göstermektedir." Çözüm olarak önerilenler: eşdeğerlik sınıflarıyla token normalizasyonu, belge genişletme, sorgu genişletme.
Kaynak: https://doi.org/10.3906/elk-1010-819

Türkçe alfabede Latin'den türetilmiş yedi özel harf vardır (Ç, Ğ, I, İ, Ö, Ş, Ü) ve noktalı/noktasız i ayrımı yazılımda "Türkçe-I problemi" olarak bilinen ayrı bir mantık gerektirir.
Kaynak: https://en.wikipedia.org/wiki/Turkish_alphabet

**Pratik kural:**
- Metinde **her zaman doğru Türkçe karakter kullan.** Aksansız yazmak okuru kaybettirir ve profesyonelliği zedeler.
- **URL slug'larında** Türkçe karakter kullanma; `ahsap-oyuncak` yaz. (Teknik uyum + kopyalama/paylaşma kolaylığı.)
- Google Ads/Keyword Planner tanımı aksanları yakın varyasyon saydığı için (https://support.google.com/google-ads/answer/2472708), sayfada aksansız varyantı ayrıca "serpiştirmeye" gerek yoktur. Bunu yapmak keyword stuffing'e girer.

### 2.3 Soru kalıpları

**[KAYNAKSIZ — dilbilimsel gözlem]** Türkçe'de bilgi amaçlı sorgular İngilizce'den yapısal olarak farklı kurulur. İngilizce'de "how to ..." tek kalıptır; Türkçe'de soru sözcüğü fiilden önce gelir ve fiil sona düşer:

| İngilizce kalıp | Türkçe karşılığı | Sorgu biçimi |
|---|---|---|
| how to X | X nasıl yapılır / X nasıl + fiil | "ahşap oyuncak nasıl yapılır" |
| what is X | X nedir | "montessori oyuncak nedir" |
| what does X mean | X ne demek | "CE belgesi ne demek" |
| why X | X neden / niçin | "ahşap oyuncak neden tercih edilir" |
| how much / how many | kaç / ne kadar | "ahşap oyuncak kaç yaşına uygun" |
| which X is best | en iyi X hangisi / hangi X | "hangi ahşap oyuncak daha iyi" |
| is X safe | X zararlı mı / güvenli mi | "ahşap oyuncak zararlı mı" |
| X vs Y | X mi Y mi / X ve Y farkı | "ahşap mı plastik mi oyuncak" |

Not: `-mı/-mi/-mu/-mü` soru eki TDK'ye göre **ayrı yazılır**: "Kaldı mı?", "Verecek misin?"
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/soru-eki-mi-mi-mu-munun-yazilisi/

**Kural:** H2/H3 başlıkları, kullanıcıların gerçekten yazdığı soru kalıbıyla birebir eşleşmeli — İngilizce başlığın çevirisi değil. "Nasıl Ahşap Oyuncak Yapılır" (İngilizce sözdizimi kalıntısı) yerine "Ahşap Oyuncak Nasıl Yapılır?" yazılmalı.

### 2.4 Yazım düzeltme ve eş anlamlılar

Google'ın kendi ifadesiyle sistem "yazım hatalarını tanıyıp düzeltmek"le başlar ve eş anlamlı sistemi aramaların %30'undan fazlasını iyileştirir.
Kaynak: https://www.google.com/search/howsearchworks/how-search-works/ranking-results/

**Sonuç:** Türkçe'de sık yapılan yazım hatalarını ("yalnış", "herkez", "yanlız") sayfaya "hata avı" için koymak gereksizdir ve zararlıdır.

---

## 3. TÜRKÇE OKUNABİLİRLİK

### 3.1 Flesch-Kincaid neden Türkçe'de çalışmaz

Orijinal formüller:

- **Flesch Reading Ease** = `206,835 − 1,015 × (toplam kelime / toplam cümle) − 84,6 × (toplam hece / toplam kelime)`
- **Flesch-Kincaid Grade Level** = `0,39 × (toplam kelime / toplam cümle) + 11,8 × (toplam hece / toplam kelime) − 15,59`

Wikipedia'nın da not ettiği gibi bu formüller "İngilizce okunabilirliğini göstermek için tasarlandı" ve okul kitapları üzerinden kalibre edildi.
Kaynak: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

**Neden Türkçe'de bozulur:**
1. Sabitler (84,6 / 11,8) İngilizce'nin hece-kelime dağılımına göre kalibredir. Türkçe'de ekler yüzünden kelime başına hece sayısı sistematik olarak daha yüksektir; formül Türkçe'yi haksız yere "zor" gösterir.
2. Türkçe'de uzun kelime = karmaşık kelime değildir. *Gelebileceğini* altı hecedir ama günlük bir kelimedir; İngilizce'de altı heceli kelime neredeyse her zaman Latince/Yunanca kökenli teknik bir terimdir.
3. Türkçe'de bir "kelime" İngilizce'de bir cümleciğe denk gelebilir (*yapamayacaklarını* ≈ "that they will not be able to do"), dolayısıyla cümle başına kelime sayısı sistematik olarak düşüktür. Bu da formülü ters yönde saptırır.

Türkçe alanyazın bu değerlendirmede açıktır: "Bu ölçeklerin dili İngilizce olduğundan Türkçe metinlerde kullanılmazlar. Bu nedenle Türkçe metinlerin okunabilirliğini ölçmek için Ateşman ve Bezirci-Yılmaz tarafından okunabilirlik formülleri geliştirilmiştir."
Kaynak: https://doi.org/10.51982/bagimli.829808 (Bağımlılık Dergisi, 2021)

### 3.2 Ateşman formülü (Türkçe için Flesch uyarlaması, 1997)

```
Okunabilirlik puanı = 198,825 − 40,175 × (toplam hece / toplam kelime) − 2,610 × (toplam kelime / toplam cümle)
```

Puan 0-100 aralığındadır; yüksek puan = daha kolay metin.
Kaynak (formül ve tablo birebir): https://doi.org/10.7759/cureus.58603
İkincil doğrulama: https://doi.org/10.7759/cureus.16639 (aynı formül, aynı sabitler)
Orijinal atıf: Ateşman, E. (1997). *Türkçede okunabilirliğin ölçülmesi.* A.Ü. TÖMER Dil Dergisi, 58, 71-74.

| Puan | Karşılık gelen eğitim seviyesi |
|---|---|
| 90–100 | 4. sınıf ve altı (çok kolay) |
| 80–89 | 5.–6. sınıf |
| 70–79 | 7.–8. sınıf |
| 60–69 | 9.–10. sınıf |
| 50–59 | 11.–12. sınıf |
| 40–49 | 13.–15. sınıf (ön lisans / lisans başı) — "zor" |
| 30–39 | Lisans (16. sınıf) |
| ≤29 | Lisansüstü (>16. sınıf) — "çok zor" |

Kaynak: https://doi.org/10.7759/cureus.58603

### 3.3 Bezirci-Yılmaz formülü (2010)

```
Okunabilirlik = √( OKS × [ (H3 × 0,84) + (H4 × 1,5) + (H5 × 3,5) + (H6 × 26,25) ] )
```

- **OKS** = ortalama kelime sayısı (cümle başına kelime)
- **H3** = 3 heceli kelimelerin ortalama sayısı
- **H4** = 4 heceli kelimelerin ortalama sayısı
- **H5** = 5 heceli kelimelerin ortalama sayısı
- **H6** = 6 ve daha fazla heceli kelimelerin ortalama sayısı

Kaynak (formül birebir, üç bağımsız makalede aynı): https://doi.org/10.7759/cureus.16639 , https://doi.org/10.7759/cureus.58603 , http://www.fppc.com.tr/en/download/article-file/675235
Orijinal atıf: Bezirci, B. & Yılmaz, A. E. (2010). *Proposal of a new readability metric for Turkish*, IEEE SIU 2010 — https://doi.org/10.1109/siu.2010.5652572

Sonuç doğrudan sınıf düzeyi verir:

| Puan / Sınıf | Eğitim seviyesi |
|---|---|
| 1–8 | İlköğretim |
| 9–12 | Lise |
| 12–16 | Lisans |
| 16+ | Akademik düzey |

Kaynak: https://doi.org/10.7759/cureus.58603

**Formülün mantığı, yazım kılavuzu açısından en değerli kısmıdır:** 6+ heceli kelimeler `26,25` katsayısıyla cezalandırılırken 3 heceliler `0,84` ile neredeyse serbest bırakılır. Yani Türkçe'de okunabilirliği asıl bozan şey **çok uzun kelimelerdir**, orta uzunluktakiler değil. Ve tüm ifade cümle uzunluğuyla (`OKS`) çarpılır: uzun cümle + uzun kelime birleşimi çarpan etkisiyle metni okunmaz hâle getirir.

### 3.4 Türkçe web metinlerinin gerçek okunabilirlik durumu (kıyas noktası)

- Sigara bırakma konulu 62 Türkçe web sitesi: medyan Ateşman **48,47** ("zor"), medyan Bezirci-Yılmaz **13,08** ("lisans düzeyi"). Yazarların yorumu: "Bu sonuçlar, halkımızın eğitim seviyesinin çok üstündedir."
  Kaynak: https://doi.org/10.51982/bagimli.829808
- Şaşılık konulu 41 Türkçe site: ortalama Ateşman **55,2 ± 7,9** (11.-12. sınıf), Bezirci-Yılmaz **10,5 ± 2,3** yıl eğitim.
  Kaynak: https://doi.org/10.7759/cureus.58603
- Obezite/bariatrik cerrahi konulu 79 Türkçe site: Ateşman'a göre "zor", Bezirci-Yılmaz'a göre "lisans düzeyi".
  Kaynak: https://doi.org/10.33808/clinexphealthsci.763167

**Yazım kılavuzu hedefi:** Genel okur için üretilen Türkçe web içeriğinde **Ateşman 60-75** (9.-8. sınıf) bandı hedeflenmelidir. Bu, Türkçe web'in bugünkü ortalamasının (≈48-55) belirgin biçimde üzerindedir ve tek başına bir farklılaşma kaynağıdır.

### 3.5 Somut yazım normları

**[KAYNAKSIZ — yukarıdaki formüllerden türetilmiş çalışma kuralları]**

- Ortalama cümle uzunluğu: **12–18 kelime.** 25 kelimeyi geçen cümleyi böl.
- Bir paragrafta en fazla **3–4 cümle**; mobil ekranda 4-5 satır.
- 6+ heceli kelimeleri paragraf başına **1'i geçmeyecek** şekilde kullan. (`değerlendirilebilmektedir`, `gerçekleştirilmektedir`, `sürdürülebilirliğinin` gibi.)
- `-mektedir/-maktadır` yerine `-iyor` veya geniş zaman kullan: her değişim kelimeyi 2 hece kısaltır ve Bezirci-Yılmaz puanını doğrudan iyileştirir.
- Uzun bir isim tamlaması zincirini (`müşteri memnuniyeti yönetimi süreçlerinin iyileştirilmesi`) fiilli bir cümleye çevir (`müşteri memnuniyetini nasıl yönettiğimizi iyileştiriyoruz`).

---

## 4. TÜRKÇE'DE YAPAY ZEKÂ VE ÇEVİRİ KOKUSU

Google, "arama sıralamalarını manipüle etmek amacıyla, kullanıcılara yardımcı olmadan çok sayıda sayfa üretmeyi" (scaled content abuse) ve "yapay zekâ araçları kullanarak değer katmadan çok sayıda sayfa üretmeyi" açıkça spam sayar; ayrıca "belirli bir kelime sayısına ulaşmak için yazmayı" da reddeder.
Kaynak: https://developers.google.com/search/docs/essentials/spam-policies , https://developers.google.com/search/docs/fundamentals/creating-helpful-content

Aşağıdaki listelerin tamamı **[KAYNAKSIZ — dilbilimsel gerekçelendirmeye ve metin gözlemine dayanır]**. Türkçe'ye özgü AI kalıp listesi yayımlanmış bir akademik kaynakta mevcut değildir; gerekçeler her başlığın altında verilmiştir.

### 4.1 Neden Türkçe'de AI izi daha görünürdür

1. **Ek seçimi bir üslup seçimidir.** Türkçe'de `-mektedir` (kurumsal/edilgen), `-iyor` (nötr/konuşma), `-ir` (genel doğru) arasında seçim yaparsınız. Model, eğitim verisindeki akademik ve kurumsal Türkçe ağırlığı nedeniyle sistematik olarak `-mektedir`e kayar. İnsan yazar bu üç eki karıştırır; model karıştırmaz.
2. **Edilgen çatı Türkçe'de "kolay"dır.** `-il-/-ın-` eki hemen her fiile takılır, dolayısıyla model özne bulmak zorunda kalmadan cümle kurabilir. Sonuç: özne yokluğu ve sorumluluk yokluğu.
3. **İsimleştirme (nominalizasyon) zinciri kolaydır.** `-me/-ma`, `-lik`, `-sel` ekleriyle fiiller isme çevrilir ve tamlama zinciri kurulur. Türkçe bu zincire karşı gramer olarak direnmez; okur direnir.
4. **SOV yapısı çevirinin izini saklamaz.** İngilizce kaynak metnin SVO yapısı Türkçe'ye kelime kelime aktarıldığında fiil sona düşmez, "bir" gereksiz yere kalır, iyelik eki düşer — hepsi anında fark edilir.

### 4.2 Kaçınılacak Türkçe kalıplar — TARAMA LİSTESİ

#### A. Boş açılış kalıpları (yazıya hiçbir bilgi eklemez)
- "Günümüzde..."
- "Günümüz dünyasında..."
- "Hızla gelişen dünyada..."
- "Hızla değişen teknoloji çağında..."
- "Teknolojinin gelişmesiyle birlikte..."
- "Son yıllarda artan..."
- "İnsanlık tarihi boyunca..."
- "Çağımızın vazgeçilmezleri arasında..."
- "Modern yaşamın getirdiği..."
- "Dijitalleşen dünyada..."
- "Bilindiği üzere..."
- "Herkesin bildiği gibi..."

#### B. Bağlaç enflasyonu / geçiş kalıpları
- "Bu bağlamda..."
- "Bu doğrultuda..."
- "Bu noktada..."
- "Bu çerçevede..."
- "Bu kapsamda..."
- "Bu anlamda..."
- "Bu vesileyle..."
- "Diğer taraftan..." (her paragrafta)
- "Öte yandan..." (her paragrafta)
- "Bununla birlikte..." (her paragrafta)
- "Ayrıca belirtmek gerekir ki..."
- "Şunu da eklemek gerekir ki..."

#### C. Otorite taklidi / vurgu şişirmesi
- "Unutulmamalıdır ki..."
- "Göz ardı edilmemelidir ki..."
- "Şüphesiz ki..."
- "Kuşkusuz..."
- "Hiç şüphe yok ki..."
- "Altını çizmek gerekir ki..."
- "Vurgulamak gerekir ki..."
- "Dikkat edilmesi gereken bir diğer husus..."
- "Kritik öneme sahiptir."
- "Hayati önem taşımaktadır."
- "Büyük önem arz etmektedir."
- "Önemli bir rol oynamaktadır."
- "Kilit bir rol üstlenmektedir."

#### D. `-mektedir / -maktadır` kümesi (edilgen + uzun + kurumsal)
- "...dikkat çekmektedir."
- "...ön plana çıkmaktadır."
- "...öne çıkmaktadır."
- "...tercih edilmektedir."
- "...kullanılmaktadır."
- "...sunulmaktadır."
- "...hedeflenmektedir."
- "...amaçlanmaktadır."
- "...sağlanmaktadır."
- "...gerçekleştirilmektedir."
- "...değerlendirilmektedir."
- "...uygulanmaktadır."
- "...yer almaktadır."
- "...bulunmaktadır."
- "...oluşturmaktadır."
> **Kural:** Bir yazıda `-mektedir/-maktadır` sayısı **sıfır** olmalı (pazarlama/blog metni) veya toplam fiillerin %5'ini geçmemeli (kurumsal/hukuki metin).

#### E. Pazarlama boşluğu (anlamı olmayan sıfat yığını)
- "kaliteli ve güvenilir"
- "hızlı ve güvenilir"
- "profesyonel ve deneyimli kadromuzla"
- "uzman ekibimizle"
- "müşteri memnuniyeti odaklı"
- "geniş bir yelpazede"
- "geniş ürün yelpazemiz"
- "zengin içerik"
- "ihtiyaçlarınıza yönelik çözümler"
- "ihtiyaçlarınıza özel çözümler"
- "size özel çözümler sunuyoruz"
- "yenilikçi çözümler"
- "sektörün öncüsü"
- "sektörde lider konumdayız"
- "en uygun fiyatlarla"
- "eşsiz bir deneyim"
- "benzersiz bir deneyim"
- "yılların tecrübesiyle"
- "titizlikle hazırlanmış"
- "özenle seçilmiş"
- "sizlere sunuyoruz"
- "hizmetinizdeyiz"

#### F. Kapanış kalıpları
- "Sonuç olarak..."
- "Sonuç olarak diyebiliriz ki..."
- "Özetle..."
- "Kısacası..."
- "Toparlamak gerekirse..."
- "Tüm bunlar göz önünde bulundurulduğunda..."
- "Yukarıda bahsedilenler ışığında..."
- "Umarız bu yazı işinize yaramıştır."
- "Bu konuda daha fazla bilgi için bizimle iletişime geçebilirsiniz."

#### G. İngilizceden çeviri kokusu (yapısal kalıntılar)
| Çeviri kokan | Türkçesi |
|---|---|
| "Hadi başlayalım!" (*Let's get started*) | (Sil. Doğrudan konuya gir.) |
| "Bu yazıda ... hakkında konuşacağız." (*we'll talk about*) | "Bu yazıda ...'yi anlatıyorum." veya sil. |
| "... hakkında konuşalım." | "...'ye bakalım." / sil |
| "Sizin için derledik." (*we've put together for you*) | "Derledik." (iyelik zaten var) |
| "Sizin için en iyi seçenekler" | "En iyi seçenekler" |
| "Bu bir harika bir fırsattır." (*a great opportunity*) | "Bu iyi bir fırsat." |
| "Bir kullanıcı bir sayfaya bir link ekleyebilir." | "Kullanıcı sayfaya bağlantı ekleyebilir." |
| "Merak etmeyin!" (*Don't worry!*) | (Sil.) |
| "İşte bu kadar!" (*That's it!*) | (Sil.) |
| "Ne demek istediğimi anlıyor musunuz?" | (Sil.) |
| "Yukarıda belirtildiği gibi" (*as mentioned above*) | (Referans ver veya sil.) |
| "Aşağıda listelenmiştir" (*listed below*) | (İki nokta koy ve listele.) |
| "Doğru okudunuz." (*You read that right*) | (Sil.) |
| "gün sonunda" (*at the end of the day*) | "sonuçta" / sil |
| "oyunun kurallarını değiştiren" (*game changer*) | (Somut etkisini yaz.) |
| "yolculuğunuzda size eşlik ediyoruz" (*journey*) | (Sil.) |

#### H. "Bir" belirsiz artikeli hastalığı
Türkçe'de belirsizlik çoğu zaman eksizlikle kurulur; İngilizce'deki *a/an* her seferinde "bir" ile çevrilirse metin şişer.
- ✗ "Bu, bir işletme için bir avantaj sağlayan bir yöntemdir."
- ✓ "Bu yöntem işletmeye avantaj sağlar."
- ✗ "Bir web sitesi bir hedef kitleye bir mesaj iletir."
- ✓ "Web sitesi hedef kitleye mesaj iletir."
> **Kural:** Bir cümlede ikiden fazla "bir" varsa cümleyi yeniden kur.

#### I. İyelik eki eksikliği (çevirinin en yaygın izi)
- ✗ "Kullanıcı deneyim iyileştirme" → ✓ "Kullanıcı deneyiminin iyileştirilmesi" / daha iyisi: "Kullanıcı deneyimini iyileştirmek"
- ✗ "Ürün sayfa tasarım" → ✓ "Ürün sayfası tasarımı"
- ✗ "Marka bilinirlik artırma" → ✓ "Marka bilinirliğini artırmak"
- ✗ "Ahşap oyuncak güvenlik standartları" → ✓ "Ahşap oyuncakların güvenlik standartları"

#### J. `-abilir/-ebilir` aşırılığı (yetenek kipinin belirsizlik sisi)
- ✗ "Bu ürün cildinizi nemlendirebilir, kuruluğu azaltabilir ve görünümü iyileştirebilir."
- ✓ "Bu ürün cildi nemlendirir, kuruluğu azaltır."
> Gerçekten şart varsa koru ("alerjiniz varsa tahriş **olabilir**"); yoksa kesin kipe geç. İngilizce hedge dili (*can/may/might*) Türkçe'ye üç kez `-abilir` olarak yansıdığında metin kendine güvensiz görünür.

#### K. Sıralı sıfat tamlaması yığını
- ✗ "Yüksek kaliteli, doğal malzemelerden üretilmiş, çocuk gelişimini destekleyen, güvenli ahşap oyuncak modelleri"
- ✓ "Ahşap oyuncaklarımız doğal kayın ağacından yapılır. Boyaları çocuk sağlığına uygundur."
> **Kural:** Bir isimden önce en fazla iki sıfat.

#### L. Diğer AI parmak izleri
- Her paragrafın aynı uzunlukta olması (4-5 satır, sapmasız).
- Her H2'nin altında tam üç madde bulunması.
- Madde işaretlerinin hepsinin "**Kalın başlık:** açıklama" formatında olması.
- Emoji ile başlayan başlıklar.
- "Avantajları / Dezavantajları" karşıtlığının her konuya uygulanması.
- Örnek verilmemesi; sadece kategori adlarının sayılması.
- Sayı verilmemesi; "birçok", "pek çok", "sayısız" ile geçiştirilmesi.
- İsim verilmemesi; "bazı markalar", "kimi uzmanlar" denmesi.
- Aynı fikri ikinci kez farklı kelimelerle söylemek (paraphrase döngüsü).
- Türkçe'de olmayan "em dash" ritmi: her paragrafta bir uzun çizgi ara cümlesi.

### 4.3 Türkçe metni insanlaştıran şeyler (pozitif liste)
**[KAYNAKSIZ — üslup önerisi]**
- Kısa cümlenin uzun cümleyle karıştırılması. Üç kelimelik bir cümle bir paragrafı kurtarır.
- Somut rakam, marka adı, tarih, yer adı.
- Birinci tekil/çoğul şahıs ("ölçtük", "yanıldık", "denedik").
- Kabul edilen sınır ("Bunu ölçemedik.").
- Türkçe deyim ve konuşma diline ait bağlaç ("ama", "yalnız", "gerçi", "hani") — "ancak / fakat / lâkin" zincirinin yerine.
- Cümleye "ve" ile başlamaktan çekinmemek.
- Nadiren, bilinçli devrik cümle (bkz. Bölüm 6).

---

## 5. TÜRKÇE YAZIM KURALLARI (TDK)

Tüm kurallar Türk Dil Kurumu Yazım Kuralları bölümünden alınmıştır: https://tdk.gov.tr/kategori/icerik/yazim-kurallari/

### 5.1 Bağlaç olan "de / da" ayrı yazılır
Kural: Bağlaç olan *de/da* ayrı yazılır ve kendisinden önceki kelimenin son ünlüsüne göre ünlü uyumuna uyar. **"te/ta" biçimi yoktur.** "ya da" her zaman ayrı yazılır. Bağlaçtan önce kesme işareti konmaz.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-da-denin-yazilisi/

- ✓ "Kızı **da** geldi." / ✗ "Kızıda geldi."
- ✓ "Sen **de mi**?" / ✗ "Sende mi?" (farklı anlam: "sende" = sende bulunan)
- ✓ "Ayşe **de** geldi." / ✗ "Ayşe'de geldi."
- ✓ "ya **da**" / ✗ "yada"
- **Ayırt etme testi:** Cümleden çıkarınca anlam bozulmuyorsa bağlaçtır, ayrı yazılır. Bulunma hâli eki ise ("evde", "okulda") bitişik yazılır.
  Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/bulunma-durumu-eki-da-de-ta-tenin-yazilisi/

### 5.2 Bağlaç olan "ki" ayrı yazılır
Kural: Bağlaç olan *ki* ayrı yazılır: "bilmem ki, demek ki, kaldı ki". Kalıplaşmış birkaç kelime bitişik yazılır: **belki, çünkü, hâlbuki, mademki, meğerki, oysaki, sanki.** Şüphe/pekiştirme işlevindeki *ki* de ayrıdır.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-kinin-yazilisi/

- ✓ "Demek **ki** haklıymış." / ✗ "Demekki haklıymış."
- ✓ "Öyle güzeldi **ki**..." / ✗ "Öyle güzeldiki..."
- ✓ "**Halbuki** biliyordu." (kalıplaşmış, bitişik)
- İlgi zamiri *-ki* bitişiktir: "benim**ki**", "yarın**ki** toplantı".

### 5.3 Kesme işareti ( ' )
TDK yedi kullanım sayar: özel adlara gelen çekim ekleri ("Atatürk'üm", "Türkiye'mizin"); unvanlardan sonra ("Nihat Bey'e", "Ayşe Hanım'dan"); kısaltmalara gelen ekler ("TBMM'nin", "TDK'nin"); sayılara gelen ekler ("1985'te", "8'inci madde"); ay/gün adlarına gelen ekler ("17 Aralık'a kadar"); düşen ses yerine ("Düştü m'ola"); harf ve ek ayırmada ("a'dan z'ye").
**İstisna:** Kurum/kuruluş adlarına, çoğul eklerine ve özel addan türeyen sıfatlara kesme konmaz.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/kesme-isareti/

- ✓ "Türk Dil Kurumundan" (kurum adı — kesme yok) / ✗ "Türk Dil Kurumu'ndan"
- ✓ "Türkiye'nin", "İstanbul'da"
- ✓ "Türkçe" (özel addan türemiş — kesme yok) / ✗ "Türk'çe"
- ✓ "Aliler geldi" (çoğul — kesme yok) / ✗ "Ali'ler geldi"
- ✓ "2026'da", "%25'lik"

Kısaltmalara gelen ek, kısaltmanın **okunuşuna** göre seçilir: "TDK'den", "THY'de", "cm'yi", "kg'dan". Kelime gibi okunanlarda normal okunuş: "NATO'ya", "BOTAŞ'ın".
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar/

### 5.4 Kısa çizgi ( - ) — TDK ne diyor
TDK'ye göre kısa çizgi şu yerlerde kullanılır: satır sonunda kelime bölmede; **cümle içinde ara sözleri/ara cümleleri ayırmak için (metne bitişik yazılır)**; kök ve ekleri ayırmada ("al-ış", "-lık"); heceleri göstermede ("a-raş-tır-ma"); "arasında / ve / ile" anlamıyla iki öğeyi bağlamada ("Aydın-İzmir yolu", "Türk-Alman ilişkileri"); matematikte eksi işareti ("50-20=30"); sıfır altı sıcaklıklarda ("-2 °C").
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/

- ✓ "Küçük bir sürü -dört inekle birkaç koyun- köye giren yolun ağzındaydı." (TDK örneği; çizgiler metne **bitişik**)
- ✓ "Ankara-İstanbul uçuşu"
- ✗ "Türkçe — bir dil — güzeldir." (İngilizce em dash alışkanlığı)

### 5.5 Uzun çizgi ( — ) — konuşma çizgisi
TDK'ye göre uzun çizginin işlevi tektir: **"Yazıda satır başına alınan konuşmaları göstermek için kullanılır."** Bu yüzden adı *konuşma çizgisi*dir. Ayrıca oyun metinlerinde kişi adından sonra kullanılır.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/

- ✓ Diyalog:
  ```
  — Neredeydin?
  — Okuldaydım.
  ```
- ✗ "Türkçe — sondan eklemeli bir dil — bu yüzden farklıdır." (Bu, İngilizce em dash kullanımıdır; **Türkçe'de ara sözü kısa çizgi veya virgül/parantez taşır.**)
- ✓ "Türkçe -sondan eklemeli bir dil- bu yüzden farklıdır."
- ✓ "Türkçe, sondan eklemeli bir dil, bu yüzden farklıdır." (virgülle)

> **Yazım kılavuzu için en önemli tek fark bu olabilir:** İngilizce metinde em dash ( — ) retorik bir araçtır ve serbestçe kullanılır. Türkçe metinde uzun çizgi diyalog işaretidir. İngilizce taslaktan çevrilen Türkçe metinlerdeki em dash'ler, çevirinin en görünür izidir ve TDK'ye aykırıdır.

### 5.6 Tırnak işareti ( " " )
Doğrudan alıntıları, vurgulanan ifadeleri ve eser adlarını içine alır.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/
- ✓ "Cumhuriyet, fikren, ilmen, fennen kuvvetli nesiller ister." dedi.
- ✗ Tırnak içindeki eke kesme: ✓ "Nutuk"u okudum → TDK yazımında eser adına gelen ek kesmesiz de yazılabilir; en temizi tırnağı kapatıp eki dışarıda vermektir.
- **Not:** Türkçe'de tırnak `" "` biçimindedir. İngilizce curly quote (" ") veya Almanca `„ "` kullanımı çeviri/kopyala-yapıştır izidir. **[KAYNAKSIZ — biçim gözlemi]**

### 5.7 Üç nokta ( … )
Tamamlanmamış cümleyi, alıntıda atlanan bölümü, kaba/sakıncalı sözün yerini, ürperti/beklenti etkisini gösterir.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/
- ✓ "Ne diyeceğimi bilemedim…"
- ✗ Her paragrafı üç noktayla bitirmek (AI/pazarlama tiki).
- ✗ "...." (dört nokta) — üç nokta üç noktadır.

### 5.8 Soru eki ayrı yazılır
`-mı / -mi / -mu / -mü` ayrı yazılır; kendisinden sonraki ekler ona bitişir.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/soru-eki-mi-mi-mu-munun-yazilisi/
- ✓ "Kaldı **mı**?" / ✗ "Kaldımı?"
- ✓ "Verecek **misin**?" / ✗ "Vereceksin mi?"
- ✓ "Okuyor **muyuz**?"
- ✓ "Güzel **mi** güzel!" (pekiştirme)

### 5.9 Büyük harf
Cümle başı; dize başı; kişi ad ve soyadları; kişi adından önce/sonra gelen unvan, saygı sözü ve rütbeler; coğrafya adları; kurum-kuruluş-kurul adlarının **her kelimesi**; kitap, dergi, gazete ve sanat eserlerinin **her kelimesi**; millî ve dinî bayramlar; tarihî olaylar.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/
- ✓ "Türk Dil Kurumu", "Cumhuriyet Bayramı", "Kurtuluş Savaşı", "Ağrı Dağı"
- ✗ İngilizce Title Case'i Türkçe başlığa taşımak: "Ahşap Oyuncak Nasıl Seçilir" değil ✓ "Ahşap oyuncak nasıl seçilir?" — Türkçe'de başlıkta yalnızca cümle başı ve özel adlar büyüktür. **[KAYNAKSIZ — TDK başlık yazımı için ayrı kural vermez; kural cümle başı kuralından türetilmiştir]**

### 5.10 Sayıların yazımı
Sayılar harfle de rakamla da yazılabilir; ancak **saat, para tutarı, ölçü ve istatistik verilerde rakam zorunludur.** Birden fazla kelimeli sayılar ayrı yazılır ("üç yüz altmış beş"). Dört ve daha çok basamaklı sayılar sondan üçlü gruplara ayrılır (4.567 / 326.197). Kesirler virgülle ayrılır (15,2). Yüzde/binde işaretiyle sayı arasında boşluk bırakılmaz (%25). Sıra sayıları ya nokta ile (15.) ya da ekle (15'inci) yazılır. Üleştirme sayıları **yalnızca yazıyla** yazılır ("ikişer", "2'şer" değil). Cümleye rakamla başlamaktan kaçınılır.
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/
- ✓ "%25 indirim" / ✗ "% 25 indirim" / ✗ "25%"
- ✓ "1.250 TL" / ✓ "15,2 kg"
- ✓ "üç yüz altmış beş gün" / ✗ "üçyüzaltmışbeş gün"
- ✓ "3'er kişi" değil ✓ "üçer kişi"

### 5.11 Düzeltme işareti ( ^ )
Üç işlevi vardır: yazılışı aynı, anlamı farklı kelimeleri ayırmak ("hal / hâl", "adem / âdem"); Arapça-Farsça kökenli kelimelerde ince *g, k* ve ince *l* sonrası ünlüyü göstermek ("dergâh", "dükkân", "kâğıt", "Lâle"); nispet ekini ayırmak ("askerî" sıfat ≠ "askeri" isim). Türkçe ek geldiğinde işaret korunur: "millîleştirmek", "resmîlik".
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/duzeltme-isareti/
- ✓ "hâlâ" / ✗ "hala" (teyze anlamına gelir)
- ✓ "kâğıt", "dükkân", "rüzgâr"

### 5.12 Ayrı/bitişik yazılan birleşikler (sık hata alanı)
Yardımcı fiillerle kurulanlar ayrı ("arz etmek", "dans etmek"); hayvan-bitki tür adları ayrı ("ada balığı", "ayrık otu"); renk adları ("bal rengi", "boncuk mavisi"); yön/yer adları ("Doğu Anadolu", "Orta Asya"); "alt, üst, ana, ön, arka, iç, dış" ile kurulanlar ayrı ("arka plan", "iç savaş", "ön yargı" — ancak "önyargı" TDK'de bitişik değildir, "ön yargı" ayrıdır).
Kaynak: https://tdk.gov.tr/icerik/yazim-kurallari/ayri-yazilan-birlesik-kelimeler/
- ✓ "her şey" / ✗ "herşey"
- ✓ "bir şey" / ✗ "birşey"
- ✓ "hiçbir" (bitişik), "birçok" (bitişik), "birkaç" (bitişik)
- ✓ "yarın", "peki", "niçin" (bitişik)

---

## 6. İYİ TÜRKÇE YAZMA GELENEĞİ

### 6.1 Sadelik geleneği

**Nurullah Ataç.** Dil devriminin ve dilde yalınlaşmanın en ısrarlı savunucusu. Yazı diliyle konuşma dili arasındaki uçurumu kapatmak için öz Türkçe sözcükleri ve devrik cümleyi bilinçli olarak kullandı; tutumunun kişisel zevkten değil kuramsal bir tercihten kaynaklandığını savundu. Latince-Yunanca öğretilmeyen bir ülkede somut düşünme geleneğinin ancak kavramlar anlaşılır olduğunda gelişebileceğini öne sürdü.
Kaynak: https://tr.wikipedia.org/wiki/Nurullah_Ata%C3%A7

**Sabahattin Ali.** Öykülerinde "yalın bir dili tercih eder"; romanlarına göre daha az eski ifade kullanır. Öz Türkçede aşırıya gitmeye karşı çıktı, "dile yerleşen ve kalıplaşan kelimelerin kullanılması gerektiğini" düşündü. Karakterlerini yargılayarak değil betimleyerek anlatır; yerel ifadelere ve şiveye yer verir.
Kaynak: https://tr.wikipedia.org/wiki/Sabahattin_Ali
> **Çıkarılacak kural:** Sadelik ≠ kelime fakirliği. Yerleşmiş kelimeyi kullan; ne uydurmaya çalış, ne Osmanlıca tamlamaya kaç.

**Nermi Uygur.** Türkiye'de "felsefede denemeci anlayışın öncüsü" sayılır; "filozof denemeci gibi çalışırsa başarıya ulaşır" düşüncesiyle edebiyata yöneldi.
Kaynak: https://tr.wikipedia.org/wiki/Nermi_Uygur
> **Çıkarılacak kural:** Soyut/teknik konuyu anlatırken deneme tonunu koru — okuru düşünceye ortak et, sonucu ilan etme.

**Memet Fuat.** Türk edebiyat eleştirisinin merkezî isimlerinden; 1959'da Ataç Eleştiri Ödülü'nü aldı, *Düşünceye Saygı* (1960) ve *Eleştiri Sorumluluğu* (1994) gibi deneme-eleştiri kitapları yayımladı.
Kaynak: https://tr.wikipedia.org/wiki/Memet_Fuat
> Not: Wikipedia maddesi üslubuna dair ayrıntı vermiyor; üslup çıkarımı için birincil kaynak gerekir. **[KAYNAK YETERSİZ]**

**Ahmet Hamdi Tanpınar.** Edebiyat tarihçiliğinde "ayrıntılara büyük önem vermiş, edebî şahsiyetler ile metinler hakkındaki şairane üslubunu belgelere dayanan bilimsel bir tarih anlayışıyla harmanlamıştır."
Kaynak: https://tr.wikipedia.org/wiki/Ahmet_Hamdi_Tanp%C4%B1nar
> **Çıkarılacak kural:** Tanpınar, uzun ve dolanan cümlenin *işlevli* olabildiği kutbu temsil eder — ama bu kutup edebiyat içindir. Web metninde Tanpınar cümlesi taklit edilirse yalnızca uzunluk kalır, ritim kalmaz.

### 6.2 Devrik cümle tartışması

Tanım: "Devrik cümleler, öğeleri bir dilin yaygın kullanım kurallarına göre sıralanmamış cümlelerdir." Türkçe'de yüklemin sonda olmadığı cümlelerdir. **Bunlar dilbilgisi hatası değil, bilinçli yapısal tercihlerdir**; kurallı cümlenin (yüklem sonda) karşıtıdır. Üç kullanım amacı sayılır: edebî/sanatsal etki yaratmak, yüklemi vurgulamak, pratik iletişim ihtiyacı. Devrik cümle, yüklemi tamamen düşüren eksiltili cümleden ve gerçek dilbilgisi hatası olan anlatım bozukluğundan ayrılır.
Kaynak: https://tr.wikipedia.org/wiki/Devrik_c%C3%BCmle

Tarihsel bağlam: Ataç'ın devrik cümleyi programlı biçimde kullanması dönemin yazarlarını ve sonraki kuşakları etkiledi; kendisine "anlaşılmaz" eleştirisi de yöneltildi.
Kaynak: https://tr.wikipedia.org/wiki/Nurullah_Ata%C3%A7

**Web metninde ne zaman işe yarar? [KAYNAKSIZ — üslup önerisi]**
- **İşe yarar:** Uzun kurallı cümleler dizisinden sonra ritmi kırmak için; bir paragrafın son cümlesinde vurguyu öne almak için; diyalog veya doğrudan hitapta.
  - "Bunu üç kez denedik. Olmadı hiçbiri."
- **İşe yaramaz:** Başlıkta (arama sorgusuyla eşleşmez); teknik talimatta (belirsizlik yaratır); tablo/liste maddelerinde; ard arda iki cümlede.
- **Oran:** 20 cümlede en fazla 1-2.

### 6.3 Somut üslup önerileri (bu gelenekten damıtılmış)
**[KAYNAKSIZ — yukarıdaki kaynaklardan türetilmiş sentez]**
1. Yüklemi geciktirme. Türkçe'de fiil sondadır; özneyle fiil arasına üç satırlık tamlama koyarsan okur cümlenin başını unutur.
2. İsimleştirmeyi çöz. `-me/-ma` ile kurulan her isimden bir fiil çıkarılabilir. "İyileştirilmesi sağlanmıştır" → "İyileştirdik."
3. Edilgen çatıyı sadece fail bilinmiyorsa kullan.
4. Yerleşmiş kelimeyi seç; ne "mütehassıs" ne "uzmanlaşımcı" — "uzman".
5. Tamlama zincirini üçten fazla halkaya çıkarma. ("X'in Y'sinin Z'sinin iyileştirilmesi" okunmaz.)
6. Deyimi kullan, klişeyi kullanma. Deyim Türkçe'nin sıkıştırma aracıdır ("ipin ucunu kaçırmak"); klişe boşluk doldurucudur ("kaliteli ve güvenilir").
7. Bir paragrafta bir fikir.

---

## 7. TÜRKÇE-İNGİLİZCE ÇOK DİLLİ SEO

### 7.1 hreflang — Google'ın kuralları
- **Karşılıklılık zorunlu:** "Her dil versiyonu kendisinin yanı sıra diğer tüm dil versiyonlarını listelemelidir." X → Y veriyorsa Y → X de vermelidir.
- **Kendine referans (self-referencing) şart.**
- **Kodlar:** Dil için ISO 639-1 (`tr`, `en`), isteğe bağlı ülke için ISO 3166-1 Alpha 2 (`tr-TR`, `en-US`, `en-GB`).
- **Yalnızca ülke kodu geçersizdir.** `hreflang="tr"` doğru; `hreflang="TR"` niyeti ülke ise yanlıştır.
- **x-default:** Belirtilen dil/ülke kombinasyonlarının hiçbiriyle eşleşmeyen kullanıcılar için; dil seçici sayfalar için tasarlanmıştır.
- **Üç uygulama yolu:** `<head>` içinde `<link rel="alternate" hreflang="…" href="…">`, HTTP `Link` başlığı (PDF gibi HTML olmayan dosyalar için), XML sitemap içinde `<xhtml:link>`.
- **Sık hatalar:** eksik karşılıklı bağlantı, geçersiz/ayrılmış ülke kodları ("EU", "UK"), desteklenmeyen bölge kodları.
Kaynak: https://developers.google.com/search/docs/specialty/international/localized-versions

### 7.2 URL yapısı ve yönlendirme
Google dört seçenek sayar: ccTLD (`example.com.tr` — en net hedefleme, en pahalı), alt alan adı (`tr.example.com` — kurulumu kolay, hedefleme URL'den anlaşılmayabilir), alt dizin (`example.com/tr/` — bakımı düşük, tek sunucu konumu), URL parametresi (önerilmez).
**Otomatik yönlendirmeden kaçının:** "Kullanıcıları bir sitenin dil versiyonundan başka bir sürüme yönlendirmeyin" — bu, arama motorlarının tüm sürümleri görmesini engelleyebilir.
**Sayfa başına tek dil:** Aynı sayfada dilleri karıştırmak, aynı içeriğin birden fazla dilde arama sonuçlarında görünmesine yol açabilir. Google dili **görünür içerikten** belirler, kod düzeyindeki bilgiden değil.
Kaynak: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites

**Pratik öneri [KAYNAKSIZ — sentez]:** Türkçe+İngilizce ikili bir site için alt dizin (`/tr/` ve `/en/`) en düşük maliyetli, en dayanıklı yapıdır. Kullanıcıyı otomatik yönlendirmek yerine, tarayıcı diline göre üstte bir bant göster ve seçimi kullanıcıya bırak.

### 7.3 Çeviri mi, yeniden yazım (transcreation) mı?
Google, otomatik üretilen/değer katmayan ölçekli içeriği spam sayar; makine çevirisi de bu kapsamda değerlendirilebilir.
Kaynak: https://developers.google.com/search/docs/essentials/spam-policies

**Neden Türkçe'de çeviri yetmez [KAYNAKSIZ — dilbilimsel gerekçe]:**
1. **Sorgu dili farklıdır.** İngilizce "best wooden toys for toddlers" → Türkçe'de "1 yaş ahşap oyuncak" veya "montessori oyuncak 2 yaş". Kelime kelime çeviri hiçbir Türkçe sorguyla eşleşmez.
2. **Başlık sözdizimi farklıdır.** "How to Choose a Wooden Toy" → ✗ "Nasıl Bir Ahşap Oyuncak Seçilir" → ✓ "Ahşap oyuncak nasıl seçilir?"
3. **Uzunluk oranı farklıdır.** Türkçe metin, ekler nedeniyle aynı bilgiyi genellikle daha az kelimeyle ama daha uzun kelimelerle taşır; İngilizce'den çevrilen metin karakter sayısı olarak şişer. Meta description ve buton metinleri taşar.
4. **Kültürel referans karşılığı yoktur.** ABD ölçüleri (inch, fahrenheit), federal kurumlar, "Black Friday" dışındaki takvim; Türkçe'de karşılığı yeniden kurulmalıdır.
5. **Ters yön:** Türkçe'den İngilizce'ye çeviride, Türkçe'nin ikilemeleri ("tıkır tıkır", "ufak tefek"), deyimleri ve `-mış` (rivayet/dolaylı aktarım) kipi karşılıksız kalır. `-mış` İngilizce'de zorunlu olarak "apparently / it is said that" gibi bir ek yapıya dönüşür, aksi hâlde Türkçe'de var olan "ben tanık değilim" bilgisi kaybolur.

**Kural:** Anahtar kelime araştırması **dil başına ayrı** yapılır. Aynı sayfanın iki dildeki sürümü aynı H2 setine sahip olmak zorunda değildir. Ortak olan şey **konu ve niyet**tir, cümleler değil.

---

## 8. TÜRKÇE İÇERİK REKABETİ

### 8.1 Nicel çerçeve
W3Techs'in içerik dili istatistiğine göre (26 Ağustos 2026):

| Sıra | Dil | Web sitelerindeki pay |
|---|---|---|
| 1 | İngilizce | %49,5 |
| 2 | İspanyolca | %6,0 |
| 3 | Almanca | %5,9 |
| 4 | Japonca | %4,9 |
| 5 | Fransızca | %4,5 |
| 6 | Portekizce | %4,1 |
| 7 | Rusça | %3,4 |
| 8 | İtalyanca | %2,8 |
| 9 | Hollandaca | %2,2 |
| 10 | Lehçe | %1,8 |
| **11** | **Türkçe** | **%1,6** |
| 12 | Çince | %1,3 |

Kaynak: https://w3techs.com/technologies/overview/content_language

Buna karşılık Türkiye'de 77,5 milyon internet kullanıcısı vardır (nüfusun %88,3'ü).
Kaynak: https://datareportal.com/reports/digital-2026-turkey

**Arz-talep açığı:** Web'in içeriğinin %1,6'sı Türkçe iken, dünya internet kullanıcılarının kabaca %1,4-1,5'i Türkiye'dedir; ancak bu oran *sayfa sayısını* verir, *kaliteli sayfa sayısını* değil.

### 8.2 "Türkçe'de kaliteli içerik daha kolay sıralanır" tezi — kanıt durumu

**Destekleyen dolaylı kanıt (sourced):** Türkçe web içeriğinin okunabilirlik düzeyi ölçülmüş ve sistematik olarak hedef kitlesinin çok üstünde bulunmuştur. Sigara bırakma sitelerinde medyan Ateşman 48,47 ("zor"), Bezirci-Yılmaz 13,08 ("lisans"); yazarların yorumu: "Bu sonuçlar halkımızın eğitim seviyesinin çok üstündedir."
Kaynak: https://doi.org/10.51982/bagimli.829808
Aynı örüntü obezite/bariatrik cerrahi sitelerinde (https://doi.org/10.33808/clinexphealthsci.763167) ve şaşılık sitelerinde (https://doi.org/10.7759/cureus.58603) tekrarlanmıştır. Şaşılık çalışmasında siteler ayrıca JAMA (0,8/4) ve DISCERN (34,2/80) ölçütlerinde **düşük kalite** çıkmıştır.

Yani en azından sağlık alanında, Türkçe web içeriğinin hem okunabilirliği hem içerik kalitesi ölçülü biçimde düşüktür. Basit ve doğru yazılmış Türkçe içeriğin rakiplerine göre net bir kalite avantajı olduğu bu üç bağımsız çalışmayla desteklenir.

**Doğrudan kanıt yok [KAYNAKSIZ]:** "Türkçe'de aynı kalitede içeriğin İngilizce'ye göre daha kolay sıralandığı" iddiasını doğrudan ölçen, yayımlanmış bir sıralama çalışması bulunamadı. Bu tez, aşağıdaki dolaylı gerekçelere dayanır ve kılavuzda **hipotez** olarak sunulmalıdır:
1. Türkçe'de içerik hacmi daha düşük (%1,6), dolayısıyla belirli bir uzun kuyruk sorgusunda rakip sayfa sayısı azdır.
2. Türkçe web'de yayınlayanların büyük bölümü çeviri veya otomatik üretim kullanır; ölçülmüş okunabilirlik verileri bunu destekler.
3. Google'ın dil anlama katmanı BERT sonrası dilden dile aktarım yapıyor (https://blog.google/products/search/search-language-understanding-bert/), yani Türkçe'de "sistemin anlamadığı" bir avantaj alanı kalmıyor — kalite sinyalleri Türkçe'de de işliyor.

### 8.3 Boşluk olan alanlar [KAYNAKSIZ — gözlem]
- **Yerelleştirilmemiş teknik konular:** Türkçe'de var olan içerik çoğunlukla İngilizce kaynakların özetidir; birincil deney, ölçüm veya vaka içeren Türkçe içerik nadirdir.
- **Yandex boyutu:** Türkiye'deki aramaların %17,5'i Yandex'te (https://gs.statcounter.com/search-engine-market-share/all/turkey). İngilizce SEO literatürünün tamamen yok saydığı bu kanal ölçülebilir bir trafik farkıdır.
- **Okunabilirlik:** Yukarıdaki verilere göre Türkçe web'in ortalama okunabilirliği "zor" bandındadır. Ateşman 65-75 bandında yazmak, ölçülebilir ve kopyalanması zor bir farklılaşmadır.
- **Türkçe karakter tutarlılığı ve TDK uyumu:** Kesme işareti, de/da, ki hatalarının yaygınlığı, doğru yazımı bir güven sinyaline dönüştürüyor.

---

## 9. YAZIM KILAVUZUNA GİRECEK ÖZET KURALLAR

1. Anahtar kelimeyi değil, **kök öbeğini** hedefle; metinde her geçişte cümlenin gerektirdiği eki kullan.
2. `-mektedir/-maktadır`ı sıfırla.
3. Edilgen çatıyı yalnızca fail bilinmiyorsa kullan.
4. Cümle ortalaması 12-18 kelime; 6+ heceli kelime paragraf başına en fazla 1.
5. Ateşman puanını 60-75 bandında tut; Bezirci-Yılmaz'ı 8-12 bandında.
6. Uzun çizgi ( — ) yalnızca diyalogda; ara söz için kısa çizgi veya virgül.
7. Soru eki, de/da bağlacı, ki bağlacı **ayrı**.
8. Kurum adlarına kesme koyma; özel adlara koy.
9. Başlıkta Türkçe soru sözdizimi kullan ("X nasıl yapılır?"), İngilizce sözdizimini çevirme.
10. URL slug'ında Türkçe karakter kullanma; metinde her zaman kullan.
11. İngilizce ve Türkçe için ayrı anahtar kelime araştırması, ayrı H2 seti; ortak olan yalnızca konu ve niyettir.
12. hreflang'i karşılıklı ve kendine referanslı kur; otomatik yönlendirme yapma.
13. Bölüm 4.2'deki kalıp listesini yayın öncesi tarama listesi olarak kullan.

---

## 10. KAYNAK DİZİNİ

**Arama motorları / SEO**
- Google — Ranking Results (eş anlamlı sistemi, %30 iddiası): https://www.google.com/search/howsearchworks/how-search-works/ranking-results/
- Google — Spam Policies (keyword stuffing, scaled content abuse): https://developers.google.com/search/docs/essentials/spam-policies
- Google — Creating Helpful Content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google — Localized Versions / hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions
- Google — Managing Multi-Regional Sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Google Ads — Search terms report / close variants tanımı: https://support.google.com/google-ads/answer/2472708
- Google Ads — Keyword Planner: https://support.google.com/google-ads/answer/7337243
- Google Blog — BERT in Search: https://blog.google/products/search/search-language-understanding-bert/

**İstatistik**
- StatCounter — Türkiye arama motoru payı: https://gs.statcounter.com/search-engine-market-share/all/turkey
- StatCounter — Türkiye platform payı: https://gs.statcounter.com/platform-market-share/desktop-mobile-tablet/turkey
- DataReportal — Digital 2026 Turkey: https://datareportal.com/reports/digital-2026-turkey
- W3Techs — Content Languages: https://w3techs.com/technologies/overview/content_language

**Türkçe dil ve bilgi erişimi**
- Can et al., *Information retrieval on Turkish texts* (JASIST): https://doi.org/10.1002/asi.20750
- *Effects of diacritics on Turkish information retrieval*: https://doi.org/10.3906/elk-1010-819
- Oflazer, *Two-level Description of Turkish Morphology*: https://doi.org/10.1093/llc/9.2.137
- *Impact of Tokenization on Language Models: An Analysis for Turkish*: https://doi.org/10.1145/3578707
- *Unlimited vocabulary speech recognition for agglutinative languages*: https://doi.org/10.3115/1220835.1220897
- Wikipedia — Turkish language: https://en.wikipedia.org/wiki/Turkish_language
- Wikipedia — Turkish alphabet: https://en.wikipedia.org/wiki/Turkish_alphabet

**Okunabilirlik**
- Ateşman ve Bezirci-Yılmaz formülleri (birebir): https://doi.org/10.7759/cureus.58603
- Bezirci-Yılmaz formülü (doğrulama): https://doi.org/10.7759/cureus.16639
- Bezirci & Yılmaz 2010 orijinal bildiri: https://doi.org/10.1109/siu.2010.5652572
- Türkçe web okunabilirliği (sigara bırakma): https://doi.org/10.51982/bagimli.829808
- Türkçe web okunabilirliği (obezite): https://doi.org/10.33808/clinexphealthsci.763167
- Flesch-Kincaid formülleri ve İngilizce'ye özgülüğü: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests

**TDK yazım kuralları**
- Dizin: https://tdk.gov.tr/kategori/icerik/yazim-kurallari/
- Noktalama işaretleri (kısa çizgi, uzun çizgi, tırnak, üç nokta): https://tdk.gov.tr/icerik/yazim-kurallari/noktalama-isaretleri-aciklamalar/
- Bağlaç olan da/de: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-da-denin-yazilisi/
- Bulunma durumu eki -da/-de/-ta/-te: https://tdk.gov.tr/icerik/yazim-kurallari/bulunma-durumu-eki-da-de-ta-tenin-yazilisi/
- Bağlaç olan ki: https://tdk.gov.tr/icerik/yazim-kurallari/baglac-olan-kinin-yazilisi/
- Kesme işareti: https://tdk.gov.tr/icerik/yazim-kurallari/kesme-isareti/
- Kısaltmalar: https://tdk.gov.tr/icerik/yazim-kurallari/kisaltmalar/
- Büyük harflerin kullanıldığı yerler: https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/
- Sayıların yazılışı: https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/
- Soru eki mı/mi/mu/mü: https://tdk.gov.tr/icerik/yazim-kurallari/soru-eki-mi-mi-mu-munun-yazilisi/
- Düzeltme işareti: https://tdk.gov.tr/icerik/yazim-kurallari/duzeltme-isareti/
- Ayrı yazılan birleşik kelimeler: https://tdk.gov.tr/icerik/yazim-kurallari/ayri-yazilan-birlesik-kelimeler/

**Üslup geleneği**
- Nurullah Ataç: https://tr.wikipedia.org/wiki/Nurullah_Ata%C3%A7
- Sabahattin Ali: https://tr.wikipedia.org/wiki/Sabahattin_Ali
- Nermi Uygur: https://tr.wikipedia.org/wiki/Nermi_Uygur
- Memet Fuat: https://tr.wikipedia.org/wiki/Memet_Fuat
- Ahmet Hamdi Tanpınar: https://tr.wikipedia.org/wiki/Ahmet_Hamdi_Tanp%C4%B1nar
- Devrik cümle: https://tr.wikipedia.org/wiki/Devrik_c%C3%BCmle

---

## 11. KAYNAKSIZ KALAN İDDİALARIN LİSTESİ (şeffaflık)

Aşağıdaki bölümler yayımlanmış kaynakla desteklenememiştir; dilbilimsel gerekçe veya metin gözlemine dayanır:
1. Türkçe'de eklerin arama hacmi dağılımı örüntüsü (Bölüm 1.4, madde 3).
2. Türkçe soru kalıpları tablosu (Bölüm 2.3) — kalıplar dilbilgisel olarak doğrudur, hacim sıralaması ölçülmemiştir.
3. Türkçe'ye özgü AI kalıp listesinin tamamı (Bölüm 4.2). Türkçe için yayımlanmış bir AI-metin işaretleyici listesi bulunamadı; her başlığın dilbilimsel gerekçesi Bölüm 4.1'de verilmiştir.
4. Çeviri kokusu tablosu (Bölüm 4.2/G-K).
5. Cümle/paragraf uzunluğu sayısal normları (Bölüm 3.5) — formüllerden türetilmiş çalışma kurallarıdır, ampirik norm değildir.
6. Türkçe başlıklarda Title Case kullanılmaması kuralı (Bölüm 5.9) — TDK başlık yazımı için ayrı kural vermiyor.
7. Devrik cümlenin web metnindeki kullanım oranı önerisi (Bölüm 6.2).
8. "Türkçe'de kaliteli içerik daha kolay sıralanır" tezinin doğrudan kanıtı (Bölüm 8.2) — yalnızca dolaylı kanıt vardır.
9. Boşluk alanları listesi (Bölüm 8.3).
10. Memet Fuat'ın üslubuna dair çıkarım — Wikipedia maddesi yetersiz.
