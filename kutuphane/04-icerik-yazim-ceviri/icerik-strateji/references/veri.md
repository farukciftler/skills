# Veriden üretim listesi çıkarma

Site GA4'e olay gönderiyor (bkz. `web/src/lib/analytics.ts`). Dördü doğrudan
"ne üretelim" sorusunu yanıtlıyor. Envanter betiği depodaki **eksiği** gösteriyor;
bu dosya okurun **istediğini** gösteriyor. İkisi farklı sorular ve ikisine de
bakmak gerekiyor.

> Rıza kapılı: veri yalnızca kabul eden ziyaretçilerden geliyor. Yani mutlak
> sayılar gerçek trafiğin altında. **Oranlara ve sıralamaya bak, mutlak sayıya
> değil.**

## 1. `search` + `result_count = 0` — en ucuz fikir kaynağı

İnsanların sitede arayıp **bulamadığı** şey. Uydurma değil, kanıt.

GA4'te: `search` olayı → `result_count` parametresi 0 olanlar → `search_term`
kırılımı.

Okuma biçimi:

| Sorgu deseni | Ne demek | Eylem |
| --- | --- | --- |
| Var olmayan bir şehir adı | O şehir için talep var | Küme koşulları sağlanıyorsa aç |
| Var olan şehirde olmayan bir mekan | Küme eksik | O mekanı üret — P1 zaten diyordur |
| Var olan kaydın başka adı | Kayıt var ama bulunamıyor | Başlık/özet o adı taşımıyor; **yeni kayıt değil**, mevcudu düzelt |
| Tip dışı bir şey (otel, vize, uçuş) | Site bunu yapmıyor | Üretme. Rezervasyon OTA'nın işi. |

Dördüncü satır önemli: sıfır sonuç her zaman içerik açığı değil. Bazen sitenin
kapsamı dışında bir istek ve doğru cevap "hayır".

## 2. `not_found` — var sandıkları adres

`attempted_path` kırılımı. İki tür bulgu veriyor:

- **Silinmiş ya da değişmiş slug.** Dışarıdan bağlantı geliyor demektir; kaydı
  geri getirmek ya da yönlendirme koymak gerekir.
- **Tahmin edilen adres.** Okur `/tr/mekanlar/emevi-camii` yerine
  `/tr/mekanlar/umeyye-camii` deniyorsa adlandırma sezgisi tutmuyor.

## 3. `content_click` — hub gerçekten dağıtıyor mu

En değerli ve en çok atlanan sinyal. `click_context = "hub"` olan olaylar, şehir
sayfasından mekana geçişleri sayıyor.

Şehir sayfası çok görüntülenip az `content_click` üretiyorsa üç olasılık var ve
sırayla elenir:

1. **Mekan yok.** Envanter zaten ölü hub diyordur — önce onu kapat.
2. **Kartlar zayıf.** Görsel yok, özet ilgi çekmiyor. Yeni kayıt değil, mevcut
   kayıtların özet ve görselleri düzeltilmeli.
3. **Şehir metni çok uzun.** Okur mekanlara ulaşmadan bırakıyor; `read_progress`
   ile çapraz kontrol et.

## 4. `read_progress` — içerik tutuyor mu

%25'te belirgin düşüş varsa sorun **giriş paragrafında**. Ön yüz ilk paragrafı
serif ve büyük basıyor; tutmuyorsa yazının tamamı okunmuyor.

%100'e ulaşan oran yüksekse o kayıt iyi çalışıyor — **benzerini üret**. Hangi
tipte, hangi şehirde olduğuna bak, deseni tekrarla.

`content_key` boyutu sayesinde üç dil tek satırda toplanıyor, `content_language`
ile dil kırılımı alınabiliyor. Bir kayıt Türkçede tutup İngilizcede tutmuyorsa
sorun içerikte değil çeviridedir — `ceviri` becerisiyle o sürümü gözden geçir.

## GA4'te tanımlanması gereken özel boyutlar

Bunlar tanımlanmadan yukarıdaki kırılımların hiçbiri raporlarda görünmüyor:

| Parametre | Kapsam |
| --- | --- |
| `content_key` | Olay |
| `content_language` | Olay |
| `content_type` | Olay |
| `click_context` | Olay |
| `search_term` | Olay *(GA4'ün yerleşik alanı, yine de doğrula)* |
| `result_count` | Olay |

Yönetici → Özel tanımlar → Özel boyut oluştur.

## Sıralama kuralı

Veri ve envanter çeliştiğinde **envanter kazanır**. Sebebi: envanterdeki bulgular
zaten kırık şeyler; veri ise iyileştirme fırsatı. Kırığı bırakıp fırsat
kovalamak, ölü hub dururken yeni şehir açmakla aynı hata.
