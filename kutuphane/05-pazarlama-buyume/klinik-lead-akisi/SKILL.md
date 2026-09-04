---
name: klinik-lead-akisi
description: Terapi Panel için psikoloji kliniği adayı bulma, Attio CRM'e ekleme, uygunluk puanlama, 6 puan üstüne tanıtım maili gönderme ve statü güncelleme akışı. "Yeni klinik bul", "lead ara", "CRM'e ekle", "kliniklere mail at", "PDR listesini büyüt", "aday tara", "takip maili" gibi isteklerde kullan. Ayrıca haftalık aday taraması ve gönderim sonrası statü bakımı için de bu akışı izle.
---

# Klinik lead akışı

Tek cümlelik amaç: İstanbul ve çevresindeki psikoloji merkezlerinden Terapi Panel'e uygun olanları bulup, Attio'daki **PDR Klinikler** listesine puanlanmış halde yazmak, uygunluk puanı 6 ve üstü olanlara kişiselleştirilmiş tanıtım maili göndermek, sonra statüyü ve takip tarihini güncellemek.

Akış altı adım: **Ara → Zenginleştir → Puanla → CRM'e yaz → Mail at → Statü güncelle.**

---

## Adım 0. Her turdan önce kontrol et

| Konu | Kural |
|---|---|
| Gönderim hacmi | Günde en fazla 20 ila 30 mail. Bu bir soğuk gönderim değil, birebir yazışma hacmi; hem sınırların altında kalır hem itibar bozmaz. |
| Kimlik doğrulama | Gönderen alan adında SPF ve DKIM şart, DMARC en az `p=quarantine`. Bunlar yoksa gönderime başlama, önce onu çözdür. |
| İYS | Alıcı tacir veya esnafsa önceden onay gerekmiyor, fakat adresin İYS'ye kaydı ve ret hakkı kontrolü gerekiyor. Toplu gönderime geçmeden önce İYS tarafını netleştir. |
| Şikâyet oranı | Spam şikâyeti binde 1'i geçerse itibar bozulur, binde 3'te alan adı cezalanır. Her maile ret cümlesi koy: "Bu tür mailleri almak istemezseniz tek kelime yazmanız yeterli, listeden çıkarırım." |
| Sunum | Sunum PDF'i mail bağlayıcısına ek olarak sığmıyor. Her zaman paylaşım linki kullan. |

---

## Adım 1. Lead arama

Amaç, rastgele klinik listesi değil. Aranan profil: **birden fazla uzmanın aynı mekânı ve aynı kasayı paylaştığı, seans dışında oda kiralama veya gelir paylaşımı yapan, sekreteri olan, tek şubeden büyük ama zincir olmayan merkez.** Tek kişilik ofis de, otuz şubeli zincir de bu ürünün müşterisi değil.

Kaynakları şu sırayla tara, çünkü üstteki kaynaklar hem daha hızlı hem daha nitelikli aday veriyor.

### 1.1 Acı sinyali taşıyan ilanlar (en yüksek isabet)

En hızlı yol, sorunu zaten kabul etmiş klinikleri bulmak. İş ilanı sitelerinde şu aramalar doğrudan aday listesi üretir:

- "klinik yöneticisi" psikoloji merkezi
- "klinik sekreteri" veya "hasta karşılama" psikolojik danışmanlık
- "randevu sorumlusu" terapi merkezi

İlan veren merkez, operasyon yükünü insan alarak çözmeye çalışıyor demektir. Açılış cümlen hazır gelir. Sade Zihin bu şekilde bulundu ve listedeki en güçlü sinyal oldu.

### 1.2 Oda kiralama satan merkezler (en yüksek uygunluk)

Ürünün tam karşılığı burada. Arama kalıpları:

- terapi odası kiralama İstanbul saatlik
- "kiralık terapi odası" veya "paylaşımlı ofis" psikolog
- site içi arama: `site:*.com "oda kiralama" psikoloji`
- "ofis kiralama" psikoloji merkezi fiyat listesi

Fiyat listesini yayınlamış olanları öne al. Fiyatı yayınlayan merkez, doluluğu ölçmek zorunda olan merkezdir. Kim Psikoloji, Anatolia, Mental Ofis, Psikomental ve Psikoloji Ağı bu aramadan çıktı.

### 1.3 Harita taraması

Google Haritalar'ı ilçe ilçe tara, tek seferde bütün İstanbul'u değil. İlçe listesi ile "psikolojik danışmanlık merkezi", "psikoloji merkezi", "terapi merkezi", "aile danışmanlık merkezi" terimlerini çaprazla.

