# Kategoriler

## Nasıl kullanılır

Kategori iki biçimde ifade edilir:

- **Slug** — URL yolunda: `/satilik-daire/...`
- **Sayısal ID** — detaylı arama ve bazı filtre uçlarında: `/arama/detayli?category=3518`

Slug arama sayfası için yeterlidir. ID yalnızca **filtre keşfi** (`discover-filters`)
için gerekir, çünkü `aNN` attribute setleri kategori ID'sine bağlıdır.

Kategori ID'sini bulma: sitede kategoriye gir → sol menüde "Detaylı Arama" → adres
çubuğundaki `?category=NNNN`. Bulduğun ID'yi `data/categories.json` içine yaz:

```bash
emlakarama category set satilik-daire --id 3518 --label "Satılık Daire"
```

## Emlak ağacı (slug'lar)

Sahibinden'in emlak slug'ları `{satilik|kiralik|devren-kiralik|devren-satilik}-{tip}`
kalıbını izler. Doğrulanmış olanlar:

### Konut
| Slug | Karşılığı |
|---|---|
| `satilik` | Tüm satılık emlak |
| `kiralik` | Tüm kiralık emlak |
| `satilik-daire` | Satılık daire |
| `kiralik-daire` | Kiralık daire |
| `satilik-residence` | Satılık rezidans |
| `kiralik-residence` | Kiralık rezidans |
| `satilik-mustakil-ev` | Satılık müstakil ev |
| `kiralik-mustakil-ev` | Kiralık müstakil ev |
| `satilik-villa` | Satılık villa |
| `kiralik-villa` | Kiralık villa |
| `satilik-yazlik` | Satılık yazlık |
| `kiralik-yazlik` | Kiralık yazlık |
| `gunluk-kiralik-daire` | Günlük kiralık daire |

### Arsa / arazi
| Slug | Karşılığı |
|---|---|
| `satilik-arsa` | Satılık arsa |
| `kiralik-arsa` | Kiralık arsa |

Arsa aramalarında imar durumu (konut, ticari, tarla, bağ-bahçe, sanayi) bir
`aNN` attribute'udur — keşif akışıyla çıkar.

### İşyeri
| Slug | Karşılığı |
|---|---|
| `satilik-isyeri` | Satılık işyeri |
| `kiralik-isyeri` | Kiralık işyeri |
| `devren-satilik-isyeri` | Devren satılık işyeri |
| `devren-kiralik-isyeri` | Devren kiralık işyeri |

### Bina / turistik / devremülk
| Slug | Karşılığı |
|---|---|
| `satilik-bina` | Satılık bina |
| `kiralik-bina` | Kiralık bina |
| `satilik-turistik-tesis` | Satılık turistik tesis |
| `kiralik-turistik-tesis` | Kiralık turistik tesis |
| `devremulk` | Devremülk |

> Emin olmadığın bir slug'ı denemenin en ucuz yolu: kullanıcıdan siteye girip
> kategoriyi seçmesini ve URL'i yapıştırmasını istemek. Yanlış slug 404 verir,
> sessizce boş sonuç değil — yani `emlakarama` yanlış slug'ı tespit edebilir
> (`parse` sonucu 0 ilan + 404 başlığı).

## Diğer üst kategoriler (emlak dışı)

Bu skill emlak odaklıdır ama URL dilbilgisi aynıdır:

| Slug | Alan |
|---|---|
| `otomobil` | Vasıta → otomobil |
| `arazi-suv-pickup` | Vasıta → SUV |
| `motosiklet` | Vasıta → motosiklet |
| `ticari-araclar` | Vasıta → ticari |
| `ikinci-el-ve-sifir-alisveris` | İkinci el alışveriş |
| `is-makineleri-sanayi` | İş makineleri & sanayi |
| `ustalar-ve-hizmetler` | Hizmetler |
| `yardimci-arayanlar` | İş ilanları |

Vasıta kategorilerinde `aNN` setleri tamamen farklıdır (yıl, km, yakıt, vites);
her biri için ayrı keşif gerekir.

## Kategori dosyası biçimi

`data/categories.json`:

```json
{
  "satilik-daire": {
    "slug": "satilik-daire",
    "label": "Satılık Daire",
    "group": "emlak/konut",
    "category_id": null,
    "confidence": "verified"
  }
}
```

- `category_id: null` → filtre keşfi henüz yapılmamış.
- `confidence`: `verified` (gerçek URL'de görüldü) | `likely` | `unverified`.
