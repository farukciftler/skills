# Analitik — hangi sayı hangi soruyu cevaplar

Bir kanal panosunda otuz sayı var ve otuzu da bir şey söylüyormuş gibi duruyor.
Bu dosya hangisinin gerçekten bir soruya cevap verdiğini ve hangi sırayla
okunacağını tutar.

## 1. Huni — her zaman bu sırayla oku

Yayının önündeki dört kapı. Kırılan **ilk** kapı bulunur, sonrakiler o
düzelmeden yorumlanmaz.

```
gösterim (impressions)   → seni gösteriyor mu?          dağıtım sorunu
   ↓ CTR                 → tıklanıyor mu?               başlık/thumbnail sorunu
   ↓ ortalama süre       → kalıyor mu?                  vaat/içerik uyumu
   ↓ abone + kaydetme    → geri geliyor mu?             kimlik sorunu
```

Sık yapılan hata: görüntüleme düştü diye başlığı değiştirmek. Görüntüleme
huninin çıktısı, girdisi değil. Gösterim durduysa başlık zaten okunmuyor.

## 2. Ne zaman okunur

| Yaş | Ne yapılır |
|---|---|
| 0–48 saat | **Hiçbir karar yok.** YouTube dağıtımı deniyor, görüntüleme oturmamış. |
| gün 2 | İlk sağlık kontrolü: video işlendi mi, chapter'lar göründü mü, thumbnail doğru mu, ses senkron mu. Sayı değil, **bütünlük** kontrolü. |
| **gün 7** | İlk gerçek okuma. `analytics.csv` gün-7 satırı. |
| gün 14 | İkinci okuma; gün-7 ile karşılaştırılabilir ilk nokta. |
| **gün 30** | Karar noktası. `publishing.csv` `views` alanı buradan dolar (`views_check_date`). |
| gün 90 | Uzun format için gerçek eğri. Fonksiyonel müzikte trafiğin çoğu ilk aydan sonra gelir. |

Uzun format (bir saatlik albümler) 30 günde hüküm giymez: uyku/odaklanma
müziği araması yavaş birikir ve arama trafiği aylar içinde büyür. Gün-30
kararı "bu video öldü" değil, "bu başlık talep buluyor mu" sorusudur.

## 3. Gürültü eşikleri — altında yorum yok

| Metrik | Eşik | Altında ne denir |
|---|---|---|
| CTR | **1000 gösterim** | "veri yetersiz" |
| Ortalama görüntülenme süresi | **50 görüntüleme** | "veri yetersiz" |
| Trafik kaynağı dağılımı | **200 görüntüleme** | "erken" |
| Arama sorgusu listesi | **birkaç yüz arama gösterimi** | "erken" |
| Abone dönüşümü | **1000 görüntüleme** | "erken" |

Bu eşikler yeni bir kanalda çoğu videoda karşılanmaz. Doğru cevap **"henüz
ölçülemiyor"**dur; tahmini sayıyla karar üretmek kataloğa yalan yazmaktır.

> **Süre değil, örneklem karar verir.** 2026-08-09 auditinde kanal iki günlüktü
> ama **31.100 gösterim** birikmişti — eşiğin 31 katı. Gösterim, görüntülemeden
> çok daha hızlı birikiyor: YouTube küçük resmi göstermek için beklemiyor,
> tıklanmasını bekliyor. Yani 48 saat kuralı **karar** içindir; gösterim eşiği
> dolduysa CTR o gün de okunur ve `analytics.csv`'ye taban satırı olarak yazılır
> (`period` ve "taban" notuyla). Yazılmayan taban, gün-7'de karşılaştıracak
> hiçbir şey bırakmıyor.

## 4. Uzun formatın kendine ait okuması

Bir saatlik albümde standart yorumlar bozulur:

- **Ortalama izlenme yüzdesi anlamsız.** %4 kötü değil; 61 dakikanın %4'ü 2.5 dakika. Bakılacak sayı **mutlak dakika**.
- **İzlenme süresi (saat) ana metriktir.** Görüntüleme değil. On kişinin 40 dakikası, yüz kişinin 20 saniyesinden değerli — YouTube da öyle sayıyor.
- **Retention eğrisinin ilk 30 saniyesi.** Fonksiyonel müzikte terk hep başta olur; ilk 30 saniyede sert düşüş varsa sorun sesin girişinde ya da vaat uyumsuzluğunda.
- **Tekrar oynatma ve "Sonra izle"** kaydetme sinyali; fonksiyonel müzikte abone dönüşümünden daha erken görünür.

## 5. Trafik kaynakları — bu katalogda ne demek

