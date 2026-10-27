🇬🇧 English · 🇫🇷 [Version française](DEFI-M12_RAPPORT.md)

# DEFI-M12 — The aristocratic slowness: neither a power law nor an exponential in n; at mean degree 4, t½ ≈ exp(0.96·√n) from n = 17 to 193

*Contribution by the laboratory's AI pilot (Claude, Anthropic), 27 October 2026. Filed like any contribution, as an `ia-assistee` issue. Checked by the pilot (two measurement methods, a second implementation independent at code level) and reviewed by a second AI agent acting as a hostile reviewer, with its own engine (see § 6); **no human review at this stage**. The French version is the reference text.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It partially answers DEFI-M12 (RO-25, RO-20), on abstract graphs only; the canonical engine is not addressed.

## 1. The question

DEFI-M12 (#38), opened by [DEFI-M11_REPORT_EN.md](DEFI-M11_REPORT_EN.md), § 3 B2: on abstract graphs with mean degree 4, the half-time t½ for a newborn to acquire its equilibrium triangle mass goes from 0.5 sweep (N = 8) to 442 (N = 64), "at least of order N³, perhaps exponential". **A power of N, or exponential?** Deliverable ([DEFIS.md](../../DEFIS.md), DEFI-M12 row): a proven bound, or a measurement up to N ≥ 128 at two densities at least, with error bars, and on the canonical engine at N ≥ 250.

Authoritative sources: armature V347.1, § II.0 (strata A_gen and A_Gibbs, p. 10; the two missing bridges, RO-25 and RO-08); RO-25 box (p. 11: a joint dynamics at variable N, combining mitosis/closure and relaxation, whose conditional law at fixed N reproduces or derives π_N); axioms A3–A4, labelled [A][ARCH] (p. 18): S_sim(C) = log(1 + n_tri(C)) − β·D(C), β = 0.30; π_N ∝ exp(N·S_sim/τ), τ = 0.50; A0′ (p. 18: "persisting" is not defined by π_N > 0, RO-20). Computational frame: hypothesis H-abs of [DEFI-M8_REPORT_EN.md](DEFI-M8_REPORT_EN.md), § 2 (abstract labelled simple graphs, no Rips constraint; D = population standard deviation of degrees / mean degree; Metropolis swaps at fixed edge number). n is the number of vertices (n = N + 1 after a birth), M the number of edges, λ the factor of the measure π ∝ exp(λ·S_sim) (λ = n/τ = 2n for axiom A4); a **sweep** is M swaps. The birth studied (attachment to k = 4 vertices) is not the generator μ of A_gen (p. 10: one leaf, a single edge, no closure): it is the frame of DEFI-M11.

## 2. Method

**Stationary method (new, `defi_m12_lenteur.py`).** In an equilibrium chain, T_v (triangles containing v) is recorded for every vertex every Δ sweeps, and the pooled autocorrelation C(t) is computed with a mean common to all vertices (equal to 3T/n). t½ is the first time at which C(t) = 1/2 (linear interpolation). C(t) essentially follows the persistence of membership in the aristocracy: at n = 65 the reviewer finds t½ = 412 for T_v, 389 for the indicator T_v > 6 and 289 for membership in the nine most triangulated vertices. t½ is an autocorrelation half-time of one observable, not a mixing time. Three settings:

- **c2**: M = 2n (mean degree 4, the density of DEFI-M11), λ = n/τ (axiom A4);
- **c3**: M = 3n (mean degree 6), λ = n/τ;
- **c2T**: M = 2n, λ = 33/τ = 66 fixed (effective temperature held constant).

n = 17, 25, 33, 49, 65, 97, 129, 193; L = 3,000 records per chain (6,000 for c2T); four chains per point, two from random starts and two from a "planted core" (largest clique compatible with M); error bar: standard deviation across chains / 2 (standard error over four chains, probably optimistic: see § 5). Δ targets t½/Δ ≥ 5, except c3 at n ≤ 25 (Δ = 1 sweep, t½/Δ = 2.2 and 4.6) and c2T at n = 129 and 193 (Δ = 1, t½/Δ = 6.5 and 2.7); the reviewer estimates the interpolation bias below 1 % even at t½/Δ = 2.2.

**Discarded passes.** Two passes had too large a Δ: the first for c3 and c2T (the Δ of c2), the second for c2T (Δ = 5). They are kept (`defi_m12_lenteur_premiere_passe_sortie.txt`, `defi_m12_lenteur_c3_c2T_sortie.txt`) and excluded from the analysis, which keeps only chains with the Δ of the final code (`defi_m12_analyse.py`). This is not selection on results: discarded and retained c3 differ by 1 to 4 %; the discarded c2T is biased upwards because t½ there is of order Δ or less (e.g. 157 instead of 6.5 at n = 129 with Δ = 314).

**Birth method (that of DEFI-M11, `defi_m12_naissance.py`).** The engine `defi_m11_monte_carlo.experience` is reused unchanged (uniform attachment, k = 4, M = 2N − 2) at N = 96 (400 births) and N = 128 (200 births), with parent burn-in of 12,000 and 40,000 sweeps and spacing of 1,000 and 3,000 sweeps (0.3 t½ at N = 128: births are not independent, so the bootstrap 90 % interval is optimistic); t½ from the function in [defi_m11_demi_temps.py](defi_m11_demi_temps.py).

**Direct cooling test (`defi_m12_arrhenius.py`, suggested by the reviewer).** At fixed n = 65, λ = 98, 162, 194 (plus λ = 66 from c2T and λ = 130 from c2); at fixed λ, n = 49 versus 65 (λ = 98) and n = 65 versus 97 (λ = 194). Four chains per point, t½/Δ between 13 and 17.

## 3. Results

### 3.1 Mean degree 4, armature measure (c2): t½ ≈ exp(0.96·√n) from n = 17 to 193 [M]

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| stationary t½ (sweeps) | 9.2 ± 0.1 | 21.5 ± 0.4 | 43.3 ± 0.7 | 146 ± 2 | 389 ± 4 | 2,297 ± 64 | 9,760 ± 173 | 111,873 ± 1,230 |
| birth t½ (DEFI-M11 up to 65; here at 97 and 129, 90 % CI) | 7.5 | 22.9 | 46.8 | 139; 147 | 442 | 2,383 (1,860–3,141) | 11,317 (7,719–26,437) | — |
| Δ log t½ / Δ log n | — | 2.19 | 2.53 | 3.08 | 3.46 | 4.43 | 5.07 | 6.05 |
| Δ log t½ / Δ √n | — | 0.97 | 0.94 | 0.97 | 0.92 | 0.99 | 0.96 | 0.96 |

- The log-log slope keeps increasing (2.2 → 6.1): **no power law** over this range. The slope per unit of n decreases (0.106 → 0.038): **no exponential in n** either. The slope per unit of √n is constant within ± 4 %.
- Fits on n ≥ 25 (sum of squared residuals of log t½): power (exponent 4.13) 1.26; exponential in n 1.06; exponential of √n 0.0020 (log t½ = 0.964·√n − 1.77; largest residual 4 %). With a free exponent, log t½ = a·n^γ + b gives **γ = 0.507 ± 0.010** (n ≥ 25) and 0.497 ± 0.027 (n ≥ 49).
- **Out-of-sample prediction** (fit on n ≤ 97, prediction at n = 129 and 193): exponential of √n, 9,611 and 110,086 sweeps, measured/predicted ratios **1.02 and 1.02**; power law, ratios 2.0 and 5.8; exponential in n, 0.47 and 0.09.
- The two methods agree: at n = 97 and 129 the 90 % intervals of the birth t½ (1,860–3,141; 7,719–26,437) contain the stationary t½ (2,297; 9,760); from n = 17 to 65 the differences range from −19 % to +14 %.
- In Metropolis swaps (2n·t½), the half-time goes from 3·10² swaps at n = 17 to 4.3·10⁷ at n = 193.

### 3.2 Mean degree 6 (c3): super-polynomial too, but not exp(a√n) [M]

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| t½ (sweeps) | 2.20 ± 0.02 | 4.57 ± 0.03 | 8.25 ± 0.14 | 21.4 ± 0.2 | 52.7 ± 0.4 | 247 ± 2 | 974 ± 14 | 10,447 ± 214 |
| Δ log t½ / Δ √n | — | 0.83 | 0.79 | 0.76 | 0.85 | 0.86 | 0.91 | 0.94 |

At equal n, relaxation is faster than at mean degree 4, but also super-polynomial (log-log slopes 1.9 → 5.9). Of the three two-parameter forms, the exponential of √n is the least bad (sum of squares 0.062 against 0.49 and 1.53), but its slope drifts (0.76 → 0.94) and the out-of-sample prediction underestimates n = 193 by a factor 1.6. With a free exponent: **γ = 0.63 ± 0.01** (n ≥ 25), 0.61 ± 0.01 (n ≥ 49). The exp(a√n) form is therefore not universal: at this density growth is faster, without being exponential in n over the measured range.

### 3.3 The slowness follows λ, not size [M]

**At fixed λ (c2T, λ = 66), as n grows:**

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| t½ (sweeps) | 117 ± 4 | 56.3 ± 0.9 | 43.8 ± 1.2 | 37.1 ± 0.9 | 34.0 ± 1.0 | 17.7 ± 0.8 | 6.5 ± 0.3 | 2.7 ± 0.1 |
| share of the mean of T_v carried by vertices with T_v > 6 | 0.98 | 0.96 | 0.94 | 0.87 | 0.79 | 0.54 | 0.27 | 0.07 |

t½ decreases with n and the aristocracy dissolves. On its own this test does not separate two things: at fixed λ, increasing n changes the equilibrium state itself (the aristocracy disappears). It shows that λ growing with n is necessary for the slowness. (Reproducibility check: at n = 33, c2T and c2 have the same λ and close t½, 43.8 and 43.3.)

**At fixed n (n = 65), as λ grows:**

| λ | 66 | 98 | 130 | 162 | 194 |
|---|---|---|---|---|---|
| t½ (sweeps) | 34.0 ± 1.0 | 141 ± 2 | 389 ± 4 | 1,032 ± 17 | 2,873 ± 58 |

log t½ is affine in λ for λ ≥ 98 (slope 0.031): the signature of an activated, Arrhenius-type barrier at fixed n. **At equal λ and different n**: t½(n = 49, λ = 98) = 141 against t½(n = 65, λ = 98) = 141; t½(n = 97, λ = 194) = 2,276 against t½(n = 65, λ = 194) = 2,873. On these points t½ depends mainly on λ, and only weakly on n at fixed λ (it decreases with n).

**Reading.** The slowness of 3.1 is carried by the scaling λ = n/τ of axiom A4, which cools the measure as n grows, not by the size of the swap kernel. The [H] mechanism of DEFI-M11 (§ 4, "cooling") is **compatible** with these measurements (necessary condition verified, activated growth in λ at fixed n); the exp(a·n) form it suggested is not observed along λ = 2n.

### 3.4 Anatomy of the aristocracy at mean degree 4: a dominant clique of size of order √n [M], and an [H] reading

Forty equilibrium snapshots per size, one chain per size, setting c2 (`defi_m12_structure.py`; correlated snapshots, spaced by 0.19 t½ at n = 193; no error bars):

| n | 17 | 25 | 33 | 49 | 65 | 97 | 129 | 193 |
|---|---|---|---|---|---|---|---|---|
| largest clique (mean) | 5.5 | 5.8 | 6.5 | 7.7 | 8.8 | 10.8 | 12.1 | 14.8 |
| share of Σ T_v carried by its vertices | 0.74 | 0.69 | 0.72 | 0.75 | 0.78 | 0.83 | 0.85 | 0.90 |
| maximal T_v | 17.5 | 23.0 | 28.7 | 40.4 | 50.3 | 67.9 | 82.1 | 112.4 |

The largest (exact) clique grows as n^0.47 (n ≥ 33) and its vertices carry 69 to 90 % of the triangles: at this density, the "aristocracy" of DEFI-M11 is essentially **a dominant clique of size of order √n**. log t½ is affine in the size q of this clique on n ≥ 33 (slope 0.94, largest residual 0.13), less well than in √n (residual 0.04); since q varies as n^0.47, this is not an independent confirmation.

**[H] reading, not proven.** For an outside vertex to enter the dominant clique, or for a member to leave it, of order q edges each carrying of order q triangles must be undone and redone. If each step costs a Boltzmann factor of at most e^(−c), with c > 0 independent of n, the member-exchange time is at least of order exp(c·q) = exp(c′·√n). A sharper variant (from the reviewer): removing a clique edge costs about λ·q/T with T ≈ q³/6, i.e. 6λ/q²; this cost is constant along λ = 2n (since q² ∝ n), giving a barrier of about 6λ/q ∝ √n; at fixed n it is proportional to λ (consistent with 3.3); at fixed λ it decreases as q grows (consistent with c2T). **Unresolved tension**: this scheme also predicts exp(a√n) at mean degree 6, where γ ≈ 0.6 is measured (3.2); the structure was not measured there.

### 3.5 Cross-checks

- **Second implementation, independent at code level** (`defi_m12_second_moteur.py`: 64-bit neighbourhood words and popcount, numpy PCG64 generator, T_v from diag(A³), autocorrelation by direct sum; no shared code; same Δ, same 200 Δ burn-in, same estimator, two chains per point, random starts only). c2, n = 17, 33, 65, 129: t½ = 8.9, 44.0, 387, 10,074 against 9.2, 43.3, 389, 9,760 (−3 % to +3 %). c3 (Δ of the first pass, t½/Δ ≈ 1.7 to 3 for n = 33 to 129): 2.16, 8.44, 54.7, 978 against 2.20, 8.25, 52.7, 974 (−2 % to +4 %). It first revealed an error in *its own* code (sum of squared degrees wrong when a vertex of the added edge coincides with a vertex of the removed edge), fixed before any comparison; it now checks triangles, degrees and Σ d² at every record.
- **Reviewer's engine** (its own Metropolis code, c2): t½ = 44.4, 144, 2,194, 9,467 at n = 33, 49, 97, 129, against 43.3, 146, 2,297, 9,760; same mean number of triangles.
- **Reference engine**: the parameterised kernel of `defi_m12_lenteur.py` reproduces `defi_m11_monte_carlo.balayer` bit for bit for λ = n/τ (same seed, 20,000 swaps; also checked by the reviewer at n = 49).
- **Equilibrium**: random and "planted core" starts give the same mean number of triangles (difference ≤ 1.3, for a standard deviation of T of 5 to 45) and compatible t½ (relative standard deviation across the four chains ≤ 6 % for c2 and c3, ≤ 9 % for c2T).

## 4. Reading for the RO-25 bridge

- **[M]** On abstract graphs, at mean degree 4 and under the armature measure, the pooled autocorrelation half-time of T_v, which essentially follows the persistence of membership in the aristocracy, grows as exp(0.96·√n) from n = 17 to 193, out-of-sample prediction included; at mean degree 6, faster (about exp(a·n^0.6)) over the measured range. This growth is carried by λ = n/τ (3.3).
- **Consequence [H], extrapolation beyond n = 193.** A growth → Gibbs bridge letting each newborn reach its equilibrium triangle mass before the next birth, with this swap kernel, would require an inter-birth interval of order t½(n) ≈ 0.17·exp(0.96·√n) sweeps: 1.4·10⁵ at n = 200, and of order 10⁴¹ at n = 10⁴ if the law continued. **That bridge would not be practicable at large n for massive vertices, if the law continued and if the conditional law of labelled graphs is required.**
- **What this does not refute.** RO-25 is not refuted: the armature's falsifier (p. 11) is about the *existence* of a local Markov extension, not its slowness. The slowness measured is that of edge swaps at fixed number; another relaxation kernel (vertex moves, label swaps) may mix faster. But a label swap makes the newborn's identity, hence the genealogy, irrelevant: the slowness concerns precisely the memory of who was born when. Finally, the birth studied is not the μ of A_gen (§ 1).
- **Link with RO-20 [H].** The dominant clique persists longer as n grows: its persistence is a candidate "persisting" criterion distinct from π > 0 (A0′, p. 18), to be examined.
- **Canonical engine [OPEN].** None of this is measured on the canonical (Rips) engine, where DEFI-M9 does not, so far, see growth in N of the bulk of the mass law; DEFI-M10 remains the challenge that must decide.

## 5. What is established, what remains to be checked, the weakest point

- **Established**: the c2, c3 and c2T series and the fixed-n test (four chains per point), cross-checked by a second implementation (eight points), by the reviewer's engine (four points) and, for c2, by the birth method (seven sizes).
- **To be checked**: everything, by a person; the form beyond n = 193; the form at mean degree 6 and at other densities; the "barrier ∝ clique size" reading; the canonical engine.
- **Error bars**: standard errors over four chains, probably optimistic. Reproducing at n = 65 the protocol of n = 193 (eight chains of 28 t½, burn-in 1.9 t½), the reviewer finds a per-chain standard deviation of 5.7 %, against 2.2 % across the four chains at n = 193; weighted by the report's bars, the √n fit gives χ² = 12.8 for 5 degrees of freedom. The conclusion rests on the shape (slopes, free exponent, prediction), not on these bars.
- **Armature readability rules** (p. 18, rule 10.4, stability under lengthening): not applied at n = 193 (no longer chain); the reviewer finds no lengthening bias at n = 65 (389.4 against 389.2).
- **Weakest point**: at n = 193 (c2), burn-in is only 1.9 t½ and the chain 28 t½; the agreement of random and planted starts, and the prediction made on n ≤ 97, reassure without proving. The exponential of √n is a fit over eight sizes, not a proven law, and it does not hold at mean degree 6.

## 6. Hostile review

A second AI agent, which did not produce this work, re-ran the analysis (outputs identical byte for byte), checked every number against the JSON files and the armature references (p. 10, 11, 18: correct), and redid the c2 curve with its own engine (§ 3.5). Blocking issues accepted and fixed: "confirmed" replaced by "compatible" in § 3.3, with the direct fixed-n test it proposed added, then re-run by the pilot (`defi_m12_arrhenius.py`); consequence for RO-25 labelled [H], prefactor 0.17 restored, conclusion made conditional; title and § 3.1 restricted to mean degree 4, c3 free exponent (≈ 0.6) added; [H] reading corrected (direction of the inequality, notation, tension with c3); false sentence ("bracket") fixed; numbers fixed (slope 0.106 → 0.038; 974; exceptions to t½/Δ ≥ 5). Minor points accepted: optimistic bars (§ 5), interpretation of C(t) (§ 2), structure without bars (§ 3.4), optimistic birth bootstrap, μ of A_gen, rule 10.4, discarded passes detailed, scope of the second implementation, references made precise. Not applied: non-breaking spaces (current typographic convention of the repository).

## 7. Next step on the proof path (P1)

**DEFI-M13 — The barrier of the dominant clique.** At mean degree 4 under π ∝ exp(n·S_sim/τ): prove, or refute, that the largest clique has size of order √n and that the exchange time of its members by edge swaps grows as exp(Θ(√n)) (bottleneck, conductance bound); explain why growth is faster at mean degree 6 (γ ≈ 0.6); look for the same signature on the canonical engine at N ≥ 250 (DEFI-M10).

## Reproduce

See the « Reproduire » section of the [French version](DEFI-M12_RAPPORT.md#reproduire) (same commands). Python 3.13, numpy 2.5.3, scipy 1.18.1, networkx 3.7, numba 0.68.0.
