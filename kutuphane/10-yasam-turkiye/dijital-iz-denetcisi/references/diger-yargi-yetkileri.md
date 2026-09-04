# AB ve ABD Rotaları

Öznenin bu yargı yetkileriyle bağı varsa (ikamet, vatandaşlık, çalışma, hizmet kullanımı) ek kaldıraçlar açılır. Türkiye'de yaşayan biri için bile, veri sorumlusu AB'de yerleşikse veya AB'de hizmet sunuyorsa GDPR rotası çalışabilir.

---

## AB — GDPR

### m.17 — Silme hakkı ("unutulma hakkı")

Klasik rota. Talep, veri sorumlusuna doğrudan yapılır; yanıt süresi **1 ay** (karmaşık taleplerde 2 ay uzatma bildirimi ile).

Silme talebinin dayanabileceği gerekçeler: veri artık toplanma amacı için gerekli değil, rıza geri çekildi, veri hukuka aykırı işlendi, itiraz edildi ve üstün meşru menfaat yok.

**İstisnalar:** İfade ve bilgi özgürlüğü, hukuki yükümlülük, kamu yararı, arşiv/araştırma. Haber içeriğinde bu istisnalar sık devreye girer.

### m.21 — İşlemeye itiraz

Standart opt-out'tan **daha güçlü** bir araç ve az kullanılıyor. Meşru menfaate dayanan işlemeye itiraz edildiğinde, veri sorumlusu ya işlemeyi durdurmak ya da menfaatinin üstünlüğünü ispat etmek zorunda.

**Pratik kullanım:** LLM eğitimi. Birkaç AB veri koruma otoritesi, m.21 itirazları ve inceleme baskısıyla platformları AB kullanıcı verisi üzerinde eğitimi durdurmaya zorladı. Standart ayar toggle'ından farklı olarak yazılı, gerekçeli bir itiraz gönderilir.

**Metin kalıbı:** "GDPR m.21 uyarınca, kişisel verilerimin [amaç] için işlenmesine itiraz ediyorum." Somut madde referansı olmadan gönderilen talepler işleme alınmıyor.

### Arama motoru delisting

Google'ın AB kullanıcıları için ayrı bir delisting formu var (Google Spain kararı sonrası kurulan mekanizma). Türkiye'deki KVKK rotasından ayrı bir kanal — özne AB'de ise ikisi paralel işletilebilir.

### Şikâyet mercii

Kendi ülkesinin veri koruma otoritesine. Yanıt gelmezse veya yetersizse mahkeme yolu açık.

---

## ABD

Federal düzeyde genel bir veri koruma kanunu yok; eyalet bazlı işliyor. En güçlü rota Kaliforniya.

### Kaliforniya — DROP (en önemli gelişme)

**Delete Request and Opt-Out Platform.** Delete Act (SB 362, 2023) ile kuruldu, CPPA (CalPrivacy) tarafından işletiliyor.

| Tarih | Ne oldu |
|---|---|
| 1 Ocak 2026 | Tüketiciye açıldı — Kaliforniya sakinleri talep göndermeye başladı |
| 1 Ağustos 2026 | Veri simsarları için işleme yükümlülüğü başladı |

**Ne yapıyor:** Tek bir doğrulanmış talep ile Kaliforniya'da kayıtlı **tüm** veri simsarlarına silme talebi gönderiyor. Yüzlerce ayrı form doldurma işini tek submission'a indiriyor. Ücretsiz.

**Broker yükümlülükleri (1 Ağustos 2026'dan itibaren):** DROP'a en az **45 günde bir** girip talep listesini indirmek, verilen sürede kişisel veriyi (çıkarımlar dahil) silmek, doğrulanamayan talepleri en azından satış/paylaşım opt-out'u olarak işlemek, yeniden toplanmayı önlemek için suppression listesi tutmak, durumu DROP üzerinden raporlamak. İhlalde talep başına günlük para cezası.

**Gerçekçi sınırlar — raporda yaz:**
- Yalnızca **Kaliforniya sakinleri** kullanabiliyor (ikamet doğrulaması var)
- Yalnızca **Kaliforniya'da kayıtlı** brokerları kapsıyor (~500-600); toplam broker evreninin bir kısmı
- Sürekli izleme yok — tek seferlik talep
- Kamunun erişimine açık devlet kayıtları ve başka kanunlara (finansal, sağlık) tabi veriler kapsam dışı

**Sonuç:** DROP uygunsa manuel opt-out turundan **önce** çalıştırılır, ama onun yerine geçmez.

### CCPA / CPRA — bireysel talepler

DROP dışında, her şirkete ayrı ayrı silme (§1798.105) ve bilme (§1798.110) talebi gönderilebilir. Kendi self-servis formu olmayan brokerlar için (LexisNexis, Acxiom gibi kurumsal veri sağlayıcıları) tek yol bu — yazılı CCPA talebi, verinin kaynağını ve alıcılarını da sorarak.

### Diğer eyalet sicilleri

California, Vermont, Texas ve Oregon kayıtlı veri simsarı sicilleri yayımlıyor. Hedef listesi çıkarmak için bu resmî siciller blog listelerinden daha güvenilir — opt-out URL'leri sık değişiyor, siciller güncel kalıyor.

---

## Hangi rotanın açık olduğunu belirleme

| Durum | Açılan rota |
|---|---|
| Özne Türkiye'de ikamet ediyor | KVKK (varsayılan) |
| Veri sorumlusu AB'de yerleşik veya AB'ye hizmet sunuyor | GDPR paralel olarak açık |
| Özne AB'de ikamet ediyor / AB vatandaşı | GDPR birincil |
| Özne Kaliforniya sakini | DROP + CCPA |
| Özne başka bir ABD eyaletinde | O eyaletin gizlilik kanunu (varsa); yoksa brokerların gönüllü opt-out'u |
| Hiçbiri | Yalnızca platformların gönüllü politikaları — beklenti düşük tutulmalı |

**Not:** Bir talebin **hangi hukuki dayanakla** gönderildiğini yazmak, kabul oranını belirgin biçimde değiştiriyor. Dayanaksız "bunu kaldırın" talepleri, dayanağı olan taleplere göre çok daha sık yanıtsız kalıyor veya reddediliyor. Uygulanabilir bir dayanak varsa mutlaka madde numarasıyla yaz.
