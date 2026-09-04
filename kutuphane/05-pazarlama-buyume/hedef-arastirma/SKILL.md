---
name: hedef-arastirma
description: Danışmanlığı satabileceğimiz firmaları bulur, eler, puanlar ve Attio'ya yazar. "Kime satalım", "hedef listesi çıkar", "şu sektörde firma bul", "şu listeyi CRM'e yaz", "bunu elemeli miyiz" gibi işlerde kullan. Aynı akış müşteriye kurduğumuz düzenin kendisidir, yani burada yapılan iş satılan işin ta kendisi.
---

# Hedef araştırma

Bu depoda satılan şey şu: aradığın müşteri profilini bir kere yaz, internet o
profile göre taransın, uygun firmalar gerekçesiyle birlikte CRM'e düşsün. Bu
skill o düzenin bizim kendi satışımız için çalışan hali.

İki şeye birden hizmet ediyor. Birincisi, danışmanlığı kime satacağımızı
buluyoruz. İkincisi, müşteriye kuracağımız akışı önce kendimizde çalıştırmış
oluyoruz, yani sunumda anlattığımız yöntemin kendi kaydını üretiyoruz.

Uzun anlatımlar ayrı dosyalarda. Sırasıyla:

| Dosya | Ne zaman açılır |
|---|---|
| `referans/profil.md` | Kime satacağız, kimi eleyeceğiz |
| `referans/kaynaklar.md` | Firmayı nereden bulacağız, hangi kaynak gerçekten açılıyor |
| `referans/puanlama.md` | Uygunluk puanı, sert eleme, geri besleme |
| `referans/crm-alanlari.md` | Attio'da hangi alan tutulur, hangisi tutulmaz |
| `referans/sinirlar.md` | İYS, KVKK ve teslim edilebilirlik sınırları |

## Kalite neye bağlı

Bu işin kötü yapılan hali şudur: arama kutusuna sektör adı yazılır, çıkan ilk
otuz firma listeye eklenir, hepsine aynı mail gider. Sonuç sıfır cevaptır ve
sebebi mail metni sanılır. Sebep listedir.

Aşağıdaki yedi kural listeyi düzeltir. Hepsi zorunlu.

**Profil aramadan önce yazılır.** Önce arayıp sonra "bunlar da olur" demek en
sık yapılan hata. Profili sonradan yazarsan bulduğun her firmayı beğenirsin.
Profil yazılmadan tek bir arama yapılmaz.

**Kaynak taranmadan önce erişimi denenir.** Kaynakların bir kısmı dışarıya
kapalı. Bir dizini taramaya başlamadan önce tek sayfasını aç, gerçekten
okunuyor mu bak. Kapalıysa `referans/kaynaklar.md` içindeki tabloya yaz ve
başka kaynağa geç, tahminle doldurma.

**Her firma en az iki kaynaktan doğrulanır.** Dizinde yazan bilgi eskimiş
olabilir. Firmanın kendi sitesi ikinci kaynaktır ve çelişki varsa site kazanır.
Tek kaynaklı kayıt CRM'e "doğrulanmadı" işaretiyle girer.

**Kanıtsız alan boş kalır.** Çalışan sayısını bilmiyorsan boş bırak. Tahminî
rakam listeyi kirletmekle kalmıyor, sonra o rakama dayanıp yanlış firmayı
arıyorsun. Bu deponun genel kuralı zaten bu.

**Tek sinyalle mail yazılmaz, sinyal yığılır.** Bir firmanın satış temsilcisi
ilanı açması tek başına zayıf bir işaret. Aynı firmada iki üç işaret üst üste
geldiğinde (ilan artı fuar katılımı, ilan artı yeni şube) öncelik olur.
Puanlama bunu ödüllendirir.

**Sinyal tazeliği ölçülür.** Tetikleyicinin tarihi kayıt altına alınır. Bir
haftayı geçmiş tetikleyici mailin açılış cümlesini taşımaz, çünkü artık haber
değil. Tetikleyici tarihini `Tetikleyici tarihi` alanına yazmadan geçme.

**Elenenin sebebi kaydedilir.** Asıl kaliteyi bu getiriyor. Elediğin firmanın
sebebini yazmazsan bir sonraki taramada aynı firmaları tekrar bulursun.
Sebepler biriktikçe profil kendiliğinden düzeliyor.

## Akış

### 1. Profili yaz

`referans/profil.md` içinde danışmanlığın hazır profili var. Yeni bir kesime
gireceksen o dosyanın biçimini kullanarak yeni profil yaz. Profil beş katmandan
oluşur: firma özellikleri, bugün ne kullandığı, gözle görülür davranış işaretleri,
karar verme düzeni ve eleme sebepleri. Beşincisi olmadan profil yarım kalır.

