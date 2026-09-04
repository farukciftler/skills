#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kartela Klinik OS — arayuz denetimi kosucusu.

Uc demo rolu ile oturum acar, her rotanin uc gorunumde ekran goruntusunu alir
ve ayni gezintide olculebilir kusurlari (yatay tasma, kucuk dokunma hedefi,
etiketsiz alan, konsol hatasi, dusuk kontrast) JSON olarak toplar.

Kullanim:
    python3 .claude/skills/arayuz-denetimi/scripts/denetim_ss.py
    python3 ... --cikti denetim --tema acik,koyu --rol sekreter
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

TABAN = os.environ.get("KARTELA_TABAN", "http://127.0.0.1:8091")
PAROLA = "Kartela2026!"

ROLLER = {
    "danisman": {
        "eposta": "danisman@demo.local",
        "rotalar": ["/bugun", "/takvim", "/danisanlarim", "/hakedisim",
                    "/guncellemeler", "/gruplar", "/projeler", "/gorevlerim",
                    "/kaynaklar", "/stajyerler", "/bildirimler"],
    },
    "sekreter": {
        "eposta": "sekreter@demo.local",
        "rotalar": ["/pano", "/seanslar", "/tahsilat", "/danisanlar", "/talepler",
                    "/guncellemeler", "/gruplar", "/projeler", "/stajyerler",
                    "/senkron"],
    },
    "yonetici": {
        "eposta": "yonetici@demo.local",
        "rotalar": ["/kokpit", "/seanslar", "/gelir", "/danismanlar",
                    "/onay-merkezi", "/hakedis", "/doluluk", "/danisanlar",
                    "/guncellemeler", "/gruplar", "/projeler", "/stajyerler",
                    "/belgeler", "/ayarlar", "/denetim"],
    },
    # Yurutucu seans almaz; kabugu grup calismalari uzerine kuruludur.
    "yurutucu": {
        "eposta": "yurutucu@demo.local",
        "rotalar": ["/gruplar", "/gorevlerim", "/projeler", "/kaynaklar",
                    "/guncellemeler"],
    },
    # Stajyerin acilisi kendi gelisim panosu.
    "stajyer": {
        "eposta": "stajyer@demo.local",
        "rotalar": ["/gelisimim", "/gorevlerim", "/projeler", "/kaynaklar",
                    "/gruplar", "/guncellemeler"],
    },
}

GORUNUMLER = {
    "mobil":    {"width": 390,  "height": 844, "dpr": 3, "dokunma": True},
    "tablet":   {"width": 1024, "height": 768, "dpr": 2, "dokunma": True},
    "masaustu": {"width": 1440, "height": 900, "dpr": 1, "dokunma": False},
}

# ── Olcum betikleri ──────────────────────────────────────────────────────────

