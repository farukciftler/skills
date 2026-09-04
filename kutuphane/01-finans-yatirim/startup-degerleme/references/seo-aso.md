# Bulunabilirlik: SEO, ASO ve Marka Talebi

**Her raporda zorunlu.** İndirme sayısı "kaç kişi geldi" sorusunu cevaplar. Bulunabilirlik
"gelmeye devam eder mi" sorusunu cevaplar. Bir alıcı için ikincisi daha pahalıdır, çünkü
satın aldığı şeyin kendi kendine kullanıcı üretip üretmediğini belirler.

Reklam durduğunda ayakta kalan tek kanal organik bulunabilirliktir. Organik kanalı olmayan
bir ürün, alıcının her ay para koymayı sürdürmesi şartıyla yaşar. Bu, satın alınan şeyin
bir varlık değil bir gider taahhüdü olduğu anlamına gelir ve fiyatı doğrudan düşürür.

## Ölçüm

```bash
python3 scripts/seo_aso_tara.py --ios-id 6633421265 --marka uniboom \
  --site uniboom.com.tr \
  --kelimeler "üniversite,kampüs,öğrenci,üniversite sosyal,kampüs ağı,kampüs etkinlik" \
  --rakip-ios-id 6744582219 --rakip-marka kampusify --ulke tr
```

Script dört şeyi ölçer.

### 1. App Store arama sırası
`itunes.apple.com/search` alaka sırası kullanılır. Bu gerçek App Store sıralaması değil,
ona yakın bir vekildir; raporda `[T]` etiketiyle geçer. Yine de karşılaştırma için
güvenilirdir çünkü hedef ve rakip aynı sorguda aynı ölçütle sıralanır.

Kelime seçimi ölçümün kalitesini belirler. Üç grup seç:
- **Ticari kelimeler**: kullanıcının ürünü bilmeden arayacağı terimler (üniversite, kampüs,
  öğrenci). Asıl önemli olanlar bunlar.
- **Kategori kelimeleri**: kampüs ağı, öğrenci sosyal medya.
- **Marka kelimesi**: kendi adı. Burada birinci olmak bir başarı değil, olmamak felakettir.

Kelime kapsamı, ürünün ilk 100'de göründüğü kelime sayısı bölü test edilen kelime sayısı.
Yüzde 35'in altı, indirmelerin neredeyse tamamının dışarıdan yönlendirmeyle geldiği anlamına
gelir. Yönlendirme durduğunda büyüme de durur.

Ürünün yalnızca kendi alt başlığındaki ifadede sıralanması sık görülen bir yanılsamadır.
"Kampüsün Sosyal Medyası" alt başlığı olan bir uygulama "kampüs sosyal ağ" aramasında çıkar.
Bu bir ASO başarısı değil, mağazanın metni geri yansıtmasıdır. Kimse o cümleyi aramaz.

### 2. Mağaza listeleri
Apple'ın ücretsiz RSS ucu genel ilk 100'ü verir. Bu yüksek bir eşiktir ve küçük ürünlerde
ayırt edici değildir; hem hedef hem rakip listede yoksa bulgu üretmez, raporda bunu yaz.
Kategori listesi ücretsiz uçla alınamıyor, gerekiyorsa mağaza uygulamasından elle bakılır.
Google Play'in resmî listesi yok.

### 3. Site teknik SEO
Bakılanlar: title, meta description, Open Graph, schema.org, canonical, h1, iç link sayısı,
mağaza indirme linki, robots.txt, sitemap.xml, indekslenebilir kelime sayısı.

Bunların hepsi birkaç günlük iştir. Eksik olmaları teknik borçtan çok, **organik kanala hiç
yatırım yapılmadığının** işaretidir. Ürün sitesinde mağaza indirme linki bile yoksa, site
zaten bir dönüşüm aracı olarak düşünülmemiş demektir.

300 kelimenin altındaki bir site arama motorunda hiçbir şeyde sıralanamaz. Bu, aynı zamanda
ucuz bir fırsattır: içerik üretme kabiliyeti olan bir ekip için birkaç haftalık iş, ve
alıcıya gösterilebilecek somut bir organik kanal başlangıcı yaratır.

### 4. Marka arama talebi
Google otomatik tamamlama, arama talebinin ücretsiz vekilidir. Markayı yazıp gelen önerilere
bak. Üç sonuç mümkün:

| Sonuç | Anlamı | Değere etkisi |
|---|---|---|
| Öneri yok | Marka için anlamlı arama talebi yok. Kimse aramıyor | Marka bir varlık değil |
| Öneriler ürünle ilgili | Marka tanınıyor, insanlar hakkında soru soruyor | Gerçek marka değeri var |
| Öneriler başka bir sektöre ait | Marka adı daha güçlü bir oyuncuya ait | Devirde ek maliyet |

Üçüncü durum en çok gözden kaçanı. Marka adı başka bir sektörde daha güçlü bir şirkete aitse,
alıcı markayı konumlandırmak için harcama yapmak zorunda kalır. Kullanıcı ürünü adıyla
aradığında karşısına başka bir şirket çıkar. Bu, isim değişikliği maliyetine kadar gidebilir
ve fiyattan düşer.

Rakibin markasını da aynı sorguyla ölç. Rakip için "X nedir", "X indir", "X yorum" önerileri
çıkıyor da hedef için hiçbir şey çıkmıyorsa, aradaki fark reklam bütçesi farkı değil,
kültürel varlık farkıdır ve para ile hızlı kapanmaz.

## Raporda nasıl yazılır

Üç sayıyı birlikte ver: **kelime kapsamı**, **sitenin indekslenebilir kelime sayısı**,
**marka önerilerinin ürünle ilgili oranı**. Rakiple yan yana koy; tek başına bir sayı
anlamsız, karşılaştırma anlamlıdır.

Sonra tek cümleyle bağla: bu ürün organik olarak bulunuyor mu, bulunmuyorsa büyümenin
kaynağı ne, o kaynak alıcıya devredilebilir mi.
