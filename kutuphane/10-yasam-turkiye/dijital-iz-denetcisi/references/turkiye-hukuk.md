# Türkiye Hukuki Rotası

Özne Türkiye'deyse varsayılan rota budur. Bilgi verirsin, dava tahmini yapmazsın; ceza boyutu ve mahkeme başvurusu gerektiren kalemlerde avukatla çalışılması gerektiğini bir kez söyle.

---

## Rota haritası

```
Veri sorumlusuna başvuru (KVKK m.13)   ← ZORUNLU İLK ADIM
        ↓ 30 gün
   Yanıt yok / ret / yetersiz
        ↓
KVKK Kurulu'na şikâyet (m.14)          ← süreler hak düşürücü
        ↓ 60 gün (yanıt yoksa ret sayılır)
İdare mahkemesinde iptal davası
```

**Paralel rota:** Kişilik hakkı ihlali varsa 5651 s.K. m.9 kapsamında Sulh Ceza Hâkimliği'ne doğrudan erişim engelleme/içerik kaldırma başvurusu. Bu, KVKK rotasından bağımsız işler ve genelde daha hızlıdır.

---

## 1. Veri sorumlusuna başvuru (m.13)

**Atlanamaz.** İlgili kişi, veri sorumlusuna başvurmadan doğrudan Kurul'a şikâyette bulunamaz. Doğrudan yapılan şikâyetler usulden reddediliyor. (İstisna: zarara uğrama ihtimali veya telafisi imkânsız zarar doğacaksa Kurul doğrudan müdahale edebilir — ama Kurul'un bunu istisnai bir durum olarak kabul etmesi gerekir.)

**Geçerli başvuru yöntemleri** (Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında Tebliğ):
- Yazılı (ıslak imzalı, elden/noter/iadeli taahhütlü)
- KEP adresi
- Güvenli elektronik imza
- Mobil imza
- **İlgili kişinin daha önce veri sorumlusuna bildirdiği ve veri sorumlusunun sisteminde kayıtlı olan** e-posta adresi
- Veri sorumlusunun başvuru amacıyla geliştirdiği yazılım/uygulama

**En sık yapılan usul hatası:** Rastgele bir e-posta adresinden başvuru göndermek. Kayıtlı olmayan bir adresten gönderilen başvuru geçersiz sayılabiliyor ve tüm süreç boşa gidiyor. Kullanıcıya bunu net söyle — KEP veya sistemde kayıtlı adres kullanılmalı.

**Süre:** Veri sorumlusu en kısa sürede, en geç **30 gün** içinde yanıtlamak zorunda. Kural olarak ücretsiz; olağan dışı masraf doğarsa Kurul tarifesi üzerinden ücret talep edilebilir.

**Talebin dayanağı:** KVKK m.11 (ilgili kişinin hakları) + m.7 (silme, yok etme, anonim hale getirme). Silme talebi, işleme sebebinin ortadan kalkmış olmasına dayandırılır.

---

## 2. Kurul'a şikâyet (m.14)

**Süreler hak düşürücü** — kaçırılırsa şikâyet hakkı tamamen düşer. Kurul'un 2019/9 sayılı kararı üç senaryoyu netleştirmiş:

| Senaryo | Süre |
|---|---|
| Veri sorumlusu 30 gün içinde yanıt verdi (ret veya yetersiz) | Yanıtın öğrenildiği tarihten itibaren **30 gün**. Bu durumda başvuru tarihinden itibaren 60 günlük ek süre **yok**. |
| Hiç yanıt gelmedi | İlk başvuru tarihinden itibaren **60 gün** |
| Yanıt 30 günden geç geldi | İlk başvuru tarihinden itibaren **60 gün** |

**Nasıl:** `sikayet.kvkk.gov.tr` üzerinden e-Devlet ile, ya da yazılı olarak. Belgeler PDF yüklenir. Online şikâyetin alındı belgesi tarihi ispatlar — sakla.

**Dilekçe şartı:** 3071 sayılı Dilekçe Hakkının Kullanılmasına Dair Kanun m.6 şartlarını taşımayan dilekçeler incelemeye alınmıyor. Ad-soyad, imza, adres ve somut talep bulunmalı.