| Kaynak | Ne söyler | Ne yapılır |
|---|---|---|
| **YouTube araması** | Başlık bir talebe oturmuş | Sorguyu `analytics.csv` `top_query`'ye yaz; sonraki yayında `healing-audio-youtube-seo`'ya besle |
| **Önerilen video** | Algoritma komşu buldu | Hangi videonun yanında çıktığına bak; bitiş ekranı ve playlist onu takip etsin |
| **Göz atma (Browse)** | Ana sayfaya düştü | Genelde thumbnail'ın işi; CTR ile birlikte oku |
| **Kanal sayfaları** | Mevcut dinleyici | Düşükse kanal düzeni ve playlist mimarisi zayıf |
| **Harici** | Dış bağlantı | Nereden geldiğini yaz; bu katalogda beklenmiyor |
| **Bildirimler / Doğrudan** | Sadık kesim | Topluluk gönderisi buradan görünür |

## 6. Karar tablosu

Kırılan halkaya göre müdahale. Her müdahale **tek değişken** — iki şeyi aynı
anda değiştirirsen ölçüm yok olur. Bu, prompt logu kuralının aynısı.

| Görülen | Teşhis | Müdahale |
|---|---|---|
| Gösterim çok düşük (<500 / 7 gün) | Sınıflandırma sorunu: YouTube kimi göstereceğini bilmiyor | Etiket ve açıklamada birincil ifadeyi netleştir; playlist'e ekle; benzer videolarla ilişkilendir. Başlığa **dokunma** |
| Gösterim var, CTR <%2 | Başlık ya da thumbnail tıklatmıyor | Önce thumbnail (110 px testi), sonra başlık. İkisini aynı hafta değiştirme |
| CTR iyi, ilk 30 sn'de sert düşüş | Vaat uyumsuzluğu | Başlıktaki süre/tür/tempo vaadi ile dosyayı karşılaştır; yanlış olan başlıktır, video değil |
| Ortalama süre iyi, gösterim durgun | İçerik tutuyor, dağıtım yok | Aynı şeritte ikinci yayın; seri ve playlist sinyali. Bekle, bozma |
| Arama sorgusu listesi hedeflenenden farklı | Talep başka yerde | Sorguyu yeni yayının birincil ifadesi yap; mevcut başlığı **değiştirme**, o zaten o sorguyu buluyor |
| Abone var ama izlenme kısa | Kanal ilgi çekiyor, bu yayın değil | Kanal düzeyi iş: playlist, kanal fragmanı, topluluk |

**Başlık değişimi bir müdahaledir, bakım değil.** Yapılırsa: eski başlık,
yeni başlık, gerekçe ve değişim tarihi `channel_log.csv`'ye `title_edit`
olarak yazılır — sonraki ölçüm o tarihe göre okunur. Metin
`healing-audio-youtube-seo`'dan gelir ve `metadata_audit.py`'den geçer.

## 7. Şerit deneyi — sonda dalgasının ölçüm kuralı

`docs/roster-experiment.md` on sanatçı, on single ile **tek değişkeni şerit**
tutuyor. Yani:

- Thumbnail'lar aynı kuraldan üretilir (elle yapılan bir thumbnail deneyi bozar).
- Yayınlar aynı gün-N'de karşılaştırılır.
- Karşılaştırılan metrik **CTR ve ortalama süre**, ham görüntüleme değil — görüntüleme yayın sırasına ve güne bağlı.
- Bir yayına müdahale edilirse (başlık/thumbnail), o yayın deneyden **çıkar**; `channel_log.csv` notunda yazar.

Deneyin sonucu okunmadan sonda dalgasının yayın takvimi değiştirilmez.

## 8. Kanal düzeyi okuma

Video okumasından ayrı, ayda bir: `scope=channel` satırı. Bakılacaklar —
toplam izlenme saati, abone net değişimi, en çok izlenen ilk beş video, dönemin
en büyük trafik kaynağı, "Araştırma" sekmesindeki izleyici arama terimleri.

Araştırma sekmesindeki terimler bir sonraki yayının anahtar kelime araştırmasına
girdi olur; `healing-audio-youtube-seo/references/keyword-research.md` bunu
bekliyor. Terim listesini `analytics.csv` `top_query` alanına ve gerekiyorsa
`notes`'a yaz — kanalın kendi verisi, dışarıdan araştırmadan daha değerli.

## 9. Neyi asla yazma

- Gerçek zamanlı karttan okunan sayı (kesin değil, geriye dönük düzeltiliyor).
- Dönemi bilinmeyen sayı.
- Grafikten "yaklaşık" okunan değer — sayı kartlardan ya da dışa aktarımdan gelir.
- Başka bir oturumdan hatırlanan sayı.
