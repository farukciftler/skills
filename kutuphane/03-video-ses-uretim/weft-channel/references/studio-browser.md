# YouTube Studio'yu Chrome eklentisiyle sürmek

Bu dosya mekanik: hangi adres, hangi seçici, hangi tuzak. Karar ve içerik
kuralları diğer referanslarda.

## 0. Oturum açılışı — atlanmaz

1. `tabs_context_mcp` — mevcut sekmeleri gör. Eski oturumdan sekme kimliği **yeniden kullanılmaz**.
2. `tabs_create_mcp` ile yeni sekme, `navigate` ile `https://studio.youtube.com`.
3. **Kanalı doğrula.** Sol üstte `Weft Records` yazmalı. Yazmıyorsa dur ve Faruk'a söyle — hesap değiştirme işi onun.
4. Kanal kimliğini adresten al (`/channel/UC…`) ve `docs/brand/youtube-channel.md` § 5'e yaz. Bir kez alınır, sonra hep oradan okunur.

## 1. Adres haritası

`<UC>` kanal kimliği, `<VID>` 11 karakterlik video kimliği.

| Ekran | Adres |
|---|---|
| Kanal analitiği | `studio.youtube.com/channel/<UC>/analytics/tab-overview/period-default` |
| Kanal analitiği — erişim | `…/analytics/tab-reach_viewers/period-default` |
| Kanal analitiği — kitle | `…/analytics/tab-build_audience/period-default` |
| Video analitiği | `studio.youtube.com/video/<VID>/analytics/tab-overview/period-default` |
| Video düzenleme (başlık, açıklama, tag, thumbnail) | `studio.youtube.com/video/<VID>/edit` |
| Bitiş ekranı | `studio.youtube.com/video/<VID>/editor` (Bitiş ekranı sekmesi) |
| İçerik listesi | `studio.youtube.com/channel/<UC>/videos/upload` |
| Oynatma listeleri | `studio.youtube.com/channel/<UC>/playlists` |
| Yorumlar | `studio.youtube.com/channel/<UC>/comments` |
| Topluluk gönderileri | `studio.youtube.com/channel/<UC>/posts` |
| Kanal özelleştirme (banner, avatar, düzen, temel bilgiler) | `studio.youtube.com/channel/<UC>/editing/images` |

Adres değişmişse Studio yönlendirir; yönlendirmeden sonra **nerede olduğunu
doğrula**, körlemesine tıklama.

Studio tek sayfalık uygulama: `navigate` sonrası içerik gecikmeli geliyor.
Bir eylemden önce beklenen metnin sayfada olduğunu `find` ya da
`get_page_text` ile gör.

## 2. Sayı okumak

**Sıra: `get_page_text` → gerekiyorsa `find` → doğrulama için ekran görüntüsü.**
Ekran görüntüsüyle sayı okumak hem yavaş hem yanlış okumaya açık.

İki yol var, ikisi de meşru:

**(a) Tek video, birkaç sayı.** Video analitiği → Genel Bakış kartından
görüntüleme, izlenme süresi, abone; Erişim sekmesinden gösterim ve CTR. Sayıları
`yt_import.py add` ile yaz.

**(b) Çok video ya da dönem karşılaştırması.** Analitik → sağ üst **Gelişmiş
mod** → dönemi seç → **Dışa aktar → Virgülle ayrılmış değerler (.csv)**.
İndirilen `.zip` `~/Downloads`'a düşer; `yt_import.py import --export` onu okur.
Elle sayı kopyalamaktan hem hızlı hem hatasız.

> Gelişmiş modda dönem seçici sayfanın sağ üstünde ve seçilen dönem dışa
> aktarıma **aynen** girer. `--period` bayrağını ekranda seçtiğinle aynı yaz;
> uyuşmazsa tablo yalan söyler.

Dışa aktarım birden çok CSV içerir (`Table data.csv`, `Totals.csv`,
`Chart data.csv`). Script sayaç sütunu bulduğu **ilk** tabloyu kullanır ve
hangisini kullandığını basar.

## 3. Metin yazmak — React kontrollü alanlar

