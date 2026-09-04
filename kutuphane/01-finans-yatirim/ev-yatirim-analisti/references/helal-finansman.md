# Helal (faizsiz) konut finansman kaynakları — Türkiye

**Bu dosyadaki her oran, ücret, şart ve mevzuat atfı doğrulanmadan kullanılmaz.** Derleme
tarihi Eylül 2026; rakamlar büyüklük hissi içindir. Analize koymadan önce bankanın/şirketin
kendi sayfasından, BDDK ve TKBB kaynaklarından teyit et, rapora "kaynak + tarih" yaz.

**Fıkhî hüküm bu dosyanın işi değildir.** Burada kanalların *nasıl çalıştığı, neye mal
olduğu ve nerede tökezlediği* var. "Caiz mi" sorusu → `helal-yatirim-uzmani`.

---

## Kanal 1 — Katılım bankası konut finansmanı (murabaha)

Türkiye'de yaygın olan ana kanal. Banka konutu satıcıdan satın alır, üzerine kâr koyarak
vadeli olarak müşteriye satar. Faiz değil **kâr payı** denir; oran **aylık** ilan edilir.

**Sağlayıcılar:** Kuveyt Türk, Albaraka Türk, Türkiye Finans, Ziraat Katılım, Vakıf Katılım,
Emlak Katılım. (Güncel liste ve oranlar için TKBB üyeleri + bankaların kendi sayfaları.)

**Maliyet seviyesi (Eylül 2026 civarı gözlem):** aylık kâr payı bandı kabaca %2,6–3,4;
katılım tarafı kamu bankalarının faiz oranlarına yakın seyrediyordu. Tahsis ücreti,
ekspertiz, ipotek harcı ve sigortalarla birlikte **yıllık toplam maliyet %40 civarına**
çıkabiliyordu. Vade tipik olarak 120 aya kadar; tutar üst sınırları bankaya göre değişiyor.

**Süreç kuralları — burada hata yapılırsa işlem fıkhen zedelenir (TKBB Murabaha Standardı):**
- Banka malı **gerçekten satın almalı ve kabzetmeli**; iki satış sözleşmesi (satıcı→banka,
  banka→müşteri) ayrı ve bağımsız olmalı.
- **Satıcı ile alıcı arasında önceden yapılmış bir satış sözleşmesi bulunmamalı.** Kaparo
  verip satış vaadi/ön sözleşme imzaladıktan sonra bankaya gitmek işlemi bozar; gerekirse
  mevcut sözleşmenin usulünce ikale ile sonlandırılıp belgelenmesi gerekir.
  **Pratik kural: bankaya, satıcıyla akit kurmadan önce git.**
- Ödeme doğrudan satıcıya yapılmalı; alım vekâletinin müşteriye verilmesi istisnadır.
- Satıcı ile alıcı arasında akrabalık/ortaklık varsa muvazaa incelemesi gerekir.
- Sürece uyulmaması, gelirin "uygun olmayan gelir" sayılmasına yol açar.

**Kontrol listesi (müşteri tarafı):**
- Peşin fiyat, vadeli fiyat ve kâr payı açıkça beyan edilmiş mi (maliyet + kâr bilinmeli)?
- Gecikme halinde ne uygulanıyor (gecikme cezası/temerrüt bedeli ve akıbeti)?
- Erken kapamada ne oluyor — indirim, tazminat, hangi oran?
- Sigortalar: DASK zorunlu; hayat/konut poliçesi **tekafül (katılım sigortası)** olarak
  alınabiliyor mu, yoksa konvansiyonel mi dayatılıyor?
- Ekspertiz değeri, anlaşılan fiyattan düşük çıkarsa aradaki fark cepten kapatılır —
  senaryoyu buna göre kur.

**Ne zaman mantıklı:** aylık kâr payının yıllık karşılığı, beklenen konut fiyat artışının
altındaysa. Üstündeyse kaldıraç serveti eritir. `helal_finansman_kiyas.py` bu karşılaştırmayı
doğrudan yapar.

---

## Kanal 2 — Tasarruf finansman şirketleri ("evim sistemi")

6361 sayılı Kanun kapsamında **BDDK lisanslı** şirketler. Katılımcı bir tasarruf planına
girer, sözleşme başında bir defaya mahsus **organizasyon ücreti** öder, sırası/şartları
oluşunca konut tahsis edilir, kalan bedel taksitle ödenir. Faiz yoktur; gelir modeli
organizasyon ücretidir.

**Başlıca şirketler:** Eminevim, Birevim, Fuzul Ev, Katılımevim, Sinpaş, Emlak Katılım
(tasarruf finansman kolu). BDDK'nın güncel lisanslı şirket listesini mutlaka doğrula.

**Ekonomisi:**
- Organizasyon ücreti sektörde tipik olarak sözleşme tutarının **%5–14** bandında;
  **sözleşmeden cayılsa dahi genellikle iade edilmez.**
- Erken teslim için ödenmesi gereken tutar oranı BDDK kararlarıyla değişiyor (2026'da
  erken teslim eşiği yükseltildi, süreler uzadı) — **başvuru anındaki kuralı doğrula.**
- Yatırılan paralar **TMSF güvencesinde değildir.**

**Asıl risk — satın alma gücü erozyonu:** sözleşme tutarı nominal olarak sabitlenir, teslim
2–4 yıl sonraya sarkar. Konut fiyatı bu sürede sözleşme tutarını aşarsa aradaki farkı cepten
kapatmak zorunda kalırsın. Yüksek enflasyon ortamında bu, organizasyon ücretinden çok daha
büyük bir maliyettir. `helal_finansman_kiyas.py` bunu **satın alma gücü açığı** olarak
hesaplar; her tasarruf finansman senaryosunda bu satırı raporla.

