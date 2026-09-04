# Eleme ve puanlama

İki ayrı iş var ve sırası önemli. Önce sert eleme çalışır, sonra kalanlar
puanlanır. Elenecek firmayı puanlamak boşa iş, üstelik puan ortalamasını da
bozuyor.

## Sert eleme

Aşağıdakilerden biri doğruysa firma listeden çıkar, puanlanmaz. Sebebi
`Elenme sebebi` alanına yazılır.

| Durum | Neden |
|---|---|
| Son kullanıcıya satıyor | Yöntemin çıkardığı şey firma listesi, karşılığı yok |
| Tek kişilik işletme | Ölçeklenecek ekip yok |
| Satışı ihaleyle yapıyor | Sorun liste değil, ihale |
| Kendi satış geliştirme ekibi ve hazır veri aboneliği var | Sorunu çözmüş |
| Kamu kurumu | Satın alma düzeni başka |
| İki yıldan uzun süredir sitesi güncellenmemiş | Faal olup olmadığı belirsiz |
| Ret bildirimi var | Yasal olarak yazılamaz, `referans/sinirlar.md` |
| İletişim adresi hiç bulunamıyor | Ulaşılamayan kayıt liste kalabalığı |

Son madde önemsiz görünüyor ama değil. Kendi ilk çalışmamızda taranan 59
merkezin beşinde adres hiç bulunamadı. O beş kayıt listede durursa dönüşüm
oranını yanlış hesaplıyorsun.

## Uygunluk puanı

Puan yüz üzerinden ve dört parçadan geliyor. `Uygunluk` alanına toplam yazılır.
Her parçanın yanında bir kanıt satırı olmak zorunda. Kanıtı olmayan parça sıfır
alır, ortalama almaz. Bu kural puanın şişmesini engelleyen tek şey.

### Profil uyumu, 40 puan

Firmanın kendisi profile ne kadar uyuyor.

| Ne bakılıyor | Puan |
|---|---|
| Dışarı satış yaptığı görülüyor (satış ekibi, bayi ağı, ihracat) | 15 |
| Çalışan aralığı on ile iki yüz elli arasında | 10 |
| Hedef kitlesi firma, yani listesi çıkarılabilir bir kitle | 10 |
| Coğrafya ve dil uyuyor | 5 |

### Tetikleyici, 30 puan

Şimdi aranması için bir sebep var mı.

| Ne bakılıyor | Puan |
|---|---|
| Bir tetikleyici var ve bir haftadan taze | 15 |
| İkinci bir bağımsız tetikleyici var | 10 |
| Tetikleyici doğrudan satış kapasitesiyle ilgili (satış ilanı, fuar, yeni bölge) | 5 |

Tetikleyici bir haftadan eskiyse on beş puanın yarısı yazılır. Bir aydan
eskiyse sıfır, çünkü mailin açılış cümlesini artık taşıyamıyor.

Tek sinyal ile iki sinyal arasındaki fark burada bilerek büyük tutuldu. Tek
işaret gürültü sayılıyor, aynı firmada üst üste gelen iki işaret önceliğe
dönüşüyor.

### Ulaşılabilirlik, 20 puan

| Ne bakılıyor | Puan |
|---|---|
| Genel iletişim adresi var (bilgi, satis, iletisim gibi) | 10 |
| Karar vericinin adı ve görevi biliniyor | 7 |
| Telefon doğrulandı | 3 |

Kişi adı taşıyan adresler (ad.soyad biçiminde) buradan puan almaz, hatta
soğuk mail için kullanılmaz. Sebebi `referans/sinirlar.md` içinde.

### Kanıt kalitesi, 10 puan

| Ne bakılıyor | Puan |
|---|---|
| En az iki bağımsız kaynaktan doğrulandı | 6 |
| Doğrulama tarihi bir aydan taze | 4 |

## Eşikler

| Puan | Ne yapılır |
|---|---|
| 70 ve üzeri | Mail yazılır, `Aday` aşamasında CRM'e girer |
| 50 ile 69 arası | CRM'e girer ama beklemede kalır. Yeni bir tetikleyici gelirse yükselir |
| 50 altı | Yazılmaz. Sebebiyle birlikte elenir |

Eşikleri değiştirmek serbest, ama değiştirdiğinde eski kayıtları da yeniden
puanlaman gerekiyor. Yarısı eski eşikle yarısı yeni eşikle puanlanmış liste
hiçbir şey ölçmüyor.

## Geri besleme

Asıl kaliteyi getiren kısım burası. Ayda bir şu üç şeye bak.

**Elenme sebeplerinin dağılımı.** Bir sebep listenin dörtte birinden fazlasını
kaplıyorsa o sebep aslında bir arama ölçütü olmalı. Sonradan eleyeceğine baştan
arama. `referans/profil.md` içine taşı.

**Cevap veren kayıtların ortak yanı.** Cevap gelen firmaların puan bileşenlerine
bak. Hepsinde aynı bileşen yüksekse o bileşenin ağırlığı artmalı. Hiçbirinde
belirleyici değilse ağırlığı düşmeli.

**Puanı yüksek ama cevap vermeyenler.** Bunlar puanlamanın yanlış ölçtüğü yeri
gösteriyor. Beş tanesini elle aç ve neyi kaçırdığını bul. Puanlama tablosunu
buna göre düzelt, mail metnini değil.

Ölçüm için yeterli kayıt biriktirmeden değişiklik yapma. Yirmi kayda bakıp
karar vermek mail testinde de burada da en sık yapılan hata.
