# CS / ML konferans yayıncılığı

Bilgisayar bilimlerinde birincil mecra çoğu zaman dergi değil **konferanstır** (NeurIPS, ICML, ICLR, CVPR, ACL/EMNLP, AAAI, KDD, IEEE konferansları). Kurallar dergiden ciddi biçimde farklıdır. Tarihler ve kurallar her yıl değişir — **canlı doğrula**.

## Dergiden farklar

| Konu | Dergi | Konferans |
|---|---|---|
| Takvim | Sürekli gönderim | Sabit deadline, tek tur |
| Revizyon | Birden çok tur | Genelde tek rebuttal turu |
| Sayfa | Esnek | Sert sınır (8–9 sayfa + referans + ek) |
| Şablon | Yayıncı stili | Zorunlu LaTeX stil dosyası, sapma = masa reddi |
| Anonimlik | Genelde açık | Çoğunlukla çift kör |
| Ek materyal | İsteğe bağlı | Standart ve önemli |
| Ön baskı | Serbest (genelde) | Politikaya bağlı; anonimlik dönemi kısıtı olabilir |

## Zaman planı (geriye doğru)

Abstract deadline (genelde tam metinden 1 hafta önce, kaçırılırsa gönderim hakkı yok) → tam metin → ek materyal → hakem raporları → rebuttal penceresi (genellikle çok kısa) → karar → camera-ready → sunum.

Deneyleri deadline'dan **en az 3 hafta önce** dondur; son hafta yazım, şekil ve kontrol listesi içindir.

## Yapı normu

1. Abstract — problem, boşluk, yaklaşım, ana sayısal sonuç.
2. Introduction — son paragrafta madde madde **katkılar**.
3. Related Work — konumlandırma; her rakip için "biz ne farklı yapıyoruz" cümlesi.
4. Method — anlaşılır notasyon, tek şema şekli (Figure 1 makalenin vitrini).
5. Experiments — kurulum, veri, baseline'lar, ana sonuç tablosu, ablation, analiz.
6. Limitations — çoğu mecrada zorunlu ve hakemler cezalandırmamakla yükümlü; dürüst yaz.
7. Broader Impact / Ethics — gerekiyorsa.
8. Reproducibility statement, kod linki (gönderimde anonim).

Figure 1 ve ana sonuç tablosu, hakemin ilk 3 dakikasında gördüğü şeydir; en çok emeği oraya ver.

## NeurIPS Paper Checklist (16 soru) — evrensel bir öz denetim listesi

Diğer konferanslarda muadili olmasa bile bu listeyi denetimde kullan:
1. **Claims** — abstract ve giriş, gerçek katkı ve kapsamla örtüşüyor mu?
2. **Limitations** — ayrı bölümde dürüstçe tartışıldı mı?
3. **Theory/Proofs** — tüm varsayımlar yazıldı, ispatlar tam mı?
4. **Reproducibility** — ana sonuçları tekrar üretecek kadar detay var mı?
5. **Open access** — kod/veri erişimi (zorunlu değil, teşvik ediliyor).
6. **Experimental details** — hiperparametreler, veri bölünmesi, seçim yöntemi.
7. **Statistical significance** — hata çubukları, GA, testler; neyi temsil ettikleri yazılmış mı?
8. **Compute** — GPU tipi, toplam hesaplama, maliyet.
9. **Code of Ethics** — uyum.
10–16. Broader impact, güvenlik önlemleri (yüksek riskli model/veri yayımı), varlıkların lisans ve atıfları, yeni varlıkların dokümantasyonu, insan denekler/crowdsourcing, IRB onayı, LLM'in yöntemin parçası olarak kullanımı.

Her soruya Yes/No/NA ve **gerekçe** yazılır. "No" cevabı yasak değildir; gerekçesiz "Yes" tehlikelidir.

## Veri kümesi ve model yayımlama

- Veri kalıcı bir depoda ve **kalıcı tanımlayıcıyla** (DOI vb.) yayımlanmalı.
- Makaleden veriye link (gönderimde anonim, camera-ready'de açık).
- Lisans ve erişim kısıtları makalede tarif edilir.
- Metadata standardı (Schema.org / DCAT) beklenir.
- Kapalı model kullanılıyorsa bile başkalarının sonucu doğrulamak için bir yol tarif edilmeli.

## Ön baskı (arXiv) stratejisi

- Öncelik iddiası ve görünürlük için gönderimle eş zamanlı arXiv yaygın pratiktir; **ama** çift kör mecralarda kurallar farklıdır. Tipik kısıt: gönderim penceresi çevresinde reklam yapmama, "Under review at X" ibaresi koymama.
- Doğru kategori ve iyi bir abstract, arXiv'de bulunurluğu belirler.
- Sürüm disiplini: kabul sonrası camera-ready sürümü v2 olarak yükle, DOI'yi ekle.
- arXiv üzerinden literatür taraması ve radar kurmak gerekiyorsa `arxiv-api-uzmani` skill'i devrede.

## Rebuttal

- Karakter sınırı serttir; en kritik yanlış anlamayı **ilk cümleye** koy.
- Yapı: (a) tüm hakemlere ortak yanıt, (b) hakem başına kısa maddeler.
- Yeni sonuç ekleyebiliyorsan tek kompakt tablo halinde ekle.
- Hedef kitle AC'dir; "hakem haksız" değil "şu kanıt bu itirazı çözüyor" dili kullanılır.
- Puan yükseltme talebi etme; itirazı çöz.

## IEEE özel notları

- IEEE şablonuna (IEEEtran) uyum ve sayfa/overlength ücretleri.
- YZ ile üretilmiş içerik **teşekkür bölümünde** beyan edilir: sistem adı, hangi bölümler, hangi düzeyde. Dil/gramer iyileştirmesi politikanın amacı dışında sayılır ama beyan yine tavsiye edilir.
- IEEE hakemlerin YZ araçlarıyla rapor yazmasını yasaklar.
- Konferans bildirisinin dergi sürümüne genişletilmesi kabul edilir; beyan ve yeterli yeni içerik şarttır.
- Bazı IEEE konferansları için Türkiye'deki yazarlarda sık görülen hata: bildirinin IEEE Xplore'a girip girmediğini kontrol etmemek — akademik puanlamada fark yaratır.

## TMLR / dergi alternatifi

Makale konferans döngüsüne yetişmiyorsa veya "yenilik" değil "doğruluk" ekseninde güçlüyse TMLR gibi mecralar (sürekli gönderim, kabul kriteri: iddialar kanıtlanmış ve ilgi çekici) mantıklı olabilir. Reprodüksiyon çalışmaları için MLRC/TMLR yolu ayrıca var.
