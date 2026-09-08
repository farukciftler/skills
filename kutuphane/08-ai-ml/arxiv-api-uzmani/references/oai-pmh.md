# OAI-PMH ile Toplu Metadata Hasadı ve S3 Bulk Veri

Kaynak: https://info.arxiv.org/help/oa/index.html,
https://info.arxiv.org/help/bulk_data_s3.html — doğrulama 2026-09-08.

## İçindekiler
1. Base URL (Mart 2025 değişikliği)
2. Verb'ler
3. Metadata formatları
4. Set yapısı
5. Datestamp ve artımlı hasat
6. resumptionToken
7. Hasat stratejisi
8. S3 bulk (tam metin)

---

## 1. Base URL

```
https://oaipmh.arxiv.org/oai
```

**Mart 2025'te sistem baştan yazıldı.** Eski `http://export.arxiv.org/oai2`
adresini kullanan kod ve tutorial'lar hâlâ dolaşımda — güncelini kullan.
Diğer değişiklikler:
- En erken datestamp `2007-05-23` → **`2005-09-16`**; 2005 öncesi tüm makaleler
  dahil edildi ve hepsi aynı en erken tarihi paylaşıyor.
- Set yapısı `group:archive:CATEGORY` biçiminde detaylandı (eski setSpec'ler
  hâlâ geçerli).
- resumptionToken artık toplam sayıyı ve cursor'ı içermiyor, **günlük
  expire oluyor** → uzun hasadı ertesi güne sarkıtma.
- Alias kategorideki makaleler her iki sette de görünüyor.

## 2. Verb'ler

| Verb | Kullanım |
|---|---|
| `Identify` | Depo bilgisi, `earliestDatestamp`, politikalar |
| `ListMetadataFormats` | Desteklenen formatlar |
| `ListSets` | Tüm setler (kategori/arşiv/grup) |
| `ListIdentifiers` | Sadece ID + datestamp (hafif; önce bunu çek) |
| `ListRecords` | Tam metadata kayıtları |
| `GetRecord` | Tek makale (`identifier=oai:arXiv.org:0804.2273`) |

Örnek:
```
https://oaipmh.arxiv.org/oai?verb=ListRecords&set=cs:cs:AI&from=2026-09-01&metadataPrefix=arXiv
https://oaipmh.arxiv.org/oai?verb=GetRecord&identifier=oai:arXiv.org:0804.2273&metadataPrefix=arXiv
```

Identifier biçimi: `oai:arXiv.org:{arxiv_id}`.

## 3. Metadata formatları

| Prefix | İçerik | Ne zaman |
|---|---|---|
| `oai_dc` | Dublin Core | Sadece jenerik katalog uyumu gerekiyorsa |
| `arXiv` | arXiv'e özgü: ayrıştırılmış yazar adları, kategoriler, **lisans** | Varsayılan tercih |
| `arXivRaw` | İç formata en yakın, **versiyon geçmişi** dahil | Versiyon/tarih analizi gerekiyorsa |

Lisans bilgisi yalnızca `arXiv` / `arXivRaw` formatlarında gelir — bir makalenin
PDF'ini yeniden dağıtıp dağıtamayacağını **burada** kontrol edersin.

Her item = bir makale ve **yalnızca en güncel versiyon** ifşa edilir; geçmiş
versiyonlar için `arXivRaw`.

## 4. Set yapısı

`group:archive:CATEGORY` hiyerarşisi:

```
cs:cs:AI          → sadece cs.AI kategorisi
physics:hep-th    → tüm hep-th arşivi
physics           → tüm fizik arşivleri
math:math:NA      → math.NA
(set verilmezse)  → tüm arXiv
```

Tam liste: `?verb=ListSets`. Kategori kodunun harf büyüklüğü setSpec'te
korunur (`cs:cs:AI`, `math:math:NA`).

## 5. Datestamp ve artımlı hasat

`datestamp` = kaydın **son değişiklik** zamanı, gönderim zamanı değil. arXiv
geçmişte toplu metadata güncellemeleri yaptığı için eski makalelerin datestamp'i
gerçek gönderim tarihiyle uyuşmaz.

**Bunun sonucu:** OAI-PMH ile "Şubat 2001'de gönderilen makaleler" gibi seçici
bir hasat **yapılamaz**. Gönderim tarihine göre seçim gerekiyorsa Query API
`submittedDate` kullan.

OAI-PMH'nin tasarım amacı: tam kopya al, sonra artımlı senkronize et.

- İlk hasat: `from`/`until` **vermeden** (önerilen) ya da
  `earliestDatestamp`'ten itibaren.
- Sonraki hasatlar: `from` = son hasadın tarihi (tarihi **sunucunun son
  yanıtından** al), `until` verme.

## 6. resumptionToken

Yanıtın sonunda gelir; bir sonraki istekte **tek başına** gönderilir:

```
?verb=ListRecords&resumptionToken=<token>
```

Kurallar:
- `resumptionToken` ile birlikte `set`/`from`/`metadataPrefix` **gönderme**.
- Token günlük expire olur; hasat kesilirse token'ı değil, son işlenen
  datestamp'i checkpoint'le ve `from` ile yeniden başla.
- Boş `resumptionToken` elemanı = liste bitti.
- `noRecordsMatch` hata kodu bir arıza değil, "eşleşme yok" demektir.

## 7. Hasat stratejisi

1. `Identify` ile `earliestDatestamp` ve `granularity`yi al.
2. Kapsamı daralt: tüm arXiv yerine ihtiyacın olan set(ler).
3. Önce `ListIdentifiers` ile hacmi ölç (kaç kayıt geleceğini gör), sonra
   `ListRecords`.
4. Her istek arası **≥3 saniye**, tek bağlantı. Paralel hasat ToU ihlali.
5. Ham XML yanıtları diske de yaz (yeniden ayrıştırabilmek için) — hasadı
   tekrarlamak pahalıdır.
6. JSONL olarak akıt, belleğe toplama.
7. Checkpoint: son datestamp + işlenen kayıt sayısı.
8. 503 gelirse `Retry-After` başlığına uy; OAI-PMH'de 503 normal akış
   kontrolüdür, hata değil.

## 8. S3 bulk (tam metin)

Metadata değil, **PDF ve LaTeX kaynak** dosyaları için:

- Bucket: `s3://arxiv/` — **requester-pays**, bölge us-east-1 (N. Virginia).
  İndirme bedelini sen ödersin, bölge dışına çıkmak pahalıdır.
- PDF: `pdf/arXiv_pdf_YYMM_NNN.tar` (~500 MB'lık parçalar)
- Kaynak: `src/arXiv_src_YYMM_NNN.tar`
- Manifestler: `pdf/arXiv_pdf_manifest.xml`, `src/arXiv_src_manifest.xml` —
  her parça için md5, ilk/son makale ID'si, kayıt sayısı, boyut.
- Toplam boyut Nisan 2025 itibarıyla ~9,2 TB, aylık ~100 GB büyüyor.
- Güncelleme: yaklaşık aylık.

**Lisans uyarısı:** makalelerin büyük çoğunluğu arXiv'e yeniden dağıtım hakkı
vermeyen varsayılan lisansla gönderilmiştir. Full-text üzerine indeks/araç
kurabilirsin ama **indirme için arXiv'e link vermek zorundasın**; PDF'leri
kendi sunucundan servis edemezsin. İstisnaları OAI-PMH `arXiv` formatındaki
lisans alanından kontrol et.
