# Kalibrasyon ve Sistem İyileştirme

Ayda bir ya da kullanıcı istediğinde oku. Bu, sistemin "daha iyi tahmin eden yapıya" dönüştüğü yer — ama beklenen yoldan değil.

## Metrikler ne anlatır

```bash
python scripts/pt.py --root <yol> calibrate --window 30
```

| Metrik | Şans seviyesi | Nasıl okunur |
|---|---|---|
| `skill_score` | 0 | `1 - MAE/baseline_MAE`. **En önemli metrik.** >0 ise tahminler "hiç değişmeyecek" demekten iyi. ≤0 ise tahminlerin değer üretmiyor. |
| `yon_isabeti` | 0.50 | Yön tutturma oranı. n<30 iken yorumlama, gürültü. |
| `bant_kapsama` | 0.80 hedef | Gerçekleşenin %80 bandı içinde kalma oranı. >0.90 bantlar çok geniş, <0.70 çok dar. |
| `brier` | 0.25 | `p_up` olasılıklarının kalitesi. Düşük iyi. 0.25'in üstü, sabit 0.5 demekten kötü. |
| `bias_pct` | 0 | Ortalama işaretli hata. Pozitif = sistematik iyimserlik. |
| `baseline_yenme_orani` | 0.50 | Tahminlerin baseline'dan iyi çıktığı gün oranı. |

## İstatistiksel anlamlılık — buna dikkat

Bu en kolay kendini kandırma noktası. Kaba eşikler:

- **n < 20**: Hiçbir şey yorumlanamaz. Rapora "henüz anlamlı veri yok" yaz.
- **n = 20–50**: Yön isabetinin %50'den anlamlı sapması için kabaca %65 üstü veya %35 altı gerekir.
- **n = 100+**: %58 üstü yön isabeti dikkate değer olmaya başlar.
- **n = 250+ (yaklaşık 1 yıl günlük)**: Ancak burada gerçek bir sonuca varılabilir.

10 günlük veriyle "%70 isabet, sistem çalışıyor" demek, sistemi çöpe atmanın en hızlı yoludur. Kullanıcı erken heyecanlanırsa bunu nazikçe ama net söyle.

Ayrıca **çoklu karşılaştırma tuzağı**: 5 varlık × 3 ufuk = 15 metrik seti bakıyorsun. Şans eseri birinin iyi görünmesi neredeyse kesindir. "KUT'ta 1 aylık tahminlerim %80 tutuyor" cümlesi, n=6 ise hiçbir şey ifade etmez.

---

## Aylık inceleme prosedürü

### Adım 1 — Sayıları çek

```bash
python scripts/pt.py --root <yol> calibrate --window 30
python scripts/pt.py --root <yol> calibrate --window 90    # varsa
```

30 ve 90 günü karşılaştır. Sadece 30 güne bakmak trend yerine gürültü gösterir.

### Adım 2 — Bant genişliğini ayarla

Tek net eyleme dönüşebilen metrik budur, çünkü doğrudan kontrol edilebilir:

- `bant_kapsama` > 0.90 ve n ≥ 30 → bantlar gereksiz geniş, tahminler bilgisiz. `tahmin-protokolu.md`'deki bant tablosunu ilgili satırda **%20 daralt**.
- `bant_kapsama` < 0.70 ve n ≥ 30 → aşırı güven. Bantları **%30 genişlet**. (Daralma ve genişleme asimetriktir çünkü aşırı güvenin maliyeti daha yüksektir.)
- 0.75–0.85 arası → dokunma.

Değişikliği referans dosyasına gerçekten uygula, sadece raporda söyleme.

### Adım 3 — Sistematik sapmayı düzelt

`bias_pct` sürekli pozitifse (n ≥ 30), tahminler yapısal olarak iyimser. Düzeltme: sonraki ay tüm `point_pct` değerlerinden ortalama bias'ı çıkar. Bu naif ama etkili bir düzeltmedir ve işe yarayıp yaramadığı bir sonraki incelemede ölçülür.

