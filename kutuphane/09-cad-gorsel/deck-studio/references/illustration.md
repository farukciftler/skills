# İllüstrasyon, diyagram ve doku

Bu skill fotoğraf üretmez. Ürettiği şey vektör: kavramsal illüstrasyon,
sistem diyagramı, doku, ve tipografik kompozisyon. Hepsi SVG veya HTML olarak
yazılır ve `render_html.py` ile PNG'ye alınır.

Kural: **illüstrasyon slaytın argümanının bir parçası olmalı.** Süslemek için
çizilen soyut şekiller boşluğu doldurur ama slaytı zayıflatır. Çizecek bir
şeyin yoksa çizme; tipografiyi büyüt.

## Neyi nasıl çizmeli

| İhtiyaç | Yöntem |
|---|---|
| Sistem/mimari diyagramı | SVG, kutu + ok, paletten iki renk, tek yön |
| Kavramsal illüstrasyon | Geometrik soyutlama veya izometrik sahne |
| Süreç akışı | Slaytın kendisinde (G arketipi), ayrı görsel değil |
| Doku / zemin | SVG `feTurbulence` grain veya CSS mesh degrade |
| Kapak tipografisi | HTML + `clip-path` / `mix-blend-mode`, PNG olarak |
| Harita, ağ, Sankey | SVG; pptxgenjs'te karşılığı yok |

## Temel iskelet

Her illüstrasyonu bu iskeletle başlat — token'ları `DECK.md`'den kopyala,
uydurma:

```html
<!doctype html><meta charset="utf-8"><style>
  :root{ --ink:#14140F; --paper:#F4F1EC; --accent:#9E3B1F; --muted:#7C7A6E; }
  html,body{margin:0;background:transparent}
  #art{width:1200px;height:800px;position:relative}
</style>
<div id="art"> ... </div>
```

Sonra `python scripts/render_html.py art.html art.png --selector "#art"
--transparent --scale 2`. Şeffaf üret; slayt zemini görünsün.

## Diyagramlar

İyi bir sistem diyagramı üç şey yapar: akışın yönünü belli eder, katmanları
ayırır, ve isimlendirmeyi gerçek dünyadan alır.

- **Tek yön.** Soldan sağa veya yukarıdan aşağı. Okların yön değiştirdiği
  diyagram okunmaz.
- **En fazla üç kademe derinlik.** Daha fazlası varsa iki slayta böl.
- **Renk bilgi taşısın.** Vurgu rengi yalnız hikâyenin geçtiği yolda; geri
  kalan her şey `muted`. Her kutuyu farklı renge boyamak bilgi değil gürültüdür.
- **Ok uçları küçük.** 8-10px yeter; büyük oklar amatör durur.
- **Etiketler kutunun içinde.** Dışarı taşan etiketler slayt küçüldüğünde
  çakışır.

Ok işaretleyici için kullanılabilir SVG parçası:

```svg
<defs>
  <marker id="a" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/>
  </marker>
</defs>
<path d="M120,90 H280" stroke="var(--muted)" stroke-width="1.5" marker-end="url(#a)"/>
```

## İzometrik sahneler

Bir altyapıyı, katmanlı mimariyi veya "sistem" fikrini anlatmanın en okunaklı
yolu. Projeksiyon matematiği basit — 2:1 izometri:

```
ekranX = (x - y) * cos(30°) * s        ≈ (x - y) * 0.866 * s
ekranY = (x + y) * sin(30°) * s - z*s  ≈ (x + y) * 0.5   * s - z*s
```

Bir kutunun üç yüzü üç ton alır: üst `%100`, sol `%82`, sağ `%64` parlaklık.
Tek bir taban renginden türet, üç ayrı renk seçme. Kutuları **arkadan öne**
çiz (yüksek `x+y` sona), yoksa üst üste binme yanlış olur.

Izgara zeminin altına ince eşkenar dörtgen ızgara koymak sahneyi oturtur;
çizgi kalınlığı 0.75px, renk `muted` üzerinde %20 opaklık.

## Geometrik soyutlama

İzometri fazla teknikse: tek bir geometrik birim seç (daire, eşkenar dörtgen,
yay, dikey çubuk) ve onu bir kurala göre tekrar et — büyüyen dizi, yoğunlaşan
grid, dönen kademe. Kural içerikten gelmeli: büyüme anlatıyorsan dizi büyür,
dağılım anlatıyorsan yoğunluk değişir.

Rastgele yerleştirilmiş "soyut şekiller" kompozisyonu yapma; tekrarlanan
kural ile rastgelelik arasındaki fark, tasarım ile dekorasyon arasındaki
farktır.

## Doku ve zemin

**Grain (Arşiv yönü için).** Metnin *arkasına*, düşük opaklıkla:

```svg
<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8"
  numOctaves="3" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/></filter>
<rect width="100%" height="100%" filter="url(#g)" opacity="0.07"/>
```

**Mesh degrade.** pptxgenjs gradyan çizemediği için zemin PNG olarak üretilir:

```css
background:
  radial-gradient(60% 50% at 18% 22%, #2A4C41 0%, transparent 60%),
  radial-gradient(50% 45% at 82% 78%, #9E3B1F 0%, transparent 62%),
  #0E1512;
```

1600x900'de üret, `slide.background = { path: 'bg.png' }` ile ver. Renkler
paletten; mor→mavi kombinasyonuna asla düşme.

**Kılcal kural sistemi (Bilanço yönü).** 0.75pt, `rule` rengi, tutarlı dikey
ritim. Kalınlaştırma; 1pt'yi geçen çizgi tabloyu ağırlaştırır.

## Kapak tipografisi

Bazı tipografik etkiler pptxgenjs'te yok: harf içine görsel kırpma, karışım
modu, taşan/kesilmiş harf, değişken font ekseni. Bunlar HTML'de yapılır ve
PNG olarak slayta girer.

```css
h1{ font:800 190px/0.86 'Anton'; letter-spacing:-.03em;
    background:url(doku.jpg) center/cover; -webkit-background-clip:text;
    color:transparent; }
```

Bunu yalnızca kapak ve bölüm ayraçlarında yap — içerik slaytlarındaki metin
düzenlenebilir kalmalı, yoksa müşteri desteyi güncelleyemez.

## Kalite eşiği

Slayta koymadan önce PNG'ye bak:

- Şeffaf mı üretilmiş, kenarda beyaz kutu var mı?
- Slaytta duracağı gerçek boyutta (genelde 5-6 inç) çizgiler görünüyor mu?
  0.5px çizgiler küçülünce kaybolur; minimum 1.25px kullan.
- Palet dışı renk kaçmış mı? Tek bir gri tonu bile yönü bozar.
- Diyagramda okunmayan bir etiket var mı? Slaytta 11pt'nin altına düşen hiçbir
  metin okunmaz.
- Aynı destede iki illüstrasyon yan yana konsa aynı elden çıkmış gibi duruyor
  mu? Çizgi kalınlığı, köşe yarıçapı ve ton mantığı deste boyunca sabit olmalı.
