---
name: masifico-parti-uretim
description: Masifico'nun parti (seri) üretim planlayıcısı — bir SKU'yu tek prototipten N adetlik partiye çevirir; parti numarası açar, iş emri ve operasyon sırasını kurar, mesai/kapasite takvimini hesaplar (kaç gün sürer, mesai tavanını aşıyor mu), fason siparişlerini ve teslim tarihlerini takip eder, malzeme ihtiyacını fire katsayısıyla çıkarır, QC ve sevkiyat adımlarını izlenebilirlik kaydına bağlar. Kullanıcı "parti", "seri üretim", "30 set üretelim", "iş emri", "üretim planı", "ne kadar sürer", "kaç günde biter", "kapasite", "kaç kereste lazım", "sipariş geçelim", "üretime başla", "partiyi kapat", "stok", "yetişir mi", "kreş siparişi geldi" dediğinde; prototip onaylandıktan sonra seriye geçilirken; teslim tarihi taahhüt edilirken; veya üretim sırasında darboğaz konuşulduğunda bu skill'i kullan. Kapasite hesabı yapılmadan teslim tarihi verilmez; parti kaydı açılmadan üretime başlanmaz.
---

# Masifico Parti Üretim Planlayıcısı

Amaç: "30 set DT-10 üretelim" cümlesini, **tarihleri, malzeme miktarları ve sorumlusu belli bir iş emrine** çevirmek — ve o partiyi izlenebilirlik kaydına bağlamak.

Zincirdeki yeri: `masifico-uretim-muhendisi` (bir setin dosyaları hazır) → **bu skill** (N adete ölçekler) → `masifico-tedarik-rfq` (fason siparişi) → `masifico-kalite-izlenebilirlik` (QC + sevk).

## 0 · Dört kural

1. **Parti kaydı açılmadan üretime başlanmaz.** `parti.py ac` ile numara alınır; numara olmadan yapılan üretim izlenemez ve geri çağırmada tüm tarihçeyi riske atar.
2. **Kapasite hesaplanmadan teslim tarihi verilmez.** Mesai tavanı aşılıyorsa çözüm zam değil, süreç yatırımıdır (pah frezesi + kızak, toplu zımpara).
3. **Parti sınırı dört şeye bağlıdır** — hammadde lotu, kimyasal lotu, fason atölye, operatör. Biri değişirse **yeni parti**.
4. **Asıl kısıt genelde malzeme değil mesai.** `sku_maliyet.py::gereken_mesai()` verilen fiyatta mesai tavanını verir; KB-24 şu an **AŞIYOR** durumunda — parti planı bunu görmezden gelemez.

## 1 · Parti açma

```
~/masifico-venv/bin/python uretim/parti/parti.py ac \
   --sku DT10 --adet 30 --operator "Faruk" \
   --kereste-tedarikci SNC --irsaliye "SNC-2026-0912" --kereste-lot "KYN-26-08-A" \
   --doc-no "MSF-DT10-DOC-v1" --teknik-dosya "TD-DT10-v1"
```

Numara `MSF-<SKU>-<YYYY>W<WW>-<NN>` biçiminde otomatik üretilir (ISO hafta). Eksik alan varsa script uyarır — **kapatmadan önce doldurulması zorunlu** alanlar: kereste tedarikçisi, irsaliye no, kereste lotu, AT Uygunluk Beyanı no.

## 2 · Malzeme ihtiyacı

Set başı net hacim `BOM`'dan gelir; parti ihtiyacı:

```
kereste (m³) = set_net_hacim × adet × FIRE
FIRE = 1,40-1,60  (kesim + kusur firesi; nesting raporu varsa onu kullan)
```

**Kaba ölçü ↔ net ölçü tuzağı:** toptancı fiyatı genelde **kaba ölçü** üzerinedir; 5×10 kereste kuruyup rendelenince 4,5×9,5'e düşer (**−%14,5**). Net ölçüyle iş yapıyorsan gerçek birim maliyet **%15-17 yüksektir**. RFQ'da ölçü esası açıkça yazılır.

