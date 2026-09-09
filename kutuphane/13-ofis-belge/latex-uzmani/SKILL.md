---
name: latex-uzmani
description: LaTeX dizgi uzmanı — CV/özgeçmiş ve akademik makale/tez odaklı; Türkçe/İngilizce dizgide birinci sınıf (XeLaTeX/LuaLaTeX, polyglossia/babel-turkish, ı/İ tuzakları, hece bölme, TR tırnak ve sayı biçimi), dergi/konferans sınıflarını (IEEEtran, acmart, elsarticle, LNCS, tez şablonları) kurar, BibTeX/biblatex kaynakçasını temizler, gerçekten derleyip PDF üretir ve log'u okuyup hatayı teşhis eder. Kullanıcı "LaTeX", "tex", "Overleaf", "xelatex/pdflatex", "derlenmiyor", "Undefined control sequence", "kaynakça çıkmıyor", "?? çıkıyor", "bibtex/biber", "IEEE formatı", "çift sütun", "tablo taşıyor", "şekil yanlış yere gidiyor", "CV/özgeçmiş hazırla", "akademik CV", "tez şablonu", "Türkçe karakter sorunu" dediğinde kullan. Bir .tex/.bib/.cls dosyası ya da LaTeX log çıktısı paylaşıldığında; bir CV, makale veya tez PDF olarak istendiğinde — kullanıcı "LaTeX" demese bile — devreye gir. Makalenin İÇERİK ve yayın stratejisi `bilimsel-makale-yazimi` skill'ine aittir; bu skill dizgi/mühendislik katmanıdır.
---

# LaTeX Uzmanı

Bu skill LaTeX'in **dizgi ve mühendislik** katmanıdır: kaynağı doğru kur, gerçekten derle, log'u oku, PDF'i doğrula. İçerik/argüman/yayın stratejisi başka bir işin konusudur (`bilimsel-makale-yazimi`).

Temel ilke: **derlenmemiş LaTeX teslim edilmez.** Bu ortamda TeX Live kurulu; her `.tex` çıktısı `scripts/build.py` ile derlenip PDF üretilerek doğrulanır. Derlenemiyorsa bu açıkça söylenir — "muhtemelen çalışır" denmez.

## Çalışma sırası

1. **Bağlamı sabitle** (aşağıdaki 5 soruyu kendi kendine cevapla; belirsizse *tek seferde* kullanıcıya sor, tek tek değil):
   - Dil: TR / EN / ikisi birden?
   - Hedef: CV mi, makale/tez mi, başka bir belge mi?
   - Zorunlu şablon var mı? (dergi/konferans sınıfı, üniversite tez şablonu, iş ilanı formatı)
   - Teslim biçimi: sadece `.tex` kaynak mı, PDF de mi, Overleaf'e yapıştırılacak tek dosya mı?
   - Kısıt: sayfa limiti, anonim (blind) gönderim, ATS uyumu, font zorunluluğu?
2. **Motoru seç** (aşağıdaki tabloya göre). Motor kararı font ve dil paketini belirler; sonradan değiştirmek pahalıdır.
3. **İskeleti kur** — mümkünse `assets/` altındaki şablonlardan başla, sıfırdan preamble yazma.
4. **Derle ve doğrula** — `scripts/build.py`. Hata varsa `references/hata-ayiklama.md` protokolünü uygula.
5. **Denetle** — `scripts/lint.py` + aşağıdaki teslim kontrol listesi. Sonra PDF'i `present_files` ile ver.

## Motor seçimi

| Durum | Motor | Dil paketi | Font |
|---|---|---|---|
| Türkçe metin (varsayılan) | **XeLaTeX** | `polyglossia` + `\setmainlanguage{turkish}` | `fontspec` ile sistem fontu |
| TR + karışık dil (Arapça, matematik ağırlıklı) | **LuaLaTeX** | `polyglossia` | `fontspec` |
| Dergi sınıfı `pdflatex` şart koşuyorsa (IEEEtran, acmart çoğu zaman) | **pdfLaTeX** | `babel` + `[turkish]` | `T1` + `lmodern` |
| Sadece İngilizce, klasik makale | pdfLaTeX yeter | `babel`+`english` | `T1`+`lmodern`/`newtx` |

Kural: **Türkçe varsa `\usepackage[utf8]{inputenc}` + `[T1]{fontenc}` ikilisi pdfLaTeX'te ZORUNLUDUR**; XeLaTeX/LuaLaTeX'te ikisi de kullanılmaz (hata verir veya sessizce bozar). Motor ile paketleri karıştırmak bu işteki bir numaralı hata kaynağıdır.

Dergi şablonu bir motoru dayatıyorsa şablon kazanır — Türkçe rahatlığı için IEEEtran'ı XeLaTeX'e zorlama; `babel` yoluyla çöz.

