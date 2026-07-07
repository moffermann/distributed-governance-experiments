#!/usr/bin/env python3
"""F-0 panel runner: one family per invocation, all 120 vignettes.

Usage:
    python run_panel.py --family gemma    # gemma4:26b via ollama
    python run_panel.py --family qwen     # qwen3.6:35b-a3b via ollama
    python run_panel.py --family deepseek # deepseek-r1:14b via ollama
    python run_panel.py --family gpt      # gpt-5.5 via codex exec
    python run_panel.py --family claude   # Claude (Fable) via claude -p

Identical prompt protocol for every family (pre-registered). Results stream to
results/<family>.jsonl (one line per case) and are resumable: already-answered
case ids are skipped on rerun. Ground truth is never sent to the model.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIGNETTES = json.loads((HERE / "vignettes.json").read_text(encoding="utf-8"))["cases"]
RESULTS_DIR = HERE / "results"
RESULTS_DIR.mkdir(exist_ok=True)

FAMILIES = {
    "gemma": {"backend": "ollama", "model": "gemma4:26b"},
    "qwen": {"backend": "ollama", "model": "qwen3.6:35b-a3b"},
    "deepseek": {"backend": "ollama", "model": "deepseek-r1:14b"},
    "gpt": {"backend": "codex", "model": "gpt-5.5"},
    "claude": {"backend": "claude", "model": "claude-fable (session default)"},
}

PROMPT_TEMPLATE = """You are a milestone verification agent for public-works projects. Judge the following fulfillment evidence bundle on its internal and circumstantial consistency: dates, amounts, quantities, locations, provenance, and custody. Flag the bundle if anything indicates the evidence may not truthfully support the milestone; pass it only if it is credible.

EVIDENCE BUNDLE (JSON):
{bundle}

Respond with ONLY a JSON object, no other text:
{{"verdict": "pass" or "flag", "reason": "<one sentence>"}}"""


def render(case: dict) -> str:
    return PROMPT_TEMPLATE.format(bundle=json.dumps(case["bundle"], indent=1))


def parse_verdict(raw: str) -> dict:
    candidates = re.findall(r"\{[^{}]*\}", raw, re.DOTALL)
    for cand in reversed(candidates):
        try:
            obj = json.loads(cand)
            if obj.get("verdict") in ("pass", "flag"):
                return obj
        except json.JSONDecodeError:
            continue
    raise ValueError(f"unparseable: {raw[-200:]!r}")


def call_ollama(model: str, prompt: str) -> str:
    # HTTP API instead of the CLI: complete non-streamed responses, JSON-mode
    # decoding, temperature 0 for panel reproducibility; thinking disabled for
    # reasoning models (they emit malformed JSON under grammar constraint).
    import urllib.request
    body = {"model": model, "prompt": prompt, "stream": False, "format": "json",
            "options": {"temperature": 0}}
    if "deepseek" in model or "qwen" in model:
        body["think"] = False  # thinking models emit empty/malformed JSON under grammar constraint
    req = urllib.request.Request("http://localhost:11434/api/generate",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        return json.loads(resp.read().decode("utf-8"))["response"]


CODEX_SCHEMA: Path | None = None


def call_codex(prompt: str) -> str:
    global CODEX_SCHEMA
    codex = shutil.which("codex.cmd") or shutil.which("codex") or "codex"
    workdir = Path(tempfile.mkdtemp(prefix="f0-codex-"))
    if CODEX_SCHEMA is None:
        CODEX_SCHEMA = workdir / "schema.json"
        CODEX_SCHEMA.write_text(json.dumps({
            "type": "object",
            "properties": {"verdict": {"type": "string", "enum": ["pass", "flag"]}, "reason": {"type": "string"}},
            "required": ["verdict", "reason"], "additionalProperties": False}), encoding="utf-8")
    out_file = workdir / "out.json"
    cmd = [codex, "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config",
           "-m", "gpt-5.5", "-s", "read-only", "-C", str(workdir),
           "-c", 'model_reasoning_effort="low"',
           "--output-schema", str(CODEX_SCHEMA), "-o", str(out_file), "--color", "never", "-"]
    subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=600)
    return out_file.read_text(encoding="utf-8")


def call_claude(prompt: str) -> str:
    claude = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    # Prompt via stdin: the Windows .cmd shim mangles argv containing quotes/newlines.
    proc = subprocess.run([claude, "-p", "--output-format", "text"], input=prompt.encode("utf-8"), capture_output=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[-300:])
    return proc.stdout.decode("utf-8", "replace")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=sorted(FAMILIES))
    args = ap.parse_args()
    fam = FAMILIES[args.family]
    out_path = RESULTS_DIR / f"{args.family}.jsonl"
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line)["id"])
            except (json.JSONDecodeError, KeyError):
                continue
    todo = [c for c in VIGNETTES if c["id"] not in done]
    print(f"[{args.family}] {len(done)} done, {len(todo)} to go", flush=True)
    with out_path.open("a", encoding="utf-8") as fh:
        for i, case in enumerate(todo):
            prompt = render(case)
            t0 = time.time()
            verdict, error = None, None
            for attempt in range(3):
                try:
                    if fam["backend"] == "ollama":
                        raw = call_ollama(fam["model"], prompt)
                    elif fam["backend"] == "codex":
                        raw = call_codex(prompt)
                    else:
                        raw = call_claude(prompt)
                    verdict = parse_verdict(raw)
                    break
                except Exception as exc:  # noqa: BLE001
                    error = str(exc)[:200]
                    time.sleep(2.0)
            rec = {"id": case["id"], "family": args.family, "model": fam["model"],
                   "verdict": (verdict or {}).get("verdict"), "reason": (verdict or {}).get("reason"),
                   "error": None if verdict else error, "secs": round(time.time() - t0, 1)}
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            print(f"[{args.family}] {case['id']} -> {rec['verdict'] or 'ERROR'} ({rec['secs']}s) [{i + 1}/{len(todo)}]", flush=True)
    print(f"[{args.family}] COMPLETE", flush=True)


if __name__ == "__main__":
    main()