**Alım zamanlaması:** OGM kayın tomruk fiyatı **Ocak zirve, Temmuz dip** (2026'da fark ~%38, mevsimsellik iki yıldır aynı). Yıllık kereste stoğu **Temmuz-Eylül'de** bağlanır.

**Kalınlık uyumu:** TR'de kayın kereste **50/60/80/100 mm**'den başlar. KB-24 (tüm boyutlar ≥50 mm) standart kesitle birebir uyumludur — **bu bir tasarım avantajıdır, korunur**. Daha ince parçalar dilme gerektirir; teklifte ayrı kalem olarak sorulur.

## 3 · Operasyon sırası ve mesai

DT-10 örneği (set başı 80-110 dk):

| # | Operasyon | Yer | Not |
|---|---|---|---|
| 1 | Ebatlama (blok kesim) | fason | RFQ ile teklif; termin 10 iş günü |
| 2 | Facet kesimi | atölye | jig ile; her set benzersiz, mastar bağlayıcı |
| 3 | Zımpara 120 → 180 | atölye | kum atlanmaz |
| 4 | **Lif kaldırma** (nemli bez + 30-60 dk kuruma) | atölye | atlanırsa müşteride kıymık çıkar |
| 5 | Zımpara 220 | atölye | yağlanacak yüzeyde son kum |
| 6 | Kıymık kontrolü (naylon çorap) | atölye | yağdan ÖNCE |
| 7 | Yağ 1. kat → 10-20 dk sonra fazlasını sil | atölye | fazla kalırsa yapış yapış kürlenir |
| 8 | Bekleme 12-24 saat | — | **takvimde yer kaplar** |
| 9 | Yağ 2. kat + silme | atölye | |
| 10 | **Tam kür 7-14 gün** | — | **ambalaj ve EN 71-3 numunesi bundan önce alınmaz** |
| 11 | Gravür (parti no + marka) | fason lazer | minimum iş bedeli devreye girer |
| 12 | Kıymık kontrolü (kür sonrası) + QC | atölye | `qc.py` |
| 13 | Montaj/paketleme + parti no etiketi | atölye | |

**Takvim kuralı:** kür süresi mesai değildir ama **takvimdir**. 30 setlik DT-10 partisinde net mesai ~40-55 saat olsa da, kür ve fason terminleri yüzünden **takvim 3-4 haftadır**. Kreşe teslim tarihi verirken mesaiyi değil takvimi taahhüt et.

**Kapasite kontrolü:** `mesai_dk × adet ÷ günlük_çalışma` → gün sayısı. Sonuç fason terminleriyle çakıştırılır; darboğaz hangisiyse teslim tarihini o belirler.

## 4 · Fason sipariş takibi

Her fason iş parti kaydında `fason_atolye[]` altına yazılır: unvan, adres, iş emri no, sipariş tarihi, teslim tarihi, adet. **Adres alanı teknik dosyanın Ek IV(e) gereğidir** (üretim yerlerinin adresleri) — boş bırakılmaz.

**İlk parça onayı (FAI) olmadan seri sipariş geçilmez.** Numune geldiğinde: kalite skill'inin gelen mal kontrolü uygulanır → onay/ret **yazılı** verilir → onaylanan numune **altın numune** olarak saklanır.

## 5 · Parti kapanışı

```
parti.py qc <parti_no> --gecti --kabul 28 --red 2
parti.py sevk <parti_no> --kanal kres --musteri "X Anaokulu" --siparis-no .. --adet 5
```

- **QC geçmeden sevk yok** (numune hariç) — script engeller.
- İlk sevkte `arz_tarihi` otomatik işlenir; **10 yıllık saklama sayacı buradan başlar**.
- Red oranı %10'u aşarsa script uyarır: maliyet motorundaki `ZAYIAT = 0.08` varsayımı gerçeği tutmuyor demektir.
- Parti kapanışında `parti_kontrol.py` çalıştırılır — izlenebilirlik zincirinde boşluk varsa HATA verir.

## 6 · Neyi YAPMAZ

- Fiyat belirlemez (`masifico-maliyet-fiyat`).
- Teklif istemez / sipariş göndermez (`masifico-tedarik-rfq`).
- QC kriterlerini tanımlamaz (`masifico-kalite-izlenebilirlik`).
- Tasarım dosyası üretmez (`masifico-uretim-muhendisi`).

## Dosyalar

```
uretim/parti/
├── parti.py          ← parti aç · QC işle · sevk · arz tarihi
├── partiler.json     ← parti kayıt defteri
└── parti_kontrol.py  ← denetçi (çıkış kodu 1 = sevk edilemez)
```
