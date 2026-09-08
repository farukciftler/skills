# Yayın etiği ve yapay zekâ

Politikalar hızlı değişiyor. Hedef mecra belliyse **o mecranın kendi sayfasını canlı doğrula**; buradaki bilgiler 8 Eylül 2026 itibarıyla geçerli çerçevedir.

## ICMJE — Ocak 2026 güncellemesi

ICMJE, Recommendations belgesini Ocak 2026'da güncelledi. İki **yeni bölüm** eklendi:
- **Bölüm V: Yayında yapay zekâ kullanımı** — yazarlar (V.A), hakemler (V.B) ve editörler (V.C) için ayrı alt başlıklar.
- **Bölüm III.L.2: Yazarların veriye erişimi** — yazarların, çalışmanın bütünlüğü ve doğruluğu için sorumluluk alabilecek düzeyde veriye erişimi olmalı. Sanayi destekli veya dış fonlu çalışmalarda sözleşmelerin yazarın veri erişimini açıkça koruması artık resmî bir beklenti.

Güncellenen başlıklar: sponsor anlaşmaları ve akademik özgürlük (II.B), bilimsel suistimal (III.B), klinik çalışma kaydı (III.L.1 — kayıt, **ilk katılımcının onamı anında veya öncesinde** ve WHO/ICMJE standartlarını karşılayan halka açık bir kayıt sisteminde), destek kaynaklarının bildirimi (IV.3.A).

Ayrıca düzeltme/geri çekme terminolojisi: bilimi geçersiz kılmayan ama büyük düzeltme gerektiren dürüst hatalarda "retraction with republication" kullanılabilir; eski "replacement" terimi bırakıldı.

### Yazarlık — dört kriter (hepsi karşılanmalı)
1. Kavram/tasarıma veya veri toplama, analiz, yorumlamaya **önemli** katkı;
2. Taslağı yazma veya önemli entelektüel içerik için eleştirel revizyon;
3. Yayımlanacak sürümü **son onay**;
4. Çalışmanın tüm yönlerinden **hesap verebilirlik**.

Yalnızca fon sağlama, genel süpervizyon, veri toplama veya idari destek → teşekkür bölümü, yazarlık değil.

Yasak pratikler: **hediye yazarlık** (katkısı olmayan kıdemliyi ekleme), **hayalet yazarlık** (yazan kişiyi gizleme), yazar sırasının pazarlıkla belirlenmesi, gönderim sonrası gerekçesiz yazar ekleme/çıkarma.

### CRediT taksonomisi
14 rol: Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Visualization, Writing – original draft, Writing – review & editing. Çoğu dergi artık zorunlu tutuyor; yazma başlamadan yazarlarla netleştir.

## Yapay zekâ: ortak paydalar

Tüm büyük politikaların (ICMJE, COPE, IEEE, ACM, Elsevier, Springer Nature, PLOS) uzlaştığı üç ilke:
1. **YZ yazar olamaz** — hesap verebilirlik üstlenemez.
2. **İnsan yazar tümüyle sorumludur** — uydurma atıf, yanlış bilgi, intihal YZ'nin değil yazarın hatasıdır.
3. **İlgili kullanım beyan edilir.**

Ayrışma, "ilgili kullanım"ın nerede başladığında.

| Mecra | Beyan yeri | Dil düzeltme istisnası |
|---|---|---|
| ICMJE (tıp dergileri) | Kapak mektubu + uygun bölüm: yazım/düzenleme → Teşekkür; veri analizi/görsel üretimi → Yöntem | Politika metni kapsam dışı bırakmaz, beyanı önerir |
| IEEE | **Teşekkür bölümü**: kullanılan sistem adı + hangi bölümlerde + hangi düzeyde | Dil/gramer düzeltmesi politikanın amacı dışında sayılır; beyan yine de tavsiye edilir |
| ACM | İşin içinde tam beyan; temel kelime işlem araçları istisna | Var |
| Elsevier / Springer Nature | Yazar denetimi + doğrulama + beyan; ayrı beyan bölümü | Genelde var |
| NeurIPS ana track | Yöntemin parçası olan veya sıradışı LLM/ajan kullanımı belgelenir; rutin yazım/kod yardımı beyan gerektirmez | Var |
| NeurIPS Position Paper track | Çok daha sert — aşağıya bak | Yalnızca kopya düzeltme |
| TR Dizin dergileri (tipik) | Yazar beyanı bölümünde: araç adı, sürüm, kullanım amacı; YZ üretimi görsel/tablo ayrıca belirtilir | Dergiye göre değişir |

