---
name: ceviri
description: ComeSyria içeriğini Türkçe, küresel İngilizce ve Suriye Arapçası arasında çevirir — makine kokmayan, o dilin okuru için baştan yazılmış metinler üretir; ad/sayı sadakatini ve yapay zekâ tikliklerini betikle denetler. "çevir", "çeviri yap", "İngilizceye çevir", "Arapçaya çevir", "Türkçeye çevir", "translate", "çeviriyi denetle", "çeviri kalitesi", "dil versiyonu ekle", "hreflang eksik", "Arapça sürüm" dendiğinde kullan.
---

# ComeSyria çeviri

Bu beceri üç dil arasında çeviri yapar: **Türkçe**, **küresel İngilizce**,
**Suriye Arapçası**. Ölçüt tek: metin o dilde yaşayan birinin elinden çıkmış
gibi okunmalı. Çevrilmiş gibi bile durmamalı — makine çevirisi gibi hiç.

## Temel ilke

Çevirdiğin şey kelime değil, **etki**. Kaynak cümle okurda ne yapıyorsa hedef
cümle de onu yapmalı; aynı sırayla, aynı uzunlukta, aynı yapıyla olması hiç
gerekmiyor.

Pratik karşılığı: kaynak metni bir kez oku, kapat, hedef dilde **yeniden yaz**,
sonra sadakat için kaynağa dön. Cümle cümle ilerlemek — ekranın solunda kaynak,
sağında hedef — makine kokusunun bir numaralı sebebi. Cümle sınırları kaynağın
sınırları olmak zorunda değil: Türkçe bir cümle İngilizcede ikiye bölünür,
Arapçada üçe.

Değişmez ölçüt: **yüksek sesle oku.** Nefes almak için yanlış yerde durmak
zorunda kalıyorsan cümle hedef dilin cümlesi değil, kaynağın cümlesi.

## Bu üç dil ne demek

| Dil | Ne kastediliyor |
| --- | --- |
| `tr` | Yazı Türkçesi. Ne resmî yazışma, ne sosyal medya. İyi bir gazete/dergi Türkçesi. |
| `en` | **Küresel** İngilizce. Ana dili İngilizce olmayan okur da rahat okumalı. Amerikan deyimi, spor benzetmesi, kültür göndermesi yok. |
| `ar` | **Suriye Arapçası.** Gövde modern fasih, damar Şamî. Aşağıda ayrıntısı var. |

### Arapçada register kararı

En kritik karar bu ve yanlış tarafa düşmek metni ya kitabî ya da ciddiyetsiz
yapıyor. Kural:

- **Gövde metni: modern fasih (MSA).** Klasik değil, gazete fasihçesi — kısa
  cümle, az bağlaç, süs yok. Enab Baladi ölçüsü.
- **Yerel her şey için Şamî sözcük.** Yer, yemek, zanaat, eşya, gündelik nesne
  Suriyelinin dediği gibi yazılır. Mısır ya da Körfez sözcüğü kullanmak, bir
  Suriye rehberinde en çok sırıtan hata.
- **Alıntı, replik, resim altı: gerçek Şamî.** Birinin ağzından bir şey
  aktarıyorsan onu fasihe çevirme; söylediği gibi yaz.

Ayrıntı ve sözcük listesi: `references/arapca.md`.

## Önce oku

Çeviriye başlamadan üç dosya:

- `references/adlar.md` — **yer ve özel ad sözlüğü.** Buraya bakmadan tek bir
  yer adı yazma. En sık ve en utandırıcı hata burada: Türkçe "Halep"i İngilizce
  metinde "Halep" bırakmak, ya da "Şam"ı "Sham" diye çevirmek.
- `references/<hedef-dil>.md` — o dile özgü tuzaklar.
- `wp/plugins/comesyria-content/includes/fields.php` — hangi alan var, hangi
  alan çevrilir.

## Alan alan ne yapılır

Bir kayıt tek bir metin değil; her alanın kendi kuralı var.

