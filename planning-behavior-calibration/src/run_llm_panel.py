"""LLM calibration panel runner (PROMPT_PROTOCOL.md, prompt version v0.3).

Runs the Spanish calibration instrument against any OpenAI-compatible
chat-completions endpoint (LM Studio local server by default) with structured
JSON-schema output, one call per simulated respondent.

Per the protocol, the pipeline stores raw responses, parsed/normalized
responses, and validation warnings, and fits per-field distributions
(mean/sd/percentiles + Beta method-of-moments) per archetype and pooled.

Methodological statement (PROMPT_PROTOCOL.md): the LLM does not represent real
citizens. Outputs are synthetic prior elicitation over behavioral parameters,
to be replaced or validated by the human instrument.

Usage (LM Studio running on localhost:1234 with a small fast model):

    python src/run_llm_panel.py --model google/gemma-3-4b --n-per-archetype 20

Standard library only.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import random
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

PROMPT_VERSION = "v0.3"

ARCHETYPES = {
    "A1": "Persona mayor, comodidad limitada con aplicaciones móviles, puede depender de la familia para tareas digitales.",
    "A2": "Adulto que trabaja a tiempo completo, poco tiempo para participación cívica, usa aplicaciones móviles con comodidad.",
    "A3": "Ciudadano políticamente atento, sigue los asuntos públicos, compara proyectos, valora la transparencia.",
    "A4": "Ciudadano desconfiado de políticos, instituciones y posiblemente de delegados.",
    "A5": "Ciudadano rural o territorialmente distante de las instituciones centrales, valora el conocimiento local.",
    "A6": "Joven digitalmente activo, cómodo con aplicaciones, notificaciones e interfaces de decisión en línea.",
}

# Permitted prompt variations (PROMPT_PROTOCOL.md); core app facts never change.
VARIATIONS = {
    "setting": ["urbano", "rural", "ciudad intermedia"],
    "age_band": {
        "A1": ["65-74", "75+"],
        "A2": ["30-44", "45-59"],
        "A3": ["30-44", "45-59", "60-69"],
        "A4": ["25-39", "40-59"],
        "A5": ["30-49", "50-69"],
        "A6": ["18-24", "25-29"],
    },
    "digital_literacy": {
        "A1": ["baja", "media-baja"],
        "A2": ["media", "alta"],
        "A3": ["media", "alta"],
        "A4": ["media-baja", "media", "alta"],
        "A5": ["baja", "media"],
        "A6": ["alta"],
    },
    "political_interest": ["bajo", "medio", "alto"],
    "time_availability": ["muy poco", "algo", "bastante"],
    "family_trust": ["media", "alta"],
    "institutional_trust": ["baja", "media", "alta"],
}

CONTEXT_BRIEF = (
    "Imagina que existe una aplicación móvil oficial, simple y segura, que permite a los "
    "ciudadanos participar en la priorización y financiamiento de proyectos públicos. "
    "La aplicación NO te pide pagar dinero adicional de tu bolsillo: los recursos provienen "
    "de fondos públicos o impuestos que el Estado ya recauda y que serán destinados a "
    "proyectos públicos de todas maneras. La pregunta es cómo participarías si pudieras "
    "influir, desde tu celular, en qué proyectos públicos se financian. "
    "La aplicación permitiría: revisar proyectos elegibles con información resumida; apoyar "
    "prioridades o proyectos; delegar tu participación en otra persona (familiar, pareja, "
    "amigo, vecino, dirigente local, experto, organización, persona pública); recibir "
    "reportes sobre lo que hizo tu delegado y revisar sus acciones; revocar la delegación "
    "con un clic dentro de la app (sin trámites ni papeleo); cambiar de delegado cuando "
    "quieras; y volver a participar directamente cuando quieras. Si no tienes tiempo, "
    "interés o comodidad con la tecnología, delegar es una opción normal."
)

DELEGATE_TYPES = [
    "family_member", "partner_or_spouse", "trusted_friend", "trusted_neighbor",
    "local_community_leader", "technical_expert", "public_institution_or_ngo",
    "political_party_or_political_actor", "public_influencer", "would_not_delegate",
]

PROB = {"type": "number", "minimum": 0, "maximum": 1}
LLM_SCHEMA = {
    "type": "object",
    "properties": {
        "context_understanding": {
            "type": "object",
            "properties": {
                "not_extra_personal_money": {"type": "boolean"},
                "public_funds": {"type": "boolean"},
                "one_click_revocation": {"type": "boolean"},
                "understanding_score": PROB,
            },
            "required": ["not_extra_personal_money", "public_funds", "one_click_revocation", "understanding_score"],
        },
        "platform_behavior": {
            "type": "object",
            "properties": {
                "platform_trial_probability": PROB,
                "monthly_platform_use_probability": PROB,
                "notification_driven_use_probability": PROB,
            },
            "required": ["platform_trial_probability", "monthly_platform_use_probability", "notification_driven_use_probability"],
        },
        "citizen_behavior": {
            "type": "object",
            "properties": {
                "direct_review_probability": PROB,
                "direct_planning_participation_probability": PROB,
                "delegation_probability": PROB,
                "preferred_delegate_type_distribution": {
                    "type": "object",
                    "properties": {t: PROB for t in DELEGATE_TYPES},
                    "required": DELEGATE_TYPES,
                },
                "revocation_ease_effect": PROB,
                "report_visibility_effect": PROB,
                "report_read_probability_short": PROB,
                "report_read_probability_detailed": PROB,
                "revocation_likelihood_after_misalignment": PROB,
                "revocation_likelihood_after_inactivity": PROB,
            },
            "required": [
                "direct_review_probability", "direct_planning_participation_probability",
                "delegation_probability", "preferred_delegate_type_distribution",
                "revocation_ease_effect", "report_visibility_effect",
                "report_read_probability_short", "report_read_probability_detailed",
                "revocation_likelihood_after_misalignment", "revocation_likelihood_after_inactivity",
            ],
        },
        "delegate_behavior": {
            "type": "object",
            "properties": {
                "would_accept_delegation": PROB,
                "delegate_platform_use_rate": PROB,
                "delegate_planning_coverage": PROB,
                "delegate_responsibility_effect": PROB,
                "delegate_revocation_discipline_effect": PROB,
                "alignment_with_close_delegator": PROB,
                "alignment_with_impersonal_delegators": PROB,
                "delegate_report_quality_willingness": PROB,
            },
            "required": [
                "would_accept_delegation", "delegate_platform_use_rate", "delegate_planning_coverage",
                "delegate_responsibility_effect", "delegate_revocation_discipline_effect",
                "alignment_with_close_delegator", "alignment_with_impersonal_delegators",
                "delegate_report_quality_willingness",
            ],
        },
        "friction": {
            "type": "object",
            "properties": {
                "perceived_ease_of_use": PROB,
                "perceived_understanding": PROB,
                "need_for_assistance": PROB,
            },
            "required": ["perceived_ease_of_use", "perceived_understanding", "need_for_assistance"],
        },
        "free_text": {
            "type": "object",
            "properties": {
                "participation_reason": {"type": "string"},
                "trust_reason": {"type": "string"},
                "revocation_reason": {"type": "string"},
            },
            "required": ["participation_reason", "trust_reason", "revocation_reason"],
        },
        "confidence": {
            "type": "object",
            "properties": {"overall": PROB, "notes": {"type": "string"}},
            "required": ["overall", "notes"],
        },
    },
    "required": ["context_understanding", "platform_behavior", "citizen_behavior", "delegate_behavior", "friction", "free_text", "confidence"],
}

SYSTEM_PROMPT = (
    "Actúa como un participante simulado dentro del arquetipo indicado. No respondas como "
    "experto en políticas públicas ni como diseñador del sistema. Responde como una persona "
    "razonable que pertenece al arquetipo descrito, usando el contexto entregado. "
    "Las respuestas de texto libre deben ser de una sola frase corta. Devuelve solo JSON."
)

QUESTION_BLOCK = (
    "Responde el cuestionario completo con valores entre 0 y 1 donde corresponda: "
    "probabilidad de probar la app al menos una vez; de usarla al menos una vez al mes; de "
    "usarla si recibes recordatorios; de revisar directamente prioridades o proyectos; de "
    "participar directamente en planificación/priorización (no solo leer o delegar); de "
    "delegar tu participación; en quién delegarías (distribución que sume 1.0 entre los "
    "tipos dados); efecto de la revocación con un clic y de los reportes visibles en tu "
    "confianza; probabilidad de leer reportes cortos y detallados; probabilidad de revocar "
    "ante desalineación o inactividad del delegado; si un familiar o vecino te pidiera ser "
    "SU delegado, probabilidad de que aceptes (would_accept_delegation); si fueras delegado, "
    "qué tan seguido usarías la plataforma y qué fracción del plan revisarías; tu "
    "alineación con un delegante cercano versus impersonal; qué tan fácil te parecería usar "
    "la app, cuánto crees que la entenderías y cuánta ayuda necesitarías."
)


def build_persona(archetype_id: str, rng: random.Random, country: str) -> dict:
    return {
        "archetype_id": archetype_id,
        "description": ARCHETYPES[archetype_id],
        "country": country,
        "setting": rng.choice(VARIATIONS["setting"] if archetype_id != "A5" else ["rural", "ciudad intermedia"]),
        "age_band": rng.choice(VARIATIONS["age_band"][archetype_id]),
        "digital_literacy": rng.choice(VARIATIONS["digital_literacy"][archetype_id]),
        "political_interest": rng.choice(VARIATIONS["political_interest"]),
        "time_availability": rng.choice(VARIATIONS["time_availability"]),
        "family_trust": rng.choice(VARIATIONS["family_trust"]),
        "institutional_trust": rng.choice(VARIATIONS["institutional_trust"]),
    }


def build_user_prompt(persona: dict) -> str:
    block = (
        f"ARQUETIPO_ID: {persona['archetype_id']}\n"
        f"DESCRIPCIÓN: {persona['description']}\n"
        f"PAÍS/CONTEXTO: {persona['country']}, sector {persona['setting']}\n"
        f"EDAD_APROXIMADA: {persona['age_band']}\n"
        f"ALFABETIZACIÓN_DIGITAL: {persona['digital_literacy']}\n"
        f"INTERÉS_POLÍTICO: {persona['political_interest']}\n"
        f"TIEMPO_DISPONIBLE: {persona['time_availability']}\n"
        f"CONFIANZA_EN_FAMILIA: {persona['family_trust']}\n"
        f"CONFIANZA_EN_INSTITUCIONES: {persona['institutional_trust']}\n\n"
    )
    return block + CONTEXT_BRIEF + "\n\n" + QUESTION_BLOCK


def openai_strict(schema):
    """OpenAI strict structured outputs require additionalProperties:false on every object."""
    if isinstance(schema, dict):
        out = {k: openai_strict(v) for k, v in schema.items()}
        if out.get("type") == "object":
            out["additionalProperties"] = False
        return out
    if isinstance(schema, list):
        return [openai_strict(v) for v in schema]
    return schema


def call_codex_exec(codex_cmd: str, model: str, effort: str, persona: dict, schema_file: Path, workdir: Path, retries: int = 2) -> tuple[str, dict]:
    """Backend: `codex exec` (OpenAI Codex CLI, ChatGPT-plan auth). True server-side
    parallelism; reasoning effort 'low' is the fastest tier compatible with the
    model's built-in tools; temperature is provider-controlled."""
    prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(persona)
    out_file = workdir / f"{persona['response_id']}.json"
    cmd = [
        codex_cmd, "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config",
        "-m", model, "-s", "read-only", "-C", str(workdir),
        "-c", f'model_reasoning_effort="{effort}"',
        "--output-schema", str(schema_file), "-o", str(out_file), "--color", "never", "-",
    ]
    last_error: Exception | None = None
    for _ in range(retries + 1):
        try:
            proc = subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=600)
            raw = out_file.read_text(encoding="utf-8")
            return raw, json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            stderr = proc.stderr.decode("utf-8", "replace")[-200:] if "proc" in dir() else ""
            last_error = RuntimeError(f"{exc} {stderr}")
            time.sleep(1.0)
    raise RuntimeError(f"codex exec failed after retries: {last_error}")


