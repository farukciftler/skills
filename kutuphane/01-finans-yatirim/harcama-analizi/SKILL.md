---
name: harcama-analizi
description: >
  Faruk'un banka ekstrelerinden (VakıfBank, Vakıf Katılım, Akbank; PDF) çıkarılan
  hesap hareketleriyle harcama, gelir, nakit akışı, kategori, abonelik, altın/döviz
  işlemleri, fon lot maliyeti ve defter mutabakatı analizi yapar; sonuçları
  data-belgeler/analiz/ altına deterministik olarak yazar ve istenirse PDF sunum
  üretir. Kullanıcı "harcamalarım", "bu ay ne harcadım", "nereye gidiyor param",
  "aylık gider", "kategori", "abonelikler", "kira ne kadar", "ekstre yükle",
  "ekstremi tara", "PDF yükledim", "bütçe", "tasarruf oranı", "altın alım satım
  kârım", "fon maliyetim", "lot bazında getiri", "defterle mutabakat", "harcama
  raporu", "sunum hazırla" gibi bir şey dediğinde ya da bir banka ekstresi /
  fon dökümü PDF'i paylaştığında bu skill'i kullan. Portföy TAHMİNİ üretmez —
  o portfoy-tahmin skill'inin işi; buradaki veri `data/` defterine yalnız
  mutabakat düzeltmesi olarak ve ayrı komutla girer.
---

# Harcama Analizi

Bu skill bir **bütçe koçu değil, ölçüm aracıdır.** Amaç "şuraya az harca"
demek değil; paranın nereden gelip nereye gittiğini ekstreden **satır satır,
uydurmadan** kaydetmek, kategorilemek, aydan aya ölçmek ve ölçülemeyeni
açıkça "belirsiz" diye göstermektir. Depo genelindeki iş bölümü burada da
geçerlidir:

| Kim | Ne yapar | Ne yapmaz |
|---|---|---|
| `scripts/belgeler.py` | PDF → satır (metin çıkarımı, font çözümü, bakiye zinciri) | yorumlamaz, kategorilemez |
| `scripts/harcama.py` | kategoriler, toplar, eşleştirir, mutabakat yapar, JSON/CSV yazar | internete çıkmaz, sözlüğü kendisi büyütmez |
| `scripts/rapor_pdf.py` | analiz çıktısından HTML+SVG → PDF sunum | sayı üretmez, `ozet.json`'u okur |
| **Claude (sen)** | belgeyi tanır, taranmış tabloyu görüntüden okur, sözlüğe aday önerir, anlatıyı yazar, kullanıcıya soruları sorar | **hesap yapmaz**, kategori uydurmaz, "muhtemelen kira" diye kesin yazmaz |

Sebep: 02.09.2026'da ilk yüklemede görüldü — OCR bir tabloyu sütun sırasıyla
karıştırıyor, Vakıf Katılım PDF'i başlıkları kaymış bir fontla yazıyor
(`7$5ø+` = TARİH), Akbank ekstresi iOS taramasından geliyor. Bunların hiçbiri
"dikkatli okuyarak" çözülmez; deterministik çözücü + doğrulama zinciri gerekir.

---

## 0. Dürüstlük çerçevesi — yumuşatma

1. **Kategori bilinmiyorsa `belirsiz` yazılır.** Bir işyeri adından kategori
   *tahmin edilebiliyorsa* bile sözlükte yoksa `belirsiz` kalır; sözlüğe
   eklemek ayrı bir adımdır ve kullanıcıya listelenir. Yüzde 5'lik bir
   "belirsiz" dilimi, yüzde 0'lık uydurulmuş bir dilimden değerlidir.
2. **Karşı tarafın kim olduğu çıkarımsa `varsayim` etiketi taşır.** Örnek:
   Atila Özgüç'e aylık düzenli FAST + İGDAŞ/İSKİ sözleşmelerinin aynı isimde
   olması "kira" çıkarımını **güçlü** yapar ama **kesin** yapmaz. Sözlükte
   `guven=varsayim` olarak durur; kullanıcı teyit edince `kesin` yapılır.
   Raporda varsayım satırları ayrı işaretlenir.
3. **İç transfer harcama değildir.** Kendi hesapları arasındaki her hareket
   (VakıfBank → Vakıf Katılım, cari → günlük katılma, cari → yatırım hesabı,
   döviz alış/satış, altın alım/satım) `ic_transfer` ya da `varlik_transferi`
   sınıfındadır ve **hiçbir harcama toplamına girmez.** 12 aylık ekstrede
   "transfer" sütunu aylık 80–187 bin TL görünüyordu; bunun neredeyse tamamı
   kendi hesaplarına gidiyordu. Ayıklanmadan yapılan her analiz yanlıştır.
