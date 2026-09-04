# Yaşam & Türkiye Hizmetleri

Satın alma, seyahat, vize, hak arama, dijital mahremiyet, etkinlik ve bölgesel mevzuat.

11 skill. Üst dizin: [../../README.md](../../README.md)

## `arac-uzmani`

[SKILL.md](arac-uzmani/SKILL.md)

Türkiye pazarı için 2. el ve sıfır araç uzmanı — kullanıcının bütçe, şehir, kilometre, yaş, yakıt, vites, kasa tipi gibi kısıtlarına göre "sorun çıkarmayacak", kronik arızası bilinmeyen veya az olan araçları önerir; kronik sorunlu motor/şanzıman kombinasyonlarını eler; sıfır araçta güncel fiyat/kampanya araştırır; 2. elde ilan araması, Tramer/ekspertiz kontrol listesi ve pazarlık noktaları üretir. Kullanıcı "hangi arabayı alayım", "X TL'ye araba", "2. el önerin", "sıfır mı 2. el mi", "bu araba alınır mı", "şu motor sorunlu mu", "kronik arıza", "km'si düşük araba", belirli bir model/motor hakkında güvenilirlik sorusu sorduğunda ya da bir ilan linki/ekran görüntüsü paylaşıp görüş istediğinde bu skill'i kullan. "Araba" kelimesi geçmese bile bütçe + araç sınıfı + kısıt kombinasyonu varsa (örn. "300 bine aile aracı lazım, İstanbul içi") devreye gir. Alım-satım kararının son sözünü ekspertiz verir; skill bunu asla atlatmaz.

- **Ölçü:** 7.550 bayt · 2 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `dijital-iz-denetcisi`

[SKILL.md](dijital-iz-denetcisi/SKILL.md)

Bir kişinin kendi (veya açık yetki verdiği bir müvekkilin) dijital ayak izini uçtan uca tarar — arama motorları, veri simsarları, sosyal platformlar, sızıntı veritabanları, yüz arama motorları, arşivler, Türkiye'ye özgü kamu kayıtları ve LLM/AI yüzeyleri. Sonra her bulgu için hangi kanaldan, hangi hukuki dayanakla, hangi sürede kaldırılacağını gösteren önceliklendirilmiş bir denetim raporu üretir. Kullanıcı "dijital izimi tara", "googleda adımı arayınca çıkanları sildir", "kişisel bilgilerim internette", "unutulma hakkı", "veri simsarlarından çıkmak istiyorum", "numaram/adresim ortada", "eski hesaplarımı bul ve sil", "OSINT self-audit", "remove my info from Google", "data broker opt-out", "right to be forgotten" dediğinde kullan. Ayrıca kamusal bir role girmeden önce, bir sızıntıdan etkilendiğinde, taciz/stalk/doxxing durumunda ya da "hakkımda ne bulunuyor" dediğinde — "denetim" demese bile — devreye gir. Sadece öznenin kendisi veya yetkili temsilcisi için çalışır; üçüncü kişi hakkında dosya çıkarmaz.

- **Ölçü:** 13.621 bayt · 6 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `hak-arama-turkiye`

[SKILL.md](hak-arama-turkiye/SKILL.md)

Türkiye'de tüketici, abonelik, kamu hizmeti ve idare kaynaklı mağduriyetlerde doğru mercii bulan, escalation basamaklarını sırayla kuran ve her basamak için hazır dilekçe/başvuru metni üreten hak arama uzmanı. Ayıplı ürün, iade/cayma, kargo kaybı, internet-telefon aboneliği, elektrik/doğalgaz/su faturası ve kesintisi, banka ücreti, sigorta reddi, belediye hizmeti, e-Devlet başvurusu ve idari işlemlerde kullan. Kullanıcı "şikayet edeceğim", "nereye başvurayım", "hakkımı nasıl ararım", "para iadesi", "dilekçe yaz", "CİMER", "hakem heyeti", "tüketici mahkemesi", "BTK", "EPDK", "ombudsman", "cevap vermiyorlar", "faturayı haksız kestiler", "ürün ayıplı çıktı", "kargo kayboldu", "su/elektrik kesik" dediğinde devreye gir. "Şikayet" kelimesi hiç geçmese bile bir kurumla/şirketle yaşanan çözümsüz sorun anlatılıyorsa uygula. Parasal sınırları, süreleri ve başvuru adreslerini ASLA ezberden verme — her seferinde canlı doğrula. Avukat değildir; dava stratejisi değil, idari hak arama yolu kurar.

