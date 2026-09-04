# Web Sitesi — UI / UX

Site henüz yok: `moonstoneresidence.com` alan adı 26 Ocak 2026'da GoDaddy'den
alınmış, ad sunucuları `NS1/NS2.FIRMADOSTU.COM`, ancak A kaydı yok — yani hiçbir
şey yayında değil. Bu bir dezavantaj değil, temiz sayfa: doğru kurulursa
teknik borç ve göç maliyeti oluşmaz.

## İçindekiler
1. Sitenin tek işi
2. Site mimarisi
3. Sayfa şablonları
4. Tasarım sistemi
5. Kritik bileşenler
6. Dönüşüm ve lead akışı
7. Performans bütçesi
8. Erişilebilirlik
9. Teknoloji seçimi
10. Yayına alma sırası
11. Ölçüm

---

## 1. Sitenin tek işi

Bir konut projesi sitesi bir "kurumsal site" değildir. Tek işi vardır:
**nitelikli bir ziyaretçiyi satış ofisiyle temasa geçirmek.** Her tasarım
kararı bu soruya cevap vermeli: bu öğe, ziyaretçiyi telefona/forma bir adım
yaklaştırıyor mu, yoksa sadece güzel mi duruyor?

Ziyaretçinin karar vermek için ihtiyacı olan üç şey — sırayla: **ne** (tip, m²,
oda), **nerede** (konum ve ulaşım), **kim** (yapan firma güvenilir mi). Site bu
üçünü kaydırma mesafesinde vermeli. Ne kadar sürer? Mobilde 30 saniye.

## 2. Site mimarisi

Kimlik çalışmasındaki 8 ikon zaten navigasyon iskeletini öneriyor. Ona uy:

```
/                       Ana sayfa
/proje                  Proje Detayları — konsept, mimari, teknik özellikler
/daire-planlari         Tip 1–6, mahal listeleri, interaktif kat/tip seçici
/sosyal-alanlar         Yaşam Tarzı — havuz, spor salonu, spa
/ticari-alanlar         3.000 m² ticari alan — yatırımcı odaklı ayrı ürün
/lokasyon               Harita, ulaşım, çevre  [DOĞRULA: mesafeler]
/insaat-sureci          İnşaat Süreci — ilerleme galerisi, tarihli
/hakkimizda             Ayhanlar Mimarlık Yapı ve İnşaat  [DOĞRULA: referans projeler]
/iletisim               İletişim — form, harita, satış ofisi
/galeri                 Render ve görseller
/blog                   İçerik SEO'su (seo.md'ye bak)
/kvkk  /gizlilik  /cerez-politikasi
```

**URL kuralları:** Türkçe karakter kullanma (`daire-planlari`, `dairé-planları`
değil), tire ile ayır, kısa tut, sonradan değiştirme. Yayına almadan önce URL
şemasını kesinleştir — sonradan değişen URL SEO'da en pahalı hatadır.

Navigasyon **7 öğeyi geçmesin**; ticari alanlar, blog ve kurumsal alt sayfalar
menüde ikinci seviyeye ya da altbilgiye insin. Menünün sağında sabit bir
**"Randevu Al"** düğmesi dursun.

## 3. Sayfa şablonları

### Ana sayfa (yukarıdan aşağı)

1. **Kahraman:** Tam ekran gece render'ı, üzerinde koyu degrade, koyu zemin
   logosu, H1 olarak slogan, alt satırda somut künye (`1+1 – 3+1 · Tuzla
   Aydıntepe · 3.000 m² ticari alan`), iki buton: birincil "Randevu Al",
   ikincil "Daire Planları". Sağ altta köşede "temsili görseldir".
2. **Künye şeridi:** 4 rakam — daire tipi sayısı (6), en küçük/en büyük m²,
   ticari alan (3.000 m²), sosyal alan sayısı (3). Rakam + altın ince çizgi +
   Cormorant başlık.
3. **Konsept:** Katalogdaki ilk paragraf + tek büyük render. Krem zemin.
4. **Daire tipleri:** 6 kart, her kartta tip adı, oda, net/brüt m², minik plan
   görseli, "İncele" bağlantısı. Yatay kaydırma değil, ızgara — karşılaştırma
   yapılabilsin.
