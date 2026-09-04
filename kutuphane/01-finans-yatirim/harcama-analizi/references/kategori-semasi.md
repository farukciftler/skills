# Kategori şeması

Kanonik ağaç. `harcama.py` yalnız buradaki `kategori/alt_kategori` çiftlerini
kabul eder; sözlükte bunların dışında bir değer varsa **durur** (tıpkı
`hata_ozet.py`'nin sözlük denetimi gibi — sözlük dışı değer sessizce yeni
kategori açamaz).

## Türler (`tur`)

| tur | Anlam | Hane dışına çıkan toplama girer mi |
|---|---|---|
| `gelir` | maaş, iade, kâr payı, diğer | — (gelir) |
| `harcama` | tüketim | **evet** |
| `aile_destek` | eş ve aile üyelerine transfer | **evet** |
| `kisi_odeme` | amaç bilinmeyen kişi transferi | **evet** (ayrı gösterilir) |
| `nakit` | ATM çekimi | **evet** (ayrı gösterilir, kategorisi bilinmez) |
| `finans_masraf` | ücret, BSMV, stopaj, kambiyo vergisi | **evet** |
| `ic_transfer` | kendi hesapları arası | hayır |
| `varlik_transferi` | fon/altın/döviz/katılma hesabı — bir varlıktan diğerine | hayır (ayrı "varlığa net" sütunu) |
| `belirsiz` | sınıflanamadı | **evet** (ayrı gösterilir) |

## Kategoriler (`kategori/alt_kategori`)

| kategori | alt_kategori seçenekleri | Not |
|---|---|---|
| `gelir` | `maas` · `iade` · `kar_payi` · `diger` | maaş = işveren havalesi/"MAAŞ ÖDEMESİ"; ikinci bankaya geçişi `ic_transfer` |
| `konut` | `kira` · `elektrik` · `dogalgaz` · `su` · `internet` · `aidat` · `ev_esyasi` | kira karşı taraf sözlüğünden gelir (varsayım olabilir) |
| `iletisim` | `mobil` · `sabit` | Turkcell, Vodafone tahsilatları |
| `gida_market` | `market` · `kasap_sarkuteri` · `manav_pazar` · `online_market` | BİM, File, Getir, Misto Gıda, peynirci, kasap |
| `yemek` | `restoran` · `kafe` · `paket_servis` · `fast_food` | Yemeksepeti tüm aracıları → `paket_servis` |
| `ulasim` | `taksi` · `toplu_tasima` · `sehirlerarasi` · `akaryakit` · `otopark` | Bi Taksi, Belbim/İstanbulkart, TCDD, obilet, İnegöl Seyahat |
| `seyahat` | `ucak` · `konaklama` · `tur_acente` · `yurt_disi_pos` · `yurt_disi_atm` · `muze_giris` · `harc` | THY, Pegasus, Trip.com, Saraybosna POS, yurt dışı çıkış harcı |
| `giyim` | `giyim` · `ayakkabi_aksesuar` | LCW, Boyner, QDF |
| `alisveris` | `e_ticaret` · `elektronik` · `ev_dekor` · `kitap_kirtasiye` · `hediye_cicek` | Hepsiburada, Media Markt, English Home, Cazip Home |
| `egitim` | `dil` · `harc` · `kurs` · `kitap` | Preply, AÖF harcı |
| `saglik` | `eczane` · `hastane` · `sigorta` | |
| `dijital` | `yazilim` · `uygulama` · `oyun` · `bulut` | PayTR/Bulutova, Apple, Google Workspace, Gameplus |
| `kisisel` | `kuafor_bakim` · `spor` · `hobi` | |
| `eglence` | `sinema_etkinlik` · `abonelik_medya` | |
| `bagis_hediye` | `bagis` · `hediye` | |
| `vergi_resmi` | `vergi` · `harc` · `ceza` | "Vergi Tahsilatı", yurt dışı çıkış harcı `seyahat/harc`'a gider |
| `finans_masraf` | `islem_ucreti` · `bsmv` · `stopaj` · `kambiyo_vergisi` · `mkk` | |
| `nakit` | `atm_yurtici` · `atm_yurtdisi` | |
| `aile_destek` | `es` · `aile` | karşı taraf sözlüğü |
| `kisi_odeme` | `kisi` | amaç bilinmiyor |
| `ic_transfer` | `kendi_hesabi` · `gunluk_katilma` · `maas_gecisi` | |
| `varlik_transferi` | `fon` · `altin` · `doviz` · `katilma_hesabi` · `birikim` | Akbank "Esnek Birikim" → `birikim` |
| `belirsiz` | `belirsiz` | |