Studio'nun başlık ve açıklama alanları `contenteditable` div, textarea değil.
`value` atamak işlemez. Çalışan yol (`CLAUDE.md` § 5'te yükleme için de aynısı):

```js
el.focus();
const r = document.createRange(); r.selectNodeContents(el);
const s = getSelection(); s.removeAllRanges(); s.addRange(r);
document.execCommand('delete');
document.execCommand('insertText', false, metin);
```

Gerçek `<input>`/`<textarea>` alanlarında (etiketler, playlist adı) native
setter gerekir:

```js
const set = (el, v) => {
  const d = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value');
  d.set.call(el, v);
  el.dispatchEvent(new Event('input',  {bubbles: true}));
  el.dispatchEvent(new Event('change', {bubbles: true}));
};
```

Düğmeler `.click()` ile tetiklenir; React sentetik olayı `isTrusted`'a bakmaz.

## 4. Ateşle-ve-unutma — doğrula

Suno'da öğrenilen kural burada da geçerli: **tıklama sessizce kaydolmayabilir.**
Düğme `disabled` değildir, hata çıkmaz, ama hiçbir şey olmaz.

Her yazma işleminden sonra doğrulama şu şekilde:

| İşlem | Doğrulama |
|---|---|
| Başlık/açıklama düzenleme | `Kaydet`e bas → durum göstergesi `Kaydedildi` olsun → sayfayı yenile, metni tekrar oku |
| Etiket ekleme | Virgülden sonra çip oluştuğunu gör; çip yoksa metin etiket olmamıştır |
| Playlist'e ekleme | Video düzenleme ekranını yenile, playlist alanında adı gör |
| Topluluk gönderisi | Gönderiden sonra `/posts` listesinde ilk sırada olduğunu gör, URL'ini al |
| Thumbnail değişimi | Yenile, küçük resmin yeni dosya olduğunu gözle doğrula |

Doğrulamadan `channel_log.csv`'ye satır yazılmaz. Log, yapıldığını sandığın
değil, **gördüğün** işi tutar.

## 5. Tuzaklar

| Tuzak | Çözüm |
|---|---|
| **Modal diyalog oturumu kilitler.** Silme onayı, "Çıkmak istediğinize emin misiniz" gibi bir kutu açılırsa eklenti komut alamaz. | Silme ve iptal düğmelerine yaklaşma. Zaten geri alınamayan iş Faruk'un onayına bağlı — orada zaten duruyorsun. |
| **Uzun JS çağrıları ~45 sn'de kesiliyor.** | İşi küçük partilere böl. Zaman aşımı aldığında **kod çoğu zaman çalışmıştır** — panik yapıp tekrarlama, önce sayfada doğrula. Tekrarlanan gönderi silinmesi gereken bir iş demektir. |
| **Kaydetmeden gezinme.** Studio bazı ekranlarda otomatik kaydeder, bazılarında `Kaydet` ister. | Düğme varsa bas ve `Kaydedildi`yi gör. Görmeden sekmeyi terk etme. |
| **Etiketler "Daha fazla göster"in altında.** | Video düzenleme ekranında önce genişlet, sonra ara. |
| **Analitik verisi ~48 saat gecikebilir.** Gerçek zamanlı kart ayrı bir ölçüm ve kesin değil. | Gerçek zamanlı sayıyı `analytics.csv`'ye **yazma**. Yazılan sayı ana rapordan gelir. |
| **Yeni yüklenen video işlenirken analitik boş görünür.** | Video işlemesi bitmeden ölçüm yok; yükleme günü yapılacak iş ölçüm değil, kapanış (`post-upload-runbook.md`). |
| **Yorum listesi varsayılan olarak filtreli.** | "Yanıtlanmadı" filtresi açıkken toplam yorum sayısı yanlış okunur; filtreyi kontrol et. |

## 6. Ne zaman tarayıcıya hiç girme

- Sadece "durum ne" soruluyorsa: `channel_report.py` yeter, kanalı açma.
- Ölçüm günü gelmemişse: rapor zaten söylüyor, boş ölçüm gürültü üretir.
- Yayın 48 saatten genç ve soru performansla ilgiliyse: tarayıcıyı açmak yerine
  neden erken olduğunu söyle ve gün-7 tarihini ver.
