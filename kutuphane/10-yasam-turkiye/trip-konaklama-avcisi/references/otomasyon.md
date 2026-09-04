# Otomasyon (Seviye 3)

Yalnızca kullanıcı **izleme/tarama isteyince** oku. Tek seferlik bir arama için bu dosyaya
ihtiyacın yok.

## 1. Ne zaman otomasyon, ne zaman tek arama

| İstek | Yol |
|---|---|
| "Şu tarihlerde şu şehirde otel bul" | Tek arama, bu dosyaya gerek yok |
| "Hangi hafta daha ucuz?" | Tarih ızgarası taraması (§2) |
| "Fiyat düşerse haber ver" | İzleme (§3) |
| "İptal tarihi geçmeden hatırlat" | Politika takvimi (§4) |

## 2. Tarih ızgarası taraması

Aynı şehir + aynı filtreler, kayan tarih pencereleri. Her pencere bir sayfa yüklemesi.

```
for (checkin, checkout) in pencereler:
    url = trip_url.py ... --checkin X --checkout Y
    aç, bekle, liste_oku.js çalıştır
    en ucuz 3 sonucu kaydet
    1,5-3 sn bekle
```

Hacim disiplini: 8 haftalık bir tarama = 8 sayfa yüklemesi, kabul edilebilir.
Aynı anda 5 şehir × 8 hafta = 40 yükleme, **tek oturumda yapma** (bkz. `tarayici-okuma.md` §6).

Sonucu her zaman **toplam fiyat** üzerinden karşılaştır — farklı pencereler farklı gece sayısı
demek olabilir. Gecelik fiyat karşılaştırması 3 gece ile 5 geceyi aynı kefeye koyar.

## 3. Fiyat izleme

Basit ve yeterli bir depo: JSONL. Her satır bir gözlem.

```json
{"ts":"2026-08-25T14:10:00+03:00","hotelId":"730508","ad":"Gresham Hotel Bloomsbury",
 "checkin":"2026-10-01","checkout":"2026-10-06","curr":"TRY","gecelik":5788,"toplam":34725,
 "oda":"İki Yataklı En-Suite Oda","iptalSonTarih":"2026-09-30T16:00","url":"..."}
```

Kurallar:
- **Her gözlemi yaz**, sadece değişenleri değil. Değişmediğini bilmek de veridir.
- Zaman damgasını saat dilimiyle yaz.
- Para birimini her satırda taşı — `curr` değişirse geçmiş bozulmasın.
- Aynı otelin aynı tarih penceresi için gözlem sayısı 5'i geçtiğinde anlamlı bir taban
  oluşur; **o zamana kadar "düştü/çıktı" iddiası üretme**, sadece kaydet.

Bildirim eşiği: **%10 ve üzeri** düşüş. Daha küçük dalgalanmalar gürültüdür ve kullanıcıyı
bildirim körü yapar.

## 4. Politika takvimi

Rezervasyon yapılmışsa asıl değerli hatırlatma fiyat değil, **ücretsiz iptal son tarihidir.**

- Son tarihten **3 gün önce** hatırlat: "iptal penceresi 3 gün sonra kapanıyor, planın hâlâ
  geçerli mi?"
- Son tarihten **1 gün önce** tekrar hatırlat.
- Bu tarih otelin yerel saatinde; hatırlatmayı kullanıcının saat dilimine çevirerek yaz.

Bu, aynı otelin fiyatını yeniden okuyup "şimdi daha ucuz, iptal edip yeniden al" önerisi
üretmek için de doğru andır — ama öneriyi yeni fiyat `[OKUNDU]` etiketiyle doğrulanmadan verme.

## 5. Cron

```bash
# günde bir kez, sabah 09:00
0 9 * * * cd /path/to/proje && /usr/bin/python3 izle.py >> izle.log 2>&1
```

Sessiz bozulma korumaları (bunlar olmadan cron aylarca boş veri toplar):
- Çalışma sonunda **kaç gözlem yazıldığını** logla. 0 ise hata olarak işaretle.
- Üst üste 2 kez 0 gözlem → kullanıcıya "izleme bozuldu" bildirimi gönder, sessizce devam etme.
- Fiyat alanı `null` gelen gözlemi **yazma**, ayrı bir hata sayacına yaz.
- Ayda bir `filtre_hasadi.js` çalıştırıp filtre kodlarının hâlâ geçerli olduğunu doğrula.

## 6. API yolu

Trip.com'un açık, belgeli bir konaklama arama API'si yok; buradaki her şey sitenin kendi iç
kodlamasına dayanıyor ve haber verilmeden değişebilir. Ciddi hacim gerekiyorsa doğru cevap
daha fazla kazımak değil, **bir affiliate/partner erişimi** almaktır. Kullanıcı yüzlerce
sorgulu bir sistem tarif ediyorsa bunu bir kez söyle, sonra istediği şeyi yapmaya devam et.
