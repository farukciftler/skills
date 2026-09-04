#!/usr/bin/env python3
"""
kling_video.py — fal.ai üzerinden Kling image-to-video üretimi (Moonstone).

Yalnızca standart kütüphane (urllib). Ek paket gerekmez.

Anahtar sırası:
  1. FAL_KEY ortam değişkeni
  2. ~/.config/fal/key   (tek satır, chmod 600)
Anahtar hiçbir çıktı dosyasına yazılmaz.

Alt komutlar
------------
  modeller   kullanılabilir Kling katmanları, alan adları, fiyat
  maliyet    senaryo.json ya da tek iş için tahmini ücret (API çağrısı yok)
  yukle      yerel görseli fal CDN'e yükler, URL döner
  uret       tek klip: gönder → bekle → indir → künye yaz
  toplu      senaryo.json'daki tüm çekimleri gönderir, hepsini bekler
  durum      request_id ile kuyruk durumu
  sonuc      tamamlanmış isteği indir
  calistir   herhangi bir fal uç noktasını ham JSON ile çalıştır (upscale, RIFE, Veo…)

Örnekler
--------
  python3 kling_video.py uret --gorsel cephe-9x16.jpg \
      --prompt "Slow, steady push-in toward the entrance..." \
      --model v3-pro --sure 5 --out cikti/cephe-01.mp4

  python3 kling_video.py toplu senaryo.json --out-dir cikti/2026-09
  python3 kling_video.py toplu senaryo.json --kuru        # sadece istek gövdesi + maliyet
  python3 kling_video.py calistir fal-ai/topaz/upscale/video \
      --json '{"video_url":"https://...","upscale_factor":2}' --out buyuk.mp4
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

QUEUE = "https://queue.fal.run"
REST = "https://rest.fal.ai"
CDN = "https://v3.fal.media"
UA = "moonstone-kling/1.0"
POLL_S = 4.0            # 1–5 dk süren işlerde 4 sn yeterli; 0,1 sn kota israfı
SUBMIT_RETRIES = 5

# ---------------------------------------------------------------- model tablosu
# Doğrulama: references/fal-kling-api.md (1 Eylül 2026 fal sayfaları).
# image  : başlangıç karesi alanının adı — uç noktaya göre değişiyor!
# end    : bitiş karesi alanı (yoksa None)
# dur    : izin verilen süreler (sn)
# audio  : generate_audio alanı var mı; audio_default: fal'daki varsayılan
# neg/cfg: negative_prompt / cfg_scale alanları var mı
# usd    : saniye başı ücret — (ses kapalı, ses açık)
MODELS = {
    "v3-pro": dict(id="fal-ai/kling-video/v3/pro/image-to-video",
                   image="start_image_url", end="end_image_url", dur=range(3, 16),
                   audio=True, audio_default=True, neg=True, cfg=True,
                   res="1080p", usd=(0.112, 0.168),
                   not_="Varsayılan. En iyi fizik/tutarlılık, negatif prompt + cfg var."),
    "v3-standard": dict(id="fal-ai/kling-video/v3/standard/image-to-video",
                        image="start_image_url", end="end_image_url", dur=range(3, 16),
                        audio=True, audio_default=True, neg=True, cfg=True,
                        res="720p?", usd=(0.084, 0.126),
                        not_="v3'ün ucuz katmanı; çözünürlük fal sayfasında yazmıyor."),
    "v3-turbo-pro": dict(id="fal-ai/kling-video/v3/turbo/pro/image-to-video",
                         image="start_image_url", end="end_image_url", dur=range(3, 16),
                         audio=True, audio_default=True, neg=True, cfg=True,
                         res="1080p", usd=(0.14, 0.14),
                         not_="Daha hızlı; ses açık/kapalı aynı fiyat."),
    "v3-turbo-standard": dict(id="fal-ai/kling-video/v3/turbo/standard/image-to-video",
                              image="image_url", end=None, dur=range(3, 16),
                              audio=False, audio_default=False, neg=False, cfg=False,
                              res="720p", usd=(0.112, 0.112),
                              not_="720p; negatif prompt ve bitiş karesi yok."),
    "v3-4k": dict(id="fal-ai/kling-video/v3/4k/image-to-video",
                  image="start_image_url", end="end_image_url", dur=range(3, 16),
                  audio=True, audio_default=True, neg=True, cfg=True,
                  res="4K", usd=(0.42, 0.42),
                  not_="Yerel 4K. Web hero / büyük ekran için; Reels için gereksiz."),
    "o3-pro": dict(id="fal-ai/kling-video/o3/pro/image-to-video",
                   image="image_url", end="end_image_url", dur=range(3, 16),
                   audio=True, audio_default=False, neg=False, cfg=False,
                   res="1080p", usd=(0.112, 0.14),
                   not_="Omni; başlangıç+bitiş karesi kontrolü güçlü. Negatif prompt yok."),
    "o3-standard": dict(id="fal-ai/kling-video/o3/standard/image-to-video",
                        image="image_url", end="end_image_url", dur=range(3, 16),
                        audio=True, audio_default=False, neg=False, cfg=False,
                        res="720p?", usd=(0.084, 0.112),
                        not_="En hızlı ölçülen (~95 sn / 5 sn klip)."),
    "v2.6-pro": dict(id="fal-ai/kling-video/v2.6/pro/image-to-video",
                     image="start_image_url", end="end_image_url", dur=(5, 10),
                     audio=True, audio_default=True, neg=True, cfg=False,
                     res="1080p", usd=(0.07, 0.14),
                     not_="Ses kapalıyken ucuz ve sağlam; cfg yok."),
    "v2.5-turbo-pro": dict(id="fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
                           image="image_url", end="tail_image_url", dur=(5, 10),
                           audio=False, audio_default=False, neg=True, cfg=True,
                           res="1080p", usd=(0.07, 0.07),
                           not_="Kaynak kompozisyonu ve ışığı iyi koruyor; ekonomik ana seçenek."),
    "v2.5-turbo-standard": dict(id="fal-ai/kling-video/v2.5-turbo/standard/image-to-video",
                                image="image_url", end=None, dur=(5, 10),
                                audio=False, audio_default=False, neg=True, cfg=True,
                                res="720p", usd=(0.042, 0.042),
                                not_="TASLAK katmanı: prompt denemesi için, yayın için değil."),
    "v2.1-pro": dict(id="fal-ai/kling-video/v2.1/pro/image-to-video",
                     image="image_url", end=None, dur=(5, 10),
                     audio=False, audio_default=False, neg=True, cfg=True,
                     res="1080p", usd=(0.09, 0.09), not_="Eski nesil."),
    "v2.1-master": dict(id="fal-ai/kling-video/v2.1/master/image-to-video",
                        image="image_url", end=None, dur=(5, 10),
                        audio=False, audio_default=False, neg=True, cfg=True,
                        res="1080p", usd=(0.28, 0.28), not_="Pahalı; v3-pro onu geçti."),
    "o1": dict(id="fal-ai/kling-video/o1/image-to-video",
               image="start_image_url", end="end_image_url", dur=range(3, 11),
               audio=False, audio_default=False, neg=False, cfg=False,
               res="1080p", usd=(0.112, 0.112),
               not_="İlk/son kare kontrolünde topluluk favorisi; girdi ≤10 MB."),
}
ALIASES = {"varsayilan": "v3-pro", "taslak": "v2.5-turbo-standard", "ekonomik": "v2.5-turbo-pro"}
DEFAULT_NEG = ("blur, distortion, warping, morphing, bending lines, warped windows, "
               "melting glass, distorted architecture, extra buildings, people, "
               "pedestrians, cars, crowds, text, logos, watermark, flicker, "
               "camera shake, fast camera, zoom out, low quality")


# ---------------------------------------------------------------- anahtar + http

def load_key():
    key = os.environ.get("FAL_KEY", "").strip()
    if key:
        return key
    kf = Path(os.path.expanduser("~/.config/fal/key"))
    if kf.is_file():
        key = kf.read_text(encoding="utf-8").strip()
        if key:
            return key
    sys.exit("fal.ai anahtarı yok. FAL_KEY ortam değişkenini ayarla ya da anahtarı "
             "~/.config/fal/key dosyasına yaz (chmod 600). Depoya ve sohbete yazma.")


def _req(method, url, data=None, headers=None, key=None, timeout=120, raw=False):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if key:
        h["Authorization"] = "Key " + key
    if headers:
        h.update(headers)
    body = None
    if data is not None:
        if isinstance(data, (bytes, bytearray)):
            body = bytes(data)
        else:
            body = json.dumps(data).encode("utf-8")
            h.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(url, data=body, method=method, headers=h)
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        payload = resp.read()
        if raw:
            return payload, dict(resp.headers)
        return (json.loads(payload) if payload else {}), dict(resp.headers)


def _err_text(e):
    """fal hata gövdesini okunur Türkçe'ye çevirir."""
    try:
        body = e.read().decode("utf-8", "replace")
        j = json.loads(body)
    except Exception:
        return f"HTTP {e.code}: {getattr(e, 'reason', '')}"
    det = j.get("detail")
    et = j.get("error_type") or ""
    if isinstance(det, list):
        parts = []
        for d in det:
            loc = ".".join(str(x) for x in d.get("loc", []) if x != "body")
            parts.append(f"{loc}: {d.get('msg')} [{d.get('type')}]")
            et = et or d.get("type", "")
        det = "; ".join(parts)
    hint = {
        "content_policy_violation": "İçerik denetimine takıldı (görsel ya da prompt). "
                                    "Prompt'tan insan/marka/metin ifadelerini çıkar, görseli değiştir.",
        "image_too_large": "Görsel çok büyük (sınır 50 MB). hazirla.py ile küçült.",
        "image_too_small": "Görsel çok küçük (kısa kenar ≥ 300 px).",
        "concurrent_requests_limit": "Eşzamanlı istek sınırı (yeni hesapta 2). Bekleyip yeniden dene.",
        "generation_timeout": "Üretim zaman aşımı. Yeniden gönder.",
    }.get(et, "")
    return f"HTTP {e.code} {et}: {det} {hint}".strip()


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# ---------------------------------------------------------------- yükleme

