# Yapay Zeka Üretimi Metnin Dilsel İmzaları ve Bunlardan Kaçınma Kılavuzu

## 0. Bu belgenin mantığı

Aşağıdaki listeler "AI tespit aracını atlatma" listesi değil. Ölçülmüş bulgulara dayanan bir gözlem var: talimatla eğitilmiş (instruction-tuned) dil modelleri, insanların yazdığından **istatistiksel olarak ayrışan** dar bir üslup bandında yazıyor. Reinhart ve ark. (2025) bu farkı doğrudan ölçtü: temel (base) Llama 3 modelleri insan metnine yakın davranırken, talimatla eğitilmiş sürümler insandan **uzaklaşıyor**. Yani "insanlaştırma" eğitimi modelleri insana benzetmemiş, hepsini aynı tek üsluba sıkıştırmış:

> "instruction tuning appears to make the model output less human, not more"
> — Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G. (2024/2025), *Do LLMs write like humans? Variation in grammatical and rhetorical styles*, arXiv:2410.16107, PNAS 122 (2025). <https://arxiv.org/abs/2410.16107>

Sonuç olarak bu imzalardan kaçınmak, tespit aracını kandırmakla değil, **daha iyi yazmakla** aynı şey. Belgeyi bu varsayımla kurdum.

---

## 1. NOKTALAMA İMZALARI

### 1.1 Uzun çizgi (em dash, U+2014) — ölçülmüş veriler

Uzun çizginin en çok konuşulan AI belirteci olmasının nedeni artık anekdot değil; nüfus düzeyinde ölçüldü.

**medRxiv çalışması (ön kayıtlı):**
Czuma, P. (2026), *Em-ergence of the em-dash: a population-level rise in em-dash frequency in medRxiv preprints at the dawn of the large-language-model era*, arXiv:2606.29540. <https://arxiv.org/abs/2606.29540> (OSF ön kayıt: HFT8C)

- Örneklem: 2020–2025 arası medRxiv ön baskılarının tam metin XML'i, ilk sürümler, Discussion bölümü ≥500 karakter, **N = 69.632**
- Discussion bölümünde en az bir em dash bulunma oranı:
  - ChatGPT öncesi (30 Kasım 2022 öncesi): **%4,23**
  - ChatGPT sonrası: **%11,58**
  - Mutlak artış: **+7,35 puan** (%95 GA 6,94–7,77), **olasılık oranı 2,96** (%95 GA 2,77–3,17)
- Yıllara göre kırılım — ani sıçrama değil, **gecikmeli hızlanma**:
  - 2023 boyunca: ~%4
  - 2024: **%8,0**
  - 2025: **%20,3**
- Plasebo testi (LLM öncesi dönem içinde yapay bölme): +0,13 puan (%95 GA −0,33 ile +0,58) → anlamsız. Yani artış yöntemsel bir yapaylık değil.
- Kalıp (boilerplate) bölümlerde etki neredeyse yok → sinyal, insanın gerçekten yazdığı yerlerde.
- Etki tüm duyarlılık analizlerinde ayakta kaldı (7,35–7,60 puan aralığı) ve iki yanlışlama testini de geçti.

**ABD Kongresi basın bültenleri çalışması:**
Czuma, P. (2026), *The em-dash em-beds in Congress: A population-level rise in em-dash frequency in U.S. congressional press releases at the dawn of the large-language-model era, 2021-2025*, arXiv:2608.05889. <https://arxiv.org/abs/2608.05889> (OSF: 10.17605/OSF.IO/U5NEY)

- 480 Temsilciler Meclisi ve Senato ofisinden **146.239** basın bülteni, 2021–2025
- Ölçüm: boşluksuz, düzyazı biçimli em dash yoğunluğu (1.000 karakter başına). Not: `word---word` biçimi tipografik İngilizcede normaldir ama ABD basın yazımında AP stili **boşluklu** tire ister — bu yüzden boşluksuz biçim orada özellikle sırıtır.
  - 2021–2024: **0,10–0,12** arası sabit
  - 2025: **0,217** → dört yıllık taban çizgisinin iki katından fazla
- En az bir em dash içeren bülten oranı: **~%13 → %24,8**
- Frekans oranı (2023–2025 / 2021–2022): **1,55** (%95 GA 1,28–1,93; kayıtlı kesme değeri 1,528)
- Tire (hyphen) yoğunluğu sabit kaldı → artış "net-yeni", biçimlendirme kaymasından değil
- 262 sürekli ofisin **%75,6'sı** artış gösterdi (p ≈ 1e-16); 224 ofislik kapalı panelde de aynı
- Artış parti ve kanat bakımından simetrik; ChatGPT kesme noktasında basamak yok, sonrasında hızlanma var
- Yazarın kendi uyarısı: bu **nüfus düzeyinde bir gösterge**, tek bir metin için yazarlık dedektörü değil.

**Mekanizma açıklaması — em dash neden var:**
Freeburg, E. M. (2026), *The Last Fingerprint: How Markdown Training Shapes LLM Prose*, arXiv:2603.27006. <https://arxiv.org/abs/2603.27006>

- Tez: em dash, **markdown'ın düzyazıya sızmasıdır** — modelin markdown-doygun eğitim verisinden edindiği yapısal yönelimin hayatta kalan en küçük birimi.
- Beş sağlayıcıdan (Anthropic, OpenAI, Meta, Google, DeepSeek) **12 model** üzerinde iki koşullu bastırma deneyi: "markdown kullanma" talimatı verildiğinde başlıklar, madde işaretleri ve kalın yazı **ortadan kalkıyor**, ama em dash **kalıyor**. İstisna: Meta'nın Llama modelleri hiç üretmiyor.
- Frekans aralığı: **1.000 kelimede 0,0** (Llama) ile **9,1** (GPT-4.1, bastırma altında) arası.
- Üç koşullu bastırma gradyanı: açık em dash yasağı bile bazı modellerde eseri silmiyor. Base-vs-instruct karşılaştırması gizli eğilimin RLHF öncesinde de var olduğunu gösteriyor.
- Pratik sonuç: em dash sıklığı bir **üslup kusuru değil, ince ayar yönteminin parmak izi**. Bu yüzden "bir tane bile kullanma" demek yerine, insan yazısının doğal em dash oranını hedeflemek gerekir.

### 1.2 Noktalama kuralları — kaçınılacaklar listesi

**Aşırı kullanılan (AZALT):**
- `—` em dash (özellikle boşluksuz `word—word` biçimi)
- `:` iki nokta üst üste — özellikle "Here's the thing:" / "The result: X" / madde başlığı sonrası
- `;` noktalı virgül — LLM'ler iki bağımsız cümleyi noktalı virgülle bağlamayı fazla seviyor; insanlar genelde nokta koyar
- `"` `"` kıvrık tırnak ve `'` kıvrık kesme işareti — bir editörden geçmemiş insan metninde genellikle düz `"` ve `'` bulunur; kıvrık tipografi otomatik üretim sinyalidir
- `…` tek karakterlik üç nokta (U+2026) — insanlar `...` yazar
- `**kalın başlık:**` + açıklama kalıbı
- Oxford virgülü — tek başına imza değil ama **%100 tutarlı** Oxford virgülü kullanımı imzadır; insan yazarlar tutarsızdır
- Parantez içi açıklamalar; `(i.e., …)` ve `(e.g., …)` LLM'lerde insanlardan sık
- `/` eğik çizgiyle ikili sunum ("clarity/precision")

**Az kullanılan (ARTIR):**
- `!` ünlem — Reinhart ve ark. LLM'lerin ünlemden kaçındığını bulguladı
- Kısaltmalar/contraction: `don't`, `won't`, `it's`, `you're`, `I'd`, `we'll`
- Cümle parçaları (fragment). Nokta. Sonra devam.
- Küfür, argo ve kaba sözcükler — Reinhart ve ark. (2025) LLM'lerin bazı küfürleri insanlardan **100 kattan fazla az** kullandığını ölçtü (SI Appendix Table S8)
- Tek tırnak içinde ironi, soru işaretiyle biten yarım cümle, düz `-` tire
- Ara cümleyi parantezle değil virgülle vermek

**Somut kural:** 1.000 kelimede en fazla 1–2 em dash. Onların yerini virgül, nokta, parantez ve iki ayrı cümle alsın.

---

## 2. KELİME VE KALIP İMZALARI (İngilizce)

### 2.1 Akademik kaynak: PubMed'de aşırı kelime kullanımı

Kobak, D., González-Márquez, R., Horvát, E.-Á., Lause, J. (2024/2025), *Delving into ChatGPT usage in academic writing through excess vocabulary*, arXiv:2406.07016; *Science Advances* 11(27), eadt3813 (Temmuz 2025). <https://arxiv.org/abs/2406.07016>

Yöntem: 2010–2024 arası **15 milyondan fazla** PubMed özeti. COVID döneminden ödünç alınan "aşırı ölüm" (excess mortality) mantığı kelimelere uygulandı: gözlenen frekans P ile karşı-olgusal beklenen frekans Q karşılaştırıldı; frekans farkı Δ = P − Q ve **aşırı frekans oranı r = p/q**.

**Bulunan somut oranlar (2024):**

| Kelime | Aşırı frekans oranı r |
|---|---|
| **delves** | **28,0×** |
| **underscores** | **10,9×** |
| **showcasing** | **10,2×** |

