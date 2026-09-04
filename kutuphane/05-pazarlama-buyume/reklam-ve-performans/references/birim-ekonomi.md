# Birim Ekonomi — Maliyet Kıyasları, Huni Matematiği, Bütçe Tahsisi

## İçindekiler

1. Kıyas verilerini nasıl kullanacaksın (ve nasıl kullanmayacaksın)
2. Türkiye maliyet kıyasları — Google
3. Türkiye maliyet kıyasları — Meta, TikTok
4. Global emlak kıyasları (yalnızca oran çıkarmak için)
5. Pazar bağlamı — talep tarafı
6. Huni matematiği: hedef CPL'i satıştan geriye hesaplama
7. Kanal bazında CPL türetme (örnek hesap)
8. Bütçe tahsisi ve senaryo tablosu
9. Hangi metrik ne zaman yalan söyler

---

## 1. Kıyas verilerini nasıl kullanacaksın

Aşağıdaki rakamların hiçbiri Moonstone'un verisi değil. İşlevleri iki tane:
**büyüklük mertebesi vermek** ve **bir teklifin/sonucun makul olup
olmadığını sınamak**. "Ajans 250 TL'ye lead getiririz dedi" cümlesini bu
tablolarla tartarsın; kampanya hedefini bu tablolarla koymazsın.

Kaynak kalitesi konusunda dürüst ol. Aşağıdaki verilerin çoğu **ajans blogu
seviyesinde**, birincil platform verisi değil. Bunları aktarırken kaynağı ve
tarihi yaz, aralık geniş ise geniş bırak. Sahte kesinlik, yokluktan kötüdür.

**İlk gerçek veriden sonra bu dosya devre dışıdır.** 30 günlük kendi verimiz
geldiğinde kıyas tablosu yalnızca "biz sektöre göre nerede duruyoruz"
sorusuna hizmet eder, hedef koymaya değil.

Kur referansı: **USD/TRY ≈ 48** (25 Ağustos 2026). Kur hareketi Türkiye'de
CPM'i doğrudan etkiler — platformlar açık artırmayı dolar tabanlı yürütür,
lira zayıfladıkça TL cinsinden maliyet yükselir. Son 12 ayda lira dolar
karşısında ~%17 değer kaybetti; **TL bütçe sabit tutulursa reklam hacmi
her ay biraz erir.** Yıllık plan yapılırken bütçeye kur artışı payı koy.

---

## 2. Türkiye maliyet kıyasları — Google Ads

| Metrik | Değer | Kaynak / not |
|---|---|---|
| Arama Ağı ortalama TBM (tüm sektörler, Ç1 2026) | **5,20 TL** | 2025: 4,60 TL · 2024: 3,80 TL — yıllık ~%13 artış trendi |
| Gayrimenkul sektörü TBM aralığı | **35 – 110 TL** | Yüksek niyetli, rekabetçi terimler |
| "Satılık ev" tipi jenerik aramalar | **9 – 26 TL** | Aynı kaynak, düşük niyet ucu |
| Gayrimenkul arama ağı CTR | **~%3,71** | |
| Gayrimenkul dönüşüm oranı (CVR) | **~%2,47** | |
| Gayrimenkul EBM (CPA) | **116 USD üzeri** (≈ 5.500 TL) | Bu rakam offline dönüşüm aktarımını zorunlu kılan seviyedir |

> **Uyarı:** 35–110 TL ile 9–26 TL aralıkları aynı kaynaktan ve çelişkili
> görünüyor. Doğru okuma: terim tipine göre 10 kat fark var. "satılık ev"
> jenerik ve ucuz; "Tuzla satılık 3+1 rezidans" dar, pahalı ve değerli.
> Bir bütçe planında bu iki ucu ayrı kampanya olarak ele al, ortalamasını alma.

---

## 3. Türkiye maliyet kıyasları — Meta ve TikTok

| Metrik | Değer | Not |
|---|---|---|
| Emlak sektörü CPM | **60 – 120 TL** | |
| Emlak sektörü CPC | **3 – 7 TL** | |
| Instagram genel CPC | **0,25 – 2,50 USD** (≈ 12 – 120 TL) | Aralık çok geniş; kreatif kalitesi belirleyici |
| Genel Türkiye CPM | **3 – 7 USD** (≈ 145 – 335 TL) | Emlak rakamıyla çelişiyor — emlak rakamı daha muhafazakâr, onu kullan |
| TikTok CPM | **30 – 120 TL** | Rekabetçi kategorilerde 150 TL'ye çıkabiliyor |

**Google ile Meta arasındaki CPC uçurumu (35–110 TL vs 3–7 TL) yanıltıcıdır
ve bu skill'in en çok tekrarlaması gereken uyarıdır.** Meta'da tık 10-20 kat
ucuz çünkü niyet 10-20 kat düşük. Karşılaştırma tık düzeyinde değil,
**nitelikli lead (randevu) düzeyinde** yapılır.

---

## 4. Global emlak kıyasları