Profilde her satırın karşılığı bir CRM alanı olmalı. Karşılığı olmayan ölçüt
ölçülemez, o yüzden ya alanı aç ya ölçütü at.

### 2. Kaynak seç ve erişimini dene

`referans/kaynaklar.md` içindeki tablodan işe uyanları seç. Tek kaynakla
yetinme, en az üç farklı türden kaynak kullan: bir dizin, bir davranış işareti
(iş ilanı, fuar, sicil ilanı) ve bir de firmanın kendi yayını.

Kaynağı taramaya başlamadan tek bir sayfasını aç. Açılmıyorsa tabloya yaz.

### 3. Tara ve ham listeyi çıkar

Ham listede sadece iki şey olsun: firma adı ve nereden bulunduğu. Bu aşamada
temizlik yapma, ne bulduysan yaz. Temizliği sonraki adımda topluca yapmak
hem hızlı hem tutarlı oluyor.

Doyma noktasını ölç. Yeni bir tarama turu, o kaynaktan gelen listeye onda
birinden az yeni firma ekliyorsa o kaynak bitmiştir. Aynı kaynağı zorlamak
yerine kanal değiştir.

### 4. Ele

`referans/puanlama.md` içindeki sert eleme listesini uygula. Sert eleme
puanlamadan **önce** çalışır, çünkü elenecek firmayı puanlamak boşa iş.

Elenen her firma için sebep yaz. Sebepler `Elenme sebebi` alanının seçeneklerinden
biri olmalı. Listede karşılığı yoksa yeni seçenek açılır, serbest metin yazılmaz.

### 5. Doğrula ve puanla

Kalan firmaların her biri için `referans/puanlama.md` içindeki dört bileşeni
doldur. Her bileşenin yanında kanıt satırı olacak. Kanıtı olmayan bileşen sıfır
alır, ortalama puan almaz.

Puanlama bitince listenin rastgele beş kaydını elle aç ve kontrol et. Beşte
birden fazla hata çıkarsa taramayı tekrarla, listeyi düzeltmeye çalışma.

### 6. CRM'e yaz

`referans/crm-alanlari.md` içindeki alan düzenine uy. Genel alanlar Companies
nesnesinde, işe özel alanlar listenin kendisinde durur. Firma tarifi ile
"neden uygun" gerekçesi ayrı alanlarda tutulur, aynı yere sıkıştırılmaz.

Her kayıtta kaynağı, kaynak bağlantısını ve doğrulama tarihini doldur. Bunlar
olmadan kayıt üç ay sonra çöp oluyor, çünkü bilginin nereden geldiği kayboluyor.

### 7. Tetikleyiciyi çıkar, sonra mail

Mail şablonlarındaki köşeli parantezli satır firmanın kendi yayınladığı bir
şeyden gelmek zorunda **ve teklifin cevap verdiği soruya bağlanmak zorunda.**
İkisi ayrı şart. Doğru olan her bilgi kişiselleştirme değil: firmanın stant
numarası doğrudur ama liste çıkarmakla ilgisi yoktur, o cümle karşı tarafta
"beni taramış" etkisi bırakır.

Sınama: gözlem cümlesini okuyup "e yani?" diye sorabiliyorsan o gözlem işe
yaramıyor. Gözlemden sonra gelen cümle, gözlemin neden yazıldığını göstermeli.

Bu satır doldurulamıyorsa firmaya mail atılmaz, kayıt `Beklemede` aşamasında
kalır. Sayı tutturmak için zayıf gözlemle mail göndermek, o firmayı bir daha
yazılamaz hale getiriyor. Kural `../../../CLAUDE.md` içinde de yazıyor.

Göndermeden önce `referans/sinirlar.md` içindeki kontrol listesini geç. Adres
tipi, ret kaydı, günlük gönderim sayısı ve aydınlatma cümlesi orada.

## Bunu yaparken yapılmayacaklar

Attio'ya toplu kayıt yazmadan önce kaç kayıt yazılacağını söyle ve onay al.
Yanlış profil ile yazılmış iki yüz kayıt, elle temizlemesi yarım gün süren bir
iş oluyor.

Mail gönderme. Taslak bırak. Bu kural deponun kendi kuralı ve burada da geçerli.

Attio'nun kendi zenginleştirme alanlarına (konum, sektör, çalışan aralığı)
doğrulamadan güvenme. Gerçek bir örnek: kayıtlı bir kliniğin adresi Bakırköy
iken zenginleştirme "Cumhuriyet Meydanı" yazmış. Karar bu alanlara dayandırılmaz.
