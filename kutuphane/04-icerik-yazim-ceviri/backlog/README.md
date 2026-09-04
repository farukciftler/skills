# ComeSyria — İçerik Backlog ve Web Araştırma Sistemi

Bu dizin, **ComeSyria** (`comesyria.com`) platformunun tüm yayınlanmış, kuyrukta bekleyen ve web araştırmalarıyla keşfedilen yeni içerik adaylarını **Excel / CSV / JSON** formatında senkronize olarak yöneten master backlog sistemidir.

---

## 🎯 Temel Amaç ve Doktrin

1. **Siteyle Canlı Senkronizasyon:** `content/` altındaki tüm şehir (`city`), mekan (`place`), yeme-içme (`food`) ve rota (`route`) kayıtlarını tarayarak neyin **YAYINDA**, neyin `kuyruk.json`'da **KUYRUKTA**, neyin **ARAŞTIRILACAK ADAY** olduğunu tek tabloda güncel tutar.
2. **%100 Alkolsüz & Kültürel Miras Filtresi:** Sitenin editoryal ilkeleri gereği tüm yeme-içme mekanları alkolsüz, geleneksel, aileye uygun ve kültürel kökeni olan yerlerden seçilir. Menüsünde alkol, bar veya şüpheli durum olan adaylar anında elenir (`REDDEDİLDİ`).
3. **Excel ve E-Tablo Uyumluluğu:** `comesyria_backlog.csv` dosyası **UTF-8 with BOM** formatında üretilir; Microsoft Excel, Google Sheets ve Apple Numbers'ta Türkçe (`ç, ğ, ı, ö, ş, ü`) ve Arapça karakterler bozulmadan açılır.

---

## 📊 Backlog Tablo Şeması (Sütunlar)

| Sütun | Açıklama | Değer Örnekleri |
| :--- | :--- | :--- |
| `ID` | Benzersiz slug / kimlik | `emevi-camii`, `bosra-roma-tiyatrosu`, `hama-su-dolaplari` |
| `Kategori` | İçerik tipi | `city` (Şehir), `place` (Mekan), `food` (Yeme-İçme), `route` (Rota) |
| `Şehir` | Bağlı olduğu şehir | `Şam`, `Halep`, `Humus`, `Lazkiye`, `Hama`, `Tedmür`, `Bosra`, `Tartus` |
| `Türkçe Adı` | Türkçe başlık | `Emevî Camii`, `Bakdaş Dondurmacısı`, `Hama Su Dolapları (Noria)` |
| `İngilizce Adı` | Global İngilizce adı | `Umayyad Mosque`, `Bakdash Ice Cream`, `Norias of Hama` |
| `Arapça Adı` | Özgün Arapça adı | `الجامع الأموي`, `بوظة بكداش`, `نواعير حماة` |
| `Alt Tür` | Mekanın detay türü | `Cami`, `Kale`, `Antik Kent`, `Tatlıcı`, `Booza`, `Çarşı Rota`, `Manastır` |
| `Durum` | Güncel yayın durumu | `YAYINDA`, `KUYRUKTA`, `ARAŞTIRILACAK`, `YAYINLANABİLİR`, `REDDEDİLDİ` |
| `Alkol Durumu` | Alkol filtresi | `Alkolsüz (Doğrulandı)`, `Alkol Var (Elendi)`, `Kontrol Edilecek` |
| `Öncelik` | Üretim sırası | `P0 - Acil (Ölü Hub Çözücü)`, `P1 - Yüksek`, `P2 - Orta`, `P3 - Düşük` |
| `Sitedeki Slug` | `content/` içindeki dosya | `emevi-camii.json`, `bakdas-dondurmacisi.json` |
| `Kaynak ve Notlar` | Doğrulama & web notu | `Hamidiye Çarşısı ortası, 1885, dövme booza, nakit ödeme` |
| `Son Güncelleme` | Güncellenme tarihi | `2026-08-20` |

---

## 🚦 Durum Yaşam Döngüsü (Workflow)

```
[WEB ARAŞTIRMASI & KEŞİF]
           │
           ▼
    [ARAŞTIRILACAK]  ──(Alkol / Turist Tuzağı / Doğrulanamadı)──▶ [REDDEDİLDİ]
           │
     (Doğrulandı: Saat, Ücret, Koordinat, Somut Bilgi)
           ▼
      [KUYRUKTA]     (content/kuyruk.json dosyasına yazılır)
           │
     (icerik-uret ile TR/EN/AR üretildi ve yayına alındı)
           ▼
       [YAYINDA]     (content/places/*.json vb. dosya oluştu)
```

---

## 🛠️ Otomasyon ve CLI Komutları

```bash
# 1. Mevcut site içeriklerini ve kuyruğu tarayıp backlog tablosunu güncelle:
node backlog/scripts/sync-inventory.mjs

# 2. Web'den yeni aday araştırması yap (Şehir veya kategori bazlı):
node backlog/scripts/search-candidates.mjs --sehir hama
node backlog/scripts/search-candidates.mjs --kategori food --alkolsuz

# 3. Excel uyumlu CSV ve istatistik raporu üret:
node backlog/scripts/export-excel.mjs
```

---

## 📁 Dizin Mimarisi

```
backlog/
├── README.md                  # Bu belge — Sistem ve kurallar
├── SKILL.md                   # Web araştırma ve backlog yönetim becerisi
├── comesyria_backlog.csv      # Excel uyumlu (UTF-8 BOM) ana veritabanı
├── comesyria_backlog.json     # Makinece okunabilir JSON veri tabanı
└── scripts/
    ├── sync-inventory.mjs     # Site dosyalarıyla backlog'u senkronize eden script
    ├── search-candidates.mjs  # Web kaynaklarını tarayıp aday çıkaran araç
    └── export-excel.mjs       # CSV/JSON dışa aktaran ve özet rapor basan araç
```
