# Fiyat Araştırma Yöntemleri + Benchmark Tabloları

İçindekiler: 1. Araştırma yöntemleri · 2. Rakip teardown yöntemi · 3. Benchmark: danışmanlık (küresel) · 4. Benchmark: engagement arketipleri · 5. Benchmark: TR pazarı · 6. Benchmark: SaaS/ürün normları · 7. Temel oranlar ve kurallar · 8. Kaynaklar

> **Tazelik kuralı:** Bu dosyadaki tüm rakamlar **Ağustos 2026 itibarıyla** derlenmiştir ve *gösterge* niteliğindedir. 25 bin $ üstü teklif, yeni pazar/segment girişi, rakip kıyası veya kullanıcının "emin miyiz" dediği her durumda web search ile canlı doğrula; çelişkide güncel kaynak kazanır. TR tarafında TL rakamlar enflasyon nedeniyle en hızlı bayatlayan satırlardır.

## 1. Araştırma yöntemleri

**Ne zaman hangisi:** 5–10 müşteriyle konuşabiliyorsan görüşme + teardown yeterlidir; 30+ yanıt toplayabiliyorsan Van Westendorp ekle; özellik-fiyat takası kritik bir kurumsal üründe conjoint düşün. Araştırmasız fiyat = tahmin; tek yöntemle fiyat = yarım tahmin. En az iki kaynağı kesiştir.

### 1.1 Müşteri görüşmesi (WTP sinyali)
- **Asla sorma:** "Ne kadar öderdiniz?" — insanlar pazarlık moduna girer ve düşük söyler.
- **Sor:** "Bu problemi bugün nasıl çözüyorsunuz, neye mal oluyor?" · "Bu iş çözülse ne değişirdi, kabaca parasal karşılığı?" · "Benzer araçlara/danışmanlıklara ne ödüyorsunuz?" · (fiyat testi için) "X fiyat deseydim ilk tepkiniz ne olurdu?" — tepkinin *gerekçesi* rakamdan değerlidir.
- 5 görüşmede aynı itiraz iki kez geliyorsa o itiraz fiyat sayfasında/teklifte peşinen cevaplanır.

### 1.2 Van Westendorp (Price Sensitivity Meter)
Dört soru (her katılımcıya, ürün net anlatıldıktan sonra):
1. Hangi fiyatta bu ürün **kalitesinden şüphe edecek kadar ucuz** olurdu?
2. Hangi fiyatta **kelepir/çok iyi alım** olurdu?
3. Hangi fiyatta **pahalı ama yine de değerlendirilebilir** olurdu?
4. Hangi fiyatta **satın almayı düşünmeyecek kadar pahalı** olurdu?
Kümülatif eğriler çizilir; "çok ucuz"×"pahalı" ve "ucuz"×"çok pahalı" kesişimleri **kabul edilebilir fiyat aralığını**, ortadaki kesişimler optimal/kayıtsızlık noktalarını verir. Pratik notlar: n≥30 minimum, ~100 ideali; segment bazında ayrı çiz (TR-içi ve global aynı ankete karışmaz); zayıflığı — niyet beyanıdır, gerçek satın alma değildir → çıkan aralığı birim ekonomi ve teardown ile çapraz kontrol et.

### 1.3 Gabor-Granger
Tek fiyat sorusu merdiveni: "X'e alır mıydınız?" evet→daha yüksek, hayır→daha düşük fiyat sorulur; talep eğrisi ve gelir-maksimize fiyat çıkar. VW'den hızlıdır ama çapa etkisine açıktır; kısa anketlerde VW ile birlikte kullan.

### 1.4 Conjoint / MaxDiff
Özellik+fiyat kombinasyonlarını seçtirerek her özelliğin parasal değerini ölçer. Ne zaman: paket/çit kararının belirsiz olduğu, yanıt toplayabilen (n≥150) kurumsal ürünler. Solo/mikro işte overkill — teardown + görüşme + VW yeter.

### 1.5 Smoke test / fiyat sayfası testi
Ürün yokken fiyatlı sayfa + "satın al" niyeti ölçümü meşrudur; ancak ödeme alıp teslim etmemek olmaz — buton sonrası "erken erişim listesi" dürüstçe açıklanır. Canlıda fiyat A/B testi yapılacaksa aynı anda aynı segmente farklı fiyat göstermenin güven riskini yönet: kohort bazlı (yeni kayıtlar), bölge bazlı veya süre bazlı test tercih et.

## 2. Rakip teardown yöntemi

