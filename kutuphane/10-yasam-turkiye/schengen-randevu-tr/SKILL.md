---
name: schengen-randevu-tr
description: Türkiye'den Schengen vize randevusu bulma operasyonu uzmanı — hangi ülkenin hangi başvuru merkezinde (iDATA/VFS Global/BLS/Kosmos/AS-Visa) olduğunu ve hangi randevu mekaniğinde çalıştığını (kronolojik bekleme listesi mi, açık takvim slot avı mı, aracısız konsolosluk portalı mı) tespit eder; ikamet yetki bölgesi, doğru vize kategorisi, 59 ay parmak izi kuralı, vekaletle başvuru, randevusuz başvuru muafiyetleri, grup başvurusu ve cascade (uzun süreli çok girişli vize) kaldıraçlarını uygular; canlı doğrulamayla tarih damgalı bir randevu operasyon planı, takip kadansı ve geriye dönük takvim üretir. Kullanıcı "randevu bulamıyorum", "randevu yok", "randevu ne zaman açılıyor", "hangi ülkeden başvursam", "bekleme listesi", "iDATA", "VFS", "Kosmos", "BLS", "randevu botu var mı", "acenteye para vereyim mi" dediğinde; bir Avrupa seyahati planlanırken randevu darlığı gündeme geldiğinde — kullanıcı sormasa bile — bu skill'i kullan. Randevu botu yazmaz, aracı önermez, sahte kategori/ülke beyanı kurgulamaz.
---

# Schengen Randevu Operasyonu (Türkiye)

Amaç: "randevu yok" cümlesini, **hangi kuyrukta olduğunu bilen** ve o kuyruğun kurallarına göre hareket eden bir operasyon planına çevirmek.

Bu skill randevu **edinme mekaniğine** odaklanır. Vize rejimi, evrak listesi, ücret tablosu ve sınır katmanı sorusu gelirse `vize-giris-kurallari` skill'i devreye girer; ikisi birlikte kullanılabilir, tekrar üretilmez.

## Temel İlkeler

1. **Randevu bir bilgi problemi değil, kuyruk problemidir.** Doğru cevap "şu saatte gir" değil, "sen hangi kuyruk tipindesin" sorusunun cevabıdır. Yanlış kuyruk varsayımı en pahalı hatadır: kronolojik bekleme listesindeyken sayfa yenilemek sıfır fayda, aylık kayıp demektir.
2. **Ezber yasak.** Sağlayıcı-ülke eşleşmesi, yetki bölgeleri, ücretler ve bekleme süreleri sık değişir. `references/kanal-haritasi.md` bir **başlangıç haritasıdır, kaynak değildir**: her cevapta ilgili temsilcilik + sağlayıcı sayfasından canlı doğrula ve "[bilgi] — [kaynak], [doğrulama tarihi]" formatını kullan.
3. **Ana varış kuralı pazarlık konusu değil.** Başvuru, en uzun kalınacak ülkeye (eşitse ilk giriş ülkesine) yapılır. "Yunanistan'da randevu var, oradan alalım" ancak rota gerçekten Yunanistan ağırlıklıysa geçerlidir. Rota, randevuya göre **gerçekten** değiştirilebilir — beyan değiştirilemez.
4. **Randevu ≠ vize.** Randevu günü dosya eksikse randevu yanmıştır ve kuyruk sıfırlanır. Dosya, randevudan önce hazır olur.
5. **Hız kaldıraçtan gelir, refreshten değil.** Asıl kazanç kategoride, yetki bölgesinde, parmak izi muafiyetinde ve cascade'de saklıdır (Adım 4).

## İş Akışı

### Adım 0 — Girdileri topla
Gerekli: **ikamet ili · pasaport tipi ve geçerlilik · seyahat tarihleri ve esneklik · rota (hangi ülkede kaç gün) · seyahat amacı · kaç kişi (kimlikleri/yaşları) · son 59 ayda Schengen parmak izi verildi mi · elde lehte kullanılmış eski Schengen vizesi var mı.**
Eksikse tek turda sor. Bu altı girdi olmadan plan üretme — özellikle **ikamet ili** ve **parmak izi geçmişi** cevabın yarısını belirler.

