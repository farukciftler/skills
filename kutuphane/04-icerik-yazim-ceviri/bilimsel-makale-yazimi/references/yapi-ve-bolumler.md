# Yapı ve bölümler

İçindekiler: Başlık · Öz · Anahtar kelimeler · Giriş · Yöntem · Bulgular · Tartışma · Sonuç · Şekil ve tablolar · Kaynaklar · Beyan bölümleri · Derleme/olgu/bildiri varyantları · Dil notları

---

## Başlık

Editör ve okur önce başlığı görür; masa reddi kararının ilk girdisidir.

Çalışan kalıplar:
- **Sonuç bildiren (declarative):** "Düşük doz X, Y hastalarında Z'yi azaltır" — bulgunun net ve tekil olduğu yerde güçlü, ama tasarım nedenselliği desteklemiyorsa yasaktır.
- **Betimleyici:** "X'in Y üzerindeki etkisi: çok merkezli kesitsel çalışma" — çoğu klinik/gözlemsel iş için güvenli.
- **İki parçalı (CS/ML):** "KısaAd: Ne yaptığını anlatan alt başlık" — konferans normu.

Kurallar: 12–15 kelimeyi geçme; taranabilir anahtar kelimeleri başa al; soru formunu gerekmedikçe kullanma; kısaltmayı yalnızca alanın tamamı biliyorsa kullan; tasarımı alt başlıkta belirtmek çoğu dergide zorunlu (randomized controlled trial, systematic review, cross-sectional study).

Ürettiğin her başlık için 3 alternatif ver ve hangisinin hangi mecraya uygun olduğunu tek cümleyle söyle.

## Öz (abstract)

Hakemin ilk beş dakikası burada geçer. Yapılandırılmış öz (Amaç–Yöntem–Bulgular–Sonuç) çoğu dergide zorunlu; serbest özde de aynı beş hamle sırayla bulunmalı.

Beş hamle, cümle bütçesiyle (250 kelimelik öz için):
1. **Bağlam ve boşluk** (1–2 cümle) — bilinen ne, eksik ne.
2. **Amaç** (1 cümle) — "Bu çalışmada … amaçlandı."
3. **Yöntem** (2–4 cümle) — tasarım, ortam, katılımcı/veri, örneklem büyüklüğü, birincil çıktı, analiz.
4. **Bulgular** (3–5 cümle) — **rakamla**. Etki büyüklüğü + %95 GA; yalnız p verme. Birincil çıktıyı önce.
5. **Sonuç** (1–2 cümle) — bulgudan çıkan tek çıkarım; tasarımın izin verdiği kadar. "Daha fazla çalışma gerekli" tek başına sonuç değildir.

Özde olmayacaklar: metinde geçmeyen sonuç, kaynak, kısaltma seli, "umut vaat edici" gibi ölçülemeyen sıfatlar, veri olmadan yapılan öneri.

Klinik çalışmada kayıt numarası, sistematik derlemede PROSPERO numarası öze eklenir. PRISMA'nın öz için ayrı kontrol listesi vardır (PRISMA 2020 for Abstracts).

## Anahtar kelimeler

Başlıkta geçmeyen, indeksleme terimlerinden seçilmiş 4–6 terim. Tıpta MeSH, mühendislikte IEEE Taxonomy/ACM CCS. Başlıktakini tekrar etmek arama görünürlüğünü israf eder.

## Giriş

Üç hamleli huni (Swales CARS uyarlaması) — üç paragraf çoğu zaman yeter:

1. **Alanı kur.** Neden önemli, kim etkileniyor, ne biliniyor. Genel geçer cümleyle başlama ("Teknoloji hızla gelişmektedir" gibi açılışlar editörü kaybeder).
2. **Boşluğu aç.** Mevcut literatürün ne yaptığı ve **tam olarak neyi yapmadığı**. Boşluk iddiası kanıtlanır: hangi çalışmalar, hangi sınırlılıkla. "Literatürde çalışma yoktur" cümlesi ancak sistematik bir arama anlattıysan geçerlidir.
3. **Boşluğu doldur.** Bu çalışmanın amacı, tasarımı ve — çoğu alanda — ana katkısı. Son paragrafta hipotez veya araştırma sorusu açıkça yazılır.