4. **Nakit çekimi harcama değil, harcama *kaynağıdır*.** ATM çekimleri ayrı
   satırda gösterilir; neye harcandığı bilinmez, bilinmediği yazılır.
5. **Toplamlar ekstreyle tutmalı.** Her belge için `Σ tutar` ekstrenin kendi
   "toplam çekilen / toplam yatırılan" alanıyla kuruşuna kadar karşılaştırılır;
   tutmuyorsa analiz **durur**, rapor üretilmez.
6. **Kredi kartı ekstresi yoksa "harcama" eksiktir** ve bu rapora yazılır.
   02.09.2026 itibarıyla elde yalnız banka (debit) hesapları var.
7. **Bu bir yatırım/bütçe tavsiyesi değildir.** Rapor sonunda "şunu kes"
   önerisi yok; kararı etkileyebilecek olgular ve sorular var.

---

## 1. Veri düzeni

```
data-belgeler/
  README.md                          şema, mutabakat tablosu, bilinen sınırlar
  pdf/<slug>.pdf                     orijinaller (sha256 belgeler.json'da)
  metin/<slug>.txt | .ocr.txt        çıkarılmış metin / OCR
  hesap_hareketleri.csv              TÜM bankalar tek şema (belgeler.py yazar)
  hesaplar.json                      ekstre başlıkları, bakiyeler
  belgeler.json                      belge dizini
  fon_pozisyonlari_YYYY-MM-DD.csv    lot bazlı fon dökümü (tarama → elle okundu)
  kategori_sozlugu.csv               işyeri deseni → kategori   (sen + kullanıcı büyütür)
  karsi_taraf_sozlugu.csv            FAST/havale karşı tarafı → tür (kendi/aile/kira/…)
  analiz/                            harcama.py ÇIKTISI — elle dokunma, yeniden üret
    hareketler_kategorili.csv        her satır + kategori + tür + eşleşme kaynağı + güven
    aylik.csv                        ay × (gelir, harcama kategorileri, transferler, tasarruf)
    kategori_ozet.csv · isyeri_ozet.csv · abonelikler.csv
    altin_islemleri.csv · doviz_islemleri.csv · fon_lotlari.csv
    mutabakat.csv                    defter akışları ↔ ekstre eşleşmesi
    ozet.json                        raporun tek girdisi
    rapor_YYYY-MM-DD.html / .pdf     sunum
```

Slug kuralı: `<banka>_<hesap>_<dönem başı>_<dönem sonu>`. Aynı belge iki kez
verilirse satırlar yeniden yazılır, çoğalmaz. **Aynı hesabın örtüşen iki
ekstresi** (ör. yıllık + günlük) `harcama.py` tarafından
`(banka, hesap_no, tarih, referans, tutar)` anahtarıyla tekilleştirilir.

Kişisel veri (IBAN, TCKN, isimler) içerir; depo özeldir. `research-paper/`
dışa aktarımı beyaz listeyle çalışır, buradan hiçbir şey yayına gitmez.

---

## 2. Modlar

### `yukle` — yeni PDF geldi

1. **Belge türünü tanı** (ilk sayfa metni): VakıfBank "Hesap Hareketleri",
   Vakıf Katılım "HESAP EKSTRESİ / ACCOUNT STATEMENT" (font kaymalı), Akbank
   "HESAP HAREKETLERİ … AKBANK", TEFAS/banka fon dökümü, kredi kartı ekstresi
   (henüz görülmedi), imza sirküleri, diğer. `pdftotext -l 1` boş dönüyorsa
   **tarama**dır.
2. **Metinli PDF** → doğrudan:
   ```bash
   python3 scripts/belgeler.py --out data-belgeler <pdf> [<pdf> ...]
   ```
   Çıktıdaki `islem` sayısını ve `hesaplar.json`'daki toplamları oku; script
   bakiye zincirini doğrular, kırık varsa **önce onu çöz** (bkz.
   `references/ekstre-bicimleri.md`), analize geçme.
