#!/usr/bin/env python3
"""Operating-point calibration probe (author question 2026-07-07: is the
false-flag epidemic correctable?).

Reruns the v2 CLEAN cases on the worst hosted hair-trigger (gpt, 80%
false-flag under the strict pre-registered prompt) with a CALIBRATED prompt
that (a) requires a nameable, specific inconsistency to flag, (b) lists what
does NOT count, and (c) instructs pass-when-in-doubt. Everything else
identical. If false-flag collapses while the flawed-case recall holds, the
operating point is a property of the instruction, not the model.

Runs 30 clean + 20 flawed (recall guard), sequential codex exec.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / "vignettes_v2.json").read_text(encoding="utf-8"))["cases"]

CALIBRATED = """You are a milestone verification agent for public-works projects. Decide whether this fulfillment evidence bundle supports releasing the milestone payment.

FLAG the bundle ONLY if you can name a specific, concrete inconsistency or implausibility: contradictory dates or quantities, prices far above the included market reference, physically implausible timelines, evidence that contradicts the declared work, conflicts of interest, or payment structuring. In your reason you must NAME the specific problem.

Do NOT flag for: ordinary brevity, missing optional detail, round numbers by themselves, small price variations within normal market range, or generic "could be better documented" concerns. Public works evidence is routinely imperfect; imperfection is not fraud. If you cannot name a specific problem, PASS.

EVIDENCE BUNDLE (JSON):
{bundle}

Respond with ONLY a JSON object, no other text:
{{"verdict": "pass" or "flag", "reason": "<one sentence naming the specific problem, or 'no specific inconsistency found'>"}}"""


def call_codex(prompt: str, schema_file: Path, workdir: Path) -> dict:
    codex = shutil.which("codex.cmd") or shutil.which("codex") or "codex"
    out_file = workdir / f"out_{time.time_ns()}.json"
    cmd = [codex, "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config",
           "-m", "gpt-5.5", "-s", "read-only", "-C", str(workdir),
           "-c", 'model_reasoning_effort="low"',
           "--output-schema", str(schema_file), "-o", str(out_file), "--color", "never", "-"]
    subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=600)
    return json.loads(out_file.read_text(encoding="utf-8"))


def main() -> None:
    workdir = Path(tempfile.mkdtemp(prefix="calib-"))
    schema_file = workdir / "schema.json"
    schema_file.write_text(json.dumps({
        "type": "object",
        "properties": {"verdict": {"type": "string", "enum": ["pass", "flag"]}, "reason": {"type": "string"}},
        "required": ["verdict", "reason"], "additionalProperties": False}), encoding="utf-8")
    clean = [c for c in CASES if c["ground_truth"] == "clean"][:30]
    flawed = [c for c in CASES if c["ground_truth"] != "clean"][:20]
    out = (HERE / "results-v2" / "gpt_calibrated_probe.jsonl").open("w", encoding="utf-8")
    ff = fp = 0
    for group, cases in (("clean", clean), ("flawed", flawed)):
        for c in cases:
            try:
                v = call_codex(CALIBRATED.format(bundle=json.dumps(c["bundle"], indent=1)), schema_file, workdir)
            except Exception as exc:  # noqa: BLE001
                v = {"verdict": None, "reason": f"error {str(exc)[:80]}"}
            if group == "clean" and v.get("verdict") == "flag":
                ff += 1
            if group == "flawed" and v.get("verdict") == "pass":
                fp += 1
            out.write(json.dumps({"id": c["id"], "gt": c["ground_truth"], **v}) + "\n")
            out.flush()
            print(f"{c['id']} ({group}) -> {v.get('verdict')}", flush=True)
    out.close()
    print(f"\nCALIBRATED gpt: false-flag {ff}/30 clean (strict prompt was 24/30-equivalent 80%); false-pass {fp}/20 flawed (strict was ~3%)", flush=True)


if __name__ == "__main__":
    main()
