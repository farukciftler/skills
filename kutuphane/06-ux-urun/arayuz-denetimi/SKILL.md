---
name: arayuz-denetimi
description: Kartela Klinik OS arayüzünü uçtan uca denetler — üç demo rolüyle (danışman, sekreter, yönetici) her rotanın mobil / yatay tablet / masaüstü ekran görüntüsünü alır, kart-liste-tablo düzenlerini, erişilebilirliği, renk kontrastını, dokunma hedeflerini ve kullanıcı akışlarını puanlar, bulguları düzeltilebilir maddelere çevirir. Arayüz denetimi, UI/UX incelemesi, ekran görüntüsü alma, responsive kontrol, erişilebilirlik taraması, akış/user story incelemesi istendiğinde kullan.
---

# Arayüz denetimi — Kartela Klinik OS

Bu beceri, arayüzü **gerçek çalışan uygulamadan** denetler. Kaynak koda bakarak
tahmin yürütmez: önce ekran görüntüsünü alır, sonra görüntüdeki kusuru koda
bağlar.

## 0. Ön koşullar

| şart | doğrulama |
|---|---|
| Uygulama ayakta | `curl -s http://127.0.0.1:8091/api/health` |
| Demo hesapları var | `scripts/demo_veri.py` en az bir kez çalışmış olmalı |
| Playwright kurulu | `python3 -c "import playwright"` · tarayıcı `/root/.cache/ms-playwright` |

**Uygulama `127.0.0.1:8091` üzerindedir. `8090` sunucudaki BAŞKA bir
PocketBase'e aittir; asla kullanma.**

`lib/pb.ts` API tabanını `window.location.origin`'den alır. Bu yüzden
`next dev` (:3000) üzerinden anlamlı ekran görüntüsü alınamaz — API 404 döner.
Denetim **daima** derlenmiş çıktı üzerinden yapılır:

```bash
cd web && npm run build
docker cp web/out/. kartela:/app/pb_public/     # anında yayına girer
```

## 1. Demo hesapları

Parola üçünde de `Kartela2026!` (`scripts/demo_veri.py` → `PAROLA`).

| e-posta | rol | açılış | rotalar |
|---|---|---|---|
| `danisman@demo.local` | danisman (Rana Çilek) | `/bugun` | bugun · takvim · danisanlarim · hakedisim · bildirimler |
| `sekreter@demo.local` | sekreter | `/pano` | pano · tahsilat · danisanlar · talepler · senkron |
| `yonetici@demo.local` | yonetici | `/kokpit` | kokpit · hakedis · doluluk · ayarlar · denetim |

Oturum `pocketbase_auth` anahtarıyla `localStorage`'ta durur. Görüntü almadan
önce oturumu **API ile** aç ve `localStorage`'a yaz — giriş formunu her seferinde
doldurmak yavaş ve kırılgandır. Hazır betik: `scripts/denetim_ss.py`.

## 2. Görüntü alma matrisi

Üç görünüm zorunlu — `CONTRACT.md §7` kırılma noktalarının her tarafını örnekler:

| ad | ölçü | DPR | dokunma | karşılık |
|---|---|---|---|---|
| `mobil` | 390 × 844 | 3 | evet | iPhone 14 · xs kuşağı (<480) |
| `tablet` | 1024 × 768 | 2 | evet | iPad yatay · lg sınırı |
| `masaustu` | 1440 × 900 | 1 | hayır | xl kuşağı (≥1440) |

Ek olarak **her görünümde** şunları da al:
- `koyu` tema (`prefers-color-scheme: dark`) — en az kritik 6 ekran için
- `siki` yoğunluk (`data-density="siki"`) — tablo ağırlıklı ekranlar için
- **tam sayfa** (`full_page=True`) *ve* **katlanan alan** (viewport) ayrı ayrı —
  "ekrana sığıyor mu" sorusunun cevabı ikisinin farkındadır

