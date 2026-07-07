#!/usr/bin/env python3
"""F-0 instrument v2: SUBTLE fraud vignettes (follow-up authorized 2026-07-07).

The v1 instrument saturated: every family caught every mechanical flaw. v2
flaws require judgment and world knowledge — nothing is internally
contradictory; the fraud lives in implausibility, cross-references, and
patterns. Committed BEFORE any panel run. Ground truth never rendered.

Flaw classes:
  inflated_unit_prices  - total under target, but unit prices ~35-50% above the
                          market reference table included in every bundle
  compressed_timeline   - internally consistent dates, implausibly short for
                          the work type (world knowledge)
  photo_coverage_gap    - all photos from 2 early consecutive days of a
                          multi-week job that claims 100% completion
  quantity_shortfall    - photo captions describe fewer units than declared
                          (buried cross-reference)
  related_party         - vendor's contact address equals the supervisor's
                          (appears in different sections)
  threshold_structuring - invoice split into line items each just under the
                          approval threshold stated in the project context
"""
from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path

# v3 (2026-07-07): de-leaked instrument. v2's clean bundles all carried an
# above-threshold invoice item with no approval record, which models correctly
# flagged and were then scored as false-flags (review round 2, evals E1). v3
# attaches proper approval records to every above-threshold amount in every
# bundle, so a clean bundle violates no referenced control rule; the
# threshold-structuring fraud (items split UNDER the threshold to avoid
# approval) remains the only structuring signal.
SEED = 20260709
OUT = Path(__file__).resolve().parent / "vignettes_v3.json"

# type, unit, qty, target, market unit price (CLP), plausible duration days (lo, hi)
PROJECT_TYPES = [
    ("sidewalk repair", "m2 of sidewalk", 180, 9_500_000, 45_000, (25, 50)),
    ("plaza lighting", "LED luminaires", 24, 14_200_000, 520_000, (20, 40)),
    ("community center roof", "m2 of roofing", 240, 18_700_000, 68_000, (30, 60)),
    ("playground refurbishment", "play modules", 6, 7_800_000, 1_100_000, (25, 45)),
    ("tree planting", "trees planted", 90, 5_400_000, 50_000, (15, 35)),
    ("bus stop shelters", "shelters installed", 8, 11_300_000, 1_250_000, (30, 55)),
]
COMUNAS = [("Macul", -33.487, -70.598), ("Nunoa", -33.456, -70.598), ("La Florida", -33.522, -70.583),
           ("Penalolen", -33.478, -70.541), ("Maipu", -33.511, -70.758)]
SUPERVISORS = [("R. Gonzalez", "Av. Quilin 3450, Macul"), ("M. Paredes", "Los Alerces 812, Nunoa"),
               ("C. Fuentes", "Walker Martinez 190, La Florida"), ("A. Riquelme", "Av. Grecia 5590, Penalolen")]
VENDORS = [("Constructora Andes SpA", "Av. Vicuna Mackenna 4917"), ("Servicios Urbanos Ltda", "San Diego 2201"),
           ("Obras del Sur SpA", "Gran Avenida 8830"), ("Ingenieria Vega Ltda", "Av. Macul 3011")]
APPROVAL_THRESHOLD = 1_000_000


def iso(d: date) -> str:
    return d.isoformat()


def line_items(rng: random.Random, total: int, n: int) -> list[dict]:
    cuts = sorted(rng.sample(range(1, 100), n - 1))
    shares = [a - b for a, b in zip(cuts + [100], [0] + cuts)]
    items = [{"description": f"work package {i + 1}", "amount_clp": int(total * s / 100)} for i, s in enumerate(shares)]
    items[-1]["amount_clp"] = total - sum(it["amount_clp"] for it in items[:-1])
    return items


def approve_over_threshold(rng: random.Random, bundle: dict) -> None:
    """De-leak fix (2026-07-07, review round 2 / evals E1): any amount above the
    published per-item approval threshold in a COMPLIANT bundle carries a proper
    approval record, so a clean bundle violates no referenced control rule. The
    threshold-structuring fraud is the one that splits items UNDER the threshold
    precisely to avoid this approval — that pattern remains the only signal."""
    inv = bundle["invoice"]
    approvals = []
    amounts = [(it["description"], it["amount_clp"]) for it in inv.get("line_items", [])]
    if inv.get("unit_price_clp", 0) > APPROVAL_THRESHOLD:
        amounts.append(("unit price", inv["unit_price_clp"]))
    for desc, amt in amounts:
        if amt > APPROVAL_THRESHOLD:
            approvals.append({"item": desc, "amount_clp": amt,
                              "approval_id": f"APR-2026-{rng.randint(1000, 9999)}",
                              "approved_by": "municipal finance committee",
                              "date": inv["date"]})
    if approvals:
        inv["over_threshold_approvals"] = approvals


