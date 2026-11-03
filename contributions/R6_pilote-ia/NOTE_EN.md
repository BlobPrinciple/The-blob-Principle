🇬🇧 English · 🇫🇷 [Version française](NOTE.md)

# DEFI-R6 — The web without viability: what belongs to nucleation, to mobility and to viability

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. Note by the laboratory's AI pilot (Claude, Anthropic), scheduled session of 3 November 2026, under delegation from Rudolphe Mirante. Not reviewed by a person. The French version is the reference.

## Object

The V346 master (XXV.2, pp. 644–645; PDF 692–693) calls the "nodes + voids" structuring of the simulated cosmic web "specific to viability", with a P_max/median ratio that "grows with N" (≈ 630 at N = 5,000, ≈ 1,900 at N = 20,000) and voids "growing with N and specific to viability". The DEFI-R5 note (`contributions/R5_pilote-ia/NOTE_EN.md`, E4) showed that the "mobility without viability" control in the archived file reproduces most of the effect. DEFI-R6 asks what, in the web, belongs to multi-site nucleation, to mobility and to viability.

Sources: `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json` (the archived file, 4 arms, N = 1,000 to 20,000, 3 to 8 seeds); `blob gravite colab.py` in the same folder (the 25 May "position mobility" engine: `relax_positions`, `local_S`, κ = 6.6, β = 0.30, τ = 0.50; V346 XXV.1 p. 642). The script that produced the web file **is missing from the corpus** (R5 note, E4).

## Result in brief

1. **[T] + [M], archived file.** The growth of P_max/median with N is the kinematic scaling of a fixed-shape density modulation, not a growing structure: the relative amplitude P_max/N² is constant from N = 1,000 to 20,000 (log-log slope 0.01 ± 0.04 for the multi-site Blob, 0.04 ± 0.04 without viability), and the median stays at shot noise (median/N ≈ 1.0 to 1.1 up to N = 15,000). The file does contain a small-scale viability signal: power at intermediate k (k ≈ 6 to 12), absent or much weaker without viability, which raises the median at N = 20,000.
2. **[M], reconstructed four-arm campaign (reconstructed seeds, archived engine, 8 seed configurations, N = 1,000 to 20,000).** At 5 and 20 sweeps, nucleation carries 89 to 99% of the large-scale amplitude; [H] if the archive had a duration of that order (which cannot be established without its script), the same would hold for it; mobility without viability erodes it (at most 1 seed in 8 going up, at all sizes and durations); viability increases it and deepens the voids (8 seeds out of 8 everywhere). The viability share grows with duration: at N = 2,500, nucleation carries only 70% of the amplitude after 80 sweeps.
3. **[M], viability alone.** From a uniform start, viability alone creates voids (+0.025 after 20 sweeps, +0.074 after 80, +0.128 after 320, N = 2,500; +0.156 after 80 sweeps, N = 5,000) and a P(k) peak at k = 3 to 5, a length of about 3 times the connection radius r_N: a model scale, not a cosmic scale; mobility without viability does nothing of the kind. The amplitude reached (P_max/N² ≤ 0.011) stays at least 14 times below that of the seeds.

**Verdict.** "Specific to viability" does not hold for the master's P_max/median figure: in the file, that effect (the k = 1 or 2 mode) is already present without viability, and in the reconstruction it is set by nucleation. Viability does have its own measurable, small-scale action: it condenses and deepens voids, even without seeds, this action grows with the duration of the dynamics, and it is also visible in the archived file (power at intermediate k). This condensation is partly built into the engine's local rule (ln(1 + triangles) of the moved vertex alone rewards local density). "The excess grows with N" is not evidence of growing structure. No status change.

## A. Re-reading the archived file

**Identity [T].** For N points drawn independently from a density ρ on [0,1]³ and A(k) = Σ_j exp(2πi k·x_j),

E |A(k)|² = Σ_j Σ_l E exp(2πi k·(x_j − x_l)) = N + N(N − 1) |ρ̂(k)|².

Proof: the N diagonal terms equal 1; the N(N − 1) cross terms factorise by independence into ρ̂(k)·ρ̂(k)* (with points assigned to grid cells, ρ̂ is that of the cell law; the identity is unchanged). Hence, for a density shape that does not depend on N, P_max/median ≈ [1 + (N − 1)|ρ̂(k_max)|²] / [1 + (N − 1)|ρ̂(k_med)|²] grows linearly in N as long as the median stays at shot noise. Blob configurations are not independent draws: the identity is the reference, the constancy measured below is the fact.

**Measurement [M]** (`r6_archive.py`, output `r6_archive_sortie.txt`):