Places API kullanacaksan bil ki: Text Search çağrıları bin çağrı başına ücretlendiriliyor ve istediğin alan üst kademeye giriyorsa fiyat yükseliyor, ayda ilk beş bin çağrı ücretsiz. Daha önemlisi **API e-posta adresi dönmüyor**, yalnızca telefon ve site veriyor. Yani mail bulma işi her hâlükârda site taramasına kalıyor. Küçük hacimde elle tarama, API kurmaktan hızlıdır.

Eleme kısayolu: yorum sayısı 30'un altındaysa ve sitede tek isim geçiyorsa muhtemelen tek kişilik ofistir, atla.

### 1.4 Dizinler ve dernekler

- DoktorTakvimi psikoloji ve psikolojik danışmanlık şehir sayfaları, merkez adıyla listelenenleri al, tek çalışan profilleri eleme.
- Türk PDR Derneği ve benzeri meslek örgütü üye listeleri.
- Aile ve Sosyal Hizmetler il müdürlüklerinin ruhsatlı özel aile danışma merkezi listeleri. Bu liste ruhsatlı ve kurumsal merkezleri verir, ancak merkezî tek bir yayın yok, il müdürlüğü üzerinden istenmesi gerekir.

### 1.5 Yeni açılan ve büyüyen merkezler

Yeni ofise taşınan veya yeni şube açan klinikte sistem kurma penceresi açıktır. İki yol:

- Ticaret Sicili Gazetesi üzerinden yeni kuruluş ve unvan sorgusu. Açık bir API yok, sorgulama arayüzünden ya da e-Devlet üzerinden bakılır, bu yüzden bunu haftalık değil aylık tur olarak yap.
- Instagram konum ve hashtag taraması: yeni ofis paylaşımları, ikinci hesap açılışları, atölye ve grup duyuruları. Grup ve atölye satan merkez, kontenjanı elle tutuyor demektir, bu da ayrı bir kanca.

### 1.6 Hızlandırma kuralları

1. **Tur başına ilçe seç.** Bir turda tek ilçe, on beş ile yirmi aday. Bütün şehri tek seferde taramak yarım kalmış listeye yol açıyor.
2. **Önce ele, sonra zenginleştir.** Adayın uygunluğunu telefon ve site bakmadan, yalnız isim, yorum sayısı ve ekip büyüklüğünden kabaca kes. Zenginleştirme pahalı adım, onu yalnız hayatta kalanlara uygula.
3. **Tekrarı domain ve telefondan yakala.** Aynı ekip birden fazla Google kaydı işletiyor olabilir. Erguvan bunun örneği, Çapa hattında dört ayrı kayıt var.
4. **Bulduğun her adayı aynı turda CRM'e yaz.** Ara adımda not tutma, kayıt tek yerde dursun.

---

## Adım 2. Zenginleştirme ve mail bulma

Sırayla dene, ilk bulduğunda dur:

1. Sitenin iletişim sayfası ve alt bilgi. `mailto:` bağlantısını ara.
2. Sitenin künye, hakkımızda, kariyer ve KVKK aydınlatma metni sayfaları. KVKK metinlerinde iletişim adresi neredeyse her zaman yazar, çoğu kişi bunu unutuyor.
3. Instagram biyografisi ve linktree bağlantıları.
4. LinkedIn şirket sayfası.
5. Google kaydındaki site alanı boşsa ve yalnız telefon varsa, o kaydı **arama listesine** al, mail listesine değil.

Dikkat edilecek iki durum:

- **Cloudflare e-posta koruması.** Sayfada adres `[email protected]` gibi görünüyorsa adres gizlenmiştir, tarayıcıda açıp okumak gerekir. Sade Zihin'de bu çıktı.
- **Sertifikası bozuk site.** Süresi dolmuş sertifika sayfayı okunamaz yapar. Psikoloji Ağı bu yüzden hâlâ mailsiz duruyor. Bu aynı zamanda bir kanca: teknik tarafın sahipsiz olduğunu gösterir.

**Asla tahmini adrese mail atma.** `info@` diye deneme yapma. Adres doğrulanamıyorsa kaydı telefonla aranacaklar kuyruğuna al ve `sonraki_adim_6` alanına "mail adresi doğrulanamadı, telefonla ulaş" yaz.

---

## Adım 3. Puanlama

`uygunluk` alanı 0 ile 10 arası. Şu tablodan topla, 10'da kes:

