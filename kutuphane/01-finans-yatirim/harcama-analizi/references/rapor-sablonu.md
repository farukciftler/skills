# PDF sunum şablonu (`rapor_pdf.py`)

Yatay A4, sayfa başına tek konu, büyük sayı + bir grafik + kısa tablo.
**Her sayfanın altında dipnot zorunlu:** veri kaynağı (hangi belgeler),
dönem, ne dahil ne değil ("kredi kartı yok", "iç transferler hariç").
Rapor sayıları **yalnız** `analiz/ozet.json`'dan gelir; script sayı üretmez.

| # | Sayfa | İçerik | Grafik |
|---|---|---|---|
| 1 | Kapak | başlık, tarih, kapsam (belgeler, dönem), "ölçümdür, tavsiye değildir" | — |
| 2 | Bir bakışta | 6 büyük sayı: portföy toplamı (defter), hane toplamı, 12 ay gelir, 12 ay hane dışına çıkan, tasarruf oranı, belirsiz payı | — |
| 3 | Portföy | dağılım (defterden), look-through maruziyet, kurum kırılımı | halka |
| 4 | Portföy performansı | değer serisi, akış-düzeltilmiş getiri, USD karşılığı; kalibrasyon özeti (baseline ailesi, bant kapsama, BSS) | çizgi |
| 5 | Nakit akışı | ay × gelir / hane dışına çıkan / varlığa net; tasarruf oranı çizgisi | çubuk+çizgi |
| 6 | Harcama kategorileri | 12 ay toplam, pay; `belirsiz` ve `varsayim` ayrı | yatay çubuk |
| 7 | Kategori × ay | ısı tablosu (en büyük 8 kategori) | tablo/ısı |
| 8 | İşyerleri | en büyük 15 (tutar) + en sık 10 (adet) | tablo |
| 9 | Abonelikler ve düzenli ödemeler | işyeri, aylık medyan, ay sayısı, yıllıklandırılmış | tablo |
| 10 | Transferler | iç transfer / aile / kira (varsayım) / kişi; karşı taraf tablosu | çubuk |
| 11 | Altın ve döviz işlemleri | alım/satım sayısı, gram, FIFO gerçekleşen, eşleşmeyen gram; döviz alış/satış | çizgi/tablo |
| 12 | Fon lotları | lot tablosu: fon, alış, adet, maliyet/adet, son NAV, gerçekleşmemiş %, yıllık % | tablo |
| 13 | Bankacılık maliyeti | FAST ücreti, BSMV, stopaj, kambiyo vergisi; aylık | çubuk |
| 14 | Mutabakat | defter ↔ ekstre: eşleşen / defterde var ekstrede yok / ekstrede var defterde yok; hesap bakiyeleri tablosu | tablo |
| 15 | Veri kalitesi | belge listesi, satır sayıları, zincir kontrolü, belirsiz/varsayım oranları, eksik belgeler | tablo |
| 16 | Sorular ve sonraki adımlar | ≤8 madde, hepsi kullanıcıya soru ya da eksik belge; "şunu kes" yok | — |

## Tasarım

- Sistem fontu (`-apple-system`), koyu lacivert başlık, tek vurgu rengi; her
  kategori için sabit renk (`rapor_pdf.py::RENK`).
- Sayılar TR biçimi (`1.234.567 TL`), yüzde bir ondalık.
- Grafikler **gömülü SVG**, dış kaynak yok (Chrome headless çevrimdışı basar).
- Sayfa kırılımı `page-break-after: always`; taşma olmasın diye tablo satırı
  sınırı (15/10/12) script'te sabit.
- PDF üretildikten sonra en az iki sayfa `Read` ile görsel kontrol.

## Chrome

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=<out.pdf> <in.html>
```
Chrome yoksa script HTML'i bırakır ve "PDF üretilemedi, HTML hazır" der;
tarayıcıda Yazdır → PDF ile aynı sonuç alınır.
