# Google Ads — Konut Projesi Kurgusu

## İçindekiler

1. Hesap mimarisi
2. Kampanya tipleri ve emlaktaki gerçek işlevleri
3. Arama kampanyası: anahtar kelime mimarisi
4. Negatif anahtar kelimeler — emlak için kritik liste
5. Reklam metni ve varlıklar
6. Teklif stratejisi ve öğrenme
7. Performance Max ve AI Max (2026 durumu)
8. Remarketing ve kitle katmanları
9. Coğrafi hedefleme
10. İlk 30 gün kurulum sırası
11. Sık yapılan pahalı hatalar

---

## 1. Hesap mimarisi

Emlakta hesabı **satış hareketine göre** böl, ürün özelliğine göre değil.
Moonstone karma kullanım olduğu için en az iki ayrı hat var ve bunlar farklı
alıcıya, farklı mesajla, farklı bütçeyle gider:

```
Moonstone Google Ads hesabı
├── Kampanya: Marka Savunması            [Arama, düşük bütçe, sürekli açık]
├── Kampanya: Rezidans — Yüksek Niyet    [Arama, dar terimler]
├── Kampanya: Rezidans — Keşif           [Arama, geniş terimler, ayrı bütçe]
├── Kampanya: Ticari Alan / Dükkân       [Arama, ayrı alıcı profili]
├── Kampanya: Remarketing                [Demand Gen veya Display, yalnız yeniden pazarlama]
└── Kampanya: PMax                       [yalnızca 100.000 TL+ kademesinde]
```

**Ayırma gerekçesi:** Bütçe kampanya düzeyinde yönetilir. "Tuzla satılık daire"
ile "Tuzla kiralık dükkân" aynı kampanyada olursa, hangisinin daha çok tık
aldığına Google karar verir — sen değil. Emlakta ticari alan sorgusu genelde
daha ucuz ve daha çok tıklanır, rezidans bütçesini yer.

Ad grubu kuralı: **ad grubu başına 10-15 sıkı ilişkili anahtar kelime.**
Daha geniş ad grupları alaka düzeyini düşürür, Kalite Puanını indirir, TBM'i
yükseltir.

---

## 2. Kampanya tipleri ve emlaktaki gerçek işlevleri

| Tip | Emlaktaki işlevi | Ne zaman aç |
|---|---|---|
| **Arama** | Var olan talebi hasat eder. Ana lead kaynağı | Her zaman ilk |
| **Marka araması** | Rakip ve portal, senin adına teklif verir. En ucuz ve en sıcak trafiği savunur | Site yayına girer girmez |
| **Remarketing (Demand Gen / Display)** | Emlak karar süreci haftalar sürer; hatırlatma dönüşümü ciddi yükseltir | 30 günde 1.000+ ziyaretçi biriktikten sonra |
| **Performance Max** | Kanalları tek kampanyada birleştirir, hacim getirir. Kontrolü düşük | Ölçüm sağlam + 30 gün / 30+ dönüşüm hacmi varsa |
| **Demand Gen** | YouTube, Discover, Gmail. Talep yaratma tarafı | Video varlıkları hazırsa, orta-üst bütçede |
| **YouTube** | Proje lansmanı, hatırlanma | Güçlü video varsa ve bütçe 100.000 TL üstüyse |
| **Display (soğuk)** | **Açma.** Emlakta soğuk display bütçe yakar | — |

---

## 3. Arama kampanyası: anahtar kelime mimarisi

Emlak sorgularını niyet derinliğine göre üç katmana ayır. Her katman **ayrı
ad grubu**, mümkünse ayrı kampanya — çünkü dönüşüm oranları 5-10 kat farklıdır
ve aynı teklif stratejisi altında ucuz-kalabalık katman pahalı-değerli katmanı
boğar.

**Katman 1 — Proje/marka niyeti (en değerli, en ucuz)**
`moonstone residence`, `moonstone tuzla`, `ayhanlar inşaat` · Tam eşleme.
Bu terimler için gösterim payı hedefi %90+ olmalı.

**Katman 2 — Konum + tip niyeti (asıl lead kaynağı)**
`tuzla satılık daire`, `tuzla 3+1 satılık`, `aydıntepe satılık daire`,
`tuzla yeni proje daire`, `tuzla rezidans satılık`, `tuzla sıfır daire`
Sıralı eşleme (phrase) ağırlıklı. Geniş eşleme yalnızca dönüşüm verisi
oturduktan ve akıllı teklif çalıştıktan sonra, negatif listesi sıkıyken.

