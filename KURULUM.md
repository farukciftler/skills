# Başka Bir Bilgisayarda Kurulum

Bu depo Faruk'un skill kütüphanesidir. Yeni bir makinede iki şey yapılır:
depoyu klonlamak, sonra o makinedeki skill'leri kütüphaneyle **karşılaştırmak**.

## 1 · Klonla

```bash
git clone https://github.com/farukciftler/skills.git ~/skills
cd ~/skills
```

Gereken tek şey Python 3 (macOS'ta yerleşik). Bağımlılık yok.

## 2 · Global skill'leri kur

`~/.claude/skills/` altındaki skill'ler her projede yüklenir. Kütüphanedeki
karşılıklarını oraya bağla:

```bash
mkdir -p ~/.claude/skills
for s in headless-reel-forge ml-expert mobile-ux-flow-expert web-ux-flow-expert startup-degerleme; do
  hedef=$(find ~/skills/kutuphane -maxdepth 2 -type d -name "$s" | head -1)
  [ -n "$hedef" ] && [ ! -e ~/.claude/skills/"$s" ] && ln -s "$hedef" ~/.claude/skills/"$s"
done
ls -l ~/.claude/skills/
```

Başka bir skill'i de global yapmak istersen aynı kalıpla ekle. Hangi skill'in
ne yaptığı için [INDEX.md](INDEX.md).

## 3 · Bu makinede fazladan skill var mı, bak

Asıl mesele bu: başka bilgisayarındaki projelerde burada olmayan skill'ler
olabilir. `topla.py` bunu tespit eder.

```bash
python3 scripts/topla.py
```

Çıktı, bu makinede bulunan kaynakları ve kütüphane girdilerini sayar.
Kütüphanede karşılığı olmayan bir ad varsa `99-siniflandirilmamis` uyarısı
verir. Kütüphaneye almak için:

```bash
python3 scripts/topla.py --uygula     # yeni bulunanları kutuphane/ altına ekler
python3 scripts/katalog_uret.py       # INDEX + katalog + kategori README'leri
git add -A && git commit -m "…makinesinden N skill eklendi" && git push
```

> `topla.py` mevcut kütüphane girdilerinin **üzerine yazmaz** — yalnız eksik
> olanları ekler. Aynı isimli ama içeriği farklı bir skill bulursa onu
> `--<kaynak>` ekiyle ayrı girdi olarak alır, hiçbir şey kaybolmaz.

Yeni bir skill kategori eşlemesinde yoksa iki dosyaya birden eklenmeli:
`scripts/topla.py` içindeki `KATEGORI`, `scripts/katalog_uret.py` içindeki
`KATEGORI_BASLIK`.

## 4 · İsteğe bağlı: proje skill'lerini kütüphaneye bağla

Proje depolarındaki `.claude/skills/<ad>` dizinlerini kütüphaneye symlink
yapmak, skill'i tek yerden düzenlemeni sağlar. **Geri dönüşü zahmetli bir
adımdır** ve git deposunda silme + symlink olarak görünür — depo başına ilerle:

```bash
python3 scripts/bagla.py                          # tüm kapsamı göster
python3 scripts/bagla.py --proje <depo-adı>       # tek depo, kuru çalıştırma
python3 scripts/bagla.py --proje <depo-adı> --uygula
```

`bagla.py` bir kaynağı, kütüphanedeki kopyayla birebir aynı olduğunu
doğrulamadan değiştirmez. Geri alma: `python3 scripts/coz.py --uygula`.

Ayrıntı ve makineler arası ayrışma uyarıları: [TASIMA.md](TASIMA.md).

## Makineler arası çalışırken

Kütüphane git ile senkronlanır, **symlink'ler senkronlanmaz** —
`katalog/baglanti-kaydi.json` her makinede kendi kaydını tutar ve depoya
girmez. Yani her makinede 2. ve 4. adımı ayrıca çalıştırırsın; içerik ortaktır.

Bir makinede bir skill'i düzenledikten sonra:

```bash
python3 scripts/katalog_uret.py && git add -A && git commit -m "…" && git push
```

Diğer makinede `git pull` yeter; symlink'ler zaten kütüphaneye baktığı için
güncel içerik anında geçerli olur.