## Karar sırası

1. `islem_adi` sabit kuralları (banka türü)
2. karşı taraf sözlüğü (transferler)
3. Vakıf Katılım iç kalıpları (açıklama regex'i)
4. POS: **MCC** → **işyeri sözlüğü** → `belirsiz`
5. Akbank kuralları

Aynı satır için iki kural çakışırsa **erken olan kazanır**; motor çakışmayı
`eslesme_kaynagi` sütununda gösterir (`islem_adi` · `karsi_taraf` · `vk_kalip`
· `mcc` · `sozluk` · `akbank` · `yok`).

## MCC tablosu (POS satırlarında `Mcc: NNNN`)

| MCC | kategori/alt | Not |
|---|---|---|
| 5411 | gida_market/market | |
| 5499 | gida_market/market | çeşitli gıda |
| 5462 | gida_market/manav_pazar | fırın/pastane → yemek/kafe değil, gıda |
| 5812 | yemek/restoran | |
| 5814 | yemek/fast_food | |
| 5813 | yemek/kafe | bar/kafe |
| 5818 | dijital/uygulama | dijital ürün (Apple) |
| 5734 | dijital/yazilim | yazılım mağazası |
| 7372 | dijital/yazilim | programlama/SaaS |
| 4121 | ulasim/taksi | |
| 4111 | ulasim/toplu_tasima | |
| 4112 | ulasim/sehirlerarasi | tren |
| 4131 | ulasim/sehirlerarasi | otobüs |
| 5541 · 5542 | ulasim/akaryakit | |
| 7523 | ulasim/otopark | |
| 3000–3299 · 4511 | seyahat/ucak | |
| 4722 | seyahat/tur_acente | Trip.com |
| 7011 · 3501–3999 | seyahat/konaklama | |
| 9399 | seyahat/muze_giris | kamu hizmeti — yurt dışında müze bileti olarak görüldü |
| 5691 · 5651 · 5611 · 5621 | giyim/giyim | |
| 5661 | giyim/ayakkabi_aksesuar | |
| 5948 | giyim/ayakkabi_aksesuar | deri/valiz |
| 5309 | alisveris/e_ticaret | duty free |
| 5311 · 5399 · 5964 · 5969 | alisveris/e_ticaret | |
| 5732 · 5045 | alisveris/elektronik | |
| 5712 · 5719 | alisveris/ev_dekor | |
| 5942 · 5943 | alisveris/kitap_kirtasiye | |
| 5992 | alisveris/hediye_cicek | |
| 8299 · 8220 | egitim/kurs | |
| 5912 · 8062 · 8011 | saglik/eczane · hastane | |
| 7230 · 7298 | kisisel/kuafor_bakim | |
| 7832 · 7922 | eglence/sinema_etkinlik | |
| 6011 | nakit/atm_yurtici — **yurt dışı ATM ise `nakit/atm_yurtdisi`** (işlem adı "Yurt Dışı") | |
| 4814 · 4816 | iletisim/mobil · dijital/bulut | Google Workspace 4816 |
| 8398 | bagis_hediye/bagis | |

Listede olmayan MCC → sözlüğe düşer; sözlükte de yoksa `belirsiz` ve MCC kodu
`isyeri_ozet.csv`'de görünür ki tabloya eklenebilsin.

## Sözlük dosyası biçimi (`kategori_sozlugu.csv`)

```
desen,kategori,alt_kategori,tur,guven,not
YEMEKSEPET,yemek,paket_servis,harcama,kesin,tüm ödeme aracıları (Param/İyzico/Sipay/Yemekpay)
```

- `desen`: regex, büyük/küçük duyarsız; metin önce **ASCII'ye indirgenir**
  (İ→I, ı→i, ş→s, ğ→g, ü→u, ö→o, ç→c) sonra eşlenir → desenleri ASCII yaz.
- **Sıra**: yukarıdan aşağı ilk eşleşen kazanır. Özel > genel.
- `guven`: `kesin` · `varsayim`. Varsayımlar raporda ayrı sayılır.
- `not`: neden bu kategori; kullanıcı teyidi varsa tarihiyle.