| Alan | Ne yapılır |
| --- | --- |
| `title` | Çevrilir. Marka adı **eklenmez** — ön yüz `%s · ComeSyria` şablonunu kendi uyguluyor. |
| `slug` | **Çevrilmez, yeniden türetilir.** Her dilde o dilin okuru için: `sam` / `damascus` / `dimashq`. ASCII, küçük harf, tire. Arapça slug Latin harfle yazılır — Arap harfli yol paylaşımda yüzde kodlamasına dönüp okunmaz oluyor. |
| `excerpt` | Yeniden yazılır, çevrilmez. 150–160 karakter hedefi **dile göre kayar** (bkz. aşağısı). Arama sonucunda görünen metin bu. |
| `content` | Çevrilir. H2/H3 yapısı korunur — ama başlıkların **metni** yeniden yazılır, birebir çevrilmez. |
| `subtitle` | Yeniden yazılır. Künye satırı: "Halep · 12. yüzyıl" → "Aleppo · 12th century" → "حلب · القرن الثاني عشر". |
| `tips`, `highlights` | Çevrilir. Madde sayısı korunur. |
| `entry_fee`, `opening_hours` | **Sayı ve para birimi aynen kalır.** Yalnızca çevresindeki kelime çevrilir: "1500 SYP" sabit, "pazartesi kapalı" → "closed Mondays". |
| `lat`, `lng`, `duration`, `distance`, `population` | **Hiç dokunulmaz.** |
| `address`, `period` | Çevrilir; ad sözlüğüne uyulur. |
| `featured_media`, `gallery` | **Kaynaktaki kimlik aynen kopyalanır.** Ayrıntı aşağıda. |

### Görseller: her dilde aynı, kimliği kopyala

Bir kaydın çevirisi **aynı fotoğrafı** kullanır. Yeniden yükleme yapılmaz,
başka bir kare seçilmez: aynı yerin İngilizce sayfasında farklı bir fotoğraf
olması siteyi üç ayrı site gibi gösteriyor.

Teknik olarak bu zaten mümkün, çünkü Polylang'in medya çevirisi **kapalı**
(`media_support: false`). Yani bir ek (attachment) bütün dillerde ortak; aynı
kimlik her dilde aynı dosyayı veriyor.

Pratik kural:

```
kaynak: "featured_media": 14   →   çeviri: "featured_media": 14
kaynak: "gallery": [43,44,45]  →   çeviri: "gallery": [43,44,45]
```

`cek.mjs` bu kimlikleri fişin `sabit` bloğuna koyuyor; oradan olduğu gibi
kopyala.

> **Kopyalamayı unutmak sessiz bir hata.** Kayıt yayımlanıyor, hiçbir uyarı
> çıkmıyor, ama çeviri sayfası kapak görselsiz kalıyor ve ön yüz onu tipografik
> karta düşürüyor. Sitede şu an tam olarak bu olmuş durumda: `damascus` ve
> `dimashq` kayıtlarında görsel yok, Türkçe `sam` kaydında var. `denetle.mjs`
> artık bunu yakalıyor.

**`alt` metni dile göre değişemiyor.** Medya çevirisi kapalı olduğu için `alt`
ekin üstünde duruyor (`_wp_attachment_image_alt`) ve tek bir değer üç dilde de
okunuyor. Yani çeviri kaydında `alt` yazmanın bir anlamı yok — yazarsan
kaynağın alt metnini eziyorsun. Bunu değiştirmek Polylang'de medya çevirisini
açmayı gerektirir; açılmadıkça alt metin Türkçe kalır.

### Özet uzunluğu dile göre

Aynı bilgi üç dilde aynı yeri kaplamıyor. 150–160 karakter kuralı Türkçe için
yazılmıştı; diğerlerinde hedef şu:

| Dil | Karakter | Neden |
| --- | --- | --- |
| `tr` | 150–160 | Referans. Eklemeli yapı yüzünden kelime sayısı az, karakter çok. |
| `en` | 150–160 | Aynı. |
| `ar` | 130–150 | Arapça aynı anlamı daha az karakterle taşıyor; 160'a zorlamak metni sulandırıyor. |

## Akış

### 1. Kaynağı çek

```bash
node .claude/skills/ceviri/scripts/cek.mjs --type place --slug halep-kalesi --lang tr
```

Çeviri fişi (JSON) döner: çevrilecek alanlar, aynen kalacak alanlar, ve kaynak
kaydın `id`'si — çeviri bağını kurarken lazım olacak.

### 2. Çevir

Metni yeniden yaz. Fişteki `sabit` bloğunu **kopyala, dokunma**.

### 3. Yayımla ve bağla

`icerik-uret` becerisinin betiği kullanılır; ayrı bir yayın betiği yok:

```bash
node .claude/skills/icerik-uret/scripts/wp-post.mjs ceviri.json \
  --translation-of <kaynak-id>
```

Bağ kurulmazsa hreflang etiketleri eksik kalır, dil değiştirici ana sayfaya
düşer ve üç dil arama motoruna birbirinin kopyası gibi görünür.

### 4. Denetle

