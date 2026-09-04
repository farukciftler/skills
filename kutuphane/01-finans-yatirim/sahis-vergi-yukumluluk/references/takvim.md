# Yükümlülük Takvimi — iskelet

> Beyan ve ödeme süreleri sık sık sirkülerle **uzatılır**. Bu dosya hatırlatma iskeletidir;
> her kullanımda GİB vergi takvimi canlı doğrulanır. Teyit: Ağustos 2026.

## Yıllık ritim (gerçek usulde ticari kazanç)

| Dönem | Yükümlülük | Not |
|---|---|---|
| Her ayın belirli günü | KDV beyannamesi ve ödemesi | Aylık dönem; bazı mükelleflerde üç aylık |
| Her ayın belirli günü | Muhtasar ve Prim Hizmet Beyannamesi | İşçi/kira stopajı varsa |
| 1. dönem (Oca-Mar) | Geçici vergi beyanı | Beyan/ödeme takip eden ikinci ayda |
| 2. dönem (Nis-Haz) | Geçici vergi beyanı | |
| 3. dönem (Tem-Eyl) | Geçici vergi beyanı | |
| 4. dönem (Eki-Ara) | **Gelir vergisi mükelleflerinde dördüncü dönem geçici vergi kaldırılmıştır** (7338 s.K.) — doğrula | |
| Mart | Yıllık Gelir Vergisi Beyannamesi | Ödeme genelde iki taksit (Mart–Temmuz) |
| Yıl başı | Defter tasdiki / e-defter beratları | Defter türüne göre |
| Aylık | Bağ-Kur (4/b) primi | |

## 20/B istisnasından yararlanan taraf

| Ne zaman | Ne |
|---|---|
| Faaliyete başlarken | Vergi dairesinden **İstisna Belgesi**; bankaya ibraz |
| Her tahsilatta | Bankanın %15 tevkifatı — banka yapar, ayrıca beyan yok |
| Sürekli | Hasılatın **yalnızca** o hesaptan geçtiğinin kontrolü |
| Çeyreklik | Yıllık tavana ne kadar kalındığının hesabı |
| Yıl sonu | Tavan aşıldıysa → yıllık beyanname zorunluluğu doğar |

**Ayrıca ticari mükellefiyet varsa:** üstteki ticari kazanç ritmi aynen geçerlidir; 20/B tarafı bu ritmi ortadan kaldırmaz.

## Yıl başı kontrol listesi (her Ocak)

- [ ] Yeniden değerleme oranı açıklandı mı? Yeni hadler ne oldu?
  - 20/B tavanı (GVK 103 dördüncü dilim)
  - Fatura düzenleme haddi
  - e-Arşiv / e-Fatura eşikleri ve geçiş dönemi bitiş tarihleri
  - Defter tutma hadleri (işletme ↔ bilanço geçişi)
  - Bağ-Kur prim tabanı
  - Özel usulsüzlük ceza tutarları, uzlaşma sınırı
- [ ] Geçen yıl cirosu, bu yıl için yeni bir zorunluluk (e-fatura, bilanço esası) doğurdu mu?
- [ ] Yeni bir satış kanalı (pazaryeri, yurt dışı) açıldıysa vergisel etkisi işlendi mi?
- [ ] Destek/teşviklerin (genç girişimci vb.) kapsamı değişti mi?

## Hatırlatıcı kurma
Kullanıcı isterse `reminder_create_v0` ile: her çeyreğin geçici vergi tarihi, Mart beyannamesi, Ocak had kontrolü, ve tavanın %80'ine ulaşıldığında yapılacak ara kontrol. Kendiliğinden kurma — öner.
