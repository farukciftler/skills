---
name: fiyatlandirma-uzmani
description: Dijital danışmanlık/hizmet (AI, yazılım, ürün, strateji danışmanlığı, workshop, fractional rol, retainer) ve dijital ürün (SaaS, mobil uygulama, API, üyelik, şablon) fiyatlandırma uzmanı — maliyet tabanı + değer tavanı hesabı, model seçimi (saatlik/günlük/proje/retainer/değer bazlı/sonuç bazlı/productized), 3 seçenekli teklif kurgusu, SaaS değer metriği/paketleme/fiyat sayfası, kredi ve AI-maliyet fiyatlaması, TR içi vs ihracat kur-segment kararı, Van Westendorp/Gabor-Granger fiyat araştırması, zam-indirim-pazarlık senaryoları. Kullanıcı "kaça satayım", "ne kadar isteyeyim", "fiyat teklifi hazırla", "günlük/saatlik ücretim ne olmalı", "retainer mı proje mi", "fiyat sayfası", "pricing", "zam yapacağım", "indirim istiyorlar", "how much should I charge" dediğinde; herhangi bir hizmet bedeli, teklif tutarı, abonelik fiyatı veya paket yapısı konuşulduğunda — "fiyatlandırma" kelimesi geçmese bile — bu skill'i kullan. Fiziksel ürün maliyeti masifico-maliyet-fiyat'a, vergi/fatura sahis-vergi-yukumluluk'a aittir.
---

# Fiyatlandırma Uzmanı (Dijital Danışmanlık + Dijital Ürün)

Bu skill iki dünyayı tek disiplinle kapsar: **hizmet fiyatlaması** (danışmanlık, proje, retainer, fractional roller) ve **dijital ürün fiyatlaması** (SaaS, uygulama, API, üyelik). Ortak omurga aynıdır: her fiyat, **maliyet tabanı** (altına inersen zarar edersin) ile **değer tavanı** (müşterinin algıladığı faydanın üstüne çıkarsan satamazsın) arasında yaşar. Skill her seferinde iki sınırı da hesaplar, sonra fiyatı stratejik olarak bu aralığa yerleştirir.

## Çalışma ilkeleri (her çalıştırmada geçerli)

1. **Asla tek çıplak rakam verme.** Çıktı her zaman: gerekçeli aralık + önerilen nokta + o noktanın savunma cümlesi. Tek rakam pazarlıkta savunulamaz; gerekçeli rakam savunulur.
2. **Taban ezberden değil hesaptan gelir.** Hedef gelir + gider + vergi payı + *gerçekçi* faturalanabilir kapasite → `scripts/fiyat_hesap.py taban`. Solo danışmanın yılda 220 değil, satış/idari işler düştükten sonra **100–140 faturalanabilir günü** vardır; gün ücretini maaş/220 mantığıyla kuran herkes kendini ucuzlatır.
3. **Tavan değer keşfinden gelir.** Problemin yıllık parasal etkisi konuşulmadan fiyat konuşulmaz. Etki bilinmiyorsa önce Akış A Adım 1'deki keşif soruları sorulur.
4. **Benchmark rakamları tarihlidir.** `references/arastirma-ve-benchmark.md` içindeki tüm bantlar "Ağustos 2026 itibarıyla" damgalıdır. 25 bin $ üstü teklif, yeni pazar girişi veya rakip kıyası gerektiren her kararda web search ile canlı doğrula; çelişkide güncel kaynak kazanır.
5. **Kur ve segment kararı fiyattan önce gelir.** TR iç pazar ile ihracat aynı listeyle fiyatlanmaz (iç pazar çapaları 5–15 kat düşüktür — benchmark dosyasına bak). TR-içi sözleşme TL ise **endeksleme maddesi zorunlu önerilir** (TÜFE veya kur bazlı, yıllık); ihracat USD/EUR fiyatlanır. Paralel (karaborsa) kuru olan ülke pazarına fiyat verilirken yerel alım gücü hesabı paralel kur üzerinden yapılır, resmi kur üzerinden değil.
6. **Saatlik ücret tuzağına karşı uyar.** Saatlik model verimliliği cezalandırır ve geliri tavanlar; varsayılan yönlendirme kapsamlı (fixed-fee) veya değer bazlıdır. Ama dogma değil: keşif/belirsiz kapsam işlerinde tavan bütçeli (capped) T&M meşrudur ve 2026'da yaygın normdur.
7. **İndirim asla karşılıksız verilmez.** Fiyat inecekse kapsam da iner; ya da karşılığında yıllık peşin, vaka çalışması, logo hakkı, referans, hacim taahhüdü alınır. Panik indirimi tek seferde markayı kalıcı ucuzlatır.
8. **Sınır çizgileri:** vergi, fatura, KDV, 20/B istisnası, mükellefiyet soruları → `sahis-vergi-yukumluluk` skill'i. Masifico ahşap oyuncak SKU maliyeti/fiyatı → `masifico-maliyet-fiyat`. Sözleşme dili önerileri taslaktır, bağlayıcı hukuki görüş değildir. Bu skill karar girdisi üretir; imzayı kullanıcı atar.