- **Ölçü:** 6.379 bayt · 2 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `konaklama-kesif`

[SKILL.md](konaklama-kesif/SKILL.md)

Global konaklama keşif uzmanı — herhangi bir ülke/şehir için HER SORGUDA üç kanalı birden — otel, Airbnb/apart/daire ve hostel-private/pansiyon — ve yerel kiralık seçeneklerini SADECE OTA'larla sınırlı kalmadan (yerel forumlar, Facebook grupları, Telegram kanalları, Reddit, yerel rezervasyon siteleri) tarar; en merkezi ve ulaşımı kolay bölgelerde, özel banyolu seçenekleri, TL bazında fiyatlarla, misafir yorumları + WiFi kalitesi + çevre bilgisiyle sunar. Paralel (karaborsa) döviz kuru olan ülkelerde resmi kur ve karaborsa kurunu ayrı ayrı gösterir ve fiyatı her iki kurla TL'ye çevirir. Kullanıcı "X ülkesinde Y şehrinde şu kadar gün kalacağım", "nerede kalayım", "otel bul", "Airbnb bak", "konaklama araştır", "ucuz pansiyon", "aylık kiralık daire", "where to stay in..." dediğinde ya da herhangi bir seyahat planında konaklama ayağı gündeme geldiğinde bu skill'i kullan — kullanıcı "skill" veya "detaylı araştır" demese bile. Otel/kur bilgisini asla ezberden verme; her seferinde canlı web araştırması yap.

- **Ölçü:** 7.529 bayt · 2 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `kultur-sanat-radari`

[SKILL.md](kultur-sanat-radari/SKILL.md)

Belirli bir tarih aralığında ve şehirde (İstanbul başta olmak üzere Türkiye ve yurt dışı) açık olan sergileri, bienalleri, müze programlarını, konser/sahne etkinliklerini, atölye ve söyleşileri canlı web araştırmasıyla tarar; bitiş tarihi yaklaşanları öne çıkarır, ücretsiz/indirimli günleri ve müze kart kapsamını çıkarır, semt semt gerçekçi bir hafta sonu veya akşam rotası kurar (yürüme mesafesi, kapalı günler, yemek molası dahil). Kullanıcı "bu hafta sonu ne yapsak", "hangi sergiler var", "gezilecek yer", "sergi öner", "müzeye gidelim", "konser var mı", "atölye", "bienal", "ücretsiz müze", "şu şehirdeyim ne görmeliyim", "kapanmadan yetişmem gereken sergi" dediğinde kullan. Bir seyahat planı ya da boş bir hafta sonu konuşuluyorsa kullanıcı sormasa bile kültür programını gündeme getir. Sergi tarihleri ve bilet fiyatları hızla değişir ve sergiler kapanır — ASLA ezberden program verme, her seferinde canlı ara ve kurumun kendi sayfasından doğrula.

- **Ölçü:** 5.007 bayt · 1 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `schengen-randevu-tr`

[SKILL.md](schengen-randevu-tr/SKILL.md)

