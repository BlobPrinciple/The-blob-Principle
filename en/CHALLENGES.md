🇫🇷 [Version française](../DEFIS.md) · 🇬🇧 English

# The Blob challenges — “Break the Blob”

> **TOE demonstrated: NO.** The Blob Principle does not ask to be believed. It asks to be **tested**.
> Each challenge below is a real open problem of the programme. Succeeding at one — including by **refuting** a claim — advances science, and your name goes on the [Honour roll](#honour-roll).

**Golden rule:** a clean refutation is worth as much as a proof. The programme has already retracted dozens of its own claims; it invites you to continue.

To take up a challenge: open an *issue* with the appropriate template, cite the challenge code (e.g. `DEFI-R1`), then deposit your work in `contributions/`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## The guiding thread: the Blob cosmogony, and how to prove it

Every challenge serves a single goal, stated by the author: make the Blob a strong TOE candidate, then a TOE. Today it stands at level 1 (reproducible mathematical model); the distance to cover is known and divided into four steps, detailed in [AI_PILOT.md](AI_PILOT.md#the-proof-path):

- **P1** — unify the cosmogony: a single dynamics derived from Ω⁰ up to the G0 sector;
- **P2** — close gate G0 / continuum;
- **P3** — pass the physical gates (0/7) through confrontation with reality;
- **P4** — external validation (G6);
- **T** — cross-cutting: read, translate, explain, replicate, hunt errors, try to break the Blob.

**The challenges evolve.** Every accepted contribution is entered in the [advances log](ADVANCES_LOG.md); a closed challenge opens at least one other, closer to the guiding thread; a refutation opens the challenge “repair or abandon” the affected branch. Leave the Blob more tested than you found it.

### Challenge status

<!-- ETAT-DEFIS:DEBUT (généré par outils/defis.py, ne pas modifier à la main) -->
*Status as of 2026-11-07 — challenges v1.15.*

| Challenge | Proof-path step | State | Latest event |
|---|---|---|---|
| DEFI-L1 | T | open | — |
| DEFI-L2 | T | open | — |
| DEFI-L3 | T | open | — |
| DEFI-L4 | T | open | — |
| DEFI-L5 | T | open | — |
| DEFI-R1 | T | replicated | 2026-10-06: SELFTEST: 4/4 on a third-party machine, numpy 2.5.3 |
| DEFI-R2 | P2 | open | — |
| DEFI-R3 | T | open | 2026-10-15: [T]+[M] the archived V109 engine (V346 pp. 291–292) overcounts triangles by +1.4% to +2.7% when the added edge touches the removed one; the current canonical engine is not affected |
| DEFI-R4 | P1 | open | — |
| DEFI-R5 | T | open | 2026-10-23: [M] six JSON ↔ V346 master inconsistencies: table M-7.1 (p. 173), N = 1000 row copied from N = 3000 (JSON: 2.847 ± 0.082, 5 seeds); area law (pp. 259–260): "σ² ∝ V^≈1" against 3.23 in the JSON, verdict depending on the window; A1.5 (p. 560): expression evaluated as 0.0982 instead of 0.00981, δ₀ = 0.252 [T] against 0.159 [T*] in the JSON; cosmic web (pp. 644–645): the control without viability reproduces most of the effect called "specific to viability"; ρ* "4.8–5.0 stable" (p. 1203) against 4.630 at N = 8,000; III.3.6 (p. 255): standard deviation and standard error mixed; four minor discrepancies |
| DEFI-R6 | T | open | 2026-11-03: [T]+[M] archived file: P_max/N² constant from N = 1,000 to 20,000 (slope 0.01 ± 0.04), the growth of P_max/median is kinematic; viability signal at intermediate k; [M] reconstructed four-arm paired campaign (archived engine): at 5–20 sweeps nucleation carries 89 to 99% of the amplitude, mobility alone erodes it, viability increases it and deepens voids (8/8), share growing with duration; viability alone from uniform: voids +0.025 → +0.128, peak at k = 3–5 ≈ 1/(2.9·r_N) |
| DEFI-R7 | T | open | — |
| DEFI-M1 | P2 | open | — |
| DEFI-M2 | P2 | open | — |
| DEFI-M3 | P1 | open | 2026-10-15: [T] mitosis + fixed-|E| exchanges conserve M − N (mean degree < 2 from Ω⁰); [CERT] at M = N − 1, π concentrates on disjoint triangle islands: the 'most economical option' for RO-24 is refuted for the fixed-|E| engine |
| DEFI-M4 | P1 | open | — |
| DEFI-M5 | P1 | open | — |
| DEFI-M6 | P1 | open | — |
| DEFI-M7 | P1 | open | 2026-10-15: [M] canonical engine: newborn degree relaxes in 8 to 16 sweeps, no growth from N = 250 to 4,000; cost of a birth proportional to N; [OPEN] newborn triangle mass unresolved (−3.0 ± 2.0 at 512 sweeps) |
| DEFI-M8 | P1 | open | 2026-10-20: [T] at fixed k, the Gibbs attachment G*(A | C) ∝ π_{N+1,M+k}(C + v_A), derived from S_sim with no new parameter, attains the bound of proposition C and uniquely minimises KL at birth; its weights vary only with the edges among targets and the sum of their degrees (anti-preferential triadic closure); [CERT] abstract graphs, N + 1 ≤ 7, 39 transitions: no gain over uniform in 25 cases, gain at the best k from 0 to 0.41; in the 5 cases where G* gains, relaxation slowed by 25 to 44%; anti-Gibbs attachment relaxes fastest in 5 cases out of 6; k not derived |
| DEFI-M9 | P1 | open | 2026-10-16: [M] body of the newborn's mass law indistinguishable from the population's after 16 to 256 sweeps (N = 250 to 2,000, 200 births per size); [M] slow tail: 6 to 7% of newborns in the massive decile up to 1,024 sweeps (10% expected), 8.5% at 2,048; [M, partial] massive decile largely shared between chains on 9 clouds out of 10, and avoiding the cube's boundaries; [OPEN] role of age |
| DEFI-M10 | P1 | open | — |
| DEFI-M11 | P1 | open | 2026-10-20: [CERT] exact map, 102 cases with N + 1 ≤ 7: where G* gains at birth it slows relaxation in 50 cases out of 57 (45 out of 47 for a gain ≥ 10⁻³), anti-Gibbs speeds it up in 44 out of 57; [M] Monte Carlo N = 8 to 64, M + k = 2(N + 1), k = 4: global observables indifferent to the birth law after a few sweeps; half-time for the newborn's triangles at least of order N³ sweeps (0.5 at N = 8, 442 at N = 64), barely sensitive to the birth law of the family G_θ: 87 to 97% of the triangle mass is carried by an aristocracy of vertices |
| DEFI-M12 | P1 | open | 2026-10-31: [M] maximum clique measured: q_max ~ N^0.40 (mean degree 4, N = 17 to 129); q_eff underestimates by factor 1.3 to 2.5 |
| DEFI-M13 | P1 | open | 2026-10-30: [M] abstract graphs, mean degree 4, armature measure: the equilibrium law of T_v, measured by multicanonical sampling (two independent implementations, reviewer's third engine up to n = 97), is bimodal; the exit barrier from the aristocracy goes from 0.55 (n = 17) to 11.0 (n = 193); [M] DEFI-M12's t½ follows the residence time in the aristocracy measured without bias (ratio 1.5 to 1.9 from n = 25 to 193); [M] concave ln t½ ↔ barrier relation, slope 0.75 to 1.24 depending on the estimator: T_v is only an approximate reaction coordinate; no saddle left at λ = 66 (n = 65); [M] mean degree 6: no saddle up to n = 49, onset around n = 65; [H] exponent ≈ 0.6 = late crossover; [H] over n = 65 to 193 the barrier is compatible with √n; at n = 257 the predicted ln t½ ranges from 13.6 to 15.9 depending on the calibration, against 13.68 for exp(0.96·√n): asymptotics open |
| DEFI-M14 | P1 | open | 2026-11-06: [M] abstract graphs, mean degree 4, armature measure; predictions and criterion written before the measurement (local timestamp): at n = 257, two engines sharing no kernel code (four chains of 2·10⁷ sweeps) give an aristocracy sojourn of 2.02·10⁶ sweeps and ln t½ = 14.03 to 14.11; verdict under the criterion: undecided; the DEFI-M13 linear calibration (ln t½ = 15 to 16) is excluded, the exp(0.96·√n) law is exceeded by 30 to 41 %; [M] at n = 225 the √n law is verified (0.99); [H] an exploratory point at n = 289 (8.9·10⁶) continues the rise of the local slope (1.0 → 1.25 → 1.53): the √n law would be a law of the range |
| DEFI-M15 | P1 | open | 2026-10-31: [H] algebraically correct (factor 6/q²) but barrier = max not sum; t½ follows N³ (power law), not Arrhenius; δ(max clique) ≈ 0.40 |
| DEFI-M16 | P1 | open | — |
| DEFI-M17 | P1 | open | — |
| DEFI-M18 | P1 | open | — |
| DEFI-M19 | P1 | open | — |
| DEFI-G1 | P2 | open | — |
| DEFI-G2 | P2 | open | — |
| DEFI-G3 | P2 | open | — |
| DEFI-G4 | P2 | open | — |
| DEFI-T0 | T | open | — |
| DEFI-D1 | T | open | — |
| DEFI-D2 | T | open | — |
<!-- ETAT-DEFIS:FIN -->

Source: [docs/defis.json](../docs/defis.json), machine-readable version.

---

## Level 0 — Curious (no technical skills required)

| Code | Challenge | What to submit |
|---|---|---|
| **DEFI-L1** | **The reader.** Read the [V347.1 armature](../corpus/00_master_courant/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf) (29 pp.) and report the least clear passage. | A “Question” *issue*: page, sentence, what blocks you. |
| **DEFI-L2** | **The translator.** Translate a chapter of Book I of the armature (English, Spanish, Arabic, Chinese…) respecting the [locked lexicon](../index/LEXIQUE_FR-EN.md) — *viabilité* is *viability*, never *sustainability*. | The translation in `contributions/traduction_<langue>_<nom>/`. |
| **DEFI-L3** | **The illustrator.** Draw the cascade point → edge → triangle → tetrahedron, or the three times of the Blob, faithfully to the narrative (I.1 to I.6). | An image (PNG/SVG) and one sentence of explanation. |
| **DEFI-L4** | **The populariser.** Explain the Blob in 60 seconds (text, video, comic), **with the status block**: TOE demonstrated: NO. | The link or the file. |
| **DEFI-L5** | **The Builder.** On the [Grow your own universe](https://blobprinciple.github.io/The-blob-Principle/univers.html?lang=en) page, get a universe in one piece and regular (D < 0.50) at 80 vertices with **only 3 closure edges**. None of the 2,400 universes simulated by the lab achieves it; record to beat: D = 0.542 (seed 5215). | A comment in the [gallery of universes (#33)](https://github.com/BlobPrinciple/The-blob-Principle/issues/33): link, D, number of pieces. Checkable with `node outils/univers_batisseur.js`. |

## Level 1 — Coder, student, engineer

| Code | Challenge | Starting point | Success criterion |
|---|---|---|---|
| **DEFI-R1** | **The replicator.** Run the C2-R engine self-test on your machine. | `python3 corpus/07_complements/blob_c2r_autonome-2.py --selftest` (dependency: numpy) | “Replication” report: machine, versions, full output. Expected: `SELFTEST : 4/4`. *Verified on 6 October 2026 on a third-party machine (numpy 2.5.3): 4/4.* |
| **DEFI-R2** | **L = 6.** Complete the C2-R campaign at L = 6, inconclusive for lack of compute (about 17 % of the required budget). | Same script, `--all` then `--finalize` | Report with R̂, ESS, MCSE and decision of the frozen contract. Addresses **RO-12**. |
| **DEFI-R3** | **The second engine.** Rewrite **independently**, without reading the existing code, the sampler of the functional *S_sim(C) = log(1 + n_tri(C)) − βD(C)* and compare your invariants with the published ones. | Definitions in armature V347.1, II.0 and II.4; data in `corpus/04_donnees/` | Quantified deviations with error bars. Any divergence is a result. |
| **DEFI-R4** | **Nucleation.** Can the Blob be born from the strict void? Today: 0/40 seeds under both canonical engines. | Armature II.3, **RO-02** | A **preregistered** protocol (published before execution) on ≥ 30 seeds: P(Ω¹ \| Ω⁰) ≥ 0.9 from the strict void, **or** a clean negative bound. |
| **DEFI-R5** | **The error hunter.** Find a numerical inconsistency between a published result (JSON) and the master text that cites it. | `corpus/03_scripts/`, `corpus/06_campagnes_et_sauts/`, master V346 | File, page, cited value, actual value. |
| **DEFI-R6** | **The web without viability.** The V346 master (XXV.2) calls the "nodes + voids" structuring of the simulated cosmic web "specific to viability"; the "mobility without viability" control in the same file reproduces most of the effect, viability adding only a small void excess ([note](../contributions/R5_pilote-ia/NOTE_EN.md), E4). What sculpts the nodes and voids: multi-site nucleation, mobility or viability? | `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob_toile_results.json`, V346 master pp. 644–646 | A campaign with at least four arms (with viability, mobile without viability, frozen multi-site, Poisson), N ≥ 5,000 at two sizes, 8 seeds per arm, per-seed statistics, code and JSON published; or a proven argument. |
| **DEFI-R7** | **Viable condensation: a model scale or endless coarsening?** Under the archived mobility engine, viability alone, from a uniform start, deepens voids and produces a P(k) peak at k = 3–5, about 2.9 times the connection radius r_N; mobility without viability does not ([note](../contributions/R6_pilote-ia/NOTE_EN.md), part C). Does this condensation stop at a scale set by r_N, β and τ, or coarsen without end? Does it survive a periodic box? | `corpus/06_campagnes_et_sauts/Audit 25 mai — paliers et gravite/blob gravite colab.py` (`relax_positions`), V346 master pp. 642–645, [#47](https://github.com/BlobPrinciple/The-blob-Principle/issues/47) | Periodic box, uniform start, at least 3 sizes and 8 seeds per point, up to at least 1,280 sweeps: length L(t, N) with error bars, compared with r_N; or a proven argument. |

## Level 2 — Mathematician, physicist

| Code | Challenge | Open research problem | What counts as success |
|---|---|---|---|
| **DEFI-M1** | **The four points of SUP-1.** Bounded degree versus O(log N), order of limits, 3-torus versus cube with boundary, inconsistent labels (H1)–(H3). | [STATUS § 5](PROGRAMME_STATUS.md) | A supersession note that settles each of the four points. |
| **DEFI-M2** | **The spectral squeeze.** Can the same object satisfy the uniform ellipticity required by Delmotte (INF-1) and the non-elliptic framework of SUP-1? | [INF-1 audit](../corpus/02_portes_et_audits/audits_18-09-2026/) | Proof that the squeeze closes on an explicit class, **or** a demonstrated obstruction. |
| **DEFI-M3** | **Closure.** Mitosis alone never produces a triangle (no-go proven). Propose a **local** closure generator compatible with viability. | **RO-24** | An explicit generator, or a proof that no compatible local generator exists (which would kill the causal cascade). |
| **DEFI-M4** | **The σ₀ bit.** Show that the choice of polarity at the first scission cannot be derived from Ω⁰ and must remain an axiom — or derive it. | **RO-03** | An obstruction theorem, or an internal mechanism. |
| **DEFI-M5** | **The double scission.** Does every “scission into two opposite simplices” reduce to two successive mitoses? | **RO-04** | A demonstrated reduction, or a new operation made explicit. |
| **DEFI-M6** | **Persisting.** Give a definition of “persisting” independent of the mere fact that π > 0. | **RO-20** | A robust, non-arbitrary, computable criterion. |
| **DEFI-M7** | **The cost of the bridge.** After the birth of a vertex with its closure edges, how many Metropolis exchanges per edge are needed to return to π_N? On abstract graphs: 2.5 to 4.7 per edge (ε = 0.01, N = 5 to 7, [report](../contributions/RO-25_pilote-ia/REPORT_EN.md)). Does this cost stay bounded as N grows, on the Rips engine? | **RO-25** | A proven bound, or a multi-seed measurement with error bars up to N ≥ 500, showing a bounded or divergent cost. |
| **DEFI-M8** | **A non-arbitrary closure.** Mitosis alone cannot carry the cascade: ≈ κ̄/2 − 1 closure edges are needed per birth ([report](../contributions/RO-25_pilote-ia/REPORT_EN.md)). Derive from S_sim, without positing it, the attachment law of the new vertex that minimises the distance to π from birth. | **RO-24**, **RO-25** | The derived law and its distance at birth compared with uniform attachment, or a proof that no local law does better. |
| **DEFI-M9** | **The aristocracy of massive vertices.** On the canonical engine, a newborn's degree reaches the mean in 8 to 16 sweeps, but its triangle mass stays in deficit ([report](../contributions/RO-25_pilote-ia/DEFI-M7_REPORT_EN.md)). Does the newborn ever reach the typical mass, or does viability freeze an aristocracy of massive vertices? | **RO-25**, **RO-20** | The law of the newborn's incident triangles versus the population's, in total variation, with at least 200 births per size over at least three sizes; or a proven argument. |
| **DEFI-M10** | **The slow accession to the massive decile.** A newborn's mass law reaches the population's in 16 to 256 sweeps, except the tail: 6 to 7% of newborns are in the massive decile up to 1,024 sweeps, against 10% expected ([report](../contributions/RO-25_pilote-ia/DEFI-M9_REPORT_EN.md)). How many sweeps to reach 10%, does this time grow with N, and does the newborn reach the equilibrium mass of its position? | **RO-25**, **RO-20** | Share measured to ± 1 point (at least 1,000 births per size, two sizes) up to at least 16,384 sweeps, compared with the equilibrium mass of the position (independent chain, preferably in a periodic box); or a proven bound. |
| **DEFI-M11** | **Born right or relaxed fast.** The Gibbs attachment, derived from S_sim, exactly minimises the gap to π at birth, but slows relaxation by 25 to 44% in the five cases where it gains; anti-Gibbs attachment relaxes fastest in five cases out of six (abstract graphs, N ≤ 6; [report](../contributions/RO-25_pilote-ia/DEFI-M8_REPORT_EN.md)). Which attachment law minimises the bridge's total cost, and is it derivable from S_sim? | **RO-25**, **RO-24** | The law minimising relaxation time after birth (proven bound, or exact measurement up to N + 1 ≥ 8 and multi-seed on the canonical engine at N ≥ 250), compared with U, G\* and G_θ; or a proof that both criteria coincide asymptotically. |
| **DEFI-M12** | **The aristocratic slowness.** On abstract graphs with mean degree 4, a newborn takes longer and longer to acquire its equilibrium triangle mass: half-time from 0.5 sweep at N = 8 to 442 at N = 64, at least of order N³, possibly exponential; the mass is carried by an aristocracy of vertices ([report](../contributions/RO-25_pilote-ia/DEFI-M11_REPORT_EN.md)). Power law or exponential? | **RO-25**, **RO-20** | A proven bound (spectral gap, bottleneck), or a measurement up to N ≥ 128 at two or more densities and on the canonical engine at N ≥ 250, with error bars. |
| **DEFI-M13** | **The barrier of the dominant clique.** On abstract graphs with mean degree 4, under the armature measure, the time for a vertex to change its triangle rank grows as exp(0.96·√n) from n = 17 to 193 (neither a power law nor an exponential in n); the slowness follows λ = n/τ and the aristocracy is a dominant clique of size ≈ √n; at mean degree 6, growth is faster ([report](../contributions/RO-25_pilote-ia/DEFI-M12_REPORT_EN.md)). Why √n, and why not at mean degree 6? | **RO-25**, **RO-20** | A proof or refutation of an exp(Θ(√n)) barrier (bottleneck, conductance) and of a clique of size Θ(√n); an explanation of the ≈ 0.6 exponent at mean degree 6; or the same signature sought on the canonical engine at N ≥ 250. |
| **DEFI-M14** | **Does the √n law survive at n = 257?** On abstract graphs with mean degree 4, under the armature measure, the equilibrium law of T_v is bimodal and the exit barrier from the aristocracy, compatible with √n over n = 65 to 193, can still be measured at n = 257; depending on the calibration, it predicts ln t½ between 13.6 and 15.9 there, against 13.68 for the exp(0.96·√n) law ([report](../contributions/RO-25_pilote-ia/DEFI-M13_REPORT_EN.md)). Asymptotic law or crossover effect? | **RO-25**, **RO-20** | Residence time in the aristocracy (or t½) measured at n = 257 and beyond, with error bars; or a proven bound on the dominant-clique membership barrier; or a better reaction coordinate than T_v. |
| **DEFI-M16** | **After √n: the law of aristocratic slowness.** On abstract graphs with mean degree 4, under the armature measure, the sojourn in the aristocracy follows exp(0.96·√n) up to n ≈ 225, exceeds it by 30 % at n = 257, and an exploratory point at n = 289 indicates an acceleration ([report](../contributions/RO-25_pilote-ia/DEFI-M14_REPORT_EN.md)). What law beyond, what mechanism? | **RO-25**, **RO-20** | Sojourn at n ≥ 321 (two engines, equilibrium profile) and the form of the growth; or the exit mechanism; or a proven bound; decision criterion deposited publicly before the measurement. |
| **DEFI-M17** | **Regeneration of the binders.** The author proposes that renewing the binders before rupture extends a structure's viability ([clarifications of 26 October](debates/AUTHOR_CLARIFICATIONS_2026-10-26.md), P2). On abstract graphs of mean degree 4, compare two paired populations, one left to the canonical dynamics, one in which a fraction of the oldest links is replaced every k sweeps, at constant |E|. Does regeneration extend persistence, or merely postpone the rupture? First difficulty: regeneration must be a rule distinct from the canonical dynamics, targeted by link age and not by viability. | **RO-20**, **RO-25** | Paired campaign, 3 sizes and 8 seeds per point, scan over r and k, criterion deposited before the measurement; verdict: extension, postponement, or no effect. |
| **DEFI-M18** | **Kleiber versus √n: a power law at fixed λ?** The living follows power laws (Kleiber 1932: B ∝ M^(3/4); West, Brown and Enquist 1997: internal times in M^(1/4)). The engine gives an aristocratic sojourn in exp(0.96·√n) under the cooling λ = n/τ of axiom A4, and DEFI-M12 showed that at fixed λ the slowness disappears ([clarifications of 26 October](debates/AUTHOR_CLARIFICATIONS_2026-10-26.md), part 2). At fixed λ, is t(n) a power law, and with what exponent? | **RO-25**, **RO-20** | Five sizes spanning a factor of 10, two engines with no shared code, explicit power-versus-exponential test, criterion deposited before the measurement; or the n ↔ mass correspondence written down and the question declared ill-posed. |
| **DEFI-M19** | **The filter before matter.** The author proposes that viability sorts the possibles explored in t₁ and that only viable configurations enter t₂ ([clarifications of 26 October](debates/AUTHOR_CLARIFICATIONS_2026-10-26.md), P3). Write this filter as an object of the model, without presupposing what it must sort and without reducing it to "π > 0". | **RO-20**, **RO-21**, **RO-23** | A written definition, a pair of configurations with the same S_sim separated by the filter and not by π, and a consistency theorem with A4; or a demonstration that no such non-circular filter exists. |

## Level 3 — Specialist (gate G0)

| Code | Challenge | Open research problem |
|---|---|---|
| **DEFI-G1** | Uniform local margin on the typical Gibbs sector (GEN-4 *typical-set*) | **RO-13** |
| **DEFI-G2** | MARKED ↔ CONNECTED intertwiner in a declared Banach norm | **RO-14** |
| **DEFI-G3** | Convergence under removal of the regulator, projective limit | **RO-15** |
| **DEFI-G4** | Non-trivial fixed point and universality (C4, C5, C7) | **RO-16** |

## The trial of the 22 paradoxes — the debate is open

The narrative of the books *Du simplexe au complexe* gives a place to twenty-two great paradoxes. How many stand up to mathematics? Provisional verdict: **class A = 0**, B = 3, C = 14, D = 5. Case files: [debates/TRIAL_OF_PARADOXES.md](debates/TRIAL_OF_PARADOXES.md) · [#32](https://github.com/BlobPrinciple/The-blob-Principle/issues/32).

| Code | Challenge | Deliverable |
|---|---|---|
| **DEFI-D1** | **The juror** (level 0). Contest the classification of a paradox: too harsh or too generous. | A comment in [#32](https://github.com/BlobPrinciple/The-blob-Principle/issues/32): number, proposed class, argument, page cited. |
| **DEFI-D2** | **The advocate** (level 2). Move a paradox up one class — D → C: an explicit mechanism; C → B: a formal object defined in the armature; B → A: a [T] statement in the canonical sector — or prove it must move down. | A note in `contributions/`; candidates closest to class A: no. 5, 8 and 9 (**RO-03**, **RO-10**, **RO-26**). |

## The grand challenge — the open Tribunal

**DEFI-T0 — Break the Blob.** Find a **fatal** flaw: an internal contradiction, a hidden assumption that brings down an entire branch, a central result that is not reproducible. Argue it with the rigour of a journal reviewer.

Accepted refutations are entered on the **Wall of Refuters**, with the name of their author, in every master version that takes them into account.

---

## Honour roll

| Date | Contributor | Challenge | Result | Effect on the programme |
|---|---|---|---|---|
| 06/10/2026 | (opening verification) | DEFI-R1 | `SELFTEST : 4/4` on a third-party machine, numpy 2.5.3 | Reproducibility of the self-test confirmed |
| 16/10/2026 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M9 (RO-25) | [M] The newborn's mass deficit is concentrated in the massive tail, which is joined slowly; the massive decile is largely shared between independent chains ([report](../contributions/RO-25_pilote-ia/DEFI-M9_REPORT_EN.md), [#19](https://github.com/BlobPrinciple/The-blob-Principle/issues/19)) | Partial result; derived challenge DEFI-M10; status unchanged |
| 20/10/2026 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M8 (RO-24, RO-25) | [T] The Gibbs attachment derived from S_sim is the best genealogical law at birth (at fixed k); [CERT] yet it slows relaxation in the five cases where it gains ([report](../contributions/RO-25_pilote-ia/DEFI-M8_REPORT_EN.md), [#35](https://github.com/BlobPrinciple/The-blob-Principle/issues/35)) | Partial result; derived challenge DEFI-M11; status unchanged |
| 20/10/2026 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M11 (RO-25, RO-24) | [CERT] Being born right slows the bridge in 50 exact cases out of 57; [M] at large N, the newborn's accession to the equilibrium triangle mass takes at least of order N³ sweeps, whatever birth law was tested ([report](../contributions/RO-25_pilote-ia/DEFI-M11_REPORT_EN.md), [#37](https://github.com/BlobPrinciple/The-blob-Principle/issues/37)) | Partial result; derived challenge DEFI-M12; status unchanged |
| 2026-10-27 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M12 (RO-25, RO-20) | [M] The aristocratic slowness is neither a power law nor an exponential in n: at mean degree 4, t½ ≈ exp(0.96·√n) from n = 17 to 193, out-of-sample prediction verified; it follows the cooling λ = n/τ of the measure and the aristocracy is a dominant clique of size ≈ √n ([report](../contributions/RO-25_pilote-ia/DEFI-M12_REPORT_EN.md), [#41](https://github.com/BlobPrinciple/The-blob-Principle/issues/41)) | Partial result; derived challenge DEFI-M13; status unchanged |
| 2026-10-30 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M13 (RO-25, RO-20) | [M] The aristocracy barrier measured: the equilibrium law of T_v is bimodal, its saddle rises from 0.55 to 11.0 from n = 17 to 193, and DEFI-M12's t½ follows the residence time in the dominant clique; [H] over n = 65 to 193 the barrier is compatible with √n, the asymptotics remain open ([report](../contributions/RO-25_pilote-ia/DEFI-M13_REPORT_EN.md), [#43](https://github.com/BlobPrinciple/The-blob-Principle/issues/43)) | Partial result; derived challenge DEFI-M14; status unchanged |
| 2026-11-06 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M14 (RO-25, RO-20) | [M] Aristocracy sojourn measured at n = 225 and 257 by two engines: the √n law holds at 225 and is exceeded by 30 % at 257 (criterion written in advance: undecided); the DEFI-M13 linear calibration is excluded; [H] an exploratory point at n = 289 indicates an acceleration ([report](../contributions/RO-25_pilote-ia/DEFI-M14_REPORT_EN.md), [#48](https://github.com/BlobPrinciple/The-blob-Principle/issues/48)) | Partial result; derived challenge DEFI-M16; status unchanged |

## Wall of Refuters

| Date | Refuter | Challenge | What is refuted | Effect on the programme |
|---|---|---|---|---|
| 2026-10-15 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M3 (RO-24) | The "most economical option" proposed for RO-24: mitosis and fixed-\|E\| exchanges conserve M − N, and selection then fragments the graph into disjoint triangle islands ([report](../contributions/RO-25_pilote-ia/REPORT_EN.md)) | RO-24 stays open; any closure must create edges; derived challenges DEFI-M7 and DEFI-M8; no status change |
| 2026-10-15 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-R3 | The incremental triangle count of the archived V109 engine (V346 pp. 291–292): +1.4% to +2.7% overcount ([note](../contributions/R3_pilote-ia/NOTE_EN.md)) | [ARCH] script corrected; the canonical engine is not affected; status unchanged |
| 2026-10-23 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-R5 | Six passages of the V346 master contradicted by the JSON files they report: N = 1000 row of table M-7.1 copied from N = 3000; "σ² ∝ V^≈1" (recorded fit: 3.23); A1.5 bound evaluated ten times too high; web "specific to viability" although the control without viability reproduces most of the effect; "stable" ρ*; two error metrics mixed ([note](../contributions/R5_pilote-ia/NOTE_EN.md), [#39](https://github.com/BlobPrinciple/The-blob-Principle/issues/39)) | Corrections to be made to the master if re-issued; V347.1 framework untouched; derived challenge DEFI-R6; status unchanged |
| 2026-11-03 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-R6 | The web "specific to viability" whose "excess grows with N" (V346 XXV.2–XXV.3, pp. 644–646): the relative amplitude P_max/N² is constant from N = 1,000 to 20,000, the growth of P_max/median is only the shot-noise normalisation, and the large-scale structure is present without viability; viability keeps a small-scale action of its own ([note](../contributions/R6_pilote-ia/NOTE_EN.md), [#46](https://github.com/BlobPrinciple/The-blob-Principle/issues/46)) | Correction to be made to the master if re-issued; V347.1 framework untouched; derived challenge DEFI-R7; status unchanged |

*The next place is waiting for you.*

---

### What you gain

- **Permanent credit by name** in [CONTRIBUTORS.md](CONTRIBUTORS.md) and in the master version that integrates your contribution.
- **A citable record**: every version of the repository receives a Zenodo DOI.
- The satisfaction of having tested a candidate theory of everything — whether it holds or falls.
