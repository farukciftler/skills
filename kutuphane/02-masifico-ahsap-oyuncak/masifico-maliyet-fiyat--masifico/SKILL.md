---
name: masifico-maliyet-fiyat
description: Masifico'nun maliyet ve fiyatlandırma motoru — SKU bazında birim maliyet (malzeme+fire, fason CNC/torna, boya, ambalaj, zayiat, test amortismanı, mesai gölge maliyeti), dört kanalın (kreş toptan, kendi kanal, Trendyol, Etsy) güncel kesinti/komisyon/kargo/vade hesabı, mikro ihracat (ETGB + KDV iadesi) etkisi, başabaş analizi, vergi-şirket yapısı maliyetleri (Bağ-Kur, muhasebe, genç girişimci, esnaf muafiyeti) ve fiyat önerisi. Kullanıcı "kaça mal olur", "ne kadara satayım", "marjım ne", "kâr eder miyim", "toptan fiyat", "Etsy fiyatı", "komisyon", "kargo maliyeti", "başabaş", "zarar mı ederim", "fiyat zammı", "maliyet çıkar", "vergi", "Bağ-Kur", "stopaj", "KDV", "hakediş", "vade", "nakit akışı" dediğinde; yeni SKU'nun fiyatı konuşulduğunda; kanal karşılaştırması yapıldığında; kampanya/indirim planlanırken; veya bir üretim/tasarım kararının para etkisi sorulduğunda bu skill'i kullan. Fiyat/maliyet rakamı geçen her hesapta devreye gir — kullanıcı "hesapla" demese bile. Tüm hesaplar TL (Etsy USD); her sonuç kalem kalem şeffaf, oranlar tarihli, önemli kararda canlı doğrulanır.
---

# Masifico Maliyet & Fiyat Motoru

Her SKU kararının para tarafını tek formatta, kalem kalem şeffaf hesaplayan sistem. İlke: **hiçbir fiyat önerisi maliyet dökümü olmadan verilmez; hiçbir maliyet tek sayı olarak değil aralık + varsayımlarla verilir.** Bu dosyadaki oranlar Ağustos 2026 tabanıdır — bağlayıcı oran her zaman ilgili panel/sözleşmededir; önemli kararda canlı doğrula.

## 1. Birim maliyet modeli

```
BİRİM NAKİT MALİYET =
  Malzeme (kereste + hazır parça + elastik/tutkal)
+ Fason işçilik (CNC + torna)
+ Yüzey sarfı (boya/yağ + zımpara)
+ Ambalaj + etiket
+ Zayiat payı (üretim redleri)
+ Test amortismanı
```

**Kereste:** parça net hacmi (m³) × **fire katsayısı 1,4-1,6** × güncel m³ fiyatı. Kayın fiyatını ezberden alma — teklif iste ya da son alım fişini sor. Nesting fire oranı üretim-mühendisi skill'inden geliyorsa katsayı yerine onu kullan.

**Zayiat:** QC red oranı ilk serilerde ~%5-10; `maliyet × zayiat% / (1−zayiat%)` olarak eklenir.

**Test amortismanı:** ürün ailesinin toplam test faturası ÷ ailenin planlanan toplam üretim adedi. (Ör. tam EN 71 paketi aile başına tipik €300-600; 30.000 TL / 600 adet = 50 TL/adet.) Aile gruplama stratejisi mevzuat skill'inde.

**Mesai gölge maliyeti (ayrı satır, nakit değil):** adet başı el işi dakikası (zımpara+montaj+boya+QC, tipik 20-90 dk) × saat ücreti (piyasa usta saati baz). Nakit maliyete eklenmez ama **fiyat kararında mutlaka gösterilir** — "kâr" sanılan şeyin çoğu ödenmemiş mesaidir.

## 2. Kanal kesintileri (Ağustos 2026 tabanı — panelden doğrula)