5. **Sosyal alanlar:** 3 öğe (havuz, spor salonu, spa), koyu zemin, altın ikonlar.
6. **Ticari alanlar:** Yatırımcıya ayrı çağrı; farklı zemin rengiyle ayrılmış.
7. **Lokasyon:** Harita + ulaşım listesi. `[DOĞRULA: mesafeler]`
8. **Ayhanlar güvencesi:** Kısa kurumsal blok, "Ayhanlar Mimarlık Yapı ve
   İnşaat Güvencesiyle..." cümlesi burada yaşar.
9. **İletişim:** Form + telefon + satış ofisi adresi + harita.

Bölüm zeminleri lacivert ↔ krem arasında dönüşümlü olsun; katalog ritmi bu.

### Daire planları sayfası

Bu sitenin **en çok bakılan sayfası** olacak — burada emek harca.

- Üstte filtre: oda sayısı (1+1 / 2+1 / 3+1) ve m² aralığı.
- Her tip için: büyük plan görseli (yakınlaştırılabilir), mahal listesi tablosu,
  net/brüt, hangi katta, "Bu tip için bilgi al" düğmesi (tip bilgisi forma
  otomatik geçsin).
- Plan görselleri PDF'ten yüksek çözünürlükte çıkarılmalı; SVG'ye çevrilebilirse
  daha iyi (keskin ve hafif).
- Mobilde plan görseli tam genişlik + çift dokunuşla yakınlaştırma.
- Yazdırılabilir / PDF indirilebilir tek sayfalık tip föyü sun — satış ofisine
  gitmeden önce insanlar bunu indirir, e-posta karşılığı istemek meşru bir
  lead kapısıdır.

### İnşaat süreci sayfası

Güvenin en ucuz kanıtı: **tarihli fotoğraf.** Ay ay ilerleme galerisi kur
(`Ocak 2026`, `Şubat 2026` …). Bu sayfa aynı zamanda siteyi düzenli
güncelleyen tek mekanizma olur — SEO ve sosyal medya içeriği buradan doğar.

## 4. Tasarım sistemi

Renk ve font token'ları için `marka-kimligi.md`'ye bak; burada düzen kuralları:

- **Izgara:** 12 sütun, azami içerik genişliği 1280px, metin bloklarında 720px.
- **Boşluk ölçeği:** 4px tabanlı — 8, 12, 16, 24, 32, 48, 64, 96, 128.
  Bölüm arası dikey boşluk masaüstünde 96–128px. **Cömert boşluk markanın
  kendisidir**; sıkışık düzen prestiji öldürür.
- **Köşe yarıçapı:** 0 veya 2px. Yuvarlak köşeler bu markaya yabancı — mimari
  keskin ve dikey.
- **Gölge yerine çizgi.** Kartları ayırmak için `1px solid rgba(184,153,47,.25)`
  altın ince çizgi kullan; materyal tarzı yumuşak gölge kullanma.
- **Hareket:** yavaş ve az. Geçişler 250–400ms, `ease-out`. Kaydırmada beliren
  öğeler için 16px yukarı + opaklık; parallax, sayaç animasyonu, otomatik
  oynayan slider kullanma. `prefers-reduced-motion` mutlaka desteklensin.
- **Düğmeler:** Birincil — altın degrade zemin, lacivert metin. İkincil —
  şeffaf zemin, 1px altın kontur, altın metin (koyu zeminde). Yükseklik 48px,
  yatay iç boşluk 32px, `letter-spacing: .08em`, tümü büyük harf.

## 5. Kritik bileşenler

Rakip incelemesinden gelen üç zorunluluk (ayrıntı: `rakip-analizi.md`):
**mobil sabit aksiyon çubuğu**, **"Sizi Arayalım" mantığı** (form doldurtmak
yerine geri arama sözü) ve **çalışan `tel:` / `wa.me` bağlantıları**. Üçü de
Türk konut sitelerinde standart; üçüncüsü çoğunda bozuk.

