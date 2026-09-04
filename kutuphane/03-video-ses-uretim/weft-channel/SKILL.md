---
name: weft-channel
description: Weft Records YouTube kanalını yükleme SONRASINDA yönetir — Studio analitiklerini okumak, sayıları kataloğa yazmak, topluluk (Community) duyurusu geçmek, oynatma listesi/bitiş ekranı/sabitlenmiş yorum kurmak, yorumları yanıtlamak, kanal açıklaması ve anahtar kelimelerini güncellemek, düşük performansta başlık/thumbnail müdahalesine karar vermek. Kanal işleri Chrome eklentisiyle studio.youtube.com üzerinden sürülür. Tetikleyiciler: "kanala bak", "analitik", "youtube studio", "kaç görüntüleme", "views ölç", "CTR", "duyuru geç", "community post", "topluluk gönderisi", "oynatma listesi", "playlist", "bitiş ekranı", "sabitlenmiş yorum", "yorumlara bak", "abone", "kanal açıklaması", "başlığı değiştir", "thumbnail değiştir", "video yayınlandı sonra ne yapacağız", "+30 gün ölçümü". Bir video YouTube'a yüklendikten sonraki HER iş bu skill'e aittir.
---

# Weft Channel — kanal yönetimi ve ölçüm

`weft-release` bir yayını **çıkarır**. Bu skill onu **yaşatır**: yüklendikten
sonra kapanmayan işler, kanal düzeyindeki her alan ve sayının kataloğa dönmesi.

İki şeyi garantiler:

1. **Hiçbir yayın ölçülmeden geçmez.** Sayı ekranda kalmaz, `analytics.csv`'ye yazılır.
2. **Hiçbir kanal işi hafızada kalmaz.** Duyuru, playlist, başlık düzeltmesi — hepsi `channel_log.csv`'ye bir satır.

## İş bölümü

| İş | Nerede |
|---|---|
| Kimlik, brief, beste, kapak, video, preflight | `weft-release` |
| Başlık/açıklama/tag'lerin **ilk** yazımı ve SEO denetimi | `healing-audio-youtube-seo` |
| Yükleme (adım 10) — dosyayı Studio'ya sokup yayına alma | `CLAUDE.md` § 5 |
| **Yüklemeden sonrası: analitik, duyuru, playlist, yorum, kanal alanları, müdahale kararı** | **burası** |

Sınır nettir: video yayına girdiği an iş bu skill'e geçer. Başlık **yeniden**
yazılacaksa metni yine `healing-audio-youtube-seo` üretir, bu skill kararı
verir, değişikliği Studio'da uygular ve loglar.

## Her işten önce çalıştır

```bash
python3 .claude/skills/weft-channel/scripts/channel_report.py
```

Ölçüm borcu olan yayınlar, tutarsız `status` alanları, URL'siz yayınlar, gecikmiş
topluluk gönderisi — hepsi tek çıktıda. **Kanala bakmadan önce bu çalışır**;
tarayıcıda ne arayacağını bu belirler. `--json` makine okuması, `--today` ölçüm
gününü sabitlemek için.

## Beş iş

Kullanıcının isteğine göre birini seç ve **sadece onu** yürüt.

| Kullanıcı der ki | İş | Oku |
|---|---|---|
| "video yüklendi", "sırada ne var" | Yükleme sonrası kapanış | `references/post-upload-runbook.md` |
| "analitiğe bak", "kaç görüntüleme", "CTR ne" | Ölçüm ve okuma | `references/analytics-playbook.md` |
| "duyuru geç", "topluluk gönderisi" | Duyuru | `references/community-and-channel.md` + `assets/community-post-templates.md` |
| "playlist", "bitiş ekranı", "kanal açıklaması" | Kanal bakımı | `references/community-and-channel.md` |
| "bu video tutmadı", "başlığı değiştirelim mi" | Müdahale kararı | `references/analytics-playbook.md` § Karar tablosu |

Tarayıcı mekaniği hepsinde ortak: `references/studio-browser.md`. Studio'da ilk
tıklamadan önce oku — hangi URL, hangi seçici, hangi tuzak orada.

## Değişmez kurallar

**Kanalı yüklemeden önce doğrula.** Studio'da sol üstte `Weft Records` yazmıyorsa
hiçbir şey yapma. Faruk'un birden fazla Google hesabı var; yanlış kanala geçilen
bir duyuru geri alınamaz. (`CLAUDE.md` § 5, aynı kural yüklemede de var.)

**Sayı ekrandan okunur, hafızadan değil.** Bir metriği yazmadan önce onu o
oturumda gördüğün ekranda göster. Önceki oturumdan hatırlanan sayı yazılmaz.
Her sayının yanında **hangi gün** ve **hangi dönem** (lifetime/28d/7d) okunduğu
yazar — dönemsiz sayı karşılaştırılamaz, yani işe yaramaz.

**Farklı yaştaki yayınlar karşılaştırılmaz.** WR-015 üç günlük, WR-002 bir
aylık; ham `views` bunları sıralamaz. Karşılaştırma **gün-N** kovalarıyla
yapılır (`channel_report.py` GÜN-N tablosu). Sonda dalgasının şerit deneyi de
bu kurala bağlı: `docs/roster-experiment.md` § 2.

**Gürültü eşiği: 1000 gösterim.** Altında CTR bir ölçüm değil, rastlantı. "CTR
düşük, thumbnail'ı değiştirelim" demeden önce gösterim sayısına bak. Ölçüm
yapılamıyorsa **"veri yetersiz" de**, tahmin üretme.

