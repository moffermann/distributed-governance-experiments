#!/usr/bin/env python3
"""High-temperature rescue for loop-resistant gemma v2 cases (same procedure
as the v1 rescue, recorded in provenance with a rescue note)."""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

os.environ["PANEL_INSTRUMENT"] = "v2"
HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
import run_panel  # noqa: E402  (v2 instrument via env)

best: dict[str, bool] = {}
res = HERE / "results-v2" / "gemma.jsonl"
for line in res.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    if r.get("verdict") in ("pass", "flag"):
        best[r["id"]] = True
pending = [c for c in run_panel.VIGNETTES if c["id"] not in best]
print(f"rescuing {len(pending)} cases: {[c['id'] for c in pending]}", flush=True)

out = res.open("a", encoding="utf-8")
for case in pending:
    prompt = run_panel.render(case)
    verdict = None
    for temp in (0.7, 0.9, 1.0):
        body = {"model": "gemma4:26b", "prompt": prompt, "stream": False, "format": "json",
                "options": {"temperature": temp, "repeat_penalty": 1.25}}
        req = urllib.request.Request("http://localhost:11434/api/generate",
                                     data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        try:
            raw = json.loads(urllib.request.urlopen(req, timeout=900).read().decode("utf-8"))["response"]
            verdict = run_panel.parse_verdict(raw)
            break
        except Exception as exc:  # noqa: BLE001
            print(case["id"], "temp", temp, "fail:", str(exc)[:80], flush=True)
    rec = {"id": case["id"], "family": "gemma", "model": "gemma4:26b",
           "verdict": (verdict or {}).get("verdict"), "reason": (verdict or {}).get("reason"),
           "error": None if verdict else "loop-resistant", "secs": None,
           "note": "high-temp rescue" if verdict else None}
    out.write(json.dumps(rec) + "\n")
    out.flush()
    print(case["id"], "->", rec["verdict"], flush=True)
out.close()
print("rescue complete", flush=True)