| Bileşen | Not |
|---|---|
| Yapışkan üstbilgi | Kaydırmada arka planı `rgba(4,12,29,.92)` + blur, yüksekliği küçülsün |
| Mobil sabit alt çubuk | "Ara" · "WhatsApp" · "Randevu Al" — mobil dönüşümün çoğu buradan gelir |
| Daire tipi kartı | Tip, oda, net/brüt m², kat, mini plan, CTA |
| Plan görüntüleyici | Yakınlaştır/kaydır, mahal listesiyle senkron |
| Galeri ışık kutusu | Klavye ile gezilebilir, `alt` metinleri dolu |
| İletişim formu | Bölüm 6 |
| WhatsApp düğmesi | `https://wa.me/902125303020?text=...` — ön dolu metinle |
| Harita | Lazy yüklenen gömme; ilk yüklemede statik görsel, tıklayınca canlı harita (performans ve KVKK için) |
| Çerez izni | **Gerçek reddetme düğmesi olan**, alt şerit biçiminde (ilk ekranı yutmasın); analitik betikler onaydan önce çalışmasın. Rakiplerde sık görülen "sadece Kabul Et" kutusu KVKK açısından savunulamaz. |
| Tip karşılaştırma tablosu | Altı tipi süzülebilir tek ekranda karşılaştırma. İncelenen altı rakip sitede yok — bu projenin en yüksek getirili tasarım kararı. |

## 6. Dönüşüm ve lead akışı

Form alanları **az** olsun. Her ek alan doldurma oranını düşürür:

```
Ad Soyad*        Telefon*        E-posta
İlgilendiğim tip (seçmeli, tip sayfasından otomatik dolar)
Mesaj (isteğe bağlı)
[ ] KVKK aydınlatma metnini okudum, kişisel verilerimin işlenmesini kabul ediyorum*
[ ] Ticari elektronik ileti almak istiyorum   (ayrı kutu, ön işaretli DEĞİL)
```

- Yıldızlı üç alan yeterli. E-postayı zorunlu yapma — bu segmentte insanlar
  telefon bırakır.
- Telefonu `tel` klavyesiyle al, maskeleme yap, sunucu tarafında doğrula.
- **Spam koruması:** görünmez honeypot alanı + oran sınırlama. CAPTCHA koyma,
  dönüşümü düşürür.
- Gönderim sonrası **teşekkür sayfasına yönlendir** (`/tesekkurler`) — dönüşüm
  ölçümü ve reklam pikseli için ayrı URL şart.
- Lead nereye düşecek? En az: satış ofisi e-postası + WhatsApp bildirimi. Bir
  CRM varsa oraya. Bu akış test edilmeden site yayına alınmaz — çalışmayan form
  reklam bütçesini yakar.
- **Yanıt süresi hedefi 5 dakika.** Konut alıcısı aynı gün 4-5 projeye form
  bırakır; ilk arayan kazanır. Bunu kullanıcıya söyle, teknik bir mesele değil
  ama sitenin başarısını en çok belirleyen değişken bu.

## 7. Performans bütçesi

Render fotoğrafları ağırdır; bu sitenin en büyük riski budur.

| Ölçüt | Hedef |
|---|---|
| LCP (mobil, 4G) | < 2,5 sn |
| INP | < 200 ms |
| CLS | < 0,1 |
| Ana sayfa toplam ağırlığı | < 1,5 MB |
| JS (sıkıştırılmış) | < 150 KB |

Kurallar:
- Görselleri **AVIF + WebP** ver, JPEG'i yedek bırak. Kahraman görselini
  `fetchpriority="high"`, geri kalanı `loading="lazy"`.
- `srcset` ile en az 3 boy (640 / 1280 / 1920) sun.
- Her `<img>` için `width` ve `height` yaz — CLS'nin ana kaynağı bu.
- Fontlar: `display=swap` + `preconnect`. Sadece kullanılan ağırlıkları yükle.
- Otomatik oynayan arka plan videosu **koyma**; mobilde LCP'yi ve veri
  kullanımını mahveder. Gerekiyorsa poster görselli, sessiz, tıklayınca oynayan.
