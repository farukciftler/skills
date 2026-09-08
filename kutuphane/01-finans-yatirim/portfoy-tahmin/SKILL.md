---
name: portfoy-tahmin
description: Kişisel yatırım portföyü için disiplinli tahmin günlüğü ve kalibrasyon sistemi - portföy tanımlama, günlük fiyat/piyasa snapshot'ı, web araştırmasına dayalı 1 gün / 1 hafta / 1 ay yön tahminleri, tahminlerin gerçekleşenle otomatik eşleştirilmesi, ve tahmin isabetinin naif baseline'a karşı ölçülmesi. Kullanıcı portföyünü paylaştığında, "portföyümü takip et", "sabah raporu", "bugünkü tahmin", "portföy tahmini", "dünkü tahmin tuttu mu", "geçen ayki tahminim", "fon/altın ne olur", "yeni fon ekle", "kalibrasyon", "tahmin geçmişim" dediğinde; ya da gram altın, TEFAS fonları (KTJ, KIK, KUT vb.), katılma hesabı, hisse, kripto gibi varlıkların değer takibi/senaryo analizi istendiğinde bu skill'i kullan. Kullanıcı "tahmin" kelimesini hiç kullanmasa bile, elindeki varlıkların yarın/haftaya/aya ne olacağını konuşuyorsa devreye gir. Yatırım tavsiyesi vermez; tahmin kaydeder, ölçer ve isabetsizliği açıkça raporlar.
---

# Portföy Tahmin Günlüğü

Bu skill bir kâhin değil, bir **kalibrasyon defteri** kurar. Amaç "yarın altın ne olur" sorusunu doğru cevaplamak değil — cevabı yazılı olarak kayda geçirmek, gerçekleşenle karşılaştırmak, ve zaman içinde hangi tahminlerin işe yaradığını, hangilerinin gürültü olduğunu **sayıyla** göstermek.

## Dürüstlük çerçevesi (her çalıştırmada geçerli)

Bu maddeler sistemin omurgası. Bunları yumuşatma, atlamayı teklif etme:

1. **1 günlük fiyat tahmini fiilen rastgeledir.** Gram altın, fon veya kur için ertesi gün yönü tutturma oranının uzun vadede %50'ye yakınsaması normaldir ve beklenendir. Sistem bunu gizlemez, ölçer.
2. **Her tahmin naif baseline ile karşılaştırılır.** Baseline = "yarın bugünkü fiyatta kalacak" (%0 değişim). Tahminlerin baseline'dan daha iyi değilse rapor bunu açıkça yazar. Çoğu dönemde daha iyi olmayacak.
3. **Nokta tahmini asla tek başına verilmez.** Her tahmin bir aralık (%80 güven bandı) ve bir yön olasılığı (p_up) içerir. Aralık, nokta tahminden daha bilgilendiricidir.
4. **Bu çıktı yatırım tavsiyesi değildir ve alım/satım kararı için kullanılmamalıdır.** Claude lisanslı bir yatırım danışmanı değildir. Kullanıcı "alayım mı / satayım mı" diye sorarsa: karar girdisi olabilecek olguları ver, kararı verme.
5. **Kayıt tahminden önemlidir.** Bir gün veri bulunamazsa tahmin uydurma; `veri_yok` olarak kaydet ve geç.
6. **1 aylık çıktı `projeksiyon`dur, tahmin değildir.** 1 aylık ufukta yılda ~12 örtüşmeyen gözlem vardır; %55'lik bir edge'i ölçmek ~21 yıl sürer. Ölçülemeyen bir şeye "tahmin" demek, kalibrasyon defterinde ölçülüyormuş izlenimi yaratır. Üretmeye devam et, ama skill iddiasına dahil etme.
7. **Birincil metrik eşleştirilmiş işaret testidir, yön isabeti değildir.** Yön isabeti bir teşhistir; ikili sınıflama `p_up`'ın taşıdığı bilgiyi atar (0,54 ile 0,80 aynı sayılır) ve aynı edge'i göstermek için 3-6 kat fazla gözlem ister. Raporda başlık sayı olarak kullanma. Güven aralığı %50'yi kapsıyorsa **"şans"** de.
8. **Analiz planı `data/reviews/on-kayit.md`'de sabittir.** Orada yazmayan bir sonuç raporlanıyorsa **keşifsel** diye etiketlenir ve kanıt sayılmaz. Bu, "veriyi görüp hangi alt kümede iyi çıkmışım" diye bakmayı engelleyen tek mekanizmadır.

