# Makale / Tez Dizgi Referansı

## Sınıf hızlı kartları

### IEEEtran (IEEE dergi ve konferansları)
```latex
\documentclass[conference]{IEEEtran}   % dergi için: [journal] veya seçeneksiz
\usepackage[T1]{fontenc}
\usepackage{cite}                      % biblatex DEĞİL — IEEE gönderiminde BibTeX bekleniyor
\bibliographystyle{IEEEtran}
```
- Çift sütun varsayılan. Geniş şekil/tablo için `figure*` / `table*` (sayfanın üstüne düşer, `[t]` dışında yer bulamaz).
- Motor: **pdfLaTeX**. XeLaTeX ile de derlenir ama gönderimde sorun çıkarabilir.
- `\thanks{}` fon bilgisi için; anonim gönderimde kaldırılır.
- Sayfa limiti kesindir ve kaynakça dahildir (konferansa göre değişir).

### acmart (ACM konferans/dergi)
```latex
\documentclass[sigconf,review,anonymous]{acmart}  % kabul sonrası: [sigconf]
\acmConference[KISALTMA '26]{Tam Ad}{Tarih}{Yer}
\begin{abstract}...\end{abstract}
\begin{CCSXML}...\end{CCSXML}   % ACM CCS sınıflandırması ZORUNLU
\keywords{...}
```
- `review` seçeneği satır numarası ekler, `anonymous` yazarları gizler. Kabul sonrası ikisi de kaldırılır ve telif bloğu (`\setcopyright`, `\acmDOI`...) editörden gelen değerlerle doldurulur.
- Şablon güncel olmadan gönderim reddedilir; sürümü ACM sayfasından doğrula.

### elsarticle (Elsevier dergileri)
```latex
\documentclass[preprint,12pt]{elsarticle}   % gönderim: preprint/review; final: 1p, 3p, 5p
\begin{frontmatter}
\title{...}
\author[a]{Ad Soyad}
\affiliation[a]{organization={...}, city={...}, country={...}}
\begin{abstract}...\end{abstract}
\begin{keyword} kelime \sep kelime \end{keyword}
\end{frontmatter}
```
- `\bibliographystyle{elsarticle-num}` veya `elsarticle-harv` (dergiye göre).
- Elsevier "highlights" ve "graphical abstract" ayrı dosya ister; ana `.tex`'e gömme.

### llncs (Springer LNCS)
```latex
\documentclass{llncs}
\bibliographystyle{splncs04}
```
- Yazar/kurum eşlemesi `\institute{}` içinde `\and` ile; ORCID `\orcidID{}`.
- Sayfa limiti sıkıdır; `llncs` kenar boşluklarını değiştirmek yasaktır.

