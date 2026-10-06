🇫🇷 [Version française](../DEFIS.md) · 🇬🇧 English

# The Blob challenges — “Break the Blob”

> **TOE demonstrated: NO.** The Blob Principle does not ask to be believed. It asks to be **tested**.
> Each challenge below is a real open problem of the programme. Succeeding at one — including by **refuting** a claim — advances science, and your name goes on the [Honour roll](#honour-roll).

**Golden rule:** a clean refutation is worth as much as a proof. The programme has already retracted dozens of its own claims; it invites you to continue.

To take up a challenge: open an *issue* with the appropriate template, cite the challenge code (e.g. `DEFI-R1`), then deposit your work in `contributions/`. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Level 0 — Curious (no technical skills required)

| Code | Challenge | What to submit |
|---|---|---|
| **DEFI-L1** | **The reader.** Read the [V347.1 armature](../corpus/00_master_courant/BLOB_PRINCIPLE_MASTER_V347_1_ARMATURE_CANONIQUE.pdf) (29 pp.) and report the least clear passage. | A “Question” *issue*: page, sentence, what blocks you. |
| **DEFI-L2** | **The translator.** Translate a chapter of Book I of the armature (English, Spanish, Arabic, Chinese…) respecting the [locked lexicon](../index/LEXIQUE_FR-EN.md) — *viabilité* is *viability*, never *sustainability*. | The translation in `contributions/traduction_<langue>_<nom>/`. |
| **DEFI-L3** | **The illustrator.** Draw the cascade point → edge → triangle → tetrahedron, or the three times of the Blob, faithfully to the narrative (I.1 to I.6). | An image (PNG/SVG) and one sentence of explanation. |
| **DEFI-L4** | **The populariser.** Explain the Blob in 60 seconds (text, video, comic), **with the status block**: TOE demonstrated: NO. | The link or the file. |

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

## Level 3 — Specialist (gate G0)

| Code | Challenge | Open research problem |
|---|---|---|
| **DEFI-G1** | Uniform local margin on the typical Gibbs sector (GEN-4 *typical-set*) | **RO-13** |
| **DEFI-G2** | MARKED ↔ CONNECTED intertwiner in a declared Banach norm | **RO-14** |
| **DEFI-G3** | Convergence under removal of the regulator, projective limit | **RO-15** |
| **DEFI-G4** | Non-trivial fixed point and universality (C4, C5, C7) | **RO-16** |

## The grand challenge — the open Tribunal

**DEFI-T0 — Break the Blob.** Find a **fatal** flaw: an internal contradiction, a hidden assumption that brings down an entire branch, a central result that is not reproducible. Argue it with the rigour of a journal reviewer.

Accepted refutations are entered on the **Wall of Refuters**, with the name of their author, in every master version that takes them into account.

---

## Honour roll

| Date | Contributor | Challenge | Result | Effect on the programme |
|---|---|---|---|---|
| 06/10/2026 | (opening verification) | DEFI-R1 | `SELFTEST : 4/4` on a third-party machine, numpy 2.5.3 | Reproducibility of the self-test confirmed |

## Wall of Refuters

*Empty to date. It is waiting only for you.*

---

### What you gain

- **Permanent credit by name** in [CONTRIBUTORS.md](CONTRIBUTORS.md) and in the master version that integrates your contribution.
- **A citable record**: every version of the repository receives a Zenodo DOI.
- The satisfaction of having tested a candidate theory of everything — whether it holds or falls.