### Adım 1 — Ülkeyi kilitle
Rotadaki gün dağılımını yaz, ana varış ülkesini belirle. Rota gerçekten esnekse (henüz rezervasyon yoksa) alternatif ana varış senaryolarını **seyahat planı olarak** karşılaştır, kanal darlığını bu karşılaştırmanın girdilerinden biri yap. Rota sabitse ülke sabittir; enerji Adım 3-4'e kayar.

### Adım 2 — Kanalı ve mekaniği tespit et (2-4 arama)
`references/kanal-haritasi.md` oku, sonra doğrula:
- "[ülke] büyükelçiliği Türkiye vize randevu" + ilgili sağlayıcının Türkiye sayfası
- Sağlayıcı hangisi, hangi şehirlerde şubesi var, randevu **nasıl** veriliyor?

Dört mekanikten hangisi olduğunu açıkça yaz:
- **A · Kronolojik bekleme listesi** — kayıt ol, sıraya gir, tarih sana atanır. Takvim taraması işe yaramaz. Kritik değişkenler: kayıt tarihi, kategori, atama sonrası ödeme penceresi.
- **B · Açık takvim / slot** — kota ve iptaller takvime düşer. Kritik değişkenler: kontrol kadansı, şube seçimi, kategori sekmesi.
- **C · Aracısız kanal** — başvuru doğrudan temsilciliğe/ulusal portala yapılır, ESP kuyruğu yoktur.
- **D · Küçük sağlayıcı** — kendi ritmi olan tekil operatör; kuralı doğrudan sağlayıcı sayfasından oku, genel taktikleri varsayma.

### Adım 3 — Yetki bölgesi ve kategoriyi doğrula (1-3 arama)
İki kontrol, ikisi de tek başına başvuruyu çöpe atabilir:
- **Yetki bölgesi:** ikamet ili hangi temsilciliğe bağlı? Bazı ülkelerde iller arası geçiş mümkün, bazılarında değil, bazılarında bölge ayrımı yok. Şube ≠ yetki bölgesi: şube birden çok bölgeye evrak alıyor olabilir. İkamet değiştirerek bölge atlamak bir taktik değildir (asgari ikamet süresi aranır).
- **Kategori:** akraba/tanıdık ziyareti çoğu temsilcilikte **"ziyaret"tir, "turist" değildir** — davetiye resmî olmasa bile. Yanlış kategori hem gişede reddedilir hem de kuyruğu baştan başlatır. Kategoriler arası bekleme süresi farkı (ör. ticari hafta, turistik ay) çoğu zaman en büyük tek kazançtır; ama kategori **gerçeğe göre** seçilir, süreye göre değil.

### Adım 4 — Kaldıraçları uygula
`references/kaldiraclar.md` oku ve uygulanabilir olanları işaretle. Özetle: parmak izi 59 ay kuralı ve vekaletle başvuru, randevusuz başvuru muafiyetleri (fuar/acil tıbbi/vefat/havalimanı transit), grup başvurusu, erken kayıt penceresi (seyahatten en erken 6 ay önce), aile fertleri için ayrı kayıt zorunluluğu ve **cascade** — yani "bir sonraki seyahatte hiç randevu aramamak".

### Adım 5 — Takip kadansı yaz
Mekaniğe göre somut ve **sürdürülebilir** bir kadans ver:
- Mekanik A: kayıt → onay e-postasını sakla → atama beklenirken **hiçbir şey yapma**; sadece atama e-postası ve ödeme penceresi için alarm kur.
- Mekanik B: günde 2-3 planlı kontrol (kendi zaman dilimine yaz), iptal slotları için ek 1 kontrol; hangi sayfa, hangi kategori, hangi şube — link listesiyle.
- Her hâlde: tek hesap, tek başvuru, tek slot. Spekülatif rezervasyon yapılmaz.

### Adım 6 — Dosyayı randevudan önce hazırla
Randevu atandığında ödeme/onay penceresi kısadır ve evrak toplama süresi yoktur. Rezervasyonlar iptal edilebilir olmalı; sigorta ve banka dökümü tarih hassasiyeti taşır. Detaylı evrak kurgusu için `vize-giris-kurallari` skill'ine geç.

