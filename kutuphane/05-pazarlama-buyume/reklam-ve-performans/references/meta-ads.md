# Meta Ads (Instagram / Facebook) — Konut Projesi Kurgusu

## İçindekiler

1. 2026'da Meta'nın çalışma mantığı: Andromeda
2. Hesap ve kampanya mimarisi
3. Advantage+ ve ne zaman kullanılır
4. Lead formu, WhatsApp, açılış sayfası — hangisi
5. Hedefleme: ne kaldı, ne gitti
6. Özel Reklam Kategorisi (Housing) — Türkiye durumu
7. Kreatif hacmi ve yenileme ritmi
8. Sinyal kalitesi: Piksel, CAPI, EMQ
9. Yerleşimler ve format
10. Bütçe, öğrenme ve ölçekleme
11. Sık yapılan pahalı hatalar

---

## 1. 2026'da Meta'nın çalışma mantığı: Andromeda

Bu bölümü anlamadan Meta kurgusu yapma; son iki yılda platformun mantığı
kökten değişti.

**Andromeda**, Meta'nın 2025 ortasında yayına alıp Ekim 2025'te çoğu hedef
ve yerleşimde tamamladığı yeni reklam sıralama altyapısı. Yaptığı iş:
**hedeflemeyi kitleden kreatife taşımak.** Eskiden ilgi alanı, demografi ve
benzer kitlelerle "kime göstereceğini" sen söylerdin; artık sistem
kreatifini okuyup kime uyacağını kendisi tahmin ediyor ve paralelde binlerce
kat daha fazla aday değerlendiriyor.

**Sonuç — Meta'da üç kaldıraç kaldı:**

| Kaldıraç | Ne demek | Emlak karşılığı |
|---|---|---|
| **Kreatif çeşitliliği** | Farklı kanca ve formatta 15-20 aktif reklam | Tek render ile Meta çalışmaz |
| **Sade kampanya yapısı** | Az kampanya, az reklam seti, tek havuz | Ad set çoğaltmak artık zarar |
| **Temiz dönüşüm sinyali** | Piksel + CAPI birlikte, EMQ 7 üstü | Ölçüm bölümüne bak |

Kitle segmentasyonuyla uğraşmak 2026'da vakit kaybı; o vakti kreatif üretimine
harcamak ölçülebilir kazanç. Bu, bu dosyanın en önemli cümlesi.

---

## 2. Hesap ve kampanya mimarisi

Sadelik burada estetik tercih değil, öğrenme eşiği zorunluluğu. Reklam seti
başına haftada ~50 optimizasyon olayı gerekiyor; ad set çoğaltmak bu havuzu
böler ve hepsini "Öğrenme sınırlı" durumuna düşürür.

**Küçük-orta bütçe (< 100.000 TL/ay) — hedeflenen yapı:**
```
Kampanya: Lead Üretimi (Advantage+ leads ya da standart, tek hedef)
└── Reklam seti: Tek, geniş (İstanbul Anadolu + hedef yaş bandı)
    └── 8-15 reklam: farklı kanca, farklı format, farklı vaat

Kampanya: Yeniden Pazarlama
└── Reklam seti: Site ziyaretçileri + video izleyenler + etkileşim
    └── 4-6 reklam: hatırlatma ve somut adım (randevu)
```

**Orta-büyük bütçe (> 100.000 TL/ay) — eklenir:**
```
Kampanya: Talep Yaratma / Erişim (video, üst huni)
Kampanya: Ticari Alan (ayrı alıcı profili, ayrı mesaj)
```

Rezidans ve ticari alanı ayırma gerekçesi hedefleme değil **kreatif ve
mesajdır**: aynı reklam setinde yarışan iki farklı vaat, Andromeda'nın
sinyalini bulandırır.

---

## 3. Advantage+ ve ne zaman kullanılır

Meta 2026 ilk çeyreğinde eski kampanyaların Advantage+'a geçişini zorunlu
kıldı. Advantage+ Sales, e-ticaretin ötesine geçip lead üretimi ve uygulama
yüklemesini de kapsıyor. Meta'nın global testlerinde manuel kampanyalara
göre ortalama **%32 daha yüksek ROAS ve %17 daha düşük EBM** raporlandı
[KIYAS: Meta kaynaklı, satıcı verisidir — bağımsız değil].

**Emlak için okuma:** Advantage+ hacim ve öğrenme hızı kazandırır, kontrol
kaybettirir. Karar kuralı basit:

