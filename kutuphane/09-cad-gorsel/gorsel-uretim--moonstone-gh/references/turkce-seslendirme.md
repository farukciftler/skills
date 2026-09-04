# Türkçe Seslendirme — Fonetik, Prozodi, Ölçüm

Seslendirmenin "Türkçe tonlamaya uymaması" bir his değil, **ölçülebilir** bir
şey. Bu dosya neyin ölçüldüğünü, hangi ayarın kazandığını ve metnin nasıl
yazılması gerektiğini tutuyor. Metnin **yazımı** için `moonstone-residence/
references/seslendirme-metni.md`; burası **sesin** tarafı.

## İçindekiler
1. Neden yabancı duyuluyor — Türkçenin üç prozodi kuralı
2. Ölçüm: kulak yerine sayı
3. Ölçülmüş ayarlar — kazanan üçlü
4. Ölçümden çıkan yazım kuralları
5. Eşikler ve denetim kapısı
6. Aracın sınırları

---

## 1. Neden yabancı duyuluyor

### 1.1 Sözcük vurgusu son hecededir, ama istisnalar çok

Türkçede vurgu kural olarak **son hecede**. Bozanlar:

| Durum | Vurgu | Örnek |
|---|---|---|
| **Yer adları** | ilk hece | **TUZ**la, **AN**kara. İki heceli yer adlarında her zaman ilk hece. |
| `-ya` ile biten yer adı | sondan bir önceki | Al**MAN**ya |
| `-istan` ile biten | sonda (kurala döner) | Kazakis**TAN** |
| Olumsuzluk `-ma/-me` | kendinden önceki heceye kayar | **GEL**me |
| Akrabalık adları | ilk hece | **AN**ne, **YEN**ge, **HA**la, **AM**ca |

Pratikte: **"Tuzla Aydıntepe" ikisi de yer adı, ikisi de ilk heceden vurgulu.**
TTS son heceye vurgu koyarsa cümle anında yabancı duyulur. Doğrudan denetim
yok, ama yer adını **odak konumuna sokmamak** riski azaltıyor (bkz. 1.2).

### 1.2 Cümle vurgusu yüklemden önceki ögededir

Türkçenin en güçlü prozodi kuralı ve **yazarken kullanılabilen tek kaldıraç**:

> Fiil cümlesinde vurgulanan öge, **yüklemden bir önce gelen** ögedir.
> İsim cümlesinde vurgu yüklemin kendisindedir.

Yani vurguyu kelime seçerek değil **dizilişle** yönetiyorsun. Neyi
vurgulamak istiyorsan fiile yaklaştır:

> "Cam yüzeyleri **geniş** tutmuşlar."  → geniş vurgulanır
> "**Cam yüzeylerini** geniş tutmuşlar." → cam vurgulanır

Bu, TTS'e verdiğin en net prozodi talimatıdır ve hiçbir etiket gerektirmez.

### 1.3 Cümle sonunda alçalır, virgülde yükselir

Türkçe bildirme cümlesi **düşen** konturla biter. Cümle içi virgülde ise ton
**yükselir ya da asılı kalır** — bu devam konturudur ve doğrudur.

TTS bunu iki yönde de bozabiliyor:
- Cümle sonu yükselirse → soru soruyormuş gibi, yabancı.
- Virgülde düşerse → cümle parçalanmış, telgraf gibi.

Ölçüm ikisini ayrı ayrı bakar (bkz. 2).

## 2. Ölçüm: kulak yerine sayı

`scripts/soz_olcum.py` üç şeyi ölçer:

```bash
python3 scripts/soz_olcum.py --ses vo.mp3 --metin "Yazdığım cümle."
```

**ASR geri-dönüşü.** ElevenLabs Scribe sesi yazıya çevirir, kaynakla
karşılaştırılır, kelime hata oranı çıkar. Telaffuz felaketlerini yakalar.
Sayılar iki tarafta da yazıya çevrilerek karşılaştırılır (ASR "kırk" → "40"
yazıyor, bu fark hata sayılmamalı).

**Kontur.** F0 izi otokorelasyonla çıkarılır. **Kaynak metnin noktalaması ASR
kelime zaman damgalarına hizalanır**, böylece cümle sonu ile cümle içi virgül
ayrı ayrı ölçülür. Bu hizalama olmadan araç, virgüldeki doğru yükselişleri
hata sayıyordu.

**Hız.** İki ayrı sayı: *konuşma hızı* (duraklar dahil, doğal 4–6 hece/sn) ve
*boğumlama hızı* (duraklar hariç, doğal 5–7). İkisini karıştırmak yanıltıyor —
ilk turda boğumlama hızını konuşma hızı ölçütüyle karşılaştırıp yanlışlıkla
"çok hızlı" teşhisi koydum.

## 3. Ölçülmüş ayarlar — kazanan üçlü

Aynı Türkçe cümle, altı ayar. Ses: **Elif** (kütüphanedeki tek Türkçe adlı ses).

