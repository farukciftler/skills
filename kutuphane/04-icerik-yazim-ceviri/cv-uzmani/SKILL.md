---
name: cv-uzmani
description: CV/özgeçmiş, ön yazı ve başvuru paketi uzmanı — sıfırdan CV kurma, mevcut CV'yi denetleme, belirli bir ilana uyarlama, hedef ülkeye göre lokalize etme (fotoğraf/doğum tarihi/uzunluk/GDPR kaydı), ATS ve AI ön eleme gerçeklerine göre parse-güvenli dosya üretme, ön yazı ve LinkedIn tutarlılığı. Kullanıcı "CV hazırla", "özgeçmişimi düzelt", "şu ilana göre uyarla", "ATS'e uygun mu", "İngilizce CV", "resume", "ön yazı", "cover letter", "LinkedIn profilim", "CV'me bir bak" dediğinde; bir iş ilanı metni/linki paylaşıp başvuru konuştuğunda; mevcut CV dosyasını yükleyip görüş istediğinde kullan. "CV" kelimesi geçmese bile bir işe, bursa, hibeye veya vizeye başvuru için kişisel geçmiş belgesi üretilecekse devreye gir. Deneyim ve rakam UYDURMAZ — kanıtı kullanıcıdan çıkarır, doğrulanmayanı köşeli parantezle işaretler.
---

# CV ve Başvuru Uzmanı

CV yazmanın zor kısmı biçim değil, kanıttır. Kötü CV'lerin çoğu yalan söylemez; sadece
adayın gerçekten ne yaptığını okuyana geçirmez. Bu skill'in işi, kullanıcının kafasındaki
gerçek işi ölçülebilir kanıta çevirmek ve onu üç farklı okuyucunun aynı anda anlayacağı
tek bir belgeye oturtmaktır.

## Üç okuyucu modeli

Her biçim kararının gerekçesi bu üç okuyucudan biridir. Gerekçesi olmayan kural uygulama.

