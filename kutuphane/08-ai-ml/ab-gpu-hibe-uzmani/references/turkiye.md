# Türkiye — Uygunluk Zemini, Kanallar, Emsaller

> **SNAPSHOT: Ağustos 2026.** Asosiyasyon durumları ve ulusal kurallar değişebilir; çağrı bazında "eligible countries" listesini mutlaka canlı doğrula.

## 1. Uygunluk Zemini (üç ayak — Türkiye üçünü de sağlar)

1. **EuroHPC JU Katılımcı Devleti:** Türkiye, JU'nun üyesi (TÜBİTAK temsilci). 2020 sonrası alınan tüm EuroHPC sistemlerinde Birlik payı erişimine uygunluk için tek başına yeterli.
2. **Digital Europe Programme asosiyasyonu:** Anlaşma 2023'te imzalandı, 1 Oca 2023'ten geçerli; **tam asosiye — İSTİSNA: Specific Objective 3 (Siber Güvenlik ve Güven) hariç.** Türk kuruluşları DEP AI/HPC/beceri çağrılarına başvurabilir, Türkiye'de EDIH kurulabilir.
   - **Dikkat:** Bazı DEP konuları "stratejik otonomi/güvenlik" gerekçesiyle katılımı AB üyeleriyle sınırlar. Uygunluk her çağrının kendi şartnamesinden teyit edilir — "Türkiye DEP'e asosiye" cümlesi tek başına yetmez.
3. **Horizon Europe asosiyasyonu:** Türkiye asosiye ülke → Horizon çağrıları, EIC Accelerator (hibe bileşeni dahil) ve EuroHPC JU R&I çağrıları açık. TÜBİTAK, EuroHPC JU R&I çağrıları için **ulusal başvuru kuralları + eş-finansman** dokümanları yayımlar (tubitak.gov.tr'de çağrı bazlı PDF'ler) — R&I hattında ulusal kural setini mutlaka indir.

**Pratik sonuç:** İstanbul'daki bir AI startup'ı, İspanya'daki bir startup'la aynı statüde AI Factories Playground/Fast Lane/Large Scale'e başvurabilir.

## 2. Türkiye'nin Yapısal Kartları

- **MareNostrum 5 konsorsiyum ortaklığı:** MN5'in alım ve işletmesi İspanya + Portekiz + **Türkiye** eş-finansmanıyla; ~€129M'lik AI upgrade'i de (DEP fonlu) aynı üçlü + Romanya çerçevesinde. Türkiye'nin "kendi parası olan" sistem MN5'tir.
- **BSC AI Factory ortağı TÜBİTAK:** BSC AIF konsorsiyumu = BSC + FCT (PT) + **TÜBİTAK (TR)** + ICI (RO). Türk başvurucular için doğal ev sahibi fabrika: **BSC AIF / MareNostrum 5.** Sektör vurguları: sağlık, iklim/tarım, finans, hukuk, enerji, medya, kamu.
- **Antenna yok:** 13 Antenna listesinde Türkiye bulunmuyor (MN5 ortaklığı zaten daha güçlü bir konum). Yeni antenna/genişleme turu açılırsa izle.

## 3. Ulusal Kanallar

| Kanal | Ne işe yarar | Erişim |
|---|---|---|
| **TRUBA** (TÜBİTAK ULAKBİM Yüksek Başarımlı Hesaplama) | Ulusal HPC/GPU + depolama; prototip, ön deney, EuroHPC öncesi ölçekleme kanıtı üretme yeri | portal.truba.gov.tr üyelik; akademi ağırlıklı, kamu/özel için truba@ulakbim.gov.tr |
| **EuroCC@Turkey (NCC)** | EuroHPC Ulusal Yetkinlik Merkezi — ULAKBİM koordinasyonunda ODTÜ + Sabancı; eğitim, başvuru danışmanlığı, sanayi-akademi köprüsü. **Başvuru öncesi ücretsiz akıl hocası — kullan** | ncc@ulakbim.gov.tr · eurocc.truba.gov.tr |
| **TÜBİTAK EuroHPC JU R&I ulusal kuralları** | JU'nun Ar-Ge çağrılarına (ör. kuantum, uygulama projeleri) Türk ortakların katılım/bütçe kuralları | tubitak.gov.tr çağrı sayfaları |
| **Ufuk Avrupa UKO (TÜBİTAK)** | Horizon başvurularında ulusal irtibat, seyahat/hazırlık destekleri | ufukavrupa.org.tr |

## 4. Emsaller (ikna gücü yüksek — sunumlarda kullan)

- **Newmind AI (İstanbul):** EuroHPC üzerinden MareNostrum 5'te proje **etur46** ile erişim aldı (BSC destek ekibiyle); Muhakim modeli gibi çıktılarında hem MN5 hem TRUBA acknowledgment'ı var. Ayrıca Mecellem platformu için **1,55M GPU saatlik** EuroHPC tahsisi duyurdu. → "Türk özel şirketi bu hattan geçti" kanıtı.
- **BSC/MN5 hattı genel emsal havuzu:** eurohpc-ju.europa.eu "Awarded Projects" sayfasından ülke/sistem filtresiyle Türk PI'lı projeler taranabilir — danışmanlık sunumu için güncel emsal listesi buradan çıkarılır.

## 5. Türkiye'ye Özgü Taktik Notlar

1. **Merdiven önerisi:** TRUBA'da prototip → Benchmark/Playground ile ölçekleme kanıtı → Fast Lane/Large Scale. Ölçekleme verisi olmayan başvuruya göre belirgin avantaj.
2. **Sistem tercihi:** İlk tercih MN5/BSC AIF (ortaklık + Türkçe konuşulan destek ihtimali + emsal yoğunluğu); CUDA dışı esneklik varsa LUMI kapasitesi geniş.
3. **Dil:** Başvurular İngilizce. İç karar/onay süreci için TR özet paketi hazırla (bu skill'in danışmanlık çıktı standardı).
4. **KOBİ beyanı:** AB KOBİ tanımı Türk KOSGEB tanımıyla birebir değil — çalışan sayısı/ciro/bilanço ve bağlı-ortak işletme hesabını AB tanımıyla yap.
5. **Veri/GDPR:** Türkiye'den AB sistemine veri taşınacaksa KVKK + GDPR düzlemini proposal'ın veri yönetimi bölümünde açıkça ele al; hassas veri varsa fabrikaların güvenli işleme ortamlarını sor.
6. **Döviz/bütçe yok:** EuroHPC erişimi para transferi içermez (compute aynî destektir) — vergi/teşvik muhasebesi gerektirmez; nakit hibelerde (EIC/DEP) ise TL/EUR bütçelendirme ve eş-finansman kuralları devreye girer.