1. 5–8 rakip seç (2 pahalı lider, 3 emsal, 2 ucuz alternatif — "hiçbir şey yapmamak" ve "içeride Excel'le yapmak" da rakiptir).
2. Her biri için: fiyat sayfası (plan/metrik/fiyat), yıllık indirim, kurumsal kapı, deneme/iade koşulu, son fiyat değişikliği (arşiv sitelerinden geçmiş sürümlere bak), G2/Capterra yorumlarında fiyat şikayeti/övgüsü.
3. Çıktı: fiyat-değer haritası (x: fiyat, y: kapsam/değer) → boş kadran fırsattır. Kendini haritaya koy ve konum cümlesi yaz: "X'ten kapsamlı, Y'den ucuz, Z'nin yapamadığı A'yı yapıyor."
4. Danışmanlıkta teardown: rakip teklifleri, kamu çerçeve fiyatları (İngiltere G-Cloud, ABD GSA gibi yayınlanmış gün ücretleri) ve alıcının alternatif maliyeti (kadro, Big-4) üzerinden yapılır.

## 3. Benchmark: danışmanlık saatlik bantları (küresel, Ağustos 2026)

| Katman | Saatlik (USD) | Not |
|---|---|---|
| Offshore/nearshore SI (Hindistan, CEE, LATAM) | 80–250 | Ölçek işi; kıdemli AI mimarı kıt |
| Bağımsız/freelance uzman | 75–200 (AI odaklıda tipik 100–300) | ABD günlük ~600–1.200$ |
| Butik ajans/danışmanlık | 150–350 (Avrupa butik blended 250–450) | Orta pazarın ana bandı |
| Orta ölçek firma | 300–600 | |
| Big-4 / MBB | 300–900 (partner 900$+; pod blended ~480–580) | Marka primi; piramit maliyeti |

Ek gözlemler: ABD ajans günlükleri ~1.500–2.500$; SF/NYC ulusal ortalamanın %15–25 üstü; regüle sektörler %15–30 prim; 12+ ay taahhüt %10–20 hacim indirimi normal. AI danışmanlık ücretleri 2024'ten beri yılda ~%10–15 arttı; AI-native sabit fiyatlı firmalar orta pazarda aşağı yönlü baskı yaratıyor.

## 4. Benchmark: engagement arketipleri (AI/dijital danışmanlık, Ağustos 2026)

| Arketip | Süre | Bant (USD) |
|---|---|---|
| Executive briefing / fırsat taraması | 2–4 hafta | 15K–40K |
| Strateji yol haritası | 4–12 hafta | 40K–200K |
| Pilot uygulama (production-grade MVP) | 6–12 hafta | 80K–300K |
| Çoklu use-case rollout | 6–12 ay | 300K–2M+ |
| Fractional advisor retainer | sürekli | 15K–45K/ay |
| Eğitim/capability academy | 4–12 hafta | 50K–200K (kişi başı ~2–8K) |

Yıl-1 kurumsal GenAI programı tipik 170K–680K$; faz payları: keşif %10–15, pilot %25–35, productionization %25–35, entegrasyon+governance %15–20, adaptasyon %10–15. Yıl-2 "operate" retainer'ları (yönetilen AI operasyonu) 5–25K$/ay. Konum sinyalleri: 50K$ altı "pilot" çoğunlukla notebook demosudur (alıcı için kırmızı bayrak, satıcı için konumlandırma dersi); sonuç bazlı sözleşmeler danışmanlıkta hâlâ <%8. Norm ticari yapı: **fixed-fee keşif → tavanlı T&M uygulama**.

## 5. Benchmark: TR pazarı (Ağustos 2026 — en hızlı bayatlayan bölüm)

- TR-içi freelance yazılım saatlikleri (yerel müşteri): junior ~150–300 TL, orta ~400–700 TL, kıdemli ~800–1.200+ TL — yani orta seviye ~10–17$/saat: küresel bağımsız bandının ~1/10'u. **Sonuç:** TR-içi işte saatlik pazarlığına girme; productized/proje fiyatı çalış ve iki-liste kuralını uygula (playbook §7).
- TR maaş çapaları (aylık, ilan/veri siteleri): yazılımcı ortalama ~69K TL (bant ~43–119K); "yazılım danışmanı" beklenti ortalaması ~41K TL. Kurumsal TR alıcısının kafasındaki çapa budur; danışmanlık günlüğünü bu çapayla değil, projenin değeriyle konuştur.
- TR forum/piyasa görüşü: ihracat işinde bağımsız yazılımcı tabanı "min ~50$/saat" düzeyinde telaffuz ediliyor; TR'de saatlik model zaten zayıf, iş proje bazlı dönüyor.
- Taban formülü (TR şahıs için): (hedef yıllık net + yıllık gider + vergi/SGK payı) ÷ satılabilir gün — `fiyat_hesap.py taban` bunu hesaplar; vergi payının gerçek oranı için `sahis-vergi-yukumluluk` çerçevesi geçerlidir.

## 6. Benchmark: SaaS/ürün normları (Ağustos 2026)

