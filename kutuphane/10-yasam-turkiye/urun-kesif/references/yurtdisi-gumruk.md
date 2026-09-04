# Yurt Dışı Alışveriş — Gümrük Rejimi ve Toplam Maliyet (2026)

## Mevcut rejim (Şubat 2026 sonrası)

- 7 Ocak 2026 Resmî Gazete kararıyla **30 Euro gümrük muafiyeti tamamen kaldırıldı**; 6 Şubat 2026'dan itibaren tutarı ne olursa olsun **her** yurt dışı bireysel sipariş gümrük vergisine ve gümrük beyanname hizmet bedeline tabidir.
- Vergi, **ürün bedeli + kargo toplamı** üzerinden, menşe bölgeye göre farklı maktu oranlarla hesaplanır (AB menşeli düşük, Çin/ABD gibi ülkeler belirgin yüksek). ÖTV kapsamındaki ürünlerde (parfüm, elektronik cihaz, konsol) ek ÖTV tahsil edilir.
- **Oranlar değişkendir — asla ezberden oran verme.** Her yurt dışı senaryosunda güncel oranları web araması ile teyit et (`yurt dışı alışveriş gümrük vergisi oranı <ay yıl>`), sonra hesabı kalem kalem göster.
- Ek kısıtlar: 30 kg brüt ağırlık sınırı; kimlik başına aylık sipariş sayısı fiilen sınırlı; bazı ürün grupları (replika, peruk, kozmetik türleri vb.) bireysel ithalatta takılabilir/imha edilebilir.

## Platform modelleri

- **Temu (WhaleCo TR):** Türkiye'de kurulu şirket üzerinden **yerel/ticari ithalat** modeline geçti — vergi baştan fiyata dahil, gümrükte takılma riski yok, yerel kargo ile teslim. Bu model geçerliyken Temu fiyatı "vergiler dahil nihai fiyat" olarak karşılaştırılabilir; yine de teslim süresi (7-12 iş günü) ve iade zorluğunu belirt.
- **AliExpress / Amazon (yurt dışı gönderim):** klasik bireysel ithalat — vergi + beyanname bedeli alıcıya sonradan yansır. Toplam maliyeti sen hesaplayıp göster; "kapıda sürpriz" uyarısı yap.
- **Amazon TR üzerinden "yurt dışından gelir" ürünler:** gümrük depozitosu genelde ödeme anında tahsil edilir; ürün sayfasındaki toplam tutarı esas al.

## Yurt dışı ne zaman mantıklı?

Sırayla test et; biri bile sağlanmıyorsa yurt dışını önerme:
1. Ürün Türkiye'de hiç satılmıyor veya stok yok, **veya**
2. Vergiler + kargo + beyanname bedeli dahil toplam maliyet, yurt içi en iyi fiyattan hâlâ anlamlı ölçüde (≥%15-20) ucuz, **veya**
3. Platform yerel-ithalat modeliyle vergisi ödenmiş nihai fiyat sunuyor ve bu fiyat yurt içinden ucuz.

Ek maliyet-dışı faktörleri her zaman not et: teslim süresi, iade pratikte imkânsıza yakın, Türkiye garantisi yok (elektronikte kritik), fiş/fatura yerli servislerde geçmez.

## Hesap şablonu (çıktıda kullan)

```
Ürün bedeli:            €X  (₺...)
Kargo:                  €Y
Vergi matrahı (X+Y):    €Z
Gümrük vergisi (%..):   ₺...
ÖTV (varsa, %..):       ₺...
Beyanname hizmet bedeli:₺...
─────────────────────────────
TOPLAM:                 ₺...   vs. yurt içi en iyi: ₺...
```
