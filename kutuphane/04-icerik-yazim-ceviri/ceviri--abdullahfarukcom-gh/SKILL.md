---
name: ceviri
description: Bir yazıyı Türkçe ile İngilizce arasında çevirir. Yazı eklendiğinde, mevcut bir yazının karşı dildeki sürümü eksik olduğunda ya da kullanıcı "bunu çevir", "İngilizcesini de yap", "iki dile de koy" dediğinde kullan. Çeviri, makine çevirisi gibi değil; aynı kültürel kodu taşıyan, B2 seviyesinde bir insanın yazdığı gibi olmalı.
---

# Yazı çevirisi

Bu sitede her yazının iki dilde de bulunması hedefleniyor. Çeviri mekanik bir
iş değil: okuyan kişi metnin çevrildiğini anlamamalı.

## Ölçüt

Çıkan metin, konuyu bilen ve karşı dili **B2 seviyesinde** kullanan bir insanın
kendi oturup yazdığı metin gibi olmalı. Bu iki şey demek:

- **Sadeleşme, bozulma değil.** Cümleler kısa ve doğrudan olsun, ama dilbilgisi
  kusursuz olsun. B2 demek "hatalı" demek değil, "gösterişsiz" demek.
- **Kültürel kod korunur.** Yazar Türkiye'den yazıyor. İngilizce sürümde de
  Türkiye'den yazan biri olarak kalır. Yerel örnekler silinmez, açıklanır.

## Yapılacaklar

### 1. Kaynağı oku, cümle cümle çevirme

Önce paragrafın ne dediğini anla, sonra o fikri hedef dilde yeniden kur.
Türkçenin uzun ve iç içe cümleleri İngilizcede bölünür; İngilizcenin kısa
cümleleri Türkçede birleşebilir. Paragraf sınırları ve sıralaması korunur.

### 2. Kültürel bağlamı taşı

- Yerel kurum ve marka adları (TÜBİTAK, Diyanet, Yıldız Teknik, Boyner,
  teknopark) **silinmez**. İngilizce sürümde kısa bir açıklama eklenir:
  "TÜBİTAK, the national science and technology council".
- Türkçe deyimler birebir çevrilmez. Karşılığı varsa karşılığı kullanılır,
  yoksa deyim düz anlatıma çevrilir. "Ayağın alışsın" -> "get them used to
  coming back".
- Para birimi, tarih ve ölçü biçimleri hedef dilin alışkanlığına uyar:
  `%64,3` -> `64.3%`, `19 Ağustos 2026` -> `19 August 2026`.

### 3. Yasaklar

Bunlar sitenin genel kuralları, çeviride de geçerli:

- **Tire yok.** Uzun tire (—), kısa tire (–) ve noktalama olarak " - "
  kullanılmaz. Yerine virgül, iki nokta, noktalı virgül, parantez veya yeni
  cümle. Markdown liste imleri muaf.
- **Yapay zekâ tikleri yok.** Şunlardan kaçın:
  - "Bu sadece X değil, aynı zamanda Y" / "It's not just X, it's Y"
  - Üçlü sıralama alışkanlığı ("hızlı, güvenli ve ölçeklenebilir")
  - Her paragrafta kalın vurgu. Kalın yazı yalnızca gerçekten tanım
    veriyorsa kullanılır, sayfada birkaç taneyi geçmez.
  - "Delve", "leverage", "robust", "seamless", "unlock", "dive into",
    "in today's fast-paced world"
  - Sonuç paragrafını "Sonuç olarak" / "In conclusion" ile açmak
- **Abartı yok.** Kaynak metin ne kadar iddialı ise çeviri de o kadar iddialı
  olur. Kaynakta olmayan bir sonuç cümlesi eklenmez.

### 4. Frontmatter

Karşı dildeki dosya `src/content/posts/<dil>/<slug>.md` yoluna yazılır.

