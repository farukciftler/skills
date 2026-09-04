# Duyuru ve kanal bakımı

Videonun dışındaki her alan: topluluk gönderileri, oynatma listeleri, bitiş
ekranları, sabitlenmiş yorumlar, kanal düzeyi metinler ve düzen.

## 1. Topluluk (Community) gönderileri

### Önce erişimi doğrula

Topluluk sekmesi abone eşiğine bağlı — **son bilinen eşik 500 abone**, ama
YouTube bunu geçmişte iki kez değiştirdi. `studio.youtube.com/channel/<UC>/posts`
açılmıyor ya da "Gönderi oluştur" yoksa **eşik dolmamıştır**. Bu durumda:

1. Uydurma. "Gönderi geçtim" deme, sekmenin olmadığını söyle.
2. Duyurunun yerine geçen iki yol var ve ikisi de bugün çalışıyor:
   **sabitlenmiş yorum** (yeni yayının altında, önceki yayına bağlantı) ve
   **video açıklamasının ilk satırı**.
3. Kanal açıklamasındaki roster satırını güncelle — kalıcı duyuru orada.

### Ne zaman gönderi geçilir

| An | Gönderi | Neden |
|---|---|---|
| Yayın günü | Yeni yayın duyurusu, video bağlantısıyla | Bildirimi olan kesime ulaşır |
| Yayından ~7 gün sonra | Sanatçının şeridinden bir detay (enstrüman, makam, ritim) | Yayını değil kimliği anlatır; ikinci kez aynı bağlantıyı atmaz |
| Seri tamamlandığında | Seri özeti + playlist bağlantısı | Playlist'e trafik |
| Ölçüm sonrası | Sadece anlatılacak bir şey varsa | Boş gönderi sadık kesimi yorar |

**Sessizlik eşiği 14 gün.** `channel_report.py` bunu iş listesine düşürüyor.
Ama "gecikti" demek "bir şey uydur" demek değil — anlatacak bir şey yoksa
gönderi geçmemek doğru karardır, gerekçesi `channel_log.csv` notuna yazılır.

### Metin kuralları

- **İngilizce.** Bütün dinleyiciye bakan metin gibi.
- **İlk satır tek başına anlamlı olsun** — akışta gönderinin ilk satırı ve
  görseli görünür, gerisi "devamını oku" altında kalır.
- **Yer tutucu yok.** Adres yoksa satır açılmaz (`CLAUDE.md` § 4).
- **Künye satırı**, müziği plak gibi sunan her gönderide bulunur.
- **Sağlık iddiası yok** — fonksiyonel müzikte gönderi de açıklama kadar politikaya tabi (`healing-audio-youtube-seo/references/claims-and-policy.md`).
- **Etiket (hashtag) en fazla üç**, gönderinin sonunda.
- Uzunluk sınırını Studio'nun sayacından oku; şablonlar zaten kısa tutuluyor.

Görsel eklenecekse: albüm kapağı **kare** olduğu için akışta iyi duruyor —
video karesinden farklı olarak burada kapak doğru seçim. Thumbnail kullanma,
o videoya ait.

Şablonlar: `assets/community-post-templates.md`.

### Anket (poll)

Anket abone kesimini yoklamanın ucuz yolu ama **katalog kararını ankete
bağlama**. Şerit kilidi dinleyici oyuyla değişmez. Anket sorusu meşru olduğu
yer: hangi şehir/seri sırası, hangi uzunluk (30 dk / 1 saat / 3 saat), hangi
saat diliminde yayın. Sonuç `channel_log.csv` notuna yazılır.

## 2. Oynatma listeleri

Playlist bu katalogda dekorasyon değil: aynı şeridin videolarını birbirine
bağlayan tek sinyal ve fonksiyonel müzikte oturumu uzatan asıl mekanizma.

**Mimari — üç eksen:**

| Eksen | Örnek | Ne zaman açılır |
|---|---|---|
| **Seri** | `Soul of Cities`, `One Hour` | Seri tanımlandığı an, ilk yayından önce |
| **Sanatçı** | `KUMBENGO — every release` | Sanatçının ikinci yayınında |
| **İşlev** | `One Hour of Sleep Music`, `Focus` | Aynı işleve hizmet eden üçüncü videoda |

