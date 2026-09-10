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
geldi (§ İkinci makine taraması). Son olarak claude.ai önbelleğinin eski
oturum anlık görüntüleri tarandı ve yalnız orada kalan 5 skill eklendi
(§ Eski bulut anlık görüntüsü). **Güncel toplam: 143 benzersiz skill, 170 girdi, 15 kategori.**
(Yukarıdaki 14 kategori ilk taşımanın hâlidir; 15'incisi 10 Eylül'de açıldı,
bkz. § Oyun geliştirme kategorisi.)

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

## Eski bulut anlık görüntüsü (4 Eylül 2026)

`topla.py` claude.ai önbelleğinden **yalnız en yeni** anlık görüntüyü okuyordu.
Önbellekte üç görüntü var:

| Görüntü | Tarih | Skill |
|---|---|---|
| `19b5885a…/15af82d8…` | 4 Eyl 2026 | 49 — claude.ai'ın **güncel** hâli |
| `19b5885a…/f181d07d…` | 26 Ağu 2026 | 36 |
| `2fee50bc…/f181d07d…` | 26 Ağu 2026 | 35 |

En eski görüntüde, güncel claude.ai listesinde **artık olmayan** 5 skill duruyordu;
yerel önbellek bunların elde kalan tek kopyasıydı:

| Skill | Boyut | Kategori |
|---|---|---|
| `finops-expert` | 84 K, 6 dosya | 07-yazilim-muhendislik |
| `tesvik-avcisi` | 68 K, 7 dosya | 01-finans-yatirim |
| `trend-setter` | 60 K, 7 dosya | 04-icerik-yazim-ceviri |
| `hypercasual-lab` | 48 K, 5 dosya | 05-pazarlama-buyume |
| `product-self-knowledge` | 4 K, 1 dosya | 14-meta-sistem |

Aynı görüntü `physics-reel-forge`'un kütüphanede eksik olan 4 script'ini de
taşıyordu; girdi yerinde tazelendi (üst küme, ayrı girdi açılmadı):
`synth_impacts.py` (18,7 K) · `batch_render.py` (15,2 K) · `encode_reel.sh` (6,7 K) ·
`preflight.sh` (4,8 K).

### Tarama nasıl düzeltildi

`cloud_dizini()` → `cloud_dizinleri()`: artık **tüm** anlık görüntüler taranıyor.
Gürültüyü `ekle.py` içindeki `en_yeni_cloud()` eliyor — bir ad en yeni görüntüde
varsa eskilerdeki kopyası aday sayılmaz, çünkü tanım gereği geridedir. Bu kural
olmasa `docx`, `pptx`, `xlsx` ve `setup-cowork` için dört `--cloud` girdisi daha
açılırdı.

Kuralın dışında kalan, yalnız eski görüntüde duran ama kütüphanedeki kopyası
**ileride** olan ikisi `ekle.py`'ın `ATLA` listesine yazıldı:

| Skill | Kütüphanedeki kopyanın fazlası |
|---|---|
| `ucuz-bilet-avcisi` | `scripts/fiyat_deposu.py` içinde `from __future__ import annotations` |
| `ambient-video-forge` | `check_env.sh` macOS `sysctl` ve ffmpeg 8.x filtre düzeltmeleri; `presets.json` 2,7 K daha dolu |

### Buluta geri yüklenmesi gerekenler

Bu taramada, kütüphanedeki sürümün claude.ai'dakinden ileride olduğu bir vaka
daha çıktı — § Bayat cloud kopyaları listesine ek:

| Skill | Bulutta eksik olan |
|---|---|
| `procedural-game-audio` | `references/theme-design.md` (4,8 K) |


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

## Terminale kurma (8 Eylül 2026 — yapıldı)

`bagla.py` kurulum noktalarını kütüphaneye bağlar; `kur.py` tersini yapar —
kütüphanedeki her girdiyi `~/.claude/skills/<ad>` altına symlink'leyerek her
projedeki `claude` oturumunda yüklenir hale getirir.

```bash
python3 scripts/kur.py               # ne olacağını göster
python3 scripts/kur.py --uygula      # kur
python3 scripts/kur.py --coz --uygula  # tümünü geri al
```

Sonuç: **142 skill kuruldu** — 137 yeni symlink, 5 mevcut gerçek dizin
(`headless-reel-forge`, `ml-expert`, `mobile-ux-flow-expert`,
`startup-degerleme`, `web-ux-flow-expert`) içerikçe birebir aynı doğrulanıp
symlink'e dönüştürüldü. Kayıt: `katalog/kurulum-kaydi.json` (git dışı).