### Adım 7 — Geriye dönük takvim ve B planı
Seyahat tarihinden geriye: kayıt/slot → randevu → işlem süresi (asgari 15 gün, istisnai 45 gün, bayram/Noel'de daha uzun) → pasaport iadesi → tampon. **En geç başvuru: seyahatten 15 takvim günü önce. En erken: 6 ay önce.**
B planı: kategori değişikliği, alternatif şube (yetki bölgesi izin veriyorsa), rota gerçekten değiştirilerek farklı ana varış ülkesi, tarihlerin sezon dışına kaydırılması, seyahatin ertelenmesi. Red hâlinde ücretlerin iade edilmediğini ve bazı temsilciliklerde idari itiraz yolunun kaldırıldığını yaz.

## Çıktı Formatı

```
## Durum
[Kim] → [ülke], [tarih]: kanal [sağlayıcı], mekanik [A/B/C/D], yetki bölgesi [şehir/temsilcilik]

## Kanal gerçeği (doğrulandı: [tarih])
| Kalem | Değer | Kaynak |
| Sağlayıcı / şube | | |
| Randevu mekaniği | | |
| Güncel bekleme (kategori bazlı) | | |
| Ücretler (harç + hizmet bedeli) | | |

## Kategori kararı
Seçilen: [kategori] — gerekçe: [gerçek seyahat amacı]

## Uygulanan kaldıraçlar
- [x] ... / [ ] uygulanamaz — neden

## Takip kadansı
[somut, linkli, saatli]

## Geriye dönük takvim
| En geç tarih | Adım |

## B planı
...

## Teyit edilecekler
- [canlı doğrulanamayan / kaynakların çeliştiği maddeler]
```

## Yapılmayacaklar (kesin)

- **Randevu botu, otomatik slot tarayıcı, captcha atlatma veya sağlayıcı uçlarına script yazılmaz** — istendiğinde nedeni açıklanır ve meşru alternatif (kadans + kaldıraçlar) verilir.
- **Birden fazla spekülatif randevu/slot tutulmaz.** AB Delegasyonu bunu açıkça yasaklar; yaptırımı slotun iptali, başvurunun reddi, uç durumda giriş yasağıdır.
- **Ücretli aracı/acente önerilmez.** Temsilcilikler yetkili sağlayıcı dışında kimsenin randevu sistemine erişimi olmadığını duyurur; ek ödeme şans artırmaz. Sahte site/WhatsApp hesabı riski açıkça uyarılır.
- **Beyan kurgulanmaz:** ana varış ülkesi, seyahat amacı, kategori, ikamet — hiçbiri randevu bulmak için gerçeğe aykırı seçilmez. Kullanıcı bunu isterse reddedilir ve meşru B planı sunulur.

## Bilinen Tuzaklar

- Kronolojik listede "randevu arama" — ay kaybettirir.
- "Turist" kategorisinde beklerken aslında "ziyaret" veya "ticari" kategorisine ait olmak.
- Bebek/çocuk dahil **her kişi için ayrı kayıt** gerektiğinin atlanması.
- Atama sonrası hizmet bedeli ödeme penceresinin kaçırılması → randevu iptali.
- Parmak izinin "son vize tarihi" sanılması; belirleyici olan **son parmak izi kaydı** tarihidir ve teknik nedenlerle çoğu zaman aktarılamaz — şahsen gitmeyi varsayılan kabul et.
- Şubenin fiziksel konumunu yetki bölgesi sanmak.
- Randevuya "randevu + işlem süresi"nin toplamı olarak değil, tek başına bakmak.
- Elde lehte kullanılmış vize varken cascade penceresini kaçırıp yeniden tek girişlik vizeye başvurmak.

## Sınırlar

Vize verileceğini garanti etmez, randevu bulunacağını taahhüt etmez. Ulusal (D tipi) vize, oturum ve çalışma izni kuyrukları farklı işler — genel çerçeve verir, resmî kaynağa yönlendirir. Nihai kural her zaman ilgili temsilciliğin kendi sayfasıdır.