Giriş literatür taraması değildir. Derleme niteliğindeki geniş anlatım, ayrı bir "İlgili Çalışmalar" bölümüne (CS geleneği) ya da Tartışma'ya aittir.

## Yöntem

Tek ölçüt: **başka biri bunu tekrar edebilir mi?** Alt başlıklarla yaz.

Ortak iskelet:
- Tasarım ve ortam (yer, tarih aralığı)
- Katılımcı/veri kaynağı; dahil–hariç kriterleri; örnekleme yöntemi
- Örneklem büyüklüğü gerekçesi (güç analizi varsa parametreleriyle)
- Değişkenler: birincil/ikincil çıktı tanımları, ölçüm araçları, geçerlik-güvenirlik
- Müdahale/uygulama detayı (TIDieR düzeyinde: ne, kim, ne kadar, ne sıklıkla)
- Yanlılık kaynakları ve kontrolü (körleme, randomizasyon yöntemi, karıştırıcı değişkenler)
- Kayıp veri politikası
- İstatistiksel analiz: her hipotez için hangi test, hangi yazılım+sürüm, anlamlılık düzeyi, çoklu karşılaştırma düzeltmesi
- Etik: kurul adı, karar tarihi ve sayısı, onam türü
- Kayıt/protokol referansı; protokolden sapmalar açıkça yazılır

ML/mühendislik için ek: veri kümesi sürümü ve bölünmesi (train/val/test), önişleme, model mimarisi ve parametre sayısı, hiperparametre arama uzayı ve seçim yöntemi, tohum (seed) sayısı, donanım ve toplam hesaplama maliyeti, değerlendirme metrikleri ve neden onlar, karşılaştırılan temel yöntemlerin (baseline) ayarları. Ayrıntı: `cs-ml-konferans.md`.

Geçmiş zaman ve edilgen/etken karışımı serbesttir; tutarlılık şart.

## Bulgular

Yalnızca sonuç; yorum yok, kaynak yok.

Sıra: katılımcı akışı ve tanımlayıcı istatistikler → birincil çıktı → ikincil çıktılar → alt grup/keşifsel analizler (keşifsel olduğu açıkça yazılır) → istenmeyen etkiler/başarısızlık modları.

- Her sayı bir kez verilir: metinde tekrar edilen tablo satırı yer israfıdır. Metin tabloyu özetler, kopyalamaz.
- Etki büyüklüğü ve %95 GA ile başla, p'yi arkasına ekle.
- "Anlamlı" kelimesini yalnızca istatistiksel anlamda kullan; klinik/pratik önem ayrı bir cümledir.
- Beklenmedik ve olumsuz sonuçları da yaz. Yalnızca çalışan konfigürasyonu raporlamak, hakemin en sert itirazıdır.

## Tartışma

Beş bloklu yapı:

1. **Ana bulgunun tekrarı** (yorumlanmış hâliyle, rakam tekrarı olmadan) — 1 paragraf.
2. **Literatürle karşılaştırma** — kimle uyumlu, kimle çelişiyor ve **neden**. Çelişkiyi açıklamaya çalışmak, örtmeye çalışmaktan güçlüdür.
3. **Mekanizma/yorum** — bulgu neden böyle çıktı; spekülasyon açıkça spekülasyon olarak etiketlenir.
4. **Sınırlılıklar** — gerçek olanlar. "Örneklem küçüktü" deyip geçmek yerine: hangi sınırlılık hangi sonucu nasıl etkiler, yönü ne. Dürüst sınırlılık bölümü güven kazandırır; savunmacı olan kaybettirir.
5. **Çıkarım** — uygulamaya ve sonraki araştırmaya ne diyor. Somut olsun.

Tartışma'da yeni sonuç yok, Bulgular'ın tekrarı yok, kendi çalışmanı literatürdeki her şeyden üstün ilan etme yok.

## Sonuç

Çoğu dergide Tartışma'nın son paragrafı yeterlidir; ayrı bölüm isteniyorsa 3–5 cümle. Yeni bilgi girmez.

## Şekil ve tablolar

