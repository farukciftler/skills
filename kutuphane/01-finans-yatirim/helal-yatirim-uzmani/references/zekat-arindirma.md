# Zekât ve Arındırma (Purification)

İki kavram ayrıdır ve birbirinin yerine geçmez:
- **Zekât** = ibadet; nisaba ulaşan ve üzerinden yıl geçen zekâta tâbi servetin %2,5'i, zekât verilebilecek kimselere.
- **Arındırma** = temizlik; uygun olmayan (ağırlıkla faiz) gelirin portföy sahibine düşen payının, sevap beklemeden hayra verilmesi. Sadaka sevabı niyetiyle değil, "üzerimden çıkarma" niyetiyle verilir; zekât matrahından düşülmez, zekât sayılmaz.

## 1. Arındırma

### Yöntem A — Temettü arındırması (Zoya/Islamicly ve fon pratiği; en yaygın)
`arındırma = alınan brüt temettü × (uygun olmayan gelir / toplam gelir)`
Şirketin son denetlenmiş finansallarındaki oran kullanılır. Temettü almayan yatırımcı bu yöntemde arındırma yapmaz.

### Yöntem B — Kapsamlı / hisse başına arındırma (AAOIFI çizgisi; Musaffa "comprehensive"; TKBB md. 3.6)
`arındırma = hisse başına uygun olmayan gelir × elde tutulan hisse adedi × (elde tutma günü / dönem günü)`
Temettü **dağıtılsın dağıtılmasın** uygulanır; TKBB standardı bu yaklaşımı benimser. TKBB'ye özgü nüans (md. 3.6.2): arındırılacak faiz gelirinin hesabında **enflasyonu aşan kısım** esas alınır — yüksek enflasyon ortamında Türkiye pratiğini ciddi etkiler; kullanıcı TKBB çizgisindeyse bunu uygula ve açıkla.

### Sermaye kazancı arındırılır mı?
Çoğunluk görüşü: uygun statüdeki hissenin satış kârı arındırılmaz (fiyat, faiz gelirinin doğrudan yansıması değildir). Zoya danışmanları gibi bazıları ihtiyaten temettü+sermaye kazancı birleşik arındırmayı tavsiye eder. İkisini de sun; varsayılan çoğunluk görüşü.

### Pratik kurallar
- Bedelsiz hisse/warrant gibi nakit olmayan menfaatler nakde çevrilmedikçe arındırılmaz; satılırsa aynı oranla arındırılır.
- Uygunluğunu kaybetmiş hisseyi elden çıkarma penceresinde elde edilen gelir/kazancın uygun olmayan kısmı arındırılır.
- Helal ETF/katılım fonlarında arındırmayı genelde fon yapar ve raporlar; kullanıcıya fonun arındırma açıklamasını kontrol etmesini söyle (SPK, fon izahnamesinde arındırma esaslarının yer almasını ister).
- Arındırma tutarı hayır işlerine (eğitim, sağlık, yoksula yardım, altyapı) verilir; kişisel fayda sağlanacak yere verilmez.
- `scripts/helal_hesap.py arindirma` her iki yöntemi ve TKBB enflasyon nüansını hesaplar.

## 2. Zekât