**Süreç:** Sekretarya ön inceleme (usul/şekil) → esastan inceleme → veri sorumlusundan savunma (veri sorumlusu istenen belgeleri **15 gün** içinde göndermek zorunda) → karar. Karar süresi pratikte 4-12 ay.

**Sonuç:** Kabul, ret veya kısmen kabul. Kurul idari para cezası uygulayabilir. Şikâyet tarihinden itibaren 60 gün içinde cevap verilmezse talep **reddedilmiş sayılır** ve idari yargıda dava süresi işlemeye başlar.

**Kurul kararına karşı:** 60 gün içinde idare mahkemesinde iptal davası (İYUK m.7).

---

## 3. Unutulma hakkı — arama motorları

**Dayanak:** Anayasa m.20/3 + KVKK m.4, 7, 11 + Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi Hakkında Yönetmelik m.8.

Kurul'un 23.06.2020 tarih ve **2020/481** sayılı kararı iki şeyi netleştirdi:
1. Arama motorları KVKK anlamında **veri sorumlusudur** — yani doğrudan onlara başvurulabilir.
2. Ad-soyadla yapılan aramada çıkan sonuçların indeksten çıkarılması talebi, unutulma hakkı kapsamındadır.

Kurum ayrıca "Unutulma Hakkının Arama Motorları Özelinde Değerlendirilmesi" başlıklı bir rehber yayımladı.

### Denge testi ve 13 kriter

Unutulma hakkı **mutlak değil, istisnai bir haktır.** Kurul, ilgili kişinin temel hak ve özgürlükleri ile kamunun bilgiyi edinmedeki menfaati arasında bir **denge testi** yapıyor. 2020/481 kararının ekindeki kriterler:

1. İlgili kişinin kamusal yaşamda önemli bir rol oynaması
2. Arama sonuçlarının öznesinin çocuk olması
3. Bilginin içeriğinin doğruluğu
4. Bilginin kişinin çalışma hayatı ile ilgisi
5. Bilginin hakaret, onur kırıcı, iftira niteliği taşıması
6. Bilginin özel nitelikli kişisel veri olması
7. Bilginin güncelliği
8. Bilginin kişi hakkında önyargıya sebep olması
9. Bilginin kişi açısından risk doğurması
10. Bilginin kişinin kendisi tarafından yayımlanmış olması
11. İçeriğin gazetecilik faaliyeti kapsamında olması
12. Bilgilerin yayınlanmasında yasal zorunluluk bulunması
13. Bilginin ceza gerektiren bir suçla ilgili olması

Kriterler sınırlı sayıda değil; Kurul somut olay bazında ek ölçüt getirebiliyor.

**Bu kriterleri denetim raporunda kullanma biçimi:** Her indeksten çıkarma talebi için, kriterleri lehte/aleyhte olarak sıralayıp bir başarı beklentisi çıkar. Bu, kullanıcının hangi taleplere emek harcayacağını bilmesini sağlar.

**Örnek okuma** (2020/927 sayılı karar): Kamu üniversitesinde çalışan bir kişinin, hakkındaki usulsüzlük iddialarına ilişkin haberlerin kaldırılması talebi reddedildi — bilgi doğruydu, çalışma hayatıyla ilgiliydi, güncel ve gazetecilik faaliyeti kapsamındaydı. Yani "haber doğru ve güncel ise" indeksten çıkarma zayıf bir taleptir; bunu kullanıcıya baştan söyle.