### NeurIPS 2026 Position Paper track — kategorileştirme örneği
Bu tablo, "ne kadarı fazla" sorusuna verilmiş en açık cevaplardan biri ve genel bir pusula olarak kullanılabilir:
- **Açıkça serbest:** yazım denetimi; hafif kopya düzeltme (yerel netlik, kısalık, cümle düzeyi cila — içerik değişmeden).
- **Sınırda:** ağır kopya düzeltme / satır düzenleme; çeviri-geri çeviri (anlam korunur, yüzey ifadesi büyük ölçüde değişir).
- **Açıkça yasak:** tek cümlelik plandan tam pasaj üretimi; iddiaları, akıl yürütmeyi veya çerçeveyi değiştiren YZ yeniden yazımı; özgün YZ-yazımı pasaj; YZ metnini insanın küçük düzenlemelerle sahiplenmesi.
Ayrıca: önemli YZ katkısı olan gönderimler **denetim izi** sunmak zorunda; prompt injection dahil hakemlik sürecini manipüle etme girişimi yasak; ajanlar/LLM'ler yazar olamaz.

### Hakemlik tarafı
Neredeyse tüm mecralar, gizli bir müsveddenin gizliliği garanti etmeyen üçüncü taraf sistemlere yüklenmesini yasaklar. IEEE, hakem raporunun YZ ile yazılmasını tümüyle yasaklar. ACM, tanımlayıcı bilgi çıkarıldıktan sonra dil kalitesi için kullanıma izin verir. Kullanıcı hakemlik yapıyorsa bunu hatırlat.

### YZ dedektörleri
Yanlış pozitif üretirler ve ana dili İngilizce olmayan yazarları orantısız etkilerler. Skor tek başına kanıt değildir; ne kullanıcıya "temiz" garantisi ver, ne de bir skoru suçlama gibi sun. Savunma, denetim izidir: taslak sürümleri, notlar, veri ve analiz kayıtları.

## Diğer etik başlıkları

**İntihal ve kendine intihal.** Benzerlik yazılımı (iThenticate/Turnitin) skoru bir tanı değil bir haritadır: kaynakça ve standart yöntem cümleleri şişirir, 3 kelimelik örtüşme masumdur, tek kaynaktan %8 örtüşme sorunludur. Birçok TR dergisi %20 gibi eşikler koyar. Kendi önceki metnini kaynak göstermeden tekrar kullanmak da ihlaldir.

**Salam dilimleme (salami slicing).** Tek çalışmayı yapay şekilde birden fazla makaleye bölmek. Test: her parça bağımsız bir araştırma sorusuna cevap veriyor mu? Aynı örneklemden ikinci makale çıkıyorsa ilkine atıf ver ve editöre kapak mektubunda bildir.

**Çift gönderim / yinelenen yayın.** Aynı anda iki dergiye gönderim yasak. Konferans bildirisinin genişletilmiş dergi sürümü çoğu alanda kabul edilir ama **açıkça beyan edilir** ve genişleme oranı (çoğunlukla %30+ yeni içerik) belirtilir.

**Görsel bütünlüğü.** Seçici kontrast/parlaklık müdahalesi, panel kopyalama, aynı görselin farklı deneyler için kullanılması. Ham dosyaları sakla; jel/mikroskopi çalışmalarında bu geri çekilmelerin başlıca nedenidir.

**Çıkar çatışması.** Finansal (fon, danışmanlık, patent, hisse, konuşmacı ücreti) ve finansal olmayan (kişisel ilişki, rekabet, ideolojik bağ). Şüphede beyan et. ICMJE Disclosure Form standarttır.

**Etik izin ve onam.** İnsan katılımcı, insan verisi, biyolojik materyal, hayvan, kişisel veri (KVKK/GDPR), başkasına ait ölçek/anket/fotoğraf kullanımı → izin gerekir. Onam metinde açıkça belirtilir; olgu sunumlarında yayın onamı zorunludur. Geriye dönük çalışmalarda muafiyet kararı da bir karardır ve yazılır.

**Kağıt fabrikaları (paper mill).** Yazarlık satın almak, sahte veri, sahte hakem önerisi (kontrol edilebilir olmayan e-posta adresleriyle) — hem geri çekilme hem kariyer sonu riski. Kullanıcı bu yönde bir hizmetten söz ediyorsa açıkça uyar.

**Geri çekme ve düzeltme.** Hata fark edildiğinde erken ve şeffaf davranmak, örtmekten her zaman daha az maliyetlidir. Erratum/corrigendum/retraction ayrımını ve COPE akış şemalarını hatırlat.
