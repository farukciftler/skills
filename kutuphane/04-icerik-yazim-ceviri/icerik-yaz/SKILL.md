---
name: icerik-yaz
description: Türkçe ve İngilizce uzun form içerik yazar. Metin elle yazılmış gibi okunur: yapay zeka imzası taşımaz, uzun çizgi kullanmaz, kalıp geçiş ifadelerine sığınmaz, somut sayı ve isim verir. SEO tarafı 2026 gerçeğine dayanır, folklora değil. "Yazı yaz", "blog yazısı", "makale", "içerik üret", "SEO içeriği", "uzun yazı", "İngilizcesini de yaz", "metni denetle", "bu metin yapay zeka gibi mi duruyor", "meta açıklama yaz" dendiğinde kullan. Yazıyı teslim etmeden önce scripts/denetle.py ile taramak bu becerinin parçasıdır.
---

# İçerik yazımı

Bu beceri tek bir şeyi hedefler: **okuyanın "bunu bir insan yazmış" dediği metin.** Bu bir
kılık değiştirme numarası değil. Yapay zeka metninin imzalarının neredeyse hepsi, aslında
söylenecek somut bir şey olmamasının belirtisidir. Sayı, isim, tarih ve ilk elden gözlem
eklendiğinde kalıp cümleler kendiliğinden buharlaşır.

Dört referans dosyası var, hepsi ölçülmüş bulgulara dayanıyor. Yazmaya başlamadan önce
işine yarayanı oku, ezberden yazma:

| Dosya | Ne zaman oku |
|---|---|
| [references/yapay-zeka-imzalari.md](references/yapay-zeka-imzalari.md) | Her yazıdan önce. Kaçınılacak kelime ve yapıların tam listesi. |
| [references/turkce-yazim.md](references/turkce-yazim.md) | Türkçe yazarken. TDK kuralları, okunabilirlik formülleri, Türkçe kalıp listesi. |
| [references/uzun-form.md](references/uzun-form.md) | 1500 kelimeden uzun yazılarda. Yapı, giriş, okuyucu tutma. |
| [references/seo-2026.md](references/seo-2026.md) | Arama görünürlüğü konuşulacaksa. Google'ın resmi söylemi ve ölçülmüş veriler. |

---

## Değişmez kurallar

Bunlar tartışmaya açık değil. Metin bunlardan birini ihlal ediyorsa yayına hazır değildir.

1. **Uzun çizgi ( — ) yok.** Türkçede TDK'ye göre uzun çizgi yalnızca konuşma çizgisidir,
   ara söz için kullanılmaz. İngilizcede ise em dash yapay zeka metninin en çok ölçülmüş
   imzasıdır: medRxiv ön baskılarında kullanım oranı 2022 öncesi %4,23 iken 2025'te %20,3'e
   çıkmış. Ara söz için virgül, nokta veya parantez kullan.
2. **Kalıp geçiş ifadesi yok.** "Bu bağlamda", "unutulmamalıdır ki", "günümüzde", "sonuç
   olarak", "moreover", "furthermore", "in conclusion". Cümleler mantıkla bağlanır.
3. **Metnin kendisi hakkında konuşma.** "Bu yazıda inceleyeceğiz", "hadi başlayalım",
   "let's dive in" yok. Yazı, konuya girerek başlar.
4. **Her 500 kelimede en az üç somut sayı, tarih veya özel isim.** Yoksa metin bir şey
   söylemiyor demektir.
5. **Cümle uzunluğu değişken.** En kısa cümle 5 kelimeden kısa, en uzunu 30 kelimeden uzun
   olsun. Standart sapma 8'in altındaysa metin düz okunur.
6. **Üçlü paralel liste en fazla bir kez.** "X, Y ve Z" kalıbı yapay zekanın ritmik imzası.
   İki ya da dört öğe de sayılabilir.
7. **"Sadece X değil, Y" kalıbı yok.** Türevleri de yok: "It's not just a tool, it's a
   philosophy", "X meselesi değil, Y meselesi".
8. **Bölümler özet cümlesiyle bitmez.** "Kısacası X önemlidir" okuyucuyu aptal yerine koyar.
9. **Kaynaksız otorite yok.** "Uzmanlara göre", "araştırmalar gösteriyor ki" yazılmaz.
   Hangi araştırma, kim, hangi yıl yazılır ya da cümle silinir.
10. **Belirsizlik saklanmaz.** Bilinmeyen bir şey varsa yazılır. "Bunu henüz çözemedik"
    cümlesi, uydurulmuş bir kesinlikten iyidir.

---

## Ses tonu

Yazan kişi konuyu bilen ama kendini uzman ilan etmeyen biridir. Anlatır, satmaz.