**Katman 3 — Keşif / araştırma niyeti (ucuz tık, düşük dönüşüm)**
`tuzla oturulacak yerler`, `tuzla yatırımlık daire mi`, `2+1 mi 3+1 mi`
Bu katman lead değil, remarketing havuzu ve SEO içeriği besler. Ayrı ve
küçük bütçeyle, ayrı hedefle çalıştır — yoksa CPL ortalamasını bozar.

**Ticari alan tarafı** ayrı bir dil konuşur: `tuzla satılık dükkân`,
`tuzla işyeri satılık`, `aydıntepe kiralık dükkân`. Alıcı profili yatırımcı;
mesaj metrekare ve cadde trafiği üzerine kurulur, "yaşam" üzerine değil.

---

## 4. Negatif anahtar kelimeler — emlak için kritik liste

Emlakta negatif listesi, anahtar kelime listesinden daha çok para kurtarır.
Kampanya açılırken bu liste hesap düzeyinde hazır olmalı, sonradan değil.

**Kiralama niyeti** (satış kampanyasında): `kiralık`, `kira`, `günlük kiralık`,
`aylık kiralık`, `öğrenci`, `eşyalı kiralık`

**Ödeme gücü uyumsuzluğu:** `ucuz`, `en ucuz`, `bedava`, `ücretsiz`,
`hacizli`, `icradan`, `bankadan satılık`, `kelepir`, `takas`, `arsa payı`

**Meslek / kariyer niyeti:** `emlakçı`, `emlak danışmanı`, `iş ilanı`,
`eleman`, `komisyon oranı`, `emlak yetki belgesi`

**Bilgi niyeti (satın alma değil):** `nedir`, `nasıl`, `hesaplama`,
`tapu harcı`, `emlak vergisi`, `kredi hesaplama`, `değerleme`, `ekspertiz`

**Alakasız coğrafya:** Tuzla dışındaki ilçe adları + **"Tuzla" adının başka
şehirlerde de olduğunu unutma** (Adana Tuzla vb.) — coğrafi hedefleme bunu
tam çözmez, negatif ekle.

**Rakip proje adları:** Rakip markaya teklif vermek pahalı ve düşük
dönüşümlüdür; ayrı ve bilinçli bir karar olmadan negatif listede kalsın.
Rakip listesi için `moonstone-residence/references/rakip-analizi.md`.

Arama terimleri raporunu **ilk iki hafta her gün, sonra haftada bir** oku.
Otomatik teklif ve geniş eşleme çağında negatif listesi bakımı, hesabın
en yüksek getirili tekrar eden işidir.

---

## 5. Reklam metni ve varlıklar

Duyarlı arama reklamında (RSA) 15 başlık + 4 açıklama alanı var. Boş bırakma;
Google kombinasyonları kendi test eder.

**Başlık dağılımı [MUHAKEME — alaka, ayırt edicilik ve eylem dengesi]:**
- 4-5 başlık: sorgu eşleşmesi (`Tuzla Satılık Daire`, `Tuzla'da Sıfır Daire`)
- 4-5 başlık: ayırt edici özellik (`Karma Kullanımlı Rezidans`,
  `Aydıntepe'de Yeni Yaşam Alanı`)
- 3-4 başlık: marka (`Moonstone Residence`, `Ayhanlar Yapı Güvencesi`)
- 2-3 başlık: eylem (`Kat Planlarını İnceleyin`, `Randevu Oluşturun`)

**Marka sesi bağlayıcı.** "Kaçırmayın", "son fırsat", "muhteşem" gibi
ifadeler CTR'yi yükseltse bile kullanılmaz — `moonstone-residence/references/ton-ve-dil.md`.

**Fiyat, teslim tarihi, "%X değer artışı" gibi doğrulanmamış veri metne
girmez.** Fiyat girilecekse mevzuat devreye girer:
`references/mevzuat-ve-politika.md`.