Türkiye'den Schengen vize randevusu bulma operasyonu uzmanı — hangi ülkenin hangi başvuru merkezinde (iDATA/VFS Global/BLS/Kosmos/AS-Visa) olduğunu ve hangi randevu mekaniğinde çalıştığını (kronolojik bekleme listesi mi, açık takvim slot avı mı, aracısız konsolosluk portalı mı) tespit eder; ikamet yetki bölgesi, doğru vize kategorisi, 59 ay parmak izi kuralı, vekaletle başvuru, randevusuz başvuru muafiyetleri, grup başvurusu ve cascade (uzun süreli çok girişli vize) kaldıraçlarını uygular; canlı doğrulamayla tarih damgalı bir randevu operasyon planı, takip kadansı ve geriye dönük takvim üretir. Kullanıcı "randevu bulamıyorum", "randevu yok", "randevu ne zaman açılıyor", "hangi ülkeden başvursam", "bekleme listesi", "iDATA", "VFS", "Kosmos", "BLS", "randevu botu var mı", "acenteye para vereyim mi" dediğinde; bir Avrupa seyahati planlanırken randevu darlığı gündeme geldiğinde — kullanıcı sormasa bile — bu skill'i kullan. Randevu botu yazmaz, aracı önermez, sahte kategori/ülke beyanı kurgulamaz.

- **Ölçü:** 9.198 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `suriye-is-mevzuat`

[SKILL.md](suriye-is-mevzuat/SKILL.md)

Suriye'de iş yapmanın tüm hukuki ve kurumsal katmanını Türk vatandaşı perspektifinden yöneten uzman — şirket kurma (LLC/JSC/şube), Yatırım Kanunu 18/2021 + KHK 114/2025 teşvikleri ve SIA süreçleri, vergi reformu, iş/çalışma hukuku ve çalışma izni, bankacılık/para transferi, yaptırımların güncel durumu, teknoloji/SaaS/telekom/e-ticaret lisansları ve ilgili tüm kurumlar (SIA, MoCT, Merkez Bankası; TR'de Ticaret Bakanlığı, GİB). Kullanıcı 'Suriye'de şirket kurmak', 'Suriye mevzuatı', 'Şam'da ofis', 'Suriye'ye yazılım/SaaS satmak', 'yaptırımlar ne durumda', 'Suriye'de vergi/çalışma izni/banka hesabı', 'hangi kuruma başvurulur' dediğinde kullan. Suriye'ye dönük bir girişim, ürün veya pazar konuşulurken hukuki/kurumsal boyut geçtiği anda — 'mevzuat' kelimesi hiç geçmese bile — devreye gir. Suriye mevzuatı geçiş hâlinde: oran, ücret, kural ve kurum bilgisini ASLA ezberden verme; her seferinde canlı doğrula ve tarih damgası koy. Avukat değildir; nihai söz yerel avukat ve mali müşavirindir.

- **Ölçü:** 7.839 bayt · 5 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `tech-etkinlik-kesif`

[SKILL.md](tech-etkinlik-kesif/SKILL.md)

Belirli bir tarih/tarih aralığında, belirli bir ülke veya şehirdeki yerel IT, yazılım, startup ve girişimcilik etkinliklerini (meetup, konferans, hackathon, demo day, workshop, öğrenci topluluğu ve kolektif buluşmaları dahil) canlı web araştırmasıyla kapsamlı biçimde bulur ve her biri için adım adım "nasıl katılırım" talimatı üretir. Kullanıcı "X ülkesinde/şehrinde şu tarihte ne var", "etkinlik bul", "meetup var mı", "hackathon arıyorum", "konferansa katılmak istiyorum", "tech events in [country]", "öğrenci topluluğu etkinlikleri", "GDG/IEEE/ACM buluşması", "startup ekosistemi etkinliği", "demo day", "networking etkinliği" dediğinde bu skill'i kullan. "Etkinlik" kelimesi hiç geçmese bile — "o hafta Berlin'deyim, yazılımcılarla tanışmak istiyorum" gibi — niyet yerel tech/startup sahnesine katılım ise devreye gir. Etkinlik organize etme taleplerinde kullanma; bu skill keşif ve katılım içindir.

- **Ölçü:** 7.918 bayt · 1 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `ucuz-bilet-avcisi`

