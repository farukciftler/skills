---
name: icerik-strateji
description: ComeSyria'da sıradaki içeriğin ne olacağına karar verir — envanteri tarayıp ölü hub, eksik alan ve zayıf kümeleri sıralar, GA4 verisinden üretim listesi çıkarır, derinlik/genişlik dengesini kurar. "ne ekleyelim", "içerik planı", "sıradaki içerik", "içerik stratejisi", "hangi şehri ekleyelim", "içerik takvimi", "eksikleri göster", "envanter", "içerik boşlukları" dendiğinde kullan.
---

# ComeSyria içerik stratejisi

Bu beceri **ne üretileceğine** karar verir. Nasıl üretileceği ayrı bir işin
konusu — onun için `icerik-uret`.

İkisini karıştırmak en pahalı hata: iyi yazılmış ama yanlış sıradaki bir kayıt,
kötü yazılmış doğru kayıttan daha az iş görüyor.

## Tek cümlelik doktrin

**Derinlik önce, genişlik sonra.** Üç şehir ve her birinde altı mekan, dokuz
şehir ve her birinde iki mekandan kesinlikle daha iyi bir site.

Sebebi hub & spoke kurgusunun kendisinde: şehir sayfası mekanlara dağıtmak için
var. Bir mekanı olan şehir dağıtacak bir şeyi olmayan bir dağıtım noktası —
yani **ölü hub**. Ve ölü hub, o şehrin hiç olmamasından daha kötü:

- Okura verilen söz tutulmuyor: "Bu şehirde" başlığı altında bir satır.
- Arama motoru için ince sayfa; üstelik tarama bütçesi harcıyor.
- Dil değiştirici üç dilde de aynı boşluğu gösteriyor.

## Çalışan küme

Bir şehrin "açıldı" sayılması için asgari:

```
1 şehir  +  3 mekan  +  1 rota
```

Altındaysa o şehir henüz yayında değil, yolda demektir. **Bu asgariye ulaşmadan
yeni şehir açma.**

Üçün nedeni: şehir sayfasındaki mekan ızgarası üç sütun. İki kayıt ızgarayı
yarım bırakıyor, üç kayıt bir satır tamamlıyor. Rota ise mekanları birbirine
bağlayan tek şey; rotasız bir küme, birbirine bakmayan sayfalar yığını.

## Önce envanteri çalıştır

Tahmin etme, ölç:

```bash
node .claude/skills/icerik-strateji/scripts/envanter.mjs
```

Çıktı öncelik sırasına dizilmiş bir eylem listesi. Kaynak `content/` dizini,
yani sunucuya hiç gitmiyor ve saniyeler sürüyor.

`--json` ile makine okunur çıktı verir; `--sehir <slug>` tek bir kümeye odaklanır.

## Öncelik sırası

Envanter betiği bu sırayı uyguluyor. Elle karar verirken de bu sıra geçerli:

