# ATS ve AI Ön Eleme — Gerçekler ve Biçim Kararları

*Son doğrulama: Eylül 2026. Bu alanda internetteki tavsiyenin büyük kısmı 2015 dönemi
sistemlerini anlatır. Kullanıcı çelişkili bir şey duyduysa, aşağıdaki mekanizmayı anlat —
kural listesi vermek yerine nedenini açıklamak daha ikna edici ve daha doğru.*

## İçindekiler
1. Boru hattı: dosyaya ne oluyor
2. Efsane tablosu
3. Parse-güvenli biçim kuralları
4. Dosya türü, dosya adı, portal davranışı
5. Semantik eşleştirme çağında anahtar kelime
6. AI ile yazılmış CV meselesi
7. Hızlı kontrol listesi

---

## 1. Boru hattı: dosyaya ne oluyor

```
Başvuru → [1] Dosya saklanır ve AYRIŞTIRILIR (parse)
        → [2] Form cevapları KNOCKOUT filtresinden geçer
        → [3] Profil ilana karşı SKORLANIR / sıralanır (her sistemde yok)
        → [4] İNSAN recruiter listeyi tarar ve seçer
```

- **[1] Ayrıştırma tek gerçek teknik engeldir.** Metin okunamıyorsa geri kalan hiçbir şeyin
  önemi yok. Görsel/taranmış PDF, sütunlu yerleşim, tablo hücresine gömülü metin,
  header/footer'daki iletişim bilgisi, ikon grafiği olarak çizilmiş e-posta buradan kaybeder.
- **[2] Otomatik red esas olarak burada olur** ve CV metniyle değil, formdaki evet/hayır
  sorularıyla ilgilidir: çalışma izni, minimum deneyim, lokasyon, eğitim, bazen maaş.
- **[3] Skorlama yaygın ama karar verici değil.** Recruiter'a sıralama ve filtre "düğmesi"
  verir; adayı sistem kendiliğinden reddetmez.
- **[4] Asıl eleme burada.** Nitelikli bir başvuru havuzunda kaybın büyük kısmı hacim ve
  insan seçimi kaynaklıdır. Bu yüzden "makineyi kandırma" değil, **insanı ilk 10 saniyede
  ikna etme** optimizasyonu yap.

## 2. Efsane tablosu

| Yaygın inanış | Gerçek |
|---|---|
| "ATS CV'lerin %75'ini insan görmeden reddediyor" | Büyük ATS'ler CV'yi otomatik reddetmez. Rakamın kaynağı belirsiz ve tekrar tekrar çürütüldü. Otomatik red knockout sorularından gelir. |
| "Evrensel bir ATS puanı var" | Yok. Üçüncü parti "ATS skoru" araçları kendi ölçütlerini ölçer, işverenin gördüğünü değil. Faydası: eksik terminolojiyi göstermek. |
| "PDF gönderme, mutlaka .docx" | Her büyük ATS metni seçilebilir PDF'i temiz ayrıştırır. Sorun PDF değil, **görsel** PDF'tir. Portal hangisini istiyorsa onu gönder. |
| "Sihirli bir ATS fontu var" | Parser tipografiyi değil, altındaki metni okur. Standart fontlar (Arial, Calibri, Helvetica, Georgia, Inter) sorunsuz; süslü/el yazısı fontlar riskli. |
| "Beyaz metinle gizli anahtar kelime koy" | Ayrıştırma biçimi soyar, gizli metin görünür hâle gelir ve manipülasyon olarak işaretlenebilir. Yakalanınca sonuç red. Asla yapma. |
| "Anahtar kelimeyi ne kadar çok tekrar edersen o kadar iyi" | Bağlamsız yığma skoru düşürür ve insana anında belli eder. |
| "Yaratıcı tasarım hep zarar verir" | Tek sütun ve gerçek metin korunduğu sürece renk ve tipografi serbesttir. Tasarım riski yerleşimden gelir, estetikten değil. |
| "Grafik beceri çubukları etkileyici" | Parser için anlamsız, insan için ölçüsüz. "Python ●●●○○" hiçbir şey söylemez. Kullanma. |

## 3. Parse-güvenli biçim kuralları

**Zorunlu:**
- Tek sütun. İki sütunlu şablonlar okuma sırasını bozar ve en sık görülen ayrıştırma hatasıdır.
- Gerçek, seçilebilir metin. Görsele gömülü hiçbir bilgi olmayacak.
- İletişim bilgisi belgenin **gövdesinde**, header/footer'da değil.
- Standart bölüm başlıkları: Deneyim / Experience, Eğitim / Education, Beceriler / Skills,
  Sertifikalar / Certifications, Projeler / Projects. "Yolculuğum", "Neler Yapabilirim"
  gibi yaratıcı başlıklar parser'ı ve tarayan insanı yavaşlatır.