def upload(path, key, data_uri=False):
    """Yerel dosya → fal URL. Sıra: CDN v3 → GCS initiate/PUT → data URI."""
    p = Path(path)
    if not p.is_file():
        sys.exit(f"dosya yok: {path}")
    ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    data = p.read_bytes()
    if data_uri:
        return "data:%s;base64,%s" % (ctype, base64.b64encode(data).decode("ascii"))
    # 1) fal CDN v3
    try:
        tok, _ = _req("POST", REST + "/storage/auth/token?storage_type=fal-cdn-v3",
                      data={}, key=key)
        base = tok.get("base_url") or CDN
        j, _ = _req("POST", base + "/files/upload", data=data,
                    headers={"Content-Type": ctype, "X-Fal-File-Name": p.name,
                             "Authorization": f"{tok['token_type']} {tok['token']}"},
                    timeout=300)
        if j.get("access_url"):
            return j["access_url"]
    except Exception as e:  # noqa
        sys.stderr.write(f"[not] CDN yüklemesi olmadı ({e}); GCS deneniyor\n")
    # 2) GCS initiate + PUT
    try:
        init, _ = _req("POST", REST + "/storage/upload/initiate?storage_type=gcs",
                       data={"file_name": p.name, "content_type": ctype}, key=key)
        _req("PUT", init["upload_url"], data=data, headers={"Content-Type": ctype},
             timeout=300, raw=True)
        return init["file_url"]
    except Exception as e:  # noqa
        sys.stderr.write(f"[not] GCS yüklemesi olmadı ({e}); data URI kullanılıyor\n")
    # 3) data URI (fal kabul ediyor; büyük dosyada yavaş)
    return "data:%s;base64,%s" % (ctype, base64.b64encode(data).decode("ascii"))