- **Ölçüm sağlamsa** → Advantage+ kullan, kreatife odaklan.
- **Ölçüm zayıfsa** → Advantage+ senin körlüğünü hızlandırır. Önce ölçümü kur.

Advantage+ kreatif özellikleri (otomatik kırpma, müzik ekleme, metin
varyasyonu, görsel iyileştirme) **marka kimliği açısından denetlenmeli.**
Otomatik kırpma logoyu ya da "Temsili görseldir" notunu güvenli alanın
dışına atabilir. Kreatif iyileştirmeleri açtıysan çıktıyı önizlemeden
yayına alma — `gorsel-uretim` skill'indeki güvenli alan kuralları geçerli.

---

## 4. Lead formu, WhatsApp, açılış sayfası — hangisi

Bu, Moonstone'un bugünkü durumunda en önemli karar. Site yayında olduğu için
üç yol da açık — ama Meta Pixel kurulmadan açılış sayfası yolu ölçülemez.

| Yol | Güçlü yanı | Zayıf yanı | Ne zaman |
|---|---|---|---|
| **Anlık lead formu** | En düşük sürtünme, en düşük CPL. Açılış sayfası kampanyalarına göre CPL %30-50 daha düşük [KIYAS] | Lead kalitesi en düşük. Yanlış numara oranı yüksek | Hacim ve mesaj testi için |
| **Tıkla-WhatsApp** | Niyet yüksek, sohbet kişisel. Yüksek WhatsApp kullanımı olan pazarlarda lead→sohbet oranı belirgin şekilde daha iyi [KIYAS] | CPL daha yüksek. **Anında insan cevabı gerekir** | Danışmanlı satışta — emlak tam buraya oturur |
| **Açılış sayfası** | En nitelikli lead, tam ölçüm, remarketing havuzu besler | Site gerekiyor, CPL en yüksek | Site yayına girdiğinde ana yol |

**Türkiye'de WhatsApp yaygınlığı yüksek ve emlak danışmanlı bir satış** —
tıkla-WhatsApp bu proje için doğal seçim. Ama tek şartı var: **mesaja
dakikalar içinde dönülmesi.** Dönülmeyecekse lead formu daha az zarar verir.

**Önerilen kurgu [MUHAKEME]:** Site yayına girene kadar lead formu ve
WhatsApp'ı **aynı kampanyada ayrı reklamlarla** paralel çalıştır, 30 gün
sonunda ikisinin **randevu maliyetini** karşılaştır — CPL'ini değil.
Bu karşılaştırma, ilk ayın en değerli çıktısıdır.

**Lead formu ayarları:**
- **"Daha yüksek niyet" (higher intent) formunu seç.** Ek onay adımı ekler,
  lead sayısını düşürür, kaliteyi belirgin yükseltir. Emlakta doğru tercih.
- 3-4 alandan fazlasını sorma: ad, telefon, daire tipi tercihi.
- **Nitelendirici soru ekle** ("Hangi daire tipiyle ilgileniyorsunuz?",
  "Ne zaman taşınmayı planlıyorsunuz?") — hem kaliteyi yükseltir hem satış
  ekibine ilk cümleyi verir.
- Fiyat sorusu sorma; elimizde fiyat yokken beklenti yaratır.
- **KVKK aydınlatma metni bağlantısı zorunlu** → `references/olcum-ve-crm.md`.
- Lead'ler CRM'e otomatik akmalı; Meta panelinden manuel indirme, gecikme
  demektir ve gecikme lead öldürür.

---

## 5. Hedefleme: ne kaldı, ne gitti

Andromeda sonrası doğru varsayılan **geniş hedefleme**. Daraltmak artık
çoğu durumda performansı düşürüyor çünkü sistemin aday havuzunu kısıtlıyorsun.

**Kullan:**
- Coğrafya: İstanbul Anadolu Yakası ana halka, İstanbul geneli ikinci halka
- Yaş: geniş bırak (25-65+). Daraltmanın kazancı, öğrenme kaybından küçük
- Yeniden pazarlama kitleleri: site, video izleyenler, Instagram etkileşimi,
  lead formu açıp göndermeyenler
- Müşteri listesi (CRM) — **KVKK açık rızası olmadan yüklenmez**

**Kullanma / boşuna uğraşma:**
- İlgi alanı yığınları ("lüks yaşam", "gayrimenkul yatırımı") — Andromeda
  bunları zaten kreatiften çıkarıyor, elle daraltmak erişimi kısıtlıyor