| Kanal | Kesintiler | Etkin kesinti |
|---|---|---|
| Kreş toptan | Kesinti yok; toptan = perakendenin ~%50-60'ı. Kamu alımında (doğrudan temin) fatura + CE dosyası | iskonto fiyatta |
| Kendi kanal (IG + site) | Sanal POS + kargo + ambalaj | ~%12-18 |
| Trendyol | Komisyon **%19** (ahşap/eğitici oyuncak, KDV dahil oran, KDV-hariç fiyata; seviye 4-5 satıcıda %14) + **hizmet bedeli 10,99 TL+KDV/koli** (Bugün Kargoda: 6,99) + desi kargo + iade kargo riski + **şahıs şirketine %1 stopaj** | toplam ~%40-50 |
| Etsy | Listing $0,20 + işlem %6,5 + ödeme %6,5+~14 TL + kur çevrimi %2,5 + TR düzenleyici ücreti %1,67 (22.06.2026'dan beri) + ücretlere %20 KDV + (ops. Offsite Ads %12-15) | ~%17-25 |

**Trendyol ayrıntıları:**
- Hesap sırası: (1) KDV dahil fiyattan KDV'yi ayır (oyuncak KDV **%20**), (2) KDV-hariç fiyata komisyon, (3) hizmet bedeli + kargo ekle. Komisyon faturası KDV'si indirilecek girdi KDV'sidir.
- **Kargo baremi fiyat stratejisidir:** sipariş <300 TL ve ≤5 desi → destekli barem (TEX/PTT ~34-66 TL+KDV); sipariş ≥300 TL → tam liste (2 desi ~78 TL, 3-5 desi ~94-143 TL+KDV, kargocuya göre). Premium üründe tam liste varsayılır.
- **Vade:** oyuncakta teslimattan **21 iş günü** sonra hakediş → pratik nakit döngüsü 4-5 hafta. Erken ödeme günlük ~%0,10-0,16 maliyetle mümkün — nakit sıkışığında hesapla, alışkanlık yapma.
- İade kargo satıcıda; komisyon iadede geri gelir.

**Etsy notları:** fiyat USD kurulur, maliyet TL → hesapta günün kuru + **%5 kur tamponu**. Etsy Payments TR'de TRY öder. ABD'ye satışta alıcı tarafında gümrük sürtünmesi (de-minimis yok + TR'ye ek tarife) — ABD fiyatlaması/bloğu mevzuat skill'iyle birlikte kararlaştırılır.

**Mikro ihracat avantajı (ETGB):** limit sevkiyat başına **600 kg / €30.000** (Aralık 2025'te ikiye katlandı). ETGB'li satış = tam ihracat → **%0 KDV'li fatura + girdi KDV iadesi** (~%20 malzeme/ambalaj/kargo KDV'si geri alınır) — Etsy marjına gizli +%3-5 puan; muhasebeciyle iade sürecini kur. Kargo: ShipEntegra/Navlungo tarzı konsolidatörle 1-2 kg paket AB ~$10-20, ABD ~$12-25 (ekonomi).

## 3. Sabit giderler ve şirket yapısı (2026)

- **Bağ-Kur 4B:** oran %35,75 (7566 s.K.), düzenli ödeme indirimiyle %30,75 → asgari matrahtan **~10.157 TL/ay**. Dikkat: kuruluş yılı Bağ-Kur prim desteği 2026 kurulumları için **kaldırıldı**.
- **Genç girişimci** (18-29, ilk mükellefiyet): 3 yıl gelir vergisi istisnası yaşıyor — 2026'da **400.000 TL/yıl** kazanç istisnası.
- Mali müşavir: ~3.500-6.000 TL/ay · e-fatura SaaS: ~180-350 TL/ay (500.000 TL ciroda e-belge zorunlu).
- **Tipik aylık sabit toplamı: ~13.700-17.200 TL** (Bağ-Kur + muhasebe + e-belge; kira/araç hariç). Eski "7-9 bin TL" varsayımı güncel değil — başabaş hesabında bunu kullan.
- **Alternatif yapı — esnaf muafiyeti (GVK 9/10):** evde üretilen el yapımı ürünün yalnız internetten satışında 2026 tavanı **1,9 milyon TL ciro**; vergi yerine %4 (işçi yoksa) banka stopajı. Şirket kurmadan önce/ilk dönemde ciddi seçenek — muhasebeciyle uygunluğu teyit et (atölye/fason kullanımının "evde üretim" şartına etkisi sorulacak soru).

## 4. Fiyatlama kuralları

1. **Hedef brüt marjlar** (mesai gölge maliyeti düşüldükten sonra): kendi kanal ≥%40 · kreş toptan ≥%25-30 · Etsy ≥%40 · Trendyol ≥%20 — altına düşen SKU Trendyol'a çıkmaz.
2. **Fiyat merdiveni:** kreş toptan < Trendyol'da ele geçen olmalı (kanal çatışması olmasın); kendi kanal perakendesi = referans; Trendyol aynı ya da üstü (komisyon gömülür), asla altı.
3. **Psikolojik eşikler:** TR: 890 / 990 / 1.250 / 1.490 / 1.990 · Etsy: $39 / $49 / $59 / $79. Hesap sonucu eşiğin hemen altına yuvarlanır. Trendyol'da 300 TL kargo baremini de gözet (ucuz aksesuar SKU'ları bilinçli olarak <300 TL kurulabilir).
4. **Konum koruması:** premium bant (450-1.500 TL, vitrin 1.750-2.500 TL). Hesap "daha ucuza satabilirsin" dese bile dip fiyat önerme; marj fazlası varsa değer ekle (ambalaj, kişiselleştirme), fiyat düşürme.
5. **Zam disiplini:** girdiler çeyrekte bir güncellenir; birim maliyet %10+ arttıysa fiyat gözden geçirilir. Enflasyon ortamında "geçen ayki fiyat" veri değildir.
6. **Kampanya kuralı:** indirim ancak marj tablosu yeniden hesaplanarak verilir; komisyon+stopaj+kargo sonrası marj %15'in altına inen indirim reddedilir.

## 5. Başabaş analizi

```
Aylık sabitler (2026 tabanı ~13.700-17.200 TL; kullanıcının gerçek kalemleriyle güncelle)
Ortalama katkı payı = ağırlıklı ort. satış fiyatı − birim nakit maliyet − kanal kesintisi
Başabaş adedi = Aylık sabitler ÷ Ortalama katkı payı
```

Sonuç her zaman: "ayda ~X adet satınca sıfırdasın, üstü kâr." Sabit kalemleri bilmiyorsan sor ya da son bilineni "tarihli varsayım" olarak işaretle. Nakit akışı notu: Trendyol vadesi (4-5 hafta) nedeniyle büyüme döneminde "kârlı ama nakitsiz" ay olabilir — sipariş artışında işletme sermayesi ihtiyacını ayrıca yaz.

## 6. Çıktı formatı — SKU Kartı

```
── [SKU adı] · [tarih] ──
Birim nakit maliyet: X TL (malzeme A + fason B + yüzey C + ambalaj D + zayiat E + test F)
Mesai: ~Z dk/adet (gölge maliyet: Y TL)
Önerilen fiyatlar:
  Kendi kanal: ___ TL → net marj %__
  Kreş toptan: ___ TL → net marj %__
  Trendyol:   ___ TL → ele geçen ___ TL (komisyon %19 + hizmet 10,99 + kargo ___ + stopaj %1), marj %__  [çıkar/çıkma]
  Etsy:       $__  → ele geçen ~___ TL (kur ___ − %5 tampon; ETGB KDV iadesi dahil/dahil değil), marj %__
Başabaş etkisi: bu SKU ayda __ adetle sabitlerin %__'sini taşır
Varsayımlar: [kereste fiyatı/tarih, komisyon oranı/tarih, kargo baremi, kur]
```

## 7. Kırmızı çizgiler

- Tek sayı telaffuz etme: her sonuç aralık ya da ±%10 toleransla; varsayım tablosu eksikse hesap eksiktir.
- Kanal kesintisini unutan brüt hesap yasak — "1.000'e satıyorum, maliyet 400, kârım 600" her zaman düzeltilir.
- Mesai gölge maliyeti gizlenmez; ölçek kararlarında asıl kısıt genelde para değil el emeği saatidir.
- KDV karıştırma: fiyatlar KDV dahil konuşulur, marj hesabı KDV ayrıştırılarak yapılır; komisyon KDV'sinin indirilebilirliği hesaba katılır.
- Blog/üçüncü el komisyon oranı ile hesap kapatma: bağlayıcı oran satıcı panelindeki sözleşmedir; çelişki görürsen paneli kontrol ettir.
