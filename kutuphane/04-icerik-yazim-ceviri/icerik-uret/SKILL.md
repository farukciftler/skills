---
name: icerik-uret
description: ComeSyria için üç dilde (TR/EN/AR) SEO uyumlu şehir, mekan ve rota içeriği üretir — anahtar kelimeyi dil dil araştırır, metni yazar, ticari kullanıma açık arşivlerden görsel bulup yükler, çeviri becerisiyle EN ve AR sürümlerini kurar ve üçünü bağlayarak yayımlar. Yemek yerleri için önce yeme-icme becerisini kullan. "içerik üret", "yeni şehir ekle", "mekan yaz", "rota oluştur", "içerik ekle", "SEO içerik", "üç dilde yayımla", "görsel bul", "kapak görseli", "Suriye içeriği" dendiğinde kullan.
---

# ComeSyria içerik üretimi

Bir kaydı baştan sona üretir: araştırma, metin, görsel, üç dil, çeviri bağı,
yayın, doğrulama. Elle WordPress paneline girmeye gerek kalmaz.

**Bir kayıt üç dilde yayımlanmadan iş bitmiş sayılmaz.** Türkçesi yayımlanıp
İngilizcesi sonraya bırakılan kayıt, dil değiştiriciyi kıran ve hreflang
sinyalini bölen yarım bir kayıttır.

## İçerik tipleri

Site dört tip taşıyor. Hikâye/haber tipi **kaldırıldı** — üretme.

| Tip | Klasör | Rolü | Ayrıntılı rehber |
| --- | --- | --- | --- |
| `city` | `content/cities/` | **Hub.** Bir şehrin giriş kapısı; mekan ve rotalara dağıtır. | `references/sehir.md` |
| `place` | `content/places/` | **Spoke.** Tek bir yer: cami, kale, çarşı, müze. | `references/mekan.md` |
| `route` | `content/routes/` | **Spoke.** Sıralı duraklardan oluşan güzergâh. | `references/rota.md` |
| `food` | `content/food/` | **Spoke.** Yeme içme yeri. Ayrı bölüm, mekan altında filtre değil. | **`yeme-icme` becerisi** |

**Yemek yerini bu beceriyle yazma** — önce `yeme-icme` becerisini aç. Orada
adayın sayfayı hak edip etmediğine karar veren süzgeç var ve alan kuralları
farklı: `entry_fee` boş kalır, `price_range` ve `signature` zorunludur,
`kind` değeri `restaurant`/`cafe`/`bakery`/`icecream`/`sweets` olur.

Ortak SEO doktrini: `references/seo.md`. Google yorumlarından bilgi çıkarma ve
harita bağlantıları: `references/google.md`. **Yazmaya başlamadan tipin kendi
dosyasını ve seo.md'yi oku** — tiplerin arama niyeti, başlık yapısı ve okur
sorusu birbirinden farklı ve bunları karıştırmak en sık yapılan hata.

**Dosya adı Türkçe slug olmalı.** Dışa aktarma dosyaları böyle adlandırıyor;
farklı adla yazarsan bir sonraki `--export` ikinci bir kopya üretir ve biri
kapak görselli, öbürü görselsiz kalır. Sessiz ve bulması zor.

## Alan şeması

`wp/plugins/comesyria-content/includes/fields.php`. Yeni alan icat etme —
şemada olmayan bir meta anahtarı REST'e düşmez ve ön yüz onu hiç görmez.

## Ses tonu

Davetkâr ama emir kipsiz. Somut, klişesiz. "Unutulmaz bir deneyim" değil,
"giriş 500 SYP, sabah ışığında avlu boş". Nostalji merakla bağlanır, yasla
değil.

Bu ton bir üslup tercihi değil, aynı zamanda **SEO ve AEO stratejisi**: yapay
zekâ arama motorları paragrafın içine gömülmüş izlenimi değil, çıkarılabilir
somut olguyu alıntılıyor. "Tarihi dokusuyla büyüleyen şehir" hiçbir sorguya
cevap vermiyor; "giriş 1500 SYP, kapı 09:00'da açılıyor" hem okura hem makineye
cevap.

## Akış

### 1. Anahtar kelimeyi **her dil için ayrı** belirle

En kritik adım ve en çok atlanan yer burası.

Türk okur *"halep gezilecek yerler"* aratıyor. İngiliz okur *"things to do in
Aleppo"*. Arap okur *"أماكن سياحية في حلب"*. Bunlar birbirinin çevirisi değil;
farklı sorgular, farklı beklenti, bazen farklı sıralama.

Bu yüzden:

- **Türkçe metni Türkçe niyete göre yaz.**
- **Çeviriyi o dilin niyetine göre yeniden çerçevele.** Başlık ve özet birebir
  çevrilmez; hedef dilin okurunun arattığı şeye göre yazılır.
- Gövde çevrilir, ama açıklama dozu değişir: Türk okur "Şam"ı bilir, İngiliz
  okur Bab Şarki'yi bilmez, Suriyeli okur ikisini de bilir.

