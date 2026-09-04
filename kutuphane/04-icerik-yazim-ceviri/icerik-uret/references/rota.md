# Rota sayfası

**Rolü: spoke, ama diğerlerinden farklı bir ritimde.** Şehir ve mekan sayfaları
betimler; rota **sıralı ve kararlı** ilerler. Okur burada bir plan istiyor, bir
anlatı değil.

Cümleler kısalır, emir kipine yaklaşır ama düşmez: "Sabah sekizde çık",
"Bab Şarki'den gir, batıya yürü".

## Arama niyeti

Rota sorgularının belirleyici özelliği **zaman kalıbı**. Okur süreyi baştan
söylüyor ve içeriği ona göre arıyor.

| Dil | Tipik sorgular |
| --- | --- |
| tr | `şam 1 günlük gezi programı` · `lazkiye'den krak'a nasıl gidilir` · `3 günlük suriye rotası` |
| en | `1 day in Damascus itinerary` · `Latakia to Krak des Chevaliers drive` · `3-day Syria itinerary` |
| ar | `برنامج يوم واحد في دمشق` · `كيف أصل من اللاذقية إلى قلعة الحصن` |

Sonuç: **süre başlığa ya da üst başlığa girer.** "Eski Şam'da bir gün",
"Sahilden kaleye" + `subtitle: Araçla · 1 gün`. Süreyi gizleyen bir rota
başlığı bu sorguların hiçbirini yakalamıyor.

Yaygın kalıplar: yarım gün, 1 gün, 3 gün, 7 gün. 3 ve 7 en çok aranan ikisi.

## İskelet

```
<p>  Giriş: rotanın vaadi tek paragrafta. Ne göreceksin, neyle gideceksin,
     ne kadar sürüyor. "Suriye'nin en keskin manzara değişimini bir günde
     görmenin yolu bu: sabah Akdeniz, öğleden sonra dağda bir kale."

<h2> Yol            ← güzergâh sırayla, dönülecek yerler
<h2> Zamanlama      ← saat saat: ne zaman çık, nereye ne zaman var, neden
<h2> Dikkat         ← yol koşulu, dönüş, mevsim uyarısı
```

`Zamanlama` bölümü rotanın en değerli parçası ve çoğu rehberde yok. Saat ver:
"Sabah sekizde çık. Kaleye öğleden sonra varmak iyi: iç avlu gölgeye giriyor."

Duraklar gövdeye yazılmaz — `stops` alanına girer, ön yüz numaralı ve çizgiyle
bağlı listeyi kendisi çiziyor.

## Alanlar

| Alan | Not |
| --- | --- |
| `subtitle` | **Araç + süre** künyesi: "Yürüyerek · 4 saat", "Araçla · 1 gün". Sorgunun yakaladığı yer burası. |
| `city` | Başlangıç şehri. Rotanın hangi şehir sayfasında görüneceğini bu belirliyor. |
| `duration` | Saat. Kapıdan kapıya, molalar dâhil. |
| `distance` | Km, bir ondalık. Yürüyüşte de doldur: `3.2`. |
| `difficulty` | `easy` · `moderate` · `hard`. Ön yüz bunu dile çeviriyor. |
| `best_season` | Ay adıyla: "Nisan–Haziran, Eylül–Ekim". |
| `stops` | **Zorunlu.** Sıralı mekan + not. Boşsa rota sayfası iskeletsiz kalıyor. |

### `stops` notları

Her durak notu **bir sonraki adımı** söyler, mekanı tanıtmaz — mekanın kendi
sayfası zaten var ve ön yüz ona bağlanıyor.

> ✗ Emevî Camii 715'te tamamlanmış önemli bir yapıdır
> ✓ Çarşı seni doğrudan caminin batı kapısına bırakıyor
> ✓ Dağ yolunun sonunda, son virajda birden görünüyor

En fazla sekiz durak. Daha fazlası rota değil, günlük plan — ikiye böl.

### Yürüyüşte iki durak arası en fazla 1 km

`mode: walking` ise ardışık iki durak arası **yürünen** mesafe 1 km'yi geçmez.

Sebep sayfanın kendi vaadi: yürüyüş rotası okura "bunu yürüyerek yap" diyor.
Bacak uzadıkça vaat zayıflıyor, üstelik aradaki boşlukta durak notunun
anlatacağı bir şey kalmıyor — not "bir sonraki adımı söyler" ve o adım
yirmi dakikalık boş bir yürüyüşse söylenecek adım yok demektir.

Ölçü **kuş uçuşu değil yürünen mesafe**. İkisi eski şehir dokusunda ciddi
biçimde ayrışıyor; ölçülen sapma 1 km dolayında 1.16–1.35 kat (Bab Şarkî →
Azm Sarayı kuş uçuşu 1.01 km, yürüyerek 1.17 km). Gerçek mesafe:

```bash
curl -s -G https://valhalla1.openstreetmap.de/route \
  --data-urlencode 'json={"locations":[{"lat":33.5117,"lon":36.3178},{"lat":33.5106,"lon":36.307}],"costing":"pedestrian","directions_options":{"units":"kilometers"}}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["trip"]["summary"]["length"], "km")'
```

Bacak uzunsa çözüm **araya gerçek bir durak koymak**, mesafeyi küçük yazmak
değil. Araya koyacak mekan yoksa o mekan önce üretilir — yani rota beklemeye
geçer. `envanter.mjs` bunu P2 olarak açıyor; ağa çıkmadığı için orada kuş
uçuşu 0.75 km eşiğiyle *fazladan* uyarıyor, son sözü yukarıdaki ölçüm söylüyor.

## Sıra bağımlılığı

Rota, duraklarına `stops` ile bağlanıyor ve duraklar **mekan kaydı** olmak
zorunda. Yani:

```
şehir  →  mekanlar  →  rota
```

Bir rotayı, durakları henüz yayımlanmamışken yayımlarsan durak listesi boş
çıkıyor. `yayimla.php` bunu uyarı olarak bildiriyor ama önlemek daha ucuz.

## Üç dilde

- Süre ve mesafe **sayı olarak aynı** kalır; yalnızca birim kelimesi çevrilir.
- `subtitle` yeniden yazılır: "Araçla · 1 gün" → "By car · 1 day" →
  "بالسيارة · يوم واحد". Rakam Latin kalır (Arapçada da).
- Durak notları çevrilir, **sıra ve sayı korunur.**
- İngilizce başlıkta iki nokta üstü kalıbı iyi çalışıyor: *"From the coast to
  the castle: Latakia to Krak des Chevaliers"* — hem imge hem sorgu.
