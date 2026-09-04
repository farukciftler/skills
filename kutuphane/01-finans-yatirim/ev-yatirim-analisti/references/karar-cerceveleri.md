# Karar çerçeveleri ve yorumlama

## 1. Kira çarpanı / amortisman süresini doğru okumak

- **Brüt çarpan** = alım fiyatı ÷ yıllık brüt kira. Piyasada konuşulan "amortisman süresi"
  budur ve iyimserdir.
- **Net çarpan** = toplam giriş maliyeti ÷ vergi ve giderler sonrası yıllık net gelir.
  Gerçek geri dönüş budur ve brütün tipik olarak **1,5–3 yıl** üstündedir. Yatırım kararı
  net çarpanla verilir.
- Kaynak farkı önemlidir: ilan bazlı endeksler (Endeksa/Emlakjet) ile değerleme bazlı
  seriler (TCMB konut birim fiyatı/kira) aynı dönem için belirgin biçimde farklı süre
  verebilir — 2026'da ilan bazlı ~13–14 yıl, değerleme bazlı ~16–17 yıl seviyeleri
  raporlandı. İkisini de göster, tek bir rakama tapınma.
- Çarpan **statik** bir ölçüdür: kira ve fiyat artış hızını, vergiyi, kaldıracı içermez.
  Ön eleme için kullan, karar için IRR'a bak.

**Ön eleme kabası (Türkiye, canlı veriyle güncelle):**

| Brüt çarpan | Yorum |
|---|---|
| < 12 yıl | Kira tarafı güçlü; neden ucuz olduğunu ara (yapı, tapu, semt, kiracı) |
| 12–16 yıl | Piyasa bandı; karar diğer değişkenlerde |
| 16–20 yıl | Fiyat kira tarafından desteklenmiyor; tez tamamen değer artışına dayanıyor |
| > 20 yıl | Yatırım değil, spekülasyon veya prestij alımı |

## 2. Kaldıraç kararı (yalnızca faizsiz kanallar)

Üç sayıyı yan yana koy: **yıllık finansman maliyet oranı**, **brüt kira getirisi**,
**beklenen nominal değer artışı**. Kanal karşılaştırmasını `helal_finansman_kiyas.py` ile
yap; kanalların işleyişi `references/helal-finansman.md`'de.

