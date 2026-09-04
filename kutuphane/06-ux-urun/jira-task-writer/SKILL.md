---
name: jira-task-writer
description: Writes and creates Jira issues that contain ONLY what the user actually said - no invented scope, no best-practice padding, no unrequested sections. Every missing-but-relevant consideration is raised as a warning in chat instead of being written into the ticket. Use whenever the user wants a Jira task/story/bug/epic created, drafted, rewritten or cleaned up - "jira'ya task aç", "şunu ticket'a çevir", "FINOPS'a bir task gir", "bunu Jira'ya yaz", "task açalım", "issue oluştur", "acceptance criteria yaz", "bu maili task'a dönüştür", "şu spec'i Jira'ya taşı" - and also when reviewing an existing ticket for scope creep or hallucinated requirements. Trigger even if the user never says "skill" or gives only two sentences of input; short input must produce a short ticket, not an inflated one.
---

# Jira Task Writer

Bu skill'in tek bir amacı var: **Jira task'ı kullanıcının söylediklerinden ibaret olsun.**

Varsayılan davranışın (bir spec gördüğünde onu "tamamlama", eksik gördüğün başlıkları
doldurma, iyi bir PM gibi kapsamı genişletme refleksi) burada **hatadır**. Kullanıcı
task'ı okuduğunda kendi cümlelerini görmeli; senin eklediklerini ayıklamak için
zaman harcamamalı.

Ekleme yapmak yerine **uyarırsın**. Uyarı chat'e gider, task'a değil.

---

## Temel ilke: Sıfır Ekleme

Task'taki her satır, kullanıcının girdisindeki bir ifadeye geri izlenebilir olmalı.
İzlenemiyorsa o satır task'a girmez.

İki soruyu ayır:

| Soru | Cevap |
|---|---|
| "Bu maddeyi kullanıcı söyledi mi?" | Evet → task'a yaz. Hayır → yazma. |
| "Bu madde iyi bir fikir mi?" | **Bu soruyu sorma.** İyi fikirse uyarı bölümünde söyle. |

Bir maddenin doğru, faydalı, sektör standardı veya "zaten olması gereken" bir şey
olması, task'a girmesi için gerekçe değildir. Tek gerekçe: kullanıcının söylemiş olması.

---

## Varsayılan olarak KAPALI bloklar

Aşağıdakiler yalnızca kullanıcı **açıkça** istediğinde task'a girer. Kullanıcı
bunlardan bahsetmediyse bölüm başlığı bile açılmaz:

- **Tarayıcı / cihaz / çözünürlük matrisi** ("Chrome, Safari, Firefox, Edge'de test edildi", "1280/1440/1920/375px")
- **Performans bütçeleri ve araçları** (Lighthouse skoru, FPS hedefi, ms eşiği, bundle size, Core Web Vitals)
- **Erişilebilirlik** (WCAG, kontrast oranı, klavye navigasyonu, aria, screen reader)
- **Mobil / dokunmatik davranış** (tap-to-show, scrubbing, touch-action, responsive kırılımlar)
- **Kapsam Dışı / Out of Scope bölümü** — kullanıcı "şunlar kapsam dışı" demediyse bu başlığı hiç açma
- **Hukuk ve uyum** (KVKK, GDPR, veri saklama, aydınlatma metni, log maskeleme)
- **Güvenlik** (yetkilendirme, RBAC, rate limit, input sanitization, XSS/CSRF)
- **Test planı** (unit/integration/e2e coverage, test senaryoları, QA adımları)
- **Rollout** (feature flag, kademeli açılım, rollback planı, migration)
- **Lokalizasyon / i18n**, **analytics / telemetry / event tracking**, **dokümantasyon**, **SEO**
- **Tahmin ve planlama alanları** (story point, effort, süre, sprint, due date, bağımlılık)
- **Kişiler** (assignee, reviewer, watcher) ve **etiketler / component / epic link**

Bu liste kapalı değil. Kural şu: girdide yoksa, task'ta da yok.

---

## İzin verilen dönüşümler

Sıfır ekleme "kelimesi kelimesine kopyala" demek değil. Şunlar serbest:

- **Yeniden yazma:** dağınık cümleyi net, buyurgan bir gereksinime çevirmek
- **Yapılandırma:** kullanıcının anlattıklarını bileşene/başlığa göre gruplamak
- **Kabul kriterine çevirme:** girdideki bir davranışı doğrulanabilir bir ifadeye dönüştürmek
- **Tekrarı birleştirme:** aynı şeyi iki kez söylediyse tek maddede toplamak
- **Terminoloji tutarlılığı:** aynı kavram için tek isim kullanmak

Şunlar serbest **değil**:

- Girdide olmayan bir davranışı "ima ediliyor" diye eklemek
- Bir maddeyi genelleştirip kapsamı büyütmek
  ("tooltip anomali detayı göstersin" → "tüm grafiklerde anomali görselleştirmesi")
- Sayısal eşik uydurmak (kullanıcı "hızlı" dediyse "<100ms" yazma; "hızlı" yaz ve sor)
- Bir örneği zorunlu kurala çevirmek

---

## Kabul kriterleri kuralı

Kabul kriterleri **yeni gereksinim üretme yeri değildir**. Her kriter, gövdede zaten
yazan bir maddenin doğrulanabilir hâlidir. 1:1 türetilir.

Girdide 6 gereksinim varsa kabul kriteri 6 civarı olur; 12 olamaz. Sayı şişiyorsa
kesin ekleme yapmışsındır — geri dön ve fazlalıkları uyarıya taşı.

