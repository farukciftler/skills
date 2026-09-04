---
name: masifico-tedarik-rfq
description: Masifico'nun tedarik ve teklif (RFQ) operatörü — fason atölyelere (ebatlama, CNC, torna, lazer) ve malzeme tedarikçilerine gidecek teklif isteğini hazırlar, teknik dosyaları paketler, e-posta/WhatsApp taslağını üretir, ONAY ALARAK gönderir, gönderimi kayda geçirir, gelen teklifleri normalize edip karşılaştırır ve seçilen fiyatları maliyet motoruna işler; tedarikçiden alınması gereken uygunluk belgelerini (EN 71-3 raporu, SDS, PFAS/bisfenol beyanı, nem/menşe beyanı) ister ve eksikleri denetler. Kullanıcı "teklif al", "fiyat sor", "ustaya gönder", "dosyayı yolla", "RFQ", "kaça yapar", "tedarikçi", "kereste alacağım", "numune iste", "sipariş geçelim", "teklifleri karşılaştır", "hangi usta daha uygun", "belge iste", "SDS", "malzeme beyanı" dediğinde; yeni bir üretim paketi (uretim/<sku>/cikti) tamamlandığında; parti planı fason iş gerektirdiğinde; veya bir maliyet kalemi "TEKLİF" etiketiyle tahmin olarak duruyorsa bu skill'i kullan. E-postayı asla habersiz göndermez — taslağı gösterir, açık onay alır, sonra yollar ve kaydeder.
---

# Masifico Tedarik & Teklif (RFQ) Operatörü

Amaç: bir üretim paketini **fason atölyenin soru sormadan fiyat verebileceği** bir teklif isteğine çevirmek, gönderimi tek elden yürütmek ve gelen fiyatları maliyet motoruna bağlamak.

Zincirdeki yeri: `masifico-uretim-muhendisi` (dosya üretir) → **bu skill** (fiyat alır) → `masifico-maliyet-fiyat` (fiyatı karara çevirir) → `masifico-parti-uretim` (siparişi işe döker).

## 0 · Altın kurallar

1. **Onaysız e-posta yok.** Script gönderim yapmaz; gönderim Claude'un MCP e-posta aracıyla ve Faruk'un o mesajdaki açık onayıyla olur. Onay bir RFQ ve bir alıcı içindir; "hepsini yolla" demeden çoklu gönderim yapılmaz.
2. **Gönderilen her şey kayda geçer.** `uretim/tedarik/gonderim_kaydi.jsonl` — kime, ne zaman, hangi RFQ, hangi kanal. Tedarikçiyle fiyat tartışması çıktığında tek kanıt bu.
3. **Aynı iş, aynı şartlar.** Bir işe iki tedarikçiden teklif alınırken metin, adet kademeleri ve termin **birebir aynı** gider; yoksa teklifler karşılaştırılamaz.
4. **Teklif alınmadan maliyet kesinleşmez.** `sku_maliyet.py` içindeki `TEKLİF` etiketli sabitler tahmindir; gerçek teklif geldiğinde aynı commit'te güncellenir.
5. **CE durumu her yazışmada doğru anlatılır:** "1-3 yaş çocuk oyuncağı, CE/EN 71 süreci devam ediyor, ürün henüz satışta değil." Tedarikçiye asla "belgeli ürün" denmez.
6. **Esnaf ustanın kanalı WhatsApp'tır.** `tedarikciler.json` içindeki `tercih_kanal` neyse o kullanılır; e-posta ısrarı iş yavaşlatır. E-posta taslağı WhatsApp metnine de kaynaktır (`eposta.txt` kısaltılır).

## 1 · Akış

```
1. talep yaz      → uretim/tedarik/talepler/RFQ-<YYAA>-<NN>.json
2. paket üret     → ~/masifico-venv/bin/python uretim/tedarik/rfq.py talepler/RFQ-....json
3. taslağı göster → cikti/<RFQ>/<TED>/eposta.txt + teklif formu PDF'i (konuşmada özetle)
4. ONAY al        → Faruk "gönder" der
5. gönder         → MCP: html_eposta_gonder(alici, konu, eposta.html)   [tek alıcı, tek çağrı]
6. kaydet         → rfq.py --kaydet <RFQ> <TED> --kanal eposta --adres <adres>
7. takip          → 3 iş günü sessizlik = hatırlatma; 7 gün = telefon
8. teklif gelince → uretim/tedarik/teklifler/<RFQ>-<TED>.json + teklif_karsilastir.py
9. karar          → maliyet-fiyat skill'i ile birim maliyet güncelle
```