Sayfa içi durumları atlama. Bir rotanın tek görüntüsü denetim değildir:
- sekmeli ekranlar (`/ayarlar` → oda · oran · kullanıcı) her sekme ayrı
- alt sayfa / yan ray açık hâli (`AltSayfa`, `YanRay`)
- boş durum (`BosDurum`), yükleniyor (`Yukleniyor`), hata (`Uyari`)
- form doğrulama hatası görünürken
- uzun içerikli liste **ve** sayfalamanın son sayfası

## 3. Denetim eksenleri

Her ekran için aşağıdaki altı ekseni ayrı ayrı puanla. Bir eksende bulgu yoksa
"temiz" yaz; eksen atlanmaz.

### E1 — Sığma ve taşma
- Gövde yatay kaydırıyor mu? (`document.scrollingElement.scrollWidth > clientWidth`)
- Tablo/kod/diyagram kendi `overflow-x:auto` kabında mı, yoksa sayfayı mı itiyor?
- 390px'te kesilen metin, kırpılan rozet, sarmalanmayan uzun Türkçe ad var mı?
- Yapışkan başlık + alt gezinme, 844px'lik ekranda içeriğin kaç pikselini yiyor?
- `100vh` kullanımı — mobil tarayıcı çubuğu altında içerik kaybı yaratır mı?
  (`100dvh`/`svh` tercih edilmeli)

### E2 — Kart · liste · tablo (bu projenin kalbi)
- `CONTRACT.md`: **xs/sm'de oda ızgarası render edilmez**, yerine ajanda listesi
  gelir. Doğrulandı mı?
- Tablo mobilde ne oluyor? Üç meşru cevap var — kart düzenine dönüşmek, yatay
  kaydırılabilir kap, sütun gizleme. **Sütun gizleme yapılıyorsa gizlenen bilgiye
  başka bir yoldan erişim olmalı.** (Bkz. `f1c4973` — tahsilat kart düzenine geçti.)
- Sütun başlıkları kaydırırken kayboluyor mu? (`position: sticky`)
- Sayısal sütunlar sağa hizalı ve `tabular-nums` mı? Para birimi tutarlı mı?
- Kart hiyerarşisi: bir kartta kaç birincil eylem var? >1 ise hangisi birincil
  belli mi?
- Liste satırı tıklanabilirse tamamı mı tıklanabilir, yoksa 12px'lik bir metin mi?
- Boş durum bilgilendirici mi, yoksa "kayıt yok" mu? Sonraki adımı öneriyor mu?
- Sıralama/filtre durumu ekranda görünüyor mu, yoksa gizli mi?

### E3 — Erişilebilirlik
- **Dokunma hedefi**: `pointer: coarse` altında her etkileşimli öğe ≥44×44px.
  Hedefler arası boşluk ≥8px. Ölç, göz kararı yapma.
- **Klavye**: `Tab` sırası görsel sıraya uyuyor mu? Odak halkası her öğede
  görünür mü (`:focus-visible`)? Alt sayfa/yan ray açıkken odak tuzağı var mı,
  `Esc` kapatıyor mu, kapanınca odak tetikleyene dönüyor mu?
- **Anlamsal yapı**: tablo `<table>` mı yoksa div ızgarası mı? `<th scope>` var mı?
  Başlık seviyeleri (h1→h2→h3) atlanmıyor mu? Her sayfada tek `h1` var mı?
- **Ad-rol-değer**: yalnız simgeden ibaret butonların `aria-label`'ı var mı?
  Form alanlarının `<label>`'ı var mı (placeholder etiket değildir)?
- **Canlı bölge**: kaydetme/hata sonucu `aria-live` ile duyuruluyor mu?
- **Bilgi yalnız renkle taşınmıyor**: `CONTRACT.md` oda rozetinde kısaltma
  (`MO SO YO KM BH`), durum rozetinde metin şartı koyar. Uygulanmış mı?
- `prefers-reduced-motion` saygı görüyor mu?
- Ekran okuyucu için gizlenmesi gereken süs öğelerinde `aria-hidden` var mı?

