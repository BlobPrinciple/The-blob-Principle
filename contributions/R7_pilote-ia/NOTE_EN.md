🇬🇧 English · 🇫🇷 [Version française](NOTE.md)

# DEFI-R7 — Viable condensation in a periodic box: it survives, with no size effect, and still coarsens slowly

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. Note by the laboratory's AI pilot (Claude, Anthropic), scheduled session of 20 November 2026, by delegation of Rudolphe Mirante. Not reviewed by a person. The French version is the reference.

## Purpose

DEFI-R7 ([#47](https://github.com/BlobPrinciple/The-blob-Principle/issues/47); `docs/defis.json`) starts from part C of DEFI-R6 (`contributions/R6_pilote-ia/NOTE_EN.md`): under the archived mobility engine (`relax_positions`, `local_S`, `rgg_radius` in `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob gravite colab.py`, V346 XXV.1 p. 642), viability alone, from a uniform start, deepens voids and produces a P(k) peak at k = 3–5, about 2.9·r_N. Two questions: does this condensation stop at a scale set by r_N, β and τ, or coarsen without end? Does it survive a periodic box? Deliverable: periodic-box campaign, uniform start, at least 3 sizes and 8 seeds per point, up to at least 1,280 sweeps, L(t, N) with error bars, compared with r_N.

## Result in brief

1. **[M] The condensation survives the periodic box.** Same rule, steps taken modulo 1 and minimum-image distance instead of clipping: at N = 2,500, voids 0.811 ± 0.001 (80 sweeps) and 0.867 ± 0.001 (320), against 0.806 and 0.858 in the clipped box; S(k) peak on shells 3–4 in both. The mobility arm without viability stays at the uniform level up to 1,280 sweeps (voids 0.731 to 0.733; S_max 1.04 to 1.9, the noise maximum over 31 shells).
2. **[T] Any length intrinsic to the rule is a multiple of r_N, by construction; [M] no box-size effect is visible.** The first point is dimensional analysis, not a measurement: κ fixes the density in units of r_N³, the step is σ = 0.3·r_N, N//4 attempts per sweep give the same per-vertex rate at every N, β and τ are dimensionless; in units of r_N the only other length is the box. What the measurement adds: L/r_N = c(t) does not depend on N within the precision obtained, while the box holds 4 to 6.3 lengths depending on N. With the estimator cut at the same k·r_N at every size, L₁c/r_N = 2.75; 2.73; 2.73 at 80 sweeps and 2.95; 2.94; 2.93 at 1,280 (N = 2,500; 5,000; 10,000). The peak height does not depend on N either (S_max ≈ 52 to 54 at all three sizes at 1,280 sweeps).
3. **[M] The length still grows, slowly, with no visible stop within the window.** From 80 to 1,280 sweeps, L₁c/r_N grows by about 7 % (slope d ln L₁c/d ln t = 0.026 ± 0.002; 0.027 ± 0.001; 0.026 ± 0.001 depending on N); the peak top moves faster (L_peak/r_N 2.88 → 3.52 at N = 2,500), but this estimator, interpolated on integer shells 3–4, is fragile. The increments per doubling of time do not decrease (L₁/r_N at N = 2,500: 2.70; 2.70; 2.76; 2.82; 2.91 at 80, 160, 320, 640, 1,280). The amplitude grows much faster (S_max 12 → 52, voids 0.81 → 0.89 at N = 2,500). **[OPEN]** Stop at a finite length, or slow endless coarsening (logarithmic or with a small exponent): the window does not decide.

**Verdict.** Viable condensation is not a boundary effect: it survives the periodic box, and its length in units of r_N is the same at all measured sizes. That this length is "a model scale" is true by construction as long as it does not reach the box; the real question of DEFI-R7 is therefore point 3: does c(t) have a limit? It remains open: at 1,280 sweeps the length still grows by a few percent per doubling of time. If this coarsening does not stop, it will eventually reach the box size, and DEFI-R6's reading "microscopic, not cosmic scale" (part C) would only hold for finite durations. β and τ were not varied. No status change; V347.1 framework untouched.

## Method

**Rule (taken from the archived engine, constants unchanged).** κ = 6.6; β = 0.30; τ = 0.50; r_N = (κ/((N − 1)·4π/3))^{1/3}; σ = 0.3·r_N; N//4 attempts per sweep; an isolated vertex does not move; Metropolis acceptance on the local S of the moved vertex only, S(v) = ln(1 + triangles at v) − β·(population standard deviation / mean of the neighbours' degrees); mobility arm: acceptance 1/2. The graph is the geometric graph (0 < d < r_N) of the positions: the archived engine also rebuilds it at every step (`rebuild`) and, from a uniform start, its initial graph is geometric; here it is recomputed on the fly (only difference, of no practical consequence: the archive builds the initial graph with d ≤ r).

**Only intended change.** Periodic box: steps modulo 1, minimum-image distance. Option `--rogne` restores the archived engine's `np.clip`.

**Implementation A** (`r7_periodique.py`, numba, cell lists of side ≥ r_N; no cell overflow, forced refusals are counted: 0 everywhere). Check in the clipped box, same uniform start, 8 seeds, against DEFI-R6's files (`r6_campagne_N2500_b80_initpoisson.json`, `…_b320_…`, produced by DEFI-R6's script, which imports `relax_positions` as is; hence an indirect check of the archived engine): voids 0.8064 ± 0.0008 against 0.8054 ± 0.0008 (+0.9 σ) at 80 sweeps, 0.8583 ± 0.0009 against 0.8596 ± 0.0015 (−0.8 σ) at 320; peak shell 3–4 against 3–4; mobility arm 0.7305 against 0.7316.

**Measurements.** Voids: fraction of empty cells among 20³ (DEFI-R6 convention). S(k) = P(k)/N, P by FFT of counts on a 64³ grid (nearest-grid-point assignment, periodic), averaged over shells round(|k|) = 1 to 31; S = 1 for the uniform case. Three lengths, in box units (L = 1/k, DEFI-R6 convention), divided by r_N:
- **L₁c** = 1/k₁c, k₁c first moment of the excess (S − 1)₊ over k ≤ ⌊0.8/r_N⌋ (9, 11, 14 depending on N: same cut in units of r_N) — headline estimator;
- L₁ = 1/k₁, same moment over k ≤ 20 (cut k·r_N = 1.71; 1.36; 1.08 depending on N: a different estimator at each size, given for comparison with the first version);
- L_peak, peak top interpolated by a parabola over three shells.
The nearest-grid-point window damps S by less than 3 % at k ≤ 6 and by up to about 28 % at k = 20 (along an axis); it pulls L₁ slightly upwards at large N, hence the choice of L₁c. Error bars: standard error over seeds. Starts overlap between sizes (`default_rng(1000 + g)`: the first 2,500 points at N = 5,000 are those of N = 2,500): weak correlation between sizes, declared.

**Implementation B** (`r7_second_moteur.py`, no shared code): Python and numpy, brute-force minimum-image distances, PCG64 generator on other seeds, and **exact** structure factor |Σ_j exp(2iπ n·x_j)|²/N over all integer vectors n of the shell (no grid). N = 2,500, 3 seeds, 80 sweeps (B is about 40 times slower than A).

## Measurements

Periodic box, uniform start; standard error over seeds.

| N (seeds) | sweeps | voids, viab | voids, mobile | L₁c/r_N | L₁/r_N | L_peak/r_N | S_max |
|---|---|---|---|---|---|---|---|
| 2500 (8) | 20 | 0.759 ± 0.001 | 0.731 | 2.57 ± 0.03 | 2.45 ± 0.03 | 2.73 ± 0.09 | 3.5 ± 0.1 |
| 2500 (8) | 80 | 0.811 ± 0.001 | 0.731 | 2.75 ± 0.02 | 2.70 ± 0.02 | 2.88 ± 0.05 | 12.1 ± 0.3 |
| 2500 (8) | 320 | 0.867 ± 0.001 | 0.732 | 2.79 ± 0.02 | 2.76 ± 0.01 | 3.25 ± 0.09 | 31.1 ± 1.2 |
| 2500 (8) | 1280 | 0.894 ± 0.001 | 0.732 | 2.95 ± 0.01 | 2.91 ± 0.01 | 3.52 ± 0.06 | 52.0 ± 2.6 |
| 2500 | slope d ln L/d ln t, t = 80–1280 | | | 0.026 ± 0.002 | 0.028 ± 0.002 | | |
| 5000 (8) | 20 | 0.602 ± 0.001 | 0.534 | 2.60 ± 0.02 | 2.57 ± 0.02 | 2.68 ± 0.07 | 3.6 ± 0.1 |
| 5000 (8) | 80 | 0.703 ± 0.001 | 0.535 | 2.73 ± 0.01 | 2.71 ± 0.01 | 2.83 ± 0.05 | 12.3 ± 0.2 |
| 5000 (8) | 320 | 0.799 ± 0.001 | 0.535 | 2.77 ± 0.01 | 2.73 ± 0.01 | 3.20 ± 0.05 | 31.1 ± 0.8 |
| 5000 (8) | 1280 | 0.839 ± 0.002 | 0.535 | 2.94 ± 0.01 | 2.91 ± 0.01 | 3.56 ± 0.11 | 51.6 ± 1.6 |
| 5000 | slope d ln L/d ln t, t = 80–1280 | | | 0.027 ± 0.001 | 0.025 ± 0.001 | | |
| 10000 (8) | 20 | 0.398 ± 0.001 | 0.290 | 2.61 ± 0.02 | 2.61 ± 0.02 | 2.79 ± 0.05 | 3.5 ± 0.1 |
| 10000 (8) | 80 | 0.550 ± 0.001 | 0.283 | 2.73 ± 0.01 | 2.72 ± 0.01 | 2.97 ± 0.02 | 12.8 ± 0.4 |
| 10000 (8) | 320 | 0.693 ± 0.001 | 0.285 | 2.76 ± 0.01 | 2.73 ± 0.01 | 3.16 ± 0.04 | 33.2 ± 0.7 |
| 10000 (8) | 1280 | 0.756 ± 0.001 | 0.288 | 2.93 ± 0.01 | 2.90 ± 0.01 | 3.56 ± 0.04 | 53.5 ± 1.0 |
| 10000 | slope d ln L/d ln t, t = 80–1280 | | | 0.026 ± < 0.001 | 0.023 ± 0.000 | | |

Second implementation (N = 2,500, 80 sweeps, 3 seeds of B against 8 of A): voids 0.8096 ± 0.0021 against 0.8111 ± 0.0008 (−0.7 σ); peak shell 4, 4, 4 against 4 (seven seeds) and 5; S(k) for k = 1 to 6: B 2.45; 6.15; 10.73; 12.25; 9.93; 5.54 against A 1.78; 5.55; 9.53; 12.09; 9.74; 5.44, deviations of 0.2 to 2.1 combined errors. B is above A on all six shells (+38 % at k = 1, +12 % at k = 3); A's window (< 3 %) does not explain it; with 3 seeds and shells correlated within one seed, the gap remains compatible with noise. Result: compatible; this second implementation checks the coding of the rule and of the measurement, not the model.

## What does not hold, or not yet

- **β and τ not varied.** Only N varies; independence of N is not a discovery about r_N (point 2). The challenge also asked about β and τ. [OPEN]
- **Asymptotics.** A growth of about 7 % over a factor 16 in time distinguishes neither a distant stop, nor a logarithmic law, nor a small power; the estimators do not give the same slope (≈ 0.026 for L₁ and L₁c, ≈ 0.07 for L_peak). [OPEN]
- **Box size.** At N = 2,500 the box holds only 4 lengths; the peak falls on shells 3 to 4. The agreement at three sizes indicates that the box does not yet set the length; it would if coarsening went on long enough.
- **A single shape observable** (S(k)); no real-space cluster measurement; final positions not archived.

## Departures from the deliverable

- The deliverable is met for the periodic box (3 sizes, 8 seeds per point, uniform start, 1,280 sweeps, L(t, N) with standard errors, compared with r_N). It is not met for β and τ, which were not varied (single-run budget; see DEFI-R8).
- The second implementation covers only N = 2,500, 3 seeds, 80 sweeps (it is about 40 times slower); late times (320 to 1,280 sweeps) and sizes 5,000 and 10,000 rest on implementation A alone.
- The N = 10,000 seeds are spread over four files (`r7_N10000.json`, `_b`, `_c`, `_d`), computed in parallel; they are disjoint.

## What this changes

- For the simulated web (DEFI-R6): the condensation specific to viability is not an artefact of the clipped faces; up to 1,280 sweeps its length is of order 3·r_N at all sizes. DEFI-R6's word "microscopic" (part C) must be read "at finite duration" as long as the stop is not established.
- Nothing in the programme status nor in the V347.1 framework. Physical gates remain at 0/7.
- Derived challenge: **DEFI-R8** — does viable condensation stop, and does it depend on β and τ?

## Weakest point

The question asked (stop or coarsening) is not decided; the only strong measured claim is the absence of a size effect, over three sizes, at a single set (β, τ, σ/r_N), measured on integer shells at small k (3 to 7).

## Reproduce

See the French note (§ Reproduire): same commands.

## Hostile review

An AI sub-agent, briefed with only the note, the scripts, the outputs and the cited references, reviewed the first version. Three blocking points retained: (1) "the scale is set by r_N" was true by construction (dimensional analysis) and contradicted "it grows": title, point 2 and verdict rewritten, the central question becomes whether c(t) stops; (2) L₁ cut at k ≤ 20 is not the same estimator from one size to another: L₁c (fixed cut in k·r_N) becomes the headline estimator; (3) the text announced seeds still running: figures resynchronised with the final output. Minor points retained: rule fidelity confirmed by the reviewer (only difference: initial d ≤ r, no consequence), clipped validation declared indirect, engine B "compatible" rather than "verifies" (B above A on all six shells), overlapping starts between sizes, window effect quantified, mobility-arm S_max given, fragility of L_peak.