### Tez şablonları (üniversite)
- Üniversitenin kendi `.cls`/`.sty` dosyası bağlayıcıdır; kenar boşluğu, satır aralığı, kapak, onay sayfası ve "Çizelge/Şekil" terminolojisi enstitü kılavuzuna göre kilitlidir.
- Şablon eskiyse (TeX Live'ın yeni sürümüyle patlıyorsa) sınıfı değiştirme, uyumsuz paketi izole et — enstitü biçim kontrolünde şablon dışı çıktı geri döner.
- Türkçe tezlerde `turkce-dizgi.md` kuralları + enstitünün terim tercihi birlikte uygulanır.

## Yerleşim ve kayan nesneler

- Konum: `\begin{figure}[htbp]`. `[H]` (`float` paketi) akışı kilitler ve büyük boşluklar üretir — son çare.
- Şekil "yanlış yere gidiyor" şikayetinin çözümü genelde yeri zorlamak değil, şekli küçültmek veya metin bloğunu yeniden bölmek.
- Çift sütunda tam genişlik: `figure*`. Bu float sadece sayfa üstüne yerleşebilir; sayfanın ortasında istersen `stfloats`/`dblfloatfix` gerekir.
- Sayfanın sonunda biriken float yığını: `\clearpage` ile boşalt, ama bölüm ortasında kullanma.
- `\label` **daima** `\caption`'dan sonra gelir; önce yazarsan numara yanlış çıkar (`??` değil, *sessizce yanlış*).

## Tablolar

- `booktabs` kullan: `\toprule`, `\midrule`, `\bottomrule`. Dikey çizgi ve `\hline` yığını akademik dizgide kötü görünür.
- Sayı hizalama: `siunitx`'in `S` sütunu (`\begin{tabular}{l S[table-format=2.2]}`) ondalık noktaya hizalar.
- Geniş tablo: önce `\small`, sonra sütun eleme, sonra `adjustbox`/`\resizebox` (yazı boyutu tutarsızlaşır, son çare), sonra `landscape`.
- Uzun tablo (sayfa aşan): `longtable` (tek sütun) — çift sütun düzeninde çalışmaz, `supertabular` veya `figure*` gerekir.
- Başlık tabloda **üstte**, şekilde **altta** (çoğu dergi kuralı).

## Matematik

- `amsmath` + `amssymb` her zaman. `eqnarray` kullanma (bozuk boşluk üretir) → `align`, `gather`, `equation`.
- Numaralanmasın: `align*`, `equation*` veya `\nonumber`.
- Metin içi birim/değişken: metin modunda `x` yazma, `$x$` yaz.
- Uzun denklem kırma: `split` içinde `align`.
- Referans: `\eqref{}` (parantezli), `cleveref` ile `\cref{}`.

## Çapraz referans ve atıf

```latex
\usepackage[hidelinks]{hyperref}   % hyperref DAİMA en son yüklenir (cleveref hariç)
\usepackage{cleveref}              % hyperref'ten SONRA
```
- `\cref{fig:sonuc}` → "Şekil 3" metnini kendi üretir; Türkçe için `\crefname{figure}{Şekil}{Şekiller}`.
- Bağlamayı kırma: `Şekil~\ref{...}` — `~` kırılmayan boşluktur, satır sonunda ayrılmayı önler.
- Etiket önekleri tutarlı olsun: `fig:`, `tab:`, `eq:`, `sec:`, `alg:`.

## Anonim (blind) gönderim kontrol listesi

- [ ] Yazar adları, kurumlar, e-postalar kaldırıldı (sınıfın `anonymous`/`review` seçeneği)
- [ ] Teşekkür ve fon/proje numaraları kaldırıldı
- [ ] Kendi atıfları üçüncü şahıs: "our previous work [7]" değil, "Yılmaz et al. [7]"
- [ ] GitHub/veri linkleri anonimleştirildi (anonymous.4open.science vb.)
- [ ] PDF metadata temiz: `pdfinfo makale.pdf` ile Author/Creator alanlarına bak; `hyperref`'in `pdfauthor` alanı doldurulmasın
- [ ] Dosya adı yazar adı içermiyor

## Sayfa limitine sığdırma (meşru yollar)

Sırayla dene, dergi kurallarını çiğneyenleri (satır aralığı/kenar boşluğu/font boyutu değiştirme) yapma:

1. Şekil boyutlarını küçült, boş alanları kırp (`\includegraphics[trim=...,clip]`)
2. Gereksiz float'ları birleştir (`subcaption` ile yan yana)
3. Tabloları sıkılaştır (`\setlength{\tabcolsep}`, gereksiz sütun at)
4. Kaynakça stilini kısalt (dergi izin veriyorsa `abbrv`, `maxbibnames`)
5. Metni gerçekten kısalt — en dürüst yol
6. `\vspace{-...}` hack'i: son çare, gözle kontrol et, hakem fark eder

## Gönderim öncesi teknik kontroller

```bash
pdffonts makale.pdf     # tüm fontlar "yes" (embedded) olmalı, Type3 olmamalı
pdfinfo makale.pdf      # sayfa sayısı, sayfa boyutu (A4 vs Letter!), metadata
```
- Type3 font çıkıyorsa: `lmodern` yükle veya bitmap font kullanan bir paketi değiştir. Birçok dergi Type3'ü reddeder.
- Sayfa boyutu: IEEE/ACM Letter, çoğu Avrupa dergisi A4. Yanlış boyut otomatik kontrolde takılır.
- Şekiller vektör olsun (PDF/EPS); raster gerekiyorsa ≥300 dpi.
- Gönderim paketi tek klasör: `.tex`, `.bib` **ve** `.bbl`, şekiller, sınıf dosyası. Birçok sistem `.bbl` ister çünkü kendi tarafında bibtex çalıştırmaz.