| Ayar | Kelime hatası | Cümle sonu düşüşü | F0 aralığı |
|---|---|---|---|
| **v3 · hız 0,88 · kararlılık 0,50** | **%2–4** | **%100** | **10,3–10,5 yarıton** |
| v3 · hız 0,84 | %2 | %83 | 10,6 |
| v3 · hız 0,78 | %4 | %83 | 11,5 |
| v2 · hız 0,88 | %11 | %67 | 8,4 |
| v2 · hız 0,88 · **kararlılık 0,75** | %8 | **%0** | 7,6 |
| v2 · hız 0,82 | %8 | %0 | 8,4 |

**Üç bulgu:**

1. **`eleven_v3`, `eleven_multilingual_v2`'yi açık ara geçiyor.** Aynı metinde
   kelime hatası %11 → %4, düşen kontur %67 → %100.
2. **Yüksek kararlılık düşen konturu kırıyor.** 0,75'te eğim **+20,3
   yarıton/sn** — cümle yükselerek bitiyor. Kararlılık 0,50'de kalmalı.
3. **Yavaşlatmak her zaman iyi değil.** 0,84 ve 0,78'de birer cümlenin konturu
   bozuldu. 0,88 tatlı nokta.

Bu üçlü `vo.py`'nin varsayılanı: `eleven_v3 · 0,88 · 0,50 · stil 0,15`.

## 4. Ölçümden çıkan yazım kuralları

Bunlar teoriden değil, **kalan denemelerden** çıktı.

**Sıralı yan cümleyle bitirme.** Ölçülen: *"Bir eve girince insan önce ışığına
bakar, sonra pencereye yürür."* cümlesi **yükselerek** bitti (+15,7). Model
"sonra …" öbeğini devam sayıyor. İkiye bölününce düşüşe döndü (−13,5).

> ✗ "… önce ışığına bakar, sonra pencereye yürür."   → +15,7 (yükseliyor)
> ✓ "… önce ışığına bakar."                           → −13,5 (düşüyor)

**Açık liste ögesiyle bitirme.** Ölçülen: *"Burada altı ayrı plan var, en
küçüğü kırk metrekare."* cümlesi **+21,4** ile yükselerek bitti — model
"en büyüğü de …" devamını bekliyor. Cümleyi kapat, listeyi ayrı cümlede ver.

**"diye" ile bitirme.** *"…akşam da geç çekilsin diye."* → **+1,2**, düz kaldı.
`diye`, `için`, `rağmen` gibi bağlayıcılar doğal olarak devam konturu alıyor.
Yükleme çevir: *"…içeride kalsın istemişler."* → **−33,3**.

**Üç öbekli zincirle bitirme.** Ölçülen: *"Sabah camdan girer, gün boyu içeride
kalır, akşam geç çekilir."* → **+19,1** yükseldi. Model üç öbeği liste sayıp
devam konturunu sürdürüyor. İkiye indirince düştü (**−6,9**).

**Kısa geniş zaman cümlesi yükselebiliyor.** *"Ay taşı ışığını içinden verir."*
→ **+9,4**. `-dır` koşacıyla kapatınca oturdu: *"…adı ay taşıdır."* → düşen.

**Bileşik kelimeyi bölünecek yerde kullanma.** *"metrekaresi"* → ASR
*"metre karesi"* olarak döndü, yani TTS araya sınır koyuyor. Ayrı ve yalın
kullan: *"kırk metrekare"*.

**Sayı ve birim yazıyla.** `96,54 m²` sese hiç girmez. Ses yuvarlar
("doksan altı metrekare"), tam değer ekranda durur.

**Odaklanacak ögeyi fiile yaklaştır** (1.2). Vurgu talimatı budur.

**Virgül nefes yeridir, gerçekten kullan.** Ölçülen çıktılarda 9–13 doğal
duraklama, sessizlik oranı %25–30 — bu aralık akıcı duyuluyor. Virgülsüz uzun
cümle hem TTS'i hem dinleyiciyi boğuyor.

## 4b. Tek düze tondan kurtulmak — parçalı sentez

Tek çağrıda üretilen seslendirmede bütün cümleler aynı perdede kalıyor.
Ölçüldü: kapanış cümlesi *"Tuzla Aydıntepe'de, Ayhanlar Mimarlık imzasıyla"*
**222 Hz, 5,7 hece/sn, öncesinde 0,40 sn boşluk** — ortadaki cümlelerle birebir
aynı. Hiçbir şey onu ayırmıyordu.

**Çözüm: metni parçalara böl, her parçaya ayrı ayar ver, sonra birleştir.**

```bash
python3 scripts/vo.py --senaryo senaryo.json --out vo.mp3 --denetle
```

```json
{ "ses":"elif", "hiz":0.90, "stil":0.15, "kararlilik":0.50,
  "parcalar":[
    {"metin":"Bir eve girince insan önce ışığına bakar.",
     "etiket":"[curious]", "hiz":0.94, "stil":0.28, "kararlilik":0.46},
    {"metin":"Planlar kırk metrekareden doksan altıya kadar gidiyor.",
     "hiz":0.86, "stil":0.10, "kararlilik":0.56, "onceki_bosluk":0.28},
    {"metin":"Tuzla Aydıntepe'de, Ayhanlar Mimarlık imzasıyla.",
     "etiket":"[slowly][emphasizes]", "hiz":0.74, "stil":0.42,
     "kararlilik":0.40, "onceki_bosluk":0.85, "kazanc":2.0}
  ]}
```