| # | Bulgu | Neden en üstte |
| --- | --- | --- |
| 0 | **Yetim mekan** (şehri yok) | Hiçbir şehir sayfasında görünmüyor; üretilmiş ama görünmez |
| 1 | **Ölü hub** (şehir, 2'den az mekan) | Verilen söz tutulmuyor, sayfa ince |
| 2 | **Rota, 3 duraktan az** | Rota sayfası iskeletsiz; şema bile çizilmiyor |
| 3 | **Boş `entry_fee` / `opening_hours`** | Mekan aramalarının birebir cevabı bu alanlar |
| 4 | **Koordinat yok** | `GeoCoordinates` düşüyor, zengin sonuç kartı çıkmıyor |
| 5 | **Zayıf küme** (2 mekan) | Bir kayıt daha ile sağlıklıya dönüyor — en ucuz kazanç |
| 6 | **Kapak görseli yok** | Kart tipografiye düşüyor; kötü değil ama zayıf |

**P6 kapatmanın iki yolu var.** Doğrulanmış görsel bulup bağlamak, ya da
aranıp bulunamadığını kayda yazmak: gerekçeli bir `gorselsiz` alanı o kaydı
listeden düşürür. Yanlış fotoğraf fotoğrafsızdan kötü olduğu için
"arandı, doğrulanamadı" geçerli bir sonuç — ama **gerekçe zorunlu**, yoksa
unutulmuş kayıtla bilinçli karar birbirinden ayırt edilemez.

**P0 dosya adı uyuşmazlığı** ayrı bir tuzak: dosya adı Türkçe slug ile
eşleşmiyorsa bir sonraki `--export` aynı kayıt için ikinci bir dosya üretir
ve biri kapak görselli, öbürü görselsiz kalır.

**Kural:** üstteki madde açıkken alttakine geçme. Yeni bir şehir açmak bu
listede hiç yok — çünkü liste boşalana kadar sırası gelmiyor.

## Yeni şehir ne zaman açılır

Üç koşul birden:

1. Mevcut şehirlerin **hepsi** çalışan küme eşiğinde (3 mekan + 1 rota).
2. Yeni şehir için **en az üç mekan** hakkında somut bilgin var — ziyaret saati,
   giriş, koordinat düzeyinde. Yoksa açtığın şey bir ölü hub.
3. O şehri bir rotayla mevcut kümeye bağlayabiliyorsun. Bağsız şehir adadır.

Üçünü de karşılamıyorsan **derinleş**: var olan şehirlerden birine mekan ekle.

## Veri üretim listesini veriyor

Site GA4 olayları gönderiyor ve üçü doğrudan "ne üret" sorusunu yanıtlıyor.
Ayrıntı: `references/veri.md`.

| Sinyal | Ne söyler |
| --- | --- |
| `search` + `result_count = 0` | İnsanların arayıp bulamadığı şey. **En ucuz içerik fikri.** |
| `not_found` | Var sandıkları adres |
| `content_click` az olan hub | Şehir sayfası dağıtmıyor: ya mekan yok ya kartlar zayıf |
| `read_progress` %25'te düşüyor | Giriş tutmuyor; yeni kayıt değil, mevcudu düzelt |

## Ne üretilmemeli

- **İnce varyant.** "Halep gezilecek yerler" ve "Halep'te ne yapılır" ayrı iki
  sayfa değil; aynı arama niyeti, tek sayfa. İkiye bölmek ikisini de zayıflatıyor.
- **Hakkında somut bilgin olmayan yer.** Ziyaret saati, giriş, koordinat
  bilinmiyorsa kayıt künye ızgarasını dolduramıyor — sitenin en güçlü yanı orası.
- **Hikâye/haber.** O tip siteden kaldırıldı.
- **Sırf sayı için mekan.** Bir rotayı üç durağa çıkarmak için uydurma durak
  eklemek, rotayı da mekanı da bozuyor. Gerçekten o güzergâhta olan yeri ekle.

## Tazelik

Üretim kadar önemli ve tamamen unutulan iş: fiyat ve ziyaret saati en hızlı
eskiyen veri. `references/tazelik.md` hangi alanın ne sıklıkla doğrulanacağını
ve nasıl işaretleneceğini anlatıyor.

## Kuyruk boşaldığında

Envanter temiz + kuyruk boş = üretim duruyor. Doğru tepki konu uydurmak değil,
**adayı doğrulayıp onaya hazırlamak**: `references/aday-havuzu.md` varlık/konum
kapısını geçmiş adayları ve her birinin durumunu taşıyor.

Aday kapısı **tek**: varlık ve konum. Saat/ücret kuyruk kapısı değil, yazım
anında doldurulan alan — `envanter.mjs:266` boş alanı bulgu sayıyor, dürüst
yer tutucuyu değil. Havuza yeni bir kapı eklemeden önce eşiği yayımlanmış
külliyata karşı ölç; çoğu kayıt geçmiyorsa o eşik yanlıştır.

Kuyruğa yazmak ayrı bir karar. Kuyruk, otomatik üretimin konu uydurmasını
engelleyen kapı — **otomatik tur kendi kapısını kendi doldurmaz.**

## Akış

```
1. envanter.mjs çalıştır
2. En üstteki bulguyu al
3. Yeni kayıt gerekiyorsa  →  icerik-uret
   Mevcut kayıt eksikse    →  content/ altında düzelt
4. git push  →  sunucuda ./deploy.sh --content
5. envanter.mjs tekrar: bulgu kapandı mı
```