OLC = r"""() => {
  const se = document.scrollingElement;
  const etkilesimli = [...document.querySelectorAll(
    'a[href],button,input,select,textarea,[role=button],[role=tab],[role=link],[tabindex]:not([tabindex="-1"])')]
    .filter(e => {
      const cs = getComputedStyle(e);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && e.offsetParent !== null;
    });

  const tanim = e => (e.tagName.toLowerCase() +
    (e.id ? '#' + e.id : '') +
    (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\s+/).slice(0,3).join('.') : '') +
    ' «' + (e.textContent || '').trim().slice(0, 30) + '»');

  // dokunma hedefleri
  const kucuk = etkilesimli.map(e => {
    const r = e.getBoundingClientRect();
    return {sec: tanim(e), w: Math.round(r.width), h: Math.round(r.height)};
  }).filter(o => o.w > 0 && o.h > 0 && (o.w < 44 || o.h < 44));

  // etiketsiz form alani
  const etiketsiz = [...document.querySelectorAll('input:not([type=hidden]),select,textarea')]
    .filter(e => !(e.labels && e.labels.length) && !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby') && !e.closest('label'))
    .map(e => tanim(e));

  // adsiz buton (yalniz simge)
  const adsizButon = [...document.querySelectorAll('button,[role=button],a[href]')]
    .filter(e => !(e.textContent || '').trim() && !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby') && !e.getAttribute('title'))
    .map(e => e.outerHTML.slice(0, 140));

  // 16px alti girdi — iOS yakinlasmasi
  const kucukGirdi = [...document.querySelectorAll('input:not([type=hidden]),select,textarea')]
    .map(e => ({sec: tanim(e), px: parseFloat(getComputedStyle(e).fontSize)}))
    .filter(o => o.px < 16);

  // baslik hiyerarsisi
  const basliklar = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
    .map(e => ({lv: +e.tagName[1], t: (e.textContent||'').trim().slice(0,50)}));

  // tablo anlamsalligi
  const tablolar = [...document.querySelectorAll('table')].map(t => ({
    th: t.querySelectorAll('th').length,
    scope: t.querySelectorAll('th[scope]').length,
    caption: !!t.querySelector('caption'),
    sutun: t.querySelector('tr') ? t.querySelector('tr').children.length : 0,
    satir: t.querySelectorAll('tbody tr').length,
    tasma: t.scrollWidth > t.clientWidth,
    kapTasiyor: (() => { let p = t.parentElement; for (let i=0;i<3&&p;i++,p=p.parentElement) {
        const o = getComputedStyle(p).overflowX; if (o==='auto'||o==='scroll') return true; } return false; })(),
  }));

  // izgara/div-tablo sayisi (anlamsal olmayan tablo suphesi)
  const rolTablo = document.querySelectorAll('[role=table],[role=grid]').length;

  // yatay tasan ogeler
  const tasanlar = [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect();
    return r.width > 0 && (r.right > se.clientWidth + 1 || r.left < -1);
  }).slice(0, 12).map(e => {
    const r = e.getBoundingClientRect();
    return {sec: tanim(e), sol: Math.round(r.left), sag: Math.round(r.right)};
  });

  // kontrast — metin tasiyan yaprak ogeler
  // getComputedStyle oklch()/oklab() dondurur; sRGB'ye canvas ile cevrilir.
  const cnv = document.createElement('canvas'); cnv.width = cnv.height = 1;
  const cx = cnv.getContext('2d', {willReadFrequently: true});
  const onbellek = new Map();
  const cozRGBA = css => {
    if (onbellek.has(css)) return onbellek.get(css);
    cx.clearRect(0,0,1,1);
    cx.fillStyle = '#000'; cx.fillStyle = css;
    cx.fillRect(0,0,1,1);
    const d = cx.getImageData(0,0,1,1).data;
    // saydam renk siyah zemine dusmus olur; alfayi ayri cikar
    const v = [d[0], d[1], d[2], d[3]/255];
    onbellek.set(css, v);
    return v;
  };
  const kar = (on, arka) => on[3] >= 0.999 ? on.slice(0,3)
    : [0,1,2].map(i => Math.round(on[i]*on[3] + arka[i]*(1-on[3])));

  const yaprak = [...document.querySelectorAll('body *')].filter(e =>
    e.children.length === 0 && (e.textContent||'').trim().length > 0);
  const opakArka = e => {
    const yigin = [];
    let p = e;
    while (p) {
      const c = cozRGBA(getComputedStyle(p).backgroundColor);
      if (c[3] > 0.001) yigin.push(c);
      if (c[3] >= 0.999) break;
      p = p.parentElement;
    }
    let sonuc = [255,255,255];
    for (let i = yigin.length - 1; i >= 0; i--) sonuc = kar(yigin[i], sonuc);
    return sonuc;
  };
  const lum = ([r,g,b]) => {
    const k = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
    return 0.2126*k(r) + 0.7152*k(g) + 0.0722*k(b);
  };
  const kontrastlar = [];
  for (const e of yaprak.slice(0, 500)) {
    const cs = getComputedStyle(e);
    if (parseFloat(cs.opacity) < 0.99) continue;   // solmus oge ayri degerlendirilir
    const bg = opakArka(e);
    const fg = kar(cozRGBA(cs.color), bg);
    const a = lum(fg), b = lum(bg);
    const o = (Math.max(a,b) + 0.05) / (Math.min(a,b) + 0.05);
    const px = parseFloat(cs.fontSize);
    const kalin = (parseInt(cs.fontWeight)||400) >= 700;
    const buyuk = px >= 18.66 || (kalin && px >= 14);
    const esik = buyuk ? 3 : 4.5;
    if (o < esik) kontrastlar.push({
      sec: tanim(e), oran: +o.toFixed(2), esik, px: +px.toFixed(1),
      on: `rgb(${fg.join(',')})`, arka: `rgb(${bg.join(',')})`, ham: cs.color,
    });
  }

  // odak halkasi — ilk 10 etkilesimli ogede :focus-visible stili var mi
  return {
    olcu: {w: se.clientWidth, h: se.clientHeight, scrollW: se.scrollWidth, scrollH: se.scrollHeight},
    yatayTasma: se.scrollWidth - se.clientWidth,
    kucukHedef: kucuk,
    etiketsizAlan: etiketsiz,
    adsizButon: adsizButon,
    kucukGirdi: kucukGirdi,
    basliklar: basliklar,
    tablolar: tablolar,
    rolTablo: rolTablo,
    tasanOge: tasanlar,
    kontrast: kontrastlar.sort((a,b) => a.oran - b.oran).slice(0, 25),
    kontrastToplam: kontrastlar.length,
  };
}"""

