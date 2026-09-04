# Program Kataloğu — AB GPU/Compute Kaynakları

> **SNAPSHOT: Ağustos 2026.** Buradaki her tarih, kota ve aralık o güne aittir. Kullanıcıya sunmadan önce ilgili çağrı sayfasından canlı doğrula. EuroHPC çağrılarında son saat kuralı: cut-off günü **10:00 (CET/CEST)** — gece yarısı değil.

## İçindekiler
1. EuroHPC JU erişim modları (compute — ücretsiz)
2. AI Factories erişim modları (compute — KOBİ/startup odaklı)
3. AI Gigafactories (altyapı ihalesi)
4. Yarışmalar (nakit + compute)
5. Nakit hibe programları (EIC, DEP, Horizon, STEP)
6. Kesişen kurallar (uygunluk, kotalar)
7. Resmi URL dizini

---

## 1. EuroHPC JU Erişim Modları (klasik hat, birim: node saati)

Yönetim: EuroHPC Joint Undertaking. JU, petascale sistemlerin %35'ini, pre-exascale/exascale sistemlerin %50'ye kadarını "Birlik payı" olarak dağıtır. Erişim ücretsizdir. Dayanak: Council Regulation (EU) 2021/1173 + 2024/1732 + **2026/150** değişiklikleri ve EuroHPC Access Policy (son sürüm: 2025.12).

### 1.1 Benchmark Access
- **Amaç:** Kod ölçeklenebilirlik/AI uygulama testi — sonuç, ileride Regular/Extreme Scale başvurusuna kanıt olur.
- **Tahsis:** ~200–2.500 node saati (sistem bazında sabit menü), süre 2-3 ay.
- **Takvim:** Sürekli açık, **her ayın 1'i saat 10:00 cut-off**. Erişim: cut-off'tan ~2 hafta sonra.
- **Değerlendirme:** İdari + teknik kontrol; hakem paneli yok. Giriş bariyeri en düşük mod.

