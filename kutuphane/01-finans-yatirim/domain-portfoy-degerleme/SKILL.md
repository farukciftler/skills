---
name: domain-portfoy-degerleme
description: Elde tutulan alan adları için gerçekçi değer aralığı, tut/sat/bırak kararı ve satış planı üreten domain portföy uzmanı — birden çok değerleme aracının çapraz okunması, NameBio benzeri gerçek satış karşılaştırmaları, marka/ticari marka çakışması taraması, geçmiş kullanım ve spam mirası kontrolü, yenileme maliyetine karşı taşıma maliyeti hesabı, pazaryeri ve fiyatlama stratejisi, registrar/DNS taşıma prosedürü. Kullanıcı "bu domain ne eder", "domainimi satsam mı", "elimde şu alan adları var", "yenilesem mi bıraksam mı", "domain değerleme", "nereye listeleyeyim", "Afternic", "Sedo", "domain transfer", "EPP kodu", "registrar değiştirmek", "bu ismi alsam mı", "marka çakışması var mı" dediğinde kullan. Yeni bir proje için isim/alan adı seçilirken de devreye gir. Değeri ASLA ezberden söyleme; her tahmin canlı araç sorgusu ve karşılaştırmalı satış verisiyle desteklenir, tek bir aracın rakamı gerçek sayılmaz. Yatırım tavsiyesi değildir.
---

# Domain Portföy Değerleme & Karar

Amaç: elde duran ya da alınması düşünülen alan adları için **savunulabilir bir değer aralığı**, net bir tut/sat/bırak kararı ve uygulanabilir bir satış/taşıma planı üretmek.

## Temel İlkeler

1. **Tek araç = tek görüş.** Otomatik değerleme araçları aynı domaine 10 kat fark verebilir. Asla tek rakam sunulmaz; en az 3 kaynak + gerçek satış karşılaştırması ile **aralık** verilir.
2. **Gerçek satış > algoritma.** Karşılaştırılabilir satış verisi (comps) her zaman algoritmik tahminden ağır basar. NameBio türü satış arşivi bir "değerleme aracı" değildir; **kanıt kaynağıdır** ve asıl referanstır.
3. **İki fiyat vardır.** "Vitrin fiyatı" (retail, alıcı gelirse) ile "hızlı satış fiyatı" (30 gün içinde likidite) farklıdır ve genelde arada 3-10 kat vardır. Her çıktıda ikisi de gösterilir.
4. **Likidite acı gerçektir.** Ortalama bir domainin yıllık satılma olasılığı düşüktür. "Değeri X TL" cümlesi, "X TL'ye alıcı bulunur" anlamına gelmez. Bu her raporda açıkça yazılır.
5. **Ezber fiyat yasak.** Her sorguda araçlar ve comps canlı aranır, tarih damgası konur.

## İş Akışı

### Adım 0 — Portföyü topla
Her domain için: **ad · TLD · kayıt tarihi (yaş) · registrar · yıllık yenileme bedeli · aktif kullanım var mı · trafik/backlink durumu · duygusal bağ.** Kullanıcı liste verdiyse eksikleri tek soruda topla; bilinmiyorsa WHOIS/araç üzerinden tahmin edilir ve "tahmin" etiketlenir.

### Adım 1 — Değer taraması (domain başına 2-4 arama)
`references/araclar.md` dosyasını oku. Her domain için:
- En az **üç** otomatik değerleme kaynağı (ör. Estibot, GoDaddy Appraisal, Afternic tahmini, Humbleworth, Atom, Dynadot) — hangileri aktifse
- **Comps:** "[anahtar kelime] domain sold price", NameBio araması, benzer uzunluk/TLD/anlamdaki satışlar
- TLD çarpanı: .com dışı uzantılarda değer belirgin düşer; yeni gTLD'lerde comps çok daha seyrektir

