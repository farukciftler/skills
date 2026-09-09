# Kaynakça: BibTeX / biblatex

## Karar: hangisi?

| Kullan | Ne zaman |
|---|---|
| **BibTeX** (`\bibliographystyle` + `\bibliography`) | Dergi/konferans şablonu bunu bekliyorsa (IEEE, ACM, Elsevier, LNCS gönderimlerinin çoğu). Gönderim sistemleri `.bbl` ister. |
| **biblatex + biber** | Serbest belgeler, tezler, CV yayın listesi, Türkçe kaynakça, karmaşık gruplama/filtreleme, çok dilli kaynakça |

Şablon ne diyorsa o. "biblatex daha modern" diye IEEE şablonunu değiştirme — editör `.bbl`'i kendi derlemez, biçim bozulur.

## Derleme sırası (en sık hata kaynağı)

```
BibTeX:   pdflatex → bibtex → pdflatex → pdflatex
biblatex: pdflatex → biber  → pdflatex → pdflatex
```
`latexmk` bunu kendi halleder — elle derleme yapma. `scripts/build.py --bib` bunu zorlar.

Boş kaynakça veya `[?]` görüyorsan sebebi neredeyse her zaman: (a) yeterince tur derlenmedi, (b) `.bib` dosya adı yanlış, (c) `\cite` anahtarı `.bib`'te yok, (d) `.bbl`/`.aux` bayat → `latexmk -C` ile temizle.

## Kurulum

**BibTeX:**
```latex
\bibliographystyle{IEEEtran}   % veya plain, abbrv, unsrt, apalike, elsarticle-num, splncs04
\bibliography{kaynaklar}       % kaynaklar.bib — uzantı YAZILMAZ
```

**biblatex:**
```latex
\usepackage[backend=biber,style=numeric,sorting=nyt,maxbibnames=99,giveninits=true]{biblatex}
\addbibresource{kaynaklar.bib}   % uzantı YAZILIR
...
\printbibliography
```

Sık stiller: `numeric` (sayısal), `alphabetic`, `authoryear` (APA benzeri), `ieee`, `apa` (`biblatex-apa` paketi), `iso-authoryear` (TR tezlerde yaygın).

Türkçe kaynakçada dil paketi yüklüyse biblatex "ve", "ss.", "Erişim tarihi" gibi terimleri Türkçe basar; basmıyorsa `\DefineBibliographyStrings{turkish}{...}` ile elle ayarla.

### Doğrulanmış hata: biblatex "Içinde"

biblatex'in `turkish.lbx` dosyasında `in` dizesi küçük harfle (`içinde`) tanımlıdır ve cümle başında `\MakeCapital` ile büyütülür. `\MakeCapital` İngilizce kuralı uygular → kaynakçada **`Içinde`** çıkar, doğrusu `İçinde`'dir. Konferans bildirisi (`@inproceedings`) içeren her Türkçe kaynakçada görülür.

Düzeltme (test edilmiştir):
```latex
\newcommand{\bbxTRicinde}{İçinde}
\DefineBibliographyStrings{turkish}{%
  in = {{\noexpand\protect\noexpand\bbxTRicinde}{i\c{c}inde}},
}
```
Aynı kalıp `\MakeCapital` ile bozulan diğer dizeler için de kullanılır. Kaynakçayı PDF'te gözle kontrol et — bu hata log'a hiçbir uyarı düşürmez.

## `.bib` hijyeni

```bibtex
@article{yilmaz2024derin,
  author  = {Y{\i}lmaz, Ay{\c s}e and {\"O}zt{\"u}rk, Mehmet},
  title   = {Derin {\"O}{\u g}renme ile {T}{\"u}rk{\c c}e Metin S{\i}n{\i}fland{\i}rma},
  journal = {Bilgisayar Bilimleri Dergisi},
  year    = {2024},
  volume  = {12},
  number  = {3},
  pages   = {45--62},
  doi     = {10.1234/bbd.2024.123}
}
```

Kurallar:
- **Büyük harf koruma:** BibTeX çoğu stilde başlığı küçültür. Korunması gereken özel ad/kısaltmayı süslü parantez içine al: `{T}{\"u}rk{\c c}e`, `{BERT}`, `{COVID-19}`. biblatex bunu daha az yapar ama alışkanlık iyidir.
- **Türkçe karakterler:** XeLaTeX/LuaLaTeX + biber ile doğrudan UTF-8 yaz (`Yılmaz, Ayşe`). pdfLaTeX + BibTeX ile TeX kaçışları güvenlidir (`Y{\i}lmaz`) — özellikle `ı` ve `İ` bazı BibTeX stillerinde UTF-8 olarak patlar.
- Sayfa aralığı `--` (en dash), tek tire değil.
- `author` alanında yazarlar `and` ile ayrılır, virgülle değil. `Soyad, Ad` biçimi çok isimli/ekli soyadlarda güvenlidir.
- Kurum yazarı: `author = {{Türkiye İstatistik Kurumu}}` — çift parantez, yoksa "Kurumu, Türkiye İstatistik" olur.
- DOI varsa yaz; URL sadece DOI yoksa. `urldate`/`note` ile erişim tarihi.
- Google Scholar'dan alınan girdiler eksik/yanlış olur (dergi adı kısaltılmış, sayfa yok, "et al." yazar alanında). Yayıncının kendi BibTeX'ini tercih et; arXiv için `@misc` + `eprint`/`archivePrefix`.
- Anahtar biçimi tutarlı olsun: `soyadYILanahtar`. Aynı anahtar iki kez tanımlanırsa sessizce biri kazanır.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Kaynakça hiç çıkmıyor | `\printbibliography`/`\bibliography` yok, veya biber/bibtex hiç çalışmadı |
| `[?]` veya `Citation undefined` | Anahtar `.bib`'te yok / yazım hatası; ya da tek tur derlendi |
| Sadece atıf yapılanlar çıkıyor, hepsini istiyorum | `\nocite{*}` ekle |
| `Package biblatex Error: Incompatible package` | `natbib` ile biblatex birlikte yüklenmiş; biri kaldırılır |
| `biber: Cannot find 'x.bcf'` | Önce LaTeX derlenmemiş veya dosya adı yanlış; `latexmk -C` sonra tekrar |
| Türkçe karakterler kaynakçada bozuk | pdfLaTeX+BibTeX'te UTF-8 kullanılmış → TeX kaçışına çevir, veya biber'e geç |
| Yazar adı `A. Yılmaz` yerine `Ayşe Y.` | `giveninits`/stil ayarı; `Soyad, Ad` biçimi kullanılmamış |
| Aynı kaynak iki kez listeleniyor | İki farklı anahtarla girilmiş; `.bib`'i DOI üzerinden tekilleştir |

## Kaynakçayı gönderim öncesi denetle

- `.bbl` dosyasını aç ve gözle oku — çıktının nihai hâli odur.
- Her kaynakta yıl, dergi/konferans adı ve sayfa/DOI var mı?
- Dergi adı kısaltma politikası tutarlı mı (hepsi tam veya hepsi kısaltılmış)?
- Metin içi atıf sayısı ile kaynakça uzunluğu tutuyor mu (`\nocite{*}` unutulmuş olabilir)?
