# Akışlar — rol başına user story seti

Her hikâye tarayıcıda **gerçekten yürütülür**. Yürütmeden yazılan akış raporu
geçersizdir. Her adımda kaydet: dokunuş sayısı, ekranda eksik olan bilgi,
duraksama noktası, geri dönüş.

Ölçüm şablonu:

```
HİKÂYE   D1 — sabah ajandası
GÖRÜNÜM  mobil 390×844
ADIMLAR  giriş → /bugun → seans kartı → "gelmedi" → onay
DOKUNUŞ  5   (ideal 3)
KUSUR    "gelmedi" eylemi kartın altındaki üç nokta menüsünde; ilk bakışta
         görünmüyor, kullanıcı önce detay sayfasına giriyor (fazladan 2 dokunuş)
SONUÇ    tamamlandı / yarıda kaldı / yanlış sonuç
```

---

## Danışman (mobil öncelikli — telefon, tek el, koridorda)

**D1 — Sabah ajandası.** Girer, `/bugun`'ü açar, bugünkü seanslarını görür.
İlk ekranda görmesi gereken: kaç seans, ilki saat kaçta, hangi odada.
*Kusur ara:* seans sayısı yok, oda kısaltması yok, geçmiş ve gelecek seans
görsel olarak ayrılmamış, "şimdi" çizgisi yok.

**D2 — Gelmeyen danışan.** Bir seansı "gelmedi" olarak işaretler.
*Kusur ara:* eylem kaç dokunuş uzakta, yanlışlıkla basılması kolay mı, geri
alınabilir mi, işaretleme sonrası kart görsel olarak değişiyor mu.

**D3 — Haftaya bakış.** `/takvim`'e geçer, önümüzdeki haftayı görür.
*Kusur ara:* hafta gezinme dokunma hedefi, hangi günde olduğunu anlama,
mobilde hafta ızgarası okunabilir mi yoksa ajanda listesine mi düşmeli.

**D4 — Boş slot talebi.** Takvimde boş bir slot görür, randevu talebi açar.
*Kusur ara:* boş slot ile dolu slot ayırt ediliyor mu (yalnız renkle mi?),
talep formu alt sayfada mı, `Esc`/geri kapatıyor mu, gönderim sonrası
"talebiniz sekretere gitti" geri bildirimi var mı.

**D5 — Danışan geçmişi.** `/danisanlarim`'dan bir danışanı bulur, geçmiş
seanslarına bakar. *Kusur ara:* arama var mı, liste uzunsa sayfalama nerede,
danışan kartından geçmişe geçiş kaç dokunuş.

**D6 — Ayın hakedişi.** `/hakedisim`'i açar, bu ay ne kazandığını görür.
*Kusur ara:* dönem seçici görünür mü, tutarlar `tabular-nums` mı, komisyon
kesintisi anlaşılır mı, toplam ile kalemler tutarlı mı.

**D7 — Bildirim kurulumu.** `/bildirimler`'den push izni verir, takvim akışına
abone olur. *Kusur ara:* izin reddedilirse ne oluyor, kurtarma yolu var mı,
takvim bağlantısı kopyalanabilir mi (mobilde uzun URL seçmek işkencedir),
kopyalandı geri bildirimi var mı.

---

## Sekreter (masaüstü öncelikli — resepsiyon, klavye ağırlıklı, çok pencere)

**S1 — Oda doluluk taraması.** Girer, `/pano`'da bugünün oda ızgarasını görür.
*Kusur ara:* beş oda aynı anda ekrana sığıyor mu, saat sütunu kaydırırken
sabit mi, boş slot ile dolu slot 3:1 kontrastla ayrılıyor mu.

**S2 — Telefonla gelen randevu.** Bir danışan arar, sekreter hızlı giriş
(`HizliGiris`) ile randevu açar. *Kusur ara:* klavyeyle uçtan uca yapılabiliyor
mu, danışan arama (`DanisanArama`) yazarken sonuç veriyor mu, çakışma uyarısı
(`CakismaUyarisi`) ne zaman çıkıyor — kaydetmeden önce mi sonra mı.

**S3 — Çakışan randevu.** Dolu bir slota randevu yazmayı dener.
*Kusur ara:* uyarı anlaşılır Türkçe mi, hangi seansla çakıştığını söylüyor mu,
düzeltme yolu öneriyor mu, yoksa sadece "çakışma var" mı diyor.

**S4 — Günün tahsilatı.** `/tahsilat`'ta ödenmemiş seansları görür, birini
tahsil eder. *Kusur ara:* liste hangi ölçüte göre sıralı, toplam bakiye
görünüyor mu, ödeme sonrası satır listeden çıkıyor mu yoksa yenileme mi
gerekiyor, kısmi ödeme mümkün mü ve arayüzde belli mi.

