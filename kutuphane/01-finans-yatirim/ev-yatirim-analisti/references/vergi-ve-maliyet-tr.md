# Türkiye — maliyet ve vergi kalemleri

**Bu dosyadaki her oran, eşik ve tutar doğrulanmadan kullanılmaz.** Aşağıdaki rakamlar
2026 yılına ait olarak derlendi (derleme tarihi: Eylül 2026) ve yalnızca büyüklük hissi
vermek içindir. Analize koymadan önce GİB, ilgili belediye ve banka sayfalarından teyit et
ve rapora "kaynak + tarih" yaz.

## 1. Alım anındaki yan maliyetler

| Kalem | Tipik 2026 seviyesi | Not |
|---|---|---|
| Tapu harcı | Toplam %4 (alıcı %2 + satıcı %2) | Uygulamada tamamı alıcıya yıkılabilir — pazarlık konusu. Matrah beyan edilen satış bedelidir ve emlak vergi değerinin altında olamaz |
| Döner sermaye | Birkaç bin TL | Tapu müdürlüğü |
| Emlakçı komisyonu | %2 + KDV (taraf başına) | Pazarlığa açık |
| İpotek tesis harcı | Kredi tutarı üzerinden binde ~4,55 | Sadece kredili alımda |
| Ekspertiz/değerleme | Sabit ücret | Kredili alımda zorunlu |
| Kredi tahsis ücreti | Kredi tutarının belli oranı, üst sınırlı | Bankaya göre değişir |
| DASK + konut sigortası | Yıllık, m² ve bölgeye göre | Kredide konut + hayat sigortası istenebilir |
| Tadilat / mobilya / taşınma | Gerçekçi tut | Yatırımlıkta boya-badana + beyaz eşya asgari |

**Kural:** yan maliyetler tipik olarak fiyatın %8–12'sidir ve getiri paydasına eklenir.

> Uyarı — düşük beyan: tapuda gerçek bedelin altında beyan, harç kaybı cezası yanında
> satışta değer artış kazancını şişirir. Analizde gerçek bedeli kullan, kullanıcıyı riske
> karşı uyar, düşük beyan planlamasına yardım etme.

## 2. Elde tutma maliyetleri (yıllık)

