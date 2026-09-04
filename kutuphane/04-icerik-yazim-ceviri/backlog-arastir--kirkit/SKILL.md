---
name: backlog-arastir
description: ComeSyria için internette alkolsüz, kültürel mirasa ve site kategorilerine (şehir, mekan, rota, yeme-içme) uyan içerik adaylarını araştırır, sitedeki mevcut içeriklerle (`content/`) ve kuyrukla (`kuyruk.json`) sürekli senkron tutar, Excel/CSV formatında master backlog tablosunu günceller. "backlog", "web araştır", "yeni mekan araştır", "alkolsüz mekan", "içerik listesi", "excel güncelle", "site senkronizasyonu", "aday araştır", "backlog güncelle" dendiğinde kullan.
---

# ComeSyria — Web Araştırma ve Master Backlog Becerisi

Bu beceri; internetteki güvenilir açık kaynakları (UNESCO, Wikipedia, OpenStreetMap, yerel Arapça rehberler, tarihi seyahatnameler, doğrulanmış gezgin kayıtları) tarayarak ComeSyria'ya eklenebilecek **%100 alkolsüz, kültürel değeri olan ve doğrulanabilir** yeni mekan, yeme-içme, rota ve şehir adaylarını keşfeder; site envanteriyle senkronize bir **Excel/CSV master tablosunda** yönetir.

---

## 🎯 1. TEMEL KURALLAR VE SÜZGEÇLER

### A. %100 Alkolsüzlük Kuralı (Pazarlıksız)
* **Yeme-İçme (`food`) ve Mekan (`place`) Adayları:** Menüsünde alkol, bar, gece kulübü veya "rooftop lounge" olan hiçbir yer listeye giremez.
* **Onaylanan Yerler:** Asırlık dövme dondurmacılar (Booza), geleneksel tatlıcılar (Halawet el-Jibn, Knafeh, Baklava), tarihi çay ve nargile kahvehaneleri (Hakawati geleneği), fırınlar, geleneksel lokantalar (Humus, Falafel, Fatteh, Halep kebabı).
* **Şüpheli Durum:** Alkol durumu net değilse `Alkol Durumu: Kontrol Edilecek` olarak işaretlenir ve teyit edilmeden `KUYRUKTA` aşamasına geçirilmez.

### B. Kategoriler ve Eşleme
1. **`city` (Şehir):** Şam, Halep, Humus, Lazkiye, Hama, Tedmür, Bosra, Tartus, Süveyda, Deyrizor, İdlib.
2. **`place` (Miras & Mekan):** Cami, kale, kilise, manastır, antik kent, han/kervansaray, hamam, çarşı, medrese, bimaristan, saray.
3. **`food` (Yeme-İçme):** Geleneksel tatlıcı, asırlık dondurmacı, tarihi kahve, yöresel fırın, geleneksel sofra.
4. **`route` (Rota):** Adım adım sıralı duraklar içeren yarım/tam günlük yürüyüş veya araç rotaları.

---

## 🔄 2. ENTEGRASYON VE SENKRONİZASYON AKIŞI

1. **Mevcut Envanteri Tara:**
   * `content/cities/*.json` ➔ `Durum: YAYINDA`
   * `content/places/*.json` ➔ `Durum: YAYINDA`
   * `content/food/*.json` ➔ `Durum: YAYINDA`
   * `content/routes/*.json` ➔ `Durum: YAYINDA`
   * `content/kuyruk.json` ➔ `Durum: KUYRUKTA` (Henüz yazılmamış olanlar)
2. **Web Adaylarını Karşılaştır:**
   * Keşfedilen yeni aday sitede zaten var mı? Slug veya isim kontrolü yap.
   * Varsa durumunu `YAYINDA` yap ve sitedeki dosya adını bağla.
   * Yoksa ve doğrulanabilir somut bilgisi varsa `ARAŞTIRILACAK` veya `YAYINLANABİLİR` olarak ekle.
3. **Excel / CSV Çıktısını Güncelle:**
   * `backlog/comesyria_backlog.csv` (UTF-8 BOM ile Excel uyumlu)
   * `backlog/comesyria_backlog.json`
