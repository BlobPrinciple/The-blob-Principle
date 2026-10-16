🇫🇷 [Français](DEFI-M9_RAPPORT.md) · 🇬🇧 English

# DEFI-M9 — The aristocracy of massive vertices: largely shared across chains, slow to join

*Contribution from the laboratory's AI pilot (Claude, Anthropic), 16 October 2026. Follow-up to advance no. 3 ([DEFI-M7_REPORT_EN.md](DEFI-M7_REPORT_EN.md), issue #17). Reviewed by a second AI agent, a hostile reviewer who did not produce it; its objections have been incorporated (§3.3, §4). Not reviewed by a person. Translated with DeepL, then terminology corrected. The French version is authoritative.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. No status change.

## 1. Question

The growth → Gibbs bridge (RO-25) requires that a vertex born by growth become indistinguishable from a vertex drawn under π_N (armature V347.1, p. 11, RO-25: "the conditional law at fixed N reproduces, or derives, the measure π_N of A_Gibbs"). DEFI-M7 left an open point: the newborn's triangle mass remained in mean deficit (−3.0 ± 2.0 at 512 sweeps, [DEFI-M7_REPORT_EN.md](DEFI-M7_REPORT_EN.md) §3.3). DEFI-M9 asks whether this deficit is absorbed, or whether viability freezes an aristocracy of massive vertices.

## 2. Protocol (fixed before execution)