## 2 · Talep (RFQ) dosyası — zorunlu alanlar

`uretim/tedarik/talepler/RFQ-2608-01.json` şablondur. Bir RFQ **şu sekiz sorunun** hepsini cevaplamadan gönderilmez; eksik olan tedarikçiyi tahmine zorlar, teklif de tahmin gelir:

| # | Soru | JSON alanı |
|---|---|---|
| 1 | Hangi malzeme, hangi kalitede? | `malzeme` (cins, nem, sınıf, kimin temin ettiği) |
| 2 | Tam olarak ne, kaç ölçüde? | `kalemler[]` (kod, tanım, ölçü, tolerans) |
| 3 | Kaç adet — ve hacim artarsa fiyat ne olur? | `kademeler_set` (1 / 30 / 100 / 300) |
| 4 | Ne zaman? | `termin_gun` |
| 5 | Nasıl ödenir? | `odeme` |
| 6 | Nereden teslim, nasıl paketli? | `teslim`, `ambalaj` |
| 7 | Hangi dosyalara bakacak? | `ek_dosyalar[]` (repo yolu; script varlığını doğrular) |
| 8 | Hangi belgeleri getirecek? | `istenen_belgeler[]` (kodlar `rfq.py` içindeki `BELGELER`'de) |

**Adet kademesi kuralı:** her zaman en az `1` (numune) ve hedef parti adedi sorulur. Numune fiyatı seri fiyatının 2-4 katı çıkar — bu normaldir, kurulum/hazırlık payıdır; seri kararını numune fiyatıyla verme.

**Tolerans kuralı:** ahşapta ±0,5 mm'den dar tolerans istemek fiyatı gereksiz büyütür. Kritik olan yüzey/ölçü hangisiyse yalnız onda dar tolerans yaz, gerisine "serbest" de.

## 3 · Gönderim protokolü (MCP e-posta)

- Araçlar: `html_eposta_gonder` (asıl) / `eposta_gonder` (düz metin yedeği). Gönderen hesap: `farukmakeitproduct@gmail.com`.
- **Ek dosya desteği yoktur.** Bu yüzden e-posta gövdesi tek başına fiyat vermeye yetecek kadar doludur (kalem tablosu + şartlar). Teknik dosyalar üç yoldan biriyle gider:
  1. `dosya_linki` alanı doldurulmuşsa gövdeye indirme linki konur (tercih edilen),
  2. WhatsApp'tan dosya olarak (esnaf usta için en hızlısı),
  3. elden/USB (ilk numune görüşmesinde).
  `dosya_linki` boşsa `rfq.py` bunu "gönderime engel" olarak işaretler — engel gösterilerek gönderilebilir ama dosyaların ayrıca iletildiği aynı gün kayda yazılır.
- Gönderimden önce konuşmada **mutlaka** şunlar gösterilir: alıcı adresi, konu satırı, gövdenin ilk 10 satırı, hangi dosyaların ekli/linkli olduğu.
- Adres `tedarikciler.json`'da boşsa **gönderim yapılmaz**; adres sorulur. Adres eldeyse aynı commit'te kayıt dosyasına yazılır.
- Bir RFQ'nun aynı tedarikçiye ikinci gönderimi ancak "hatırlatma" konu ön ekiyle ve ilk gönderimden ≥3 iş günü sonra yapılır.

## 4 · Tedarikçiden istenecek belgeler

`rfq.py` içindeki `BELGELER` sözlüğü tek doğruluk kaynağıdır; `oyuncak-mevzuat` ve `masifico-teknik-dosya` skill'leri **aynı kodları** kullanır — belge oradan teknik dosyaya birebir taşınır.

İş tipine göre asgari istek listesi:

| İş / malzeme | İstenecek belgeler |
|---|---|
| Kereste, ebatlama | `nem_beyani`, `kereste_mensei`, (varsa) `fsc_pefc` |
| CNC / torna / lazer (fason işçilik) | belge yok — kalite şartı sözleşmede; ilk parça onayı (FAI) şart |
| Yüzey ürünü (yağ/vernik/boya) | `en71_3_rapor`, `sds`, `oyuncak_uygunluk_beyani`, `pfas_bisfenol_beyani`, `teknik_veri_foyu` |
| Tutkal | `en71_3_rapor`, `sds`, `formaldehit_sinifi`, `pfas_bisfenol_beyani` |
| Ambalaj (kese, kutu, etiket) | gıda/oyuncak teması yoksa belge yok; baskı boyası çocuk ürününde ise `en71_3_rapor` |

Gelen belgeler `uretim/teknik-dosya/` altındaki ilgili SKU klasörüne kopyalanır; eksikler `belge_kontrol.py` ile denetlenir. **Belgesi olmayan yüzey ürünü satın alınmaz** — bir litre yağ için alınan kolaylık, tüm teknik dosyayı çürütür.

## 5 · Teklif değerlendirme

Gelen teklif `uretim/tedarik/teklifler/<RFQ>-<TED>.json` olarak kaydedilir, `teklif_karsilastir.py` normalize eder. Karşılaştırma **asla yalnız birim fiyatla** yapılmaz; şu beş kalem aynı tabloda durur:

1. **Set başı toplam maliyet** (birim fiyat × set başı adet, tüm kalemler)
2. **Kurulum/hazırlık** (parti adedine bölünmüş hali — 30'luk partide 500 TL kurulum = +17 TL/set)
3. **MOQ** (bizim parti adedimizin altındaysa fiili fiyat farklıdır)
4. **Termin** (10 gün vs 25 gün, kreş sezonunda fiyattan önemli)
5. **Fire kime yazılıyor** (malzeme bizdeyse fire bizim maliyetimiz; katsayı 1,4-1,6)

Karar notu her zaman şu cümleyle biter: *"Seçim X, çünkü ___; ikinci kaynak Y elde tutuluyor."* **Tek kaynağa kilitlenme yasak** — her kritik iş için ikinci kaynak `tedarikciler.json`'da `durum: ikinci_kaynak` olarak yaşatılır ve yılda en az bir kez teklif yarıştırılır.

## 6 · İlk parça onayı (FAI) — sipariş açmadan önce

Seri sipariş, numune onayı olmadan geçilmez. Numune geldiğinde:

1. `masifico-kalite-izlenebilirlik` skill'inin gelen mal kontrolü uygulanır (ölçü, nem, kusur).
2. Onay/ret yazılı verilir (WhatsApp mesajı yeter, ama kayda yazılır).
3. Onaylanan numune **saklanır** ("altın numune") — sonraki partilerde tartışma bununla biter.
4. Onay sonrası fiyat/termin yazılı teyit alınır; teklif geçerlilik süresi dolmuşsa yenilenir.

## 7 · Bu skill neyi YAPMAZ

- Fiyat pazarlığını Faruk yapar; skill pazarlık metni önerir, kendiliğinden indirim taahhüt etmez.
- Sipariş **vermez** (sipariş = `masifico-parti-uretim` skill'inin iş emri adımı).
- Tedarikçiye ürün tasarımının ticari sırlarını (satış fiyatı, marj, kanal stratejisi) yazmaz.
- Belgesiz malzemeyi "sonra hallederiz" diye geçiştirmez.

## Dosyalar

```
uretim/tedarik/
├── tedarikciler.json          ← kayıt defteri (e-posta/telefon burada; boşsa gönderim yok)
├── talepler/RFQ-YYAA-NN.json  ← teklif isteği girdisi
├── rfq.py                     ← paket + e-posta taslağı üretir · --kaydet ile gönderimi işler
├── teklif_karsilastir.py      ← gelen teklifleri normalize eder, tablo + karar notu üretir
├── belge_kontrol.py           ← tedarikçi belgeleri tam mı (çıkış kodu 1 = eksik)
├── teklifler/<RFQ>-<TED>.json ← gelen teklif kayıtları
├── gonderim_kaydi.jsonl       ← ne, kime, ne zaman gitti
└── cikti/<RFQ>/<TED>/         ← gönderilecek paket (dosyalar + eposta.html/.txt + form PDF)
```
