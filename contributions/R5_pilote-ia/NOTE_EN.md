🇬🇧 English · 🇫🇷 [Version française](NOTE.md)

# DEFI-R5 — Six inconsistencies between corpus JSON files and the V346 master

*Laboratory AI pilot (Claude, Anthropic), 23 October 2026. Search split across four AI agents; the retained values are recomputed by two independent implementations; two-pass hostile review by a separate AI agent, whose blocking objections were incorporated. Not reviewed by a person. The French note is the reference text.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. No status change. None of the values at issue is carried over into the V347.1 framework, which is authoritative (its open research item RO-08 points to the V346 PDF range 1243–1274, which contains the E5 passage, without carrying over its ρ* value).

## Method

Text of the V346 master (1,918 pp.) extracted with `pdftotext -layout`. Pages are given as printed page numbers, with the PDF page in parentheses (offset 48, except for separately paginated volumes such as V292). The corpus holds 176 JSON files (165 distinct names). The 169 readable JSON files were compared with the passages reporting the same campaign: by file name when the master gives it, otherwise by content (script, N, seeds, date, values). Every derived quantity stated in the text (mean, ratio, σ, slope, arithmetic) was recomputed from the JSON. Rounding and standard-deviation conventions (ddof 0 or 1) that change no conclusion are not retained.

## Retained inconsistencies

**E1 — Table M-7.1 "Convergence d_s → 3", p. 173 (PDF 221).**
- Quoted: N = 1000, 20 seeds, 3.045 ± 0.026, deviation 1.5%; rows N = 260 and N = 400.
- JSON: `06_campagnes_et_sauts/SAUT 9 et 10 et 11/Manifestes v99 et addendum v102/EXPECTED_OUTPUT_v93_updated 2.json`, `ds_N1000` = 2.847 ± 0.082, 5 seeds, deviation 5.1%; `ds_N3000` = 3.045 ± 0.026, 20 seeds; no entry for N = 260 or N = 400.
- The N = 1000 row copies the N = 3000 row (quoted values). The master itself gives the JSON values on p. 225 (PDF 273, M-13.1 "V2 corrigée") and states on pp. 224–225 (PDF 272–273) that the N = 400 value "does not exist"; table M-7.1 keeps it (3.180 ± 0.036). From N = 300 to 1,000 the JSON does not increase (2.908; 2.887; 2.847, differences smaller than the error bars) before 3.045 at N = 3,000: table M-7.1, which concludes to a "confirmation [M] that d_s converges to 3", does not rest on these data.

**E2 — Area-law test, III.5.1, pp. 259–260 (PDF 307–308); table VII.1.3, p. 329 (PDF 377).**
- Quoted: σ²(n_K4) ∝ V^≈1.0 "intermediate regime", verdict "extensive, standard thermal"; σ² vs A ≈ 1.
- JSON: `06_campagnes_et_sauts/Test O2v4 projection 3D à 2D trou noir/loi aire results.json`, `fits`: σ² ∝ V^3.230 (R² 0.789), σ² ∝ A^7.462 (R² 0.929). The master itself prints this JSON on pp. 322–323 (PDF 370–371).
- The rule of the printed script (pp. 303–304, PDF 351–352: `alpha < 0.78` area law, `alpha > 1.2` super-extensive) classifies 3.23 as "super-extensive". ≈ 1 is recovered only by dropping the first two bins, an undeclared window (bins 3 to 6: 0.980; 3 to 7: 0.923); bins 4 to 6 give 0.774, below the area-law threshold. Depending on the window, the exponent ranges from 0.77 (bins 4 to 6) to 7.97 (bins 1 to 3), 3.23 over all bins: neither the "extensive" label nor the absence of an area law is established by these data. σ² ∝ A^≈1 is recovered by no window of three or more bins (closest: 1.74).

