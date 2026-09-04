# Attio'da ne tutuyoruz

Kayıt tutmanın amacı arşiv değil. Üç soruya cevap verebilmek için tutuyoruz:
bu firmayı neden seçtik, bu bilgiyi nereden aldık, sırada ne var. Bu üçüne
cevap vermeyen alan yer kaplamaktan başka bir şey yapmıyor.

Çalışma alanındaki listeler Companies nesnesine bağlı. Danışmanlığın kendi
satışı `Danışmanlık Hedefleri` listesinde yürüyor, alan düzeni bu dosyada
anlatılan düzenin birebir kurulmuş hali.

## Üç katman

**Companies nesnesi** her işte aynı kalan bilgiyi tutar. Firma adı, alan adı,
tarif, konum, çalışan aralığı. Aynı firma iki ayrı işte karşına çıkarsa
buradaki bilgi ikisinde de geçerli olur.

**Liste alanları** o işe özel olanı tutar. Klinik listesindeki `Terapist sayısı`
başka hiçbir işte anlam taşımıyor, o yüzden liste üzerinde duruyor. Bu ayrımı
bozma, dikey alanları Companies nesnesine koyma. Koyarsan altı ay sonra elli
tane boş sütunla uğraşırsın.

**Notlar** gerekçeyi ve konuşma geçmişini tutar. Alan değil not olması lazım,
çünkü tarihi ve yazarı kendiliğinden geliyor.

## Her işte bulunması gereken alanlar

Yeni bir liste açarken aşağıdakiler mutlaka olsun. İlk yedisi şu an hiçbir
listede yok ve en çok eksikliği hissedilenler bunlar.

| Alan | Tip | Ne işe yarıyor |
|---|---|---|
| Kaynak | Seçim | Firmayı hangi kaynaktan bulduk. Hangi kaynağın işe yaradığını ancak böyle ölçebiliyoruz |
| Karar verici | Kişi bağlantısı | People kaydına bağlanır. Mail gönderiminin ön şartı, aşağıya bak |
| Kaynak bağlantısı | Metin | Kaydın çıktığı sayfanın adresi. Üç ay sonra "bunu nereden bulmuştuk" sorusuna cevap |
| Doğrulama tarihi | Tarih | Bilgi ne zaman kontrol edildi. Bir aydan eski kayıt karar için kullanılmaz |
| Neden uygun | Metin | Tek cümlelik gerekçe ve dayandığı kanıt. Sunumda satılan şeyin kendisi bu |
| Tetikleyici tarihi | Tarih | Tetikleyici ne zaman oldu. Tazeliği ölçmenin tek yolu |
| Adres tipi | Seçim (Genel / Kişi adı taşıyan / Yok) | Yasal olarak yazılabilir mi, `sinirlar.md` |
| Ret durumu | Onay kutusu | Biri "istemiyorum" dediyse işaretlenir ve bir daha yazılmaz |
| Tetikleyici | Metin | Zaten var. Mailin açılış cümlesini taşıyan gözlem |
| Uygunluk | Sayı | Zaten var. Yüz üzerinden puan |
| Aşama | Durum | Zaten var. Aday, Temas kuruldu, Nitelendi, Demo yapıldı, Pilot, Kazanıldı, Beklemede, Elendi |
| Elenme sebebi | Çoklu seçim | Zaten var. Geri beslemenin çalıştığı yer |
| Karar verici | Kişi bağlantısı | Var ama tipi yanlış, aşağıya bak |
| Sonraki adım ve tarihi | Metin ve tarih | Zaten var. Boş kalan kayıt ölü kayıttır |

## Mevcut şemada düzeltilmesi gerekenler

Bunlar `PDR Klinikler` listesinde bugün duran gerçek sorunlar. Yeni liste
açarken tekrarlama.

**`Karar Verici` alanı yanlış tipte.** Bugün actor-reference, yani çalışma
alanındaki kullanıcıları gösteriyor. Karşı taraftaki karar vericiyi değil,
bizim kendi kullanıcılarımızı seçtiriyor. People nesnesine bağlı bir kayıt
bağlantısı olması gerekiyordu.

**`Durum` alanının adı yaptığı işi anlatmıyordu.** İlk bakışta `Aşama` ile
çakışıyor sanılıyor ama içine bakınca öyle olmadığı görülüyor: 59 kaydın
55'inde uygunluk gerekçesi yazıyor, "tek şube, 15 bin takipçi, site yok,
hedef profilin merkezi" gibi. Yani alan zaten `Neden uygun` işini görüyordu,
yanlış adla. Silinmedi, adı düzeltildi.