### Ön şartlar
- **Nisap:** 80,18 gr altın karşılığı (Diyanet'in kullandığı değer; klasik kaynaklarda 85 gr da yaygındır — kullanıcıya hangisini kullandığını söyle). Nisap tespitinde altının **alış** fiyatı esas alınır (Diyanet pratiği).
- **Havelan-ı havl:** matrahın üzerinden bir kameri yıl geçmesi. Oran: kameri yıl için %2,5; miladi yıl üzerinden hesaplayan için %2,577 kullanılabilir.
- Zekât matrahından, vadesi bir yıl içinde gelecek borçlar düşülür.

### Hisse senedi zekâtı — niyet belirler
| Niyet | Yöntem |
|---|---|
| Alım-satım (trade) amaçlı | Ticaret malı hükmü: **piyasa değerinin tamamı** × %2,5 (Diyanet görüşü de budur) |
| Uzun vadeli / temettü amaçlı — Diyanet yöntemi | Zekât **alınan kâr payı** üzerinden verilir; kâr payının zekâtı verilince hisse değeri üzerinden ayrıca zekât gerekmez |
| Uzun vadeli — dönen varlık (zekâta tâbi varlık) yöntemi | Şirketin bilançosundan zekâta tâbi varlık oranı (≈ dönen varlıklar: nakit, alacak, stok) bulunur; `hisse değeri × bu oran × %2,5`. Fiilî şirket ortağı için Diyanet'in de esas aldığı yaklaşımdır; halka açık hissede AAOIFI çizgisiyle uyumludur |
| İhtiyat yöntemi | Uzun vadeli tutulsa bile piyasa değerinin tamamından vermek — en güvenli, en cömert seçenek |

Kullanıcının niyetini sor; yöntemi ona göre seç, seçtiğin yöntemi ve alternatifini söyle.

### Diğer varlıklar
| Varlık | Zekât muamelesi |
|---|---|
| Katılma hesabı | Anapara + tahakkuk etmiş kâr payı, tamamı matraha girer |
| Kira sertifikası / sukuk / kira sertifikası fonu | Piyasa değeriyle matraha girer (ticari menkul kıymet) |
| Katılım hisse/endeks fonu, helal ETF | Hisse zekâtı kuralları; pratikte fon birim değerinin tamamı (trade niyeti) veya dönen varlık oranı |
| Altın/gümüş (fiziki, gram hesabı, ziynet) | Tamamı matraha girer (Hanefî görüş; ziynet dahil) |
| Nakit, döviz | Tamamı |
| Alacaklar | Tahsili kuvvetli alacaklar matraha girer |
| Oturulan ev, araç, işte kullanılan demirbaş | Girmez |
| Kiraya verilen gayrimenkul | Mülkün kendisi girmez; birikmiş kira geliri nakit olarak girer |
| BES birikimi | İhtilaflı: tasarrufa erişim kısıtı nedeniyle "erişilebilir değilse yıllık zekât gerekmez, çekince birikmiş yıllar hesaplanır" görüşü ile "her yıl net erişilebilir değer üzerinden verilir" görüşü vardır — ikisini de sun |
| Kripto (elinde tutan için) | Mübadele/ticaret varlığı olarak piyasa değeriyle matraha girer (elde tutmayı caiz gören görüşe göre); hüküm tartışması ayrı, zekât yükümlülüğü ayrıdır |

### Hesap akışı (Claude için)
1. Zekât gününü netleştir (kullanıcının kendi kameri tarihi).
2. Matrah kalemlerini topla (yukarıdaki tablo) − 1 yıl içinde vadesi gelen borçlar.
3. Nisap kontrolü: güncel gram altın alış fiyatını web'den çek → 80,18 gr eşiği.
4. `scripts/helal_hesap.py zekat` ile hesapla; hisselerde niyet bazlı yöntemi parametre olarak geçir.
5. Çıktıda: matrah dökümü, kullanılan yöntemler, tutar, ve "arındırma bundan ayrıdır" hatırlatması.

## 3. İşlenmiş örnek

Portföy: 500.000 TL katılım hisse fonu (trade niyeti), 200.000 TL kira sertifikası fonu, 30 gr altın (gram fiyatı X TL), 100.000 TL katılma hesabı; 50.000 TL kredi kartı dönem borcu.
- Matrah = 500.000 + 200.000 + 30·X + 100.000 − 50.000 → nisap üstüyse × %2,5.
- Ayrıca yıl içinde tek hissesi olan ABC'den 10.000 TL brüt temettü aldıysa ve ABC'nin uygun olmayan gelir oranı %1,8 ise → arındırma = 180 TL (Yöntem A). TKBB kapsamlı yöntem istenirse hisse başına uygunsuz gelir verisiyle B yöntemi hesaplanır.