| N | seeds | P_max/median, multi-site | P_max/N², multi-site | P_max/N², no viability | P_max/N², single site | median/N, multi-site |
|---|---|---|---|---|---|---|
| 1,000 | 8 | 131 ± 11 | 0.133 ± 0.011 | 0.117 ± 0.010 | 0.165 ± 0.002 | 1.02 |
| 2,500 | 8 | 335 ± 26 | 0.137 ± 0.011 | 0.126 ± 0.011 | 0.157 ± 0.002 | 1.02 |
| 5,000 | 6 | 662 ± 73 | 0.138 ± 0.015 | 0.129 ± 0.015 | 0.153 ± 0.001 | 1.04 |
| 10,000 | 5 | 1,329 ± 180 | 0.141 ± 0.018 | 0.134 ± 0.018 | 0.152 ± 0.001 | 1.06 |
| 15,000 | 4 | 2,032 ± 279 | 0.148 ± 0.021 | 0.141 ± 0.021 | 0.149 ± 0.001 | 1.09 |
| 20,000 | 3 | 2,060 ± 242 | 0.129 ± 0.015 | 0.124 ± 0.017 | 0.149 ± 0.001 | 1.26 |

(standard errors over seeds). Log-log slopes over all seeds: P_max/median 0.972 ± 0.039 (multi-site), 1.039 ± 0.042 (no viability), 0.926 ± 0.008 (single site); P_max/N² 0.014 ± 0.037, 0.044 ± 0.042, −0.033 ± 0.004. The peak is at k = 1 or 2 (the largest box scale) in every seed.

Consequences for XXV.2:
- "The excess grows with N (≈ 630 at N = 5,000 → 1,900 at N = 20,000)": this is the shot-noise normalisation. The relative amplitude of the structure does not grow. [M]
- The dip at N = 20,000 comes from the median: on the same seeds 0 to 2, proportionality from N = 15,000 would give ≈ 2,410; the amplitude is the same (0.1295 vs 0.1294) and the median goes from 1.08·N to 1.26·N. This rise exists only with viability (multi-site 1.26; single site 1.25; no-viability control 1.02). [M]
- Viability-only signal (`r6_archive.py`, mean P(k)/N): at k = 10, 2.0 / 4.9 / 9.1 (multi-site, N = 5,000 / 10,000 / 20,000) vs 1.0 / 1.2 / 1.8 without viability; at k = 8, 9.0 / 21 / 46 vs 2.2 / 4.7 / 13. For the single site, a bump moves to larger k as N grows (among k = 6, 8, 10, 12, 15, maximum of P/N at k = 6 for N = 5,000 and at k = 10 for N = 20,000), roughly like 1/(2.9·r_N) (5.1; 8.0). [M] for the values; [H] for the link with the r_N scale, also seen in part C.
- Estimator: this table averages the per-seed ratios (662 at N = 5,000; 2,060 at N = 20,000); the master and the R5 note take the ratio of the mean spectrum (635; 1,879). [M]
- The voids "resist filling": for a fixed density shape, the fraction of empty cells decreases with N anyway, the more slowly the more concentrated the density; the no-viability control decreases almost the same way (0.921 → 0.743). [M]
- Pairing by seed (same seed keys in the file): viability adds to P_max/N² +0.016 ± 0.002 at N = 1,000, then +0.011, +0.009, +0.007, +0.006, +0.005 ± 0.002 at N = 20,000, all pairs positive; to voids, +0.015 to +0.027 (all pairs positive, as in E4). [M] That both arms share the initial configuration is an assumption: the script is missing.

## B. Reconstructed four-arm campaign

**Protocol (reconstructed, declared as such).** The producing script is missing; the protocol follows V346 XXV.2 ("K = 8 seeds of varied ages", "positions mobile under viability Metropolis") and the conventions inferred from the archived file:
- measurements (`r6_mesures.py`): voids = fraction of the 20³ = 8,000 empty cells (the archived Poisson follows exp(−N/8,000): 0.883 at N = 1,000, 0.083 at N = 20,000); P(k) = |FFT|² of counts on a 64³ grid, averaged over shells round(|k|) = 1 to 31 (the archived Poisson is ≈ N at every k); my Poisson arm gives 0.882 and median/N = 1.00;
- seeds: 8 uniform centres, ages a ~ U(0.2; 1), sizes ∝ a³, Gaussian clouds of standard deviation 0.12·a, brought back into [0,1]³ by `np.clip` as in the engine; 0.12 was chosen because, frozen, it gives voids close to the file's at N = 1,000 (0.929 vs 0.921–0.937); clipping puts 24% of the initial points exactly on a face (10 to 42% depending on the configuration, N = 2,500), artificial sheets that weigh on k = 1 and on the voids; the initial degree of the seeds (49 to 85) is far from κ = 6.6;
- dynamics: `relax_positions` and `local_S` **imported as is** from `blob gravite colab.py`, on the geometric graph of radius `rgg_radius(N, 6.6)`; `sweeps` × ⌊N/4⌋ proposals;
- arms paired by seed (same initial configuration): **frozen** (no dynamics), **mobile** (`viab=False`), **viab** (`viab=True`), **poisson** (frozen uniform);
- 8 seed configurations (the same at every size N: "8/8" stands for only 8 realisations); N = 1,000, 2,500, 5,000, 10,000, 20,000 at 5 sweeps; 20 sweeps at N = 2,500 and 5,000; 80 sweeps at N = 2,500.

