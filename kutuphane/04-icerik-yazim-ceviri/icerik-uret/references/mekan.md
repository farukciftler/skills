# Mekan sayfası

**Rolü: spoke.** Tek bir yer — cami, kale, çarşı, müze, han. Sitenin en çok
trafik alan ve en çok alıntılanan tipi, çünkü sorular en somut burada.

## Arama niyeti

Mekan sorguları **kararı verilmiş** okurdan geliyor: gitmeye niyetli, pratik
bilgi arıyor. Bu tip, sitenin AEO tarafının bel kemiği.

| Dil | Tipik sorgular |
| --- | --- |
| tr | `halep kalesi giriş ücreti` · `emevi camii ziyaret saatleri` · `hamidiye çarşısı nerede` · `... gezilir mi` |
| en | `aleppo citadel opening hours` · `umayyad mosque entry fee` · `how long to visit ...` |
| ar | `قلعة حلب أوقات الزيارة` · `رسوم دخول الجامع الأموي` · `كيف أصل إلى ...` |

Dikkat: bu sorguların neredeyse hepsinin cevabı **künye alanlarında**, gövdede
değil. `entry_fee`, `opening_hours`, `duration`, `best_time` doldurulmadan bu
tip işini yapmıyor.

## İskelet

```
<p>  Giriş: yerin ne olduğunu ve neden gitmeye değdiğini bir paragrafta.
     Tarihi burada başlatma — okur önce "ne bu" cevabını istiyor.

<h2> Nasıl gidilir          ← hangi kapıdan, hangi çarşıdan, yürüme mesafesi
<h2> Ne kadar sürer         ← gerçekçi süre, kalabalık saatler
<h2> Ne görülür             ← içeride sırayla ne var
<h2> Neyi kaçırma           ← çoğu ziyaretçinin görmeden geçtiği tek şey
```

`Neyi kaçırma` bölümü bu tipin imzası. Tek bir somut ayrıntı — "tiyatronun
arkasındaki Palmira yazıtları", "Hazine Kubbesi avlunun batısında" — sayfayı
kopyala-yapıştır rehberlerden ayıran şey o.

Kısa mekanlarda (küçük bir çarşı, tek bir kapı) H2 zorlamaya gerek yok; tek
paragraf + dolu künye ızgarası yeterli ve dürüst.

## Alanlar

| Alan | Not |
| --- | --- |
| `subtitle` | `Şehir · dönem` künyesi: "Şam · 8. yüzyıl", "Halep · 12. yüzyıl". |
| `city` | **Zorunlu.** Bağlanmazsa mekan hiçbir şehir sayfasında görünmez. |
| `lat` / `lng` | Dört ondalık. `GeoCoordinates` bunlardan çıkıyor. |
| `address` | "Eski Şehir, Şam" düzeyinde yeterli; sokak numarası gerekmiyor. |
| `google_place_id` | `ChIJ…`. Harita ve yol tarifi bağlantıları bundan üretiliyor. Boşsa koordinata düşülür. Alınışı: `google.md`. |
| `period` | "Emevî", "Eyyûbî", "Osmanlı", "Haçlı — Memlûk". |
| `opening_hours` | Somut: `09:00–17:00, pazartesi kapalı`. Bilinmiyorsa "Gün doğumundan gün batımına" gibi dürüst bir aralık. |
| `entry_fee` | **Somut yaz.** "1500 SYP", "Ücretsiz". Bilinmiyorsa "Değişken — girişte teyit et" — uydurma. |
| `duration` | Dakika. Gerçekçi ol: acele değil, oyalanma da değil. |
| `best_time` | Sebebiyle birlikte: "Öğleden sonra, ışık huzmeleri için". |
| `tips` | 2–4 madde. Her biri **eyleme dönük** olmalı, övgü değil. |

### `tips` nasıl yazılır

Bu alan sayfanın en çok paylaşılan parçası. Kural: her madde okurun
**davranışını değiştirsin.**

> ✗ Kale çok etkileyici, mutlaka görülmeli
> ✓ Rampa taş ve dik; kaygan tabanlı ayakkabı zorlar
> ✓ Güneybatı kulesine çık: açık havada Akdeniz görünüyor
> ✓ Hazine Kubbesi avlunun batısında, çoğu ziyaretçi kaçırıyor

## Google yorumlarını tara — bu tipin ayırt edici adımı

Resmî kaynakta olmayan bilgi burada: kapının gerçekte kaçta açıldığı, hangi
girişin kullanıldığı, kalabalığın ne zaman bastığı, nakit mi kart mı.

**Yorum metni kopyalanmaz** — Google şartları saklamayı kısıtlıyor ve zaten
kopyalanan yorum arama motoruna yeni bir şey vermiyor. On yorumdan çıkan ortak
örüntü kendi cümlemizle yazılır. Doğrulama eşiği: aynı şeyi söyleyen **üç
yorum**. Tam yöntem ve dil dil ne aranacağı: `google.md`.

## Fiyat ve saat: en kritik nokta

Bu iki alan hem zengin sonuç kartını hem yapay zekâ alıntısını üretiyor, hem de
**en hızlı eskiyen** bilgi.

- Bilmiyorsan **uydurma.** "Değişken — girişte teyit et" dürüst ve
  kullanılabilir; yanlış fiyat siteye olan güveni tek seferde bitiriyor.
- Para birimi ve sayı üç dilde **aynen** kalır: `1500 SYP` her dilde 1500.
  Yalnızca çevresindeki kelime çevrilir ("pazartesi kapalı" → "closed Mondays").
- Dolar karşılığı yazma — kur oynuyor, metin bayatlıyor.

## Üç dilde

- Ad sözlüğüne uy: Emevî Camii / the Umayyad Mosque / الجامع الأموي.
- İngilizcede yapı adlarının önündeki `the` yerleşik kullanıma göre değişiyor
  (*the Umayyad Mosque* ama *Bab Sharqi*) — sözlükte işaretli.
- Dönem adları İngilizce okur için **bir yan cümle** açıklama ister
  (Ayyubid, Mamluk); Türk ve Arap okur bunları biliyor.
- `tips` maddeleri çevrilir ama **madde sayısı korunur.**