- Her şekil/tablo **kendi başına anlaşılır** olmalı: başlık, eksen etiketleri, birimler, n, hata çubuğunun ne olduğu (SD mi SE mi %95 GA mı — mutlaka yaz), kısaltma açıklamaları.
- Tablo 1 genelde örneklem tanımıdır; gruplar arası p değeri koymak çoğu metodolog tarafından hatalı sayılır (randomizasyonda anlamsız).
- Bar grafiği yerine dağılımı gösteren gösterim (nokta, kutu, violin) küçük n'de tercih edilir.
- Renk tek başına bilgi taşımasın (renk körlüğü + siyah-beyaz baskı).
- **Görsel bütünlüğü:** panel birleştirme, kontrast/parlaklık ayarının seçici uygulanması, aynı görüntünün farklı figürlerde tekrar kullanımı geri çekilme sebebidir. Ham görüntüleri sakla.
- Şekil sayısı derginin sınırına uyar; fazlası ek materyale.

## Kaynaklar

- Hedef derginin stili (Vancouver, APA 7, IEEE, ACM) baştan seçilir; referans yöneticisi kullanılır.
- Her künye doğrulanır (DOI/arXiv). Erişim tarihi gereken kaynaklarda tarih yazılır.
- Güncellik: alanın hızına göre son 5 yılın payı anlamlı olmalı; klasikler ayrı.
- Yağmacı/şüpheli dergilere atıf yapmaktan kaçın (ICMJE bunu açıkça önerir).
- Aşırı kendine atıf (self-citation) ve dergiye yaranmak için yapılan zorlama atıflar editör tarafından fark edilir.

## Beyan bölümleri

Metnin sonunda, dergi düzenine göre: Yazar katkıları (CRediT), Fon, Çıkar çatışması, Etik onay ve onam, Veri erişilebilirliği, Kod erişilebilirliği, Teşekkür, Yapay zekâ kullanım beyanı. Boş bırakmak yerine "yoktur" yaz.

## Varyantlar

- **Sistematik derleme:** PRISMA akış diyagramı zorunlu; arama stratejisi tam olarak (veri tabanı, tarih, sorgu dizisi) verilir; PROSPERO kaydı; yanlılık değerlendirme aracı (RoB 2, ROBINS-I, AMSTAR-2) belirtilir.
- **Olgu sunumu:** CARE; hasta onamı zorunlu; zaman çizelgesi şekli; "nadir" iddiası kanıtlanır.
- **Konferans bildirisi:** sayfa sınırı serttir; katkı erken ve net; ilgili çalışmalar kısa; ek materyal ayrı.
- **Kısa/letter formatı:** tek bulgu, tek şekil disiplini.

## Dil notları (Türkçe konuşan yazarlar için)

İngilizce yazarken en sık müdahale gereken noktalar:
- **Artikel:** sayılabilir tekil isim artikelsiz kalamaz ("We used dataset" → "We used a dataset"); genel çoğul kullanımda "the" gereksizdir ("The neural networks are powerful" → "Neural networks are…").
- **Present perfect vs. past:** kendi çalışmanın yaptıkları geçmiş zaman ("We collected"), literatürün birikimi present perfect ("Prior work has shown").
- **Şişme kalıplar:** "It is worth noting that", "In the literature, it is known that", "Due to the fact that" → sil ya da kısalt.
- **Yanlış dost:** "eventually" (sonunda ≠ muhtemelen), "actual" (güncel değil, gerçek), "control" (denetlemek ≠ kontrol etmek/incelemek), "propose" vs "suggest".
- **Belirsiz özne:** "It is thought that" yerine kimin düşündüğünü yaz.
- Uzun zincir tamlamalardan kaçın; bir cümlede tek fikir.

Türkçe yazarken: terim tutarlılığı (bir kavram = bir terim), "-mektedir" yığılmasından kaçınma, edilgen yapının aşırı kullanımından kaçınma, ondalık ayırıcı olarak virgül ve binlik nokta kullanımının dergi kuralına uydurulması.

**Not:** Dil düzeltme araçlarının (Grammarly, LLM) kullanımı çoğu mecrada serbesttir ama IEEE gibi bazıları beyanı yine de önerir; kapsamlı yeniden yazım ise farklı bir kategoridir. Bkz. `etik-ve-yapay-zeka.md`.
