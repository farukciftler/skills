# Tazelik

Üretim kadar önemli, tamamen unutulan iş. Sitenin en güçlü yanı somut alanlar —
ve **en hızlı eskiyen veri de tam olarak onlar.**

Yanlış fiyat, olmayan fiyattan kötü: birincisi güveni bitiriyor, ikincisi
yalnızca eksik.

## Eskime hızına göre alanlar

| Alan | Doğrulama sıklığı | Neden |
| --- | --- | --- |
| `entry_fee` | **3 ayda bir** | Enflasyon altında en hızlı bayatlayan veri |
| `opening_hours` | 6 ayda bir | Mevsimlik değişiyor, restorasyonla kapanıyor |
| Gövdedeki "şu an kapalı / onarımda" cümleleri | 6 ayda bir | Onarım biter, cümle yalan olur |
| `best_time`, `best_season` | Yılda bir | Mevsim döngüsü sabit |
| `duration`, `distance` | Değişmez | Yalnızca rota değişirse |
| `lat`, `lng`, `period`, `founded` | Değişmez | — |

## Nasıl doğrulanır

`icerik-uret` becerisinin Google yorumu adımı burada da geçerli: son üç ayın
yorumlarında fiyat ve saat geçiyorsa, üç yorumda aynı değer varsa güncelle.

Yöntem: `icerik-uret/references/google.md`.

## Bilinmiyorsa ne yazılır

**Uydurma.** Site bu kararı zaten vermiş durumda ve tutarlı olmalı:

```
entry_fee: "Değişken — girişte teyit et"
```

Bu cümle bir eksiklik değil, dürüst bir bilgi. `llms.txt` de siteyi böyle
tanıtıyor: *"Belirsizlik gizlenmez."*

## Eski içeriği güncellemek yeni içerik üretmekten önce gelir mi

Genelde **hayır** — ama bir istisnayla.

Sıradan bir tazelik borcu (best_time gözden geçirme gibi) yeni kaydın önüne
geçmiyor. Ancak **yanlış olduğu bilinen** bir fiyat ya da saat, her şeyin
önündedir: yayında duran yanlış bilgi aktif zarar veriyor, eksik kayıt yalnızca
fırsat kaybı.

Sıralama:

```
1. Yanlış olduğu bilinen veri        → hemen düzelt
2. Envanterdeki P0–P2 bulguları      → SKILL.md sırası
3. Rutin tazelik borcu               → toplu, üç ayda bir
4. Yeni kayıt
```

## Toplu tazelik turu

Üç ayda bir, tek oturumda:

```bash
node .claude/skills/icerik-strateji/scripts/envanter.mjs --json \
  | python3 -c "import sys,json;[print(b['hedef']) for b in json.load(sys.stdin)['bulgular'] if b['tur']=='eksik alan']"
```

Çıkan listedeki her mekan için `entry_fee` ve `opening_hours` doğrula, düzelt,
tek commit'te gönder. Ayrı ayrı commit'lemek hem gürültü hem de tazelik turunun
ne zaman yapıldığını `git log`'da görünmez kılıyor.

Commit başlığı sabit tutulursa geçmiş okunabilir kalıyor:

```
content: tazelik turu (2026-11)
```