## Türkçe dizgi — pazarlık edilmeyen kurallar

Türkçe LaTeX'te bozulan şeyler İngilizce'de görünmez. Bu yüzden Türkçe bir belgede şunlar **her seferinde** kontrol edilir (ayrıntı: `references/turkce-dizgi.md`):

- **ı/İ felaketi:** `\MakeUppercase` ve otomatik büyütme (bölüm başlıkları, `\textsc`, bazı CV sınıfları) Türkçe'de `i → I` üretir; doğrusu `i → İ`. Başlıkları otomatik büyüten sınıflarda ya büyütmeyi kapat ya da dil paketinin Türkçe büyütmesini devrede tut. Üretilen PDF'te başlıkları gözle kontrol et.
- **Hece bölme:** Türkçe tireleme kuralları yüklenmezse satır sonları yanlış bölünür. `polyglossia`/`babel` Türkçe dilini yükle, `\language` kilitli kalsın.
- **Tırnak:** Türkçe'de `"...."` değil `“...”` kullanılır; kaynakta `` `` `` ve `''` yaz veya `csquotes` + `\enquote{}` kullan. Düz `"` karakteri asla bırakılmaz.
- **`shorthands`:** babel-turkish `=`, `:`, `!` karakterlerini kısayola çevirir ve TikZ/tablo/matematik içinde patlar. Türkçe belgede daima `\usepackage[shorthands=off,turkish]{babel}` ile aç, ardından gerekli kısayolları elle kur.
- **Font kapsaması:** Seçilen fontta `ğ Ğ ş Ş ı İ ç Ç ö Ö ü Ü` yoksa harfler sessizce düşer. Yeni bir fonta geçildiğinde bu altı çifti test satırıyla dene.
- **Tarih/sayı:** Türkçe'de ondalık ayırıcı virgül (`3,14`), binlik nokta; tarih `8 Eylül 2026`. Matematik modunda virgül ondalık ayırıcı olarak boşluk açar — `3{,}14` yaz.
- **Kaynakça dili:** Türkçe belgede "References" değil "Kaynaklar/Kaynakça", "Figure" değil "Şekil", "Table" değil "Çizelge/Tablo" olmalı — dil paketi bunu yapar, yapmıyorsa `\addto\captionsturkish` ile düzelt.

İki dilli (TR+EN paralel) teslimlerde ortak bir `.sty`/`.bib` üzerinden iki ayrı ana dosya kur; içeriği kopyala-yapıştır iki kez sürdürme.

## CV işi

Ayrıntı: `references/cv.md`. Şablon: `assets/cv/`.

- Varsayılan: `assets/cv/` altındaki özel şablon (XeLaTeX, tek sütun, ATS dostu). `moderncv` sadece kullanıcı isterse — sidebar/ikon dolu tasarımlar ATS'te parse edilemez.
- **ATS kuralı:** iki sütunlu yerleşim, metin kutusu, tablo içine gömülü iş deneyimi, ikonların yanına gömülü metin ve grafik yetenek çubukları ATS'te kaybolur. Akademik CV'de serbest, iş başvurusu CV'sinde kaçın.
- Uzunluk: iş CV'si 1–2 sayfa (kesin), akademik CV sınırsız ama yayın listesi `biblatex` ile üretilir, elle yazılmaz.
- TR ve EN sürüm istendiğinde ikisini de derle; tarih biçimi, şehir adı ve derece adlarını (Lisans/BSc) dile göre çevir — sadece cümleleri değil.
- Kişisel veri: TC kimlik, tam adres, doğum tarihi, fotoğraf — TR piyasasında yaygın ama uluslararası başvuruda çıkarılır. Hedef pazara göre sor.

## Makale / tez işi

Ayrıntı: `references/makale.md` (sınıflar) ve `references/kaynakca.md` (BibTeX/biblatex).

- Önce **hedef dergi/konferansın kendi şablonunu** al; jenerik `article` ile yazıp sonra dönüştürme — yerleşim, kaynakça stili ve sayfa sayımı değişir.
- Sınıf kuralları: `IEEEtran` çift sütun + `\bibliographystyle{IEEEtran}`, `acmart` `\documentclass[sigconf]{acmart}` ve zorunlu CCS/telif blokları, `elsarticle` `\begin{frontmatter}`, LNCS `llncs` + `splncs04` stili. Sınıf ortamda yoksa `references/ortam.md`'deki apt eşlemesine bak.
- Kayan nesneler: `[htbp]` yaz, `[H]` ile zorlamayı son çare say; tablolarda `booktabs` (dikey çizgi yok), şekillerde vektör (PDF/EPS) tercih et.
- Çapraz referans: `\label` daima `\caption`'dan **sonra**; `cleveref` (`\cref`) ile "Şekil~3" metnini elle yazma. `~` ile bağlanmamış referans satır başına düşer.
- Anonim gönderimde: yazar bloğu, teşekkür, fon numarası, kendi atıflarındaki "our previous work", PDF metadata ve dosya adları temizlenir.
- Sayfa limiti aşımında: `\vspace` hack'leri ve `\small` ile küçültme çoğu konferansta gerekçe ile reddedilir — önce şekil boyutu, kaynakça stili ve gereksiz float'ları düzelt.

