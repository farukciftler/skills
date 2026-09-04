# Veri Alma (Acquisition)

## Neden düz HTTP çalışmaz

sahibinden.com bot korumasına sahiptir. `curl`, `requests`, `httpx`, `WebFetch`,
ham headless Chrome → HTTP 403 veya şu sayfa:

```
Olağan dışı erişim tespit ettik...
Destek kodu: XXXXXXXX-MMDD
```

Bu sayfa 200 döner, yani "başarılı" görünür. **Parser bunu tanır ve
`BlockedError` fırlatır.** Sessizce boş sonuç döndürmez.

## Desteklenen yöntemler

### A) CDP — kullanıcının kendi Chrome'u (varsayılan)

Kullanıcı kendi tarayıcısında zaten insan olarak doğrulanmıştır. Araç o oturuma
bağlanır, yeni bir kimlik üretmez.

**Kurulum (kullanıcı bir kez yapar):**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.emlakarama-chrome"
```

Açılan pencerede `https://www.sahibinden.com` adresine git, sayfa normal
yükleniyorsa hazırsın. (Doğrulama çıkarsa kullanıcı kendisi geçer — araç
CAPTCHA çözmez.)

**Kullanım:**

```bash
emlakarama fetch 'https://www.sahibinden.com/satilik-daire/istanbul-kadikoy' \
  --cdp --pages 5 --out samples/
emlakarama sync kadikoy-3+1 --cdp --max-pages 6
```

Davranış:
- `playwright.chromium.connect_over_cdp("http://localhost:9222")`
- Mevcut context'i kullanır (çerezler, oturum korunur)
- Sayfalar arası **4–9 sn rastgele** bekleme (insan hızı)
- `--rate` ile dakikada azami sayfa (varsayılan 12)
- `--max-pages` zorunlu üst sınır (varsayılan 20, oturum başına sert tavan 200)
- Her sayfa diske ham HTML olarak yazılır → tekrar parse için ağa çıkmaya gerek yok
- Engel sayfası görülürse **durur**, o ana kadarki veriyi saklar, kullanıcıya
  destek kodunu ve "tarayıcıda elle bir sayfa aç" talimatını verir. Yeniden
  denemez, IP/UA değiştirmez.

Playwright kurulu değilse: `pip install playwright && playwright install chromium`
(chromium indirmesi yalnızca CDP dışı mod için gerekir; CDP modunda kullanıcının
kendi Chrome'u kullanılır.)

### B) Elle kaydedilmiş HTML

En güvenli yol, kurulum gerektirmez.

1. Kullanıcı aramayı tarayıcıda yapar
2. `Cmd+S` → "Web Page, Complete" (veya `Cmd+Option+U` → tümünü kopyala)
3. `samples/` altına kaydeder

```bash
emlakarama parse samples/*.html --format csv > ilanlar.csv
emlakarama sync kadikoy-3+1 --from samples/
```

Çok sayfa için: kullanıcıya `pagingOffset` değerleri hazır URL listesi ver,
sırayla açıp kaydetsin.

### C) Sadece URL

Fetch hiç gerekmiyorsa yapma. `emlakarama url` / `learn` / `plan` komutları
tamamen çevrimdışıdır.

## Yapılmayanlar

Bu araç bilinçli olarak şunları **içermez** ve eklenmesi kabul edilmez:

- Proxy havuzu / IP rotasyonu
- User-Agent, `sec-ch-ua`, TLS/JA3 parmak izi taklidi
- `stealth` eklentileri, `navigator.webdriver` gizleme
- CAPTCHA çözme servisi entegrasyonu
- Engel sayfasında otomatik yeniden deneme / geri çekilip tekrar deneme döngüsü
- Paralel eşzamanlı istek

Kullanıcı bunları isterse: aracın bunu yapmadığını bir cümleyle söyle, (B)
yöntemini öner, konuyu uzatma.

## Hız sınırı ve nezaket

| Ayar | Varsayılan | Sert tavan |
|---|---|---|
| Sayfa arası bekleme | 4–9 sn rastgele | ≥ 3 sn |
| Dakikada sayfa | 12 | 20 |
| Oturumda sayfa | 20 (`--max-pages`) | 200 |
| Eşzamanlılık | 1 | 1 |

Takip aramaları için günde 1–2 çalıştırma yeterlidir. `date_desc` + tek sayfa
ile yeni ilanların tamamı yakalanır; tüm arşivi her gün yeniden çekmek gereksizdir.

## Önbellek

Çekilen her sayfa `cache/{canonical_key}/{offset}-{timestamp}.html` olarak
saklanır. `--cache-ttl` (varsayılan 6 saat) içinde aynı sayfa istenirse ağa
çıkılmaz. `emlakarama cache clear` temizler, `emlakarama cache size` boyut verir.

Ham HTML'i saklamak önemlidir: markup değişince veya parser hatası bulununca
geçmişi yeniden işleyebilirsin.