### E4 — Renk ve kontrast
- Gövde metni ≥4.5:1, ≥18.66px veya kalın ≥14px metin ≥3:1, arayüz kenarı /
  ikonu / odak halkası ≥3:1.
- **Kartela kuralı**: rozet ve etiket yazısı daima `--ok-ink` `--warn-ink`
  `--danger-ink` `--info-ink` `--accent-ink` tokenlarından gelir; dolgu tonu
  (`--ok`, `--warn`…) küçük puntoda AA'yı tutturmaz. İhlal ara.
- `--ink-3` beyaz **ve** `--surface-2` üzerinde AA tutmalı.
- Açık **ve** koyu temanın ikisi de ölçülür. Koyu tema ayrı bir denetimdir.
- Tanımsız token kullanımı (`var(--yok)`) sessizce şeffaf/siyah verir —
  `grep -o 'var(--[a-z0-9-]*)' | sort -u` çıktısını `kartela.css` tanımlarıyla
  karşılaştır. (Bkz. `8e5420a`.)
- Oda renkleri beş oda arasında ayırt edilebilir mi — renk körlüğü (döteranopi,
  protanopi) benzetiminde de?

### E5 — Etkileşim ve durum
- iOS'ta girdi odaklanınca sayfa yakınlaşıyor mu? (girdi yazı boyutu <16px ise
  yakınlaşır — bkz. `8e5420a`)
- Yükleniyor durumu düzen kayması yaratıyor mu? İskelet mi, spinner mı, hiçlik mi?
- Eylem sonrası geri bildirim var mı? Kaydet → ne oldu?
- Yıkıcı eylem (silme, iptal) onay istiyor mu? Geri alınabilir mi?
- Çevrimdışı / hata hâli: `public/cevrimdisi.html` ve `Uyari` bileşeni nerede
  devreye giriyor? Ağ hatası kullanıcıya anlaşılır Türkçeyle mi dönüyor?
- Çift gönderim korumalı mı (buton `disabled` + `aria-busy`)?
- İlk boyama flash'ı — tema/yoğunluk okumadan önce yanlış renk çakıyor mu?

### E6 — Akış ve bilgi mimarisi
Her rol için **user story** yaz, sonra o hikâyeyi tarayıcıda gerçekten yürüt:

> *Danışman olarak, sabah kliniğe girerken telefonumdan bugünkü seanslarımı
> görmek ve birinin gelmediğini işaretlemek istiyorum.*

Her adımda ölç: kaç dokunuş, kaç saniye, kaç kez geri döndü, hangi adımda
duraksadı, hangi bilgi ekranda yoktu da aramak zorunda kaldı.

