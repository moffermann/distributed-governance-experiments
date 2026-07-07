#!/usr/bin/env python3
"""F-0 instrument generator: evidence-case vignettes with known ground truth.

Deterministic (seeded); produces vignettes.json with 120 structured evidence
bundles: 60 clean, 60 flawed (10 per flaw class, 6 classes). Committed BEFORE
any panel run, per the pre-registration. The ground truth never appears in the
rendered prompt text.

Flaw classes (from EXPERIMENT_F_LAYERED_VERIFICATION_DESIGN.md):
  fabricated_progress    - evidence timestamps precede the works themselves
  metadata_inconsistency - dates/signers internally contradictory
  wrong_location         - geotags far from the project site
  recycled_evidence      - photo hashes duplicate a prior project's registry
  quantity_mismatch      - invoiced amounts/quantities exceed the funded scope
  plausible_staging      - internally consistent but circumstantially staged
                           (the predicted shared blind spot, PF0-3)
"""
from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20260707
OUT = Path(__file__).resolve().parent / "vignettes.json"

PROJECT_TYPES = [
    ("sidewalk repair", "m2 of sidewalk", 180, 9_500_000),
    ("plaza lighting", "LED luminaires", 24, 14_200_000),
    ("community center roof", "m2 of roofing", 240, 18_700_000),
    ("playground refurbishment", "play modules", 6, 7_800_000),
    ("tree planting", "trees planted", 90, 5_400_000),
    ("bus stop shelters", "shelters installed", 8, 11_300_000),
]
COMUNAS = [("Macul", -33.487, -70.598), ("Nunoa", -33.456, -70.598), ("La Florida", -33.522, -70.583),
           ("Penalolen", -33.478, -70.541), ("Maipu", -33.511, -70.758)]
FAR = [("Antofagasta", -23.650, -70.400), ("Valdivia", -39.819, -73.245), ("Iquique", -20.230, -70.135)]
SUPERVISORS = ["R. Gonzalez", "M. Paredes", "C. Fuentes", "A. Riquelme", "P. Soto"]
VENDORS = ["Constructora Andes SpA", "Servicios Urbanos Ltda", "Obras del Sur SpA", "Ingenieria Vega Ltda"]


def iso(d: date) -> str:
    return d.isoformat()


def make_base(rng: random.Random, idx: int) -> dict:
    ptype, unit, qty, target = rng.choice(PROJECT_TYPES)
    comuna, lat, lon = rng.choice(COMUNAS)
    start = date(2026, rng.randint(1, 4), rng.randint(1, 28))
    dur = rng.randint(18, 45)
    end = start + timedelta(days=dur)
    supervisor = rng.choice(SUPERVISORS)
    vendor = rng.choice(VENDORS)
    invoice_amt = int(target * rng.uniform(0.90, 0.99))
    n_photos = rng.randint(3, 6)
    photo_days = sorted(rng.sample(range(2, dur), min(n_photos, dur - 3)))
    photos = [{"file": f"IMG_{idx:03d}_{i}.jpg", "timestamp": iso(start + timedelta(days=d)) + f"T{rng.randint(9, 17):02d}:{rng.randint(0, 59):02d}",
               "geotag": [round(lat + rng.uniform(-0.002, 0.002), 4), round(lon + rng.uniform(-0.002, 0.002), 4)],
               "sha256_prefix": f"{rng.getrandbits(48):012x}"} for i, d in enumerate(photo_days)]
    qty_delivered = qty
    return {
        "project": {"type": ptype, "comuna": comuna, "site_geotag": [lat, lon], "funded_target_clp": target,
                    "contracted_quantity": f"{qty} {unit}"},
        "certificates": {"works_start": {"date": iso(start), "signed_by": supervisor},
                          "completion": {"date": iso(end), "signed_by": supervisor,
                                          "declared_quantity": f"{qty_delivered} {unit}"}},
        "invoice": {"vendor": vendor, "amount_clp": invoice_amt, "date": iso(end + timedelta(days=rng.randint(1, 5))),
                     "items": f"{qty_delivered} {unit}"},
        "photos": photos,
        "custody_log": [f"captured by fiscalizer on site, uploaded {iso(start + timedelta(days=d))}" for d in photo_days[:2]]
                       + ["hash-sealed at ingestion", "stored WORM archive"],
        "prior_evidence_registry_excerpt": [],
    }


