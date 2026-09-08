# Kontrol listesi — sekiz başlık

Sırayla geç. Her başlıkta ya bulgu yaz ya "temiz" işaretle; **atlama**.

## 1. Kaynaksız veya tarihsiz sayı

`forecasts/<gün>.json` → `evidence[*]`:
- `claim` içinde sayı var ama `source`/`url` yok → **ağır**
- `source` var ama sayının **hangi güne ait olduğu** yazmıyor → **ağır**
- `market_state` alanı var ama `<alan>_asof` damgası yok → **ağır**
  - **Damga GRUP düzeyinde olabilir** — yanlış alarm vermeden önce bunu kontrol et:
    `gram_altin_alis`/`gram_altin_satis` için damga `gram_altin_asof`,
    `usdtry_tcmb_alis`/`_satis`/`_mid` için `usdtry_tcmb_asof`,
    `usdtry_serbest_alis`/`_satis` için `usdtry_serbest_asof`.
    Doğru kontrol: alan adından son eki (`_alis`/`_satis`/`_mid`) atıp
    `<grup>_asof`'a da bak; ikisi de yoksa bulgu. (05.09.2026'da naif kontrol
    yedi alan için yanlış alarm verdi; yanlış alarma alışan denetim gerçek
    alarmı da görmezden gelir — K40.)
  - `_asof` değeri `KASTEN NULL - <gerekçe>` biçimindeyse **bulgu değildir**;
    boşluğun adıyla kaydedilmesi K80'in istediği davranıştır.
- Üçüncü taraf bir site TEFAS/FRED/TCMB ile çelişirken tercih edilmiş → **ağır**

> Kanıt: 03.09'da arama motorunun verdiği AA linki **2024** tarihliydi ve
> tamamen farklı bir TÜFE taşıyordu. Link açılmasaydı deftere girecekti.
> K11 (US10Y 40bp), K18 (Nasdaq 4 gün bayat), K19 (BIST 675 puan),
> K72 (GC=F bar revizyonu) aynı aile.

## 2. Eşiği dolmamış bir kuralın uygulanması

`rationale` / `invalidator` metinlerinde bir düzeltme terimi, katsayı ya da
"bu yüzden şu yönde ayarladım" ifadesi arıyorsun. Sonra ön kayda bak:

| Kural | Eşik | Nerede |
|---|---|---|
| K73 büyük artık sonrası ters düzeltme | n ≥ 12 | `2026-09.md` → K73 |
| Bant kuralı v5'e geçiş | n ≥ 100 **ve** ikinci rejim | `on-kayit.md` → H14-b |
| Kovaryat regresyonunun baseline olması | n ≥ 200 + bilgi kümesi denetimi | H17 |
| KIK beta yeniden kestirimi | n ≥ 20 | H18-a |
| Look-through zinciri tercihi | 20 ayırt edici gün | H18-b |

Eşik dolmadan uygulanmışsa **ağır**. Eşik dolmadığı **yazılıysa** ve
uygulanmamışsa temiz — bu doğru davranış.

## 2b. Anomali ilan edilmiş ama yüzdeliği hesaplanmamış (K43)

Bugünün kanıtlarında/gerekçelerinde bir sapma "keskin ayrışma", "anomali",
"açıklanamıyor", "olağandışı" diye geçiyor mu? Geçiyorsa **yüzdeliği yazılı
mı?**

- Yüzdelik yok → **ağır**. Kural: sapma anomali sayılmadan önce aynı varlığın
  **tarihsel sapma dağılımındaki yüzdeliği** hesaplanır; **üst %10'un
  dışındaysa kayıt açılmaz.**
- Yüzdelik var ve üst %10 dışında ama yine de kayıt açılmış → **ağır**.
- Sapma tahmin gerekçesine (bant genişletme, güven düşürme) geçirilmiş ama
  yüzdelik yok → **ağır**, çünkü gürültü tahmine sızmış olur.

> Kanıt: 14.08'de KIK'in KTJ'den "keskin ayrıştığı" kaydedildi ve **iki gün**
> tahmin gerekçesi olarak kullanıldı. Ölçüldüğünde z=−0,84, **246 günün
> 87.'si = üst %35** — ortalama her üç günde bir görülen bir sapma. Kesin
> kanıt: bir **önceki** gün daha büyük artık üretmişti (+0,74 pp) ve
> işaretlenmemişti. İşaretleten şey sinyal değil **sapmanın yönüydü**.

## 3. Lehte düzeltme (H9)

Bugün bir model, bant, adet veya baz düzeltildi mi? Düzeltme skoru **iyileştiriyorsa**:
- Gerekçe, sonucu görmeden mi yazıldı? Yazılı mı?
- `hata_gunlugu.csv` → `skor_etkisi` alanı dolduruldu mu?

Gerekçe sonradan yazılmışsa **ağır**. H9'un anlamlı çıkması kötü haberdir:
düzeltme kararının sonuca bakılarak verildiği anlamına gelir.

## 4. Sonradan genişletilmiş bant

Bugünün bandını dünün bandıyla ve o varlığın son artığıyla karşılaştır.
Bant, **bugünün artığı görüldükten sonra** o artığı kapsayacak şekilde
genişletilmiş görünüyorsa **ağır** — kapsama oranı sahte iyileşir.

Meşru genişletme: ima oynaklık yükseldi (`gvz`/`vxn` sayısıyla gösterilmiş),
takvimli olay girdi (`scheduled_events`), rejim değişti. **Gerekçe sayı
taşımıyorsa** meşru sayılmaz.

## 5. `day_type` doğru mu

`veri` = o gün takvimi **önceden belli**, sayısal, fiyat hareket ettiren bir
açıklama var. Sonradan çıkan haber `veri` yapmaz. `scheduled_events` ile
tutarlı mı? Değilse **orta**.

Veri günü ile sakin günün oynaklığı aynı değil; yanlış etiket hem bandı hem
yön isabetini bulanıklaştırır.

## 6. Ön kayıt ihlali

Raporda/anlatıda bir **sonuç** iddiası var mı? `on-kayit.md`'de o test yazılı
mı? Yazılı değilse `keşifsel` etiketi taşıyor mu?

- Etiketsiz keşifsel bulgu → **ağır**
- Alt küme seçilerek elde edilmiş bir sayı ("hafta sonları hariç") → **ağır**
- Başlık sayı olarak yön isabeti kullanılmış → **orta** (birincil metrik
  eşleştirilmiş işaret testi; `p_up` için BSS)

## 7. Sessizce kaybolan alan

- `market_state` alan sayısı düne göre **düştü** mü? → **ağır**
- Tahmin sayısı, kanıt sayısı beklenenden az mı?
- Kanıt **ikilendi** mi (aynı `id` iki kez, K52)?
- `model_id` her tahmin kaleminde var mı, bugünün gerçek modeli mi (K78)?
- Dosya düzeyinde tanınmayan alan uyarısı çıktı mı (#26)?

## 8. Açık `actual` (H4 paydası)

```bash
python3 scripts/pt.py --root data evidence-acik --date <gün>
```

- `olay_tarihi_gecmis > 0` → **orta** (geciktikçe kaynak bulmak zorlaşır)
- `tutarsizlik.ayni_gosterge_farkli_actual` boş değil → **ağır**, aynı olay
  iki farklı değerle kapanmış olabilir
- `event_date_yok` boş değil → **not**, tekilleştirme yapılamıyor
- `actual_unavailable` var ama gerekçesi yok → **ağır**

## Bulgu YOKSA

"Sekiz başlık denetlendi, bulgu yok" yaz ve bitir. Uydurma.
