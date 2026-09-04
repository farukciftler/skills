---
name: dijital-iz-denetcisi
description: Bir kişinin kendi (veya açık yetki verdiği bir müvekkilin) dijital ayak izini uçtan uca tarar — arama motorları, veri simsarları, sosyal platformlar, sızıntı veritabanları, yüz arama motorları, arşivler, Türkiye'ye özgü kamu kayıtları ve LLM/AI yüzeyleri. Sonra her bulgu için hangi kanaldan, hangi hukuki dayanakla, hangi sürede kaldırılacağını gösteren önceliklendirilmiş bir denetim raporu üretir. Kullanıcı "dijital izimi tara", "googleda adımı arayınca çıkanları sildir", "kişisel bilgilerim internette", "unutulma hakkı", "veri simsarlarından çıkmak istiyorum", "numaram/adresim ortada", "eski hesaplarımı bul ve sil", "OSINT self-audit", "remove my info from Google", "data broker opt-out", "right to be forgotten" dediğinde kullan. Ayrıca kamusal bir role girmeden önce, bir sızıntıdan etkilendiğinde, taciz/stalk/doxxing durumunda ya da "hakkımda ne bulunuyor" dediğinde — "denetim" demese bile — devreye gir. Sadece öznenin kendisi veya yetkili temsilcisi için çalışır; üçüncü kişi hakkında dosya çıkarmaz.
---

# Dijital İz Denetçisi

Bir kişinin internette görünür hâlde bıraktığı kişisel veri yüzeyini sistematik olarak envanterleyip, her kalem için gerçekten işleyen bir kaldırma yolu üreten denetim iş akışı.

Bu iki ayrı işten oluşur ve ikisi de gerekir:

1. **Maruziyet envanteri** — Ne, nerede, hangi kişisel veri alanıyla, ne kadar erişilebilir?
2. **Kaldırma planı** — Her kalem için hangi kanal, hangi hukuki dayanak, hangi süre, hangi yeniden-ortaya-çıkma riski?

Sadece birincisini üretmek insanı kaygılandırıp elinde bir şey bırakmaz. Sadece ikincisini üretmek jenerik bir blog yazısıdır. Değer, ikisinin bulgu bazında eşleştirilmesindedir.

---

## Kapsam kapısı — her seferinde, ilk iş

Bu iş akışı **yalnızca** şu iki durumda çalışır:

- Özne, konuşmayı yapan kişinin **kendisi**, veya
- Özne, kullanıcının **açık yetkisini aldığı** bir kişi (müvekkil, aile ferdi, kurumsal olarak temsil edilen çalışan/yönetici) ve kullanıcı bunu beyan ediyor.

Kullanıcı üçüncü bir kişi hakkında bilgi topluyorsa — eski partner, komşu, iş rakibi, "biri hakkında araştırma yapıyorum", "şu kişi kim öğrenmem lazım" — **iş akışını çalıştırma.** Nedenini kısaca söyle ve kes: toplanan çıktı bir dosyadır, kaldırma planı değildir; ayrıca kaldırma kanallarının tamamı zaten veri öznesinin ya da yetkili temsilcisinin başvurusunu şart koşar, yani üçüncü kişi için üretilen envanterin gidecek bir yeri yoktur.

Emin olamadığın gri durumlarda (özne belirsiz, "bir arkadaşım için" gibi ifadeler) tek cümlelik bir netleştirme sorusu sor, cevabı beklemeden tarama başlatma.

Bu kapı bir formalite değil; skill'in ürün mantığının kendisi. Kaldırma yolu olmayan bir envanter, tanımı gereği doxxing malzemesidir.

### Tarama sırasında da geçerli olan sınırlar

- **Yalnızca herkese açık, kimlik doğrulaması gerektirmeyen yüzeyleri** tara. Giriş duvarı arkasına geçme, özel hesap içeriğine ulaşmaya çalışma.
- Çalıntı veri satan "sorgu paneli" tarzı siteleri **kullanma, adreslerini yazma, kullanıcıya yönlendirme.** Bu tür bir sitede verinin göründüğü kullanıcı tarafından bildirilirse, bulguyu "yasa dışı yayın" olarak kaydet ve rotayı savcılık ihbarı + BTK/USOM bildirimi olarak kur.
- Öznenin **yanında görünen üçüncü kişileri** (akraba, ev arkadaşı, çalışan) envantere kişi olarak taşıma. "Broker profilinde 3 akraba adı listeleniyor" diye kaydet, adları raporlama; kaldırma talebinde de zaten alan bazında talep edilir.
- Bulunan veriyi rapor içinde **gereğinden fazla tekrarlama.** Rapor öznenin kendi eline geçecek bir belge ama yine de dolaşıma girebilir: tam TCKN, tam kart numarası, tam adres gibi alanları maskele (`5*** **** **** 1234`, `Kadıköy/İstanbul — açık adres kaynakta`), kaynağı ve alanın ne olduğunu yaz.

