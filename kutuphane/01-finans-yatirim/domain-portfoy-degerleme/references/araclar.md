# Araçlar, Kriterler ve Pazaryerleri

> Teyit: Ağustos 2026. Araçlar kapanır, fiyatlar değişir — her kullanımda doğrula.

## 1. Değerleme araçları — ne işe yarar, nerede yanılır

| Araç | Güçlü olduğu yer | Zayıf olduğu yer |
|---|---|---|
| **Estibot** | En eski sürekli çalışan otomatik sistem; tek kelimelik değerli .com'larda ve toplu portföy taramasında iyi | Çok kelimeli domainlerde zayıf; sonuçlar geniş sapabiliyor |
| **GoDaddy Appraisal** | Ücretsiz, hızlı, geniş veri; likit kısa .com'larda makul | Yeni gTLD'lerde ve niş dillerde geride kalıyor |
| **Afternic tahmini** | Canlı listeleme envanteri ve gerçekleşen satışlara dayandığı için "bugün ne eder" sorusuna en yakın ücretsiz cevap | Yalnızca aftermarket perspektifi |
| **Sedo appraisal** | İnsan destekli, Avrupa ccTLD'lerinde (.de, .co.uk, .fr) güçlü; belge gerektiren durumlarda kredibilite | Ücretli (temel paket ~29 EUR), 24-48 saat, hızlı kontrol için uygun değil |
| **Dynadot / Humbleworth / Atom / NameWorth** | Toplu portföy taraması, ikinci-üçüncü görüş | Tekil doğrulukta değişken |
| **NameBio** | **Değerleme aracı değil** — gerçekleşmiş satışların arşivi. Asıl kanıt kaynağı | Yalnızca kamuya açıklanan satışları içerir; özel satışlar görünmez |

Kullanım kuralı: **en az 3 araç + NameBio comps.** Uç değerler atılır, kalan aralık sunulur. Domain Name Wire gibi bağımsız kaynaklar bu araçları düzenli test eder; bir aracın güncel durumu şüpheliyse aranabilir.

## 2. Değeri belirleyen kriterler

**Yapısal**
- Uzunluk: kısa daha değerli; 3-4 harfli .com'lar en likit sınıflardan
- Telaffuz edilebilirlik: CVCV yapılar rastgele harf dizisinden belirgin değerli
- Tire ve rakam: değeri ciddi düşürür (özellikle tire)
- Hece sayısı: 1-3 hece ideal

**Anlamsal**
- Ticari niyet taşıyan anahtar kelime (bir sektörün parayı harcadığı terim)
- Marka olmaya uygunluk (brandable) vs tam eşleşen anahtar kelime (EMD)
- Dil pazarı: İngilizce > büyük yerel pazar dilleri > dar diller. Türkçe domainlerde alıcı havuzu dar ama doğru terimde yerel şirketler için değerli
- Trend: Google Trends ile terimin yönü

**Teknik / tarihsel**
- Yaş ve kesintisiz kayıt geçmişi
- Backlink profili ve gerçek trafik (varsa gerçek değer katar)
- Wayback geçmişi: spam/kumar/yetişkin içerik → ceza mirası riski
- TLD: .com temel referans; .net/.org belirgin düşük; ccTLD yerel pazarda güçlü; yeni gTLD'lerde comps seyrek ama .app/.ai gibi bazıları toparlıyor

**Risk**
- Ticari marka çakışması → varlık değil yükümlülük; UDRP ile kaybedilebilir
- Tanınmış marka türevleri (typo-squat) asla önerilmez

## 3. Fiyat mantığı

- **Vitrin (retail) fiyatı:** doğru alıcı geldiğinde istenen fiyat. Genelde araç tahminlerinin üst bandı.
- **Hızlı satış (liquidation) fiyatı:** 30 gün içinde satmak için gereken fiyat. Tipik olarak vitrin fiyatının küçük bir yüzdesi.
- **Yenileme maliyeti:** yıllık bedel × tutulacak yıl. Portföy kararının paydası budur.
- **Make offer vs BIN:** "Buy It Now" fiyatı satış olasılığını artırır (özellikle Fast Transfer ağında). Teklife açık bırakmak fiyatı yükseltebilir ama süreyi uzatır.

## 4. Pazaryerleri ve kanallar

- **Afternic (GoDaddy)** — en geniş dağıtım ağı; Dan.com Eylül 2024'te Afternic'e katıldı, ayrı marka olarak emekliye ayrıldı. Lander, LTO (taksitli/kiralık satış) ve Fast Transfer özellikleri buraya taşındı.
- **Sedo** — özellikle Avrupa pazarında güçlü; ayrıca ücretli değerleme hizmeti.
- **Atom (eski Squadhelp)** — brandable/isim odaklı; kurumsal isim arayanlara satışta iyi.
- **Doğrudan satış (outbound)** — en yüksek fiyat buradan çıkar ama emek ister. Kısa, kibar, tek soruluk temas; fiyat önce alıcıdan sorulmaz.
- **Escrow:** yüksek tutarlı doğrudan satışlarda escrow.com veya pazaryeri güvencesi zorunludur.

## 5. Registrar ve taşıma notları

- Squarespace domainleri farklı registrar'lar üzerinden kayıtlı olabilir: Squarespace Domains LLC / Squarespace Domains II LLC / Tucows ailesi / Key-Systems ailesi. **Kayıt registrar'ı, transfer akışını ve auth kodunun hangi e-postaya gideceğini belirler:** Squarespace Domains LLC kodu Owner Contact adresine, Tucows Admin Contact adresine gönderir. İkisi de güncel olmalı.
- Transfer adımları: kilidi kapat → auth/EPP kodu al → DNSSEC'i kaldır (bekleyen transferde açıp kapatılamaz) → yeni registrar'da transferi başlat → gelen onay e-postasındaki linke **hemen** tıkla (tıklanmazsa süreç 5 iş günü sonra başlar) → transfer 7 güne kadar sürebilir.
- Sahiplik değişikliği (registrant change) ICANN Inter-Registrar Transfer Policy'ye tabidir; hem eski hem yeni registrant onayı gerekir ve bu işlem bazı registrar'larda 60 günlük transfer kilidi tetikler.
- **Taşımadan önce tüm DNS kayıtlarını (A, CNAME, MX, TXT/SPF/DKIM) dışa aktar.** En sık yaşanan zarar, alan adının değil e-postanın kesilmesidir.
- Ücretsiz/pakete dahil gelen domain başka registrar'a taşındığında ücretsizlik devam etmez.
