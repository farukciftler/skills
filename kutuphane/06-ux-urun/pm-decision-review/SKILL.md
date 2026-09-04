---
name: pm-decision-review
description: Product manager gözüyle otomatik netleştirme soruları sorar, alternatifler ve kazanç/maliyet analizi üretir, karar kaydı çıkarır. Feature fikri, yeni sayfa/akış, "X'i nereye koyalım", UI yerleşimi, veri modeli, yetki/rol, onboarding, kısıt veya kapsam sorusu geçtiği anda kullan — kullanıcı "PM analizi yap" demese bile. Ayrıca mevcut ürünün UX denetimini de yapar — HTML/JS/ekran görüntüsü dosyaları verildiğinde veya "eksikleri bul", "UX'i incele", "tara", "review et" gibi ifadelerde tüm ekranları/akışları sistematik tarar, eksik arayüzleri ve tutarsızlıkları önceliklendirilmiş bulgu raporu + tavsiyelerle sunar. Use this whenever a product/feature decision, UI placement, data model, permissions, onboarding flow, or scope question appears, AND whenever the user shares product UI files or asks for a UX review, gap analysis, or audit of existing screens, even casually.
---

# PM Decision Review

İki mod var; hangisinin istendiğini konuşmadan çıkar:

- **Mod 1 — Karar incelemesi:** Bir ürün kararı tartışılıyorsa (yerleşim, veri modeli, akış, kapsam). Soru sor → alternatif → öneri → karar kaydı.
- **Mod 2 — Proaktif UX denetimi:** Kullanıcı ürün dosyaları paylaştıysa veya "eksikleri bul / incele / tara / review" diyorsa. Soru sormadan önce KENDİN tara, bulguları önceliklendirilmiş rapor olarak getir. Amaç: tasarımcı/geliştirici arkadaş görmeden eksiklerin masada hazır olması.

İkisi iç içe geçebilir: denetim bulgularından çıkan büyük kararlar (ör. "org yönetimi ekranı yok — nereye konmalı?") Mod 1 formatıyla işlenir.

## Mod 1 — Karar incelemesi: çalışma sırası

1. **Kararı tanımla** — konuşmadaki asıl karar cümlesini tek satırda yaz ("Organizasyon yönetimi: cloud connections içine gömülsün mü, ayrı sayfa mı?").
2. **Soru kataloğunu tara** — aşağıdaki boyutlardan yalnızca bu karara dokunanları seç. Konuşmada zaten yanıtlanmış olanları SORMA; yanıtı "veri" olarak kullan.
3. **Varsayım öner, sonra doğrulat** — açık soru bırakmak yerine en olası yanıtı varsayım olarak yaz, kullanıcıya tek satırda onaylat. Soru sayısını 3–5 ile sınırla; kalanını varsayım yap.
4. **Alternatifleri üret** — 2–3 seçenek, her biri kazanç/maliyet/geri dönüş maliyeti ile.
5. **Öner ve kaydet** — tek bir öneri + gerekçe + mini karar kaydı (ADR) formatı.

## Soru kataloğu (boyutlar)

Her boyut için tipik sorular. Karara dokunmayan boyutu atla.

**Veri modeli & kardinalite**
- İlişki 1-1 mi, 1-N mi, N-N mi? (ör. "bir kişinin birden fazla organizasyonu olabiliyor mu?")
- Aynı entity tipinden birden fazla kayıt aynı üst nesne altında olabilir mi? (ör. bir org içinde aynı cloud provider için birden fazla bağlantı)
- Bu kardinalite ileride değişirse hangi ekranlar/endpointler kırılır?

**Yetki & roller**
- Bu işlemi kim yapabilir? (end user / org admin / superadmin)
- Superadmin'in kullanıcıdan bağımsız yapabildiği işlemler neler? (oluştur/düzenle/sil)
- Kullanıcının kendi kaydında değiştiremediği alanlar var mı? (ör. e-postadan çıkarılan domain)