Ayrıntı: `ceviri` becerisi ve `references/seo.md`.

### 2. Türkçe metni yaz

Tipin kendi rehberindeki iskeleti izle. Her tip için zorunlu:

- **Tek H1** (`title`), anahtar kelimeyi doğal taşır, marka adı yok — ön yüz
  `%s · ComeSyria` şablonunu kendisi uyguluyor.
- **Özet (`excerpt`) elle yazılır.** Meta açıklama bu; boş bırakılırsa gövdeden
  rastgele bir cümle kesiliyor ve sonuna `&hellip;` konuyor. Hedef uzunluk
  `denetle.mjs` ile aynı: **TR/EN 150–165, AR 125–155 karakter.** Arapça aynı
  anlamı daha az karakterle taşıdığı için hedefi ayrı. Uzun özet arama
  sonucunda ortadan kesiliyor, kısa özet yeri boş bırakıyor.
- **İlk paragraf** yazının tamamını özetler — ön yüz onu serif ve büyük basıyor.
- **H2'ler okurun sorusunu karşılar**, başlık değil soru mantığıyla kurulur.
- **Somut alanlar doldurulur.** Bunlar JSON-LD'ye düşüyor ve zengin sonuç
  kartını üreten şey bunlar.

### 2b. Mekan için Google yorumlarını tara

Yalnızca `place` tipinde ve **atlanmaması gereken** adım: ziyaret saati, giriş
ücreti, gerçek süre ve pratik ipuçlarının çoğu resmî kaynakta değil Google
yorumlarında. Üç dilde de tara — Arapça, İngilizce ve Türkçe yorumlar farklı
şeyler söylüyor.

**Yorum metnini kopyalama.** Google şartları saklamayı kısıtlıyor; ortak örüntüyü
kendi cümlenle yaz. Doğrulama eşiği üç yorum. Yöntem: `references/google.md`.

`google_place_id` alanını doldur — harita ve yol tarifi bağlantıları bundan
üretiliyor.

### 3. Görseli bul, gözle doğrula, depoya koy

**Görsel de depoda yaşar.** `content/media/` altında dosya, `content/media.json`
içinde anahtar. Dağıtım onları medya kitaplığına kendisi yüklüyor — WordPress'e
elle yükleme yapma, yoksa depo ile veritabanı ayrışır.

```bash
node .claude/skills/icerik-uret/scripts/gorsel-ara.mjs "Bab Antakiya Aleppo gate"
```

Betik Wikimedia Commons, Openverse ve Library of Congress'i tarar ve yalnızca
**ticari kullanıma açık** olanı döndürür (CC0, kamu malı, CC BY, CC BY-SA;
NC ve ND reddedilir). `pexels.mjs` duruyor ama Suriye anıtları için yetersiz —
yapıya özgü karesi yok.

Sonra sırasıyla:

1. **Gözle doğrula.** Dosyayı indirip **bak.** Ada bakarak karar verme:
   "Bab Sharqi" araması Kudüs'teki Şam Kapısı'nı döndürüyor ve otomatik seçim
   Kattina Gölü'ne bir İngiliz kanalı fotoğrafı getirmişti. Doğru yer olsa
   bile kare kullanılabilir mi diye bak — Bab Antakya'nın ilk sonucu kapıyı
   bir ağacın arkasında bırakıyordu, ikinci kare alındı.
2. `content/media/<anahtar>.jpg` olarak indir. Commons'ta **kendi `thumburl`'ünü**
   kullan (`iiurlwidth=1600`); elle thumb adresi kurma, uç keyfi genişlikte
   400 döndürüyor.
3. `content/media.json`'a `{ file, alt, credit, title }` ekle.
4. Kaydın `featured_media` alanına **anahtarı** yaz — sayısal kimlik değil.

**Doğrulanamıyorsa görsel koyma.** Yanlış fotoğraf görselsiz kayıttan kötüdür;
ön yüz görselsiz kartı zaten tipografik karta çeviriyor. Bunun yerine kayda
gerekçeli `gorselsiz` alanı yaz — envanter gerekçe görürse o kaydı bir daha
listelemez, gerekçesiz bayrağı ise hata sayar.

- **İngilizce ara.** Arşiv etiketleri İngilizce; "Şam camii" hiçbir şey bulmaz.
- **Somut ara.** "syria" genel manzara döndürür; "aleppo citadel stone wall"
  kullanılabilir kare döndürür.
- `alt` **her zaman** yazılır ve betimleyicidir. Dikkat: alt metin ek üzerinde
  duruyor ve **üç dilde ortak** — Polylang'de medya çevirisi kapalı. Yani alt
  metni bir kez, Türkçe yazılır.

### 4. Üç dili tek dosyada hazırla

`scripts/ornek-icerik.json` şemasına bak. Tek dosya, üç dil bloğu:

```json
{
  "type": "place",
  "status": "publish",
  "featured_media": "bab-antakya-halep-kapi",
  "city": "halep",
  "ortak": { "lat": 36.1995, "lng": 37.1626, "duration": 120, "kind": "gate" },
  "tr": { "slug": "...", "title": "...", "excerpt": "...", "content": "...", "fields": {} },
  "en": { "...": "..." },
  "ar": { "...": "..." }
}
```

