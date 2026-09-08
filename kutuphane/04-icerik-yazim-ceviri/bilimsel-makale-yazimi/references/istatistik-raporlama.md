# İstatistik ve kanıt raporlaması

Bu skill istatistik danışmanlığı yerine geçmez; analiz tasarımı tartışmalıysa biyoistatistikçiye yönlendir. Ama **raporlamanın** doğruluğu yazım işidir ve hakem itirazlarının büyük kısmı buradadır.

## Temel ilke: önce kestirim, sonra test

Raporlama sırası her başlık karşılaştırma için:
1. **Mutlak etki**, doğal birimiyle — "ortalama gecikme 70 ms azaldı", "mutlak risk farkı %4,2".
2. **Göreli etki**, yorumu kolaylaştırıyorsa — "%62 azalma".
3. **Belirsizlik** — farkın %95 güven aralığı.
4. **p değeri**, destekleyici olarak.

Bunun tersi (p ile başlayıp büyüklüğü gömme) en yaygın hatadır. Yeterince büyük örneklemde her sıfırdan farklı fark "anlamlı" çıkar.

Amerikan İstatistik Derneği'nin (ASA, 2016) altı ilkesi bu yaklaşımın dayanağıdır: p değeri verinin belirtilen modelle ne kadar uyumsuz olduğunu gösterir; hipotezin doğru olma olasılığını **vermez**; bilimsel karar tek bir eşiğe dayandırılamaz; doğru çıkarım tam ve şeffaf raporlama gerektirir; p etkinin büyüklüğünü veya önemini ölçmez; tek başına kanıtın iyi bir ölçüsü değildir.

## p değeri yazım kuralları

- Kesin değer yaz: `p = 0,03` — `p < 0,05` değil. Çok küçükse `p < 0,001`.
- Ondalık disiplini: 0,001–0,20 arası üç basamak, 0,20 üstü iki basamak (Annals of Internal Medicine konvansiyonu; birçok dergi benzer).
- `NS` (not significant) yazma.
- **"Trend" dili yasak**: "anlamlılığa yaklaşan bir eğilim (p = 0,07)" cümlesi editörlerin özellikle işaretlediği bir hatadır. Farkı ve güven aralığını yaz, yorumu okuyucuya bırak.
- Çoklu karşılaştırma yapıldıysa: düzeltme yapıldı mı, hangi yöntemle (Bonferroni, Holm, Benjamini–Hochberg/FDR) — düzeltme yapılmadıysa bunu açıkça yaz ve çıkarımın keşifsel olduğunu belirt.
- Ön tanımlı analiz ile keşifsel analiz ayrımı metinde görünür olmalı. Protokol/SAP'de tanımlanmamış analizler keşifsel etiketiyle raporlanır.

## Etki büyüklükleri

| Durum | Uygun ölçü |
|---|---|
| İki grup, sürekli çıktı | Ortalama farkı (+GA), standardize: Cohen's d / Hedges' g |
| İkili çıktı | Risk farkı, RR, OR (+GA); NNT klinik yorum için |
| Korelasyon | r veya ρ (+GA) |
| ANOVA | η², kısmi η², ω² |
| Sağkalım | HR (+GA), orantılı hazard varsayımı kontrolü |
| Sistem/ML | Doğal birimde mutlak ve göreli fark + GA; standardize ölçü tamamlayıcı |

Küçük/orta/büyük eşikleri (d = 0,2/0,5/0,8; η² = 0,01/0,06/0,14) kaba pusuladır, alanın kendi ölçeği önceliklidir.

## Tanımlayıcı istatistik

- Normal dağılan veri: ortalama ± SD. Çarpık veri: medyan (IQR). "Ortalama ± SE" tanımlayıcı tabloda kullanılmaz.
- Yüzdelerde payda mutlaka görünsün: "%23 (34/148)".
- Aşırı ondalık hassasiyet güvenilirliği düşürür: ölçüm hassasiyetini aşan basamak yazma.
- Tablo 1'de gruplar arası p değeri: randomize çalışmada anlamsız, gözlemselde çoğu dergi istemez.

## Sık yapılan hatalar (denetimde ara)

1. Kesitsel/gözlemsel veriden nedensel dil ("neden oldu", "sağladı", "etkiledi").
2. Grup içi anlamlılıktan gruplar arası fark çıkarımı — karşılaştırma **farkın kendisi** üzerinden yapılır.
3. Anlamsız sonucun "etki yok" diye yorumlanması. Geniş GA = bilgisizlik, yokluk kanıtı değil.
4. Örneklem büyüklüğü/güç analizinin hiç raporlanmaması; ya da post-hoc güç hesabı yapılması (metodolojik olarak sorunlu).
5. Kayıp verinin sessizce dışlanması (complete-case) — mekanizma ve yöntem yazılmalı.
6. Çoklu test düzeltmesinin yokluğu + alt grup avcılığı.
7. Testin varsayımlarının kontrol edildiğine dair hiçbir ifade olmaması.
8. Yazılım ve sürüm bilgisinin verilmemesi.
9. Tabloda ve metinde farklı sayılar (denetimde her sayıyı çapraz kontrol et).
10. Yuvarlama sonrası toplamın %100 tutmaması.

## ML / mühendislik değerlendirmesi

- **Tek koşu sonucu rapor etme.** Birden çok tohum (seed) ile ortalama ± standart sapma veya GA; kaç koşu olduğu yazılır.
- Test kümesi bir kez kullanılır; hiperparametre seçimi doğrulama kümesinde yapılır. "Test setinde ayarladık" sızıntıdır.
- Temel yöntemler (baseline) adil ayarlanmalı: kendi yöntemine ayırdığın arama bütçesini rakibe de ayırdığını yaz.
- Metrik seçimi gerekçelendirilir; dengesiz sınıfta accuracy yerine F1/AUPRC/dengeli doğruluk.
- Ablation: hangi bileşenin ne kadar katkı verdiği.
- Hesaplama maliyeti (donanım tipi, süre, toplam GPU-saat) raporlanır — NeurIPS kontrol listesinde ayrı madde.
- İstatistiksel karşılaştırma: eşleştirilmiş testler, mümkünse bootstrap GA. Çok sayıda benchmark üzerinde karşılaştırma yapılıyorsa düzeltme veya sıralama temelli testler.
- LLM değerlendirmesinde: prompt sürümü, sıcaklık, model sürümü ve tarih, kaç tekrar, değerlendirici (insan/LLM-judge) protokolü.

## Denetim çıktısı

İstatistik denetimi yaparken her bulguyu şu formda ver:

```
🔴 Bulgular §3.2 — "Grup A'da anlamlı iyileşme görüldü (p=0,04)"
Sorun: Etki büyüklüğü ve güven aralığı yok; grup içi karşılaştırmadan gruplar arası sonuç çıkarılmış.
Öneri: "A ve B grupları arasındaki ortalama fark X birim (%95 GA: a–b; p=0,04)" biçimine çevir; fark hesaplanmamışsa hesaplanması gerekir.
```
