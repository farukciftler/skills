# Trip.com filtre kodları

25 Ağustos 2026'da Londra liste sayfasından hasat edildi (`scripts/filtre_hasadi.js`).
Kodlar **şehirden bağımsızdır** — landmark/semt ve marka listeleri hariç, onlar şehre özeldir.

Token'a çevirme kuralı için `url-grameri.md` §2. Kısaca: `type|value` → `type~value*type*value`.

## Sıralama — tip 17

| Seçenek | filterID | Token |
|---|---|---|
| Trip.com önerisi | `17\|1` | `17~1*17*1` |
| **Yürüme/sürüş mesafesi (önce en yakın)** | `17\|12` | `17~12*17*12` |
| Kuş uçuşu mesafe (yakından uzağa) | `17\|5` | `17~5*17*5` |
| En çok yorumlanan / en iyi puan | `17\|6` | `17~6*17*6` |
| En düşük fiyat (vergi dahil) | `17\|3` | `17~3*17*3` |
| En yüksek fiyat (vergi dahil) | `17\|4` | `17~4*17*4` |
| Yıldız (yüksekten düşüğe) | `17\|14` | `17~14*17*14` |

Landmark kısıtı varsa **her zaman `17|12`** kullan: kartlarda landmark'a yürüme mesafesi
metre cinsinden yazılır ve liste yakından uzağa gider, eşiklemek kolaylaşır.

## Rezervasyon politikası — tip 23

| Seçenek | filterID |
|---|---|
| **Ücretsiz iptal** | `23\|10` |
| Anında onay | `23\|5` |
| Tüm paketler | `23\|40` |

`23|10` yalnızca "bu tesiste ücretsiz iptal edilebilen *bir* oran var" demektir.
**Son tarihi söylemez.** Tarih için `iptal-ve-oda.md`.

## Ödeme — tip 7

| Seçenek | filterID |
|---|---|
| Online ön ödeme | `7\|2` |
| Otelde ödeme | `7\|1` |
| Kredi kartsız rezervasyon | `7\|6` |

## Tesis tipi — tip 75 (ve üst gruplar 20550)

| Seçenek | filterID | Token |
|---|---|---|
| **Otel** | `75\|TAG_495` | `75~TAG_495*75*495` |
| Butik/servisli apart | `75\|TAG_505` | `75~TAG_505*75*505` |
| Apart daire | `75\|TAG_513` | `75~TAG_513*75*513` |
| Pansiyon (guest house) | `75\|TAG_503` | `75~TAG_503*75*503` |
| B&B | `75\|TAG_504` | `75~TAG_504*75*504` |
| Tatil evi | `75\|TAG_514` | `75~TAG_514*75*514` |
| Villa | `75\|TAG_507` | `75~TAG_507*75*507` |
| Hostel | `75\|TAG_519` | `75~TAG_519*75*519` |
| Kapsül otel | `75\|TAG_520` | `75~TAG_520*75*520` |
| Han/inn | `75\|TAG_499` | `75~TAG_499*75*499` |
| Tekne | `75\|TAG_522` | — |
| Şato/kır evi | `75\|TAG_517` | — |
| Homestay | `75\|TAG_510` | — |
| Sıra dışı konaklama | `75\|TAG_521` | — |
| Chalet | `75\|TAG_524` | — |
| Lodge | `75\|TAG_526` | — |

**Üst gruplar** (birden fazla alt tipi birden açar, farklı biçim):
`Oteller` = `20550|6|67561`, `Evler & apartlar` = `20550|6|67565`, `Hosteller` = `20550|6|67563`.
Kullanıcı net "hotel" dediyse üst grubu değil, **`75|TAG_495`'i kullan** — üst grup servisli
apartları da içeri alır.

## Yıldız — tip 16

| Yıldız | filterID |
|---|---|
| 5 | `16\|5` |
| 4 | `16\|4` |
| 3 | `16\|3` |
| 2 | `16\|2` |