def call_llm(base_url: str, api_key: str, model: str, persona: dict, temperature: float, max_tokens: int, retries: int = 2) -> tuple[str, dict]:
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "calibration_response", "strict": True, "schema": LLM_SCHEMA},
        },
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(persona)},
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    last_error: Exception | None = None
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(
                base_url.rstrip("/") + "/chat/completions",
                data=body,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                raw = resp.read().decode("utf-8")
            content = json.loads(raw)["choices"][0]["message"]["content"]
            return content, json.loads(content)
        except (urllib.error.URLError, json.JSONDecodeError, KeyError, IndexError) as exc:
            last_error = exc
            time.sleep(1.0)
    raise RuntimeError(f"LLM call failed after retries: {last_error}")


def validate(parsed: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []

    def walk_clamp(obj, path=""):
        if isinstance(obj, dict):
            return {k: walk_clamp(v, f"{path}.{k}") for k, v in obj.items()}
        if isinstance(obj, (int, float)) and not isinstance(obj, bool):
            if obj < 0 or obj > 1:
                warnings.append(f"clamped {path}={obj}")
                return max(0.0, min(1.0, float(obj)))
            return float(obj)
        return obj

    normalized = walk_clamp(parsed)
    dist = normalized["citizen_behavior"]["preferred_delegate_type_distribution"]
    total = sum(dist.values())
    if abs(total - 1.0) > 0.02:
        warnings.append(f"delegate distribution sums to {total:.3f}; renormalized")
    if total > 0:
        normalized["citizen_behavior"]["preferred_delegate_type_distribution"] = {k: v / total for k, v in dist.items()}
    cu = normalized["context_understanding"]
    if not (cu["not_extra_personal_money"] and cu["public_funds"] and cu["one_click_revocation"]):
        warnings.append("context check failed (flagged, kept)")
    return normalized, warnings


def numeric_fields(normalized: dict, prefix: str = "") -> dict:
    out = {}
    for key, value in normalized.items():
        path = f"{prefix}{key}"
        if isinstance(value, dict):
            out.update(numeric_fields(value, f"{path}."))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            out[path] = float(value)
    return out


def fit_field(values: list[float]) -> dict:
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / n if n > 1 else 0.0
    sorted_vals = sorted(values)

    def pct(q):
        idx = q * (n - 1)
        lo, hi = int(math.floor(idx)), min(int(math.floor(idx)) + 1, n - 1)
        return sorted_vals[lo] * (1 - (idx - lo)) + sorted_vals[hi] * (idx - lo)

    beta = None
    if 0.0 < mean < 1.0 and 0.0 < var < mean * (1 - mean):
        common = mean * (1 - mean) / var - 1
        beta = [round(mean * common, 4), round((1 - mean) * common, 4)]
    return {"n": n, "mean": round(mean, 4), "sd": round(math.sqrt(var), 4),
            "p10": round(pct(0.10), 4), "p50": round(pct(0.50), 4), "p90": round(pct(0.90), 4),
            "beta_moments": beta}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LLM calibration panel (PROMPT_PROTOCOL.md).")
    parser.add_argument("--backend", choices=["openai-compatible", "codex-exec"], default="openai-compatible",
                        help="openai-compatible: HTTP endpoint (LM Studio/OpenAI). codex-exec: OpenAI Codex CLI "
                             "(ChatGPT-plan auth, true parallel requests, ~10x throughput vs a serialized local server).")
    parser.add_argument("--base-url", default="http://localhost:1234/v1", help="OpenAI-compatible endpoint (LM Studio default).")
    parser.add_argument("--api-key", default="lm-studio")
    parser.add_argument("--model", default="google/gemma-3-4b")
    parser.add_argument("--codex-cmd", default="codex", help="Codex CLI executable for --backend codex-exec.")
    parser.add_argument("--codex-effort", default="low", help="model_reasoning_effort for codex-exec ('low' = fastest tier compatible with built-in tools).")
    parser.add_argument(
        "--models", default=None,
        help="Comma-separated model/instance ids to round-robin across (e.g. "
             "'google/gemma-3-4b,google/gemma-3-4b:2'). Load extra instances of the SAME "
             "base model in LM Studio for real server-side parallelism; mixing different "
             "base models in one panel contaminates the fitted distributions.",
    )
    parser.add_argument("--n-per-archetype", type=int, default=20)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--concurrency", type=int, default=6)
    parser.add_argument("--country", default="Chile")
    parser.add_argument("--seed", type=int, default=42, help="Seed for persona variation sampling.")
    parser.add_argument("--output-dir", default=None, help="Defaults to results/<run_id>/.")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    if args.backend == "codex-exec" and args.model == "google/gemma-3-4b":
        args.model = "gpt-5.5"  # sensible default for the codex backend
    model_pool = [m.strip() for m in args.models.split(",")] if args.models else [args.model]
    base_models = {m.split(":")[0] for m in model_pool}
    if len(base_models) > 1:
        print(f"WARNING: mixing different base models in one panel: {sorted(base_models)} — "
              "distributions will be contaminated; prefer instances of one model.")
    run_id = f"{date.today().isoformat()}-{model_pool[0].split('/')[-1].split(':')[0]}-n{args.n_per_archetype}"
    out_dir = Path(args.output_dir) if args.output_dir else Path(__file__).resolve().parent.parent / "results" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    personas = []
    for archetype_id in ARCHETYPES:
        for i in range(args.n_per_archetype):
            persona = build_persona(archetype_id, rng, args.country)
            persona["response_id"] = f"{run_id}-{archetype_id}-{i:03d}"
            personas.append(persona)

    started = time.time()
    results, failures = [], []

    if args.backend == "codex-exec":
        args.codex_cmd = (
            shutil.which(args.codex_cmd + ".cmd") or shutil.which(args.codex_cmd) or args.codex_cmd
        )
        codex_workdir = Path(tempfile.mkdtemp(prefix="codex-panel-"))
        schema_file = codex_workdir / "schema.json"
        schema_file.write_text(json.dumps(openai_strict(LLM_SCHEMA)), encoding="utf-8")

        def worker(persona, model_id):
            raw, parsed = call_codex_exec(args.codex_cmd, model_id, args.codex_effort, persona, schema_file, codex_workdir)
            normalized, warnings = validate(parsed)
            return persona, raw, normalized, warnings
    else:
        def worker(persona, model_id):
            raw, parsed = call_llm(args.base_url, args.api_key, model_id, persona, args.temperature, args.max_tokens)
            normalized, warnings = validate(parsed)
            return persona, raw, normalized, warnings

    max_workers = max(args.concurrency, len(model_pool))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(worker, p, model_pool[i % len(model_pool)]): p for i, p in enumerate(personas)}
        for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
            persona = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:  # noqa: BLE001 - recorded, run continues
                failures.append({"response_id": persona["response_id"], "error": str(exc)})
            if done % 10 == 0 or done == len(personas):
                print(f"{done}/{len(personas)} responses ({time.time() - started:.0f}s)")

    metadata = {
        "run_id": run_id, "respondent_source": "llm", "model_name": ",".join(model_pool),
        "provider": args.base_url if args.backend == "openai-compatible" else f"codex-exec (reasoning_effort={args.codex_effort})",
        "temperature": args.temperature if args.backend == "openai-compatible" else "provider-default",
        "prompt_version": PROMPT_VERSION, "date": date.today().isoformat(),
        "country": args.country, "language": "es", "persona_seed": args.seed,
        "n_requested": len(personas), "n_ok": len(results), "n_failed": len(failures),
        "methodological_statement": (
            "LLM-elicited synthetic priors over behavioral parameters; not real citizens, "
            "not empirical data (PROMPT_PROTOCOL.md)."
        ),
    }

    with (out_dir / "raw_responses.jsonl").open("w", encoding="utf-8") as fh:
        for persona, raw, _, _ in results:
            fh.write(json.dumps({"response_id": persona["response_id"], "persona": persona, "raw": raw}, ensure_ascii=False) + "\n")
    with (out_dir / "normalized_responses.jsonl").open("w", encoding="utf-8") as fh:
        for persona, _, normalized, warnings in results:
            record = {"response_id": persona["response_id"], "respondent_source": "llm",
                      "archetype_id": persona["archetype_id"], "persona": persona,
                      "model_or_sample_info": {k: metadata[k] for k in ("model_name", "temperature", "prompt_version", "date", "country", "language")},
                      **normalized, "validation_warnings": warnings}
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    by_archetype: dict[str, list[dict]] = {}
    for persona, _, normalized, _ in results:
        by_archetype.setdefault(persona["archetype_id"], []).append(numeric_fields(normalized))
    pooled = [fields for group in by_archetype.values() for fields in group]

    def summarize(groups: list[dict]) -> dict:
        keys = sorted({k for g in groups for k in g})
        return {k: fit_field([g[k] for g in groups if k in g]) for k in keys}

    summary = {
        "metadata": metadata,
        "failures": failures,
        "pooled": summarize(pooled),
        "by_archetype": {a: summarize(g) for a, g in sorted(by_archetype.items())},
        "pooled_preferred_delegate_type": {
            t: fit_field([g[f"citizen_behavior.preferred_delegate_type_distribution.{t}"] for g in pooled])["mean"]
            for t in DELEGATE_TYPES
        },
        "context_check_flags": sum(1 for _, _, _, w in results for x in w if "context check" in x),
    }
    with (out_dir / "panel_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")

    print(f"\nrun: {run_id}  ok={len(results)} failed={len(failures)}  elapsed={time.time() - started:.0f}s")
    for field in ("platform_behavior.platform_trial_probability",
                  "platform_behavior.monthly_platform_use_probability",
                  "citizen_behavior.direct_planning_participation_probability",
                  "citizen_behavior.delegation_probability",
                  "delegate_behavior.would_accept_delegation",
                  "delegate_behavior.delegate_platform_use_rate",
                  "delegate_behavior.delegate_planning_coverage"):
        stats = summary["pooled"].get(field)
        if stats:
            print(f"  {field:62s} mean={stats['mean']:.3f} sd={stats['sd']:.3f}")
    print(f"outputs: {out_dir}")


if __name__ == "__main__":
    main()
