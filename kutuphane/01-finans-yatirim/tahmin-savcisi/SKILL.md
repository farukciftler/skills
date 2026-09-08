---
name: tahmin-savcisi
description: Bir günün tahmin ve kanıt kayıtlarını, commit edilmeden önce ADVERSARYAL olarak denetler - kaynaksız/tarihsiz sayı, eşiği dolmamış bir kuralın uygulanması, sonucu görüp lehte yapılmış düzeltme (H9), artık görüldükten sonra genişletilmiş bant, yanlış day_type, model_id eksikliği, ön kayıt ihlali. Kullanıcı "savcı", "denetle", "bugünkü tahmini kontrol et", "commit öncesi bak", "ön kayda uygun mu", "kendimi kandırıyor muyum" dediğinde ya da günlük akışın 7. adımında commit'ten önce çalıştır. SALT OKUNUR - hiçbir dosyayı değiştirmez, tahmin üretmez, yalnızca bulgu listeler.
---

# Tahmin Savcısı

Bu skill deponun **tek denetimsiz katmanını** denetler.

Motor şemayı doğruluyor: `day_type` geçerli mi, `market_state` tam mı,
`model_id` var mı, nokta bandın içinde mi. Doğrulamadığı şey **muhakeme**:
bir sayının kaynağı var mı, bir kural eşiği dolmadan mı uygulandı, bir
düzeltme sonucu görüldükten sonra mı yapıldı.

03.09.2026'da bu üç şey aynı gün içinde üç kez yalnız **hatırlamayla** doğru
yapıldı (AA'nın 2024 tarihli linki, K73'ün n<12 eşiği, ZPE'nin yüzdeliği).
Deponun kendi doktrini bunu reddediyor: *"bir hatayı hatırlamaya bağlayan
kural, aynı hatayı yapacak olanın onu hatırlamasını gerektirir"* (K53).

## Sert kurallar

1. **SALT OKUNUR.** Hiçbir dosyayı değiştirme, hiçbir komutu `forecast` /
   `snapshot` / `resolve` ile çağırma. Bulgu üret, düzeltmeyi kullanıcıya
   ve ana akışa bırak.
2. **Tahmin üretme, yorumlama.** "Bence altın düşer" demek bu skill'in işi
   değil. Soru "bu tahmin doğru mu" değil, **"bu tahmin dürüst kaydedilmiş
   mi"**.
3. **Bulgu yoksa "temiz" de.** Her gün bulgu üretmek zorunda değilsin;
   uyduran bir denetim, denetimsizlikten kötüdür (yanlış alarma alışılır — K40).
4. **Her bulguya kanıt.** Dosya, alan, satır. "Gerekçe zayıf görünüyor" bir
   bulgu değil; "e5'in `claim`'i kaynak taşımıyor" bulgudur.

## Girdi

```bash
DATE=${1:-$(date +%F)}
cat data/forecasts/$DATE.json
cat data/evidence/$DATE.md
python3 scripts/pt.py --root data evidence-acik --date $DATE
git diff --cached --stat; git diff --stat
```

Ön kaydı **her seferinde** oku: `data/reviews/on-kayit.md`. Eşikler orada,
hafızada değil. Son ayın K kayıtları: `data/reviews/YYYY-MM.md`.

## Denetim listesi

`references/kontrol-listesi.md` tam hâli. Dokuz başlık:

| # | Ne aranır | Neden |
|---|---|---|
| 1 | **Kaynaksız/tarihsiz sayı** | K11/K18/K19 ailesi; bu deponun en verimli hata kaynağı |
| 2 | **Eşiği dolmamış kural** | K73 n≥12, H14-b n≥100+rejim, H17 n≥200, H18 n≥20 |
| 2b | **Anomali ilan edildi, yüzdeliği yok** | K43: üst %10 dışındaysa gürültüdür |
| 3 | **Lehte düzeltme (H9)** | Anlamlı sonuç KÖTÜ haberdir |
| 4 | **Sonradan genişletilmiş bant** | Artık görüldükten sonra bant oynatmak kapsamayı sahte iyileştirir |
| 5 | **`day_type` gerçekten takvimli mi** | Sonradan çıkan haber `veri` yapmaz |
| 6 | **Ön kayıt ihlali** | Planda yazmayan bulgu `keşifsel` etiketi taşımalı |
| 7 | **Sessizce kaybolan alan** | K49/K52/K53/K78 ailesi; alan sayısı düştü mü |
| 8 | **Açık `actual`** | H4'ün paydası (K79) |

## Çıktı biçimi

```
## Savcı · <tarih>

**Bulgu: N** (ağır: A · orta: B · not: C)

### AĞIR — <başlık>
`dosya:alan` · <bir cümle: ne yanlış>
Neden ağır: <hangi hipotezi/metriği kirletir>
Öneri: <somut düzeltme>

### ORTA — ...
### NOT — ...

### Temiz geçen başlıklar
1,4,5,7  (denetlendi, bulgu yok)
```

**Ağırlık ölçütü:** ölçümü kirletiyorsa **ağır**; anlatıyı kirletiyorsa
**orta**; ileride sorun olabilirse **not**.

Sonunda tek satır: **"Bu bir denetimdir, tahmin değildir."**