### Ad çakışması — kurulmayan 27 sürüm

`~/.claude/skills/<ad>` tek dizindir; aynı adın ayrışmış sürümleri aynı anda
kurulamaz. Ad başına tek kazanan seçilir:

1. slug'ı adın kendisi olan (düz ad) — CLAUDE.md'ye göre daha yeni;
2. yoksa `--cloud` ekli **olmayan** (bayat bulut kopyası elenir);
3. yoksa en büyük içerik.

Bu kural `masifico-*` ve `oyuncak-mevzuat`'ta doğru sonucu veriyor: proje
sürümü kazanıyor, § Bayat claude.ai kopyaları tablosuyla uyumlu. `ceviri`'de
ise § Aynı isim, farklı skill vakası devrede — `--comesyriacontent` kuruldu,
`--abdullahfarukcom-gh` **terminalde erişilemez**; ikisi farklı iş olduğu için
bu bir kayıptır, ihtiyaç olursa ayrı bir adla kurulmalı.

Elenen sürümlerin tam listesi için `python3 scripts/kur.py` (kuru çalıştırma).

### Kurulum dizini adı, frontmatter'a göre seçilir

Claude Code dizin adıyla SKILL.md frontmatter'ındaki `name` alanının uyuşmasını
bekler, o yüzden `kur.py` geçerli bir slug ise frontmatter adını kullanır:

| Kütüphane slug'ı | Kurulan ad | Not |
|---|---|---|
| `kaggle-kaggle-skill` | `kaggle-kaggle-competitor` | frontmatter adı esas alındı |
| `backlog` | — | frontmatter'ı `backlog-arastir` diyor, gerçek `backlog-arastir` girdisine yenildi (doğru sonuç: `backlog`, `comesyriacontent/backlog` veri dizini) |
| `postgresql` | `postgresql` | frontmatter `name: PostgreSQL Database Administration` — slug değil, manifest adına düşüldü. **Düzeltilmeli.** |

### Kurulmayan kalıntı

`~/.claude/skills/_backup-164414/headless-reel-forge` — üst düzeyinde SKILL.md
olmadığı için skill olarak yüklenmiyor, ama kütüphanedeki **iki** sürümde de
olmayan içerik taşıyor: `assets/materials.json` ve bir `recipes/` dizini
(`references/procedural-audio.md` de farklı). Silinmedi; üçüncü bir ayrışmış
sürüm olarak kütüphaneye alınıp alınmayacağı karara bağlı.

## Sürüklenme taraması (8 Eylül 2026)