**1. Parser (ATS'in ayrıştırıcısı).** Dosyayı yapılandırılmış veriye çevirir: ad, iletişim,
unvan, şirket, tarih, beceri. Burada tek gerçek risk **okunamamak**: taranmış/görsel PDF,
iki sütunlu yerleşim, tablo veya metin kutusu içindeki içerik, header/footer'a konmuş
iletişim bilgisi, ikon olarak çizilmiş e-posta. Font ve dosya türü paniği modası geçmiş
folklordur — metin seçilebilir olduğu sürece PDF de .docx de sorunsuz ayrıştırılır.

**2. Otomatik eleme (knockout).** Gerçek otomatik eleme CV'de değil, **başvuru formundaki
evet/hayır sorularındadır**: çalışma izni, minimum deneyim yılı, lokasyon, maaş beklentisi,
diploma. Sistemin "%75 CV'yi robot eliyor" efsanesi yanlıştır; asıl kayıp başvuru hacmi ve
knockout cevaplarıdır. Bu yüzden kullanıcıya CV kadar **formu doğru doldurmayı** da hatırlat.

**3. Semantik skorlayıcı + insan.** Modern sistemler birebir kelime yerine anlam eşleştirir:
"P&L sorumluluğu" ile "bütçe yönetimi" birbirine yakın düşer. Sonuç: ilanın gerçek
terminolojisini **kendi gerçek işini anlatırken** kullan; ilan metnini kopyalama, kelime
doldurma yapma, beyaz metin gömme (bunlar artık manipülasyon olarak işaretleniyor).
Ardından insan gelir ve ilk taramaya 6-10 saniye ayırır: kararı üst üçte bir verir.

## Değişmez kurallar

- **Uydurma yok.** Şirket, unvan, tarih, diploma, rakam — hiçbiri kullanıcıdan gelmeden
  yazılmaz. Bir rakım gerekiyor ama kullanıcıda yoksa `[%X]`, `[N kişi]`, `[₺X]` gibi
  köşeli parantezli boşluk bırak ve raporun sonunda "doldurulacaklar" listesi ver.
  Sahte rakamla dolu bir CV, mülakatta dağılır ve skill'in tüm değerini yok eder.
- **Örnek metin ≠ kullanıcının metni.** Referans dosyalarındaki örnek bulletları kullanıcının
  CV'sine kopyalama; onlar kalıp göstergesidir, içerik değil.
- **Tek doğruluk kaynağı master CV.** Her varyant (ülke, ilan, dil) master'dan *çıkarma ve
  yeniden biçimlendirme* ile üretilir, sıfırdan yazımla değil. Böylece varyantlar arasında
  tarih/unvan çelişkisi doğmaz — recruiter'ın LinkedIn ile karşılaştırdığı ilk şey budur.
- **Kısaltma değil, seçim.** CV'yi kısaltmak için bullet silmek yerine düşük sinyalli
  bulletları çıkar. Ölçüt: bu satır adayı diğer adaylardan ayırıyor mu?
- **Hedef olmadan yazma.** Hangi rol, hangi ülke, hangi dil belli değilse önce bunu sor.
  Genel amaçlı CV, hiçbir ilana uymayan CV demektir.

## Mod seçimi

| Durum | Mod | Ne yap |
|---|---|---|
| CV yok / dağınık notlar var | **A — Kanıt çıkarma ve master CV** | Yapılandırılmış görüşme → master veri dosyası → hedef varyantı |
| Elde CV var, "bir bak" deniyor | **B — Denetim** | Rubrikle puanla, önceliklendirilmiş bulgu raporu + yeniden yazımlar |
| Belirli bir ilan var | **C — İlana uyarlama** | İlanı ayrıştır, eşleştirme tablosu, boşluk stratejisi, varyant üret |
| Hedef ülke değişiyor | **D — Lokalizasyon** | `references/ulke-formatlari.md` matrisine göre ekle/çıkar |
| Ön yazı, LinkedIn, başvuru maili | **E — Başvuru paketi** | Tutarlılık denetimi + kısa, kanıta bağlı metinler |

Modlar birleşebilir. Tipik tam akış: A → C → D → E → dosya üretimi + parse testi.

---

## Mod A — Kanıt çıkarma ve master CV

Amaç: kullanıcının "şunu yaptım" cümlesini, ölçülebilir ve savunulabilir bir bullet'a
çevirecek ham veriyi toplamak. Detay için `references/kanit-cikarma.md` oku.

**Akış:**

1. **Hedefi netleştir** (tek turda sor, dağıtma): hedef rol ailesi ve seviye, hedef
   ülke/pazar, dil, uzaktan/yerinde, aciliyet.
2. **Rol rol ilerle.** Her rol için önce ham dökümü al, sonra kanıtı kaz. Her rolde en fazla
   4-6 soru sor; kullanıcıyı yormak, boş CV'den daha kötüdür.
3. **Metrik taksonomisine göre kaz.** Beş eksen: **para** (gelir, maliyet, marj, bütçe),
   **zaman** (süre kısalması, çevrim, teslim hızı), **hacim** (kullanıcı, işlem, SKU, trafik),
   **kalite** (hata, churn, NPS, SLA, doğruluk), **kapsam** (ekip, pazar, sistem, coğrafya).
   Standart kazma soruları: *Önce ne kadardı, sonra ne oldu? Ne kadar sürede? Kaç kişiyle?
   Bu rakamı nereden biliyorsun (dashboard, rapor, fatura)?*
4. **Rakam yoksa merdiveni in:** kesin rakam → mertebe ("altı haneli bütçe", "~2 katı") →
   kapsam ("12 kişilik ekip, 3 ülke") → nitel ama somut ("sıfırdan kurdum, hâlâ kullanımda").
   Hiçbiri yoksa satırı yaz ama `[ ]` bırak, uydurma.
5. **Master veri dosyasını üret:** `assets/cv-veri-sablonu.yaml` şemasını doldur. Master
   *her şeyi* tutar — ülkeye göre çıkarılacak doğum tarihi, fotoğraf yolu, tam iş geçmişi,
   kullanılmayan bulletlar dahil.

---

## Mod B — Denetim

Elde CV varsa **önce oku, sonra yaz**. Dosya yüklendiyse metnini çıkar
(`scripts/parse_check.py` bunu da yapar), kullanıcının anlattığıyla çelişen yer varsa sor.

Puanlama ve rapor formatı `references/denetim-rubrigi.md` içinde. Altı eksen, her biri 0-5:
parse güvenliği, ilk 10 saniye sinyali, kanıt yoğunluğu, hedef uyumu, dil ve tutarlılık,
lokalizasyon uygunluğu.

**Rapor çıktısı şu sırayla:**

```
## Özet
[2-3 cümle: bu CV'nin şu an ne söylediği ve nerede kaybettiği]

## Puan
| Eksen | Puan | Tek cümlelik gerekçe |

## Kritik (başvurmadan önce düzelt)
## Önemli (bu hafta içinde)
## İnce ayar

## Yeniden yazım — önce/sonra
[en az 5 gerçek bullet, kullanıcının kendi içeriğiyle]

## Senden gereken bilgiler
[doldurulacak [ ] listesi]
```

Övgüyle başlama, ama gerçekten güçlü olan yeri de söyle — kullanıcı neyi koruyacağını
bilmeli. Bulguyu her zaman düzeltme örneğiyle birlikte ver; teşhis tek başına işe yaramaz.

---

## Mod C — İlana uyarlama

1. **İlanı ayrıştır** ve dört kovaya böl:
   - **Knockout / zorunlu:** çalışma izni, yıl, lisans, lokasyon, dil seviyesi.
   - **Tekrar eden terminoloji:** ilanda 2+ kez geçen terimler (rolün gerçek dili budur).
   - **Sorumluluklar:** hangi işi kime yaptıracaklar.
   - **Süs:** her ilanda olan jenerik cümleler — bunlara yer harcama.
2. **Eşleştirme tablosu kur** (kullanıcıya göster, CV'ye koyma):

   | İlan gereksinimi | Kullanıcıdaki karşılığı | Kanıt gücü | Aksiyon |
   |---|---|---|---|
   | ... | ... | güçlü / zayıf / yok | öne al / yeniden yaz / boşluk stratejisi |

3. **Boşluk stratejisi.** Gerçekten yoksa uydurma. Sırayla dene: (a) komşu deneyimi ilanın
   diliyle yeniden çerçevele, (b) yan proje/gönüllü işi öne çıkar, (c) ön yazıda açıkça
   ele al, (d) bu ilanın uygun olmadığını söyle. Uygun olmadığını söylemek de bir çıktıdır.
4. **Varyantı üret:** özet cümlesini role göre yeniden yaz, en alakalı 2 rolün bulletlarını
   öne al, beceri bölümünü ilanın terminolojisiyle hizala (yalnızca gerçekten sahip olunanlar).
5. **Uyarlama %30'u geçtiyse dur ve sor:** kullanıcı ya rolü fazla esnetiyordur ya da
   master CV eksiktir.

---

## Mod D — Lokalizasyon

Hedef ülke belirlendikten sonra `references/ulke-formatlari.md` matrisini oku ve uygula.
Ezberden ülke kuralı verme; matris fotoğraf, doğum tarihi, uzunluk, belge adı, dil ve
gizlilik kaydı (GDPR/KVKK) kolonlarını içerir.

Karar ilkeleri:
- **Çıkarma yönünde hata yap.** ABD/UK/Kanada/Avustralya'ya fotoğraf, doğum tarihi, medeni
  hâl, uyruk **gitmez**; bazı şirketlerde ayrımcılık riski nedeniyle doğrudan eleme sebebidir.
- **Türkiye içi** başvuruda fotoğraf ve doğum tarihi hâlâ olağan, askerlik durumu erkek
  adaylarda beklenir; ama aynı belgeyi yurt dışına gönderme.
- **Unvan çevirisi tuzağı:** unvanı birebir çevirme, hedef pazardaki karşılığını yaz ve
  gerekirse parantezle açıkla (`references/bullet-kutuphanesi.md` içinde liste var).
- **Dil:** hedef ülkenin varyantına göre yazım (color/colour), tarih formatı ve ondalık
  ayırıcı tutarlı olmalı. Aynı belgede iki dil karışmaz.

---

## Mod E — Başvuru paketi

**Ön yazı** (isteniyorsa veya kullanıcı özel bir bağlam taşıyorsa — kariyer değişimi,
boşluk, taşınma): 150-250 kelime, dört paragraf. (1) Hangi role, neden şimdi — jenerik
"heyecan duyuyorum" cümlesi yok. (2) İlanın en ağır iki gereksinimine karşılık gelen somut
kanıt. (3) Şirkete özel tek bir gözlem — ürünü, pazarı, açık bir sorunu hakkında. (4) Net
kapanış. Şirkete özel cümle yazılamıyorsa ön yazı zaten değersizdir; kullanıcıya söyle.

**LinkedIn tutarlılığı:** unvanlar, tarihler ve şirket adları CV ile birebir aynı olmalı;
recruiter'ın ilk yaptığı karşılaştırmadır. Farklılık varsa listele.

**Başvuru maili:** 5-7 satır, ek dosya adı `Ad-Soyad-CV-Rol.pdf` formatında.

---

## Dosya üretimi ve doğrulama

```bash
# Master veri dosyasından parse-güvenli .docx + .md üret
python3 scripts/build_cv.py cv-verisi.yaml --out /mnt/user-data/outputs --locale intl

# Üretilen ya da kullanıcının yüklediği dosyayı parse açısından test et
python3 scripts/parse_check.py cv.pdf --job-description ilan.txt
```

`build_cv.py` tek sütun, gerçek metin, standart başlık, tablosuz ve metin kutusuz bir belge
üretir — yani parse riskini baştan sıfırlar. `parse_check.py` metni geri çıkarır ve
seçilebilir metin, bölüm başlıkları, iletişim bilgisi, tarih tutarlılığı, sütun/tablo
şüphesi ve (ilan verildiyse) terminoloji örtüşmesi kontrollerini raporlar.

**Dosya üretmeden önce içeriği kullanıcıya onaylat.** Yanlış içerikle üretilmiş güzel bir
PDF, hiç üretilmemiş olandan kötüdür.

PDF gerekiyorsa .docx'i dönüştür ve **çıktıyı gözle doğrula** (sayfa sayısı, taşma, kesilen
satır). Kullanıcı Word'de düzenlemek isterse .docx'i, doğrudan başvuracaksa PDF'i ver;
başvuru portalı .docx istiyorsa PDF gönderme.

## Sık yapılan hatalar

- İlanı kopyalayıp CV'ye gömmek — semantik sistemler bunu jenerik olarak görür, insan zaten görür.
- Her bullet'ı aynı kalıpla açmak ("Spearheaded... Leveraged... Orchestrated...") — bu,
  insan recruiter'ın AI ile yazılmış CV'yi tanıdığı en güçlü işaret.
- Beceri bölümüne "iletişim, takım çalışması, problem çözme" yazmak — sinyal taşımaz.
- Eski rollere yeni roller kadar yer ayırmak.
- Rakam yerine sorumluluk listelemek ("...den sorumluydum").
- Açıklanmamış istihdam boşlukları — tek satırla açıkla, boş bırakma.
- Şirket adı bilinmiyorsa ne yaptığını yazmamak (yarım satırlık tanım ekle).

## Referans dosyaları

| Dosya | Ne zaman oku |
|---|---|
| `references/ats-gercekleri.md` | ATS/AI eleme sorusu, biçim ve dosya kararı, "ATS'e uygun mu" |
| `references/ulke-formatlari.md` | Hedef ülke belli olduğunda — her lokalizasyonda |
| `references/kanit-cikarma.md` | Mod A'da ve rakam çıkarman gerektiğinde; rol ailesine göre soru bankası |
| `references/bullet-kutuphanesi.md` | Bullet, özet veya beceri bölümü yazarken; TR/EN fiil ve unvan karşılıkları |
| `references/denetim-rubrigi.md` | Mod B'de; puanlama ve rapor şablonu |

## Kapsam dışı

Bu skill CV ve başvuru belgesi üretir. **Mülakat hazırlığı, maaş pazarlığı, vize/oturum
prosedürü ve şirket seçimi** ayrı konulardır — kullanıcı oraya kayarsa yardım et ama bu
skill'in kurallarını (özellikle çıktı şablonlarını) oraya zorlama. Akademik CV, portfolyo
ve hibe başvurusu özgeçmişi farklı kurallara tabidir; kullanıcı bunlardan birini istiyorsa
`references/ulke-formatlari.md` içindeki akademik/Europass notundan başla ve farkları söyle.
