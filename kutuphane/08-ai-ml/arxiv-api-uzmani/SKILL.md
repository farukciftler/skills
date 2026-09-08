---
name: arxiv-api-uzmani
description: arXiv API ve OAI-PMH uzmanı — makale arama/keşif, günlük radar takibi, search_query kurulumu ve hata ayıklama, Atom yanıtı ayrıştırma, sayfalama ve rate-limit güvenli istemci/pipeline kodu, OAI-PMH ile toplu metadata hasadı ve artımlı senkronizasyon, RSS/ATOM beslemeleri ve S3 bulk veri seçimi. Kullanıcı "arxiv", "makale ara/bul", "paper", "preprint", "literatür taraması", "şu konuda yeni ne çıkmış", "arxiv API", "export.arxiv.org", "OAI-PMH", "harvest", "makale takip radarı", "arxiv scraper", "429/503 alıyorum", "sayfalama tıkandı" dediğinde; bir konuda güncel akademik literatür istendiğinde; arXiv verisi çeken bir uygulama, bot veya pipeline tasarlanırken bu skill'i kullan — "API" kelimesi hiç geçmese bile. Sorgu sözdizimini, limitleri ve uç noktaları ASLA ezberden verme; buradaki ve references/ altındaki doğrulanmış değerleri kullan.
---

# arXiv API Uzmanı

arXiv'in dört erişim kanalını (Query API, RSS/ATOM, OAI-PMH, S3 bulk) doğru
seçip, doğru sorguyu kurup, kurallara uyan kod üretmek için.

Doğrulama tarihi: **2026-09-08**. arXiv uç noktaları ve limitleri değişebilir;
kritik bir entegrasyon öncesi `references/` içindeki kaynak linklerini tazele.

---

## 0. Önce kanal seç

| İhtiyaç | Kanal | Uç nokta |
|---|---|---|
| Konu/yazar/başlık araması, filtreli sorgu | Query API | `http://export.arxiv.org/api/query` |
| Belirli ID'lerin metadata'sı | Query API `id_list` | aynı |
| "Bugün cs.LG'de ne çıktı" — günlük yeni liste | RSS/ATOM | `https://rss.arxiv.org/rss/cs.LG` · `/atom/cs.LG` |
| Bir kategorinin/tüm arXiv'in metadata kopyası, artımlı senkron | OAI-PMH | `https://oaipmh.arxiv.org/oai` |
| PDF/LaTeX kaynak dosyaları toplu | S3 (requester-pays) | `s3://arxiv/pdf/…`, `s3://arxiv/src/…` |

Karar kuralı: **arama varsa Query API, tam kopya varsa OAI-PMH.** Query API'yi
binlerce sonuç harvest etmek için kullanma — bu OAI-PMH'nin işi ve arXiv bunu
açıkça yazıyor. Tersine, OAI-PMH'de arama yoktur; sadece set (kategori) ve
değişiklik tarihi (`datestamp`) ile filtrelenir.

---

## 1. Pazarlıksız kurallar

1. **1 istek / 3 saniye, tek eş zamanlı bağlantı.** Bu limit tüm kanallar
   (Query API, RSS, OAI-PMH) ve senin kontrolündeki tüm makineler için
   toplamdır. Paralel makineyle aşmak ToU ihlali. Ürettiğin her istemcide
   throttle görünür olsun.
2. **Sonuçlar günde bir değişir.** Feed'in `<updated>` alanı çağrı yaptığın
   günün gece yarısıdır; yeni makaleler ~22:30 ET (Pazar–Perşembe) duyurulur.
   Aynı sorguyu günde birden fazla çalıştırmak anlamsız → **cache zorunlu.**
3. **PDF'leri kendi sunucunda barındırma.** Metadata CC0'dır, serbestçe
   saklanır/dağıtılır; e-print içeriği değildir. İndirme için arXiv abs
   sayfasına link ver.
4. **Descriptive User-Agent gönder** (proje adı + iletişim). Kimliksiz
   trafik ilk kısılan olur.
5. **Hatalar HTTP 200 ile gelir.** Query API hatayı tek `<entry>`'lik bir Atom
   feed'i olarak döndürür (`<title>Error</title>`). Kodun bunu kontrol etmeden
   "0 sonuç" deme.

---

## 2. Bu ortamda nasıl çalışırsın

**Sohbet içinde canlı sorgu:** container'ın ağı arxiv.org'a kapalı; `bash` ile
`curl` atma. Bunun yerine URL'yi kur ve `web_fetch` ile `export.arxiv.org`
adresini çek. Tek sayfa, `max_results` ≤ 50 tut; ikinci bir çağrı gerekiyorsa
arada bekle ve gerçekten gerekli olduğundan emin ol.

