---
name: startup-degerleme
description: >
  Bir startup hakkında sıfırdan derin araştırma yapıp (web, ticaret sicili, app store
  verileri, uygulama içi gezinti, app review'ları, sosyal medya, rakipler, ekip geçmişi)
  kanıta dayalı bir "tahmini net değer" aralığı, büyüme potansiyeli skoru, avantaj/dezavantaj
  listesi ve satın alma/satma tavsiyesi içeren rapor üretir. Kullanıcı bir startup/şirket/uygulama
  adı verip "araştır", "incele", "değeri ne kadar", "kaça satılır", "kaç para eder", "alınır mı",
  "bu girişim tutar mı", "due diligence", "değerleme yap", "büyüme potansiyeli", "bunu satın alsam
  mı", "satmak istiyorlar", "bilen adamlar mı yapmış", "rakipleri kim" dediğinde bu skill'i kullan.
  Bir App Store / Google Play / şirket sitesi linki paylaşıp "ne düşünüyorsun" dediğinde de kullan.
  İngilizce "value this startup", "how much is this app worth", "should I acquire", "startup
  research", "valuation" ifadelerinde de tetikle. Kullanıcı "skill" veya "derin araştırma"
  demese bile, ortada bir şirketin ne kadar ettiği veya ne kadar iyi olduğu sorusu varsa devreye gir.
  Tek bir startup için de, arka arkaya onlarca startup taraması için de aynı skill kullanılır.
---

# Startup Derin Araştırma & Değer Tespiti

## Bu skill ne işe yarar

Bir startup'ın **gerçekte ne kadar ettiğini** bulmak. "Değerleme" (valuation) kelimesinden
kaçınıyoruz çünkü o kelime lisanslı bir faaliyeti ve DCF tablolarını çağrıştırıyor. Burada
üretilen şey daha dürüst bir şey: **kanıta dayalı tahmini piyasa değeri aralığı** — yani
"bugün bir alıcı bulunsa bu iş kaç paraya el değiştirir".

Türkiye'de erken aşama startup'larda pitch deck rakamlarının çoğu doğrulanamaz. Bu skill'in
tüm mimarisi tek bir fikrin üstüne kurulu: **kurucunun anlattığı hikâyeyi değil, dış dünyada
iz bırakmış kanıtı fiyatla.** İndirme sayısı, review tarihleri, takipçi/indirme oranı, ticaret
sicil tarihi, son güncelleme tarihi — bunlar yalan söylemez. Deck söyler.

---

## Çalışma prensipleri (bunları atlarsan rapor değersizleşir)

### 1. Her rakamı etiketle
Rapordaki her sayının yanına kaynağı ve güven seviyesi gider:

- `[D]` **Doğrulandı** — kendi gözünle dış kaynakta gördün (Play Store'da "1 B+ indirme")
- `[T]` **Türetildi** — doğrulanmış veriden hesapladın (27 iOS puanı → ~%1-2 puanlama oranı → ~1.500-2.500 iOS indirme)
- `[İ]` **İddia** — şirket/kurucu söylüyor, doğrulanamadı ("50 üniversitede aktifiz")
- `[Y]` **Yok** — bulunamadı; bunu gizleme, açıkça yaz

Bir raporda `[İ]` ve `[Y]` sayısı çoksa bu başlı başına bir bulgudur: şeffaf olmayan bir şirket
daha düşük çarpanla fiyatlanır. Rapor sonunda **Kanıt Skoru** ver: doğrulanmış kritik metrik / toplam kritik metrik.

### 2. Asla rakam uydurma
Bilinmeyen bir metriği "sektör ortalaması ~X'tir" diye doldurmak raporun tamamını çürütür.
Bilmiyorsan `[Y]` yaz ve o boşluğun değeri nasıl etkilediğini söyle
("MAU bilinmediği için kullanıcı başı değerleme yapılamadı; aralık bu yüzden geniş").

### 3. Vanity metrik çapraz kontrolü — en çok bulgu çıkaran adım
Tek bir metriğe bakma, **metrikler arasındaki oranlara** bak. Tutarsızlık, şişirilmiş metriğin imzasıdır:

| Oran | Sağlıklı bant | Sapma ne anlatır |
|---|---|---|
| Instagram takipçi ÷ toplam indirme | 0,1 – 1,0 | >3 ise takipçi satın alınmış ya da içerik hesabı ürüne dönüşmüyor |
| Play yorum sayısı ÷ Play indirme | %0,5 – %2 | Çok düşük = ölü kullanıcı; çok yüksek = teşvikli/sahte yorum |
| iOS puan sayısı ÷ Android indirme | TR'de ~%5-15 | Çok yüksek+5,0 puan = organik olmayan puanlama |
| Son 90 gün yorum ÷ toplam yorum | canlı üründe %10+ | ~0 ise ürün fiilen durmuş |
| Aylık altyapı gideri ÷ tahmini MAU | küçük TR sosyal app'te <2 TL | Yüksekse ya gizli ölçek var ya kötü mimari |

Bu oranların hesabı ve yorumu için `references/kirmizi-bayraklar.md`.
Sosyal hesabın kendisinin gerçekliği ayrı ve zorunlu bir adımdır — Aşama 4B.

### 4. Para birimi disiplini (Türkiye için kritik)
TL rakamları enflasyon yüzünden 6 ay sonra anlamsızlaşır. Bu yüzden:
- Her TL tutarın yanına **tarih** ve **o günkü USD karşılığı** yaz.
- Değer aralığını **hem TL hem USD** ver; ana çıpayı USD yap.
- Kur oranını rapor tarihinde canlı doğrula, ezberden yazma.
- Gider kalemlerinde para biriminin TL mi USD mi olduğu belirsizse **kullanıcıya sor** —
  40.000 TL/ay bulut gideri ile 40.000 USD/ay bulut gideri iki bambaşka şirkettir.

### 5. Tarafın alıcıdır, değeri tabandan kur
Bu raporlar kurucuya değil, **alıcıya ya da yatırımcıya** hizmet eder. Kurucu anlatısına
yakın duran bir rapor işe yaramaz; pazarlık kozu ve risk listesi üreten rapor işe yarar.

Pratikte bu, değerlemenin **yönünü** değiştirir. Tavandan aşağı inme (pazar büyüklüğü,
vizyon, potansiyel, sonra iskonto). Tabandan yukarı çık:

1. Bugün kapatılsa ne satılır (kod, marka, alan adı, veri)
2. Bugünkü haliyle devredilse ne eder (yürüyen işletme)
3. Ancak kanıt geldikçe yukarı çık (gelir, aktif kullanıcı, organik kanal, ekip devri)

Her adımda ispat yükü satıcıdadır. Doğrulanamayan iddia fiyatlamada **sıfır** kabul edilir,
düşük değil sıfır. Bu acımasız görünür ama alıcının gerçekte yaptığı budur; raporun bunu
önceden yapması satıcıyı da korur, çünkü masada sürprizle karşılaşmaz.

Eleştirel oku demek karamsar ol demek değil. Yeşil bayrakları da ara ve yaz
(`references/kirmizi-bayraklar.md` sekizinci bölüm). Fark şurada: olumlu bulguyu da
kanıtıyla yaz, izlenimle değil.

### 6. Hesap açma sınırı
Ürünü içeriden görmek raporun en değerli parçasıdır ama **kullanıcı adına hesap açmazsın,
şifre girmezsin, öğrenci/kimlik doğrulaması yapmazsın.** Bunun yerine:
1. Kullanıcıdan bir **test hesabı** iste (kullanıcı adı + şifreyi kendisi girsin ya da demo hesap versin),
2. Yoksa kayıt gerektirmeyen her yüzeyi sonuna kadar tara: onboarding ekranları (store
   ekran görüntüleri), web app'in public kısmı, davet/paylaşım linkleri, `/api` yanıtları,
   web sitesi, blog, yardım merkezi, gizlilik politikası (hangi 3. parti servisleri kullandığını ele verir),
3. Ve raporda **"ürün içi gezinti yapılamadı"** diye açıkça belirt — bu bir eksiklik notudur, gizlenmez.

---

## Klasör düzeni

Her startup kendi klasörünü alır ve o startup'a ait her şey orada durur. Bir yıl sonra
"bunu daha önce bakmış mıydık" sorusunun cevabı tek klasörde olsun diye.

```
startup değerleme/
├── skill/                    ← bu skill ve yanında kullanılan global skillerin kopyası
├── ortak/
│   ├── tarama-tablosu.csv    ← bütün startup'lar tek tabloda, kıyaslanabilir
│   └── benchmarkler.md       ← taramalardan biriken TR pazar gözlemleri
└── <startup-adi>/
    ├── README.md             ← şirket künyesi, hangi rapor ne zaman yazıldı
    ├── raporlar/             ← teslim edilen PDF'ler ve markdown çalışma dosyaları
    └── veri/                 ← ham veri, hesap girdileri, rapor içerik HTML'leri
```

**Her dosya adı tarih taşır**, `-YYYY-AA-GG` sonekiyle. Rapor da veri de. Bir startup'a
tekrar bakıldığında eski dosya silinmez, yeni tarihle yenisi eklenir; iki tarih arasındaki
fark büyümenin kendisidir ve o fark çoğu zaman rakamların kendisinden daha bilgilendiricidir.
Rapor içinde de tarih iki yerde geçer: kapakta ve veri toplama tarihi olarak yöntem notunda.

## Yanında kullanılan skiller

Bu skill değeri hesaplar. "Ne yapılmalı" sorusunu cevaplayan ayrı bir rapor isteniyorsa
yanına şunlar gelir ve kopyaları `skill/ilgili-skiller/` altında durur:

| Skill | Ne için |
|---|---|
| `aso-expert` | App Store ve Play listing denetimi, anahtar kelime, ekran görüntüsü, dönüşüm testi |
| `seo-expert` | Site teknik ve içerik SEO'su, organik kanal planı, AI aramada görünürlük |
| `mobile-ux-flow-expert` | Kayıt akışı, onboarding, izin ekranı, huninin nerede kırıldığı |
| `web-ux-flow-expert` | Web tarafındaki dönüşüm akışları |

## Akış

Aşamaları sırayla yürüt. Her aşamada bulduğunu `veri/<startup>-ham-veri.md` dosyasına
anında yaz — sonra rapor yazarken hafızadan değil dosyadan çalış, bu uydurmayı engeller.

Bağımsız aramaları **aynı mesajda paralel** yap; bu araştırma çok sayıda sorgu gerektirir,
tek tek sırayla yapmak hem yavaş hem pahalıdır.

### Aşama 0 — Kapsam ve giriş verisi
Kullanıcının verdiklerini not et: isim, sektör, bilinen finansallar, satış niyeti, elindeki
belgeler. Eksikse **bloke olma** — araştırmaya başla, sorularını Aşama 8'e sakla.

Kullanıcı satış/alım niyeti belirttiyse bunu baştan işaretle: satıcı tarafındaysan rapor
"nasıl daha pahalıya satılır"a, alıcı tarafındaysan "nereden vurulur / neyi pazarlık ederim"e bakar.

### Aşama 1 — Kimlik ve tüzel kişilik
Amaç: şirketin gerçekten var olup olmadığı ve ne zamandır var olduğu.
- Ürün adıyla tüzel kişilik adı genelde farklıdır. **App Store "Sağlayıcı" alanı tüzel adı
  neredeyse her zaman ele verir** — en hızlı yol budur.
- Kuruluş tarihi, sermaye, adres, NACE kodu, ortaklar: kaynaklar `references/kaynak-haritasi.md`.
- Kuruluş tarihi ile ürünün yayın tarihi arasındaki fark anlamlıdır (2 yıl fark = ya pivot ya uzun ölü dönem).
- Domain WHOIS kayıt tarihi ücretsiz ve güvenilir bir yaş göstergesidir.

### Aşama 2 — Ürünü ellemek
- Web sitesinin her sayfası (özellikle fiyatlandırma, hakkımızda, iletişim, KVKK/gizlilik metni).
- App Store + Play Store listing'i **tam olarak** oku: ekran görüntüleri, açıklama, sürüm
  notları geçmişi, boyut, minimum OS, desteklenen diller, yaş sınırı.
- Sürüm notları geçmişi bir mühendislik ekibinin nabzıdır. `references/kaynak-haritasi.md`
  içinde sürüm geçmişini çekmenin yolu var.
- Mümkünse test hesabıyla in (yukarıdaki sınıra uyarak) ve **ilk 5 dakika deneyimini** yaz:
  kayıt kaç adım, boş ekran var mı, içerik gerçek kullanıcıdan mı geliyor yoksa admin mi doldurmuş,
  son gönderi ne zaman atılmış. **"Son içerik tarihi" bir sosyal üründe MAU'dan daha dürüst bir metriktir.**

### Aşama 3 — Traksiyon: sert sayılar
`scripts/app_store_cek.py` bunu tek komutta yapar (iOS lookup API + RSS review'lar + Play sayfası):

```bash
python3 scripts/app_store_cek.py --ios-id 6633421265 --play-id com.example.app --ulke tr
```

Toplanacaklar: indirme bandı, puan ortalaması, puan sayısı, yorum sayısı, ilk yayın tarihi,
son güncelleme tarihi, sürüm sayısı, kategori sıralaması, web trafiği, sosyal takipçi sayıları,
LinkedIn çalışan sayısı ve trendi.

Bandları daralt: Play "1 B+" demek 1.000–5.000 arası demektir. iOS için puan sayısından indirme
türetme yöntemi `references/degerleme-yontemleri.md` içinde.

### Aşama 4 — Kullanıcının sesi
Review'lar bir startup'ın en ucuz ve en dürüst müşteri araştırmasıdır. Sadece ortalama puana bakma:
- **Zaman serisi**: yorumlar hangi aylarda yoğunlaştı? Tek bir aya yığılma = kampanya/teşvik.
- **1-2 yıldızları oku ve temalarına ayır**: çökme/bug, boş içerik, spam/bot, moderasyon,
  ödeme sorunu, destek yok. Tema dağılımı ürünün nerede kırıldığını söyler.
- **Geliştirici cevap veriyor mu?** Cevapsız 1 yıldızlar terk edilmiş ürün işaretidir.
- Şikayetvar, Ekşi Sözlük başlığı, Reddit, X aramaları: `references/kaynak-haritasi.md`.
- Rapora **birebir alıntı** koy (kısa, 1-2 cümle) — soyut özet yerine gerçek cümle ikna eder.


### Aşama 4B — Sosyal hesap gerçeklik denetimi (zorunlu)
`references/sosyal-dogrulama.md` + `scripts/sosyal_dogrula.py`.

Büyük takipçi sayısı bir raporda en çok yanlış okunan metriktir ve neredeyse her zaman
avantaj maddesi olarak yazılır. Oysa Türkiye'de 50.000 takipçi 100-250 dolara satın alınır;
yani "büyük hesap" bir startup'ta iki yüz dolarlık bir kalem olabilir. Buna karşılık
**etkileşim satın almak pahalı ve sürdürülemezdir** — bu yüzden gerçekliği ölçmenin
doğru yeri takipçi değil, etkileşimdir.

Her sosyal hesap için:
1. En az 10-12 gönderiyi **hem yeniden hem eskiden** örnekle (yalnızca son gönderilere
   bakmak en sık yapılan hata; son gönderiler reklamla öne çıkarılmış olabilir).
   Instagram'da giriş yapmadan beğeni görmenin yolu embed uç noktasıdır — yöntem referansta.
2. `sosyal_dogrula.py` ile etkileşim oranını, kararı ve **etkin takipçi** sayısını hesapla.
3. Sonucu iki ayrı teşhisten birine bağla:
   - Etkileşim düşük → takipçi sahte/ölü; **kanal diye bir şey yok**, varlık olarak yazılamaz.
   - Etkileşim sağlıklı ama indirmeye dönmüyor → kitle gerçek, ürüne ilgi duymuyor;
     sorun üründe veya onboarding'de — bu **çözülebilir** bir sorundur ve bu ayrım
     değeri doğrudan etkiler.
4. Hesabın **maliyetini** de çıkar: içerik üretimi, reklam, varsa etkileşim satın alma.
   Getirisi yoksa bu bir pazarlama varlığı değil, aylık yakımın gizli kalemidir.

Rapora asla ham takipçi sayısını tek başına yazma; her zaman
**takipçi · etkileşim oranı · etkin takipçi** üçlüsünü birlikte ver.

### Aşama 5 — Ekip: "bilen kişiler mi yapmış"
Bu, erken aşamada değerin en büyük tek bileşenidir. Rubrik ve puanlama:
`references/kurucu-degerlendirme.md`.

Özetle bakılacaklar: kurucuların önceki çıkışları/şirketleri, alan içi yılı, teknik kurucu var mı,
ekip kaç kişi ve trendi ne, danışman/yatırımcı kalitesi, kurucular arası dağılım,
ve **en önemlisi: bu ekibin daha önce dağıtım (distribution) kurmuş olması**. Ürün yapmak
kolaylaştı; kullanıcı bulmak zorlaştı. Dağıtım geçmişi olan ekip primlidir.

### Aşama 6 — Pazar ve rakipler
- Pazarı **aşağıdan yukarı** hesapla (TAM slaytına güvenme): kaç potansiyel kullanıcı ×
  gerçekçi penetrasyon × gerçekçi kullanıcı başı gelir. Yukarıdan aşağı "pazar 10 milyar $"
  cümlesi rapora girmez.
- **En az 5 rakabı aynı metriklerle tabloya çek** (indirme, puan, yorum, monetizasyon,
  son güncelleme). Bu tablo raporun en çok işe yarayan tek görselidir — hedefin nerede
  durduğunu tek bakışta gösterir.
- Rakip bulmanın en hızlı yolu: App Store ürün sayfasındaki "Beğenebilirsiniz" listesi ve
  Play'deki "Benzer uygulamalar". Google aramasından daha isabetlidir.
- **Giriş bariyeri testi**: "Yetenekli 2 kişi 3 ayda bunun aynısını yapabilir mi?" Cevap evet
  ise değer üründe değil, dağıtım/kullanıcı tabanında/markadadır — ve değerleme buna göre kurulur.

### Aşama 6B — Bulunabilirlik: SEO, ASO ve marka talebi (zorunlu)
`references/seo-aso.md` + `scripts/seo_aso_tara.py`.

İndirme sayısı kaç kişinin geldiğini söyler, bulunabilirlik gelmeye devam edip etmeyeceğini.
Alıcı için ikincisi daha pahalı bir sorudur: organik kanalı olmayan ürün, alıcı her ay para
koymayı sürdürdüğü sürece yaşar. O zaman satın alınan şey bir varlık değil bir gider
taahhüdüdür ve fiyat buna göre kurulur.

Tek komutta dört ölçüm çıkar: App Store arama sırası (hedef ve rakip yan yana), mağaza
liste görünürlüğü, sitenin teknik SEO'su, marka arama talebi.

Üç şeye özellikle bak:
- **Kelime kapsamı** %35'in altındaysa büyüme tamamen dış yönlendirmeye bağlıdır.
- **Ürün yalnızca kendi alt başlığındaki ifadede sıralanıyorsa** bu ASO başarısı değil,
  mağazanın metni geri yansıtmasıdır. Kimse o cümleyi aramaz.
- **Marka adı başka bir sektörde daha güçlü bir oyuncuya aitse** bu devirde ek maliyettir;
  alıcı markayı konumlandırmak için harcama yapar, isim değişikliğine kadar gidebilir.

Rakibi mutlaka aynı sorgularla ölç. Tek başına bir sıralama sayısı anlamsız, karşılaştırma
anlamlıdır.

### Aşama 7 — Para
- Gelir modeli var mı, fiilen para akıyor mu, ARPU ne?
- Gider yapısı: bulut, yazılım/lisans, personel, pazarlama, ofis.
- **Aylık net yakım (burn) ve pist (runway)** hesapla.
- **Gider verimliliği** çıkar: aylık altyapı gideri ÷ tahmini aktif kullanıcı. Bu oran bozuksa
  ya gizli bir ölçek vardır ya da mimari/israf sorunu — ikisi de değeri doğrudan etkiler
  (kötü mimari alıcı için "devraldıktan sonra ödenecek gizli fatura"dır).
- Giderlerin ne kadarının **devredilebilir/kısılabilir** olduğunu ayır: alıcı için
  "kapatılabilir gider" değeri artırır, "zorunlu gider" değeri düşürür.

### Aşama 8 — Değer tespiti
`scripts/deger_hesapla.py` ile birden fazla yöntemi aynı anda koştur, yöntemleri
`references/degerleme-yontemleri.md` içinden seç. Tek yöntemle rapor yazma.

Üç ayrı sayı üret — bunlar aynı şey değildir ve karıştırılmaları en sık yapılan hatadır:

1. **Tasfiye / Varlık Değeri** — bugün kapatılsa: kod tabanı, marka/domain, varsa kullanıcı
   verisi, sözleşmeler. Yeniden yapım maliyeti (rebuild cost) yaklaşımı. Bu **taban**dır.
2. **Yürüyen İşletme Değeri** — mevcut haliyle, mevcut traksiyonuyla, mevcut yakımıyla devredilse.
   Gerçekçi alıcı tipini de isimlendir (stratejik alıcı / rakip / acquihire / bireysel operatör).
3. **Potansiyel Değer** — planlar tutarsa 24 ay sonra; ve buna ulaşmak için gereken ek sermaye.
   Bu sayının yanına mutlaka **olasılık** yaz, yoksa kurucu bunu bugünkü fiyat sanır.

Sonra **tek bir "Net Tahmini Değer" aralığı** ver — kullanıcının istediği budur. Aralığın
alt ucu, üst ucu ve **en olası noktası** olsun, ve o noktayı hangi varsayımın taşıdığını yaz.
Belirsizlik yüksekse aralık geniş olur; bu dürüstlüktür, ama "0 ile 10 milyon arası" gibi
kullanılamaz bir aralık kaçamaktır — daraltmak için hangi tek verinin gerektiğini söyle.

### İkinci teslim: Bulunabilirlik ve Büyüme Denetimi

Değer raporu "kaç eder" sorusunu cevaplar. Kullanıcı "ne yapılmalı" diye sorduğunda
ayrı bir rapor yazılır, değer raporuna karıştırılmaz. İkisi farklı okuyucuya hizmet eder:
biri alıcıya, diğeri işletene.

Bu raporda `aso-expert` ve `seo-expert` skilleri kullanılır ve şu sıra izlenir:

1. **Huniyi teşhis et.** Sorun görünürlükte mi, ilk izlenimde mi, sayfada mı. Kimse görmüyorsa
   ekran görüntüsü tartışmak erkendir. Bu sırayı atlamak ASO işinin en sık hatası.
2. **Talebin nerede olduğunu ölç, varsayma.** App Store otomatik tamamlama ucu, mağazanın
   kendi kullanıcılarından gelen gerçek arama verisidir ve bedavadır. Çoğu zaman ekibin
   hedeflediği kelimede talep olmadığını gösterir.
3. **İki mağazayı ayrı yaz.** iOS'ta açıklama aramada dizinlenmez, Play'de uzun açıklama
   birincil sıralama girdisidir. Aynı metni iki mağazaya koymak birinde yanlıştır.
4. **Yerel bütçeyi hatırla.** Türkiye vitrininde ikincil dizinlenen diller İngilizce ve
   Fransızca; bunları doldurmak dizinlenebilir bütçeyi üçe katlar ve bunu yapan azdır.
5. **Site içeriğini ürünün zaten ürettiği içerikle kur.** Çoğu startup doğru içeriği
   üretip yanlış yerde yayınlıyor; sosyal medyada yirmi dört saatte ölen içerik sitede
   kalıcı olurdu. Bunu ara, çünkü bulunduğunda maliyeti sıfır olan tek büyüme kanalıdır.
6. **AI aramada görünürlüğü test et.** Alıcının soracağı beş altı soruyu çalıştır, kimin
   kaynak gösterildiğine bak. Bu test genelde raporda olmayan rakipleri de ortaya çıkarır.
7. **Yol haritasını sürüm bağımlılığına göre sırala:** bugün yapılabilecekler, sonraki
   sürüm, sonraki çeyrek. iOS'ta meta verinin çoğu sürüme bağlı, Play'de değil.
8. **Ölçüm planı olmadan teslim etme.** Ölçüm planı olmayan optimizasyon planı dilek listesidir.

Sayı disiplini burada da geçerli ve bir ekleme var: **iki mağaza için de yayımlanmış sayısal
sıralama ağırlığı yoktur.** Ortada dolaşan yüzdeler uydurmadır, rapora girmez.

### Aşama 9 — Rapor
`references/rapor-sablonu.md` şablonunu birebir kullan. Çalışma dosyası:
`raporlar/<startup>-<YYYY-AA-GG>.md`.

**Yazım kuralları zorunlu:** `references/yazim-kurallari.md`. Özet: tire kullanma
(uzun tire, kısa tire ve noktalama olarak " - " yasak), kalın vurguyu seyrek kullan,
şişirme sıfatlarından ve boş bağlayıcılardan kaçın, sayıyı önce yaz yorumu sonra.
Rapor bir insanın yazdığı iş belgesi gibi okunmalı.

**Teslim edilecek biçim PDF.** Kullanıcıya markalı PDF gider, ham markdown çalışma
dosyasıdır. Üretim:

```bash
python3 scripts/pdf_uret.py --icerik <startup>-icerik.html \
  --cikti "raporlar/<Startup>-Deger-Raporu-<tarih>.pdf" --baslik "<Startup> Değer Raporu"
```

İçerik HTML'i `assets/rapor-iskelet.html` içindeki kapak ve sınıfları kullanır; sadece
`<section>` blokları yazılır, `<html>`/`<head>` yazılmaz. Palet, tipografi ve marka
abdullahfarukcom deposundan geliyor ve font PDF'e gömülüyor. Script içerikte tire
bulursa üretmeyi reddeder.

**Üretimden sonra dizgiyi denetle, teslim etmeden önce:**

```bash
python3 scripts/pdf_denetle.py "raporlar/<Startup>-Deger-Raporu-<tarih>.pdf"
```

Chrome'un sayfalama davranışı HTML'e bakarak tahmin edilemez; hatalar ancak üretilmiş
PDF ölçülerek görülür. İki hata çok sık çıkıyor ve ikisi de gözden kaçıyor:
bölümlere verilen zorunlu sayfa sonları sayfaların yarısını boş bırakıyor, ve tabloların
son sütununda sıfır sağ boşluk içeriğin kesildiği hissini veriyor. Script her sayfanın
doluluk oranını ve kenar boşluklarını ölçüp ikisini de yakalar, çözümünü de yazar.

Kural: zorunlu sayfa sonu (`class="pagebreak"`) varsayılan değildir, içerik aksın.
Uzun tablolar bölünsün ama başlığı tekrarlansın ve satır ortadan kesilmesin; yalnızca
kısa tablolara `class="tight"` verilir. Denetim temiz çıkmadan rapor teslim edilmez.

Rapor Türkçe yazılır (kullanıcı aksini istemedikçe), ilk sayfada karar verilebilir olur,
ve kurucuya gösterilebilecek kadar saygılı ama alıcıya gösterilebilecek kadar acımasız olur.

---

## Onlarca startup'ı arka arkaya tararken

Bu skill tek seferlik bir rapordan fazlası için tasarlandı. Seri tarama yaparken:

- **Ortak dosya**: `veri/tarama-tablosu.csv` — her startup bir satır, aynı sütunlar
  (isim, sektör, kuruluş yılı, indirme, puan, yorum, IG takipçi, çalışan, aylık yakım,
  net değer alt/üst, potansiyel skoru, karar). Böylece startup'lar birbiriyle kıyaslanabilir hale gelir.
- **Aynı rubrik, aynı ölçek**: Büyüme Potansiyeli ve Ekip skorları her raporda aynı
  1-10 tanımıyla verilir (`references/kurucu-degerlendirme.md`), yoksa kıyas anlamsızlaşır.
- **Eleme önce**: Aşama 1-3 ucuzdur. Traksiyon ve tüzel kişilik bakışında iş açıkça
  ölüyse (ör. 12 aydır güncelleme yok + 100 indirme), tam raporu yazma; yarım sayfalık
  "elendi" notu yaz ve sebebini belirt. Zamanı canlı adaylara harca.
- **Öğrenilenleri biriktir**: her tarama sonunda TR pazarına dair çıkan çarpan/benchmark
  gözlemini `veri/benchmarkler.md` dosyasına ekle. 10 startup sonra bu dosya skill'in
  en değerli parçası olur — çünkü artık gerçek yerel karşılaştırma verisi vardır.

---

## Referans dosyaları

Gerektiğinde oku, hepsini baştan yükleme:

- `references/kaynak-haritasi.md` — Nereden hangi veri çekilir. TR'ye özel kaynaklar
  (ticaret sicili, KAP, Şikayetvar, Ekşi, startups.watch) + global kaynaklar + tam URL kalıpları. **Aşama 1-6'da aç.**
- `references/degerleme-yontemleri.md` — Yöntemler, hangi durumda hangisi, TR erken aşama
  çarpanları, indirme/kullanıcı türetme formülleri, senaryo kurma. **Aşama 8'de aç.**
- `references/kirmizi-bayraklar.md` — Şişirilmiş metrik tespiti, ölü ürün işaretleri,
  tüzel/hukuki riskler, satıcı tarafı oyunları. **Aşama 3-7'de aç.**
- `references/sosyal-dogrulama.md` — Takipçi gerçek mi, kitle ürüne dönüşüyor mu;
  veri toplama yöntemi (giriş yapmadan), etkileşim bantları, teşhis tablosu. **Aşama 4B'de aç.**
- `references/seo-aso.md` — App Store arama sırası, site teknik SEO'su, marka arama talebi;
  kelime seçimi ve sonuçların değere nasıl çevrileceği. **Aşama 6B'de aç.**
- `references/kurucu-degerlendirme.md` — "Bilen kişiler mi yapmış" rubriği ve puanlama;
  Büyüme Potansiyeli skoru tanımı. **Aşama 5 ve 8'de aç.**
- `references/rapor-sablonu.md` — Zorunlu rapor iskeleti. **Aşama 9'da aç.**
- `references/yazim-kurallari.md` — Tire yasağı, yapay zekâ yazımını ele veren
  alışkanlıkların listesi, ton ve Türkçe sayı biçimi. **Aşama 9'da aç.**
- `assets/rapor-iskelet.html` — PDF içeriği için kapak ve sınıf örneği. **Aşama 9'da aç.**
- `assets/veri-formu.md` — Satıcıya/kurucuya gönderilecek soru listesi. Kullanıcı şirketle
  temas halindeyse bunu ona ver; cevaplar raporun `[İ]` alanlarını `[D]`ye çevirir.

## Scriptler

- `scripts/app_store_cek.py` — iOS (iTunes Lookup + RSS yorumlar) ve Google Play verisini
  tek komutta çeker, JSON basar. `--yardim` ile kullanım.
- `scripts/sosyal_dogrula.py` — Takipçi + örneklenen beğeni/yorum sayılarından etkileşim
  oranı, gerçeklik kararı, kitle→ürün dönüşümü ve hesabın etkin varlık değeri.
- `scripts/seo_aso_tara.py` — App Store kelime sıralaması (hedef ve rakip), mağaza listesi,
  site teknik SEO'su ve Google otomatik tamamlama üzerinden marka talebi.
- `scripts/deger_hesapla.py` — Girdi JSON'undan çoklu yöntemle değer aralığı, yakım/pist,
  senaryo tablosu üretir. Elle çarpma yapma, bunu kullan; hesap izlenebilir olsun.
- `scripts/pdf_uret.py` — İçerik HTML'ini Abdullah Faruk Çiftler kimliğiyle A4 PDF'e çevirir.
  Palet abdullahfarukcom deposundan, font gömülü. Teslim biçimi budur.
- `scripts/pdf_denetle.py` — Üretilen PDF'in her sayfasını ölçer: doluluk oranı, kenar
  boşlukları, boş sayfa, sarkan son sayfa. Teslimden önce çalıştır, temiz çıkmadan gönderme.