- Toplam **829 benzersiz aşırı kelime** tespit edildi; bunların **319'u üslup kelimesi** (content/içerik kelimesi değil).
- Kritik nitel bulgu: önceki yıllarda aşırı kelimeler içerik isimleriydi (*ebola*, *zika*, *omicron*, *lockdown*, *pandemic*, *coronavirus*, *sars*, *pfizer*). 2023–24'te ise **fiil ve sıfat** oldular. Bu, kelime dağarcığındaki kaymanın konu değil **üslup** kaynaklı olduğunun kanıtı.
- Makalenin şekillerinde etiketlenmiş aşırı kelimeler: *delves, delved, delve, delving, showcasing, underscores, underscore, surpassing, intricate, excels, pivotal, insights, comprehensive, notably, utilizing, potential, findings, crucial, emphasizing, enhancing, offering, noteworthy, mash*
- LLM ile işlenmiş 2024 özetlerinin oranı için alt sınır: **en az %10** (arXiv sürümü) / yayımlanmış sürümde **%13,5**; bazı alt kümelerde **%40**'a kadar. Bu bir **alt sınır** — hiç işaret kelimesi kullanmayan özetler sayılmıyor.
- Yılda ~1,5 milyon PubMed makalesi → **yılda en az 150.000 makale** LLM yardımıyla yazılıyor.
- Yazarların ifadesiyle etki, "COVID pandemisi gibi büyük dünya olaylarının etkisini aşıyor".

**Alt grup heterojenliği (Δ değerleri) — bu, "kim yakalanıyor" sorusunun cevabı:**

| Alt grup | Δ |
|---|---|
| Hesaplamalı alanlar (computation, bioinformatics) | ≈ 0,20 |
| Çin, Güney Kore, Tayvan | > 0,15 |
| Birleşik Krallık, Avustralya | ≤ 0,04 |
| *Sensors* (MDPI) | 0,24 |
| *Cureus* (Springer Nature) | 0,19 |
| MDPI dergileri (havuz) | 0,19 |
| Frontiers dergileri (havuz) | 0,18 |
| Nature / Science / Cell | 0,06 |
| Nature ailesi dergiler | 0,08 |

Erkek/kadın yazar farkı önemsiz (0,09 / 0,07–0,08). Yazarların yorumu: kolayca tespit edilebilir LLM kullanımı, algılanan prestijle **negatif** korele.

**Makalede alıntılanan gerçek 2023 özet cümleleri (kaçınılacak üslubun canlı örneği):**

> "By **meticulously delving into the intricate web** connecting [...] and [...], this **comprehensive** chapter takes a **deep dive** into their involvement as significant risk factors for [...]."

> "A **comprehensive grasp** of the **intricate interplay** between [...] and [...] is **pivotal** for effective therapeutic strategies."

> "**Initially, we delve into the intricacies** of [...], **accentuating its indispensability** in cellular physiology, the **enzymatic labyrinth** governing its flux, and the **pivotal** [...] mechanisms."

Kobak ve ark. ayrıca önceki çalışmaları özetliyor: Gray (2024) *intricate* ve *meticulously* için 2023'te **2 kat** artış buldu; Liang ve ark. (2024) *pivotal, intricate, showcasing, realm* kelimelerini en çok LLM tercihli kelimeler olarak belirledi.

### 2.2 İkinci akademik kaynak: kat kat artış tabloları

Reinhart ve ark. (2024/2025), arXiv:2410.16107, Tablo 1 — **"LLM metinlerinde insan kullanımına göre en aşırı temsil edilen kelimeler"** (rakamlar insan oranına göre kat):

**GPT-4o:**
| Kelime | Kat |
|---|---|
| camaraderie | 162× |
| tapestry | 155× |
| intricate | 119× |
| underscore | 107× |
| unspoken | 102× |
| amidst | 100× |
| palpable | 95× |
| solace | 95× |
| fleeting | 84× |
| unravel | 83× |

**GPT-4o Mini:**
| Kelime | Kat |
|---|---|
| camaraderie | 171× |
| tapestry | 147× |
| palpable | 145× |
| grapple | 131× |
| intricate | 129× |
| fleeting | 124× |
| ignite | 122× |
| vibrant | 92× |
| amidst | 90× |
| cacophony | 89× |

**Llama 3 70B Instruct:** *unease* 63×, *palpable* 47×, *continuation* 29×, *shoutout* 28×, *intricate* 27×, *pang* 25×, *camaraderie* 24×, *policymaker* 24×, *prioritize* 24×, *reminder* 24×

**Llama 3 8B Instruct:** *unease* 101×, *continuation* 52×, *palpable* 48×, *reminder* 33×, *pang* 29×, *rut* 29×, *waft* 28×, *prioritize* 27×, *grapple* 24×, *camaraderie* 23×

(Karşılaştırma: base Llama 3 modellerinin listeleri anlamsız özel isimlerden oluşuyor — *bananas*, *paperback*, *deborah*, *rambo* — yani kelime tercihi yanlılığı **eğitim verisinden değil, talimat ince ayarından** geliyor.)

Yazarların yorumu, doğrudan uygulanabilir bir kural veriyor:

> "The point here is not that humans refrain from using these words, but that humans refrain from using these words **in certain genres**. In this case, words that are unremarkable in fiction are highly conspicuous and unconventional when used in other genres."

Ve GPT-4o'nun kelime tercihindeki ortak payda: nesneler arası karmaşık ilişki çağrıştıran sözcükler (*tapestry, intricate, camaraderie, cacophony, amidst*) + olumlu sözcükler (*vibrant, solace*) → birlikte **"grandiose, if hollow, summative sentences"** (görkemli ama içi boş özet cümleler) üretiyorlar.

Üçüncü bir kaynak, insan/AI kelime ayrımını daha da somutlaştırıyor: Najjar, A. A., Ashqar, H. I., Darwish, O. A., Hammad, E. (2025), arXiv:2501.03203 — açıklanabilir AI (XAI) analizi, insan metninin **pratik dil** (*use*, *allow*) kullandığını, AI metninin ise **soyut ve resmî terimlerle** (*realm*, *employ*) karakterize olduğunu buldu. <https://arxiv.org/abs/2501.03203>

### 2.3 KAÇINILACAK KELİME LİSTESİ (taranabilir)

**Tier 1 — neredeyse her zaman AI sinyali (sil, istisna yapma):**
```
delve, delve into, delving, delves, deep dive, take a deep dive
tapestry, rich tapestry, tapestry of
testament, a testament to
camaraderie
palpable, palpable sense of
intricate, intricacies, intricate interplay, intricate web, intricate dance
underscore, underscores, underscoring
showcase, showcasing, showcases
pivotal, pivotal role, pivotal moment
realm, in the realm of
navigate, navigating, navigate the landscape, navigate the complexities
landscape (mecazi: "the evolving landscape of")
meticulous, meticulously
embark, embark on a journey
unlock, unlock the potential, unlocking
elevate, elevate your
seamless, seamlessly, seamless integration
robust, robust framework, robust solution
leverage, leveraging
harness, harness the power of
foster, fostering
amidst
cacophony
solace
unspoken
fleeting
unravel
grapple, grapple with
myriad, a myriad of
plethora
paradigm, paradigm shift
synergy, synergistic
holistic
multifaceted
nuanced
profound, profoundly
transformative
game-changer, game-changing
cutting-edge
state-of-the-art
ever-evolving, ever-changing
vibrant
vital, vitally important
crucial, crucially
essential
significant, significantly
comprehensive, comprehensive understanding, comprehensive grasp
utilize, utilizing (yerine: use)
employ, employing (yerine: use)
facilitate
enhance, enhancing
accentuate, accentuating
indispensable, indispensability
surpassing
excels
notably
noteworthy
insights, actionable insights, key insights
interplay
labyrinth
beacon
cornerstone
bedrock
catalyst
ignite
resonate, resonates with
delicate balance
double-edged sword
uncharted territory
treasure trove
```

**Tier 2 — kalıp ifadeler (tamamen sil, yerine hiçbir şey koyma):**
```
It's important to note that
It's worth noting that
It is crucial to understand that
It should be noted that
In today's fast-paced world
In today's digital age
In today's ever-changing landscape
In an era of / In the age of
In conclusion,
To sum up, / In summary, / To summarize,
Ultimately,
At the end of the day,
Let's dive in / Let's dive deeper / Let's dive into
Let's explore / Let's take a closer look
Buckle up
Here's the thing:
Here's the kicker:
Here's what you need to know
The bottom line is
When it comes to X,
More than just X
Whether you're a X or a Y,
Not only ... but also ...
As we've seen,
As mentioned earlier,
As we move forward,
It goes without saying
Needless to say
That being said,
With that in mind,
In this article, we'll explore
In this guide, you'll learn
By the end of this article, you'll
Stay tuned
Remember,
Think of it as
Imagine a world where
Picture this:
The truth is,
What if I told you
The answer may surprise you
But there's a catch
And that's where X comes in
This is where things get interesting
Gone are the days when
Look no further
It's a win-win
The possibilities are endless
Only time will tell
One thing is clear:
```

**Tier 3 — geçiş ifadeleri (sıklığı %80 azalt):**
```
Moreover,
Furthermore,
Additionally,
In addition,
However,
Nevertheless,
Nonetheless,
Consequently,
Therefore,
Thus,
Hence,
Subsequently,
Notably,
Importantly,
Interestingly,
Crucially,
Overall,
Indeed,
Firstly / Secondly / Thirdly / Lastly
First and foremost
On the other hand,
Conversely,
Similarly,
Likewise,
In contrast,
By the same token,
That said,
```
İnsanlar bunları da kullanır ama **her paragrafın başında değil**. Bir metinde 5 paragrafın 4'ü bu kelimelerle başlıyorsa imza var demektir. Yerine: hiçbir şey (cümleler mantıkla bağlansın), veya `But`, `So`, `And`, `Still`, `Yet`, `Then`.