| Sinyal | Puan |
|---|---|
| Oda kiralama veya gelir paylaşımı satıyor, hele fiyat listesi yayında | +4 |
| Sekreter veya resepsiyon var | +1 |
| Dört ve üzeri terapist | +2 |
| Sekiz ve üzeri oda | +1 |
| Açık acı sinyali: klinik yöneticisi ilanı, randevu şikâyeti, yeni şube, yeni ofis | +2 |
| Grup, atölye veya test hattı gibi ikinci bir iş kolu | +1 |
| İki veya üç şube | +1 |
| Tek kişilik ofis | 0'a çek |
| Beş ve üzeri şubeli zincir | En fazla 6, kurucuya doğrudan ulaşılacaksa değer |

Eşikler: **8 ve üstü** hemen mail ve aynı hafta telefon. **6 ile 7** mail. **3 ile 5** mail yok, telefonla arama kuyruğu. **3 altı** backlog, dokunma.

---

## Adım 4. Attio'ya yazma

Liste: `pdr_klinikler`, ana nesne `companies`.

| Alan | Ne yazılır |
|---|---|
| `asama` | Yeni kayıt `Aday`. Diğer değerler: Temas kuruldu, Nitelendi, Demo yapıldı, Pilot, Kazanıldı, Beklemede, Elendi |
| `uygunluk` | Adım 3'teki puan |
| `tetikleyici` | Neden şimdi bu klinik, tek paragraf, kanıtıyla |
| `gelir_modeli` | Oda Kirası, Komisyon gibi |
| `oda_sayisi`, `terapist_sayisi`, `sekreter_var_mi` | Doğrulanabildiği kadarıyla |
| `sonraki_adim` | Tarih |
| `sonraki_adim_6` | Ne yapılacağı, açılış cümlesiyle birlikte |
| `durum`, `diger_sosyal_medya_vb` | Serbest notlar |

Şirket kaydının `description` alanına araştırmanın tamamını yaz, liste alanları özet kalsın. Yazmadan önce domain ve telefonla tekrar kontrolü yap.

---

## Adım 5. Mail

Yalnız `uygunluk >= 6` olanlara. Gmail bağlayıcısı ile, **`htmlBody` kullanarak**.

### Biçim kuralları

- Linkleri anchor olarak yaz: `<a href="https://abdullahfaruk.com">abdullahfaruk.com</a>`. Düz metne çıplak adres yazarsan Gmail onu `google.com/url?q=...` takip linkine çeviriyor ve imza berbat görünüyor.
- **Tire ve uzun çizgi kullanma.** Cümleleri virgülle ve noktayla kur.
- Yapay zekâ kokan kalıp yok: "umarım bu mail sizi iyi bulur", üç maddelik süslü listeler, "heyecan verici çözüm" gibi ifadeler yasak. Sözel yaz, konuşur gibi.
- Uzunluk beş paragrafı geçmesin.

### İskelet

1. Kim olduğun, tek cümle. "Terapi Panel adında bir klinik yönetim paneli geliştiriyorum."
2. **Kanca.** O kliniğe özel, kanıtlı, tek paragraf. Sonunda bir soru: bunu bugün neyle çeviriyorsunuz?
3. Panelin o kancaya verdiği cevap. Genel özellik listesi değil, o soruna ne yaptığı.
4. Referans cümlesi: paneli kullanan kliniklerin olduğu ve ay sonunun dert olmaktan çıktığı.
5. Sunum linki, sonra ihtiyaç sorusu: şu an sizi en çok yoran iş ne, panelde karşılığı var mı beraber bakalım.

### İmza

```
Abdullah Faruk Çiftler
Terapi Panel
abdullahfaruk.com
0506 631 68 42
```

### Konu satırı

Klinik neyi dert ediyorsa onu yaz. "20 odanın doluluğu ve hakediş hesabı üzerine" gibi. Kampanya dili, ünlem ve büyük harf yok.

---

## Adım 6. Statü ve takip

Mail gittikten hemen sonra, aynı turda:

1. Şirket kaydına not aç: konu, kanca, ne soruldu, hangi adrese gitti.
2. Liste kaydında `asama` alanını **Temas kuruldu** yap.
3. `sonraki_adim` alanına gönderimden beş iş günü sonrası tarihi yaz.
4. `sonraki_adim_6` alanına takip planını yaz: yanıt yoksa hangi numara aranacak, hangi cümleyle.

Takip ritmi:

