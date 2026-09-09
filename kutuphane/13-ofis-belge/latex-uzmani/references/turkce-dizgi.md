# Türkçe Dizgi Referansı

Türkçe LaTeX'te sorunların çoğu "derlenmiyor" değil, **sessizce yanlış derleniyor** biçimindedir: harf düşer, başlık `I` olur, satır yanlış bölünür. Bu yüzden Türkçe belgede PDF gözle kontrol edilmeden iş bitmez.

## İçindekiler
1. Motor + dil paketi kombinasyonları
2. ı/İ ve büyük harf tuzağı
3. babel-turkish shorthand tuzağı
4. Hece bölme
5. Tırnak, tire, kesme işareti
6. Sayı, tarih, birim
7. Başlık ve etiket çevirileri
8. Font kapsaması ve test satırı
9. Çift dilli (TR+EN) belge kurulumu

---

## 1. Motor + dil paketi kombinasyonları

**XeLaTeX / LuaLaTeX (Türkçe için varsayılan tercih):**

```latex
\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{turkish}
\setmainfont{DejaVu Serif}      % Türkçe glifleri tam olan bir font
\usepackage{csquotes}
```

`inputenc` ve `fontenc` **kullanılmaz**. UTF-8 zaten yerleşiktir.

**pdfLaTeX (dergi sınıfı dayattığında):**

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}     % TeX Live 2018+ için gereksiz ama zararsız; eski sistemlerde şart
\usepackage[shorthands=off,turkish]{babel}
\usepackage{lmodern}            % T1 ile bitmap font sorununu önler
\usepackage{csquotes}
```

`lmodern` yoksa Computer Modern'in bitmap sürümü devreye girer, PDF'te ğ/ş bulanık çıkar.

**polyglossia mı babel mi:** XeLaTeX/LuaLaTeX ile polyglossia; pdfLaTeX ile babel. Karıştırma — ikisini aynı belgede yükleme.

## 2. ı/İ ve büyük harf tuzağı

Türkçe'de `i`'nin büyüğü `İ`, `ı`'nın büyüğü `I`'dır. LaTeX varsayılan olarak İngilizce kuralını uygular ve `i → I` üretir. Nerede patlar:

- `\MakeUppercase{...}` ve `\uppercase`
- Otomatik büyüten bölüm başlıkları (`titlesec` ile `\MakeUppercase` tanımlı stiller, birçok tez şablonu, `moderncv` bazı stilleri)
- `\textsc` (küçük kapiteller) — `i` düşer veya yanlış görünür
- Üstbilgi/altbilgi (`fancyhdr` içindeki `\leftmark`, `\rightmark` çoğu sınıfta büyütülür)

**Çözüm sırası:**

1. Dil paketi yüklüyse `babel-turkish`/`polyglossia` Türkçe büyütmeyi büyük ölçüde halleder — önce onun yüklü ve **aktif** olduğunu doğrula (`\selectlanguage{turkish}` yapılmışsa).
2. Yetmiyorsa büyütmeyi kaldır: başlık stilini `\MakeUppercase` içermeyecek şekilde yeniden tanımla. Genelde en temiz çözüm budur.
3. Tek tek yerlerde: büyük harf gerekiyorsa metni elle `İSTANBUL` gibi yaz, makroya bırakma.

**Doğrulama:** PDF'te içeriğinde `i` geçen bir başlık ara (örn. "Giriş", "İlgili Çalışmalar"). `GIRIŞ` görüyorsan hata var, `GİRİŞ` olmalı.

## 3. babel-turkish shorthand tuzağı

babel-turkish varsayılan olarak `=`, `:`, `!` karakterlerini "kısayol" (shorthand) yapar. Sonuç:

- `tikz` çizimlerinde `\draw (a) -- (b);` içindeki `:` patlar
- `tabular` içinde `:` kullanan sütun tanımları bozulur
- `\url{}` ve dosya yollarındaki `:` kırılır
- `siunitx`, `pgfplots`, `listings` seçenekleri hata verir
- Matematik modunda `a:b` beklenmedik boşluk üretir

**Her zaman `shorthands=off` ile yükle:**

```latex
\usepackage[shorthands=off,turkish]{babel}
```

Kapatınca kaybettiğin tek şey `"` tabanlı tireleme yardımıydı; onu `\-` ile elle yapabilirsin.

Semptom tanıma: "TikZ kodum başka belgede çalışıyordu, bu belgede patlıyor" → önce shorthand'lere bak.

## 4. Hece bölme

Türkçe tireleme kalıpları yüklenmezse LaTeX İngilizce kurallarıyla böler ("çalış-ma" yerine "ça-lışma" gibi yanlışlar) veya hiç bölmez ve satırlar taşar.