**Varlıklar (uzantılar) — hepsini kur, ücretsiz alan kazandırır:**
- Site bağlantıları: Kat Planları · Sosyal Alanlar · Konum · Randevu
- Açıklama metinleri: kısa özellik listesi
- Yapılandırılmış snippet'ler ("Olanaklar" başlığı altında sosyal alanlar)
- Arama uzantısı: satış ofisi telefonu, **çalışma saatleriyle sınırlı**
  (cevapsız çağrı, kaybedilmiş lead'dir)
- Konum uzantısı: Google Business profili bağlıysa. `[DOĞRULA: GBP var mı]`
- Lead formu uzantısı: site hazır olana kadar geçici köprü olabilir

---

## 6. Teklif stratejisi ve öğrenme

Sıralama, hesabın olgunluğuna göre:

| Aşama | Strateji | Geçiş koşulu |
|---|---|---|
| 0-2 hafta, dönüşüm verisi yok | Tıklamaları Maksimize Et (TBM üst sınırıyla) | İlk dönüşümler gelene kadar |
| Dönüşüm gelmeye başladı | Dönüşümleri Maksimize Et | 30 günde ~30 dönüşüme yaklaşınca |
| Hacim oturdu | Hedef EBM (tCPA) | Hedef, gerçekleşen EBM'in %10-15 üstünden başlar |
| Nitelikli lead ölçülüyor | tCPA, ama **nitelikli lead dönüşümü** üzerine | Offline aktarım çalışıyorsa |

**Öğrenme kuralları:**
- tCPA için yaygın eşik: **30 günde ~30 dönüşüm** (kampanya düzeyinde).
  Bunun altındaysan tCPA'ya geçme; oynaklık seni yanlış kararlara iter.
- Teklif stratejisi durumu **üç haftaya kadar "öğreniyor"** kalabilir ve
  **her hedef değişikliği bu sayacı sıfırlar.** Hedefi haftada birden fazla
  oynatma; değiştireceksen tek seferde %15'ten fazla oynatma.
- Bu yüzden küçük bütçede kampanya sayısını azaltmak, dönüşümü tek havuzda
  toplamak için de gerekli.

---

## 7. Performance Max ve AI Max (2026 durumu)

**PMax'ta 2026 itibarıyla gelen kontroller** — bunlar PMax'ı emlak için
kullanılabilir hale getirdi, eskisi gibi kara kutu değil:
- **Negatif anahtar kelime desteği** (eskiden yoktu — emlakta hayati)
- **Kanal düzeyinde raporlama** (hesap düzeyinde): hangi kanal ne getiriyor
- **Arama temaları 50'ye çıktı** (eskiden 25)
- Marka kontrolleri ve genişletilmiş raporlama

**AI Max for Search:** beta bitti; Dinamik Arama Reklamları (DSA) Eylül'den
itibaren otomatik olarak AI Max'e yükseltiliyor. AI Max anahtar kelimesiz
niyet eşleştirmesi yapıyor, başlıkları gerçek zamanlı üretiyor ve nihai URL'i
sorguya göre genişletiyor.

**Emlak için pratik sonuç ve uyarı:**
Google'ın tamamı otomasyona kayıyor; kontrol anahtar kelimeden **negatif
listesi, dönüşüm sinyali kalitesi ve varlık kalitesine** geçti. Bu iyi haber
değil, sorumluluk kayması: **platform sana ne beslersen ona optimize eder.**
Ham lead'i dönüşüm olarak beslersen, PMax sana ham lead üretmekte
uzmanlaşır — çöp lead dahil. Bu yüzden bu dosyadaki tek katı kural:

> **Ölçüm ve nitelikli-lead sinyali kurulmadan PMax veya AI Max açma.**

AI Max'in URL genişletmesi, site yayına girdiğinde kontrol edilmeli:
istenmeyen sayfalara (blog, KVKK metni) trafik gönderebilir — URL kurallarıyla
sınırla.

---

## 8. Remarketing ve kitle katmanları

Emlakta karar süreci uzun; remarketing burada lüks değil, temel.

**Havuz kurgusu (öncelik sırasıyla):**
1. Kat planı sayfasını görüntüleyip form doldurmayanlar — en değerli havuz
2. Formu açıp göndermeyenler (terk edilmiş form)
3. 60 saniyeden uzun kalan tüm ziyaretçiler
4. Sanal turu izleyenler / video izleyenler
5. Mevcut lead listesi (Müşteri Eşleştirme) — **KVKK açık rızası şart**

**Kitle katmanları (observation modunda):** Pazar içi (in-market) "Gayrimenkul",
"Konut Kredisi" segmentleri arama kampanyalarına gözlem olarak eklenir —
başta teklif değiştirmez, veri toplar. 30 gün sonra performansa göre teklif
ayarlaması yapılır. Bunu başından "hedefleme" moduna almak, erişimi gereksiz
daraltır.

**Sıklık kontrolü:** Remarketing'de aynı kişiye günde 3'ten fazla gösterim
markayı yorar. Prestij segmentinde bıktırma, tasarruftan pahalıdır.

---

## 9. Coğrafi hedefleme

- **Ana halka:** Tuzla ve komşu ilçeler (Pendik, Kartal, Gebze hattı) — en
  yüksek teklif.
- **İkinci halka:** İstanbul Anadolu Yakası geneli — orta teklif.
- **Üçüncü halka:** İstanbul geneli + yakın iller — düşük teklif, yalnızca
  yatırımcı mesajıyla.
- **Yabancı hedefleme:** Yalnızca böyle bir karar varsa. Yabancıya satış
  toplam pazarın %1,7'si (`references/birim-ekonomi.md`) — otomatik yapılacak bir iş
  değil, ayrı bir strateji kararı. `[DOĞRULA: yabancı yatırımcı hedefi]`

**Konum ayarı kritik:** "Bulunduğu veya ilgilendiği konumlar" varsayılanı,
Tuzla'yı aratmayan ama Tuzla'da yaşayan herkese reklamı açar. Emlakta
genelde doğru olan **"İlgi duyulan konum"** — Ankara'dan Tuzla'ya yatırım
arayan kişi değerli bir lead'dir, İstanbul dışını komple kapatma.

---

## 10. İlk 30 gün kurulum sırası

| Gün | İş |
|---|---|
| 0 | Hesap Moonstone mülkiyetinde açılır (ajans hesabı değil), faturalandırma kurulur |
| 0 | GA4 + GTM + dönüşüm izleme + Consent Mode → `references/olcum-ve-crm.md` |
| 1 | Dönüşüm eylemleri tanımlanır: form, WhatsApp, telefon, katalog indirme — **değerleri farklı** |
| 2 | Negatif anahtar kelime listesi hesap düzeyinde yüklenir |
| 3 | Marka savunması kampanyası açılır (düşük bütçe, sürekli) |
| 5 | Yüksek niyet arama kampanyası açılır, Tıklamaları Maksimize Et |
| 7-14 | Arama terimleri raporu **günlük** okunur, negatif listesi büyür |
| 14 | İlk dönüşümler varsa Dönüşümleri Maksimize Et'e geçiş |
| 21 | Remarketing havuzu doluysa remarketing kampanyası |
| 30 | İlk gerçek CPL ölçümü. `references/birim-ekonomi.md` tablosu artık devre dışı, kendi verimiz devrede |

---

## 11. Sık yapılan pahalı hatalar

1. **Tüm anahtar kelimeleri tek kampanyada toplamak.** Ucuz-kalabalık terimler
   bütçeyi yer, pahalı-değerli terimler gösterim payı kaybeder.
2. **Negatif listesi olmadan geniş eşleme.** 2026'nın otomasyon ağırlıklı
   Google'ında bu, bütçeyi rastgele dağıtmakla eşdeğer.
3. **Ham lead'i tek dönüşüm sinyali yapmak.** Platform ne beslersen onu
   çoğaltır. Nitelikli lead sinyali gitmiyorsa akıllı teklif körlemesine çalışır.
4. **Ana sayfaya trafik göndermek.** "Tuzla 3+1 satılık" arayan kişi 3+1
   sayfasına düşmeli. Yanlış sayfa, dönüşüm oranını yarıya indirir.
5. **Teklif hedefini haftada birkaç kez oynatmak.** Her değişiklik öğrenmeyi
   sıfırlar; kampanya hiç olgunlaşamaz.
6. **Telefon uzantısını 7/24 açık bırakmak.** Cevapsız çağrı, parayla satın
   alınmış ve çöpe atılmış lead'dir.
7. **Marka aramasını "zaten bizi buluyorlar" diye kapatmak.** Rakip ve portal
   o boşluğu doldurur; en sıcak trafiği rakibe hediye edersin.
