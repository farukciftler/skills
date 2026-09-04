# Veri kaynakları ve arama protokolü

Amaç: ilan fiyatını değil, **gerçekçi fiyatı ve gerçekçi kirayı** bulmak. Her rakamın
yanına kaynak ve tarih yaz.

## 1. Fiyat ve kira emsali

| Ne | Nereye bak | Dikkat |
|---|---|---|
| İlan fiyat aralığı | Sahibinden, Emlakjet, Hepsiemlak, Zingat, Hürriyet Emlak | İlan ≠ satış; pazarlık payı vardır |
| Mahalle/ilçe m² fiyatı ve kirası | Endeksa, Emlakjet bölge raporları | İlan bazlıdır, iyimserdir |
| Değerleme bazlı seri | TCMB Konut Fiyat Endeksi ve konut birim fiyatları, konut değerleme istatistikleri | Ekspertizden gelir, ilan bazlıya göre daha muhafazakâr |
| Resmî fiyat endeksi | TÜİK Konut Fiyat Endeksi (reel/nominal) | Reel seriye özellikle bak |
| Satış hacmi ve ipotekli satış | TÜİK konut satış istatistikleri | Talep ve kredili alım payının göstergesi |
| Emlak vergi değeri | İlgili belediye e-belediye sorgusu | Tapu harcı alt sınırını belirler |
| Kira sözleşme/piyasa kirası | Kiralık ilanlar + ilanda kalma süresi | Kısa ilan süresi = güçlü talep |

**Arama kalıpları:** `"<mahalle> <ilçe> satılık daire m2 fiyat"`, `"<mahalle> kiralık 2+1"`,
`"<ilçe> konut amortisman süresi <yıl>"`, `"<ilçe> kentsel dönüşüm planı"`,
`"<semt> metro açılış tarihi"`.

Emsal toplarken en az 5 satılık + 3 kiralık nokta; m² başına normalize et; aykırı değerleri
(çok yeni/çok eski, farklı kat, manzaralı) ayıkla ve neyi ayıkladığını yaz.

## 2. Makro ve alternatif getiri

- TCMB politika faizi ve beklenti anketi (enflasyon beklentisi → reel hesap varsayımı)
- TÜİK TÜFE ve ÜFE (ÜFE, değer artış kazancı endekslemesinde kullanılır)
- Konut kredisi / konut finansmanı oranları: bankaların kendi sayfaları + karşılaştırma
  siteleri (hangikredi, hesapkurdu). Katılım tarafında "kâr payı oranı" olarak geçer.
- Alternatif getiri için: TEFAS fon getirileri, katılma hesabı kâr payı oranları, gram altın.
  Kullanıcının mevcut portföy tercihi varsa onu referans al.

## 3. Yapı ve hukuk

- e-Devlet: Tapu Bilgileri, Yapı Kayıt Belgesi sorgulama, adres/bina bilgileri
- Belediye: imar durumu, iskân, takdir komisyonu vergi değerleri, kentsel dönüşüm ilanları
- AFAD/belediye zemin ve mikrobölgeleme çalışmaları, deprem risk haritaları
- Çevre, Şehircilik ve İklim Değişikliği Bakanlığı: riskli yapı ve dönüşüm mevzuatı
- GİB: kira geliri rehberi, değer artış kazancı, harç oranları

## 4. Bölge dinamiği

- Ulaşım yatırımları (metro, tramvay, köprü) — **açılış tarihi teyitli mi**, kaç kez ertelendi
- Yeni proje arzı: bölgede ruhsat alan/inşa hâlindeki konut sayısı
- İstihdam odakları: OSB, plaza bölgesi, hastane, üniversite; tek işverene bağımlılık riski
- Yerel haber ve forumlar: su baskını, altyapı, otopark, gürültü, site yönetim sorunları
- Nüfus ve göç verisi (TÜİK ADNKS) — ilçe bazında talep yönü

## 5. Kayıt disiplini

Analiz sonunda kullanılan tüm varsayımları girdi JSON'una yaz ve rapora şu tabloyu ekle:

| Varsayım | Değer | Kaynak | Tarih | Güven |
|---|---|---|---|---|

"Güven" için yüksek/orta/düşük kullan. Düşük güvenli varsayımın duyarlılıkta ne kadar
oynadığını mutlaka göster.
