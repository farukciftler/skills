# Rapor Şablonu

Bu iskeleti birebir kullan. Sıralama bilinçli: karar vericinin ilk 60 saniyede kararı
verebilmesi, sonra isterse derine inebilmesi için.

Dosya adı: `raporlar/<startup-adi>-<YYYY-AA-GG>.md`

Uzunluk hedefi: 3-6 sayfa. Uzun rapor okunmaz. Detay, ham veri dosyasında durur.

---

```markdown
# <Startup Adı> — Değer ve Potansiyel Raporu
**Tarih:** <GG Ay YYYY> · **Hazırlayan:** Claude · **Kur:** 1 USD = <X> TL (<tarih>)
**Kanıt Skoru:** <n>/<m> kritik metrik doğrulandı

## 1. Tek Paragraf Özet
<Ne yapıyorlar, hangi aşamadalar, bugün ne ediyorlar, ana risk ne. En fazla 5 cümle.
Bir yatırımcı sadece bunu okusa doğru kararı verebilmeli.>

## 2. Net Tahmini Değer

| Katman | Aralık (USD) | Aralık (TL) | Not |
|---|---|---|---|
| Tasfiye / Varlık | | | Kod, marka, domain |
| **Yürüyen İşletme (bugünkü gerçekçi satış fiyatı)** | | | **Ana rakam** |
| Potansiyel (24 ay, %<p> olasılıkla) | | | Ulaşmak için gereken ek sermaye: <X> |

**En olası nokta: <tek sayı>.**
Bu sayıyı taşıyan varsayım: <tek cümle>.
Bu varsayım çökerse değer <alt sayı>'ya iner.

**Gerçekçi alıcı profili:** <stratejik rakip / kurumsal / acquihire / bireysel operatör /
alıcı yok>. İsim önerisi varsa yaz.

## 3. Büyüme Potansiyeli: <n>/10

| Boyut | Ağırlık | Skor | Gerekçe (tek satır) |
|---|---|---|---|
| Pazar | %20 | | |
| Dağıtım | %25 | | |
| Ürün farkı / bariyer | %15 | | |
| Gelir modeli | %15 | | |
| Ekip yürütme | %20 | | |
| Sermaye/pist | %5 | | |

## 4. Bilen Kişiler mi Yapmış? — Ekip Skoru: <n>/10
<Kurucular, geçmişleri, en güçlü ve en zayıf yanları. 2-3 paragraf.
Her iddianın yanında [D]/[İ]/[Y] etiketi.>

## 5. Sert Veriler

| Metrik | Değer | Kaynak | Etiket |
|---|---|---|---|
| Kuruluş tarihi | | | |
| Tüzel unvan | | | |
| İlk yayın tarihi (iOS/Android) | | | |
| Son güncelleme | | | |
| Play indirme | | | |
| Play puan / yorum | | | |
| iOS puan / yorum | | | |
| Tahmini toplam indirme | | | |
| Tahmini MAU | | | |
| Instagram / TikTok takipçi | | | |
| LinkedIn çalışan | | | |
| Aylık gelir | | | |
| Aylık gider (kalem kalem) | | | |
| Aylık net yakım | | | |
| Nakit / pist | | | |

## 6. Rakip Tablosu

| Ürün | İndirme | Puan (yorum) | Monetizasyon | Son güncelleme | Not |
|---|---|---|---|---|---|
| **<Hedef>** | | | | | |
| Rakip 1 | | | | | |
| ... | | | | | |

<Tablonun altına tek paragraf: hedef bu tabloda nerede duruyor.>

## 7. Kullanıcı Ne Diyor
<Review temaları, olumlu/olumsuz dağılımı, birebir 2-4 kısa alıntı (tarih + kaynak ile).
Yorumların zaman dağılımı hakkında bir cümle.>

## 8. Avantajlar
<Madde madde. Her maddede "neden değer üretiyor" bir cümleyle. Abartma; 3 gerçek avantaj,
8 zoraki avantajdan iyidir.>

## 9. Dezavantajlar ve Riskler
<Madde madde, **etkisine göre sıralı** (en ölümcül üstte). Her maddede:
risk · kanıt · değere etkisi · giderilebilir mi, ne kadara/ne kadar sürede.>

## 10. Senaryolar

| Senaryo | Varsayım | Değer | Olasılık |
|---|---|---|---|
| Kötü | | | |
| Baz | | | |
| İyi | | | |
| **Beklenen değer** | | **<Σ>** | %100 |

## 11. Karar ve Tavsiye
<Kullanıcının tarafına göre net tavsiye:>
- **Satıcıysa:** Şu fiyatı iste, şu tabana kadar in, satıştan önce şu 3 şeyi yap
  (her biri fiyata şu kadar ekler), şu alıcılarla konuş, şunu asla söyleme/sakla.
- **Alıcıysa:** Şu fiyata kadar öde, şunları due diligence'ta iste, şu maddeleri
  sözleşmeye koy (earn-out, kurucu kalma, IP devri), şu koşulda çekil.
- **Yatırımcıysa:** Gir/girme, hangi değerlemede, hangi milestone'a bağlı.

## 12. Bunu Netleştirecek 5 Soru
<Aralığı daraltacak, cevabı olmayan en kritik 5 soru. Her sorunun yanında:
"cevap X ise değer yukarı/aşağı şu kadar oynar".>

---
### Ek: Kaynaklar
<Kullanılan tüm URL'ler, erişim tarihiyle.>
### Ek: Yöntem notu
<Hangi değerleme yöntemleri kullanıldı, hangi çarpanlar, neden.>
```

## Yazım notları

- **Tablo kullan, paragraf değil** — sayısal her şey tabloya girer.
- Her sayının yanında etiket (`[D]/[T]/[İ]/[Y]`) olsun; okuyucu neye güveneceğini bilsin.
- Kötü haberi yumuşatma ama saygılı ol: "ürün başarısız" değil, "mevcut indirme ve yorum
  hacmi, ürünün henüz ürün-pazar uyumuna ulaşmadığını gösteriyor".
- Bir şeyi bilmiyorsan yaz. Rapordaki `[Y]` sayısı, raporun zayıflığı değil dürüstlüğüdür —
  ve satıcıya "bunları belgelersen fiyatın artar" demenin yoludur.
- Sonuç cümlesi tek ve net olsun. "Duruma göre değişir" ile biten rapor işe yaramaz.