### Adım 2 — Nitel puanlama
`references/araclar.md` içindeki kriter setiyle her domaini puanla: uzunluk, telaffuz edilebilirlik, hece sayısı, ticari niyet taşıyan anahtar kelime, tire/rakam varlığı, dil pazarı (Türkçe domain'in alıcı havuzu dar ama niş), yaş ve geçmiş.

### Adım 3 — Risk taraması (1-2 arama/domain)
- **Ticari marka çakışması:** TÜRKPATENT ve/veya WIPO/USPTO araması. Çakışma varsa satış değeri değil, **hukuki risk** konuşulur (UDRP).
- **Geçmiş kirlilik:** Wayback Machine ile eski kullanım; spam, kumar, yetişkin içerik geçmişi SEO değerini sıfırlayabilir.
- **Blacklist/itibar:** domain daha önce ceza yemiş mi?

### Adım 4 — Karar matrisi
Her domain için **TUT / SAT / GELİŞTİR / BIRAK** kararı ve tek cümlelik gerekçe.
- Yıllık yenileme × kalan bekleme süresi = taşıma maliyeti. Bunu tahmini satış değeri ve satış olasılığıyla karşılaştır.
- Aktif projede kullanılan domain kural olarak TUT — değerleme burada "marka varlığı" olarak okunur, satış adayı olarak değil.
- Yıllardır boş duran, comps'u zayıf, marka riski taşıyan domain BIRAK adayıdır.

### Adım 5 — Satış / taşıma planı (satılacaklar için)
- **Pazaryeri seçimi:** Afternic/GoDaddy (Dan.com 2024'te Afternic'e katıldı), Sedo, Atom. Fast Transfer ağına dahil olma, komisyon oranları ve ödeme yöntemleri karşılaştırılır → canlı doğrula.
- **Fiyatlama:** vitrin fiyatı + "make offer" eşiği + kiralama/taksitli satış (LTO) seçeneği.
- **Lander:** satılık sayfası, iletişim, minimum teklif.
- **Doğrudan alıcı:** aynı isimle çalışan şirketler taranır; soğuk temas metni yazılır (aşırı ısrarcı olmadan, fiyatı önce onlara sormadan).
- **Taşıma prosedürü:** registrar kilidi kapatılır → EPP/auth kodu istenir → DNSSEC varsa kaldırılır → yeni registrar'da transfer başlatılır → onay e-postası hızlıca tıklanır (tıklanmazsa süreç 5 iş günü bekler) → transfer 7 güne kadar sürebilir → tamamlanınca kilit yeniden açılır. Transfer öncesi WHOIS iletişim adresleri güncel olmalı; **auth kodu Owner/Admin contact adresine gider.**
- Son 60 gün içinde transfer edilmiş veya yeni kayıtlı domainlerde ICANN kısıtı olabileceği hatırlatılır.

## Çıktı Formatı

```
## Portföy özeti
| Domain | Yaş | Yenileme | Vitrin aralığı | Hızlı satış | Karar |

## Domain bazında
### example.com
- Araç tahminleri: A: $X · B: $Y · C: $Z  (doğrulandı: [tarih])
- Karşılaştırılabilir satışlar: ...
- Güçlü/zayıf yönler: ...
- Risk: ...
- **Karar:** [TUT/SAT/GELİŞTİR/BIRAK] — gerekçe

## Aksiyon listesi
1. ...
```

## Sık Yapılan Hatalar
- Tek aracın rakamını "değer" sanmak.
- Kendi projesine duyduğu bağı piyasa değeri sanmak.
- .com dışı uzantıyı .com fiyatıyla değerlemek.
- Ticari marka içeren domaini varlık sanmak — o bir yükümlülüktür.
- Yenileme maliyetini toplamda hesaplamamak (10 domain × 10 yıl gerçek paradır).
- Alıcıya önce "ne kadar verirsin" diye sorup pozisyonu kaybetmek — ya da tersine, piyasanın 50 katını isteyip görüşmeyi bitirmek.
- Transfer sırasında DNS kayıtlarını yedeklememek → site/e-posta kesintisi. Taşımadan önce tüm DNS kayıtları not edilir.

## Sınırlar
Yatırım tavsiyesi değildir; alım-satım kararını kullanıcı verir. Marka çakışması analizi hukuki görüş yerine geçmez, ciddi çakışmada marka vekili/avukata yönlendirilir.