**Sıra:** Önce arama motoruna başvuru (Google/Yandex'in kendi formları) → ret veya yanıtsızlık → Kurul'a şikâyet **veya** doğrudan yargı yolu (Kurul her ikisinin de mümkün olduğunu açıkça belirtmiş).

---

## 4. 5651 s.K. m.9 — erişim engelleme / içerik kaldırma

İnternette kişilik haklarına saldırı niteliği taşıyan yayın, fotoğraf veya video için **Sulh Ceza Hâkimliği**'ne başvurulur. Talep: içeriğe erişimin engellenmesi ve/veya içeriğin kaldırılması.

Bu kanunun bir de özel bir imkânı var: belirli içeriklerin çıkarılmasına ek olarak, **kişinin adı ile URL arasındaki ilişiğin kesilmesine** karar verilip bunun doğrudan arama motorlarına uygulattırılması mümkün. Yani mahkeme kararı, Google'ın gönüllü değerlendirmesini devre dışı bırakan bir kaldıraç.

KVKK rotasından farkı: daha hızlı, daha güçlü, ama kişilik hakkı ihlali eşiği gerekiyor ve avukatla yürütülmesi gereken bir süreç.

---

## 5. Ceza boyutu (TCK 135-136-138)

- **TCK 135** — kişisel verilerin hukuka aykırı kaydedilmesi
- **TCK 136** — verileri hukuka aykırı verme, yayma veya ele geçirme
- **TCK 138** — verileri yok etmeme

**Önemli:** Bu suçlar **şikâyete bağlı değil, resen takip edilir.** Yetkili mercilere yapılan bildirim hukuken "şikâyet" değil "ihbar"dır; şikâyetten vazgeçme gibi bir kurum işlemez.

Bu, yasa dışı sorgu panellerinde verisi bulunan kullanıcı için pratik bir kaldıraç: Cumhuriyet Başsavcılığı'na ihbarda bulunmak için mağdur sıfatı ve şikâyet süresi tartışması yok.

**Paralel bildirim kanalları:** BTK / USOM (ihbar), CİMER.

---

## 6. Türkiye'ye özgü pratik notlar

**Ticaret Sicil Gazetesi:** Kurul'un 2022/6 sayılı kararı, TSG'nin limited şirket pay devri ilanlarında ad-soyadı yayımladığını ama **kimlik numarası ve adres bilgisini gizleyerek** ilan ettiğini tespit etti. Ticaret Sicili Yönetmeliği m.41 de gerçek kişilerin kimlik numaralarının ilan edilmeyeceğini düzenliyor. Kurul, şirket ortaklığının mevzuat gereği tescil ve ilan edilmesi nedeniyle **aleni bilgi** olduğunu değerlendirdi.

**Sonuç:** TSG'deki ad-soyad + ortaklık bilgisi kaldırılamaz — yasal yayın zorunluluğu var. Ama TSG verisini kazıyıp yeniden yayımlayan **özel şirket bilgi siteleri** ayrı birer veri sorumlusudur ve bunlar sıklıkla TSG'nin gizlediği alanları başka kaynaklardan birleştirip yayımlıyor. Denetimde hedef bunlardır. Raporda ayrımı net yaz, yoksa kullanıcı imkânsız bir hedefe emek harcar.

**Veri ihlali bildirimleri:** `kvkk.gov.tr/veri-ihlali-bildirimi` sayfasında ilan edilen ihlaller taranmalı — öznenin kullandığı Türk platformları bu listede olabilir. (Not: `ihlalbildirim.kvkk.gov.tr` formu yalnızca **veri sorumluları** içindir; ilgili kişi buradan bildirim yapmaz, `sikayet.kvkk.gov.tr` kullanır.)

**Yurt dışı veri sorumluları:** Google, Meta gibi şirketler Türkiye'de temsilci bulunduruyor ve KVKK başvuruları Türkiye'deki iletişim kanallarından yapılabiliyor — Kurul 2020/481 kararında bu kanalların ülkemizde kullanılabilir olmasını özellikle istemişti.

---

## 7. Rapora nasıl yazılır

Her Türkiye rotalı kalem için şu beş alanı doldur:

| Alan | İçerik |
|---|---|
| Veri sorumlusu | Kim (kaynak site sahibi / arama motoru / broker) |
| Başvuru kanalı | KEP / kayıtlı e-posta / form / noter |
| Hukuki dayanak | KVKK m.11-e + m.7, veya unutulma hakkı (2020/481), veya 5651 m.9 |
| Kritik tarih | Başvuru tarihi + 30 gün + şikâyet penceresi son günü |
| Başarı beklentisi | 13 kriterden lehte/aleyhte olanlar |

Kritik tarih sütununu **takvimlenmiş** ver. Hak düşürücü sürelerin kaçırılması, bu işte en sık görülen ve en telafisiz hatadır.
