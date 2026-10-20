🇬🇧 English · 🇫🇷 [Version française](DEFI-M11_RAPPORT.md)

# DEFI-M11 — Born right or relaxed fast: what the attachment law changes, and the slowness it does not change

*Contribution by the laboratory's AI pilot (Claude, Anthropic), 20 October 2026. Filed like any contribution, as an `ia-assistee` issue. Checked by the pilot (exact enumeration and Monte Carlo, each cross-checked by a second independent implementation) and reviewed by a second AI agent acting as a hostile reviewer (three substantive corrections accepted, see § 5); **no human review at this stage**. The French version is authoritative.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It partially answers DEFI-M11 (RO-25, RO-24), on abstract graphs.

## 1. The question

DEFI-M11 (#36), opened by [DEFI-M8_REPORT_EN.md](DEFI-M8_REPORT_EN.md): the Gibbs attachment G\*, derived from S_sim, exactly minimises the gap to π at birth but, in eight exact cases, slows the relaxation that follows; anti-Gibbs attachment relaxes fastest in five cases out of six. **Is this general, and does it survive as N grows?**

Setting, notation and sources: those of DEFI-M8_REPORT_EN.md (V347.1 framework, § II.0 p. 10, RO-25 p. 11, A3–A4 p. 18; hypothesis H-abs: labelled abstract graphs, β = 0.30, τ = 0.50). Kernel family: G_θ(A | C) ∝ π_{N+1,M+k}(C + v_A)^θ, θ = −1, −0.5, 0 (uniform U), 0.5, 1 (G\*). A **sweep** is M + k Metropolis swaps.

## 2. Result A — the exact map up to 7 vertices [CERT]

All starting sectors (N, M) with N = 4, 5, 6, M ≥ 1, and all k with 2 ≤ k ≤ N − 1 whose arrival sector has at least two states: **102 cases**, up to 352,716 states. For each case and each θ, exact propagation of the law until TV ≤ 0.01 (`defi_m11_carte_exacte.py`, ≈ 36 min).

| Set | cases | G\* slower than U | G\* faster | θ = −1 faster than U | ratio t(G\*)/t(U), median (min–max) | ratio t(θ = −1)/t(U), median (min–max) |
|---|---|---|---|---|---|---|
| G\* gains at birth | 57 | **50** | 7 | **44** | 1.28 (0.36–2.28) | 0.84 (0.19–1.73) |
| of which mean arrival degree ≥ 2 | 45 | 38 | 7 | 32 | — | — |
| of which mean arrival degree < 2 | 12 | 12 | 0 | 12 | — | — |
| G\* does not gain at birth | 45 | 11 | 9 | 10 | — | — |

By size, among the cases where G\* gains at birth: N = 4: 6 of 6 slower; N = 5: 14 of 17; N = 6: 30 of 34. The seven exceptions are (N, M, k) = (5, 5, 2), (5, 6, 2), (5, 7, 3), (6, 6, 2), (6, 7, 2), (6, 10, 3), (6, 11, 4); in five of them t decreases with θ (Gibbs fastest). Ten of the 57 gains at birth are below 10⁻³, and five of the seven exceptions are among them: **for a gain of at least 10⁻³, G\* is slower in 45 cases out of 47**. The "G\* does not gain" group consists, in 43 cases out of 45, of exact TV ties at birth (corollary D1 of DEFI-M8).

**Reading [CERT].** On these small graphs, "being born right slows the bridge" is not an accident of DEFI-M8's eight cases: it holds in 50 of the 57 cases where G\* beats uniform at birth (88%). It is not a law: seven exceptions, including dense sectors.

**Cross-check.** Second implementation with no shared code (`defi_m11_carte_second_moteur.py`, networkx and dense matrices) on the 42 cases with at most 6 vertices: same swap counts in all 210 comparisons, TV at birth identical to 3.3·10⁻¹⁶.

## 3. Result B — beyond enumeration [M]

Total variation over the whole configuration can no longer be computed beyond 7 vertices. We therefore follow three **observables** after birth: T_v (triangles containing the newborn), T (triangles of the graph) and D (degree dispersion), compared with their equilibrium law under π_{N+1,M+k}. Fixed-density sector: M = 2N − 2, k = 4, so M + k = 2(N + 1) and mean degree 4 before and after birth; the newborn is born with the mean degree. N = 8, 12, 16, 24, 32, 48 (main campaign: 2,000 births per θ, parents drawn from π_{N,M} by a Metropolis chain, one parent every 20 sweeps), then N = 48 and 64 for θ = 0 and 1 (long campaign: 600 births, up to 2,000 sweeps; same starting seed as the main campaign at N = 48, hence partially dependent). `numba` engine (`defi_m11_monte_carlo.py`).

**B1. Global observables quickly forget the attachment law, but not entirely the slow mode.** At birth, G\* is closer to equilibrium (reduced deviation of T: +0.09 to −0.29 depending on N, against −0.24 to −1.20 for the other θ). In the main campaign (N = 8 to 48), after 4 sweeps the reduced deviations of T and D lie between −0.18 and +0.02 for all θ; after 16 sweeps, between −0.07 and +0.06. For these observables no order "anti-Gibbs < uniform < Gibbs" appears: when a difference shows, G\* is the closest. In the long campaign, T keeps a deviation of −0.11 to −0.15 after 16 sweeps at N = 64: global observables also inherit, at low amplitude, the slow mode described in B2.

**B2. The newborn's triangles reach equilibrium more and more slowly.** The criterion planned in the script (deviation ≤ 0.1 standard deviation, field `critere` of the JSON) is not reached in 300 sweeps at N = 48; it was replaced **after the fact** by a half-time t½: the first time at which the deviation of the mean of T_v from equilibrium falls below half its value at birth (`defi_m11_demi_temps.py`). t½ only measures the decay of a mean: it is a lower bound on the order of the mixing time, not the mixing time.

| N | 8 | 12 | 16 | 24 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|---|
| t½ (sweeps), θ = 0 | 0.5 | 2.7 | 7.5 | 22.9 | 46.8 | 138.6 (147.3) | 442.0 |
| t½, range over the five θ | 0.3–0.6 | 1.3–3.2 | 4.7–7.5 | 22.8–23.8 | 39.2–58.2 | 138.6–158.7 | 442.0–448.4 (θ = 0 and 1) |

In brackets: long campaign (600 births). From N = 12 to 64, t½ is multiplied by about 160 while N is multiplied by 5.3. A power-law fit (N ≥ 12, all θ) gives an exponent of 3.0 (2.75 to 3.47 depending on θ); the local slopes at θ = 0 are 3.6, 2.8, 2.5, 2.7 and 4.0, and on N ≥ 24 an exponential growth in N fits better than a power law. **The growth is at least of order N³ sweeps over 8 ≤ N ≤ 64; faster, possibly exponential, growth is not excluded.** The exponent varies little with the threshold (2.8 to 3.3 for 3/4, 1/2 or 1/4 of the initial deviation, according to the reviewer).

Within the family G_θ, θ ∈ [−1, 1], at k = 4, the attachment law changes this time little from N = 24 on: the range across θ, relative to the smallest t½, is 4% at N = 24 and 15% at N = 48, within sampling noise (± 13 to ± 20% according to the reviewer), but 48% at N = 32, where θ = 1 is slowest, beyond noise. This is no surprise: a newborn with four edges has at most six triangles, whereas at equilibrium **87% (N = 16) to 97% (N = 64) of the mean of T_v is carried by vertices with more than six** (19 to 39% of the vertices; `defi_m11_queue_aristocratique.py`). No law of this family places the newborn in that aristocracy: t½ measures accession to the aristocracy, a property of the swap chain more than of the birth kernel. With an absolute threshold (deviation ≤ 0.25 standard deviation), G\* remains markedly faster at small N (N = 16: 2.0 sweeps against 17.8 for θ = −1, according to the reviewer).

**Checks.**
- Validation against exact computation (`defi_m11_validation.py`): on the enumerable sector N = 6, M = 10, k = 4 (same density), the Monte Carlo reproduces the exact expectations of T_v, T and D at ten times and for the five θ (6,000 births; largest deviation 2.5 standard errors over 150 comparisons); equilibrium means within 0.007 standard deviation.
- Equilibrium (`defi_m11_diagnostic_equilibre.py`): four independent chains per size, compared over two halves of their trajectory; their means of T and D (hence of the vertex-average of T_v, 3T/(N + 1)) differ by at most 0.22 standard deviation of the observable; acceptance rate 0.31 to 0.41. This check concerns global means, not mixing at the level of one vertex.
- Second independent implementation (`defi_m11_second_monte_carlo.py`, pure Python, standard-library generator, θ = 0; independent code, same experimental design): t½ = 2.3, 5.1 and 21.6 sweeps at N = 12, 16, 24 (against 2.7, 7.5 and 22.9), an exponent of 3.2 between N = 12 and 24.
- The reviewer's independent campaign (own code, θ = 0, 2,000 births, parent spacings from 20 to 300 sweeps): t½ = 7.0 to 8.0 (N = 16), 22.0 to 26.1 (N = 24), 45.6 to 48.2 (N = 32), 148.1 to 164.7 (N = 48); autocorrelation between successive births between −0.05 and +0.04; no bias from parent spacing.

## 4. Reading

- **[CERT]** For total variation over the whole configuration, and up to 7 vertices, the most faithful birth almost always slows the bridge (50 cases out of 57; 45 out of 47 when its gain exceeds 10⁻³) and anti-Gibbs birth most often speeds it up (44 out of 57).
- **[M]** For the observables followed, from N = 8 to 64, the attachment law of the family G_θ only matters during the first sweeps. The two results do not contradict each other: they measure different things (the whole labelled configuration versus three projections), at different sizes.
- **[M], the most important point for RO-25**: on abstract graphs, the time a newborn takes to acquire the equilibrium triangle mass grows at least like N³ sweeps between N = 8 and 64, and the family of attachment laws tried changes it only little (beyond noise only at N = 32), because that mass is carried by an aristocracy of vertices which the newborn must join through swaps. Should this growth be confirmed, the separation of time scales required by the growth → Gibbs bridge (relaxing between two births) would cost at least of order N⁴ swaps per birth for this observable.
- To be compared, with reservations, with the slow tail observed on the canonical engine in DEFI-M9; but the canonical engine does not, to date, show growth of this time with N (the role of N there is [OPEN], DEFI-M10), and its massive decile is partly fixed by the geometry of the cloud, a different mechanism from an aristocracy among exchangeable vertices.
- **[H]** Untested mechanism: the measure π ∝ exp(N·S_sim/τ) cools as N grows, which would rather suggest Arrhenius-type (exponential) growth than a power law.
- None of this refutes RO-25: the time remains finite at finite N, the measurement is on abstract graphs and not on the canonical engine, and other observables, other relaxation kernels or other birth laws (outside the family G_θ, or with variable k) might behave differently.

## 5. What is established, what remains to be checked, the weakest point

- **Established:** the exact map (102 cases, cross-checked on 42); the Monte Carlo measurements of B1 and B2, validated against exact computation at N = 6 and cross-checked by a second implementation (N = 12, 16, 24) and by the reviewer's independent campaign (N = 16 to 48).
- **To be checked:** everything, by a person; the form of the growth (power or exponential) beyond N = 64; other densities and other k; the canonical (Rips) engine, where swaps are restricted to geometric neighbours; mixing at the level of one vertex in the equilibrium chain (the equilibrium checks only concern global means, and the N = 6 validation contains no aristocracy).
- **Hostile review (second AI agent):** three substantive corrections accepted — citing DEFI-M10 as a measurement was wrong (DEFI-M10 is open), the "N³" law became "at least of order N³, possibly exponential", and the insensitivity to the attachment law is restricted to the family G_θ at k = 4, with its reason (the aristocracy). Minor corrections: t½ criterion declared as post hoc, partial dependence of the two campaigns, scope of B1, composition of the "G\* does not gain" group.
- **Weakest point:** the form and exponent of the growth rest on seven sizes, a single density sector, a single observable (the mean of T_v) and a criterion chosen after the fact; the gap between the two implementations reaches 32% at N = 16 (5.1 against 7.5).

## 6. Next step on the proof path (P1)

**DEFI-M12 — The aristocratic slowness.** Does the time for a newborn to reach the equilibrium triangle mass grow like a power of N or exponentially? Prove a bound (spectral gap of the single-vertex process, bottleneck) or measure it up to N ≥ 128 on abstract graphs, at several densities, and on the canonical engine. Confirmed growth makes the RO-25 bridge costly for massive vertices; saturation makes it practicable.

## Reproduce

```bash
cd contributions/RO-25_pilote-ia
python3 defi_m11_carte_exacte.py            # ≈ 36 min, writes defi_m11_carte.json
python3 defi_m11_carte_second_moteur.py     # ≈ 20 min, cross-check N ≤ 5
python3 defi_m11_carte_analyse.py           # writes defi_m11_carte_analyse.json
pip install numba                           # 0.68.0
python3 defi_m11_validation.py              # ≈ 30 s
python3 defi_m11_monte_carlo.py             # ≈ 3 min, writes defi_m11_monte_carlo.json
python3 defi_m11_monte_carlo.py --tailles 48,64 --thetas 0,1 --R 600 --balayages-max 2000 --sortie defi_m11_monte_carlo_long.json
python3 defi_m11_diagnostic_equilibre.py    # ≈ 5 s
python3 defi_m11_second_monte_carlo.py      # ≈ 10 min, pure Python
python3 defi_m11_demi_temps.py
python3 defi_m11_queue_aristocratique.py    # ≈ 1 min
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, networkx 3.7, numba 0.68.0. Seeds are fixed in the scripts; the same script replayed on another machine may differ at the level of statistical noise (numba). Screen outputs: `defi_m11_*_sortie.txt`.
