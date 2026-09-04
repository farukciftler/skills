---
name: pexels-gorsel-bulucu
description: >
  Moonstone Residence için telifsiz Pexels fotoğrafı ve videosu bulur, puanlar,
  hak/izin riskini denetler ve künyesiyle birlikte indirir. Blog kapağı, site
  bölüm arka planı, OG görseli, sosyal medya zemini, doku/malzeme plakası,
  Reels ara kesiti ve Tuzla/İstanbul çevre içeriği için kullanılır. Türkçe ya
  da muğlak bir brief'i gerçekten sonuç veren İngilizce sorgulara çevirir;
  adayları teslim edilecek ölçüye göre (çözünürlük payı, kırpma dayanıklılığı,
  marka rengi, metin için sessiz alan, klip süresi) sıralar. Şu ifadeler
  geçtiğinde kullan: "telifsiz görsel", "stok fotoğraf", "arka plan görseli",
  "blog kapağı", "doku bul", "Pexels", "ücretsiz görsel", "b-roll", "video
  arka plan", "banner görseli". Pexels adı hiç geçmese bile, bir teslimat için
  hazır görsel seçilecekse devreye gir. **Proje render'ının yerine geçecek
  görsel aramak için KULLANILMAZ** — o sınır aşağıda.
---

# Pexels Görsel Bulucu — Moonstone

Stok arama iki yerde tutarlı biçimde başarısız oluyor: sorgu bir nesne yerine bir
duygu tarif ediyor, ve seçilen kare küçük ızgarada güzel göründüğü için
seçiliyor — asıl teslimatta ayakta kalıp kalmadığına bakılmadan. Bu skill ikisini
de düzeltir, sonra yayına çıktıktan sonra ortaya çıkan hak sorunlarını önden yakalar.

İş bölümü: **sen** yaratıcı çeviriyi yaparsın (brief → sorgu varyantları, son
görsel karar), **betik** mekaniği yapar (sayfalı arama, puanlama, tekrar
ayıklama, doğru dosya varyantı, künye).

## Kırmızı çizgi — bunu önce oku

Moonstone bir inşaat projesidir. Stok görsel burada **atmosfer ve bağlam**
içindir, **ürün** için değil.

**Asla yapılmaz:**
- Başka bir binanın fotoğrafını Moonstone'un cephesi, dairesi, havuzu ya da
  sosyal alanı yerine kullanmak. Bu yalnızca yanlış değil, Ticari Reklam ve
  Haksız Ticari Uygulamalar Yönetmeliği kapsamında yanıltıcı reklamdır.
- Bir stok iç mekân fotoğrafını "Tip 5 salonu" gibi sunmak.
- Tuzla'ya ait olmayan bir manzarayı proje çevresi gibi göstermek.
- Stok görselin üstüne proje adı koyup ürün iletişimi yapmak.

**Serbest ve doğru kullanım:**
- Blog yazısı kapakları (kredi süreci, net/brüt farkı, yatırım rehberi).
- Site bölüm arka planları — üzerine koyu katman gelen, soyut ya da dokusal.
- Doku ve malzeme plakaları: beton, mermer, ahşap, cam, kâğıt.
- Sosyal medyada bilgi/rehber içeriğinin zemini.
- Soyut mimari detay — **tanınabilir bir bina olmamak şartıyla**.
- Sunum ve teklif belgelerinde nötr bölüm ayraçları.

Şüphedeysen sor: *"Bu görseli gören biri, Moonstone'u gördüğünü sanabilir mi?"*
Cevap evet ya da belki ise kullanma.

Proje görseli gerektiğinde kaynak **`Moonstone-katalog-baskı-revize3.pdf`** ve
kurumsal kimlik klasörüdür — orada gerçek render'lar var. Bkz. `marka-kimligi.md`.

## Kurulum

API anahtarı `~/.config/pexels/key` dosyasında (600 izinli) ya da
`PEXELS_API_KEY` ortam değişkeninde tutulur. **Depoya yazılmaz, sohbete
yapıştırılmaz.**

```bash
mkdir -p ~/.config/pexels
printf '%s' 'ANAHTAR' > ~/.config/pexels/key && chmod 600 ~/.config/pexels/key
```

Bir anahtar herhangi bir yerde düz metin olarak paylaşıldıysa (sohbet, ticket,
commit) bunu açıkça söyle ve kullanmadan önce pexels.com/api adresinden
yenilenmesini iste. Sessizce devam etme.

Kota: `python3 scripts/pexels_scout.py quota`. Betik yanıtları 24 saat
önbelleğe alır — aynı sorguyu tekrar çalıştırmak kota harcamaz.

## Akış

### 1. Teslimatı sabitle

Teslimat yönü, çözünürlük tabanını ve insan olup olamayacağını belirler.
`python3 scripts/pexels_scout.py presets` listeler.

Moonstone için sık kullanılanlar: `blog-kapak`, `web-bolum`, `og-image`,
`ig-feed-45`, `ig-story`, `doku`, `reels-bstok`, `web-hero`.

