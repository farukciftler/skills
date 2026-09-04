---
name: masifico-urun-gorsel
description: Masifico'nun ürün görseli ve satış materyali operatörü. Ahşap oyuncak fotoğraf çekimi (ışık, zemin, iPhone akışı, Etsy/Amazon kural setleri), Blender ile fotogerçekçi render (build123d GLB export, prosedürel kayın materyali, HDRI sahne şablonları, M2 Pro Cycles sabitleri, fSpy foto-harman), farklı mekan/evren sahneleri ve üretim-satış materyalleri (teknik antet, DXF teslim kuralları, lookbook + line sheet, ambalaj mockup, insert/QR, CMYK baskı) için tek kaynak. Kullanıcı "ürün görseli", "render al", "farklı ortamda göster", "Etsy fotoğrafları", "katalog", "lookbook", "kutu mockup", "sahne kur", "görsel çek", "fotoğraf planı", "hero görsel" dediğinde; yeni SKU'nun görselleri hazırlanırken; ya da üreticiye/kreşe giden görsel-belge paketi derlenirken bu skill kullanılır. Derin kaynak docs/arastirma/urun-gorsel-sahneleme-arastirma-v1.md; skill oradaki değerleri uygulama reçetesine indirir.
---

# Masifico Ürün Görseli & Satış Materyali Operatörü

Amaç: model dosyasından (STEP/STL/GLB) veya numuneden, kanala göre doğru görseli tekrarlanabilir
script'le üretmek. Kural repo geneliyle aynı: çıktı elle düzenlenmez, sahne script'i düzenlenir.
Sayısal değerlerin kaynağı `docs/arastirma/urun-gorsel-sahneleme-arastirma-v1.md` (bölüm
numaralarıyla); platform kuralları yayın öncesi canlı doğrulanır.

## 1 · Render hattı (varsayılan akış, numune gerekmez)

