# Two-Layer Allocation Redesign — Macro Categorization vs Project Allocation Profiles (pre-registered design v2)

Registered 2026-07-07, before implementation. Corrects a conceptual defect the terminology work surfaced: the engine fuses **two distinct institutional objects** into a single per-project weight, so it is numerically consistent but conceptually wrong — a third party reading the code would misunderstand the architecture. This v2 replaces an earlier draft whose "category weight vector × routing" multiplication was itself wrong (the corpus assigns **no weights** to macro categories). It supersedes and renames the misnamed "agenda-setting study" to **project-allocation-rules** (*agenda* wrongly implies planning/#1; *setting* wrongly implies fixed configuration).

## The defect

Each project currently gets one weight `w_j = mix·θ_j + (1−mix)·noise`, and the passive/default share funds projects ranked on `w_j`, with `mix` calibrated central-vs-distributed. This fuses:

- **Layer 1 — the macro categorization (`#1`).** A partition/tree of **eligible categories** (Education → Early-Childhood; Health → Elderly), chosen by the planner (central | distributed), through which every project must be **channeled**. It assigns **no budget weights** — it is *structure*. What varies is the partition's **alignment with latent value**: how well its categories match what society actually values.
- **Layer 2 — project allocation profiles (`#2`).** How each citizen's share reaches concrete projects, through channels the engine already models.

## The corrected model

### Layer 1 — macro categorization, characterized by alignment (not weights)

Projects belong to categories `c ∈ C`. Project `j` has true value `θ_j`, category `c(j)`, and attributes (e.g. proximity to each citizen, "pending-funding"). Each category carries an **emergent alignment** with latent value

```
α_c  ≈  correlation( category c's projects , latent value )   ∈ [0,1]
```

α is **not** planner-assigned; it emerges from the partition choice:
- **central partition**: risk of misaligned categories — some `α_c` low (the authority creates a category society does not value, e.g. a "Health → Gender Dysphoria" node society deprioritizes).
- **distributed partition**: `α_c` high by construction — society drew the categories around what it values.

Crucially, α does **not** hard-gate: with a single category (`|C| = 1`) all projects are in it, α is constant, and funding is not zeroed — it reduces to pure project routing. So Layer 1 acts **competitively/relatively across categories**, never as an absolute multiplier.

### Layer 2 — allocation channels, with a spectrum of alignment to `#1`

Society routes budget through the channels already in the engine (`allocateAttentive`, `allocateProfile`, `allocateDelegated`, `allocateSalience`, `allocateDefault`), which differ in **how their alignment relates to the categorization**:

- **Attentive / direct**, and **delegated** (delegate reviews at attentive grade): conscious of value *and* category → **avoid misaligned categories**, fund high `θ`. These punish a bad `#1`.
- **Profiles (inattentive)** — weighted rules over project attributes, spanning a spectrum:
  - **Value/category-targeted rules** ("rural early-childhood education", "elderly care"): select a value-relevant category/need → **high alignment, category-aware**; they help correct a bad `#1` by steering to good categories.
  - **Attribute-incidental rules** ("projects near me"): route by an attribute orthogonal to value → alignment is **incidental**, depending on (a) the local project mix and (b) `#1`'s quality (near-me hits value only if the nearby categories are well-aligned). **Category-blind → they leak funding into misaligned categories** (the citizen funds a nearby low-α project without choosing it consciously).
  - A profile's effective alignment = weighted by its **rule composition** (share of targeted vs incidental rules) — a per-population parameter.
- **Salience**: social-proof, value-blind (unchanged).

### Composition — sum of channels, each with its own α-sensitivity

```
funding_j = Σ_channels  share_channel · route_channel( j )
```

- attentive / delegated / **targeted-profile** routing: selection ∝ f(α_{c(j)}, θ_j) — category- and value-aware.
- **incidental-profile** routing ("near me"): selection ∝ attribute-match, **blind to α_{c(j)}** (so it funds low-α projects — the leak); the value it *realizes* is θ_j, and the attribute's value-correlation itself scales with α (a good partition makes "near me" hit value).
- salience: ∝ salience, value-blind.

Delivered value = Σ θ_j · fundedFraction_j. This is **not** the fused single weight, and **not** a plain category×project multiply; it is the sum of channels differing in category-awareness over a partition whose alignment is `#1`.

### What this measures that the fused model cannot

1. Separate contribution of `#1` (partition alignment) vs `#2` (channel routing quality).
2. The **leakage**: how much a bad central categorization is *not* corrected, because attribute-incidental profile rules fund misaligned-category projects anyway.
3. The role of **profile-rule composition** (targeted vs incidental) in self-correcting a bad `#1`.
4. How the **attentive share** and the profile-rule mix jointly set robustness to central mis-categorization.

## Pre-registered predictions

- **PL1.** The value of distributing `#1` (a well-aligned partition) is **largest when the profile channel is dominated by attribute-incidental rules** ("near me"): then only the attentive minority punishes bad categories and the inattentive majority leaks into them. With more value-targeted profile rules, `#1`'s alignment matters less — profiles self-correct. *(Validated in the static engine, `two_layer_validate.mjs`: the **relative** advantage of distributing the partition grows with the incidental share — 1.42× at 0.1 to 2.19× at 0.9. It holds as a **ratio/multiplier**, not as an absolute delivered-value gain: when incidental routing dominates both partitions deliver little in absolute terms, so the ratio is the meaningful measure — and it is also how the paper reports advantages.)*
- **PL2.** A bad central categorization leaks value in proportion to `(inattentive share) × (incidental-rule share)`; the gain from distributing `#1` is largest exactly there.
- **PL3.** The fused engine is the special case `|C| = 1` (α constant) or all-channels-equal-alignment; its published advantage decomposes into an `#1` (partition) share and a `#2` (routing) share, summing to the old number at `|C| = 1` — the regression bridge.
- **PL4 (robustness).** F1–F6's qualitative conclusions (default layer existential; deterrence stack complements-not-substitutes; attentiveness structural; release/verification results) survive the refactor; numbers shift, orderings and collapse structures hold.

## Regime mapping (docs/110), now representable

| regime | `#1` partition | `#2` channels |
|---|---|---|
| tutored, mandated agenda (scaffold) | central (misalignment risk) | distributed (attentive + profiles) |
| tutored, distributed agenda | distributed | distributed |
| semi-open | mandated over some categories, distributed elsewhere | distributed |
| open | distributed | distributed |

The fused model could not express the scaffold row (central `#1`, distributed `#2`), nor the leakage that makes a central partition only partially corrected.

## Migration plan (honest about cost)

1. **New engine version** (static + longitudinal): add categories + attributes to projects; give each category an emergent α; make attentive/delegated/targeted-profile channels category-aware and the incidental-profile channel category-blind (leaking); `prioritizationSource` splits into `partitionSource` (`#1`) and the per-channel routing of `#2`. The companion subsystem keeps its name — it builds `#1` (the partition + its α calibration); a new path calibrates the profile-rule composition of `#2`.
2. **New anchor.** `0.303844218531` belongs to the fused (`|C| = 1`) model and is retired; a new two-layer anchor is established and bit-pinned. The `|C| = 1` reduction reproducing the old number is the bridge proving no silent behavioral change.
3. **Re-run / re-validate** A, C, E, F, G on the two-layer engine; re-derive F1–F6; confirm PL4; report honestly any conclusion that does not survive.
4. **Terminology against a model that now separates the concepts**: `macro categorization` / `planning vector` = `#1`; `allocation profile` / `project allocation rules` = `#2`; the earlier fused-weight `planning→prioritization` rename is superseded (the weight is *split*, not renamed).
5. **Papers + corpus** updated to the two-layer model, with the fused single-weight model named as the prior reduced form and its limitation stated; re-deposit once re-validated.
6. **Rename** `agenda-setting-study-design` → `project-allocation-rules` (the `#2` mechanism-design questions), with the distinct `#1` question (how the partition is constructed) named precisely and separately — never "agenda-setting".

## Scope and non-goals

- Corrects the *conceptual structure* of the allocation model. Downstream mechanisms (deterrence, verification, release — F4–F8) are unchanged; they act on whichever projects get funded.
- Elicitation honesty, Sybil-resistance, and contraposition remain declared open problems; the two-layer model attaches them to the correct layer (`#2`), not to a fused abstraction.
- Still simulation evidence about a model — now one that does not misrepresent the institution it studies.
