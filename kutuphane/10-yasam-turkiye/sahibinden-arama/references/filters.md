# Attribute Filtreleri (`aNN`)

## Sistem

Kategoriye özel her filtre URL'de sayısal bir attribute ID ile taşınır:

| Kalıp | Tür | Örnek |
|---|---|---|
| `a{ID}={değer}` | Tekil seçim / metin | `a6=3+1` |
| `a{ID}={v1}&a{ID}={v2}` | Çoklu seçim (tekrarlı) | `a6=2%2B1&a6=3%2B1` |
| `a{ID}_min` / `a{ID}_max` | Aralık | `a4_min=100&a4_max=160` |
| `a{ID}=true` | Evet/hayır (özellik kutusu) | `a123=true` |

**ID'ler kategoriye göre değişir.** `satilik-daire`'deki `a4` ile
`satilik-arsa`'daki `a4` aynı şey olmak zorunda değildir. Bu yüzden ID'ler koda
gömülü değil, `data/attributes/{kategori-slug}.json` içinde tutulur.

`+` işareti sorgu dizesinde **boşluk** demektir; oda sayısı `3+1` gönderilirken
`3%2B1` olarak kodlanmalıdır. `emlakarama` bunu otomatik yapar — elle URL yazarken
en sık yapılan hata budur.

## Keşif akışı (ground truth üretir)

1. Kategorinin detaylı arama sayfasını aç:
   `https://www.sahibinden.com/arama/detayli?category={ID}`
2. Tarayıcıda `Cmd+S` → "Web Page, Complete" veya "Page Source" →
   `samples/detayli-{kategori}.html`
3. ```bash
   emlakarama discover-filters samples/detayli-satilik-daire.html \
     --category satilik-daire --write
   ```
4. Araç şunları çıkarır:
   - `name="aNN"`, `name="aNN_min"`, `name="aNN_max"` olan tüm `input`/`select`
   - Her alanın `<label>` metni (Türkçe etiket)
   - `<select>` içindeki `<option value>` / görünen metin çiftleri
   - Alan tipi çıkarımı: `range` | `enum` | `bool` | `text`
5. Sonuç `data/attributes/satilik-daire.json`:

```json
{
  "category": "satilik-daire",
  "category_id": 3518,
  "discovered_at": "2026-08-24",
  "source": "samples/detayli-satilik-daire.html",
  "attributes": {
    "a4": {
      "id": "a4", "label": "m² (Brüt)", "type": "range",
      "aliases": ["m2", "metrekare", "brut"], "confidence": "discovered"
    },
    "a6": {
      "id": "a6", "label": "Oda Sayısı", "type": "enum",
      "options": {"1+0": "1+0", "1+1": "1+1", "2+1": "2+1", "3+1": "3+1"},
      "aliases": ["oda", "oda sayisi"], "confidence": "discovered"
    }
  }
}
```

Bundan sonra Türkçe etiketle filtre verilebilir:

```bash
emlakarama url satilik-daire istanbul-kadikoy \
  --attr "m² (Brüt)=100..160" --attr "Oda Sayısı=3+1"
```

## Tek filtre için hızlı yol: `learn`

Kullanıcı filtreyi sitede elle uygular, URL'i yapıştırır:

```bash
emlakarama learn 'https://www.sahibinden.com/satilik-daire/istanbul-kadikoy?a4_min=100&a6=3%2B1'
```

Çıktı: bilinen parametreleri isimlendirir, **bilinmeyen `aNN`'leri listeler** ve
`--label` ile etiketlemeyi önerir:

```
a4_min=100   → bilinmiyor  (öneri: emlakarama attr label satilik-daire a4 "m² (Brüt)" --type range)
a6=3+1       → bilinmiyor
```

Bir kez etiketlenen ID kalıcı olarak kayda geçer.

## Konut kategorileri için beklenen filtre listesi

Keşif yapılmadan önce **hangi filtrelerin var olduğunu** bilmek işe yarar
(ID'leri değil). Satılık/kiralık daire formunda tipik olarak şunlar bulunur:

- m² (Brüt), m² (Net) — aralık
- Oda Sayısı — çoklu enum (`Stüdyo`, `1+0`, `1+1`, `2+1`, `3+1`, `4+1`, `5+1`, `5+ üzeri`)
- Bina Yaşı — aralık veya enum (`0`, `1`, `2`, `3`, `4`, `5-10`, `11-15`, `16-20`, `21+`)
- Bulunduğu Kat — enum (`Bodrum`, `Zemin`, `Bahçe Katı`, `Giriş Katı`, `1`…`30+`, `Çatı Katı`)
- Kat Sayısı — aralık
- Isıtma — enum (`Doğalgaz (Kombi)`, `Merkezi`, `Klima`, `Yerden Isıtma`, …)
- Banyo Sayısı — enum
- Balkon — bool
- Eşyalı — bool
- Kullanım Durumu — enum (`Boş`, `Kiracılı`, `Mülk Sahibi`)
- Site İçerisinde — bool
- Aidat — aralık (kiralıkta)
- Depozito — aralık (kiralıkta)
- Krediye Uygun — bool
- Tapu Durumu — enum (`Kat Mülkiyetli`, `Kat İrtifaklı`, `Hisseli Tapu`, …)
- Takas — enum (`Evet`, `Hayır`)
- Cephe — çoklu enum (`Kuzey`, `Güney`, `Doğu`, `Batı`)
- Satıcı tipi — `Sahibinden` / `Emlak Ofisinden` / `İnşaat Firmasından` / `Bankadan`
- Video/Sanal Tur olanlar — bool
- Fotoğraflı ilanlar — bool

Arsa: İmar Durumu, m², Ada No, Parsel No, Pafta No, Kaks/Emsal, Gabari, Tapu Durumu.
İşyeri: m², Oda Sayısı, Bina Yaşı, Kat Sayısı, Isıtma, Krediye Uygun, Aidat, Depozito.

## Satıcı tipi — özel not

"Sahibinden" (mal sahibinden) filtresi emlak avcılığında en değerli filtredir
(komisyon yok, pazarlık payı farklı). Ancak URL'de nasıl taşındığı kategoriye
göre değişir; bazı sayfalarda ayrı bir `aNN=true`, bazılarında `userType`
benzeri bir parametredir. **Keşif akışı olmadan tahmin etme.** Filtre uygulanmış
URL'i kullanıcıdan iste, `learn` ile yakala, `attr label ... --alias sahibinden`
ile isimlendir. Sonra:

```bash
emlakarama url satilik-daire istanbul-kadikoy --attr "sahibinden=true"
```

## Güven seviyeleri

| Seviye | Anlamı | Kullanım |
|---|---|---|
| `discovered` | Detaylı arama HTML'inden çıkarıldı | Güvenle kullan |
| `learned` | Gerçek bir URL'de görüldü + kullanıcı etiketledi | Güvenle kullan |
| `observed` | Gerçek URL'de görüldü, etiketi bilinmiyor | Aynen geçir, yorumlama |
| `guessed` | Tahmin | **Kullanma**, önce doğrula |

`emlakarama url` varsayılan olarak `guessed` attribute'ları reddeder;
`--allow-guessed` ile zorlanabilir.
