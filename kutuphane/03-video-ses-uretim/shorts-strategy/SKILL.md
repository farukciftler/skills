---
name: shorts-strategy
description: Format seçimi ve yayın temposu kuralları — yeni bir video/seri fikri değerlendirilirken veya yayın planlanırken uygula
---

# Shorts format & cadence — karar kuralları

Tam araştırma: `docs/headless-reel-forge/references/shorts-strategy.md`.
Bu skill, bir fikir "üretilmeye değer mi" ve "hangi tempoda yayınlanır"
sorularının kontrol listesidir.

## Format testi — beşi de geçmeyen fikir üretilmez

1. **Soru**: İzleyicinin ilk 2 saniyede *görebildiği* açık bir soru var mı?
   ("Kaçabilecek mi?", "Ekran dolacak mı?") Cevabı bilinen ama *ne zaman*
   olacağı bilinmeyen bir soru en iyisidir.
2. **Eskalasyon**: Tek yönde ilerleyen görünür bir durum var mı (hız, sayı,
   boyut, doluluk)? Düz bir anlatı (dövüş turnuvası gibi) eskalasyon değildir.
3. **Payoff ritmi**: Ara ödüller var mı (duvar kırılır, renk taşar, top
   bölünür)? Tek büyük final yetmez.
4. **Loop**: Son kare ilk kareye görsel olarak bağlanabiliyor mu? (%100 üstü
   izlenme sinyalinin kaynağı.)
5. **30 video testi**: Aynı tariften seed/parametre değişimiyle 30 video
   çıkar mı? Çıkmıyorsa bu bir seri değil, tek seferlik gösteridir — üretme.

## Kanıtlanmış formatlar (rigid-body ile yapılabilenler)

- **Tier 1 — ball-escape** ("Will the ball escape?"): iç içe dönen halkalar,
  boşluktan kaçış, kırılan duvarlar, **melodi senkronu** (her çarpma şarkının
  sıradaki notası — contact log'dan üretilebilir). Referans: tek videoda 38–67M.
- **Tier 2 — çoğalma/doldurma/kırma**: her sekmede klonlanan top, renk dolduran
  tuğla duvar, sığmayana kadar büyüyen cisim.
- **Tier 3 — marble race** (mevcut gauntlet): takım kimliği + eleme + seri
  numarası şart; spike değil birikim yapar.
- **Yapılmayacak**: soft-body taklidi (rigid ile olmuyor, denendi), tek seferlik
  anlatılar, format oturmadan cila yatırımı.

## Tempo kuralları

- Günde 1, en fazla 2 video; haftada 3–4'ün altına düşme (her video sıfırdan
  başlar).
- Kalite > adet: %60 retention'lı haftalık video, %25'lik günlük videoyu döver.
  Retention ~%70+ APV hedef.
- Seri kimliği: aynı palet, aynı çerçeve, numaralı başlık ("ESCAPE #N").
- ~200 video kalibrasyon fazıdır: her yayının APV'sini seed/parametreyle
  birlikte kaydet, sweep gibi işle.
- Yükleme pratiği CLAUDE.md § "Publishing throughput"ta: içerik kontrolü ~9 dk,
  kontroller paralel yürütülür, tek video için 30 dk'lık tempo mümkün.

## Silme politikası

Az izlenme tek başına silme sebebi değildir: silmek watch-time'ı geri alır,
linkleri kalıcı kırar ve algoritma düşük videoları cezalandırmaz. Niş dışı /
bayat / riskli içerik → Gizli'ye çek; kalıcı silmeyi yalnız kullanıcı kendi
yapar.