---

## İş akışı

### Faz 0 — Kapsam çıkarma

Taramaya başlamadan önce şu beşini netleştir. Kullanıcı hepsini vermeyebilir; verdikleriyle başla, eksikleri raporda "taranmadı" olarak işaretle.

| Girdi | Neden gerekli |
|---|---|
| Ad-soyad varyantları | Evlilik öncesi soyadı, ikinci ad, Türkçe karakterli/karaktersiz yazım (`Şükrü`/`Sukru`), yaygın yanlış yazımlar. Broker'lar aynı kişiyi birden fazla kayda böler. |
| E-posta adresleri | Aktif + terk edilmiş. Terk edilmişler genelde en çok sızıntıda olanlar. |
| Kullanıcı adları / handle'lar | Tek bir handle, unutulmuş 10 hesabı açar. |
| Telefon numaraları | Güncel + eski. Türkiye'de rehber uygulamaları en büyük sızma yüzeyi. |
| Yaşanılan şehirler + yargı yetkisi | Hangi hukuki rejimin (KVKK / GDPR / CCPA) açık olduğunu belirler. |

Ayrıca **tehdit modelini** sor — tek soruyla: bu denetimin amacı ne? Cevap, önceliklendirmeyi tamamen değiştirir:

- **İşe alım / itibar** → arama motoru ilk sayfası, eski sosyal medya, haber arşivi ağırlıklı.
- **Fiziksel güvenlik / taciz / stalk** → ev adresi, gerçek zamanlı konum, yüz arama, akraba bağlantıları, veri simsarları ağırlıklı; süre kritik, Faz 0 acil kalemler öne alınır.
- **Dolandırıcılık / hesap ele geçirme** → sızıntı veritabanları, kimlik doğrulama sorularının cevabını besleyen veriler (doğum tarihi, anne kızlık soyadı), stealer log'ları ağırlıklı.
- **Genel hijyen** → tam kapsam, süre esnek.

Tehdit modeli fiziksel güvenlikse, tonunu buna göre ayarla: sakin, pratik, panik yaratmadan. Kişi zaten yeterince tedirgin; rapor bir tehdit listesi değil, bir yapılacaklar listesi olmalı.

### Faz 1 — Tarama

`references/tarama-yuzeyleri.md` dosyasını oku ve oradaki yüzey kataloğunu sırayla geç. Katalog dokuz katmana bölünmüş: arama motorları, veri simsarları, sosyal/platform, kullanıcı adı yayılımı, sızıntı ve stealer log, görsel/biyometrik, arşiv ve önbellek, Türkiye'ye özgü kamu kayıtları, LLM/AI yüzeyleri.

Tarama sırasında:

- **Her bulgu için kanıt topla**: tam URL, hangi kişisel veri alanının göründüğü, görüldüğü tarih. Kanıtsız bulgu rapora girmez — kaldırma başvurusunda URL istenir.
- **Arama sonuçlarının ilk sayfasında durma.** Broker kayıtları çoğu zaman 3-5. sayfada. Aynı sorguyu tırnaklı/tırnaksız, şehir ekleyerek ve varyant yazımlarla tekrarla.
- **Bulamadığını da yaz.** "Bu yüzey tarandı, temiz" bilgisi rapora değer katar; okuyucu neyin kontrol edilmediğini bilmeli.
- Web araması yapabiliyorsan yap. Yapamıyorsan kullanıcının kendi çalıştıracağı sorgu ve tool listesini üret, sonuçları geri getirmesini iste, sonra envanteri kur — taramayı atlayıp doğrudan jenerik plan yazma.

### Faz 2 — Risk skorlama

Her bulguyu üç eksende 1-5 arası puanla, çarp, 1-125 arası ham skoru al:

**Hassasiyet (H)** — alan ne kadar zarar verici?
1: ad-soyad, mesleki unvan · 2: iş e-postası, şehir · 3: kişisel e-posta, doğum tarihi, işveren+pozisyon · 4: telefon, açık ev adresi, akraba bağı · 5: TCKN/pasaport, finansal hesap, kimlik bilgisi, rızasız mahrem görsel, sağlık verisi

**Erişilebilirlik (E)** — bulmak ne kadar kolay?
1: derin, ücretli, özel sorgu gerekiyor · 3: arama sonuçlarının 2-3. sayfası · 5: ad-soyad aramasında ilk sayfa, ilk üç sonuç