Kullanıcı sistemi "para kazandıran bir şey" gibi konumlandırmaya başlarsa bunu bir kez, sakin şekilde düzelt: bu bir öğrenme ve disiplin aracı.

## Veri düzeni

Tüm veri tek bir kökte durur (varsayılan `~/portfoy-takip`, kullanıcı başka yer derse orası):

```
portfoy-takip/
  portfolio.json              # varlık tanımları + miktarlar + look-through
  snapshots/YYYY-MM-DD.json   # o günün fiyatları ve portföy değeri
  forecasts/YYYY-MM-DD.json   # tahminler + kanıtlar + market_state + day_type
  resolutions.jsonl           # çözümlenmiş tahmin sonuçları (append-only)
  evidence/YYYY-MM-DD.md      # o günün dünya gündemi notu (serbest metin)
  holdings/YYYY-MM-DD.json    # fonların iç varlık dağılımı (look-through)
  reviews/YYYY-MM.md          # aylık kalibrasyon değerlendirmesi
  reviews/on-kayit.md         # ANALİZ PLANI — hangi test, hangi n, hangi eşik
```

Tüm dosya işlemleri `scripts/pt.py` üzerinden yapılır — elle JSON düzenleme yapma, şema bozulur.

```bash
python scripts/pt.py --help          # tüm alt komutlar
python scripts/pt.py <komut> --help  # tek komut detayı
```

Script yalnızca standart kütüphane kullanır ve **internete çıkmaz**. Fiyat ve haber toplama işini Claude web search ile yapar, script sadece deterministik defter tutar. Bu ayrım kasıtlı: hesap makinesi kısmı asla halüsinasyon görmemeli.

---

## Mod 1 — Kurulum (`kur`)

Kullanıcı portföyünü ilk kez paylaştığında.

1. Varlıkları sınıflandır. Sınıf, tahmin yönteminin ne olacağını belirler:

| class | Örnek | Fiyat kaynağı | Tahmin edilir mi |
|---|---|---|---|
| `spot` | Gram altın, gümüş, USD/TRY | Anlık, 7/24 veya seans içi | Evet |
| `fund_tefas` | KTJ, KIK, KUT | TEFAS, **T+1 gecikmeli**, sadece iş günü | Evet, gecikme dikkate alınarak |
| `accrual` | Katılma hesabı, mevduat | Fiyat yok, birikim var | Hayır — projeksiyon yapılır |
| `equity` | BIST/ABD hissesi | Seans içi | Evet |
| `crypto` | BTC, ETH | 7/24 | Evet |

2. Miktar mı değer mi belli değilse: kullanıcı çoğu zaman "263.000 TL KTJ" der, kaç pay olduğunu bilmez. Bu normal. `value_try` gir, ilk fiyat snapshot'ında script `implied_units` hesaplar ve sonrasında miktar üzerinden çalışır.

3. `python scripts/pt.py init --root <yol>` ve her varlık için `add-asset`.

4. Kurulum bittiğinde portföyü tabloyla geri göster ve **hangi varlığın tahmin edilebilir olmadığını** söyle (accrual olanlar).

Yeni varlık sonradan eklendiğinde aynı akış, sadece o varlık için. Geçmiş tahminler etkilenmez.

---

## Mod 2 — Sabah raporu (`sabah`) — ana akış

Kullanıcı "sabah raporu", "günaydın portföy", "bugün ne durumdayız" dediğinde. Sıra önemli:

### Adım 1 — Bağlamı çek (script)

```bash
python scripts/pt.py report --root <yol> --date <bugün>
```