**Results [M]** (`r6_campagne.py`, `r6_analyse.py`, output `r6_analyse_sortie.txt`). Amplitude A = P_max/N²; paired differences, mean ± standard error, number of seeds out of 8 where the difference is positive:

| N | sweeps | A frozen | A mobile | A viab | nucleation share | ΔA mobility | ΔA viability | Δvoids mobility | Δvoids viability |
|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 5 | 0.150 | 0.146 | 0.156 | 0.96 | −0.0041 ± 0.0007 (0/8) | +0.0098 ± 0.0013 (8/8) | −0.0028 (0/8) | +0.0050 (8/8) |
| 2,500 | 5 | 0.149 | 0.147 | 0.153 | 0.97 | −0.0022 ± 0.0003 (0/8) | +0.0065 ± 0.0010 (8/8) | −0.0049 (0/8) | +0.0101 (8/8) |
| 5,000 | 5 | 0.150 | 0.149 | 0.154 | 0.98 | −0.0016 ± 0.0003 (0/8) | +0.0051 ± 0.0008 (8/8) | −0.0050 (0/8) | +0.0112 (8/8) |
| 10,000 | 5 | 0.151 | 0.150 | 0.153 | 0.99 | −0.0007 ± 0.0002 (1/8) | +0.0030 ± 0.0005 (8/8) | −0.0041 (0/8) | +0.0100 (8/8) |
| 20,000 | 5 | 0.151 | 0.150 | 0.152 | 0.99 | −0.0005 ± 0.0001 (1/8) | +0.0021 ± 0.0003 (8/8) | −0.0037 (0/8) | +0.0063 (8/8) |
| 2,500 | 20 | 0.149 | 0.140 | 0.167 | 0.89 | −0.0085 ± 0.0013 (0/8) | +0.026 ± 0.004 (8/8) | −0.017 (0/8) | +0.036 (8/8) |
| 5,000 | 20 | 0.150 | 0.144 | 0.163 | 0.92 | −0.0059 ± 0.0011 (0/8) | +0.019 ± 0.003 (8/8) | −0.017 (0/8) | +0.040 (8/8) |
| 2,500 | 80 | 0.149 | 0.118 | 0.210 | 0.70 | −0.031 ± 0.005 (0/8) | +0.092 ± 0.010 (8/8) | −0.047 (0/8) | +0.106 (8/8) |

"Nucleation share" = per-seed mean of (A frozen − A poisson)/(A viab − A poisson). "Viability" = viab − mobile, the comparison the archived file allows; viab − frozen is also positive everywhere (8/8, except 7/8 for voids at N = 1,000).

Reading:
- Nucleation sets the large-scale structure; at 5 sweeps the dynamics changes it by less than 4% (at most 1.6% at N ≥ 10,000, where the mean vertex displacement is only 0.010 to 0.017). [M] This "share" mostly measures how little dynamics has elapsed: it is not a causal share, and it ignores the (negative) mobility term.
- Mobility without viability diffuses: it erodes the amplitude (at most 1 seed in 8 going up) and fills the voids (0 seeds in 8 going up), at all sizes and durations. [M]
- Viability sharpens: it increases amplitude and voids in every seed. Its effect grows with duration (×3 to ×4 from 5 to 20 sweeps, ×14 from 5 to 80 sweeps at N = 2,500 for the amplitude). [M]
- The archived file's void excess over its control (+0.024 at N = 2,500; +0.027 at N = 5,000) lies here between 5 and 20 sweeps (+0.010 → +0.036; +0.011 → +0.040). [M] If the archive had a duration of the same order (not established; the calibration depends on s, on the seed model and on the engine), its large-scale structure would be carried at least 89% by nucleation. [H]
- The arms do not move equally: 55 to 61% of vertices displaced in viab vs 46% in mobile at 5 sweeps (review). [M]
- Edges: the engine clips steps to [0,1] (non-periodic box). The check was done only from a uniform start (part C); for the seeds it is missing. [OPEN]

