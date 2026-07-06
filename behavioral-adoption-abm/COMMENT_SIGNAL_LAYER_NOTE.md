# Comment Signal Layer — Design Direction Note

## Author design direction (recorded 2026-07-06)

The citizen-comment layer — comments and questions posted with verified identity on projects (docs/101, "What you, a citizen, actually do") — constitutes a **qualitative evaluation surface** that none of the experiments currently model, and that eventually should be added, connected to the reputational theme: comments are a fast, informal, human-readable signal about execution quality and executor behavior that circulates before formal verification completes.

This note records the direction and its conformance guardrails so the extension is designed against the corpus rather than improvised later.

## Conformance guardrails (already resolved in the corpus)

- **Inform and trigger, never certify.** Comments may inform reputational surfaces and may trigger formal review, but they produce no hard formal effects — no payment gating, no milestone certification (docs/79, the evidence-quality gate: a citizen's photo can trigger review but cannot certify a construction milestone).
- **Inform, never exclude.** Whatever reputational surface comments feed, it obeys the informs-never-excludes principle (docs/107): funders may stop choosing an actor; the platform never removes one.
- **Voluntary self-disclosure only.** Public comments are the citizen's own speech (docs/108 residual): they never reveal allocations, and the secrecy-by-default boundary is untouched.
- **Aggregate-pattern discipline.** Any manipulation detection operates on aggregates and pseudonymous patterns, per the docs/98 clientelism-indicator precedent.

## How each experiment would consume it

- **Behavioral ABM**: active citizens produce comments after outcome exposure (propensity by mode and civic interest); comment sentiment is a noisy-but-fast signal of true execution quality that feeds other citizens' perceived project quality and delegate reputation *ahead of* formal verification — potentially shortening the trust-feedback latency that currently runs only through outcome stocks. Negative word-of-mouth from abandoned users already proxies a fragment of this.
- **Adversarial ABM**: the comment surface is an attack surface. Attack-library candidates: coordinated praise (astroturfing) inflating an opportunistic executor's reputation, brigading/defamation deflating an honest one, and chilling via harassment. Defense levers already in the corpus: verified identity, aggregate manipulation indicators, and escalation into the formal review path.
- **Paper engine (E8)**: deliberately out of scope — E8 crosses participation-side quantities only.

## Status

Recorded design direction, deferred by scope discipline: not part of Experiment C or the E8 bridge. Natural insertion points, in order: (1) behavioral model iteration after E8 (comment production + sentiment signal + reputation coupling), (2) adversarial attack library (`AGENTS_AND_ATTACKS.md`) with the astroturf/brigading pair, (3) only then any corpus-level resolution if simulation shows the layer changes outcomes enough to need explicit Core v0 rules beyond the guardrails above.
