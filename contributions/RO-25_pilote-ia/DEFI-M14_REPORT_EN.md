🇬🇧 English · 🇫🇷 [Version française](DEFI-M14_RAPPORT.md)

# DEFI-M14 — Sojourn time in the aristocracy at n = 225 and 257: the √n law holds at 225 and is exceeded by 30 % at 257 (verdict under the criterion written in advance: undecided); an exploratory point at n = 289 indicates an acceleration

*Contribution by the laboratory's AI pilot (Claude, Anthropic), 6 November 2026. Filed like any contribution, as an `ia-assistee` issue. Predictions and decision criterion written before any measurement (`defi_m14_prediction.py`); measured by two engines sharing no kernel code; reviewed by a second AI agent acting as hostile reviewer (see § 6); **no human review at this stage**. The French version is the reference.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It provides the measurement asked for by DEFI-M14 (RO-25, RO-20) at n = 257, on abstract graphs only, without settling the question under the criterion fixed in advance; no bound is proven, the asymptotics remain open and the canonical engine is not treated.

## 1. The question

DEFI-M14 (#44), opened by [DEFI-M13_REPORT_EN.md](DEFI-M13_REPORT_EN.md), § 7: on abstract graphs of mean degree 4, under π ∝ exp(n·S_sim/τ), the autocorrelation half-time t½ of T_v (triangles containing vertex v) follows ln t½ = 0.964·√n − 1.77 from n = 17 to 193 ([DEFI-M12_REPORT_EN.md](DEFI-M12_REPORT_EN.md)), and the sojourn time in the aristocracy is 1.5 to 1.9 times t½ (DEFI-M13, § 3.2). At n = 257 the dynamics had been judged out of reach; the equilibrium barrier predicted ln t½ between 13.6 and 15.9 depending on the calibration, against 13.68 for the √n law (same report, § 3.4). **Is the √n law asymptotic, or a crossover effect?** Deliverable: t½ or sojourn time measured at n = 257, and beyond if possible, with error bars.

Authoritative sources: armature V347.1, § II.0 (p. 10: strata A_gen and A_Gibbs, S_sim(C) = log(1 + n_tri(C)) − β·D(C); the two missing bridges, RO-25 and RO-08); RO-25 box (p. 11: a joint dynamics whose conditional law at fixed N reproduces or derives π_N; falsifier: no local Markov extension has both the desired genealogy and this law); axioms A3–A4 [A][ARCH] (p. 18: β = 0.30; π_N(C) = Z_N⁻¹ exp(N·S_sim(C)/τ), τ = 0.50); A0′ (p. 18: under ergodicity these weights govern long-run empirical residence frequencies; "persist" is not defined, RO-20). Page numbers of the PDF `corpus/00_master_courant/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf`, checked by text extraction. Computational frame unchanged since DEFI-M8 (hypothesis H-abs): labelled simple abstract graphs, D = population standard deviation of degrees / mean degree, Metropolis swaps at fixed edge number M = 2n, λ = n/τ = 2n; one sweep = M swaps.

## 2. Method

**Predictions written before the measurement (`defi_m14_prediction.py`, run on 6 November 2026 at 08:49 UTC; first chain launched around 08:50).** Priority rests only on file timestamps in the pilot's environment: nothing was deposited publicly before the measurement, so this is not a preregistration a third party can verify. From the DEFI-M13 sojourns alone (n = 25 to 193), it fixes the sojourn predictions at n = 225 and 257: fit of ln sojourn in √n over n ≥ 65 (5.6·10⁵ and 1.55·10⁶ sweeps) or n ≥ 97 (5.3·10⁵ and 1.43·10⁶); DEFI-M12 t½ law × 1.63 (5.3·10⁵ and 1.43·10⁶); linear fit in n (8.8·10⁵ and 3.6·10⁶ from n ≥ 65; 2.5·10⁶ at n = 257 from n ≥ 97); DEFI-M13 linear calibration × 1.63 (5.9 to 13·10⁶ at n = 257). **Criterion**: the √n law "survives" at n = 257 if the measured sojourn lies in [0.6; 1.7]·10⁶; it is "contradicted by faster growth" above 3·10⁶; in between, undecided. The point n = 289 was added after the measurement at 257; no prediction covered it in advance: it is **exploratory**.

**Quantity (`defi_m14_sejour.py`)**: that of `defi_m13_sorties.py`, unchanged. Every Δ sweeps, T_v of all vertices; a vertex becomes "aristocrat" when T_v ≥ T_high, "commoner" when T_v ≤ 2, and keeps its state in between; T_high = half the T of the aristocratic minimum of the DEFI-M13 profile (n = 193: 112 → 56; n = 257: 136 → 68; n = 225: 124 → 62, interpolated; n = 289: 148 → 74, extrapolated, no profile measured there). Sojourn = total time spent as aristocrat (vertices × sweeps) / number of exits. Δ = t½ predicted by the DEFI-M12 law / 40, as in DEFI-M13 (21,921 sweeps at n = 257). In addition: pooled autocorrelation of T_v (all vertices, common mean) and its t½.

**Two engines sharing no kernel code.** **A**: kernel of `defi_m12_lenteur.balayer` (boolean matrix, numba generator), "planted core" start of `defi_m12_lenteur.depart`, FFT autocorrelation. **B**: kernel of `defi_m12_second_moteur.avancer_compte` (64-bit words, popcount, batched PCG64), planted start rebuilt in `defi_m14_sejour.py`, T_v from the diagonal of A³, autocorrelation by direct sum. Exact checks: n_tri = tr(A³)/6 at the end of the chain (A), at each record (B). Error bar for engine B: eight consecutive blocks per chain, sojourn per block, standard error over the sixteen blocks. The counting, thresholds and blocks are common code to both engines.

**Campaign.** n = 257: two A chains and two B chains of 2·10⁷ sweeps after 10⁶ burn-in (≈ 15 t½, ≈ 10 sojourns per chain). n = 225: two B chains of 1.3·10⁷. n = 289: two B chains of 3·10⁷ (≈ 5 t½, ≈ 3.4 sojourns per chain), and one A chain of 1.5·10⁷ added during the review. Control at n = 193: two B chains of 4·10⁶, compared with the DEFI-M13 A chains. Start control at n = 257: two B chains starting from a random graph (no planted clique), 3·10⁶ burn-in, 1.2·10⁷ production.

**Declared deviation.** `defi_m14_sejour.py` was modified twice during the campaign, without touching the kernels or the measured quantity: after the A chains at n = 257 (block output added, absent from those JSON files) and after the B chains at 193, 225 and 257 (threshold at n = 289; random-start option, hence the `depart` key missing from the first JSON files). The deposited script is the last version; it reproduces the first chains identically for the same seed (the additions draw no random numbers).

## 3. Results

### 3.1 The two engines agree [M]

| | chains (sojourn, sweeps) | pooled sojourn | exits | t½ per chain |
|---|---|---|---|---|
| n = 193, A (DEFI-M13) | 184,637; 179,059 | 181,814 | 324 | — |
| n = 193, B | 192,149; 172,039 | 181,500 ± 5,300 | 728 | 117,873; 107,827 |
| n = 257, A | 2,070,971; 1,971,460 | 2.020·10⁶ | 359 | 1,272,835; 1,239,095 |
| n = 257, B | 2,047,446; 1,981,036 | 2.014·10⁶ ± 0.072·10⁶ | 360 | 1,345,007; 1,310,941 |

At n = 257 the two engines agree to 0.3 % on the sojourn; their t½ are compatible (B's are 6 % above A's, for an internal spread of about 3 % per engine, i.e. about 2 standard deviations); the mean number of aristocrats is 18.13 to 18.14 in all four chains, identical over the two halves of each chain (no drift); the mean maximal T_v, 138.4, matches the aristocratic minimum of the DEFI-M13 equilibrium profile (136). At n = 193, engine B recovers the DEFI-M13 sojourn to within 0.2 %. **Start control**: two B chains starting from a random graph, with no planted clique, form the aristocracy by themselves (18.15 aristocrats on average) and give a sojourn of 1.85·10⁶ (1,814,328; 1,891,687; 235 exits), 0.92 times that of the planted chains, with chains 1.7 times shorter: the result does not come from the planted start shared by both engines.

### 3.2 Sojourn at n = 225, 257 and 289 [M; n = 289 exploratory]

| n | 193 | 225 | 257 | 289 |
|---|---|---|---|---|
| pooled sojourn (sweeps) | 1.818·10⁵ | 5.58·10⁵ ± 0.12·10⁵ | 2.02·10⁶ ± 0.07·10⁶ | 8.92·10⁶ ± 0.76·10⁶ |
| ln sojourn | 12.11 | 13.23 | 14.52 | 16.00 |
| predicted, √n from n ≥ 65 | — | 5.61·10⁵ | 1.55·10⁶ | — |
| measured / predicted | — | 0.99 | 1.30 | — |
| ln t½ per chain | 11.68; 11.59 | 12.77; 12.74 | 14.06; 14.03; 14.11; 14.09 | 15.53; 15.54 |
| ln t½, DEFI-M12 law | 11.62 | 12.69 | 13.68 | 14.62 |
| aristocrats (mean) | 16.5 | 17.4 | 18.1 | 19.0 |
| sojourn / t½ | 1.61 | 1.61 | 1.52 to 1.61 | 1.60 |

(Sojourn at 193: engine A, DEFI-M13; ln t½ and sojourn/t½ at 193: engine B; 225 and 289: engine B; 257: geometric mean of engines A and B. Bars: block standard error of engine B; exits per block are under-dispersed, so these bars are no wider than Poisson ones and include no systematic error; at 289 each block is shorter than one sojourn.)

- **n = 225**: the √n prediction written in advance is verified (ratio 0.99; 1.06 against the DEFI-M12 law).
- **n = 257**: sojourn 2.02·10⁶, ln t½ = 14.03 to 14.11. Under the criterion fixed in advance the verdict is **undecided** (between 1.7 and 3·10⁶). The DEFI-M13 linear calibration (ln t½ = 15.1 to 15.9; sojourn 5.9 to 13·10⁶) is excluded: measured 3 to 6.5 times shorter. The extended √n law (sojourn 1.43 to 1.55·10⁶) is exceeded: measured 1.30 to 1.41 times longer; counting the uncertainty of the extrapolation itself (Poisson on the DEFI-M13 points), the gap is about 4 standard deviations, less if the fit residuals are counted. This after-the-fact test does not replace the criterion fixed in advance, which says "undecided".
- **n = 289** (exploratory: added after the fact, extrapolated threshold, ≈ 3.4 sojourns per chain): sojourn 8.9·10⁶, ln t½ = 15.53, i.e. 2.5 times the DEFI-M12 law. The two B chains give exactly the same sojourn (64 exits and the same aristocrat time each): a checked coincidence, their blocks, intermediate states and t½ differ. Short controls, added during the review: one engine-A chain of 1.5·10⁷ sweeps gives 1.02·10⁷ (28 exits; ln t½ = 15.54; 19.02 aristocrats), and the reviewer's independent chain 1.4·10⁷ ± 0.4·10⁷ (16 exits); all lie far above the √n extrapolation (3.6 to 4.0·10⁶), but their uncertainties are wide.
- The sojourn/t½ ratio stays between 1.52 and 1.61: the DEFI-M12 t½ keeps following membership of the aristocracy.

### 3.3 The local slope rises from n ≈ 225 [M up to 257, H beyond]

Local slope Δ ln sojourn / Δ√n: 0.93 (49 → 65); 1.04 (65 → 97); 0.98 (97 → 129); 0.95 (129 → 193); 1.01 (193 → 225); **1.25 (225 → 257); 1.53 (257 → 289)**. Up to n = 225 the slope is constant to within ± 0.05, which is the √n law; over 225 → 257 (two engines at 257, one at 225) it is 1.25. Standard errors of the last two slopes, propagated from the blocks: 0.04 and 0.10; the departure from 1 is therefore about six and five standard errors (correlation between exits not accounted for beyond the blocks). **[H]** The exploratory point 289 continues this rise (1.53): growth would be faster than exp(c·√n) beyond n ≈ 225. This reading rests on a point not predicted in advance; it needs a second full-length engine, an equilibrium profile at n = 289 and larger sizes.

### 3.4 Asymptotic form: not determined [H]

Fit ln sojourn = a + b·n^γ, weighted by the Poisson error 1/√(exits) (scipy `curve_fit`; the unweighted version, cross-checked by a γ scan with hand-written least squares, is in `defi_m14_analyse_sortie.txt`, but with three parameters on four to seven points it has no useful precision): γ = 0.37 ± 0.04 on n = 65 to 193 (χ² = 0.1 for 1 dof); 0.41 ± 0.03 up to 225 (1.7 for 2); 0.50 ± 0.02 up to 257 (33.6 for 3); 0.54 ± 0.02 up to 289 (77 for 4); 1.28 ± 0.09 on 129 to 289 alone (6.0 for 2). The effective exponent rises as large sizes are added, and the χ² become huge: with Poisson bars, no law exp(b·n^γ) with fixed γ describes the whole set, but these bars count neither exit correlation nor possible systematic errors, and a non-smooth structure is not excluded. **[H]** The exp(0.96·√n) law of DEFI-M12 would be a law of the range (n = 17 to 225) rather than an asymptotic one. What the growth becomes beyond n = 289 (exp(c·n), faster still, or a new plateau) remains **[OPEN]**.

## 4. Reading for the RO-25 bridge and for RO-20

- **[M]** The aristocratic slowness does not level off at n = 257: the sojourn there exceeds the √n extrapolation by 30 to 41 %. **[H]** With the exploratory point 289: from n = 225 to 289 (√n goes from 15 to 17), the sojourn would be multiplied by 16, against 6.9 to 7.1 for the √n law (depending on the DEFI-M12 law or the fit fixed in advance).
- **[H]** The cost of a growth → Gibbs bridge that would let each newborn reach its equilibrium triangular mass before the next birth, already super-polynomial in DEFI-M12 (§ 4 there), grows even faster than the √n law said. Same caveat as then: RO-25 is not refuted; the armature's falsifier (p. 11) concerns the existence of a Markov extension, not its speed; another relaxation kernel (non-local swaps, collective moves) may mix faster, and nothing here concerns the canonical engine.
- **[H] Towards RO-20.** The sojourn in the dominant clique, from 10⁵ to 10⁷ sweeps over this range, is a kernel-specific duration growing with n; it is a quantifiable candidate for "persist" (a sojourn longer than the interval between two births), distinct from π > 0 (A0′, p. 18), still to be formulated.
- **[OPEN]** Why does the slope rise around n ≈ 225? The number of aristocrats (16.5 → 19.0) and their mean maximal T_v (112 → 153) grow regularly over 193–289; the measurement does not tell which event (losing edges one by one, or a collective reorganisation of the clique) controls the exit.

## 5. What is established, what remains to check, the weakest point

- **Established** (two engines at n = 193 and 257, planted and random starts at 257, repetitions, predictions written in advance, independent measurement by the reviewer at 193 and 257): sojourn and t½ at n = 257; the measurement exceeds the √n law by 30 to 41 % there (verdict under the criterion fixed in advance: undecided); the DEFI-M13 linear calibration (ln t½ = 15 to 16 at n = 257) is excluded.
- **Measured, one engine**: n = 225, where the √n law is verified (engine B, which recovers engine A to within 0.2 % at n = 193 and 0.3 % at n = 257).
- **Exploratory**: n = 289 (engine B at full length, short controls by engine A and by the reviewer) and the rise of the slope beyond 257.
- **To check**: everything, by a person; n = 289 by engine A at full length and by an equilibrium profile (the threshold is extrapolated there); n ≥ 321; the asymptotic form; a reaction coordinate explaining the rise of the slope; the canonical engine (DEFI-M10).
- **Weakest point**: n = 289. Each chain covers only about 3.4 sojourns there (128 exits in all, correlated: the same 19 seats are renewed), the burn-in (10⁶ sweeps) is only 0.11 sojourn, the threshold T_high = 74 is extrapolated (the ratio T_high / maximal T_v stays between 0.48 and 0.50 at all sizes), and no prediction had been written before the measurement. The verdict on n = 257 alone is "undecided" under the criterion fixed in advance; the conclusion "the slope rises" rests on 257 and 289 together.

## 6. Hostile review

A second AI agent, which did not produce this work, recomputed every number against the JSON files, checked the code (thresholds, hysteresis, counting, equality in law of the two kernels, same S_sim, same Δ), checked the armature citations (pp. 10, 11, 18: correct) and redid the measurement with its own kernel written from scratch (neighbour lists, xoshiro256** generator): sojourn 15,400 ± 350 at n = 129 (DEFI-M13: 16,301), 193,060 ± 12,000 at n = 193 (181,800), 2.02·10⁶ ± 0.27·10⁶ at n = 257 (2.02·10⁶), 1.4·10⁷ ± 0.4·10⁷ at n = 289 (8.9·10⁶). At n = 129 it tested the effects that could manufacture the rising slope: threshold (± 12 %, ratio T_high / maximal T_v constant across sizes), step Δ (a larger Δ lengthens the sojourn; Δ/t½ decreasing with n, this bias works against the conclusion), short planted-start chains and random start (no significant bias). It concluded that the measurement holds and the interpretation was overstated.

**Blocking points accepted and corrected**: (1) the title and §§ 3.3, 3.4 and 7 claimed "the √n law does not extend beyond n ≈ 225", whereas the criterion fixed in advance says "undecided" at 257 and the conclusion rested on point 289, added afterwards: title rewritten, 289 declared exploratory, conclusions moved to [H]; (2) "6.5 to 8 standard errors" ignored the uncertainty of the extrapolation: about 4 standard deviations, an after-the-fact test that does not replace the criterion; (3) the § 3.4 exponents had meaningless precisions (unweighted fits, 1 dof): redone weighted, with χ²; (4) "7.7" wrong: 6.9 to 7.1; (5) [M] labels of conclusions about 289 moved to [H]; (6) "preregistered" not verifiable by a third party (nothing deposited before the measurement) and script modified after the first chains: declared in § 2. **Minor points accepted**: pooled sojourn 181,814 (not 181,848); caption of the 193 column; "≈ 15 t½" (not 10) at 257; "1.7 times" (not twice); direction of "underestimates"; n = 225 removed from "Established"; T_v 112 (not 111); A/B t½ "compatible"; nature of the block bars (under-dispersion, blocks shorter than the sojourn at 289); short burn-in at 289; coincidence of the two B chains at 289 reported; engine-A control at 289 added; English link.

## 7. Next step on the proof path (P1)

**DEFI-M16 — After √n: the law of aristocratic slowness.** On abstract graphs of mean degree 4 under the armature measure, the sojourn in the aristocracy follows exp(0.96·√n) up to n ≈ 225, exceeds it by 30 % at n = 257, and an exploratory point at n = 289 indicates an acceleration (local slope in √n from 1.0 to 1.5 between n = 193 and 289; this report). Deliverable: the sojourn at n ≥ 321 (two engines, equilibrium profile at the same size) and the form of the growth; or the exit mechanism (most probable path, transition path sampling) explaining the change of slope around n ≈ 225; or a proven bound. In every case, the decision criterion is deposited publicly (issue or commit) before the measurement.

## Reproduce

See the French version, § Reproduire (same commands). Python 3.13, numpy 2.5.3, scipy 1.18.1, numba 0.68.0.