- Detaylı hedefleme genişletmesini kapatmak — kapatmak genelde zarar
- Çok sayıda benzer (lookalike) kitleyi ayrı ad set'lerde çoğaltmak

**Yeniden pazarlama havuzları (öncelik sırasıyla):**
1. Lead formunu açıp göndermeyenler — en sıcak
2. Video %50+ izleyenler
3. Site ziyaretçileri (site yayına girince)
4. Instagram/Facebook etkileşimi son 90 gün
5. Mevcut lead listesi — yeni proje/etap duyurusu için

---

## 6. Özel Reklam Kategorisi (Housing) — Türkiye durumu

**Bilinen:** Meta'nın Özel Reklam Kategorisi (Housing / Employment / Credit)
kuralları ABD, Kanada ve "Avrupa'nın belirli bölgeleri" için zorunlu. Kategori
seçildiğinde yaş ve cinsiyet hedeflemesi kilitlenir, ilgi alanı hedeflemesi
ve kitle hariç tutmaları kalkar, coğrafi yarıçapa alt sınır gelir.

**Bilinmeyen:** Türkiye'yi hedefleyen konut reklamları için bu kategorinin
zorunlu olup olmadığı, Meta'nın kamuya açık dokümanlarında net değil.
**Bunu ben doğrulayamadım — uydurmuyorum, bilmiyorum diyorum.**

**Ama şu risk gerçek:** 2026 itibarıyla Meta'nın konut/istihdam/kredi
kategorisi tespiti **çok modlu ve otomatik** hale geldi — yani reklamı sen
beyan etmesen de sistem içerik ve görselden sınıflandırabiliyor. Yanlış
beyan, reklam reddine ve tekrarında hesap kısıtına yol açar.

**Yapılacak iş:**
1. Reklam hesabı kurulurken **kampanya oluşturma ekranında kategori seçeneği
   çıkıyor mu** kontrol et — pratikte tek kesin cevap budur.
2. Çıkıyorsa ve zorunluysa doğru beyan et; hedefleme kısıtlarına göre planı
   revize et (ki geniş hedefleme zaten önerdiğimiz yol, kayıp sınırlı olur).
3. Çıkmıyorsa not düş, üç ayda bir tekrar bak — politika değişiyor.
4. `[DOĞRULA: Meta Özel Reklam Kategorisi Türkiye'de konut için zorunlu mu]`

Ayrımcılık çağrıştıran hedefleme ve metin (belirli bir demografiyi dışlayan
ifadeler) kategori zorunlu olmasa da her pazarda politika ihlalidir. Bu
ayrıca marka açısından da doğru olan yol.

---

## 7. Kreatif hacmi ve yenileme ritmi

Andromeda sonrası performansın birinci belirleyicisi bu. Hedef: **kampanyada
aynı anda 15-20 aktif reklam**, farklı kanca ve formatta [KIYAS: 2026 sektör
pratiği]. Küçük bütçede bu sayı orantılı düşer ama **4'ün altına inmemeli** —
altına inince kreatif yorulur, sıklık artar, CPM tırmanır.

**Emlak için kreatif arketipleri** (her birinden en az bir varyant):
1. Dış cephe / gündoğumu-günbatımı render — marka ve ölçek
2. İç mekân yürüyüşü (dikey video) — yaşam hissi
3. Kat planı + metrekare kartı — niyeti yüksek olanı yakalar
4. Konum ve çevre — "burada yaşamak nasıl"
5. Sosyal alan vitrini — ayırt edici özellik
6. İnşaat ilerlemesi / şantiye — güven ve gerçeklik (en çok küçümsenen format)
7. Danışman yüzü, telefon çekimi (UGC tadında) — güven
8. Statik tek kare, tek cümle — hızlı test için ucuz

**Yenileme ritmi [MUHAKEME]:** Haftada en az 2 yeni kreatif üretim hattına
girmeli. Bir kreatifi sıklığı 3'ü geçtiğinde ya da hook rate düştüğünde
emekliye ayır — CPL bozulmasını bekleme, o geç bir sinyal.

Kreatifi *değerlendirme* ve *öldürme* kararı ayrı bir iştir:
`references/kreatif-degerlendirme.md`.

Kreatif *üretimi* için `gorsel-uretim` skill'i; ölçüler ve güvenli alan
için `moonstone-residence/references/post-uretimi.md`.

---

## 8. Sinyal kalitesi: Piksel, CAPI, EMQ

Andromeda kreatiften tahmin yapıyor ama **öğrenmek için temiz dönüşüm
sinyaline muhtaç.** Sinyal bozuksa kreatif ne kadar iyi olursa olsun sistem
yanlış kişiye gösterir.