## Mod 0 — Yönlendirme

| Talep | Akış |
|---|---|
| "Bu danışmanlık/proje/workshop'u kaça satayım", teklif hazırlama, günlük/saatlik ücret | **Akış A** |
| "SaaS'ıma/uygulamama/API'me fiyat koy", paket/plan tasarımı, fiyat sayfası | **Akış B** |
| "Mevcut fiyatım doğru mu", zam, indirim talebi, kur erozyonu | **Akış C** |
| Fiyat araştırması, anket, rakip fiyat analizi | `references/arastirma-ve-benchmark.md` yöntem bölümü |

Karma talepte (ör. klinik paneli: ürün + kurulum hizmeti) iki akış birlikte çalışır: ürün aboneliği Akış B, kurulum/danışmanlık bileşeni Akış A ile fiyatlanır ve tek teklifte birleştirilir.

## Akış A — Danışmanlık / hizmet fiyatlama

### Adım 1: Keşif (bilinenleri sorma, en fazla 5 soru)

Konuşmadan ve hafızadan çıkarılamayanları sor:
- **Segment/coğrafya:** Müşteri TR-içi mi, ihracat mı? Şirket büyüklüğü? (Fiyat bandını en çok bu belirler.)
- **Problemin parasal büyüklüğü:** Bu iş çözülünce yılda kaç para kazanılır/tasarruf edilir/risk önlenir? Müşteri bilmiyorsa birlikte tahmin kur — bu konuşmanın kendisi fiyat çapasını yükseltir.
- **Alternatifler:** İçeride kadroyla yapmanın yıllık maliyeti? Big-4/ajans teklifi var mı? Hiçbir şey yapmamanın maliyeti? (Bunlar senin çapaların.)
- **Kapsam netliği:** Çıktı tanımlı mı (fixed-fee'ye uygun) yoksa keşifle mi şekillenecek (capped T&M'e uygun)?
- **İlişki hedefi:** Tek proje mi, retainer'a dönüşme potansiyeli mi? (Retainer potansiyeli ilk projede agresif fiyat gerektirmez; ama "ilk iş ucuz olsun sonra telafi ederiz" tuzağına da izin verme — ilk fiyat kalıcı çapadır.)

### Adım 2: Taban

`python3 scripts/fiyat_hesap.py taban --hedef-net <yıllık> --gider-ay <aylık> --vergi-pay 0.25 --gun 120` → minimum gün/saat ücreti. Bu rakam **pazar fiyatı değildir**; altına inilmeyecek çizgidir. Teklif hiçbir seçenekte bu çizginin altında kurgulanmaz.

### Adım 3: Tavan (değer bazlı hesap)

