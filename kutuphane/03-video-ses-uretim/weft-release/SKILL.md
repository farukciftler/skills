---
name: weft-release
description: Weft Records etiketinin uçtan uca yayın hattını yürütür — yeni sanatçı kimliği açma, yayın brief'i, Suno bestesi, retro kapak, yayın metadata'sı ve katalog kaydı. Bu repoda müzik, sanatçı, albüm, kapak, prompt veya katalog ile ilgili HER iş bu skill ile başlar. Tetikleyiciler: "yeni sanatçı", "yeni albüm aç", "WR-0NN", "şarkı üretelim", "kapak yap", "prompt logla", "kataloğa ekle", "yayına hazırla", "roster", "bu sanatçının tarzı", "albüm çıkaralım", "metadata yaz", "excel'i güncelle". Sanatçı kimliğinin şeridini korumak ve her üretim denemesini loglamak bu skill'in birincil görevidir.
---

# Weft Release — etiket yayın hattı

Bu skill, bu repodaki katalog sisteminin doğru kullanılmasını sağlar. Amacı iki şeyi garantilemek:

1. **Hiçbir sanatçı şeridinden çıkmaz.**
2. **Hiçbir üretim denemesi kaydedilmeden kaybolmaz.**

## Her işten önce oku

- `CLAUDE.md` — aktif marka yönü ve proje durumu
- `docs/conventions.md` — ID formatları, klasör/dosya adları, şerit kilidi kuralı
- `docs/workflow.md` — altı aşamalı akış
- İlgili sanatçının `artists/<slug>/identity.md` dosyası

Sanatçı kimlik kartını okumadan o sanatçı için hiçbir şey üretme. Şerit tanımı orada.

## Hangi aşamadayız

Kullanıcının isteğine göre `docs/workflow.md` içindeki aşamayı belirle ve **sadece o aşamayı** yürüt. Aşama atlama; bir sonrakine geçmeden önce o aşamanın CSV satırı yazılmış olmalı.

| Kullanıcı der ki | Aşama | Kullanılacak skill |
|---|---|---|
| "yeni sanatçı", "roster'a ekleyelim" | 1 — Kimlik | `suno-composer` (çekirdek), `retro-record-label` (görsel kimlik) |
| "yeni albüm", "WR-0NN açalım" | 2 — Brief | — |
| "şarkıyı üretelim", "suno prompt'u" | 3 — Beste | `suno-composer` |
| "kapak yap", "kapak alternatifi" | 4 — Kapak | `retro-record-label` |
| "youtube açıklaması", "track adları" | 5 — Metadata | `retro-record-label` |
| "yayınlayalım", "checklist" | 6 — Yayın | — |

## Değişmez kurallar

**Şerit kilidi.** Bir üretim, sanatçının `identity.md` içindeki Şerit tablosundaki bir alanı ihlal ediyorsa dur ve kullanıcıya söyle. Üç seçenek sun: (a) üretimi şeride çek, (b) yeni sanatçı aç, (c) bilinçli evrim olarak Evrim günlüğüne yaz. Sessizce ihlal etme.

**"Asla yapmaz" listesi.** Kimlik kartındaki bu maddeler doğrudan Suno **Exclude** alanına girer. Her yayında yeniden.

**Prompt logu.** Suno'da çalıştırılan her Style/Exclude kombinasyonu — beğenilmeyenler dahil — `catalog/prompt_log.csv`'ye bir satır. Style ve Exclude metinleri **tam** yazılır, kısaltılmaz. Satır sonları ` / ` ile birleştirilir.

**ID tahsisi.** Yeni ID vermeden önce ilgili CSV'yi oku, en yüksek numarayı bul, bir artır. ID yeniden kullanılmaz.

**Beste sırası.** `suno-composer` çağrılırken müzikal kararlar (ton, tempo, ölçü, bar sayılı form, armonik plan, tessitura) önce üretilir, Style alanı sonra yazılır. Bu sıra bozulursa çıktı jenerikleşir — skill'in tüm değeri bu sırada.

**Dönem doğruluğu.** Aktif marka yönü A (Arşiv) ise ve yayının kurgusal bir yılı varsa, `docs/conventions.md` içindeki dönem kontrolünü uygula. 1972 albümünde DX7 olmaz.

**Görsel süreklilik.** Kapak paleti ve tipografisi sanatçı kimlik kartından gelir, yayına göre keyfî değişmez. Değişen: görüntü ve tretman dozu.

**Künye satırı.** Her yayın metadata'sında, kurgunun gerçek sanılmaması için `templates/metadata.md` sonundaki künye satırı bulunur. Atlanamaz.

## Her iş bitiminde

1. İlgili CSV satır(lar)ını yaz.
2. `python3 catalog/build_workbook.py` çalıştır — Excel'i tazele.
3. Kullanıcıya ne yazdığını tek tabloyla göster: hangi ID, hangi dosya, hangi CSV.

## Şablonlar

Yeni dosya oluştururken daima `templates/` altındaki şablondan başla, sıfırdan yazma:
`artist-identity.md` · `release-brief.md` · `suno.md` · `cover-spec.md` · `metadata.md`
