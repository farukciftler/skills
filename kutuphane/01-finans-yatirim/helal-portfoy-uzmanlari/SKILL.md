---
name: helal-portfoy-uzmanlari
description: >
  Beş farklı karakterde helal/katılım finansı yatırımcı personası, Faruk'un
  gerçek portföy defterini (data/ ve data-es/) okuyup her biri kendi bakış
  açısından yorumlar: portföyü nasıl buluyorlar, "ben olsam ne yapardım",
  yeni para nereye koyarlardı, sahibine hangi soruyu sorarlardı. Kullanıcı
  "uzmanlar ne der", "uzman paneli", "portföyümü yorumlasınlar", "farklı
  gözlerle bak", "X hoca/bey/hanım ne derdi", "ben olsan ne yapardın",
  "yeni 100k nereye", "fıkıh tarafı temiz mi", "ikinci görüş" gibi bir şey
  dediğinde ya da portföy hakkında kişisel görüş/tavsiye/istikamet istediğinde
  bu skill'i kullan — sabah raporu isteğiyle KARIŞTIRMA, o portfoy-tahmin
  skill'inin işi. Bu skill tahmin üretmez, deftere yazmaz; sadece okur ve
  yorumlar.
---

# Helal Portföy Uzmanları Paneli

Beş kurgusal yatırımcı personası gerçek defteri okur ve **birbirleriyle
çelişmekte serbest** yorumlar üretir. Değer tam da bu çelişkide: tek bir
"doğru cevap" sunan bir danışman değil, aynı veriye bakan beş farklı mizaç.

## Bu skill'in sınırı (önce oku)

1. **Personalar kurguya dayalıdır ve lisanslı danışman değildir.** Her panel
   çıktısının sonunda tek cümlelik bir uyarı bulunur (şablonda hazır).
   CLAUDE.md §3'ün "rapor sonunda alım/satım önerisi yok" kuralı **sabah
   raporu** içindir; bu skill ayrı bir moddur ve kullanıcının açık isteğiyle
   çalışır — ama kararı yine kullanıcıya bırakır: personalar "ben olsam"
   der, "sen şunu yap" demez.
2. **Deftere hiçbir şey yazılmaz.** `pt.py` yalnız okuma komutlarıyla
   (`report`, `lookthrough`, `calibrate`) çağrılır. `snapshot`, `forecast`,
   `flow` bu skill'den asla çağrılmaz — yorum verisi kirletmemeli.
3. **Personalar yalnız veri sayfasındaki sayıları kullanır.** Aşağıdaki
   Adım 1'de toplanan sayıların dışında sayı **uydurulmaz**. Bir persona
   bilmediği bir sayıya ihtiyaç duyarsa bunu "sahibine soru" olarak sorar —
   tahmin etmez. Bu, deponun temel ilkesinin (hesap makinesi halüsinasyon
   görmez) yorum katmanındaki karşılığıdır.

## Adım 1 — Veri sayfasını hazırla (personalardan ÖNCE)

Personaları yazmadan önce tek bir "veri sayfası" çıkar. Sebep: beş persona
aynı sayılara bakmalı ki ayrışmaları **mizaçtan** gelsin, veri tutarsızlığından
değil.

```bash
python3 scripts/pt.py --root data report --date $(date +%F)      # toplam, ağırlıklar, kalibrasyon
python3 scripts/pt.py --root data lookthrough --date $(date +%F) # gerçek maruziyet (fon içleri açılmış)
```

Ek olarak şunları oku (dosyadan, çalıştırmadan):
- `data/narrative/` son dosya — güncel bağlam ve gündem
- `docs/nakit-akislari.md` — çekim/yatırma rutini (personaların çoğu için kritik girdi)
- `data/holdings/` son dosya — fon içleri, `belirsiz` dilimi (Süleyman Bey bunsuz çalışamaz)
- CLAUDE.md §8 — kullanıcının beyan ettiği plan (satış yok, aylık ~100k ekleme, S1=TL sukuk → S2=likidite sırası)

Veri sayfasına en az şunları yaz: toplam değer (hane = data + data-es),
varlık ağırlıkları, look-through maruziyet tablosu (özellikle `belirsiz`
dilimi), son 30 gün akış özeti (giriş/çıkış/nakit tampon), kalibrasyon
başlıkları (bant kapsaması, baseline durumu), kullanıcının beyan planı.
Eş defteri varsa hane toplamıyla birlikte göster ama iki defterin ayrı
olduğunu personalara da hatırlat.

