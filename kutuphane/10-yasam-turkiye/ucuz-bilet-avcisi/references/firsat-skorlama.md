# Fırsat Skorlama, Gerçek Maliyet ve Hata Fiyatı Protokolü

## 1. Skor matematiği

```
skor = bulunan_fiyat / referans_bant_tabanı
```

Referans bant tabanı = `vizesiz-destinasyonlar.md` tablosundaki bandın **alt** ucu (üst ucu değil).
Alt ucu kullanmanın sebebi: üst uçla bölmek her şeyi fırsat gibi gösterir, skill güvenilirliğini
kaybeder.

| Skor | Etiket | Davranış |
|---|---|---|
| < 0,40 | 🔴 Hata fiyatı olabilir | §4 protokolünü uygula, aciliyeti belirt |
| 0,40–0,60 | 🟢 Gerçek fırsat | Öne çıkar, gerekçesini yaz |
| 0,60–0,85 | 🟡 İyi | Listele ama acele önerme |
| > 0,85 | ⚪ Normal | **Listeden çıkar** |

### Sezon düzeltmesi

Bant, ortalama sezon içindir. Zirve sezonda skoru olduğu gibi bırakmak yanlış negatif üretir:

| Dönem | Çarpan (banda uygula) |
|---|---|
| Okul tatilleri, dini bayramlar, 15 Tem–20 Ağu | × 1,5 |
| Yılbaşı haftası, sömestr | × 1,4 |
| Ramazan (Umre rotaları), Hac dönemi | × 1,8–2,5 |
| Kasım, Şubat, Mart başı (ölü sezon) | × 0,8 |

Yani 10 Ağustos'ta Üsküp için taban 90 × 1,5 = 135 EUR olur; 120 EUR'a bulunan bilet 🟢 fırsattır,
düzeltme yapılmasa ⚪ görünürdü.

### Km başına sağlama testi

Bant güvenilmez göründüğünde ikinci bir kontrol:

| Mesafe | Tek yön EUR/km — normal | Fırsat sınırı |
|---|---|---|
| < 1.500 km | 0,08–0,15 | < 0,05 |
| 1.500–4.000 km | 0,05–0,10 | < 0,035 |
| > 4.000 km | 0,03–0,07 | < 0,022 |

İki test çelişirse muhafazakâr olanı (daha yüksek skor) al ve belirsizliği söyle.

---

## 2. Gerçek maliyet şablonu

Bilet fiyatını çıplak karşılaştırmak, ucuz taşıyıcıları haksız yere kazandırır. Her adayı bu
kalemlerle topla ve **karşılaştırmayı toplam üzerinden** yap.

```
Bilet (gidiş-dönüş)                        ....... TL
+ Bagaj (kaç kg, kaç yön, ne kadar)        ....... TL
+ Koltuk/check-in (bazı LCC'lerde zorunlu) ....... TL
+ Havaalanı ulaşımı (IST vs SAW farkı)     ....... TL
+ Vize / kapıda vize ücreti                ....... TL
+ Aktarma gecesi konaklama (varsa)         ....... TL
+ Varış transferi (uzak havaalanı ise)     ....... TL
─────────────────────────────────────────────────────
= GERÇEK MALİYET
```

Sık yakalanan ters çevirmeler:
- **Bagajlı yolcu için** Pegasus 1.800 + 2×600 bagaj = 3.000 iken THY 3.200'ün içinde bagaj var
  → THY kazanır. Bunu hesaplamadan LCC önermek hatalı.
- **SAW ulaşımı**, Ortaköy/Beşiktaş tarafından IST'e göre belirgin şekilde daha uzun ve pahalıdır;
  ~250–400 TL fark + zaman. Fiyat farkı bunun altındaysa IST tercih edilir.
- **Bergamo/Stansted tipi ikincil havaalanları**: bilet 40 EUR ucuz, şehir transferi 30 EUR ×2.
- **Gece 02:00 varış**: taksi zorunluluğu + otelde bir gecenin boşa gitmesi.

---

## 3. Perşembe–Pazar saat mekaniği

Aynı gün içinde saat seçimi, gün seçiminden daha çok para kazandırır. Rota sınıfına göre:

**Bölgesel/iş rotaları (Balkan başkentleri, Bakü, Tiflis, Körfez):**
- En pahalı dilimler: Perşembe 17:00–21:00 (iş çıkışı), Pazar 18:00–23:00 (dönüş zirvesi).
- En ucuz dilimler: Perşembe 06:00–08:00 ve 22:00 sonrası, Pazar 10:00–14:00.
- **Perşembe 23:xx kalkış** çift kazanç: en ucuz dilim + Cuma gününün tamamı elinde kalır.

**Tatil rotaları (Batum yaz, Şarm, Dubai kış):**
- Cumartesi/Pazar kalkışlar pahalı (paket tur döngüsü), hafta içi ucuz.
- Perşembe kalkış burada zaten avantajlı; asıl mesele dönüş gününü Pazar'dan Pazartesi sabaha
  kaydırmak.

**Aktarma payı:** aynı bilette (tek PNR) 1,5 saat kabul edilebilir; ayrı biletlerde asla 4
saatin altına inme, çünkü ilk uçuş gecikirse ikincisinin sorumluluğu sende.

## 4. Hata fiyatı (error fare) protokolü

Skor < 0,40 veya fiyat mantık dışıysa muhtemelen sistem/kur/yayın hatası. Yapılacaklar sırayla:

1. **Hızlı al.** Bu fiyatlar saatler içinde kapanır.
2. **Bileti doğrudan havayolundan al** mümkünse — acente üzerinden alınan hata fiyatları daha
   kolay iptal edilir.
3. **Havayoluyla iletişime geçme.** "Bu fiyat doğru mu?" diye sormak, biletin iptal edilmesinin
   en hızlı yoludur.
4. **72 saat bekle.** Bilet gerçekten düzenlendi mi (ticketed / PNR'da e-bilet numarası var mı)
   kontrol et. Bu süre geçmeden otel, tur, iç hat bileti gibi **iptal edilemez** hiçbir şey alma.
5. **Yayma.** Sosyal medyada paylaşılan hata fiyatları çok daha hızlı kapatılır ve iptal edilir.
6. **İptal riskini kabul et.** Havayolu iptal ederse genelde para geri döner ama seyahat planı
   çöker. Yıllık izin ayarlamayı bekletmek mantıklı.

**Türkiye özel notu:** Uçak bileti, mesafeli sözleşmelerde cayma hakkı istisnaları arasında.
Yani "24 saat içinde iade" otomatik bir hak değil; tamamen bilet tarifesine ve havayolunun
kendi politikasına bağlı. Kullanıcıya "nasıl olsa iade ederim" güvencesi verme.

## 5. Kampanya doğrulama kontrol listesi

Bir kampanya bulduğunda şu beşini kontrol et, eksik olanı "belirtilmemiş" diye yaz:

1. **Satış penceresi** — hangi tarihe kadar bilet alınabilir?
2. **Seyahat penceresi** — hangi tarihler arasında uçulabilir? (Genelde asıl kısıt bu.)
3. **Kapsanan rotalar** — "yurt dışı" ifadesi genelde sadece belirli rotaları kapsar.
4. **Koltuk kotası** — "kontenjanlı" ibaresi varsa ilan edilen fiyatı bulmak zor olabilir.
5. **Dahil olanlar** — bagaj, değişiklik hakkı. Kampanya fiyatları genelde en kısıtlı tarifedir.

Süresi geçmiş kampanyayı fırsat olarak sunmak bu skill'in en sık ve en can sıkıcı hatasıdır.
Bugünün tarihiyle karşılaştırmadan yazma.

## 6. Ne zaman "bekle" demeli

Fiyat düşer diye beklemeyi önermek genelde kötü tavsiyedir, ama şu üç durumda geçerli:

- Kalkışa **8 haftadan fazla** var ve skor > 0,85 → bant içine inmesi olası, bekle.
- Rotada **yeni taşıyıcı** giriyor (haberi varsa) → giriş fiyatları agresif olur.
- Sezon çarpanı yüksek bir dönemdesin ve tarih esnek → tarih kaydırmayı bekle.

Kalkışa 3 haftadan az kaldıysa **asla bekleme önerme**; bu aralıkta fiyatlar tek yön yukarı gider.
