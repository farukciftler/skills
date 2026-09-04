# Mockup üretimi

Bir ürün destesinde en çok işi yapan görsel, ürünün kendisidir. İki adım var ve
karıştırılmaları en sık yapılan hata: **önce inandırıcı bir arayüz ekranı
tasarla, sonra onu bir cihaza yerleştir.** Boş bir telefon çerçevesi içinde
jenerik bir dashboard, çerçevesiz iyi bir ekrandan daha kötüdür.

## 1. Arayüz ekranını tasarla

Ekranı HTML/CSS ile kur ve Chromium'la render et. Bu, tasarımın *tasarım* olduğu
yer — `/mnt/skills/public/frontend-design/SKILL.md` burada geçerlidir.

Hedef boyutlar (`device_frame.py`'nin çerçeve kutularıyla eşleşir):

| Cihaz | Render boyutu | Not |
|---|---|---|
| `phone` | 390 x 844, `--scale 3` | Dynamic Island üstteki ~54px'i kapatır, oraya içerik koyma |
| `tablet` | 744 x 1050, `--scale 2` | |
| `browser` / `laptop` | 1100 x 690, `--scale 2` | üstte 44px'lik adres çubuğu çerçeveden gelir |

```bash
python scripts/render_html.py ekran.html ekran.png --width 390 --height 844 --scale 3
```

### Ekranı inandırıcı yapan şeyler

- **Gerçek içerik.** "Lorem ipsum", "Kullanıcı Adı", "$1,234" değil; destenin
  konusundan gelen gerçek isimler, gerçek rakamlar, gerçek Türkçe cümleler.
  Ekranın anlattığı şey slaytın argümanını desteklemeli.
- **Ürünün paletini kullan, destenin paletini değil.** Ürün gerçekten var ise
  onun renkleriyle; yoksa destenin paletiyle ama daha nötr bir kesitiyle.
  Ekranın slaytla birebir aynı renkte olması sahte görünür.
- **Kusurlu doluluk.** Gerçek arayüzlerde bir liste yarım kalır, bir sayı uzun,
  bir etiket iki satıra düşer. Her kartın aynı boyda olduğu ekran maket kokar.
- **Durum işaretleri.** Bir yerde seçili sekme, bir yerde bildirim rozeti,
  bir yerde devam eden işlem. Statik mükemmellik ölü görünür.
- **Sistem çubuğu koyma.** Saat/pil/sinyal çizmeye çalışma; çerçeve zaten
  cihazı ima ediyor, kötü çizilmiş bir status bar tek başına maketi ele verir.

Referans arıyorsan ve oturumda Mobbin bağlıysa (`search_screens`,
`search_flows`) gerçek ürünlerin ekran akışlarını oradan çek ve *yapıyı* örnek
al — piksel kopyalama, bir ürünün ekranını başka bir markanın destesine koyma.

## 2. Cihaza yerleştir

```bash
# koyu zeminli slayt için, hafif açılı, arkasında marka renginde hale
python scripts/device_frame.py ekran.png telefon.png \
  --device phone --bg "#0E1512" --glow "rgba(31,111,92,.5)" --tilt -6

# slayt zeminini alsın diye şeffaf
python scripts/device_frame.py ekran.png telefon.png --device phone --bg none

# tarayıcı penceresi, gerçekçi adres çubuğuyla
python scripts/device_frame.py dash.png tarayici.png \
  --device browser --url "app.cloud4next.com" --bg "#F4F1EC"

# laptop kapağı + gövdesi
python scripts/device_frame.py dash.png laptop.png --device laptop --url "cloud4next.com"
```

Seçenekler: `--tilt` (derece), `--pad` (çerçeve çevresi boşluk), `--glow`
(cihazın arkasında radyal hale), `--scale` (varsayılan 2).

### Kompozisyon kuralları

- **Şeffaf PNG varsayılan olsun.** `--bg none` ile üret, slayt zemini görünsün.
  Çerçeveye ayrı bir arka plan basmak slaytta ikinci bir dikdörtgen yaratır ve
  kompozisyonu böler.
- **Taşır.** Cihazı slaytın içine hapsetme; alt kenardan veya sağ kenardan
  kırparak taşır (D arketipi). Tam görünen, ortalanmış, gölgeli tek cihaz en
  jenerik yerleşimdir.
- **Eğim ya vardır ya yoktur.** `--tilt 0` (katı, İsviçre/Beyaz Lab yönleri)
  veya `-6..-10` derece (dinamik). 2-3 derece kararsızlık gibi görünür.
- **İki cihaz yan yana konacaksa** boyutları eşit olmasın: biri önde ve büyük,
  diğeri arkada ve küçük. Eşit iki cihaz karşılaştırma ima eder; karşılaştırma
  yapmıyorsan yanlış sinyal verir.
- **Bir slaytta bir mockup.** Üç telefon dizmek "ürün turu" değil, gürültüdür.

### Kalite kontrol

Mockup'ı slayta koymadan önce PNG'ye tek tek bak:

- Ekran görüntüsü çerçeveye tam oturmuş mu, altta beyaz boşluk kalmış mı?
  (Kaynak HTML'in `body` yüksekliği hedef yükseklikten kısaysa olur — `body`'ye
  `min-height` ver.)
- Dynamic Island bir başlığın veya ilk kartın üstüne düşmüş mü?
- Metin 100%'de okunuyor mu? Slaytta cihaz küçülecek; ekrandaki 12px gövde
  metni slaytta okunmaz hale gelir. Mockup'taki tipografiyi gerçek üründen bir
  kademe iri kur.
- Şeffaf üretildiyse kenarlarda gri halka var mı? (Gölgenin kırpılması —
  `--pad` değerini artır.)

## Özel çerçeve gerekirse

`device_frame.py` içindeki `SPECS` sözlüğü ekran kutusu, çerçeve kalınlığı ve
köşe yarıçaplarını tutar; yeni bir cihaz eklemek birkaç satırdır. Ama gerçek
bir cihazın fotoğrafını taklit etmeye çalışma — CSS ile çizilen sade ve doğru
bir çerçeve, kötü taklit edilmiş fotogerçekçilikten her zaman daha iyi durur.
