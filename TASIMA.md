# Taşıma Raporu

Ne tarandı, ne toplandı, ne **toplanamadı**, ayrışmış sürümler ve nasıl geri
alınacağı. Kütüphane kurulurken kaynak konumlara **dokunulmadı** — hepsi
yerinde duruyor.

## Ne yapıldı

Ev dizini ve claude.ai yerel önbelleği tarandı, **174 skill kaynağı** bulundu
(1.966 `SKILL.md` görüldü; 1.792'si `~/.claude/remote/plugins/` altındaki eski
oturum anlık görüntüleriydi, IDE eklentileri ve iş dizinleriyle birlikte elendi).

Kalan 174 kaynak **113 benzersiz skill**'e, oradan da **131 kütüphane girdisine**
indirildi (18 ayrışmış sürüm ayrı girdi olarak korundu) ve 14 kategoriye
dağıtıldı.

Ardından 175 GitHub deposu tarandı ve yalnız orada duran 6 skill eklendi
(§ GitHub taraması). Son olarak ikinci bir bilgisayar tarandı ve oradan 16 girdi
geldi (§ İkinci makine taraması). **Güncel toplam: 127 benzersiz skill,
153 girdi.**

Tam yedek: `~/skills-yedek-20260904-135254.tar.gz` (2,6 MB).

## Kaynak konumları üç sınıfa ayrıldı

**1 · Gerçek kurulum noktası — bağlanabilir (69 kaynak).**
Claude'un skill'i fiilen yüklediği yerler: `~/.claude/skills/<ad>` ve
`<proje>/.claude/skills/<ad>`. Bunlar symlink'e çevrilebilir; kütüphane gerçek
tek kaynak olur.