def resolve_image(src, key, data_uri=False):
    if src.startswith(("http://", "https://", "data:")):
        return src
    return upload(src, key, data_uri)


# ---------------------------------------------------------------- istek kurma

def model_of(name):
    name = ALIASES.get(name, name)
    if name in MODELS:
        return name, MODELS[name]
    if name.startswith("fal-ai/"):          # ham uç nokta
        return name, dict(id=name, image="image_url", end=None, dur=range(1, 31),
                          audio=False, audio_default=False, neg=True, cfg=True,
                          res="?", usd=(0.0, 0.0), not_="bilinmeyen uç nokta")
    sys.exit(f"model bilinmiyor: {name}. Seçenekler: {', '.join(MODELS)} | {', '.join(ALIASES)}")


def build_args(m, image_url, prompt, duration, negative=None, cfg=None,
               end_url=None, audio=False, extra=None):
    if int(duration) not in m["dur"]:
        sys.exit(f"{m['id']} için süre {duration} geçersiz; izinli: {list(m['dur'])}")
    a = {m["image"]: image_url, "prompt": prompt, "duration": str(int(duration))}
    if m["neg"]:
        a["negative_prompt"] = negative if negative else DEFAULT_NEG
    if m["cfg"] and cfg is not None:
        a["cfg_scale"] = float(cfg)
    if end_url:
        if not m["end"]:
            sys.exit(f"{m['id']} bitiş karesi desteklemiyor")
        a[m["end"]] = end_url
    if m["audio"]:
        a["generate_audio"] = bool(audio)       # mimari içerikte ses kapalı — müzik post'ta
    elif audio:
        sys.stderr.write(f"[not] {m['id']} ses üretmiyor; generate_audio yok sayıldı\n")
    if extra:
        a.update(extra)
    return a