Bu JSON döner: dünkü tahmin, 1 hafta önce bugün için yapılmış tahmin, 1 ay önce bugün için yapılmış tahmin, son snapshot, açık (henüz çözülmemiş) tahminler ve güncel kalibrasyon özeti. **Önce bunu çalıştır**, sonra arama yap — neyi aramaya ihtiyacın olduğunu bu belirler.

### Adım 2 — Güncel fiyatları topla

**Önce makine-okunur kaynaklar, sonra web search.** Arama motoru özetinden sayı okuma — bu deponun kaydettiği makro hataların hepsi oradan geldi (US10Y'de 40bp, Nasdaq'ta 4 gün bayat veri, BIST'te 675 puan, XAUUSD'de ~95 dolar). Haber metni bir sayıyı **hangi güne ait olduğunu söylemeden** taşır.

```bash
python3 scripts/fetch_market.py --date $(date +%F)   # insan okunur
python3 scripts/fetch_market.py --json               # market_state blogu
```

`market_state`'in neredeyse tamamını tarihli ve çapraz kontrollü getirir (FRED, Yahoo, TCMB, LBMA). Bulamadığını `null` bırakır, sebebini yazar.

Web search yalnızca üçü için: **TEFAS fon fiyatları** (API kapalı → `WebFetch` ile `tefas.gov.tr/FonAnaliz.aspx?FonKod=<KOD>`; üçüncü taraf siteler bayat veri gösteriyor, çelişkide daima TEFAS), **gram altın TL** (iki bağımsız TR kaynağı, alış fiyatı, saatiyle), **`accrual` bakiyesi** (sadece banka ekranı).

`references/veri-kaynaklari.md` dosyasını oku: doğrulanmış uç noktalar, denenip elenen kaynaklar, kaynak başına değişen User-Agent tuzağı ve gram altın baz aralığı orada. Bulamadığın fiyatı **uydurma**, `null` bırak.

```bash
python scripts/pt.py snapshot --root <yol> --date <bugün> --prices '{"gram_altin": 6187.5, ...}'
```

Kullanıcı para çektiyse/yatırdıysa **aynı komutta** `--flows '{"hesap": -28000}'`
ekle (+ yatırma, − çekme); unutulduysa sonradan `flow` alt komutu. Akış
kaydedilmezse günün getirisi nakit hareketiyle kirlenir.

### Adım 3 — Dünkü/geçen haftaki/geçen ayki tahminleri çözümle (script)

```bash
python scripts/pt.py resolve --root <yol> --date <bugün>
```

Snapshot yazıldıktan sonra çalıştır. Vadesi gelen tüm tahminleri gerçekleşenle eşleştirir, `resolutions.jsonl`'a yazar. Snapshot yoksa (hafta sonu, tatil, TEFAS gecikmesi) `pending` bırakır ve bir sonraki iş gününde tekrar dener — bunu hata sanma.

### Adım 4 — Dünya gündemini tara (web search) — **ATLANMAZ**

**Sert kural (kullanıcı talimatı, 07.08.2026): bir gün için snapshot alındıysa
o gün için gündem taraması da yapılır ve `evidence/YYYY-MM-DD.md` yazılır.
İstisnası yok.** Kullanıcı sadece "şu bakiyeyi güncelle", "şu çekimi işle" gibi
**dar bir iş** istese bile geçerli — snapshot alınıyorsa tarama da yapılır.

Sebep: bu dosya, "hangi tür haber gerçekten fiyatı hareket ettirdi" analizinin
tek ham verisi ve **geriye dönük doldurulamaz.** Bir haftanın altı gününde
kanıt varken bir gününde yoksa, o gün kayıp gözlem değildir — daha kötüsüdür:
kanıt/fiyat eşleşmesinde **seçilim yanlılığı** yaratır, çünkü boş kalan günler
rastgele değil "acelesi olan günler"dir. Fiyat serisinin boşluğu göze batar,
kanıt serisinin boşluğu batmaz.

Tarama küçük olabilir — üç madde de meşrudur — ama **sıfır olamaz.** Gerçekten
gündem yoksa bunu yaz: `day_type: sakin` + "tarandı, portföyü ilgilendiren yeni
bir şey yok" notu. Boş dosya ile "baktım, yoktu" kaydı aynı şey değildir.