**S5 — Yeni danışan kaydı.** `/danisanlar`'dan yeni kayıt açar.
*Kusur ara:* zorunlu alanlar işaretli mi, doğrulama hatası alanın yanında mı
yoksa formun tepesinde mi, telefon biçimi maskeli mi, çocuk/ergen seçilince
veli alanı zorunlu oluyor mu, yarıda bırakılan form uyarıyor mu.

**S6 — Talep kuyruğu.** `/talepler`'de danışman isteklerini görür, birini
onaylar birini reddeder. *Kusur ara:* onay/ret dokunma hedefi ve renk ayrımı,
ret gerekçesi isteniyor mu, işlem sonrası kart nereye gidiyor, kuyruk boşsa
boş durum ne diyor.

**S7 — Senkron kontrolü.** `/senkron`'da ayna durumuna bakar.
*Kusur ara:* senkron kapalıyken (`KARTELA_SYNC_ENABLED=false`) ekran "bozuk" mu
görünüyor yoksa "kapalı" olduğunu net söylüyor mu — bu ikisi çok farklı.
Kuyruk birikmişse endişe mi yaratıyor, açıklıyor mu.

---

## Yönetici (masaüstü + tablet — finans, karşılaştırma, dışa aktarma)

**Y1 — Ayın özeti.** Girer, `/kokpit`'te ciro, doluluk, tahsilat oranını görür.
*Kusur ara:* KPI kutuları (`KpiKutu`) karşılaştırma taşıyor mu (geçen aya göre),
sayılar bağlamsız mı, tablet yatayda kaç kutu yan yana sığıyor.

**Y2 — Bordro hazırlama.** `/hakedis`'te dönem seçer, psikolog bazında hakedişi
inceler. *Kusur ara:* tablo sütun sayısı tablette taşıyor mu, dönem seçici
(`DonemSecici`) durumu URL'de mi, satır toplamı ile genel toplam tutarlı mı,
dışa aktarma var mı.

**Y3 — Doluluk ısı haritası.** `/doluluk`'ta hangi oda hangi saatte boş görür.
*Kusur ara:* ısı ölçeği açıklanmış mı (lejant), renk körlüğünde okunuyor mu,
tek bir hücreden ayrıntıya inilebiliyor mu, mobilde ne oluyor.

**Y4 — Komisyon oranı değişikliği.** `/ayarlar` → oran sekmesinden bir psikoloğun
oranını değiştirir. *Kusur ara:* değişiklik geçmişe mi ileriye mi işliyor ve bu
ekranda yazıyor mu, kaydet öncesi etkisi gösteriliyor mu, yanlışlıkla değiştirmeye
karşı koruma var mı.

**Y5 — Yeni kullanıcı açma.** `/ayarlar` → kullanıcı sekmesinden danışman hesabı
açar, psikoloğa bağlar. *Kusur ara:* rol seçiminin ne anlama geldiği açıklanıyor
mu, psikolog bağlama zorunluluğu belli mi, parola kuralları önden yazıyor mu.

**Y6 — Denetim izi.** `/denetim`'de dün ne değişti bakar.
*Kusur ara:* filtre var mı (kullanıcı, tarih, koleksiyon), kayıt satırı ham JSON
mu yoksa insan diline çevrilmiş mi, sayfalama çalışıyor mu.

---

## Rol ötesi akışlar

**X1 — Yanlış rota.** Danışman `/kokpit`'e doğrudan gitmeyi dener.
`RolKapisi` ne yapıyor — boş ekran, yönlendirme, açıklayıcı mesaj? Doğrusu
sonuncusudur.

**X2 — Oturum bitişi.** `OturumAyaci` süresi dolduğunda form doldururken ne
oluyor? Yazılan veri kayboluyor mu? Uyarı önceden geliyor mu?

**X3 — Çevrimdışı.** Ağ kesilir. `sw.js` + `cevrimdisi.html` devreye giriyor mu,
yoksa tarayıcı hata sayfası mı? Bağlantı gelince kendiliğinden toparlıyor mu?

**X4 — Derin bağlantı ve yenileme.** Herhangi bir iç sayfada F5. Statik export +
`trailingSlash` altında 404 var mı? Filtre/sekme durumu korunuyor mu?

**X5 — Geri tuşu.** Alt sayfa (`AltSayfa`) veya yan ray (`YanRay`) açıkken tarayıcı
geri tuşu: paneli mi kapatıyor, sayfadan mı çıkıyor? Mobil kullanıcı ilkini bekler.

**X6 — Tema geçişi.** Koyu temada tüm ekranlar gezilir. Sert beyaz kart, okunmayan
rozet, kaybolan kenar var mı? İlk boyamada açık tema flash'ı çakıyor mu?

**X7 — İlk kurulum.** `KurulumIstemi` hangi koşulda çıkıyor, atlanabiliyor mu,
atlanınca geri getirilebiliyor mu?
