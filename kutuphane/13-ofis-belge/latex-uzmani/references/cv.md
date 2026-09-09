# CV / Özgeçmiş Referansı

## Önce karar: hangi CV?

| Tür | Uzunluk | Yerleşim | Yayın listesi | Fotoğraf |
|---|---|---|---|---|
| İş başvurusu (özel sektör) | 1–2 sayfa, kesin | Tek sütun, sade, ATS dostu | Yok/kısa | Genelde hayır (TR'de yaygın, EU dışı başvuruda çıkar) |
| Akademik CV | Sınırsız | Tek sütun, bölümlü | Zorunlu, tam | Hayır |
| Burs/hibe başvurusu | Formata bağlı | Kurumun formu bağlayıcı | Seçilmiş | Forma bağlı |
| Europass | Sabit | Kurumsal şablon | — | Opsiyonel |

Belirsizse hedef pazarı sor: TR piyasası ile ABD/Kanada ve AB piyasalarının beklentileri farklıdır.

## ATS (Applicant Tracking System) kuralları

Büyük şirketlerin başvuru sistemleri PDF'ten metin çıkarır. Şunlar metni bozar veya kaybeder:

- **İki sütunlu yerleşim** — sütunlar satır satır iç içe geçer, deneyimler karışır
- İş deneyimini `tabular` içine gömmek — hücre sırası karışır
- Yan panel (sidebar) tasarımları (`moderncv`'nin `casual`/`banking` dışı stilleri, `altacv`)
- Yetenek grafikleri (dolu/boş daireler, çubuklar) — hiçbir bilgi taşımaz, ATS'te kaybolur
- İkon fontları (`fontawesome`) — okunamayan glif olarak çıkar; ikonu kullan ama **yanına düz metin de yaz** (` github.com/kullanici`)
- Metin olarak gömülmemiş logolar/görseller
- Alışılmadık bölüm başlıkları — "Experience/Deneyim", "Education/Eğitim", "Skills/Yetkinlikler" gibi standart başlıklar kullan

**Doğrulama:** `pdftotext cv.pdf - | less` çalıştır. Çıkan düz metin okunabilir ve sırası doğru mu? Değilse ATS de okuyamaz.

## Şablon seçimi

- **Varsayılan:** `assets/cv/` altındaki `cv-tr.tex` / `cv-en.tex` + `cvstil.sty`. XeLaTeX, tek sütun, ATS'ten temiz geçer, Türkçe glifleri test edilmiştir.
- `moderncv`: yaygın ve tanıdık ama tarihi eskimiş; `\MakeUppercase` kullanan stilleri Türkçe'de `İ` sorunu üretir. Kullanılacaksa `style=classic` + büyütme kapatılmış hâli tercih edilir.
- `altacv`, `awesome-cv`: görsel olarak güçlü, ATS için riskli. Portfolyo/tasarım rolleri veya doğrudan insana giden CV'ler için uygun.
- Tez/akademik CV: `biblatex` ile yayın listesi üret (aşağı bak) — elle yazılan yayın listesi her makalede güncellenmeyi unutur.

## Akademik CV'de yayın listesini otomatik üretme

```latex
\usepackage[backend=biber,style=numeric,sorting=ydnt,maxbibnames=99]{biblatex}
\addbibresource{yayinlar.bib}
% kendi adını kalınlaştır:
\renewcommand*{\mkbibnamefamily}[1]{%
  \ifboolexpr{ test {\ifcurrentname{author}} and test {\iffieldequalstr{hash}{HASH}}}
    {\textbf{#1}}{#1}}
...
\nocite{*}
\printbibliography[type=article,title={Dergi Makaleleri}]
\printbibliography[type=inproceedings,title={Konferans Bildirileri}]
```

`sorting=ydnt` = yıl azalan (en yeni üstte), akademik CV standardı. Kendi adını kalınlaştırma için `HASH` yerine biber'in ürettiği hash veya daha basiti: `\DeclareNameFormat` ile soyad eşleştirme kullan.

## Çift dilli CV (TR + EN)

Sadece cümleleri çevirmek yetmez. Dile göre değişenler:

- Tarih biçimi: `Eylül 2024 – Halen` / `Sep 2024 – Present`
- Derece adları: Lisans → BSc, Yüksek Lisans → MSc, Doktora → PhD (kurum adını çevirme: "Yıldız Technical University" değil "Yıldız Teknik Üniversitesi" — resmî İngilizce adı varsa onu kullan)
- Şehir/ülke: İstanbul, Türkiye / Istanbul, Türkiye (İngilizce metinde de "Türkiye" resmî ad)
- Askerlik, TC kimlik, medeni durum: EN sürümde çıkarılır
- Referanslar: TR'de "İstendiğinde sunulur", EN'de bu satır genelde hiç yazılmaz

Kurulum: ortak `cvstil.sty`, iki ana dosya, ortak `.bib`. Her ikisini de derleyip iki PDF teslim et.

## İçerik kalitesi (dizgi kadar önemli)

CV dizgisi iyi ama içeriği zayıfsa iş yarım kalır. Kullanıcı içerik yazdırıyorsa:

- Her madde **fiil + iş + ölçülebilir sonuç** kalıbında olsun: "Sorumluydum" değil, "X yaparak Y metriğini %Z iyileştirdim".
- Ölçüm yoksa uydurma; kapsam yaz (ekip büyüklüğü, kullanıcı sayısı, bütçe).
- İlk yarım sayfa en değerli alan; en güçlü şey oraya.
- Aynı CV'yi her ilana gönderme — anahtar kelimeleri ilana göre ayarla (ATS eşleşmesi buradan gelir).

## Sık sorunlar

| Sorun | Sebep / çözüm |
|---|---|
| Başlıklar `GIRIŞ` gibi çıkıyor | `\MakeUppercase` + Türkçe. Bkz. `turkce-dizgi.md` §2 |
| CV 1 sayfayı 3 satır aşıyor | Önce satır aralığı ve kenar boşluğu (`geometry`), sonra madde eleme. `\small` ile tümünü küçültme son çare |
| İkonlar kutu çıkıyor | `fontawesome5` yüklü değil veya pdfLaTeX ile XeLaTeX fontu karıştırılmış |
| Link tıklanmıyor | `hyperref` eksik; `\href{https://...}{metin}` kullan, `hidelinks` seçeneğiyle CV'de renkli çerçeve olmasın |
| Uzun kurum adı satırı taşırıyor | `\raggedright` veya `\mbox` yerine sütun genişliğini düzelt |
