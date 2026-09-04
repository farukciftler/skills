#!/usr/bin/env python3
"""
pt.py - Portfoy Tahmin Gunlugu defteri.

Deterministik kayit katmani. Internete CIKMAZ, fiyat CEKMEZ, tahmin URETMEZ.
Fiyatlari ve tahminleri Claude web search ile toplayip buraya besler;
bu script sadece saklar, eslestirir ve olcer.

Alt komutlar:
  init         Veri kokunu olustur
  add-asset    Portfoye varlik ekle / guncelle
  list-assets  Portfoyu goster
  snapshot     Gunun fiyatlarini ve portfoy degerini kaydet
  forecast     Tahmin kaydi ekle
  resolve      Vadesi gelen tahminleri gerceklesenle eslestir
  report       Sabah raporu icin baglam paketi (JSON)
  calibrate    Kalibrasyon metrikleri
  note         Gunun gundem notunu evidence/ altina yaz
"""

import argparse
import json
import os
import signal
import statistics
import sys

try:  # `| head` gibi kullanimlarda BrokenPipeError gurultusu olmasin
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass
from datetime import date, datetime, timedelta
from pathlib import Path

ASSET_CLASSES = ("spot", "fund_tefas", "accrual", "equity", "crypto")
FORECASTABLE = ("spot", "fund_tefas", "equity", "crypto")
BUSINESS_DAY_CLASSES = ("fund_tefas", "equity")
HORIZON_DAYS = {"1d": 1, "1w": 7, "1m": 30}
RESOLVE_GRACE_DAYS = 6  # bu kadar gun sonra hala snapshot yoksa veri_yok


# ---------------------------------------------------------------- yardimcilar

def parse_date(s):
    if s is None:
        return date.today()
    return datetime.strptime(s, "%Y-%m-%d").date()


