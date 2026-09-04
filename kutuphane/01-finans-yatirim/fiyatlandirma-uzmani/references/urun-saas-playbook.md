# Dijital Ürün / SaaS Fiyatlama Playbook'u

İçindekiler: 1. Değer metriği seçimi · 2. Paketleme (G-B-B) · 3. Model karar ağacı · 4. AI maliyeti ve kredi tasarımı · 5. Fiyat noktası psikolojisi · 6. Fiyat sayfası kontrol listesi · 7. İndirim disiplini · 8. Zam ve grandfathering · 9. Mikro-SaaS / indie gerçekleri · 10. Mobil/App Store notları · 11. TR pazarı özel notlar

## 1. Değer metriği seçimi

Fiyatın bağlandığı birim, ürün stratejisinin kendisidir. Dört test: **değerle korelasyon** (müşteri değeri arttıkça metrik artar), **öngörülebilirlik** (müşteri ay sonunu tahmin edebilir), **ölçülebilirlik** (tartışmasız sayılır), **oyunlanamazlık** (hesap paylaşımı gibi kaçaklara dayanıklı).

| Metrik | İyi olduğu yer | Riski |
|---|---|---|
| Koltuk (seat) | İnsanların günlük kullandığı iş araçları | AI ajan çağında değerle korelasyonu zayıflıyor; hesap paylaşımı |
| Aktif kullanıcı | Geniş yayılan iç araçlar | Gelir öngörüsü zor |
| Kayıt/varlık sayısı (kontak, ilan, SKU, hasta, danışan) | CRM/pano tipi ürünler (klinik paneli gibi) | Temizlik yapan müşteri "cezalandırılmış" hissetmesin — bantlı fiyatla |
| İşlem/kullanım (API çağrısı, rapor, mesaj, GB) | Altyapı, API, otomasyon | Fatura şoku → tavan/uyarı şart |
| Sonuç (çözülen talep, tamamlanan iş) | Ajan tipi ürünler, atfedilebilir dar işler | Atıf kavgası; ölçüm altyapısı ister |

Pratik: tek metrik seç, en fazla bir ikincil sınır ekle (ör. "kullanıcı başına + aylık X rapor dahil"). Üç metrikli fiyat anlaşılmaz ve satış maliyetini büyütür.

## 2. Paketleme — Good-Better-Best

- 3 plan (gerekirse + kurumsal "Bize ulaşın"). Her planın hedef persona'sı tek cümle: "Solo kullanıcı / büyüyen ekip / kurumsal". Persona yazamıyorsan plan fazladır.
- **Çit (fence) özellikleri:** üst plana geçmeyi zorunlu kılan az sayıda güçlü özellik (koltuk sınırı, entegrasyonlar, SSO, rapor/analitik, öncelikli destek, API). Çit yanlışsa herkes en ucuz planda oturur.
- **Decoy/Goldilocks:** en pahalı plan çapa görevi görür; orta plan "önerilen" işaretlenir ve ekonominin en iyi olduğu plan orta olur. Fiyat aralıkları: planlar arası tipik 2–3x sıçrama (₺199 → ₺499 → ₺1.299 gibi); 1.2x farklar karar veremeyen müşteri üretir.
- **Freemium kararı:** bedava plan bir pazarlama gideridir; ancak (a) marjinal maliyet ~0, (b) viral/ağ etkisi var, (c) bedava→ücretli dönüşüm yolu netse açılır. AI-yoğun üründe bedava plan COGS yaktığı için sınırlı deneme (14 gün / N kredi) genelde daha doğrudur.

## 3. Model karar ağacı (2026)

1. Ürünü insan mı kullanıyor, ürün işi kendisi mi yapıyor?
   - **İnsan kullanıyor** (araç): koltuk veya kayıt bazlı taban + gerekirse kullanım bileşeni.
   - **İş kendisi yapılıyor** (ajan/otomasyon): kullanım veya sonuç bazlı; koltuk anlamsız.
2. Maliyet kullanımla mı ölçekleniyor (AI çağrıları, altyapı)? → Evet ise mutlaka kullanım/kredi bileşeni ekle; saf sabit fiyat marjı kullanıcı davranışına rehin bırakır.
3. Müşteri fatura öngörüsü istiyor mu (B2B hep ister)? → Taban abonelik + dahil kullanım + aşım (overage) yapısı: **hibrit**. 2026'da baskın norm budur; saf kullanım bazlı, alıcı tarafında bütçe oynaklığı direnci üretiyor.
4. Sonuç tartışmasız atfedilebiliyor mu (çözülen destek talebi, tamamlanan rezervasyon)? → Evet ise sonuç bazlı bileşen düşünülebilir (ör. çözüm başına ücret). Yine de taban ücretle hibritle; saf sonuç bazlı geliri müşterinin adaptasyonuna rehin bırakır.
5. Kurumsal segment varsa: yıllık taahhütlü commit (önceden alınan kullanım havuzu, indirimli) + aşım oranı + gerçek kullanım raporu.

