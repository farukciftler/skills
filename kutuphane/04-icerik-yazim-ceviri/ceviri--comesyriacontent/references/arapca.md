# Arapçaya çeviri — Suriye Arapçası

Hedef: Şamlı bir gazetecinin yazdığı gibi okunan metin. Ne Ezher hutbesi, ne
Mısır dizisi altyazısı, ne de Google Translate.

## Register: fasih gövde, Şamî damar

| Nerede | Ne kullanılır |
| --- | --- |
| Gövde metni, açıklama, tarih anlatımı | Modern fasih (MSA) — gazete fasihçesi |
| Yer, yemek, zanaat, eşya, gündelik nesne | Şamî sözcük |
| Alıntı, replik, resim altı, birinin sözü | Gerçek Şamî |
| Başlık ve künye satırı | Fasih, ama kısa |

Modern fasih derken kastedilen: **kısa cümle, az bağlaç, süs yok.** Klasik
Arapçanın uzun devrik yapıları değil. Cümle 20 kelimeyi geçiyorsa böl.

## Şamî sözcükler — kullan

Bunlar alıntıda, replikte ve yerel nesne adında kullanılır:

| Şamî | Anlam | Mısır/Körfez karşılığı — **kullanma** |
| --- | --- | --- |
| هلق | şimdi | دلوقتي *(Mısır)*, الحين *(Körfez)* |
| شو | ne | إيه *(Mısır)*, وش *(Körfez)* |
| كتير | çok | قوي / أوي *(Mısır)* |
| منيح | iyi | كويس *(Mısır)* |
| بدي | istiyorum | عايز *(Mısır)*, أبغى *(Körfez)* |
| هون | burada | هنا *(fasih, dialogda düz durur)* |
| لسا | hâlâ / henüz | — |
| عم + fiil | şimdiki zaman | بـ + fiil *(Mısır)* |

## Yakalanması gereken Mısır/Körfez sızıntıları

Yapay zekâ Arapçası varsayılan olarak Mısır'a kayıyor — eğitim verisinin
ağırlığı orada. En sık sızanlar:

- **دلوقتي، إيه، عايز، كويس، أوي** — hiçbiri Suriye ağzı değil.
- **جـ harfinin Mısır telaffuzuna göre yazımı.** Şam'da ج normal telaffuz edilir.
- **سوريا** yazımı → bu sitede **سورية**.
- Körfez basınının resmî kalıpları: **الشقيقة، المملكة** gibi kalıplar bir
  gezi rehberinde yersiz.

## Fasih tarafında yapay zekâ tiklikleri

Bunlar dilbilgisi olarak doğru ama metni anında makine yapıyor:

| Kalıp | Sorun | Yerine |
| --- | --- | --- |
| علاوة على ذلك | Gereksiz bağlaç, her paragrafta çıkıyor | Sil, ya da و |
| بالإضافة إلى ذلك | Aynı | Sil |
| من الجدير بالذكر أن | Yastık ifade | Cümleyi doğrudan kur |
| تجدر الإشارة إلى أن | Aynı | Sil |
| يُعتبر ... من أهم | Kalıplaşmış övgü, hiçbir şey söylemiyor | Somut bilgi ver |
| يتميز بـ ... العريق | Turizm broşürü | Ne olduğunu yaz |
| في الختام | "Sonuç olarak" — yazı zaten bitiyor | Sil |
| تاريخ عريق وثقافة غنية | Boş övgü ikilisi | Hangi tarih, hangi kültür? |

## Yapı

- **إنّ ile başlama alışkanlığı.** Vurgu gerçekten gerekmiyorsa cümleyi düz kur.
- **و ile cümle bağlama** Arapçanın kendi yapısıdır, ama makine bunu mekanik
  yapıyor: her cümle و ile başlıyor. Paragrafta en fazla bir iki tane.
- **Pasif (المبني للمجهول) az kullanılır.** Fasih yazıda etken cümle normaldir;
  İngilizceden gelen pasif yığını Arapçada ağır durur.
- **Masdar zinciri kırılır.** "عملية ترميم القلعة" yerine "رُمّمت القلعة".
- **Sıfat tamlaması yığma.** Arapça sıfatı isimden sonra alır ve üç sıfat
  arka arkaya geldiğinde cümle çöker. En fazla iki.

## Rakamlar

**Latin rakam kullan: 1500، 09:00، 12.** Arap-Hint rakamı (١٥٠٠) yazma.

Sebep teknik: ön yüz tarih ve sayıları `ar-u-nu-latn` ile basıyor
(`article-shell.tsx`, `cities/[slug]/page.tsx`). Gövdede ١٥٠٠ yazarsan aynı
sayfada iki rakam sistemi yan yana gelir ve okuma bozulur.

### Yüzyıl istisnası

**Yüzyıl rakamla değil sıra sayısıyla yazılır:** `القرن الثامن عشر`, yani
"18. yüzyıl". Kural Latin rakamla çelişmiyor — o kural Arap-Hint rakamına
karşı, sayının nereye yazılacağına değil. Sitenin on sekiz kaydı böyle ve
düzgün Arapça bu.

`القرن 18` yazma. Aralıkta rakam serbest, çünkü yazıyla hantallaşıyor:
`بين القرنين 15 و13 ق.م`.

Bir dönem bu, `denetle.mjs`'te "sayı düştü" diye HATA veriyordu; betik artık
yüzyıl sözcüğünün çevresine bakıp rakamı da sıra sayısını da kabul ediyor.
Ama **atlamıyor**: yüzyıl gerçekten yazılmamışsa hâlâ HATA. İngilizcede ev
üslubu ters yönde — orada rakam (`18th century`), yazıyla değil.

## Tipografi ve RTL

- **Harf aralığı verilmez.** Arapça bağlı yazıdır; `letter-spacing` kelimeyi
  kırar. Site bunu `html[lang='ar'] *` ile zaten sıfırlıyor — ama gövdeye elle
  `style` yazma.
- **Latin harfli terim gömerken** yönü karışıyor: sayı ve Latin sözcük
  RTL akışın içinde ters sıraya düşebiliyor. Mümkünse Arapça karşılığını yaz;
  yazmak zorundaysan parantez içine al.
- **Noktalama Arapça olur:** virgül `،`، soru işareti `؟`، noktalı virgül `؛`.
  Latin `,` ve `?` kullanma.

## Okur kim

Suriye'deki okur ve diasporadaki Suriyeli. İkisi de:

- Yer adını **biliyor** — "Bab Sharqi'nin nerede olduğu" açıklanmaz.
- Tarihi kabaca biliyor — Emevî'nin kim olduğu anlatılmaz.
- Ama **neden bu yazının yazıldığını** merak eder. Türkçe metin "burası şöyle
  bir yer" diye başlıyorsa Arapça metin "burası şu an nasıl" diye başlamalı.

Bu yüzden Arapça sürüm çoğu zaman **en çok yeniden yazılan** sürüm oluyor. Bu
doğru; birebir çeviri burada en kötü sonucu veriyor.

## Duygu tonu

Suriye içeriğinde en kolay düşülen tuzak: **ağıt tonu.** Marka sesi bunu açıkça
reddediyor — nostalji merakla bağlanır, yasla değil.

Arapça yazarken bu tehlike daha büyük, çünkü dilde hazır bir ağıt repertuvarı
var (ما تبقى من، أطلال، ذكريات ضائعة). Kullanma. Yıkımı anlatman gerekiyorsa
somut yaz: ne yıkıldı, ne kadarı onarıldı, bugün açık mı.
