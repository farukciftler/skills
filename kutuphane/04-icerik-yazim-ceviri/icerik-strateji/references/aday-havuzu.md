# Aday havuzu

Kuyruk boşaldığında sıfırdan başlamamak için. Buradaki her madde **varlık ve
konum kapısını geçmiş**, ama kuyruğa girmesi için ikinci kapı gerekiyor.

## Tek kapı

| Kapı | Ne gerekir | Nereden |
| --- | --- | --- |
| 1 — Varlık ve konum | Üç bağımsız kaynak ~50 m içinde örtüşür (alansal kayıtta gevşek) | Wikidata `P625`, Nominatim, Overpass |

Mekan adayı için kapı bu kadar. **Saat ve ücret kuyruk kapısı değil, yazım
anında doldurulan alanlardır.**

### Düzeltme (2026-08-20): "Kapı 2 — Somutluk" diye bir kapı yok

Bu dosyanın 2026-08-19 sürümü ikinci bir kapı tanımlıyordu: "OSM'de
`opening_hours` ve `fee` etiketi yoksa kuyruğa yazma." O kural **yanlıştı** ve
dört doğrulanmış adayı süresiz bloke ediyordu. Üç ayrı yerden çürüdü:

| İddia | Gerçek |
| --- | --- |
| "envanterde P3 olarak anında geri geliyor" | `envanter.mjs:266` P3'ü yalnızca alan **boşken** ateşliyor — ve çaresi olarak tam olarak `"Değişken — girişte teyit et"` dizesini **öneriyor**. Dolu alan bulgu üretmiyor. |
| "'Değişken' yazmak kaçamak" | CLAUDE.md §7 ve `icerik-uret/references/mekan.md:51` bu dizeyi **dürüst seçenek** diye adlandırıyor: "Bilinmiyorsa uydurma." |
| "somutluk olmadan kayıt yazılamaz" | Yayındaki 28 mekanın **12'si** `entry_fee`'de tam bu dizeyi taşıyor — Krak des Chevaliers, Tedmür kalıntıları, Ugarit, Azm Sarayı dâhil. |

`opening_hours`'ta tablo daha da net: 28 kaydın yalnızca **4'ü** saat rakamı
taşıyor (Emevî, Hamidiye, Krak, Medine Çarşısı). Geri kalan 24'ü nitel yazıyor
— "Gündüz saatleri, namaz vakitleri dışında", "Açık alan, gün boyu",
"Gündüz saatleri — durum değişebilir, teyit et". Yani kapı 2, **kendi
külliyatımızın karşılamadığı** bir eşikti.

Üstelik kapanamazdı: Suriye anıtlarının ziyaret saati hiçbir yerde
yayımlanmıyor. Kapı olarak bırakılırsa tur her seferinde "kuyruk boş" deyip
duruyor — 2026-08-19 ve 08-20 turlarında aynen bu oldu.

### Beyt Cebri emsali neden buraya geçmiyor

`yeme-icme/references/adaylar.md` gerçekten "'Değişken — sorup öğren' yazıp
geçmek burada **kaçamak olurdu**" diyor — ama **yemek** kaydı için, ve
gerekçesi türe özgü: `price_range` sofra yolunun **zorunlu** alanı, `signature`
ise ("hangi yemek") hiçbir yer tutucuyla doldurulamaz. Mekan kaydında ikisi de
yok. Yemek kuralını mekana genellemek, dosyanın yaptığı hataydı.

**Kural:** bir alanın zorunluluğu türden gelir. Mekanda `entry_fee` ve
`opening_hours` dürüst yer tutucu kabul eder; yemekte `signature` ve
`price_range` etmez.

## Doğrulanmış adaylar (2026-08-20)

Ölçüm sunucudan yapıldı; konteyner bu uçlara çıkamıyor (CLAUDE.md §9b).

### Kapı 1 KAPALI — dördü de kuyruğa hazır

| Aday | Şehir | Wikidata | Koordinat | Kaynak uyumu |
| --- | --- | --- | --- | --- |
| Bab Kınnesrin | halep | `Q4837220` | 36.19449, 37.15590 | OSM `monument` ile **31 m** |
| Mar Semaan (Aziz Simeon Kilisesi) | halep | `Q1112125` | 36.33417, 36.84417 | OSM `attraction` ile **16 m** |
| Humus Kalesi | humus | `Q3388317` | 34.72343, 36.71446 | İki ayrı OSM `castle` ile **41 m** |
| Selahaddin Kalesi | lazkiye | `Q277531` | 35.59498, 36.05519 | Nominatim ↔ Overpass **16 m** |

Notlar:

- **Bab Kınnesrin** §5b'nin Nominatim tuzağını birebir gösterdi: ilk sonuç
  kapının kendisi değil, adını taşıyan **sokak** (193 m ötede). Kapıyı veren
  Overpass düğümü oldu. Depoda üç kapı zaten var (Antakya, Şarkî, Kîsan);
  dördüncüsü kurulu örüntüye oturuyor.
- **Mar Semaan** Halep'in ~30 km kuzeybatısında, Dâret Azze tarafında. Şehir
  içi değil — kümeye mekan olarak girer ama künyesinde mesafe belirtilmeli.
- **Selahaddin Kalesi** alansal: Wikidata etiket noktası Overpass ilişki
  merkezinden ~207 m ötede. §5b'ye göre bu **hata değil**; iki nokta kaynağı
  16 m içinde. Krak des Chevaliers ile **aynı UNESCO tesciline** ait — depoda
  Krak zaten var, ikisi doğal bir çift.

Künye ızgarası dördünde de **depodaki emsalden** doldurulur — uydurma değil,
aynı türden yayımlanmış kaydın kurduğu üslup:

