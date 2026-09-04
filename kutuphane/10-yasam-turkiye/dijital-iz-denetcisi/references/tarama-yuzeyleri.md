# Tarama Yüzeyleri Kataloğu

Dokuz katman. Sırayla geç, her katmanda "bulundu / temiz / taranamadı" kaydı bırak.

## İçindekiler
1. [Arama motorları](#1-arama-motorlari)
2. [Veri simsarları ve kişi arama siteleri](#2-veri-simsarlari-ve-kisi-arama-siteleri)
3. [Sosyal medya ve platformlar](#3-sosyal-medya-ve-platformlar)
4. [Kullanıcı adı yayılımı](#4-kullanici-adi-yayilimi)
5. [Sızıntı veritabanları ve stealer log](#5-sizinti-veritabanlari-ve-stealer-log)
6. [Görsel ve biyometrik](#6-gorsel-ve-biyometrik)
7. [Arşiv ve önbellek](#7-arsiv-ve-onbellek)
8. [Türkiye'ye özgü kamu kayıtları](#8-turkiyeye-ozgu-kamu-kayitlari)
9. [LLM / AI yüzeyleri](#9-llm--ai-yuzeyleri)

---

## 1. Arama motorları

Tek motorla yetinme. Google, Bing (DuckDuckGo ve Ecosia Bing indeksini kullanır — Bing'de duran şey oralarda da durur), Yandex (Türkiye ve Rusça kaynaklarda Google'ın kaçırdığını yakalar) ve Yahoo/Brave ayrı ayrı bakılır.

**Sorgu kalıpları** — her birini ad varyantı × şehir kombinasyonuyla tekrarla:

```
"Ad Soyad"
"Ad Soyad" şehir
"Ad Soyad" telefon OR e-posta OR adres
"Soyad, Ad"                      → resmî liste ve PDF formatı
"05XX XXX XX XX"                 → numarayı tırnak içinde, boşluklu ve boşluksuz
"ad.soyad@domain.com"
"kullaniciadi"
site:linkedin.com "Ad Soyad"
filetype:pdf "Ad Soyad"          → kurum listeleri, katılımcı listeleri, bordro/rapor ekleri
filetype:xlsx OR filetype:csv "Ad Soyad"
intitle:"Ad Soyad"
"Ad Soyad" -site:linkedin.com -site:x.com   → bilinen profilleri eleyip kalanı gör
```

`filetype:` sorguları en verimli olanlar: kurumların yanlışlıkla yayımladığı katılımcı listeleri, başvuru sonuçları ve bordro ekleri neredeyse hep PDF/XLSX olarak indekste kalır.

**Kritik nokta:** Sonuçların ilk sayfasında durma. Veri simsarı kayıtları tipik olarak 3-5. sayfada oturur ve tam da bu yüzden kimse fark etmez. En az 5 sayfa in.

**Google'ın kendi izleme aracı:** `Results about you` (myactivity.google.com/results-about-you ya da Google uygulamasında profil → "Results about you"). Telefon, e-posta, ev adresi izliyor; Şubat 2026'dan itibaren pasaport, ehliyet ve devlet kimlik numaralarını da yakalayabiliyor. Bu bir tarama aracı olarak da işe yarar: kullanıcı kaydını yapsın, birkaç saat içinde eşleşen sonuçları listeler. Ancak veri simsarı kaldırma servisi değil — sadece Google Search görünürlüğünü yönetir; kaynak sayfalar ve diğer motorlar etkilenmez.

**Kişiselleştirmeyi kapat.** Kullanıcı kendi adını kendi hesabıyla ararsa Google ona kendi bildiği sonuçları önceliklendirir. Gizli pencerede, oturum kapalı, mümkünse farklı bir konumdan bakılmalı — "başkası benim adımı arayınca ne görüyor" sorusunun cevabı bu.

---

## 2. Veri simsarları ve kişi arama siteleri

ABD merkezli ekosistem büyük ve otomatik; öznenin ABD bağlantısı (yaşamış, çalışmış, hesap açmış) varsa mutlaka bak. Yoksa bile bazı brokerlar uluslararası kayıt tutar.

**Yüksek öncelikli hedefler** (tekil çıkarma, en yüksek görünürlük): Whitepages, Spokeo, BeenVerified, Radaris, Intelius, PeopleFinders, FastPeopleSearch, TruthFinder, Instant Checkmate, PeopleLooker, Nuwber, USPhoneBook.

**Konsolidasyon avantajı:** Bu siteler bağımsız değil. PeopleConnect ailesi (Intelius, TruthFinder, Instant Checkmate) tek akışla kapatılabiliyor; BeenVerified opt-out'u aynı veritabanını paylaşan kardeş markaları da bastırıyor; Whitepages'in alt siteleri ana suppression üzerinden gidiyor. Denetimde bunları tek satır olarak grupla — kullanıcı 12 form yerine 4 form doldursun.

**Ekosistem büyüklüğü:** Dünya çapında binlerce broker var ama tüketiciye görünür profil yayımlayan ~200 tanesi gerçek maruziyetin büyük çoğunluğunu oluşturuyor. İlk 20 compiler'ı kapatmak görünür maruziyetin yaklaşık %90'ını düşürüyor. Uzun kuyruğu Faz 2'ye bırak.

**Kayıt bulma yöntemi:** Broker sitelerinde doğrudan arama yapmak yerine, `site:whitepages.com "Ad Soyad"` gibi sorgularla Google üzerinden gir — hem daha hızlı hem broker'a yeni bir sorgu izi bırakmaz.

**Resmî sicil kaynakları:** California, Vermont, Texas ve Oregon eyalet broker sicilleri kayıtlı brokerların tam listesini yayımlıyor; Privacy Rights Clearinghouse bunları birleştiriyor. Hedef listesi çıkarırken bu sicilleri temel al, blog listelerine güvenme (opt-out URL'leri sık değişiyor).

**Kaydı ararken dikkat:** Kızlık soyadı, eski şehirler, sabit hat numarası, ad kısaltmaları ve hane halkı üyeleri ayrı kayıtlara bölünmüş olabilir. Tek profili kaldırmak, aynı kişinin üç ayrı kaydını bırakır.

---

## 3. Sosyal medya ve platformlar

Her platformda üç ayrı şeye bak: **profil görünürlüğü**, **geçmiş içerik**, **meta veri**.

| Platform | Ne aranır |
|---|---|
| LinkedIn | Genel profil görünürlüğü, iletişim bilgisi alanı, eski pozisyonlar, "kim profilini görüntüledi" ayarları, herkese açık gönderiler |
| X / Twitter | Eski tweetler (konum etiketi, telefon, işyeri ifşası), yanıtlar, beğeni geçmişi, arama motoru indekslemesi |
| Instagram / Facebook | Herkese açık gönderiler, etiketlenen fotoğraflar, arkadaş listesi görünürlüğü, "Hakkında" alanı, eski profil fotoğrafları (bunlar çoğu platformda kalıcı olarak herkese açık) |
| GitHub | Commit e-postaları (`git log --format='%ae' \| sort -u`), sızmış anahtar/token, iş programı çıkarımı için commit zaman damgaları, README'lerdeki iletişim bilgisi, gist'ler |
| YouTube | Eski videolar, yorum geçmişi, kanal "Hakkında" alanındaki e-posta |
| Reddit / forumlar | Terk edilmiş hesaplar, gönderi geçmişinden konum çıkarımı |
| Ekşi Sözlük / Türkçe forumlar | Takma ad üzerinden yazı geçmişi, kişisel detay ifşası |
| Strava / fitness | Aktivite haritaları — ev ve işyeri konumunu doğrudan verir; en çok atlanan yüzeylerden |
| Venmo / ödeme uygulamaları | Varsayılan herkese açık işlem akışları |

**Meta veri katmanı:** Yüklenen fotoğrafların EXIF verisi (bazı platformlar temizler, bazıları temizlemez), profil oluşturma tarihleri, "arkadaş öner" algoritmalarının açığa çıkardığı bağlantılar.

**Terk edilmiş hesaplar** en yüksek risk taşıyanlar: eski parolalarla korunuyorlar, 2FA yok, sahibi izlemiyor, ve genelde daha genç ve daha az dikkatli bir dönemin içeriğini taşıyorlar.

---

## 4. Kullanıcı adı yayılımı

Tek bir handle, unutulmuş onlarca hesabı açar. Araçlar:

- **WhatsMyName** (whatsmyname.app / whatsmyname.io) — 700+ site üzerinde topluluk tarafından bakımlanan veri seti, hâlâ en güncel olanı.
- **Sherlock** — komut satırı, aynı işi yapar.
- **Maigret** — Sherlock türevi, daha geniş kapsam.

Handle varyantlarını dene: `adsoyad`, `ad.soyad`, `ad_soyad`, `adsoyad91`, eski oyun/forum takma adları. Kullanıcıya "15 yaşında kullandığın nick neydi" diye sor — cevap genelde en riskli hesabı açar.

**Yanlış pozitif uyarısı:** Bu araçlar isim çakışması üretir. Her hit'i doğrula; doğrulanmamış hit'i rapora "olası" etiketiyle koy, kesin diye yazma.

---

## 5. Sızıntı veritabanları ve stealer log

**Have I Been Pwned** (haveibeenpwned.com) — birincil kaynak. Tarayıcıdan e-posta araması ücretsiz; ihlal bildirimlerine abone olunabilir. API erişimi ve alan adı araması ücretli katmanlarda; kendi alan adına sahip olan bir kullanıcı için (Faruk gibi) alan adı doğrulaması yapıp o alandaki tüm adresleri tek seferde taramak çok verimli. HIBP'nin bir MCP sunucusu da var — ajanik akışlarda doğrudan bağlanabilir.

**Pwned Passwords** — parola kontrolü tamamen ücretsiz ve k-anonimlik modeliyle çalışıyor: SHA-1 hash'in yalnızca ilk 5 karakteri gönderiliyor, parola makineden çıkmıyor. Kullanıcıya güvenle önerilebilir.

**Ne aranır:**
- Hangi sızıntıda, hangi alanlar açığa çıkmış (parola mı, adres mi, kimlik mi)
- Parola sızmışsa: aynı parolanın başka yerde kullanılıp kullanılmadığı (credential stuffing riski)
- Stealer log'ları — bunlar geleneksel ihlallerden farklı ve daha tehlikeli: kurbanın kendi makinesinden çalınmış oturum çerezleri ve kayıtlı parolalar. HIBP bunları ayrı kategoride tutuyor.

**Türkiye bağlamı:** Yerli platformlardan (e-ticaret, ilan siteleri, oyun platformları) kaynaklanan ihlaller KVKK'nın veri ihlali duyuruları sayfasında ilan ediliyor — kvkk.gov.tr/veri-ihlali-bildirimi. Öznenin kullandığı Türk servislerini bu listeye karşı kontrol et; HIBP Türk platformlarının hepsini kapsamıyor.

**Yapma:** Çalıntı veriyi arama yüzeyi olarak sunan "combolist" siteleri, Telegram kanalları, sorgu panelleri. Bunlara girmek verinin kendisini daha da yayar ve Türkiye'de TCK 136 kapsamındadır.

---

## 6. Görsel ve biyometrik

**Ters görsel arama:** Google Lens, TinEye, Yandex Görsel (yüz eşleştirmede belirgin şekilde daha agresif). Profil fotoğrafı, kurumsal headshot ve sosyal medyada paylaşılmış net yüz fotoğraflarıyla ayrı ayrı ara.

**Yüz arama motorları:** PimEyes, FaceCheck.ID, Clearview AI (Clearview tüketiciye kapalı ama veri talebi hakkı bazı yargı yetkilerinde işliyor). Bunlar ters görsel aramadan farklı çalışır — yüzü hash'leyip indeksler, yani fotoğrafın bulunduğu bağlamı hiç bilmeden eşleşme bulur.

**Kritik ayrım:** Bu motorlardan opt-out, fotoğrafı internetten silmez. Kaynak site fotoğrafı yayımlamaya devam eder; sadece yüzle aranarak bulunması engellenir. Raporda bunu net yaz.

**Her veritabanı ayrıdır.** PimEyes opt-out'u FaceCheck.ID'yi etkilemez. Her biri için ayrı başvuru gerekir.

---

## 7. Arşiv ve önbellek

Kaynak sayfa silinse bile içerik burada yaşamaya devam eder — ve denetimlerin en sık atladığı katman budur.

- **Wayback Machine** (web.archive.org) — `web.archive.org/web/*/site.com/*` ile domain bazlı tarama yapılabilir.
- **archive.today / archive.ph** — Wayback'in kaçırdıklarını yakalar; kaldırma politikası çok daha katı.
- **Google önbelleği ve snippet'leri** — sayfa gitmiş olsa da snippet'te kişisel veri durabiliyor.
- **Common Crawl** (index.commoncrawl.org) — LLM eğitim verisinin en büyük tek kaynağı ve doğrudan aranabiliyor. Kullanıcının adını, eski blog URL'sini veya handle'ını tırnak içinde, güncel bir crawl'da (ör. `CC-MAIN-2026-*`) ara. Burada çıkması, verinin eğitim boru hattına girmiş olma ihtimalinin somut kanıtıdır.
- **Haber arşivleri ve mirror siteler** — bir haber kaldırılsa da alıntılayan onlarca site kalır.

---

## 8. Türkiye'ye özgü kamu kayıtları

Bu katman ABD merkezli rehberlerde hiç geçmez ve Türkiye'deki gerçek maruziyetin büyük kısmını burası üretir.

**Rehber uygulamaları** — Getcontact, Truecaller ve benzerleri. Kullanıcının kendisi hiç yüklemese bile, rehberine kayıtlı biri yüklediyse numarası ve o kişinin verdiği isim etiketiyle havuzda. Türkiye'de neredeyse evrensel bir maruziyet. Kaldırma yolu için `kaldirma-kanallari.md`.

**Ticaret Sicil Gazetesi ve türevleri** — Şirket kurmuş, ortak olmuş veya yönetim kurulunda yer almış herkes için. Gazete'nin kendisi mevzuat gereği TCKN ve adresi gizleyerek ilan ediyor; asıl sorun bu ilanları kazıyıp yeniden yayımlayan **özel şirket bilgi siteleri**. Bunlar çoğu zaman gizlenmesi gereken alanları da başka kaynaklardan birleştirip yayımlıyor ve KVKK önünde ayrı bir veri sorumlusu konumundalar — yani ilanın kendisi kaldırılamaz ama türev site kaldırılabilir. `site:ticaretsicil.gov.tr` ve şirket adı + ad-soyad kombinasyonlarıyla ara.

**Meslek odaları ve birlikler** — Barolar, tabip odaları, mühendis odaları, SMMM odaları üye listelerini iletişim bilgisiyle yayımlayabiliyor.

**Kurum duyuruları** — Üniversite sınav/atama sonuçları, kamu kurumu ilanları, KPSS/atama listeleri. Bunlar tipik olarak PDF ve tam ad + TCKN'nin bir kısmını içeriyor. `filetype:pdf "Ad Soyad"` sorgusu bunları yakalar.

**Resmî Gazete** — atamalar, ihaleler, kararlar.

**e-Devlet ve tapu/icra** — Doğrudan herkese açık değil ama bazı sorgu sonuçları üçüncü taraf sitelere sızmış olabilir.

**Yasa dışı sorgu panelleri** — Çalıntı MERNİS/GSM verisi satan siteler. Bu skill bunları **kullanmaz ve adres vermez.** Kullanıcı verisinin böyle bir sitede olduğunu bildirirse: bulguyu kaydet, rotayı savcılık ihbarı (TCK 135/136 — resen takip edilen suçlar, şikâyet şartı yok) + BTK/USOM bildirimi olarak kur, siteyi ziyaret etme.

---

## 9. LLM / AI yüzeyleri

2026 itibarıyla ayrı bir katman ve çoğu denetim rehberinde hâlâ yok.

**Üç ayrı boru hattı var, karıştırılmamalı:**

1. **Eğitim verisi** — Model ağırlıklarına girmiş veri. Geriye dönük çıkarılamaz. Yapılabilecek tek şey, gelecek eğitim turlarından çıkmak.
2. **Web erişimi / RAG** — Model cevap verirken canlı web'i çekiyor. Burada kaynak sayfayı temizlemek doğrudan işe yarar; eğitim ayarlarının hiçbir etkisi yok. Bir kullanıcı ChatGPT eğitiminden çıktığı hâlde Gemini'nin hakkında doğru bilgi vermesinin sebebi tam olarak bu ayrımdır.
3. **Sohbet geçmişi** — Kullanıcının kendi girdilerinin eğitimde kullanılması. Ayardan kapatılır.

**Tarama yöntemi:** ChatGPT, Claude, Gemini, Perplexity ve Grok'a öznenin adını sorup ne döndüğünü kaydet. "X kimdir", "X'in iletişim bilgileri", "X nerede çalışıyor" gibi varyantlarla. Modelin ürettiği yanlış bilgi de bir bulgudur — itibar açısından doğru bilgi kadar önemli olabilir.

**Common Crawl kontrolü** (bkz. katman 7) bu katmanın kanıt tabanını verir.
