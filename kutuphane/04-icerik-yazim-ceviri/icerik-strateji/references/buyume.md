# Büyüme modeli

## Neden derinlik önce

Site hub & spoke üstüne kurulu: şehir sayfası mekan ve rotalara dağıtıyor, onlar
şehre geri bağlanıyor. Bu yapıda **bir kaydın değeri tek başına değil, kümesiyle
belirleniyor.**

Üç şehir × altı mekan ile dokuz şehir × iki mekanı karşılaştır. İkisinde de
kayıt sayısı aynı sırada, ama:

| | 3 şehir × 6 mekan | 9 şehir × 2 mekan |
| --- | --- | --- |
| Çalışan hub | 3 | 0 |
| Şehir sayfasında dolu ızgara | 3 | 0 |
| Kurulabilen rota | 3–6 | neredeyse yok |
| İç bağlantı yoğunluğu | yüksek | dağınık |
| Okurun bir sonraki adımı | var | yok |

İkinci sütun dokuz tane ince sayfa üretiyor ve hiçbiri kimseyi bir yere
götürmüyor.

## Çalışan küme eşiği

```
1 şehir  +  3 mekan  +  1 rota
```

**Üç mekan** keyfi değil: şehir sayfasındaki ızgara üç sütun. İki kayıt satırı
yarım bırakıyor, üç kayıt bir satır tamamlıyor — okur "burada içerik var"
sinyalini oradan alıyor.

**Bir rota** de keyfi değil: rota, mekanları birbirine bağlayan tek yapı.
Rotasız küme, aynı şehri anlatan ama birbirine bakmayan sayfalar yığını.

## Ölü hub neden zararlı

Bir şehri açıp mekanla beslememek, o şehri hiç açmamaktan **kötü**:

- **Söz tutulmuyor.** Sayfa "Bu şehirde" başlığı atıyor ve altına bir kart
  koyuyor. Okur bunu eksiklik olarak okuyor, "yeni site" olarak değil.
- **İnce sayfa.** Arama motoru için değeri düşük; üstelik üç dilde üç ayrı ince
  sayfa demek.
- **Tarama bütçesi.** Site haritasına üç kayıt giriyor, karşılığında bir şey
  vermiyor.

Bu yüzden envanterde ölü hub P1: yetim mekandan sonra en acil borç.

## Genişleme sırası

```
şehir aç  →  3 mekan  →  1 rota  →  küme kapandı  →  sonraki şehir
```

Sıra bozulursa borç birikiyor. Bugünkü tablo tam olarak bunun sonucu: beş şehir
açılmış, biri kapanmış.

## Yeni şehir açma koşulları

Üçü birden sağlanmalı:

1. **Mevcut kümelerin hepsi kapalı.** `envanter.mjs` "Yeni şehir açılabilir"
   diyene kadar açma.
2. **En az üç mekan hakkında somut bilgin var** — ziyaret saati, giriş,
   koordinat düzeyinde. Yoksa açtığın şey doğrudan bir ölü hub.
3. **Mevcut kümeye bir rotayla bağlanabiliyor.** Bağsız şehir ada; ne okur ne
   tarayıcı oraya bir yoldan varıyor.

## İstisna: rota bir şehri erken açabilir

Tek meşru istisna. Var olan bir küme ile yeni bir şehri birleştiren bir rota
kuruyorsan, o rotanın durakları yeni şehirde iki mekan gerektirebilir. Bu
durumda şehir "rota tarafından açılıyor" ve üçüncü mekan borcu kalıyor —
envanter bunu zayıf küme olarak zaten gösteriyor.

Sahil rotası (Lazkiye → Marqab → Krak) tam olarak böyle çalıştı: rota, iki yeni
mekanı ve aralarındaki bağı aynı anda getirdi.

## Ne zaman genişlemeyi bırakıp derinleşmeli

Kayıt sayısı değil, **kümenin doygunluğu** ölçü. Bir şehirde altı-sekiz mekan ve
iki-üç rota varsa o küme doygun; dokuzuncu mekan artık yeni bir şehrin ilk
mekanı kadar değer getirmiyor. O noktada genişle.

Altının altındaysan derinleş.
