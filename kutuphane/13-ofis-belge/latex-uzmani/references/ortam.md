# Ortam, Kurulum ve Motor Davranışı

## Bu container'da ne var

TeX Live (Debian paketleri) kurulu. Motorlar: `pdflatex`, `xelatex`, `lualatex`, `latexmk`. Kaynakça: `bibtex`, `biber`.

Tipik olarak hazır gelen paket setleri:
`texlive-base`, `texlive-latex-base`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-pictures`, `texlive-science`, `texlive-xetex`.

Bunlarla gelen sık kullanılanlar: `graphicx`, `booktabs`, `siunitx`, `cleveref`, `hyperref`, `geometry`, `titlesec`, `multirow`, `subcaption`, `xcolor`, `tcolorbox`, `listings`, `algorithm2e`, `natbib`, `caption`, `todonotes`, `microtype`, `csquotes`, `enumitem`, `fontspec`, `polyglossia`, `tikz`, `pgfplots`, `moderncv`, `koma-script`.

**Kurulu olduğunu varsayma — kontrol et:**
```bash
kpsewhich paketadi.sty    # boş dönerse yok
kpsewhich sinifadi.cls
```

## Eksik paket → apt eşlemesi

CTAN'a ağ erişimi yoktur; **`tlmgr install` çalışmaz**. Eksik olan apt ile gelir:

| Paket / sınıf | apt paketi |
|---|---|
| `IEEEtran`, `acmart`, `elsarticle`, `llncs`, `sig-alternate` | `texlive-publishers` |
| `biblatex`, `biblatex-apa`, ek `.bst` stilleri | `texlive-bibtex-extra` |
| `biber` | `biber` |
| `babel-turkish`, diğer Avrupa dilleri | `texlive-lang-european` |
| `fontawesome5`, ek metin fontları | `texlive-fonts-extra` (büyük, ~500 MB) |
| Arapça/İbranice desteği | `texlive-lang-arabic` |
| Genel eksikler | `texlive-latex-extra`, `texlive-science` |
| Her şey (son çare, çok büyük) | `texlive-full` |

```bash
apt-get install -y texlive-publishers texlive-bibtex-extra biber texlive-lang-european
```

Kurulum uzun sürebilir; arka plana atma — bash aracı dönerken arka plan süreci ölür. Önplanda `timeout` ile çalıştır.

Kurulum sonrası doğrula: `kpsewhich IEEEtran.cls`.

Paket apt'ta da yoksa: kullanıcıya durumu söyle, belgeyi **Overleaf'te derlenecek** biçimde teslim et ve o paketi devre dışı bırakan bir yerel önizleme sürümüyle içeriği yine de doğrula. "Muhtemelen derlenir" deme.

## Fontlar

`fc-list : family` ile sistem fontlarını listele. Türkçe gliflerini tam kapsayan güvenli seçenekler: **DejaVu Serif/Sans/Sans Mono**, **Latin Modern** (`lmodern`, TeX Gyre), **Liberation**, **FreeSerif**, **Bitstream Charter**, **Carlito**/**Caladea** (Calibri/Cambria metrik uyumlu).

`fontspec` ile font adı **tam olarak** `fc-list` çıktısındaki gibi yazılır:
```latex
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
```
Font bulunamazsa XeLaTeX hata verir (sessiz geçmez) — hata mesajı net değilse `fc-list | grep -i ad` ile doğrula.

Yeni font seçildiğinde `turkce-dizgi.md` §8'deki test satırını derleyip gözle kontrol et.

## Motor davranış farkları

| | pdfLaTeX | XeLaTeX | LuaLaTeX |
|---|---|---|---|
| Sistem fontu (`fontspec`) | Hayır | Evet | Evet |
| `inputenc`/`fontenc` | Gerekli (T1) | Kullanma | Kullanma |
| EPS şekil | `epstopdf` ile evet | Hayır (PDF'e çevir) | Hayır |
| `microtype` | Tam | Kısmi | Tam |
| Hız | En hızlı | Orta | En yavaş |
| Dil paketi | `babel` | `polyglossia` (veya babel) | `polyglossia` |
| `minted`/kabuk erişimi | `-shell-escape` gerekir | aynı | aynı |

`minted` kullanılıyorsa `pygmentize` kurulu olmalı ve derleme `-shell-escape` ile yapılmalı; yoksa `listings`'e geç (bağımlılığı yok, gönderim sistemlerinde daha güvenli).

## Derleme

Her zaman `latexmk` (veya `scripts/build.py`) kullan — tur sayısını, bibtex/biber'i ve yeniden derlemeyi kendi yönetir.

```bash
latexmk -pdf belge.tex                 # pdflatex
latexmk -pdfxe belge.tex               # xelatex
latexmk -pdflua belge.tex              # lualatex
latexmk -C                             # tüm yardımcı dosyaları temizle
latexmk -pdf -interaction=nonstopmode  # hata olsa da durmadan devam et (log incelemek için)
```

## Çıktı doğrulama araçları

```bash
pdfinfo belge.pdf        # sayfa sayısı, sayfa boyutu, metadata
pdffonts belge.pdf       # font gömme (hepsi "yes"), Type3 var mı
pdftotext belge.pdf -    # metin çıkarımı — ATS ve kopyalanabilirlik testi
```

`pdftotext` çıktısında Türkçe karakterler bozuksa PDF'te font kodlaması sorunludur; kaynakta doğru görünse bile düzeltilmeli (özellikle CV'de kritik).