Türkiye rakamlarının yerine geçmezler. İşlevleri **oran çıkarmak**: örneğin
Google CPL'in Meta CPL'inin kaç katı olduğu, ülkeden bağımsız olarak
benzer bir orandır.

| Platform | Metrik | Değer (2026, ABD ağırlıklı) |
|---|---|---|
| Google Ads | Emlak ortalama CPC | 3,22 USD (yıllık +%27) |
| Google Ads | Emlak dönüşüm oranı | %3,70 |
| Google Ads | Emlak CPL | ~102 USD |
| Meta | Emlak CPL (konut) | 18 – 35 USD |
| Meta | Emlak CPM | 14 – 22 USD (bazı analizlerde 29,85 USD) |
| Meta | Emlak bağlantı CTR | %0,8 – %1,4 |
| WhatsApp (tıkla-sohbet) | Lead başı | 22 – 38 USD |

**Çıkarılacak oran:** Google CPL ≈ Meta CPL × 3-5. Bu oran Türkiye'de de
benzer beklenir ve bütçe tahsisinin mantığıdır: Meta hacim, Google nitelik.

---

## 5. Pazar bağlamı — talep tarafı (TÜİK, Temmuz 2026)

Reklam maliyeti kadar önemli: talep hangi yönde?

| Gösterge | Temmuz 2026 | Yıllık değişim |
|---|---|---|
| Toplam konut satışı | 123.603 | **−%17** |
| İlk el (sıfır) konut satışı | 42.529 | −%8,6 |
| İlk el payı | %34,4 | — |
| İkinci el satış | 81.074 | −%20,8 |
| **İpotekli satış** | — | **+%23,7** |
| Yabancıya satış | 2.120 (pay %1,7) | +%1,9 |
| Yabancı alıcıda ilk üç ülke | Rusya (394), İran (189), Ukrayna (145) | — |

Konut kredisi faizi Ağustos 2026'da aylık **%2,87 – %3,73** bandında
[KIYAS: Hesapkurdu, 21-23 Ağustos 2026].

**Bu tablonun reklam anlamı:**
- Pazar daralıyor ama **ipotekli satış artıyor** — yani alıcı var, krediyle
  alıyor. Mesajın "yatırım fırsatı"ndan çok **ödeme kolaylığı ve finansman**
  tarafına yaslanması bu veriyle destekleniyor. (Banka anlaşması bilgisi
  elimizde yok: `[DOĞRULA: banka anlaşması ve ödeme planı]`)
- İlk el, ikinci elden daha az daraldı — sıfır proje göreli olarak dayanıklı.
- Yabancı alıcı payı %1,7 ve Rusya/İran/Ukrayna ağırlıklı. **Çok dilli site
  ve yabancı hedefli kampanya, %1,7'lik bir pay için yapılacak yatırımdır** —
  Moonstone'un böyle bir hedefi var mı bilinmiyor, varsayma, sor.

---

## 6. Huni matematiği: hedef CPL'i satıştan geriye hesapla

Bütçe "ne ayırabiliriz" ile değil, "bir satış ne kazandırıyor" ile başlar.

```
Hedef CPL = (Satış başı brüt katkı × Lead → Satış oranı) / Pazarlama pay katsayısı
```

Adım adım:

1. **Satış başı brüt katkı**: Bir daire satışından projeye kalan kâr payı.
   `[DOĞRULA: daire fiyatı ve birim kârlılık]` — elimizde yok, kullanıcıya sor.
2. **Lead → Satış oranı**: Kaç lead bir satışa dönüyor. Emlakta bu oran
   düşüktür ve kanaldan kanala 10 kat değişir. Kendi verimiz gelene kadar
   **kanal bazında ayrı varsay**, tek ortalama kullanma.
3. **Pazarlama pay katsayısı**: Satıştan kalan katkının kaçta kaçını medyaya
   ayırabiliyoruz. 3 katsayısı = katkının üçte biri pazarlamaya.

**Örnek [MUHAKEME — gerçek veri değil, formülün nasıl işlediğini gösterir]:**

Diyelim satış başı brüt katkı 400.000 TL, lead→satış oranı %1,5, katsayı 4:
```
Hedef CPL = (400.000 × 0,015) / 4 = 1.500 TL
```
Bu, **ham lead** için tavan değil, **ortalama** hedeftir. Meta'dan 200 TL'ye
gelen lead ile Google'dan 1.400 TL'ye gelen lead aynı sepette toplanır ve
ortalama tutar — asıl soru hangisinin randevuya döndüğüdür.

**Aynı hesabı nitelikli lead için tekrarla.** Nitelikli lead (randevu alınmış,
bütçesi projeye uyan) sayısı, ham lead sayısından çok daha güvenilir bir
optimizasyon hedefidir:
```
Hedef nitelikli-lead maliyeti = (400.000 × 0,15) / 4 = 15.000 TL
```
(Burada %15, nitelikli lead → satış oranı varsayımı.)