def cost(m, duration, audio=False):
    return m["usd"][1 if audio else 0] * int(duration)


# ---------------------------------------------------------------- kuyruk

def submit(endpoint, args, key, webhook=None):
    url = f"{QUEUE}/{endpoint}"
    if webhook:
        url += "?" + urllib.parse.urlencode({"fal_webhook": webhook})
    delay = 3.0
    for attempt in range(1, SUBMIT_RETRIES + 1):
        try:
            j, _ = _req("POST", url, data=args, key=key)
            return j
        except urllib.error.HTTPError as e:
            msg = _err_text(e)
            if e.code in (429, 500, 502, 503, 504) and attempt < SUBMIT_RETRIES:
                sys.stderr.write(f"[not] gönderim {attempt}. deneme: {msg} — {delay:.0f} sn sonra\n")
                time.sleep(delay); delay *= 2
                continue
            sys.exit("gönderim başarısız: " + msg)
        except urllib.error.URLError as e:
            if attempt < SUBMIT_RETRIES:
                time.sleep(delay); delay *= 2
                continue
            sys.exit(f"ağ hatası: {e}")


def status(status_url, key, logs=True):
    u = status_url + ("&" if "?" in status_url else "?") + "logs=1" if logs else status_url
    j, _ = _req("GET", u, key=key)
    return j


def wait(handle, key, timeout=1500, label=""):
    """status_url'i yoklar; COMPLETED olunca response_url'den sonucu döner."""
    t0 = time.time()
    seen_logs = 0
    last_pos = None
    while True:
        try:
            s = status(handle["status_url"], key)
        except urllib.error.HTTPError as e:
            sys.stderr.write(f"[not] durum sorgusu: {_err_text(e)}\n")
            time.sleep(POLL_S); continue
        st = s.get("status")
        if st == "IN_QUEUE":
            pos = s.get("queue_position")
            if pos != last_pos:
                sys.stderr.write(f"  {label} kuyrukta, sıra {pos}\n"); last_pos = pos
        elif st == "IN_PROGRESS":
            for lg in (s.get("logs") or [])[seen_logs:]:
                sys.stderr.write(f"  {label} · {lg.get('message','')}\n")
            seen_logs = len(s.get("logs") or [])
        elif st == "COMPLETED":
            j, _ = _req("GET", handle["response_url"], key=key)
            inf = (s.get("metrics") or {}).get("inference_time")
            return j, {"elapsed_s": round(time.time() - t0, 1), "inference_s": inf}
        elif st in ("FAILED", "ERROR"):
            sys.exit(f"{label} başarısız: {json.dumps(s.get('error') or s, ensure_ascii=False)}")
        if time.time() - t0 > timeout:
            sys.exit(f"{label} zaman aşımı ({timeout} sn). request_id={handle.get('request_id')} "
                     f"— 'sonuc' komutuyla sonra alınabilir.")
        time.sleep(POLL_S)


def first_file_url(result):
    """Sonuç JSON'undan ilk dosya URL'sini bulur (video / videos[0] / image …)."""
    if isinstance(result, dict):
        for k in ("video", "output", "image"):
            v = result.get(k)
            if isinstance(v, dict) and v.get("url"):
                return v["url"], v
        for v in result.values():
            if isinstance(v, dict) and v.get("url"):
                return v["url"], v
            if isinstance(v, list) and v and isinstance(v[0], dict) and v[0].get("url"):
                return v[0]["url"], v[0]
    return None, None


def download(url, out):
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    data, _ = _req("GET", url, raw=True, timeout=600)
    out.write_bytes(data)
    return out, len(data)


def write_kunye(out, record):
    """Klibin yanına .json künye + dizin günlüğüne satır. Anahtar asla yazılmaz."""
    side = Path(out).with_suffix(".json")
    side.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    log = Path(out).parent / "uretim-gunlugu.jsonl"
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return side


