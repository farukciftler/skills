---
name: masifico-maliyet-fiyat
description: Masifico'nun maliyet ve fiyatlandırma motoru — SKU bazında birim maliyet hesabı (malzeme+fire, fason CNC/torna, boya, ambalaj, mesai gölge maliyeti, test amortismanı), dört kanalın (kreş toptan, kendi kanal, Trendyol, Etsy) kesinti ve net marj hesabı, başabaş analizi ve fiyat önerisi. Kullanıcı "kaça mal olur", "ne kadara satayım", "marjım ne", "kâr eder miyim", "toptan fiyat", "Etsy fiyatı", "komisyon", "başabaş", "zarar mı ederim", "fiyat zammı", "maliyet çıkar" dediğinde; yeni SKU'nun fiyatı konuşulduğunda; kanal karşılaştırması yapıldığında; veya bir üretim/tasarım kararının para etkisi sorulduğunda bu skill'i kullan. Fiyat/maliyet rakamı geçen her hesapta devreye gir — kullanıcı "hesapla" demese bile. Tüm hesaplar TL (Etsy USD); her sonuç kalem kalem şeffaf gösterilir, oranlar tarihlidir ve önemli kararda canlı doğrulanır.
---

# Masifico Maliyet & Fiyat Motoru

Her SKU kararının para tarafını tek formatta, kalem kalem şeffaf hesaplayan sistem. İlke: **hiçbir fiyat önerisi maliyet dökümü olmadan verilmez; hiçbir maliyet tek sayı olarak değil aralık + varsayımlarla verilir.**

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

**Kereste hesabı:** parça net hacmi (m³) × **fire katsayısı 1,4-1,6** (kesim+kusur firesi) × güncel m³ fiyatı. Kayın m³ fiyatını ezberden alma — teklif iste ya da son alım fişini sor.

**Zayiat:** QC red oranı ilk serilerde ~%5-10; birim maliyete `maliyet × zayiat% / (1-zayiat%)` olarak eklenir.

**Test amortismanı:** ürün ailesinin toplam test faturası ÷ ailenin planlanan toplam üretim adedi. (Ör. 30.000 TL test / 600 adet = 50 TL/adet.)

**Mesai gölge maliyeti (ayrı satır, nakit değil):** adet başı el işi dakikası (zımpara+montaj+boya+QC, tipik 20-90 dk) × saat ücreti (kendi emeğin için piyasa usta saati baz alınır). Nakit maliyete eklenmez ama **fiyat kararında mutlaka gösterilir** — "kâr" sanılan şeyin çoğu ödenmemiş mesaidir.

## 2. Kanal kesintileri (taban oranlar — Ağustos 2026, önemli kararda canlı doğrula)

| Kanal | Kesintiler | Etkin kesinti |
|---|---|---|
| Kreş toptan | Kesinti yok; toptan fiyat = perakendenin ~%50-60'ı | iskonto zaten fiyatta |
| Kendi kanal (IG + site) | Sanal POS ~%2-3 + kargo + ambalaj ekstra | ~%12-15 |
| Trendyol | Oyuncak komisyonu ~%20-22 (KDV hariç satış fiyatı üzerinden) + hizmet bedeli + kargo (desi bazlı) + iade riski | toplam ~%40-50 |
| Etsy | Listing 0,20$ + işlem ~%6,5 + ödeme ~%4-6,5 + (opsiyonel offsite ads %12-15) + döviz çevrimi | ~%17-25 |

**Trendyol hesap sırası:** (1) KDV dahil fiyattan KDV'yi ayır (oyuncakta KDV %20), (2) KDV hariç fiyata kategori komisyonunu uygula, (3) komisyon KDV'si + kargo desisini ekle. Kesin oranı satıcı panelinden doğrula — oranlar kategori/dönem bazlı değişir.

**Etsy notu:** fiyat USD kurulur, maliyet TL'dir → kur marjı lehimizedir ama hesapta günün kuru kullanılır ve %5 kur tamponu düşülür.

## 3. Fiyatlama kuralları

1. **Hedef brüt marjlar** (mesai gölge maliyeti düşüldükten sonra): kendi kanal ≥%40 · kreş toptan ≥%25-30 · Etsy ≥%40 · Trendyol ≥%20, altına düşüyorsa o SKU Trendyol'a çıkmaz.
2. **Fiyat merdiveni tutarlılığı:** kreş toptan < Trendyol'daki net eline geçen olmalı ki kanal çatışması olmasın; kendi kanal perakendesi = referans fiyat, Trendyol aynı ya da üstü (komisyonu fiyata göm), asla altı.
3. **Psikolojik eşikler:** TR: 890 / 990 / 1.250 / 1.490 / 1.990 · Etsy: $39 / $49 / $59 / $79. Hesap sonucu bu eşiklerin hemen altına yuvarlanır.
4. **Konum koruması:** Masifico premium banttadır (600-1.500 TL, vitrin 1.750-2.500 TL). Hesap "daha ucuza satabilirsin" dese bile dip fiyat önerme; marj fazlası varsa fiyatı düşürmek yerine değer ekle (ambalaj, kişiselleştirme).
5. **Zam disiplini:** girdi maliyetleri (kereste, boya, kargo) çeyrekte bir güncellenir; birim maliyet %10+ arttıysa fiyat gözden geçirilir. Enflasyon ortamında "geçen ayki fiyat" veri değildir.

## 4. Başabaş analizi

```
Aylık sabitler = muhasebe + Bağ-Kur + araç/abonelikler + (varsa kira)
Ortalama katkı payı = ağırlıklı ort. satış fiyatı − birim nakit maliyet − kanal kesintisi
Başabaş adedi = Aylık sabitler ÷ Ortalama katkı payı
```

Sonucu her zaman "ayda ~X adet satınca sıfırdasın, üstü kâr" cümlesiyle ver. Sabit kalemlerin güncel tutarlarını bilmiyorsan sor ya da son bilinen değeri "tarihli varsayım" olarak işaretle.

## 5. Çıktı formatı — SKU Kartı

Her hesap şu şablonla biter:

```
── [SKU adı] · [tarih] ──
Birim nakit maliyet: X TL (malzeme A + fason B + yüzey C + ambalaj D + zayiat E + test F)
Mesai: ~Z dk/adet (gölge maliyet: Y TL)
Önerilen fiyatlar:
  Kendi kanal: ___ TL → net marj %__
  Kreş toptan: ___ TL → net marj %__
  Trendyol:   ___ TL → eline geçen ___ TL, marj %__  [çıkar/çıkma]
  Etsy:       $__  → eline geçen ~___ TL, marj %__
Başabaş etkisi: bu SKU ayda __ adetle sabitlerin __%'sini taşır
Varsayımlar: [kereste fiyatı/tarih, komisyon oranı/tarih, kur]
```

## 6. Kırmızı çizgiler

- Tek sayı telaffuz etme: her sonuç aralık ya da "±%10" toleransıyla verilir; varsayım tablosu eksikse hesap eksiktir.
- Kanal kesintisini unutan brüt hesap yasak — "1.000 TL'ye satıyorum, maliyet 400, kârım 600" cümlesi her zaman düzeltilir.
- Mesai gölge maliyeti gizlenmez; ölçek kararlarında (kaç SKU, kaç adet) asıl kısıt genelde para değil el emeği saatidir, bunu görünür tut.
- KDV karıştırma: fiyatlar KDV dahil konuşulur, marj hesabı KDV ayrıştırılarak yapılır.