- Dil paketini yükle (yukarıdaki kurulumlar bunu yapar).
- Kontrol: log'ta `Overfull \hbox` sayısı anormal yüksekse veya sağ kenar düzensizse tireleme yüklenmemiş olabilir.
- Tek kelimeyi elle bölmek: `çalış\-ma\-lar`.
- Hiç bölünmesin istenen (kod, URL, marka): `\mbox{...}` veya `\url{}`.
- İki yana yaslamada aşırı boşluk oluşuyorsa `\usepackage{microtype}` belirgin fark yaratır (pdfLaTeX ve LuaLaTeX'te tam, XeLaTeX'te kısmi).

## 5. Tırnak, tire, kesme işareti

| İstenen | Kaynak kod | Not |
|---|---|---|
| “Türkçe tırnak” | `` ``Türkçe tırnak'' `` veya `\enquote{...}` | Düz `"` asla kullanılmaz |
| ‘tek tırnak’ | `` `tek' `` | |
| kısa çizgi (birleşik) | `-` | Türk-İş |
| en dash (aralık) | `--` | 1990--2000 |
| em dash (ara söz) | `---` | Türkçe'de genelde `--` tercih edilir |
| kesme (Ankara'da) | `'` (düz apostrof) | Tipografik istenirse `\textquoteright` |

`csquotes` + `\enquote{}` kullanmak en güvenlisidir: dil değiştiğinde tırnak otomatik doğru şekle döner.

## 6. Sayı, tarih, birim

- Ondalık: virgül. Matematik modunda `$3,14$` fazladan boşluk açar → `$3{,}14$` yaz veya `siunitx` ile `\num{3,14}` (paket `output-decimal-marker={,}` ile yapılandırılır).
- Binlik: `1.250.000` (nokta). `siunitx`'te `group-separator={.}`.
- Tarih: `8 Eylül 2026`. `\today` dil paketi yüklüyse Türkçe basar; basmıyorsa dil aktif değildir.
- Yüzde: Türkçe'de işaret sayıdan **önce** gelir → `%25`. LaTeX'te `\%25` yaz (kaçırılmamış `%` yorum satırı başlatır ve satırın geri kalanı sessizce kaybolur — Türkçe metinlerde çok sık yapılan hata).
- Birim: `\SI{5}{\kilo\gram}` (siunitx) sayı-birim arasında kırılmayan boşluk verir.

## 7. Başlık ve etiket çevirileri

Dil paketi yüklüyse otomatik gelir: Şekil, Tablo/Çizelge, Kaynaklar, İçindekiler, Özet, Bölüm. Gelmiyorsa veya kurum farklı terim istiyorsa:

```latex
\addto\captionsturkish{%
  \renewcommand{\figurename}{Şekil}%
  \renewcommand{\tablename}{Çizelge}%
  \renewcommand{\refname}{Kaynaklar}%
  \renewcommand{\bibname}{Kaynakça}%
  \renewcommand{\abstractname}{Özet}%
  \renewcommand{\contentsname}{İçindekiler}%
}
```

polyglossia ile karşılığı `\gappto\captionsturkish{...}`.

Tez şablonlarında YÖK/üniversite terminolojisi bağlayıcıdır: "Çizelge" mi "Tablo" mu, "Kaynaklar" mı "Kaynakça" mı — şablonun kılavuzuna bak, tahmin etme.

## 8. Font kapsaması ve test satırı

Yeni bir font seçildiğinde şu satırı derleyip PDF'te gözle kontrol et:

```
Ağrı'da şişli çığlık: ĞÜŞİÖÇI ğüşiöçı — İstanbul, Iğdır, 3,14
```

Harf düşüyor veya kutu (`□`) çıkıyorsa font Türkçe'yi kapsamıyor. Bu ortamda güvenli seçenekler: DejaVu Serif/Sans, Latin Modern (`lmodern`), TeX Gyre ailesi, Liberation, FreeSerif. Ticari/dekoratif fontlarda kapsama sık sık eksiktir.

pdfLaTeX'te `T1` kodlaması olmadan `ğ ş ı` doğru çıkmaz veya kopyala-yapıştır bozulur.

## 9. Çift dilli (TR + EN) belge kurulumu

**İki ayrı PDF isteniyorsa (CV, rapor):** ortak `icerik/` ve ortak `.bib`, iki ana dosya (`belge-tr.tex`, `belge-en.tex`), ortak `stil.sty`. Metni iki kez sürdürme; farklı olan sadece dil yükü ve çevrilmiş içerik dosyaları olsun.

**Tek belgede iki dil (özet TR + abstract EN):**

```latex
% polyglossia
\setmainlanguage{turkish}
\setotherlanguage{english}
...
\begin{english}
Abstract text here.
\end{english}
```

```latex
% babel
\usepackage[shorthands=off,english,turkish]{babel}  % son yazılan ana dildir
...
\begin{otherlanguage}{english} Abstract text \end{otherlanguage}
```

Dil geçişi tireleme kurallarını da değiştirir — İngilizce özeti Türkçe dilinde bırakmak satır sonlarını bozar.
