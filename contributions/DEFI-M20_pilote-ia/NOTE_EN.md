# DEFI-M20 (RO-08), "κ ≥ 8" strand — the aristocracy and the local obstacle survive a larger mean degree

> **Status unchanged: TOE demonstrated NO · physical gates 0/7 · level 1.** Contribution of the laboratory's AI pilot (Claude, Anthropic), by delegation of Rudolphe Mirante, 27 November 2026. Challenge: [DEFI-M20](https://github.com/BlobPrinciple/The-blob-Principle/issues/56), third possible deliverable ("the measurement of the local conditions under a variant of A_Gibbs with κ ≥ 8"). Starting point, not redone: `contributions/RO-08_pilote-ia/NOTE_EN.md`. French version, which prevails: [NOTE.md](NOTE.md).

## Purpose

At κ = 6.6, Walkup's bound excludes outright that the A_Gibbs graph be the 1-skeleton of a connected closed 3-manifold (RO-08, Result 1). That lock is arithmetic: it falls as soon as κ ≥ 8 − 20/N. The question is whether the **local** obstacle (aristocracy of triangles, violations of the link conditions) was only an effect of the small mean degree. We change κ alone in the engine and measure.

**Criterion and predictions publicly filed before the measurement**: [issue #56, comment of 2026-11-27](https://github.com/BlobPrinciple/The-blob-Principle/issues/56#issuecomment-7213958737).

## Result in brief

1. **[M] The aristocracy is kept at every κ tested (6.6 to 14), by the filed criterion.** Gini of triangles per vertex: Blob 0.73 to 0.88 against RGG 0.34 to 0.48; share of triangles carried by the top decile: Blob 0.68 to 0.88 against 0.23 to 0.32. The Blob − RGG gaps are at least 0.37 (Gini) and 0.43 (decile) at every κ and N, at least four times the 0.10 threshold. The aristocracy weakens slowly as κ grows (Gini 0.877 → 0.747 at N = 4,000) and the gap to the control narrows (A10: 0.58 → 0.46 at N = 4,000, κ = 6.6 to 14); nothing is extrapolated beyond κ = 14.
2. **[M] The local obstacle does not move with κ; without viability, it recedes.** Fraction of vertices violating (C1), (C2) or (C3): Blob 0.972 to 0.981 at every κ and N; RGG 0.92 → 0.47 from κ = 6.6 to 14 (N = 4,000). At vertex level, (C3) alone carries all the Blob's violations: in all 15 rows, the fraction of vertices touching an edge with fewer than 3 common neighbours equals V (97 to 98 %, at every κ, against 45 % for the RGG at κ = 14); (C2) comes on top (0.78 → 0.91, rising with κ; RGG 0.78 → 0.24). Prediction "obstacle persists": verified by the criterion; "carried mostly by (C3)": verified qualitatively, outside any numerical criterion.
3. **[M] At κ ≥ 12, viability loses triangles relative to its own starting state; from κ = 10 on, the global condition is sometimes violated.** The RGG is exactly the initial state of the Blob chain (same points, same edges, `_rips`). At N = 4,000: n_tri/N = 5.23 (Blob) against 3.60 (RGG) at κ = 6.6, 8.47 against 8.32 at κ = 10, but 10.36 against 12.02 at κ = 12 and 12.04 against 16.42 at κ = 14. The necessary global condition n_tri/N ≥ κ − 2 (sum of (C2), [T]) is violated by 1 Blob configuration out of 12 at κ = 10, 2 out of 12 at κ = 12 and 2 out of 12 at κ = 14. This counting exclusion is redundant (the global condition is the sum of (C2), and every Blob configuration is already excluded locally), but it shows that viability no longer even creates enough triangles in total.

**Verdict.** Raising κ lifts Walkup's arithmetic lock but not the obstacle: under the variant with κ alone changed (canonical β, τ, therm_fac), the graph stays aristocratic and almost all its vertices remain incompatible with a 2-sphere link. From an identical initial state, it is the viability chain (in this setting and for this duration), not the small degree, that takes the graph away from a triangulation; the control without viability gets closer as κ grows. RO-08 stays open; DEFI-M20 stays open (completion algorithm and cost per vertex not addressed). No status change.

## Variant and protocol

- Canonical engine `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py` imported as is; `build_blob(N, seed, kappa=κ)` with β = 0.30, τ = 0.50, pool_fac = 1.6, therm_fac = 120 unchanged. **This is not canonical A_Gibbs**: it is a variant with κ alone changed; the initial edges (the round(κN/2) shortest pairs of the pool of radius 1.6 r) and the pool follow κ (`_rips`).
- Control `build_rgg` at the same κ (same |E|, no viability).
- κ ∈ {6.6; 8; 10; 12; 14}; N ∈ {1,000; 2,000; 4,000}; seeds 0 to 3; 120 configurations.
- Necessary conditions [T] from RO-08: (C1) deg ≥ 4; (C2) t_v ≥ 3 deg − 6; (C3) at least 3 common neighbours per edge; (Glob) n_tri/N ≥ κ − 2.
- κ = 14 is the mean degree of the Freudenthal–Kuhn seed of T³, RO-08's positive control (zero violation).

## Measurements (means over 4 seeds)

| κ | N | Blob V | C1 | C2 | C3 (edges) | G | A10 | Z | n_tri/N (threshold κ − 2) | RGG V | RGG G | RGG A10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6.6 | 1,000 | 0.972 | 0.277 | 0.772 | 0.640 | 0.871 | 0.860 | 0.283 | 5.38 (4.60) | 0.906 | 0.478 | 0.316 |
| 6.6 | 2,000 | 0.975 | 0.274 | 0.772 | 0.645 | 0.865 | 0.852 | 0.291 | 5.04 (4.60) | 0.916 | 0.460 | 0.299 |
| 6.6 | 4,000 | 0.975 | 0.273 | 0.776 | 0.649 | 0.877 | 0.877 | 0.310 | 5.23 (4.60) | 0.920 | 0.461 | 0.302 |
| 8 | 1,000 | 0.972 | 0.167 | 0.832 | 0.627 | 0.852 | 0.834 | 0.185 | 6.90 (6.00) | 0.844 | 0.447 | 0.299 |
| 8 | 2,000 | 0.972 | 0.166 | 0.819 | 0.621 | 0.847 | 0.826 | 0.195 | 6.60 (6.00) | 0.864 | 0.426 | 0.279 |
| 8 | 4,000 | 0.978 | 0.156 | 0.843 | 0.647 | 0.859 | 0.853 | 0.199 | 6.60 (6.00) | 0.870 | 0.425 | 0.280 |
| 10 | 1,000 | 0.976 | 0.081 | 0.877 | 0.597 | 0.819 | 0.797 | 0.092 | 9.12 (8.00) | 0.731 | 0.407 | 0.274 |
| 10 | 2,000 | 0.979 | 0.078 | 0.871 | 0.599 | 0.814 | 0.786 | 0.100 | 8.52 (8.00) | 0.745 | 0.389 | 0.258 |
| 10 | 4,000 | 0.981 | 0.070 | 0.886 | 0.629 | 0.828 | 0.809 | 0.103 | 8.47 (8.00) | 0.759 | 0.388 | 0.260 |
| 12 | 1,000 | 0.976 | 0.042 | 0.898 | 0.538 | 0.778 | 0.736 | 0.050 | 11.27 (10.00) | 0.581 | 0.384 | 0.261 |
| 12 | 2,000 | 0.977 | 0.044 | 0.879 | 0.547 | 0.775 | 0.724 | 0.055 | 10.39 (10.00) | 0.603 | 0.365 | 0.246 |
| 12 | 4,000 | 0.980 | 0.036 | 0.899 | 0.584 | 0.790 | 0.757 | 0.053 | 10.36 (10.00) | 0.618 | 0.361 | 0.245 |
| 14 | 1,000 | 0.974 | 0.024 | 0.891 | 0.472 | 0.732 | 0.677 | 0.028 | 13.27 (12.00) | 0.446 | 0.362 | 0.247 |
| 14 | 2,000 | 0.975 | 0.023 | 0.891 | 0.503 | 0.737 | 0.681 | 0.029 | 12.36 (12.00) | 0.461 | 0.342 | 0.233 |
| 14 | 4,000 | 0.981 | 0.019 | 0.905 | 0.532 | 0.747 | 0.696 | 0.030 | 12.04 (12.00) | 0.472 | 0.340 | 0.234 |

Source: `m20_kappa.json`, `m20_analyse_sortie.txt`. Values at κ = 6.6 reproduce RO-08 (same seeds).

Global condition per Blob configuration: violated at κ = 10 (N = 4,000 seed 2: 7.95 < 8), κ = 12 (N = 1,000 seed 0: 9.89; N = 4,000 seed 2: 9.76) and κ = 14 (N = 2,000 seed 0: 11.59; N = 4,000 seed 2: 11.06); never at κ ≤ 8. The RGG violates it in all its configurations at κ = 6.6 and 8 (3.66 and 5.41 on average over 12 configurations), never at κ ≥ 10.

**Supplement outside the criterion (cube core, vertices more than 2 r from the faces, N = 1,000 and 2,000):** the Blob stays at 0.92 to 1.00 of violating vertices; the RGG is violated about as much as over the whole cube (gap ≤ 0.04 either way). Not a boundary effect.

## Cross-check

`m20_second_moteur.py`: measurements redone with no shared code (sparse matrices; decile by `np.partition`; Gini by a rank form, algebraically identical to the engine's, so distinct code but not an independent method) on 40 configurations (κ, N, seed) at N = 1,000 and 2,000, for both models, and RGG rebuilt without the engine then compared edge by edge. **AGREEMENT**: 560 comparisons, maximum gap 2.2·10⁻¹⁶; rebuilt RGG identical edge by edge in all 40 configurations. Blob generation is not independent (same deterministic engine): only the measurements are.

## Limits

- Variant, not the canonical engine: β and τ are not recalibrated. [H] At fixed τ_eff = τ/N, the weight of one triangle relative to τ_eff is ≈ 2/(n_tri/N), ≈ 0.38 at κ = 6.6 and ≈ 0.17 at κ = 14: the chain becomes more entropic as κ grows, the likely explanation of point 3, not tested here.
- therm_fac = 120 gives about 17 attempts per edge at κ = 14 against 36 at κ = 6.6; no long relaxation at κ ≥ 8.
- Degree cap CAP = 96 not reached (maximum degree 76).
- Necessary conditions only. For T³, the Novik–Swartz bound requires κ ≥ 8 + 40/N: κ = 8 exactly stays globally excluded for T³.
- 4 seeds per point; seed-to-seed standard deviation ≤ 0.01 for V; up to 0.04 (G) and 0.07 (A10) at N = 1,000.

## Open question

[OPEN] Is there a setting (κ, β, τ) of the viability measure that keeps its properties (aristocracy, web, persistence) **and** satisfies the local link conditions, or is the aristocracy incompatible by nature with the 1-skeleton of a 3-manifold?

## Reproduce

```
pip install numba
python3 contributions/DEFI-M20_pilote-ia/m20_kappa.py          # ≈ 14 min on 2 cores
python3 contributions/DEFI-M20_pilote-ia/m20_analyse.py
python3 contributions/DEFI-M20_pilote-ia/m20_second_moteur.py  # ≈ 4 min; last line ACCORD
```