**Ölçülen etki:** ton çeşitliliği **1,5 → 3,2 yarıton**, cümleler 205–246 Hz
arasında geziniyor, kapanış 1,04 sn boşluktan sonra +2 dB ile geliyor.

### v3 ses etiketleri Türkçede çalışıyor

Ölçüldü: `[warmly]`, `[slowly]`, `[emphasizes]`, `[curious]` **sesli
okunmuyor** — ASR üçünde de temiz Türkçe metin döndürdü. Yalnızca teslimatı
değiştiriyorlar:

| Metin | F0 | Aralık |
|---|---|---|
| düz | 225 Hz | 10,0 yarıton |
| `[warmly]` | 246 Hz | 10,7 |
| `[slowly][emphasizes]` | 242 Hz | 11,2 |

### Vurgu nasıl kurulur

Perde kaydırarak değil, **dört kaldıraçla birlikte**:

1. **Öncesine boşluk** — 0,8–1,1 sn. En güçlü tek araç.
2. **Yavaşlat** — `hiz` 0,74–0,78.
3. **Etiket** — `[slowly][emphasizes]`.
4. **Seviye** — `kazanc: 2.0` (dB). Miksajda müzik zaten yan zincirle geriliyor.

**Perde kaydırma denenmedi, bilerek.** Bu ffmpeg'de `rubberband` yok; `asetrate`
ile perde kaydırmak formantları da kaydırıyor ve ses metalikleşiyor.

### Bir parçaya rol ver

Beş cümlelik bir seslendirmede işe yarayan şekil:

| Parça | Rol | Ayar |
|---|---|---|
| 1 | Açılış, merak | `hiz` 0,92–0,94 · `stil` 0,26 · `[warmly]`/`[curious]` |
| 2 | Anlatım | varsayılan |
| 3 | Veri | `hiz` 0,85 · `stil` 0,08 · `kararlilik` 0,56 (sakin, net) |
| 4 | Bağlama | varsayılan |
| 5 | Marka, kapanış | `hiz` 0,74 · `stil` 0,42 · boşluk 0,85 · `kazanc` 2,0 · etiket |

## 5. Eşikler ve denetim kapısı

```bash
python3 scripts/vo.py --out vo.mp3 --denetle --text "…"
```

Üretir, ölçer, geçer/kalır der ve kalırsa **nedenini ve çözümünü** yazar.

| Ölçüt | Eşik | Kalırsa ne yapılır |
|---|---|---|
| Kelime hata oranı | ≤ %8 | Sayıları yazıya çevir, bileşikleri ayır |
| Cümle sonu düşüşü | ≥ %80 | Yükselerek biten cümleyi böl, sıralı yan cümleyle bitirme |
| Konuşma hızı | 4,0–6,2 hece/sn | `--speed` ayarla |
| F0 aralığı | ≥ 7 yarıton | `--stability` düşür (0,75 konturu kırıyor) |
| Ton çeşitliliği | ≥ 2,5 yarıton | `--senaryo` ile parçala, vurgulu cümleye etiket + kazanç + boşluk ver |

**Duymadan onaylama.** Kapı felaketleri ve kontur hatalarını yakalar; ses
tonunun markaya uyup uymadığını yakalamaz. O karar insanın.

## 5b. Kapının kendi kusuru: özel adlar

ASR marka adlarını kendi yazım alışkanlığıyla döküyor: *Moonstone* →
*"Moon Stone"*, *ay taşı* → *"Aytaşı"*. Bunlar **telaffuz hatası değil**, ama
kelime hata oranını şişirip kapıyı yanlış yere kapatıyordu — bir metin
yalnızca marka adı yüzünden %8 hatayla kaldı.

`soz_olcum.py` artık karşılaştırmadan önce her iki tarafı normalleştiriyor
(`OZEL_AD` listesi). Yeni bir özel ad eklendiğinde o listeye de yazılmalı,
yoksa kapı gerçek olmayan bir hata gösterir.

Ders: **ölçüm aracının kendisi de yanlış alarm verebilir.** Kapı bir cümleyi
reddettiğinde önce ASR çıktısına bak, sonra metni değiştir.

## 6. Aracın sınırları

- **F0 kestirimi otokorelasyonla.** Mutlak doğruluk değil, eğilim ölçer. İki
  seçeneği karşılaştırmaya yarar, mutlak hakem değildir.
- **ASR sayıları normalize ediyor.** Karşılaştırma her iki tarafı yazıya
  çevirerek yapılıyor ama tam değil; %2–5 arası fark gürültü olabilir.
- **Sözcük vurgusunu ölçmüyor.** Yalnızca cümle konturu ve kelime doğruluğu
  ölçülüyor. "TUZla" mı "tuzLA" mı denildiğini araç bilmiyor.
- **Örneklem küçük.** Tablodaki her satır tek bir metnin tek üretimi. Eğilim
  güçlü ama her rakam ±birkaç puan oynayabilir.
