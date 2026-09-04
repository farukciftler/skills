# Veri Kaynakları ve Fiyat Toplama

Snapshot almadan önce oku.

## 0. Tek kural

> **Arama motoru özetinden sayı okuma.**

Bu deponun ilk beş gününde kaydedilen makro hataların **tamamı** bundan geldi:

| Vaka | Ne oldu | Neden |
|---|---|---|
| **K11** | `us10y` 4,23 kaydedildi, gerçek 4,65 (40bp) | özet başka bir enstrümanın getirisini verdi |
| **K18** | Nasdaq 4 gün boyunca 31.07 kapanışıydı, "03.08" diye etiketliydi | haber metni sayıyı **tarihsiz** taşıdı |
| **K19** | BIST 03.08 kaydı 14.085, gerçek 13.410,54 (675 puan) | gün içi bozuk kotasyon ya da başka endeks |
| 05.08 | "05.08 açılışı" diye gelen 13.399,44 aslında **04.08 açılışıydı** | arama motoru iki günün haberini karıştırdı |
| 05.08 | `xauusd` 4.127,04 kaydedildi, gerçek ~4.222 | üç kaynak üç farklı sayı verdi, hepsi tarihsizdi |

Ortak nokta: **haber metni bir sayıyı hangi güne ait olduğunu söylemeden taşır.**
Bir sayıyı tarihinden ayıran her kaynak, er ya da geç bayat veriyi güncel gibi
gösterir. Çözüm daha dikkatli okumak değil, **tarihi verinin kendisinden gelen
kaynak kullanmak.**

```bash
python3 scripts/fetch_market.py --date $(date +%F) --gram-altin <piyasa fiyati>
python3 scripts/fetch_market.py --json    # market_state blogu olarak
```

Bu script her değeri `<değişken>_asof` damgasıyla getirir, bağımsız iki kaynağı
çapraz kontrol eder ve bulamadığını `null` bırakır. **Web search yalnızca
TEFAS fon fiyatları, banka bakiyesi ve gündem taraması için kullanılır.**

### Sağlayıcı sağlığı

```bash
python3 scripts/fetch_market.py --health
```

Her sağlayıcıyı tek tek dener, `✅/❌` listeler ve kritik bir alan hiçbir
sağlayıcıdan gelmiyorsa **çıkış kodu 1** verir. `gunluk.sh` her sabah çalıştırır.

En tehlikeli bozulma "erişilemedi" değil, **kaynağın yaşayıp alan adlarını
değiştirmesidir** — o zaman alan sessizce `null` kalır. Script bunu ayrı bir
`SEMA DEGISTI` etiketiyle raporlar, çünkü teşhisi ve çözümü farklıdır:

| Etiket | Ne demek | Ne yapılır |
|---|---|---|
| `erisilemedi` | ağ/timeout | tekrar dene; kalıcıysa yedek sağlayıcı |
| `SEMA DEGISTI` | kaynak yaşıyor, alan adları kaydı | `WebFetch` ile aç, ayıklayıcıyı güncelle |
| `bot duvari` | WAF/UA reddi | önce UA değiştir (FRED ↔ Yahoo zıt), sonra yedek ara |
| `makul olmayan deger` | sıfır/negatif döndü | kaynağı doğrula, körü körüne kaydetme |

Düzeltme her zaman `data/reviews/YYYY-MM.md`'ye yazılır: hangi sağlayıcı, ne
zaman, neden bozuldu, yerine ne kondu.

---

## 1. Doğrulanmış uç noktalar

Hepsi 05.08.2026'da bu makineden test edildi; anahtar/kayıt gerektirmiyor.

