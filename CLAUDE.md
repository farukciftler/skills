# CLAUDE.md — Skill Kütüphanesi

Bu dizin Faruk'un tüm Claude skill'lerinin **kataloğu ve arşividir**. Burası bir
kod deposu değil; her alt dizin başka bir yerde çalışan (ya da çalışması gereken)
bir skill'in kopyasıdır.

## Önce bunu bil: buradaki kopya çalışan skill değil

`kutuphane/` altındaki dosyalar Claude tarafından **otomatik yüklenmez**. Bir
skill'in gerçekten tetiklenmesi için kurulu olduğu yerde durması gerekir:

| Konum | Ne yükler |
|---|---|
| `~/.claude/skills/<ad>/` | Her oturumda, her projede |
| `<proje>/.claude/skills/<ad>/` | Yalnız o proje açıkken |
| claude.ai senkronu | Desktop/web oturumlarında, `anthropic-skills:` ön ekiyle |

Bu yüzden buradaki bir dosyayı düzenlemek, o skill'in davranışını **değiştirmez**
— kaynak konumu da güncellenmeli. Kalıcı çözüm için `TASIMA.md`'deki bağlama
(symlink) adımına bak; bağlandıktan sonra kütüphane gerçek tek kaynak olur.

## Bir skill ararken

1. **[INDEX.md](INDEX.md)** — 160 girdilik alfabetik tablo, tek satırlık özetlerle.
2. **`katalog/skills.json`** — programatik arama için. Her kayıtta `ad`, `ozet`,
   `aciklama` (tam frontmatter), `kategori`, `yol`, `kaynaklar`, `script_var`.
3. Kategori sayfaları — `kutuphane/<kategori>/README.md`, o alandaki her skill'in
   tam açıklamasıyla.

Konu bazlı arama için `katalog/skills.json` üzerinden grep, dosya ağacında
gezinmekten hızlıdır:

```bash
python3 -c "import json;[print(f\"{x['ad']:34} {x['ozet'][:70]}\") for x in json.load(open('katalog/skills.json')) if 'vergi' in x['aciklama'].lower()]"
```

## Adlandırma kuralı

Çoğu girdi düz adıyla durur. `--` içeren adlar **ayrışmış sürümlerdir**:

- `weft-channel` / `weft-channel--weftrecords-gh` → aynı skill, iki repo klonunda
  farklı içerikte. Düz ad **daha yeni** olandır.
- `ceviri--comesyriacontent` / `ceviri--abdullahfarukcom-gh` → aynı isimli ama
  **gerçekten farklı iki skill**. İkisi de eklenti alır; birini diğeri sanma.
- `--cloud` ekli olanlar claude.ai'daki kopyadır ve genelde **daha eskidir**
  (bkz. `TASIMA.md` § Bayat cloud kopyaları). claude.ai önbelleğinde birden
  çok oturum anlık görüntüsü durur; tarama hepsine bakar ama bir ad en yeni
  görüntüde varsa eskilerdeki kopyası elenir — eskiden gelen tek şey,
  claude.ai'dan **silinmiş** skill'lerdir (bkz. § Eski bulut anlık görüntüsü).
- İkinci makine taramasından gelen 8 girdide **"düz ad daha yenidir" kuralı
  geçerli değil** — hangisinin yeni olduğu belirlenemedi. Listesi ve gerekçesi:
  `TASIMA.md` § İkinci makine taraması.

Bir skill üzerinde çalışırken hangi sürümün doğru olduğundan emin değilsen
`katalog/manifest.json`'daki `srcs` alanına bak — her sürümün geldiği gerçek yol
orada.

## Bu skill'lerin ortak sözleşmeleri

Korpusu okurken tekrar eden ve **korunması gereken** desenler:

- **Ezberden veri yok.** Fiyat, kur, mevzuat haddi, randevu tarihi, model fiyatı
  içeren skill'lerin neredeyse hepsi "canlı doğrula + tarih damgası koy" kuralı
  taşıyor. Bir skill'i düzenlerken bu kuralı yumuşatma.
- **Referanslar talep üzerine okunur.** `references/` dosyaları kasıtlı olarak
  SKILL.md'nin dışında; hepsini birden okumak bütçe israfıdır. SKILL.md'deki
  yönlendirme tablosuna uy.
- **Script varsa aritmetiği elle yapma.** 46 skill'de `scripts/` var (ör.
  `aso_calc.py`, `helal_hesap.py`, `ev_analiz.py`, `pt.py`). Hesap çıktıya
  gidiyorsa script'i çalıştır.
- **Sınırlar açıkça yazılı.** Skill'ler "ne yapmaz"ını söylüyor (fetva vermez,
  yatırım tavsiyesi değildir, avukat değildir, ekspertizin yerini almaz). Bu
  bölümleri kırpma.
- **Dil.** Türkiye'ye özgü olanlar Türkçe, uluslararası/teknik olanlar İngilizce
  yazılmış. Bir skill'i düzenlerken mevcut dilinde kal.

## Skill eklerken veya düzenlerken

1. Skill'i **kaynak konumunda** yaz veya düzenle (`~/.claude/skills/…` ya da
   `<proje>/.claude/skills/…`). Yeni skill yazımı için `skill-creator`
   (`kutuphane/14-meta-sistem/skill-creator/`) kullanılır.
2. Kütüphaneyi ve kataloğu tazele:
   ```bash
   python3 scripts/katalog_uret.py
   ```
3. Yeni bir skill kaynak konumdan kütüphaneye alınacaksa `scripts/ekle.py`
   çalıştır (tarar, yalnız eksik/ayrışmış içeriği kopyalar, manifest'e ekler).
   `scripts/topla.py --uygula` yalnız ilk kurulum içindir — manifest'i sıfırdan
   yazdığı için ikinci bir makinede çalıştırılırsa öteki makinenin girdilerini
   katalogdan düşürür.

Kategori ekleme/değiştirme: `scripts/katalog_uret.py` içindeki
`KATEGORI_BASLIK` sözlüğü ile `scripts/topla.py` içindeki `KATEGORI` eşlemesi
birlikte güncellenmeli.

## Dokunma

- `kutuphane/` altındaki dosyaları **kaynağı güncellemeden** düzenleme — sessizce
  ayrışır.
- `katalog/skills.json`, `katalog/skills.csv`, `INDEX.md` ve kategori
  `README.md`'leri **üretilmiş çıktıdır**; elle düzenleme, `katalog_uret.py`
  ezer. Kalıcı değişiklik script'te yapılır.
- `katalog/manifest.json` taşıma kaydıdır; `scripts/topla.py` dışında yazma.
