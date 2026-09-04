# Yükleme sonrası — kapanış listesi

`CLAUDE.md` § 2'deki akış 10. adımda videoyu yayına alıyor, 11'de URL'i
kaydediyor. Bir yayın orada bitmiyor. Bu dosya 10'dan sonrasını yürütür.

```
10  YÜKLEME     yüklendi, yayına alındı                       (weft-release / CLAUDE.md § 5)
─────────────────────────────────────────────────────────────────────────────
11  KAYIT       URL + tarih                → publishing.csv + LINKS.md
12  DOĞRULAMA   yayınlanan sayfa kontrolü  → gerekiyorsa düzeltme
13  KANAL       playlist · bitiş ekranı · sabitlenmiş yorum   → channel_log.csv
14  DUYURU      topluluk gönderisi                            → channel_log.csv
15  ÖLÇÜM       gün-2 bütünlük · gün-7 · gün-30               → analytics.csv
```

11 ve 12 **yayın günü** yapılır, 13–14 aynı gün ya da ertesi gün, 15 takvime
bağlıdır.

---

## 11 — Kayıt

```bash
python3 scripts/build_links.py          # LINKS.md tazelenir
python3 catalog/build_workbook.py       # Excel
```

`publishing.csv`: `url`, `published_date`, `status = released`,
`views_check_date = published_date + 30 gün`, `notes` (dosya adı, çözünürlük,
süre, boyut). `releases.csv`: `status = released`, `released_date`.

> **`published` yazma, `released` yaz.** `docs/conventions.md` durum listesinde
> `published` yok; veride iki farklı ad var ve `channel_report.py` bunu uyarı
> olarak gösteriyor. Yeni satırlar `released` yazar.

## 12 — Doğrulama (yayın günü, yüklemeden ~20 dk sonra)

Videonun **izleyici sayfasında** — Studio'da değil — kontrol edilecekler:

| Kontrol | Nasıl |
|---|---|
| Başlık birebir doğru | `metadata.md` ile karşılaştır, kopyalanırken kırpılmış olabilir |
| Açıklama tam, bağlantılar tıklanabilir | ilk satır ve künye satırı görünüyor mu |
| **Bölümler (chapters) oluşmuş** | oynatıcı çubuğunda bölünme var mı; yoksa `0:00` ilk satır değildir ya da bölüm sayısı/aralığı yetersizdir |
| Thumbnail doğru dosya | akışta görünen kare video sahnesinden mi (kapak değil) |
| Etiketler kaydolmuş | Studio'da düzenleme ekranı, "Daha fazla göster" altında çipler |
| Görünürlük **Herkese açık** | Faruk'un kalıcı talimatı (2026-08-08) |
| Çocuklara özel **Hayır** | zorunlu alan, yanlışsa yorumlar kapanır |
| Çözünürlük 1440p'ye çıkmış | işlenme bitmemişse 720p'de takılı görünür, birkaç saat bekler |
| Ses senkron ve sonuna kadar var | son dakikaya atla, sessizlik yoksa tamam |

Bölüm oluşmadıysa açıklama düzeltilir ve yeniden kaydedilir; düzeltme
`channel_log.csv`'ye `desc_edit` olarak yazılır.

## 13 — Kanal işleri

1. **Playlist.** Seri playlist'i + varsa sanatçı ve işlev playlist'i. Yoksa aç (`community-and-channel.md` § 2).
2. **Bitiş ekranı.** İzleyiciye en uygun video + abone ol + seri playlist'i.
3. **Sabitlenmiş yorum.** Bir cümle iddia + playlist bağlantısı.
4. Uzun formatta kart **konmaz**.

Her biri doğrulanır (`studio-browser.md` § 4) ve `channel_log.csv`'ye bir satır
yazar. Üç iş üç satır; tek satırda toplama.

## 14 — Duyuru

Topluluk sekmesi varsa yayın günü gönderisi (`assets/community-post-templates.md`
§ 1). Yoksa sabitlenmiş yorum ve kanal açıklaması duyuru yerine geçer — eksik
sekme uydurulmaz.

## 15 — Ölçüm takvimi

| Gün | İş |
|---|---|
| gün 2 | Bütünlük kontrolü (12. adım hâlâ doğru mu, işlenme bitti mi). **Sayı yazılmaz.** |
| gün 7 | İlk ölçüm → `analytics.csv` (`period=lifetime`) |
| gün 14 | İkinci ölçüm |
| gün 30 | Karar ölçümü → `analytics.csv` + `publishing.csv` `views` |
| gün 90 | Uzun format eğrisi |

`channel_report.py` eksik gün-N ölçümlerini iş listesine düşürüyor; takvimi ayrı
tutmaya gerek yok, rapor hatırlatıyor.

---

## Kapanış kontrolü

Bir yayın için hepsi doğruysa iş bitmiştir:

- [ ] `publishing.csv` — URL, tarih, `status=released`, `views_check_date`
- [ ] `releases.csv` — `status=released`, `released_date`
- [ ] `LINKS.md` tazelendi
- [ ] İzleyici sayfası 12. adımdaki dokuz kontrolden geçti
- [ ] En az bir playlist'te
- [ ] Bitiş ekranı kurulu
- [ ] Sabitlenmiş yorum var
- [ ] Duyuru geçildi ya da neden geçilmediği loglandı
- [ ] `channel_log.csv` satırları yazıldı
- [ ] `catalog/build_workbook.py` çalıştırıldı

Eksik varsa yayın "bitti" sayılmaz — `channel_report.py` bunu bir sonraki
oturumda önüne getirir.
