---
name: kultur-sanat-radari
description: Belirli bir tarih aralığında ve şehirde (İstanbul başta olmak üzere Türkiye ve yurt dışı) açık olan sergileri, bienalleri, müze programlarını, konser/sahne etkinliklerini, atölye ve söyleşileri canlı web araştırmasıyla tarar; bitiş tarihi yaklaşanları öne çıkarır, ücretsiz/indirimli günleri ve müze kart kapsamını çıkarır, semt semt gerçekçi bir hafta sonu veya akşam rotası kurar (yürüme mesafesi, kapalı günler, yemek molası dahil). Kullanıcı "bu hafta sonu ne yapsak", "hangi sergiler var", "gezilecek yer", "sergi öner", "müzeye gidelim", "konser var mı", "atölye", "bienal", "ücretsiz müze", "şu şehirdeyim ne görmeliyim", "kapanmadan yetişmem gereken sergi" dediğinde kullan. Bir seyahat planı ya da boş bir hafta sonu konuşuluyorsa kullanıcı sormasa bile kültür programını gündeme getir. Sergi tarihleri ve bilet fiyatları hızla değişir ve sergiler kapanır — ASLA ezberden program verme, her seferinde canlı ara ve kurumun kendi sayfasından doğrula.
---

# Kültür-Sanat & Program Radarı

Amaç: "önümüzdeki hafta sonu / şu tarihlerde şu şehirde ne var" sorusunu, **hâlâ açık olduğu doğrulanmış**, coğrafi olarak tutarlı ve gerçekçi zamanlanmış bir programa çevirmek.

## Temel İlkeler

1. **Kapanmış sergi önermek en büyük hatadır.** Her öneri için bitiş tarihi bulunur; bulunamazsa "tarih doğrulanamadı, kurumun sayfasından teyit et" yazılır. Eğitim verisinden sergi adı üretilmez.
2. **Kapalı gün kontrolü zorunlu.** Türkiye'de çoğu müze ve galeri **pazartesi kapalıdır**; bazı kurumlarda farklı gün. Program kurulmadan önce hedef günün kapalı günü olup olmadığı kontrol edilir.
3. **Aciliyet sırala.** "Bu ay bitiyor" olanlar listenin başına konur — asıl değer budur; sürekli koleksiyonlar her zaman görülebilir.
4. **Coğrafya mantıklı olsun.** Bir programda mekânlar yürüme veya tek toplu taşıma mesafesinde gruplanır. Beyoğlu-Karaköy, Nişantaşı-Dolapdere, Kadıköy-Moda gibi kümeler bozulmaz; boğaz karşıya geçiş varsa süresi hesaba katılır.
5. **Ücretsiz olanı kaçırma.** Bienaller, kurumsal galeriler ve belediye mekânlarının çoğu ücretsizdir; müzelerin belirli gün/saat indirimleri vardır. Bunlar açıkça etiketlenir.

## İş Akışı

### Adım 0 — Girdi
Gereken: **şehir + tarih aralığı.** Varsa: kişi sayısı, ilgi alanı (çağdaş sanat / klasik / mimari / fotoğraf / tasarım / sahne / müzik), bütçe, çocuk var mı, ne kadar süre (yarım gün / tam gün / akşam). Eksikse tek soruda topla; tarih yoksa "en yakın hafta sonu" varsayılır ve bu belirtilir.

### Adım 1 — Tarama (4-8 arama)
`references/kaynaklar.md` dosyasını oku, şehre uygun kaynakları seç. Zorunlu üç kanal:
- **a) Kurum programları:** büyük müze/kurumların güncel sergi sayfaları
- **b) Ajanda/derleme siteleri:** "[şehir] [ay] [yıl] sergiler", "güncel sergiler [şehir]"
- **c) Bilet/etkinlik platformları:** sahne, konser, festival, atölye tarafı

Her bulgu için topla: **mekân · sergi/etkinlik adı · başlangıç-bitiş tarihi · ücret · kapalı gün · semt.**

### Adım 2 — Doğrulama (2-4 arama)
Programa girecek her öğe için kurumun kendi sayfasından tarih ve saat teyidi. Derleme sitesi ile kurum sayfası çelişirse **kurum sayfası** geçerlidir. Doğrulanamayan öğe listede kalabilir ama "teyit edilmedi" etiketiyle.

### Adım 3 — Rota kur
Yarım gün için 2-3 durak, tam gün için 3-4 durak, akşam için 1 etkinlik + 1 yeme-içme. Her durak arası ulaşım süresi yazılır. Aralara yemek/kahve molası konur; istenirse `places_search` ile yakın mekân önerilir ve `places_map_display_v0` ile harita gösterilir.

### Adım 4 — Pratik notlar
- Bilet önceden alınmalı mı, kapıda sıra olur mu?
- Müzekart / öğrenci / 65 yaş indirimleri kapsamda mı?
- Rezervasyon zorunlu turlar (ücretsiz rehberli turlar dahil) var mı?
- Fotoğraf çekimi serbest mi (sergiye göre değişir)?
- Yoğunluk: hafta içi öğleden önce en sakin; ücretsiz günlerde kalabalık.

### Adım 5 — Uzun vadeli takvim (istenirse)
Önümüzdeki 3-6 ayda açılacak büyük sergiler, bienal ve festival tarihleri ayrı bir kısa liste hâlinde verilir; kullanıcı isterse `reminder_create_v0` veya `event_create_v1` ile takvime eklenir. Kendiliğinden ekleme yapma, teklif et.

## Çıktı Formatı

```
## Şu an açık — kapanmak üzere olanlar
| Sergi/Etkinlik | Mekân (semt) | Bitiş | Ücret |

## Bu hafta sonu için rota
**Cumartesi**
- 11:00 — [Mekân] · [ne görülecek] · [ücret] · [~süre]
- 13:00 — yemek: [semt]
- 14:30 — [Mekân] ...

## Süresi bol olanlar / alternatifler
- ...

## Notlar
- Pazartesi kapalı olanlar: ...
- Bilet önceden: ...
```

## Sık Yapılan Hatalar
- Geçen sezonun sergisini "şu an açık" diye sunmak.
- Pazartesi programı kurmak.
- Bir günde şehrin iki ucundaki mekânları aynı programa koymak.
- Bienal/festival gibi süreli oluşumların mekân listesinin dağınık olduğunu atlamak.
- Ücretsiz sanılan kurumun bilet almaya başladığını fark etmemek.
- Son giriş saatinin kapanıştan 30-60 dk önce olduğunu hesaba katmamak.

## Sınırlar
Bilet satın alma veya rezervasyon yapmaz. Fiyat ve kontenjan bilgisi anlıktır; kesin bilgi kurumun kendi kanalıdır.