Bu iki rakamı yan yana koyduğunda kampanya kararı netleşir: **CPL 200 TL ama
randevu maliyeti 25.000 TL olan kanal, CPL 1.400 TL ama randevu maliyeti
9.000 TL olan kanaldan pahalıdır.** Emlak reklamcılığında kazanan bu ayrımı
gören taraftır.

---

## 7. Kanal bazında CPL türetme (örnek hesap)

Kendi verimiz yokken bir kampanyanın ne getirebileceğini şöyle tahmin et.
Her adımda kullandığın varsayımı yaz ki kullanıcı itiraz edebilsin.

**Meta lead formu — 50.000 TL/ay [MUHAKEME]**
```
CPM 90 TL varsayımı        → 555.000 gösterim
Bağlantı CTR %1,1          → ~6.100 tık
Lead formu dönüşümü %10    → ~610 lead
CPL                        → ~82 TL
Nitelikli oran %8          → ~49 randevu → randevu başı ~1.020 TL
```

**Google Arama — 50.000 TL/ay [MUHAKEME]**
```
Ortalama TBM 45 TL         → ~1.110 tık
Açılış sayfası dönüşümü %3 → ~33 lead
CPL                        → ~1.515 TL
Nitelikli oran %35         → ~12 randevu → randevu başı ~4.330 TL
```

Bu iki hesabın öğrettiği: aynı parayla Meta 610, Google 33 lead veriyor;
ama randevu tarafında fark 49'a 12'ye iniyor. **Meta hacim üretir, Google
niyet üretir, ikisi de gerekir.** Ve dikkat: Meta'nın nitelikli oranı (%8)
tamamen varsayım — bu skill'in ilk 30 gün sonunda ölçmesi gereken tek en
önemli sayı budur.

Nitelikli oranlar ölçüldükçe bu tabloyu kendi verinle yeniden kur.

---

## 8. Bütçe tahsisi ve senaryo tablosu

Kademeler `SKILL.md` içinde. Burada tahsisi bir plana çevirmenin sırası:

| Adım | Soru | Karar |
|---|---|---|
| 1 | Ölçüm kurulu mu? | Değilse bütçenin %0'ı reklama, %100'ü kuruluma |
| 2 | Marka araması korunuyor mu? | Aylık birkaç bin TL — ilk ve en ucuz kalem |
| 3 | Remarketing havuzu var mı (30 günde 1.000+ site ziyareti) | Yoksa remarketing bütçesi ayırma, prospecting'e koy |
| 4 | Kaç kreatif hazır? | 4'ten az kreatifle Meta bütçesi artırma — kreatif tükenir, CPM tırmanır |
| 5 | Satış ekibi günde kaç lead işleyebiliyor? | Kapasitenin üstünde lead üretmek, lead'i çöpe atmaktır |

Adım 5 en çok atlanan ve en pahalı olanıdır. Günde 10 lead işleyebilen bir
ekibe günde 40 lead gönderen kampanya, CPL'i düşürürken satışı düşürür.

**Sezonluk not:** Türkiye'de reklam açık artırması yılın belirli
dönemlerinde sertleşir (yılsonu, büyük indirim dönemleri, seçim dönemleri).
Emlak için ayrıca bayram ve yaz tatili dönemlerinde karar süreci uzar.
Bu etkiler için elimizde veri yok — gözlemleyip not al, varsayma.

---

## 9. Hangi metrik ne zaman yalan söyler

| Metrik | Ne zaman yalan söyler | Yerine bak |
|---|---|---|
| **CPL** | Lead kalitesi değiştiğinde. Lead formunu kısaltınca CPL yarıya iner, satış değişmez | Nitelikli lead maliyeti |
| **CTR** | Kreatif merak uyandırıp yanlış beklenti kurduğunda ("fiyat" yazıp fiyat vermeyen reklam) | CTR × açılış sayfası dönüşüm oranı |
| **ROAS** | Emlakta satış döngüsü aylar sürdüğü için reklam ayına yazılmaz | Kohort bazlı: "Mart lead'lerinden bugüne kaç satış" |
| **Gösterim / erişim** | Her zaman. Erişim bir maliyettir, sonuç değil | Erişim yerine sıklık (frequency) ve hatırlanma |
| **Platform içi dönüşüm sayısı** | İki platform aynı dönüşümü kendine yazdığında. Toplam, gerçeğin 1,5-2 katı görünür | CRM'deki tekil lead sayısı — tek gerçek kaynak |
| **Ortalama pozisyon / gösterim payı** | Bütçe kısıtlıyken. Gösterim payını yükseltmek her zaman kârlı değildir | Marjinal lead maliyeti: bütçeyi %20 artırınca CPL ne oldu |

Son satır özellikle önemli: **bütçe artırma kararı ortalama CPL'e değil,
marjinal CPL'e bakılarak verilir.** Son eklenen 20.000 TL, ortalamadan
%40 pahalı lead getiriyorsa o para başka kanalda daha iyi çalışır.