| Alan | Kural |
| --- | --- |
| `title` | Çevrilir. Başlıkta tire yoksa çeviride de olmaz. |
| `description` | Çevrilir, tek cümle, 155 karakteri geçmez. |
| `date` | **Kaynakla aynı.** Çeviri tarihi değil, yazının tarihi. |
| `topics` | Aşağıdaki eşleşmeye göre çevrilir. |
| `featured`, `draft` | Kaynakla aynı. |
| `translationKey` | **İki dosyada da aynı olmalı.** Yoksa ikisine birden eklenir. Kaynakta yoksa İngilizce slug kullanılır. |
| `translatedFrom` | Çeviri olan dosyaya eklenir: `tr` ya da `en`. |
| `originalUrl`, `originalName` | Varsa kaynaktan **olduğu gibi** taşınır. Yazı ilk nerede yayımlandıysa orası değişmez. |

Konu eşleşmesi:

| Türkçe | English |
| --- | --- |
| Veri Bilimi | Data Science |
| Makine Öğrenmesi | Machine Learning |
| Yapay Zekâ | AI |
| Ürün Yönetimi | Product Management |
| Müşteri Deneyimi | Customer Experience |
| Strateji | Strategy |
| Yazılım | Software |
| DevOps | DevOps |
| Görüntü İşleme | Computer Vision |
| FinOps | FinOps |
| Karar Verme | Decision Making |

Listede olmayan bir konu çıkarsa hem çevirisini yap hem de bu tabloya ekle.

### 5. Gövde

- **Başlık sayısı ve sırası aynı kalır.** `##` sayısı iki dosyada eşit olmalı.
- **Görseller aynı dosyayı gösterir.** `/posts/<slug>/img-N.webp` yolu
  değişmez, yalnızca `alt` metni çevrilir. Görsel kopyalanmaz.
- **Kod blokları değişmez.** İçindeki yorum satırları çevrilebilir, kodun
  kendisi çevrilmez. Değişken ve fonksiyon adlarına dokunulmaz.
- **Site içi bağlantılar dil kökünü değiştirir:** `/tr/work/tacet` ->
  `/en/work/tacet`. Dış bağlantılar aynı kalır.
- Slug hedef dilde okunur olmalı: `veri-bilimi-notlari-5-lineer-regresyon` ->
  `data-science-notes-5-linear-regression`.

## Doğrulama

Çeviri bittikten sonra:

```bash
node -e "
const fs=require('fs');
import('./scripts/admin/markdown.mjs').then(m=>{
  for (const f of process.argv.slice(1)) {
    const raw = fs.readFileSync(f,'utf8');
    const { frontmatter, body } = m.splitFrontmatter(raw);
    console.log(f, '| tire:', m.lintDashes(raw).length,
                '| baslik:', (body.match(/^## /gm)||[]).length,
                '| gorsel:', (body.match(/!\[/g)||[]).length,
                '| kelime:', m.wordCount(body));
  }
});" src/content/posts/tr/KAYNAK.md src/content/posts/en/CEVIRI.md
```

İki dosyanın başlık ve görsel sayısı eşit olmalı, tire sayısı sıfır olmalı.
Kelime sayısı eşit olmayabilir: İngilizce genelde Türkçeden %10 ile %20
arasında daha uzun çıkar, bu normal.

Sonra `npm run build` ve `npm run check` hatasız bitmeli. Çeviri anahtarı
doğru eşleştiyse yazının başında "bu yazı diğer dilde de var" bağlantısı
görünür.

## Kontrol listesi

- [ ] `translationKey` iki dosyada aynı
- [ ] `date` kaynakla aynı
- [ ] `originalUrl` taşındı
- [ ] `translatedFrom` eklendi
- [ ] Tire yok
- [ ] Başlık ve görsel sayısı eşit
- [ ] Görsel yolları kaynakla aynı
- [ ] Yerel kurum adları korundu ve gerekiyorsa açıklandı
- [ ] Kalın vurgu sayfada birkaç taneyi geçmiyor
- [ ] `npm run build` ve `npm run check` temiz