- Kullanım bazlı fiyatlamanın (UBP) herhangi bir biçimini kullanan SaaS oranı ~%30'dan (2019) ~%85'e (2024) çıktı; 2026'da baskın yapı **hibrit** (taban abonelik + kullanım/kredi). Saf koltuk modeli AI ajan baskısıyla geriliyor; Gartner 2030'a dek kurumsal SaaS harcamasının en az %40'ının kullanım/ajan/sonuç bazlı modellere kaymasını öngörüyor.
- Sonuç bazlı SaaS örnek bandı: çözüm-başına ücret (ör. AI destek ajanlarında çözülen talep başına ~1$ mertebesi kamuya mal olmuş örnek) — sadece atfedilebilir sonuçta.
- Alıcı tarafı gerçeği: AI tüketim modelleri bütçe oynaklığı yaratıyor (token fiyatları yıllık ~%80 düşerken toplam harcama ~3 kat arttı) → kurumsal satışta commit + tavan + kullanım raporu satış kolaylaştırıcıdır.
- Sağlık eşikleri: brüt marj ≥%70 (AI-yoğun üründe plan bazında stres testi şart), LTV/CAC ≥3, CAC geri ödeme ≤12 ay, yıllık plan indirimi %15–20, B2B SaaS'ta logo churn ayda ≤%1–2 iyi kabul edilir (mikro-SaaS'ta %3–5 normal başlangıç).

## 7. Temel oranlar ve kurallar (ezber seti)

- **%1 fiyat iyileştirmesi ≈ %8–11 işletme kârı etkisi** (klasik McKinsey/pricing literatürü kuralı) — fiyat, kâr kaldıraçlarının en güçlüsüdür; hacim ve maliyetten önce gelir.
- İndirim matematiği: gerekli ek hacim = indirim ÷ (marj − indirim). Zam matematiği: tolere edilebilir hacim kaybı = zam ÷ (marj + zam). (`fiyat_hesap.py indirim|zam`)
- Değer bazlı pay: düzeltilmiş yıllık etkinin %10–20'si; müşteriye 3–10x ROI bırakılır.
- Solo danışman kapasitesi: yıl ~100–140 faturalanabilir gün (satış+admin+izin sonrası); %60–70 doluluk sürdürülebilir tavandır.
- Fixed-fee tamponu %15–35 (kapsam netliğine göre); yarım gün = tam günün %60–70'i; peşinat %30–50.
- Win-rate: >%80 → fiyat düşük; %40–60 → sağlıklı; <%25 → fiyat/segment/konumlandırma sorunu.

## 8. Kaynaklar (derleme tarihi: Ağustos 2026)

- Alice Labs — AI Consulting Rates 2026 (katman/arketip/faz tabloları; G-Cloud 14, Kammarkollegiet, GSA çerçeve verileriyle çapraz): alicelabs.ai/en/insights/ai-consulting-rates-2026
- AY Automate — AI Automation Consultant Hourly Rates 2026: ayautomate.com/blog/ai-consultant-hourly-rate-guide-2026
- Layer3 — AI Consulting Rates & Pricing 2026: layer3labs.io/guides/ai-consulting-rates-pricing
- Nicola Lazzari — US/UK AI consultant günlük bantları: nicolalazzari.ai/guides/ai-consultant-pricing-us
- AIDOLS — AI Consulting Cost Guide 2026 (yıllık %10–15 artış tespiti): aidolsgroup.com
- Flexprice — Why AI Companies Adopted UBP (UBP %30→%85; outcome-based bölümü): flexprice.io/blog/why-ai-companies-have-adopted-usage-based-pricing
- Monetizely — 2026 Guide to SaaS, AI and Agentic Pricing Models: getmonetizely.com
- Userpilot — SaaS Pricing Models 2026 (hibrit > outcome tespiti; Intercom Fin örneği): userpilot.com/blog/saas-pricing-models
- BetterCloud — 2026 State of SaaS (bütçe oynaklığı; token -%80 / harcama +%320): bettercloud.com/monitor/saas-industry
- SPI Research Professional Services Maturity Benchmark 2026 (outcome <%8) — Alice Labs üzerinden aktarım
- Stripe — Cost-based vs value-based pricing (taban/tavan çerçevesi): stripe.com/resources
- Alan Weiss — Value-Based Fees (değer bazlı ücret ilkeleri; kitap)
- Wikipedia — Good–better–best pricing; Van Westendorp PSM (yöntem tanımları)
- TR verisi: eleman.net yazılımcı 2026 kazanç haritası; kariyer.net yazılım danışmanı maaş beklentisi; gksoft.com.tr freelance saatlik bantları (2025); r10.net piyasa görüşü; vergimerkezi.com.tr tersine maaş hesabı formülü