`references/tahmin-protokolu.md` içindeki kanıt toplama protokolünü izle. Kısaca: portföyün ağırlığı neredeyse arama oraya odaklanır. Bu portföy için ağırlık merkezi altın ve teknoloji, dolayısıyla Fed/reel faiz/DXY, jeopolitik risk primi, Nasdaq/yarı iletken haber akışı, TCMB ve TL tarafı.

Bulduklarını `evidence/YYYY-MM-DD.md` içine serbest metin olarak yaz — bu dosya ileride "hangi tür haber gerçekten fiyatı hareket ettirdi" analizinin ham verisi.

### Sinyal katmanı — ne kullanılır, ne kullanılmaz (13.08.2026)

Dünyaca tanınmış tahmin literatürü tarandı. **Net sonuç: 1 günlük ufukta
yönü öngören sinyal bulunamadı** — bu, dürüstlük çerçevesinin 1. maddesini
çürütmedi, **doğruladı**. Araştırmanın getirisi yön değil **bant** tarafında.

**Bant için (ölçülür, yön için değil):**

| Sinyal | Kaynak | Varlık |
|---|---|---|
| Altın ima oynaklık | FRED `GVZCLS` | `gram_altin`, `KUT` |
| Nasdaq ima oynaklık | FRED `VXNCLS` | `KTJ`, `KIK` |
| VIX vade yapısı | `VIXCLS` ÷ `VXVCLS` | rejim |

Formül ve VRP düzeltmesi: `references/tahmin-protokolu.md`.
**Bugün operatif değil, ölçümde** — IV bantları K25'in bulgusuyla çelişiyor
(bkz. `on-kayit.md` → H10).

**Rejim için (yalnız 1 aylık projeksiyon):**
`BAMLH0A0HYM2` (yüksek getirili spread) · `NFCI` (finansal koşullar) ·
`T10YIE` (başabaş enflasyon) · `T10Y2Y` (eğri eğimi) · `DFF` (carry hesabı).

**Süperforecasting'ten alınan davranışlar (kanıt gücü A):**

1. **Küçük ve sık güncelleme** — en isabetli tahminciler sık, küçük adımlarla
   güncelledi. Açık tahminleri gün içinde revize etmek meşru, **ama
   `superseded` izi korunur.**
2. **Granülerlik korunur** — `p_up`'ı 0,56 diye yaz, 0,55/0,60 diye değil.
   0,05'e yuvarlamak bile ölçülebilir isabet kaybı yaratıyor.
3. **Referans sınıf (outside view) önce gelir** — "son 250 iş gününde bu
   varlığın 1 günlük değişim dağılımı" nedir? İç görü düzeltmesi onun
   **üstüne** yazılır, yerine değil. Brier 0,17 vs 0,26 (Chang ve ark. 2016).
4. **Fermi ayrıştırma** — gram altın tek parça tahmin edilmez;
   `XAUUSD × USDTRY / 31,1035` iki ayrı bacaktır.
5. **Ekstremleştirme YAPILMAZ** — turnuvada işe yaradı ama tekrarlanmadı.

**Eklenmeyecekler:** teknik analiz · analist hedefleri · trend takibi ·
pre-FOMC drift · PEAD · altın/gümüş rasyosu · AAII/put-call · kazanç revizyon
momentumu. Hepsinin belgelenmiş başarısızlığı `tahmin-protokolu.md` → §2b'de.

**Ağırlığı düşürülen:** `us10y_real`. Altın–reel faiz korelasyonu 2022'de
%84'ten %3'e düştü; marjinal alıcı ETF'lerden merkez bankalarına kaydı.
Kanıt ağırlığı `orta` → **`dusuk`**.

### Adım 5 — Tahminleri üret ve kaydet

Her `spot` / `fund_tefas` / `equity` / `crypto` varlık için 1g, 1h, 1a. Format ve kalibrasyon kuralları `references/tahmin-protokolu.md`'de.

