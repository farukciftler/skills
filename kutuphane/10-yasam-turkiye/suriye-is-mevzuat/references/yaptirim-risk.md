# Yaptırımlar, Uyum (Compliance) ve Risk Yönetimi

Son güncelleme: 28 Ağustos 2026. Yaptırım mimarisi 2025-2026'da katman katman söküldü ama **sıfırlanmadı**: liste bazlı yaptırımlar, FATF gri listesi ve bankaların temkinli uyum kültürü sürüyor. "Yaptırımlar kalktı mı?" sorusuna asla tek cümlelik evet/hayır verme — aşağıdaki zaman çizelgesini güncelleyip katmanlı cevap ver.

## Yaptırım zaman çizelgesi (ABD odaklı — doğrulanmış çıpalar)

| Tarih | Gelişme |
|---|---|
| Oca 2025 | OFAC Genel Lisans 24 (ilk gevşeme) |
| May 2025 | GL 25 + Caesar yaptırımlarının 180 gün askıya alınması; Riyad'da Trump'ın "tüm yaptırımları kaldırma" açıklaması (13 May) |
| 29 May 2025 | **AB** çoğu sektörel yaptırımı kaldırdı (UK benzer çizgide) |
| 30 Haz 2025 | **EO 14312**: ABD Suriye Yaptırım Programı feshedildi (1 Tem yürürlük); ~518 kişi/kuruluş SDN'den çıkarıldı |
| 10 Kas 2025 | Caesar askıya alma yenilendi — **Rusya/İran bağlantılı işlemler hariç** |
| 18 Ara 2025 | **FY2026 NDAA ile Caesar Act tamamen ve koşulsuz yürürlükten kalktı** (4 yıl boyunca 180 günde bir başkanlık raporu şartıyla) |
| 24 Ağu 2026 | ABD Dışişleri **State Sponsor of Terrorism (SST) tanımını kaldırdı**; HTS'nin FTO/SDGT listelemeleri daha önce kaldırılmıştı |

## Ne kaldı? (her cevapta güncelle)

- **Liste bazlı (SDN) yaptırımlar:** Esad ve çevresi, insan hakları ihlalcileri, Captagon ticareti, IŞİD/El Kaide bağlantılı kişiler. → Ortak, müşteri, tedarikçi, bina sahibi seçerken **tarama şart**.
- **Rusya/İran bağlantısı:** Rusya veya İran menşeli mal/teknoloji/finansman içeren işlemler hassasiyetini koruyor.
- **İhracat kontrolleri:** SST kalkışıyla dual-use rejimi yumuşuyor olabilir — ileri teknoloji/şifreleme donanımı ihracında güncel BIS/EAR durumunu doğrula (yazılım/SaaS için genelde sorun değil ama sunucu/ağ donanımı götürürken bak).
- **FATF gri listesi:** Suriye gri listede (çıkış süreci izleniyor — DOĞRULA) → tüm bankalar gelişmiş inceleme (EDD) uygular; transferlerde belge iste-me normaldir, buna hazırlıklı evrak seti kur.
- **AB/UK kalıntıları:** kişi bazlı listeler ve silah ambargosu çizgisi sürer — AB pazarıyla da çalışan yapılar için ayrıca tara.

## Asgari uyum protokolü (her iş ilişkisi için öner)

1. **Taraf taraması:** ortak/müşteri/tedarikçi + gerçek faydalanıcıları (UBO) → OFAC SDN, AB, UK, BM listeleri (sanctionssearch.ofac.treas.gov + opensanctions.org gibi ücretsiz araçlar; kritik işlemde profesyonel tarama servisi öner).
2. **Rusya/İran bağı sorgusu:** sermaye, ekipman, yazılım lisansı zincirinde Rusya/İran menşei var mı.
3. **Belge disiplini:** her transferin sözleşme + fatura + banka dekont zinciri; TR bankası uyum sorularına hazır dosya.
4. **Devletle iş:** kamu ihalesi/devlet ortaklığı içeren işlerde karşı tarafın kurumsal kimliğini ve imza yetkisini doğrulat (geçiş dönemi kurumsal belirsizliği).
5. **Periyodik tekrar:** listeler ve kurallar oynak; ilişki başına en az yılda bir yeniden tarama.

## Uyuşmazlık çözümü

- **Yerel mahkemeler:** yeniden yapılanma hâlinde; ticari dava öngörülebilirliği düşük — sözleşmede mahkeme yerine tahkim tercih et.
- **Tahkim:** Suriye **New York Konvansiyonu** tarafı (1959'dan) → yabancı hakem kararı tenfizi hukuken mümkün (fiilî tenfiz pratiğini doğrula). ICSID üyeliği ve YKTK dayanaklı yatırım tahkimi seçeneklerini doğrula.
- **KHK 114/2025 koruması:** SIA lisanslı yatırımlarda tahkim erişimi + ihtiyati haciz yasağı + 6 ay düzeltme hakkı — büyük yatırımda SIA rotasının en güçlü gerekçesi.
- **Sözleşme pratiği:** uygulanacak hukuk + tahkim yeri (ör. İstanbul ISTAC / DIFC-LCIA benzeri) + dil + kur maddesi; Arapça-İngilizce çift dilli metin.

## Operasyonel/politik risk haritası (rapora göm)

- **Bölgesel kontrol farkları:** Şam-Halep hattı merkezî idare; kuzeydoğu (SDF), Süveyda, sahil şeridi dönemsel gerginlik — fiziksel varlık planında güncel güvenlik durumunu (seyahat uyarıları: TR Dışişleri, UK FCDO, US State) çek.
- **Kurumsal akışkanlık:** bakanlıklar birleşiyor/yeniden adlanıyor; bugün geçerli prosedür yarın değişebilir → her resmî işlemde "bu hafta geçerli usul"ü yerel avukatla teyit ettir.
- **Güç yoğunlaşması:** SIA + Yüksek Konsey cumhurbaşkanlığına bağlı; büyük projelerde siyasi ilişki riski/gerekliliği (MEI, 2026) — raporda açıkça adlandır.
- **Makro:** enflasyon, SYP oynaklığı, CBS rezerv zayıflığı (~200M USD, 2025 sonu) → sözleşmeleri USD'ye endeksle, SYP pozisyonu taşıma.
- **Altyapı:** elektrik kesintileri, internet dalgalanması → SLA taahhütlerini buna göre yaz.
- **Sigorta:** siyasi risk sigortası (MIGA benzeri, İslami tekafül, TR Eximbank'ın Suriye kapsamı) seçeneklerini büyük yatırımda araştır.
- **Çıkış planı:** sermaye repatriasyonu garantisi (SIA lisansıyla) + banka kanalı; her yapı önerisinde "nasıl çıkarım" bölümü ekle.

## Hazır doğrulama sorguları

- "OFAC Syria sanctions FAQ [yıl]" · "state.gov Syria sanctions advisory [yıl]"
- "Syria SDN remaining designations" · "EU Syria sanctions [yıl]"
- "FATF grey list Syria [yıl]" · "Syria FATF removal"
- "Syria export controls EAR dual use [yıl]"
- "Syria travel advisory [ülke] [yıl]" · "Suriye seyahat uyarısı Dışişleri"
- "Syria ICSID membership" · "Syria New York Convention enforcement"
