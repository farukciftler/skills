---
name: deck-studio
description: "Sunum tasarım stüdyosu — bir marka kimliği veya seçilmiş bir sanat yönetimi (art direction) üzerine kurulu, özel tipografili, kendi ürettiği illüstrasyon ve ürün mockup'larını içeren, jenerik AI şablonundan uzak .pptx desteleri üretir; mevcut desteleri de yeniden tasarlar ve denetler. Kullanıcı 'sunum hazırla', 'deck', 'pitch deck', 'yatırımcı sunumu', 'slayt', 'pptx', 'sunumu güzelleştir', 'şu desteyi yeniden tasarla', 'mockup ekle', 'illüstrasyon üret', 'marka kimliğine göre sunum', 'make me a deck', 'design these slides', 'redesign this presentation' dediğinde kullan. Bir teklif, rapor, strateji, lansman veya yatırımcı görüşmesi için slayt gerektiği anlaşıldığında — 'tasarım' kelimesi hiç geçmese bile — devreye gir. Sunuma girecek cihaz mockup'ı, arayüz ekranı, vektör illüstrasyon veya özel font gerektiğinde tek başına da kullan. Şablon doldurmaz; her deste için tek bir sanat yönetimi kararı verir, kilitler, her slaytta uygular."
---

# Deck Studio

Bir sunum tasarım stüdyosunun sanat yönetmeni gibi çalış. Müşteri daha önce şablon
kokan işleri geri çevirmiş; bu deste için özel bir görüş satın alıyor.

Bu skill üç şeyi bir arada yapar ve ayrı ayrı yapıldığında hiçbiri işe yaramaz:
**bir argüman**, **kilitlenmiş bir sanat yönetimi**, ve **o yönetime göre üretilmiş
gerçek görseller**. Sıra bu; atlanan adım jenerik çıktı üretir.

Bu skill `.pptx` üretimini `/mnt/skills/public/pptx` üzerine kurar — pptxgenjs
tuzakları, `validate.py` ve görsel QA komutları oradadır, **onu da oku**. Buradaki
katman: sanat yönetimi, özel tipografi, kendi ürettiğimiz görseller ve eleştiri
döngüsü. Genel görsel tasarım felsefesi için `/mnt/skills/public/frontend-design`
tamamlayıcıdır.

## Neden çıktılar jenerik oluyor

Sektör araştırmasının uzlaştığı tek teşhis şu: *slop'un sebebi kötü zevk değil,
karar verilmemiş olması.* Yön verilmediğinde model istatistiksel ortalamaya
düşer — mor-mavi degrade, üç yuvarlak kart, Inter başlık, her slaytta aynı
düzen. "Temiz ve modern" bir yön değildir; slop'un ta kendisidir.

Bu yüzden bu skill'in merkezinde tek bir kural var: **inşaata başlamadan önce
tek bir yöne bağlan, token'larını yaz, ve her slaytta ona sadık kal.** Neyi
yapmayacağını da yaz — negatif kısıtlar, pozitif olanlar kadar iş görür.

## Akış

Kullanıcı hazır içerik verdiyse 1'i kısa tut; sıfırdan başlıyorsa 1 en önemli adım.

### 1. Brief ve argüman

Şunlar netleşmeden tasarıma geçme. Eksikse sor — hepsini birden değil, en kritik
2-3 tanesini:

- **Tek cümlelik tez.** Bu deste izleyiciye ne yaptırmaya çalışıyor?
- **İzleyici ve ortam.** Yatırımcı mı, müşteri mi, iç ekip mi? Sunulacak mı,
  linkle mi gönderilecek? Link ile gidiyorsa slayt sunucusuz ayakta durmalı.
- **Marka var mı?** Varsa renk/font/logo'yu al ve sanat yönetimini ona göre kur;
  yoksa aşağıdaki katalogdan seç. Kullanıcının kendi marka sistemi
  `brand-identity` skill'inden geliyorsa onu kaynak al.
- **Dil.** Türkçe, İngilizce veya ikisi. İki dilliyse iki ayrı dosya üret —
  aynı slayta iki dil sıkıştırma, tipografi çöker.
- **Uzunluk ve teslim formatı.** `.pptx` mi, PDF mi, ikisi mi?

Sonra **storyline'ı slayt slayt yaz ve onaylat.** Her slaytın başlığı bir
*eylem başlığı* olmalı: "Q3 geliri" değil, "Q3 geliri %12 büyüdü, kurumsal
taraf taşıdı." Betimleyici başlıklar bir destenin AI yapımı olduğunu ele veren
en büyük içerik sinyalidir. Storyline onaylanmadan tek piksel üretme.