```bash
node .claude/skills/ceviri/scripts/denetle.mjs kaynak.json ceviri.json
```

Betik iki şeye bakar:

- **Sadakat** — kaynaktaki her sayı, fiyat, saat ve koordinat çeviride duruyor
  mu; H2 sayısı, madde sayısı, bağlantı sayısı tutuyor mu.
- **Yapay zekâ tiklikleri** — hedef dile göre yasak kalıp listesi, cümle
  uzunluğu tekdüzeliği, bağlaç yoğunluğu.

Uyarı çıkarsa **düzelt, gerekçelendirme.** Betik tek tek kalıpları biliyor ama
metnin tamamını okuyamıyor; temiz rapor iyi çeviri demek değil, sadece bilinen
hataların yok olması demek.

## Yapay zekâ kokusu — ortak tiklikler

Dile özgü olanlar referans dosyalarında. Üçünde de geçerli olanlar:

1. **Tekdüze cümle uzunluğu.** Makine hep 15–25 kelimelik cümle yazıyor. İnsan
   yazısında dört kelimelik cümle de var, kırk kelimelik de. Ritim değişmezse
   metin okunmuyor, akıyor — ve okur bunu fark ediyor.
2. **Gereksiz bağlaç.** "Ayrıca", "bununla birlikte", "moreover", "علاوة على
   ذلك". İki cümle arasındaki ilişki çoğu zaman zaten belli; söylemek onu
   zayıflatıyor.
3. **Üçlü liste hastalığı.** "Tarihi, kültürü ve mutfağıyla." Her şeyin üç
   sıfatı olmaz. İkiyi kes, bazen bir yeter.
4. **Yastık ifadeler.** "Şunu belirtmek gerekir ki", "it is worth noting",
   "من الجدير بالذكر". Sil; altındaki cümle zaten oradaydı.
5. **Nominalleştirme.** Fiili isme çevirmek: "restorasyonun gerçekleştirilmesi"
   yerine "restore edildi". Makine isim yığar, insan fiil kullanır.
6. **Turizm sloganı.** "Eşsiz", "büyüleyici", "unutulmaz", "hidden gem",
   "must-visit", "vibrant". Bu site somut yazıyor: fiyat, saat, kaç dakika
   sürdüğü. Sıfat değil bilgi.
7. **Her mecazı olduğu gibi taşımak.** Kaynaktaki deyim hedef dilde yoksa
   karşılığını bul, tercüme etme. Yoksa at — düz cümle, sakat mecazdan iyi.

## Çevirinin sadakat sınırı

Çeviri kopya değil ama **serbest yazı da değil.** Şunlar korunur:

- Her sayı, tarih, fiyat, mesafe, süre.
- Her özel ad (ad sözlüğündeki karşılığıyla).
- Bilginin doğruluğu. Kaynakta olmayan bir bilgi eklenmez — üç dilin biri
  fazladan bir iddia taşıyorsa hangisinin doğru olduğu belli olmaz.
- H2 yapısı, yani yazının iskeleti.

Şunlar korunmaz, korunmamalı:

- Cümle sınırları ve sırası.
- Paragraf uzunluğu.
- Deyimler ve mecazlar.
- Okurun bildiği varsayılan şeyler. **Türk okur "Şam" der geçer; İngiliz okur
  Damascus'un nerede olduğunu bilir ama Bab Şarki'yi bilmez; Suriyeli okur
  ikisini de bilir ama neden anlattığını merak eder.** Aynı paragraf üç dilde
  farklı yerde açıklama ister.

## Sık yapılan hatalar

- **Yer adını çevirmemek ya da uydurmak.** `references/adlar.md` var, bak.
- **Slug'ı kopyalamak.** Üç dilde aynı slug varsa çeviri bağı kurulsa bile
  adresler ayırt edilemez hale geliyor.
- **Özeti çevirmek.** Özet ayrı bir metin türü; kaynağın özeti hedef dilde iyi
  bir özet olmuyor.
- **Arapçaya Mısır sözcüğüyle yazmak.** En sık yakalanan ve en çok sırıtan hata.
- **Arap rakamı kullanmak.** Ön yüz Latin rakam basıyor (`ar-u-nu-latn`);
  gövdede ١٥٠٠ yazarsan sayfa iki rakam sistemi karıştırıyor. **1500 yaz.**
- **Sayıyı düşürmek.** "1500 SYP" çeviride kaybolursa okur fiyatı hiç görmüyor.
  Denetim betiği bunu yakalar; yakalamadan önce yapma.