3. **Tarama** → önce OCR metni üret ve sakla (macOS Vision, `pdftoppm` +
   `VNRecognizeTextRequest`, `references/ekstre-bicimleri.md` §Tarama):
   ```bash
   python3 scripts/belgeler.py --out data-belgeler --scan <slug>=<pdf> --ocr-txt <slug>=<ocr.txt> --tur <slug>=<tür>
   ```
   **Tablo içeren taramayı OCR'dan okuma.** Görüntüyü döndür/kırp (`sips`),
   `Read` ile bak, tabloyu **elle** yaz, `kaynak: "tarama - elle okundu"`
   etiketiyle CSV'ye koy (`fon_pozisyonlari_*.csv` böyle yazıldı). Her
   satırın toplamı belgedeki toplamla tutmalı; tutmuyorsa yanlış okumuşsundur.
4. **Mutabakat** (her yüklemede, atlanmaz): ekstredeki bakiyeler ve fon
   adetleri ile `data/` + `data-es/` defterleri karşılaştırılır
   (`harcama.py mutabakat`). Fark varsa **deftere otomatik yazma**; farkı
   listele, kullanıcı "evet" derse `pt.py snapshot --prices` / `pt.py flow`
   ile **ayrı komutla** işle ve snapshot notuna gerekçe yaz (02.09.2026:
   günlük katılma gerçek bakiyesi 14.831,13 böyle işlendi; 170.000 TL maaş
   girişi **işlenmedi**, kullanıcı dağılımı bekleniyor).
5. `data-belgeler/README.md` mutabakat tablosunu güncelle, commit.

### `analiz` — tam çalıştırma

```bash
python3 scripts/harcama.py --root data-belgeler --defter data --es-defter data-es
```

Sırasıyla: tekilleştir → sınıfla (§3) → aylık tablo → abonelik → altın/döviz
→ fon lotları → mutabakat → `ozet.json`. Her adımın kontrol sayısı stdout'a
yazılır; **`belirsiz` payı ve `varsayim` sayısı** raporun başında durur.

Sonra sen: `analiz/ozet.json`'u oku, `references/rapor-sablonu.md`'deki
şablonla sohbette özet ver. Sayıları JSON'dan al, **yeniden hesaplama**.

### `kategori` — sözlük bakımı

`analiz/kategori_ozet.csv`'de `belirsiz` toplamı ve
`analiz/isyeri_ozet.csv`'de eşleşmeyen işyerleri listelenir. Kural:

- Sözlüğe **yalnız işyeri adından kategorisi açık olan** desenleri ekle
  (`YEMEKSEPETI` → yemek, `LCWAIKIKI` → giyim). "MUSTAFA KAYA" gibi kişi
  adları, "PARAM/" gibi ödeme aracıları tek başına eklenmez.
- Her eklemeyi kullanıcıya **liste olarak göster**, onaylananları yaz.
  `guven` sütunu: `kesin` (adından açık / kullanıcı teyit etti) ·
  `varsayim` (çıkarım). Varsayımlar raporda ayrı sayılır.
- Desen `regex`'tir, büyük/küçük harf duyarsız, Türkçe harfler
  normalize edilmiş (İ→I, ş→s …) metne uygulanır. Sıra önemli: **ilk
  eşleşen kazanır**, o yüzden özel desen genel desenden önce gelir
  (`PARAM/YEMEKSEPETI` satırı `PARAM/` satırından önce).
- Kanonik kategori ağacı `references/kategori-semasi.md`'de; ağaca yeni dal
  eklemek şema değişikliğidir, gerekçesiyle README'ye yazılır.

### `abonelik`, `altin`, `fon-lot`, `mutabakat`

Hepsi `analiz` içinde üretilir; kullanıcı yalnız birini sorarsa ilgili CSV'yi
oku ve anlat. Tanımlar:

- **Abonelik**: aynı normalize işyeri, ≥3 farklı ayda, tutar değişkenliği
  (std/ort) < 0,25. Yıllık maliyet = 12 × medyan tutar (**tahmin değil,
  ölçülen ritmin uzantısı**; raporda "yıllıklandırılmış" denir).
- **Altın işlemleri**: Vakıf Katılım cari ekstresindeki
  "`<kur> Türk Lirası Kurundan <gram> Gr Altın Alımı/Satışı`" satırları.
  Gram ve kur metinden gelir, TL ekstre tutarıdır. Gerçekleşen kâr **FIFO**
  ile hesaplanır ve **açılış stoğu bilinmiyorsa** (ekstre dönem başında
  pozisyon varsa) satışların bir kısmı eşleşemez → `eslesmeyen_gram` olarak
  raporlanır, kâr uydurulmaz. BSMV satırları maliyete eklenir.
