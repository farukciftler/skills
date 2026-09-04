# Başvuru Rehberi — Portallar, Proposal, Boyutlandırma, Ret Stratejisi

> **SNAPSHOT: Ağustos 2026.** Şablonlar ve form alanları çağrıdan çağrıya değişir; her modun sayfasındaki "Documents" bölümünden güncel Terms of Reference (ToR) + şablonu indirip esas al.

## 1. Portallar ve Süreç Mekaniği

- **EuroHPC erişim başvuruları:** access.eurohpc-ju.europa.eu (snapshot'ta esas kapı). Oca 2026 civarında platform geçişi yaşandı; **EuroHPC Federation Platform / MyEuroHPC** (ilk sürüm 15 Nis 2026, CSC liderliğinde, MyAccessID/eduGAIN kimlik) kademeli olarak tek kapı oluyor. Başvuru öncesi hangi portalın geçerli olduğunu çağrı sayfasından teyit et.
- **Nakit hibeler (EIC/DEP/Horizon):** EU Funding & Tenders Portal — kuruluşun PIC numarası gerekir (yoksa önce kayıt).
- **Süreç (EuroHPC):** Gönderim → idari uygunluk → teknik değerlendirme → (Regular/Extreme/Large Scale/AI for Science'ta) hakem paneli → tahsis kararı → hosting entity ile kullanıcı sözleşmesi → hesap açılışı.
- **Saat kuralı:** Cut-off günü **10:00 CET/CEST** — son geceye bırakılmaz.
- **Kimlik/kurum:** PI + ekip üyeleri; PI sözleşmesi tahsis bitiminden ≥3 ay sonrasına geçerli. Kurum bilgileri (KOBİ beyanı dahil) doğru olmalı — KOBİ statüsü AI Factories ücretsizliğinin kilididir.

## 2. Proposal İskeletleri (mod bazlı)

### 2.1 Playground / Fast Lane (kısa form, FIFO)
Değerlendirme yarışmasız; amaç "uygun + teknik olarak çalıştırabilir" görünmek. 1-2 sayfa:
1. Şirket ve KOBİ statüsü (çalışan/ciro), AI faaliyetinin tanımı
2. Yapılacak iş: model/iş yükü, framework (PyTorch/JAX...), veri hacmi ve kaynağı
3. Kaynak talebi: sistem + partisyon, GPU saati, süre (1/2/3 ay), depolama
4. Teknik hazırlık: konteyner/ortam, daha önce çalıştırıldığı ortam, ölçekleme planı
5. Beklenen çıktı ve inovasyon değeri (kısa)

### 2.2 Large Scale (hakemli — asıl savaş alanı)
1. **Excellence/Innovation:** Problemin önemi, state-of-the-art'a göre fark, yüksek etki/yüksek kazanım iddiası (bu ifade ToR dilidir — karşıla)
2. **Teknik olgunluk:** Kodun kanıtlanmış ölçeklenebilirliği (benchmark verisi, ideal olarak Playground/Fast Lane veya Benchmark Access çıktısı), dağıtık eğitim stratejisi (FSDP/DeepSpeed/Megatron vb.), checkpoint/yeniden başlatma planı
3. **Kaynak gerekçesi:** §4'teki matematikle hesap tablosu — hakemin ilk baktığı yer. "Ne kadar GPU saati, neden, hangi dağılımla (deneme/ana eğitim/değerlendirme)"
4. **Veri yönetimi:** Veri hakları, GDPR, transfer planı, depolama ihtiyacı
5. **İş planı bağlantısı:** Sonucun ürünleşme yolu (Industrial Innovation'ın varlık sebebi)
6. **Ekip:** HPC/dağıtık eğitim deneyimi; yoksa AI Factory desteğinin nasıl kullanılacağı
7. **Zaman çizelgesi:** Ay bazında milestone'lar; süre seçimi (3/6/12) buna oturmalı

### 2.3 AI for Science / Regular / Extreme Scale (bilimsel hakemli)
Yukarıdakine ek: bilimsel arka plan + hipotez, yöntem, beklenen bilimsel etki, yayın planı, açık bilim uyumu, önceki tahsislerin çıktıları. Extreme Scale'de "neden bu iş ancak bu ölçekte yapılabilir" sorusuna açık cevap şart.

### 2.4 Nakit hibeler (EIC/DEP/Horizon)
Bu skill iskelet kurar ama tam proposal ayrı disiplindir: EIC (excellence/impact/implementation + pitch), DEP (deployment + uptake metrikleri; araştırma değil), Horizon (RIA/IA şablonu, konsorsiyum). DEP'te kullanıcı "hâlâ araştırıyorsa" Horizon'a yönlendir; çalışan ürünü + gerçek deploy sahası varsa DEP.

## 3. Değerlendirmede Elenme Sebepleri (hakem gözü)

1. Kaynak talebi gerekçesiz ("10M GPU saati istiyoruz" — hesap yok)
2. Ölçeklenebilirlik kanıtı yok (tek GPU'da çalışan kodla 512 GPU istemek)
3. Yanlış mod (akademisyen Industrial Innovation'a, kapalı ticari iş ücretsiz moda başvurmuş)
4. KOBİ statüsü belgesiz/şüpheli
5. Veri hakları belirsiz (lisanssız scrape edilmiş veri seti)
6. Etik/AI Act uyumu hiç anılmamış (üretken AI projelerinde etik AI vurgusu ToR dili)
7. Sürdürme planı yok (tahsis bitince ne olacak)

## 4. Boyutlandırma Matematiği (GPU saati hesabı)

**Eğitim FLOPs ≈ 6 × N × D** (N = parametre sayısı, D = eğitim token'ı).
**GPU saati = FLOPs ÷ (GPU tepe FLOPS × MFU) ÷ 3600.**
MFU (Model FLOPs Utilization) varsayımı: iyi ayarlı büyük eğitimde %35-45; güvenli plan %30-40. Tepe değerler (BF16, yoğun): H100 ≈ 989 TFLOPS · A100 ≈ 312 TFLOPS · MI250X ≈ 383 TFLOPS (GCD başına ~191,5) · GH200 ≈ H100 sınıfı.

**Örnek — 7B model, 2T token, H100, MFU %40:**
FLOPs = 6 × 7e9 × 2e12 = 8,4e22 → 8,4e22 ÷ (989e12 × 0,4) ÷ 3600 ≈ **59.000 H100 saati** → +%15-20 deneme/ablation/başarısız koşu payı ≈ **68-71k GPU saati** → Large Scale bandı. MN5 ACC'de (4 H100/node) ≈ ~17-18k node saati.

**Fine-tune/LoRA:** Tam eğitimin kabaca %1-10'u; 6·N·D'yi eğitilen token sayısıyla kur, LoRA'da geri yayılım maliyeti düşer ama aktivasyon maliyeti kalır — pratik kestirim: full FT ≈ aynı formül; LoRA ≈ ×0,3-0,5.
**Inference/değerlendirme:** ≈ 2 × N × D_out; toplam bütçenin ayrı satırı olarak yaz.
**Sunum kuralı:** Hesabı tabloyla ver (aşama × GPU saati), varsayımları (MFU, tepe FLOPS, pay) açıkça listele, hedef sistemin node saatine çevir. Talebi çağrının min-max bandına oturt: bandın altındaysa bir küçük moda in, üstündeyse aşamalara böl.

## 5. Tahsis Sonrası Yükümlülükler

- Yayın/duyurularda acknowledgment (hosting entity'nin verdiği kalıpla; örnek kalıp: "This work was supported by the EuroHPC JU through project <kod> with access to <sistem> hosted by <merkez>")
- Final raporu (ve uzun modlarda ara rapor — uzatma ara rapor onayına bağlı)
- Yaygınlaştırma etkinliklerine katkı; bazı ödüllerde açık kaynak model yayını şartı
- Uzatma: tipik +3 ay/+%10, tek sefer, gerekçeli talep; 3. aydan sonra yeni uzatma kabul edilmez (Access Policy)
- Kullanım disiplini: tahsisin ciddi altında kalmak (ör. <%30) sonraki başvurularda aleyhe delildir — burn-rate'i izle, gerekirse erken uyarıyla plan revize et

## 6. Ret ve Yeniden Başvuru Stratejisi

1. **Hakem yorumlarını sınıflandır:** teknik olgunluk / kaynak gerekçesi / kapsam-mod uyumu / etki anlatısı. Her maddeye yazılı cevap hazırlanıp revize proposal'a işlenir.
2. **Merdiven kur:** Benchmark (ölçekleme kanıtı) → Development (kod olgunlaştırma) → Regular/Large Scale. Bu zincir hakem nezdinde en güçlü anlatıdır.
3. **Mod düşür:** Large Scale reddi → Fast Lane ile başla, gerçek kullanım verisiyle 2-3 ay sonra tekrar Large Scale.
4. **Cut-off avantajı:** Large Scale ayda 2, AI for Science 2 ayda 1 tur — revizyon hızlıysa bekleme maliyeti düşük.
5. **Sistem değiştir:** Partisyon doluluğu retlerin sessiz sebebi olabilir; alternatif sistem/partisyonla yeniden dene.
6. **Destek çağır:** AI Factories Helpdesk + EuroCC ulusal yetkinlik merkezi (TR için `turkiye.md`) başvuru öncesi danışmanlık verir — ücretsiz, az bilinir, kullan.

## 7. Danışmanlık Modu Kontrol Listesi (müşteri adına çalışırken)

1. Müşteri keşfi: tüzel yapı, ülke, KOBİ statüsü belgeleri, iş yükü, IP hassasiyeti (açık bilim şartını kaldırabilir mi?)
2. Uygunluk taraması → rota raporu (ana+yedek, takvim, yükümlülük tablosu)
3. Boyutlandırma hesabı (müşteri verisiyle, varsayımlar yazılı)
4. Proposal üretimi (EN) + iç onay süreci için TR özet
5. Gönderim provası: portal hesabı, PIC/kurum kayıtları, ekler
6. Başvuru sonrası: sonuç takibi, hesap açılışı, kullanım/burn-rate takibi, rapor takvimi
7. Beklenti yönetimi: FIFO modlarda gün, hakemli modlarda hafta-ay ölçeği; hiçbir mod "garanti" değil — yazılı taahhütte başarı garantisi verme
