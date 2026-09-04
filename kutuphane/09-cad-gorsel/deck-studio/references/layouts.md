# Düzen arşivi

Tüm koordinatlar `LAYOUT_WIDE` içindir: **13.33 x 7.5 inç**. Slayt eklemeden
önce `pres.layout = 'LAYOUT_WIDE'` yaz, yoksa varsayılan 10x5.625'te çalışırsın
ve kenardan taşan şekiller sessizce kaybolur.

## Izgara

Tek bir ızgara kur, deste boyunca değiştirme:

```
dış boşluk    0.9in (üst/alt/sol/sağ)   → içerik alanı 11.53 x 5.7in
kolon         12 kolon, oluk 0.2in      → kolon genişliği 0.8275in
kolon x       x(n) = 0.9 + (n-1) * 1.0275      n = 1..12
blok aralığı  0.35in (tek değer, deste boyunca aynı)
```

Faydalı kolon sınırları: `x1=0.90` `x4=3.98` `x5=5.01` `x7=7.07` `x9=9.12`
`sağ kenar=12.43`.

## Arketipler

Ardışık iki slaytta aynı arketipi kullanma. 12-16 slaytlık bir destede her
arketip en fazla iki kez görünsün.

### A — Kapak
Koyu (veya blok renkli) zemin, üç-dört satırlık dev başlık sola dayalı, altta
tek satır mikro künye. Görsel yoksa tipografinin kendisi görseldir.
```
başlık   x0.9  y1.5  w8.5  h3.4   display 48-56pt, lineSpacing ≈ fontSize*1.06
künye    x0.9  y5.7  w7.0  h0.4   12-13pt, muted
```

### B — Manşet + kanıt (statement)
Slaytın tek işi bir cümle söylemek. Üst yarıda 32-40pt eylem başlığı, alt yarıda
tek destekleyici görsel veya üç kısa kanıt satırı.
```
başlık   x0.9  y0.75 w11.5 h1.2
içerik   x0.9  y2.35 w11.5 h4.2
```

### C — İki kolon (metin / görsel)
En çok kullanılan, bu yüzden en çabuk sıkıcı olan. Oranı 50/50 yapma; 5/7 veya
7/5 böl, ve hangi tarafın ağır olduğunu slayttan slayta değiştir.
```
metin    x0.9  y1.4  w5.3  h4.8
görsel   x6.9  y0.9  w5.53 h5.7    (veya tam taşan: x6.67 y0 w6.66 h7.5)
```

### D — Tam taşan görsel + kapak metni (half-bleed)
Görsel slaytın bir yarısını kenardan kenara doldurur; metin diğer yarıda veya
görselin üstünde koyu katmanla. Mockup'lar için en güçlü sunum biçimi.
```
görsel   x0    y0    w6.66 h7.5
metin    x7.4  y1.6  w5.03 h4.3
```

### E — Büyük sayı (stat)
Tek metrik, dev punto. İki-üç metriği yan yana koyacaksan puntoları eşit tut,
etiketleri kısa.
```
sayı     54-72pt display; etiket 12-13pt muted, sayının hemen altında
3'lü:    x0.9 / x5.02 / x9.14, her biri w3.3, y2.4, h2.2
```

### F — Kart ızgarası (2x2 / 2x3)
Kartlar `surface` renginde, kenarlıksız veya tek kılcal kenarlıklı. Eşit üç
yuvarlak kart klişesinden kaçmak için: kartlardan birini iki kolon geniş yap
(bento mantığı) ya da içeriklerini farklı biçimlendir.
```
2x2:  x0.9 / x7.07 ; y1.5 / y4.3 ; w5.36 h2.5
2x3:  x0.9 / x4.98 / x9.06 ; w3.47
```

### G — Süreç / zaman çizgisi
Yalnızca içerik gerçekten sıralıysa. Adımlar arasında tek yönlü ilerleme
görünmeli; numaralandırma ancak burada meşrudur.
```
yatay eksen y3.6, adımlar x0.9'dan başlayıp eşit aralıklı
adım başlığı eksenin üstünde, açıklama altında — hepsi aynı tarafta değil
```

