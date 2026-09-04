# Kırmızı Bayraklar ve Doğrulama Testleri

Bu dosya "neyin yanlış olduğunu bulma" dosyasıdır. Bir raporun değeri, kurucunun
söylemediklerini bulabilmesiyle ölçülür. Her bulguyu **kanıtıyla** yaz — suçlama değil gözlem.

## İçindekiler
1. Şişirilmiş metrik testleri
2. Ölü / ölmekte olan ürün işaretleri
3. Ekip ve yönetişim bayrakları
4. Tüzel, hukuki ve KVKK riskleri
5. Teknik borç ve maliyet bayrakları
6. Satıcı tarafı oyunları (satın alırken)
7. Alıcı tarafı oyunları (satarken)
8. Yeşil bayraklar

---

## 1. Şişirilmiş metrik testleri

**Takipçi/İndirme testi.** `IG takipçi ÷ toplam indirme`. Bir sosyal üründe bu oran 1'i
belirgin aşıyorsa iki açıklama var: takipçi organik değil, veya hesap ürüne dönüşüm
üretmiyor. Hangisi olduğunu gönderi etkileşimine bakarak ayır: 50.000 takipçili bir hesapta
gönderi başına 100 beğeni (%0,2) satın alınmış takipçiye işaret eder; 3.000 beğeni (%6)
gerçek ama dönüşmeyen kitleye.

**Yorum/İndirme testi.** `Play yorum ÷ Play indirme`. %0,5-2 normal. %0,1 altı: indirenler
uygulamayı açmıyor. %5 üstü: teşvikli/organik olmayan yorum.

**Puan dağılımı testi.** Gerçek bir ürünün puan dağılımı U şeklindedir (çok 5, biraz 1, az orta).
Sadece 5 yıldız ve hiç 1-2 yıldız yoksa, özellikle düşük hacimde, yorumlar toplanmıştır.
Tersine, App Store'da 5,0 ortalama + 27 puan gibi bir tablo "arkadaş çevresi puanlaması"nın
klasik imzasıdır — bunu Play tarafındaki daha düşük ve dağınık puanla karşılaştır.

**Yorum tarih yığılması.** Yorumların çoğu 2-3 haftaya sıkışmışsa bir kampanya vardır;
o dönem dışındaki organik akış gerçek talebi gösterir.

**Yorum dili testi.** Aynı kalıpla yazılmış, kısa, jenerik övgüler ("Mükemmel", "Harika app")
ve profil adlarının benzerliği. Buna karşılık uzun, spesifik, kusur da içeren yorum gerçektir.

**"X üniversitede/şehirde/ülkede varız" iddiası.** Ürün içinde bunu doğrula: gerçekten
o kurumlarda içerik akıyor mu, yoksa liste sadece kayıt formunda mı? Boş bölge, var olan
bölge değildir.

**Kayıtlı vs aktif.** "100.000 kullanıcı" neredeyse her zaman kümülatif kayıttır. MAU sor.
MAU verilmiyorsa raporda bunu `[Y]` yaz ve değer aralığını genişlet.

**Ödüller ve programlar.** Hızlandırma programı, "yılın girişimi" ödülü, demo day katılımı
traksiyon değildir. Rapora yazılır ama değere çevrilmez.

## 2. Ölü / ölmekte olan ürün işaretleri