### Adım 4 — Kanıt türü analizi

`forecasts/*.json` içindeki `drivers` bağını kullanarak, kanıt ağırlığına göre grupla: "yüksek ağırlıklı kanıta dayanan tahminler, düşük ağırlıklıya dayananlardan daha iyi mi?" Değilse — ki muhtemelen değil — bu, haber okumanın tahmin gücü katmadığının kanıtıdır ve **bu da bir bulgudur**, üzerini örtme.

`evidence/*.md` dosyalarını gözden geçirip şunu sor: büyük hareket olan günlerde o hareketi önceden işaret eden bir şey var mıydı, yoksa gerekçe sonradan mı uyduruldu? İkincisi çok yaygındır.

### Adım 5 — Karar ver ve yaz

`reviews/YYYY-MM.md` dosyasına şu şablonla yaz:

```markdown
# Kalibrasyon · YYYY-MM

## Sayılar
30g: n=.. skill=.. yön=.. bant=.. brier=.. bias=..
90g: ...

## Geçen ay ne değiştirmiştik, işe yaradı mı
(bir önceki review'daki kararlar ve sonuçları)

## Bu ayın bulguları
- ...

## Bu ay yapılan değişiklikler
- [ ] ...

## Vazgeçilenler
- (hangi varlık/ufuk için tahmin üretmeyi bıraktık ve neden)
```

"Geçen ay ne değiştirmiştik, işe yaradı mı" bölümü zorunlu. Olmadan sistem iyileşmez, sadece rastgele salınır.

---

## İyileştirme aslında neye benziyor

Kullanıcının beklentisi muhtemelen "model zamanla daha iyi tahmin etmeyi öğrenecek". Gerçekte olan şey daha çok şu, ve bunu söylemekten çekinme:

1. **Ay 1-3**: Bantlar yanlış kalibre, aşırı güven yüksek, skill skoru negatif. Normal.
2. **Ay 3-6**: Bantlar oturur, `bant_kapsama` 0.80'e yaklaşır. Yön isabeti hâlâ %50 civarı. Bu **başarıdır** — belirsizliği doğru ölçmeyi öğrendin.
3. **Ay 6+**: Muhtemel sonuç, 1 günlük ufukta hiçbir tahmin gücü olmadığının kesinleşmesi; 1 aylık ufukta makro rejim (faiz yönü, enflasyon patikası) sayesinde zayıf ama sıfırdan farklı bir sinyal.

Sistemin gerçek getirisi şunlar:
- **Karar günlüğü**: 6 ay sonra "o zaman ne düşünüyordum" sorusunun yazılı cevabı var. Hafıza bunu yeniden yazar, dosya yazmaz.
- **Aşırı işlem yapmaya karşı fren**: Tahmin gücünün olmadığını sayıyla görmek, haberle işlem yapma dürtüsünü kırar. Bu, çoğu bireysel yatırımcı için en yüksek getirili tek davranış değişikliğidir.
- **Belirsizliği doğru ölçme alışkanlığı**: Bu beceri portföyün çok ötesinde işe yarar.

Eğer 6 ay sonra skill skoru hâlâ ≤0 ise, doğru sonuç sistemi karmaşıklaştırmak değil, **1 günlük tahmin üretmeyi bırakıp** sadece snapshot + gündem günlüğü + aylık projeksiyon tutmaktır. Bunu önermekten çekinme.

---

## Ne zaman durmalı

Kullanıcı şunlardan birini yapmaya başlarsa sistem amacından sapıyor demektir, ve bunu bir kez açıkça söyle:

- Tahminlere dayanarak sık alım/satım yapmak
- Kaldıraçlı pozisyon almak
- "Sistem şunu dedi" diye portföy ağırlığını büyük ölçüde değiştirmek
- Zarar sonrası tahmin sıklığını artırmak

Bunlar sistemin ürettiği bilgiye, o bilginin taşıyabileceğinden fazla ağırlık vermektir. Skill'in dürüstlük çerçevesi tam olarak bunu önlemek için var.
