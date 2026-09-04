---
name: yeme-icme
description: ComeSyria'ya yeme içme mekanı ekler — Google Maps yorumlarını API'siz okuyup süzer, turist tuzağını ve sahte yorumu eler, yalnızca hak edeni üç dilde yayımlar. "yeme içme ekle", "restoran ekle", "lokanta", "kahve", "nerede yenir", "yemek mekanı", "Şam'da ne yenir", "yeme içme içeriği" dendiğinde kullan.
---

# Yeme içme mekanı ekleme

Yeme içme kayıtları **`food` tipinde** yazılır — `place` değil. Yemek sitede
ayrı bir bölüm; mekanlar sayfasının altındaki bir filtre değil. Dosya
`content/food/` altına, **Türkçe slug adıyla** konur. Üretim akışının tamamı
`icerik-uret` becerisiyle aynı — bu beceri yalnızca **hangi yerin ekleneceğine**
karar veren süzgeci getiriyor.

> Tipi karıştırmak sessiz bir hata: kayıt yayımlanır, uyarı çıkmaz, ama GA4'te
> `type="place"` görünür ve ayrı bölümün varlık sebebi olan ayrım bozulur.

> **Google Places API anahtarı yok.** Yorumlar tarayıcıdan elle okunuyor.
> Yöntem bu kısıta göre tasarlandı; anahtar eklenirse otomatikleşir ama
> **eşikler ve editoryal ölçüt aynı kalır.**

## İki yol: mekan ya da sofra

Bir yeme içme kaydı sayfayı iki ayrı yoldan hak edebilir. **İkisi de geçerli**,
ama ikisinin de bir eşiği var.

### Yol 1 — Mekan

Yer, yemekten bağımsız olarak bir şey anlatıyor:

- **Kurum olmuş yerler.** 1885'ten beri aynı çarşıda dondurma döven bir dükkân
  bir adres değil, bir kurum.
- **Deneyimin kendisi olan yerler.** Emevî Camii'nin karşısındaki kahvede
  hikâye anlatıcısı varsa, oraya kahve için gidilmiyor.
- **Zanaatın görüldüğü yerler.** Üretim önünde yapılıyorsa okur bir şey
  öğreniyor.
- **Bir yemeğin kaynağı olan yerler.** Şehir o yemekle anılıyorsa ve yer o
  yemeğin adresiyse.

### Yol 2 — Sofra

**Yemeği iyi diye de girilir.** Anıt olması gerekmiyor; okurun asıl sorusu çoğu
zaman "bu akşam nerede yerim". Ama sayfa bunu **somutlukla** hak etmeli:

| Zorunlu | Neden |
| --- | --- |
| `signature` — adıyla bir yemek | "Bol çeşit" bir bilgi değil |
| `price_range` — kişi başı aralık | Okurun ilk sorusu |
| `opening_hours` | Kapalı kapıya göndermemek için |
| Gövdede **en az bir ayırt edici ayrıntı** | Yan kapıdaki lokantadan farkı ne |

Son satır belirleyici. "Fettuşu ekmeği kuzu yağında kızartarak yapıyorlar" bir
ayrıntıdır; "yemekleri çok lezzetli" değildir. O ayrıntı yoksa kayıt yazılmaz —
çünkü yazılacak bir şey yok demektir, yer kötü olduğu için değil.

### Yine de kabul edilmeyenler

- **Alkol servisi olan yer.** Pazarlıksız ve ilk bakılan şey: menüde içki
  listesi, masada şişe, "bar" ya da "rooftop lounge" tanımı varsa aday elenir.
  Yemeği ne kadar iyi olursa olsun. Sayfanın varlığı zaten bir öneri olduğu
  için "alkolden söz etmemek" yetmiyor — yer listeye hiç girmiyor. Emin
  olamıyorsan alma. (Bkz. CLAUDE.md §7.)
- **Zincir ve otel restoranı.**
- **Menüsü her şeyi kapsayan yer.** Suriye mutfağı + pizza + burger: hiçbirinde
  iddiası yok. Bu bir kalite yargısı değil, turist tuzağı işareti.
- **Fiyatı ya da saati doğrulanamayan yer.** Künye ızgarası boş kalıyorsa kayıt
  sitenin en güçlü yanını kullanamıyor.
- **Hakkında yazacak tek cümlesi olmayan yer.** Bkz. yukarıdaki son satır.

## Suriye'ye özgü: asıl soru "iyi mi" değil

Genel rehberler "kaliteli mi" diye sorar. Suriye'de **ilk soru başkadır:**

