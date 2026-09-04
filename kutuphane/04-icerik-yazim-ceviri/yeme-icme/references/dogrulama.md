# Doğrulama — API anahtarı olmadan

Google Places API yok. Yorumlar tarayıcıdan okunuyor: Google Maps'te yeri aç,
yorumlar sekmesine geç, dile göre sırala. Yavaş ama yeterli — bu site ayda
onlarca değil birkaç yeme içme kaydı ekliyor.

**Anahtar eklenirse yöntem otomatikleşir, eşikler değişmez.**

---

## Kapı 1 — Varlık: hâlâ açık mı

Suriye'de bu ilk soru, ve genel rehberlerin sormadığı soru bu. Onarım, taşınma
ve el değiştirme yaygın; 2019 tarihli parlak bir yorum bugün kapalı bir kapıyı
anlatıyor olabilir.

**Eşik: son 12 ayda yazılmış, açık olduğunu gösteren en az iki bağımsız iz.**

İz sayılanlar:

- Son 12 aydaki bir Google yorumu (fotoğraflı olması güçlü sinyal)
- Yerin kendi sosyal medya hesabında son 6 ayda paylaşım
- Son bir yıl içinde yayımlanmış bir haber ya da blog yazısı

İz sayılmayanlar: yerin web sitesi (yıllarca güncellenmeden durur), rehber
sitelerindeki liste sayfaları (birbirinden kopyalanır), tarihsiz içerik.

**İki iz yoksa aday elenir.** "Muhtemelen açıktır" yazmak, okuru kapalı bir
kapıya göndermek demek.

---

## Kapı 2 — Kimlik: neden bir mekan

Sitenin ölçütü SKILL.md'de: kurum, deneyim, zanaat ya da kaynak olma. Bu
kapıda cevaplanacak tek soru:

> Bu yerin sayfasında, yemekten bağımsız olarak **ne anlatılacak?**

Cevap "yemekleri çok güzel"se aday elenir. Cevap "1885'ten beri aynı çarşıda ve
booza hâlâ tahta tokmakla dövülüyor"sa geçer.

---

## Kapı 3 — Somutluk ve yorum süzme

Burada Google yorumları okunur. **Yorum metni kopyalanmaz** — Google şartları
saklamayı kısıtlıyor ve zaten kopyalanan yorum arama motoruna yeni bir şey
vermiyor. On yorumdan çıkan ortak örüntü kendi cümlemizle yazılır. Doğrulama
eşiği **üç yorum**.

### Suriye kalibrasyonu

Genel rehberler "300–800 yorum, 4.2–4.7 puan" der. Bu eşikler turistik
başkentler için; Suriye'de hiçbir yeri geçirmez.

| Sinyal | Genel rehber | **Suriye'de** |
| --- | --- | --- |
| Yorum sayısı | 300–800 | **40+ kayda değer, 150+ güçlü** |
| Puan | 4.2–4.7 | Aynı — **4.9 şüphelidir**, 4.0 altı sorgulanır |
| Dil | Yerel dil yorumları | **Arapça yorumlar belirleyici** |
| Tazelik | Önemli | **Belirleyici** — bkz. Kapı 1 |

**Neden 4.9 şüpheli:** gerçek bir işletme memnuniyetsiz müşteri de toplar.
Kusursuz puan genelde ya çok az yorumdan ya da toplu yorumdan geliyor.

### Gerçek yorum neye benzer

Araştırmanın verdiği ayırt edici sinyaller:

| Gerçek | Sahte / değersiz |
| --- | --- |
| Yemeği adıyla anıyor | "Yemekler harikaydı" |
| Personelden, saatten, sıradan bahsediyor | Genel övgü, hiçbir ayrıntı yok |
| Kullanıcı fotoğrafı var (porsiyon, kalabalık, gerçek ışık) | Yalnızca işletmenin kendi kareleri |
| Olumsuz bir ayrıntı da var ("sıra uzundu") | Tamamen kusursuz |
| Hesabın başka yorum geçmişi var | Tek yorumluk hesap |

### Turist tuzağı işaretleri

- **Menü her şeyi kapsıyor.** Suriye mutfağı + pizza + burger. Hiçbirinde
  iddiası yok.
- **Anıtın kapısında.** Araştırmanın net bulgusu: simgesel yapıdan iki sokak
  uzaklaşınca fiyat belirgin düşüyor, yemek düzeliyor. Kapıdaki yer istisna
  olabilir ama **kanıt istemeli** — Bakdash gibi kurumlar istisnadır, sıradan
  bir lokanta değil.
- **Sokakta müşteri çağıran görevli.** Kendi başına yeten bir yer bunu yapmıyor.
- **Yorumların tamamı yabancı dilde.** Yerel hiç gitmiyorsa bir şey söylüyor.

### Yorumdan alana ne çıkar

| Yorumda geçen | Alan |
| --- | --- |
| "kişi başı X tuttu" (üç yorumda tutarlı) | `price_range` |
| "akşam yedide sıra kapıya taşıyordu" | `best_time`, `tips` |
| "sadece nakit" | `tips` |
| "üst katta oturulabiliyor" | `tips` |
| adı geçen belirli yemek | `signature` |
| "cuma kapalı" | `opening_hours` |

### Üç dilde tara

Aynı yerin farklı dillerdeki yorumları farklı şeyler söylüyor:

- **Arapça** — gerçek fiyat, gerçek kalabalık saati, yerelin ne yediği. En
  değerli kaynak ve genelde en çok göz ardı edilen.
- **İngilizce** — yabancı ziyaretçinin takıldığı yer: kart geçmiyor, menü
  çevirisi yok, konum bulunamıyor.
- **Türkçe** — Türkiye'den gidenin sorusu: porsiyon, acı seviyesi, fiyatın
  Türkiye'ye göre yeri.

---

## Yazılmayacaklar

- **Puan.** Sayfaya basılmaz: şartlar kısıtlıyor ve birkaç ayda eskiyor.
- **Yorum alıntısı.** Girdidir, içerik değildir.
- **Sıralama.** "En iyi 5" listesi yok; her kayıt kendi başına duruyor.
- **Emin olunmayan fiyat.** "Değişken — sorup öğren" dürüst ve kullanılabilir;
  yanlış fiyat güveni tek seferde bitiriyor.

## Anahtar eklenirse

`.env`'e `GOOGLE_PLACES_API_KEY` konursa yorum çekme otomatikleşir. Değişmeyen
iki şey:

1. **Yorum saklanmaz.** Kalıcı saklanabilen tek alan `place_id`.
2. **Üç kapı ve eşikler aynı kalır.** Otomasyon okumayı hızlandırır, ölçütü
   değiştirmez.