**E3 — Appendix A1.5, cascades 2 and 3, pp. 559–560 (PDF 607–608), status [T].**
- Quoted: "(0,30 × 0,2 × 8 × 0,414)/(2 × 0,125 × 81) = 0,0982"; "with D_min^obs = 0,35: Nβ|ΔD| ≤ 0,035"; "δ₀ ≥ 0,350 − 0,098 = 0,252 > 0".
- Computation: the printed expression equals 0.00981; with D_min = 0.35, 0.00350. Both printed evaluations are ten times the expression. The reviewer found no definition of the constants in the master that makes 0.0982 correct (it would need c₇ = 2 instead of 0.2).
- JSON: `06_campagnes_et_sauts/BLOB SCALING V30 DU 23 AVRIL 2026/EXPECTED_OUTPUT_v93_updated.json` (version "v93-consolidated-April2026", not cited by the appendix, which says it is "reproduced from v105"): `delta0_analytic` = 0.159 [T*], `delta0_measured` = 0.274 [M].
- Scope: the evaluation error is internal to the master and certain. If the expression is right, the bound becomes δ₀ ≥ 0.340, stronger than 0.252; the [T] is weakened only if the expression itself is wrong. The disagreement with the JSON sets two versions of the computation against each other (0.252 [T] against 0.159 [T*]). The sign δ₀ > 0 holds in every case. The value 0.252 is reused in step 2 of theorem LIT (A1.4, p. 559, PDF 607).

**E4 — Cosmic web, XXV.2, pp. 644–645 (PDF 692–693).**
- Quoted: "large-scale structuring specific to viability", P_max/median ≈ 1900 (Blob) against 1.2 (Poisson); "large voids, growing with N and specific to viability"; "up to 6 seeds".
- JSON: `06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json`. The Blob and Poisson values in the text match. The "mobility without viability" control, announced in the protocol and present in the file, is not reported:

| N | P_max/median Blob | without viability | single site | voids Blob | without viability | paired void excess |
|---|---|---|---|---|---|---|
| 5,000 | 635 | 619 | 739 | 0.861 | 0.834 | +0.027 (6/6) |
| 10,000 | 1,296 | 1,263 | 1,458 | 0.808 | 0.785 | +0.024 (5/5) |
| 20,000 | 1,879 | 2,277 | 2,380 | 0.763 | 0.743 | +0.020 (3/3) |

- Most of the "nodes + voids" effect remains without viability. Viability adds only a small void excess, of the same sign in every seed pair (+0.015 to +0.027 from N = 1,000 to 20,000); for P_max/median, the Blob exceeds the control by 13% at N = 1,000 and by 3 to 5% from N = 2,500 to 10,000, then the control exceeds the Blob at N = 15,000 (+4%) and 20,000 (+21%). "Specific to viability" does not hold; lacking a frozen multi-site control, the file cannot separate nucleation from mobility. The XXV.3 synthesis (pp. 645–646) is affected. Minor: the file has 8 seeds at N = 1,000 and 2,500.

**E5 — CXL.7.2, p. 1203 (PDF 1251).**
- Quoted: "ρ* ≈ 4,8–5,0 stable", under "Non-variété confirmée à N=8000".
- JSON: `04_donnees/DERNIER JSON/palier_1000-2.json`, `palier_2000-2.json`, `palier_4000.json`, `palier_8000.json` (one campaign, 4 seeds; κ = 6.6 and date 2 July 2026 according to `env-2.json` in the same folder): ρ* = 4.993; 4.800; 4.803; 4.630 for N = 1,000, 2,000, 4,000, 8,000; at N = 8,000 none of the 4 seeds reaches 4.8 (4.565 to 4.690). `03_scripts/SCRIPTS DIVERS BLOB/Grand N — paliers 32000/palier_32000.json`, a separate 8-seed campaign: 4.421.
- The master itself recalibrates the constant on ρ = 4.42 on p. 1214 (PDF 1262) and declares "outdated" the computation done with ρ = 4.9.

**E6 — Local collapse, III.3.6, p. 255 (PDF 303).**
- Quoted: "⟨d_H^loc⟩ = 1.87 ± 0.24, statistically compatible with 2 (the exact value 2.00 lies within the 1σ error bar)"; "the effect exceeds 40σ".
- JSON: `06_campagnes_et_sauts/Test O2v4 projection 3D à 2D trou noir/local collapse results.json`, `stats.dense`: 1.8685 ± 0.2418, standard deviation over n = 515 vertices.
- Two metrics in the same paragraph: the Welch t values of the text (−25.33; −44.37) are recovered (−25.36; −44.40) with the per-vertex standard error, at which 2 lies 12.3 standard errors away. The 515 vertices come from 5 seeds: per-vertex standard errors are pseudo-replicates, and "compatible with 2 at 1σ" and "40σ" cannot be computed at the seed level from the JSON, which does not give the dense class per seed. The ordering of means Dense < Bulk < Void holds.

## Minor discrepancies

