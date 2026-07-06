# LLM Panel Run Results — 2026-07-06

## Execution

First executable runs of the calibration instrument (prompt version v0.3, Spanish, 6 archetypes × persona variations, schema-enforced structured output):

| Panel | Backend | Personas | Valid | Wall time | Effective rate |
|---|---|---:|---:|---:|---:|
| `2026-07-06-gpt-5.5-n15` | codex-exec (gpt-5.5, reasoning `low`) | 90 | 90/90 | 105 s | 1.2 s/resp |
| `2026-07-06-gemma-3-4b-n15` | LM Studio local (gemma-3-4b) | 90 | see results folder | ~20 s/resp serialized | — |

Backend benchmark (same panel prompt, 12 parallel requests): codex-exec ~2.0 s effective per response vs ~20.3 s on the serialized local server — ~10–17× throughput. Notes: codex reasoning effort `minimal` is rejected (incompatible with the model's built-in tools); `low` is the fast tier that works; codex does not expose temperature, so runs record `provider-default` and rely on persona variation for spread. Local-server parallelism is possible by loading multiple instances of the same model and using the runner's `--models` round-robin.

## Pooled results (gpt-5.5 panel, n=90)

| Field | mean | sd |
|---|---:|---:|
| platform_trial_probability | 0.709 | 0.151 |
| monthly_platform_use_probability | 0.441 | 0.178 |
| direct_planning_participation_probability | 0.416 | 0.194 |
| delegation_probability | 0.519 | 0.145 |
| would_accept_delegation (v0.3) | 0.418 | 0.154 |
| delegate_platform_use_rate | 0.536 | 0.175 |
| delegate_planning_coverage | 0.516 | 0.147 |

Preferred delegate types: trusted-person types (family, partner, friend, neighbor, community leader) 74.1%; institutional types (expert, institution/NGO, party, influencer) 22.7%; would not delegate 3.2%.

Archetype differentiation is coherent: the older low-digital archetype (A1) shows the lowest trial (0.56), ease (0.38), and delegate-acceptance (0.24); the young digital archetype (A6) the highest across the board (trial 0.90, direct planning 0.65, acceptance 0.60); the low-trust archetype (A4) delegates least (0.44). Zero context-check failures.

## Model sensitivity

The gemma-3-4b pilot (12 responses) produced much higher delegation (0.75) and delegate acceptance (0.73) with less plausible archetype ordering (A1 accepting delegation at 0.85). Both models converge on the micro-over-institutional delegate preference (gemma 84/15, gpt-5.5 74/23) and on `delegate_planning_coverage` around 0.40–0.52, inside the trusted-microdelegation prior band. Read only cross-model-stable patterns as informative; per-model levels are priors, not findings.

## Downstream use

The gpt-5.5 panel was mapped into the behavioral adoption ABM (`OUTPUT_TO_BEHAVIORAL_ABM.md` → `behavioral-adoption-abm/scenarios/llm_calibrated.json`); results in `behavioral-adoption-abm/RUN_2026_07_06_LLM_CALIBRATED_RESULTS.md`. Headline there: adoption-side outcomes are prior-sensitive, but the attentive share (~4.1%) and the verification bottleneck are structural — stable across synthetic and llm-elicited priors.

## Caveats

Stated intention overestimates behavior: no gpt-5.5 persona reported trial probability under 0.2, so the mapped permanent-rejection rate is 0.0 — treat adoption levels from this panel as upper bounds. These are synthetic priors under the protocol's methodological statement; the identical human instrument replaces them. Protocol scale (50–100 per archetype) is now cheap: ~600 personas ≈ 12 minutes on the codex backend.