# ---------------------------------------------------------------- tek iş akışı

def run_job(job, key, out, kuru=False, webhook=None):
    """job: dict(model, gorsel, prompt, sure, negatif, cfg, bitis_gorsel, ses, ekstra, ad)"""
    name, m = model_of(job.get("model", "varsayilan"))
    dur = job.get("sure", 5)
    audio = bool(job.get("ses", False))
    est = cost(m, dur, audio)
    label = job.get("ad") or Path(out).stem
    if kuru:
        img = job["gorsel"] if job["gorsel"].startswith(("http", "data:")) else "<yüklenecek: %s>" % job["gorsel"]
        endv = job.get("bitis_gorsel")
        a = build_args(m, img, job["prompt"], dur, job.get("negatif"), job.get("cfg", 0.5 if m["cfg"] else None),
                       endv, audio, job.get("ekstra"))
        print(f"[kuru] {label}: {m['id']}  ~${est:.2f}\n" + json.dumps(a, ensure_ascii=False, indent=2))
        return est, None
    src = job["gorsel"]
    image_url = resolve_image(src, key, job.get("data_uri", False))
    end_url = resolve_image(job["bitis_gorsel"], key) if job.get("bitis_gorsel") else None
    args = build_args(m, image_url, job["prompt"], dur, job.get("negatif"),
                      job.get("cfg", 0.5 if m["cfg"] else None), end_url, audio, job.get("ekstra"))
    sys.stderr.write(f"→ {label}: {m['id']} · {dur} sn · ~${est:.2f}\n")
    h = submit(m["id"], args, key, webhook)
    h["_meta"] = dict(name=name, model=m, args=args, est=est, label=label, src=src,
                      src_sha=_sha(src) if os.path.isfile(src) else None, out=out,
                      submitted=dt.datetime.now().isoformat(timespec="seconds"))
    return est, h


def finish_job(h, key, timeout):
    meta = h["_meta"]
    result, timing = wait(h, key, timeout, meta["label"])
    url, fobj = first_file_url(result)
    if not url:
        sys.exit(f"{meta['label']}: sonuçta dosya URL'si yok: {json.dumps(result)[:400]}")
    out, n = download(url, meta["out"])
    args = dict(meta["args"])
    for k in ("image_url", "start_image_url", "end_image_url", "tail_image_url"):
        if k in args and str(args[k]).startswith("data:"):
            args[k] = "<data-uri>"
    rec = {
        "dosya": str(out), "kaynak_gorsel": meta["src"], "kaynak_sha256_16": meta["src_sha"],
        "model": meta["name"], "endpoint": meta["model"]["id"], "request_id": h.get("request_id"),
        "istek": args, "tahmini_usd": round(meta["est"], 3),
        "fal_url": url, "boyut_bayt": n, "fal_meta": fobj,
        "gonderim": meta["submitted"], "bitis": dt.datetime.now().isoformat(timespec="seconds"),
        "sure_sn": timing, "not": "Temsili görseldir; yapay zekâ desteğiyle hareketlendirilmiştir.",
    }
    side = write_kunye(out, rec)
    print(f"✓ {meta['label']}  {out}  ({n/1e6:.1f} MB, {timing['elapsed_s']} sn)  künye: {side.name}")
    return rec


# ---------------------------------------------------------------- komutlar

def cmd_modeller(a):
    print(f"{'ad':<20} {'çöz.':<6} {'süre':<7} {'$/sn ses kapalı':>15} {'$/sn ses açık':>14}  bitiş  neg  cfg  not")
    for k, m in MODELS.items():
        d = m["dur"]
        ds = f"{d[0]}–{d[-1]}" if isinstance(d, range) else "/".join(map(str, d))
        print(f"{k:<20} {m['res']:<6} {ds:<7} {m['usd'][0]:>15.3f} {m['usd'][1]:>14.3f}  "
              f"{'✓' if m['end'] else '·':^5}  {'✓' if m['neg'] else '·':^3}  {'✓' if m['cfg'] else '·':^3}  {m['not_']}")
    print("\ntakma adlar: " + ", ".join(f"{k}→{v}" for k, v in ALIASES.items()))
    print("5 sn v3-pro (ses kapalı) ≈ $%.2f · taslak ≈ $%.2f" % (cost(MODELS['v3-pro'], 5), cost(MODELS['v2.5-turbo-standard'], 5)))