- Son store güncellemesi **6 aydan eski** (mobilde 12 ay = terk edilmiş sayılır; OS güncellemeleri kırar)
- Sosyal hesaplarda son gönderi 3+ ay önce
- Ürün içindeki son kullanıcı içeriği aylar öncesine ait
- 1-2 yıldızlı yorumlara geliştirici cevabı yok
- Web sitesi telif yılı geçmiş yılda kalmış (`© 2025` — 2026'da)
- `web.archive.org` üzerinde site 1+ yıldır aynı
- LinkedIn'de çalışan sayısı düşüyor
- Domain veya SSL sertifikası yakında bitiyor / yenilenmemiş
- Destek e-postasına yanıt yok (kullanıcı test etmişse sor)

Bunlardan üç veya fazlası varsa değerleme "yürüyen işletme" değil "varlık satışı" olarak kurulur.

## 3. Ekip ve yönetişim

- Tek kurucu + teknik kurucu yok → ürün dışarıya bağımlı, devirde en kırılgan senaryo
- Kurucuların LinkedIn'de bu girişimi yazmaması veya "part-time" görünmesi
- Ekipte yüksek sirkülasyon (kısa süreli çıkışlar)
- Kurucular arası hisse dağılımı bilinmiyor / eşit olmayan katkıda eşit dağılım
- **Vesting yok** — devirde alıcı için ciddi risk
- Ana geliştirici ajans/freelancer ve sözleşmede fikri mülkiyet devri yok → **kod aslında şirketin değil**
- Kurucunun aynı anda 3 başka işi var
- Önceki girişimin kapanışı gizleniyor

## 4. Tüzel, hukuki, KVKK

- Marka tescili yok veya başka bir gerçek kişinin üstüne (devirde pazarlık konusu)
- Domain kurucunun kişisel hesabında
- Şirketin faaliyet kodu (NACE) yaptığı işle uyumsuz
- Play/App Store hesabı şirket değil şahıs adına → **devir zahmetli, bazen imkânsız**
- Veri güvenliği bölümünde "veriler şifrelenmiyor" → KVKK yaptırım riski + olgunluk sinyali
- KVKK aydınlatma metni, VERBİS kaydı, açık rıza akışı yok
- 18 yaş altı kullanıcı toplayan ürün ama yaş doğrulaması yok
- Ödenmemiş vergi/SGK, icra takibi (ticaret sicil ilanları ve UYAP kamu duyurularından kısmen görünür)
- Kullanıcı üretimli içerik var ama moderasyon politikası/aracı yok → yasal + itibar riski

## 5. Teknik borç ve maliyet bayrakları

**Altyapı gideri / aktif kullanıcı** oranı bu bölümün merkezidir.
```
Aylık bulut gideri ÷ tahmini MAU = kullanıcı başı aylık altyapı maliyeti
```
Basit bir TR sosyal/içerik uygulamasında bu rakam **kullanıcı başı 1-2 TL'yi aşmamalı**.
Aşıyorsa üç olasılık var, üçünü de raporda ayır:
1. Gerçek kullanım açıkladığından büyük (iyi haber — ama kanıt iste)
2. Mimari verimsiz: küçültülmemiş medya, sürekli çalışan büyük instance'lar, gereksiz managed servis, log israfı
3. Bulut hesabında bu ürün dışında başka yükler var (gider kalemi saf değil)

Olasılık 2 ise bu **alıcı için devraldıktan sonra ödenecek gizli fatura**dır ve doğrudan
fiyattan düşer. Aynı zamanda satıcı için en hızlı değer artırma fırsatıdır: giderin
yarıya inmesi, SDE çarpanıyla birlikte değeri katlar.

Diğer bayraklar:
- Rezerve edilmemiş, hep on-demand kaynak kullanımı
- Yazılım/lisans giderinin abartılı olması (kullanılmayan koltuklar, çift araç)
- CI/CD, test, hata izleme yok
- Tek kişi dışında kimsenin sistemi ayağa kaldıramaması ("bus factor = 1")
- Dokümantasyon yok
- Store'daki app boyutu kategorisine göre anormal büyük (optimize edilmemiş varlıklar)

## 6. Satıcı tarafı oyunları (sen alıcıysan dikkat)

- Gelir rakamının tek seferlik/ilişkili taraf işlemlerini içermesi
- Son 2-3 ayda pazarlamaya para basıp traksiyon eğrisini yukarı büken "makyaj çeyreği"
- Kritik müşterinin sözleşmesinin bitmek üzere olduğunun söylenmemesi
- Kurucunun satış sonrası kalacağını ima edip sözleşmeye yazdırmaması
- Giderlerin bir kısmının kurucunun şahsi hesabından ödenip P&L'de görünmemesi
  (gerçek maliyet göründüğünden yüksek)
- "Başka alıcı var, hızlı karar ver" baskısı

## 7. Alıcı tarafı oyunları (sen satıcıysan dikkat)

- Due diligence'ı uzatarak pisti tüketip fiyatı kırma
- Earn-out'un kontrolü alıcıya geçtikten sonra ulaşılamayacak hedeflere bağlanması
- Değerlemenin büyük kısmının nakit değil hisse/vadeli olması
- Münhasırlık (exclusivity) süresinin uzun olması — başka alıcıyla konuşmayı engeller

## 8. Yeşil bayraklar (dengeli rapor için bunları da ara)

- Organik, tarihe yayılmış, spesifik içerikli yorumlar
- 1 yıldızlı yoruma verilmiş özenli geliştirici cevabı
- Düzenli sürüm ritmi (ayda 1-3 sürüm) ve sürüm notlarının kullanıcı geri bildirimini yansıtması
- Küçük ama ödeyen müşteri kitlesi (para, takipçiden daha güçlü kanıttır)
- Sahip olunan dağıtım kanalı: e-posta listesi, kampüs temsilci ağı, topluluk, kurum anlaşması
- Ekipte alan içinde 5+ yıl geçirmiş kişi
- Şeffaflık: kurucunun kötü metrikleri kendiliğinden söylemesi — **en güçlü yeşil bayraktır**