## Derleme ve doğrulama

```bash
python3 scripts/build.py belge.tex              # motoru preamble'dan sezer, latexmk çalıştırır
python3 scripts/build.py belge.tex --engine xelatex --bib
python3 scripts/lint.py belge.tex               # dizgi/Türkçe/kalite denetimi
```

`build.py` log'u ayrıştırır ve dosya:satır bazında hata, çözülmemiş referans, eksik atıf ve taşan satır (overfull) özeti verir; PDF sayfa sayısını yazar. Kırmızı çıktı varsa iş bitmemiştir.

**Ortam kısıtı:** Bu container'da CTAN'a erişim yoktur, `tlmgr install` çalışmaz. Eksik sınıf/paket `apt-get install texlive-*` ile gelir; eşleme `references/ortam.md`'de. Paket hiç gelmiyorsa şunu yap: kullanıcıya durumu söyle, belgeyi Overleaf'te derlenecek şekilde teslim et ve yerel olarak paketi devre dışı bırakan bir "önizleme" sürümüyle içeriği yine de doğrula.

## Hata ayıklama protokolü

Bir hata mesajı geldiğinde tahmin yürütme; `references/hata-ayiklama.md` sırasını uygula:

1. **İlk** hatayı çöz, sonrakileri değil — LaTeX hataları çığ yapar, ilk hata çoğu zaman diğer 40'ının sebebidir.
2. Log'ta `!` ile başlayan satırı ve hemen ardındaki `l.<satır>` bilgisini oku.
3. Hata satırını daraltmak için ikiye bölme: gövdenin yarısını `\end{document}` ile kısalt, derle, tarafı belirle.
4. Şüpheli paketi tek başına minimal bir belgede test et (MWE) — çakışma mı, eksiklik mi ayrıştır.
5. `.aux`, `.bbl`, `.toc` bozulmuş olabilir: `latexmk -C` ile temizle ve yeniden derle. "Değişiklik görünmüyor" şikayetlerinin çoğu budur.

Kaynakça özel bir durumdur: `??` ve boş kaynakça neredeyse her zaman "yeterince derlenmedi" (latex → bibtex/biber → latex → latex) veya `.bib` anahtarı yanlış demektir.

## Teslim kontrol listesi

Her teslimden önce:

- [ ] PDF üretildi, sayfa sayısı beklenen aralıkta
- [ ] Log'ta hata yok; `Undefined references` ve `Citation undefined` uyarıları sıfır
- [ ] Türkçe belgede: başlıklarda İ/I doğru, ğüşıöç görünüyor, hece bölme çalışıyor, "Şekil/Tablo/Kaynaklar" Türkçe
- [ ] Overfull hbox'lar 10pt üstü değil (sayfa kenarına taşan metin yok)
- [ ] Tüm `\ref`/`\cite` çözülmüş, `??` yok
- [ ] Sayfa/kelime limiti varsa ölçüldü
- [ ] Kaynak dosyalar derlenebilir halde teslim edildi (tek klasör: `.tex`, `.bib`, `.cls`, şekiller)

## Yazma tarzı

Kullanıcı bir hata sorduğunda: önce **tek cümlelik teşhis**, sonra düzeltilmiş kod, sonra (gerekiyorsa) neden. Uzun paket tarihçesi anlatma. Kod bloklarında sadece değişen preamble satırlarını göster; 80 satırlık preamble'ı her cevapta tekrarlama.

## Referans dosyaları

| Dosya | Ne zaman oku |
|---|---|
| `references/turkce-dizgi.md` | Türkçe (veya çift dilli) herhangi bir belge; karakter/büyütme/tireleme sorunu |
| `references/cv.md` | CV/özgeçmiş; ATS, akademik CV, çift dilli CV |
| `references/makale.md` | Dergi/konferans sınıfları, tez, float/tablo/matematik yerleşimi, anonim gönderim |
| `references/kaynakca.md` | BibTeX vs biblatex kararı, stil seçimi, `.bib` temizliği, atıf sorunları |
| `references/hata-ayiklama.md` | Herhangi bir derleme hatası veya beklenmedik çıktı |
| `references/ortam.md` | Paket/sınıf eksik, kurulum, Overleaf farkı, motor davranışı |
