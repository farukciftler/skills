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

### Fiyatlanmışlık testi

Bir haberi kanıt olarak kullanmadan önce sor: *bu bilgi zaten fiyatta mı?* Herkesin bildiği, günlerdir konuşulan bir beklenti yarının hareketini açıklamaz. Sadece **sürpriz** hareket ettirir. Beklentiyle gerçekleşen arasındaki fark yoksa, kanıt ağırlığını düşür.

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

### p_up ve aşırı güven

`p_up` = fiyatın yükselme olasılığı. Kritik kural: **1 günlük ufukta p_up neredeyse hiçbir zaman 0.40–0.60 aralığının dışına çıkmamalı.** Ertesi gün yönünü %70 güvenle bildiğini düşünüyorsan yanılıyorsun. Büyük bir olay gerçekleşmiş ve piyasa henüz açılmamışsa (ör. hafta sonu gelen kritik haber) 0.65'e kadar çıkabilirsin, o kadar.

1 haftalık ufukta 0.35–0.65, 1 aylık ufukta 0.30–0.70 makul sınırlar.

`confidence` alanı ayrıca "dusuk / orta / yuksek" — 1g tahminler için varsayılan **her zaman `dusuk`**.

### Trendi tahmin sanma

En sık yapılan hata: son 3 günün yönünü uzatıp buna "tahmin" demek. Momentum kısa vadede zayıf bir sinyaldir. Eğer gerekçen "son zamanlarda yükseliyordu" ise, `point_pct` değerini 0'a yaklaştır ve `confidence`'ı `dusuk` bırak.

### Sıfır tahmin meşrudur

Belirleyici bir kanıt bulamadıysan `point_pct: 0` yaz. Bu bir başarısızlık değil, doğru cevaptır. Sistem bunu ödüllendirir çünkü baseline'ın kendisi budur.

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
  "market_state": {"usdtry": 41.2, "xauusd": 3350, "dxy": 97.1, "us10y": 4.2},
  "evidence": [
    {"id": "e1", "asset": "gram_altin", "direction": "up", "weight": "orta",
     "claim": "Fed tutanaklarında Eylül indirimi sinyali", "source": "reuters.com",
     "url": "https://..."}
  ],
  "forecasts": [ ... ]
}
```

`drivers` alanı kanıt `id`'lerine referans verir. Bu bağ, kalibrasyon aşamasında "hangi tür kanıt gerçekten işe yaradı" sorusunu cevaplamayı mümkün kılar — bağ kurmazsan o analiz yapılamaz.

`target_date` yazmana gerek yok, script hesaplar (fon ve hisse için sonraki iş gününe yuvarlar).

---

## 5. Raporda tahminleri sunarken

- Nokta tahmini bandsız yazma. Hiçbir zaman.
- "Altın yükselecek" değil, "%56 ihtimalle yukarı, beklenen %0.3, bant [-1.2, +1.8]".
- Gerekçeyi tek cümlede ver, paragraf yazma.
- `invalidator`'ı mutlaka göster — kullanıcının tahmini ne zaman çöpe atacağını bilmesi, tahminin kendisinden değerli.
- Alım/satım önerisi yok. Kullanıcı doğrudan sorarsa: kararı etkileyecek olguları listele, kararı verme, lisanslı danışman olmadığını bir kez belirt.