| Zaman | Hareket |
|---|---|
| T+5 gün | Telefon. Mailden değil, kancadan gir. |
| T+12 gün | Kısa ikinci mail, aynı başlık altında yanıtla, yeni bilgi ekle. |
| T+25 gün | Yanıt yoksa `Beklemede`. Üç ay sonra yeni bir tetikleyici çıkarsa geri aç. |
| Ret gelirse | `Elendi` ve sebebini not düş. Bir daha mail atma. |

Her turun sonunda şunu ölç: hangi kanca tipi yanıt getiriyor. Oda kiralama kancası mı, ilan kancası mı, randevu şikâyeti kancası mı. Sonraki turda arama sırasını buna göre değiştir.

---

## Adım 5.5. Gönderimden sonra bounce kontrolü

Statüyü güncellemeden önce Gmail'de `from:mailer-daemon newer_than:1d` ara. 26.08.2026'da giden sekiz mailin ikisi `550 5.1.1` ile geri döndü, ikisi de siteden değil aramadan bulunmuş adreslerdi, ama CRM'de "Temas kuruldu" yazıyordu. Geri dönen kayıtta:

1. `asama` alanını **Aday**'a çek.
2. `email` alanını boşalt, yanlış adres bir daha kullanılmasın.
3. `sonraki_adim_6` alanına "mail geri döndü, adres yok, telefonla ara" yaz ve numarayı koy.

Ayrıca **Google araması Google'ın kendi sayfası üzerinden yapılabilir.** Tarayıcıda bir arama sonucu sayfası açıkken sayfa bağlamında `fetch('/search?q=...')` çalışır ve tam sonuç HTML'i döner; doğrudan gezinmede Google yalnız yerel sonuç kutusunu render ediyor. Bing ve DuckDuckGo bu iş için işe yaramadı.

---

## Adım 7. Türkiye geneli tarama workflow'u

İstanbul dışına çıkarken tek tek aramak yerine bölge bölge fan-out yap. 26.08.2026'da kurulan akış yedi bölgeye birer tarama ve birer zenginleştirme ajanı koyuyor (14 ajan): Ankara · İzmir · Bursa-Eskişehir-Kocaeli-Sakarya · Antalya-Muğla-Denizli-Aydın · Adana-Mersin-Gaziantep-Hatay · Konya-Kayseri-Samsun-Trabzon-Diyarbakır · İstanbul Anadolu yakası. Tarama ajanı bölge başına en az 12 aday çıkarıyor, zenginleştirme ajanı aynı bölgenin adaylarını doğrulayıp puanlıyor ve maile girecek kanca paragrafını da yazıyor.

O turda 111 aday, 23'ü 6 puan ve üzeri, 18'inin adresi doğrulandı, 17 tekil kliniğe mail gitti, hiçbiri geri dönmedi.

Ajan istemine mutlaka konması gerekenler:

1. **Tahmini adres yasak.** Adresi kliniğin kendi yayınında görmediyse alanı boş bıraksın ve sebebini yazsın. Bu kural sayesinde beş klinik "adres yok" diye telefon kuyruğuna düştü, uydurma adrese mail gitmedi.
2. **Hariç listesi.** Mevcut CRM kayıtlarını isim ve alan adıyla iste, yoksa aynı klinikleri tekrar buluyor.
3. **Kanca paragrafını ajan yazsın**, tire kullanmadan ve o kliniğe özel kanıtla. Mail yazarken sıfırdan uğraşmıyorsun.
4. **Puanlama tablosunu istemin içine koy**, ajanlar kendi ölçütünü uydurmasın.

Eşik altı kalanların `eleme_sebebi` alanını da doldurt; sonraki turda aynı kliniği yeniden araştırmamak için o gerekçe işe yarıyor.

---

## Adım 7. Fiyat ve görüşme

Fiyat konuşmasına girmeden önce `fiyat-mimarisi.md` dosyasını oku. Özet kurallar:

- Bant **aktif uzman** sayısıyla belirlenir, kayıtlı kadroyla değil.
- Yıllık peşin, on iki ayın on ay fiyatına verilmesidir.
- Ömür boyu lisans **yirmi aylık bedeldir**, bu oran pazarlıkta bozulmaz. Bozulursa aylık model ölür ve fiyat keyfi görünür.
- Karşılıksız indirim yok, tavan yüzde 40, daha aşağısı gerekiyorsa fiyat değil kapsam küçültülür.
- Gerekçe üründen verilir, kendi ekip kısıtından değil.
- Fiyat tek mesajda söylenir, kapanış her zaman tarihlidir.