Buradan çıkan kural: bir alanı kaldırmadan önce içine bak. Ada bakıp karar
verirsen elli beş kaydın gerekçesini silersin.

**`Sonraki Adım` ile `Sonraki Adım Tarihi` alanlarının anahtarları karışmış.**
Metin alanının anahtarı `sonraki_adim_6`, tarih alanınınki `sonraki_adim`.
Dışarıdan yazarken karıştırmaya çok müsait, kontrol ederek yaz.

**Gerekçe `Description` alanına sıkıştırılmış.** Bugün kayıtlı bir kliniğin
tarif alanında şube adresleri, oda sayısı, gelir modeli, çalışma saatleri ve
"sitedeki e-posta gizli" notu iç içe duruyor. Hepsi doğru bilgi ama tek bir
metin alanında durduğu için süzülemiyor, sayılamıyor ve raporlanamıyor.
Tarif alanı firmanın ne iş yaptığını anlatır, gerekçe `Neden uygun` alanına,
gözlemler kendi alanlarına gider.

**Zenginleştirme alanlarına güvenilmiş.** Aynı kayıtta konum alanı otomatik
dolmuş ve yanlış: klinik Bakırköy'de ama alan başka bir adres gösteriyor.
Sektör, çalışan aralığı ve konum alanları Attio tarafından tahmin ediliyor.
Doğrulanmadıkça puanlamada kullanılmaz.

## E-posta adresi kişide durur

Mail firmaya değil kişiye gidiyor, Attio da yazışmayı People kaydına işliyor.
Bu yüzden adres firmanın ya da listenin bir alanında değil, People kaydının
`Email addresses` alanında durur. O alan gerçek e-posta tipinde ve tekil, yani
aynı adres iki kez giremiyor. Liste üzerine metin tipinde e-posta alanı açmak
bu denetimi devre dışı bırakıyor, o yüzden açılmıyor.

Bağ iki yönlü ve hazır geliyor: People kaydındaki `Company` alanı firmayı,
firmadaki `Team` alanı kişileri gösteriyor. Ayrıca liste üzerindeki
`Karar verici` alanı o işte kime yazılacağını söylüyor.

**Kural: bağlı People kaydı ve adresi olmayan firmaya mail gönderilmez.**
Kayıt `Beklemede` aşamasında kalır. Adres bulunmuş ama kişi kaydı açılmamışsa
iş yarım demektir, çünkü gönderilen mailin nereye işleneceği belirsiz kalıyor.

Genel adresler için de kişi kaydı açılır. `bilgi@firma.com` bir kişi değil ama
Attio yazışmayı yine bir People kaydına bağlıyor. Kaydı firmanın adıyla açıp
`Adres tipi` alanına `Genel` yaz. Bu hem yazışmanın kaydını tutuyor hem de
ticari elektronik ileti kuralına uyuyor, çünkü soğuk mail zaten genel adrese
gidiyor.

Attio özel alanlarda e-posta tipini vermiyor, API bunu açıkça reddediyor.
Yani adres için doğru yer zaten tek: People kaydı.

## Yazılmayacaklar

Tahmin yazılmaz. Çalışan sayısını bilmiyorsan alan boş kalır. Bu deponun
genel kuralı ve CRM'de de geçerli.

Kişinin özel bilgisi tutulmaz. Karar vericinin adı, görevi ve kurumsal
iletişim adresi işin gereği. Bunun dışına çıkan hiçbir şey saklanmaz.

Kişisel cep telefonu toplanmaz. Firmanın yayınladığı kurumsal numara başka,
bir kişinin cebi başka.

Kaynağı olmayan puan yazılmaz. Puan bileşenlerinin her birinin kanıtı olacak,
yoksa o bileşen sıfır alır.

Silinen kayıt gerçekten silinir. Biri listeden çıkmak istediğinde kayıt
kapatılmakla kalmaz, ret bilgisi işaretlenir ve bir daha hiçbir taramada
yeniden açılmaz. Mail şablonlarındaki çıkma cümlesi gerçek bir taahhüt.

## Yeni liste açarken

Listeyi açmadan önce şu üçünü yaz: hangi profili arıyorsun, hangi dikey
alanlar gerekecek, hangi elenme sebepleri olacak. Üçü de yazılmadan liste
açılmaz. Sonradan alan eklemek kolay ama önceki kayıtlar boş kalıyor ve
liste hiçbir zaman tam olmuyor.

Toplu kayıt yazmadan önce kaç kayıt yazılacağını söyle ve onay al.
