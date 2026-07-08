# Experiment F-2: the control-cost frontier (engine v0.12.0)

V_total = verifiedValue / (delivery budget + human cost + machine cost + evidence premium); tranche=400, rho=0.3; pull W*=7; 20 runs, seed 1.
Machine cost swept over {0.1%/milestone (hosted-API stipulation), 0 (open-weights local: energy/hardware are sunk or marginal — author correction 2026-07-07)}.

| K | regime | h (human %/milestone) | e (evidence %/milestone) | machine cost | V plain | control+evidence cost (% of budget) | V per TOTAL budget |
|---:|---|---:|---:|---:|---:|---:|---:|
| 6 | pure human | 3% | 0.5% | 0.1% | 0.304 | 3.3% | 0.294 |
| 6 | pure human | 3% | 0.5% | 0 (local) | 0.304 | 3.3% | 0.294 |
| 6 | pure human | 3% | 2.0% | 0.1% | 0.304 | 4.8% | 0.290 |
| 6 | pure human | 3% | 2.0% | 0 (local) | 0.304 | 4.8% | 0.290 |
| 6 | pure human | 3% | 5.0% | 0.1% | 0.304 | 7.6% | 0.282 |
| 6 | pure human | 3% | 5.0% | 0 (local) | 0.304 | 7.6% | 0.282 |
| 6 | pure human | 6% | 0.5% | 0.1% | 0.304 | 6.2% | 0.286 |
| 6 | pure human | 6% | 0.5% | 0 (local) | 0.304 | 6.2% | 0.286 |
| 6 | pure human | 6% | 2.0% | 0.1% | 0.304 | 7.6% | 0.282 |
| 6 | pure human | 6% | 2.0% | 0 (local) | 0.304 | 7.6% | 0.282 |
| 6 | pure human | 6% | 5.0% | 0.1% | 0.304 | 10.5% | 0.275 |
| 6 | pure human | 6% | 5.0% | 0 (local) | 0.304 | 10.5% | 0.275 |
| 6 | pure human | 10% | 0.5% | 0.1% | 0.304 | 10.0% | 0.276 |
| 6 | pure human | 10% | 0.5% | 0 (local) | 0.304 | 10.0% | 0.276 |
| 6 | pure human | 10% | 2.0% | 0.1% | 0.304 | 11.4% | 0.273 |
| 6 | pure human | 10% | 2.0% | 0 (local) | 0.304 | 11.4% | 0.273 |
| 6 | pure human | 10% | 5.0% | 0.1% | 0.304 | 14.3% | 0.266 |
| 6 | pure human | 10% | 5.0% | 0 (local) | 0.304 | 14.3% | 0.266 |
| 6 | triage 1-layer (E-1c) | 3% | 0.5% | 0.1% | 0.306 | 1.7% | 0.301 |
| 6 | triage 1-layer (E-1c) | 3% | 0.5% | 0 (local) | 0.306 | 1.7% | 0.301 |
| 6 | triage 1-layer (E-1c) | 3% | 2.0% | 0.1% | 0.306 | 3.2% | 0.296 |
| 6 | triage 1-layer (E-1c) | 3% | 2.0% | 0 (local) | 0.306 | 3.2% | 0.296 |
| 6 | triage 1-layer (E-1c) | 3% | 5.0% | 0.1% | 0.306 | 6.2% | 0.288 |
| 6 | triage 1-layer (E-1c) | 3% | 5.0% | 0 (local) | 0.306 | 6.2% | 0.288 |
| 6 | triage 1-layer (E-1c) | 6% | 0.5% | 0.1% | 0.306 | 2.9% | 0.297 |
| 6 | triage 1-layer (E-1c) | 6% | 0.5% | 0 (local) | 0.306 | 2.8% | 0.297 |
| 6 | triage 1-layer (E-1c) | 6% | 2.0% | 0.1% | 0.306 | 4.4% | 0.293 |
| 6 | triage 1-layer (E-1c) | 6% | 2.0% | 0 (local) | 0.306 | 4.3% | 0.293 |
| 6 | triage 1-layer (E-1c) | 6% | 5.0% | 0.1% | 0.306 | 7.4% | 0.285 |
| 6 | triage 1-layer (E-1c) | 6% | 5.0% | 0 (local) | 0.306 | 7.3% | 0.285 |
| 6 | triage 1-layer (E-1c) | 10% | 0.5% | 0.1% | 0.306 | 4.4% | 0.293 |
| 6 | triage 1-layer (E-1c) | 10% | 0.5% | 0 (local) | 0.306 | 4.4% | 0.293 |
| 6 | triage 1-layer (E-1c) | 10% | 2.0% | 0.1% | 0.306 | 5.9% | 0.289 |
| 6 | triage 1-layer (E-1c) | 10% | 2.0% | 0 (local) | 0.306 | 5.9% | 0.289 |
| 6 | triage 1-layer (E-1c) | 10% | 5.0% | 0.1% | 0.306 | 8.9% | 0.281 |
| 6 | triage 1-layer (E-1c) | 10% | 5.0% | 0 (local) | 0.306 | 8.9% | 0.281 |
| 6 | layered k=2 (rho=0.3) | 3% | 0.5% | 0.1% | 0.307 | 1.9% | 0.301 |
| 6 | layered k=2 (rho=0.3) | 3% | 0.5% | 0 (local) | 0.307 | 1.8% | 0.302 |
| 6 | layered k=2 (rho=0.3) | 3% | 2.0% | 0.1% | 0.307 | 3.4% | 0.297 |
| 6 | layered k=2 (rho=0.3) | 3% | 2.0% | 0 (local) | 0.307 | 3.3% | 0.297 |
| 6 | layered k=2 (rho=0.3) | 3% | 5.0% | 0.1% | 0.307 | 6.4% | 0.289 |
| 6 | layered k=2 (rho=0.3) | 3% | 5.0% | 0 (local) | 0.307 | 6.3% | 0.289 |
| 6 | layered k=2 (rho=0.3) | 6% | 0.5% | 0.1% | 0.307 | 3.2% | 0.297 |
| 6 | layered k=2 (rho=0.3) | 6% | 0.5% | 0 (local) | 0.307 | 3.2% | 0.298 |
| 6 | layered k=2 (rho=0.3) | 6% | 2.0% | 0.1% | 0.307 | 4.7% | 0.293 |
| 6 | layered k=2 (rho=0.3) | 6% | 2.0% | 0 (local) | 0.307 | 4.7% | 0.293 |
| 6 | layered k=2 (rho=0.3) | 6% | 5.0% | 0.1% | 0.307 | 7.7% | 0.285 |
| 6 | layered k=2 (rho=0.3) | 6% | 5.0% | 0 (local) | 0.307 | 7.7% | 0.285 |
| 6 | layered k=2 (rho=0.3) | 10% | 0.5% | 0.1% | 0.307 | 5.0% | 0.292 |
| 6 | layered k=2 (rho=0.3) | 10% | 0.5% | 0 (local) | 0.307 | 5.0% | 0.293 |
| 6 | layered k=2 (rho=0.3) | 10% | 2.0% | 0.1% | 0.307 | 6.5% | 0.288 |
| 6 | layered k=2 (rho=0.3) | 10% | 2.0% | 0 (local) | 0.307 | 6.5% | 0.288 |
| 6 | layered k=2 (rho=0.3) | 10% | 5.0% | 0.1% | 0.307 | 9.5% | 0.280 |
| 6 | layered k=2 (rho=0.3) | 10% | 5.0% | 0 (local) | 0.307 | 9.5% | 0.281 |
| 4 | pure human | 3% | 0.5% | 0.1% | 0.254 | 2.7% | 0.247 |
| 4 | pure human | 3% | 0.5% | 0 (local) | 0.254 | 2.7% | 0.247 |
| 4 | pure human | 3% | 2.0% | 0.1% | 0.254 | 3.8% | 0.244 |
| 4 | pure human | 3% | 2.0% | 0 (local) | 0.254 | 3.8% | 0.244 |
| 4 | pure human | 3% | 5.0% | 0.1% | 0.254 | 6.1% | 0.239 |
| 4 | pure human | 3% | 5.0% | 0 (local) | 0.254 | 6.1% | 0.239 |
| 4 | pure human | 6% | 0.5% | 0.1% | 0.254 | 5.0% | 0.242 |
| 4 | pure human | 6% | 0.5% | 0 (local) | 0.254 | 5.0% | 0.242 |
| 4 | pure human | 6% | 2.0% | 0.1% | 0.254 | 6.1% | 0.239 |
| 4 | pure human | 6% | 2.0% | 0 (local) | 0.254 | 6.1% | 0.239 |
| 4 | pure human | 6% | 5.0% | 0.1% | 0.254 | 8.4% | 0.234 |
| 4 | pure human | 6% | 5.0% | 0 (local) | 0.254 | 8.4% | 0.234 |
| 4 | pure human | 10% | 0.5% | 0.1% | 0.254 | 8.0% | 0.235 |
| 4 | pure human | 10% | 0.5% | 0 (local) | 0.254 | 8.0% | 0.235 |
| 4 | pure human | 10% | 2.0% | 0.1% | 0.254 | 9.2% | 0.232 |
| 4 | pure human | 10% | 2.0% | 0 (local) | 0.254 | 9.2% | 0.232 |
| 4 | pure human | 10% | 5.0% | 0.1% | 0.254 | 11.4% | 0.228 |
| 4 | pure human | 10% | 5.0% | 0 (local) | 0.254 | 11.4% | 0.228 |
| 4 | triage 1-layer (E-1c) | 3% | 0.5% | 0.1% | 0.305 | 1.7% | 0.300 |
| 4 | triage 1-layer (E-1c) | 3% | 0.5% | 0 (local) | 0.305 | 1.6% | 0.301 |
| 4 | triage 1-layer (E-1c) | 3% | 2.0% | 0.1% | 0.305 | 3.2% | 0.296 |
| 4 | triage 1-layer (E-1c) | 3% | 2.0% | 0 (local) | 0.305 | 3.1% | 0.296 |
| 4 | triage 1-layer (E-1c) | 3% | 5.0% | 0.1% | 0.305 | 6.2% | 0.288 |
| 4 | triage 1-layer (E-1c) | 3% | 5.0% | 0 (local) | 0.305 | 6.1% | 0.288 |
| 4 | triage 1-layer (E-1c) | 6% | 0.5% | 0.1% | 0.305 | 2.8% | 0.297 |
| 4 | triage 1-layer (E-1c) | 6% | 0.5% | 0 (local) | 0.305 | 2.8% | 0.297 |
| 4 | triage 1-layer (E-1c) | 6% | 2.0% | 0.1% | 0.305 | 4.3% | 0.293 |
| 4 | triage 1-layer (E-1c) | 6% | 2.0% | 0 (local) | 0.305 | 4.3% | 0.293 |
| 4 | triage 1-layer (E-1c) | 6% | 5.0% | 0.1% | 0.305 | 7.3% | 0.285 |
| 4 | triage 1-layer (E-1c) | 6% | 5.0% | 0 (local) | 0.305 | 7.3% | 0.285 |
| 4 | triage 1-layer (E-1c) | 10% | 0.5% | 0.1% | 0.305 | 4.4% | 0.293 |
| 4 | triage 1-layer (E-1c) | 10% | 0.5% | 0 (local) | 0.305 | 4.3% | 0.293 |
| 4 | triage 1-layer (E-1c) | 10% | 2.0% | 0.1% | 0.305 | 5.9% | 0.289 |
| 4 | triage 1-layer (E-1c) | 10% | 2.0% | 0 (local) | 0.305 | 5.8% | 0.289 |
| 4 | triage 1-layer (E-1c) | 10% | 5.0% | 0.1% | 0.305 | 8.8% | 0.281 |
| 4 | triage 1-layer (E-1c) | 10% | 5.0% | 0 (local) | 0.305 | 8.8% | 0.281 |
| 4 | layered k=2 (rho=0.3) | 3% | 0.5% | 0.1% | 0.306 | 1.9% | 0.300 |
| 4 | layered k=2 (rho=0.3) | 3% | 0.5% | 0 (local) | 0.306 | 1.8% | 0.300 |
| 4 | layered k=2 (rho=0.3) | 3% | 2.0% | 0.1% | 0.306 | 3.3% | 0.296 |
| 4 | layered k=2 (rho=0.3) | 3% | 2.0% | 0 (local) | 0.306 | 3.3% | 0.296 |
| 4 | layered k=2 (rho=0.3) | 3% | 5.0% | 0.1% | 0.306 | 6.3% | 0.288 |
| 4 | layered k=2 (rho=0.3) | 3% | 5.0% | 0 (local) | 0.306 | 6.2% | 0.288 |
| 4 | layered k=2 (rho=0.3) | 6% | 0.5% | 0.1% | 0.306 | 3.2% | 0.296 |
| 4 | layered k=2 (rho=0.3) | 6% | 0.5% | 0 (local) | 0.306 | 3.2% | 0.296 |
| 4 | layered k=2 (rho=0.3) | 6% | 2.0% | 0.1% | 0.306 | 4.7% | 0.292 |
| 4 | layered k=2 (rho=0.3) | 6% | 2.0% | 0 (local) | 0.306 | 4.6% | 0.292 |
| 4 | layered k=2 (rho=0.3) | 6% | 5.0% | 0.1% | 0.306 | 7.6% | 0.284 |
| 4 | layered k=2 (rho=0.3) | 6% | 5.0% | 0 (local) | 0.306 | 7.6% | 0.284 |
| 4 | layered k=2 (rho=0.3) | 10% | 0.5% | 0.1% | 0.306 | 5.0% | 0.291 |
| 4 | layered k=2 (rho=0.3) | 10% | 0.5% | 0 (local) | 0.306 | 5.0% | 0.291 |
| 4 | layered k=2 (rho=0.3) | 10% | 2.0% | 0.1% | 0.306 | 6.5% | 0.287 |
| 4 | layered k=2 (rho=0.3) | 10% | 2.0% | 0 (local) | 0.306 | 6.4% | 0.287 |
| 4 | layered k=2 (rho=0.3) | 10% | 5.0% | 0.1% | 0.306 | 9.4% | 0.279 |
| 4 | layered k=2 (rho=0.3) | 10% | 5.0% | 0 (local) | 0.306 | 9.4% | 0.279 |

## Dominance notes
- K=6, h=3%: e=0.5%: layered>=triage; e=2.0%: layered>=triage; e=5.0%: layered>=triage
- K=6, h=6%: e=0.5%: layered>=triage; e=2.0%: layered>=triage; e=5.0%: layered>=triage
- K=6, h=10%: e=0.5%: triage>layered; e=2.0%: triage>layered; e=5.0%: triage>layered
- K=4, h=3%: e=0.5%: triage>layered; e=2.0%: triage>layered; e=5.0%: triage>layered
- K=4, h=6%: e=0.5%: triage>layered; e=2.0%: triage>layered; e=5.0%: triage>layered
- K=4, h=10%: e=0.5%: triage>layered; e=2.0%: triage>layered; e=5.0%: triage>layered