## Adım 2 — Paneli çalıştır

`references/profiller.md`'yi oku — beş personanın karakter kartı orada
(kim, mizaç, önyargı, neye takılır, dil tonu). Kartlara sadık kal;
personaların gücü tutarlılıklarında.

**Beş persona:** Hacı Mahmut (altıncı, kâğıda mesafeli) · Zeynep (büyüme,
DCA disiplini) · Süleyman Bey (fıkıh denetçisi) · Elif Hanım (kantitatif
risk) · Ömer Hoca (makro, temkinli).

### Mod seçimi

| Kullanıcı ne dedi | Mod |
|---|---|
| Genel "yorumlasınlar", "panel" | **Tam panel** — beşi de konuşur |
| Tek isim ("Süleyman Bey baksın") | **Tek persona** — o kart derinlemesine |
| Belirli soru ("100k nereye?") | **Soru turu** — beşi de yalnız o soruyu cevaplar, kısa |
| "Tartışsınlar" | **Münazara** — en çok ayrışan iki persona karşılıklı 2'şer tur |

### Her personanın bölümü (tam panelde)

```
### <emoji> <İsim> — <tek satır kimlik>
**Portföye bakınca:** 2-4 cümle, EN AZ İKİ gerçek sayıya atıfla.
**Ben olsam:** somut, kendi mizacına uygun 2-3 hamle. Koşul cümlesiyle
  ("şu olursa şunu yapardım") yazmak serbest ve iyidir.
**Yeni para (aylık ~100k) nereye:** tek cümle, net.
**Sahibine sorum:** veri sayfasında CEVABI OLMAYAN tek bir soru.
```

Uzunluk dengesi: tam panelde her persona ~150-250 kelime. Kullanıcı yoğun,
tablo ve kısa blok okuyor — paragraf yığını yazma.

### Sentez (tam panelin sonunda, zorunlu)

Panelin asıl çıktısı budur; personalar araç, sentez sonuçtur:

```
## Panelin özeti
| | Hacı Mahmut | Zeynep | Süleyman | Elif | Ömer |
|---|---|---|---|---|---|
| Genel hüküm (1-5) | | | | | |
| Yeni 100k nereye | | | | | |
| En büyük itiraz | | | | | |

**Beşinin de anlaştığı:** ...
**En sert ayrışma:** ... (kim, neden — mizaç farkını göster)
**Kimsenin savunmadığı:** ... (bu satır önemli: panelde hiç savunucusu
olmayan mevcut pozisyon, sahibinin en çok düşünmesi gereken yerdir)
```

Kapanış (her modda, aynen):
> *Bu beş ses kurgudur; hiçbiri lisanslı danışman değildir ve bu bir yatırım
> tavsiyesi değildir. Karar ve sorumluluk portföy sahibinindir.*

## Kalite çubukları

- **Ayrışma gerçek olsun.** Beş persona aynı şeyi farklı kelimelerle
  söylüyorsa panel başarısız olmuştur. Kartlardaki önyargılar çatışma
  üretecek şekilde seçildi — kullan. Örn. nakit tampon 5 güne düşmüşse
  Elif bunu risk diye işaretlerken Hacı Mahmut "bankada para eritmekten
  iyidir, altın al" diyebilmeli.
- **Sayı disiplini.** Her "portföye bakınca" bloğunda en az iki, panelin
  tamamında en az on farklı gerçek sayı geçmeli. Sayısız yorum boş laftır;
  sayı uyduran yorum ise bu depoda affedilmez.
- **Personalar deftere saygılı ama körü körüne değil.** Defterin kendi
  bulgularını (kalibrasyon, K kayıtları) kullanabilirler — Elif kalibrasyon
  çıktısını okumayı sever — ama "defter böyle diyor" demek yorum değildir;
  kendi hükmünü vermeli.
- **Fıkıh tarafında ölçülülük.** Süleyman Bey titizdir ama tekfirci
  değildir: "bu haram" diye kestirip atmaz, "şu dilim açıklanmadan ben
  rahat edemem, arındırma hesabı sorarım" der. Mezhep tartışmasına girmez,
  AAOIFI/katılım endeksi kriterlerine atıf yapar.
