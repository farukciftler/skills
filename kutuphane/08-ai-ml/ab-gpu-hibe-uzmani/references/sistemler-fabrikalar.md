# Sistemler ve AI Factory Ağı

> **SNAPSHOT: Ağustos 2026.** Sistem/partisyon mevcudiyeti çağrı turuna göre değişir; kurulum halindeki sistemlerin devreye girişi kayabilir. Sistem önerirken o çağrının sayfasındaki güncel sistem tablosunu canlı kontrol et.

## 1. Faal EuroHPC Süperbilgisayarları

| Sistem | Ülke / İşletici | Sınıf | GPU/hızlandırıcı (AI için önemli kısım) | Not |
|---|---|---|---|---|
| **JUPITER** | Almanya / JSC Jülich | **Exascale** (Avrupa'nın ilk exascale'i; Kas 2025 Top500'de dünya 4.) | Booster: ~24.000 NVIDIA **GH200** Grace-Hopper | JAIF AI Factory'nin çekirdeği. Bazı çağrı turlarında Booster kapalı olabilir — kontrol et |
| **LUMI** | Finlandiya / CSC (konsorsiyum) | Pre-exascale (Top500 ~9.) | LUMI-G: ~2.978 node × 4× AMD **MI250X** | AI Factory: LUMI AIF. AMD/ROCm yığını — CUDA bağımlı kod için uyum notu düş |
| **Leonardo** | İtalya / CINECA | Pre-exascale (Top500 ~10.) | Booster: ~3.456 node × 4× NVIDIA **A100** custom | IT4LIA AIF. LISA genişlemesi yolda |
| **MareNostrum 5** | İspanya / BSC | Pre-exascale | ACC: ~4× **H100** per node; AI upgrade sözleşmesi Oca 2026'da imzalandı (~€129M; LLM eğitim + uygulama/inference için 2 yeni partisyon; FSAS Technologies + Telefónica) | **Türkiye MN5 konsorsiyum ortağı** (İspanya+Portekiz+Türkiye). BSC AIF çekirdeği |
| **MeluXina** | Lüksemburg / LuxProvide | Petascale | A100 GPU partisyonu + FPGA | L-AI Factory (MeluXina-AI) |
| **Karolina** | Çekya / IT4Innovations | Petascale | A100 GPU partisyonu | Çekya AIF (3. dalga) |
| **Vega** | Slovenya / IZUM | Petascale | A100 GPU partisyonu | SLAIF bağlantılı |
| **Discoverer** | Bulgaristan / Sofia Tech Park | Petascale | Ağırlıklı CPU; Discoverer+ GPU genişlemesi | BRAIN++ AIF |
| **Deucalion** | Portekiz / MACC | Petascale | ARM + x86 + GPU bölümleri | |

## 2. Yolda Olan Önemli Sistemler (snapshot)

- **Alice Recoque** (Fransa, GENCI/CEA) — Avrupa'nın 2. exascale'i; AI Factory France ile bağlı.
- **DAEDALUS** (Yunanistan, GRNET) — Pharos AIF'in sistemi.
- **Arrhenius** (İsveç, Linköping) — MIMER AIF ile ilişkili.
- **MN5 AI genişlemesi**, **LUMI-AI**, **JUPITER AIF platformları** ve 3. dalga AIF'lerin yeni AI-optimize makineleri: toplamda **≥9 yeni AI-optimize süperbilgisayar** tedarik ediliyor; mevcut EuroHPC AI kapasitesini 3 kattan fazla artıracak.

## 3. AI Factory Ağı — 19 Fabrika (16 üye ülke + 2 katılımcı devlet ortaklıklarıyla)

**1. dalga (Ara 2024, 7):**
| AIF | Ülke / Merkez | Sistem | Sektör vurgusu |
|---|---|---|---|
| LUMI AIF | Finlandiya / CSC, Kajaani | LUMI (+LUMI-AI) | Genel + imalat; Nordik ağı |
| HammerHAI | Almanya / HLRS Stuttgart | Hunter/yeni AI sistemi | Mühendislik + imalat (otomotiv) |
| IT4LIA | İtalya / CINECA Bologna | Leonardo (+LISA) | Agri-food, siber, imalat |
| L-AI (MeluXina-AI) | Lüksemburg / LuxProvide | MeluXina-AI | Finans, uzay, yeşil ekonomi |
| BSC AIF | İspanya / BSC Barcelona | MareNostrum 5 (+AI upgrade) | Sağlık, iklim, finans, hukuk, kamu. **Ortaklar: BSC + FCT (PT) + TÜBİTAK (TR) + ICI (RO)** |
| Pharos | Yunanistan / GRNET | DAEDALUS | Sağlık, kültür/dil, sürdürülebilirlik |
| MIMER | İsveç / Linköping | Arrhenius | Tıp, malzeme, otonom sistemler, oyun |

**2. dalga (Mar 2025, 6):** AI:AT (Avusturya) · BRAIN++ (Bulgaristan) · **AI Factory France** (GENCI — Alice Recoque) · **JAIF** (Almanya, Jülich — JUPITER) · **PIAST** (Polonya, PSNC Poznań) · SLAIF (Slovenya, Maribor). Toplam yatırım ~€485M.

**3. dalga (Eki 2025, 6):** Çekya (IT4I) · Litvanya · Hollanda · Romanya · İspanya-Galiçya (**1HealthAI** — sağlık/One Health odaklı) · Polonya (2.).

## 4. AI Factory Antennas — 13 Antenna (Eki 2025 seçimi, ~€55M AB fonu)

Kendi fabrikası olmayan ülkelere uzaktan erişim + destek köprüsü. **Üye ülkeler:** Belçika (BE-AI → LUMI+JAIF) · Kıbrıs (Pharos-CY → Pharos/DAEDALUS) · Macaristan (HunAIFA) · İrlanda · Letonya · Malta (CALYPSO → Pharos) · Slovakya. **Ortak ülkeler:** İzlanda · Moldova (FAIMA) · İsviçre · Birleşik Krallık · Kuzey Makedonya · Sırbistan.
- **Türkiye'nin Antenna'sı YOK** — ama gerek de düşük: Türkiye MN5 ortağı ve TÜBİTAK BSC AIF konsorsiyumunda (bkz. `turkiye.md`). Yeni antenna turu açılırsa canlı takip et.
- MoU'lar 2026 ortasına kadar imzalanıyor; antenna hizmetlerinin fiilen açılıp açılmadığını ülke bazında doğrula.

## 5. Sistem Seçim Notları

- **CUDA bağımlılığı:** LUMI (AMD MI250X/ROCm) için PyTorch ROCm build'i gerekir; saf CUDA çekirdekli kod Leonardo/MN5/JUPITER'e (NVIDIA) daha uygun.
- **Node → GPU saati çevrimi (yaygın kabuller):** LUMI-G 1 node saati = 4 MI250X (=8 GCD) saati; Leonardo Booster 1 node = 4 A100 saati; MN5 ACC 1 node = 4 H100 saati. Çağrı ToR'unda farklı sayım varsa ToR esas alınır.
- **Depolama/veri:** Büyük tahsislerde depolama (TB-saat) ayrıca talep edilir; veri taşıma planını (giriş/çıkış, GDPR) proposal'a yaz.
- **Destek katmanları:** L1 → sistemin kendi destek ekibi; L2/L3 (porting, ölçekleme, performans, refactoring) → **EPICURE**. AI Factory modlarında fabrikanın uzman desteği pakete dahil.
