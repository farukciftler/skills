# Seslendirme — ElevenLabs, Okunuş, Altyazı

Kaynak: `~/projects/reelsindustry` (`motor/ses/tts.py`, `okunus.py`, `altyazi.py`,
`.claude/skills/turkce-anlati/`), ölçümler 23–24 Ağustos 2026. Moonstone'a
uyarlandı: marka sesi sakin, ölçülü; karaoke vurgusu yok; CTA yok.

## 0. Ne zaman seslendirme

Mimari ve yaşam içeriği **sessiz** kalır (K8, brif 01/02/05/09: "CTA yok,
sessiz-derin ambiyans"). Seslendirme şu türlerde: alıcı rehberi (R7 "net ve
brüt"), süreç anlatısı (brif 08), tip tanıtımı (C2), satış ofisi. Kural:
konuşma bir bilgi taşıyorsa var, atmosfer için yok.

## 1. Mekanik

- Uç nokta: `POST /v1/text-to-speech/{voice_id}/with-timestamps` → `audio_base64`
  + `alignment{characters, character_start_times_seconds, character_end_times_seconds}`.
  **Karakter hizalaması modelden gelir**, tahmin değil; Whisper'a gerek yok.
- Model `eleven_multilingual_v2` (Türkçe). `voice_settings`: stability 0,55
  (sakin okuma), similarity_boost 0,8, style 0, speed 0,97.
- Çıktı WAV 48 kHz mono, tek geçişli loudnorm −16 LUFS (konuşmada tek geçiş
  oturuyor; müzikle miks `bitir.py`'de iki geçişli).
- Anahtar `~/.config/elevenlabs/key` (600) ya da `ELEVENLABS_API_KEY`.
  Hata sessizce yutulmaz: 402 ödeme/kota, 401 anahtar, 429 hız.
- Ses efekti: `POST /v1/sound-generation` (`text`, `duration_seconds`,
  `prompt_influence`) → MP3. Ambiyans yatağı için ("distant city at dusk, soft
  wind, no music"); Reels müziği değil.
- Kota: `GET /v1/user/subscription`.

```bash
python3 scripts/seslendir.py uret "Net ve brüt, her tipte yan yana." --ses bill --out vo.wav
python3 scripts/altyazi.py vo.zamanlama.json --out-dir alt --baslangic 0.6 --toplam 15
python3 scripts/bitir.py k1.mp4 k2.mp4 --seslendirme vo.wav --ses-baslangic 0.6 --altyazi alt/altyazi.txt \
    --muzik yatak.mp3 --muzik-db -20 --kapanis logo-kart.png --out r.mp4
```

## 2. Ses seçimi — marka kararı

reelsindustry ölçümü (aynı cümle, altı ses, ASR geri dönüşü): **altısı da
Türkçeyi %0 hatayla söylüyor; seçim tını.**

| ses | F0 ort. | F0 dip | not |
|---|---|---|---|
| bill | 157,8 Hz | 100 Hz | reelsindustry seçimi |
| brian | 112,3 Hz | 80,6 Hz | en derin |
| arnold | 121,6 Hz | 96,6 Hz | |
| george | 130,1 Hz | 97,8 Hz | |
| daniel | 137,4 Hz | 105,2 Hz | |

Moonstone için `deneme` komutuyla aynı marka cümlesini 3–4 sesle üret,
**Çise Hanım dinlesin, seçsin.** Kadın ses istenirse `sesler --dil turkish`
ile hesaptaki adayları listele. Seçim `senaryo.json`'a `ses:` alanıyla
kilitlenir; üretim değiştiremez. Ses klonlama yapılmaz (gerçek kişi, KVKK).

## 3. Okunuş — ölçülmüş kırılmalar (`seslendir.py okunus` otomatik)

| Yazım | Sonuç | Söylenen hâl |
|---|---|---|
| `426 km` | 2/2 felaket | `dört yüz yirmi altı kilometre` |
| `426 kilometre` | 2/3 bozuk | yazıyla |
| `%74'ü` | 1/2 bozuk | `yüzde yetmiş dördü` |
| `II. Mehmet` | yanlış sayı | `İkinci Mehmet` |
| `DSİ`, `İBB` | bozuk (İ harfi) | açık yazım |
| `1453'te`, `3,5`, `TBMM`, `vb.` | doğru | **dokunma** |

**Moonstone'a özgü dönüşümler** (betikte): `3+1` → `üç artı bir` (ekli:
`3+1'e` → `üç artı bire`) · `96,54 m²` → `doksan altı virgül elli dört
metrekare` · `3.000 m²` → `üç bin metrekare` · `10. kat` → `onuncu kat` ·
`%10'u` → `yüzde onu`. Altyazıda özgün yazım geri gelir (`gorunum` haritası):
ekranda `96,54 m²`, kulakta yazıyla.

Sayı + birim **her zaman** yazıyla; yıl ve ondalık tek başına rakam. Telefon
numarası seslendirmeye girmez (K4: karede ve seste iletişim yok; açıklamada).

## 4. Metin yazma — doğal, jenerik, konuşulan Türkçe

**Kimse "doksan altı virgül elli dört metrekare" demez.** Seslendirme spec okumaz;
sayı ve teknik veri **ekranda** (katman, altyazı, carousel) kalır, ses **hissi ve
tek bir somut şeyi** taşır. `okunus` dönüşümü bir emniyet kemeridir, bir yazım
tarzı değil.

| Yapma | Yap |
|---|---|
| "Tip 5, 3+1, net 96,54 metrekare, 10. katta." | "En üst katlardan biri. Salon, terasa açılıyor." (rakam ekranda) |
| "3.000 metrekare ticari alan bulunmaktadır." | "Aşağıda kafeler, dükkânlar, akşam kalabalığı." |
| "Kapalı yüzme havuzu, spor salonu, hamam ve sauna mevcuttur." | "Havuz, spor salonu, hamam... hepsi aynı katta." |
| "Detaylı bilgi için profildeki bağlantıya tıklayın." | "Görüşme takvimi profilde." — ya da hiç (K8) |

**Kurallar** (reelsindustry `turkce-anlati` + `insanca`, Moonstone tonuna uyarlı):
- **Söylendiği gibi yaz, sesli oku.** Ağız takılıyorsa metin yanlış.
- Cümle 6–12 kelime; ritim değişken. Kısa cümleleri noktayla dizme, virgülle bağla;
  vurgu için **tek** kısa cümle ayrı kalsın ("Üstte, huzur.").
- Kancada yükü öne al (devrik): "Akşam iniyor Aydıntepe'ye... ve bir bina, kat kat ışıklanıyor."
- Zamir yok, emir kipi yok, ünlem yok. "Siz" yerine "…çıkın" gibi davetkâr çekim en fazla bir kez.
- Parantez, noktalı virgül, uzun tire, dipnot yok. Üç nokta ve virgül serbest — onlar tonlamadır.
- Bir çekim = bir cümle (en fazla iki). Cümle çekimden uzunsa `parcali` uyarır; kısalt, hızlandırma.
- Kapanış çağrı değil bağlama: "Ayhanlar Mimarlık Yapı ve İnşaat güvencesiyle."
- `ton-ve-dil.md` sözlüğü: "lüks, fırsat, kaçırmayın, muhteşem" seste iki kat sırıtır.
- Doğrulanmamış veri (fiyat, teslim, mesafe, "yükseliyor") seslendirmeye girmez; ses metinden
  zor değişir.

## 4b. Tonlama — ses iniş çıkışını ne belirler

ElevenLabs'ta tonlama iki yerden gelir: **metin** (noktalama, cümle yapısı) ve
**voice_settings**. reelsindustry'de ölçülen, `seslendir.py`'de `--ton` ön ayarı:

| ton | stability | style | speed | ne zaman |
|---|---|---|---|---|
| `sakin` | 0,62 | 0,0 | 0,94 | mimari, manifesto, kapanış — düz, prestijli |
| `sicak` | 0,45 | 0,15 | 0,97 | yaşam, rehber — konuşur gibi, hafif iniş çıkış |
| `kanca` | 0,35 | 0,25 | 1,0 | ilk cümle — belirgin vurgu, merak |

- **stability düşük** = daha çok iniş çıkış, cümleler arası fark; **yüksek** = tekdüze.
  0,3'ün altı tutarsızlaşır; 0,7'nin üstü robotlaşır.
- **Metinle tonlama:** nokta düşürür, soru işareti yükseltir, virgül kısa durak,
  üç nokta askıda bırakır ("…çıkın..."), `<break time="0.4s" />` kesin durak
  (ölçülü; 1 sn üstü boşluk gibi okunur). Vurgulanacak kelimeyi cümle başına al —
  Türkçede vurgu yüklemden önceki öğeye düşer. Büyük harf, ünlem, `*` kullanma.
- **Çekim başına ayrı sentez** (`parcali`): her cümle kendi tonuyla üretilir,
  `previous_text`/`next_text` ile tını tutarlılığı korunur, cümle çekimin
  başlangıcına (+0,6 sn) yerleşir. Tek uzun sentezde kanca ile kapanış aynı
  tonda çıkar; parçalıda kanca `kanca`, gövde `sicak`, kapanış `sakin` olabilir.
- Hız 0,94–1,0; 1,05 üstü "satıcı" duyulur. Prestij yavaşlıkta.
- `eleven_v3` ses etiketleri ([softly], [pause]) var ama alpha ve zamanlama
  vermiyor; altyazı için `multilingual_v2` kalır `[?]`.
- Ölçüm yöntemi: aynı cümleyi üç tonla üret, dinle; ASR geri dönüşü anlaşılırlığı
  ölçer, tınıyı ölçmez (reelsindustry: altı ses de %0 WER, fark yalnızca kulakta).

## 5. Altyazı (`altyazi.py`)

- Öbek ≤ 4 kelime, ≤ 2,2 sn; noktalama ve > 0,45 sn sessizlik böler.
- Bir öbek = bir alfa PNG, concat demuxer `duration` satırları, ara kodlama yok.
  **Son girdi boş kareyle tekrarlanır** (demuxer son duration'ı yok sayar).
- Stil `post-uretimi.md` §8: beyaz Lora, yarı saydam lacivert kutu (150/255),
  en fazla iki satır, güvenli alan içinde. Kutu **mürekkep kutusundan**
  (alfa bbox); font metriği kutuyu yukarı kaydırıyordu.
- Karaoke kelime vurgusu yok; marka sakin. Rakam ekranda katmanla görünür, altyazıda değil — altyazı yalnızca söyleneni gösterir. Vurgu istenirse altın `#B8992F`
  yalnızca koyu kutu üstünde (7,1:1).
- Türkçe düzeltme: özel ad ve m² ifadeleri `gorunum` ile doğru gelir; yine de
  yayın öncesi öbekleri oku.

## 6. Miks (`bitir.py --seslendirme`)

reelsindustry `ffmpeg_serit.py` üç geçiş: (1) konuşma + yatak → WAV, (2) miksi
ölç, (3) `linear=true` ile uygula. Yatak 1–3 kHz'de −7 dB oyulur (ünsüz
anlaşılırlığı), `sidechaincompress threshold=0.03 ratio=8 attack=15 release=350`,
yatak seviyesi −20 dB (ölçülen SNR ≈ 32 dB, konuşma net; −12'de 23 dB, hâlâ
temiz; −4'te 15 dB, yarışıyor). Konuşma 0,6 sn'de başlar (açılış karartması).

## 7. Beyan

Açıklamaya: `Seslendirme yapay zekâ ile üretilmiştir.` (görsel beyanının
yanına). Yönetmelik Madde 18: tüketici davranışını etkileyen AI kullanımı
belirtilir; sentetik ses buna girer. Gerçek bir kişinin sesi klonlanmaz
(Madde 27).

## Kaynaklar
`~/projects/reelsindustry/motor/ses/{tts,okunus,altyazi,hizalama}.py` ·
`~/projects/reelsindustry/.claude/skills/turkce-anlati/{SKILL.md,references/olcumler.md}` ·
`~/projects/reelsindustry/docs/{ffmpeg-hatti.md,arastirma.md §"Sahada karar: ElevenLabs"}` ·
ElevenLabs API: `api.elevenlabs.io/v1/text-to-speech/{id}/with-timestamps`, `/v1/voices`,
`/v1/sound-generation`, `/v1/user/subscription`.
