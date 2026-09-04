# Konum Yolu ve Slug Kuralları

## Biçim

Konum, URL'de **tek bir yol segmenti** olarak, tirelerle birleşik yazılır:

```
/satilik-daire/istanbul                      → il
/satilik-daire/istanbul-kadikoy              → il-ilçe
/satilik-daire/istanbul-kadikoy-caferaga     → il-ilçe-mahalle
```

Bazı mahalle slug'ları sitede `-mah` ekiyle biter (`...-caferaga-mah`). İkisi de
çalışabilir ama **kanonik olan sitenin verdiğidir**; şüphedeyken kullanıcının
kopyaladığı URL'i kullan.

Çoklu ilçe/mahalle seçimi yol segmentine sığmaz; site bunu `address_town=` /
`address_quarter=` sayısal ID'leriyle tekrarlayarak taşır. Bu ID'ler ezberlenemez —
`emlakarama learn <url>` ile yakala ve kayıtlı sorguda sakla.

**Pratik tavsiye:** çoklu ilçe yerine **ilçe başına bir sorgu** kur ve sonuçları
birleştir. Hem 1000 tavanına karşı korur hem ID bağımlılığını kaldırır.

## Slugify kuralları (kesin)

1. Türkçe harfler ASCII'ye indirgenir:

   | Kaynak | Slug |
   |---|---|
   | `ç` `Ç` | `c` |
   | `ğ` `Ğ` | `g` |
   | `ı` `I` | `i` |
   | `İ` `i` | `i` |
   | `ö` `Ö` | `o` |
   | `ş` `Ş` | `s` |
   | `ü` `Ü` | `u` |
   | `â` `î` `û` | `a` `i` `u` |

   Dikkat: büyük `I` → `i` (Türkçe'de `ı` okunur ama slug `i`'dir).
   `İstanbul` → `istanbul`, `Iğdır` → `igdir`.

2. Tümü küçük harfe indirilir.
3. Alfanümerik olmayan her şey `-` olur; ardışık `-` teke iner; baş/son `-` atılır.
4. Nokta ve kısaltmalar açılır: `K.Maraş` → `kahramanmaras`, `Afyon` → `afyonkarahisar`.
5. Sayılar korunur: `19 Mayıs` → `19-mayis`.

Örnekler:

```
Kadıköy        → kadikoy
Şişli          → sisli
Beyoğlu        → beyoglu
Üsküdar        → uskudar
Çankaya        → cankaya
Gaziosmanpaşa  → gaziosmanpasa
Şanlıurfa      → sanliurfa
Muğla          → mugla
Ağrı           → agri
Nevşehir       → nevsehir
Kahramanmaraş  → kahramanmaras
Afyonkarahisar → afyonkarahisar
Zonguldak Ereğli → zonguldak-eregli
```

CLI: `emlakarama slug "Kadıköy"` → `kadikoy`

## 81 il slug'ı

```
adana adiyaman afyonkarahisar agri aksaray amasya ankara antalya ardahan artvin
aydin balikesir bartin batman bayburt bilecik bingol bitlis bolu burdur bursa
canakkale cankiri corum denizli diyarbakir duzce edirne elazig erzincan erzurum
eskisehir gaziantep giresun gumushane hakkari hatay igdir isparta istanbul izmir
kahramanmaras karabuk karaman kars kastamonu kayseri kilis kirikkale kirklareli
kirsehir kocaeli konya kutahya malatya manisa mardin mersin mugla mus nevsehir
nigde ordu osmaniye rize sakarya samsun sanliurfa siirt sinop sivas sirnak tekirdag
tokat trabzon tunceli usak van yalova yozgat zonguldak
```

Not: sahibinden bazı illerde yaygın kullanımı tercih eder — `mersin` (İçel değil),
`kahramanmaras` (K.Maraş değil), `afyonkarahisar` (Afyon değil).

## Büyükşehirlerde sık kullanılan ilçe slug'ları

**İstanbul (Avrupa):** `arnavutkoy` `avcilar` `bagcilar` `bahcelievler` `bakirkoy`
`basaksehir` `bayrampasa` `besiktas` `beylikduzu` `beyoglu` `buyukcekmece`
`catalca` `esenler` `esenyurt` `eyupsultan` `fatih` `gaziosmanpasa` `gungoren`
`kagithane` `kucukcekmece` `sariyer` `silivri` `sisli` `sultangazi` `zeytinburnu`

**İstanbul (Anadolu):** `adalar` `atasehir` `beykoz` `cekmekoy` `kadikoy`
`kartal` `maltepe` `pendik` `sancaktepe` `sile` `sultanbeyli` `tuzla` `umraniye`
`uskudar`

**Ankara:** `akyurt` `altindag` `ayas` `bala` `beypazari` `cankaya` `cubuk`
`elmadag` `etimesgut` `evren` `golbasi` `gudul` `haymana` `kahramankazan`
`kalecik` `kecioren` `kizilcahamam` `mamak` `nallihan` `polatli` `pursaklar`
`sincan` `sereflikochisar` `yenimahalle`

**İzmir:** `aliaga` `balcova` `bayindir` `bayrakli` `bergama` `beydag` `bornova`
`buca` `cesme` `cigli` `dikili` `foca` `gaziemir` `guzelbahce` `karabaglar`
`karaburun` `karsiyaka` `kemalpasa` `kinik` `kiraz` `konak` `menderes` `menemen`
`narlidere` `odemis` `seferihisar` `selcuk` `tire` `torbali` `urla`

Tam ilçe listesi gerektiğinde `data/locations.json` içine ekle:
`emlakarama location add istanbul --district kadikoy --quarter caferaga`

## Doğrulama

Yanlış konum slug'ı **404 verir**, boş sonuç değil. `emlakarama url --check`
yalnızca yerel listeye karşı doğrular (ağa çıkmaz); listede yoksa uyarır ama
URL'i yine de üretir.
