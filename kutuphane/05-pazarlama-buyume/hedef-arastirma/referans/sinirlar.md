# Sınırlar

Bu dosya iki ayrı konuyu tutuyor: yasal olarak neye izin var ve teknik olarak
mailin karşı tarafa ulaşması için neye uymak gerekiyor. İkisi de listeyi
etkiliyor, o yüzden tarama aşamasında biliniyor olmalı, gönderim gününde değil.

## Ticari elektronik ileti

Dayanak 6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun ve
İleti Yönetim Sistemi (İYS).

**Tacir ve esnafa önceden onay almak gerekmiyor.** B2B soğuk mailin yasal
olarak mümkün olmasının sebebi bu. Ama iki şartı var: adresin İYS'ye kayıtlı
olması ve ret hakkının işlemesi.

**Kişi adı taşıyan adres alıcıyı gerçek kişi yapıyor.** `bilgi@firma.com`
gibi genel bir adres tacirin adresi sayılıyor. `ad.soyad@firma.com` biçimindeki
adres o kişinin adresi sayılıyor ve onun için önceden onay gerekiyor. Buradan
çıkan kural net: **soğuk mail yalnızca genel adrese gider.** Kişi adı taşıyan
adres bulduysan `Adres tipi` alanına yaz ve o adrese yazma.

**Ret bildirimi en geç üç iş günü içinde uygulanır.** Biri "istemiyorum"
dediğinde kayıt kapatılır, `Ret durumu` işaretlenir ve bir daha hiçbir
taramada açılmaz.

**Gönderen taraf İYS'ye kayıtlı olmak zorunda.** Bu firmanın kendi
yükümlülüğü, kampanya başına değil. Kayıtların on yıl saklanması gerekiyor.

Cezalar caydırıcı büyüklükte. 2026 için onaysız gönderim kişi başına yaklaşık
14.300 lira, toplu gönderimde on katına kadar çıkıyor, ret yükümlülüğüne
uymamak yaklaşık 42.900 lira. Tekerrürde ikiye katlanıyor.

## KVKK

Firma verisi ile kişi verisi ayrı şeyler. Firmanın adı, adresi ve kurumsal
iletişim bilgisi kişisel veri değil. Karar vericinin adı, görevi ve iş adresi
kişisel veri.

**Veriyi kişiden almadıysan aydınlatma ilk iletişimde yapılır.** Kanunun
onuncu maddesi bunu istiyor. Pratikte şu demek: internetten bulduğun bir
adrese ilk kez yazıyorsan, o mailde bilgiyi nereden aldığını söylemen gerekiyor.
Mail şablonlarındaki çıkma cümlesinin yanına bir cümle daha lazım, adresin
firmanın kendi yayınından alındığını söyleyen bir cümle.

İYS ve KVKK ayrı kanunlar ve ayrı kurumlar denetliyor. Aynı gönderim ikisini
birden ihlal edebiliyor ve iki ayrı ceza gelebiliyor.

## Mailin ulaşması

Bunlar yasal değil teknik sınırlar ama listeyi doğrudan etkiliyor.

**Geri dönme oranı yüzde ikinin altında kalmalı.** Google, Yahoo ve Microsoft
bu eşiği uyguluyor. Kendi ilk çalışmamızda 31 mailin 2'si geri döndü, yani
yaklaşık yüzde altı buçuk. Eşiğin üç katı. Sebebi şablon değil, doğrulanmamış
adres. Bu yüzden `Doğrulama tarihi` alanı zorunlu ve doğrulanmamış adrese
gönderim yapılmıyor.

**Şikayet oranı binde birin altında tutulmalı.** Binde üçe ulaştığında
engelleme başlıyor. Şikayet oranı yükseliyorsa sorun liste seçiminde, metinde
değil.

**Kutu başına günde otuz ile elli mail.** Üstüne çıkınca kutuya düşme oranı
belirgin biçimde bozuluyor. Bu sayı aynı zamanda "her maili göndermeden önce
insan okur" kuralıyla da uyumlu, zaten günde elli maili elle okumak bir
sınırdır.

**Soğuk mail ana alan adından gönderilmez.** Ayrı bir alan adı kullanılır.
Tek bir kötü kampanya ana alan adının itibarını bozduğunda müşteri yazışmaları
ve fatura mailleri de kutuya düşmüyor.

**Yeni alan adı ısıtılmadan kullanılmaz.** Günde beş on mailden başlanıp dört
ile altı hafta arasında kademeli artırılıyor. Her adımda hacim bir buçuk
katından fazla artırılmıyor.

**SPF, DKIM ve DMARC üçü birden kurulmuş olmalı.** Bunlar olmadan itibar ve
etkileşim sinyalleri hiç değerlendirilmiyor.

## Gönderim öncesi kontrol listesi

Her gönderimden önce sırayla:

1. Firmaya bağlı bir People kaydı ve adresi var mı
2. Adres genel mi, kişi adı mı taşıyor
3. Ret kaydı var mı
4. Doğrulama tarihi bir aydan taze mi
5. Köşeli parantezli kişiselleştirme satırı doldurulabildi mi
6. Aydınlatma cümlesi ve listeden çıkma cümlesi mailde duruyor mu
7. Bugünkü gönderim sayısı elliyi aştı mı
8. Metinde uzun ya da kısa tire kaldı mı

Sonuncusu diğerleri kadar önemli, çünkü bu depodaki her metnin kuralı.