**Kullanıcının makinesi/sunucusu için:** `scripts/` altındaki hazır istemcileri
ver veya uyarla. Sunucuda çalıştırılacaksa `serverim-build` skill'inin
kurallarına uy.

---

## 3. Sorgu kurma akışı

1. **İhtiyacı alana çevir.** Konu → `abs:` + `ti:`; kişi → `au:`; alan →
   `cat:`; "şu konferansa gönderilmiş" → `co:` (comment) veya `jr:`.
2. **Terimleri tırnakla.** `abs:"mixture of experts"` ile `abs:mixture of
   experts` bambaşka şeydir; ikincisinde son iki kelime alansız serbest terime
   düşer.
3. **Boolean kur:** `AND`, `OR`, `ANDNOT`. Gruplama parantezle.
4. **Tarih daralt:** `submittedDate:[YYYYMMDDHHMM+TO+YYYYMMDDHHMM]` (GMT).
5. **Sıralamayı seç:** varsayılan `relevance`. "Yeni ne çıktı" sorusunda
   **her zaman** `sortBy=submittedDate&sortOrder=descending`.
6. **URL kaçışları:** boşluk `+`, tırnak `%22`, parantez `%28` `%29`.
7. **Doğrula:** dönen feed'in `<title>` alanı sorgunun kanonik hâlidir. Tırnak
   ve parantezler orada doğru görünüyorsa kaçışın doğrudur. Yanlış kurulmuş bir
   sorgu hata vermez — sessizce alakasız sonuç döndürür, bu yüzden `<title>`
   kontrolü ilk hata ayıklama adımıdır.

Alan önekleri, tam operatör tablosu, hazır sorgu reçeteleri ve isim
normalizasyonu tuzakları: **`references/query-syntax.md`**.

---

## 4. Sayfalama ve ölçek

- `max_results` tek çağrıda en fazla **2000**; `start` en fazla **30000**.
  `max_results > 30000` → HTTP 400.
- arXiv 1000'den fazla sonuç döndüren sorguyu daraltmanı öneriyor. 30000
  sonuçluk bir çağrı ~2 dakika sürer ve 15 MB'tan büyüktür.
- Pratikte sayfa boyutu **100–200** iyi dengedir; her sayfa arası 3 sn.
- **Derin sayfalama kırılgandır.** Yüksek `start` değerlerinde boş sayfa
  dönebilir. Çözüm: sayfalamayı derinleştirmek yerine sorguyu
  `submittedDate` aralıklarına böl (ay ay tara), her dilimi ayrı sorgula.
- Durma koşulu: dönen entry sayısı 0 **veya** `start ≥ opensearch:totalResults`.
  `totalResults`'a tek başına güvenme, boş sayfayı da kontrol et.
- Binlerce kaydı düzenli çekiyorsan yanlış kanaldasın → OAI-PMH.

---

## 5. Sonuçları okuma

Her `<entry>` için çıkarılacak çekirdek: `id` (URL'den arXiv ID + versiyon),
`title`, `summary` (abstract), yazarlar, `published` (v1 tarihi), `updated`
(çekilen versiyonun tarihi), `arxiv:primary_category`, tüm `category` etiketleri,
`arxiv:comment`, `arxiv:journal_ref`, `arxiv:doi`, PDF linki.

Sık yapılan hatalar:
- `category` listesi **cross-list** etiketlerini de içerir. "Bu makale asıl
  hangi alandan" sorusunun cevabı `arxiv:primary_category`.
- `published ≠ güncel versiyon tarihi`. v3 çektiysen `updated` v3'ün tarihidir.
- Aynı makale farklı versiyonlarla iki kez sayılabilir; dedupe anahtarı
  **versiyonsuz base ID**.
- Başlık ve abstract'ta satır sonu + fazladan boşluk vardır; whitespace
  normalize et. LaTeX matematik (`$...$`) ham gelir.
- `arxiv:comment` altın değerinde: sayfa sayısı, "accepted at NeurIPS 2026",
  "code available at …" bilgisi orada saklıdır.

Tam Atom şeması, alan tablosu, hata feed'i formatı ve ID formatları (eski
`cond-mat/0703001` vs yeni `2401.12345v2`): **`references/atom-schema.md`**.

---

## 6. Kullanıcıya sunum formatı

Makale listesi verirken ham XML veya çıplak link listesi dökme. Her makale:

```
**[Başlık]** — arXiv:2509.01234v1 · 2026-09-03 · cs.LG
Yazarlar (ilk 3, sonra "+N")
Ne yapıyor: [abstract'tan 1-2 cümle, kendi cümlelerinle]
Neden ilgilenirsin: [kullanıcının bağlamına göre tek cümle; yoksa atla]
https://arxiv.org/abs/2509.01234
```

Kurallar:
- Abstract'ı **özetle**, kopyalama.
- 5'ten fazla sonuçta önce tek paragraflık "genel manzara" (kaç makale, hangi
  temalar öne çıkmış), sonra liste.
- Alakasız sonuçları eleyip kaç tanesini elediğini söyle — sessizce kırpma.
- Bulamadıysan bunu açıkça söyle ve denediğin sorguyu göster; uydurma makale
  başlığı/ID'si **asla** üretme.

---

## 7. Radar (sürekli takip) kurmak

"Şu konuları takip et" isteği bir cron işidir, tek seferlik arama değil:

1. Her konu için **isimli sorgu** tanımla (2–5 konu ideal).
2. Günlük çalıştır (arXiv duyuru saatinden sonra, ör. sabah).
3. Görülen ID'leri kalıcı state dosyasında tut → sadece **yeni** olanları göster.
4. Versiyon güncellemelerini (v2, v3) ayrı bölümde göster ya da tamamen ele.
5. Çıktı: tarihli markdown digest.

`scripts/arxiv_radar.py` bunu yapar; örnek konfig `assets/radar.example.json`.

---

## 8. Kod üretirken standart

Ürettiğin her arXiv istemcisi şunları içerir, istenmese bile:

- Descriptive `User-Agent`
- İstekler arası ≥3 sn throttle (tek bağlantı, paralel yok)
- 429/503 için exponential backoff + `Retry-After` başlığına saygı
- Atom hata entry kontrolü
- Sayfa döngüsünde kesin durma koşulu (sonsuz döngü koruması)
- Uzun işlerde checkpoint (resumptionToken / son `start`) ki kesilince baştan
  başlamasın
- Yerel cache (aynı sorgu aynı gün → diskten)

Bunlar isteğe bağlı süsleme değil; olmadığı kod arXiv tarafından engellenir.

---

## 9. Bu skill'in yapamadıkları — kullanıcıya açıkça söyle

arXiv API şunları **vermez**, bu yüzden vaat etme:
- Atıf sayısı, h-index, etki faktörü (kaynak: Semantic Scholar / OpenAlex)
- Full-text arama (yalnızca başlık/abstract/comment/yazar alanları aranır)
- Semantik/embedding tabanlı benzerlik
- Hakem değerlendirmesi durumu — arXiv preprint arşividir, `journal_ref` veya
  `comment` alanı doluysa yayınlanmış olabilir, garanti değil
- "En popüler / en çok okunan" sıralaması

Kullanıcı bunları istiyorsa sınırı söyle ve elde edilebilir en yakın vekil
ölçütü öner (ör. `journal_ref` doluluğu, `comment`'teki konferans adı).

---

## Referans dosyaları

Gerektiğinde oku, hepsini birden yükleme:

- **`references/query-syntax.md`** — alan önekleri, boolean/gruplama,
  `submittedDate` aralığı, `id_list` mantığı, hazır sorgu reçeteleri,
  yazar adı ve kategori tuzakları. Sorgu kurarken veya "sonuç yanlış geliyor"
  denildiğinde oku.
- **`references/atom-schema.md`** — Atom feed ve entry alanlarının tam tablosu,
  `arxiv:` uzantı elemanları, hata feed'i, ID/versiyon formatları,
  RSS/ATOM besleme yapısı. Parser yazarken veya alan eşlemesi yaparken oku.
- **`references/oai-pmh.md`** — OAI-PMH verb'leri, yeni base URL, set yapısı,
  metadata prefix'leri, resumptionToken ve artımlı hasat stratejisi, S3 bulk
  erişim. Toplu hasat, senkronizasyon veya veri seti kurulumunda oku.

## Scriptler

Python 3, sadece standart kütüphane (`urllib`, `xml.etree`) — bağımlılık yok.

- **`scripts/arxiv_query.py`** — rate-limit'e uyan sayfalamalı Query API
  istemcisi. `--query`, `--id`, `--since/--until`, `--max`, çıktı `md|json|csv`.
- **`scripts/arxiv_oai.py`** — resumptionToken'lı OAI-PMH hasatçısı, JSONL
  çıktısı, checkpoint ile kaldığı yerden devam.
- **`scripts/arxiv_radar.py`** — konfig dosyasındaki sorguları çalıştırır,
  görülenleri state'te tutar, yalnızca yeni makalelerin markdown digest'ini üretir.

Kullanım: `python scripts/arxiv_query.py --help`