**48 saat kuralı karar içindir, ölçüm için değil.** Yayının ilk 48 saati
YouTube'un dağıtım denemesidir; o pencerede müdahale kararı verilmez. Ama
gösterim eşiği dolmuşsa (≥1000) CTR o gün de okunur ve taban satırı olarak
yazılır — gösterim, görüntülemeden çok daha hızlı birikiyor. İlk **karar**
okuması gün 7.

**Geri alınamayan işi sorma olmadan yapma.** Video silme, görünürlük düşürme,
topluluk gönderisi silme, kanal adı/handle değiştirme, yorum silme, oynatma
listesi silme — hepsi Faruk'un onayıyla. Ekleme ve düzeltme (playlist'e ekleme,
açıklama düzeltme, tag ekleme) serbest.

**Yayın metni İngilizce.** Topluluk gönderisi, playlist adı ve açıklaması,
sabitlenmiş yorum — hepsi dinleyiciye bakar, hepsi İngilizce. Yer tutucu yok
(`CLAUDE.md` § 4). Müziği plak gibi sunan her gönderide künye satırı bulunur.

**Sağlık iddiası yok.** Bu kanal fonksiyonel müzik yayınlıyor; topluluk
gönderisi de açıklama kadar politikaya tabi. Kural ve ikame tablosu
`healing-audio-youtube-seo/references/claims-and-policy.md`'de.

## Her iş bitiminde

1. Ölçüm yaptıysan → `analytics.csv` satırı (`yt_import.py` ile, elle değil).
2. Kanalda bir şey değiştirdiysen → `channel_log.csv` satırı.
3. Yayın durumu değiştiyse → `publishing.csv` (`views`, `status`, `notes`) ve gerekiyorsa `releases.csv`.
4. `python3 catalog/build_workbook.py` — Excel'i tazele.
5. Kullanıcıya tek tabloyla göster: ne ölçüldü, ne değişti, hangi CSV'ye yazıldı.

## Katalog alanları

Bu skill iki yeni tabloyu besler; ID'ler asla yeniden kullanılmaz.

| Dosya | Ne tutar | Anahtar |
|---|---|---|
| `catalog/analytics.csv` | Her ölçüm anlık görüntüsü — video ve kanal | `AN-NNNN` |
| `catalog/channel_log.csv` | Kanalda yapılan her iş | `CH-NNNN` |

`analytics.csv` alanları: `date` (ölçümün yapıldığı gün), `scope`
(`video`/`channel`), `period` (`lifetime`/`90d`/`28d`/`7d`/`48h`),
`impressions`, `ctr_pct`, `views`, `avg_view_duration_sec`, `watch_hours`,
`subs_gained`, `likes`, `comments`, `top_traffic_source`, `top_query`,
`source` (`studio-export:…` / `studio-ui`), `notes`.

`channel_log.csv` `type` değerleri: `community` · `playlist` · `end_screen` ·
`card` · `pinned_comment` · `title_edit` · `desc_edit` · `thumbnail_edit` ·
`tag_edit` · `settings` · `reply` · `branding`.

## Script'ler

```bash
# durum — her işten önce
python3 .claude/skills/weft-channel/scripts/channel_report.py

# Studio → Analitik → Gelişmiş mod → Dışa aktar (CSV) çıktısını içeri al
python3 .claude/skills/weft-channel/scripts/yt_import.py import \
  --export ~/Downloads/Analytics.zip --period 28d [--dry-run]

# ekrandan okunan tek video ölçümü
python3 .claude/skills/weft-channel/scripts/yt_import.py add \
  --release WR-015 --views 612 --impressions 12400 --ctr 5.1 \
  --avd 17:40 --watch-hours 180.2 --period 28d
```

`yt_import.py` sütun adlarını İngilizce ve Türkçe arayüz için tanır; tanımadığı
sütunu **uydurmaz**, gördüğü başlıkları basıp o alanı boş bırakır. Sayaç
sütunlarında ayırıcı binlik, oran sütunlarında ondalık kabul edilir
(`24.905` → 24905, `4,7` → 4.7).

## Bu skill nerede kırılır

- **Tek sayıya bakıp karar vermek.** `views` düştü diye başlık değiştirmek; oysa görünen tek şey gösterimin durduğu. Önce gösterim → CTR → ortalama süre zincirine bak, kırılan halkayı bul.
- **Ölçmeden duyuru geçmek.** Topluluk gönderisi trafiği kanalın en sadık kesimine gider; henüz izlenmemiş bir videoya atılan gönderi o kesimi harcar. Yayın günü gönderisi doğru, ama ikinci gönderi ölçümden sonra.
- **Studio'yu ekran görüntüsüyle sürmek.** Sayıyı `get_page_text` ile al, ekran görüntüsünü **doğrulama** için kullan. Tersi hem yavaş hem hataya açık.
- **Kaydetmeden çıkmak.** Studio'nun bazı ekranları otomatik kaydeder, bazıları `Kaydet` düğmesi ister. Düğme varsa basıldığını ve durumun `Kaydedildi` olduğunu **gör**, sonra sekmeyi bırak.
- **Uzun videoyu yüzdeyle yargılamak.** Bir saatlik albümde "ortalama izlenme yüzdesi %4" normaldir; anlamlı olan **mutlak dakika** ve toplam izlenme saati.