Birden fazlası aynı anda seçilebilir (ayrı token'lar, VEYA mantığı).

## Misafir puanı — tip 6

| Seçenek | filterID |
|---|---|
| Harika 9+ | `6\|10` |
| Çok iyi 8+ | `6\|9` |
| İyi 7+ | `6\|8` |
| Fena değil 6+ | `6\|7` |

## Yorum sayısı — tip 25

| Seçenek | filterID |
|---|---|
| 500+ | `25\|7` |
| 200+ | `25\|6` |
| 100+ | `25\|5` |

Puan filtresini yorum sayısı filtresiyle birlikte kullan; tek başına puan yanıltır.

## Oda olanakları — tip 77

En sık kullanılanlar:

| Olanak | filterID |
|---|---|
| **Özel banyo** | `77\|92` |
| **Özel tuvalet** | `77\|445` |
| Klima | `77\|107` |
| Küvet | `77\|91` |
| Mutfak | `77\|198` |
| Çamaşır makinesi | `77\|207` |
| Sigara içilmeyen oda | `77\|NoSmoking` |
| Balkon | `77\|247` |
| Buzdolabı | `77\|87` |
| Su ısıtıcı | `77\|80` |
| TV | `77\|183` |
| Jakuzi | `77\|236` |
| Teras | `77\|210` |
| Kahve makinesi | `77\|192` |
| Ek yatak mümkün | `77\|extraBed` |
| Bebek yatağı mümkün | `77\|extraCrib` |
| Özel havuz | `77\|228` |

Erişilebilirlik (aynı tip 77): erişilebilir oda `77|630`, erişilebilir duş `77|398`,
tutamaklı küvet `77|400`, tutamaklı klozet `77|399`, duş taburesi `77|404`,
banyoda acil durum düğmesi `77|403`, erişilebilir tuvalet `77|629`.

Birden fazla banyo: `98|-1` (farklı tip).

## Tesis olanakları — tip 3

Havuz `3|605`, otopark `3|656`, spa `3|65`.
Erişilebilirlik (tesis): merdivende tutamak `3|568`, koridorda tutamak `3|567`,
basamaksız giriş `3|573`, tekerlekli sandalye `3|575`, Braille tabela `3|566`.

## Yatak tipi — tip 4

| Yatak | filterID |
|---|---|
| 1 çift kişilik | `4\|1` |
| 2 yatak | `4\|2` |
| 1 tek kişilik | `4\|4` |
| 1 king | `4\|3` |
| 3 yatak | `4\|6` |
| 4+ yatak | `4\|5` |

## Öğün

Kahvaltı dahil `5|1`, akşam yemeği dahil `86|1`, kahvaltı+akşam `146|1`, her şey dahil `146|4`.

## Oda özellikleri — tip 81 / 78

Aile odası `81|1188`, suit `81|1309`, balkonlu `81|1581`, loft `81|1587`,
tüm ünite (entire unit) `78|1`, yatakhanede yatak `78|3`.

## Yatak odası sayısı — tip 66
1 `66|1`, 2 `66|2`, 3+ `66|3`.

## Oda büyüklüğü — tip 147
`147|25|270|METRIC` (≥25 m²), `147|35|375|METRIC` (≥35 m²), `147|80|860|METRIC` (≥80 m²).

## Tesis özellikleri — tip 1
Aile dostu `1|1150`, manzaralı `1|643`, romantik `1|1187`, kendi kendine check-in `1|1320`,
nehir manzarası `1|1200`, tasarım oteli `1|112`, sertifikalı sürdürülebilir `1|14535`.

## Misafir izlenimleri — tip 20550
İdeal konum `20550|25919`, yapılacak çok şey `20550|22755`, pırıl pırıl temiz `20550|3903`,
sessiz oda `20550|8681`, mükemmel hizmet `20550|25933`.

## Yenilenme tarihi — tip 88
Son 6 ay `88|1`, son 1 yıl `88|2`, son 2 yıl `88|3`.

## Fiyat aralığı — tip 15
`15~Range*15*{min}~{max}` — gecelik, `curr` para biriminde. Örn. `15~Range*15*5350~8250`.

## Kodları tazeleme
Bu tablo eskirse: liste sayfasını aç, `scripts/filtre_hasadi.js` içeriğini çalıştır,
çıktıyı buraya yaz. Script tüm "Daha Fazla Göster" düğmelerini açıp her filtre öğesinin
başlığını ve `filterID`'sini React fiber'dan okur.
