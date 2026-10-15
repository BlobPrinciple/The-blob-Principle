🇫🇷 [Version française](DEFI-M7_RAPPORT.md) · 🇬🇧 English

*Translated with DeepL and corrected by the pilot; the French original prevails.*

# DEFI-M7 — The cost of the growth → Gibbs bridge on the canonical engine

*Contribution by the laboratory's AI pilot (Claude, Anthropic), 15 October 2026. Direct follow-up to advance no. 2 ([REPORT_EN.md](REPORT_EN.md), issue #16). Not reviewed by a person.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. No change of status.

## 1. Question

After the birth of a vertex (one mitosis edge and closure edges), how many Metropolis exchanges per edge are needed for the newborn to become indistinguishable from a typical vertex? Does this cost stay bounded as N grows? On abstract graphs, advance no. 2 gave 2.5 to 4.7 exchanges per edge for N = 5 to 7.

## 2. Protocol (fixed before execution)

- **Engine**: `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py`, imported as is, frozen canonical parameters (κ = 6.6; β = 0.30; τ = 0.50; pool factor 1.6; τ_eff = τ/N; thermalisation 120 N steps). Unlike advance no. 2, the Rips geometric constraint is **present** here.
- **Birth**: a new uniform point in the cube, linked to its k nearest neighbours, k (3 or 4) chosen to keep |E| = round(κ(N+1)/2); its pairs at distance < 1.6 r join the pool; r stays that of N₀. **[H-loc]** This attachment law is posited, not derived (the subject of DEFI-M8).
- **Measurement**: degree and incident triangles of the newborn at lags t = 0 to 512 sweeps (1 sweep = |E| exchange attempts), compared with the mean over all vertices at the same moment; mean gap and standard error over all births and seeds.
- **Plan**: N₀ = 250, 500, 1,000, 2,000 (4 seeds, 20 to 25 successive births per seed) and 4,000 (3 seeds, 12 births).
- **Preliminary check**: is the engine's working point stationary? The `build_blob` chain was extended to 2,520 N steps (21 times the canonical thermalisation) for N = 500, 1,000 and 2,000.

## 3. Results

### 3.1 The working point is stationary at the level of global observables [M]

Over 3 seeds × 3 sizes, n_tri/N, CV(degrees) and Gini(mass) do not drift between 120 N and 2,520 N steps: their variations stay within each seed's fluctuations (for example N = 2,000, seed 1: n_tri/N = 5.146 → 5.137; CV = 0.876 → 0.881). The differences **between** seeds (N = 1,000: n_tri/N from 5.05 to 6.04) persist throughout: they reflect the quenched disorder of the positions (each seed draws its own point cloud, hence its own measure π), not a thermalisation failure. File: `defi_m7_stationnarite.json`.

### 3.2 The newborn's degree relaxes in 8 to 16 sweeps, with no growth in N [M]

Mean gap newborn − population, degree (population: 6.6):

| N₀ | t = 0 | t = 4 | t = 8 | t = 16 | t = 512 | t_relax (gap < 2 standard errors) |
|---|---|---|---|---|---|---|
| 250 | −3.28 ± 0.05 | −1.31 ± 0.33 | −0.70 ± 0.44 | −0.52 ± 0.51 | −0.40 ± 0.51 | 8 |
| 500 | −3.32 ± 0.05 | −1.26 ± 0.31 | −0.49 ± 0.40 | −0.36 ± 0.48 | −0.21 ± 0.50 | 8 |
| 1,000 | −3.32 ± 0.05 | −1.17 ± 0.31 | −0.88 ± 0.41 | −0.48 ± 0.42 | −0.48 ± 0.49 | 16 |
| 2,000 | −3.30 ± 0.05 | −1.34 ± 0.38 | −0.68 ± 0.47 | −0.33 ± 0.58 | −0.36 ± 0.61 | 8 |
| 4,000 | −3.27 ± 0.08 | −0.99 ± 0.49 | −0.99 ± 0.58 | −0.63 ± 0.65 | −0.43 ± 0.79 | 8 |

The relaxation time **per edge** does not grow from N = 250 to N = 4,000 (8 to 16 sweeps). Direct consequence: the cost of a birth, in exchange attempts, is of order 10 |E|, hence **proportional to N**; growing the Blob from N₀ to N while keeping the conditional law close to π costs of order N² attempts. The bridge is workable, at the price of a quadratic global effort.

### 3.3 The newborn's triangles: unresolved [M][OPEN]

Mean gap in incident triangles (population: 15.3 to 16.2):

| N₀ | t = 0 | t = 8 | t = 16 | t = 64 | t = 512 |
|---|---|---|---|---|---|
| 250 | −14.9 ± 0.2 | −6.6 ± 2.8 | −3.2 ± 3.8 | −3.1 ± 3.6 | −2.5 ± 3.8 |
| 500 | −14.4 ± 0.1 | −7.2 ± 2.0 | −4.6 ± 3.0 | −4.9 ± 2.8 | −3.2 ± 3.3 |
| 1,000 | −15.2 ± 0.2 | −8.0 ± 2.8 | −6.3 ± 3.2 | −5.0 ± 3.6 | −3.6 ± 3.8 |
| 2,000 | −14.2 ± 0.1 | −6.4 ± 2.8 | −2.5 ± 4.4 | −1.9 ± 4.7 | −2.0 ± 4.8 |
| 4,000 | −14.6 ± 0.2 | −9.0 ± 3.9 | −6.5 ± 4.9 | −5.1 ± 6.3 | −3.6 ± 6.2 |

The deficit falls below 2 standard errors at around 16 sweeps, but the standard errors are large because the triangle mass is highly concentrated (Gini ≈ 0.86: a few vertices carry many triangles). Pooling all sizes, the gap at 512 sweeps is about −3.0 ± 2.0: **compatible with zero at 1.5 standard errors, but also with a lasting deficit** (a newborn that never reaches the status of the massive vertices). These data cannot settle it.

## 4. What is established, what remains to be checked, the weakest point

- **Established [M]**: stationarity of the global observables over 21 times the canonical thermalisation; relaxation of the degree in 8 to 16 sweeps, with no growth from N = 250 to 4,000; global cost of a birth proportional to N.
- **Not established [OPEN]**: the relaxation of the newborn's triangle mass; a proven bound (spectral gap); the dependence on the attachment law.
- **Weakest point**: the observable. Comparing means is a necessary, not a sufficient, criterion; one should compare laws (total variation on the histogram of incident triangles), with many more births.

## 5. Proposed effect and next step

- DEFI-M7 stays **open**, with a partial result recorded: bounded cost per edge for the degree in the measured range.
- **Derived challenge DEFI-M9**: does the newborn ever reach the typical triangle mass, or does viability freeze an aristocracy of massive vertices? Deliverable: law of the newborn's incident triangles versus the population's, in total variation, with at least 200 births per size.

## Reproduce

```bash
pip install numba            # optional, speeds up the engine; without numba, reduce the plan
python3 contributions/RO-25_pilote-ia/defi_m7_stationnarite.py   # ≈ 15 s with numba
python3 contributions/RO-25_pilote-ia/defi_m7_cout_du_pont.py    # ≈ 6 min with numba
```

Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Outputs: `defi_m7_resultats.json`, `defi_m7_stationnarite.json`.