- Finansman maliyeti > kira getirisi ise (Türkiye'de neredeyse her zaman) → negatif taşıma.
  Aylık açığı kim, hangi gelirden kapatacak? Kapatamıyorsa kaldıraç uygun değil.
- Kaldıracı savunan tek şey nominal değer artışının finansman maliyetini aşmasıdır. Motorun
  **başabaş değer artışı** çıktısı bunu doğrudan verir: gereken oran, geçmiş yıllardaki
  bölgesel artışın belirgin üstündeyse tez zayıftır.
- TOKİ/kooperatif gibi sübvansiyonlu kanal erişilebilirse hesabı ayrıca çalıştır; sonuç
  genellikle tersine döner (kura riski ve teslim süresi de senaryoya girer).
- Tasarruf finansmanında kaldıraç değil **gecikme** riski vardır: sözleşme tutarı sabit,
  konut fiyatı hareketli. Satın alma gücü açığını ayrı satır olarak göster.
- Kredi vadesinin uzaması taksiti düşürür ama toplam maliyeti ve faiz/kâr payı yükünü
  büyütür; erken kapama esnekliği (ve katılım tarafındaki tazminat uygulaması) not edilir.
- Kaldıraç riski simetrik değildir: fiyat düşerse özkaynak orantısız erir, borç aynı kalır.

## 3. Alternatif yatırım karşılaştırması

Karşılaştırma **aynı özkaynakla ve aynı vadede** yapılır. Motor, gayrimenkulün ürettiği
yıllık nakit akışlarını alternatif getiri oranında değerlendirip iki nihai serveti
karşılaştırır — kira gelirinin yeniden yatırılmasını göz ardı eden karşılaştırmalar
gayrimenkul lehine yanlıdır.

Karşılaştırmada dürüst ol:
- Gayrimenkulün **lehine**: enflasyona doğal endeksleme, kaldıraç imkânı, kullanım değeri,
  borcu enflasyonun eritmesi, uzun vadede vergi avantajı (5 yıl sonrası satış).
- Gayrimenkulün **aleyhine**: likidite yokluğu, yüksek işlem maliyeti, tek varlık riski,
  yönetim yükü, kiracı riski, deprem riski, ısrarcı bakım maliyeti.
- Alternatif **helal enstrüman** olmalıdır: katılım fonu, kira sertifikası (sukuk), altın,
  katılma hesabı. Mevduat faizi veya konvansiyonel fon getirisi referans alınmaz.
  Kullanıcı belirleyemiyorsa iki senaryo çalıştır (temkinli: enflasyon civarı; iyimser:
  son dönem katılım fonu/katılma hesabı getirisi).
- Sonucu **reel** olarak sun. Nominal %30 getiri, %25 enflasyonda %4 reeldir.

## 4. Oturum amaçlı alım: "al" vs "kirala + yatır"

Ayrı bir hesap kur:
- **Alırsan:** yan maliyetler + taksit + aidat + emlak vergisi + bakım − mülkün değer artışı
- **Kiralarsan:** kira ödemesi + kira artışı; buna karşılık peşinat ve taksit farkı alternatif
  yatırımda büyür.
- Karar değişkeni genellikle **elde tutma süresi**: işlem maliyeti (%8–12) kısa sürede
  amorti edilemez. 5 yıldan kısa oturum planında kiralamak çoğu zaman daha rasyoneldir.
- Parasal olmayan tarafı da yaz: taşınma zorunluluğundan kurtulma, tadilat özgürlüğü,
  çocuğun okul istikrarı. Bunları rakama çevirme ama görmezden de gelme.

## 5. "Satsam mı, tutsam mı"

Doğru soru "kâr ettim mi" değil: **bugün elimde nakit olsa bu evi bu fiyattan alır mıydım?**
- Bugünkü net satış geliri (masraf + vergi sonrası) hesapla.
- Bu tutar alternatif yatırımda ne yapar, kalan yıllarda evin toplam getirisi ne olur?
- Değer artış kazancı istisnası için 5 yıl dolmadıysa bekleme maliyetini hesapla.
- Batık maliyet ve "girdiğim fiyattan aşağı satmam" tuzağını açıkça adlandır.

## 6. Senaryo kurgusu (her raporda en az iki)

| Senaryo | Değer artışı | Kira artışı | Boşluk |
|---|---|---|---|
| Temkinli | Enflasyonun 5 puan altı | Yasal artış sınırı | %8 |
| Beklenen | Bölgesel uzun vade ortalaması | Enflasyona yakın | %4–5 |
| İyimser | Kullanıcının varsayımı | Piyasa kirasına yakınsama | %2 |

Nominal fiyat artışının uzun vadede enflasyonun çok üstünde kalacağı varsayımına dikkat et:
reel konut fiyatları dönemsel olarak uzun süre geriler. "Nominal artıyor" ile "reel
kazanıyorum" farkını her raporda açıkça ayır.

## 7. Karar cümlesi

Analizi şu kalıplardan biriyle bitir, gerekçesi tek satır:
- **AL** — reel IRR alternatifi belirgin geçiyor ve kırmızı çizgi yok.
- **PAZARLIK ET** — şu fiyatın altında mantıklı: (başabaş fiyatı hesapla ve yaz).
- **ALMA** — tez tamamen agresif değer artışı varsayımına dayanıyor / kırmızı çizgi var.
- **BEKLE** — kararı değiştirecek bilinmeyen var (iskân, ekspertiz, zemin, kiracı durumu).
- **KANALI DEĞİŞTİR** — mülk iyi ama seçilen finansman kanalı getiriyi yiyor; şu kanalla
  yeniden bak.

Kaçamak yapma; hangi bilginin kararı ters çevireceğini söyle.