**Yerleşim & bilgi mimarisi**
- Mevcut bir sayfaya mı gömülür, ayrı sayfa mı olur? Karar kriteri: işlem sıklığı, hedef rol, mevcut sayfanın zaten kalabalık olup olmadığı, navigasyon derinliği.
- Bu ekranı hangi rol, hangi sıklıkla kullanacak? (superadmin'in nadiren kullandığı şey ana akışa gömülmez)

**Onboarding & davet akışı**
- Sisteme giriş self-signup mı, invite-only mu?
- Daveti kim atar, davet edilen hangi bilgileri kendisi girer?
- İlk kullanıcı ile sonraki kullanıcıların akışı farklı mı? (ilk kullanıcı org bilgilerini girer, sonrakiler katılır)
- Otomatik türetilen alanlar var mı ve kim override edebilir? (domain'i e-postadan extract etme gibi)

**Kısıtlar & esnetilebilirlik**
- Şimdi konan kısıt (ör. aynı domain'e davet) kalıcı mı, "şimdilik böyle" mi? "Şimdilik" ise gevşetme anını tetikleyecek sinyal ne?
- Kısıtı esnetmek veri modelinde değişiklik gerektirir mi, yoksa sadece validasyon mu?

**Edge case'ler**
- Silme: son kayıt/son admin silinirse ne olur? Soft delete mi hard delete mi? Bağlı kayıtlar (bağlantılar, kullanıcılar) ne olur?
- Devretme: sahiplik/adminlik başka kullanıcıya aktarılabilir mi?
- Çakışma: aynı domain'den ikinci bir org oluşturulmaya çalışılırsa?
- Davet: süresi dolan, reddedilen, zaten üye olan birine atılan davet?

**Tasarım sistemi & tutarlılık**
- Yeni ekran mevcut palet/komponent setiyle mi kurulacak? Benzer bir mevcut ekran (liste + detay + modal kalıbı) referans alınabilir mi?
- Aynı işlem başka bir yerde farklı desenle mi yapılıyor? (tutarsızlık borcu)

**Kapsam: MVP vs sonrası**
- Bu kararın MVP için asgari hali ne, hangi kısmı bilinçli olarak erteleniyor?
- Ertelenen kısım şimdi verilecek kararı kilitliyor mu? (kilitliyorsa şimdi düşün, kilitlemiyorsa ertele)

**Ölçek & güvenlik**
- Multi-tenant izolasyonunu etkiliyor mu? Bir org'un verisi başka org'a sızabilir mi?
- Audit gerektiren bir işlem mi? (superadmin'in org silmesi loglanmalı mı?)

## Alternatif formatı

Her seçenek için ZORUNLU üç alan:

```
### Seçenek A — [kısa ad]
- Kazanç: [neyi hızlandırır/basitleştirir]
- Maliyet: [geliştirme + UX + bakım maliyeti]
- Geri dönüş: [yanlış çıkarsa vazgeçmek ne kadar pahalı — kolay/orta/pahalı]
```

Geri dönüşü pahalı kararlarda (veri modeli, URL yapısı, davet semantiği) muhafazakâr seçeneği öner; geri dönüşü ucuz kararlarda (buton yeri, sayfa yerleşimi) hızlı olanı öner ve "sonra taşırız" de.

## Karar kaydı (mini ADR) formatı

Tartışma sonunda şunu üret:

```
Karar: [tek cümle]
Bağlam: [neden gündeme geldi]
Seçenekler: [A, B, C — bir satır özet]
Seçilen: [X] — Gerekçe: [1-2 cümle]
Bilinçli ertelenenler: [liste]
Yeniden değerlendirme tetikleyicisi: [hangi sinyalde bu karar tekrar açılır]
```

## Mod 2 — Proaktif UX denetimi

Verilen her şeyi (HTML sayfaları, JS dosyaları, ekran görüntüleri, canlı URL, kod deposu) önce envantere çevir, sonra kontrol listesinden geçir, sonra rapor üret. İzin isteme, "ister misin?" diye sorma — kullanıcı taramayı zaten istedi; doğrudan bulgularla dön.

### Adım 1 — Envanter çıkar

- Dosyaları oku: HTML'den sayfaları/bölümleri, JS'den route/komponent/API çağrılarını, nav menüsünden erişilebilir ekranları listele.
- Üründeki entity'leri tespit et (organization, user, connection, dashboard, alert...).
- **CRUD matrisi kur:** her entity × (listele / oluştur / görüntüle / düzenle / sil / davet-vb özel işlem). Arayüzü olmayan hücreler ilk bulgu adayıdır — "org var ama ekleme arayüzü yok" tam bu matristen çıkar.
- Backend'de/veri modelinde var olup UI'da karşılığı olmayan alan ve işlemleri işaretle (JS'deki API çağrıları ile ekranları çapraz kontrol et).

### Adım 2 — Kontrol listesi (her ekran/akış için)

**Akış tamlığı**
- Empty state: hiç kayıt yokken ekran ne gösteriyor? İlk kaydı oluşturmaya yönlendiriyor mu?
- Loading / error / success durumları: spinner, hata mesajı, işlem sonrası geri bildirim (toast/redirect) var mı?
- Yarım akış: başlayan ama sonuçlanmayan yollar (buton var, hedef sayfa yok; form var, submit sonrası ne olacağı belirsiz).

**Navigasyon**
- Erişilemeyen ekran (nav'da linki olmayan sayfa) ve dead-end (geri dönüş yolu olmayan ekran).
- Breadcrumb/başlık tutarlılığı; kullanıcı nerede olduğunu biliyor mu?

**Form & etkileşim**
- Validasyon: zorunlu alan, format kontrolü, anlaşılır hata mesajı (alanın yanında mı, genel mi?).
- Yıkıcı işlemlerde onay (org/bağlantı silme → confirm + sonuçlarının açıklanması).
- Disabled/duplicate koruması: çift tıklamada çift kayıt oluşuyor mu?

**Yetki görünürlüğü**
- Superadmin'e özel işlemler end-user'a görünüyor mu (görünmemeli)?
- Rolün yapamayacağı işlem: gizli mi, disabled mı, tıklayınca mı hata veriyor? (tutarlı tek desen olmalı)

**Veri durumları**
- Uzun liste: pagination/virtual scroll, arama, filtre, sıralama var mı?
- Boş/uzun/uç değerler: uzun isimler taşıyor mu, sıfır/negatif değerler (FinOps'ta maliyet verisi) doğru gösteriliyor mu?
- Tarih/para birimi/sayı formatı tutarlılığı.

**Tutarlılık & tasarım sistemi**
- Aynı işlem farklı ekranlarda farklı desenle mi (bir yerde modal, bir yerde ayrı sayfa)?
- Palet/komponent dışına çıkan tekil stiller; buton hiyerarşisi (primary/secondary) tutarlı mı?

**Metin & dil**
- TR/EN karışımı, placeholder/lorem kalıntısı, teknik jargonun kullanıcıya sızması (raw hata kodu vb.).

**Temel erişilebilirlik & responsive**
- Kontrast, yalnızca renkle kodlanan durumlar (grafiklerde kritik), klavye ile erişim, dar ekranda kırılma.

### Adım 3 — Bulgu raporu formatı

ZORUNLU şablon:

```
# UX Denetim Raporu — [ürün/sayfa] — [tarih]

## Özet
[2-3 cümle: genel durum + en kritik 1-2 bulgu]

## Bulgular
| # | Bulgu | Yer | Önem | Etki | Öneri | Efor |
- Önem: 🔴 Kritik (akışı kırıyor / veri riski) · 🟡 Orta (sürtünme yaratıyor) · 🟢 Düşük (cila)
- Efor: S / M / L

## Eksik arayüzler (CRUD matrisinden)
[entity × işlem, arayüzü olmayanlar]

## Hızlı kazanımlar
[🔴-🟡 önem + S efor kesişimi — ilk sprintlik liste]

## Karara bağlanması gerekenler
[Mod 1'e girecek maddeler — her biri tek soru cümlesi]
```

- Her bulguya somut öneri iliştir; "iyileştirilmeli" gibi boş tavsiye yazma ("silmede onay yok" → "confirm modalı: 'X bağlantısı ve 3 dashboard'u silinecek' metniyle").
- Raporun sonunda ekip arkadaşına iletilecek özet biçimi hazır olsun: kopyala-yapıştır edilebilir kısa madde listesi.

## Örnek (Mod 1)

**Girdi:** "Organizasyon eklemek için arayüz koymamışız. Organization manage'ı cloud connections içine mi gömelim, ayrı sayfa mı?"

**Doğru davranış:**

Önce sorular (konuşmada yanıtlananlar atlanır):
1. Bir kullanıcının birden fazla organizasyonu olabiliyor mu? → *1 kullanıcı = 1 org, ama org içinde aynı provider için N bağlantı.*
2. Org yönetimini kim kullanacak — end user mı superadmin mi? → *Ağırlıklı superadmin.*
3. Kullanıcı girişi self-signup mı invite mi? → *Invite; domain e-postadan türetilir, kullanıcı değiştiremez.*

Sonra alternatifler:
- **A — Cloud connections içine göm:** Kazanç: sayfa sayısı artmaz, tek yerden yönetim. Maliyet: connections sayfası iki farklı kavramı (bağlantı vs org) taşır, superadmin işlemleri end-user akışına karışır. Geri dönüş: orta.
- **B — Ayrı "Organization" sayfası:** Kazanç: rol ayrımı net (superadmin CRUD burada), invite/domain kuralları için doğal yuva, ileride üye yönetimi/rol ekranı buraya büyür. Maliyet: bir sayfa + nav girişi daha. Geri dönüş: kolay.
- **Öneri: B.** Gerekçe: org yönetimi ileride üye, rol, domain kısıtı gibi alt özellikler doğuracak; gömülü başlarsa taşıma maliyeti şimdi ayırma maliyetinden büyük olur.

Ve mini ADR ile kapat.

## Davranış kuralları

- Konuşmada zaten verilen yanıtı asla tekrar sorma; alıntılayıp üstüne kur.
- Kısa ve keskin yaz; her soru tek satır, her kazanç/maliyet tek satır.
- "İkisi de olur" deme — her zaman tek öneri + gerekçe ver, karşı görüşün ne zaman haklı çıkacağını bir cümlede söyle.
- Kullanıcı hızlıca "tamam şöyle yapalım" dediyse soru faslını kes, doğrudan mini ADR üret.
- Denetim modunda önce tara sonra konuş: dosya verilmişse soru sormadan oku, envanteri kur, raporla. Eksik bilgi varsa (ör. bazı ekranlar dosyalarda yok) bunu raporda "kapsam dışı / dosyası paylaşılmadı" olarak belirt, tarama için bekleme.
- Denetimde bulgu sayısını şişirme: aynı kök nedene bağlı tekrarları tek bulgu altında topla ("5 formda da inline validasyon yok" tek satır).
- Kesin bilmediğini bulgu diye yazma: koddan doğrulanamayan şüpheleri ayrı "doğrulanacaklar" başlığına koy.
- Türkçe tartışmada Türkçe, İngilizce tartışmada İngilizce yanıt ver; teknik terimleri (invite, superadmin, soft delete) olduğu gibi bırak.