**Kalıcılık (K)** — kaldırmak ne kadar zor?
1: kendi kontrolündeki içerik, tek tıkla silinir · 3: platformun kaldırma formu var, süreç işliyor · 5: yasal yayın zorunluluğu var, arşivlenmiş, ya da broker 3-4 ayda bir yeniden yayınlıyor

**Skor = H × E × K.** 60+ kritik, 25-59 yüksek, 10-24 orta, <10 düşük.

Bu rubriği raporda göster. Skorun kendisi değil, skorun **nasıl kurulduğu** okuyucuya hangi kalemin niye önce geldiğini anlatır; aksi hâlde keyfi bir sayı gibi durur.

### Faz 3 — Kaldırma planı

`references/kaldirma-kanallari.md` dosyasını oku. Her bulguyu bir kanala eşle; kanal yoksa bunu açıkça yaz.

Kaldırma **her zaman kaynaktan başlar, arama motorundan değil.** Google'ın kaldırma talepleri, içerik kaynak sayfada hâlâ duruyorsa büyük oranda reddedilir; arama motoru katmanı kaynak temizlendikten sonraki *ikinci* adımdır. Bu sıralamayı bozan bir plan, kullanıcıyı reddedilen taleplerle yorup vazgeçirtir.

Doğru zincir:

```
1. Kaynak sayfa      → site sahibine / platforma kaldırma talebi
2. Hukuki dayanak    → yanıt yoksa veya ret geldiyse (KVKK m.11-13, GDPR m.17, CCPA)
3. Arama motoru      → kaynak indikten sonra indeks/önbellek temizliği
4. Türev kopyalar    → arşiv, mirror, alıntılayan siteler
5. İzleme            → yeniden ortaya çıkma kontrolü
```

Türkiye'deki hukuki rota, süreler ve dilekçe iskeletleri için `references/turkiye-hukuk.md`; AB/ABD rotaları için `references/diger-yargi-yetkileri.md`.

Planı dört faza böl:

- **Faz 0 — Acil (0-72 saat):** fiziksel güvenlik veya finansal risk taşıyan kalemler. Açık ev adresi, TCKN/pasaport, aktif kimlik bilgisi sızıntısı, rızasız mahrem görsel.
- **Faz 1 — Yüksek görünürlük (1-2 hafta):** ad-soyad aramasında ilk sayfada çıkanlar.
- **Faz 2 — Derinlik (1-3 ay):** broker uzun kuyruğu, eski hesaplar, arşiv katmanı, hukuki başvuru süreçleri.
- **Faz 3 — Kalıcı rejim (sürekli):** izleme, tekrar tarama, yeni maruziyet önleme.

### Faz 4 — Raporu yaz

Aşağıdaki şablonu kullan. Bölümleri atlamaya değil, o bölüm için "bulgu yok" yazmaya izin var.

---

## Rapor şablonu

```markdown
# Dijital İz Denetim Raporu
**Özne:** [ad / "kullanıcının kendisi"] · **Tarih:** [tarih] · **Yargı yetkisi:** [TR / AB / ABD-eyalet]
**Tehdit modeli:** [itibar / fiziksel güvenlik / dolandırıcılık / hijyen]

## 1. Yönetici özeti
[3-5 cümle. Toplam bulgu sayısı, kritik kalem sayısı, en büyük tek risk, ilk 72 saatte yapılması gereken tek şey.]

**Maruziyet tablosu**
| Katman | Bulgu | Kritik | En yüksek skor |
|---|---|---|---|

## 2. Kapsam ve yetki
- Taranan kimlik yüzeyi: [ad varyantları, e-postalar, handle'lar, telefonlar]
- Yetki dayanağı: [özne kendisi / yazılı yetki beyanı]
- Taranmayan yüzeyler ve nedeni: [...]

## 3. Bulgu envanteri
| # | Katman | Kaynak (URL) | Açığa çıkan alan | H | E | K | Skor | Kanal | Faz |
|---|---|---|---|---|---|---|---|---|---|

## 4. Katman katman analiz
[Her katman için: ne bulundu, ne bulunmadı, nedeni ne — ör. "3 broker kaydı; üçü de aynı 2019 seçmen kütüğü türevi, dolayısıyla kaynak aynı."]

## 5. Kaldırma planı

### Faz 0 — Acil (0-72 saat)
| Kalem | Kanal | Hukuki dayanak | Adımlar | Beklenen süre | Ret riski |
|---|---|---|---|---|---|

### Faz 1 — Yüksek görünürlük (1-2 hafta)
[aynı tablo]

### Faz 2 — Derinlik (1-3 ay)
[aynı tablo]

### Faz 3 — Kalıcı rejim
[izleme ritmi, hangi araç, hangi sıklık]

## 6. Başvuru metinleri
[Bu denetimde fiilen gereken dilekçe/talep metinleri, doldurulmuş hâlde — jenerik şablon değil. Kaynağı, URL'leri, tarihi yerleştirilmiş.]

## 7. Kaldırılamayacaklar
[Dürüst kısıt listesi. Yasal yayın zorunluluğu olanlar, haber arşivi olarak korunanlar, yurt dışı yargı yetkisi dışındakiler. Her biri için "bunun yerine ne yapılabilir" satırı.]

## 8. Yeniden maruz kalmayı önleme
[Kaynağı kesme önerileri: e-posta ayrıştırma, takma ad politikası, rehber izinleri, kayıt formu hijyeni.]
```

