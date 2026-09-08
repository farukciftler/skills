# Atom Yanıtı, ID Formatları ve Beslemeler

Kaynak: https://info.arxiv.org/help/api/user-manual.html (§3.3, §5.2),
https://info.arxiv.org/help/rss.html — doğrulama 2026-09-08.

## İçindekiler
1. Namespace'ler
2. Feed düzeyi alanlar
3. Entry düzeyi alanlar
4. arxiv: uzantı elemanları
5. Hata feed'i
6. arXiv ID formatları
7. Parser iskeleti
8. RSS / ATOM günlük beslemeleri

---

## 1. Namespace'ler

```xml
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
```

Python `xml.etree` için:
```python
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}
```

## 2. Feed düzeyi alanlar

| Alan | Anlamı |
|---|---|
| `<title>` | Sorgunun **kanonik** hâli — kaçış doğrulaması burada yapılır |
| `<id>` | Bu sorguya özel benzersiz id |
| `<updated>` | Sonuçların son güncellenme anı = çağrı gününün gece yarısı |
| `<link rel="self">` | Aynı feed'i getirecek GET URL'i |
| `<opensearch:totalResults>` | Toplam eşleşme sayısı |
| `<opensearch:startIndex>` | Dönen ilk sonucun 0 tabanlı indeksi |
| `<opensearch:itemsPerPage>` | Dönen sonuç sayısı |

## 3. Entry düzeyi alanlar

| Alan | Anlamı |
|---|---|
| `<title>` | Makale başlığı (satır sonları içerir, normalize et) |
| `<id>` | `http://arxiv.org/abs/{id}v{n}` — ID buradan çıkarılır |
| `<published>` | **v1**'in gönderim tarihi |
| `<updated>` | Çekilen versiyonun gönderim tarihi (v1 ise `published` ile aynı) |
| `<summary>` | Abstract |
| `<author><name>` | Yazarlar, yazarlık sırasında; opsiyonel `<arxiv:affiliation>` |
| `<category term=… scheme=…>` | arXiv + varsa ACM/MSC etiketleri (cross-list dahil) |
| `<link>` | En çok 3 tane, aşağıdaki tabloya göre ayrışır |

`<link>` ayrımı:

| rel | title | işaret ettiği | her zaman var mı |
|---|---|---|---|
| `alternate` | — | abstract sayfası | evet |
| `related` | `pdf` | PDF | evet |
| `related` | `doi` | çözümlenmiş DOI | hayır |

## 4. arxiv: uzantı elemanları

| Eleman | İçerik |
|---|---|
| `<arxiv:primary_category term=…>` | **Birincil** kategori — asıl alan budur |
| `<arxiv:comment>` | Yazar notu: sayfa/şekil sayısı, konferans kabulü, kod linki |
| `<arxiv:affiliation>` | `<author>` altında, varsa kurum |
| `<arxiv:journal_ref>` | Dergi künyesi (varsa yayımlanmış demektir) |
| `<arxiv:doi>` | DOI |

`comment` alanı yapılandırılmamış serbest metindir ama pratikte en bilgi yoğun
alandır: "Accepted at ICLR 2026", "code: github.com/…", "v2: fixed proof".

## 5. Hata feed'i

Hatalar **HTTP 200** ile, tek entry'li Atom olarak döner:

```xml
<entry>
  <id>http://arxiv.org/api/errors#incorrect_id_format_for_1234.12345</id>
  <title>Error</title>
  <summary>incorrect id format for 1234.12345</summary>
</entry>
```

Parser kontrolü: tek entry var **ve** `title == "Error"` → hata; `summary`'yi
kullanıcıya göster.

Bilinen hata sebepleri: `start` int değil / negatif, `max_results` int değil /
negatif, bozuk ID formatı. `max_results > 30000` ise HTTP 400 döner.

## 6. arXiv ID formatları

- **Yeni (2007-04'ten beri):** `YYMM.NNNNN` — 2015 öncesi 4 haneli sıra
  (`0704.0001`), sonrası 5 haneli (`2401.12345`).
- **Eski:** `archive/YYMMNNN` — ör. `cond-mat/0703001`, `hep-ex/0307015`.
  Slash içerir; dosya adı/URL/DB anahtarı yaparken kaçış gerektirir.
- **Versiyon:** sona `v{n}` — `2401.12345v2`. Versiyonsuz hâl "en güncel"
  anlamına gelir.

Regex (ikisini de yakalar):
```python
r"(?:(\d{4}\.\d{4,5})|([a-z\-]+(?:\.[A-Z]{2})?/\d{7}))(v\d+)?"
```

Dedupe anahtarı **versiyonsuz base ID**'dir.

## 7. Parser iskeleti

```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_bytes)
entries = root.findall("atom:entry", NS)

if len(entries) == 1 and (entries[0].findtext("atom:title", "", NS).strip() == "Error"):
    raise RuntimeError(entries[0].findtext("atom:summary", "", NS).strip())

for e in entries:
    abs_url = e.findtext("atom:id", "", NS)
    full_id = abs_url.rsplit("/abs/", 1)[-1]          # 2401.12345v2
    base_id = full_id.split("v")[0] if "." in full_id else full_id
    rec = {
        "id": base_id,
        "version_id": full_id,
        "title": " ".join(e.findtext("atom:title", "", NS).split()),
        "abstract": " ".join(e.findtext("atom:summary", "", NS).split()),
        "authors": [a.findtext("atom:name", "", NS)
                    for a in e.findall("atom:author", NS)],
        "published": e.findtext("atom:published", "", NS),
        "updated": e.findtext("atom:updated", "", NS),
        "primary": (e.find("arxiv:primary_category", NS) or {}).get("term"),
        "categories": [c.get("term") for c in e.findall("atom:category", NS)],
        "comment": e.findtext("arxiv:comment", "", NS),
        "journal_ref": e.findtext("arxiv:journal_ref", "", NS),
        "doi": e.findtext("arxiv:doi", "", NS),
        "abs_url": f"https://arxiv.org/abs/{base_id}",
    }
```

Not: eski ID'lerde `split("v")` yanlış keser (`cond-mat/...` içinde `v` yok ama
arşiv adında olabilir) — yukarıdaki regex'i kullanmak daha güvenlidir.

## 8. RSS / ATOM günlük beslemeleri

Query API'den ayrı bir kanaldır; "bugün ne duyuruldu" için tasarlanmıştır.
Günlük, gece yarısı ET güncellenir.

```
https://rss.arxiv.org/rss/cs.LG          (RSS 2.0)
https://rss.arxiv.org/atom/cs.LG         (Atom)
https://rss.arxiv.org/rss/cs            (tüm arşiv)
https://rss.arxiv.org/rss/cs.AI+q-bio.NC (çoklu kategori, `+` ile; limit 2000 sonuç)
```

Durum sayfası: https://rss.arxiv.org/feed/status
Spesifikasyonlar: `/help/rss_specifications.html`, `/help/atom_specifications.html`

Besleme öğeleri yeni gönderimleri **ve** güncellenen (replace) makaleleri
içerir; ayrımı öğe açıklamasındaki duyuru tipinden yaparsın. Sadece yeni
makale istiyorsan Query API + `submittedDate` aralığı daha kesin sonuç verir.
Aynı 1 istek/3 saniye limiti burada da geçerlidir.
