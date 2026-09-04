# Sayfa Desenleri ve Karar Kuralları

Tam spesifikasyon: `docs/kartelapsikoloji-site-plani.md`. Bu dosya sık verilen kararların
kısa referansıdır.

## Ana sayfa bölüm sırası

Sıra, kaygılı ziyaretçinin sorularının **gerçek sırasını** izler — kurumun anlatmak
istediklerinin sırasını değil.

| # | Bölüm | Cevapladığı soru | Zemin |
|---|---|---|---|
| 1 | Sakin karşılama + 2 eylem | Doğru yerde miyim? | Beyaz |
| 2 | Kime, ne için (kartlar) | Benim durumum var mı? | Nane |
| 3 | **Nasıl başlıyoruz** | Ne olacak? | Beyaz |
| 4 | **Mekân** | Nasıl bir yer? | Nane |
| 5 | Ekip | Kim karşılayacak? | Beyaz |
| 6 | Yaklaşan etkinlikler | Burası canlı mı? | Nane |
| 7 | Blogdan | Bunlar ne biliyor? | Beyaz |
| 8 | Kurumlar şeridi | (B2B için) | Petrol |
| 9 | Konum ve iletişim | Nerede, ne zaman? | Nane |
| 10 | Footer (kilitli logo, karekod) | — | Petrol |

**Boş bölüm gizlenir.** Yaklaşan etkinlik yoksa 6. bölüm hiç render edilmez — boş bir bölüm
kurumu ölü gösterir.

## Karar kuralları

| Soru | Kural |
|---|---|
| Bu bölüm nereye gelmeli? | Cevapladığı sorunun kullanıcının zihninde geldiği sıraya |
| Modal mı, sayfa mı? | Sayfa. Modal yalnızca yarıda bırakılmaması gereken akışta; bu sitede neredeyse hiç |
| Kaç menü öğesi? | En fazla 6 + birincil eylem. Fazlası bilişsel yük |
| Bölümleri nasıl ayırayım? | Beyaz ↔ nane zemin ritmi. Çizgi, kutu, gölge yok |
| Kaç CTA? | Sayfa başına **bir** birincil eylem, tekrarlanabilir. İkincil eylem farklı görünür |
| Fotoğraf mı illüstrasyon mu? | Gerçek fotoğraf. İllüstrasyon gerekirse soyut renk alanı; karakter yok |
| Animasyon ekleyeyim mi? | Yalnızca yönlendiriyorsa. 150–250 ms. `prefers-reduced-motion` kapatır |
| Sosyal kanıt nasıl? | Danışan yorumu **yasak**. Yerine: mekân, süreç şeffaflığı, ekip yetkinliği, ruhsat |
| Fiyat yazayım mı? | Evet — şeffaflık bu markanın tezi ve beklenmedik biçimde güçlü bir güven sinyali |
| Pop-up? | Hayır. Hiçbir biçimde |

## Form deseni

**Adım 1 (tek başına gönderilebilir):** ad + (telefon **veya** e-posta) → **[Talebi gönder]**
**Adım 2 (açıkça isteğe bağlı):** kimin için · yaş · uygun saat · serbest not

- Zorunlu alan **iki tane**. Ölçülmüş etki: gereksiz alanları kaldırmak +%24,68
- Doğrulama alandan **çıkınca**, yazarken değil
- Hata suçlamaz, yazılanlar korunur
- KVKK ve ticari ileti onayı **ayrı**; ticari ileti önceden işaretsiz ve koşul değil
- Serbest metin sağlık detayı istemez
- Gönderim sonrası: ne zaman dönüleceği + acil durumda telefon + "şimdilik yapmanız gereken
  bir şey yok"

**Neden böyle:** iletişim formunu görenlerin yalnızca %9,09'u gönderiyor; ama başlanmış
formların tamamlanma oranı çok yüksek. Dar boğaz form değil, **forma başlama kararı**.

## Ekip sayfası

- Tutarlı fotoğraf: farklı zamanlarda çekilmişse arka planı temizleyip aynı nötr zemine koy
- Kart: fotoğraf · ad · **ruhsattaki kadro unvanı** · tek cümle uzmanlık
- 8 kişiden fazlaysa: çalışma alanı / yaş grubu filtresi
- Detayda: eğitim, sertifika, yaklaşım, yaş grupları + **[Bu uzmanla ön görüşme talebi]**
- Unvanlar: *psikolog*, *rehber öğretmen / psikolojik danışman*. "Terapist" yok

## Mekân sayfası

- Bekleme alanı · görüşme odası · çocuk/oyun odası · giriş · **bina dışı**
- Her fotoğrafın altında bir cümle
- Bina girişi fotoğrafı atlanmaz — "doğru kapı bu mu?" gerçek bir stres kaynağı
- İnsansız, doğal ışık, düşük kontrast, boş kadraj
- Video varsa otomatik oynatma yok

## Kurumsal sayfa

Ayrı huni, ayrı dil, ayrı form. Yapı: giriş → paket kartları (aynı yapıda, karşılaştırılabilir)
→ nasıl işler (4 adım) → neden Kartela (kanıtlanabilir olanlar) → SSS → **tek eylem: teklif iste**

Form alanları bireyselden farklı: kurum adı · yetkili · unvan · telefon · e-posta ·
çocuk sayısı · yaş aralığı · ilgilenilen paket · not

## Oyun grupları

- **Yaş filtresi en üstte** — velinin ilk sorusu
- Kart: yaş · gün/saat · süre · kontenjan · eğitmen · koşul
- Dolu grup: "Sıradaki dönem için haber verelim mi?" (kayıp yerine yeni dönüşüm)
- Tek başvuruda ikinci çocuk eklenebilsin

## Etkinlikler

Yaklaşan / Geçmiş sekmeleri · boş durum tasarlı · geçmiş silinmez ·
detayda tarih, saat, süre, yer, kimin için, kontenjan, ücret, kayıt

## Blog

Yazar kutusu (fotoğraf, ad, unvan) · yayın **ve** güncelleme tarihi · **gelecek tarihli yazı
olmaz** · 60–75 karakter satır · yazı sonunda baskısız köprü: "Bu konuda konuşmak isterseniz
buradayız."

## Lokasyon

NAP tutarlı · **çalışma saatleri sitenin her yerinde aynı** · gömülü harita + yol tarifi ·
toplu taşıma, otopark, binaya giriş bilgisi · mobilde tıkla-ara · `LocalBusiness` schema

## WhatsApp butonu

Sağ alt (konvansiyon; sapma keşfedilirliği düşürür) · **site genelinde değil** — yasal
sayfalarda ve form doldurulurken gizli · hazır mesaj: "Merhaba, ön görüşme hakkında bilgi
almak istiyorum." · mesai dışında durum notu · gerçek telefonda test edilir