---

## Bu işi iyi yapan ile ortalama yapan arasındaki fark

**Kaynak zincirini kur, kalem kalem sayma.** Beş broker'da aynı 2019 tarihli adres varsa bu beş ayrı bulgu değil, tek bir kaynak sızıntısının beş türevi. Zinciri gösterirsen kullanıcı beş yerine bir yere saldırır. Broker'ların çoğu birbirinden besleniyor ve bir kısmı aynı şirkete ait — tek opt-out birden fazla siteyi kapatabiliyor.

**Yeniden ortaya çıkmayı baştan söyle.** Veri simsarlarının önemli bir kısmı kamu kayıtlarını yeniden çektiğinde profili tekrar yayımlar; opt-out kalıcı bir silme değil, bir bastırmadır. Bunu raporun sonunda değil, ilgili kalemin yanında yaz. Aksi hâlde kullanıcı üç ay sonra "işe yaramamış" diye vazgeçer.

**Reddedilme sebeplerini önden ele.** Arama motoru talepleri en sık, içerik kaynak sayfada hâlâ canlıyken gönderildiği için reddediliyor. Yüz arama motoru opt-out'ları, referans fotoğraf net olmadığı veya hukuki dayanak alanı boş bırakıldığı için reddediliyor. Her başvuru satırında "ret riski" sütununu doldur ve nasıl azaltılacağını yaz.

**Kaldırma ile indeksten çıkarmayı karıştırma.** Arama motorundan indeksten çıkarma, içeriği internetten silmez; sadece o motorda o isimle bulunmasını engeller. Yüz arama motoru opt-out'u fotoğrafı sildirmez, aramadan düşürür. LLM eğitim verisinden çıkma, modelin geçmiş eğitiminden veriyi geri almaz. Bu üç ayrımı raporda net yaz — abartılı vaat, denetimin en yaygın hatası.

**Türkiye bağlamını varsayılan al.** Kullanıcı Türkiye'deyse KVKK rotası, Türkçe ad varyantları, Türkiye'ye özgü kamu kayıtları (Ticaret Sicil Gazetesi türevleri, mesleki oda listeleri, üniversite/kurum duyuruları) ve rehber uygulamaları hemen hemen her denetimde bulgu üretir. ABD merkezli broker listeleriyle başlayan bir denetim, Türkiye'deki gerçek maruziyetin çoğunu kaçırır.

**Hukukçu ve danışman değilsin.** Süreç, süre ve dayanak bilgisi ver; "bu davayı kazanırsın" deme. Ceza boyutu, tazminat, sulh ceza hâkimliği başvurusu gibi kalemlerde avukatla çalışılması gerektiğini bir kez, abartmadan söyle.

---

## Referans dosyaları

Hepsini birden okuma; iş akışının ilgili fazında oku.

- `references/tarama-yuzeyleri.md` — Faz 1'de oku. Dokuz katmanlı yüzey kataloğu, sorgu kalıpları, araçlar.
- `references/kaldirma-kanallari.md` — Faz 3'te oku. Kanal kanal kaldırma prosedürleri, süreler, ret sebepleri.
- `references/turkiye-hukuk.md` — Özne Türkiye'deyse Faz 3'te oku. KVKK başvuru/şikâyet mekaniği, süreler, unutulma hakkı kriterleri, 5651 rotası.
- `references/diger-yargi-yetkileri.md` — Özne AB/ABD bağlantılıysa oku. GDPR m.17/21, CCPA/Delete Act, DROP.
- `assets/dilekce-sablonlari.md` — Faz 4'te başvuru metinlerini üretirken temel al; boş bırakılan alan kalmayacak şekilde doldur.
- `assets/bulgu-envanteri.csv` — Envanteri dosya olarak teslim edeceksen bu başlık yapısını kullan.