**Hedef tarih = varlığın fiyatlandığı ilk gün.** Cuma günü üretilen 1g tahmini **Pazartesi'yi** hedefler, Cumartesi'yi değil; hedef resmî tatile denk gelirse tatil sonrası ilk seansa kayar. `crypto` 7/24 işlem gördüğü için kaydırılmaz. Motor bunu `next_open_day()` ile otomatik yapar.

Kapalı günün snapshot'ı yeni fiyat taşımaz, **önceki günün fiyatını taşır** — böyle bir tahmin garantili %0 değişimle çözülür, bant her zaman tutar, yön hep "yatay" olur. Bu kayıp gözlem değil **kirli** gözlemdir ve rastgele dağılmaz: yalnız Cuma ve tatil öncesi tahminlere çarpar. `calibrate` böyle satırları havuza almaz ve `haric_kapali_gun_hedefi` altında sayar.

Tahmin dosyasının **üst düzeyinde** şunlar da olmalı — eksikse motor uyarır ve o veri bir daha toplanamaz:

| Alan | Değer | Neden |
|---|---|---|
| `day_type` | `veri` · `sakin` · `tatil` · `hafta_sonu` | Veri günü ile sakin günün oynaklığı aynı değil |
| `scheduled_events` | yaklaşan takvimli olaylar | Bandın neden geniş tutulduğunun kaydı |
| `protocol_version` | tamsayı (şu an 1) | Farklı sürümler aynı havuzda toplanmaz |
| `market_state` | `MARKET_STATE_REQUIRED` hepsi | Geriye dönük doldurulamaz |
| `model_id` | tahmini üreten Anthropic modeli, örn. `claude-fable-5-1` | **Zorunlu** — motor reddeder. Farklı modeller aynı havuzda toplanmaz (K78). Motor modeli kendisi bilemez, oturum bildirir |

Her `market_state` değişkenine **`<değişken>_asof` damgası** koy. Taşınan bir değere tarih damgası vurulmazsa bayat veri sessizce güncel görünür — bu hata 04.08'de yakalandı (Nasdaq 4 gün boyunca 31.07 kapanışıydı ama "03.08 kapanışı" diye etiketlenmişti).

```bash
python scripts/pt.py forecast --root <yol> --file tahmin.json
```

### Adım 5b — gölge bant (her 1g tahmininde, K91)

`band_shadow` + `band_shadow_rule` **her 1g satırına** yazılır. Motor eksikse
**uyarır**, `gunluk.sh` sayısını basar — kural 20.08'de kondu ama 28.08–01.09
arası tamamen unutuldu (**6/6 eksik, üç gün**) ve H14'ün havuzu o günleri
**kalıcı** kaybetti: alternatif bandın o günkü değeri geriye dönük üretilemez.

```bash
python3 scripts/vol_uncond.py --json   # ampirik p10/p90, nokta üzerine oturt
```

### Adım 5c — açık `actual`'ları kapat (H4 paydası, K79)

```bash
python scripts/pt.py evidence-acik --root <yol> --date <bugün>
```

`consensus` yazılıp `actual` girilmemiş takvimli kanıtlar. Kapanmayan kayıt
H4'ün paydasına **giremez** ve eksikliği görünmez. Veri gerçekten yoksa
`actual_unavailable` + **gerekçe** yazılır — gerekçesiz kapatma kabul edilmez.

### Adım 5d — savcı (commit öncesi, salt okunur)

`tahmin-savcisi` skill'i günün kaydını adversaryal denetler: kaynaksız sayı,
eşiği dolmamış kural, lehte düzeltme (H9), sonradan genişletilmiş bant, ön
kayıt ihlali. Motor şemayı doğrular, savcı **muhakemeyi**.

### Adım 6 — Raporu yaz

**Bu şablonu kullan.** Kullanıcı yoğun ve tabloyu tarayarak okuyor:

```
## Portföy · <tarih>

**Toplam: X TL** (dün Y TL, %Z)

| Varlık | Değer | Ağırlık | 1g % | 1h % |
|---|---|---|---|---|

### Dünkü tahmin ne oldu
| Varlık | Tahmin | Gerçek | Bantta mı | Yön |
|---|---|---|---|---|
(+ tek cümle: bugün baseline'ı yendik mi, yenmedik mi)

### 1 hafta önce bugün için ne demiştim
### 1 ay önce bugün için ne demiştim
(veri yoksa "henüz yok" yaz, atlama — sistemin yaşı bilgidir)

### Bugünün gündemi
- 3-6 madde, her biri kaynaklı ve hangi varlığı ilgilendirdiği belirtilmiş

### Yarın / 1 hafta / 1 ay
| Varlık | Yatay | 1g | 1h | 1a |
|---|---|---|---|---|
(her hücre: nokta % + [alt, üst] bandı)

### Kalibrasyon (son 30 gün)
Baseline'a karşı (BİRİNCİL): eşleştirilmiş işaret testi p=X (n=Y) → <yenildi / gösterilemedi>
Bant tutma: %X [CI: alt–üst] (hedef %80) · Yön isabeti (teşhis): %X [CI] · Brier: X

### Bu tahmini bozacak şey
- 1-3 madde
```

Rapor sonunda satın alma/satma önerisi **yok**. Kullanıcı isterse bile yok.

---

## Mod 3 — Tek seferlik tahmin (`tahmin`)

Kullanıcı sabah raporu istemeden "sence altın haftaya ne olur" derse: kısa cevap ver, ama tahmini yine de kaydet (`forecast` komutu). Kaydedilmeyen tahmin ölçülemez, ölçülemeyen tahmin sistemi iyileştirmez. Kullanıcıya "kaydettim" diye ayrıca rapor verme, tek satır yeter.

---

## Mod 4 — Kalibrasyon incelemesi (`kalibrasyon`)

Ayda bir, ya da kullanıcı sorduğunda. **Önce `reviews/on-kayit.md`'yi oku** — analiz planı orada sabittir (hangi hipotez, hangi test, hangi minimum n, hangi eşik, raporlama sırası). Sonra `references/kalibrasyon.md` dosyasını oku ve oradaki prosedürü uygula.

```bash
python scripts/pt.py calibrate --root <yol> --window 30
```

Çıktı metrikleri: yön isabeti, MAE, bant kapsama oranı, Brier skoru, sistematik sapma (bias) ve **baseline'a karşı skill skoru**. En önemlisi sonuncusu.

İnceleme sonucunda somut bir değişiklik öner — bant genişliğini ayarla, bir varlık için tahmin üretmeyi bırak, belirli bir haber türüne ağırlık verme. Değişikliği `reviews/YYYY-MM.md`'e yaz ki bir sonraki incelemede "geçen ay ne değiştirmiştik, işe yaradı mı" sorusu cevaplanabilsin. Sistem böyle iyileşir — model daha "akıllı" tahmin ederek değil, neyi tahmin edemeyeceğini öğrenerek.

---

## Referans dosyaları

Hepsini birden okuma, ihtiyaç anında oku:

- `references/veri-kaynaklari.md` — doğrulanmış makine-okunur uç noktalar (FRED/Yahoo/TCMB/LBMA), denenip elenen kaynaklar, kaynak başına değişen User-Agent tuzağı, TEFAS T+1, gram altın baz aralığı, tatil takvimi. **Snapshot alırken oku.**
- `references/tahmin-protokolu.md` — kanıt toplama, ağırlıklandırma, bant genişliği seçimi, varlık sınıfına göre yöntem, tahmin JSON şeması. **Tahmin üretirken oku.**
- `references/kalibrasyon.md` — metrik tanımları, aylık inceleme prosedürü, iyileştirme kararları. **Kalibrasyon modunda oku.**
- `assets/portfoy.ornek.json` — dolu bir portföy örneği.

## Otomasyon

Kullanıcı bunu her sabah otomatik istiyorsa: script tarafı cron'a uygun (`snapshot`, `resolve`, `calibrate` deterministik). Ancak fiyat toplama ve haber tarama Claude gerektirir — tam otomasyon için sunucuda headless bir çalıştırma kurulmalı. Bunu kullanıcı isterse öner, kendiliğinden kurma.
