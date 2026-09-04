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

Kullanıcı sistemi "para kazandıran bir şey" gibi konumlandırmaya başlarsa bunu bir kez, sakin şekilde düzelt: bu bir öğrenme ve disiplin aracı.

## Veri düzeni

Tüm veri tek bir kökte durur (varsayılan `~/portfoy-takip`, kullanıcı başka yer derse orası):

```
portfoy-takip/
  portfolio.json              # varlık tanımları + miktarlar
  snapshots/YYYY-MM-DD.json   # o günün fiyatları ve portföy değeri
  forecasts/YYYY-MM-DD.json   # o gün üretilen tahminler + kanıtlar
  resolutions.jsonl           # çözümlenmiş tahmin sonuçları (append-only)
  evidence/YYYY-MM-DD.md      # o günün dünya gündemi notu (serbest metin)
  reviews/YYYY-MM.md          # aylık kalibrasyon değerlendirmesi
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

### Adım 2 — Güncel fiyatları topla (web search)

`references/veri-kaynaklari.md` dosyasını oku; kaynaklar, TEFAS'ın T+1 tuzağı ve arama kalıpları orada. Her varlık için fiyat çek. Bulamadığın fiyatı **uydurma**, `null` bırak.

```bash
python scripts/pt.py snapshot --root <yol> --date <bugün> --prices '{"gram_altin": 6187.5, ...}'
```

### Adım 3 — Dünkü/geçen haftaki/geçen ayki tahminleri çözümle (script)

```bash
python scripts/pt.py resolve --root <yol> --date <bugün>
```

Snapshot yazıldıktan sonra çalıştır. Vadesi gelen tüm tahminleri gerçekleşenle eşleştirir, `resolutions.jsonl`'a yazar. Snapshot yoksa (hafta sonu, tatil, TEFAS gecikmesi) `pending` bırakır ve bir sonraki iş gününde tekrar dener — bunu hata sanma.

### Adım 4 — Dünya gündemini tara (web search)

`references/tahmin-protokolu.md` içindeki kanıt toplama protokolünü izle. Kısaca: portföyün ağırlığı neredeyse arama oraya odaklanır. Bu portföy için ağırlık merkezi altın ve teknoloji, dolayısıyla Fed/reel faiz/DXY, jeopolitik risk primi, Nasdaq/yarı iletken haber akışı, TCMB ve TL tarafı.

Bulduklarını `evidence/YYYY-MM-DD.md` içine serbest metin olarak yaz — bu dosya ileride "hangi tür haber gerçekten fiyatı hareket ettirdi" analizinin ham verisi.

### Adım 5 — Tahminleri üret ve kaydet

Her `spot` / `fund_tefas` / `equity` / `crypto` varlık için 1g, 1h, 1a. Format ve kalibrasyon kuralları `references/tahmin-protokolu.md`'de.

```bash
python scripts/pt.py forecast --root <yol> --file tahmin.json
```

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
Yön isabeti: %X (n=Y) · Bant tutma: %X (hedef %80) · Baseline'a karşı: <daha iyi/daha kötü/fark yok>

### Bu tahmini bozacak şey
- 1-3 madde
```

Rapor sonunda satın alma/satma önerisi **yok**. Kullanıcı isterse bile yok.

---

## Mod 3 — Tek seferlik tahmin (`tahmin`)

Kullanıcı sabah raporu istemeden "sence altın haftaya ne olur" derse: kısa cevap ver, ama tahmini yine de kaydet (`forecast` komutu). Kaydedilmeyen tahmin ölçülemez, ölçülemeyen tahmin sistemi iyileştirmez. Kullanıcıya "kaydettim" diye ayrıca rapor verme, tek satır yeter.

---

## Mod 4 — Kalibrasyon incelemesi (`kalibrasyon`)

Ayda bir, ya da kullanıcı sorduğunda. `references/kalibrasyon.md` dosyasını oku ve oradaki prosedürü uygula.

```bash
python scripts/pt.py calibrate --root <yol> --window 30
```

Çıktı metrikleri: yön isabeti, MAE, bant kapsama oranı, Brier skoru, sistematik sapma (bias) ve **baseline'a karşı skill skoru**. En önemlisi sonuncusu.

İnceleme sonucunda somut bir değişiklik öner — bant genişliğini ayarla, bir varlık için tahmin üretmeyi bırak, belirli bir haber türüne ağırlık verme. Değişikliği `reviews/YYYY-MM.md`'e yaz ki bir sonraki incelemede "geçen ay ne değiştirmiştik, işe yaradı mı" sorusu cevaplanabilsin. Sistem böyle iyileşir — model daha "akıllı" tahmin ederek değil, neyi tahmin edemeyeceğini öğrenerek.

---

## Referans dosyaları

Hepsini birden okuma, ihtiyaç anında oku:

- `references/veri-kaynaklari.md` — TEFAS/gram altın/kur fiyat kaynakları, arama kalıpları, T+1 ve tatil takvimi tuzakları. **Snapshot alırken oku.**
- `references/tahmin-protokolu.md` — kanıt toplama, ağırlıklandırma, bant genişliği seçimi, varlık sınıfına göre yöntem, tahmin JSON şeması. **Tahmin üretirken oku.**
- `references/kalibrasyon.md` — metrik tanımları, aylık inceleme prosedürü, iyileştirme kararları. **Kalibrasyon modunda oku.**
- `assets/portfoy.ornek.json` — dolu bir portföy örneği.

## Otomasyon

Kullanıcı bunu her sabah otomatik istiyorsa: script tarafı cron'a uygun (`snapshot`, `resolve`, `calibrate` deterministik). Ancak fiyat toplama ve haber tarama Claude gerektirir — tam otomasyon için sunucuda headless bir çalıştırma kurulmalı. Bunu kullanıcı isterse öner, kendiliğinden kurma.
