# Kanıt Çıkarma — Görüşme Protokolü ve Soru Bankası

CV yazımının asıl işi budur. Kullanıcı kendi işini "sorumluluk" diliyle hatırlar
("raporlamadan sorumluydum"); CV ise "sonuç" dili ister. Aradaki dönüşümü tahminle değil,
soruyla yap.

## İçindekiler
1. Görüşme ilkeleri
2. Metrik taksonomisi
3. Rakam yoksa: iniş merdiveni
4. Rol ailesine göre soru bankası
5. Zor durumlar (boşluk, kovulma, kariyer değişimi, gizlilik)
6. Kanıt kaynakları

---

## 1. Görüşme ilkeleri

- **Turda az soru, sırayla.** Rol başına 4-6 soru. On soruluk anket gönderirsen kullanıcı
  yarısını cevaplar ve kalitesi düşer.
- **Önce ham döküm, sonra kazma.** "Bu rolde tipik bir haftada ne yapıyordun?" ile başla;
  ortaya çıkan iki-üç konuyu kaz.
- **Kullanıcının kendi kelimesini koru.** Ürün, ekip, araç, müşteri adları CV'yi gerçek yapan
  şeydir; onları cilalayıp jenerikleştirme.
- **"Bunu nereden biliyorsun?" diye sor.** Kaynağı olmayan rakam mülakatta risktir. Kaynak
  varsa (dashboard, OKR dokümanı, fatura, ticket) kullanıcı mülakatta da savunabilir.
- **Eleme de senin işin.** Toplanan her kanıt CV'ye girmez; master'a girer, varyanta seçilir.

## 2. Metrik taksonomisi

Kazarken bu beş eksende dolaş. Çoğu rol için en az ikisi doludur.

| Eksen | Ne aranır | Örnek soru |
|---|---|---|
| **Para** | gelir, maliyet, marj, bütçe, tasarruf, ARR | "Bu iş şirkete ne kazandırdı ya da neyi ucuzlattı?" |
| **Zaman** | süre kısalması, çevrim süresi, teslim hızı, SLA | "Önce ne kadar sürüyordu, sonra ne kadar sürdü?" |
| **Hacim** | kullanıcı, işlem, istek, SKU, trafik, veri boyutu | "Kaç kullanıcıyı / kaç işlemi etkiledi?" |
| **Kalite** | hata oranı, churn, NPS, doğruluk, uptime, iade | "Ölçtüğünüz kalite göstergesi neydi, nasıl değişti?" |
| **Kapsam** | ekip büyüklüğü, bütçe, coğrafya, sistem sayısı | "Kaç kişiyle, hangi bütçeyle, kaç ülke/ekip için?" |

Ek olarak her başarı için **zorluk**: "Bunu zor kılan neydi?" — bullet'ın ikinci yarısı
genelde buradan çıkar ve adayı benzerlerinden ayırır.

## 3. Rakam yoksa: iniş merdiveni

Sırayla in, ilk tutan basamakta dur:

1. **Kesin rakam** — "%23 düşürdü", "₺1,8M tasarruf"
2. **Mertebe / oran** — "yaklaşık iki katına", "altı haneli bütçe", "gün → saat"
3. **Kapsam** — "12 kişilik ekip, 3 ülke, 40+ müşteri"
4. **Somut nitel** — "sıfırdan kurdum, iki yıl sonra hâlâ kullanımda", "şirketin ilk X'i"
5. **Hiçbiri yok** — satırı yaz, rakam yerine `[ ]` bırak, "doldurulacaklar" listesine ekle.

Asla: tahmini rakamı kesinmiş gibi yazma, "yaklaşık %50" diye yuvarlama uydurma.

## 4. Rol ailesine göre soru bankası

Kullanıcının rolü listede yoksa en yakınını al ve metrik taksonomisiyle uyarla.

### Ürün / PM
- Hangi ürünün, hangi aşamasında (0→1, ölçekleme, bakım) sorumluydun? Kullanıcı sayısı/geliri?
- Senin kararınla gelen bir sonuç var mı — neyi yapmamaya karar verdin?
- Hangi metrik senin metrindi? Sen devraldığında ne, bıraktığında ne?
- Kaç mühendis/tasarımcıyla, hangi ritimde çalıştın? Kime raporladın?
- Keşif tarafı: kaç müşteri görüşmesi, hangi bulgu roadmap'i değiştirdi?
- Kurumsal: hangi anlaşmayı/yenilemeyi ürün tarafından etkiledin?