**Kontrol listesi:** teslim tarihi sözleşmede **taahhüt** mü yoksa sıraya/kuraya mı bağlı;
teslim gecikirse yaptırım var mı; sözleşme tutarı güncelleniyor mu; cayma halinde iade
takvimi ve kesintiler ne; şirketin BDDK lisansı ve mali durumu.

---

## Kanal 3 — TOKİ / sosyal konut ve kooperatifler

Faizli kredi kullanılmadan, satıcı ile doğrudan taksitli satış/eser sözleşmesi ilişkisi.
2026'daki büyük sosyal konut programında model: **%10 peşinat, 240 aya kadar vade**,
taksitler Ocak ve Temmuz'da **memur maaş artış oranına göre güncelleniyor**; hak sahipliği
**kura** ile belirleniyor.

**Ekonomik cazibesi yüksektir** — piyasa muadilinin belirgin altında fiyat ve düşük taksit,
sübvansiyon anlamına gelir; `helal_finansman_kiyas.py` çıktısında genellikle en yüksek net
bugünkü değeri bu kanal verir. Ama:

**Tartışma başlıkları (hüküm için `helal-yatirim-uzmani` ve ehil bir âlime yönlendir):**
- Henüz yapılmamış konutun satımı (istisna/eser akdi çerçevesi ve şartları)
- Taksitlerin endeksle güncellenmesi → bir görüş bunu enflasyon kaybının telafisi sayıp faiz
  dışı kabul eder, diğer görüş bedelin baştan belirsizliğine (cehalet) itiraz eder
- Hak sahipliğinin kura ile belirlenmesi
- Teslimde ödenecek KDV'nin baştan belli olmaması
- Başvuru/ödeme sürecine konvansiyonel bankaların aracılık etmesi
- **Peşinatı veya kalan borcu faizli kredi ile kapatmak** — kanalı helal olmaktan çıkarır.

**Kooperatifler:** üyelik, aidat ve arsa/inşaat süreci; yönetim riski ve bitmeme riski
yüksektir. Kooperatifin tapu durumu, ruhsatı, mali tabloları ve geçmiş projeleri denetlenir.

---

## Kanal 4 — Karz-ı hasen (faizsiz borç) ve aile içi düzenlemeler

Aile/çevre kaynaklı faizsiz borç en ucuz kanaldır (maliyet sıfır). Riski finansal değil
ilişkiseldir. Modellemede: vade, geri ödeme takvimi ve enflasyonun borcu eritmesi.
Alacaklıyı enflasyona karşı korumak için yapılan **altın/döviz cinsinden borçlanma veya
endeksleme** ayrı bir fıkhî tartışmadır — hükmü `helal-yatirim-uzmani`'na bırak, ama
nakit akışı etkisini mutlaka hesapla (TL borç ≠ altın borç).

---

## Kanal 5 — Peşin alım / kademeli birikim

Çoğu zaman **en iyi kanal budur** ve atlanır. Karşılaştırmada dürüst kurgu: bugün peşin
alamıyorsan, biriktirirken paran helal alternatifte (katılım fonu, kira sertifikası, altın,
katılma hesabı) büyür ama konut fiyatı da büyür. Yarış hangi tarafın kazandığıyla ilgilidir.
`helal_finansman_kiyas.py` "nakit_bekle" kanalı bu yarışı ay ay simüle eder ve hedefe kaç
ayda ulaşıldığını (veya ulaşılamadığını) söyler.

Peşin alım aynı zamanda pazarlık gücüdür: nakit alıcı, kredi bekleyen alıcıya göre satıcıdan
belirgin iskonto koparabilir. Bunu senaryoya bir avantaj olarak koy.

---

## Kanal 6 — Mülkiyet yerine gayrimenkul getirisi

Kullanıcının amacı "gayrimenkul getirisi" ise, ev satın almak tek yol değildir: kira
sertifikası (sukuk), katılım esaslı gayrimenkul yatırım fonları ve katılım endeksinde yer
alan GYO'lar daha likit ve bölünebilir alternatiflerdir. Bunların uygunluk taraması ve
seçimi `helal-yatirim-uzmani`'nın işidir; buradaki rolü, ev alımının **fırsat maliyeti
referansı** olmasıdır.

---

## Kapsam dışı — üretilmeyen senaryolar

- **Faizli konut kredisi.** Hesap motoru `finansman.model` faizli olarak verildiğinde hata
  döndürür. Kullanıcı ısrar ederse: bu skill'in kapsamı dışında olduğunu tek cümleyle söyle,
  faizsiz kanalların karşılaştırmasını sun; gizli bir faizli senaryo üretme.
- Faizli kredi ile alınmış bir evi analiz etmek kapsam dışı değildir (mevcut durum tespiti
  ayrı şeydir); ama yeni faizli borçlanma planı kurmak kapsam dışıdır.

## Mülkün kendisinin uygunluğu

Finansman helal olsa da mülkün kullanımı sonucu değiştirir:
- **Kiracının faaliyeti:** işyeri olarak faizli banka şubesi, alkol/kumar/uygunsuz eğlence
  işletmesine kiralama, geliri sorunlu hale getirir. Yatırımlık işyerinde kiracı segmentini
  baştan sor.
- **Kısa dönem kiralamada** kullanım denetimi zayıftır; kullanıcı hassasiyetini sor.
- Konut kiralamada bu sorun genellikle doğmaz.
- Alternatif yatırım karşılaştırmasında kullanılan getiri de **helal enstrümandan** gelmeli;
  mevduat faizi veya konvansiyonel fon getirisi referans alınmaz.
