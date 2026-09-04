# Arama Kaynakları, Link Şablonları ve Sorgu Kalıpları

## 1. Neyin çalıştığı, neyin çalışmadığı

Bunu bilmeden zaman kaybedilir. Araç seçimini buna göre yap.

| Kaynak | `web_fetch` fiyat verir mi? | Nasıl kullanılır |
|---|---|---|
| Google Flights | ❌ JS ile yükleniyor | Kullanıcıya **link** olarak ver |
| Skyscanner / Kayak / Momondo | ❌ Bot engeli | Kullanıcıya **link** olarak ver |
| Kiwi.com | ❌ | Link olarak ver |
| Havayolu kampanya sayfaları | ✅ Genelde statik HTML | **Birincil kanıt kaynağı** |
| Havayolu basın bültenleri | ✅ | Kampanya doğrulama |
| Haber siteleri / fırsat blogları | ✅ | Kampanya haberi, ama tarihini kontrol et |
| Fırsat takip hesapları (X, Telegram) | Kısmen | `web_search` üzerinden görünen içerik |
| Havayolu rezervasyon motoru | ❌ | Asla fiyat çekmeye çalışma |

### Kritik teknik kısıt

`web_fetch` yalnızca **konuşmada geçmiş** URL'leri açabilir: kullanıcının verdiği veya daha önce
bir `web_search` sonucunda dönen adresler. Ezberden URL yazıp fetch etmeye çalışmak reddedilir.

Bu yüzden akış her zaman şu sırada olur:

```
web_search ("Pegasus kampanya Ağustos 2026")
   ↓  sonuçlarda kampanya sayfasının URL'i döner
web_fetch (o URL)
   ↓  kampanya detayı: satış penceresi, seyahat penceresi, rotalar
```

Aşağıdaki link şablonları **fetch etmek için değil, kullanıcıya vermek için**. Onlar tarayıcıda
açıp 20 saniyede fiyatı görürler. Skill'in işi doğru sorguyu kurmaktır.

---

## 2. Kullanıcıya verilecek link şablonları

### Google Flights — belirli rota, belirli tarih

```
https://www.google.com/travel/flights?q=flights%20from%20IST%20to%20{HEDEF}%20on%20{YYYY-MM-DD}%20returning%20{YYYY-MM-DD}
```

Doğal dil `q=` parametresi en dayanıklı biçimdir; kodlanmış `tfs=` linkleri kırılıyor.
İki havaalanını birlikte aramak için `IST%2CSAW` yerine iki ayrı link vermek daha güvenilir.

### Google Flights — "her yer" keşif

```
https://www.google.com/travel/explore?q=flights%20from%20Istanbul
```

Kullanıcı burada tarih ve süre filtresini kendi ayarlar. Mod A'da mutlaka bunu da ver: skill'in
kaçırdığı bir destinasyonu kullanıcı burada görebilir.

### Skyscanner — "her yer", esnek tarihli

```
https://www.skyscanner.com.tr/transport/flights/ista/anywhere/{YYMMDD}/{YYMMDD}/
```

- `ista` = İstanbul'un tüm havaalanları (IST + SAW). Tek havaalanı için `ist` veya `saw`.
- Tarih biçimi **yymmdd** (2026-08-13 → `260813`). Bunu karıştırmak boş sonuç verir.
- Ayı komple taramak için tarih yerine `260800` benzeri ay biçimi yerine "esnek tarih" seçeneğini
  kullanıcıya söylemek daha güvenli.

Skyscanner "Her yer" araması, vizesiz-ucuz avında en verimli tek araçtır — ülke kırılımıyla en
düşük fiyatı listeliyor.

### Kiwi.com — LCC kombinasyonlarını yakalar

```
https://www.kiwi.com/en/search/results/istanbul-turkey/anywhere/{YYYY-MM-DD}/{YYYY-MM-DD}
```

