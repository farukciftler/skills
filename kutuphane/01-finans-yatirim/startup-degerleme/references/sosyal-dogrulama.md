# Sosyal Hesap Gerçeklik ve Dönüşüm Denetimi

**Her raporda zorunlu.** Takipçi sayısı, bir startup dosyasında en çok yanlış okunan
metriktir; hem kurucular hem alıcılar onu traksiyon sanır. Gerçekte:

- **Takipçi satın almak ucuzdur** — Türkiye'de 1.000 takipçi 2-5 USD. 50.000 takipçi
  100-250 USD'ye alınır. Yani "50 bin takipçi" bir startup'ta 200 dolarlık bir kalem olabilir.
- **Etkileşim satın almak pahalıdır ve sürdürülemez** — her gönderi için ayrıca ödeme gerekir.
- Bu asimetri yüzünden **etkileşim oranı, takipçi sayısından çok daha zor taklit edilir**
  ve hesabın gerçekliğini ölçmenin en ucuz, en güvenilir yoludur.

Ayrıca bu denetim sadece "sahte mi" sorusunu cevaplamaz. Şunu da cevaplar:
**bu kanal ürüne kullanıcı taşıyor mu?** Takipçiler bal gibi gerçek olup ürüne hiç
dönüşmüyor da olabilir — bu durumda pazarlama harcaması bir varlık değil, yakımdır.

---

## 1. Veri toplama — giriş yapmadan

Instagram profili çıkış yapmış tarayıcıda yalnızca ilk birkaç gönderiyi gösterir ve
beğeni sayısını grid'de göstermez. Çözüm **embed uç noktası**:

```
https://www.instagram.com/p/<KOD>/embed/captioned/
```

Bu sayfa beğeni sayısını, tam açıklamayı ve takipçi sayısını herkese açık gösterir.
Adımlar:

1. Profili aç (`instagram.com/<kullanici>/`), açılan giriş modalını kapat.
2. `read_page` ile `filter: interactive` kullanarak `/p/<KOD>/` biçimindeki gönderi
   linklerini topla. Aşağı kaydırıp tekrar okuyarak daha eski gönderileri de al.
3. Her kod için embed sayfasına git ve `find` ile "likes count text" ara.
4. **Not:** embed sayfasının HTML'i sunucudan boş gelir, beğeni JavaScript ile basılır.
   `curl` ile çekmeye çalışma — tarayıcı gerekir.

**Örnekleme kuralı:** En az 10-12 gönderi al ve **mutlaka hem en yeni hem daha eski
gönderilerden** karışık örnekle. Sadece son 3 gönderiye bakmak en sık yapılan hatadır;
bir hesabın son gönderileri reklamla öne çıkarılmış olabilirken arşivi gerçeği söyler.

Diğer platformlar:
- **TikTok**: profil sayfası izlenme sayılarını çıkış yapmışken de gösterir — en kolay platform.
- **X**: gönderi görüntülenme sayıları herkese açık.
- **YouTube**: izlenme/abone oranı; son 10 videonun izlenme medyanı ÷ abone.
- **LinkedIn**: şirket sayfası gönderilerinde beğeni görünür; takipçi sayısı sayfada yazar.

## 2. Hesaplama

```bash
python3 scripts/sosyal_dogrula.py --takipci 49300 \
  --begeniler 186,165,165,44,44,23,17,16,15,12,10,9 \
  --yorumlar 1,0,1,0,0,0,0,0,0,0,0,0 \
  --platform instagram --indirme 4300 --gonderi-sayisi 228 --takip-edilen 231
```

Script; etkileşim oranını, kararı, dağılım uyarılarını, kitle→ürün dönüşümünü ve
hesabın **etkileşime göre düzeltilmiş varlık değerini** basar. Elle oran hesaplama —
eşikler her raporda aynı olsun ki startup'lar kıyaslanabilsin.

## 3. Sağlıklı etkileşim bantları (2026)

Etkileşim oranı = (medyan beğeni + medyan yorum) ÷ takipçi × 100

| Platform | Zayıf | Sağlıklı | İyi |
|---|---|---|---|
| Instagram (10K-100K takipçi) | <%1 | %1-3 | %3+ |
| TikTok (izlenme ÷ takipçi) | <%3 | %3-9 | %9+ |
| X | <%0,3 | %0,3-1,5 | %1,5+ |
| YouTube | <%1 | %1-4 | %4+ |
| LinkedIn şirket sayfası | <%1 | %1-4 | %4+ |

Hesap büyüdükçe oran doğal olarak düşer; 1M+ takipçide %0,5 normal olabilir.
Ama 50 bin takipçide **%0,1'in altı organik olarak açıklanamaz.**