- Tarih formatı tek tip: `Tem 2024 – Haz 2026` veya `07/2024 – 06/2026`. Aynı belgede karıştırma.
- Kronolojik ters sıra (en yeni üstte). Fonksiyonel/beceri-öncelikli CV boşluk gizleme
  girişimi olarak okunur ve ayrıştırması da kötüdür.

**Kaçın:**
- Tablo, metin kutusu, çok sütunlu bölüm, SmartArt, dipnot.
- Sayfa kenarı 1,3 cm altına inen marjlar; 9 punto altı gövde metni.
- Madde işareti olarak özel semboller (`▪ ✦ ➤`). Normal liste madde işareti kullan.
- Aynı satırda hizalama için ardışık boşluk/tab yığını — sütun sanılır.

**Serbest:** renk, ince ayırıcı çizgi, kalın/italik vurgu, isim için büyük punto, ikon
*yanında* metin varsa ikon.

## 4. Dosya türü, dosya adı, portal davranışı

- **Dosya adı:** `Ad-Soyad-CV.pdf` veya hedefliyse `Ad-Soyad-CV-RolAdi.pdf`. `cv_final_v3_son.pdf`
  ilk izlenimi bozar ve bazı portallarda kırpılır. Türkçe karakter ve boşluk kullanma.
- **PDF vs .docx:** portal bir tür istiyorsa ona uy. Serbestse PDF (biçim kayması olmaz).
  İnsan kaynağına e-posta ile gidiyorsa PDF. Bazı ajanslar kendi başlığını eklemek için
  .docx ister — o zaman .docx.
- **LinkedIn "Easy Apply"** profilinden veri çeker: profil ile CV çeliştiğinde güven kaybı olur.
- **Portalın kendi formu her zaman kazanır.** Kullanıcı formu üşenip "CV'ye bakın" diye
  geçerse knockout aşamasında elenir.

## 5. Semantik eşleştirme çağında anahtar kelime

Modern skorlama, CV ile ilanı aynı anlam uzayına yerleştirip yakınlık ölçer. Pratik sonuçları:

- **Eş anlamlı artık tutuyor.** "İstatistiksel modelleme, Python" ile "makine öğrenmesi,
  scikit-learn" birbirine yakın düşer. Yine de **ilanın kendi terimini kullanmak en güvenlisi**,
  çünkü hem semantik yakınlığı hem de recruiter'ın Boolean aramasını karşılar.
- **Doğru yöntem:** ilanda 2+ kez geçen terimleri çıkar, bunlardan **gerçekten sahip olduklarını**
  kendi cümlenin içine doğal şekilde yerleştir. Beceri bölümüne liste olarak da ekle.
- **Yanlış yöntem:** ilan cümlelerini kopyalamak, alakasız bölüme terim doldurmak, sahip
  olmadığın aracı yazmak (mülakatta çöker).
- Kısaltma ve açık hâli birlikte yaz: "FinOps (Cloud Financial Management)", "OKR".
- Unvan standart değilse köprü kur: "Ürün Sorumlusu (Product Manager)".

## 6. AI ile yazılmış CV meselesi

- Büyük ATS'lerin çoğu AI-yazımı **tespit etmez**; içlerindeki yapay zekâ eşleştirme içindir.
  Bazı platformlar deneysel sınıflandırıcı sunar ama isabetsizdir ve nadiren red sebebidir.
- **Asıl dedektör insandır** ve çok hassastır. Şu kalıpları saniyede tanır:
  - Her bullet aynı ritimde ve aynı fiil ailesiyle başlıyor.
  - Ürün, müşteri, ekip, araç adı hiç geçmiyor; her cümle her role uyabilir.
  - Yuvarlak ve kanıtsız rakam enflasyonu (%50, %100, "3 kat").
  - Aşırı cilalı ama içi boş özet: "sonuç odaklı, tutkulu profesyonel".
  - CV'nin dili ile kullanıcının mülakattaki dili arasında uçurum.
- **Doğru kullanım:** taslak ve yapı için yapay zekâ, içerik için gerçek. Spesifik ad, sayı ve
  bağlam ekledikçe hem insan filtresini hem semantik skoru geçersin.

## 7. Hızlı kontrol listesi

- [ ] Metin seçilebiliyor (PDF'i aç, metni seç ve kopyala)
- [ ] Tek sütun, tablo yok, metin kutusu yok
- [ ] İletişim bilgisi gövdede, header/footer'da değil
- [ ] Standart bölüm başlıkları
- [ ] Tarih formatı tutarlı, boşluklar açıklanmış
- [ ] Bulletların en az yarısı sayı, kapsam veya somut sonuç içeriyor
- [ ] İlandaki tekrar eden terimler doğal biçimde geçiyor
- [ ] Gizli metin, beceri çubuğu, grafik ikon yok
- [ ] Dosya adı `Ad-Soyad-CV.pdf`
- [ ] LinkedIn ile unvan/tarih/şirket birebir aynı
- [ ] Başvuru formundaki knockout soruları eksiksiz ve doğru dolduruldu