def load_senaryo(path):
    j = json.loads(Path(path).read_text(encoding="utf-8"))
    shots = j.get("cekimler") or j.get("shots") or j
    if not isinstance(shots, list):
        sys.exit("senaryo.json: 'cekimler' listesi bekleniyor")
    defaults = j.get("varsayilan", {}) if isinstance(j, dict) else {}
    out = []
    for i, s in enumerate(shots, 1):
        d = dict(defaults); d.update(s)
        d.setdefault("ad", f"cekim-{i:02d}")
        for r in ("gorsel", "prompt"):
            if r not in d:
                sys.exit(f"{d['ad']}: '{r}' eksik")
        out.append(d)
    return out, (j if isinstance(j, dict) else {})


def cmd_maliyet(a):
    if a.senaryo:
        shots, _ = load_senaryo(a.senaryo)
    else:
        shots = [dict(model=a.model, sure=a.sure, ses=a.ses, ad="tek")]
    total = 0.0
    for s in shots:
        name, m = model_of(s.get("model", "varsayilan"))
        c = cost(m, s.get("sure", 5), bool(s.get("ses", False)))
        n = int(s.get("tekrar", 1))
        total += c * n
        print(f"{s.get('ad','tek'):<18} {name:<20} {s.get('sure',5):>2} sn ×{n}  ${c*n:.2f}")
    print(f"{'toplam':<18} {'':<20} {'':>2}       ${total:.2f}")


def cmd_yukle(a):
    key = load_key()
    print(upload(a.dosya, key, a.data_uri))


def cmd_uret(a):
    key = None if a.kuru else load_key()
    job = dict(model=a.model, gorsel=a.gorsel, prompt=a.prompt, sure=a.sure, negatif=a.negatif,
               cfg=a.cfg, bitis_gorsel=a.bitis_gorsel, ses=a.ses, ad=Path(a.out).stem,
               data_uri=a.data_uri, ekstra=json.loads(a.ekstra) if a.ekstra else None)
    est, h = run_job(job, key, a.out, a.kuru, a.webhook)
    if h and not a.arka_plan:
        finish_job(h, key, a.zaman_asimi)
    elif h:
        print(json.dumps({"request_id": h["request_id"], "status_url": h["status_url"],
                          "response_url": h["response_url"], "out": a.out}, indent=2))


def cmd_toplu(a):
    key = None if a.kuru else load_key()
    shots, top = load_senaryo(a.senaryo)
    out_dir = Path(a.out_dir or top.get("cikti_dizini") or "cikti")
    handles, total = [], 0.0
    for s in shots:
        reps = int(s.get("tekrar", 1))
        for r in range(1, reps + 1):
            suffix = f"-{r}" if reps > 1 else ""
            out = out_dir / f"{s['ad']}{suffix}.mp4"
            if out.exists() and not a.uzerine_yaz:
                sys.stderr.write(f"[atla] {out} var (--uzerine-yaz ile yeniden üret)\n"); continue
            est, h = run_job(s, key, str(out), a.kuru)
            total += est
            if h:
                handles.append(h)
    print(f"toplam tahmini: ${total:.2f}  ({len(handles)} iş gönderildi)")
    if a.kuru:
        return
    recs = []
    for h in handles:          # sırayla bekle; kuyruk zaten paralel çalıştırıyor
        recs.append(finish_job(h, key, a.zaman_asimi))
    print(f"\n{len(recs)} klip indi → {out_dir}")


def cmd_durum(a):
    key = load_key()
    ep = model_of(a.model)[1]["id"]
    root = "/".join(ep.split("/")[:2])       # fal durum yolu uygulama köküyle çalışır
    for base in (ep, root):
        try:
            j, _ = _req("GET", f"{QUEUE}/{base}/requests/{a.request_id}/status?logs=1", key=key)
            print(json.dumps(j, ensure_ascii=False, indent=2)); return
        except urllib.error.HTTPError as e:
            last = _err_text(e)
    sys.exit(last)


