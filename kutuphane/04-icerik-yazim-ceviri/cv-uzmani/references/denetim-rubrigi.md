# Denetim Rubriği

Mod B'de kullanılır. Amaç kullanıcıya "güzel olmuş" demek değil, **hangi düzeltmenin
mülakat oranını en çok değiştireceğini** sıraya koymaktır.

## İçindekiler
1. Puanlama eksenleri
2. Kırmızı bayraklar
3. Rapor şablonu
4. Önceliklendirme mantığı
5. Kalibrasyon örnekleri

---

## 1. Puanlama eksenleri

Altı eksen, her biri 0-5. Toplam 30. Puanı gerekçesiz verme; her puanın yanında tek cümle
kanıt olsun (CV'den alıntı veya sayım).

### E1. Parse güvenliği (0-5)
Dosya makine tarafından okunabiliyor mu? `scripts/parse_check.py` çıktısıyla puanla.
- 5: tek sütun, seçilebilir metin, standart başlıklar, iletişim gövdede, tutarlı tarih
- 3: küçük riskler (bir tablo, karışık tarih formatı)
- 0-1: görsel PDF, iki sütun, header'da iletişim bilgisi

### E2. İlk 10 saniye sinyali (0-5)
İlk üçte bir okunduğunda "bu kişi kim ve ne yapabilir" cevabı çıkıyor mu?
- 5: net unvan/özet, en güçlü kanıt üstte, hedefle uyumlu
- 3: özet var ama jenerik; güçlü kanıt ikinci sayfada
- 0-1: özet yok veya klişe; ilk gördüğün şey hobiler/kişisel bilgiler

### E3. Kanıt yoğunluğu (0-5)
**Sayılabilir ölçüt:** sayı, kapsam veya somut sonuç içeren bullet oranı.
- 5: ≥%60 · 4: %45-60 · 3: %30-45 · 2: %15-30 · 0-1: <%15
Sahte/şüpheli rakam varsa puanı düşür ve kırmızı bayrak olarak ayrıca yaz.

### E4. Hedef uyumu (0-5)
Hedef rol/ilan belliyse: tekrar eden terimlerin karşılanma oranı ve en alakalı deneyimin
konumu.
- 5: zorunlu gereksinimlerin tamamı görünür, ilanın dili doğal biçimde geçiyor
- 3: karşılık var ama gömülü, okuyucunun araması gerekiyor
- 0-1: CV başka bir rol için yazılmış

### E5. Dil ve tutarlılık (0-5)
Yazım/dilbilgisi, zaman kipi (geçmiş roller geçmiş zaman), tarih ve noktalama tutarlılığı,
tek dil, unvan/şirket adlarının doğruluğu. Yazım hatası özensizlik sinyali olarak doğrudan
eleme sebebi sayılabilir; bir hata bile puanı 4'e indirir.

### E6. Lokalizasyon uygunluğu (0-5)
Hedef ülkenin normuna göre uzunluk, fotoğraf, kişisel bilgi, belge adı, dil varyantı.
- 0-1: ABD/UK başvurusunda fotoğraf + doğum tarihi (aktif risk)

## 2. Kırmızı bayraklar

Puandan bağımsız, görülür görülmez raporun en üstüne çıkar:

- Doğrulanamayan veya birbiriyle çelişen rakamlar
- CV ile LinkedIn arasında tarih/unvan çelişkisi
- Açıklanmamış 6 aydan uzun boşluk
- Gizli metin, beyaz font, anahtar kelime yığını
- Görsel/taranmış PDF
- Kişisel veri fazlası (TCKN, tam adres, medeni hâl, çocuk sayısı, din, ehliyet — hedefte
  beklenmiyorsa)
- İlan metninden kopyalanmış cümleler
- Referansların telefon numarası (izinsiz veri paylaşımı)
- Anadili olmayan dilde çeviri kokan cümleler

## 3. Rapor şablonu

```markdown
## Özet
[2-3 cümle: CV şu an ne söylüyor, nerede kaybediyor, en yüksek getirili tek düzeltme ne]

## Puan: [X]/30
| Eksen | Puan | Gerekçe |
|---|---|---|
| Parse güvenliği | | |
| İlk 10 saniye | | |
| Kanıt yoğunluğu | | [rakamlı bullet: A/B = %C] |
| Hedef uyumu | | |
| Dil ve tutarlılık | | |
| Lokalizasyon | | |

## Kritik — başvurmadan önce düzelt
1. **[Bulgu]** → [Ne yapılacak, tek cümle]

## Önemli — bu hafta
## İnce ayar

## Yeniden yazım (önce → sonra)
**Önce:** [CV'den birebir]
**Sonra:** [düzeltilmiş, kullanıcının kendi içeriğiyle]
[en az 5 adet]

## Senden gereken bilgiler
- [ ] [eksik rakam / bağlam]
```

## 4. Önceliklendirme mantığı

Sıralamayı "ne kadar yanlış" değil, **"düzeltince mülakat olasılığını ne kadar değiştirir"**
ile yap:

1. **Kritik:** başvuruyu doğrudan öldürenler — okunamayan dosya, yanlış ülke formatı,
   yazım hatası, çelişki, hedefe hiç uymayan içerik.
2. **Önemli:** sinyali zayıflatanlar — kanıtsız bulletlar, gömülü kanıt, zayıf özet,
   yanlış uzunluk, eski rollere fazla yer.
3. **İnce ayar:** tipografi, fiil çeşitliliği, bölüm sırası, bullet uzunluğu.

Her maddeye "neden" ekle. "Bunu çıkar" değil, "bunu çıkar çünkü ABD'de fotoğraf birçok
şirkette değerlendirme dışı bırakma sebebi".

## 5. Kalibrasyon örnekleri

- **26-30:** yayına hazır; ilana göre ince uyarlama yeterli.
- **19-25:** sağlam iskelet, kanıt eksik. Odak: bullet yeniden yazımı ve özet.
- **12-18:** yeniden yapılandırma gerekir; Mod A'ya dönüp kanıt çıkarmak daha hızlı sonuç verir.
- **<12:** sıfırdan kurmak, yamalamaktan ucuz. Kullanıcıya bunu açıkça ve gerekçeli söyle.

Puanı düşük çıkan CV'de kullanıcıyı ezme: puanın ne ölçtüğünü söyle, sonra ilk üç adımı ver.
Rapor, kullanıcı bir saat içinde uygulayabilecek hâle gelmiyorsa fazla uzun demektir.
