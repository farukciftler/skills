---
name: masifico-teknik-dosya
description: Masifico'nun CE teknik dosyası derleyicisi ve denetçisi — 2009/48/EC Ek IV'ün (a)-(h) sekiz kalemini klasör klasör kurar, Modül A öz-beyan gerekçesini yazar, güvenlik değerlendirmesini (Md. 18 yedi tehlike başlığı) iskeletiyle üretir, AB/AT Uygunluk Beyanını zorunlu alanlarıyla hazırlar, BOM/BOS'u ve tedarikçi belgelerini dosyaya bağlar, etiket/CE işaretleme kurallarını doğrular ve tamlık denetçisiyle eksik belge kalmadığını kanıtlar. Kullanıcı "teknik dosya", "CE dosyası", "uygunluk beyanı", "DoC", "güvenlik değerlendirmesi", "risk analizi", "Ek IV", "Modül A", "onaylanmış kuruluş", "lab raporu geldi", "etiket içeriği", "CE nereye", "yaş uyarısı", "0-3 sembolü", "AB Sorumlu Kişi", "dosyayı Bakanlığa vereceğim", "denetim geldi" dediğinde; lab raporu eline geçtiğinde; yeni SKU satışa hazırlanırken; tasarım/malzeme/tedarikçi/renk değiştiğinde; veya satış kilidi kaldırılmadan önce bu skill'i kullan. Denetçi HATA verdiği sürece CE iliştirilmez, beyan imzalanmaz, hiçbir kanalda satış açılmaz.
---

# Masifico CE Teknik Dosyası

Amaç: piyasa gözetimi kapıyı çaldığında **10 dakikada teslim edilebilecek**, Ek IV'ün harflerine birebir oturan, eksiksiz bir dosya tutmak. Dosya bir klasör değil, bir **sözleşmedir**: her belgenin kodu, üreticisi, tazelik süresi ve denetim kuralı vardır.

Zincirdeki yeri: `oyuncak-mevzuat` (neyin gerektiğini söyler) → `masifico-tedarik-rfq` (tedarikçi belgelerini toplar) → **bu skill** (dosyayı kurar ve kanıtlar) → satış kilidi kalkar.

## 0 · Beş kural

1. **Denetçi HATA verirse satış yok.** `teknik_dosya_kontrol.py` çıkış kodu 1 → CE iliştirilmez, beyan imzalanmaz. Bu, repodaki "denetçi geçmeden paket teslim edilmez" kuralının belge tarafındaki karşılığıdır.
2. **Boş klasör yasak, "UYGULANAMAZ" serbest.** Modül A izlendiği için Ek IV (f) ve (h) doludur — içinde gerekçeli `UYGULANAMAZ.md` vardır. Sessiz boşluk denetimde hatadır.
3. **Tek doğruluk kaynağı.** Standart sürümleri yalnız `ORTAK/03-STANDART/standart_listesi` içinde; belge kodları yalnız `tedarik/rfq.py::BELGELER` içinde; yaş sınıfı yalnız `kullanim_ve_yas` içinde tanımlanır. Beyan, etiket ve denetçi oradan **okur**, kopyalamaz.
4. **İki dilli tut.** TR Yön. Md. 22(2) Türkçeye izin verir, AB Md. 21(2) bir AB resmî dili ister. AB'ye satıldığı için **İngilizce sürüm zorunludur**.
5. **10 yıl sakla.** Son bireysel ürünün piyasaya arzından itibaren (Md. 4(3) / TR Md. 5(3)). Emniyet payıyla 11 yıl tut; sayaç `partiler.json`'daki `arz_tarihi`nden işler.

## 1 · Ek IV — sekiz kalem ve Masifico'daki karşılığı