## 4. AI maliyeti ve kredi tasarımı

- **COGS gerçeği:** AI-yoğun üründe birim maliyet (token, GPU, üçüncü API) hem yüksek hem oynak; model fiyatları düşse bile kullanım patlaması toplam maliyeti büyütebilir. Fiyat kurgusu marjı iki yönden korur: (a) gelir tarafında kullanım bileşeni, (b) maliyet tarafında model yönlendirme/önbellek/fair-use.
- **Kredi tasarım kuralları:** kredi birimi **kullanıcının anladığı işe** karşılık gelir ("1 rapor", "1 analiz", "1 çözülen talep") — token/işlem gibi mühendis birimleri güven yakar. Kredi fiyatı içinde ortalama COGS × hedef marj payı bulunur; ağır uçları fair-use ile sınırla. Devir (rollover) politikası baştan yazılır (önerilen: 1 ay sınırlı devir). Kredi biterken davranış: sert kesme değil, uyarı + üst plana/ek pakete yumuşak geçiş.
- **Sınırsız (unlimited) yazma.** "Sınırsız" pazarlaması AI üründe marj intiharıdır; "adil kullanım dahilinde" bile yazacaksan sayısal eşiği sözleşmeye koy.
- **Birim ekonomi kontrolü her plan için:** `fiyat_hesap.py saas` ile plan başına brüt marj ≥%70 hedefi test edilir; en yoğun kullanıcı persona'sıyla stres testi yapılır ("bu planı tavanına kadar kullanan müşteri hâlâ kârlı mı?").

## 5. Fiyat noktası psikolojisi