### Yazılım / Veri mühendisliği
- Hangi sistem, hangi ölçek (istek/sn, veri hacmi, kullanıcı)?
- Performans/maliyet/güvenilirlik sayılarından hangisini değiştirdin — önce/sonra?
- Sahiplendiğin bileşen neydi; senden sonra kim devraldı?
- Kesinti, borç azaltma, migrasyon: kapsam ve süre?
- Kod dışı etki: gözden geçirme, mentorluk, standart getirme?

### Veri / Analitik / ML
- Modelin/analizin **kararı** neydi — kim ne yaptı sonucunda?
- Baseline neydi, ne kadar iyileştirdin, hangi metrikle (ve neden o metrik)?
- Üretime çıktı mı? Kaç kullanıcı/işlem etkiliyor, hâlâ çalışıyor mu?
- Veri hacmi, gecikme, maliyet kısıtı neydi?

### Satış / İş geliştirme
- Kota neydi, gerçekleşme? Ortalama anlaşma büyüklüğü, satış döngüsü?
- Sıralamada neredeydin (kaç kişiden kaçıncı)?
- Yeni pazar/kanal açtın mı, ilk yıl katkısı?

### Pazarlama / Büyüme
- Hangi kanal, hangi bütçe, CAC/dönüşüm nasıl değişti?
- Trafik/kayıt/gelir hangisi arttı — atıf yöntemin neydi?
- Marka/içerik tarafında sayı yoksa kapsam ver (yayın sayısı, erişim, iş birliği).

### Operasyon / Tedarik / Üretim
- Süreç önce kaç adım/kaç gün sürüyordu, sonra?
- Hata/fire/iade oranı, maliyet birim başına?
- Kaç kişilik ekip, kaç tedarikçi, hangi hacim?

### Danışmanlık / Freelance
- Müşteri sektörü ve büyüklüğü (isim gizliyse "50+ mağazalı perakende zinciri")?
- Teslimat neydi, müşteri onunla ne yaptı, tekrar iş aldın mı?
- Proje bedeli/süresi (paylaşmak istemiyorsa kapsamla anlat)?

### Yeni mezun / staj
- Projede senin yaptığın kısım neydi (ekipten ayır)?
- Ölçtüğün bir sonuç var mı — doğruluk, hız, kullanıcı testi?
- Ders dışı: topluluk, kulüp, hackathon, açık kaynak katkısı, ders asistanlığı?
- Not ortalaması yalnızca güçlüyse ve pazarda bekleniyorsa yazılır.

## 5. Zor durumlar

- **İstihdam boşluğu:** gizleme, tek satır açıkla — "Kariyer arası (aile bakımı) / eğitim /
  girişim denemesi". Açıklanmamış boşluk, açıklanmış boşluktan daha çok soru işareti üretir.
- **Kısa süreli işler:** üst üste kısa roller varsa bağlamı ver ("şirket kapandı",
  "proje bazlı sözleşme"). Aynı işverendeki birden çok rolü tek şirket başlığı altında topla —
  hem doğru hem terfiyi gösterir.
- **İşten çıkarılma:** CV'de belirtilmez; ön yazı veya mülakat konusudur.
- **Kariyer değişimi:** aktarılabilir kanıtı öne al, eski rolün jargonunu hedef pazarın
  diline çevir, özet cümlesini geçişi açıklayacak şekilde yaz.
- **Gizlilik / NDA:** müşteri ve rakam açıklanamıyorsa anonimleştir ("Fortune 500 perakendeci",
  "yedi haneli bütçe"). Uydurmak yerine bulanıklaştır.
- **Serbest çalışma dönemi:** tek bir başlık altında topla ("Bağımsız Danışman, 2023–2025"),
  altına 2-3 temsili iş.

## 6. Kanıt kaynakları

Kullanıcı "hatırlamıyorum" dediğinde bakılacak yerler: eski performans değerlendirmeleri,
OKR/hedef dokümanları, terfi yazıları, proje kapanış raporları, dashboard ekran görüntüleri,
faturalar ve teklifler, git/ticket geçmişi, sunum desteleri, LinkedIn'deki eski gönderiler,
takım e-postaları. Kullanıcıya bunları taramasını öner — beş dakikalık arama, bir saatlik
tahminden iyi CV üretir.