Kiwi'nin avantajı ayrı biletleri birleştirmesi; dezavantajı bu kombinasyonlarda gecikme
sorumluluğunun belirsizleşmesi. Kullanıcıya bunu söyle.

### Azair (azair.eu)

Düşük maliyetli taşıyıcılar arasında "kalkış şehri + esnek tarih + max fiyat" kombinasyonu
kurmakta hâlâ en iyisi. URL şablonu vermek yerine kullanıcıya "azair.eu'ya gir, kalkış İstanbul,
'weekend' filtresini seç" demek daha güvenilir — form parametreleri sık değişiyor.

### Havayolu kampanya sayfaları

Ezberden URL yazma. `web_search` ile bul:

- `"Türk Hava Yolları kampanya {ay} {yıl}"`
- `"Pegasus fırsat bileti kampanya {ay} {yıl}"`
- `"AJet kampanya {ay} {yıl}"`
- `"Wizz Air Istanbul deal {ay} {yıl}"`
- `"flynas offers {ay} {yıl}"` (Umre rotaları için)

---

## 3. Sorgu kalıpları

Aramanın kalitesi sorgu kelimelerinde. Şu kalıplar işe yarıyor:

**Kampanya avı:**
- `{havayolu} kampanya {ay} {yıl}`
- `{havayolu} indirim kodu {yıl}`
- `uçak bileti kampanyası {ay} {yıl}`

**Rota bazlı:**
- `İstanbul {şehir} ucuz bilet {ay} {yıl}`
- `IST {kod} cheapest fare {yıl}`

**Hata fiyatı:**
- `error fare Istanbul {yıl}`
- `uçak bileti fiyat hatası {ay} {yıl}`
- `mistake fare IST`

**Sezon/tarih stratejisi:**
- `{şehir} ne zaman gidilir ucuz sezon`
- `{rota} en ucuz ay`

**Vize doğrulama:**
- `Türk vatandaşları {ülke} vize {yıl}`
- `{ülke} visa on arrival Turkish passport {yıl}`

### Sorgu hijyeni

- **Yıl ve ay yaz.** Yılsız sorgu 2023 içeriği getirir ve süresi geçmiş kampanyayı canlı sanırsın.
- **Aynı sorguyu tekrarlama.** Sonuç gelmiyorsa açı değiştir: havayolu adı → rota → "fiyat düştü"
  → forum/topluluk dili.
- **Sorgu kısa olsun**, 2–6 kelime. Uzun cümleler arama motorunda kötü sonuç verir.
- Bir rota hakkında hiçbir kanıt bulamadıysan bunu **söyle**: "Bu rotada güncel kampanya
  bulamadım, aşağıdaki linkten kontrol edebilirsin." Boşluğu tahminle doldurma.

---

## 4. Ne kadar arama yapmalı

| Görev | Tipik arama sayısı |
|---|---|
| Mod C — tek fiyat yargısı | 0–2 |
| Mod B — tek rota, tarih esnekliği dahil | 4–8 |
| Mod A — 8–15 destinasyonluk fırsat taraması | 8–15 |
| Umre — rota + sezon + acente kıyası | 6–12 |

Mod A'da her destinasyon için ayrı arama yapmak verimsiz. Bunun yerine: taşıyıcı bazlı ara
(Pegasus/AJet/Wizz kampanyaları zaten çok rotayı birden kapsar), sonra kampanyada geçen rotaları
havuzla kesiştir. Bu, 15 arama yerine 5 aramayla aynı kapsamı verir.

## 5. Çıktıda linkleri nasıl sunmalı

Ham URL yığını okunmaz. Şu biçimi kullan:

```
**Doğrulama linkleri**
- Üsküp 13–16 Ağu → <link>
- Tiflis 13–16 Ağu → <link>
- Her yer birden (Skyscanner) → <link>
```

En fazla 6 link. Tablodaki her satır için değil, sadece 🔴/🟢 olanlar ve bir tane "her yer" linki.