## C. Viability alone, without seeds

Same dynamics, uniform initial configuration (`--init poisson`):

| N | sweeps | voids frozen | voids mobile | voids viab | A viab (A frozen) | P_max/median viab | peak k, viab (8 seeds) |
|---|---|---|---|---|---|---|---|
| 2,500 | 20 | 0.733 | 0.732 | 0.757 | 0.0013 (0.0005) | 3.2 | 4–5 |
| 2,500 | 80 | 0.733 | 0.732 | 0.805 | 0.0044 (0.0005) | 10.7 | 4 |
| 2,500 | 320 | 0.733 | 0.732 | 0.860 | 0.0106 (0.0005) | 25.6 | 3–4 |
| 5,000 | 80 | 0.535 | 0.536 | 0.691 | 0.0022 (0.0002) | 10.7 | 5 |

- Viability alone condenses: it deepens voids (8/8 seeds everywhere) and produces a P(k) peak at k = 3 to 5, absent from the frozen and mobile arms. [M]
- This peak follows the connection radius: after 80 sweeps, k = 4 at N = 2,500 and k = 5 at N = 5,000, ratio 1.25 for r(2,500)/r(5,000) = 1.26; the length is about 2.9·r_N in both cases (review). It is a microscopic model scale (radius, step 0.3·r), not a cosmic scale: it does not contradict the master's finding of no large-scale "characteristic length". [M] for the positions, [H] for the interpretation. The drift with time (mean k ≈ 4.5 → 4 → 3.6 at N = 2,500, on integer shells) is thin. [M, weak]
- Edges: without viability, 10% of vertices end exactly on a face (320 sweeps, N = 2,500), a clipping artefact; with viability, the share within r of a face drops (0.43 → 0.32): viability depletes the edges, an edge effect too. The reviewer checked with its own code that the void excess persists on interior cells (+0.064 vs +0.073 overall) and that the peak persists in the sub-box [0.15; 0.85]³; check not deposited here, a periodic box remains to be done. [M] (review)
- Amplitudes stay small: after 320 sweeps, A = 0.011, 14 times below the seeds (0.15); P_max/median = 26 vs ≈ 250 to 440 for the seeds at the same N. [M]

## Second implementation

Part A: every table cell, the slopes and the paired differences were recomputed by the reviewer with its own code, in agreement.

Parts B and C: `r6_second_moteur.py` rewrites, with no code shared with part B or with the archived engine, the seeds, the dynamics (cell-based neighbourhoods, recoded local viability, PCG64 generator on other seeds) and the measurements (voids by unique cells, P(k) by `histogramdd` and full `scipy.fft.fftn`, exact amplitude of shells 1 and 2 by direct sum over points). It draws other seed realisations: absolute levels differ (A frozen 0.115 vs 0.150, seed scatter), paired differences are comparable. Of 20 comparisons (5 configurations × 4 differences: N = 1,000, 5,000, 10,000 at 5 sweeps; N = 2,500 at 20 sweeps; uniform start at 80 sweeps), 17 agree within 2 combined errors; three differ by 2.1 to 2.6 combined errors: the two void differences at N = 10,000 (same sign, same order) and the mobility amplitude difference from a uniform start (+2·10⁻⁵ vs −7·10⁻⁵, of order 10⁻⁴ and close to zero in both implementations). The signs of all non-zero effects and all trends are reproduced, including the uniform start (voids 0.807 vs 0.805; peak at k = 3–4). This second implementation checks the coding, not the model: same rule, same constants, same s, same clipping.

## What this changes

- In the master, if it is reissued: XXV.2 and XXV.3 cannot call the structuring measured by P_max/median "specific to viability", nor say that "the excess grows with N" in the sense of a growing structure. What the data support: a large-scale structure present without viability (set by nucleation in the reconstruction), sharpened by viability, eroded by mobility alone; and a viability-specific condensation at the scale of a few r_N, visible in the archived file as well as without seeds.
- Nothing changes in the programme status or in the V347.1 armature, which does not use these values. Physical gates remain at 0/7.
- Derived challenge: **DEFI-R7** — viable condensation: a model scale or endless coarsening?

## Weakest point

Part B rests on a **reconstruction**: the seed model (Gaussian shape, ages, sizes, clipping that puts 24% of points on the faces), the duration of the dynamics and the choice of the gravity engine for the web are assumptions; the nucleation share depends strongly on duration (99% at 5 sweeps, 70% at 80) and is not a causal share. Part A does not depend on the reconstruction. The box is not periodic, as in the archived engine.

## Reproduce

See the French version, § Reproduire (same commands). About 2 h 30 of computation on 2 cores in total; numpy, scipy, no numba. All campaign JSON files are deposited.