| Aday | Emsal kayıt | `opening_hours` / `entry_fee` nereden |
| --- | --- | --- |
| Bab Kınnesrin | `bab-antakya`, `bab-sarki` | Şehir kapısı, açık alan — ikisi de "Açık alan, gün boyu" / "Ücretsiz" |
| Humus Kalesi | `tedmur-kalesi` | Höyük üstü kale — "Gündüz saatleri — durum değişebilir, teyit et" |
| Selahaddin Kalesi | `marqab-kalesi` | Uzak kale — "Gündüz saatleri; uzak bir alan, gitmeden önce sor" |
| Mar Semaan | `ugarit-hoyugu` | Şehir dışı ören yeri — aynı satır; künyede mesafe belirtilir |

Emsal **üslubu** verir, değeri değil: yazım turunda yer için ayrıca bakılır,
çıkmazsa dürüst yer tutucu yazılır. Yasak olan uydurulmuş rakam.

### Elenenler

| Aday | Neden |
| --- | --- |
| Kasr İbn Verdan | **Hama** valiliğinde, Humus'ta değil. Hama açık bir küme değil. |
| Han el-Vezir | Wikidata'da da Nominatim'de de koordinatlı eşleşme yok. |
| Efqa Pınarı | `Q127699512` ülke iddiası bile taşımıyor, Nominatim boş. İnce varlık. |
| Beyt Gazale | Wikidata var (`Q18398379`) ama OSM o adı doğrulamıyor — 33 m ötede **Beyt Acıkbaş** var. Cedeyde'de konaklar bitişik; yanlış eve pin çakma riski yüksek. |
| Halep Ulusal Müzesi | Wikidata (`Q1164599`) ve Nominatim ~166 m ayrı, Overpass müzeyi hiç vermedi. Üçüncü kaynak yok. |
| Tedmur Müzesi | Wikidata'da koordinatlı eşleşme yok, Overpass çevrede müze görmüyor. |

## Yön: yeni şehir değil, derinleşme

Envanter "Yeni şehir açılabilir" diyor — ama bu `buyume.md`'deki **üç koşuldan
yalnızca birincisi**. Doygunluk kuralı ("altı-sekiz mekan ve iki-üç rota")
uygulandığında tablo başka şey söylüyor:

| Küme | Mekan | Rota | Doygun mu |
| --- | --- | --- | --- |
| sam | 14 | 3 | evet (+3 yemek) |
| halep | 4 | 1 | hayır |
| humus | 4 | 1 | hayır |
| lazkiye | 3 | 1 | hayır |
| tedmur | 3 | 1 | hayır |

Dördü de altının altında. `buyume.md`: **"Altının altındaysan derinleş."**
Yukarıdaki dört aday bu yüzden var olan kümelere yazılmış — halep 6'ya,
humus 5'e, lazkiye 4'e çıkıyor.

## Kuyruğu kim doldurur

Kuyruk, otomatik üretimin konu uydurmasını engelleyen kapı. **Otomatik tur
kendi kapısını kendi doldurmaz** — bu havuz insan onayı için hazırlanır,
onaydan sonra `content/kuyruk.json`'a geçer.

Bu kural yerinde duruyor. Ama 2026-08-20 turunda görüldü ki havuzun **kendi
içine** ikinci bir kapı yazmak, o kapı yanlışsa turu süresiz durduruyor:
iki tur üst üste "kuyruk boş" raporlandı, oysa dört aday 08-19'dan beri
yazılmaya hazırdı.

**Kural:** havuza kapı eklerken eşiği önce **yayımlanmış külliyata** karşı
ölç. Depodaki kayıtların çoğu bir eşiği geçmiyorsa o eşik aday kapısı değil,
kişisel bir standarttır — ve `envanter.mjs` neyin gerçekten bulgu ürettiğinin
tek doğruluk kaynağıdır.

### ONAYLANDI (2026-08-20) — dördü de kuyruğa geçti

Dört aday da kapıyı geçti ve onay alındı; `kuyruk.json` → `sira` içine bu
sırayla yazıldılar:

1. **Bab Kınnesrin** (halep) — ✅ **üretildi 2026-08-20.** Halep 4 → 5.
2. **Humus Kalesi** (humus) — kuyrukta, sırada
3. **Selahaddin Kalesi** (lazkiye) — kuyrukta; Krak ile UNESCO çifti
4. **Mar Semaan** (halep) — kuyrukta; şehir dışı, künyede mesafe şart

Havuz bununla boşaldı. Kuyruktaki üç madde bitmeden yeni aday doğrulamaya
gerek yok; bittiğinde doğrulama turu yine buraya yazılır ve **yine onaya
sunulur** — otomatik tur kendi kapısını kendi doldurmuyor.

#### Bab Kınnesrin turundan çıkan iki not

- **Lisans listesi sayılı, "ticari kullanıma açık" değil.** Ifpo'nun 1960
  karesi (3122×2098, en yüksek çözünürlüklü aday) **Licence Ouverte** taşıyor.
  Etalab lisansı ticari kullanıma açık ve CC BY ile uyumlu ilan edilmiş, ama
  CLAUDE.md §6 dört lisans **sayıyor** ve bu onlardan biri değil. Listeyi
  yorumla genişletmek yerine aday elendi; genişletilecekse kural dosyada
  değişir, turda değil.
- **Kimlik çaprazlaması üç fotoğrafçıyla ucuz kapandı.** 1960 / 2005 / 2010
  kareleri aynı sivri kemeri, aynı ablak sıralarını ve aynı derin geçidi
  gösteriyor. Tek kare "doğru yer mi" sorusunu kapatmıyor; üç bağımsız kare
  kapatıyor — Bab Kîsan turunda kurulan örüntü burada da işledi.
