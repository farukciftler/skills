# TTS okunuş ölçümleri, ham kayıt

**Düzenek:** ElevenLabs `bill` (`nPczCjzI2devNBz1zQrb`), `eleven_multilingual_v2`,
48 kHz WAV, −16 LUFS. Geri-dönüş: faster-whisper `small`, `language=tr`.
**Tarih:** 2026-08-23. **Yöntem:** aynı cümle iki yazımla sentezlenir, ASR
çıktısı karşılaştırılır. ASR'ın kendi hatası ortak paydadır; **fark** ölçülür.

---

## Tur 1, biçim taraması

| test | metin | duyulan |
|---|---|---|
| rakam-kisa | Hat 426 kilometre uzunluğundaydı. | Hat **400, 26** kilometre uzunluğundaydı. |
| rakam-yazi | Hat dört yüz yirmi altı kilometre uzunluğundaydı. | Hat 426 kilometre uzunluğundaydı. ✅ |
| kisaltma-km | Hat 426 km uzunluğundaydı. | Hat **dört yüz yüzyüz mülandı vatid hilet** uzunluğundaydı. |
| yuzde-simge | Suyun %74'ü tarımda kullanılıyor. | Suyun **%50 kütüğü** tarımda kullanılıyor. |
| yuzde-yazi | Suyun yüzde yetmiş dördü tarımda kullanılıyor. | Suyun yüzde 74'ü tarımda kullanılıyor. ✅ |
| yil-eki | Şehir 1453'te fethedildi. | Şehir 1453'te fethedildi. ✅ |
| sira-sayi | II. Mehmet ve 5. yüzyıl. | **3. Mehmet** ve 5. Yüzyıl |
| kurum | TBMM, DSİ ve İBB ortak açıklama yaptı. | TBMM, **DSI** ve **EBB** ortak açıklama yaptı. |
| mo-ms | M.Ö. 5. yüzyılda, M.S. 300 yılında. | **Müvbeşinci** Yüz Yılda, **Meys** Üç Yüz Yılında |
| ondalik | Nüfus 3,5 milyona ulaştı. | Nüfus 3,5 milyona ulaştı. ✅ |
| ozel-ad | Konstantinopolis'te Justinianus döneminde. | Konstantinopolis'de Justinianus döneminde. ✅ |
| vb | Sarnıç, kemer, tünel vb. yapılar. | Sarnıç, kemer, tünel, vb. Yapılar. ✅ |

## Tur 2, sınır belirleme

| test | metin | duyulan |
|---|---|---|
| sayi-2hane | Tam 74 sarnıç sayıldı. | ✅ doğru |
| sayi-3hane | Tam 426 sarnıç sayıldı. | ✅ doğru |
| sayi-4hane | Tam 1453 sarnıç sayıldı. | ✅ doğru |
| sayi-nokta | Tam 1.400 sarnıç sayıldı. | ✅ doğru |
| mo-noktasiz | MÖ beşinci yüzyılda kuruldu. | MÖ 5. yüzyılda kuruldu. ✅ |
| roma-yazi | İkinci Mehmet ve beşinci yüzyıl. | ✅ doğru |
| dsi-bosluk | D S İ ve İ B B açıklama yaptı. | **DSEV-EBB Açıklamayaptı**, daha kötü |
| dsi-acik | Devlet Su İşleri ve İstanbul Büyükşehir Belediyesi… | ✅ doğru |

**Tur 2'nin gösterdiği:** `426` tek başına sorun değil. Sorun **sayı + birim**
birleşimi. Tur 1'de «Hat 426 kilometre» bozuldu, Tur 2'de «Tam 426 sarnıç»
bozulmadı.

## Tur 3, tekrarlanabilirlik

| metin | koşu | duyulan |
|---|---|---|
| Hat 426 kilometre uzunluğundaydı. | #0 | Hat **4126** kilometre… |
| | #1 | 426 kilometre… ✅ |
| | #2 | Hat **4 düzli 26** kilometre… |
| Hat dört yüz yirmi altı kilometre uzunluğundaydı. | #0 | ✅ |
| | #1 | ✅ |
| Suyun %74'ü tarımda kullanılıyor. | #0 | Suyun **%74'lüğü**… |
| | #1 | ✅ |
| Hat 426 km uzunluğundaydı. | #0 | Hat **400'yiz bu yıl altı kilo emeğe**… |
| | #1 | Hat **dört oğun duysaya müddet o altı yedi kilomantı**… |

**Sonuç:** `sayı + birim` **3'te 2 bozuk** (güvenilmez), `sayı + kısaltma birim`
**2'de 2 felaket** (asla), yazıyla yazım **2'de 2 doğru**.

---

## Uygulanan karar

`motor/ses/okunus.py` şunları otomatik dönüştürür ve altyazıda özgün yazımı
`gorunum` haritasıyla geri getirir:

| dönüşen | dönüşmeyen (ölçülen: gerek yok) |
|---|---|
| kısaltma birim (km, kg, sn, ha…) | yıl + ek (`1453'te`) |
| `%` simgesi + ek | ondalık (`3,5`) |
| Roma rakamı + nokta | Türkçe harf taşımayan kısaltma (`TBMM`, `vb.`) |
| `M.Ö.` / `M.S.` / `DSİ` / `İBB` | özel ad |
| sıra sayısı (`5.` + küçük harf) | |
| sayı + açık birim kelimesi | |

## Ses seçimi ölçümü

Aynı cümle, altı ses. Temel frekans otokorelasyonla, anlaşılabilirlik ASR
geri-dönüşüyle.

| ses | F0 ortalama | F0 dip | Türkçe WER |
|---|---|---|---|
| **bill** ← seçildi | 157,8 Hz | 100,0 Hz | %0 |
| brian | 112,3 Hz | 80,6 Hz | %0 |
| arnold | 121,6 Hz | 96,6 Hz | %0 |
| george | 130,1 Hz | 97,8 Hz | %0 |
| daniel | 137,4 Hz | 105,2 Hz | %0 |
| Supertonic M5 (yerel) | 95,7 Hz | 74,5 Hz | %0 |

**Altısı da Türkçeyi %0 hatayla söylüyor**, seçim anlaşılabilirlik değil, tını.