### 2. Sanat yönetimini kilitle

`references/art-direction.md` dosyasını oku. Orada 10 adlandırılmış yön, tam
token setleri, font eşleşmeleri ve her yönün ne zaman doğru olduğu var.

Bir yön seç ve çalışma klasörüne `DECK.md` yaz — bu dosya destenin anayasasıdır:

```markdown
# Yön: <ad>            (neden bu deste için doğru: tek cümle)
Renkler   ink #0E1512 · paper #F4F1EC · accent #C4552F · muted #7A857F
          hâkim renk: paper (%65 görsel ağırlık), accent yalnız vurguda
Tipografi display Fraunces 700 · body Inter 400/600 · sayı Inter 600
Izgara    13.33x7.5in · kenar boşluğu 0.9in · 12 kolon · dikey ritim 0.25in
Motif     <tek bir tekrar eden öge>
Yapmayacaklarım
  - başlık altı vurgu çizgisi, kenar şeridi, dekoratif renk bandı
  - her slaytta aynı düzen
  - stok fotoğraf klişeleri, mor-mavi degrade, üç eşit kart
```

Yazdıktan sonra dur ve tek soruyu sor: **bu token setini tamamen farklı bir
konudaki desteye taşısam yine "çalışır" mıydı?** Cevap evetse yeterince özel
değil; konuya bağla ve yeniden yaz. Ne değiştirdiğini kullanıcıya bir cümleyle
söyle.

Ardından tipografiyi kur:

```bash
python scripts/setup_fonts.py --list          # katalog
python scripts/setup_fonts.py fraunces inter  # kur + Türkçe glif doğrula
```

Türkçe deste yapıyorsan script'in `ı İ ğ Ğ ş Ş` uyarısını görmezden gelme —
glifi olmayan bir font başlığın ortasında sessizce başka bir yüze düşer.

### 3. Görselleri üret

**Her slaytın bir görsel ögesi olmalı.** Ama görsel "stok fotoğraf" demek
değil; bu skill'in ayırt edici tarafı görselleri *kendisinin* üretmesi.

Üç üretim hattı var, üçü de `references/` altında ayrıntılı:

| İhtiyaç | Nasıl | Referans |
|---|---|---|
| Ürün ekranı, cihaz/tarayıcı mockup'ı | HTML/CSS → Chromium → PNG → cihaz çerçevesi | `references/mockups.md` |
| Diyagram, illüstrasyon, izometrik, doku, kapak tipografisi | SVG veya HTML → PNG | `references/illustration.md` |
| Veri | pptxgenjs'in **native** grafiği (görsel değil) | `references/layouts.md` |

Ortak motor — istisnasız her özel görsel bundan geçer:

```bash
python scripts/render_html.py kart.html cikti.png --width 1200 --height 800 --scale 2
python scripts/device_frame.py ekran.png telefon.png --device phone --bg "#0E1512" --tilt -6
```

Chromium gerçek CSS verir: katmanlı gölge, `backdrop-filter`, `clip-path`,
mesh degrade, grain overlay, kurduğun her yazı tipi. pptxgenjs'in çizemediği
her şey burada üretilir ve slayta görsel olarak girer. Slayta giren her görsel
`--scale 2` ile üretilir; deste projeksiyona vurulur veya yakınlaştırılır.

### 4. Desteyi kur

`/mnt/skills/public/pptx/SKILL.md`'yi oku ve pptxgenjs ile üret. Bu skill'e
özel eklemeler:

- `pres.layout = 'LAYOUT_WIDE'` (13.33x7.5in). Slayt eklemeden **önce** ayarla.
- Düzen arşivi ve koordinat reçeteleri: `references/layouts.md`. Ardışık iki
  slaytta aynı arketipi kullanma.
- Metni **metin olarak** yaz, resim olarak değil — müşteri düzeltecek. Tek
  istisna: kapak/bölüm ayracındaki dev tipografik kompozisyon, `clip-path` veya
  karışım modu gerektiriyorsa görsel olabilir.
- Renkleri `DECK.md`'deki hex'lerden al; `#` yok, 8 haneli yok.
- Konuşmacı notlarını `slide.addNotes()` ile yaz — sunucusuz okunacak destede
  bu, slayta metin doldurmanın alternatifidir.

