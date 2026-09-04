# QA ve eleştiri döngüsü

İlk render'ın birkaç gerçek kusuru vardır — bu normaldir, bulup düzeltmek
işin parçasıdır. Atlanması gereken şey döngü değil, üçüncü tur mükemmeliyetçilik.

Sıra: **dosya sağlığı → içerik → görsel → yön sadakati.** İlk üçü mekanik,
dördüncüsü asıl iş.

## 1. Dosya sağlığı

```bash
python /mnt/skills/public/pptx/scripts/office/validate.py deste.pptx
```

Şablondan türetildiyse `--original sablon.pptx` ekle. Her hata düzeltmesini
söyler; düzeltmeyi **üreteç kodunda** yap, paketlenmiş XML'i elle kurcalama.

Font gömdüysen gömmeden **sonra** doğrula; `embed_fonts.py` paketi yeniden
zip'ler.

## 2. İçerik

```bash
markitdown deste.pptx
markitdown deste.pptx | grep -iE "lorem|ipsum|\bTODO|\[insert|xxx"
```

- Eksik içerik, yazım hatası, yanlış sıra var mı?
- Her slaytın başlığı bir **eylem başlığı** mı, yoksa etiket mi? "Pazar
  analizi" bir etikettir; "Pazar üç oyuncuya sıkıştı, dördüncüye yer var" bir
  başlıktır. Bu tek düzeltme bir desteyi en çok insan yapımı gösteren şeydir.
- Türkçe destede: apostroflar doğru mu (`'` değil `’`), sayı biçimi TR mi
  (1.250,50), tarih biçimi tutarlı mı?
- İki dilli teslimde her iki dosyada aynı sayıda slayt ve aynı sıra var mı?

## 3. Görsel

```bash
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf deste.pptx
rm -f slide-*.jpg && pdftoppm -jpeg -r 150 deste.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Mutlak yolları `view` aracına ver ve **her slayta tek tek bak**. Üretim kodunu
yazdıktan sonra beklediğini görürsün, olanı değil.

Aranacak kusurlar, en sık olandan başlayarak:

- [ ] **Metin taşması / kesilmesi** — kutu veya slayt sınırında. En yaygın ve
      her zaman görünür kusur.
- [ ] Çakışan ögeler; şeklin üstünden geçen metin; görselin altında kalan başlık
- [ ] Kenar boşluğu ihlali (< 0.5in) veya bloklar arası < 0.3in aralık
- [ ] Düzensiz boşluk: bir yerde geniş boşluk, başka yerde sıkışıklık
- [ ] Kolonların/kartların hizasızlığı
- [ ] Düşük kontrast: açık zeminde açık gri metin, koyu zeminde koyu ikon
- [ ] Şeffaf PNG'lerin kenarındaki gri halka
- [ ] Grafikte üst üste binen veri etiketleri
- [ ] Türkçe gliflerin yerine kutu veya farklı yüz (= font kapsamı eksik)

Fontlar için özel not: güvenli listede olmayan bir yüz kullandıysan LibreOffice
onu doğru render eder **çünkü sisteme kurduk** — ama alıcının makinesinde
gömülü fontlar devreye girer. Bu yüzden gömmeden sonra bir kez daha PDF al ve
bak.

## 4. Yön sadakati — asıl denetim

Slayt görüntülerini yan yana koy ve `DECK.md`'yi aç. Bunlar mekanik değil,
karar denetimidir:

- [ ] **Her slayt aynı desteden mi görünüyor?** Renk, tipografi, boşluk ve
      motif deste boyunca aynı mı?
- [ ] **Hâkim renk gerçekten hâkim mi?** Palet eşit ağırlıklı dağılmışsa yön
      çözülmüş demektir.
- [ ] **Vurgu rengi seyrek mi?** Slayt başına en fazla iki yer.
- [ ] **Düzen çeşitliliği var mı?** Ardışık iki slaytta aynı arketip yok, her
      arketip 12-16 slaytta en fazla iki kez.
- [ ] **Motif her slaytta mı, hiç mi yok mu?** Yarı yolda bırakılmış motif en
      kötüsü.
- [ ] **Yasak listeden bir şey sızmış mı?** Başlık altı vurgu çizgisi, kenar
      şeridi, üç eşit yuvarlak kart, ALL-CAPS etiket, `A · B · C` meta dizesi,
      buton sonunda `→`, mor-mavi degrade, ortalanmış gövde metni.
- [ ] **Bu desteyi tamamen başka bir konuya taşısam yine "çalışır" mıydı?**
      Evetse yön yeterince konuya bağlanmamış.

Son olarak Chanel testi: desteyi kapatmadan önce **bir aksesuarı çıkar.**
Slayttaki en zayıf görsel ögeyi sil ve slayta tekrar bak — çoğu zaman daha iyi
olur.

## Düzeltme turu

Bulduklarını üreteç kodunda düzelt, PDF'i **yeniden üret** (düzenlenmiş
`.pptx`'ten yeniden dönüştürmeden `pdftoppm` eski görüntüyü verir), ve yalnız
değiştirdiğin slaytlara bak. İki turdan sonra kalan şey genelde tercih
meselesidir — kullanıcıya sor, kendi kendine üçüncü tur atma.