| Ek IV | İçerik | Masifico'da |
|---|---|---|
| **(a)** | Tasarım ve imalatın ayrıntılı tanımı + **bileşen ve malzeme listesi** + kullanılan kimyasalların **SDS'i (tedarikçiden alınacak)** | `a-TASARIM-IMALAT/` — ürün tanımı, gerçek renkli foto, ölçü çizimi, BOM/BOS, ambalaj baskısı, TR+EN talimat, yaş gerekçesi, `sds/` |
| **(b)** | Md. 18 uyarınca yapılan **güvenlik değerlendirmesi** | `b-GUVENLIK-DEGERLENDIRMESI/` |
| **(c)** | İzlenen uygunluk değerlendirme usulünün tanımı | `c-UYGUNLUK-DEGERLENDIRME/modul_a_beyani` |
| **(d)** | AT/AB Uygunluk Beyanı kopyası | `d-UYGUNLUK-BEYANI/` (TR + EN) |
| **(e)** | **Üretim ve depolama yerlerinin adresleri** | `ORTAK/01-SIRKET/` |
| **(f)** | Onaylanmış kuruluşa sunulan belgeler | `UYGULANAMAZ.md` — Modül A |
| **(g)** | **Test raporları** + seri üretimde uygunluğun nasıl sağlandığının tanımı | `g-TEST-RAPORLARI/` |
| **(h)** | AT tip inceleme sertifikası | `UYGULANAMAZ.md` — Modül A |

**Generic file meşrudur.** Komisyon rehberi: *"Generic files are therefore permitted as long as the differences between toys and the documents unique to individual toys are held."* → `ORTAK/` gövdesi + `<SKU>/` eki = tam dosya. Ayrıca *"Information can be stored in any format and in various locations"* → git repo geçerli bir saklama biçimidir.

**Ek IV(a) açılımı (rehber §3.1) — denetçinin kontrol listesi:** ürün tanımı · **yüksek çözünürlüklü RENKLİ FOTOĞRAF** (f3d render yetmez, gerçek ürün) · imalat çizimleri · açıklamalar · **ambalajın baskı örneği** · kullanma talimatı · amaçlanan ve öngörülebilir kullanım · **yaş uygunluğu + GEREKÇESİ** · imalat sürecinin adım adım tanımı.

**BOM/BOS kuralı (rehber §3.2):** 4 seviye (bitmiş oyuncak → parçalar → malzemeler → maddeler), sütunlarda CAS no ve belge durumu. **Aynı malzemeyi iki tedarikçiden alıyorsan BOM'da iki ayrı satır** — farklı madde içerebilirler. Doğal maddede CAS yoksa `0000-00-0`. SDS gerekmeyen kaleme boş değil **"non-required"** yazılır. (MSDS ABD formatıdır; TSD **SDS** ister.)

## 2 · Güvenlik değerlendirmesi (Md. 18 / TR Md. 19)

Yedi tehlike başlığının **hepsi** ayrı ayrı ele alınır — biri eksikse denetçi HATA verir:

**kimyasal · fiziki · mekanik · elektriksel · alevlenebilirlik · hijyen · radyoaktivite**

Her başlıkta iki şey olmalı: **tehlike analizi** + **maruziyet değerlendirmesi** (dermal / oral yutma / oral emme-yalama / göz / inhalasyon). Önce worst-case varsayımı; risk çıkmazsa biter.

Kısa yazılabilecek başlıklar bile **yazılır**: "Elektrikli bileşen yok → tehlike yok" tek cümledir ama bulunmak zorundadır. Hijyen ve radyoaktivite için uyumlaştırılmış standart yoktur; yalnız yazılı değerlendirmeyle karşılanır.

**Ahşap için üç özel nokta:**
- **Ahşap doğal malzemedir** → mikrobiyolojik kontaminasyon değerlendirmesi gerekir (fırın kurutma nemi, küf riski, kuru depolama).
- **<36 ay ürünlerde temizlenebilirlik zorunlu** (Ek II Böl. V) + temizlik talimatı; *"the toy shall fulfil the safety requirements also after having been cleaned"* — yağlı yüzey nemli bezle silindikten sonra kıymık vermemeli.
- **Ahşabın tek gerçek kimyasal risk kalemi emprenye/biyosittir** (rehber Appendix III: *"Wood can contain wood preservatives which in turn can contain chrome, arsenic, copper, creosote"*). Kereste tedarikçisinden `emprenye_yok_beyani` alınır (REACH Ek-XVII md. 18/19).

**Yeniden değerlendirme tetikleyicileri:** tasarım revizyonu (yeni tehlike doğuruyorsa), hammadde/boya/katkı değişikliği, mevzuat değişikliği, tüketici şikâyeti (alerjik reaksiyon), riskten ötürü piyasadan çekme. Rehberin açık notu: **"Colour changes to toys are not considered as new innovative knowledge"** — renk değişimi tek başına yeni değerlendirme gerektirmez (ama yeni EN 71-3 kalemi doğurur, bkz. `oyuncak-mevzuat`).