def inject_flaw(rng: random.Random, v: dict, flaw: str) -> None:
    start = date.fromisoformat(v["certificates"]["works_start"]["date"])
    if flaw == "fabricated_progress":
        for p in v["photos"]:
            p["timestamp"] = iso(start - timedelta(days=rng.randint(3, 20))) + p["timestamp"][10:]
    elif flaw == "metadata_inconsistency":
        pick = rng.random()
        if pick < 0.5:
            v["certificates"]["completion"]["date"] = iso(start - timedelta(days=rng.randint(2, 15)))
        else:
            v["invoice"]["date"] = iso(start - timedelta(days=rng.randint(5, 25)))
            v["certificates"]["completion"]["signed_by"] = "J. Morales"  # never appears elsewhere
    elif flaw == "wrong_location":
        city, lat, lon = rng.choice(FAR)
        for p in v["photos"]:
            p["geotag"] = [round(lat + rng.uniform(-0.002, 0.002), 4), round(lon + rng.uniform(-0.002, 0.002), 4)]
    elif flaw == "recycled_evidence":
        dup = [p["sha256_prefix"] for p in v["photos"][:3]]
        v["prior_evidence_registry_excerpt"] = [
            {"project": "plaza repair 2024 (closed)", "file_hash_prefix": h, "archived": "2024-11-12"} for h in dup]
    elif flaw == "quantity_mismatch":
        v["invoice"]["amount_clp"] = int(v["project"]["funded_target_clp"] * rng.uniform(1.25, 1.6))
        qty = int(v["project"]["contracted_quantity"].split()[0])
        v["invoice"]["items"] = v["project"]["contracted_quantity"].replace(str(qty), str(int(qty * 1.4)), 1)
    elif flaw == "plausible_staging":
        # Internally consistent; circumstantially wrong: all progress photos
        # taken within minutes on the final day, completion signed on a Sunday,
        # round-number invoice just under the target, first-time vendor.
        end = date.fromisoformat(v["certificates"]["completion"]["date"])
        sunday = end + timedelta(days=(6 - end.weekday()) % 7)
        v["certificates"]["completion"]["date"] = iso(sunday)
        base_min = rng.randint(0, 30)
        for i, p in enumerate(v["photos"]):
            p["timestamp"] = iso(sunday) + f"T07:{base_min + i:02d}"
        v["invoice"]["amount_clp"] = int(round(v["project"]["funded_target_clp"] * 0.99, -5))
        v["invoice"]["date"] = iso(sunday)
        v["invoice"]["vendor"] = "Comercial Rapida EIRL (first registered 14 days ago)"
        v["custody_log"] = ["bulk-uploaded by executor (not fiscalizer)", "hash-sealed at ingestion"]


def main() -> None:
    rng = random.Random(SEED)
    flaws = ["fabricated_progress", "metadata_inconsistency", "wrong_location",
             "recycled_evidence", "quantity_mismatch", "plausible_staging"]
    cases = []
    for i in range(60):
        v = make_base(rng, i)
        cases.append({"id": f"C{i:03d}", "ground_truth": "clean", "bundle": v})
    idx = 60
    for flaw in flaws:
        for _ in range(10):
            v = make_base(rng, idx)
            inject_flaw(rng, v, flaw)
            cases.append({"id": f"C{idx:03d}", "ground_truth": flaw, "bundle": v})
            idx += 1
    rng.shuffle(cases)  # presentation order must not encode ground truth
    OUT.write_text(json.dumps({"seed": SEED, "n": len(cases), "cases": cases}, indent=1), encoding="utf-8")
    n_clean = sum(1 for c in cases if c["ground_truth"] == "clean")
    print(f"wrote {len(cases)} vignettes ({n_clean} clean) -> {OUT}")


if __name__ == "__main__":
    main()
