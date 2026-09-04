# Yazım Kuralları

Rapor bir insanın yazdığı iş belgesi gibi okunmalı. Aşağıdaki kurallar iki kaynaktan
geliyor: abdullahfarukcom deposunun kendi yazım kuralları ve yapay zekâ metinlerini
ele veren alışkanlıkların listesi.

## Tire yasağı

Uzun tire, kısa tire ve noktalama olarak kullanılan " - " yasak. Bu kural abdullahfarukcom
deposunun kuralı ve rapor da aynı imzayı taşıdığı için burada da geçerli. Yerine virgül,
iki nokta, noktalı virgül, parantez ya da yeni bir cümle kullan.

Aralık yazarken "12.000 ila 30.000 USD" de. Tablolarda da aynı.

`pdf_uret.py` içerikte tire bulursa PDF üretmeyi reddeder.

## Yapay zekâ yazımını ele veren alışkanlıklar

Bunların hiçbiri raporda olmayacak:

- **Aşırı kalın vurgu.** Kalın yazı bir sayfada birkaç yerde olur, her paragrafta değil.
  Vurgu, cümlenin yerinden gelir; kalınlıktan değil.
- **"Sadece X değil, aynı zamanda Y" kalıbı.** İki cümle yaz.
- **Üçlü sıralamalar.** Her listeyi üç maddeye tamamlama refleksi. Kaç madde varsa o kadar yaz.
- **Retorik soru.** "Peki bu ne anlama geliyor?" gibi cümleler. Doğrudan söyle.
- **Boş bağlayıcılar.** "Kısacası", "özetle", "unutulmamalıdır ki", "önemle belirtmek gerekir".
- **Şişirme sıfatları.** "kritik", "hayati", "çarpıcı", "dikkat çekici", "devrim niteliğinde".
  Sayı zaten çarpıcıysa sıfat gereksiz; değilse sıfat yalan.
- **Her paragrafı bir sonuç cümlesiyle bağlama.** Bazı paragraflar veriyle biter, yeter.
- **Emoji ve süs işaretleri.**
- **Aynı cümle uzunluğunun tekrarı.** Uzun ve kısa cümleleri karıştır.
- **Kaçamak dil.** "Duruma göre değişebilir", "bazı durumlarda". Bir aralık ver ve neye
  bağlı olduğunu söyle.

## Ton

Rapor, kurucuya gösterilebilecek kadar saygılı, alıcıya gösterilebilecek kadar açık olmalı.
Kötü haberi yumuşatma ama suçlayıcı da yazma. "Ürün başarısız" yerine "mevcut indirme ve
yorum hacmi ürün pazar uyumuna ulaşılmadığını gösteriyor" de. Fark üslupta değil, kanıtın
cümlede görünmesinde.

Sayıyı önce yaz, yorumu sonra. "Aylık 40.000 TL bulut gideri, yaklaşık 600 aktif kullanıcıya
bölündüğünde kullanıcı başına 67 TL çıkıyor" cümlesi, "bulut gideri çok yüksek" cümlesinden
her zaman daha iyidir.

## Türkçe ayrıntılar

- Sayılarda binlik ayırıcı nokta, ondalık ayırıcı virgül: 17.660 USD, %0,04, 48,15 TL.
- Metin içinde "yüzde 0,04", tablolarda "%0,04".
- Tarihleri açık yaz: 27 Ağustos 2026.
- Şirket unvanlarını ticaret sicilindeki haliyle yaz, kısaltma uydurma.
- Yabancı terimin Türkçesi varsa Türkçesini kullan: burn yerine yakım, runway yerine pist,
  churn yerine iptal oranı. Karşılığı yerleşmemişse ilk geçtiği yerde parantezle açıkla.

## Dizgi

Metin bittiğinde iş bitmiyor. PDF üretildikten sonra `scripts/pdf_denetle.py` çalıştırılır
ve temiz çıkmadan rapor teslim edilmez. Yakaladığı iki hata çok sık görülüyor:

- **Yarım kalan sayfalar.** Bölümlere zorunlu sayfa sonu vermek sayfaların yarısını boş
  bırakıyor. Zorunlu sayfa sonu varsayılan değil, istisna. İçerik aksın.
- **Sağ kenarda kesilmiş görüntü.** Tablo son sütununun sağ boşluğu sıfırsa metin sayfa
  kenarına yapışıyor ve içerik kesilmiş gibi duruyor. Küçük bir boşluk bırak, sayfa kenar
  boşluğunu A4'te 20mm tut.

Uzun tablolar bölünebilir, yeter ki başlık tekrarlansın ve satır ortadan kesilmesin.
Bir tabloyu bütün tutmaya çalışmak çoğu zaman ondan daha kötü bir boşluk üretir.