## 3 · Modül A — neden onaylanmış kuruluş gerekmiyor

Md. 19(2): uyumlaştırılmış standartlar **tüm ilgili güvenlik gereklerini kapsıyorsa** iç üretim kontrolü yeterlidir. Üç şart birlikte sağlanıyor:

1. EN 71-1 / -2 / -3 mevcut ve tam uygulanıyor.
2. EN 71-1'in OJEU'daki **tek kısıtlaması wave roller** içindir — blok/denge taşı etkilenmez (Md. 19(3)(c) tetiklenmez).
3. Üründe standart dışı yenilikçi özellik yok (Md. 19(3)(d) tetiklenmez).

Sonuçlar: **CE'nin yanına onaylanmış kuruluş numarası KONULMAZ.** Akredite lab raporu almak onaylanmış kuruluş işlemi değildir — Ek IV(g) kanıtıdır. Türkiye'de 2009/48/EC kapsamında **hiç onaylanmış kuruluş yoktur**; gerekirse AB kuruluşlarına gidilir.

Modül A'nın yüklediği: tasarımda risk değerlendirmesi, üretimde **detaylı test ve kontroller + uygunluğun izlenmesi**. Fasona verdiğinde sorumluluk sende kalır.

> Rehberin parti kaydını doğrudan paraya bağlayan notu: uygunsuz ürün bulunduğunda geri çağırmayı **tek partiye daraltabilmen, partinin izlenebilir olmasına bağlıdır**. `uretim/parti/` bu yüzden bir maliyet değil, sigortadır.

## 4 · Uygunluk beyanı — zorunlu alanlar

Ek III'ün 8 maddesi + imza bloğu. Kritik noktalar:

- **Md. 1'deki tekil kimlik, Md. 4(5) izlenebilirlik koduyla AYNI olmalı.** Denetçi bunu `partiler.json` parti no öneki ile karşılaştırır.
- **Md. 4'te yeterli netlikte RENKLİ GÖRSEL zorunludur.**
- Standart sürümleri **tarihiyle** yazılır (`EN 71-3:2019+A2:2024` — A1:2021 değil).
- Onaylanmış kuruluş satırına **"UYGULANAMAZ — Md. 19(2), Modül A"** yazılır; boş bırakılmaz.
- **Beyan tarihi piyasaya arzdan önce olmalı** — denetçi ilk `arz_tarihi` ile karşılaştırır.
- **Beyan ürünle birlikte verilmez.** Ürüne eşlik edecekler yalnızca: güvenlik bilgisi, kullanma talimatı, uyarılar.
- **Birleşik beyan mümkün:** aynı mevzuat ve aynı standartlara uyan SKU'lar tek beyanda listelenebilir (her birinin kendi kodu ve renkli görseliyle). Uygulanmayan standardı "as applicable" diye listelemek yasaktır.
- Standart revize olduğunda beyan etkilenmiyorsa geçerli kalır — ama **etkilenmediğinin değerlendirmesi ayrı bir belgede yazılı tutulur** (Md. 15(2)).

## 5 · Etiket ve işaretleme — dosyanın fiziksel yüzü