def cmd_sonuc(a):
    key = load_key()
    ep = model_of(a.model)[1]["id"]
    root = "/".join(ep.split("/")[:2])
    for base in (ep, root):
        try:
            j, _ = _req("GET", f"{QUEUE}/{base}/requests/{a.request_id}", key=key)
            break
        except urllib.error.HTTPError as e:
            j = None; last = _err_text(e)
    if j is None:
        sys.exit(last)
    url, fobj = first_file_url(j)
    if not url:
        print(json.dumps(j, ensure_ascii=False, indent=2)); return
    out, n = download(url, a.out)
    write_kunye(out, {"dosya": str(out), "request_id": a.request_id, "endpoint": ep,
                      "fal_url": url, "boyut_bayt": n, "fal_meta": fobj,
                      "bitis": dt.datetime.now().isoformat(timespec="seconds"),
                      "not": "Temsili görseldir; yapay zekâ desteğiyle hareketlendirilmiştir."})
    print(f"✓ {out} ({n/1e6:.1f} MB)")


def cmd_calistir(a):
    key = load_key()
    args = json.loads(a.json) if a.json else {}
    for k, v in list(args.items()):       # yerel dosya yollarını yükle
        if isinstance(v, str) and k.endswith("_url") and os.path.isfile(v):
            args[k] = upload(v, key)
    h = submit(a.endpoint, args, key)
    result, timing = wait(h, key, a.zaman_asimi, a.endpoint.split("/")[-1])
    url, fobj = first_file_url(result)
    if a.out and url:
        out, n = download(url, a.out)
        write_kunye(out, {"dosya": str(out), "endpoint": a.endpoint, "request_id": h.get("request_id"),
                          "istek": {k: (v if not str(v).startswith("data:") else "<data-uri>") for k, v in args.items()},
                          "fal_url": url, "boyut_bayt": n, "sure_sn": timing,
                          "bitis": dt.datetime.now().isoformat(timespec="seconds")})
        print(f"✓ {out} ({n/1e6:.1f} MB, {timing['elapsed_s']} sn)")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    sp.add_parser("modeller").set_defaults(fn=cmd_modeller)

    q = sp.add_parser("maliyet"); q.set_defaults(fn=cmd_maliyet)
    q.add_argument("senaryo", nargs="?"); q.add_argument("--model", default="varsayilan")
    q.add_argument("--sure", type=int, default=5); q.add_argument("--ses", action="store_true")

    q = sp.add_parser("yukle"); q.set_defaults(fn=cmd_yukle)
    q.add_argument("dosya"); q.add_argument("--data-uri", action="store_true")

    q = sp.add_parser("uret"); q.set_defaults(fn=cmd_uret)
    q.add_argument("--gorsel", required=True, help="yerel dosya, URL ya da data URI")
    q.add_argument("--prompt", required=True)
    q.add_argument("--model", default="varsayilan")
    q.add_argument("--sure", type=int, default=5)
    q.add_argument("--negatif", help="boş bırakılırsa mimari varsayılan negatif")
    q.add_argument("--cfg", type=float, default=0.5)
    q.add_argument("--bitis-gorsel", help="bitiş karesi (destekleyen modellerde)")
    q.add_argument("--ses", action="store_true", help="Kling yerel ses (varsayılan kapalı)")
    q.add_argument("--ekstra", help="uç noktaya geçecek ek JSON alanları")
    q.add_argument("--out", required=True)
    q.add_argument("--kuru", action="store_true", help="API'ye gitmeden istek gövdesi + maliyet")
    q.add_argument("--data-uri", action="store_true", help="CDN yerine base64 gönder")
    q.add_argument("--webhook"); q.add_argument("--arka-plan", action="store_true",
                                               help="gönderip çık; 'sonuc' ile al")
    q.add_argument("--zaman-asimi", type=int, default=1500)

    q = sp.add_parser("toplu"); q.set_defaults(fn=cmd_toplu)
    q.add_argument("senaryo"); q.add_argument("--out-dir")
    q.add_argument("--kuru", action="store_true"); q.add_argument("--uzerine-yaz", action="store_true")
    q.add_argument("--zaman-asimi", type=int, default=1500)

    q = sp.add_parser("durum"); q.set_defaults(fn=cmd_durum)
    q.add_argument("request_id"); q.add_argument("--model", default="varsayilan")

    q = sp.add_parser("sonuc"); q.set_defaults(fn=cmd_sonuc)
    q.add_argument("request_id"); q.add_argument("--model", default="varsayilan"); q.add_argument("--out", required=True)

    q = sp.add_parser("calistir"); q.set_defaults(fn=cmd_calistir)
    q.add_argument("endpoint"); q.add_argument("--json"); q.add_argument("--out")
    q.add_argument("--zaman-asimi", type=int, default=1500)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
