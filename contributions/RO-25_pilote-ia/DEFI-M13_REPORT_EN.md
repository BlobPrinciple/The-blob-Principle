🇬🇧 English · 🇫🇷 [Version française](DEFI-M13_RAPPORT.md)

# DEFI-M13 — The aristocracy barrier, measured: the free-energy profile of T_v at mean degree 4 and 6, and an open question on the asymptotics

*Contribution of the laboratory's AI pilot (Claude, Anthropic), 30 October 2026. Filed like any contribution, as an `ia-assistee` issue. Verified by the pilot (second implementation independent in engine code and in biasing algorithm, separate dynamical measurement) and reviewed by a second AI agent acting as hostile reviewer (see § 6); **no human review at this stage**.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It partially answers DEFI-M13 (RO-25, RO-20), on abstract graphs only; no bound is proven and the canonical engine is not addressed.

## 1. The question

DEFI-M13 (#42), opened by [DEFI-M12_REPORT_EN.md](DEFI-M12_REPORT_EN.md), § 7: on abstract graphs at mean degree 4, under π ∝ exp(n·S_sim/τ), the autocorrelation half-time t½ of T_v (triangles containing vertex v) grows as exp(0.96·√n) from n = 17 to 193, and the aristocracy is a dominant clique of size of order √n; at mean degree 6, growth is faster (about exp(a·n^0.6)). **Why √n, and why not at mean degree 6?** Deliverable: proof or refutation of an exp(Θ(√n)) barrier (bottleneck, conductance, free-energy argument), or a measured explanation.

Authoritative sources: armature V347.1, § II.0 (p. 10: strata A_gen and A_Gibbs, S_sim(C) = log(1 + n_tri(C)) − β·D(C); the two missing bridges, RO-25 and RO-08); RO-25 box (p. 11: a joint dynamics whose conditional law at fixed N reproduces or derives π_N); axioms A3–A4 [A][ARCH] (p. 18: β = 0.30; π_N ∝ exp(N·S_sim/τ), τ = 0.50); A0′ (p. 18: "under ergodicity, these weights govern the long-run empirical residence frequencies"; "persisting" is not defined by π_N > 0, RO-20). Computational frame unchanged since DEFI-M8 (hypothesis H-abs, [DEFI-M8_REPORT_EN.md](DEFI-M8_REPORT_EN.md), § 2): simple labelled abstract graphs, D = population standard deviation of degrees / mean degree, Metropolis edge swaps at fixed edge number M, λ = n/τ = 2n; one sweep is M swaps.

## 2. Method

**Idea.** DEFI-M12 measured a slowness; asking "why" requires the equilibrium law in the regions the dynamics rarely visits. Vertices being exchangeable, the law P(T) of T_v is the same for every v; F(T) = −log P(T) is the free-energy profile along the very observable whose autocorrelation DEFI-M12 measured. If the slowness is the activated crossing of a saddle of F, log t½ should follow the height of that saddle.

**Profile (`defi_m13_profil.py`).** Kernel of `defi_m12_lenteur.balayer` (same proposal, same S_sim), plus a bias exp(w(T_0)) on the triangle count of the tagged vertex 0; T_0 is updated at every swap. Support: [0, T_cap], T_cap = 1.15 × the maximal T_v observed in an unbiased chain started from a planted core, + 2. Wang–Landau (f from 1 to 10⁻⁵, flatness min H > 0.7 × mean over the whole support), then fixed-bias production (8 blocks of 5,000 sweeps) and reweighting, P ∝ H·exp(−w). Three repetitions per point (two at n = 257), distinct seeds. Exact checks at the end of each chain: n_tri = tr(A³)/6 and T_0 recomputed.

**Four estimators of the exit barrier B** (commoner minimum at T ≈ 0, aristocratic minimum in the upper half of the support, saddle = maximum of F between them): **raw** on integer values of T; **k** after grouping T into classes [C(k,2), C(k+1,2)) (F is strongly jagged: values T = C(k,2), those of a complete neighbourhood, are favoured); **smoothed** (5-bin moving average); **mfpt**, log of the mean first-passage time of a unit diffusion along T, from the aristocratic to the commoner minimum. None is a time: only their variation compares with that of log t½. The choice of estimator matters (§ 3.3); this is a limitation of the method, not a detail.

**Second implementation (`defi_m13_second_moteur.py`), independent in engine code and in biasing algorithm** (it reuses the first engine's support and mask, and the common analysis; one run per size). 64-bit-word neighbourhoods and popcount, T_0 fully recomputed after every proposal (no incremental update), batched PCG64 generator, start "clique of size 0.6·√(2M) containing vertex 0", the 1/t algorithm of Belardinelli and Pereyra (2007) instead of Wang–Landau; same support as the first engine (read from its JSON, never-reached bins excluded from the criterion). A first version (Berg multicanonical recursion) did not converge at n ≥ 129 (empty interior bins): abandoned, not retained.

**Separate dynamical measurement (`defi_m13_sorties.py`).** Unbiased chains (DEFI-M12 engine), two per size, from 16 t½ (n = 193) to 400 t½ (n = 25); a vertex is "aristocrat" above half the T of the aristocratic minimum, "commoner" below T = 2, with hysteresis in between; residence time = total time spent as aristocrat / number of exits. This is a dynamical quantity, which depends on the swap kernel; it is distinct from the stationary residence frequencies A0′ speaks of.

**Declared method deviations.** A first profile pass (final f 2·10⁻⁴, flatness 0.5, production 8 × 2,000 sweeps) gave, at n ≥ 129, barriers that were not reproducible between repetitions (up to 2 apart); it was replaced by the pass described above and is not kept. Two Wang–Landau defects were fixed during development (newly reached bin: bias inherited from the current bin; flatness required over the whole support, not only over visited bins). At n = 17 the flatness criterion is never met (inaccessible bins, e.g. T_v = 27 with 34 edges): all 17 stages hit the cap, with no visible effect on the profile (direct check, § 3.1). The truncated support can be exceeded by a free chain (observed T 46 against T_cap = 45 at n = 33, per the reviewer): negligible mass, but the support does not cover everything. The point n = 385 failed (one repetition out of two stuck in the aristocratic region during production): it is excluded from the analysis and kept in `defi_m13_profil_c2_grand.json`.

## 3. Results

### 3.1 The equilibrium law of T_v is bimodal, with a rising saddle [M]

At mean degree 4, for n ≥ 25, P(T_v) has two modes: commoners at T = 0 and the aristocracy around T ≈ C(k_ari, 2), separated by a jagged plateau. The class k_ari of the aristocratic minimum (5, 6, 7, 8, 9, 11, 12, 14.7 for n = 17 to 193) follows the largest clique measured by DEFI-M12 (5.5 to 14.8): the aristocratic mode corresponds, approximately, to membership of the dominant clique (a member of a clique of size q has T ≈ C(q − 1, 2), hence k ≈ q − 1, whereas k_ari ≈ q: the agreement is only approximate).

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 | 257 |
|---|---|---|---|---|---|---|---|---|---|
| ln t½ (DEFI-M12) | 2.22 | 3.07 | 3.77 | 4.99 | 5.96 | 7.74 | 9.19 | 11.63 | — |
| B raw | 0.55 | 0.70 | 0.86 | 1.73 | 2.65 | 5.07 | 7.37 | 11.01 | 16.37 |
| B k | 0.66 | 0.81 | 1.04 | 1.72 | 2.40 | 4.14 | 5.19 | 7.21 | 10.26 |
| B smoothed | 0.24 | 0.43 | 0.62 | 1.38 | 2.17 | 4.24 | 6.13 | 9.18 | 13.72 |
| mfpt | 4.94 | 5.62 | 6.14 | 7.23 | 8.17 | 10.21 | 12.03 | 15.41 | 19.91 |
| B raw, second engine | 0.57 | 0.59 | 0.79 | 1.89 | 2.69 | 5.14 | 7.50 | 11.68 | 16.14 |

Standard deviation between repetitions: ≤ 0.11 up to n = 65, 0.07 to 0.48 beyond (`defi_m13_analyse_sortie.txt`, table A).

**Cross-checks.** Profiles F of the two implementations, after recentring, on bins within 16 of the minimum: root-mean-square difference 0.06 to 0.16 up to n = 65, 0.15 to 0.44 from n = 97 to 193 (maximal difference 1.36); at n = 257, 1.16 to 1.43 (maximal difference 7.6) while the four barriers agree within 0.4 (first engine 16.37; 10.26; 13.72; 19.91 — second 16.14; 9.97; 13.72; 19.50). At small sizes (n ≤ 65), the direct histogram of an unbiased chain reproduces the profile (rms 0.08 to 0.19 on bins within 8 of the minimum; `defi_m13_analyse_sortie.txt`, B bis). **Third cross-check, by the reviewer**, with their own code (random start, PCG64, long unbiased chain, direct histogram over all vertices, 1.5 to 4·10⁶ sweeps): raw B 0.83; 1.73; 2.66; 5.04 at n = 33, 49, 65, 97, against 0.86; 1.73; 2.65; 5.07 here.

### 3.2 DEFI-M12's t½ follows the residence time in the aristocracy [M]

| n | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|
| exits counted (two chains) | 3,890 | 4,685 | 4,380 | 4,660 | 2,445 | 1,031 | 324 |
| mean residence (sweeps) | 40 | 72 | 216 | 582 | 3,698 | 16,301 | 181,848 |
| residence / t½ | 1.86 | 1.65 | 1.48 | 1.50 | 1.61 | 1.67 | 1.63 |

The ratio stays between 1.5 and 1.9 while the residence grows by a factor 4,500 (for exponentially distributed exits one would expect about 1/ln 2 ≈ 1.44 if t½ followed membership survival). The slowness measured by DEFI-M12 therefore follows, up to a roughly constant factor, the persistence of membership in the aristocracy. No error bars; at n = 193 each chain covers only about ten clique lifetimes and the 324 exits are correlated.

### 3.3 Saddle and slowness: same order of magnitude, non-linear relation [M]; shape of B [H]

- **Shape of B [H]: it depends on the range.** Over n = 33 to 257, the four estimators are better fitted by a straight line in n than in √n (residual sums of squares: raw 0.60 vs 5.14; mfpt 0.26 vs 3.01; free exponent 0.90 to 1.10). But this verdict rests on the point n = 257 (the most fragile, § 5) and on the onset of the saddle at small n: **over n = 65 to 193, B is compatible with √n** (raw 0.01 vs 0.21; k 0.04 vs 0.21; smoothed 0.00 vs 0.16; mfpt 0.04 vs 0.05; free exponent 0.56; 0.30; 0.54; 0.73), and the slope ΔB/Δ√n is roughly constant there (raw 1.36; 1.52; 1.44), before jumping to 2.51 on the single interval 193–257.
- **B against ln t½.** Fit ln t½ = a·B + b over n = 33 to 193: a = 0.745 (raw), 1.237 (k), 0.885 (smoothed), 0.840 (mfpt), largest residuals 0.26 to 0.52; the relation is concave (local slopes, raw 1.39 → 0.67; mfpt 1.13 → 0.72). An activated crossing of a single saddle along T_v, with a constant prefactor, would give a = 1; nothing guarantees a constant prefactor, and the mfpt contains an entropic term that grows with the support (4.94 at n = 17 for raw B 0.55): it is an order of magnitude. **T_v is only an approximate reaction coordinate**: the profile gives the order of magnitude and the trend, not a quantitative Arrhenius law.
- **At fixed n (n = 65), as λ grows.** λ = 66, 98, 130, 162, 194: raw B −0.07; 1.29; 2.65; 4.31; 6.19. At λ = 66 there is no saddle left (B ≈ 0): this is the regime where DEFI-M12 saw the aristocracy dissolve (setting c2T). Slopes over λ ≥ 98: dB/dλ = 0.051 (raw), 0.033 (k), 0.041 (smoothed), 0.040 (mfpt), against d ln t½/dλ = 0.031. Same finding: only the k grouping follows the dynamical slope.

### 3.4 The asymptotics remain open: the prediction at n = 257 depends on the calibration model [H]

Barriers can be measured where the dynamics no longer can. At n = 257, applied to the measured barriers (first engine), the ln t½ ↔ B relations calibrated on n = 33 to 193 give:

| calibration | raw | k | smoothed | mfpt |
|---|---|---|---|---|
| linear | 15.84 | 15.43 | 15.85 | 15.65 |
| slope of the last interval | 15.21 | 15.32 | 15.26 | 14.87 |
| quadratic | 13.58 | 14.94 | 13.72 | 13.88 |

DEFI-M12's law extrapolated gives 13.68 (t½ ≈ 8.7·10⁵ sweeps); the linear calibration, 15.1 to 15.9 (3.5 to 7.7·10⁶). The relation being concave, linear extrapolation overestimates by construction; the quadratic calibration is compatible with the √n law for three estimators out of four. These predictions are not independent (same data, same fits). **Conclusion: the profiles do not decide whether exp(0.96·√n) continues beyond n = 193.** Only a dynamical measurement at n = 257 (≈ 10⁷ sweeps of 514 swaps, out of reach in this session) will tell.

### 3.5 Mean degree 6: the saddle appears later [M], hence a larger effective exponent [H]

| n | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|
| ln t½ (DEFI-M12, c3) | 1.52 | 2.11 | 3.06 | 3.96 | 5.51 | 6.88 | 9.25 |
| B raw | −0.08 | −0.07 | 0.03 | 0.33 | 1.73 | 3.21 | 6.32 |
| B k | 0.01 | −0.15 | 0.20 | 0.63 | 2.06 | 3.20 | 5.40 |

At mean degree 6 there is no saddle up to n = 49 (the slightly negative values signal the absence of a distinct aristocratic minimum), while ln t½ already grows by 1.5 there: the slowness at small sizes is not activated. The saddle appears around n = 65 and then grows fast (raw ΔB = 3.1 from 129 to 193, against Δ ln t½ = 2.4). **[H]** The effective exponent γ ≈ 0.6 of DEFI-M12 (§ 3.2 of that report) would reflect this late crossover between a non-activated and an activated regime, rather than a law specific to this density.

## 4. Reading for the RO-25 bridge and for RO-20

- **[M]** DEFI-M12's aristocratic slowness is a membership persistence (§ 3.2) backed by a genuine equilibrium barrier in the law of T_v (§ 3.1), absent when λ is too low.
- **[H]** Over n = 65 to 193 the barrier is compatible with √n growth; the point n = 257 suggests an acceleration without establishing it (§ 3.3–3.4). Should growth faster than √n be confirmed, a growth → Gibbs bridge letting each newborn reach its equilibrium triangular mass before the next birth would be even less practicable than DEFI-M12 stated (§ 4 of that report): the interval between births would grow faster than exp(0.96·√n). Same caveat as then: RO-25 is not refuted; the armature's falsifier (p. 11) concerns the existence of a Markov extension, not its speed, and another relaxation kernel may mix faster.
- **[H] Towards RO-20.** A0′ (p. 18) links the weights of π_N to stationary residence frequencies, which say nothing about durations; the residence time in the dominant clique (§ 3.2) is a dynamical, kernel-dependent quantity. "Persisting", in the sense of a residence longer than the interval between two births, would be a criterion distinct from π > 0 and quantifiable for a given kernel; it remains to be formulated.
- **[OPEN]** No proven bound; T_v is not the exact reaction coordinate; DEFI-M13's question "why √n" remains open: over 65–193 the equilibrium barrier along T_v also grows like √n, which moves the question from dynamics to statics without explaining it.

## 5. What is established, what remains to be checked, the most fragile point

- **Established** (two implementations, repetitions, and a third engine from the reviewer up to n = 97): bimodality of P(T_v) and saddle height, n = 17 to 193; the constant residence/t½ ratio (§ 3.2); the absence of a saddle at λ = 66 (n = 65) and at mean degree 6 up to n = 49.
- **Depends on the estimator or the range**: the slope of ln t½ against B (0.75 to 1.24) and any quantitative Arrhenius reading; the shape of B (√n over 65–193, faster if 257 is included); the prediction at n = 257.
- **To be checked**: everything, by a person; the prediction at n = 257 by a dynamical measurement; a better reaction coordinate (e.g. the number of neighbours in the dominant clique, or path sampling); the canonical engine (DEFI-M10).
- **Most fragile point**: n = 257. Fixed-bias production is not flat there (min/mean ratio 0.03 and 0.00; one repetition did not visit T = 0 during production), the two engines' profiles differ locally by 7.6, and the point n = 385 failed. The barriers nevertheless agree between the two engines (differences ≤ 0.4); this is why § 3.4 remains an open question. From n = 97 to 193, production is also imperfectly flat (min/mean ratio 0.04 to 0.57); repetitions and the second engine agree there within ± 0.7 on B.

## 6. Hostile review

A second AI agent, which did not produce this work, replayed the analysis (byte-identical output), checked every number against the JSON files, inspected both engines (bias sign, T_0 update, reweighting, Σd² formula: no bug found), checked the armature citations (p. 10, 11, 18: exact) and recomputed the barriers at n = 33, 49, 65, 97 with its own code (§ 3.1). **Blocking points accepted and fixed**: (1) the conclusion "the exp(√n) law should not last" and the title did not hold; the ln t½ ↔ B relation is concave, linear extrapolation overestimates, a quadratic calibration is compatible with √n: § 3.4 rewritten as an open question [H], sensitivity table added, title changed; (2) "the saddle rises faster than √n" rested on n = 257: fits over 65–193 added (compatible with √n), sentence moved to [H]; (3) n = 257 removed from "Established"; (4) misreading of A0′ (stationary frequencies vs dynamical residence time): sentences removed or rephrased. **Minor points accepted**: standard deviations, range 3.5·10⁶, flatness never reached at n = 17, truncated support, direct check added to the analysis, scope of the second engine's independence (one run per size), caveats on mfpt, expected 1/ln 2 ratio and correlation of exits, approximate k_ari ≈ q agreement, English link.

## 7. Next step on the proof path (P1)

**DEFI-M14 — Does the √n law survive at n = 257?** Measure the residence time in the aristocracy (or t½) at n = 257, and beyond if possible, on abstract graphs at mean degree 4 under the armature measure, and decide between DEFI-M12's exp(0.96·√n) law (ln t½ ≈ 13.7) and faster growth (ln t½ ≈ 15 to 16 by this report's linear calibration); or prove a bound on the dominant-clique membership barrier; or find a better reaction coordinate than T_v.

## Reproduce

See the French version (§ Reproduire): same commands. Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0. Fixed seeds; the same script replayed on another machine may differ at the level of statistical noise. Screen outputs: `defi_m13_*_sortie.txt`.