1. **Export:** üreteç script'e render'a özel sıkı toleranslı GLB ekle
   (`export_gltf`/STL, tolerance 0.01, angular_tolerance 0.1; üretim STL'inden ayrı dosya).
   GLB parça adlarını korur, parça başına materyal atanır; STL seti tek gövdeye yapıştırır.
2. **Sahne script'i:** tek `bpy` script'i kurar: import → Shade Auto Smooth (~30°) →
   materyal → HDRI → kamera → render. Sahne metre kalır, import scale 0.001 (SSS için şart).
3. **Materyal, doğal kayın (Reçete A):** Object koordinatlı prosedürel ahşap
   (Mapping tek eksende ez, Noise Detail 15/Rough 0,7 + silik Wave halkaları; ColorRamp
   #E9C68F↔#DDB77E dar bant; ray fleck: mini Voronoi benekleri base'e %3-5).
   Roughness 0,35-0,5 tane senkronlu, IOR 1,45, bump strength 0,2-0,4, Coat kapalı.
   End grain Object koordinatla bedava gelir; UV açılmaz, parçalar arası doku tekrarı olmaz.
4. **Materyal, boyalı (Reçete B):** Base Color = marka hex'i; ahşap tanesi Normal/Bump'ta
   KORUNUR (boyalı plastik değil boyalı ahşap okutmanın anahtarı). Mat 0,5-0,7; satine
   Coat Weight 1 + Coat Roughness 0,2-0,35. SSS kapalı.
5. **Işık:** iki hazır set: `studio_small_08` (yumuşak katalog) ve `wooden_studio_04`
   (sıcak mekân). HDRI Z rotasyonuyla softbox yansıması yüzeye oturtulur; key ışık ahşaba
   30-45° yandan (damar ancak yan ışıkta okunur). Sonsuz zemin: plane + arka kenar extrude +
   30-40 cm bevel + Shade Smooth.
6. **Kamera:** katalog 85 mm f/8 · lifestyle 50 mm f/2.8 (Focus Object = ürün/Empty) ·
   teknik kare ortografik. Blades 8-9.
7. **Render sabitleri (M2 Pro):** Metal GPU Compute, Adaptive noise threshold 0,003 final
   (0,01 taslak), Max Samples 1024, OIDN Albedo+Normal Accurate/High GPU, **AgX** view
   transform, 2048×2048. Kare başına 1-4 dk; 4K 5-15 dk. Kuyruk: `blender -b sahne.blend -o //cikti/kare_### -f 1`.
8. **Foto-harman:** gerçek masa/atölye fotoğrafı → fSpy ile kamera çöz → Blender importer →
   zemin Shadow Catcher + Film Transparent → alpha over. Renk varyantları numune beklenmeden
   gösterilir; satış kilidi metni görselden düşmez.

**Farklı evren/mekan sahneleri:** her evren = ayrı HDRI + zemin materyali + prop seti,
aynı ürün GLB'si ve aynı render sabitleri. Sahne tanımları script'te sözlük olarak durur
(evren adı → HDRI, zemin, kamera, ışık), yeni evren eklemek sözlüğe kayıt eklemektir.

## 2 · Fotoğraf kurulumu (numune geldiğinde)

- Pencere yanı sabit masa; ışık hep yandan 45°, gölge tarafına strafor. Beyaz L-sweep
  packshot, keten/koyu ahşap zemin lifestyle: tek kurulum iki dil.
- Kayın ürün kayın zemine konmaz (yutar); koyu ceviz, taş veya krem keten.
- iPhone standardı: 2x/3x tele (1x distorsiyon yapar), AE/AF Lock + pozlamayı hafif kıs,
  ProRAW, sabit beyaz dengesi, kadraja bir kez gri kart, tripod + zamanlayıcı,
  packshot'ta portre modu kapalı. Mac'te tek preset ile seri düzenleme.
- Altın saat yalnız sosyal/lansman karesine; katalog kareleri sabit yapay ışıkla.
- Prop dili: çocuk eli (yüz asla), keten, kuru dal, kendi ambalajı + bakım yağı.
  Sukulent-mermer-altın makas üçlüsü ve ürünle aynı renk prop yasak. Negatif alan bırakılır.
- Flat lay: kamera tam dik, tele, yatay kollu tripod. KB-24 = 6×4 grid; DT-10 = boy sırası yay.

## 3 · Kanal kuralları (yayın öncesi canlı doğrula)

| Kanal | Kural |
|---|---|
| Etsy | 10 foto + 1 video; kısa kenar ≥2000 px, hedef 3000×2250; thumbnail ~4:3 kırpar; video 5-15 sn sessiz. Beyaz fon zorunlu DEĞİL, sıcak lifestyle ana görsel tıklama alır |
| Amazon | Ana görsel saf beyaz (255,255,255), GERÇEK fotoğraf (render ana görselde yasak), ürün ≥%85 doluluk, ≥1600 px; min üç tip: beyaz fon + ortam + ölçek |
| Trendyol/line sheet | Beyaz fon seti, tutarlı açı seti (ön, 45°, üst, ölçek), tüm SKU aynı ışık |

Etsy 10 kare planı çekim listesi olarak kullanılır: hero, lifestyle, ölçek (avuç içi),
doku makrosu, set flat lay, ölçü infografiği, ambalaj, atölye/süreç ("İstanbul'da elde üretim"
kanıtı), varyasyon, sertifika/bakım (satış kilidi diliyle: "sertifikasyon sürecinde").

## 4 · Üretim ve satış materyalleri

- **Teknik pakete mini antet:** parça adı, SKU-dosya-vX, tarih, "genel tolerans ±0,5 mm aksi
  belirtilmedikçe", projeksiyon sembolü (first-angle), "ölçüler mm". ISO kodu (2768-c dengi)
  yalnız ihracat/fason CNC paketinde; esnafa "±0,5 mm, mastar yuvası 42,0 +0,3/-0" yazılır.
- **DXF teslim:** kapalı kontur, duplicate/overlap yok, spline'lar polyline'a patlatılmış,
  yazılar outline, katmanlar KESIM/GRAVUR/OLCU. `paket_dogrula.py`'ye spline-yok ve
  duplicate-yok kontrolleri eklenir. Teklifte "dizilimi kendin yapabilirsin" notu maliyet düşürebilir.
- **Kreş kanalı iki belge:** 12-20 sayfa lookbook (kapak → 30-50 kelime marka → editorial →
  ürün spreadleri → doku detayı → grid özet → trade sayfası) + 1-2 sayfa line sheet
  (SKU, ölçü, toptan, MSRP, MOQ, teslim, ödeme). EN 71 durumu tablo halinde İLK sayfada.
  B2B kareler: dayanıklılık, silinebilirlik, yedek parça; duygu değil.
- **Ambalaj mockup:** dieline SVG → PackCAD Mockup (tarayıcı) → 3D export → Blender'da
  AgX + studio HDRI + 85 mm hero render. f3d yalnız doğrulama önizlemesi.
- **Insert/QR:** 300-350 gsm uncoated/kraft; tissue + tek sticker; el yazısı teşekkür;
  "5 oyun fikri" kartı. QR ≥2×2 cm, 100K siyah, ECC H, quiet zone ≥8 mm, kısa yönlendirme
  URL (parti no sorgusuna bağlanır, izlenebilirlik zinciri). Kayın zeminde kontrast sınırda, baskıda test.
- **Baskı:** CMYK (FOGRA39), 300 dpi, bleed 3-5 mm, PDF/X-1a, metin/QR 100K, zemin rich black
  C60M40Y40K100, 170 gsm+ katlamada pilyaj. Kiremit ve petrol CMYK'da söner: basımdan önce
  paletin CMYK karşılıkları bir kez sabitlenir ve tek sayfa prova bastırılır.

## 5 · Zincirdeki yeri

`masifico-uretim-muhendisi` modeli üretir → **bu skill** görseli ve satış materyalini üretir →
`masifico-video-uretim` hareketli anlatıya taşır. Anlatı dili `masifico-ahsap-kultur`den,
fiyat/kanal kararı `masifico-maliyet-fiyat`tan gelir. Görsellerde satış kilidi metni
(CE süreci bitmeden "satışta değil") her zaman korunur.