- **Fon lotları**: `fon_pozisyonlari_*.csv` (alış tarihi, adet, maliyet) +
  `data/snapshots/<son>.json` NAV → lot bazında gerçekleşmemiş getiri ve
  yıllıklandırılmış basit getiri. Fon dökümü hangi defterin lotu olduğunu
  söylemez; eşin adetleri (`data-es/portfolio.json`) **adet eşleşmesiyle**
  ayrılır (4.532 KTJ · 506 KUT · 357 ZPE, 11.08.2026 lotları).
- **Mutabakat**: `data/snapshots/*.json` içindeki `flows` ↔ ekstre satırları
  (tarih ±2 iş günü, tutar ±1 TL). Üç sonuç: `eslesti` · `defterde_var_ekstrede_yok`
  · `ekstrede_var_defterde_yok`. Üçüncü kalem **en önemlisidir**: deftere
  girmemiş nakit akışı getiri serisini kirletir (CLAUDE.md §2 Adım 2, K8/K15).

### `rapor` — PDF sunum

```bash
python3 scripts/rapor_pdf.py --root data-belgeler --defter data --es-defter data-es --out data-belgeler/analiz
```

HTML + gömülü SVG üretir, headless Chrome ile PDF'e basar (yol script'te;
Chrome yoksa HTML bırakır ve söyler). İçerik sırası ve her sayfanın **zorunlu
dipnotu** (veri kaynağı, dönem, ne dahil ne değil) `references/rapor-sablonu.md`.
Rapor sayıları **yalnız** `ozet.json`'dan gelir. Üretildikten sonra PDF'i
`Read` ile aç, en az iki sayfaya **gerçekten bak** (taşan tablo, boş grafik,
üst üste binen etiket), sonra kullanıcıya ver.

---

## 3. Sınıflama kuralları (motorun uyguladığı sıra)

Her satır bir **tür** (`tur`) ve bir **kategori/alt kategori** alır. Sıra
kesindir; ilk eşleşen kazanır. Ayrıntılı tablo `references/kategori-semasi.md`.

1. **Banka işlem adı** (VakıfBank `islem_adi`): masraf/vergi → `finans_masraf`;
   fatura tahsilatları (Turkcell, Vodafone, İGDAŞ, İSKİ, CLK, Netspeed) →
   `konut`/`iletisim`; ATM → `nakit`; döviz alış/satış → `varlik_transferi/doviz`;
   iade → `gelir/iade`; "Alınan havale … maas" → `gelir/maas`.
2. **Karşı taraf** (FAST/EFT/havale, Vakıf Katılım `Lehdar=`/`Amir`):
   `karsi_taraf_sozlugu.csv` → `kendi_hesabi` (ic_transfer) · `aile` ·
   `kira` (varsayım) · `kisi` (amaç bilinmiyor → `kisi_odeme`).
   Eşleşmeyen karşı taraf → `kisi_odeme`, `guven=yok`.
3. **Vakıf Katılım iç kalıpları**: `Gönderen Hesap: … Alıcı Hesap 1351308-4000`
   ve `Hesaptan … hesaba …` → `varlik_transferi/fon` (yatırım hesabı);
   `… 1351308-1000` ve `Günlük Hesap Kapsamında Virman` → `ic_transfer/gunluk`;
   `Gr Altın Alımı/Satışı` → `varlik_transferi/altin`; `Euro/Amerikan Doları
   … Kurundan` → `varlik_transferi/doviz`; `Kar Payı` → `gelir/kar_payi`;
   `Vergi … Hsp` → `finans_masraf/stopaj`; `BSMV` → `finans_masraf`.
4. **POS**: MCC varsa MCC tablosu (`references/kategori-semasi.md` §MCC);
   yoksa `kategori_sozlugu.csv` deseni; yoksa `belirsiz`.
5. **Akbank**: `MAAŞ ÖDEMESİ` → `gelir/maas`; kendi adına EFT → `ic_transfer`;
   `MKK ÜCRETLERİ` → `finans_masraf`; sigorta iptal iadesi → `gelir/iade`.

Tür kümesi: `gelir` · `harcama` · `aile_destek` · `kisi_odeme` · `nakit` ·
`ic_transfer` · `varlik_transferi` · `finans_masraf` · `belirsiz`.

**Aylık "hane dışına çıkan"** = harcama + aile_destek + kisi_odeme + nakit +
finans_masraf. **Tasarruf oranı** = (gelir − hane dışına çıkan) / gelir; gelir
= maaş + diğer gelir (iade ve kâr payı dahil, **döviz satışı ve iç transfer
hariç**). Aynı maaş iki bankada görünüyorsa (Akbank'a yatıp Vakıf Katılım'a
geçmesi gibi) yalnız **ilk giriş** gelirdir; sonraki `ic_transfer`dir.