Kriterler, kullanıcının kendi belirlediği ölçütle yazılır. Kullanıcı ölçüt vermediyse
kriter niteliksel kalır ("tooltip hover'da görünüyor"), uydurma bir eşik almaz.

---

## Alanlar: uydurma yok

- **Project / issue type:** kullanıcı söylediyse onu kullan. Söylemediyse sor.
  Bilinen varsayılan: FINOPS projesi, cloudId `3f896dbe-5eff-4b06-96c5-92f31eea9dcd`.
  Yine de proje/tip belirsizse tek satırlık bir soruyla teyit al, tahmin etme.
- **Priority, assignee, labels, component, epic, sprint, due date:** kullanıcı
  vermediyse **boş bırak**. "Medium" bile bir varsayımdır.
- **Başlık:** kısa, işin ne olduğunu söyleyen tek satır. Girdide olmayan bir sıfat
  ("kapsamlı", "gelişmiş") ekleme.

---

## İş akışı

1. **Ayrıştır.** Girdiyi atomik gereksinimlere böl. Her biri için kaynağı zihninde tut.
2. **Taslakla.** Yalnızca ayrıştırdığın maddelerle task gövdesini yaz.
3. **Ekleme denetimi yap.** Taslağı satır satır gez ve her satır için sor:
   *"Bu, kullanıcının hangi cümlesinden geliyor?"* Cevap veremediğin her satırı sil.
   Özellikle "Varsayılan olarak KAPALI bloklar" listesini bir checklist gibi tara.
4. **Uyarıları topla.** Sildiklerin ve girdideki boşluklar uyarı listesine gider.
5. **Önizle ve onay al.** Task'ı chat'te göster + uyarıları altına ekle. Kullanıcı
   "aç" demeden Jira'da issue **oluşturma**. (Kullanıcı zaten "aç" diyerek başladıysa
   önizleme + oluşturmayı aynı turda yapabilirsin, uyarıları yine de göster.)
6. **Oluştur.** Atlassian Rovo ile `createJiraIssue`. Ardından issue key + link ver.

---

## Uyarı formatı

Task önizlemesinden **sonra**, ayrı bir blokta. Kısa, madde madde, gerekçesiz.
Her uyarı ya bir boşluk ya da senin bilerek yazmadığın bir şey.

```
⚠️ Task'a yazmadım — istersen ekleyeyim:
- Erişilebilirlik (klavye ile gezinme, screen reader) hakkında bir şey söylemedin.
- Hangi tarayıcı/çözünürlüklerde doğrulanacağı belirsiz.
- "Hızlı görünsün" dedin ama sayısal bir eşik vermedin.
- Bu değişikliğin Cost Explorer'daki grafikleri de kapsayıp kapsamadığı net değil.
```

Üç kural: en fazla 6-7 uyarı (en önemliler), her biri tek satır, savunma yapma.
Kullanıcı "hayır" derse tekrar önerme.

Girdi net ve eksiksizse uyarı bloğunu hiç yazma. Uyarı üretmek zorunda değilsin.

---

## Task şablonu

Sadece içeriği olan başlıklar yazılır. Boş başlık bırakma.

```
## Problem
[Kullanıcının anlattığı mevcut durum / sıkıntı. Yoksa atla.]

## Amaç
[Tek paragraf. Yoksa atla.]

## Kapsam
[Kullanıcının saydığı bileşen/davranışlar. Girdi bileşenlere ayrılıyorsa
alt başlıklarla, ayrılmıyorsa düz liste.]

## Kabul Kriterleri
- [ ] [Gövdedeki maddelerden 1:1 türetilmiş]

## Notlar
[Kullanıcının söylediği, yukarıya girmeyen teknik not. Yoksa atla.]
```

Kullanıcı bir bölümü açıkça istediyse (ör. "kapsam dışını da yaz") o bölüm eklenir.

---

## Örnekler

**Örnek 1 — kapsam şişirme**

Girdi: *"Dashboard'daki donut chart'a hover olunca dilim büyüsün, ortadaki metin o
sağlayıcının değerine dönsün."*

Yanlış çıktı: donut + legend çift yönlü vurgu + tooltip içeriği + mobil tap davranışı
+ prefers-reduced-motion + WCAG kontrastı + "Kapsam Dışı: zoom/brush".

Doğru çıktı: iki gereksinim (dilim expand, merkez metin değişimi), iki kabul kriteri.
Legend, mobil, animasyon tercihi → uyarı bloğunda soru olarak.

**Örnek 2 — eşik uydurma**

Girdi: *"Tooltip anında açılsın, gecikme hissedilmesin."*

Yanlış: `- [ ] Tooltip 100ms içinde görünüyor.`
Doğru: `- [ ] Tooltip hover'da gecikme hissettirmeden açılıyor.`
+ uyarı: *"'Gecikme hissedilmesin' için sayısal bir eşik vermedin (ör. giriş gecikmesi ms)."*

**Örnek 3 — konu dışı blok**

Girdi: kullanıcı formda yeni bir alan istiyor, sadece UI'dan bahsediyor.

Yanlış: task'a "KVKK uyarınca bu alan için açık rıza alınmalı" satırı.
Doğru: task'ta böyle bir satır yok; uyarıda *"Yeni alan kişisel veri içeriyorsa
KVKK tarafını konuşmadık."*

---

## Mevcut bir task'ı denetlerken

Kullanıcı yazılmış bir ticket verip "bunu temizle / fazlalıkları at" derse: aynı
ekleme denetimini uygula, çıkarılacak satırları listele, sonra sadeleştirilmiş
sürümü ver. Ne çıkardığını göster ki kullanıcı itiraz edebilsin.
