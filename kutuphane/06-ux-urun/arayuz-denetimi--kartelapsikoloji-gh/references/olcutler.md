# Ölçütler — eşikler ve hesaplar

## Kontrast (WCAG 2.2)

| içerik | AA | AAA |
|---|---|---|
| gövde metni (<18.66px, veya <14px kalın) | 4.5:1 | 7:1 |
| büyük metin (≥18.66px, ya da ≥14px kalın) | 3:1 | 4.5:1 |
| arayüz bileşeni kenarı, ikon, grafik | 3:1 | — |
| odak göstergesi (1.4.11 + 2.4.11) | 3:1 komşu renge karşı | — |
| devre dışı öğe | muaf | — |

**Bağıl parlaklık.** sRGB kanalını 0–1'e indir, `c ≤ 0.03928 ? c/12.92 :
((c+0.055)/1.055)^2.4`, sonra `L = 0.2126R + 0.7152G + 0.0722B`.
Oran = `(L_açık + 0.05) / (L_koyu + 0.05)`.

Yarı saydam katman varsa önce arka planla harmanla — `getComputedStyle` dönen
`rgba` değerini olduğu gibi kullanmak yanlış sonuç verir. Etkin arka planı
bulmak için öğeden köke doğru yürü, ilk opak `background-color`'ı bul.

```python
def bagil_parlaklik(rgb):
    def k(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (k(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def oran(on, arka):
    a, b = bagil_parlaklik(on), bagil_parlaklik(arka)
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)
```

## Dokunma hedefi

| kaynak | eşik |
|---|---|
| WCAG 2.2 · 2.5.8 (AA) | 24×24 CSS px, ya da 24px çapında çakışmayan alan |
| Apple HIG | 44×44 pt |
| Material | 48×48 dp |
| **Kartela (`CONTRACT.md §7`)** | `pointer: coarse` altında `--dokunma` = **44px** |

Bu projede bağlayıcı olan 44px'tir. Hedefler arası açıklık ≥8px olmalı; bitişik
iki 44px hedef, aralarında boşluk yoksa tek büyük hedef gibi yanlış dokunuş üretir.

Ölçüm `getBoundingClientRect()` ile yapılır; görsel olarak küçük ama `padding`
ile büyütülmüş hedef geçerlidir, `::after` ile genişletilen tıklama alanı da
geçerlidir (`getBoundingClientRect` yakalamaz — o durumda pseudo öğeyi ayrı
kontrol et).

## Kırılma noktaları (`CONTRACT.md §7`)

| kuşak | genişlik | temsili cihaz |
|---|---|---|
| xs | <480 | iPhone SE/14 dikey |
| sm | 480–767 | büyük telefon dikey, küçük telefon yatay |
| md | 768–1023 | iPad dikey |
| lg | 1024–1439 | **iPad yatay**, küçük dizüstü |
| xl | ≥1440 | masaüstü |

Kural: **xs/sm'de oda ızgarası render edilmez** — yerine ajanda listesi.

Sınır değerlerinde ayrıca bak: 479/480, 767/768, 1023/1024, 1439/1440.
Kusurların çoğu tam sınırda çıkar.

## Yoğunluk

| mod | satır | dokunma |
|---|---|---|
| `rahat` (öntanımlı) | 48px | 44px |
| `siki` | 32px | 44px (coarse altında) |

Metin tabanı hiçbir yoğunlukta **11.5px** altına inmez (`--metin-mikro`).

## Tipografi ve okunabilirlik

- Gövde satır yüksekliği ≥1.5, paragraf arası ≥1.5× yazı boyutu (WCAG 1.4.12).
- Ölçü (satır uzunluğu) 45–75 karakter. `--col: 740px` bunu hedefler.
- iOS'ta girdi yazı boyutu **≥16px** olmalı, aksi hâlde odakta sayfa yakınlaşır.
- Türkçe uzun bileşik adlar (`Rana Betül Uysal`, `Zeynep Türkyılmaz`) taşma
  üretir; `min-width: 0` + `overflow-wrap: anywhere` ızgara/flex çocuklarında
  gerekir. Ellipsis kullanılacaksa tam değer `title` ile erişilebilir kalmalı.
- Para ve saat: `font-variant-numeric: tabular-nums` zorunlu.

## Kırpma: kutu değil, mürekkep ölç

`scrollHeight > clientHeight` kırpmanın **güvenilmez** ölçüsüdür. İki durumda
sessizce yanlış cevap verir:

1. `align-content: center` + `overflow: hidden` — taşma alta ve üste eşit
   bölünür, `scrollHeight` yalnız alt taşmayı sayar, sonuç "taşma yok" çıkar.
2. Izgara/flex çocuğu doğal satır kutusundan **sıkıştırılmışsa** —
   `getBoundingClientRect().height` sıkışmış değeri verir, glif mürekkebi ise
   sıkışmaz ve dışarı taşar.

Türkçe bunu ağırlaştırır: `ç ğ ş y j` altı uzantılıdır, `İ Ğ Ş` üstü. İngilizce
gövde metninde fark etmeyen 2–3px, Türkçe'de her satırda görünür.

Doğru ölçüm — canvas ile gerçek glif kutusu:

```js
const cs = getComputedStyle(oge);
const c = document.createElement('canvas').getContext('2d');
c.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
const m = c.measureText(oge.textContent);
const murekkep = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent;
const kutu = oge.getBoundingClientRect().height;
// murekkep > kutu  →  kirpiliyor
```

Kesin karar için **ekran görüntüsünü büyütüp bak** — kırpma her zaman piksel
düzeyinde görülür, hesapta görülmeyebilir:

```bash
python3 -c "from PIL import Image; im=Image.open('ss/x.png'); \
  im.crop((300,330,900,530)).resize((1200,400), Image.LANCZOS).save('kirp.png')"
```

Somut örnek (bu projede ölçüldü): `.k-izgara__hucre` 32px (`siki` yoğunluk),
dolgu 3px → blok 25px, iç 21px. İki satır `gap: 1px` ile 10+1+10'a **sıkıştı**;
oysa `line-height` 17.8px, glif mürekkebi 13px. Satır başına 3px mürekkep
`overflow: hidden` altında kesildi. `scrollHeight` bunu hiç görmedi.

## Yeniden akış ve yakınlaştırma (WCAG 1.4.10)

320 CSS px genişlikte (yani 1280px ekranda %400 yakınlaştırma) içerik iki yönlü
kaydırma gerektirmeden okunabilmeli. Tablo ve harita muaf değildir — kendi
kabında yatay kaydırabilir, ama **sayfa gövdesi** yatay kaydırmamalı.

Test: viewport'u 320×512 yap, `scrollWidth > clientWidth` kontrol et.

## Metin aralığı (WCAG 1.4.12)

Şu değerleri enjekte edince içerik kesilmemeli:

```css
* { line-height: 1.5 !important; letter-spacing: 0.12em !important;
    word-spacing: 0.16em !important; }
p { margin-bottom: 2em !important; }
```

Sabit yükseklikli kart/rozet varsa burada patlar.

## Hareket

`prefers-reduced-motion: reduce` altında geçiş ve animasyon süresi ~0'a inmeli;
parallax, otomatik kaydırma, yanıp sönme durmalı. 5 saniyeden uzun otomatik
hareketin duraklatma denetimi olmalı (2.2.2).

## Konsol ve ağ sağlığı

Denetim sırasında **sıfır** konsol hatası hedeflenir. Özellikle:
- React hidrasyon uyuşmazlığı (statik export + tema/yoğunluk okuması)
- `key` uyarısı — liste yeniden sıralamada durum karışması demektir
- 404 varlık (ikon, manifest, sw.js)
- iptal edilmiş fetch (`autoCancellation(false)` olduğu için beklenmez)

## Hızlı komutlar

```bash
# tanımsız CSS token avı
grep -rho 'var(--[a-z0-9-]\+' web/app web/components web/styles \
  | sed 's/var(//' | sort -u > /tmp/kullanilan.txt
grep -ho '^\s*--[a-z0-9-]\+' web/styles/kartela.css | tr -d ' ' | sort -u > /tmp/tanimli.txt
comm -23 /tmp/kullanilan.txt /tmp/tanimli.txt      # Tailwind tokenları hariç, kalanlar şüpheli

# 100vh kullanımı (mobilde tarayıcı çubuğu sorunu)
grep -rn '100vh' web/styles web/app web/components

# sabit px yazı boyutu (token dışı)
grep -rn 'font-size:\s*[0-9]' web/styles
```
