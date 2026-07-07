# Experiment D-lite — First Empirical Anchor (pilot protocol)

Registered 2026-07-07. The strongest surviving objection to the whole program is that every behavioral prior is synthetic (LLM-elicited), pending the identical human instrument. Experiment D (the full human calibration study) is not yet feasible, but a **bounded pilot** is — and it converts "pending" into "started" and provides the first empirical point against which the LLM panels can be checked.

## Purpose

Administer the *identical* instrument (`instruments/SURVEY_INSTRUMENT_ES.md`, the human twin of the LLM `PROMPT_PROTOCOL.md`) to a small convenience sample of real people (10–20: colleagues, acquaintances, non-experts), and compare their responses to the committed LLM panels on the load-bearing quantities.

## What it can and cannot establish

- **Can:** (a) that the instrument is comprehensible and completable by real people (face validity, completion time, confusion points); (b) a first empirical estimate of the load-bearing dispositional quantities — willingness to participate, channel preference (direct/profile/delegation/default), delegation acceptance, and the attentive-planning share; (c) whether the LLM-elicited distributions are inside, above, or below the human sample — the first real calibration check.
- **Cannot:** be representative (convenience sample, small n, no sampling frame), replace Experiment D, or license any population-level claim. It is a *calibration probe*, provenance class `human-pilot`, which — like `llm-elicited` — cannot be promoted to `empirical-representative`.

## Method

1. Same substantive context and question structure as the LLM protocol (the core principle of `HUMAN_STUDY_PROTOCOL.md`); no leading framing.
2. Consent and anonymity; no personal data beyond coarse demographics needed to contextualize.
3. Record raw responses under `human-pilot` provenance; compute the same summary statistics the LLM panels report.
4. Overlay the human sample on the committed LLM N=1000 panel distributions; report where they agree and diverge, with the divergence stated as a finding, not smoothed.

## Pre-registered comparison

- **PD1.** The attentive-planning share in the human pilot lands in the same low-single-digit band (2.5–5.1%) the synthetic and LLM sources produced and the participatory-budgeting field record reports — the finding's first empirical touch. If it lands materially outside, the structural-attentiveness claim is downgraded to model-and-field-only, and the divergence is the headline.
- **PD2.** Channel preference ordering (default/delegation dominating direct-active) survives in humans, or the endogenous-participation model's channel mix is recalibrated.

## Status

Instrument ready; awaiting the author's recruitment of the pilot sample (the one step the author flagged as not-yet-feasible for the full study but reachable for a pilot). Analysis harness is the existing panel analyzer with a `human-pilot` source added.