> **Hâlâ açık mı, ve hakkında yazılan hâlâ doğru mu?**

2019 tarihli parlak bir yorum bugün kapalı bir kapıyı anlatıyor olabilir.
Onarım, taşınma ve el değiştirme yaygın. Bu yüzden doğrulamada **tazelik,
puandan önce gelir.**

Ayrıca: Suriye'de yorum hacmi turistik başkentlerin çok altında. "300–800 yorum"
gibi genel eşikler burada hiçbir yeri geçirmez. Kalibrasyon
`references/dogrulama.md` içinde.

## Akış

### 1. Aday belirle

`content/kuyruk.json` içindeki `tip: "food"` maddelerinden ya da
`references/adaylar.md` listesinden. **Kendi başına aday uydurma** — var
olmayan bir lokanta yazmak bu sitenin yapabileceği en zararlı şey.

### 2. Doğrula — üç kapı

Üçünü de geçmeyen aday **elenir**, "belki" diye yazılmaz.

Üçünden önce bir eleme var: **alkol servisi olan yer hiç kapıya gelmiyor**
(bkz. "Yine de kabul edilmeyenler"). Menüye ve fotoğraflara adayı doğrulamaya
başlamadan önce bak; sonra elemek harcanmış emek demek.

| Kapı | Soru |
| --- | --- |
| **Varlık** | Son 12 ayda yazılmış, açık olduğunu gösteren en az iki bağımsız iz var mı? |
| **Gerekçe** | Hangi yoldan giriyor? Mekan yolundaysa kurum/deneyim/zanaat gerekçesi nedir; sofra yolundaysa yan kapıdaki lokantadan farkı nedir? |
| **Somutluk** | Ne yenir, ne kadar tutar, ne zaman açık — üçü de yazılabiliyor mu? |

Yöntemin tamamı: `references/dogrulama.md`.

### 3. Yaz

`icerik-uret` becerisinin kurallarıyla, üç dilde. Yeme içme kaydına özgü
alanlar:

| Alan | Not |
| --- | --- |
| `kind` | **`restaurant` / `cafe` / `bakery` / `icecream` / `sweets`.** `food` diye bir değer yok. Bu alan JSON-LD alt tipini belirliyor: `cafe` → `CafeOrCoffeeShop`, `bakery` → `Bakery`, `icecream` ve `sweets` → `IceCreamShop`, gerisi `Restaurant`. |
| `signature` | **Ne yenir.** Adıyla: "Dövme booza, fıstıklı". "Bol çeşit" değil. |
| `price_range` | Kişi başı somut aralık. Bilinmiyorsa "Değişken — sorup öğren". |
| `opening_hours` | Yeme içmede en çok değişen alan; kaynağın tarihini not et. |
| `entry_fee` | **Boş bırak.** Lokantada giriş ücreti yok. |
| `duration` | Oturma süresi — kahve 30 dk, mezeli akşam yemeği 120 dk. |

Mutfak sözlüğü ve üç dilde yemek adları: `references/mutfak.md`.

### 4. Denetle ve yayımla

`icerik-uret` ile aynı: `denetle.mjs` üç dilde temiz olmadan yayımlama, sonra
`git push` ve sunucuda `./deploy.sh --content`.

## Ton

Yeme içme yazısı klişeye en açık tür. Marka sesi burada da geçerli ve daha da
katı:

> ✗ Şam'ın en iyi dondurmacısı, mutlaka denenmeli, unutulmaz bir lezzet
> ✓ 1885'ten beri aynı çarşıda. Booza tahta tokmaklarla dövülüyor ve önünde
>   duruyorsun; sıra akşamüstü kapıya taşıyor.

**Övme, göster.** Bir yerin iyi olduğunu söylemek yerine neden öyle olduğunu
yaz: kaç yıldır orada, ne yapılıyor, hangi saatte kalabalık.

## Sık yapılan hatalar

- **Puan yazmak.** Google puanı sayfaya basılmaz — hem şartlar kısıtlıyor hem
  de birkaç ayda eskiyor.
- **Yorum alıntılamak.** Yorum girdidir, içerik değildir (bkz. `google.md`).
- **"En iyi" listesi yapmak.** Bu site sıralama yapmıyor; her kayıt kendi
  başına duruyor.
- **Ayırt edici ayrıntı olmadan yazmak.** Sofra yolundan giren bir kayıt,
  yan kapıdaki lokantadan farkını söylemek zorunda.
- **`entry_fee` doldurmak.** Yeme içmede o alan boş kalır, `price_range` kullanılır.
- **Kuyrukta olmayan yer üretmek.** Aday uydurmak yasak.
