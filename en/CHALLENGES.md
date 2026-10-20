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
*Status as of 2026-10-20 — challenges v1.7.*

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
| DEFI-R5 | T | open | — |
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
| DEFI-M11 | P1 | open | — |
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

## Wall of Refuters

| Date | Refuter | Challenge | What is refuted | Effect on the programme |
|---|---|---|---|---|
| 2026-10-15 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-M3 (RO-24) | The "most economical option" proposed for RO-24: mitosis and fixed-\|E\| exchanges conserve M − N, and selection then fragments the graph into disjoint triangle islands ([report](../contributions/RO-25_pilote-ia/REPORT_EN.md)) | RO-24 stays open; any closure must create edges; derived challenges DEFI-M7 and DEFI-M8; no status change |
| 2026-10-15 | The laboratory's AI pilot (Claude, Anthropic) — not reviewed by a person | DEFI-R3 | The incremental triangle count of the archived V109 engine (V346 pp. 291–292): +1.4% to +2.7% overcount ([note](../contributions/R3_pilote-ia/NOTE_EN.md)) | [ARCH] script corrected; the canonical engine is not affected; status unchanged |

*The next place is waiting for you.*

---

### What you gain

- **Permanent credit by name** in [CONTRIBUTORS.md](CONTRIBUTORS.md) and in the master version that integrates your contribution.
- **A citable record**: every version of the repository receives a Zenodo DOI.
- The satisfaction of having tested a candidate theory of everything — whether it holds or falls.
