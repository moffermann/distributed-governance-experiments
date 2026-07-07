#!/usr/bin/env python3
"""Experiment F — five-family panel smoke test.

Sends ONE identical evidence-judgment probe (an obviously flawed milestone
bundle: completion certificate dated before the works started, invoice above
the funded target) to every panel family and checks that each returns a
parseable verdict. This is plumbing verification only — NOT an F-0 vignette;
the F-0 instrument is committed separately before any panel run.

Expected verdict everywhere: "flag".

Families/backends:
  gemma4:26b, qwen3.6:35b-a3b, deepseek-r1:14b  -> ollama (local)
  gpt-5.5                                        -> codex exec (hosted CLI)
  claude (Fable)                                 -> claude -p (hosted CLI)
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROBE = """You are a milestone verification agent for public-works projects.
Judge the following fulfillment evidence bundle strictly on its internal consistency.

EVIDENCE BUNDLE
- project: sidewalk repair, funded target: 10,000,000 CLP
- works start certificate: dated 2026-05-10, signed by site supervisor
- completion certificate: dated 2026-04-30, signed by the same supervisor
- invoice: 12,000,000 CLP, dated 2026-05-02
- photos: 4, geotagged at the project site, timestamps 2026-05-28

Respond with ONLY a JSON object, no other text:
{"verdict": "pass" or "flag", "reason": "<one sentence>"}"""

EXPECTED = "flag"


def parse_verdict(raw: str) -> dict:
    # Tolerate reasoning-model preambles/think blocks: take the LAST JSON object.
    candidates = re.findall(r"\{[^{}]*\}", raw, re.DOTALL)
    for cand in reversed(candidates):
        try:
            obj = json.loads(cand)
            if "verdict" in obj:
                return obj
        except json.JSONDecodeError:
            continue
    raise ValueError(f"no parseable verdict in: {raw[-300:]!r}")


def run_ollama(model: str) -> tuple[dict, float]:
    import urllib.request
    t0 = time.time()
    body = {"model": model, "prompt": PROBE, "stream": False, "format": "json",
            "options": {"temperature": 0}}
    if "deepseek" in model or "qwen" in model:
        body["think"] = False  # thinking models emit empty/malformed JSON under grammar constraint
    req = urllib.request.Request("http://localhost:11434/api/generate",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        raw = json.loads(resp.read().decode("utf-8"))["response"]
    return parse_verdict(raw), time.time() - t0


def run_codex() -> tuple[dict, float]:
    codex = shutil.which("codex.cmd") or shutil.which("codex") or "codex"
    workdir = Path(tempfile.mkdtemp(prefix="evidence-smoke-"))
    out_file = workdir / "verdict.json"
    schema_file = workdir / "schema.json"
    schema_file.write_text(json.dumps({
        "type": "object",
        "properties": {"verdict": {"type": "string", "enum": ["pass", "flag"]}, "reason": {"type": "string"}},
        "required": ["verdict", "reason"], "additionalProperties": False,
    }), encoding="utf-8")
    cmd = [codex, "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config",
           "-m", "gpt-5.5", "-s", "read-only", "-C", str(workdir),
           "-c", 'model_reasoning_effort="low"',
           "--output-schema", str(schema_file), "-o", str(out_file), "--color", "never", "-"]
    t0 = time.time()
    subprocess.run(cmd, input=PROBE.encode("utf-8"), capture_output=True, timeout=600)
    return json.loads(out_file.read_text(encoding="utf-8")), time.time() - t0


def run_claude() -> tuple[dict, float]:
    claude = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    t0 = time.time()
    # Prompt via stdin: the Windows .cmd shim mangles argv containing quotes/newlines.
    proc = subprocess.run([claude, "-p", "--output-format", "text"], input=PROBE.encode("utf-8"), capture_output=True, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace")[-300:])
    return parse_verdict(proc.stdout.decode("utf-8", "replace")), time.time() - t0


def main() -> int:
    families = [
        ("gemma4:26b (Google, local)", lambda: run_ollama("gemma4:26b")),
        ("qwen3.6:35b-a3b (Alibaba, local)", lambda: run_ollama("qwen3.6:35b-a3b")),
        ("deepseek-r1:14b (DeepSeek, local; Qwen backbone declared)", lambda: run_ollama("deepseek-r1:14b")),
        ("gpt-5.5 (OpenAI, codex exec)", run_codex),
        ("claude Fable (Anthropic, claude -p)", run_claude),
    ]
    failures = 0
    print(f"{'family':<58} {'verdict':<8} {'ok':<4} {'secs':>6}  reason")
    for name, fn in families:
        try:
            verdict, secs = fn()
            ok = verdict.get("verdict") == EXPECTED
            if not ok:
                failures += 1
            print(f"{name:<58} {verdict.get('verdict', '?'):<8} {'YES' if ok else 'NO':<4} {secs:>6.1f}  {str(verdict.get('reason', ''))[:80]}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"{name:<58} ERROR    NO   {'':>6}  {str(exc)[:100]}")
    print(f"\nsmoke test: {5 - failures}/5 families operational and correct")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