| Alan | Kaynak | Uç nokta | Gecikme |
|---|---|---|---|
| `us10y` | FRED `DGS10` | `fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10` | T-1/T-2 |
| `us10y_real` | FRED `DFII10` | aynı, `id=DFII10` | T-1/T-2 |
| `nasdaq` | Yahoo `^IXIC` | `query1.finance.yahoo.com/v8/finance/chart/^IXIC` | canlı |
| `nasdaq_fred` | FRED `NASDAQCOM` | çapraz kontrol | T-1 |
| `sp500` | Yahoo `^GSPC` + FRED `SP500` | | canlı / T-1 |
| `bist100` | Yahoo `XU100.IS` | | canlı |
| `dxy` | Yahoo `DX-Y.NYB` | ICE dolar endeksi | canlı |
| `brent` | Yahoo `BZ=F` | Brent vadeli | canlı |
| `xauusd_futures` | Yahoo `GC=F` | COMEX vadeli — **spot değil** | canlı |
| `xauusd_lbma_pm` | LBMA | `prices.lbma.org.uk/json/gold_pm.json` | T-1 |
| `usdtry_spot` | Yahoo `TRY=X` | serbest piyasa | canlı |
| `usdtry_tcmb_*` | TCMB | `tcmb.gov.tr/kurlar/today.xml` | **T-1 sabahları** |
| `gram_altin_alis` | truncgil | `finans.truncgil.com/today.json` | canlı, **saniye damgalı** |
| `usdtry_serbest_*` | truncgil | aynı | canlı |

### Denenip elenenler — tekrar denemeden önce oku

| Kaynak | Sonuç |
|---|---|
| **TEFAS API** (`api/DB/BindHistoryInfo`) | `ERR-006 Method not found or disabled` — çerezli/çerezsiz, form/JSON, dört ayrı yol: hepsi 404. **Kapalı.** |
| **stooq.com** CSV | JavaScript proof-of-work duvarı, `curl` ile alınamıyor |
| **Fintables** fon sayfaları | 403 |
| **KAP** fon fiyat API'si | Next.js hata sayfası döndürüyor |
| Yahoo `XAUUSD=X` / `XAU=X` | `Not Found` — Yahoo'da spot altın sembolü yok, sadece vadeli (`GC=F`) |
| FRED `DEXTUUS` (USD/TRY) | bot duvarına takıldı; TCMB zaten daha iyi kaynak |

### User-Agent tuzağı

**Kaynaklar zıt UA istiyor.** Ölçüldü:

| Kaynak | `Mozilla/5.0` | `curl/8.4.0` |
|---|---|---|
| FRED | 18 sn timeout | 0,2 sn, 268 KB |
| Yahoo | çalışıyor | güvenilmez |

İkisini aynı UA ile çağırmak, kaynakların yarısının **sessizce `null` dönmesi**
demektir — ve `null` dönen bir alan, yanlış dolan bir alandan daha az göze
batar. `fetch_market.py` bunu kaynak başına ayarlar.

---

## 2. Script'in kapsamadıkları

### Gram altın TL — ÇÖZÜLDÜ (05.08)

`finans.truncgil.com/today.json` gram altın alış/satış **ve** USD/TRY veriyor,
üstelik `Update_Date` ile **saniye hassasiyetinde zaman damgalı** — bu deponun
tüm hata sınıfının panzehiri, çünkü sayıyı saatinden ayırmıyor.

`fetch_market.py` bunu otomatik çekiyor; `--gram-altin` bayrağı artık yalnızca
elle bir kotasyonu doğrulamak istediğinde gerekiyor.

Elle toplamak gerekirse (sağlayıcı bozulursa) eski kurallar geçerli: iki
bağımsız TR kaynağı (Bigpara, doviz.com), hep **ALIŞ** fiyatı, **kotasyon saati
yazılır** — gram altın gün içinde %1 oynayabiliyor.

**Baz hakkında — 05.08'de İKİ KEZ yanlış yapıldı, ders bu.**

Eski talimat `XAUUSD × USDTRY / 31,1035` ile karşılaştırıp %1'den fazla sapmayı
"yerel prim" saymaktı.

1. **Birinci hata:** sabah, arama motorundan gelen `XAUUSD = 4.127,04` ile
   "+%1,27 yerel prim açıldı" yazıldı. Değerin hangi ana ait olduğu bilinmiyordu.
2. **İkinci hata (düzeltmenin kendisi):** Yahoo `GC=F` ile yeniden hesaplanıp
   "baz aslında −%1,15, normal" denildi ve **[−%1,6; −%0,1] bandı** kural olarak
   yazıldı. `GC=F` **vadeli**, spot değil.

**`GC=F` ≠ spot.** Vadeli, taşıma maliyeti kadar spot'un üstünde işlem görür ve
bu fark sabit değil:

| Gün | Spot (investing) | `GC=F` | Contango |
|---|---|---|---|
| 04.08 kapanış | 4.077,48 | 4.095,40 | +%0,44 |
| 05.08 gün içi | 4.165,71 | 4.222,20 | +%1,36 |