Marka rengi puanlamayı besler: koyu içerikte `#040C1D`, sıcak içerikte
`#9C8A5D`, altın vurgu için `#B8992F`.

### 2. Brief'i 3–5 sorgu varyantına çevir

Sorgu yazmadan önce **`references/emlak-sorgu-sozlugu.md`** oku. Kısa hâli:
brief'i `[somut nesne] + [malzeme/doku] + [ışık koşulu]` olarak yeniden yaz,
sonra sorgu başına tek eksende değiştir — birebir konu, makro detay, konusuz
ortam, soyut doku, komşu nesne.

Brief'in dili ne olursa olsun **İngilizce ara**. Türkiye'ye özgü şeylerin
karşılığı zayıftır; gerektiğinde çevresini ara ve bunu söyle — genel bir
fotoğrafı yerine koyma.

### 3. Ara ve puanla

```bash
python3 scripts/pexels_scout.py search \
  --preset blog-kapak \
  -q "modern concrete facade abstract detail" \
  -q "architectural blueprint drafting desk" \
  -q "keys on wooden table close up" \
  -q "warm minimal interior morning light" \
  --color "#040C1D" --exclude-people \
  --limit 12 --out shortlist.json
```

Bayraklar: `--exclude-people` (tanınabilir insan içerenleri eler — ticari
kullanımda varsayılan tercih), `--color` (marka hex'i, filtre değil puan),
`--color-filter` (sert Pexels renk filtresi, sadece fotoğraf, sonuç kümesini
çok daraltır), `--page 2` (belirli bir sorgunun derin sayfası, genel bir
sorgunun 1. sayfasından iyidir), `--max-per-author` (varsayılan 2).

Puanlama gerekçesiyle birlikte gelir: sıra, hedefe göre çözünürlük katı,
kırpma sonrası kalan alan, renk mesafesi, üzerine metin gelecekse ton
uygunluğu, klip süresi. Negatif puan o karenin teslimatı taşıyamayacağı
anlamına gelir — genelde çözünürlük yetersizdir.

### 4. Karelere bak

Puan alanı daraltır, seçmez. Kontakt sayfası kur ve gerçekten bak:

```bash
python3 scripts/pexels_scout.py sheet --shortlist shortlist.json --out sheet.html
```

Önizlemeler dış bağlantıdır, kota harcamaz. Adayları gerekçeleri ve
bayraklarıyla kullanıcıya sun, hangisini neden seçeceğini söyle. Bütün adaylar
zayıfsa kötü bir kümenin en iyisini önerme — bunu söyle ve farklı varyantlarla
2. adıma dön. Yanlış ama kendinden emin bir seçim, bir arama daha yapmaktan
pahalıdır.

### 5. İndirmeden önce hak denetimi

Aday bayrak taşıyorsa ya da görsel ticari bir yayına gidiyorsa
**`references/licensing-and-risk.md`** oku. Lisansın kapsamadıkları:
tanınabilir yüzler (model izni yok), görünür logo ve markalı ürün (marka izni
yok), değiştirilmemiş kopyaların üründe satılması, video kliplerdeki ses.

Puanlayıcının bayrakları alternatif metin üzerinde çalışan sezgisel
kurallardır — bariz durumları yakalar, gerisini kaçırır. Kareye bak.

### 6. Künyesiyle indir

```bash
python3 scripts/pexels_scout.py download \
  --shortlist shortlist.json --pick 1,4 \
  --out ./assets --project "MOONSTONE-WEB"
```

Doğru varyantı kendi seçer. `CREDITS.md`, `credits.json` ve dosya başına
`.credit.txt` yazar.

Pexels API Kuralları, bu varlıkların göründüğü yerde belirgin bir Pexels
bağlantısı ister — site altbilgisi, blog yazısı sonu, YouTube açıklaması.
Künyenin nereye düşeceğini kullanıcıya hatırlat; yasal olarak zorunlu
olmaması onu isteğe bağlı yapmıyor.

Videoda sesi at: `ffmpeg -i in.mp4 -an -c:v copy out.mp4`

## Devir teslim

- **gorsel-uretim** — indirilen orijinali ona ver; markalı çerçeveye,
  degrade katmana, tipografiye ve doğru ölçüye o dönüştürür. `avg_color`
  değerini de ver, tasarım tonu tahmin etmesin.
- **post-uretimi.md / story-uretimi.md** — hangi ölçü ve güvenli alanın
  gerektiğini oradan al, `--preset` seçimini ona göre yap.
- **seo.md** — blog kapağı indirildiyse dosya adı ve `alt` metni oradaki
  görsel SEO kuralına uysun.

## Referans dosyaları

- `references/emlak-sorgu-sozlugu.md` — brief → sorgu çevirisi, emlak ve
  inşaat için sorgu bankaları, Türkçe içeriğin ele alınışı, sessiz alan
  vekilleri, video döngü uygunluğu. 2. adımdan önce oku.
- `references/licensing-and-risk.md` — Pexels Lisansı'nın kapsadığı ve
  kapsamadığı, API yükümlülükleri, yayın öncesi denetim listesi. 5. adımdan
  önce ve her ticari yayından önce oku.