def next_business_day(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(p)


def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def die(msg):
    print(f"HATA: {msg}", file=sys.stderr)
    sys.exit(1)


class Store:
    def __init__(self, root):
        self.root = Path(os.path.expanduser(root))
        self.portfolio_path = self.root / "portfolio.json"
        self.snapshots = self.root / "snapshots"
        self.forecasts = self.root / "forecasts"
        self.evidence = self.root / "evidence"
        self.reviews = self.root / "reviews"
        self.resolutions = self.root / "resolutions.jsonl"

    def ensure(self):
        for d in (self.snapshots, self.forecasts, self.evidence, self.reviews):
            d.mkdir(parents=True, exist_ok=True)

    def portfolio(self):
        p = read_json(self.portfolio_path)
        if p is None:
            die(f"portfolio.json yok. Once: pt.py init --root {self.root}")
        return p

    def save_portfolio(self, p):
        write_json(self.portfolio_path, p)

    def snapshot_path(self, d):
        return self.snapshots / f"{d.isoformat()}.json"

    def snapshot(self, d):
        return read_json(self.snapshot_path(d))

    def latest_snapshot(self, on_or_before=None):
        files = sorted(self.snapshots.glob("*.json"))
        for f in reversed(files):
            d = date.fromisoformat(f.stem)
            if on_or_before is None or d <= on_or_before:
                return d, read_json(f)
        return None, None

    def all_forecast_files(self):
        return sorted(self.forecasts.glob("*.json"))

    def all_resolutions(self):
        if not self.resolutions.exists():
            return []
        rows = []
        with self.resolutions.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def append_resolutions(self, rows):
        self.resolutions.parent.mkdir(parents=True, exist_ok=True)
        with self.resolutions.open("a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- komutlar

def cmd_init(args):
    st = Store(args.root)
    st.ensure()
    if st.portfolio_path.exists():
        out({"ok": True, "mesaj": "zaten var", "root": str(st.root)})
        return
    st.save_portfolio({
        "base_currency": args.currency,
        "created_at": now_iso(),
        "assets": {},
    })
    out({"ok": True, "root": str(st.root), "olusturuldu": True})


def cmd_add_asset(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    if args.asset_class not in ASSET_CLASSES:
        die(f"gecersiz class. Secenekler: {', '.join(ASSET_CLASSES)}")
    if args.quantity is None and args.value is None:
        die("--quantity veya --value verilmeli")

    existing = p["assets"].get(args.id, {})
    asset = {
        "label": args.label or existing.get("label") or args.id,
        "class": args.asset_class,
        "unit": args.unit or existing.get("unit"),
        "quantity": args.quantity if args.quantity is not None else existing.get("quantity"),
        "value_try": args.value if args.value is not None else existing.get("value_try"),
        "price_source": args.price_source or existing.get("price_source"),
        "accrual_apr": args.accrual_apr if args.accrual_apr is not None else existing.get("accrual_apr"),
        "notes": args.notes or existing.get("notes", ""),
        "updated_at": now_iso(),
    }
    if args.quantity is not None:
        asset["value_try"] = None  # miktar otoriter
    p["assets"][args.id] = asset
    st.save_portfolio(p)
    out({"ok": True, "asset": args.id, "kayit": asset})


def cmd_remove_asset(args):
    st = Store(args.root)
    p = st.portfolio()
    if args.id not in p["assets"]:
        die(f"{args.id} portfoyde yok")
    removed = p["assets"].pop(args.id)
    st.save_portfolio(p)
    out({"ok": True, "silindi": args.id, "kayit": removed})


def cmd_list_assets(args):
    st = Store(args.root)
    p = st.portfolio()
    d, snap = st.latest_snapshot()
    rows = []
    total = 0.0
    for aid, a in p["assets"].items():
        val = (snap or {}).get("values", {}).get(aid)
        if val is None:
            val = a.get("value_try")
        if val:
            total += val
        rows.append({
            "id": aid, "label": a["label"], "class": a["class"],
            "quantity": a.get("quantity"), "deger_try": val,
            "tahmin_edilebilir": a["class"] in FORECASTABLE,
        })
    for r in rows:
        r["agirlik_pct"] = round(100 * r["deger_try"] / total, 1) if (total and r["deger_try"]) else None
    rows.sort(key=lambda r: r["deger_try"] or 0, reverse=True)
    out({"toplam_try": round(total, 2), "son_snapshot": d.isoformat() if d else None, "varliklar": rows})


def cmd_snapshot(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    d = parse_date(args.date)

    prices = json.loads(args.prices) if args.prices else {}
    if args.prices_file:
        prices.update(read_json(args.prices_file, {}))

    prev_date, prev = st.latest_snapshot(on_or_before=d - timedelta(days=1))
    prev_values = (prev or {}).get("values", {})
    prev_prices = (prev or {}).get("prices", {})

    values, used_prices, warnings = {}, {}, []
    dirty_portfolio = False

    for aid, a in p["assets"].items():
        price = prices.get(aid)
        if price is not None and not isinstance(price, (int, float)):
            die(f"{aid} icin fiyat sayi olmali, gelen: {price!r}")
        used_prices[aid] = price
        cls = a["class"]

        if cls == "accrual":
            base = prev_values.get(aid, a.get("value_try") or 0.0)
            apr = a.get("accrual_apr")
            if apr and prev_date:
                days = (d - prev_date).days
                base = base * (1 + (apr / 100.0) * days / 365.0)
                warnings.append(f"{aid}: birikim projeksiyonu ({days} gun, %{apr} yillik) - gercek bakiye degil")
            elif prices.get(aid) is not None:
                base = prices[aid]  # kullanici gercek bakiyeyi fiyat alaninda verdi
            values[aid] = round(base, 2)
            continue

        qty = a.get("quantity")
        if qty is None and a.get("value_try") is not None and price:
            qty = a["value_try"] / price
            p["assets"][aid]["quantity"] = round(qty, 6)
            p["assets"][aid]["implied_from"] = {"value_try": a["value_try"], "price": price, "date": d.isoformat()}
            p["assets"][aid]["value_try"] = None
            dirty_portfolio = True
            warnings.append(f"{aid}: {round(qty, 4)} birim olarak turetildi (fiyat {price})")

        if qty is not None and price:
            values[aid] = round(qty * price, 2)
        elif aid in prev_values:
            values[aid] = prev_values[aid]
            warnings.append(f"{aid}: fiyat yok, onceki deger tasindi ({prev_date})")
        elif a.get("value_try"):
            values[aid] = a["value_try"]
            warnings.append(f"{aid}: fiyat yok, tanimdaki deger kullanildi")
        else:
            values[aid] = None
            warnings.append(f"{aid}: deger hesaplanamadi")

    if dirty_portfolio:
        st.save_portfolio(p)

    total = round(sum(v for v in values.values() if v), 2)
    prev_total = (prev or {}).get("total")
    snap = {
        "date": d.isoformat(),
        "created_at": now_iso(),
        "prices": used_prices,
        "values": values,
        "total": total,
        "prev_date": prev_date.isoformat() if prev_date else None,
        "prev_total": prev_total,
        "delta_pct": round(100 * (total - prev_total) / prev_total, 2) if prev_total else None,
        "notes": args.notes or "",
    }
    write_json(st.snapshot_path(d), snap)
    eksik = [k for k, v in used_prices.items() if v is None and p["assets"][k]["class"] != "accrual"]
    out({"ok": True, "snapshot": snap, "fiyati_eksik": eksik, "uyarilar": warnings,
         "onceki_fiyatlar": prev_prices if eksik else {}})


def cmd_forecast(args):
    st = Store(args.root)
    st.ensure()
    p = st.portfolio()
    payload = read_json(args.file) if args.file else json.loads(sys.stdin.read())

    as_of = parse_date(payload.get("as_of") or args.date)
    snap = st.snapshot(as_of)
    if snap is None:
        _, snap = st.latest_snapshot(on_or_before=as_of)
    base_prices = (snap or {}).get("prices", {})

    items, problems, skipped = [], [], []
    for fc in payload.get("forecasts", []):
        aid = fc.get("asset")
        if aid not in p["assets"]:
            problems.append(f"bilinmeyen varlik: {aid}")
            continue
        cls = p["assets"][aid]["class"]
        if cls not in FORECASTABLE:
            skipped.append(f"{aid} ({cls}) tahmin edilmeyen sinifta, atlandi")
            continue
        h = fc.get("horizon")
        if h not in HORIZON_DAYS:
            problems.append(f"{aid}: gecersiz horizon {h}")
            continue
        for k in ("point_pct", "low_pct", "high_pct", "p_up"):
            if fc.get(k) is None:
                problems.append(f"{aid}/{h}: {k} eksik")
        if fc.get("low_pct") is not None and fc.get("high_pct") is not None:
            if not (fc["low_pct"] <= fc.get("point_pct", 0) <= fc["high_pct"]):
                problems.append(f"{aid}/{h}: nokta tahmin bandin disinda")
        if fc.get("p_up") is not None and not (0 <= fc["p_up"] <= 1):
            problems.append(f"{aid}/{h}: p_up 0-1 arasinda olmali")

        tgt = fc.get("target_date")
        tgt = parse_date(tgt) if tgt else as_of + timedelta(days=HORIZON_DAYS[h])
        if cls in BUSINESS_DAY_CLASSES:
            tgt = next_business_day(tgt)

        items.append({
            "asset": aid, "class": cls, "horizon": h,
            "target_date": tgt.isoformat(),
            "base_price": base_prices.get(aid),
            "point_pct": fc.get("point_pct"),
            "low_pct": fc.get("low_pct"),
            "high_pct": fc.get("high_pct"),
            "interval": fc.get("interval", 80),
            "p_up": fc.get("p_up"),
            "confidence": fc.get("confidence", "low"),
            "drivers": fc.get("drivers", []),
            "rationale": fc.get("rationale", ""),
            "invalidator": fc.get("invalidator", ""),
        })

    if problems and not args.force:
        die("tahmin dosyasi gecersiz:\n  - " + "\n  - ".join(problems))

    path = st.forecasts / f"{as_of.isoformat()}.json"
    existing = read_json(path, {"as_of": as_of.isoformat(), "forecasts": [], "evidence": []})
    keys = {(i["asset"], i["horizon"]) for i in items}
    existing["forecasts"] = [f for f in existing.get("forecasts", [])
                             if (f["asset"], f["horizon"]) not in keys] + items
    ev = payload.get("evidence", [])
    if ev:
        existing["evidence"] = existing.get("evidence", []) + ev
    existing["market_state"] = payload.get("market_state", existing.get("market_state", {}))
    existing["created_at"] = existing.get("created_at") or now_iso()
    existing["updated_at"] = now_iso()
    write_json(path, existing)
    out({"ok": True, "as_of": as_of.isoformat(), "kaydedilen": len(items),
         "toplam": len(existing["forecasts"]), "atlanan": skipped,
         "uyarilar": problems, "dosya": str(path)})


def cmd_resolve(args):
    st = Store(args.root)
    st.ensure()
    today = parse_date(args.date)
    done = {(r["as_of"], r["asset"], r["horizon"]) for r in st.all_resolutions()}

    new_rows, pending = [], []
    for f in st.all_forecast_files():
        rec = read_json(f)
        as_of = rec["as_of"]
        for fc in rec.get("forecasts", []):
            key = (as_of, fc["asset"], fc["horizon"])
            if key in done:
                continue
            tgt = date.fromisoformat(fc["target_date"])
            if tgt > today:
                pending.append({"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
                                "target_date": fc["target_date"]})
                continue

            snap = st.snapshot(tgt)
            actual = (snap or {}).get("prices", {}).get(fc["asset"]) if snap else None
            if actual is None:
                # hedef gunde veri yoksa sonraki gunlere bak (tatil / TEFAS gecikmesi)
                for k in range(1, RESOLVE_GRACE_DAYS + 1):
                    s2 = st.snapshot(tgt + timedelta(days=k))
                    if s2 and s2.get("prices", {}).get(fc["asset"]) is not None:
                        actual = s2["prices"][fc["asset"]]
                        break
            if actual is None:
                if (today - tgt).days >= RESOLVE_GRACE_DAYS:
                    new_rows.append({**_res_stub(as_of, fc), "durum": "veri_yok"})
                else:
                    pending.append({"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
                                    "target_date": fc["target_date"], "not": "snapshot bekleniyor"})
                continue

            base = fc.get("base_price")
            if not base:
                new_rows.append({**_res_stub(as_of, fc), "durum": "baz_fiyat_yok"})
                continue

            actual_pct = 100.0 * (actual - base) / base
            err = abs(fc["point_pct"] - actual_pct)
            baseline_err = abs(actual_pct)  # naif: "degismez"
            row = {
                **_res_stub(as_of, fc),
                "durum": "cozuldu",
                "base_price": base,
                "actual_price": actual,
                "actual_pct": round(actual_pct, 3),
                "point_pct": fc["point_pct"],
                "abs_err": round(err, 3),
                "signed_err": round(fc["point_pct"] - actual_pct, 3),
                "baseline_abs_err": round(baseline_err, 3),
                "baseline_yenildi": bool(err < baseline_err),
                "bantta": bool(fc["low_pct"] <= actual_pct <= fc["high_pct"]),
                "band": [fc["low_pct"], fc["high_pct"]],
                "p_up": fc.get("p_up"),
                "yon_dogru": None if actual_pct == 0 or fc.get("p_up") is None
                             else bool((fc["p_up"] > 0.5) == (actual_pct > 0)),
                "brier": None if fc.get("p_up") is None
                         else round((fc["p_up"] - (1.0 if actual_pct > 0 else 0.0)) ** 2, 4),
                "resolved_at": now_iso(),
            }
            new_rows.append(row)

    if new_rows:
        st.append_resolutions(new_rows)
    out({"ok": True, "cozulen": len([r for r in new_rows if r["durum"] == "cozuldu"]),
         "veri_yok": len([r for r in new_rows if r["durum"] != "cozuldu"]),
         "bekleyen": len(pending), "yeni": new_rows, "bekleyenler": pending[:20]})


def _res_stub(as_of, fc):
    return {"as_of": as_of, "asset": fc["asset"], "horizon": fc["horizon"],
            "target_date": fc["target_date"]}


def _calib(rows):
    solved = [r for r in rows if r.get("durum") == "cozuldu"]
    if not solved:
        return {"n": 0}
    errs = [r["abs_err"] for r in solved]
    base = [r["baseline_abs_err"] for r in solved]
    dirs = [r["yon_dogru"] for r in solved if r.get("yon_dogru") is not None]
    briers = [r["brier"] for r in solved if r.get("brier") is not None]
    mae, bmae = statistics.fmean(errs), statistics.fmean(base)
    return {
        "n": len(solved),
        "yon_isabeti": round(sum(dirs) / len(dirs), 3) if dirs else None,
        "yon_n": len(dirs),
        "mae_pct": round(mae, 3),
        "baseline_mae_pct": round(bmae, 3),
        "skill_score": round(1 - mae / bmae, 3) if bmae else None,
        "baseline_yenme_orani": round(sum(r["baseline_yenildi"] for r in solved) / len(solved), 3),
        "bant_kapsama": round(sum(r["bantta"] for r in solved) / len(solved), 3),
        "bant_hedefi": 0.80,
        "bias_pct": round(statistics.fmean(r["signed_err"] for r in solved), 3),
        "brier": round(statistics.fmean(briers), 4) if briers else None,
    }


def cmd_calibrate(args):
    st = Store(args.root)
    today = parse_date(args.date)
    cutoff = today - timedelta(days=args.window)
    rows = [r for r in st.all_resolutions()
            if date.fromisoformat(r["target_date"]) >= cutoff]
    if args.asset:
        rows = [r for r in rows if r["asset"] == args.asset]

    by_horizon, by_asset = {}, {}
    for r in rows:
        by_horizon.setdefault(r["horizon"], []).append(r)
        by_asset.setdefault(r["asset"], []).append(r)

    res = {
        "pencere_gun": args.window,
        "tarih": today.isoformat(),
        "genel": _calib(rows),
        "horizon_bazli": {k: _calib(v) for k, v in sorted(by_horizon.items())},
        "varlik_bazli": {k: _calib(v) for k, v in sorted(by_asset.items())},
        "yorum_kilavuzu": {
            "skill_score": ">0 baseline'dan iyi, <=0 tahminlerin degeri yok",
            "bant_kapsama": "0.80 civari ideal; >0.9 bantlar cok genis, <0.7 cok dar",
            "yon_isabeti": "0.50 sans seviyesi; n<30 iken anlamli degil",
            "brier": "0.25 sans seviyesi; dusuk daha iyi",
            "bias_pct": "pozitif = sistematik olarak fazla iyimser",
        },
    }
    out(res)


def cmd_report(args):
    st = Store(args.root)
    st.ensure()
    today = parse_date(args.date)
    p = st.portfolio()

    snap_date, snap = st.latest_snapshot(on_or_before=today)
    prev_date, prev = (None, None)
    if snap_date:
        prev_date, prev = st.latest_snapshot(on_or_before=snap_date - timedelta(days=1))

    # bugunu hedefleyen tum tahminler (horizon'a gore gruplanir)
    targeting_today = {"1d": [], "1w": [], "1m": []}
    for f in st.all_forecast_files():
        rec = read_json(f)
        for fc in rec.get("forecasts", []):
            if fc["target_date"] == today.isoformat():
                targeting_today.setdefault(fc["horizon"], []).append({**fc, "as_of": rec["as_of"]})

    res_index = {(r["as_of"], r["asset"], r["horizon"]): r for r in st.all_resolutions()}
    for h, lst in targeting_today.items():
        for fc in lst:
            fc["sonuc"] = res_index.get((fc["as_of"], fc["asset"], fc["horizon"]))

    # bugun uretilmis, hala acik tahminler
    acik = []
    for f in st.all_forecast_files():
        rec = read_json(f)
        for fc in rec.get("forecasts", []):
            if date.fromisoformat(fc["target_date"]) > today:
                acik.append({"as_of": rec["as_of"], "asset": fc["asset"],
                             "horizon": fc["horizon"], "target_date": fc["target_date"]})

    all_res = st.all_resolutions()
    c30 = [r for r in all_res if date.fromisoformat(r["target_date"]) >= today - timedelta(days=30)]

    varliklar = []
    for aid, a in p["assets"].items():
        v = (snap or {}).get("values", {}).get(aid)
        pv = (prev or {}).get("values", {}).get(aid)
        varliklar.append({
            "id": aid, "label": a["label"], "class": a["class"],
            "tahmin_edilebilir": a["class"] in FORECASTABLE,
            "quantity": a.get("quantity"),
            "deger_try": v,
            "onceki_deger_try": pv,
            "gunluk_pct": round(100 * (v - pv) / pv, 2) if (v and pv) else None,
            "son_fiyat": (snap or {}).get("prices", {}).get(aid),
            "price_source": a.get("price_source"),
        })
    total = (snap or {}).get("total")
    for v in varliklar:
        v["agirlik_pct"] = round(100 * v["deger_try"] / total, 1) if (total and v["deger_try"]) else None
    varliklar.sort(key=lambda r: r["deger_try"] or 0, reverse=True)

    ev_path = st.evidence / f"{today.isoformat()}.md"
    out({
        "tarih": today.isoformat(),
        "sistem_yasi_gun": _system_age(st),
        "portfoy": {
            "toplam_try": total,
            "onceki_toplam_try": (prev or {}).get("total"),
            "delta_pct": (snap or {}).get("delta_pct"),
            "snapshot_tarihi": snap_date.isoformat() if snap_date else None,
            "bugun_snapshot_var_mi": st.snapshot(today) is not None,
            "varliklar": varliklar,
        },
        "bugunu_hedefleyen_tahminler": targeting_today,
        "acik_tahminler": sorted(acik, key=lambda r: r["target_date"])[:40],
        "kalibrasyon_30g": _calib(c30),
        "bugun_gundem_notu_var_mi": ev_path.exists(),
        "sonraki_adim": _next_step(st, today),
    })


def _system_age(st):
    files = sorted(st.snapshots.glob("*.json")) + sorted(st.forecasts.glob("*.json"))
    if not files:
        return 0
    first = min(date.fromisoformat(f.stem) for f in files)
    return (date.today() - first).days


def _next_step(st, today):
    if not st.portfolio_path.exists():
        return "init + add-asset"
    if st.snapshot(today) is None:
        return "fiyatlari topla ve snapshot al"
    if not (st.forecasts / f"{today.isoformat()}.json").exists():
        return "gundemi tara ve forecast kaydet"
    return "rapor yazilabilir"


def cmd_note(args):
    st = Store(args.root)
    st.ensure()
    d = parse_date(args.date)
    path = st.evidence / f"{d.isoformat()}.md"
    text = args.text if args.text else sys.stdin.read()
    mode = "a" if path.exists() else "w"
    with path.open(mode, encoding="utf-8") as f:
        if mode == "w":
            f.write(f"# Gundem · {d.isoformat()}\n\n")
        f.write(text.rstrip() + "\n")
    out({"ok": True, "dosya": str(path)})


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default="~/portfoy-takip", help="veri kokü (varsayilan ~/portfoy-takip)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="veri kokunu olustur")
    s.add_argument("--currency", default="TRY")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("add-asset", help="varlik ekle/guncelle")
    s.add_argument("--id", required=True)
    s.add_argument("--label")
    s.add_argument("--class", dest="asset_class", required=True,
                   help=f"{'|'.join(ASSET_CLASSES)}")
    s.add_argument("--unit")
    s.add_argument("--quantity", type=float, help="birim adedi (biliniyorsa tercih edilir)")
    s.add_argument("--value", type=float, help="TL degeri (miktar bilinmiyorsa)")
    s.add_argument("--price-source")
    s.add_argument("--accrual-apr", type=float, help="sadece accrual: yillik %% getiri projeksiyonu")
    s.add_argument("--notes")
    s.set_defaults(func=cmd_add_asset)

    s = sub.add_parser("remove-asset")
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_remove_asset)

    s = sub.add_parser("list-assets", help="portfoyu goster")
    s.set_defaults(func=cmd_list_assets)

    s = sub.add_parser("snapshot", help="gunun fiyatlarini kaydet")
    s.add_argument("--date")
    s.add_argument("--prices", help='JSON: {"gram_altin": 6187.5, "KTJ": 12.34}')
    s.add_argument("--prices-file")
    s.add_argument("--notes")
    s.set_defaults(func=cmd_snapshot)

    s = sub.add_parser("forecast", help="tahmin kaydet (JSON dosya veya stdin)")
    s.add_argument("--file")
    s.add_argument("--date")
    s.add_argument("--force", action="store_true", help="dogrulama uyarilarina ragmen kaydet")
    s.set_defaults(func=cmd_forecast)

    s = sub.add_parser("resolve", help="vadesi gelen tahminleri eslestir")
    s.add_argument("--date")
    s.set_defaults(func=cmd_resolve)

    s = sub.add_parser("report", help="sabah raporu baglam paketi")
    s.add_argument("--date")
    s.set_defaults(func=cmd_report)

    s = sub.add_parser("calibrate", help="kalibrasyon metrikleri")
    s.add_argument("--date")
    s.add_argument("--window", type=int, default=30)
    s.add_argument("--asset")
    s.set_defaults(func=cmd_calibrate)

    s = sub.add_parser("note", help="gundem notu yaz")
    s.add_argument("--date")
    s.add_argument("--text")
    s.set_defaults(func=cmd_note)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