SEKME_AC = r"""() => {
  const t = [...document.querySelectorAll('[role=tab],button')].filter(e =>
    e.getAttribute('role') === 'tab');
  return t.map(e => (e.textContent||'').trim());
}"""


def token_al(eposta: str) -> dict:
    veri = json.dumps({"identity": eposta, "password": PAROLA}).encode()
    istek = urllib.request.Request(
        f"{TABAN}/api/collections/kullanicilar/auth-with-password",
        data=veri, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(istek, timeout=10) as y:
        return json.loads(y.read())


def guvenli(ad: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", ad.lower()).strip("-") or "kok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cikti", default="denetim")
    ap.add_argument("--rol", default=",".join(ROLLER))
    ap.add_argument("--gorunum", default=",".join(GORUNUMLER))
    ap.add_argument("--tema", default="acik")
    ap.add_argument("--taban", default=TABAN)
    a = ap.parse_args()

    kok = Path(a.cikti)
    (kok / "ss").mkdir(parents=True, exist_ok=True)
    roller = [r for r in a.rol.split(",") if r in ROLLER]
    gorunumler = [g for g in a.gorunum.split(",") if g in GORUNUMLER]
    temalar = a.tema.split(",")

    rapor = []

    with sync_playwright() as p:
        tarayici = p.chromium.launch(args=["--no-sandbox", "--force-color-profile=srgb"])
        for rol in roller:
            oturum = token_al(ROLLER[rol]["eposta"])
            depo = json.dumps({"token": oturum["token"], "record": oturum["record"]})
            for gad in gorunumler:
                g = GORUNUMLER[gad]
                for tema in temalar:
                    ctx = tarayici.new_context(
                        viewport={"width": g["width"], "height": g["height"]},
                        device_scale_factor=g["dpr"],
                        has_touch=g["dokunma"],
                        is_mobile=g["dokunma"] and g["width"] < 500,
                        color_scheme="dark" if tema == "koyu" else "light",
                        locale="tr-TR",
                        timezone_id="Europe/Istanbul",
                        reduced_motion="reduce",
                    )
                    ctx.add_init_script(
                        f"try{{localStorage.setItem('pocketbase_auth', {json.dumps(depo)});}}catch(e){{}}")
                    sayfa = ctx.new_page()
                    for rota in ROLLER[rol]["rotalar"]:
                        hatalar: list[str] = []
                        sayfa.on("console", lambda m, h=hatalar:
                                 h.append(m.text[:300]) if m.type == "error" else None)
                        sayfa.on("pageerror", lambda e, h=hatalar: h.append("PAGEERROR " + str(e)[:300]))
                        url = f"{a.taban}{rota}/"
                        try:
                            sayfa.goto(url, wait_until="networkidle", timeout=30000)
                        except Exception as e:
                            rapor.append({"rol": rol, "rota": rota, "gorunum": gad,
                                          "tema": tema, "hata": str(e)[:200]})
                            continue
                        sayfa.wait_for_timeout(1400)
                        etiket = f"{rol}-{guvenli(rota)}-{gad}" + ("" if tema == "acik" else f"-{tema}")
                        try:
                            sayfa.screenshot(path=str(kok / "ss" / f"{etiket}.png"))
                            sayfa.screenshot(path=str(kok / "ss" / f"{etiket}-tam.png"), full_page=True)
                        except Exception:
                            pass
                        try:
                            olcum = sayfa.evaluate(OLC)
                        except Exception as e:
                            olcum = {"olcumHatasi": str(e)[:200]}
                        sekmeler = []
                        try:
                            sekmeler = sayfa.evaluate(SEKME_AC)
                        except Exception:
                            pass
                        rapor.append({
                            "rol": rol, "rota": rota, "gorunum": gad, "tema": tema,
                            "ss": f"ss/{etiket}.png", "ssTam": f"ss/{etiket}-tam.png",
                            "sekmeler": sekmeler, "konsol": hatalar[:10], **olcum,
                        })
                        print(f"  ✓ {etiket}  tasma={olcum.get('yatayTasma','?')} "
                              f"kucukHedef={len(olcum.get('kucukHedef',[]))} "
                              f"kontrast={olcum.get('kontrastToplam','?')} "
                              f"konsol={len(hatalar)}", flush=True)
                    ctx.close()
        tarayici.close()

    (kok / "olcum.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=2))
    print(f"\n{len(rapor)} ekran · {kok}/olcum.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