Gerçek spot ile bakınca 05.08 bazı **+%0,33** — yani ne "+%1,27 prim" ne de
"−%1,15 normal". İkisi de referans hatasıydı.

**Kural — mutlak bant yok, oran kararlılığı var.** Elimizde aynı ana ait,
ücretsiz, makine-okunur bir spot altın kaynağı **yok** (goldprice.org 403,
investing 403, exchangerate.host anahtar istiyor, Yahoo'da spot sembolü yok).
Bu yüzden `fetch_market.py` mutlak seviyeyi yorumlamaz; `GC=F`'yi **sabit ofsetli
bir referans** olarak kullanıp **oranın gün gün ne kadar kaydığına** bakar.
Ofset iki tarafta da bulunduğu için farkta sadeleşir.

```bash
python3 scripts/fetch_market.py --gram-altin 6384.05 --root data
#   gram_oran_pct          -1.18
#   gram_oran_onceki_pct   -0.83
#   gram_oran_kaymasi_pp   -0.34    <- alarm esigi ±0,6 puan
```

**Mutlak seviyeyi asla "prim" diye yorumlama.** Yalnızca kayma anlamlıdır.
Gerçekten spot lazımsa `WebFetch` ile
`investing.com/currencies/xau-usd` oku (Claude tarafında çalışıyor, `curl` 403
alıyor) ve **kotasyon saatini** kaydet — gram altın gün içinde %1 oynayabiliyor,
farklı saatlerdeki iki sayı karşılaştırılamaz.

### TEFAS fonları (KTJ, KIK, KUT, ZPE) — kazınamaz, `WebFetch` şart

İki ayrı engel var ve ikisi de aşılamadı:
1. **API kapalı**: `api/DB/BindHistoryInfo` → `ERR-006 Method not found or
   disabled`. Dört yol denendi (form/JSON gövde, çerezli/çerezsiz, `Referer` +
   `Origin` başlıklarıyla).
2. **Sayfa bir F5 ASM WAF'ı arkasında**: tam Chrome başlık seti + `Sec-Fetch-*`
   ile bile `Request Rejected ... support ID` dönüyor. Bu bir JS render sorunu
   değil, isteğin sunucuya hiç ulaşmaması.

`WebFetch` farklı bir ağ yolundan gittiği için çalışıyor — **tek yol bu**:

```
https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod=KTJ
```
Sorulacak: *"Son Fiyat (TL) ve Günlük Getiri (%) kaç?"*

**Tuzaklar:**
- **T+1 gecikmeli**: bugün gördüğün fiyat **önceki iş gününün** birim pay değeri.
- Sadece **iş günleri**. Hafta sonu/tatil `null` bırak, motor önceki değeri taşır.
- **Üçüncü taraf siteler bayat veri gösteriyor.** 05.08'de Bloomberg HT, KTJ
  için 2,48937 (dünkü değer) gösterirken TEFAS 2,597349 veriyordu — **%4,3
  fark.** Çelişki varsa **daima TEFAS**.
- **Her fonun günlük getirisini önceki snapshot fiyatıyla doğrula:**
  `yeni / eski − 1` sitenin verdiği "Günlük Getiri" ile tutmalı. Tutmuyorsa ya
  bir gün atlanmış ya yanlış fon okunmuştur.

**Mekanik avantaj uyarısı.** Fonun 1 günlük "tahmini", büyük ölçüde
**gerçekleşmiş** bir hareketi yazmaktır (ilgili endeksin dünkü kapanışı
biliniyor). Bunu tahmin diye sunma; `rationale`'a `MEKANIK:` diye başla ve
kalibrasyon skorunu bununla şişirme.

**Değerleme gecikmesi henüz çözülmedi (05.08 itibarıyla açık).** KTJ'nin
yabancı bacağının hangi ABD seansından değerlendiği belirsiz: geçiş oranı iki
gözlemde 0,65 ve 2,04 çıktı. Yurt içi fonlar (ZPE) **aynı gün** değerleniyor —
BIST 18:00'de kapanıp NAV sonra hesaplandığı için bu kesin.

### `accrual` hesaplar — sadece banka ekranı

Tahmin edilmez, projekte edilir. Gerçek bakiye eline geçince
`--prices '{"vakif_gunluk": <bakiye>}'` ile ez; projeksiyon her zaman gerçeğe
yenilir. **Para çekme/yatırma ayrıca `--flows` ile kaydedilir** — bakiyeyi ezmek
akışı kaydetmez, ikisi ayrı şeydir.

---

## 3. USD/TRY: hangi kur, ne zaman

Üç ayrı sayı var ve karıştırılmaları kolay:

| Kaynak | Ne | Ne zaman |
|---|---|---|
| `usdtry_spot` (Yahoo `TRY=X`) | serbest piyasa, canlı | 7/24 |
| `usdtry_tcmb_mid` | TCMB resmî gösterge ortası | **~15:30'da yayınlanır** |
| `usdtry_tcmb_alis/satis` | resmî döviz alış/satış | aynı |

**Sabah snapshot'ında TCMB dosyası daima bir önceki iş gününü gösterir.**
`today.xml` adına rağmen. Script bunu `usdtry_tcmb_asof` ile açıkça söyler.

**Bu tam olarak 05.08'de olan şeydi:** "serbest piyasa alış 47,4694 / satış
47,5550" diye kaydedilen değerler aslında TCMB'nin **04.08 bülteniydi** —
kaynak öyle etiketlememişti.

**Sabit konvansiyon:** snapshot'a `usdtry_spot` (Yahoo, canlı) girilir; TCMB
değerleri `market_state`'e ayrıca kaydedilir. Sebep: snapshot saati sabah,
resmî kur öğleden sonra. Resmî kuru kullanmak her güne bir gün gecikme
katardı — `doviz_katilim` `spot` sınıfında olduğu için bu doğrudan fiyat hatası
demektir.

---

## 4. Tatil ve boşluk yönetimi

- **Hafta sonu**: `spot`/`crypto` snapshot al; `fund_tefas`/`equity` `null`.
- **Resmî tatil**: aynısı. Tahmin üretmeye devam et, motor hedef tarihi
  varlığın **fiyatlandığı ilk güne** kaydırır (`next_open_day`, `crypto` hariç).
- **Kapalı güne tahmin hedeflenmez.** Hafta sonu `spot` snapshot'ı alınır ama o
  gün **yeni fiyat yoktur** — motor öncekini taşır. Hedef oraya düşerse tahmin
  garantili %0 ile çözülür ve kalibrasyonu kirletir. Cuma günü yazılan 1g
  tahmini **Pazartesi'yi** hedefler. → `reviews/2026-08.md` **K17**
- **Tatil takvimi `pt.py`'de sabit** (`MARKET_HOLIDAYS`), kaynağı
  `borsaistanbul.com/files/pay-piyasasi-<YIL>-yili-tatil-tablosu.pdf`.
  **Arife günleri yarım gün seans yapar → AÇIK sayılır.** Takvim 2026 sonuna
  kadar dolu; ötesi için motor uyarır.
- **Bir günü tamamen kaçırdın**: geriye dönük snapshot **alma**. Boşluk,
  uydurulmuş veriden iyidir.
- `accrual` hafta sonu kâr payı yazmaz; birikim Pazartesi kredilendirilir.

---

## 5. `market_state` zorunlu listesi

`MARKET_STATE_REQUIRED` alanlarının hepsi doldurulmalı; motor eksikte uyarır ve
**bu veri geriye dönük toplanamaz.**

Her değişkene `<değişken>_asof` damgası koy. `fetch_market.py` bunu kendiliğinden
yapıyor — elle doldurduğun alanlarda unutma.

**Hâlâ elle:** `fed_sep_hike_prob` (açık iş #7 — kaynaklar *yönde bile*
çelişiyor: bir kaynak %54,4 indirim, diğerleri %59-68 artış olasılığı veriyor).
Tarihli tek bir CME FedWatch kaydı bulunana kadar **`null` bırak.** Çelişkili
bir sayı yazmaktansa boş bırakmak doğrudur.

---

## 6. Genel kural

İki bağımsız kaynak %0,5'ten fazla ayrışıyorsa ikisini de not et ve **daha
resmî olanı** kullan (TEFAS, TCMB, FRED, LBMA). Ayrışma sebebi genelde
alış/satış farkı, gecikmeli veri veya farklı enstrümandır.

Her snapshot'ta fiyatın **hangi ana** ait olduğuna dikkat et ve saati
`--notes`'a yaz.