`ortak` bloğu sayısal ve konumsal alanları taşır — üç dilde aynı, bir kez
yazılır. Görsel de ortak: çeviri **aynı fotoğrafı** kullanır.

**Görsele ve ilişkiye kimlikle değil anahtarla bağlan.** `featured_media`
medya anahtarını, `city` ve `stops` ise **Türkçe slug** taşır. Sayısal ek
kimliği kullanılsaydı veritabanı yeniden kurulduğunda her sayfa yanlış
fotoğrafı gösterirdi.

EN ve AR bloklarını yazarken **`ceviri` becerisini kullan.** Suriye Arapçası
register kararı, ad sözlüğü ve yapay zekâ tikliği listesi orada.

### 5. Yayımla

Yayın **depo üzerinden** yapılır. Dosyayı `content/` altına yaz, kuyruktaki
maddeyi `uretildi: true` yap, sonra:

```bash
git add -A && git commit -F mesaj.txt && git push
# sunucuda:
cd /root/projects/comesyriacontent && ./deploy.sh --content
```

> Commit mesajında **ters tırnak kullanma** — kabuk komut olarak çalıştırıyor
> ve bir kelime sessizce yeniyor. Uzun mesajı dosyaya yazıp `git commit -F`.

`deploy.sh` içe aktarmayı kendisi çalıştırır: üç kaydı açar, dilleri atar,
çeviri bağını kurar, `content/media/` altındaki görselleri medya kitaplığına
yükler ve **ilişkileri hedef dile yeniden eşler** — çevrilmiş bir mekan Türkçe
şehre değil İngilizce şehre bağlanır. Aynı slug ikinci kez gönderilirse yeni
kayıt açılmaz, mevcut kayıt güncellenir.

`web/` altında bir şey değiştiysen `--content` yerine `--build` kullan.

`scripts/yayimla.php` tek kaydı elle yayımlamak için duruyor ama olağan akış
bu değil: panelden ya da elle yapılan değişiklik `./deploy.sh --export` ile
depoya geri yazılmazsa bir sonraki dağıtım üzerine yazar.

> **Sıra önemli.** Şehir mekandan önce, mekan rotadan önce yayımlanır. Bağlanacak
> kayıt hedef dilde henüz yoksa betik uyarı verir ve ilişkiyi boş bırakır;
> eksiği tamamlayıp betiği tekrar çalıştırmak yeterli.

### 6. Denetle ve doğrula

```bash
node .claude/skills/ceviri/scripts/denetle.mjs kaynak.json ceviri-en.json
node .claude/skills/ceviri/scripts/denetle.mjs kaynak.json ceviri-ar.json
```

Sonra canlıda:

```bash
curl -s https://comesyria.com/tr/mekanlar/<slug> | grep -o '"@type":"[^"]*"'
curl -s https://comesyria.com/en/places/<slug-en> -o /dev/null -w "%{http_code}\n"
curl -s https://comesyria.com/sitemap.xml | grep -c '<loc>'
```

Kayıt yayımlandığında WordPress ön yüzü imzalı webhook ile kendiliğinden
tazeliyor; sayfa birkaç saniye içinde canlıda olmalı.

## Ortam

Anahtarlar depoda değil, sunucudaki `.env` dosyasında:

```
PEXELS_API_KEY=...
WP_ADMIN_USER / WP_ADMIN_APP_PASSWORD / WP_ADMIN_API_URL
```

`.env` asla commit edilmez.

## Sık yapılan hatalar

- **Tek dilde yayımlayıp bırakmak.** En sık ve en pahalı hata. Yarım kayıt,
  hreflang'i bölüyor ve dil değiştiriciyi ana sayfaya düşürüyor.
- **Başlığı ve özeti çevirmek.** Bunlar hedef dilin arama niyetine göre
  **yeniden yazılır**. Birebir çeviri, o dilde kimsenin aratmadığı bir başlık
  üretiyor.
- **Slug'ı kopyalamak.** Her dilde o dilin okuru için: `halep-kalesi` /
  `aleppo-citadel` / `qalaat-halab`.
- **Görsel kimliğini kopyalamayı unutmak.** Sessiz hata: kayıt yayımlanıyor,
  uyarı çıkmıyor, çeviri sayfası kapaksız kalıyor.
- **Özeti boş bırakmak.** Meta açıklama bozulur.
- **Şehir bağı kurmamak.** Mekan hiçbir şehir sayfasında görünmez.
- **Rota duraklarını mekana bağlamamak.** Durak listesi boş çıkar.
- **Koordinat girmemek.** `GeoCoordinates` düşer, zengin sonuç kartı çıkmaz
  ve sayfa haritasız kalır — koordinatı olan her kayıt dağıtımda üretilen
  gerçek bir OSM haritası alıyor (CLAUDE.md §5b), kayıt başına ek iş yok.
- **Hikâye/haber üretmek.** O tip kaldırıldı.