Ev dizinindeki 2.363 `SKILL.md`'nin tamamı sınıflandırıldı. **Kütüphanede
bulunmayan tek bir skill çıkmadı**; `topla.py`'nin görmediği 1.952 konumun
hepsi üçüncü taraf: `.claude/remote/plugins/` (1.674), worktree kopyaları
(150), `rpm/plugin_*/skills/` altındaki Anthropic eklenti paketleri (64,
`plugin.json`'da `"author": "Anthropic"`), marketplace (31), IDE eklentileri
(27) ve Playwright paketi içinden çıkan 4 dosya. `~/Downloads`'taki 13
`.skill` paketinin 13'ü de kütüphanede.

Çıkan şey eksik skill değil, **kütüphanenin geride kalması**. Proje
kopyaları kütüphaneden bağımsız olduğu için ilerlemeye devam ediyor:

| Girdi | Yeni kaynak | Fark | Yapılan |
|---|---|---|---|
| `portfoy-tahmin` | `~/projects/portfoy-butce` (7 Eyl) | kaynakta +482 satır, kütüphanede +6 | tazelendi |
| `tahmin-savcisi` | `~/projects/portfoy-butce` (7 Eyl) | kaynakta +31, kütüphanede +1 | tazelendi |
| `ceviri--abdullahfarukcom-gh` | `~/projects/abdullahfarukcom` (7 Eyl) | kaynakta +2 sözlük satırı | tazelendi |
| `finops-expert` | `~/projects/Cloud4Next` (7 Eyl) | karşılıklı: kütüphanede `ai-finops.md`, kaynakta `cloud4next-platform.md` + 3 referans | `--cloud4next` yeni girdi |

Üzerine yazılan satırlar denetlendi: `portfoy-tahmin`'deki 6 satır `pt.py`
içinde iki kez yazılmış aynı bloktu (yeni sürüm temizlemiş),
`tahmin-savcisi`'ndeki 1 satır yeniden yazılmış bir cümleydi. Kayıp yok.

`finops-expert--cloud4next` ad çakışmasında düz ada yeniliyor, yani
terminalde kurulu değil; yalnız `~/projects/Cloud4Next` içinde yükleniyor.
Bu doğru davranış: kütüphanedeki sürüm genel FinOps skill'i, Cloud4Next
sürümü o platforma özgü.

### Gölgeleme somutlaştı

`kur.py` sonrası uyarılan risk gerçekleşmişti: `portfoy-tahmin` global
symlink'ten kütüphanenin 3 Eylül sürümünü yüklüyordu ve proje kopyası
yalnız `~/projects/portfoy-butce` içinde onu gölgeliyordu. Yani o projenin
dışındaki her oturum 482 satır eski sürümle çalışıyordu. Tazeleme bunu
kapattı, ama **yapısal olarak tekrar açılacak**: proje kurulumları
kütüphaneye `bagla.py` ile bağlanmadıkça her düzenleme aynı boşluğu yeniden
üretir.

### Kalan: klonlar hizasız

Tazeleme sonrası `ekle.py` üç aday bırakıyor, üçü de aynı depoların
`Documents/GitHub/` klonundan:

```
ceviri--abdullahfarukcom-gh-2   <- ~/Documents/GitHub/abdullahfarukcom/.claude/skills/ceviri
portfoy-tahmin--portfoy-butce-gh <- ~/Documents/GitHub/portfoy-butce/.claude/skills/portfoy-tahmin
tahmin-savcisi--portfoy-butce-gh <- ~/Documents/GitHub/portfoy-butce/.claude/skills/tahmin-savcisi
```

Bunlar **kasıtlı olarak eklenmedi**; varyant açmak `portfoy-tahmin`'in
dördüncü kopyasını üretir ve hangisinin canlı olduğunu bulanıklaştırır. Bu
bir kütüphane sorunu değil, git klonu hizasızlığı: `projects/` ve
`Documents/GitHub/` aynı depoların ayrı klonları ve `projects/` iki gün
önde. § Ayrışmış sürümler'in zaten şart koştuğu klon hizalaması yapılmadan
bu üçü kapanmaz.

## Oyun geliştirme kategorisi (10 Eylül 2026)

Downloads'tan dört oyun geliştirme skill'i geldi; dördü de claude.ai anlık
görüntüsündeki kopyayla bit bit aynı çıktı ve normal tarama yoluyla alındı:

| Skill | Dosya | Ne yapar |
|---|---|---|
| `pixel-platformer-animator` | 12 | Pixel karakter sprite seti üretir, Unity 6'ya Animator + prefab olarak sokar |
| `blender-unity-character-pipeline` | 18 | Blender'da humanoid rig/skin/animasyon, FBX ile Unity avatar ve blend tree |
| `narrative-platformer-design` | 15 | 2D platformer anlatısı, beat chart, diyalog; AI-tell lint araçlarıyla |
| `oyun-asset-kesif` | 7 | Ücretsiz asset arama (API + web), lisans denetimi, CREDITS kaydı |

**Yeni kategori açıldı: `15-oyun-gelistirme`.** Dördünü mevcut kategorilere
dağıtmak (Blender karakteri 09'a, anlatı 04'e, asset keşfi 10'a) tek bir işin
parçalarını böler; ikisi doğrudan birbirine bağlanıyor
(`oyun-asset-kesif` → `blender-unity-character-pipeline`, ikisi de Unity'ye
aynı yoldan giriyor). CLAUDE.md'nin şart koştuğu gibi `topla.py`'deki
`KATEGORI` ile `katalog_uret.py`'deki `KATEGORI_BASLIK` birlikte güncellendi.

### Açık kalan: mevcut oyun skill'leri hâlâ dağınık

Kütüphanede beş oyun skill'i daha var ve hepsi başka kategoride duruyor:

| Skill | Şu anki kategori |
|---|---|
| `chibi-character-factory` | 03-video-ses-uretim |
| `procedural-game-audio` | 03-video-ses-uretim |
| `hypercasual-lab` | 05-pazarlama-buyume |
| `mobile-puzzle-game-ui-designer` | 06-ux-urun |
| `mobile-puzzle-game-ux-audit-expert` | 06-ux-urun |

Bunlar **taşınmadı**. Bir kütüphane girdisini kategoriler arası taşımak yolunu
değiştirir, yani `~/.claude/skills/<ad>` symlink'i kırılır ve `kur.py` bunu
"başka bir symlink" diye atlar; taşıma ayrı bir işlem olarak, symlink'leri
yeniden kurarak yapılmalı. Konsolide edilirse `15-oyun-gelistirme` dokuz
girdiye çıkar ve `03`, `05`, `06` sırasıyla iki, bir ve iki girdi kaybeder.

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