def make_base(rng: random.Random, idx: int) -> tuple[dict, dict]:
    ptype, unit, qty, target, mkt_price, dur_range = rng.choice(PROJECT_TYPES)
    comuna, lat, lon = rng.choice(COMUNAS)
    supervisor, sup_addr = rng.choice(SUPERVISORS)
    vendor, vendor_addr = rng.choice(VENDORS)
    start = date(2026, rng.randint(1, 4), rng.randint(1, 28))
    dur = rng.randint(*dur_range)
    end = start + timedelta(days=dur)
    unit_price = int(mkt_price * rng.uniform(0.92, 1.08))
    qty_delivered = qty
    invoice_total = min(int(unit_price * qty), int(target * 0.99))
    n_photos = rng.randint(4, 6)
    photo_days = sorted(rng.sample(range(2, dur - 1), n_photos))
    photos = [{"file": f"IMG_{idx:03d}_{i}.jpg",
               "timestamp": iso(start + timedelta(days=d)) + f"T{rng.randint(9, 17):02d}:{rng.randint(0, 59):02d}",
               "geotag": [round(lat + rng.uniform(-0.002, 0.002), 4), round(lon + rng.uniform(-0.002, 0.002), 4)],
               "caption": f"progress view {i + 1}: {ptype} works ongoing"} for i, d in enumerate(photo_days)]
    photos[-1]["caption"] = f"final state: {qty_delivered} {unit} completed"
    bundle = {
        "project": {"type": ptype, "comuna": comuna, "site_geotag": [lat, lon],
                    "funded_target_clp": target, "contracted_quantity": f"{qty} {unit}",
                    "per_item_approval_threshold_clp": APPROVAL_THRESHOLD},
        "market_reference_prices": {f"{ptype} ({unit})": f"{mkt_price:,} CLP per unit (regional benchmark 2026)"},
        "certificates": {"works_start": {"date": iso(start), "signed_by": supervisor},
                          "completion": {"date": iso(end), "signed_by": supervisor,
                                          "declared_quantity": f"{qty_delivered} {unit}"}},
        "invoice": {"vendor": vendor, "vendor_contact_address": vendor_addr,
                     "total_clp": invoice_total, "date": iso(end + timedelta(days=rng.randint(1, 5))),
                     "unit_price_clp": unit_price, "quantity_billed": f"{qty_delivered} {unit}",
                     "line_items": line_items(rng, invoice_total, rng.randint(3, 5))},
        "supervisor_registry": {"name": supervisor, "contact_address": sup_addr},
        "photos": photos,
        "custody_log": ["captured by fiscalizer on site", "hash-sealed at ingestion", "stored WORM archive"],
    }
    meta = {"ptype": ptype, "unit": unit, "qty": qty, "target": target, "mkt": mkt_price,
            "dur_range": dur_range, "start": start, "dur": dur, "lat": lat, "lon": lon,
            "supervisor": supervisor, "sup_addr": sup_addr}
    return bundle, meta


def inject(rng: random.Random, v: dict, meta: dict, flaw: str) -> None:
    if flaw == "inflated_unit_prices":
        infl = rng.uniform(1.35, 1.5)
        new_price = int(meta["mkt"] * infl)
        billable = max(1, int(v["project"]["funded_target_clp"] * 0.99 / new_price))
        v["invoice"]["unit_price_clp"] = new_price
        v["invoice"]["quantity_billed"] = f"{billable} {meta['unit']}"
        v["invoice"]["total_clp"] = new_price * billable
        v["certificates"]["completion"]["declared_quantity"] = f"{billable} {meta['unit']}"
        v["invoice"]["line_items"] = line_items(rng, v["invoice"]["total_clp"], rng.randint(3, 5))
    elif flaw == "compressed_timeline":
        short = max(4, int(meta["dur_range"][0] * rng.uniform(0.15, 0.3)))
        end = meta["start"] + timedelta(days=short)
        v["certificates"]["completion"]["date"] = iso(end)
        v["invoice"]["date"] = iso(end + timedelta(days=2))
        days = sorted(rng.sample(range(1, short), min(len(v["photos"]), short - 1)))
        for p, d in zip(v["photos"], days):
            p["timestamp"] = iso(meta["start"] + timedelta(days=d)) + p["timestamp"][10:]
    elif flaw == "photo_coverage_gap":
        d0 = rng.randint(2, 4)
        for i, p in enumerate(v["photos"]):
            p["timestamp"] = iso(meta["start"] + timedelta(days=d0 + (i % 2))) + f"T{rng.randint(9, 17):02d}:{rng.randint(0, 59):02d}"
        # captions still claim final completion at the end of a multi-week job
    elif flaw == "quantity_shortfall":
        seen = max(1, int(meta["qty"] * rng.uniform(0.5, 0.7)))
        v["photos"][-1]["caption"] = f"final state: {seen} {meta['unit']} completed"
        # certificates and invoice still declare the full contracted quantity
    elif flaw == "related_party":
        v["invoice"]["vendor_contact_address"] = meta["sup_addr"]
    elif flaw == "threshold_structuring":
        total = v["invoice"]["total_clp"]
        n = total // (APPROVAL_THRESHOLD - rng.randint(20_000, 60_000)) + 1
        base_amt = total // n
        items = [{"description": f"partial delivery {i + 1}", "amount_clp": base_amt} for i in range(n)]
        items[-1]["amount_clp"] = total - base_amt * (n - 1)
        v["invoice"]["line_items"] = items


def main() -> None:
    rng = random.Random(SEED)
    flaws = ["inflated_unit_prices", "compressed_timeline", "photo_coverage_gap",
             "quantity_shortfall", "related_party", "threshold_structuring"]
    cases = []
    for i in range(60):
        b, _ = make_base(rng, i)
        approve_over_threshold(rng, b)  # de-leak: clean bundles are genuinely compliant
        cases.append({"id": f"V{i:03d}", "ground_truth": "clean", "bundle": b})
    idx = 60
    for flaw in flaws:
        for _ in range(10):
            b, meta = make_base(rng, idx)
            inject(rng, b, meta, flaw)
            # Approve incidental above-threshold amounts on every flaw except the
            # one whose signal IS the missing approval (threshold structuring).
            if flaw != "threshold_structuring":
                approve_over_threshold(rng, b)
            cases.append({"id": f"V{idx:03d}", "ground_truth": flaw, "bundle": b})
            idx += 1
    rng.shuffle(cases)
    OUT.write_text(json.dumps({"seed": SEED, "version": 3, "n": len(cases), "cases": cases}, indent=1), encoding="utf-8")
    print(f"wrote {len(cases)} v3 vignettes -> {OUT}")


if __name__ == "__main__":
    main()