`releases.csv` `series` alanı seri playlist'in kaynağıdır — playlist adı oradan
türer, keyfî değil.

**Playlist alanları:**
- **Ad** İngilizce, arama ifadesini taşır (playlist'ler de aranıyor).
- **Açıklama** ilk cümlede ne olduğunu söyler; künye satırı playlist açıklamasında da bulunur.
- **Sıralama** manuel: en güçlü giriş videosu başta. Kronoloji değil.
- Her yeni yayın **en az bir** playlist'e girer; hangisi(leri) `channel_log.csv`'ye `playlist` tipiyle yazılır.

## 3. Bitiş ekranı ve kartlar

Bitiş ekranı videonun **son 5–20 saniyesine** konur. Bir saatlik albümde bu,
müziğin sönümlendiği yere denk gelir — sorun değil, ses zaten bitiyor.

| Öğe | Bu katalogda |
|---|---|
| Video öğesi | "İzleyiciye en uygun" — algoritma seçsin; sabit video seçmek uzun formatta kötü çalışıyor |
| Abone ol öğesi | Her videoda, sağ altta |
| Oynatma listesi öğesi | Videonun ait olduğu seri playlist'i |

Kartlar (`i` simgesi) uzun formatta **kullanılmaz**: bir saatlik müzikte
ortada beliren kart dinleyiciyi kaçırıyor. Kısa yayınlarda (single) tek kart,
önceki yayına, videonun ortasında.

Filigran zaten kanal düzeyinde ayarlı ve "tüm video boyunca" görünüyor
(`docs/brand/youtube-channel.md` § 1).

## 4. Sabitlenmiş yorum

Her yayında bir tane, yayın günü. İçeriği:

1. Ne dinlediği — bir cümle, albümün iddiası.
2. Bölüm listesi kısayolu ya da öne çıkan parça zamanı (varsa).
3. Önceki/ilgili yayına bağlantı — playlist bağlantısı tercih edilir.

Künye satırı burada tekrarlanmaz (açıklamada zaten var); yeni bir iddia da
üretilmez.

## 5. Yorumlar

- **Yanıtlanır**, otomatik değil seçerek: müzikle ilgili gerçek yorumlar, soru soranlar, kullanım anlatanlar ("bunu çalışırken açtım").
- **Yanıt İngilizce**, kısa, etiketin sesiyle — abartılı teşekkür ve emoji yığını yok.
- **AI hakkında soru dürüstçe cevaplanır.** Kayıtlar AI destekli ve insan yönetimli; künye satırı zaten bunu söylüyor, yorumda da aynısı söylenir. Savunmaya geçme, gizleme.
- **Spam/bot yorumu** bildirilir; **silme** geri alınamaz iş sınıfında, Faruk'un onayı gerekir.
- Yanıtlanan yorum sayısı ve konusu `channel_log.csv`'ye `reply` olarak tek satır özet — her yoruma satır açma.

## 6. Kanal düzeyi alanlar

Kaynak `docs/brand/youtube-channel.md`; oradaki metin gerçek, Studio ondan
doldurulur. Bu skill kanalı değiştirdiğinde **o dosyayı da günceller** — iki
yerde iki farklı gerçek olmaz.

| Alan | Kural |
|---|---|
| **Ad / handle** | Kilitli. Değişimi geri alınamaz iş sınıfında. |
| **Açıklama** | Roster satırları yayınla birlikte büyür; sınır 1000 karakter. Künye satırı kısaltılamaz. |
| **Kanal anahtar kelimeleri** | Yeni tür/sanatçı geldikçe genişler. |
| **Bağlantılar** | İlki banner üstünde görünür — sıralama karar gerektirir, `youtube-channel.md` § 4'te açık. |
| **İletişim e-postası** | Açık karar; Faruk'a sormadan doldurulmaz. |
| **Banner / avatar / filigran** | Script çıktısı (`docs/brand/logo/weave/youtube.py`). Elle başka görsel yüklenmez. |
| **Kanal düzeni** | Yeni ziyaretçiye fragman, dönen ziyaretçiye öne çıkan video; altta seri playlist'leri sırayla. |

Kanal düzeyinde yapılan her değişiklik `channel_log.csv`'ye `branding` ya da
`settings` tipiyle girer ve `docs/brand/youtube-channel.md` aynı işte güncellenir.
