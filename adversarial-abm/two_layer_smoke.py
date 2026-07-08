"""Smoke of the CORRECTED two-channel model (design v2). Standalone.

#1 macro categorization: a CENTRAL partition admits a fraction of misaligned
(low societal value) projects into the eligible pool; a DISTRIBUTED partition
does not (pool aligned with value). #2 channels differ in category-awareness:
  - attentive / targeted-profile: value-aware  -> fund high theta (avoid lows)
  - incidental-profile ("near me"): routes ~orthogonal to value -> funds pool
    at random => leaks into the low-value projects a bad partition admitted
  - salience: value-blind
Checks PL1 (distributing #1 helps most when profiles are incidental-heavy) and
PL2 (leakage ~ inattentive_share * incidental_share).
"""
import random

N = 200            # eligible projects
SCARCITY = 0.33    # fundable fraction (budget = SCARCITY*N, each target 1.0)
P_MIS = 0.35       # under CENTRAL partition, share of pool that is misaligned (low theta)
RUNS = 300


def make_pool(distributed, rng):
    """Eligible project true values. Distributed: all aligned. Central: a P_MIS
    share are misaligned/low-value (admitted by a badly-chosen category)."""
    theta = []
    for _ in range(N):
        if not distributed and rng.random() < P_MIS:
            theta.append(rng.uniform(0.0, 0.30))   # misaligned: low societal value
        else:
            theta.append(rng.uniform(0.30, 1.0))   # aligned
    return theta


def allocate(theta, s_att, s_targ, s_inc, s_sal, rng):
    """Split budget across channels by citizen share; each channel routes with
    its own value-sensitivity. Returns delivered value and value leaked to lows."""
    B = SCARCITY * N
    order_value = sorted(range(N), key=lambda j: theta[j], reverse=True)          # value-aware
    order_noisy = sorted(range(N), key=lambda j: theta[j] + rng.gauss(0, 0.25), reverse=True)
    order_rand = list(range(N)); rng.shuffle(order_rand)                          # incidental ~ orthogonal to value
    order_sal = list(range(N)); rng.shuffle(order_sal)                            # salience ~ value-blind

    funded = [0.0] * N

    def spend(order, budget):
        for j in order:
            if budget <= 0:
                break
            give = min(budget, 1.0 - funded[j])
            funded[j] += give
            budget -= give

    spend(order_value, B * s_att)
    spend(order_noisy, B * s_targ)
    spend(order_rand, B * s_inc)
    spend(order_sal, B * s_sal)

    delivered = sum(theta[j] * funded[j] for j in range(N))
    leaked = sum(theta[j] * funded[j] for j in range(N) if theta[j] < 0.30)  # value-weighted spend on lows
    spent = sum(funded)
    return delivered / spent, sum(funded[j] for j in range(N) if theta[j] < 0.30) / spent


def avg(distributed, s_att, s_targ, s_inc, s_sal):
    rng = random.Random(42)
    vs, ls = [], []
    for _ in range(RUNS):
        v, leak = allocate(make_pool(distributed, rng), s_att, s_targ, s_inc, s_sal, rng)
        vs.append(v); ls.append(leak)
    return sum(vs) / len(vs), sum(ls) / len(ls)


print("=== PL1: gain from distributing #1 (partition) vs profile composition ===")
print("attentive fixed 5%; remaining 95% inattentive split between TARGETED and INCIDENTAL profiles\n")
print(f"{'incidental share of profiles':<30}{'V central':>10}{'V distrib':>11}{'gain(#1)':>10}{'leak(central)':>15}")
S_ATT = 0.05
for inc_frac in (0.1, 0.3, 0.5, 0.7, 0.9):
    prof = 1 - S_ATT
    s_inc = prof * inc_frac
    s_targ = prof * (1 - inc_frac)
    vc, lc = avg(False, S_ATT, s_targ, s_inc, 0.0)
    vd, ld = avg(True, S_ATT, s_targ, s_inc, 0.0)
    print(f"{inc_frac:<30.1f}{vc:>10.4f}{vd:>11.4f}{vd-vc:>10.4f}{lc:>15.3f}")

print("\n=== PL2: leakage under CENTRAL partition ~ inattentive_share * incidental_share ===")
print(f"{'inattentive share':<20}{'incidental frac':<18}{'leak (central)':>15}{'predicted ~':>14}")
for inatt in (0.5, 0.75, 0.95):
    for inc_frac in (0.2, 0.8):
        s_att = 1 - inatt
        s_inc = inatt * inc_frac
        s_targ = inatt * (1 - inc_frac)
        _, lc = avg(False, s_att, s_targ, s_inc, 0.0)
        print(f"{inatt:<20.2f}{inc_frac:<18.1f}{lc:>15.3f}{inatt*inc_frac:>14.2f}")

print("\n=== PL3 regression bridge: |C|=1 (no misaligned categories admittable) ===")
print("distributed pool == the |C|=1 well-formed case; central==bad partition. Both are pure channel routing.")
vd, _ = avg(True, 0.05, 0.5*0.95, 0.5*0.95, 0.0)
print(f"  distributed (well-formed pool) V/budget = {vd:.4f}  (this is the reduction target)")
