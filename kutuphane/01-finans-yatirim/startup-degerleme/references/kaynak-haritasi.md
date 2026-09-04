# Kaynak Haritası — Hangi veri nereden

Aşağıdaki sıra, "en yüksek kanıt değeri / en az çaba" sırasıdır. Yukarıdan başla.

## İçindekiler
1. Tüzel kişilik ve şirket kaydı (TR)
2. App store verisi
3. Web ve trafik
4. Sosyal medya
5. Kullanıcı sesi (şikayet, forum, sözlük)
6. Yatırım ve ekosistem veritabanları
7. Ekip ve kişi araştırması
8. Rakip bulma
9. Teknik iz sürme

---

## 1. Tüzel kişilik ve şirket kaydı (TR)

**En hızlı yol tüzel adı bulmak**: App Store ürün sayfasındaki **"Sağlayıcı" / "Provider"**
alanı tam ticari unvanı verir (ör. "UNIVVE SOSYAL MEDYA VE REKLAM TICARET LIMITED SIRKETI").
Play Store'daki geliştirici adı genelde kısaltmadır, iOS daha güvenilirdir.
Alternatif: web sitesinin KVKK / Aydınlatma Metni / Mesafeli Satış Sözleşmesi sayfaları —
unvan, adres, MERSİS ve vergi dairesi çoğu zaman oradadır.

| Kaynak | Ne verir | Not |
|---|---|---|
| `ticaretsicil.gov.tr` (TTSG ilan arama) | Kuruluş ilanı, sermaye artışı, ortak değişikliği, adres, tasfiye | Ücretsiz; ilan tarihleri zaman çizelgesi çıkarmak için altın değerinde |
| MERSİS (`mersis.ticaret.gov.tr`) | Unvan, MERSİS no, faaliyet kodu | Kısmen kayıt ister |
| `find.com.tr`, `firmasec.com`, benzeri dizinler | Kuruluş tarihi, adres, NACE, sermaye | Otomatik derlenmiş; **maskeli/placeholder rakam basabilirler** — 1234567890 gibi bir değer görürsen o alanı `[Y]` say |
| İlgili Ticaret Odası üye sorgu | Üyelik, faaliyet | Şehre göre değişir |
| KAP (`kap.org.tr`) | Halka açık/ilişkili ise finansal tablo | Erken aşamada nadiren işe yarar |
| Patent/Marka (`turkpatent.gov.tr` arama) | Marka tescili var mı, kimin üstüne, başvuru tarihi | Marka tescilsizse bu bir devir riski; rapora yaz |
| Domain WHOIS (`who.is`, `nic.tr` sorgu) | Domain kayıt tarihi | Şirket kaydından önce/sonra olması pivot veya hazırlık dönemini gösterir |

**Kuruluş tarihi ↔ ürün yayın tarihi farkı** her zaman yorumlanır. Örnek: şirket Aralık 2023,
uygulama Eylül 2024 → ~9 ay geliştirme, makul. Şirket 2021, uygulama 2025 → arada ne oldu, sor.

## 2. App store verisi

Bunları `scripts/app_store_cek.py` otomatik çeker; elle gerekirse:

**iOS — resmî, JSON, güvenilir:**
```
https://itunes.apple.com/lookup?id=<APPID>&country=tr
```
Verir: `trackName`, `sellerName` (tüzel ad!), `averageUserRating`, `userRatingCount`,
`releaseDate` (ilk yayın), `currentVersionReleaseDate`, `version`, `price`, `genres`,
`fileSizeBytes`, `minimumOsVersion`, `screenshotUrls`, `description`.

**iOS yorumları (ülke bazlı, RSS):**
```
https://itunes.apple.com/tr/rss/customerreviews/page=1/id=<APPID>/sortby=mostrecent/json
```
Sayfa 1-10 arası çekilebilir. Tarihli, puanlı, tam metinli yorumlar verir.

**Google Play:** resmî API yok. Ürün sayfasını tarayıcıyla açıp metnini al
(`play.google.com/store/apps/details?id=<PKG>&hl=tr&gl=TR`). Şunları not et:
indirme bandı, puan, yorum sayısı, "Güncellenme tarihi", "Yenilikler" metni, Veri güvenliği
bölümü (şifreleme yok = mühendislik olgunluğu düşük sinyali), geliştirici adı.
Ülke parametresini değiştirerek (`gl=DE` vb.) yurtdışı varlığı test edilir.

**Sürüm geçmişi (mühendislik nabzı):** `apps.apple.com/.../id<APPID>` sayfasındaki "Sürüm
Geçmişi", ya da `appfollow.io` / `apptopia` gibi izleyicilerin public sayfaları. Yoksa
sürüm numarası + ilk yayın tarihinden ortalama sürüm sıklığı türetilir
(ör. v1.0.27, 10 ayda → ~2,7 sürüm/ay = aktif ekip).

**İndirme tahmini için üçüncü taraflar:** Sensor Tower / data.ai / AppMagic / Appfigures
public sayfaları bazen bant verir. Ücretli veriye erişimin yoksa **tahmin ettiğini `[T]`
diye etiketle**, kesinmiş gibi yazma.

## 3. Web ve trafik

- Sitenin kendisi: fiyatlandırma sayfası olması gelir modelinin gerçekliğine dair en güçlü sinyaldir.
- `web.archive.org/web/*/<domain>` — sitenin geçmiş halleri. **Vaatlerin nasıl değiştiğini
  ve şirketin ne zamandır aynı sayfayı güncellemediğini gösterir.** Çok değerli, sık atlanır.
