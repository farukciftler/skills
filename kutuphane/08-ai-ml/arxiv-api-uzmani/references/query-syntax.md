# search_query Sözdizimi ve Reçeteler

Kaynak: https://info.arxiv.org/help/api/user-manual.html (§5.1) — doğrulama 2026-09-08.

## İçindekiler
1. Uç nokta ve parametreler
2. Alan önekleri
3. Boolean ve gruplama
4. Tarih filtresi
5. id_list mantığı ve versiyonlar
6. URL kaçış tablosu
7. Hazır sorgu reçeteleri
8. Tuzaklar

---

## 1. Uç nokta ve parametreler

```
http://export.arxiv.org/api/query?{parametreler}
```
HTTPS de çalışır. GET veya POST; sorgu çok uzunsa POST tercih et.

| Parametre | Tip | Varsayılan | Not |
|---|---|---|---|
| `search_query` | string | — | Alan önekli sorgu |
| `id_list` | virgüllü liste | — | arXiv ID'leri |
| `start` | int | 0 | 0 tabanlı, ≤ 30000 |
| `max_results` | int | 10 | ≤ 2000 (tek çağrı), >30000 → HTTP 400 |
| `sortBy` | enum | `relevance` | `relevance` \| `lastUpdatedDate` \| `submittedDate` |
| `sortOrder` | enum | `descending` | `ascending` \| `descending` |

`search_query` ve `id_list` birlikte verilirse: `id_list`'teki makalelerden
sorguya uyanlar döner (filtre olarak kullanılabilir).

## 2. Alan önekleri

| Önek | Alan |
|---|---|
| `ti` | Başlık |
| `au` | Yazar |
| `abs` | Abstract |
| `co` | Comment (yazar notu) |
| `jr` | Journal reference |
| `cat` | Kategori (ör. `cs.LG`) |
| `rn` | Report number |
| `id` | ID — **kullanma**, `id_list` kullan |
| `all` | Yukarıdakilerin hepsinde birden |

## 3. Boolean ve gruplama

Operatörler: `AND`, `OR`, `ANDNOT` (büyük harf).

```
au:del_maestro+AND+ti:checkerboard
au:del_maestro+ANDNOT+%28ti:checkerboard+OR+ti:Pyrochlore%29
ti:%22quantum+criticality%22
```

`ANDNOT` gürültü elemek için en değerli operatör: `cat:cs.LG+ANDNOT+cat:cs.CV`.

## 4. Tarih filtresi

Tek tarih alanı `submittedDate`, format `[YYYYMMDDHHMM+TO+YYYYMMDDHHMM]`, GMT,
dakika hassasiyetinde:

```
search_query=cat:cs.LG+AND+submittedDate:[202609010000+TO+202609080000]
```

Not: `lastUpdatedDate` yalnızca **sıralama** için vardır, filtrelenemez.
Sadece v1'leri (yeni makaleler, revizyon değil) istiyorsan API bunu doğrudan
filtreleyemez — çekip `published == updated` olanları ayıkla.

## 5. id_list ve versiyonlar

```
?id_list=2401.12345,cond-mat/0207270      → en güncel versiyon
?id_list=cond-mat/0207270v1                → v1
```
`search_query=id:xxx` versiyon davranışını doğru yönetmez; **her zaman**
`id_list` kullan. Bozuk ID → hata feed'i.

Tek çağrıda güvenli ID sayısı ~100; daha fazlasını parçala.

## 6. URL kaçış tablosu

| Sembol | Kaçış | Amaç |
|---|---|---|
| boşluk | `+` | alanları/terimleri ayırma |
| `"` | `%22` | tam ifade araması |
| `(` `)` | `%28` `%29` | gruplama |
| `:` | ham bırakılabilir | önek ayırıcı |

Doğrulama: yanıt feed'inin `<title>` alanı sorgunun kanonik hâlini gösterir.
Tırnak/parantez orada beklediğin gibi görünmüyorsa kaçış yanlıştır.

## 7. Hazır sorgu reçeteleri

**Son bir haftanın belirli konudaki makaleleri**
```
search_query=cat:cs.LG+AND+abs:%22mixture+of+experts%22+AND+submittedDate:[202609010000+TO+202609080000]
&sortBy=submittedDate&sortOrder=descending&max_results=100
```

**Bir yazarın çalışmaları, isim benzerliğini daraltarak**
```
search_query=au:%22Hinton_G%22+AND+cat:cs.LG&sortBy=submittedDate&sortOrder=descending
```

**Çok kategorili günlük tarama (cross-list dahil)**
```
search_query=%28cat:cs.LG+OR+cat:cs.CL+OR+cat:stat.ML%29+AND+abs:quantization
&sortBy=submittedDate&sortOrder=descending
```

**Konferansa kabul edilmişler (comment alanından)**
```
search_query=cat:cs.CL+AND+co:%22NeurIPS+2026%22
```

**Dergide yayımlanmış olanlar**
```
search_query=cat:cs.AI+AND+jr:Nature
```

**Gürültü elemeli daraltma**
```
search_query=abs:%22on-device%22+AND+cat:cs.LG+ANDNOT+cat:cs.CV
```

**Belirli makalelerin künyesi**
```
?id_list=2509.01234,2412.09876v2
```

## 8. Tuzaklar

1. **Tırnaksız çok kelimeli terim.** `abs:mixture of experts` → yalnızca
   `mixture` abstract'ta aranır, kalan kelimeler serbest terime düşer.
2. **Yazar adı normalizasyonu belirsizdir.** `au:del_maestro`, `au:"Del
   Maestro, A"` gibi varyantlar farklı sonuç verebilir; Türkçe/aksanlı
   karakterler eşleşmeyebilir. Yazar aramasını **her zaman** `cat:` veya `ti:`
   ile daralt ve kullanıcıya "isim eşleşmesi tam değil" uyarısı ver.
3. **`cat:` cross-list'i de yakalar.** Sadece birincil alanı istiyorsan sonucu
   `arxiv:primary_category` üzerinden filtrele.
4. **`all:` fazla geniştir.** Comment ve journal_ref'te geçen kelimeler yüzünden
   alakasız sonuç getirir; ciddi taramada `abs`/`ti` kullan.
5. **Varsayılan sıralama relevance.** "En yeni" istendiğinde `sortBy` vermeyi
   unutma; unutulduğunda sonuç sessizce yanlış olur.
6. **Boş sonuç ≠ makale yok.** Önce `<title>`'daki kanonik sorguyu oku;
   çoğu zaman kaçış hatasıdır.
7. **Kategori kodları büyük/küçük harfe duyarlı yazılır** (`cs.LG`, `math.QA`,
   `hep-th`). RSS URL'lerinde küçük harf tolere edilir, API'de doğru yaz.
   Tam liste: https://arxiv.org/category_taxonomy
8. **Aynı gün tekrar sorgulamak yeni sonuç getirmez** — sonuç kümesi günde bir
   güncellenir.