Not: Pullum (2010), Strunk & White'ın "*however* cümle başında kullanılmaz" kuralını çürütüyor — *Alice's Adventures in Wonderland*'de virgülle takip edilen 19 *however*'ın **hepsi** cümle başında. Yani sorun *however*'ın konumu değil, **sıklığı**.

**Tier 4 — hedge (çekimserlik) dili:**
```
can be, may be, might be
could potentially
often considered
is generally regarded as
some argue that
it could be argued that
tends to
in many cases
in some cases
one of the most
plays a key role in
plays a vital role in
has the potential to
may help
can help to
is thought to
arguably
relatively
somewhat
fairly
quite
rather
a bit
sort of / kind of
```
Bu ifadeler tek tek zararsız. Ama üst üste geldiğinde yazının hiçbir şey iddia etmediği anlamına gelir — ve LLM'lerin en belirgin içerik imzası budur.

**Tier 5 — nominalization (fiile çevir):**
```
make an improvement       -> improve
conduct an analysis       -> analyze
provide an explanation    -> explain
reach a decision          -> decide
perform an evaluation     -> evaluate
give consideration to     -> consider
carry out an assessment   -> assess
have a discussion         -> discuss
undertake an examination  -> examine
achieve optimization      -> optimize
implementation of         -> implement
utilization of            -> use
facilitation of           -> help
```
Reinhart ve ark. (2025): GPT-4o nominalization'ı insanın **2,1 katı** kullanıyor (d = 1,23). Orwell bunlara "verbal false limbs" diyor.

---

## 3. CÜMLE VE YAPI İMZALARI

### 3.1 Ölçülmüş sözdizimsel imzalar