[SKILL.md](ucuz-bilet-avcisi/SKILL.md)

Hunts underpriced flights out of Istanbul and turns a vague travel wish into a ranked, evidence-backed shortlist with ready-to-click search links. Two modes — open-destination deal hunting ("perşembe gidiş pazar dönüş fırsat var mı", "vizesiz nereye ucuz uçarım", "error fare var mı", "bu fiyat indirimli mi") and targeted routing, especially Umrah ("umre için bilet ara", "Cidde mi Medine mi", "aktarmalı mı aktarmasız mı", "kampanyalı bilet var mı", "başka tarihte avantajlı mı"). Also for judging a quoted fare, open-jaw versus return, IST versus SAW, Ramadan/Hajj/holiday price peaks. Adapts to environment — chat gathers campaign evidence and hands over links; a Chrome extension or browser MCP reads live fares off Google Flights date grids and Explore maps; Claude Code builds a price-history store with empirical scoring and cron monitoring ("fiyat takibi kur", "kampanyaları tara", "fırsat çıkınca haber ver", "uçuş fiyatı botu"). Use it even when the person never says "ucuz". Never invents prices.

- **Ölçü:** 15.040 bayt · 7 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/projects/ucakbileti/.claude/skills/ucuz-bilet-avcisi

## `urun-kesif`

[SKILL.md](urun-kesif/SKILL.md)

E-ticaret ürün araştırmacısı — belirli bir ürünün en uygun fiyatla nereden alınacağını bulur VEYA bir ürün tarifi/ihtiyaç tanımından yola çıkıp "en uygun ama kaliteli" seçeneği ve alternatiflerini önerir. Giyim, elektronik, ev, kozmetik, spor — kategori bağımsız çalışır. Kullanıcı "X'i en ucuza nereden alırım", "şöyle bir şey arıyorum, ne alayım", "fiyat/performans en iyisi hangisi", "bu ürünün alternatifi ne", "Trendyol mu Hepsiburada mı", "yurt dışından mı alsam", "bunu almaya değer mi", "en uygun ama kalitesiz olmasın" gibi bir şey dediğinde; bir ürün linki paylaşıp fiyatını/muadilini sorduğunda; ya da bir bütçe verip o bütçeyle en iyi ürünü istediğinde bu skill'i kullan. "Araştır" demese bile, bir satın alma kararı öncesi hangi ürün/hangi satıcı/hangi fiyat sorusu varsa devreye gir. Yatırımlık ürünler (altın, koleksiyon) ve hizmet satın alımları kapsam dışıdır.

- **Ölçü:** 8.265 bayt · 3 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `vize-giris-kurallari`

[SKILL.md](vize-giris-kurallari/SKILL.md)

Türkiye pasaportuyla (ve istenirse başka pasaportlarla) herhangi bir ülkeye giriş için vize rejimini, başvuru kanalını, güncel ücreti, randevu durumunu, evrak listesini, sınırda istenenleri, transit kurallarını ve seyahat sağlık/sigorta zorunluluklarını canlı araştırmayla çıkarır; başvuru için geriye dönük takvim ve red riskini azaltan dosya kurgusu üretir. Kullanıcı "vize gerekir mi", "vize nasıl alınır", "randevu yok", "hangi evraklar", "vize ücreti", "kapıda vize", "e-vize", "Schengen", "ABD vizesi", "transit vize", "pasaport süresi yeter mi", "sınırda ne soruyorlar", "aşı zorunlu mu", "seyahat sigortası", "reddedilirsem" dediğinde kullan. Bir seyahat planı konuşuluyorsa ("şu tarihte X ülkesindeyim") vize ve giriş ayağını kullanıcı sormasa bile gündeme getir. Vize kuralları haftalık değişir — ücret, süre, kanal ve zorunlulukları ASLA ezberden verme, her seferinde resmî kaynaktan doğrula ve tarih damgası koy.

- **Ölçü:** 6.705 bayt · 1 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