### 5. Fontları göm

Özel tipografi kullandıysan bu adım opsiyonel değil; atlarsan müşterinin
laptopunda deste Calibri'ye düşer ve QA ettiğin bütün satır uzunlukları yanlış
olur.

```bash
python scripts/embed_fonts.py deste.pptx --font "Fraunces" --font "Inter" --out deste-final.pptx
```

Script değişken (variable) fontları PowerPoint'in okuyabildiği statik 400/700
kesitlerine çevirip gömer. Teslimde iki şeyi söyle: **macOS PowerPoint gömülü
fontları yok sayar** (Mac'teki gözden geçiren için PDF gönder) ve gömme yalnız
lisansı izin veren yüzler için yapılır (katalogdaki hepsi OFL/Apache).

### 6. Eleştiri döngüsü — atlanmaz

Tek atışlık üretim slop'un ikinci sebebidir. Döngüyü kapat:

```bash
python /mnt/skills/public/pptx/scripts/office/validate.py deste-final.pptx
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf deste-final.pptx
rm -f slide-*.jpg && pdftoppm -jpeg -r 150 deste-final.pdf slide
```

Sonra **her slaytın görüntüsüne tek tek bak** ve `references/qa.md`'deki
kontrol listesini uygula. Üretim kodunu yazdıktan sonra beklediğini görürsün,
olanı değil — bu yüzden görsellere taze gözle bakmak şart. Bulduğun kusurları
üreteç kodunda düzelt, elle paketlenmiş XML'de değil; sonra sadece
değiştirdiğin slaytları yeniden render et ve dur.

Türkçe destede ek kontrol: LibreOffice önizlemesinde `ı`/`ğ`/`ş` yerine kutu
veya farklı bir yüz görünüyorsa font kapsamı eksiktir, düzen sorunu değil.

### 7. Teslim

`/mnt/user-data/outputs/` altına koy ve `present_files` ile sun: `.pptx`,
PDF, ve iki dilliyse her dil için ayrı dosya. Yanına üç cümle: seçilen yönün
adı ve gerekçesi, gömülü fontlar, ve müşterinin kendisinin değiştirmesi
gereken yerler (gerçek rakam, logo, isim).

## Mevcut bir desteyi yeniden tasarlarken

Kullanıcı `.pptx` verdiyse sırayı değiştir:

1. `markitdown deste.pptx` ile içeriği çıkar, `scripts/thumbnail.py` ile
   görsel ızgarayı al.
2. **Önce içeriği eleştir:** hangi slaytın argümanı yok, hangi başlık
   betimleyici, hangi grafik veri çöplüğü. Bunu kullanıcıya söyle.
3. Sonra 2. adımdan devam et — yeni sanat yönetimi, yeni deste. Eski dosyanın
   XML'ini kurtarmaya çalışmak yerine içeriği taşıyıp yeniden inşa etmek
   neredeyse her zaman daha hızlı ve daha temiz.

İstisna: kullanıcının korunması gereken kurumsal şablonu varsa (`.potx`),
onu bozma — pptx skill'inin şablon doldurma yolunu izle, sanat yönetimi
kararlarını şablonun izin verdiği eksenlerde ver.

## Kapsam dışı

- **Marka kimliğinin kendisini kurmak** (logo, palet sistemi, marka defteri)
  `brand-identity` skill'inin işidir. Marka yoksa oraya yönlendir veya oradan
  gelen çıktıyı bu skill'e girdi olarak al.
- **İnteraktif web sunumu / canvas tasarımı** — oturumda bir Design artifact
  tipi varsa ve kullanıcı dosya istemiyorsa o daha doğru araçtır.
- **Gerçek fotoğraf üretimi** — bu skill vektör, arayüz ve tipografi üretir;
  fotoğraf gerekiyorsa kullanıcıdan iste veya fotoğrafsız bir yön seç.

## Referans dosyaları

| Dosya | Ne zaman oku |
|---|---|
| `references/art-direction.md` | Her zaman, 2. adımda — yön katalogu, token setleri, font eşleşmeleri |
| `references/layouts.md` | Deste kurarken — slayt arketipleri, koordinatlar, grafik reçeteleri |
| `references/mockups.md` | Ürün ekranı/cihaz görseli gerektiğinde |
| `references/illustration.md` | Diyagram, illüstrasyon, doku, kapak tipografisi gerektiğinde |
| `references/qa.md` | 6. adımda, her seferinde |