- **Emlak vergisi:** konutta binde 1 (büyükşehirde binde 2), arsa/arazi ve işyeri farklı.
  Matrah belediyenin belirlediği vergi değeridir; 4 yılda bir takdir komisyonu kararıyla
  sıçrar (2026'da matrahlar ciddi biçimde artırıldı, tavan kuralı uygulandı). Güncel
  değeri **belediyeden** sorgula.
- **Aidat:** ev sahibi payı (demirbaş, büyük onarım) kiracı payından ayrıdır.
- **DASK + konut poliçesi**, varsa **kira kaybı teminatı**.
- **Bakım-onarım rezervi:** yıllık kiranın %5–10'u. Eski binada üst banda yaklaş.
- **Boş kalma ve kiracı değişim maliyeti:** yıllık efektif %4–8.
- **Yönetim:** kendin yönetmiyorsan komisyon; kısa dönem kiralamada %15–25 + temizlik.

## 3. Kira geliri vergisi (GMSİ)

- Kira geliri **gayrimenkul sermaye iradı** olarak beyan edilir (GVK m.70 vd.).
- **Mesken istisnası:** 2026 için 58.000 TL olarak açıklandı. İstisnanın kaldırılmasına
  dönük düzenleme tartışmaları da oldu — **her analizde o yıl için yürürlükte olanı
  doğrula.** İşyeri kirasında istisna yoktur, %20 stopaj mahsup edilir.
- İstisna, konut sayısına göre değil, toplam mesken kira gelirine **bir kez** uygulanır.
  Ticari/zirai/serbest meslek kazancı beyan edenler ve belirli gelir eşiğini aşanlar
  istisnadan yararlanamaz — kullanıcının başka gelirlerini sor.
- **Gider yöntemi seçimi analizin sonucunu ciddi değiştirir:**
  - *Götürü:* istisna sonrası kalanın %15'i. Basit; seçilirse 2 yıl geri dönülemez.
  - *Gerçek gider:* fiili giderler + **konut finansmanı kâr payı/faizi** + amortisman
    (iktisap bedelinin %2'si) + **iktisap bedelinin %5'i (ilk 5 yıl, konutta)**.
    Kredili ve yeni alınmış bir konutta gerçek gider çoğu zaman matrahı sıfırlar.
    Motor bunu yaklaşık hesaplar; nihai hesabı SMMM'ye doğrulat.
- Beyan Mart ayında, iki taksitte (Mart/Temmuz). Damga vergisi da vardır.
- Kiranın **banka üzerinden** tahsili zorunluluğu ve belge düzeni ihlalinde ceza vardır.

## 4. Satıştaki vergi

- **Değer artış kazancı:** iktisapten itibaren **5 yıl** içinde satışta doğar; 5 yıl
  sonrası satış gelir vergisine tabi değildir (miras/bağış hariç kurallar farklıdır).
- Kazanç hesabında maliyet bedeli, satıştan önceki aya kadar **ÜFE artışıyla endekslenir**
  (endeksleme için artış oranının %10 veya üzeri olması şartı aranır) — yüksek enflasyonda
  bu endeksleme vergiyi büyük ölçüde eritir. Motor bunu enflasyon varsayımıyla yaklaşık
  uygular.
- Yıllık istisna tutarı ve tarife dilimleri her yıl değişir — doğrula.
- Bir takvim yılında birden fazla satış / süreklilik arz eden alım-satım **ticari kazanç**
  sayılabilir; bu, KDV ve mükellefiyet doğurur. Al-sat planı varsa mutlaka uyar ve
  `sahis-vergi-yukumluluk` skill'ine devret.
- Satışta emlakçı komisyonu ve satıcı payı tapu harcı da çıkış maliyetidir.

## 5. Finansman

- Konut finansmanı **aylık** oranla ilan edilir. Eylül 2026 civarında bandın kabaca
  aylık %2,5–3,2 olduğu, katılım bankalarının kâr payı oranlarının kamu bankalarına yakın
  seyrettiği görüldü; yıllık maliyet oranı (tahsis ücreti ve sigortalar dahil) **%40
  civarına** çıkıyordu. Her analizde güncel oranı bankadan/karşılaştırma sitesinden al.
- Kredi tutarı, konut değerinin belirli bir oranıyla sınırlıdır (kredi/değer oranı; konut
  değerine ve niteliğine göre değişir) ve **ekspertiz değeri** üzerinden hesaplanır —
  anlaşılan fiyat değil.
- **Sübvansiyonlu kampanyalar** (ör. ilk konut kampanyaları) piyasa oranının çok altında
  olabilir; varsa uygunluk şartlarını (ilk konut, m², değer üst sınırı, oturma şartı,
  satış yasağı süresi) kontrol et, çünkü kaldıraç kararını tek başına tersine çevirir.
- Katılım bankalarında ürün "konut finansmanı"dır (murabaha); erken kapamada tazminat
  uygulaması ve gecikme yaklaşımı farklıdır. Ürünün helal niteliği hükmü bu skill'in
  konusu değil → `helal-yatirim-uzmani`.
- **Kaldıraç testi:** yıllık finansman maliyeti > brüt kira getirisi ise fark negatif
  taşımadır ve ancak nominal değer artışı ile kapanır. Motorun başabaş değer artışı çıktısı
  bu soruyu doğrudan cevaplar.

## 6. Kira sözleşmesi ve artış

- Konut kirasında yenileme dönemi artışı yasal bir üst sınıra tabidir (bir dönem %25 tavanı
  uygulandı, sonrasında TÜFE 12 aylık ortalama esasına dönüldü) — **güncel kuralı doğrula.**
- 5 yıl sonunda hâkim tarafından hakkaniyet/ rayiç uyarlaması istenebilir.
- Kiracı tahliyesi sınırlı gerekçelerle mümkündür; "istediğim zaman çıkarırım" varsayımı
  yanlıştır. Mevcut kiracılı mülkte hesabı **mevcut kirayla** kur, piyasa kirasına
  yakınsamayı ayrı senaryo yap.
- Kısa dönem (günlük/haftalık) kiralama izin, ruhsat ve kat malikleri onayı gerektirir;
  brüt getirisi yüksek ama işletme maliyeti, boşluk ve regülasyon riski yüksektir.