- Düz konuş. Süslü kelime, işi gören basit kelimeden iyi değildir.
- İtiraf et. Yanıldığın, bilmediğin, denemenin patladığı yeri yaz. Metni insan yapan budur.
- Okuyucuyu ikna etmeye çalışma, gerekçeyi göster, kararı ona bırak.
- Mizah kullanabilirsin ama zorlama.
- Ebeveyne yazıyorsan suçluluk duygusu üretme. Sayaç, aciliyet baskısı, "iyi anne şunu
  yapar" imaları yok. Çocuğa yönelik hiçbir karanlık desen kabul edilemez.

Bu proje için ek kural: fiyat, ölçü, sertifika durumu gibi gerçekler ana repodan gelir
(`farukciftler/masifico`). Buraya kopyalanırken nereden alındığı yazılır, burada
değiştirilmez. Detay için repo kökündeki `CLAUDE.md`.

---

## Akış

### 1. Ne yazılacağını netleştir

Önce şu üç soruyu cevapla, cevaplayamıyorsan yazma:

- Bu yazıyı okuyan kişi hangi soruyla geldi?
- Bu yazıda, internette zaten olmayan ne var? (İlk elden gözlem, gerçek sayı, başarısızlık
  anlatısı, bir yanlışın düzeltilmesi.)
- Okuduktan sonra ne yapabilecek?

Üçüncü soruya "konu hakkında bilgi sahibi olacak" cevabı geçersizdir.

Google'ın kendi ayrımı buradaki ölçüt: "7 Tips for First-Time Homebuyers" sıradan içerik,
"Why We Waived the Inspection and Saved Money: A Look Inside the Sewer Line" değil. Fark
bilgi miktarı değil, birinci elden olması.

### 2. Anahtar kelimeyi kök öbeği olarak belirle

Türkçe sondan eklemeli bir dil. "ahşap oyuncak", "ahşap oyuncaklar", "ahşap oyuncağı",
"ahşap oyuncakların" aynı kökten gelir ve Google bunları birbirine bağlar. Anahtar kelimeyi
metne tam eşleşme olarak sokmaya çalışmak Türkçede bozuk cümle üretir ve hiçbir işe yaramaz.

Yapılacak: kök öbeğini belirle, metinde her geçişte cümlenin gerektirdiği eki kullan.

İngilizce ve Türkçe için **ayrı** anahtar kelime araştırması yapılır ve **ayrı H2 seti**
kurulur. Ortak olan yalnızca konu ve arama niyetidir. İngilizce metin Türkçenin çevirisi
değildir, yeniden yazımıdır.

### 3. Yapıyı kur

Başlıkları önce yaz. Yalnız başlıkları okuyan biri metnin iskeletini görebilmeli.

- Başlıklar Türkçe soru sözdizimiyle kurulur: "Masif ahşap ile MDF nasıl ayırt edilir?"
  İngilizce sözdizimi çevrilmez.
- H2 sıklığı 300-500 kelimede bir.
- İçindekiler yalnızca 2000 kelimeden uzun ve gerçekten bölümlere ayrılan yazılarda.