Reinhart ve ark. (2025), Douglas Biber'in 66 dilbilimsel kategorisini kullanarak, GPT-4o'nun insana göre oranlarını verdi (eşleştirilmiş Cohen's d ile):

| Özellik | GPT-4o / insan oranı | Etki büyüklüğü |
|---|---|---|
| **Present participial clauses** (–ing ile başlayan yan cümle) | **5,3×** | d = 1,38 |
| **'That' clauses as subject** ("That X is true suggests…") | **2,6×** | d = 0,77 |
| **Nominalizations** (*development*, *robustness*) | **2,1×** | d = 1,23 |
| **Phrasal coordination** (A, B, and C öbek dizisi) | **1,9×** | d = 0,81 |
| **Agentless passive** | **~0,5×** (yani AZ kullanıyor) | — |

Ayrıca: her iki GPT-4o modeli **clausal coordination**'dan kaçınıyor, tüm Llama 3 varyantları insandan fazla kullanıyor; GPT-4o **downtoner**'ları (*barely*, *nearly*) insandan sık, Llama 3'ler ise az kullanıyor.

Makaleden birebir örnekler:

> Present participial clause (GPT-4o): "Bryan, **leaning** on his agility, dances around the ring, **evading** Show's heavy blows."

> Dört nominalization tek cümlede (Llama 3 70B Instruct): "These schemes can help to reduce **deforestation**, **habitat destruction**, and **pollution**, while also **promoting** sustainable **consumption patterns**."

Bu ikinci cümle aynı zamanda **üçlü paralel liste + "while also" dengeleme** kalıbının ders kitabı örneği.

Sınıflandırıcı performansı: rastgele orman sınıflandırıcıları insan/tek-LLM ayrımında tipik olarak **%93–98** doğruluk elde etti — yani bu özellikler gerçekten ayırt edici.

### 3.2 Burstiness: sayısal kanıt

Muñoz-Ortiz, A., Gómez-Rodríguez, C., Vilares, D. (2023), *Contrasting Linguistic Patterns in Human and LLM-Generated News Text*, arXiv:2308.09067. <https://arxiv.org/abs/2308.09067>

Altı LLM, üç model ailesi, dört boyut. Bulgular:
- İnsan metinleri: **daha dağınık cümle uzunluğu dağılımı**, daha çeşitli kelime dağarcığı, farklı bağımlılık/kurucu tipleri, **daha kısa kurucular**, daha optimize bağımlılık mesafeleri
- İnsanlar: daha güçlü **olumsuz duygular** (korku, tiksinti), **daha az neşe**
- LLM'ler: daha çok sayı, sembol, yardımcı fiil ve **zamir** (nesnel dil izlenimi veren öğeler)
- Modeller arası fark, model-insan farkından **daha küçük** → ortak bir "LLM üslubu" var

Sourati, Z., Karimi-Malekabadi, F., Ozcan, M., McDaniel, C., Ziabari, A., Trager, J. (2025), *The Shrinking Landscape of Linguistic Diversity in the Age of Large Language Models*, arXiv:2502.11266. <https://arxiv.org/abs/2502.11266>

- Yedi veri kümesi, **880.000'den fazla metin**
- LLM cilalama/yeniden yazma **çekirdek içeriği korur**, ama üslubu homojenleştirir: **yazı karmaşıklığı varyansını %21–50 azaltır** (p ≤ 0,05)
- Baskın karakteristiklerle ilişkili örüntüleri güçlendirir, diğerlerini bastırır — "bireysellik yerine uyum"

Miletić, F., Falk, N. (2026), arXiv:2605.19936: ACL Anthology'den 37.000+ makale (2020–2024) + 3.000 insan pasajı ve bunların LLM "iyileştirmeleri". LLM ile değiştirilmiş metinlerde: belirli sözdizimsel yapılar daha sık, **daha uzun ve karmaşık kelimeler**, **daha düşük sözcüksel çeşitlilik**. 20 uzmanla pilot değerlendirme: LLM ile iyileştirilmiş metinler "daha anlaşılır ve heyecan verici" bulunuyor, ama uzmanlar aynı anda LLM'lere karşı olumsuz nitel tutum ifade ediyor. <https://arxiv.org/abs/2605.19936>

Raffini, D., Macori, A., Porcaro, L., Catarci, T., Angelini, M. (2025), arXiv:2508.09614: ChatGPT'nin argümantatif metinlerinde **tutarlı bir argüman makro-yapısı**, **kalıp ifadelere bağımlılık** ve **sınırlı üslup zenginliği**. <https://arxiv.org/abs/2508.09614>

Gunjan, Benabderrahmane, S., Rahwan, T. (2026), arXiv:2605.12452: dokuz kriz olayı üzerinden 1.789.406 gönderiden oluşan eşleştirilmiş külliyat. Sentetik söylem **akıcı ama nüfus düzeyinde gerçekdışı**: duygu dağılımı daha dar, **yapısal olarak daha düzenli**, sözcüksel olarak **daha soyut**. Gözlenen insan söylemi: daha geniş duygusal varyasyon, **uzun kuyruklu yapısal dağılımlar**, bağlama özgü ve konuşma diline yakın sözcük belirteçleri. <https://arxiv.org/abs/2605.12452>

Lee, J., Alvero, A., Joachims, T., Kizilcec, R. (2025), arXiv:2503.20062: 30.000 üniversite başvuru denemesi vs LLM üretimi denemeler. LLM denemeleri model ve yöntem fark etmeksizin dilbilimsel olarak ayrışıyor; **demografik bilgi vererek yönlendirme homojenleşmeyi çözmüyor** — demografik istemli ve istemsiz sentetik metinler birbirine, insan metnine olduğundan daha benziyor. <https://arxiv.org/abs/2503.20062>

### 3.3 Yapısal imzalar — kaçınılacaklar

1. **Tek tip cümle uzunluğu.** LLM'ler 15–25 kelimelik cümleleri arka arkaya dizer. İnsan yazısı 3 kelimelik cümleyle 40 kelimelik cümleyi yan yana koyar. Hedef: cümle uzunluğu standart sapması yüksek olsun.
2. **Rule of three takıntısı.** "X, Y, and Z" kalıbı. LLM'ler neredeyse her listeyi üçe tamamlar. İnsanlar iki veya dört öğe de sayar, hatta bir tanesini uzun uzun anlatıp diğerlerini atlar.
3. **"It's not just X, it's Y."** ve türevleri:
   - "X isn't about A. It's about B."
   - "This isn't just a tool — it's a philosophy."
   - "Not X. Not Y. But Z."
   - "It's not that X. It's that Y."
   - "X is more than Y; it's Z."
4. **Antitez dengesi.** "While X, however Y." / "On one hand… on the other hand…" / "Yes, X. But also Y." Her paragrafta iki tarafı da tartmak, hiçbir şey söylememenin yapısal biçimidir.
5. **Eşit uzunlukta paragraflar.** Hepsi 3–4 cümle. İnsan yazısında tek cümlelik paragraf vardır. Ve on cümlelik de.
6. **Her bölümün özet cümlesiyle bitmesi.** "In short, X matters." / "The takeaway is clear." Bu, LLM'nin okuyucunun anlamadığını varsayması. Sil.
7. **Madde işaretine kaçış.** Fikirler arasındaki ilişkiyi cümlelerle kurmak yerine listeye dökmek. Freeburg (2026) bunun markdown eğitiminden geldiğini gösterdi — em dash'in atası aynı kaynak.
8. **Her maddenin kalın başlıkla başlaması.** `**Speed:** It's fast.` kalıbı.
9. **Paralel madde yapısı.** Her maddenin aynı gramer kalıbıyla başlaması (hepsi fiil, hepsi isim öbeği).
10. **Chiasmus/ayna cümle.** "We don't build tools for people. We build people for tools." Kulağa derin gelir, hiçbir şey söylemez.
11. **Present participial açılış.** "Building on this, …" / "Leveraging these insights, …" / "Understanding X requires…" — 5,3× fazla kullanılan yapı.
12. **Retorik soru + hemen cevap.** "So what does this mean? It means…" Bir metinde en fazla bir tane.
13. **Numaralı üç maddelik "key takeaways" bloğu** metin sonunda.
14. **Her cümlenin bağımsız ve tam olması.** İnsanlar cümle parçası kullanır, bir önceki cümleye zamirle asılır, yarıda keser.

---

## 4. İÇERİK İMZALARI

Bunlar dilbilimsel değil, epistemik imzalar — ve düzeltilmesi en zor olanlar.

**Kaçınılacaklar:**

1. **Somut ayrıntı yokluğu.** "Many companies have found success" → hangi şirketler? "Studies show" → hangi çalışma, kim, hangi yıl?
2. **İsim ve sayı yokluğu.** İnsan yazısı tarih, fiyat, mesafe, isim, marka, saat verir. LLM "significant improvement" der; insan "%23, üç ayda" der.
3. **Örneklerin genel olması.** "For example, a small business owner might…" — kurgusal, isimsiz, jenerik örnek. Yerine gerçek bir vaka veya hiç örnek.
4. **Kişisel deneyim yokluğu.** LLM birinci tekil şahıs deneyimi uyduramaz; uydurursa da sahte çıkar. Gerçek gözlem yoksa, gözlem taklidi de yapılmamalı.
5. **Hedge yığılması.** Bkz. Tier 4 listesi. Bir paragrafta ikiden fazla hedge varsa yazı hiçbir şey iddia etmiyordur.
6. **Her şeyi olumlu bitirme.** Dolezal, J., Alam, S., Graham, M., Bohacek, M. (2026), *The Impact of AI-Generated Text on the Internet*, arXiv:2604.26965 — İnternet Arşivi'nden temsilî örneklem: 2025 ortasında yeni yayımlanan web sitelerinin **~%35'i** AI üretimi/destekli olarak sınıflandırıldı (2022 sonu öncesinde sıfırdan). Ve internetteki AI metni artışı **olumlu duygu yaygınlığıyla pozitif**, semantik çeşitlilikle **negatif** korele. <https://arxiv.org/abs/2604.26965> Muñoz-Ortiz ve ark. (2023) de aynı yönde: insanlar daha çok korku ve tiksinti, LLM'ler daha çok neşe.
7. **Sonuç paragrafında her şeyi tekrarlama.** "In conclusion, we explored X, Y, and Z." Okuyucu az önce okudu.
8. **Okuyucuya sorulan retorik sorular dizisi.** "Sounds familiar? Ever wondered why? What if there were a better way?"
9. **"Let's dive in" tipi giriş.** Metnin kendisi hakkında konuşan metin. Meta-yorum: "In this article, we'll explore…", "Before we begin, let's define…"
10. **Sahte denge.** Her iddiadan sonra karşı-iddia getirmek, sonra ikisini de bırakmak.
11. **Tanım cümlesiyle başlama.** "X is a process by which…" — ansiklopedi açılışı.
12. **Kaynaksız otorite.** "Experts agree", "Research suggests", "It's widely accepted".
13. **Risk almama.** Hiçbir şeyi eleştirmemek, kimseyi adıyla anmamak, hiçbir tercihi savunmamak.
14. **Duygusal düzlük.** Sıkıntı, öfke, hayal kırıklığı, alay yok; sadece ölçülü olumluluk.

---

## 5. PERPLEXITY, BURSTINESS VE TESPİT ARAÇLARININ GERÇEK PERFORMANSI

### 5.1 Kavramlar

**Perplexity (şaşkınlık):** Bir dil modelinin, metindeki bir sonraki kelimeyi ne kadar "şaşırtıcı" bulduğunun ölçüsü. Teknik olarak, modelin metne atadığı ortalama olasılığın tersinin üstel hali. Düşük perplexity = kelimeler tahmin edilebilir. LLM'ler tanım gereği yüksek olasılıklı token'lar seçtiği için çıktıları düşük perplexity'ye sahiptir.

**Burstiness (patlaklılık):** Perplexity'nin (ve cümle uzunluğunun) metin boyunca **varyansı**. İnsan yazısı iniş çıkışlıdır: bir sıradan cümle, sonra beklenmedik bir imge, sonra kısa bir cümle. LLM çıktısı düz bir çizgidir.

### 5.2 Neden yalnız başına çalışmıyor — Stanford çalışması

Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., Zou, J. (2023), *GPT detectors are biased against non-native English writers*, arXiv:2304.02819; *Patterns* 4(7), 100779. <https://arxiv.org/abs/2304.02819>

Bu, kılavuzun en önemli tek bulgusu. Rakamlar:

- **91 insan tarafından yazılmış TOEFL denemesi** (anadili İngilizce olmayan yazarlar, yıl ≤2020, bir Çin eğitim forumundan), **7 yaygın GPT dedektörü**
- Ortalama **yanlış pozitif oranı: %61,22** — yani denemelerin yarısından fazlası "AI üretimi" diye damgalandı
- **%19,78** (91 denemeden 18'i) yedi dedektörün **tamamı** tarafından AI sanıldı
- **%97,80** (91'den 89'u) **en az bir** dedektör tarafından işaretlendi
- ABD 8. sınıf öğrencilerinin (anadili İngilizce) denemelerinde yanlış pozitif oranı **sıfıra yakın**
- Oybirliğiyle yanlış sınıflandırılan denemelerin perplexity'si anlamlı biçimde daha düşüktü (p = 9,74E-05)
- Bağımsız doğrulama: ICLR 2023 özetlerinde, anadili İngilizce olmayan ülkelerde çalışan yazarların özetleri anlamlı biçimde daha düşük perplexity'ye sahip (p = 0,035) — hakem puanları kontrol edildikten sonra da fark sürüyor

**Mekanizma:** Anadili İngilizce olmayan yazarlar sınırlı sözcük dağarcığı ve kalıp ifade çeşitliliğiyle yazar → düşük perplexity → dedektör "AI" der. Yani perplexity-tabanlı tespit, **AI'ı değil, dil yeterliliğini** ölçüyor. Yazarların uyarısı:

> "Practitioners should exercise caution when using low perplexity as an indicator of AI-generated text."

**Müdahale deneyi (bu kılavuzun teknik çekirdeği):**
- TOEFL denemelerine ChatGPT ile şu istem uygulandı: *"Enhance the word choices to sound more like that of a native speaker"*
- Yanlış pozitif oranı **%61,22'den %11,77'ye** düştü — **49,45 puanlık** düşüş
- Perplexity anlamlı biçimde arttı
- Ters yönde kontrol: ABD 8. sınıf denemeleri basitleştirilmiş kelime seçimiyle yeniden yazıldığında perplexity anlamlı biçimde düştü

**Ters yön (dedektörü atlatma):**
- ChatGPT-3.5 üretimi denemelere ikinci tur öz-düzenleme istemi (*"Elevate the provided text by employing literary language"*) uygulandığında, tespit oranı **%100'e kadar olan seviyeden %13'e** düştü; perplexity anlamlı arttı (p = 1,94E-15)
- Bilimsel özetlerde: **%68'den %28'e** (p = 1,06E-31)

Sonuç: perplexity düşük olduğu için "AI" diyen bir sistem, tek bir istemle atlatılabiliyor ve aynı zamanda anadili İngilizce olmayan insanları cezalandırıyor.

### 5.3 Tespit araçlarının doğruluk oranları

| Çalışma | Bulgu |
|---|---|
| Perkins, M., Roe, J., Vu, B. H., Postma, D., Hickerson, D., McGaughran, J. (2024), arXiv:2403.19148 | 6 büyük GenAI dedektörü, n=805. Zaten düşük olan doğruluk **%39,5**; kaçınma teknikleri uygulandığında **%17,4'e** düşüyor. Sonuç: bu araçlar akademik dürüstlük ihlali belirlemede **tavsiye edilemez**. <https://arxiv.org/abs/2403.19148> |
| Perkins, M. ve ark. (2023), arXiv:2305.18081 | Turnitin AI dedektörü, 22 GPT-4 üretimi ödevin **%91'ini** "bir miktar AI içeriyor" diye işaretledi, ama tespit edilen toplam içerik yalnızca **%54,8**. AI üretimi ödevler ortalama 52,3 puan aldı, gerçek ödevler 54,4 — nitelik olarak ayırt edilemedi. 15 öğretim üyesi, deneysel gönderilerin %54,5'ini disiplin sürecine sevk etti. <https://arxiv.org/abs/2305.18081> |
| Weichert, J., Dimobi, C. (2024), arXiv:2404.11408 | Watermark yüksek yanlış pozitif; ZeroGPT hem yüksek yanlış pozitif hem yüksek yanlış negatif. ChatGPT-3.5 ile parafraz, tüm dedektörlerin yanlış negatif oranını belirgin biçimde yükseltiyor. <https://arxiv.org/abs/2404.11408> |
| Banerjee, A. (2026), arXiv:2607.13044 | 500 EPO H04 patenti vs 500 LLM üretimi. **İstem düzeyinde tüm dedektörler %60'ın üzerinde yanlış pozitif**: Binoculars **%78,3**, Fast-DetectGPT **%61,3**, DetectGPT **%80,5**. Farklı IPC sınıflarında (A61K, C07D, F03D) ortalama FPR **%84,6**. Nedeni yapısal: patent istemleri EPC Madde 84 gereği "açık ve öz" olmak zorunda → LLM'lerle aynı **düşük-perplexity, düşük-burstiness manifoldunda** yaşıyorlar. <https://arxiv.org/abs/2607.13044> |
| Dik, S., Erdem, O., Dik, M. (2025), arXiv:2506.23517 | GPTZero saf AI metinlerinde başarılı (%91–100 AI tahmini), ama insan yazılarında dalgalanıyor ve yanlış pozitifler veriyor. "Eğitimciler yalnızca bu araçlara güvenirken dikkatli olmalı." <https://arxiv.org/abs/2506.23517> |
| Jung, M., Panizo, C. F., Dugan, L., Fung, Y. R., Chen, P.-Y. (2025), arXiv:2502.04528 | Sabit eşik kullanan dedektörler **kısa insan metinlerinde daha çok yanlış pozitif** üretiyor, uzun metinlerde "nevrotik yazı üsluplarını" AI sanıyor. Dokuz dedektör, üç veri kümesi. <https://arxiv.org/abs/2502.04528> |
| Li, J., Wan, X. (2025), arXiv:2502.12611 | CEFR yeterlilik düzeyi ve dil ortamı, dedektör doğruluğunu tutarlı biçimde etkiliyor — Liang ve ark.'nın bulgusunu bağımsız olarak doğruluyor. <https://arxiv.org/abs/2502.12611> |
| Tarım, İ., Onan, A. (2025), arXiv:2507.10475 | Difüzyon tabanlı metin üretimi (LLaDA) **perplexity ve burstiness'te insan metnini yakından taklit ediyor** → otoregresif modellere göre ayarlanmış dedektörlerde yüksek yanlış negatif. Tek bir metriğe dayanmak işe yaramıyor. <https://arxiv.org/abs/2507.10475> |
| Xia, Y., Stańczak, K., Roth, B. (2026), arXiv:2601.07974 | Dedektörler alan-içi ölçütlerde yüksek doğruluk gösterip görülmemiş istem, model ailesi veya alanlara genelleyemiyor; genelleme başarısı **zaman kullanımı ve zamir sıklığı** gibi dilbilimsel özellik kaymalarıyla anlamlı biçimde ilişkili. <https://arxiv.org/abs/2601.07974> |
| Adam, G. A. ve ark. (2026), arXiv:2602.13042 | GPTZero'nun kendi teknik makalesi: hiyerarşik çok görevli mimari, çok katmanlı otomatik kızıl takım ile parafraza karşı dayanıklılık iddiası. Satıcı kaynaklı olduğu için bağımsız değerlendirmelerle birlikte okunmalı. <https://arxiv.org/abs/2602.13042> |

**Sonuç:** Perplexity ve burstiness gerçek olgulardır ve iyi yazı ile kötü yazı arasındaki farkı kısmen yakalar. Ama **tespit aracı olarak** güvenilir değildirler. Bu, "o hâlde umursamayalım" anlamına gelmiyor — tam tersi, **insan okuyucu** düz ritmi ve kalıp kelimeleri fark ediyor; asıl mesele bu.

### 5.4 Google AI tespit aracı kullanıyor mu?

Google'ın kamuya açık duruşu, üretim yöntemini değil amacı hedef alıyor. Google Search Central, *Creating helpful, reliable, people-first content*:

> "If you use automation, including AI-generation, to produce content for the primary purpose of manipulating search rankings, that's a violation of our spam policies."

<https://developers.google.com/search/docs/fundamentals/creating-helpful-content>

Yani Google, "AI ile yazılmış" diye bir ceza kategorisi ilan etmiyor; **ölçekli içerik suistimalini** (scaled content abuse) cezalandırıyor ve kaliteyi üretim yönteminden bağımsız olarak değerlendirdiğini söylüyor. Google, "How was this created?" sorusunun akla gelebileceği içerikler için AI/otomasyon açıklaması yapılmasını öneriyor. Google'ın kamuya açıkladığı bir "AI metin dedektörü" ürünü yok. Şubat 2023 tarihli *Google Search's guidance about AI-generated content* yazısı da aynı çizgide. <https://developers.google.com/search/blog/2023/02/google-search-and-ai-content>

Karşılaştırma olarak, OpenAI kendi AI Text Classifier'ını 20 Temmuz 2023'te **düşük doğruluk oranı** gerekçesiyle kapattı.

Pratik çıkarım: hedef "dedektörden kaçmak" olamaz, çünkü ceza mekanizması dedektör değil. Hedef, okuyucunun ve editörün metni bayat bulmaması.

---

## 6. İNSAN YAZISININ ÖZELLİKLERİ — EL KİTAPLARINDAN SOMUT KURALLAR

### 6.1 George Orwell (1946), *Politics and the English Language*

<https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/>

Altı kural, birebir:

> i. Never use a metaphor, simile or other figure of speech which you are used to seeing in print.
> ii. Never use a long word where a short one will do.
> iii. If it is possible to cut a word out, always cut it out.
> iv. Never use the passive where you can use the active.
> v. Never use a foreign phrase, a scientific word or a jargon word if you can think of an everyday English equivalent.
> vi. Break any of these rules sooner than say anything outright barbarous.

Birinci kural, AI yazısına doğrudan isabet ediyor: *tapestry*, *navigate the landscape*, *unlock the potential*, *a testament to* — hepsi "basılı görmeye alışık olduğun" metaforlar. Orwell bunlara **ölmekte olan metaforlar (dying metaphors)** diyor.

Orwell'in kötü yazı kategorileri ve örnekleri:

- **Dying metaphors:** *ring the changes on, take up the cudgels for, toe the line, ride roughshod over, stand shoulder to shoulder with, play into the hands of, no axe to grind, grist to the mill, fishing in troubled waters*
- **Operators / verbal false limbs** (basit fiili şişiren öbekler): *render inoperative, militate against, prove unacceptable, make contact with, be subject to, give rise to, have the effect of, play a leading part in*
- **Pretentious diction:** *phenomenon, element, objective, categorical, effective, eliminate, liquidate, epoch-making, historic, inexorable, realm, throne, chariot, jackboot* — dikkat: **realm** Orwell'in listesinde. 1946'da yapmacık bulduğu kelime, 2024'te en yüksek LLM işaret kelimelerinden biri.
- **Meaningless words:** *romantic, plastic, values, human, dead, sentimental, natural, vitality; democracy, socialism, freedom, patriotic, justice, progressive*

"Verbal false limbs" kategorisi doğrudan Reinhart'ın nominalization bulgusuyla örtüşüyor: *implement an improvement* yerine *improve*, *conduct an analysis* yerine *analyze*.

### 6.2 Strunk & White ve Pullum'un eleştirisi

Pullum, G. K. (2010), *The Land of the Free and The Elements of Style*, *English Today* 26(2), 34–44. <https://pullum.ppls.ed.ac.uk/LandOfTheFree.pdf>

Pullum'un tezi sert:

> "I believe the success of *Elements* to be one of the worst things to have happened to English language education in America in the past century. The book's style advice, largely vapid and obvious ('Do not overwrite'; 'Be clear'), may do little damage; but the numerous statements about grammatical correctness are actually harmful. They are riddled with inaccuracies, uninformed by evidence, and marred by bungled analysis."

Belgelediği somut hatalar:

1. **Edilgen çatı bölümü kendi örneklerini yanlış anlıyor.** "Use the active voice" bölümünde düzeltilmesi gereken diye verilen dört örnekten **hiçbiri** edilgen bir yapının etken geçişli bir yapıyla değiştirilmesi değil:
   - *There were a great number of dead leaves lying on the ground.* → *Dead leaves covered the ground.* (ilki edilgen değil)
   - *At dawn the crowing of a rooster could be heard.* → *The cock's crow came with dawn.* (yerine geçen fiil geçişli değil)
   - *The reason that he left college was that his health became impaired.* → *Failing health compelled him to leave college.* (*became impaired* edilgen değil; *become* edilgen almaz)
   - *It was not long before she was very sorry that she had said what she had.* → *She soon repented her words.*
   - Pullum'un ifadesiyle: "The jaw-dropping fact is that not a single one of the pairs involves the replacement of a passive by an active transitive."
2. **Kitabın kendisi edilgen kaynıyor.** Strunk'un giriş bölümünün açılış cümlesindeki iki yüklem cümlesi de edilgen: *"This book is intended for use in English courses in which the practice of composition is combined with the study of literature."* Pullum: "If the passive is wicked and improper, Strunk and White are hypocrites; if it is not, they are liars. There seems to be no other possibility."
3. **"Keep related words together" bölümü kendi kuralını cümlelerinin %27'sinde çiğniyor.**
4. **"Write with nouns and verbs, not with adjectives and adverbs"** — White'ın bunu anlattığı pasaj sıfat dolu; kendi bölüm başlığı *"Use definite, specific, concrete language"* beş kelimede üç niteleyici sıfat. White'ın denemelerinde kelimelerin ~%8'i sıfat (tipik düzyazı ~%6).
5. **that/which kuralı uydurma.** *which* her zaman kısıtlayıcı yan cümle kurabilmiştir; King James İncil'i buna kanıt. Pullum bunu kitabın en kötü hatası sayıyor.
6. ***None* tekil olmalı iddiası yanlış.** *None of us are perfect* Oscar Wilde'ın *The Importance of Being Earnest* oyunundan bir replik; *Dracula*'da (1897) bu öbeklerin şimdiki zaman özneleri olarak **hiç tekil uyumu yok**.
7. ***however* cümle başında olmaz iddiası yanlış.** *Alice's Adventures in Wonderland*'de virgülle takip edilen 19 *however*'ın hepsi cümle başında; Mark Twain örneklerin üçte ikisinden fazlasında başa koyuyor, Henry James yalnızca %6'sında. Wall Street Journal'da (1987–89) yaklaşık %40.

**Kılavuz için çıkarım:** Kural listelerine kör bağlılık, kendi başına bir AI imzasıdır. LLM'ler "iyi yazı kuralları"nı fazla itaatkâr uygular: hiç edilgen yok, hiç uzun cümle yok, hep paralel yapı. İnsan yazarlar kuralları bilerek çiğner. Orwell'in altıncı kuralı tam da budur.

### 6.3 William Zinsser, *On Writing Well*

> "Clutter is the disease of American writing. We are a society strangling in unnecessary words, circular constructions, pompous frills and meaningless jargon."

> "Writing improves in direct ratio to the number of things we can keep out of it."

<https://en.wikipedia.org/wiki/On_Writing_Well>

Uygulanabilir kurallar:
- Her cümleyi en temiz bileşenine indir. Aynı işi gören iki kelimeden birini sil.
- Niteleyicileri (*a bit*, *sort of*, *rather*, *very*, *quite*, *pretty much*) çıkar. Zinsser bunlara "küçük dert giderici" der.
- "Personal transaction" ilkesi: iyi yazının çekiciliği insanlıktan ve sıcaklıktan gelir. Yazar kendisi olmalı, kurumsal ses olmamalı. Zinsser bu kavrayışa ellili yaşlarında, gündemsiz ve sadece yardım etmek için yazdığında ulaştığını anlatır.
- Giriş cümlesi (lead) okuyucuyu bir sonraki cümleye çekmeli — ve ikinci cümle üçüncüye. Konu tanımıyla değil, ilginç bir olguyla başla.
- Bitiş: en iyi son, okuyucuyu şaşırtan ama geri dönüp bakınca kaçınılmaz görünen sondur. **Özet değil.**
- Birlik (unity): tek zaman, tek şahıs, tek ton. Metnin ortasında ton değiştirme.
- Yüksek sesle oku. Kulak, gözden daha iyi editördür.

### 6.4 Ursula K. Le Guin, *Steering the Craft* (1998, gözden geçirilmiş 2015)

<https://en.wikipedia.org/wiki/Steering_the_Craft>

Le Guin'in kitabı bir yazarlık atölyesinden doğduğu için tamamen alıştırma odaklı. Kılavuza aktarılabilir çekirdek fikirler:

- **Cümlenin sesi önce gelir.** İlk bölümün adı "The Sound of Your Writing". Düzyazı da tıpkı şiir gibi kulakla yazılır. Her şeyi yüksek sesle oku.
- **Noktalama nefes almadır**, kural değil. Nokta, virgül ve noktalı virgül, okuyucunun akciğerini yönetir.
- **Cümle uzunluğu ve karmaşıklığı** ayrı bir alıştırma konusudur: bir paragrafı tek bir uzun cümleyle yaz, sonra hepsi yedi kelimeden kısa cümlelerle yaz. Fark, ritmin ne olduğunu öğretir.
- **Sıfat ve zarf konusunda pürizm değil, dikkat:** Le Guin "sıfatları sil" demez; "sıfat işini yapmıyorsa sil" der. Fiilin içinde zaten var olan zarfı sil (*shouted loudly*).
- **"Crowding and leaping":** İyi anlatı, yoğunlaştırma (crowding — canlı ayrıntı yığmak) ile atlama (leaping — gereksiz olanı tamamen atlamak) arasında gidip gelir. LLM yazısı ne yoğunlaştırır ne atlar; her şeyi eşit ağırlıkta anlatır. Bu, en tanınabilir yapısal imzalardan biri.
- **Bakış açısı tutarlılığı** ve yazarın sesinin metinden görünür olması.
- Kural değil deney: her bölüm bir "alıştırma", çünkü üslup ancak denenerek bulunur.

### 6.5 Verlyn Klinkenborg, *Several Short Sentences About Writing* (2012, Alfred A. Knopf)

Kitabın kendi biçimi tezidir: kısa, satır satır yazılmış aforizmalar. Uygulanabilir çekirdek:

- **Kısa cümleyle başla.** Klinkenborg'un merkezi iddiası, uzun cümlenin varsayılan olmadığıdır. Kısa cümle güvenilirdir; uzun cümle kazanılmalıdır.
- **Her cümle bağımsız olmalı.** Cümleler birbirine geçiş ifadeleriyle yapıştırılmaz; her cümle kendi başına ayakta durur ve bağlantı okuyucunun zihninde kurulur. Bu, "moreover/furthermore" bağımlılığına doğrudan panzehir.
- **Geçiş ifadeleri genellikle gereksizdir.** Cümleler doğru sırada dizilmişse bağlaca ihtiyaç yoktur.
- **Ritim, anlamın parçasıdır.** Cümlelerin uzunluğunu değiştirmek süs değil, iletişimdir.
- **"Akış" (flow) bir mit.** Yazı, cümle cümle inşa edilen bir şeydir; akışa kapılmak değil.
- **Revizyon, cümleyi tek tek elden geçirmektir**, paragrafı yeniden düzenlemek değil.
- **Klişeyi ve hazır ifadeyi fark et.** Zihnine ilk gelen ifade, muhtemelen başkasınındır.
- **Okuyucunun dikkatini hafife alma.** Açıklamayı tekrar etme; okuyucu anlamıştır.

### 6.6 Roy Peter Clark, *Writing Tools: 50 Essential Strategies for Every Writer* (2006, Little, Brown)

Clark'ın araçlarından bu kılavuza en çok yarayanlar:

- **Cümlenin başına özneyi ve fiili koy.** Nominalization'a karşı doğrudan ilaç.
- **Güçlü fiiller kullan.** *make an improvement* → *improve*.
- **Zarfları dikkatli kullan.** Fiil zayıfsa zarf onu kurtarmaz.
- **Vurgulu kelimeleri cümlenin sonuna koy.** Cümlenin sonu en güçlü konumdur; nokta bir durak işaretidir.
- **Cümle uzunluğunu bilinçli değiştir** ("Play with sentence length"). Karmaşık bir fikirden sonra kısa bir cümle koy.
- **Aktif ve pasifi bilinçli seç** — Strunk & White'ın aksine Clark pasifi yasaklamaz, işlevini anlatır (fail bilinmiyorsa veya önemsizse pasif doğrudur).
- **Somut ayrıntı ver, soyut özet değil** ("show and tell"). "Ladder of abstraction": en alt basamakta somut nesneler, en üstte soyut fikirler. İyi yazı merdivenin iki ucuna gider, ortada takılmaz. LLM yazısı sürekli ortada durur.
- **İsim ve sayı topla** ("Get names, numbers").
- **Örnek sayısına dikkat et.** Clark özellikle uyarır ki **üçlü liste tamamlanmışlık hissi verir**; ikili gerilim, dörtlü ise liste hissi yaratır. Sürekli üçleme yapmak, sürekli "kapanış" duygusu üretir — AI yazısının en sinsi ritmik imzası.
- **Sesli oku, sesini ayarla.**
- **Altın tuğlalar biriktir.** Yazmadan önce gözlem ve alıntı topla; malzeme yoksa üslup kurtarmaz.
- **Kısa paragraflar ve beyaz alan** okunabilirliği artırır, ama her paragraf aynı boyda olmamalı.

---

## 7. TESPİTTEN KAÇMA DEĞİL, İYİ YAZMA

### 7.1 "Dedektörü kandırma" taktikleri neden kötü fikir

**Taktikler ve neden başarısız oldukları:**

1. **Kasıtlı yazım/dilbilgisi hatası serpiştirme.** Metni okunmaz yapar, güvenilirliği düşürür ve — kritik nokta — Liang ve ark.'nın (2023) bulgusuna göre **düşük perplexity ile hata farklı şeylerdir**. Hatalı ama kalıp bir metin hâlâ düşük perplexity'li olabilir. Kazanç yok, itibar kaybı var.
2. **Eşanlamlı serpiştirme (synonym spinning).** Otomatik eşanlamlı değiştirme, kelimeleri bağlamdan koparır (*important* → *paramount*, *use* → *utilize*). Sonuç, tam da Orwell'in "pretentious diction" dediği şey — yani **AI imzasını güçlendirir**. Najjar ve ark. (2025) zaten AI metninin ayırt edici işaretinin *realm*, *employ* gibi soyut-resmî sözcükler olduğunu gösterdi.
3. **Görünmez Unicode karakter enjeksiyonu (sıfır genişlikli boşluk, homoglif).** Kopyala-yapıştırda kırılır, arama motorlarında sorun yaratır ve tespit edildiğinde kasıt kanıtı olur. Perkins ve ark. (2024) bu tür manipülasyonların dedektör doğruluğunu %39,5'ten %17,4'e düşürdüğünü gösterdi — yani **işe yarıyor**, ama işe yaraması onu iyi bir fikir yapmıyor: kaçınma başarısı, metnin kalitesiyle ilgisiz.
4. **Parafraz araçlarından geçirme (QuillBot vb.).** Weichert ve Dimobi (2024) yanlış negatifleri belirgin biçimde artırdığını doğruladı. Ama parafraz, metnin bilgi yoğunluğunu ve somutluğunu düşürür; cümleler daha da jenerikleşir.
5. **"Elevate with literary language" istemi.** Liang ve ark. (2023) bunun tespit oranını %100'den %13'e düşürdüğünü ölçtü. Ancak sonuç metin **daha da süslü** olur — *tapestry/palpable/amidst* bölgesine kayar. Yani dedektörü atlatırken **insan okuyucuya karşı daha belirgin** hâle gelir. Bu, kaçınma taktiklerinin merkezi çelişkisi.
6. **Rastgele em dash silme.** Freeburg (2026) gösterdi ki em dash bir semptom, sebep değil: markdown yönelimli yapısal düşünme. Yalnızca tireleri silmek, altındaki liste-benzeri, madde-benzeri düşünceyi bırakır.

### 7.2 Gerçek çözüm

Kaçınma değil, **ikame**. Üç adımlı yaklaşım:

**Adım 1 — Bilgi ekle.** AI imzalarının çoğu, söylenecek somut bir şey olmamasının belirtisidir. *"This is crucial for success"* cümlesi, yazarın hangi ölçüde, kim için, ne kadar bilmediği için oradadır. Bir tarih, bir isim, bir sayı, bir vaka eklendiğinde kalıp cümle kendiliğinden buharlaşır.

**Adım 2 — Ritmi kır.** Cümle uzunluğu varyansını bilinçli yükselt. Klinkenborg'un yöntemi: paragrafı cümlelere böl, her cümleyi ayrı satıra yaz, hangilerinin aynı uzunlukta olduğunu gör, üçünü birleştir, birini ikiye böl.

**Adım 3 — Sesli oku.** Le Guin, Zinsser ve Clark'ın ortak öğüdü. Nefesinin tükendiği yere nokta koy. Kulağın sıkıldığı yer kesilecek yerdir. Ağzına oturmayan kelime *tapestry*'dir.

**Ek ilke:** Bir şey iddia et. Sourati ve ark.'nın (2025) ölçtüğü homojenleşme, LLM'lerin "baskın karakteristiği güçlendirip diğerlerini bastırması"ndan geliyor. Buna karşı tek panzehir, ortalamanın dışına düşen bir yargıya sahip olmaktır.

---

## 8. GERÇEK ÖRNEKLER — SATIR SATIR KARŞILAŞTIRMA

### Örnek A: Akademik özet

**AI imzalı (Kobak ve ark. 2024'ün alıntıladığı gerçek 2023 PubMed özeti):**
> "By meticulously delving into the intricate web connecting [X] and [Y], this comprehensive chapter takes a deep dive into their involvement as significant risk factors for [Z]."

**Satır satır teşhis:**
| Öğe | Sorun |
|---|---|
| *By meticulously delving into* | Present participial/gerund açılış + iki Tier-1 kelime (*meticulously*, *delving*) |
| *intricate web connecting* | Ölmekte olan metafor (Orwell kural i); *intricate* 119× aşırı kullanım |
| *this comprehensive chapter* | Metnin kendisi hakkında meta-yorum |
| *takes a deep dive* | *delving* ile aynı metaforun tekrarı — iki kez dalış |
| *significant risk factors* | Hedge + jenerik nitelik; hangi risk, ne kadar? |
| Cümlede fiil sayısı | Bir tane gerçek yüklem (*takes*), o da nominalize bir öbek içinde |
| Sayı/isim sayısı | 0 |

**İnsan versiyonu:**
> "We asked whether high blood pressure raises stroke risk in patients under 50. In 4,100 records from three Ankara hospitals, it did — by a factor of 2.3."

Fark: özne ve fiil başta (Clark), sayı var, yer var, iddia var, ikinci cümle birinciden kısa, tek em dash gerçek bir iş yapıyor.

### Örnek B: Blog girişi

**AI imzalı:**
> "In today's fast-paced digital landscape, businesses face unprecedented challenges. Whether you're a startup founder or a seasoned executive, navigating these complexities requires more than just intuition — it demands a robust framework. In this article, we'll delve into three key strategies that can help you unlock your team's full potential. Let's dive in."

**Satır satır:**
| Satır | Teşhis |
|---|---|
| *In today's fast-paced digital landscape* | Tier-2 kalıp + *landscape* metaforu; hiçbir bilgi taşımıyor |
| *unprecedented challenges* | Kaynaksız otorite, ölçüsüz sıfat |
| *Whether you're a X or a Y* | Kalıp; sahte kapsayıcılık |
| *navigating these complexities* | *navigate* + nominalization (*complexities*) + present participial |
| *more than just intuition — it demands* | "It's not just X, it's Y" kalıbı + em dash |
| *a robust framework* | İki Tier-1 kelime yan yana |
| *delve into three key strategies* | *delve* + rule of three + *key* |
| *unlock your team's full potential* | Ölü metafor + boş vaat |
| *Let's dive in.* | Meta-yorum kapanışı; *delve* ile üçüncü dalış metaforu |
| Cümle uzunlukları | 11, 27, 20, 3 → son cümle hariç düz |
| Somut isim/sayı sayısı | **0** |

**İnsan versiyonu:**
> "Last March our team shipped four features. Three of them nobody used. I spent a week trying to figure out why, and the answer turned out to be embarrassing: we had never asked. Here's what asking looks like."

Fark: tarih, sayı, itiraf, birinci tekil şahıs, kısa-uzun-kısa ritmi, kendini övmeyen bir açılış, ve okuyucuya "dalış" daveti yerine bir söz.

### Örnek C: Açıklayıcı paragraf

**AI imzalı:**
> "Moreover, it's important to note that machine learning models can be significantly impacted by data quality. Poor data often leads to suboptimal outcomes, while high-quality data may enable more accurate predictions. Therefore, organizations should prioritize data governance. Ultimately, the quality of your data determines the quality of your insights."

**Satır satır:**
| Öğe | Teşhis |
|---|---|
| *Moreover,* | Tier-3 geçiş; öncesinde bağlanacak bir şey yok |
| *it's important to note that* | Tier-2; sil, cümle bozulmaz |
| *can be significantly impacted* | Hedge + edilgen + nominalize fiil |
| *often leads to suboptimal outcomes* | Hedge + soyut |
| *while ... may enable* | "while X, however Y" dengeleme + ikinci hedge |
| *Therefore,* | İkinci geçiş ifadesi, dört cümlede |
| *should prioritize* | Kime? Ne yaparak? |
| *Ultimately,* | Üçüncü geçiş + özet cümlesi kapanışı |
| Son cümle | Chiasmus/ayna yapısı ("quality of X determines quality of Y") |
| Cümle uzunlukları | 18, 17, 8, 13 → düşük varyans |
| Sayı/isim | 0 |

**İnsan versiyonu:**
> "Garbage in, garbage out is old advice, and it is still the whole story. A fraud model I worked on in 2023 hit 94% accuracy in testing and 61% in production. The training set had been labeled by two analysts who disagreed with each other about a third of the time. Nobody checked. We spent six weeks on the model and two days on the labels, which was exactly backwards."

Fark: klişeyi bilerek ve **kısa** kullanıyor (Orwell kural i'yi kural vi ile kırıyor), üç sayı, bir tarih, bir itiraf, dört kelimelik bir cümle (*Nobody checked.*), ve son cümle yargı veriyor — iki tarafı dengelemiyor.

### Örnek D: Aynı fikir, iki ritim

**Düz (AI):**
> "The system was designed to handle high traffic loads efficiently. It uses a distributed architecture that allows for horizontal scaling. This approach ensures reliability during peak usage periods. Additionally, it reduces the risk of single points of failure."

Dört cümle: 11, 12, 10, 12 kelime. Standart sapma ≈ 0,9. Sıfır özel isim, sıfır sayı, dört soyut isim öbeği.

**Değişken (insan):**
> "It scales sideways. When traffic spikes — Black Friday, mostly — we add machines instead of buying a bigger one, which means no single box can take the whole thing down with it. That was the point. It has failed twice in three years, both times because of DNS."

Dört cümle: 3, 34, 4, 12 kelime. Standart sapma ≈ 14. Ayrıca: bir tane em dash çifti (meşru, araya girme işlevi), somut olay (*Black Friday*), sayı (*twice in three years*), ve teknik insanların bildiği bir şaka (*both times because of DNS*).

### Örnek E: Ton ve duygu

**AI imzalı:**
> "While the transition presented certain challenges, the team ultimately emerged stronger, having gained valuable insights that will undoubtedly inform future initiatives."

Teşhis: *while* dengeleme + *ultimately* + *valuable insights* + *undoubtedly* (hedge'in tersi ama aynı içi boşluk) + zorunlu olumlu kapanış + present participial (*having gained*) + sıfır somut ayrıntı. Muñoz-Ortiz ve ark.'nın ölçtüğü "LLM'lerde fazla neşe" tam olarak bu.

**İnsan versiyonu:**
> "The migration took eleven weeks instead of four. Two people quit. I still think it was the right call, but I would not do it in December again."

Fark: sayı, olumsuz sonuç, kişisel yargı, ve yargının kendisiyle çelişmeyen bir pişmanlık. Le Guin'in "crowding and leaping"i: ayrıntı verilen yer verilir, gerisi atlanır.

---

## 9. UYGULAMA KONTROL LİSTESİ

Metni teslim etmeden önce:

**Kelime taraması (bul-değiştir):**
- [ ] Tier 1 listesindeki hiçbir kelime yok mu? (`delve, tapestry, testament, intricate, underscore, showcase, pivotal, realm, navigate, landscape, meticulous, embark, unlock, elevate, seamless, robust, leverage, harness, foster, myriad, plethora, paradigm, holistic, multifaceted, nuanced, transformative, cutting-edge, ever-evolving, vibrant, comprehensive, crucial, amidst, palpable, camaraderie, solace, fleeting, unravel, grapple, utilize, employ, facilitate, cornerstone, catalyst, beacon, resonate`)
- [ ] Tier 2 kalıp ifadelerin hiçbiri yok mu?
- [ ] Tier 3 geçiş ifadeleri metinde kaç kez geçiyor? 1.000 kelimede 3'ten fazlaysa kes.
- [ ] Hedge sayımı (Tier 4): paragraf başına en fazla 1.
- [ ] Tier 5 nominalization'lar fiile çevrildi mi? (`-tion`, `-ment`, `-ness`, `-ity`, `-ance` ile biten kelimeleri tara.)

**Noktalama taraması:**
- [ ] Em dash sayısı ≤ 1.000 kelimede 2
- [ ] Noktalı virgül sayısı ≤ 1.000 kelimede 1
- [ ] Kıvrık tırnak/kesme işareti düz karaktere çevrildi mi?
- [ ] `…` yerine `...`
- [ ] En az bir contraction var mı? (`don't`, `it's`, `we're`)
- [ ] En az bir ünlem veya cümle parçası var mı?

**Yapı taraması:**
- [ ] Cümle uzunluğu standart sapması > 8 mi? (En kısa cümle ≤ 5 kelime, en uzun ≥ 30 kelime olmalı.)
- [ ] Üçlü paralel liste sayısı: metinde en fazla 1
- [ ] "It's not just X, it's Y" ve türevleri: 0
- [ ] Paragraf uzunlukları farklı mı? En az bir tek-cümlelik paragraf var mı?
- [ ] Hiçbir bölüm özet cümlesiyle bitmiyor mu?
- [ ] Madde işaretli liste, gerçekten liste olan şeyler için mi kullanılmış? (Argüman listeye dönüştürülmemiş.)
- [ ] Present participial açılış (`Building on…`, `Leveraging…`, `Understanding…`) sayısı: 0
- [ ] Retorik soru sayısı ≤ 1
- [ ] "while X, however Y" dengeleme kalıbı sayısı ≤ 1

**İçerik taraması:**
- [ ] 500 kelimede en az 3 somut sayı var mı?
- [ ] En az bir özel isim (kişi, kurum, yer, ürün, tarih) var mı?
- [ ] Örneklerin hiçbiri "a small business owner might…" tipinde kurgusal ve isimsiz değil mi?
- [ ] Metinde en az bir yerde belirsizlik veya itiraf var mı? ("Bunu hâlâ çözemedim." / "Yanılmış olabilirim.")
- [ ] Metinde en az bir olumsuz veya eleştirel yargı var mı?
- [ ] Sonuç paragrafı yeni bir şey söylüyor mu, yoksa özet mi?
- [ ] Metin bir yerde net bir yargı veriyor mu, yoksa her iddiayı dengeliyor mu?

**Son test:**
- [ ] Metni sesli oku. Nefesinin tükendiği yere nokta koy. Ağzına oturmayan kelimeyi at.

---

## 10. KAYNAKLAR

**Kelime ve üslup imzaları — ölçüm çalışmaları**
- Kobak, D., González-Márquez, R., Horvát, E.-Á., Lause, J. (2024/2025). *Delving into ChatGPT usage in academic writing through excess vocabulary*. arXiv:2406.07016; *Science Advances* 11(27), eadt3813. <https://arxiv.org/abs/2406.07016>
- Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G. (2024/2025). *Do LLMs write like humans? Variation in grammatical and rhetorical styles*. arXiv:2410.16107; *PNAS* 122. <https://arxiv.org/abs/2410.16107>
- Liang, W., Zhang, Y., Wu, Z., Lepp, H., Ji, W., Zhao, X., Cao, H., Liu, S., He, S., Huang, Z., Yang, D., Potts, C., Manning, C. D., Zou, J. Y. (2024). *Mapping the Increasing Use of LLMs in Scientific Papers*. arXiv:2404.01268. ~951.000 makale; Bilgisayar Bilimi'nde %17,5'e kadar LLM ile değiştirilmiş cümle, Matematik ve Nature portföyünde %6,3'e kadar. <https://arxiv.org/abs/2404.01268>
- Miletić, F., Falk, N. (2026). *What Are LLMs Doing to Scientific Communication? Measuring Changes in Writing Practices and Reading Experience*. arXiv:2605.19936. <https://arxiv.org/abs/2605.19936>
- Najjar, A. A., Ashqar, H. I., Darwish, O. A., Hammad, E. (2025). *Detecting AI-Generated Text in Educational Content*. arXiv:2501.03203. <https://arxiv.org/abs/2501.03203>

**Em dash**
- Czuma, P. (2026). *Em-ergence of the em-dash* (medRxiv, N=69.632). arXiv:2606.29540. <https://arxiv.org/abs/2606.29540>
- Czuma, P. (2026). *The em-dash em-beds in Congress* (146.239 basın bülteni). arXiv:2608.05889. <https://arxiv.org/abs/2608.05889>
- Freeburg, E. M. (2026). *The Last Fingerprint: How Markdown Training Shapes LLM Prose*. arXiv:2603.27006. <https://arxiv.org/abs/2603.27006>

**Yapı, çeşitlilik, burstiness**
- Muñoz-Ortiz, A., Gómez-Rodríguez, C., Vilares, D. (2023). *Contrasting Linguistic Patterns in Human and LLM-Generated News Text*. arXiv:2308.09067. <https://arxiv.org/abs/2308.09067>
- Sourati, Z., Karimi-Malekabadi, F., Ozcan, M., McDaniel, C., Ziabari, A., Trager, J. (2025). *The Shrinking Landscape of Linguistic Diversity in the Age of Large Language Models*. arXiv:2502.11266. <https://arxiv.org/abs/2502.11266>
- Lee, J., Alvero, A., Joachims, T., Kizilcec, R. (2025). *Poor Alignment and Steerability of Large Language Models: Evidence from College Admission Essays*. arXiv:2503.20062. <https://arxiv.org/abs/2503.20062>
- Raffini, D., Macori, A., Porcaro, L., Catarci, T., Angelini, M. (2025). *How Persuasive Could LLMs Be?* arXiv:2508.09614. <https://arxiv.org/abs/2508.09614>
- Gunjan, Benabderrahmane, S., Rahwan, T. (2026). *The Algorithmic Caricature: Auditing LLM-Generated Political Discourse Across Crisis Events*. arXiv:2605.12452. <https://arxiv.org/abs/2605.12452>
- Dolezal, J., Alam, S., Graham, M., Bohacek, M. (2026). *The Impact of AI-Generated Text on the Internet*. arXiv:2604.26965. <https://arxiv.org/abs/2604.26965>

**Tespit, perplexity ve yanlış pozitifler**
- Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., Zou, J. (2023). *GPT detectors are biased against non-native English writers*. arXiv:2304.02819; *Patterns* 4(7), 100779. <https://arxiv.org/abs/2304.02819>
- Perkins, M., Roe, J., Vu, B. H., Postma, D., Hickerson, D., McGaughran, J. (2024). *GenAI Detection Tools, Adversarial Techniques and Implications for Inclusivity in Higher Education*. arXiv:2403.19148. <https://arxiv.org/abs/2403.19148>
- Perkins, M., Roe, J., Postma, D., McGaughran, J., Hickerson, D. (2023). *Game of Tones: Faculty detection of GPT-4 generated content in university assessments*. arXiv:2305.18081. <https://arxiv.org/abs/2305.18081>
- Weichert, J., Dimobi, C. (2024). *DUPE: Detection Undermining via Prompt Engineering for Deepfake Text*. arXiv:2404.11408. <https://arxiv.org/abs/2404.11408>
- Banerjee, A. (2026). *The Perplexity Trap: When Patent Law Makes Human Writing Look Like AI*. arXiv:2607.13044. <https://arxiv.org/abs/2607.13044>
- Jung, M., Panizo, C. F., Dugan, L., Fung, Y. R., Chen, P.-Y. (2025). *Group-Adaptive Threshold Optimization for Robust AI-Generated Text Detection*. arXiv:2502.04528. <https://arxiv.org/abs/2502.04528>
- Li, J., Wan, X. (2025). *Who Writes What: Unveiling the Impact of Author Roles on AI-generated Text Detection*. arXiv:2502.12611. <https://arxiv.org/abs/2502.12611>
- Dik, S., Erdem, O., Dik, M. (2025). *Assessing GPTZero's Accuracy in Identifying AI vs. Human-Written Essays*. arXiv:2506.23517. <https://arxiv.org/abs/2506.23517>
- Adam, G. A., Cui, A., Thomas, E., Napier, E., Shmatko, N., Schnell, J. (2026). *GPTZero: Robust Detection of LLM-Generated Texts*. arXiv:2602.13042. <https://arxiv.org/abs/2602.13042>
- Tarım, İ., Onan, A. (2025). *Can You Detect the Difference?* arXiv:2507.10475. <https://arxiv.org/abs/2507.10475>
- Xia, Y., Stańczak, K., Roth, B. (2026). *Explaining Generalization of AI-Generated Text Detectors Through Linguistic Analysis*. arXiv:2601.07974. <https://arxiv.org/abs/2601.07974>

**Arama motoru politikası**
- Google Search Central. *Creating helpful, reliable, people-first content*. <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- Google Search Central Blog (Şubat 2023). *Google Search's guidance about AI-generated content*. <https://developers.google.com/search/blog/2023/02/google-search-and-ai-content>

**Yazı el kitapları ve eleştiri**
- Orwell, G. (1946). *Politics and the English Language*. <https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/>
- Pullum, G. K. (2010). *The Land of the Free and The Elements of Style*. *English Today* 26(2), 34–44. <https://pullum.ppls.ed.ac.uk/LandOfTheFree.pdf>
- Zinsser, W. (1976/2006). *On Writing Well*. <https://en.wikipedia.org/wiki/On_Writing_Well>
- Le Guin, U. K. (1998/2015). *Steering the Craft*. <https://en.wikipedia.org/wiki/Steering_the_Craft>
- Klinkenborg, V. (2012). *Several Short Sentences About Writing*. Alfred A. Knopf.
- Clark, R. P. (2006). *Writing Tools: 50 Essential Strategies for Every Writer*. Little, Brown.
- Strunk, W., White, E. B. (1918/1959/2000). *The Elements of Style*. 1918 metni: <http://www.bartleby.com/141>