| Öğe | Kural |
|---|---|
| **CE** | **≥5 mm**, oranlar korunur, görünür-okunabilir-**silinmez**; ambalajın dışından görünmüyorsa **en azından ambalaja** konur. NB numarası YOK. "Silinmez" testi: su ve benzinle ovma — gravür şart değil, iliştirilmiş etiket de geçerli |
| **Tanımlama** | tip/parti/seri/model no — ürünün üzerinde; boyut/yapı elverişli değilse ambalajda. **Estetik veya ekonomik gerekçeyle ürün üstünden kaldırılamaz.** Çok parçalı setlerde ambalaj yeterlidir |
| **Üretici** | ad + **tek irtibat adresi**; 2025/2509 ile posta **ve elektronik** adres |
| **AB Sorumlu Kişi** | (AB) 2019/1020 Md. 4 — AB'ye satışta **zorunlu**; ad + posta adresi ürün/ambalaj/koli veya ekli belgede. GPSR Md. 19 gereği **ilanda ayrıca e-posta da** ister |
| **Yaş** | `<3` ürününde 0-3 uyarısı **YASAK** (Md. 11(1)); yaş derecelendirmesi yazılır. `3+` ürününde uyarı + tehlike gerekçesi ("Küçük parçalar") **ZORUNLU**. Sembol: EN 71-1 md. 7.2 — çap ≥10 mm, kırmızı daire, "Uyarı" ibaresiyle |
| **Dil** | TR'de Türkçe zorunlu (Md. 5(7), 12(3)) + 6502 md. 55 gereği **Türkçe tanıtma ve kullanma kılavuzu**. AB'de teslim edilen ülkenin dili; online satışta **ilandaki uyarı sitenin diliyle** aynı olmalı |
| **Kontrast** | kırmızı-yeşil / mavi-sarı ve düşük kontrast yasak; x-yüksekliği ürün üstünde ≥3 mm |

**Kademeli dil stratejisi:** başlangıçta AB gönderimini İngilizce yeterli ülkelerle sınırla (etiket tek dilli, maliyet sıfır) → hacim gelince DE/FR/NL/ES/IT+EN tek katlanır yaprağa.

**QR alanı bırak:** hem 6502 tanıtma-kullanma kılavuzunu kalıcı veri saklayıcıyla vermeyi hem 2030 DPP veri taşıyıcısını karşılar. Taşıyıcı biçimi delege akta bağlı olduğundan **ölçüyü şimdiden sabitleme**.

## 6 · Akış

```
1. iskeleti kur   → teknik_dosya.py --sku DT10 --sku KB24
2. belgeleri doldur (aşağıdaki sırayla — sonrakiler öncekine dayanır)
     a) urun_tanimi · olcu_cizim · bom_bos      ← üretim paketinden gelir
     b) kullanim_ve_yas                          ← yaş sınıfı BURADA tanımlanır
     c) guvenlik_degerlendirmesi                 ← 7 tehlike başlığı
     d) tedarikçi belgeleri                      ← tedarik-rfq skill'i toplar
     e) lab raporları                            ← numune gönderimi sonrası
     f) uygunluk_beyani_tr/en                    ← EN SON; arzdan önce tarihli
     g) etiket_baski · ce_yerlesim               ← beyandaki kodla aynı
3. denetle        → teknik_dosya_kontrol.py  (çıkış 1 = teslim edilemez)
4. hepsi.sh       → derle + denetle, tek komut
```

## 7 · Denetçinin uyguladığı kurallar (özet)

**HATA:** Ek IV klasörü yok/boş · (f)/(h)'de ne belge ne UYGULANAMAZ.md · zorunlu belge eksik · ad kalıbı bozuk · aynı kodun birden çok sürümü · `renkli_foto` bir render · beyanda SKU kodu yok · beyandaki standart sürümü eski/eksik · beyan tarihi arzdan sonra · güvenlik değerlendirmesinde 7 tehlikeden biri eksik · yaş gerekçesi yok · yaş sınıfı ↔ 0-3 uyarısı çelişkisi (iki yönde de) · tutkallı üründe soaking izi yok · CE < 5 mm · manifest'te atıfta bulunulan dosya yok · malzeme belgeleri eksik (`belge_kontrol.py` çıkışı devralınır).

**UYARI:** belge tazelik süresi dolmuş · `en71_2_rapor` yok (kapsam dışı gerekçesi yeterli olabilir) · EN sürümler eksik · AB Sorumlu Kişi sözleşmesi yok (AB kanalı açılmadan önce HATA'ya döner) · yağ/vaks bitişli üründe dewaxing izi yok.

## Dosyalar

```
uretim/teknik-dosya/
├── teknik_dosya.py            ← iskeleti kurar, manifest üretir, eksikleri sayar
├── teknik_dosya_kontrol.py    ← DENETÇİ (çıkış kodu 1 = teslim edilemez)
├── hepsi.sh                   ← derle → denetle
├── ORTAK/                     ← generic file gövdesi (00-KAPAK … 04-SUREC)
├── DT10/ · KB24/              ← Ek IV harflerine oturan SKU ekleri + manifest.json
└── cikti/DENETIM-RAPORU.md
```
