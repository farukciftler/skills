# Topluluk gönderisi şablonları

İngilizce, kısa, ilk satır tek başına anlamlı. `<>` içindeki her yer doldurulur;
doldurulamayan satır **silinir**, boş bırakılmaz (`CLAUDE.md` § 4).

Künye satırı (`templates/metadata.md` § Künye satırı ile birebir aynı):

```
Weft Records is a fictional label. These recordings are new works produced with AI-assisted composition and human arrangement, editing and art direction.
```

Müziği plak gibi sunan gönderilerde (1, 2, 3) bulunur; kimlik anlatan ve anket
gönderilerinde (4, 5) gerekmez.

---

## 1 — Yayın günü

Görsel: albüm kapağı (kare — akışta doğru duran biçim).

```
<ARTIST> — <Album title>. <One line that says what the record actually is.>

<n> tracks, <duration>. <The single constraint the record is built on, in one sentence.>

Watch: <video URL>

Weft Records is a fictional label. These recordings are new works produced with AI-assisted composition and human arrangement, editing and art direction.

#<tag1> #<tag2> #<tag3>
```

**İlk satır kritik.** Akışta bu satır ve görsel görünür; "New release out now"
hiçbir şey söylemiyor. Plağın ne olduğunu söyle.

---

## 2 — Seri tamamlandı

Görsel: serinin kapaklarından bir kontakt sayfası ya da en güçlü kapak.

```
<Series name> is complete: <n> records, <n> cities/artists, one rule — <the single variable that stayed fixed>.

Full series: <playlist URL>

Weft Records is a fictional label. These recordings are new works produced with AI-assisted composition and human arrangement, editing and art direction.

#<tag1> #<tag2>
```

---

## 3 — Playlist / işlev duyurusu

```
<n> hours of <function phrase>, in one place — <playlist name>.

<One sentence on what makes this set coherent: instrument, region, tuning, tempo.>

<playlist URL>

Weft Records is a fictional label. These recordings are new works produced with AI-assisted composition and human arrangement, editing and art direction.
```

---

## 4 — Şerit / kimlik gönderisi (yayından ~7 gün sonra)

Görsel: enstrüman, sahne fotoğrafı ya da kapağın bir detayı. Video bağlantısı
**yok** — bu gönderi satış değil, kimlik.

```
<One concrete fact about the instrument, mode, rhythm or region behind <ARTIST>.>

<Two or three sentences that explain why that constraint changes how the record sounds. No adjectives about feelings; name the mechanism.>

<ARTIST> stays inside that lane on every release. That's the whole idea.
```

Bu gönderi sanatçının `identity.md` § Şerit tablosundan yazılır. Kimlik
kartında olmayan bir iddia burada **üretilmez**.

---

## 5 — Anket

```
<Question about format, order or length — never about the lane itself.>
```

Seçenekler kısa ve karşılaştırılabilir olsun (ör. `30 min`, `1 hour`, `3 hours`).
Sonuç `channel_log.csv` notuna yazılır. Şerit, tempo, tür ve enstrüman
seçenekleri **ankete konmaz** — kimlik oylanmaz.

---

## Yazmadan önce

- Sağlık iddiası taraması: `healing-audio-youtube-seo/references/claims-and-policy.md`. Vücut hakkında fiil yok, müzik hakkında fiil serbest.
- Etiket en fazla üç, sonda.
- Bağlantı çalışıyor mu — gönderiden sonra tıkla ve gör.
- Gönderi geçildikten sonra `/posts` listesinde göründüğünü doğrula, URL'ini `channel_log.csv`'ye yaz.