Aranan kusurlar:
- çıkmaz sokak (geri dönüş yolu olmayan ekran)
- rol kapısının yanlış davranması (`RolKapisi`) — yetkisiz rotaya gidince ne olur?
- oturum süresi dolunca (`OturumAyaci`) ne oluyor — veri kaybı var mı?
- derin bağlantı: `/tahsilat`'a doğrudan girilince bağlam kayıp mı?
- geri tuşu alt sayfayı mı kapatıyor yoksa sayfadan mı çıkıyor?
- aynı işi iki farklı yerden yapma — hangisi kanonik?
- yenileme sonrası filtre/sekme/sayfa durumu korunuyor mu (URL'de mi tutuluyor)?

## 4. Bulgu kaydı

Her bulgu şu alanlarla yazılır — eksik alanlı bulgu rapora girmez:

```
ROTA      /tahsilat
GÖRÜNÜM   mobil 390×844, açık tema
EKSEN     E2 — tablo
KANIT     denetim/ss/sekreter-tahsilat-mobil.png — 2. kart, "tutar" satırı
SEMPTOM   Tutar sütunu 3 haneli binlik ayraçta sarmalanıp iki satıra düşüyor,
          kart yüksekliği zıplıyor.
NEDEN     web/app/(sekreter)/tahsilat/_bilesenler/OdemeSayfasi.tsx:88 —
          .tutar sınıfında min-width yok, tabular-nums yok.
ÖNEM      orta   (kritik · yüksek · orta · düşük)
ÇÖZÜM     min-width: 9ch + font-variant-numeric: tabular-nums.
```

**Önem ölçeği**
- `kritik` — kullanıcı işi tamamlayamıyor, veri kaybı, erişilemez temel akış
- `yüksek` — WCAG AA ihlali, mobilde okunamayan/dokunulamayan birincil eylem
- `orta` — sürtünme, tutarsızlık, gereksiz adım
- `düşük` — cila

## 5. Doğrulama — bulguyu kanıtla

Ekran görüntüsü sanı üretir, ölçüm kanıt üretir. Her bulguyu yayınlamadan önce
tarayıcıda sayısal olarak doğrula:

```python
# yatay taşma
page.evaluate("document.scrollingElement.scrollWidth - document.scrollingElement.clientWidth")

# 44px altı dokunma hedefleri
page.evaluate("""() => [...document.querySelectorAll('a,button,input,select,[role=button],[tabindex]')]
  .map(e => ({s: e.tagName + '.' + e.className, r: e.getBoundingClientRect()}))
  .filter(o => o.r.width && (o.r.width < 44 || o.r.height < 44))""")

# tanımsız CSS token
page.evaluate("""() => [...document.querySelectorAll('*')].flatMap(e => {
  const cs = getComputedStyle(e); return []; })""")   # daha kolayı: kaynak grep

# etiketsiz form alanı
page.evaluate("""() => [...document.querySelectorAll('input,select,textarea')]
  .filter(e => !e.labels?.length && !e.getAttribute('aria-label')).map(e => e.outerHTML.slice(0,120))""")

# etiketsiz simge butonu
page.evaluate("""() => [...document.querySelectorAll('button,[role=button]')]
  .filter(e => !e.textContent.trim() && !e.getAttribute('aria-label')).map(e => e.outerHTML.slice(0,120))""")

# konsol hataları — sayfa açılırken topla
page.on("console", lambda m: m.type == "error" and kayit.append(m.text))
```

Kontrast için hesaplanmış renkleri oku ve WCAG oranını hesapla; OKLCH tokenına
bakarak göz kararı verme — kalıtım, opaklık ve üst üste binen katmanlar sonucu
değiştirir.

## 6. Düzeltme kuralları

- **Token dışı renk yazma.** Yeni bir renk gerekiyorsa önce `kartela.css`'e token
  olarak gir, `docs/kartela-klinik-os.html` `:root` bloğuyla eşitle
  (`CONTRACT.md §7` bunu şart koşar).
- Yoğunluk ve kırılma noktası değerleri tokenlardan gelir; sayı gömme.
- Türkçe arayüz metni — yeni metinler de Türkçe, mevcut ton korunur.
- Kod yorumları ve değişken adları çevredeki dosyanın diliyle aynı olur.
- Bir düzeltme bir bulguyu kapatır. Toplu "iyileştirme" commit'i yapma.
- Düzeltmeden sonra **aynı görüntüyü yeniden al** ve önce/sonra karşılaştır.
- `npm run tip-kontrol` ve `npm run build` yeşil kalmalı.

## 7. Çıktı

1. `denetim/ss/` — ham görüntüler, `{rol}-{rota}-{görünüm}[-{durum}].png`
2. `denetim/BULGULAR.md` — önem sırasına dizilmiş bulgu listesi
3. `denetim/AKISLAR.md` — rol başına user story + yürütme kaydı
4. Düzeltmeler — bulgu başına ayrı commit
5. Kapanış tablosu — bulgu · durum (düzeltildi · ertelendi · geçersiz) · kanıt

## Referanslar

- `references/olcutler.md` — WCAG eşikleri, dokunma hedefi kuralları, kontrast hesabı
- `references/akislar.md` — üç rol için hazır user story seti
- `scripts/denetim_ss.py` — görüntü alma koşucusu (bu becerinin yanında)
