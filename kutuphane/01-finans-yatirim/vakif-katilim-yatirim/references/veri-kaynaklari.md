# Veri Kaynakları ve Doğrulama Protokolü

Bu skill'in değeri, katalogda ne yazdığında değil, **bugünün rakamını doğru getirmesinde**. Rakam içeren hiçbir cevabı aramadan verme.

## Kaynak önceliği

1. **Birincil — bankanın/kurucunun kendi sayfası.** vakifkatilim.com.tr (kampanyalar, duyurular, ücret tarifeleri, yardım merkezi), vakifkatilimportfoy.com.tr (fon sayfaları, izahname, TGO), vakifyatirim.com.tr (komisyon tarifesi PDF'i, aracılık koşulları).
2. **Resmî platform.** TEFAS (fon fiyat/getiri/portföy dağılımı), KAP (ihraç duyuruları), MKK e-Yatırımcı (kullanıcının kendi portföyü — sen göremezsin, kullanıcıya yönlendir), GİB (vergi).
3. **İkincil — haber ve karşılaştırma siteleri.** Yeni fon lansmanı, kampanya duyurusu gibi şeyleri hızlı yakalar ama **rakamı buradan alma**, sadece "böyle bir şey var mı" sinyali için kullan, sonra birinciden teyit et.
4. **Kullanma:** forum yorumu, şikâyet sitesi yorumu, tarihsiz blog. Şikâyet siteleri sadece "kullanıcılar nerede takılıyor" sinyali için okunur, oran kaynağı değildir.

## Soru → kaynak eşlemesi

| Soru | Nereye bak |
|---|---|
| Aktif kampanya var mı | vakifkatilim.com.tr kampanyalar + duyurular sayfası; ardından son 1 ay haber araması |
| Kâr payı oranı | Bankanın oranlar/katılma hesabı sayfası; farklı vadeler için ayrı ayrı |
| Fon getirisi / fiyatı / büyüklüğü | TEFAS fon detay sayfası (kod ile) |
| Fonun toplam gider oranı | Fon izahnamesi / yatırımcı bilgi formu, kurucu sitesi |
| Fon katılım kriterine uygun mu | İzahnamedeki fon tipi + `helal-yatirim-uzmani` skill'i |
| Hisse komisyonu | Vakıf Yatırım masraf/ücret/komisyon tarifesi PDF'i + banka kampanya sayfası |
| Altın/döviz kuru ve makas | Bankanın kur sayfası (alış ve satış ayrı ayrı, farkı hesapla) |
| Yeni ürün/fon çıkmış mı | KAP + kurucu sitesi + son 3 ay haber araması |
| Vergi/stopaj | GİB + bankanın yardım merkezi |
| Uygulama sürümü / yeni özellik | App Store ve Google Play sürüm notları |

## Arama kalıpları

Kısa ve spesifik tut, tarihi ekle:
- `Vakıf Katılım kampanya <ay> <yıl>`
- `Vakıf Katılım katılma hesabı kâr payı oranları`
- `Vakıf Katılım Portföy <FONKODU> TEFAS getiri`
- `Vakıf Yatırım hisse komisyon tarifesi`
- `Vakıf Katılım Portföy yeni fon <yıl>`
- `vakifkatilim.com.tr duyurular`

Bir sorgu boş dönerse aynı kelimelerle tekrar arama; terimi değiştir (ör. "kâr payı oranı" → "getiri oranları" → "hesap oranları") ya da doğrudan kurumun sayfasını çek.

## Doğrulama kuralları

- **Tarih damgası zorunlu.** Her rakamın yanına kaynağın tarihi. Tarihsiz sayfadan alınan rakam "tarihi belirsiz" diye işaretlenir.
- **Çelişki varsa banka kazanır.** Haber sitesi ile bankanın kendi sayfası çelişiyorsa bankayı yaz, çelişkiyi de bir cümleyle söyle.
- **Kampanya sayfasında yoksa kampanya yoktur diyemezsin.** Uygulamaya özel, kişiye özel ve şubeye özel kampanyalar web'de yayınlanmaz. Doğru cümle: "Web'de yayınlanan aktif kampanyalar şunlar; uygulamanın Kampanyalar/VClub ekranında sana özel tanımlı olanlar farklı olabilir, oradan da bak."
- **Bulamadıysan bulamadığını söyle.** Uydurulmuş bir kâr payı oranı, bu skill'in verebileceği en büyük zarardır.
- **Kullanıcının kendi verisi sende yok.** Bakiye, portföy, geçmiş işlem, kampanya uygunluğu — hepsi uygulamada. Yönlendir, tahmin etme.