**Üç şart:**
1. **Piksel + Conversions API (CAPI) birlikte** çalışmalı — tarayıcı tarafı
   çerez kısıtlarıyla eriyor, sunucu tarafı bunu telafi ediyor.
2. **Event Match Quality (EMQ) 7 üstü** olmalı. Altındaysa eşleşme parametresi
   ekle (hashlenmiş e-posta, telefon, ad-soyad, IP, kullanıcı aracısı).
3. **Tekilleştirme (deduplication)** doğru kurulmalı — aynı olay iki kez
   sayılırsa dönüşüm şişer, teklif motoru yanlış öğrenir.

Kurulum ve KVKK tarafı: `references/olcum-ve-crm.md`.

---

## 9. Yerleşimler ve format

**Yerleşimleri Advantage+ (otomatik) bırak.** Elle yerleşim seçmek 2026'da
neredeyse her zaman zarar — sistem hangi yerleşimin ucuz dönüşüm getirdiğini
senden iyi biliyor.

**Ama formatı sen kontrol et:**
- **9:16 dikey ana format.** Reels ve Stories hacmin çoğunu taşıyor.
- **1:1 kare** feed için ikinci varyant olarak yüklensin.
- Güvenli alan: dikeyde üst ve alt %14'lük şeritlere kritik metin ve logo
  koyma — arayüz üstünü örter. Detay: `moonstone-residence/references/story-uretimi.md`.
- **Sessiz izlenmeye göre tasarla.** İlk 3 saniyede mesaj görselden anlaşılmalı;
  altyazı zorunlu.
- Metin: birincil metnin ilk satırı kırpılmadan görünen tek satırdır. Vaadi
  oraya koy.

---

## 10. Bütçe, öğrenme ve ölçekleme

**Öğrenme eşiği:** Reklam seti başına **7 günde ~50 optimizasyon olayı**.
Sayaç reklam setinde, reklamda değil — beş kreatif tek havuzu paylaşır.
Bu, "her kreatife ayrı ad set" refleksini yanlış kılan sebep.

**Öğrenmeyi sıfırlayan hareketler:** bütçede %20'yi aşan değişiklik,
hedefleme değişikliği, teklif stratejisi değişikliği, optimizasyon hedefi
değişikliği.

**Ölçekleme kuralları [MUHAKEME — öğrenme sıfırlanmasını önlemek üzerine]:**
- Bütçe artışı **her 3-4 günde bir %20'yi geçmesin.**
- Aceleyle ikiye katlamak gerekiyorsa, kampanyayı çoğaltmak yerine bütçeyi
  kademeli artır; çoğaltma öğrenmeyi baştan başlatır.
- Ölçekleme kararı **CPL'e değil randevu maliyetine** bakılarak verilir.

**Sıklık (frequency) izle.** Haftalık sıklık 3'ü geçtiğinde ya kitle küçük
ya kreatif tükenmiş demektir. Emlak gibi uzun döngülü kategoride 2-3
bandı sağlıklı; 5 üzeri marka yıpratır.

---

## 11. Sık yapılan pahalı hatalar

1. **Kitle segmentasyonuna kreatiften çok emek harcamak.** 2026'da ters
   çevrilmiş öncelik — kaldıraç kreatifte.
2. **Her kreatife ayrı reklam seti açmak.** 50 olay havuzunu böler, hepsi
   "Öğrenme sınırlı"da kalır.
3. **CPL'e bakıp sevinmek.** Meta ucuz lead üretmekte çok iyidir; sorulacak
   soru "bu lead randevuya döndü mü".
4. **WhatsApp reklamı açıp mesajlara saatler sonra dönmek.** Bu kanalın tek
   avantajı hızdı; hız yoksa avantaj yok, maliyet var.
5. **CAPI kurmadan çalışmak.** Sinyal eksik gider, Andromeda yanlış öğrenir,
   maliyet sessizce yükselir.
6. **Advantage+ kreatif iyileştirmelerini denetlemeden açmak.** Otomatik
   kırpma marka güvenli alanını bozar.
7. **Kreatifi CPL bozulunca değiştirmek.** CPL geç sinyaldir; hook rate ve
   sıklık erken sinyaldir → `references/kreatif-degerlendirme.md`.
8. **Doğrulanmamış vaat yazmak.** "%40 değer artışı", "son 3 daire" hem marka
   hem mevzuat riski → `references/mevzuat-ve-politika.md`.