### H — Veri slaytı
Bir grafik + bir cümlelik yorum. Grafik asla slaytın tamamını kaplamaz; yorumu
grafiğe bakmadan okunabilecek şekilde yaz.
```
başlık   x0.9  y0.7  w11.5 h1.0    (eylem başlığı: bulguyu söyler)
grafik   x0.9  y2.0  w7.0  h4.4
yorum    x8.3  y2.2  w4.13 h3.0    16pt, sola dayalı
```

### I — Bölüm ayracı
Poster yönünden ödünç: koyu/blok zemin, tek kelime veya kısa öbek, bölüm
numarası küçük. Deste ritmini kurar; 12+ slaytta 2-3 tane koy.

### J — Kapanış / eylem çağrısı
Kapağın görsel eşi (aynı zemin, aynı tipografi), tek bir istek ve iletişim.
Deste sunucusuz gidiyorsa burada bir sonraki adım açıkça yazılı olmalı.

## Tipografi ölçeği

| Öge | Punto | Not |
|---|---|---|
| Kapak display | 48-56 | satır aralığı ≈ punto x 1.06 |
| Slayt başlığı | 30-38 | 3 satırı geçmesin |
| Bölüm başlığı | 20-24 | |
| Gövde | 15-17 | 14'ün altına inme, salondan okunmaz |
| Etiket / künye | 11-13 | muted renk |
| Dev sayı | 54-72 | display yüzü, tabular rakam |

Boyut kontrastı yönün kimliğini taşır: "Beyaz Laboratuvar" düşük kontrastla
(başlık 24 / gövde 15) çalışır, "Poster" uçurumla (96 / 13). Ortada kalma.

## pptxgenjs pratik notları

Bu skill'e özel olanlar; genel tuzaklar `/mnt/skills/public/pptx/SKILL.md`'de.

- Her `addText` çağrısına `isTextBox: true` ve — bir şekil/çizgi ile
  hizalanıyorsa — `margin: 0` koy. Metin kutusunun gizli iç dolgusu hizayı
  bozan en yaygın sebeptir.
- `lineSpacing` puntoyla birlikte verilmezse başlıklar aralanır. Kapakta
  `fontSize: 52, lineSpacing: 55` gibi açıkça yaz.
- `charSpacing` (negatif değer alır) display tipografide gerekir: 48pt+ bir
  başlık `charSpacing: -1` ile toparlanır. `letterSpacing` yok sayılır.
- Gradyan dolgu desteklenmez. Gradyan gerekiyorsa `render_html.py` ile bir
  arka plan PNG'si üret ve `slide.background = { path: 'bg.png' }` ver.
- Metin görselin üstüne gelecekse okunurluk katmanını **görsele gömme** —
  `addShape` ile `ROUNDED_RECTANGLE`/`RECTANGLE` koy ve `transparency: 35`
  ver; sonra dilediğin gibi ayarlarsın.
- Şeffaf PNG'ler (cihaz mockup'ları) doğru çalışır; koyu zeminde `--transparent`
  ile üretilmiş bir mockup slaytın rengini alır.

## Grafikler

Grafiği **native tut** (`addChart`), görsele çevirme — müşteri veriyi
güncelleyecek. Varsayılan pptxgenjs grafiği çıplak render eder; her grafikte
şunları ayarla:

```js
{
  chartColors: [ACCENT],                 // paletten; tek serilik grafikte tek renk
  showLegend: false,                     // tek seri varsa efsane gürültüdür
  showValue: true, dataLabelPosition: 'outEnd',
  dataLabelFontFace: BODY, dataLabelFontSize: 11, dataLabelColor: INK,
  catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
  catAxisLabelFontFace: BODY, valAxisLabelFontFace: BODY,
  valGridLine: { color: RULE, size: 1 },
  catGridLine: { style: 'none' },
}
```

- Yığılmış grafikte `dataLabelPosition` yalnız `ctr` / `inEnd` / `inBase`
  olabilir; `outEnd` dosyayı bozar.
- İkincil eksenli kombo grafikte `valAxes` **ve** `catAxes`'ı ikişer girdiyle
  birlikte tanımla; yoksa PowerPoint dosyayı bozuk sayar.
- Bir slaytta bir grafik, bir bulgu. On serilik bir grafik veri çöplüğüdür;
  hikâyeyi taşıyan seriyi vurgu rengiyle, diğerlerini `muted` ile boya.
- Sankey, ağ, chord gibi PowerPoint'te karşılığı olmayan tipler görsel olarak
  girer — onları `render_html.py` ile üret.