- Similarweb / Semrush public sayfaları: kaba ziyaret bandı. Küçük sitelerde "veri yok" çıkar,
  bu da bir bulgudur (aylık <5k ziyaret).
- `builtwith.com` veya sayfa kaynağı: analytics, ödeme, destek, reklam SDK'ları.
  **Ödeme sağlayıcısı (iyzico/Stripe/PayTR) izinin olması gerçek para akışına işarettir.**
- LinkedIn şirket sayfası: çalışan sayısı ve "yeni katılanlar" — ekip büyüyor mu küçülüyor mu.

## 4. Sosyal medya

Her platform için: takipçi, gönderi sıklığı, **son gönderi tarihi**, ortalama etkileşim
(beğeni ÷ takipçi; %1 altı ölü/şişkin hesap sinyali), yorumların gerçekliği.

Instagram, TikTok, X, LinkedIn, YouTube. TR gençlik ürünlerinde ağırlık Instagram + TikTok'tadır.

**Kritik çapraz kontrol:** takipçi sayısını indirme sayısıyla karşılaştır. Bir "sosyal uygulama"nın
50 bin takipçisi olup 1-5 bin indirmesi varsa, ya takipçi organik değildir ya da hesap
ürüne trafik çeviremiyordur. İkisi de raporda ilk sayfaya çıkar.

Bio'daki link ağacı (share.*, linktr.ee) bazen gizli sayfaları açar: temsilcilik başvurusu,
kampanya, iş ilanı, basın kiti.

## 5. Kullanıcı sesi

| Kaynak | Nasıl | Ne bulunur |
|---|---|---|
| Şikayetvar (`sikayetvar.com` arama) | Marka adı ara | Ödeme, iade, destek sorunları; şirket cevap veriyor mu |
| Ekşi Sözlük | `eksisozluk.com` başlık araması | Türk kullanıcının filtresiz görüşü; başlığın entry sayısı ve son entry tarihi ilgi seviyesini verir |
| Reddit | `site:reddit.com <marka>` | Özellikle r/Turkey, r/KGBTR |
| X / Twitter arama | `<marka> -from:<resmi hesap>` | Gerçek kullanıcı bahsi vs. sadece kendi tweetleri |
| Store yorumları | Aşama 4 | En yapılandırılmış kaynak |
| YouTube / TikTok | Marka adıyla arama | İnceleme videosu var mı, izlenme kaç |

## 6. Yatırım ve ekosistem veritabanları

- **startups.watch** — TR için en iyi kaynak; çoğu detay ücretli ama şirket sayfasının
  public kısmı yatırım olup olmadığını gösterir.
- **Webrazzi** (`webrazzi.com` site araması) — TR yatırım haberleri. Haber yoksa büyük
  ihtimalle kurumsal yatırım da yoktur.
- Crunchbase / Dealroom / Tracxn public profilleri.
- TÜBİTAK 1512/BiGG, KOSGEB, TEKNOPARK listeleri — hibe/kuluçka geçmişi. Hibe almış olmak
  hem küçük bir kalite sinyali hem de devirde **geri ödeme/taahhüt riski**dir; kontrol et.
- Melek yatırım ağları (Galata Business Angels, Keiretsu, TR Angels) portföy sayfaları.

## 7. Ekip ve kişi araştırması

- LinkedIn profilleri: geçmiş şirketler, süreler, gerçekten teknik mi, kaç kez kurucu olmuş.
- GitHub: kurucu/CTO'nun hesabı, commit sıklığı, şirket organizasyonu varsa repo aktivitesi.
- Basın/röportaj: `"<isim>" <marka>` araması; kurucunun kendi anlatımı hem vizyonu hem
  abartma eğilimini gösterir.
- Üniversite/kuluçka bağlantıları.
- Önceki girişimlerin **bugünkü durumu** — kapanmış mı, devam mı, satılmış mı. Kapanmış olması
  kötü değil; kapandığını gizlemesi kötü.

## 8. Rakip bulma

1. App Store ürün sayfası → "Beğenebilirsiniz" / "You Might Also Like" listesi (algoritmik, isabetli)
2. Play Store → "Benzer uygulamalar"
3. Play/App Store içi arama: ürünün ana anahtar kelimeleri
4. G2 / Capterra / Product Hunt (B2B ve global ürünlerde)
5. Google: `"<kategori>" alternatif OR benzeri OR rakip`

Bulduğun her rakip için **aynı metrik setini** topla, yoksa tablo kıyaslanabilir olmaz.

## 9. Teknik iz sürme (kayıt olmadan)

- Gizlilik politikası / veri güvenliği bölümü: hangi 3. parti servisler kullanılıyor
  (Firebase, OneSignal, Sentry, Mixpanel...). Yığını ve maliyet yapısını ele verir.
- Mobil app'in public API uçları: web sürümü varsa tarayıcı ağ sekmesinden görünür.
  **Sadece gözlemle** — kimlik doğrulama atlatma, yük bindirme, veri kazıma yapma.
- Uygulama boyutu ve min OS sürümü: teknoloji seçimi hakkında ipucu (React Native/Flutter/native).
- Store'daki "Veri şifrelenmiyor" ibaresi: ciddi bir olgunluk ve KVKK riski işaretidir, rapora yaz.
- Statü sayfası / dokümantasyon / API dokümanı varlığı: B2B ciddiyeti göstergesi.