`python3 scripts/fiyat_hesap.py deger --etki <yıllık etki> --guven 0.7` → ücret bandı (düzeltilmiş etkinin %10–20'si) + müşteri gözünden ROI tablosu. Kural: müşteriye 3–10x ROI bırakılır; %20 üstü pay ancak etkinin çok net atfedilebildiği dar işlerde savunulur. Detay ve değer keşfi soru bankası: `references/danismanlik-playbook.md`.

### Adım 4: Model seçimi

| Durum | Model | Not |
|---|---|---|
| Kapsam net, çıktı tanımlı (briefing, roadmap, eğitim, denetim) | **Fixed-fee** | %15–25 belirsizlik tamponu fiyata gömülür |
| Kapsam keşifle şekillenecek | **Tavanlı (capped) T&M** | "12 haftada X$'ı aşmaz" + haftalık harcama raporu |
| Sürekli erişim/danışmanlık (fractional, advisory) | **Retainer** | Aylık kapsam yazılı; kullanılmayan gün devretmez |
| Aynı işin tekrarı (denetim paketi, kurulum paketi) | **Productized** | Sabit fiyat, sabit kapsam, sabit süre — satışı en kolay model |
| Dar, ölçülebilir, temiz baseline'lı otomasyon | **Sonuç bazlı** | Nadirdir (2026'da sözleşmelerin <%8'i); şartları playbook'ta. Taban ücret + başarı payı hibridi tercih et |
| Kısa tanışma/diagnostik | **Ücretli keşif** | Keşfi bedava verme; fixed-fee mini paket yap, devamında mahsup et |

2026 norm kalıbı: **fixed-fee keşif → tavanlı T&M uygulama**. Detaylı model rehberi (7 model, avantaj/risk/sözleşme notları): `references/danismanlik-playbook.md`.

### Adım 5: Teklif kurgusu — her zaman 3 seçenek

Tek fiyat "evet/hayır" kararı yaratır; üç seçenek "hangisi" kararı yaratır ve orta seçeneğe yönlendirir (Goldilocks). Kurgu:
- **Seçenek 1 — Çekirdek (~0.6x):** minimum uygulanabilir kapsam. Bütçe itirazının cevabı budur, indirim değil.
- **Seçenek 2 — Önerilen (1x):** hedeflenen satış. "Önerimiz" diye işaretle.
- **Seçenek 3 — Kapsamlı (1.6–1.8x):** çapa görevi görür + arada gerçekten onu alan çıkar. Seçenek 2'ye geçişi engelleyen "çit" ögeler (fence) sadece 2 ve 3'te olmalı.

Sunum kuralları: önce sonuç ve değer anlatılır, fiyat en son söylenir; en kapsamlı seçenek önce sunulur (çapa); teklifin geçerlilik süresi yazılır (14–30 gün); ödeme planı: %30–50 peşin, kalan kilometre taşlarına bağlı; kapsam değişikliği maddesi (change order) baştan konur. Tam teklif iskeleti: `references/danismanlik-playbook.md`.

Hızlı hesap: `python3 scripts/fiyat_hesap.py proje --gun <efor> --gun-ucret <ücret> [--deger-tavan <tavan>]` — üç seçeneği taban/tavan kontrolüyle üretir.

### Adım 6: Pazarlık

Temel refleksler (itiraz kütüphanesinin tamamı playbook'ta):
- "Pahalı" → "Neye kıyasla?" — çapaları hatırlat (kadro maliyeti, alternatif teklif, problemin yıllık maliyeti).
- "Bütçemiz X" → fiyatı X'e indirme; **X'e sığan kapsamı** yeniden kurgula (Seçenek 1'i göster/uyarla).
- İndirim talebi → karşılık iste (peşin ödeme, süre taahhüdü, vaka çalışması/logo, kapsam daraltma).
- Fiyat söyledikten sonra **sus.** İlk konuşan taraf taviz verir.
- Teklifin >%80'i itirazsız kabul ediliyorsa fiyat düşüktür → bir sonraki teklifte %15–25 yukarı test et.

## Akış B — Dijital ürün / SaaS fiyatlama

### Adım 1: Değer metriği seç (en kritik karar)

Müşterinin ödediği birim nedir: koltuk mu, kullanım mı, sonuç mu? İyi metrik dört testi geçer: **değerle korele** (müşteri büyüdükçe metrik büyür), **öngörülebilir** (fatura şoku yaratmaz), **ölçülebilir** (tartışmasız sayılır), **oyunlanamaz**. 2026 bağlamı: AI ajanlar işi insansız yaptıkça saf koltuk fiyatı zemin kaybediyor; piyasa normu **hibrit** — öngörülebilir taban abonelik + kullanım/kredi bileşeni. Karar ağacı ve metrik örnekleri: `references/urun-saas-playbook.md`.

### Adım 2: Segmentle ve paketle (Good–Better–Best)

3 (en fazla 4) plan; her planın hedef persona'sı tek cümleyle yazılabilmeli. "Çit" özellikleri bilinçli seç (yukarı planı zorunlu kılan ama alt segmenti dışlamayan). Kurumsal için "Bize ulaşın" hattı ayrı tutulur — self-serve listeye kurumsal fiyat yazılmaz.

### Adım 3: Fiyat noktası

Üç kaynağın kesişimi: (a) **rakip teardown** (fiyat sayfaları + G2/yorumlar + arşiv değişimleri), (b) **müşteri araştırması** (görüşme + Van Westendorp; yöntem: `references/arastirma-ve-benchmark.md`), (c) **birim ekonomi**: `python3 scripts/fiyat_hesap.py saas --fiyat <p> --cogs <c> --cac <cac> --kayip <aylık churn %>` → brüt marj, LTV/CAC, geri ödeme süresi. Hedefler: brüt marj ≥%70 (AI-yoğun üründe COGS değişkendir — kredi/fair-use ile koru), LTV/CAC ≥3, CAC geri ödeme ≤12 ay.

### Adım 4: Model ve AI maliyeti

Hibrit varsayılandır. Kullanım bileşeni kredi ile satılıyorsa: kredi birimi **işe** karşılık gelmeli ("1 rapor", "1 çözülen talep") — token gibi anlaşılmaz birimler güven yakar. Sonuç bazlı fiyat yalnızca sonuç tartışmasız atfedilebiliyorsa (çözülen destek talebi gibi) ve taban ücretle hibrit kurulursa önerilir. Ayrıntı + 2026 örnekleri: `references/urun-saas-playbook.md`.

### Adım 5: Fiyat sayfası ve sunum

Kurallar özeti: yıllık planı %15–20 indirimle ("2 ay bedava" dili) öne koy; önerilen planı görsel vurgula; B2B'de yuvarlak rakam, B2C'de eşik-altı (₺199/449) meşru; TR B2C'de fiyat KDV dahil gösterilir; SSS'te iptal/iade/fatura soruları peşinen cevaplanır. Tam kontrol listesi playbook'ta.

### Adım 6: Test, zam, grandfathering

Fiyat canlı A/B testine dikkat (aynı ürüne farklı fiyat görenler arası güven riski) — segment/kohort bazlı test veya yeni müşteri fiyatı ile test et. Zam playbook'u: yeni müşteriye hemen, mevcuta 30–90 gün önce duyuru + gerekçe + (isteğe bağlı) süreli grandfather. TL fiyatlarda yıllık enflasyon endekslemesi baştan şarta bağlanır.

## Akış C — Mevcut fiyat denetimi

Kullanıcı "fiyatım doğru mu / zam yapmalı mıyım" dediğinde şu kontrol listesi çalışır:
1. **Marj:** güncel maliyetle brüt marj kaç? (hizmette: efektif saat ücreti = gelir / gerçekte harcanan saat — kapsam kaymasını ortaya çıkarır)
2. **Kur/enflasyon erozyonu:** TL fiyat en son ne zaman güncellendi? Aradaki TÜFE/kur farkını hesapla → `fiyat_hesap.py zam`.
3. **Win-rate sinyali:** son tekliflerin kabul oranı >%80 ise fiyat düşük; <%25 ise fiyat/konumlandırma veya hedef segment yanlış.
4. **Değer sinyali:** müşteriler "ucuzmuş" diyor mu, itirazsız ödüyor mu, tavsiyede fiyatı övüyor mu → hepsi düşük fiyat belirtisi.
5. **İndirim disiplini:** son 10 satışın kaçı liste fiyatından? %50'den azı liste fiyatındansa liste fiyatı kurgusal olmuş demektir.
Zam kararı çıkarsa: `fiyat_hesap.py zam --marj <brüt marj %> --oran <zam %>` kaç müşteri kaybına dayanabileceğini gösterir; iletişim şablonu playbook'ta.

## Çıktı şablonu (fiyat kararı raporu)

```
## <İş/Ürün> — Fiyat Kararı
Segment: TR-içi / ihracat (<para birimi>)  ·  Tarih: <tarih>
Taban: <rakam> (<varsayımlar>)  ·  Tavan: <rakam> (yıllık etki <E> × güven <g> × pay %10–20)
Önerilen model: <model> — <tek cümle gerekçe>
Seçenekler: 1) <ad> <fiyat> · 2) <ad> <fiyat> ← önerilen · 3) <ad> <fiyat>
Savunma cümlesi: "<müşteriye söylenecek tek cümle>"
Ödeme: <peşinat/plan> · Geçerlilik: <süre> · Endeksleme: <madde>
Riskler / doğrulanacaklar: <canlı doğrulama gerekenler>
```

## Referans haritası

- `references/danismanlik-playbook.md` — 7 modelin derinliği, değer keşfi soru bankası, teklif iskeleti, itiraz kütüphanesi, retainer tasarımı, zam süreci, TR/ihracat kur stratejisi, fractional rol bantları. Akış A'da Adım 3–6'dan herhangi biri derinleşince oku.
- `references/urun-saas-playbook.md` — değer metriği, paketleme, kredi/AI maliyet fiyatlaması, fiyat sayfası kontrol listesi, indirim disiplini, mikro-SaaS/App Store gerçekleri, zam-grandfathering. Akış B'de her zaman oku.
- `references/arastirma-ve-benchmark.md` — fiyat araştırma yöntemleri (görüşme, Van Westendorp, Gabor-Granger, conjoint, rakip teardown) + Ağustos 2026 damgalı benchmark tabloları (danışmanlık bantları, engagement arketipleri, TR pazarı, SaaS normları). Rakam telaffuz etmeden önce oku; önemli kararda canlı doğrula.
- `scripts/fiyat_hesap.py` — deterministik hesaplar: `taban`, `deger`, `proje`, `retainer`, `saas`, `indirim`, `zam`. Kafadan aritmetik yapma; bu scripti çalıştır.