- Katalog PDF'i 16 MB — siteye doğrudan koyma. Sıkıştırılmış ve sayfalara
  bölünmüş sürüm hazırla, indirmeyi form arkasına koy.

## 8. Erişilebilirlik

Yasal zorunluluk olmasa da bu segmentte alıcı kitlesinin yaş ortalaması yüksek;
erişilebilirlik doğrudan dönüşümdür.

- Altın metni açık zeminde gövde metni olarak kullanma (bkz. `marka-kimligi.md`
  kontrast bölümü) — 2,9:1, AA'nın altında.
- Odak halkası görünür olsun: `outline: 2px solid var(--ms-gold); outline-offset: 2px`.
- Tüm görsellerde anlamlı `alt`. Dekoratif olanlarda `alt=""`.
- Form etiketleri `<label>` ile bağlı; hata mesajları renk dışında metinle de
  belirtilsin.
- Dokunma hedefleri en az 44×44px.
- `lang="tr"` kökte tanımlı olsun — ekran okuyucu ve arama motoru için.

## 9. Teknoloji seçimi

Öneri: **Next.js (App Router) + Tailwind + statik/ISR üretim, Vercel'de.**
Gerekçe — bu site içerik ağırlıklı ve nadiren değişir; statik üretim en hızlı
LCP'yi ve en düşük maliyeti verir. Görsel optimizasyonu, form uç noktası ve
önizleme dağıtımları hazır gelir.

Alternatif: WordPress. Satış ekibi içeriği kendi güncelleyecekse ve teknik
destek yoksa savunulabilir; karşılığında performans ve güvenlik bakımı gelir.
Ad sunucularının bir web ajansına (firmadostu.com) işaret etmesi, ajansın
WordPress planlıyor olabileceğini düşündürür — **karar verilmeden önce mevcut
ajansla ne konuşulduğunu netleştir.** İki taraflı iş yapılırsa para ve zaman
iki kere harcanır.

İçerik yönetimi gerekiyorsa başsız CMS (Sanity/Payload) + Next.js iyi bir orta yol.

## 10. Yayına alma sırası

1. Alan adı DNS'i doğru sunucuya yönlendir, `www` → köke (ya da tersi) tek
   kanonik biçimde 301'le.
2. SSL, HSTS, `www`/HTTPS zorlaması.
3. Kurumsal e-posta doğrulaması: **SPF, DKIM, DMARC**. `info@` adresine düşen
   lead'lerin spam'a gitmemesi buna bağlı.
3b. **Altbilgi künyesi ve hukuki metinlerde ticari unvan kullanılır:**
   *Ayhanlar Mimarlık, Yapı İnşaat Ltd. Şti.* — pazarlama adı değil. KVKK
   aydınlatma metnindeki veri sorumlusu da bu unvandır. Vergi dairesi, vergi/
   MERSİS ve ticaret sicil numaraları `[DOĞRULA]`.
4. Analitik + dönüşüm izleme (bkz. bölüm 11), çerez izniyle uyumlu.
5. Search Console ve Bing Webmaster doğrulaması, site haritası gönderimi.
6. Form uçtan uca testi — gerçek telefonla, gerçek e-postayla.
7. Yayın öncesi tüm sayfalarda `[DOĞRULA:]` yer tutucularını tara; hiçbiri
   kalmasın.

## 11. Ölçüm

Kurulacak asgari set: GA4 + Google Search Console + sunucu tarafı form kaydı.
Meta ve Google reklamı planlanıyorsa Meta Pixel / Google Ads etiketi.

İzlenecek olaylar:
`form_gonderildi` · `telefon_tiklandi` · `whatsapp_tiklandi` · `plan_indirildi`
· `tip_detay_goruntulendi` (tip parametresiyle) · `galeri_acildi` ·
`randevu_al_tiklandi`

Anlamlı ana ölçüt **oturum başına iletişim oranı** ve **lead başına maliyet**.
Sayfa görüntüleme sayısı bu projede gösteriş metriğidir; kullanıcıya raporlarken
öne çıkarma.