Türkiye gençlik/fırsat/mizah hesaplarında sağlıklı bant genelde daha yüksektir (%2-6),
çünkü niş ve etkileşimli kitlelerdir. Bu, düşük oranı daha da anlamlı kılar.

## 4. Yardımcı testler

**Yorum/beğeni oranı.** Gerçek kitlede yorum, beğeninin %1-5'i kadardır.
Yüksek beğeni + sıfır yorum, satın alınmış etkileşimin imzasıdır (bot beğenir, yorum yazmaz).

**Yeni/eski dağılımı.** En yeni gönderilerin etkileşimi arşivin 4 katından fazlaysa
organik bir sıçrama değil, ya reklamla öne çıkarma ya etkileşim satın alma vardır.
Ayırt etmek için yoruma bak: **reklamda yorum da artar, satın almada artmaz.**

**Takip edilen sayısı.** Hesap, takipçi sayısına yakın sayıda hesabı takip ediyorsa
karşılıklı takip ile şişirilmiş olabilir. Tersine çok düşük takip (ör. 231) tek başına
bir şey kanıtlamaz — hem gerçek markalar hem satın alınmış hesaplar böyle görünür.

**Takipçi coğrafyası.** Yorumların ve etiketlenen hesapların dili/ülkesi ürünün pazarıyla
uyuşuyor mu? Türkiye'ye satış yapan bir üründe yabancı dilde yorum akını satın alma işaretidir.

**İçerik–ürün uyumu.** Hesabın ne paylaştığına bak. Ürünü değil, jenerik ilgi çekici
içerik (burs listeleri, iş ilanları, mizah) paylaşan hesaplar takipçiyi **içerik için**
toplar. Bu takipçiler gerçek olabilir ama **ürüne dönüşmezler** — çünkü baştan ürün için
gelmemişlerdir. Bu, sahte takipçiden farklı ama sonucu benzer bir problemdir ve raporda
ayrı teşhis edilmelidir.

**Hesap geçmişi.** Çok sayıda takipçisi olan hesabın adı/konusu değişmiş olabilir
(hazır kitle satın alınıp markaya çevirme). `web.archive.org` ve eski gönderilerin
konusu bunu ele verir.

## 5. Kitle → ürün dönüşümü

```
takipçi ÷ toplam indirme
```
Sağlıklı bant 0,1-1,0. Üstüne çıkıldığında iki teşhis vardır ve **hangisi olduğunu
etkileşim oranı söyler**:

| Takipçi/indirme | Etkileşim | Teşhis | Değere etkisi |
|---|---|---|---|
| Yüksek | Düşük | Takipçi sahte/ölü. Kanal diye bir şey yok | Takipçi sayısı varlık olarak yazılamaz |
| Yüksek | Sağlıklı | Kitle gerçek, ürüne ilgi duymuyor | Sorun üründe veya çağrı-eylem/onboarding'de; **giderilebilir**, bu iyi haberdir |
| Normal | Sağlıklı | Kanal çalışıyor | Gerçek dağıtım varlığı; prim uygulanır |

İkinci satır önemli: kitle gerçekse sorun teknik/ürünseldir ve **çözülebilir bir sorundur**.
Bu ayrımı yapmadan "kanal çalışmıyor" demek, düzeltilebilir bir sorunu ölümcül gibi göstermektir.

## 6. Bu bir yakım kalemi mi?

Sosyal hesap bedava değildir. Rapora şu maliyetleri de çıkar:
- İçerik üretimi: gönderi sayısı × gönderi başına tasarım/metin maliyeti.
  228 carousel gönderi, ayda ~20 gönderi temposunda bir tasarımcı/içerik kişisi demektir —
  Türkiye'de aylık 25.000-60.000 TL.
- Reklam harcaması (etkileşimdeki ani sıçrama bunu ele verir)
- Varsa takipçi/etkileşim satın alma

Sonra tek soruyu sor: **bu harcama kaç kullanıcı getirdi?**
`gönderi başına etkileşim × gerçekçi tıklama oranı (%5-20) × kurulum oranı`
Sonuç gülünç derecede küçükse, bu bir pazarlama varlığı değil, **aylık yakımın gizli bir
kalemidir** ve alıcı için ilk kesilecek gider odur.

## 7. Raporda nasıl yazılır

- Ham takipçi sayısını **asla** tek başına avantaj maddesi yapma.
- Her zaman şu üçlüyü birlikte yaz: takipçi · etkileşim oranı · etkin takipçi.
- Kararı ve örneklenen gönderi sayısını belirt ki okuyucu kanıtın gücünü görsün.
- Hesap ölü çıkarsa bunu değerlemeye **yansıt** — senaryo olasılıklarını ve
  varlık tabanını güncelle, sadece bir not düşüp geçme.