Kelime sayısı hedefi koyma. Google'ın kendi öz değerlendirme listesinde şu satır var:
*"Are you writing to a particular word count because you've heard or read that Google has a
preferred word count? (No, we don't.)"* Konu ne kadar gerektiriyorsa o kadar yaz.

### 4. Girişi yaz, sonra baştan oku

Giriş konuyu tanımlayarak başlamaz. Bir olayla, bir sayıyla ya da bir çelişkiyle başlar.

Kötü: "Ahşap oyuncaklar son yıllarda giderek daha popüler hale gelmektedir."
İyi: "İlk prototipimiz elimde kırıldı. Damarı yanlış yönde kesmişiz."

Giriş 3-5 cümle. Sonra kendine sor: ilk cümle okuyucuyu ikinci cümleye çekiyor mu?

### 5. Kısa cevabı yaz

Yazının başına, sorunun doğrudan cevabını veren 40-60 kelimelik bir paragraf koy. Bu hem
okuyucuya hem arama sonuçlarına hizmet eder. Masifico temasında bunun için ayrı bir alan
var: yazı düzenleme ekranındaki "Kısa cevap" kutusu.

Kısa cevap tam cümlelerle yazılır, madde işareti kullanılmaz, soruyu ilk cümlede cevaplar.

### 6. Gövdeyi yaz

Her iddianın arkasına kanıt koy. Kanıt şu biçimlerden biridir: sayı, tarih, isim, doğrudan
alıntı, kaynaklı referans, ilk elden gözlem, karşı görüş.

Somutluk merdiveni: en altta nesneler, en üstte soyut fikirler. İyi yazı merdivenin iki
ucuna da gider. Yapay zeka metni sürekli ortada durur.

Madde işaretli liste yalnızca gerçekten liste olan şeyler için. Argümanı listeye dökme,
cümlelerle kur.

### 7. Bitir

Sonuç paragrafı özet değildir. Ya yeni bir şey söyler, ya bir yargı verir, ya da okuyucuya
somut bir adım bırakır. Yazılanı tekrarlıyorsa sil, metin bir önceki paragrafta bitsin.

### 8. Meta açıklamayı yaz

155 karakter. Yazının vaadini içerir, başlığı tekrarlamaz. Masifico temasında yazı düzenleme
ekranındaki "Meta açıklama" alanına girilir; boş bırakılırsa özet kullanılır.

### 9. Denetle

```bash
python3 .claude/skills/icerik-yaz/scripts/denetle.py yazi.md
```

İngilizce metin için `--dil en` ekle. Betik şunları sayar: uzun çizgi, yasak kelimeler,
kalıp ifadeler, geçiş ifadesi yoğunluğu, cümle uzunluğu dağılımı, Ateşman okunabilirlik
puanı, somut sayı yoğunluğu, üçlü liste sıklığı, "sadece X değil Y" kalıbı. Bulgular üç
seviyede gelir: DUR (yayına engel), BAK (gözden geçir), NOT (bilgi).

Betik alıntıları ayırt edemez. Kötü örnekleri tırnak içinde gösteren bir metinde (bu
dosyanın kendisi gibi) yanlış pozitif verir. Gerçek bir yazıda DUR satırı sıfır olmalı.

Sonra [assets/kontrol-listesi.md](assets/kontrol-listesi.md) dosyasındaki soruları geç.
Betik mekanik olanı tarar, o liste taranamayanı sorar.

En son adım atlanmaz: **metni sesli oku.** Nefesin tükendiği yere nokta koy, ağzına
oturmayan kelimeyi at.

### 10. İki dili birbirine bağla

Türkçe ve İngilizce sürümler Polylang ile eşleştirilir, `hreflang` etiketleri tema
tarafından otomatik basılır. Tek dilde yayımlanan yazı yarım kalmış sayılır.

---

## Türkçe için ek kurallar

Tam liste [references/turkce-yazim.md](references/turkce-yazim.md) içinde. Sık ihlal edilenler:

- **`-mektedir` / `-maktadır` sıfırlanır.** "Artmaktadır" değil "artıyor".
- **Edilgen çatı yalnızca fail bilinmiyorsa.** "Yapılmaktadır" yerine "yapıyoruz".
- **Soru eki ayrı yazılır:** "geldi mi", "var mı".
- **Bağlaç olan de/da ve ki ayrı yazılır.** "Ben de geldim", "duydum ki".
- **Kesme işareti özel adlara konur, kurum adlarına konmaz:** "Ahmet'in", ama "Türk Dil
  Kurumundan".
- **URL slug'ında Türkçe karakter yok, metinde her zaman var.**
- **Okunabilirlik hedefi:** Ateşman puanı 60-75 bandı. Türkçe web içeriğinin medyanı 48-55,
  yani "zor" seviyede. Bu bantta yazmak tek başına farklılaşmadır.
- Cümle ortalaması 12-18 kelime. Altı heceden uzun kelime paragraf başına en fazla bir.

---

## Sık yapılan hatalar

- **Anahtar kelimeyi cümleye zorla sokmak.** Türkçede bu her seferinde bozuk cümle üretir ve
  Google zaten kökü buluyor.
- **Kelime sayısı hedefine yazmak.** Şişirilmiş metin, kısa ve dolu metinden kötüdür.
- **Her yazıya SSS bölümü eklemek.** FAQ zengin sonucu 7 Mayıs 2026'da tamamen kapandı.
  Gerçekten sorulan sorular varsa yaz, şema için yazma.
- **Kaynak göstermekten kaçınmak.** Dış bağlantı vermenin zarar verdiği bir SEO folkloru
  var, kontrollü deney bunu çürütüyor. Kaynak göstermek hem doğru hem de üretken arama
  sistemlerinde alıntılanma oranını artırıyor.
- **Metni "edebi" hale getirmeye çalışmak.** Süslü dil yapay zeka imzasını güçlendirir,
  azaltmaz.
- **Yapay zeka tespit aracına göre düzeltme yapmak.** Bu araçlar anadili İngilizce olmayan
  yazarların metinlerini %61 oranında yanlışlıkla işaretliyor. Ölçüt araç değil, okuyucu.
- **Türkçeyi İngilizceden çevirmek.** İki dil ayrı yazılır. Çeviri kokusu, yapay zeka
  kokusundan daha belirgindir.
- **Ana repodaki bir gerçeği burada değiştirmek.** Fiyat, ölçü, sertifika durumu ana repodan
  gelir. İki yerde duran fiyat en sık hata kaynağıdır.

---

## Bu becerinin sınırları

Referans dosyalarındaki her iddianın yanında kaynağı ve kanıt seviyesi var. Bazıları
ölçülmüş bulgular, bazıları sektör folkloru, bazıları da açıkça doğrulanamamış. Ayrım
dosyalarda işaretli. Bir kural uygularken gerekçesini bilmiyorsan referansa bak.

SEO tarafı hızlı değişiyor. `references/seo-2026.md` Ağustos 2026 durumunu yansıtıyor.
Altı aydan eskiyse mevzuat ve arama özelliği iddialarını doğrulamadan kullanma.
