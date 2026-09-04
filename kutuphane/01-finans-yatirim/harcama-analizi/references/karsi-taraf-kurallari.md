# Karşı taraf kuralları — kendi / aile / kira / kişi

Transferlerin (FAST, EFT, havale, Vakıf Katılım Amir/Lehdar) kategorisi
işyerinden değil **karşı taraftan** gelir. Sözlük: `data-belgeler/karsi_taraf_sozlugu.csv`.

```
desen,tur,kategori,alt_kategori,guven,not
ABDULLAH FARUK CIFTLER,ic_transfer,ic_transfer,kendi_hesabi,kesin,kendi adına tüm hesaplar (Vakıf Katılım/TEB/Papara/Akbank)
BETUL CIFTLER,aile_destek,aile_destek,es,kesin,eş — Kuveyt Türk ve Papara
ATILA OZGUC,harcama,konut,kira,varsayim,İGDAŞ/İSKİ sözleşmeleri aynı adda + aylık ~15 bin düzenli — kullanıcı teyidi yok
```

## Kurallar

1. **Kendi adı** her bankada `ic_transfer`. Karşı taraf metni bazen IBAN
   içerir (`TR61 … nolu ABDULLAH FARUK ÇİFTLER`), bazen yalnız ad; desen ada
   göre yazılır, ASCII'ye indirgenmiş metne uygulanır.
2. **Maaş tekilleştirme.** Maaş ilk hangi hesaba yattıysa (`gelir/maas`)
   oradan sonraki her geçiş `ic_transfer/maas_gecisi`dir. Motor bunu karşı
   taraf kuralıyla zaten yapar (kendi adı = iç transfer); ek kural: aynı
   tutarın 3 iş günü içinde iki bankada `gelir/maas` görünmesi → ikincisi
   uyarıyla `ic_transfer`e çevrilir ve `mutabakat.csv`'ye yazılır.
3. **Aile** (`aile_destek`): eş `es`; soyadı aynı diğer kişiler ve kullanıcı
   tarafından aile diye bildirilenler `aile`. Soyadı benzerliği **tek başına
   `varsayim`** üretir, `kesin` yapmaz.
4. **Kira** (`konut/kira`): şu üç kanıt birlikteyse `varsayim` yazılır —
   (a) aynı kişiye aylık düzenli, benzer tutarlı transfer; (b) fatura
   tahsilatlarındaki sözleşme sahibi aynı ad; (c) transferin ayın başında
   olması. Kullanıcı "evet, ev sahibi" derse `kesin`. Raporda `varsayim`
   satırları "kira (varsayım)" etiketiyle ayrı toplanır, hiçbir zaman
   "kira" başlığı altında sessizce sayılmaz.
5. **Kişi ödemeleri** (`kisi_odeme`): sözlükte olmayan gerçek kişiler.
   400 TL'lik 15 ayrı transfer gibi kalıplar (ortak hesap, hediye, borç)
   **yorumlanmaz**; sayı ve toplam verilir, kullanıcıya sorulur.
6. **Kurumlar** (APPLICENTER = işveren, MİDAS = aracı kurum, Agesa = sigorta,
   Nays = ödeme uygulaması) sözlükte kurum satırı olarak durur; işveren
   girişleri `gelir/maas`, aracı kurum iadesi `varlik_transferi/birikim`.
7. **Papara / Enpara / TEB kendi hesabı** → `ic_transfer`; başkasının Papara'sı
   → o kişinin kuralı.
8. Sözlüğe kişi eklemek **kullanıcı onayı** ister; motor eksik karşı tarafı
   `acik_sorular`a yazar, kendisi eklemez.

## Bilinen karşı taraflar (02.09.2026 ekstresinden, teyit durumu)

| Karşı taraf | Toplam (12 ay) | Adet | Tür | Güven |
|---|---|---|---|---|
| Vakıf Katılım — kendi | ~898 bin (FAST 511 + EFT 387) | 15 | ic_transfer | kesin |
| TEB — kendi | ~130 bin | 51 | ic_transfer | kesin |
| Papara — kendi | ~10 bin | 6 | ic_transfer | kesin |
| Betül Çiftler (Kuveyt Türk + Papara) | ~203 bin | 58 | aile_destek/es | kesin (eş). **Kullanıcı 02.09.2026: her Cuma 4.250 TL** — ekstrede 20 kez, 17'si Cuma |
| Atila Özgüç (Garanti) | 158 bin | 10 | konut/kira | **varsayım** — ayın 1–4'ü, 14.000 → 19.000; **kullanıcı 02.09.2026: kira+aidat 19.500/ay**, alıcı adı teyit bekliyor |
| Dönay Yıldız Çiftler | 10 bin | 6 | aile_destek/aile | varsayım (soyadı) |
| Ahmet Necip Çiftler · Muhammed Mustafa Çiftler | 12 + 50 bin | 3 | aile_destek/aile | varsayım (soyadı) |
| Applicenter Teknoloji (giriş, "maas") | 1,42 milyon | 12 | gelir/maas | kesin |
| Diğer ~25 kişi (400–14.000) | ~60 bin | ~35 | kisi_odeme | yok |

## Kullanıcının bildirdiği hane rutinleri (02.09.2026)

- **Eşe her Cuma 4.250 TL** (Vakıf Katılım cari → Kuveyt Türk). Ekstre doğruluyor:
  Oca–Ağu 2026 arasında 20 kez, 17'si Cuma, medyan aralık 7 gün. Haftalık
  ritim → `duzenli_odemeler` tablosunda `haftalik`, yıllık 52 × 4.250 = 221.000.
- **Kira + aidat aylık 19.500 TL**, cari hesaptan gönderilir. Ekstrede ayın
  1–4'ünde 19.000'lik transferler var (2025'te 14.000). 19.500 ile 19.000
  farkı (aidat?) ilk kira ödemesinde görülünce not düşülür.
- Maaş 170.000 TL 02.09.2026'da cari hesaba geldi; **aynı gün 4.250 eşe
  gitti** (Çarşamba — istisna, normali Cuma). Kalanın dağılımı (harcama kesesi /
  kalıcı yatırım) kullanıcıdan bekleniyor; deftere akış yazılmadı.