- **Çapa:** sayfada önce yüksek değer/plan gösterilir; kurumsal planın varlığı orta planı ucuz gösterir.
- **Eşik fiyatlar:** B2C'de ₺199/₺449/$9,99 tarzı eşik-altı meşru; B2B'de yuvarlak ve "ciddi" rakam ($50, $200, ₺2.500) daha iyi çalışır — B2B alıcısı kuruşla değil onay eşiğiyle düşünür (kurumsal kartla onaysız harcama limitlerinin altında kalmak self-serve satışı hızlandırır).
- **Yıllık plan:** %15–20 indirim normu; "2 ay bedava" dili yüzdeden iyi dönüşür. Yıllığı varsayılan sekme yap.
- **Para birimi:** hedef pazarın para birimiyle fiyatla; TR + global satıyorsan bölgesel fiyat listeleri ayrı tutulur (bkz. Bölüm 11). Kur çevrimini müşteriye yaptırma.
- **Fiyatı saklama (self-serve'de):** "fiyat için görüşelim" self-serve ürünü öldürür; kurumsal katman hariç fiyat şeffaf yazılır.

## 6. Fiyat sayfası kontrol listesi

1. 3(+kurumsal) plan; önerilen plan görsel vurgulu; her planda persona cümlesi.
2. Yıllık/aylık geçiş anahtarı, yıllık indirimi açık.
3. Özellik tablosu: en fark yaratan 6–8 satır üstte; devasa tablo yerine "tüm özellikleri karşılaştır" katlanır bölüm.
4. Değer metriği ve sınırlar net: neyin dahil olduğu, aşımda ne olacağı yazılı.
5. Sosyal kanıt fiyatın yanında: logo, kısa referans, kullanıcı sayısı.
6. SSS: iptal, iade, fatura (KDV/kurumsal fatura), plan değişimi, veri güvenliği.
7. Risk azaltıcı: X gün iade garantisi veya kartsız deneme — biri mutlaka.
8. Kurumsal hat: "Ekibiniz 20+ ise konuşalım" tek satır + form.
9. TR B2C sayfasında fiyat KDV dahil; B2B'de "+KDV" açıkça yazılır.

## 7. İndirim disiplini

- İndirim **sadece karşılık ile**: yıllık peşin, çok yıllık taahhüt, vaka çalışması/logo, hacim, eğitim kurumu/öğrenci gibi tanımlı segment programları. "İstedi diye" indirim, liste fiyatını kurgusallaştırır ve mevcut müşterilere haksızlıktır (duyulur).
- **Matematiği göster:** `fiyat_hesap.py indirim --marj 75 --oran 20` → %75 marjlı üründe %20 indirim, aynı kârı korumak için ~%36 ek hacim ister. Satış ekibi/kullanıcı bu sayıyı görmeden indirim konuşmasın.
- Süreli kampanya yapılacaksa: gerçek bitiş tarihi + yılda en fazla 1–2 kez; sürekli kampanya = kalıcı düşük fiyat algısı.
- **Lifetime deal (LTD):** nakit öne çeker ama en yoğun kullanıcıları sonsuza dek sübvanse edersin; AI-COGS'lu üründe özellikle tehlikeli. Kullanılacaksa kredi tavanlı ve sınırlı adetli kurgula.

## 8. Zam ve grandfathering

- Sıra: (1) yeni müşteri fiyatı hemen değişir; (2) mevcut müşteriye 30–90 gün önce e-posta + uygulama içi duyuru, tek paragraf gerekçe + yeni değerin ne olduğu (zamla birlikte gelen özellik varsa öne koy); (3) grandfather kararı: süresiz eski fiyat (sadakat ödülü ama gelir kilidi) vs süreli (12 ay eski fiyat) vs yıllığa geçene eski fiyat — genelde en dengelisi süreli/koşullu grandfather.
- TL fiyatlarda zam pazarlığını otomatiğe bağla: şartlarda yıllık güncelleme maddesi + fiyat sayfasında "fiyatlar yılda bir gözden geçirilir".
- Zam sonrası ölçüm: churn'ü 2 fatura dönemi izle; `fiyat_hesap.py zam --marj <m> --oran <z>` zammın tolere edebileceği müşteri kaybını önceden söyler — kayıp o eşiğin altındaysa zam net kazançtır.

## 9. Mikro-SaaS / indie gerçekleri

- **Düşük fiyat tuzağı:** ₺99/$5 fiyat "çok müşteri" değil "değersiz ürün + destek yükü" üretir. Az müşteri × anlamlı fiyat, çok müşteri × bozuk para'dan her zaman yönetilebilirdir; niş B2B mikro-SaaS'ta $29–99/ay bandı sağlıklı başlangıçtır.
- Tek kişilik üründe destek maliyeti fiyatın içindedir: e-posta destekli plan ucuz, öncelikli/kurulumlu plan pahalı olur.
- İlk 10 müşteriye "kurucu fiyatı" (süreli, isimli) meşru bir lansman aracıdır — kalıcı LTD değil.
- Fiyatı ürün bitince değil, ilk gerçek müşteri konuşmalarıyla belirle; ilk fiyatın "utandırmayan" değil "biraz rahatsız eden" olması gerekir — itirazsız satış = düşük fiyat.

## 10. Mobil / App Store notları (özet)

Komisyon (kademeye göre ~%15–30) ve bölgesel fiyat katmanları fiyat kurgusuna dahil edilir; abonelik > tek seferlik satın alım (LTV); deneme tasarımı ve paywall dönüşümü ASO/monetizasyon işidir → derinlik gerekirse `aso-expert` skill'i ile birlikte çalış. Bu skill fiyat noktası ve paket mantığını kurar; mağaza optimizasyonuna girmez.

## 11. TR pazarı özel notlar

- **Enflasyon ortamında fiyat ömrü kısadır:** TL fiyat listesi 6–12 ayda erir; ya USD-endeksli fiyat + TL gösterim, ya sözleşmede endeksleme, ya disiplinli periyodik zam. Hiçbiri yoksa her ay gizli indirim yapıyorsun demektir.
- B2C'de KDV dahil fiyat gösterimi yasal beklenti; B2B tekliflerinde "+KDV" net yazılır (vergi detayı `sahis-vergi-yukumluluk`).
- TR B2B'de aylık kart ödemesi kültürü zayıf, yıllık fatura + havale güçlüdür → yıllık planı ana ürün yap.
- Global + TR satan ürün için bölgesel fiyat (TR listesi daha düşük) meşrudur; ama VPN arbitrajını sınırlamak için TR fiyatını TR fatura adresi/ödeme yöntemine bağla.
- Çift kurlu ekonomilere (paralel kur olan pazarlar) yerel fiyat verirken alım gücü hesabı paralel kur üzerinden yapılır; faturalama USD/EUR tutulur.