---

## 4. Tuzaklar — 02.09.2026'da yaşananlar

| Tuzak | Ne oldu | Kural |
|---|---|---|
| Vakıf Katılım font kayması | başlıklar `+(6$3(.675(6ø`, açıklamalar `*QON+HVDS…`, satır ortasında bölünmüş tutarlar | `belgeler.py::decode_token`; kaymış alfabeyle yazılamayacak kelimeye dokunma; bölünmüş satırda tutar alt satırdan alınır |
| OCR tabloyu bozar | Vision fon tablosunu sütun sütun okudu, satırlar eşleşmedi | tablo taramaları görüntüden elle okunur, `kaynak` etiketi konur |
| Aynı gün aynı işlem | Yemeksepeti üç ödeme sağlayıcısı (Param, İyzico, Sipay, Yemekpay) altında | sözlük ödeme aracısını değil işyerini hedefler; `PARAM/ /HEPSIBURADA` gibi boşluklu varyantlar için desen gevşek |
| Transfer = harcama sanmak | aylık 80–187 bin "transfer" | karşı taraf sözlüğü + `ic_transfer` türü; raporda ayrı sütun |
| Kira çıkarımı | Atila Özgüç'e 10 × ~15 bin + İGDAŞ/İSKİ sözleşmeleri aynı ad | `varsayim`; kullanıcı teyidi olmadan "kira" başlığı yazılmaz, "kira (varsayım)" yazılır |
| Maaşın iki bankada görünmesi | Ağustos: Akbank'a 174.900, ertesi gün Vakıf Katılım'a 174.000 | ikinci giriş `ic_transfer` |
| Ekstre dönem başı stoğu | Vakıf Katılım altın satışları 2026 alımlarını aşıyor (açılış pozisyonu ekstrede yok) | FIFO eşleşmeyen gramı ayrı yaz, kâr uydurma |
| Örtüşen ekstreler | 1351308-1000 için hem yıllık hem "bugün" ekstresi | anahtarla tekilleştir |
| Akbank iOS taraması | `01.09 2026 16-07`, `04.082026` | ayrıştırıcı toleranslı; satır sayısı ekstreyle karşılaştırılır |

---

## 5. Kullanıcıya sorulacaklar (açık işler)

Analiz her çalıştığında `ozet.json → acik_sorular` üretir; sohbette
**en fazla beşini** sor, kalanını README'ye yaz:

- Teyit bekleyen `varsayim` karşı taraflar (kira, aile üyeleri).
- `belirsiz` payı en yüksek 10 işyeri.
- Defterde olmayan ekstre akışları (mutabakat üçüncü kalem).
- Eksik belge: kredi kartı ekstresi, eşin hesapları, Vakıf Katılım 2025.
- Ekstrede görülen ama defterde tanımsız hesaplar (02.09: 1351308-2'de
  5.000 TL; 1351308-4000 yatırım hesabı; VakıfBank döviz hesabı TR81…311 11).

---

## 6. Rapor şablonu (sohbet)

```
## Harcama · <dönem>
**Gelir X · Hane dışına çıkan Y · Tasarruf %Z** (kredi kartı YOK — eksik)
| Ay | Gelir | Harcama | Aile | Nakit | Masraf | Varlığa net | Tasarruf % |
### Kategoriler (12 ay)   — tablo, belirsiz payı ayrı satır
### En sık / en büyük işyerleri
### Abonelikler (yıllıklandırılmış)
### Altın / döviz işlemleri (gerçekleşen, FIFO; eşleşmeyen gram ayrı)
### Fon lotları (gerçekleşmemiş, son NAV)
### Mutabakat — defter ↔ ekstre
### Sorular (≤5)
_Ölçümdür, tavsiye değildir._
```

Kullanıcı yoğun, tabloyu tarayarak okur; paragraf yazma. "Şunu kes" yok.

## Referanslar

- `references/kategori-semasi.md` — kanonik ağaç, MCC tablosu, karar sırası
- `references/ekstre-bicimleri.md` — üç bankanın biçimi, font kayması, tarama/OCR
- `references/karsi-taraf-kurallari.md` — kendi/aile/kira/kişi ayrımı, maaş tekilleştirme
- `references/rapor-sablonu.md` — PDF sunum sayfa planı ve zorunlu dipnotlar