- **m1** — M-3.2, p. 136 (PDF 184): "factor 2.25× to 3.25×"; the Blob/null ratios in the table range from 2.51 (N = 300) to 3.25 (N = 3,000): 2.25 is the gain (+225%) read as a ratio. The "36.8σ" at N = 3,000 corresponds to n = 4, the JSON's `SNR = 41` to n = 5; no n is documented.
- **m2** — Same table, row N = 10,000 (49,204 ± 5,050 against 17,510 ± 249, [M]): the manifest `EXPECTED_OUTPUT_v93_updated 2.json` has `tri_ratio_N10000` = null, "PENDING"; no JSON found in the corpus contains this measurement.
- **m3** — Test B, triangle → tetrahedron cascade, p. 261 (PDF 309): "5 seeds"; `scout results.json` and the script printed on p. 305: 4 seeds, 56 points. b = 2.041 and R² = 0.534 match.
- **m4** — Volume V292, PART CCI, section C, p. 5 of the volume (PDF 1375): "Écart final : 0,004". `03_scripts/simulations/blob_total_V286_results.json` and the printed table give 0.014 at the final level (0.331 against 0.345); 0.004 is the script's criterion, the difference of the means over levels 1 to 3 (0.0042). Misleading label, conclusion unchanged.

## Verified agreements

Re-run by the pilot, matching up to rounding: `invariants_500k.json` and `banc_*.json` (§122.6, p. 1063); `alpha_v2_*.json` (§122.1, p. 1059: the 12 slopes recomputed from the points, α = 0.126 ± 0.008 as a weighted mean, 1.3σ and 0.4σ); `courbures_KL.json` (§123.1, p. 1065: weighted slopes −0.032 ± 0.011 and −0.012 ± 0.013); `queue_mort.json` and `rondeur_v2.json` (§124.1–§124.2, pp. 1072–1073: 7.1σ, 7.1σ, 10.6σ; slopes and differences); `campagne_blob_ir.json` (21 June appendix, pp. 1134–1135: means and spreads of the five phase-1 levels); `blob_paliers_N*.json` (PART XX, pp. 614–616: separations 8.3σ to 5.6σ and 1.8σ to 9.9σ). These checks were confirmed by the reviewer.

Reported as matching by the search agents, not re-run by the pilot: `alpha_C*.json` (§121.2), `calibration ds results.json`, `dh ds convergence.json`, the lock and building-block JSON files (PART VII), `blob_dims_N*.json`, `blob_hierarchie_seed1.json`, `frontiere_V280_results.json`, the other sections of `blob_total_V286_results.json`.

## Integrity findings, outside the challenge

- `blob_paliers_GLOBAL.json`, cited as data for PART XX, contains only the N = 1,000 level (the per-level files, which match, contain the rest).
- `campagne_blob_ir.json`, cited as a source, contains only phase 1 (N ≤ 100,000); phase 2 (250,000 to 2,000,000) is absent.
- Seven files are truncated (invalid JSON): `palier_N100_modeblob_seed1.json`, `palier_N100_modeblob_seed1-2.json`, `palier_N200_modeblob_seed1.json`, `palier_N1000_modeblob_seed1.json` ("Sauts 2 a 35"), `palier_N100_modeblob_seed1.json` and `palier_N200_modeblob_seed1.json` ("Manifestes v99 et addendum v102"), `saut9_N2000_seed1.json`.
- In `SAUT 35V3/`, every snapshot has E = 0 and n_tri = 0 (`first_edge_step` null), whereas the identically named `saut35v3_RAPPORT.json` in "Sauts 2 a 35" reports thousands of tetrahedra. None of these files is cited by the master.

## What this changes

Nothing in the programme status or in the V347.1 framework. Two substantive corrections should go into the master if it is re-issued: E1 (table M-7.1 should carry the M-13.1 values) and E4 (the "nodes + voids" structuring cannot be called specific to viability; only small excesses — voids, and P(k) at small N — are, in these data). [OPEN] A frozen multi-site control and per-seed statistics would tell what, in the web, is due to nucleation, mobility and viability.

## Reproduce

```
python3 contributions/R5_pilote-ia/r5_audit.py          # implementation A (numpy): r5_audit_sortie.json
python3 contributions/R5_pilote-ia/r5_audit_second.py   # implementation B (pure Python, fractions, scipy): checks the values of this note
```

A few seconds. Reference outputs: `r5_audit_sortie.txt`; `ACCORD COMPLET` on the last line of `r5_audit_second_sortie.txt`. Codes E1 to E6 and m1 to m4 are those of this note.