- **Engine**: `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py`, imported as is; frozen canonical parameters (κ = 6.6; β = 0.30; τ = 0.50; pool factor 1.6; τ_eff = τ/N; thermalisation 120 N steps).
- **Birth**: the DEFI-M7 law, unchanged: a uniform point in the cube, connected to its k nearest neighbours (k = 3 or 4, to keep |E| = round(κ(N+1)/2)); its pairs at distance < 1.6 r enter the pool; r stays that of N₀. **[H-loc]** (locality hypothesis, [H] in the armature's sense): this law is posited, not derived (subject of DEFI-M8).
- **Observable**: the law, no longer the mean. For the newborn's mass x (incident triangles), we compute its relative rank u = (#{others < x} + U·#{others = x}) / (N − 1), with U uniform to break ties. **[H]** If the chain reaches a unique stationary law, the newborn is exchangeable there with the other vertices (uniform position, same pool rule at radius r(N₀)), so u follows the uniform law. Two caveats: this stationary law is not exactly ∝ exp(S/τ_eff) (the deg ≤ 2 guard, the 40 tries and the pair disjoint from {u, v} break detailed balance), and it is not the canonical π_N, which would use r(N). The same u is computed for a **control vertex** drawn at random among the original vertices: it gives the statistical floor at equal sample size.
- **Plan**: N₀ = 250, 500, 1,000, 2,000; 10 seeds × 20 successive births = **200 births per size**; lags t = 0, 16, 64, 256, 1,024, 2,048 sweeps (1 sweep = |E| attempts).
- **Statistics**: mean of u (0.5 expected); total variation over 10 classes of u against the uniform law (TV₁₀); Kolmogorov–Smirnov test; share of u > 0.9 (0.1 expected).
- **Freezing checks** (added after reading the birth results, and declared as such): on the stationary chain without births, persistence of the top mass decile over 4,096 sweeps; then three chains on the **same point cloud**: A from the canonical start (shortest pairs), B from a random start (pool pairs drawn at random) with another Metropolis seed, and C, a control added at the reviewer's request, from the same start as A with another seed; compared after 4,096 sweeps. We also record the share of the decile near the faces of the cube and its overlap with the pool-degree decile.

## 3. Results

### 3.1 The body of the law is no longer distinguishable from the population's after 16 to 256 sweeps [M]

Mean relative rank u of the newborn (± standard error), Kolmogorov–Smirnov p-value, and TV₁₀; in brackets, the control.

| N₀ | t = 0 | t = 16 | t = 256 | t = 2,048 |
|---|---|---|---|---|
| 250 | 0.370 ± 0.013; p = 7·10⁻¹⁵; TV 0.28 (0.085) | 0.439 ± 0.020; p = 0.021; TV 0.12 | 0.463 ± 0.020; p = 0.16; TV 0.08 | 0.488 ± 0.020; p = 0.71; TV 0.065 (0.085) |
| 500 | 0.374 ± 0.015; p = 4·10⁻¹³; TV 0.27 (0.12) | 0.494 ± 0.019; p = 0.54; TV 0.12 | 0.492 ± 0.019; p = 0.59; TV 0.08 | 0.506 ± 0.020; p = 0.78; TV 0.10 (0.06) |
| 1,000 | 0.370 ± 0.015; p = 8·10⁻¹²; TV 0.26 (0.10) | 0.507 ± 0.019; p = 0.33; TV 0.095 | 0.480 ± 0.019; p = 0.20; TV 0.09 | 0.518 ± 0.019; p = 0.62; TV 0.095 (0.07) |
| 2,000 | 0.362 ± 0.015; p = 1·10⁻¹²; TV 0.25 (0.06) | 0.487 ± 0.020; p = 0.63; TV 0.105 | 0.485 ± 0.020; p = 0.79; TV 0.08 | 0.518 ± 0.019; p = 0.15; TV 0.10 (0.065) |

At birth, the newborn's law is clearly shifted downwards (TV₁₀ ≈ 0.26). From 16 sweeps for N₀ ≥ 500, and around 256 sweeps for N₀ = 250, it is no longer distinguishable from the uniform law **at 200 births**: TV₁₀ falls back to the control's level (0.05 to 0.135 for 200 draws). A non-rejection is not a convergence: the control itself gives p = 0.011 once (N₀ = 2,000, t = 64). This time does not grow from N₀ = 250 to N₀ = 2,000.

### 3.2 The massive tail is joined slowly [M]

All sizes pooled (800 births):

| t (sweeps) | 0 | 16 | 64 | 256 | 1,024 | 2,048 |
|---|---|---|---|---|---|---|
| newborns in the top decile (u > 0.9) | 0.000 | 0.0625 | 0.070 | 0.0725 | 0.0725 | 0.085 |
| controls in the top decile | 0.105 | 0.103 | 0.108 | 0.106 | 0.110 | 0.099 |
| binomial p (newborns against 0.1) | 4·10⁻³⁷ | 2·10⁻⁴ | 0.004 | 0.008 | 0.008 | 0.175 |
| mean mass gap newborn − population (weighted) | −14.4 ± 0.05 | −5.8 ± 1.2 | −4.9 ± 1.2 | −4.3 ± 1.3 | −4.0 ± 1.3 | −3.2 ± 1.3 |

The body of the law is no longer distinguishable; the tail is: up to 1,024 sweeps, newborns enter the massive decile less often than chance (6 to 7% against 10%, p from 2·10⁻⁴ to 0.008), and it is these vertices that carry the mean (mass Gini ≈ 0.854, engine header; [DEFI-M7_REPORT_EN.md](DEFI-M7_REPORT_EN.md) §3.3). At 2,048 sweeps, the share reaches 8.5%, with no significant gap to 10% (p = 0.175), but the mean gap remains −3.2 ± 1.3. The six lags bear on the same births: these p-values are not independent.

The mean deficit recorded by DEFI-M7 is therefore real, but it is not a global deficit: it is concentrated in the upper tail, which fills slowly.

### 3.3 The massive decile is largely shared between independent chains [M, partial]

- **Stationary chain** (N = 500 and 2,000, 3 seeds each): the Spearman rank correlation between each vertex's mass at t₀ and at t₀ + t falls to 0.34–0.54 within 16 sweeps and stays there up to 4,096; but **72% to 88%** of the vertices in the top decile at t₀ are still there after 4,096 sweeps (10% if the decile were renewed at random among all vertices; of the order of 15% to 25% if it were renewed at random among the vertices far from the boundaries only, which the decile mostly occupies, see below). On one cloud at N = 250, the reviewer observed a persistence of 0.96 at 1,024 sweeps that fell to 0.36 at 4,096: the decile is not frozen at every size.
- **Three chains, same cloud** (10 clouds, N = 250, 500, 2,000; `defi_m9_deux_chaines.json`), after 4,096 sweeps:

| N | cloud | persistence of A | overlap A–B (other start) | overlap A–C (same start) |
|---|---|---|---|---|
| 250 | 300 / 301 / 302 | 0.80 / 0.92 / 0.85 | 0.88 / 0.88 / 0.92 | 0.76 / 0.88 / 0.88 |
| 500 | 300 / 301 / 302 / 303 | 0.86 / 0.64 / 0.78 / 0.80 | **0.56** / 0.72 / 0.96 / 0.92 | **0.96** / 0.74 / 0.90 / 0.92 |
| 2,000 | 300 / 301 / 302 | 0.82 / 0.75 / 0.75 | 0.95 / 0.81 / 0.80 | 0.955 / 0.84 / 0.79 |

On 9 clouds out of 10, two chains from different starts designate as many common massive vertices as two chains from the same start (A–B ≈ A–C, from 0.72 to 0.96): there, the decile is fixed by the cloud, not by the initial state. On cloud 300 at N = 500, A–B = 0.56 against A–C = 0.96: there, the decile keeps the memory of the initial state over 4,096 sweeps.

- **What "fixed by the cloud" covers**: the cube is not periodic, and the massive decile avoids the boundaries (share of vertices within r of a face: 45% to 78% of all vertices, 0% to 56% of the decile). The mass decile overlaps the pool-degree decile by 28% to 88% (the latter, an integer with many ties, contains 10.0% to 12.8% of the vertices, which slightly inflates this overlap). Part of this hierarchy is therefore a finite-box effect.

This check does not test age: in these chains, all vertices have the same age. It establishes that, on most clouds, the massive hierarchy is largely a property of the point cloud (positions, boundaries included) and not of the chain's history. That the newborn eventually reaches the mass its position assigns it is an **[H]**, not measured here: a first trial by the reviewer (N₀ = 500, 100 births, independent chain on the same cloud) gives a rank correlation of 0.235 between mass under growth and equilibrium mass, and does not settle it.

### 3.4 Cross-check by a second implementation of the same kernel [M]

`defi_m9_second_moteur.py` rewrites the model from its specification, without importing the corpus engine (dense adjacency matrix, triangles by diag(A³)/2, separate random generator). It is a cross-check of code, not of model: same author, same specification, same particularities of the proposal kernel. Working point recovered: n_tri/N = 5.02 and Gini(mass) = 0.821 at N = 250 (10 seeds), 5.38 and 0.853 at N = 500 (6 seeds), against 5.4 and 0.854 stated (engine header, N = 1,200); the reviewer measured the canonical engine at equal N: 5.29 and 0.830 (N = 250), 5.16 and 0.846 (N = 500), compatible given the spread between seeds (4.6 to 6.4).

- Births (120 at N₀ = 250, 72 at N₀ = 500): mean u 0.384 and 0.348 at t = 0; 0.485 and 0.528 at 256 sweeps; 0.485 and 0.455 at 2,048 sweeps (KS: p = 0.53 and 0.06). Share in the top decile at 2,048 sweeps: 8.3% and 9.7%. A table close to §3.1, noisier (u = 0.455, p = 0.06 at N₀ = 500); the sample size does not allow testing the tail.
- Two chains (N = 500, 4 clouds): overlap 0.87 to 0.96, persistence 0.72 to 0.96. Same reading as the 9 concordant clouds of §3.3 (control C was not rerun on this second code).

## 4. What is established, what is not, the weakest point

- **Measured [M]** (canonical engine, N₀ = 250 to 2,000, birth law [H-loc]): at 200 births per size, the body of the newborn's mass law is no longer distinguishable from the population's after 16 to 256 sweeps, with no growth with N; newborns enter the massive decile less often than chance up to at least 1,024 sweeps.
- **Measured, partial [M]**: on 9 clouds out of 10, the massive decile is largely shared by chains from different starts; it avoids the cube's boundaries.
- **Not established [OPEN]**: the role of age (birth order) in the hierarchy; the time needed for the newborns' share in the massive decile to reach 10%, and its dependence on N; any proven bound.
- **[H]** Reading for the cosmogony: on the canonical engine, a large part of the hierarchy of massive vertices is due to the point cloud (positions and boundaries). If Book I expects a hierarchy inherited from the genealogy, these measurements do not show it; nor do they exclude it.
- **Weak points**: (1) the birth law is posited [H-loc], and r stays that of N₀, so that 20 births add up to 8% of points at fixed radius for N₀ = 250 (1% for N₀ = 2,000); (2) the frozen disorder of positions and the non-periodic boundaries are properties of the Rips engine [ARCH], not necessarily of the Blob: this result may say more about A_Gibbs than about the cosmogony; (3) the freezing checks (§3.3) were added after reading the first results, and control C at the reviewer's request; (4) the main computation was interrupted during N₀ = 2,000 and resumed in two halves (seeds 0 to 4 and 5 to 9), with the same seeds, then merged (`defi_m9_fusion.py`); raw per-birth data are archived only for N₀ = 2,000; (5) the control is ranked in a population containing up to 19 recent newborns, still in deficit (slight upward bias); (6) no human review.

## 5. Proposed effect and next step

- DEFI-M9 stays **open**, with a partial result entered: the massive hierarchy is largely a property of the cloud; the newborn's time to reach the tail and the role of age remain open.
- The bridge cost estimated by DEFI-M7 (of the order of 10 |E| attempts per birth) holds for the body of the law; for the massive tail, it is at least of the order of 100 times higher (deficit still significant at 1,024 sweeps) and remains to be measured.
- **Derived challenge DEFI-M10 — the slow accession to the massive decile**: how many sweeps are needed for the newborns' share in the top decile to reach 10%, and does this time grow with N? Does the newborn reach the equilibrium mass of its position? Deliverable: share measured to ± 1 point (at least 1,000 births per size, at least two sizes) up to at least 16,384 sweeps, compared newborn by newborn with the equilibrium mass of its position (independent chain on the same cloud), preferably in a periodic box to remove the boundary effect; or a proven bound.

## Reproduce

See the [French version](DEFI-M9_RAPPORT.md#reproduire): identical commands. Python 3.13.16, numpy 2.5.3, scipy 1.18.1, numba 0.68.0.
