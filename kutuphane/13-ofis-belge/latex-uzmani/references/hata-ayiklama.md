# LaTeX Hata Ayıklama

## Protokol

1. **İlk hatayı çöz.** LaTeX hataları çığ yapar; 40 hatanın 39'u ilkinin sonucudur. Log'un başındaki ilk `!` satırına git.
2. Log'ta `!` satırını ve altındaki `l.<numara>` satırını oku — hata satırı odur (ama gerçek sebep birkaç satır yukarıda olabilir: kapatılmamış ortam, eksik `}`).
3. Çözülmüyorsa **ikiye bölme**: gövdenin ortasına `\end{document}` koy, derle. Hata sürüyorsa sorun üst yarıda, kaybolduysa alt yarıda. 2-3 adımda satıra inersin.
4. Paket şüphesi varsa **MWE** (minimal çalışan örnek) kur: boş belge + sadece o paket + hata veren 3 satır. Çakışma mı, kullanım hatası mı ayrışır.
5. Hâlâ değilse **temizle**: `latexmk -C` (veya `.aux .bbl .toc .out .lof .lot .synctex.gz` sil) ve yeniden derle. "Değişikliğim görünmüyor" vakalarının çoğu bayat yardımcı dosyadır.

## Log okuma

| Satır | Anlamı |
|---|---|
| `! ...` | Gerçek hata, derleme durur |
| `LaTeX Warning: Reference ... undefined` | `\ref` çözülmedi → bir tur daha derle veya `\label` yok |
| `LaTeX Warning: Citation ... undefined` | bibtex/biber çalışmadı veya anahtar yok |
| `Overfull \hbox (12.3pt too wide)` | Metin kenardan taşıyor. 10pt üstü gözle kontrol edilmeli |
| `Underfull \vbox` | Sayfa dolmamış, kozmetik; genelde yok sayılır |
| `Font shape ... not available` | İstenen font varyantı yok, LaTeX benzerini koydu → görsel bozulma olabilir |
| `Missing character: There is no ğ in font ...` | **Font Türkçe'yi kapsamıyor**, harf PDF'te yok. Kritik. |

`Missing character` uyarıları sessizdir ama Türkçe belgede felakettir — `build.py` bunları ayrıca raporlar.

## Sık hatalar ve teşhis

**`! Undefined control sequence.`**
Tanımsız komut: yazım hatası veya paketi yüklenmemiş komut. `l.` satırındaki son komuta bak. Ör. `\includegraphics` → `graphicx` eksik; `\toprule` → `booktabs` eksik; `\SI` → `siunitx` eksik.

**`! Missing $ inserted.`**
Matematik komutu metin modunda kullanılmış: `_`, `^`, `\alpha`, `\times` gibi. Türkçe metinlerde en sık sebebi kaçırılmamış `_` (dosya adı yazarken) — `\_` yaz.

**`! LaTeX Error: File 'xxx.sty' not found.`**
Paket kurulu değil. `references/ortam.md`'deki apt eşlemesine bak. Bu container'da `tlmgr install` çalışmaz (CTAN erişimi yok).

**`! LaTeX Error: Environment xxx undefined.`**
`\begin{align}` için `amsmath`, `\begin{algorithm}` için `algorithm`/`algorithm2e` gibi paket eksik; ya da ortam adı yanlış yazılmış.

**`! Package babel Error: Unknown option 'turkish'.`**
`texlive-lang-european` kurulu değil.

**`! LaTeX Error: Option clash for package xxx.`**
Aynı paket iki farklı seçenekle iki kez yüklenmiş — biri sınıf dosyasının içinden geliyor olabilir. Kendi `\usepackage` satırını kaldır veya `\PassOptionsToPackage{...}{xxx}` ile `\documentclass` **öncesinde** seçeneği geçir.

**`! Too many }'s` / `! Extra }, or forgotten \end{...}`**
Süslü parantez dengesizliği. İkiye bölme uygula. Editörün parantez eşleştirmesini kullan.

**`! Paragraph ended before \xxx was complete.`**
Argüman içinde boş satır var — makro argümanı paragraf kabul etmiyor. Boş satırı kaldır veya makroyu `\long\def` ile tanımla.

**`! Dimension too large` / `! TeX capacity exceeded`**
Genelde `\resizebox`/`tikz` içinde hesaplanamayan boyut veya sonsuz döngüye giren bir tanım. Son eklenen çizim/makroyu geri al.

**`! Misplaced alignment tab character &.`**
Tablo dışında `&` kullanılmış; metinde geçiyorsa `\&` yaz.

**`Runaway argument?`**
Kapatılmayan `{` veya `\begin{...}`. Hemen üstündeki ortama bak.

**`! Package inputenc Error: Unicode character ... not set up`**
XeLaTeX/LuaLaTeX belgesinde `inputenc` yüklenmiş, ya da pdfLaTeX'te fontun desteklemediği karakter var. Türkçe'de: motor kararını gözden geçir.

**Şekil görünmüyor / `File 'sekil.png' not found`**
Yol yanlış (Linux'ta büyük-küçük harf duyarlı!), uzantı yanlış, veya XeLaTeX'e EPS verilmiş (EPS sadece pdfLaTeX'te `epstopdf` ile). `\graphicspath{{sekiller/}}` kullan.

**PDF üretiliyor ama boş / ilk sayfa eksik**
`\end{document}` erken, veya tüm içerik bir float'ta sıkışmış ve `\clearpage` yok.

**Değişiklik PDF'e yansımıyor**
Bayat `.aux`/`.bbl` veya PDF görüntüleyicide dosya kilitli. `latexmk -C` + yeniden derle.

## Overfull hbox avı

```
Overfull \hbox (23.4pt too wide) in paragraph at lines 145--149
```
Sebep sırası: (1) kırılamayan uzun kelime/URL → `\url{}` veya `\seqsplit`, (2) Türkçe tireleme yüklü değil → dil paketi, (3) dar sütun + uzun terim → `\-` ile elle bölme noktası, (4) tablo/şekil sütundan geniş → boyutu düzelt.

10pt altındaki taşmalar görsel olarak fark edilmez, yok sayılabilir. Üstündekiler PDF'te gerçekten kenara taşar.

## Overleaf farkı

Kullanıcı "Overleaf'te çalışıyordu, burada çalışmıyor" derse:
- Overleaf tam TeX Live kurulumudur, bu container'da paket seti sınırlıdır → eksik paket.
- Overleaf varsayılan motoru pdfLaTeX'tir; proje ayarından XeLaTeX seçilmiş olabilir.
- Overleaf `latexmk` kullanır ve bibtex/biber'i otomatik çalıştırır; elle tek tur derlemede kaynakça çıkmaz.
- Tersi durumda ("burada çalışıyor, Overleaf'te çalışmıyor"): Overleaf'in TeX Live sürümü ve dosya adı büyük-küçük harf duyarlılığı.
