# Otomasyon Boru Hattı — Sürekli Fırsat Takibi

Bu dosya, tek seferlik aramadan **sürekli izlemeye** geçmek için. Claude Code / sunucu ortamında
geçerli. Tek seferlik sorguda buraya bakma, gereksiz karmaşıklık ekler.

Değer önerisi net: fırsat, sen ararken değil sen bakmıyorken çıkar. Haftada bir manuel arama,
Perşembe sabahı 3 saat açık kalan bir kampanyayı kaçırır.

---

## 1. Mimari

```
  ┌─ toplayıcı ────────────┐   ┌─ depo ──────────┐   ┌─ karar ─────────┐   ┌─ bildirim ──┐
  │ kampanya sayfaları     │   │ SQLite          │   │ ampirik skor    │   │ e-posta     │
  │ (web_fetch)            │──▶│ fiyat_deposu.py │──▶│ p20 tabanına    │──▶│ eşik altı   │
  │ API veya tarayıcı      │   │ gözlem geçmişi  │   │ göre            │   │ olanlar     │
  └────────────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────┘
```

Dört parçayı ayrı tut. Toplayıcı değişir (bugün tarayıcı, yarın API), depo ve karar sabit kalır.
Hepsini tek scripte yığmak, kaynak değiştiğinde her şeyi yeniden yazmak demektir.

## 2. Depo ve ampirik skorlama

`scripts/fiyat_deposu.py` bunu hazır veriyor. Statik bantların yerini kendi gözlem geçmişin alır:

```bash
# gözlem ekle
python scripts/fiyat_deposu.py kaydet \
  --rota IST-SKP --gidis 2026-09-10 --donus 2026-09-13 \
  --fiyat 1850 --para TRY --tasiyici PC --aktarma 0 \
  --kaynak google_flights --kanit "https://..."

# elindeki fiyatı geçmişe göre skorla
python scripts/fiyat_deposu.py skor --rota IST-SKP --fiyat 1850 --gidis 2026-09-10
# → {"skor": 0.634, "etiket": "IYI", "guven": "orta", "taban_p20": 2920.0, ...}

# depodaki tüm fırsatları listele
python scripts/fiyat_deposu.py firsatlar --esik 0.6
```

Taban = aynı rota + aynı sezon gözlemlerinin **20. yüzdeliği**. Medyan yerine p20 seçilmesinin
sebebi: fırsat tanımı "normalin altı" değil, "gördüğüm en iyilere yakın".

**Güven kolonuna dikkat et.** `zayif` (< 8 gözlem) ise skoru tek başına kullanma, statik bantla
çapraz kontrol et ve kullanıcıya belirsizliği söyle. Depo ısınana kadar (rota başına ~20 gözlem)
skill'in iki bacağı birlikte yürür: ampirik + statik.

## 3. Toplayıcı yazarken

Sıra bu, çünkü maliyet ve kırılganlık sırası bu:

1. **Kampanya sayfaları** — en ucuz, en dayanıklı. `web_fetch`. Günde bir kez yeterli.
2. **API** — düzenli takibin doğru temeli. `tarayici-otomasyonu.md` §5'teki sağlayıcılar.
3. **Tarayıcı** — sadece API'nin vermediği şey için (Explore haritası, tarih ızgarası görseli).
   Cron'a tarayıcı koymak istiyorsan sıklığı düşük tut ve kırıldığında sessizce yanlış veri
   üretmemesini sağla (§5).

Her toplayıcı, aldığı her fiyatı `kaynak` ve `kanit` alanıyla depoya yazsın. Kanıtsız gözlem
sonradan doğrulanamaz.

## 4. Cron ve headless çalıştırma

Sunucuda düzenli koşma kalıbı:

```bash
# günlük kampanya taraması + fırsat bildirimi
0 7 * * *  cd ~/ucuz-bilet && ./tara.sh >> logs/tara.log 2>&1
```

Uzun süren bir tarama Claude Code ile yapılacaksa **tmux içinde detached** başlat, oturumu
öldürmeden izle. Faruk'un sunucusunda bu kalıp zaten kurulu — `serverim-build` skill'indeki
headless `claude -p` + tmux akışını kullan, yeniden icat etme.

Bildirim için mevcut e-posta borusunu kullan (`günaydin-bulten` ile aynı yol). Ayrı bir bildirim
kanalı kurmak yerine sabah bültenine **"Bugünün uçuş fırsatları"** bloğu eklemek daha az bakım
gerektirir ve okunma oranı daha yüksektir.

Bildirim içeriği kısa olsun: rota, tarih, fiyat, skor, tek link. Uzun tablo e-postada okunmaz.

## 5. Sessiz bozulmaya karşı korumalar

Otomasyonun gerçek riski çökmesi değil, **çalışmaya devam edip yanlış veri üretmesi**. Şu üç
kontrol zorunlu:

1. **Boş sonuç alarmı.** Bir toplayıcı üst üste 2 gün sıfır gözlem yazdıysa bozulmuştur.
   Sessizce geçme, bildirime "toplayıcı X veri döndürmüyor" satırı ekle.
2. **Aykırı değer kapısı.** Yeni gözlem, o rotanın medyanının 10 katı veya 1/10'u ise depoya
   `kaynak=supheli` ile yaz ve skorlamaya katma. Genelde yanlış alan okunmuştur.
3. **Kampanya tarihi kontrolü.** Toplayıcı kampanya metnini alıyorsa satış ve seyahat penceresini
   ayrıştır; süresi geçmişse depoya yazma. Süresi geçmiş kampanyayı bildirmek, otomasyonun
   güvenilirliğini bir seferde bitirir.

## 6. Ne izlenmeye değer

Her rotayı izlemek gürültü üretir. İzleme listesi şöyle kurulur:

- **Sabit hedefler** — kullanıcının gerçekten gitmeyi planladığı yerler (umre penceresi, planlanan
  seyahat). Günlük kontrol, dar tarih aralığı.
- **Fırsat havuzu** — `vizesiz-destinasyonlar.md` Tier 1'den 8–10 rota. Haftalık kontrol, geniş
  tarih aralığı. Buradaki amaç bir fiyat değil, **dip yakalamak**.
- **Kampanya akışı** — 5 taşıyıcı (TK, PC, AJ, W6, XY). Günlük. En yüksek verim/maliyet oranı
  burada; bir kampanya onlarca rotayı birden kapsar.

Toplam: günde ~15 istek. Bu, bloklanmayacak ve bakımı sürdürülebilir bir hacim. Yüzlerce rotayı
izleyen bir sistem kurmak, iki hafta sonra bakılmayan bir log dosyasına dönüşür.

## 7. Kurulum kontrol listesi

Kullanıcı "bunu otomatikleştir" dediğinde sırayla:

1. İzleme listesini onunla netleştir (§6). Liste olmadan boru hattı kurma.
2. `fiyat_deposu.py`'yi hedef makineye koy, `kaydet` ve `skor` komutlarını elle bir kez dene.
3. En basit toplayıcıyla başla: kampanya sayfaları + `web_fetch`. Çalıştığını gör.
4. Bildirimi bağla, bir gün gerçek çıktı üretmesini bekle.
5. Ancak bundan sonra API veya tarayıcı toplayıcısı ekle.
6. §5 korumalarını en sonda değil, toplayıcıyla **aynı anda** yaz.

Sırayı bozup baştan tarayıcılı, çok kaynaklı bir sistem kurmaya çalışmak en sık görülen ve en
çok zaman kaybettiren hata.
