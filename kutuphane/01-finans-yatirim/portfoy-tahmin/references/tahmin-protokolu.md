# Tahmin Protokolü

Tahmin üretirken oku. Buradaki kuralların çoğu tahminleri *daha isabetli* yapmak için değil, **daha dürüst ve ölçülebilir** yapmak için var. Ölçülebilir bir kötü tahmin, ölçülemeyen iyi bir tahminden değerlidir.

## 1. Kanıt toplama

### Nereye bakılır

Aramayı portföy ağırlığına göre yap. %37'si altında olan bir portföyde günün 6 aramasından 3'ü altın tarafına gitmeli, %6'lık bir kaleme 1 arama bile fazladır.

Varlık sınıfına göre sürücüler:

| Varlık | Birincil sürücüler | Arama odağı |
|---|---|---|
| Gram altın | ABD reel faizi, Fed beklentisi, DXY, jeopolitik risk, merkez bankası alımları, USD/TRY | `gold price forecast`, `Fed rate expectations`, `dolar kuru` |
| Teknoloji fonu | Nasdaq/NDX, yarı iletken haber akışı, büyük teknoloji bilançoları, AI capex haberleri | `Nasdaq today`, `semiconductor stocks`, `<şirket> earnings` |
| Çoklu tema fonu | Fonun içerik dağılımı (bilmiyorsan bir kez araştır ve `notes`'a yaz) | fon içeriğine göre |
| Altın+gümüş fonu | Yukarıdaki altın sürücüleri + gümüş sanayi talebi + altın/gümüş rasyosu | `silver price`, `gold silver ratio` |
| TL bazlı her şey | TCMB faiz kararı ve enflasyon verisi, CDS, portföy akımları | `TCMB faiz kararı`, `Türkiye enflasyon` |

### Ne sayılır kanıt olarak

Her kanıt kaydı şunu içermeli: iddia, kaynak, hangi varlığı etkiler, yön, ağırlık.

Ağırlıklandırma:
- **yüksek**: Gerçekleşmiş, tarihli, sayısal bir olay. Faiz kararı açıklandı, enflasyon verisi geldi, bilanço yayınlandı, savaş başladı.
- **orta**: Yetkili bir aktörün açıklaması, resmi öngörü revizyonu, büyük bir kurumun pozisyon değişikliği.
- **düşük**: Analist yorumu, "beklenti", teknik analiz, "piyasa şunu fiyatlıyor" tipi anlatılar.

**Düşük ağırlıklı kanıt tahmini değiştirmemeli.** Sadece kayda geçer. Bu kural önemli çünkü haber akışının %80'i bu kategoridedir ve model olarak bunlara aşırı tepki verme eğilimin var.

### Fiyatlanmışlık testi — ve sürprizin kaydı

Bir haberi kanıt olarak kullanmadan önce sor: *bu bilgi zaten fiyatta mı?* Herkesin bildiği, günlerdir konuşulan bir beklenti yarının hareketini açıklamaz. Sadece **sürpriz** hareket ettirir. Beklentiyle gerçekleşen arasındaki fark yoksa, kanıt ağırlığını düşür.

**Bu, metne gömülmez — alan olarak yazılır.** Takvimi belli, sayısal bir açıklama kanıt olarak giriyorsa:

```json
{"id": "g1", "asset": "hepsi", "direction": "flat", "weight": "yuksek",
 "scheduled": true, "indicator": "TR_CPI_MoM", "unit": "aylik %",
 "consensus": 1.75, "consensus_method": "TCMB (1,68) / AA (1,82) orta noktasi",
 "consensus_range": [1.35, 2.10], "actual": 1.78,
 "claim": "...", "source": "tuik.gov.tr", "url": "https://..."}
```

`surprise` ve `surprise_yon` **motorda otomatik türetilir** — elle yazma.

| Kural | Neden |
|---|---|
| `scheduled: true` ise `consensus` zorunlu | Motor reddeder; beklentisiz olay fiyatlanmışlık testine girmez |
| `consensus` tek başına meşru | Açıklama öncesi kaydedilen beklenti çıpası |
| `actual` varken `consensus` yoksa **hata** | Sürpriz ölçülemez |
| Veri gelince aynı kanıt `evidence_patch` ile güncellenir | Yeni kanıt açma — sürpriz, beklenti ile gerçekleşenin **aynı kaydında** durmalı |

`consensus_method` alanını her zaman doldur: iki anket varsa hangisini ya da orta noktayı aldığını yaz. Sonradan "sürpriz +0,03 mü +0,10 mu" tartışması çıkmasın.

Bu şemanın sınanacağı hipotez `reviews/on-kayit.md` → **H4**: fiyat hareketinin büyüklüğü olayın kendisiyle değil `|surprise|` ile ilişkilidir. Minimum 30 takvimli olay (≈1 yıl).

---

## 2. Tahmin üretme

### Yatay nokta değil, aralık

Her tahmin şunları içerir:

```json
{
  "asset": "gram_altin",
  "horizon": "1d",
  "point_pct": 0.3,
  "low_pct": -1.2,
  "high_pct": 1.8,
  "interval": 80,
  "p_up": 0.56,
  "confidence": "dusuk",
  "drivers": ["e1", "e3"],
  "rationale": "Tek cümle. Neden bu yön.",
  "invalidator": "Bu tahmini geçersiz kılacak somut olay."
}
```

`low_pct`/`high_pct`, gerçekleşenin **%80 ihtimalle** içinde kalacağını düşündüğün bant. Nokta tahmin bandın içinde olmalı (script kontrol eder).

### Bant genişliği nereden gelir

Bandın kaynağı senin hissin değil, **varlığın oynaklığıdır**. Başlangıç referansı (Türkiye koşullarında tipik günlük hareket):

| Varlık | Tipik günlük std | 1g %80 bandı | 1h bandı | 1a bandı |
|---|---|---|---|---|
| Gram altın (TL) | %0.8–1.5 | ±1.5–2.5 | ±4–6 | ±8–14 |
| Teknoloji fonu | %1.0–2.0 | ±2–3 | ±5–8 | ±10–18 |
| Altın+gümüş fonu | %1.0–1.8 | ±2–3 | ±5–7 | ±9–15 |
| Karma/çoklu tema fonu | %0.6–1.2 | ±1.2–2 | ±3–5 | ±6–11 |

Ufuk uzadıkça bant **kabaca zamanın kareköküyle** genişler; 1 haftalık bant 1 günlüğün ~2.6 katı, 1 aylık ~5.5 katı. Doğrusal genişletme yapma.

Bu tablo başlangıç noktasıdır. Kalibrasyon incelemesinde bant kapsama oranı %80'den sapıyorsa **bu sayıları güncelle** ve güncellemeyi `reviews/` altına yaz. Sistem böyle öğrenir.

### Bant, sabit tablodan değil İMA OYNAKLIKTAN türetilir (13.08.2026)

Yukarıdaki tablo bir **geri düşüş**tür. Piyasa her gün kendi oynaklık tahminini
yayınlıyor ve bu ücretsiz, tarihli, makine-okunur:

| Seri (FRED) | Ne | Hangi varlık |
|---|---|---|
| `GVZCLS` | CBOE altın ETF ima oynaklık (yıllık %) | `gram_altin`, `KUT` |
| `VXNCLS` | CBOE Nasdaq-100 ima oynaklık | `KTJ`, `KIK` |
| `VIXCLS` / `VXVCLS` | VIX 30g / 3ay — vade yapısı | rejim |
| `EVZCLS` | CBOE EUR/USD ima oynaklık | `doviz_katilim` — **zayıf vekil**, TL değil |

`fetch_market.py` bunları çekiyor ve `iv_bant()` yardımcısı bandı veriyor:

```
sigma_gun = (IV_yillik / 100) / sqrt(252)
sigma_h   = sigma_gun * sqrt(islem_gunu)        # 1g=1, 1h=5, 1a=21
bant_%80  = ± 1,2816 * sigma_h * VRP            # VRP = 0,85
```

**`VRP` (varyans risk primi):** ima oynaklık gerçekleşen oynaklığı sistematik
olarak **aşar** — yatırımcı oynaklık riskini taşımak için prim ister
(Carr & Wu 2009; Bollerslev-Tauchen-Zhou 2009). 0,85 başlangıç değeri,
kalibrasyonla ayarlanacak.

**⚠ Ufuk ölçekleme düzeltmesi.** Eski protokol "1h ≈ 2,6×, 1a ≈ 5,5×" diyordu;
bu **takvim günü** ölçeklemesiydi (√7, √30). Fiyat yalnızca işlem günlerinde
oluşur, doğrusu **√5 = 2,24×** ve **√21 = 4,58×**. Eski çarpanlar bantları
~%17-20 fazla geniş yapıyor, bu da kapsama oranını yapay olarak %80'in üstüne
çıkarıyordu.

**⚠ IV bandı BUGÜN operatif değil — ölçülüyor.** 13.08'de hesaplandığında
IV-türevli gram altın bantları (1g ±%1,95 · 1h ±%4,37 · 1a ±%8,95) mevcut
bantlardan **dar** çıktı. Bu, **K25 ile çelişiyor**: 1 haftalık bantlar
sistematik olarak dar bulunmuş ve genişletilmişti (gram altın bir haftada
gerçekte **+%8** yaptı, IV ±%4,37 diyor — yani gerçekleşen oynaklık ima
oynaklığı ciddi şekilde aştı).

İki kanıt kaynağı zıt yönü gösterdiği için **hiçbiri tek başına
uygulanmıyor**. IV değerleri `market_state`'e her gün **kaydediliyor**,
operatif bantlar şimdilik tabloda kalıyor, ve hangisinin daha iyi kalibre
olduğu `on-kayit.md` → **H10** ile ölçülecek. Bu, bu hafta iki kez yapılan
n=1 hatasının (K26) üçüncü kez yapılmaması içindir.

### Gram altını AYRIŞTIRARAK tahmin et (Fermi)

Süperforecasting literatüründeki en güçlü tekniklerden biri: çözülemez soruyu
çözülebilir parçalara böl. Gram altın **zaten bir çarpım**:

```
gram_altin = XAUUSD × USDTRY / 31,1035
```

Tek parça tahmin etmek yerine iki bacağı ayrı tahmin edip birleştir; bant da
karekök toplamıyla gelir:

```
sigma_gram = sqrt(sigma_XAU² + sigma_FX² + 2·rho·sigma_XAU·sigma_FX)
```

13.08 örneği: σ_XAU = %1,758 (GVZ 27,90), σ_FX = %0,359 (TL ima oynaklık
%5,7 yıllık), ρ≈0 → σ_gram = **%1,794**. Yani gram altının günlük oynaklığının
**neredeyse tamamı dolar bacağından** geliyor, TL bacağı %4'lük bir katkı.
Bu, "TL sürünmesi altını yukarı iter" argümanının **1 günlük ufukta neden
işe yaramadığını** açıklıyor: sürünme günde %0,04, oynaklık %1,79.

### p_up ve aşırı güven

`p_up` = fiyatın yükselme olasılığı. Kritik kural: **1 günlük ufukta p_up neredeyse hiçbir zaman 0.40–0.60 aralığının dışına çıkmamalı.** Ertesi gün yönünü %70 güvenle bildiğini düşünüyorsan yanılıyorsun. Büyük bir olay gerçekleşmiş ve piyasa henüz açılmamışsa (ör. hafta sonu gelen kritik haber) 0.65'e kadar çıkabilirsin, o kadar.

1 haftalık ufukta 0.35–0.65, 1 aylık ufukta 0.30–0.70 makul sınırlar.

`confidence` alanı ayrıca "dusuk / orta / yuksek" — 1g tahminler için varsayılan **her zaman `dusuk`**.

### USD/TRY istisnası — sürünen kur rejimi (13.08.2026, H-usdtry)

`p_up ∈ [0,40; 0,60]` kuralı **serbest dalgalanan** varlıklar içindir. USD/TRY
sürünen kur rejiminde: 259 günde pozitif gün oranı **%79,2**, drift/vol ≈ 0,67
(majör kurlarda ~0,05). Bu yüzden `doviz_katilim` 1g için:

- `p_up` tabanı **0,65** (rejim değişmedikçe — TCMB rejimi değişirse istisna düşer)
- Bant **asimetrik**: üst uç alt uçtan uzun (ampirik p10/p90 ≈ −0,03/+0,21)
- `invalidator` alanına **zorunlu sıçrama senaryosu** yazılır; |Δ|>%1 gün
  gelirse çözümleme satırı `sicrama` etiketi alır, atılmaz
- Bant sıçramaya göre **genişletilmez** — kapsama %85-90'a çıkarsa uyarıdır.
  Forward kur **üst sınırdır** (risk primi içerir, ~2× gerçekleşen), yansız
  tahminci değildir.

### p_up granülerliği

`p_up` 0,01 hassasiyetinde yazılır (0,56 gibi); 0,05 katlarına yuvarlamak
ölçülebilir isabet kaybıdır (GJP). Denetim 13.08'de yapıldı: defter temiz
(%35 yuvarlak — patoloji yok), kural ucuz olduğu için yine de sabitlendi.

### Trendi tahmin sanma

En sık yapılan hata: son 3 günün yönünü uzatıp buna "tahmin" demek. Momentum kısa vadede zayıf bir sinyaldir. Eğer gerekçen "son zamanlarda yükseliyordu" ise, `point_pct` değerini 0'a yaklaştır ve `confidence`'ı `dusuk` bırak.

### Sıfır tahmin meşrudur

Belirleyici bir kanıt bulamadıysan `point_pct: 0` yaz. Bu bir başarısızlık değil, doğru cevaptır. Sistem bunu ödüllendirir çünkü baseline'ın kendisi budur.

---

## 2b. NE İŞE YARAMAZ — kanıtla elenenler

Bu liste, sinyal eklemek kadar önemli: **eklenmemesi gerekenleri** kayda geçirir.
Hepsi hakemli literatürde belgelenmiş başarısızlıklar.

| Yöntem | Belgelenmiş durum |
|---|---|
| **Teknik analiz / basit işlem kuralları** | Sullivan-Timmermann-White (JF 1999): DJIA'da 100 yıllık veri, veri-tarama yanlılığı bootstrap ile düzeltilince **kârlı basit kural yok** |
| **Analist fiyat hedefleri** | 12 aylık hedeflerin **%70'ten fazlası tutmuyor**; mutlak hedef hatası ortalama **%45** (Brav & Lehavy JF 2003; Kerl & Walter) |
| **Hisse primi öngörü değişkenleri** | Goyal-Welch-Zafirov (RFS 2024): 29 yeni değişkenin **1/3'ünden fazlası örneklem-içinde bile** anlamlılığını yitirdi |
| **Trend takibi / zaman serisi momentum** | Moskowitz-Ooi-Pedersen'in Sharpe ~1,28'i **2010'dan beri kabaca yarıya indi**; 5 yıllık kayan Sharpe sıfırdan ayırt edilemiyor |
| **Pre-FOMC drift** | 1994-2011'de yıllık getirinin ~%80'i, **2015'ten sonra tamamen kayboldu** |
| **PEAD (kazanç sonrası sürüklenme)** | Mikro-cap dışı hisselerde **2006'da kaybolmuş** |
| **Ekstremleştirme** | Turnuvada işe yaradı, tekrarlanmadı — **eklemeyin** |
| **Altın/gümüş rasyosu** | Hakemli destek bulunamadı |
| **AAII / put-call duyarlılık** | AAII'nin **kendi sayfası** "gelecekteki piyasa yönünü öngörmez" diyor. TR eşdeğeri de yok |
| **Kazanç revizyon momentumu** | Sinyal var ama **2003 sonrası gecikme kayboldu** ve ücretsiz veri yok |

**Protokolün "trendi tahmin sanma" kuralı bu literatürle tam uyumlu ve
korunuyor.**

### ⚠ Reel faiz–altın ilişkisi 2022'de KIRILDI

| Dönem | Altın–TIPS korelasyonu |
|---|---|
| 2005–2021 | **%84** |
| 2022–2023 | **%3** |
| 2024'ten beri | **%7** |

Sebep: marjinal alıcı ETF'lerden **merkez bankalarına** kaydı (2022'de 1.082
ton, 1950'den beri rekor; 2010-21 ortalaması ~473 ton).

**Sonuç:** `us10y_real` **kaydedilmeye devam** ediyor ama kanıt ağırlığı
`orta` → **`dusuk`**. "Reel faiz düştü → altın çıkar" cümlesi 2022 sonrası
veriyle desteklenmiyor. 11.08'de bu deftere tam bu hata yapıldı ve ertesi gün
geri alındı — literatür de aynı yöne işaret ediyor.

### Kaydedilir ama tahmin girdisi YAPILMAZ

**CFTC COT konumlanma verisi** (`publicreporting.cftc.gov`, anahtarsız, altın
kodu `088691`) `market_state`'e yazılır ama **tahmin gerekçesi olmaz**:
- Kanıt zayıf ve popüler anlatının **tersi** yönde (Bessembinder & Chan 1992:
  *ticari hedger'lar* spekülatörlerden daha iyi öngörüyor)
- **Gecikme öldürücü:** rapor Salı konumlanmasını Cuma yayınlıyor → 1 günlük
  tahmin için daima **3+ gün bayat**

12 ay sonra kendi verimizle test edilebilir bir değişken olur. "Kayıt
tahminden önemlidir" ilkesinin uygulaması.

---

## 3. Portföy seviyesinde toplama

Varlık bazlı tahminleri ağırlıklarla toplayarak portföy tahmini üretebilirsin — ama **korelasyonu unutma**. Bu portföyde gram altın ve KUT (altın+gümüş fonu) neredeyse aynı riski taşır; ikisi birlikte %43 eder. Bunları bağımsız varlık gibi toplarsan portföy bandını gerçekte olduğundan dar hesaplarsın.

Pratik yaklaşım: portföy bandını, bileşenlerin ağırlıklı bandının **%70-85'i** olarak al (tam bağımsızlık %50'ye, tam korelasyon %100'e karşılık gelir). Bu portföyde korelasyon yüksek olduğu için üst uca yakın kal.

Ayrıca not et: TL bazlı bir portföyde neredeyse her varlık USD/TRY'ye pozitif duyarlıdır. Yani "portföy TL bazında %2 arttı" ile "zenginleştim" aynı şey değil. Ara sıra USD bazlı değeri de hesapla ve raporda göster — bu, TL enflasyonunun yarattığı nominal yanılsamayı kırar.

---

## 4. Kaydetme

Tahmin JSON'unu hazırla ve kaydet:

```bash
python scripts/pt.py --root <yol> forecast --file tahmin.json
```

Dosya şeması:

```json
{
  "as_of": "2026-07-30",
  "protocol_version": 1,
  "day_type": "sakin",
  "scheduled_events": [
    {"tarih": "2026-08-07", "olay": "ABD tarim disi istihdam",
     "beklenti": 130000, "birim": "kisi", "onem": "yuksek"}
  ],
  "market_state": {
    "usdtry": 41.2, "usdtry_asof": "2026-07-30",
    "xauusd": 3350, "dxy": 97.1, "us10y": 4.2,
    "nasdaq": 25373.85, "nasdaq_asof": "2026-07-29",
    "bist100": 13458.1, "brent": 92.27
  },
  "evidence": [
    {"id": "e1", "asset": "gram_altin", "direction": "up", "weight": "orta",
     "claim": "Fed tutanaklarında Eylül indirimi sinyali", "source": "reuters.com",
     "url": "https://..."}
  ],
  "forecasts": [ ... ]
}
```

**Üst düzey zorunlu alanlar:**

- `protocol_version` — bant tablosu, tahmin modeli veya skorlama kuralı değişirse artar. Farklı sürümler aynı havuzda toplanmaz.
- `day_type` — `veri` / `sakin` / `tatil` / `hafta_sonu`. `veri` = o gün **takvimi önceden belli**, sayısal, fiyat hareket ettiren bir açıklama var. Sonradan çıkan haber `veri` yapmaz.
- `scheduled_events` — yaklaşan takvimli olaylar. Bandı neden geniş tuttuğunun kaydı.
- `market_state` — `MARKET_STATE_REQUIRED` listesinin tamamı. **Her değişkene `<değişken>_asof` damgası koy**; taşınan bir değere tarih vurulmazsa bayat veri sessizce güncel görünür.

`drivers` alanı kanıt `id`'lerine referans verir. Bu bağ, kalibrasyon aşamasında "hangi tür kanıt gerçekten işe yaradı" sorusunu cevaplamayı mümkün kılar — bağ kurmazsan o analiz yapılamaz.

`target_date` yazmana gerek yok, script hesaplar: hedef, varlığın **fiyatlandığı ilk güne** yuvarlanır (hafta sonu + Borsa İstanbul resmî tatilleri; arife günleri yarım gün seans yaptığı için **açık** sayılır). `crypto` 7/24 işlem gördüğü için kaydırılmaz. Yani Cuma günü yazılan 1g tahmini **Pazartesi'yi** hedefler. Elle `target_date` verirsen motor gerekirse yine kaydırır ve `atlanan` listesinde bildirir.

---

## 5. Raporda tahminleri sunarken

- Nokta tahmini bandsız yazma. Hiçbir zaman.
- "Altın yükselecek" değil, "%56 ihtimalle yukarı, beklenen %0.3, bant [-1.2, +1.8]".
- Gerekçeyi tek cümlede ver, paragraf yazma.
- `invalidator`'ı mutlaka göster — kullanıcının tahmini ne zaman çöpe atacağını bilmesi, tahminin kendisinden değerli.
- Alım/satım önerisi yok. Kullanıcı doğrudan sorarsa: kararı etkileyecek olguları listele, kararı verme, lisanslı danışman olmadığını bir kez belirt.

---

## Sapma ne zaman anomalidir — yüzdelik kuralı (K43, 16.08.2026)

**Bir sapma anomali sayılmadan önce, aynı varlığın tarihsel sapma
dağılımındaki yüzdeliği hesaplanır. Üst %10'un dışındaysa kayıt AÇILMAZ.**

Sebep bir vakadır: 14.08'de KIK'in KTJ'den "keskin ayrıştığı" kaydedildi ve
**iki gün boyunca** tahmin gerekçesi olarak kullanıldı (KIK güveni `dusuk`,
bant geniş). Sonradan ölçüldüğünde:

| | |
|---|---|
| artık | −0,455 pp |
| z | −0,84 |
| sıra | 246 günün **87.**'si → **üst %35** |

Yani ortalama **her üç günde bir** görülen bir sapma. Kesin kanıt: bir
**önceki** gün daha büyük bir artık üretilmişti (+0,74 pp) ve
işaretlenmemişti — işaretleten şey sinyal değil **sapmanın yönüydü**.

**Pratikte:** artığı hesapla → o varlığın artık std'sine böl → yüzdeliği yaz.
Üst %10 dışındaysa kanıt kaydı açma, gerekçeye geçirme, bandı genişletme.
Kanıt yazıyorsan **yüzdelik metne girer** — savcının 2b başlığı bunu denetler.

Uygulama örneği (07.09): KTJ artığı 0,61σ → **kayıt açılmadı**; ZPE artığı
1,67σ = üst %5 → **kayıt açıldı** ve mekanizması yazıldı.