### 1.2 Development Access
- **Amaç:** Kod/algoritma geliştirme ve optimizasyon; **AI uygulama metodu geliştirme açıkça kapsamda**. Centres of Excellence / Competence Centre bağlamı da kabul.
- **Tahsis:** ~800–4.500 node saati, süre 6-12 ay, **2 kez yenilenebilir** (toplam ~3 yıla kadar).
- **Takvim:** Sürekli açık, aylık cut-off (her ayın 1'i, 10:00). Erişim ~2 hafta.

### 1.3 Regular Access
- **Amaç:** Bilimsel inovasyon; büyük tahsis gerektiren olgun projeler. Petascale + pre-exascale + exascale sistemler.
- **Track'ler:** Scientific (akademi/kamu araştırma) / **Industry** (PI sanayiden) / Public Administration.
- **Tahsis:** ~20.000–1.800.000 node saati, süre 12 ay. PI başına prensipte **tek aktif Regular** başvurusu.
- **Takvim 2026:** cut-off **30 Mart 2026** ve **4 Eylül 2026** (yılda 2). Hakemlik ~4 ay.
- **Değerlendirme:** Teknik değerlendirme + bilimsel hakem paneli (peer review).

### 1.4 Extreme Scale Access
- **Amaç:** Yüksek etki / yüksek kazanım, dev tahsisli çığır açıcı işler.
- **Sistemler (2026):** LUMI, Leonardo, MareNostrum 5, JUPITER.
- **Tahsis:** ~100.000–3.000.000 node saati, süre 12 ay. Track'ler: Scientific / Industry / Public Administration.
- **Takvim 2026:** cut-off **4 Mayıs 2026** ve **19 Ekim 2026**. Hakemlik ~6 ay.

### 1.5 AI for Science and Collaborative EU Projects
- **Amaç:** AI'ın bilimsel iş akışının parçası olduğu araştırma; etik AI, ML, foundation model, üretken AI/LLM vurgusu.
- **Kimler:** Tüm bilimsel kullanıcılar (ulusal/AB fonlu olsun olmasın), kamu; **sanayi ancak Horizon Europe veya DEP fonlu ortak projede yer alıyorsa**. Diğer sanayi → AI for Industrial Innovation modlarına.
- **Tahsis:** ~20.000–90.000 node saati, süre 6 ay (+3 ay/+%10 uzatma, ara rapor onayıyla). EuroHPC AI-uyumlu payının %25'ine kadar.
- **Takvim 2026:** cut-off **30 Nis / 30 Haz / 31 Ağu / 30 Eki / 11 Ara 2026** (2 ayda bir). Sonuç ~30 gün.

### 1.6 Quantum Access (Pilot)
- 2026'da pilot çağrı açıldı (EuroHPC kuantum bilgisayarları). GPU işi değil; kullanıcı kuantum sorarsa canlı bak.

---

## 2. AI Factories Erişim Modları — "AI for Industrial Innovation" (birim: GPU saati)

**Hedef kitle:** AI ile inovasyon yapan **KOBİ ve startup'lara ücretsiz**. KOBİ olmayan sanayi → pay-per-use ticari erişim. Akademi/kamu → §1.5'e yönlendirilir. Seçilen AI Factory uzman desteği de verir (veri hazırlama, eğitim, teknik danışmanlık).
Kota: Industrial Innovation toplamda EuroHPC payının %30'una kadar; Playground+Fast Lane birlikte ≤%10.

### 2.1 Playground
- **Kim:** Yeni/giriş seviyesi kullanıcı, küçük ihtiyaç.
- **Tahsis:** Sistem başına sabit küçük paket (snapshot: ~5.000 GPU saati), 1-3 ay, **tek sistem**.
- **Süreç:** Sürekli açık, **yarışmasız FIFO**; kısa şablon başvuru; uygunluk + teknik kontrol; **2 iş gününde erişim**.

### 2.2 Fast Lane
- **Kim:** HPC'ye aşina kullanıcı, orta ölçek.
- **Tahsis:** **10.000–50.000 GPU saati**, 1-3 ay, tek sistem.
- **Süreç:** Sürekli açık, FIFO, **4 iş gününde erişim**. (Not: Oca 2026'da platform geçişi sırasında sayfa "temporarily closed" göründü; başvurular access.eurohpc-ju.europa.eu üzerinden sürdü — güncel portal durumunu mutlaka canlı kontrol et.)

### 2.3 Large Scale
- **Kim:** Yüksek etki/yüksek kazanımlı büyük AI işleri (foundation model eğitimi tipik örnek).
- **Tahsis:** **50.000–2.400.000 GPU saati**, süre 3/6/12 ay.
- **Takvim:** Sürekli açık, **ayda 2 cut-off** (yıl boyu, ör. 14 Ağu / 31 Ağu / 15 Eyl 2026...). Teknik + hakem değerlendirmesini geçerse **cut-off'tan 10 iş günü içinde erişim**.
- **Emsal:** Newmind AI (TR) MareNostrum 5'te ~100k GPU saati aldı; sonrasında Mecellem platformu için 1,55M GPU saatlik tahsis duyurdu (bkz. `turkiye.md`).

**Partisyon uyarısı:** Talep anında bazı partisyonlar dolu olabilir; formda görünmeyen partisyon yerine erişilebilir olanı seçmek gerekir. Başvuru öncesi hedef sistemin o turdaki mevcudiyetini kontrol et.

---

## 3. AI Gigafactories (AIGF) — altyapı ihalesi, son kullanıcı hibesi DEĞİL

- **Ne:** InvestAI (€200 milyar hedefli girişim; €20 milyar AIGF fonu) kapsamında, her biri ~100.000 son teknoloji AI çipli, 7'ye kadar dev tesis. AI Factory (~25k çip) ölçeğinin 4 katı.
- **Durum (snapshot):** İhale çağrısı **30 Temmuz 2026'da açıldı**, teklif son tarihi **12 Kasım 2026**, seçim 2027 başı, faaliyete geçiş seçimden itibaren 18 ay. Öncesinde gayriresmî ilgi çağrısına 16 üye ülkeden 60 sahada 76-77 teklif gelmişti. AB, CAPEX'in %17'sini koyar; ~%65-70 özel yatırım beklenir. EIB ortak.
- **Kim başvurur:** Konsorsiyum/SPV (şirketler + kamu + yatırımcı). Tesis tek ülkede veya sınır ötesi dağıtık olabilir.
- **Son kullanıcıya anlamı:** JU + Katılımcı Devletler "çapa müşteri" olarak compute süresi satın alacak → ileride kullanıcılara erişim çağrılarıyla dağıtılması beklenir. Kullanıcı "gigafactory'den GPU alabilir miyim" derse: bugün değil, erişim modeli netleşince; takipte kal.

---

## 4. Yarışmalar (nakit + compute birlikte)

### Large AI Grand Challenge (emsal, 2023-24)
- AI-BOOST (Horizon projesi) + Komisyon + EuroHPC ortaklığı. 94 başvuru → 4 kazanan (Lingua Custodia FR, Unbabel PT, Tilde LV, Textgain BE): toplam **€1M + 8M GPU saati** (LUMI + Leonardo; MN5'e ek süre). Koşul: 12 ay sonunda modeli açık kaynak (ticari olmayan) yayınlamak veya bulguları yayımlamak.
- **Aksiyon:** AI-BOOST ve GenAI4EU sayfalarından **açık yeni edisyon/yarışma var mı** canlı tara; bu tür ödüller dönemseldir ve duyuruyla açılır.

---

## 5. Nakit Hibe Programları (compute değil para; EuroHPC ile birleştirilebilir)

| Program | Ne verir | Kim | Not (snapshot Ağu 2026) |
|---|---|---|---|
| **EIC Accelerator** | ≤€2,5M hibe (%70) + ≤€10M equity | Tek KOBİ/startup | 2026 bütçesi €634M; kalan cut-off'lar 2 Eyl ve 4 Kas 2026; 2026'da ayrı AI Challenge yok → Open kanalı |
| **EIC Transition** | ≤€2,5M (%100) | Doğrulanmış teknolojiyi pazara olgunlaştırma | AI için sık ihmal edilen sessiz kanal |
| **EIC Pathfinder** | Konsorsiyum araştırma hibesi | Uçuk/öncü AI araştırması | 2026 son tarihleri Eki civarı — canlı bak |
| **STEP Scale-Up** | ≤€30M yatırım | Series A sonrası deep-tech scale-up | 2026: €300M; stratejik bağımlılık azaltma odağı |
| **Digital Europe (DEP)** | Proje başına ~€1M–17,5M; %50 (KOBİ'de %75'e kadar) | Genelde konsorsiyum; **deploy/uptake** odaklı | GenAI4EU şemsiyesi; OpenEuroLLM DEP fonlu; DIGITAL-2026-AI-09 Mar 2026'da kapandı — yeni AI çağrılarını Funding & Tenders'tan izle |
| **Horizon Europe CL4** | RIA/IA konsorsiyum hibeleri | Araştırma ağırlıklı | 2026-27 WP'de "Challenge-Driven GenAI4EU Booster", Apply AI robotik vb. konular; RAISE (AI in science) ek ~€90-107M |
| **Ulusal (TR)** | TÜBİTAK destekleri, EuroHPC JU R&I çağrılarına ulusal eş-finansman kuralları | TR kuruluşları | `turkiye.md` |

Kombinasyon serbestisi: Aynı şirket EuroHPC compute + EIC Accelerator + EDIH hizmetleri + cascade funding'i bir arada kullanabilir (çifte finansman yasağına dikkat: aynı maliyet kalemi iki kez fonlanamaz). RRF/ulusal toparlanma fonları kapandı (kilometre taşı son tarihi 31 Ağu 2026) — RRF vaat eden danışmanlara karşı uyar.

---

## 6. Kesişen Kurallar

- **Ülke uygunluğu (2020 sonrası alınan sistemler):** AB üyesi VEYA EuroHPC Katılımcı Devleti VEYA DEP ya da Horizon Europe'a asosiye üçüncü ülke. **Türkiye üçünü de sağlar** (bkz. `turkiye.md`).
- **PI koşulu:** PI'ın iş sözleşmesi, tahsis bitiminden en az 3 ay sonrasına kadar geçerli olmalı.
- **Açıklık:** Ücretsiz erişim esasen açık Ar-Ge içindir (Open Science: sonuçlar açık erişim). Kapalı ticari Ar-Ge → pay-per-use. Industry track'lerde koşullar Terms of Reference'ta — başvuru öncesi mutlaka oku.
- **Yükümlülükler:** Yayınlarda kaynak kullanımını acknowledge etmek, yaygınlaştırma etkinliklerine katkı, tahsis bitiminde final raporu. Bazı ödüllerde açık kaynak yayın şartı.
- **Değerlendirme iskeleti:** İdari uygunluk → teknik değerlendirme (kod hazırlığı, ölçeklenebilirlik, kaynak gerekçesi) → (büyük modlarda) bilimsel hakem paneli. Peer review'u EuroHPC JU Peer-Review Office yürütür (PRACE mirası).

---

## 7. Resmi URL Dizini (canlı doğrulama noktaları)

| Ne | URL |
|---|---|
| Tüm erişim çağrıları + 2026 cut-off takvimi | eurohpc-ju.europa.eu/supercomputers/supercomputers-access-calls_en |
| Erişim politikası + SSS | eurohpc-ju.europa.eu/supercomputers/supercomputers-access-policy-and-faq_en |
| AI Factories erişim modları | eurohpc-ju.europa.eu/ai-factories/ai-factories-access-modes_en |
| AI Factories çağrıları + SSS + Helpdesk | eurohpc-ju.europa.eu/ai-factories/ai-factories-access-calls_en |
| **Başvuru portalı** (snapshot) | access.eurohpc-ju.europa.eu |
| Yeni tek kapı: EuroHPC Federation Platform (MyEuroHPC) | eurohpc-ju.europa.eu/supercomputers/eurohpc-federation-platform_en — ilk sürüm 15 Nis 2026; hangi işlemlerin EFP'ye taşındığını canlı kontrol et |
| AI Gigafactories | eurohpc-ju.europa.eu/ai-gigafactories_en |
| Kazanan projeler (emsal taraması) | eurohpc-ju.europa.eu/supercomputers/awarded-projects_en |
| Nakit hibeler tek portal | ec.europa.eu/info/funding-tenders (Funding & Tenders Portal) |
| GenAI4EU | digital-strategy.ec.europa.eu/en/policies/genai4eu |
| AI-BOOST yarışmaları | aiboost-project.eu |
| EPICURE (L2/L3 uygulama desteği) | epicure-hpc.eu |
| Türkiye kanalları | `turkiye.md` içinde |