| Depo | Adet | | Depo | Adet |
|---|---|---|---|---|
| `projects/mcailabs-v4.0` | 9 | | `Documents/GitHub/moonstone` | 4 |
| `projects/reelsindustry` | 8 | | `Documents/GitHub/portfoy-butce` | 4 |
| `projects/weftrecords` | 8 | | `projects/kartelastrateji` | 3 |
| `Documents/GitHub/weftrecords` | 7 | | `.gemini/…/kirkit-skills` | 5 |
| `projects/comesyriacontent` | 6 | | `~/.claude/skills` (global) | 5 |
| diğer 10 depo (1'er) | 10 | | | |

**2 · Proje altyapısı — bağlanamaz (57 kaynak), ayna kopya alındı.**
`SKILL.md` içeriyorlar ama skill kurulum noktası değiller; proje kodu veya
derlemesi onlara bağlı. Symlink'e çevirmek bu projeleri bozardı:

| Konum | Neden taşınamaz |
|---|---|
| `projects/masifico/skills/` | `build-skills.sh` bunları `docs/skills/*.skill` zip'lerine paketliyor |
| `projects/kirkit/data/skills/skills/` | `apps/server/src/skills/store.ts` çalışma anında okuyor |
| `projects/instagram-reels/docs/` | `README.md`, `CLAUDE.md` ve `forge/pipeline/order_report.py` referans veriyor |
| `projects/comesyriacontent/backlog/` | Kendi `scripts/*.mjs` ve CSV/JSON veri dosyalarıyla bir arada |
| `projects/mcailabs-v4.0/.agents/skills/` | Başka bir ajan aracının ayna dizini |
| `projects/autonomous-agent-prediction/submissions/` | Yarışma teslim artefaktı — değişmemeli |
| `projects/startup değerleme/skill/` | Çalışma klasörü |

**3 · claude.ai senkronu — taşınamaz (48 kaynak), ayna kopya alındı.**
Bu skill'ler `~/Library/…/local-agent-mode-sessions/skills-plugin/<oturum-id>/…`
altında yaşıyor. Yol **her oturumda yeniden üretilen geçici bir önbellek**;
oraya symlink koymak bir sonraki senkronda kaybolur. Bunların gerçek kaynağı
claude.ai hesabındaki skill deposudur — düzenleme oradan yapılır, kütüphanedeki
kopya arşiv/okuma amaçlıdır.

## Ayrışmış sürümler (16 ad)

Aynı isimli kopyalar körlemesine birleştirilmedi; farklı olan hiçbir şey
kaybolmadı. Düz ad **birincil** (en yeni içerik), `--` ekli olanlar diğer
sürümler.

### Aynı skill'in sürüklenmiş kopyaları

| Skill | Birincil | Geride kalan |
|---|---|---|
| `weft-channel` | `projects/weftrecords` + `reelsindustry` | `Documents/GitHub/weftrecords` — `superseded` statüsü ve geçmiş-URL mantığı eksik |
| `pexels-media-scout` | `projects/weftrecords` + `reelsindustry` | `Documents/GitHub/weftrecords` — `credits.json` birleştirme düzeltmesi eksik (WR-040) |
| `portfoy-tahmin` | `Documents/GitHub/portfoy-butce` (17,4 KB) | `projects/portfoy-butce` (16,6 KB), claude.ai (9,6 KB) |
| `backlog-arastir` | `comesyriacontent` | `kirkit` veri deposu (2,8 KB) |
| `sosyal-medya-post-uret` | `comesyriacontent` (8,0 KB) | `kirkit` veri deposu (5,1 KB) |
| `headless-reel-forge` | global + kirkit aynaları | `instagram-reels/docs` (5 ek dosya fazla) |
| `postgresql`, `pytest`, `gitnexus-cli` | `mcailabs-v4.0/.claude` | `mcailabs-v4.0/.agents` aynası |
| `automl` | `submissions/03_hardened` | `01_baseline`, `02_gemini_fallback` — kasıtlı deney varyantları |

> **`projects/` ve `Documents/GitHub/` aynı repoların ayrı klonları.** Farklı
> commit'lerde ve her biri farklı yerlerde önde: `weftrecords`'ta `projects/`
> ileri, `portfoy-butce`'de `Documents/GitHub/` ileri. Bağlamadan önce bu
> klonları git tarafında hizalamak gerekir.

### Bayat claude.ai kopyaları

Bu beş skill claude.ai'da, projedeki halinden **belirgin biçimde eski** duruyor.
Desktop/web oturumlarında eski sürüm tetiklenir:

| Skill | Proje sürümü | claude.ai sürümü |
|---|---|---|
| `oyuncak-mevzuat` | 20,4 KB | 7,7 KB |
| `masifico-uretim-muhendisi` | 11,1 KB | 5,5 KB |
| `oyuncak-pazar-radari` | 10,1 KB | 8,5 KB |
| `masifico-maliyet-fiyat` | 8,8 KB | 5,6 KB |
| `masifico-farklilasma` | 8,6 KB | 4,6 KB |

**Yapılacak:** `projects/masifico/skills/` altındaki güncel sürümleri claude.ai'a
yeniden yükle. `portfoy-tahmin`'in cloud kopyası da (9,6 KB → 17,4 KB) geride.

### Aynı isim, farklı skill

`ceviri` iki ayrı iştir; birleştirilmedi, ikisi de eklenti aldı:

- `ceviri--comesyriacontent` — TR / küresel İngilizce / Suriye Arapçası,
  ad-sayı sadakati ve yapay zekâ tikliği denetim script'leriyle (9,7 KB)
- `ceviri--abdullahfarukcom-gh` — düz TR↔EN çeviri (5,7 KB)

## Bağlama (yıkıcı adım — henüz yapılmadı)

Kurulum noktalarını kütüphaneye bağlamak dizini silip yerine symlink koyar.
Bundan sonra skill tek yerden düzenlenir. Git deposundaki bir kurulum noktası
symlink'e dönüşünce repo'da **silme + symlink** olarak görünür — bu yüzden
depo başına ilerle.

```bash
python3 scripts/bagla.py                        # tüm kapsamı göster
python3 scripts/bagla.py --proje kartelastrateji
python3 scripts/bagla.py --proje kartelastrateji --uygula
```

`bagla.py` bir kaynağı, kütüphanedeki kopyayla **birebir aynı olduğunu
doğrulamadan** değiştirmez; sürüklenmiş bir dizin sessizce ezilmez, atlanır.
Her işlem `katalog/baglanti-kaydi.json`'a yazılır.

Bağlamadan önce:

1. `projects/` ↔ `Documents/GitHub/` klonlarını git tarafında hizala (yukarıdaki
   ayrışma tablosu).
2. Kirli depolarda (`mobilya`, `moonstone`, `weftrecords`, `instagram-reels`,
   `portfoy-butce`) mevcut değişiklikleri commit'le.

### Geri alma

```bash
python3 scripts/coz.py --uygula                  # tümü
python3 scripts/coz.py --proje weftrecords --uygula
```

Symlink silinir, yerine kütüphanedeki içeriğin gerçek kopyası konur. Tam geri
dönüş için yedek: `~/skills-yedek-20260904-135254.tar.gz`.

## Yeniden tarama

```bash
python3 scripts/topla.py             # planı göster
python3 scripts/topla.py --uygula    # kutuphane/ + manifest tazele
python3 scripts/katalog_uret.py      # INDEX + katalog + kategori README'leri
```

Yeni bir skill kategoriye girmezse `topla.py` uyarır ve onu
`kutuphane/99-siniflandirilmamis/` altına koyar; kategori eşlemesi hem
`scripts/topla.py` hem `scripts/katalog_uret.py` içinde güncellenmeli.

## GitHub taraması (175 depo)

Yerel diskte olmayan skill'ler için hesaptaki tüm depoların varsayılan dal
ağacı tarandı. **20 depoda** `SKILL.md` bulundu; bunların 14'ü zaten yerelde
klonlu.

Yalnız GitHub'da duran **6 skill** kütüphaneye alındı:

| Skill | Depo | Kategori |
|---|---|---|
| `apple-platform-architect` | `pipsworn` | 07-yazilim-muhendislik |
| `appstore-market-analyst` | `pipsworn` | 05-pazarlama-buyume |
| `jira-task-writer` | `pipsworn` | 06-ux-urun |
| `post-forge` | `pipsworn` | 09-cad-gorsel |
| `arayuz-denetimi` | `terapipanel` | 06-ux-urun |
| `icerik-yaz` | `masifico-web` | 04-icerik-yazim-ceviri |

> `terapipanel` yerelde klonlu ama `arayuz-denetimi` yalnız GitHub'da — yerel
> klon geride. `pipsworn`, `masifico-web`, `portfolio-afc` ve `agentpanel` bu
> makinede hiç klonlu değil.

Alınmayan 5 bulgu üçüncü taraf, senin yazdığın skill değil:

| Skill | Nerede | Neden alınmadı |
|---|---|---|
| `fastapi`, `typer` | `portfolio-afc` → `mcp-env/…/site-packages/` | Kütüphanelerin kendi vendor'lanmış skill'leri |
| `skill`, `trace` | `agentpanel` → `node_modules/playwright-core/` | Playwright'ın yerleşik skill'leri |
| `verify` | `src` → `skills/bundled/` | 0 bayt, boş dosya |

Bu skill'ler kütüphaneye kopyalandı ama kaynak depolarına **dokunulmadı**;
`bagla.py` onları bağlayamaz (yerelde klon yok). O depolarda çalışırken
kütüphanedeki sürümle ayrışabilirler.

Taramayı yinelemek için:

```bash
gh repo list --limit 300 --json name,defaultBranchRef | \
  python3 -c "import json,sys,subprocess
for r in json.load(sys.stdin):
    br=(r.get('defaultBranchRef') or {}).get('name')
    if not br: continue
    p=subprocess.run(['gh','api',f\"repos/farukciftler/{r['name']}/git/trees/{br}?recursive=1\",
                      '-q','.tree[].path'],capture_output=True,text=True)
    y=[x for x in p.stdout.splitlines() if x.endswith('SKILL.md')]
    if y: print(r['name'], len(y))"
```

## İkinci makine taraması

İlk iki tur tek bir bilgisayarda yapılmıştı; orada depolar `~/projects/` altında
duruyordu. İkinci makinede aynı depolar `~/Documents/GitHub/` altında ve
`~/projects/` başka, ilgisiz bir dizin — yani manifest'teki `~/projects/…`
yolları o makinede **yok**. Bu yüzden tarama `topla.py` ile değil, kütüphaneyi
bozmayan `ekle.py` ile yapıldı (bkz. KURULUM.md § 3).

133 kaynak bulundu; 115'i kütüphanede zaten aynen vardı. Kalan 18'den 16'sı
girdi oldu, 1'i mevcut girdiyi tazeledi, 1'i atlandı.

**Yeni ad olarak gelen 8 skill**

| Skill | Nereden |
|---|---|
| `aso-optimizer`, `mobile-ux-architect`, `mobile-puzzle-game-ui-designer`, `mobile-puzzle-game-ux-audit-expert`, `tacet-ui-ux-design` | `~/.gemini/config/skills/` |
| `reklam-ve-performans` | `moonstone` |
| `sahibinden-arama` | `emlakarama` |
| `trip-konaklama-avcisi` | `tripsearch` |

**Ayrışmış sürüm olarak gelen 8 girdi**

`seo-expert--gemini`, `arayuz-denetimi--kartelapsikoloji-gh`,
`masifico-uretim-muhendisi--masifico-gh`, `oyuncak-mevzuat--masifico-gh`,
`mobilya-cad--mobilya-gh`, `gorsel-uretim--moonstone-gh`,
`moonstone-residence--moonstone-gh`, `setup-cowork--cloud`.

> Bu sekizinde **hangi sürümün daha yeni olduğu belirlenemedi:** kütüphanedeki
> kopyaların dosya zamanları toplama gününe (4 Eylül 2026) eşitlenmiş durumda,
> dolayısıyla mtime karşılaştırması anlamsız. Düz addaki girdi "daha yenidir"
> kuralı bu girdiler için **geçerli değil** — iki sürümü de tut, kullanmadan önce
> ikisini karşılaştır. `mobilya-cad`, `gorsel-uretim` ve `moonstone-residence`'ta
> iki makinenin kopyaları karşılıklı olarak birbirinde olmayan referans/script
> dosyaları taşıyor; birleştirilmeleri gerekebilir.

**Tazelenen 1 girdi.** `procedural-game-audio` — `dietrying` deposundaki kopya,
kütüphanedeki claude.ai kopyasının gerçek üst kümesiydi (aynı SKILL.md +
`references/theme-design.md`), yerinde tazelendi.

**Atlanan 1 kaynak.** `pipsworn` → `chibi-character-factory`: yalnızca
frontmatter sarımı ve son satır sonu farklıydı, içerikçe özdeş
(`scripts/ekle.py` içindeki `ATLA` kümesi).

**Taramaya girmeyen kaynaklar.** Bu makinede duran ama Faruk'un yazdığı skill
olmayan üç öbek `topla.py`'nin `HARIC` listesine eklendi:

| Konum | Adet | Ne |
|---|---|---|
| `~/.claude/plugins/cache/` | 70 | Resmî Vercel eklentisi (iki sürümü birden) ve `skill-creator` önbelleği |
| `~/.cursor/skills-cursor/` | 19 | Cursor'ın yerleşik skill'leri (`onboard`, `review`, `statusline`…) |
| `~/.claude/scheduled-tasks/` | 8 | Tek seferlik zamanlanmış görev promptları, yeniden kullanılabilir skill değil |
