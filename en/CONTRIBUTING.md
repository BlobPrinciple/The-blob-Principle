🇫🇷 [Version française](../CONTRIBUTING.md) · 🇬🇧 English

# Contributing to the Blob Principle laboratory

Thank you for wanting to test the Blob Principle. This document sets out the rules, taken from the canonical framework of V347.1 (Book III, § III.2).

## 1. First of all

1. Read the [status block](PROGRAMME_STATUS.md): **TOE demonstrated: NO**. Any contribution that contradicts it without proof will be rejected.
2. Read the [contribution agreement (CLA)](CLA.md). Any contribution integrated into the corpus implies its acceptance.
3. Identify the **open research problem (RO)** you are attacking, or open a "Critique" *issue* if you are contesting an existing result.

## 2. Types of contribution

| Type | What to provide |
|---|---|
| **Proof** (towards [T]) | Complete statement, all hypotheses declared, proof, reference to the definitions of V347.1 / V346 |
| **Refutation** (towards [R] or [FAIL]) | Counterexample or argument, reproducible; a clean refutation is a complete result |
| **Replication / measurement** (towards [M] or [CERT]) | Code, environment, data or deterministic generator, **seeds**, **SHA-256 fingerprints**, negative test, DEV / CONFIRMATORY / HELD-OUT separation |
| **Confirmatory** | Everything above **plus a second independent engine** |
| **Methodological critique** | Precise point, targeted page or file, consequence for a status |
| **Reading, translation, popularisation** | Reports of unclear passages, proposed clarifications, translations |

Any contribution that changes a status comes with a **supersession report**: which statement, which old status, which new status, and why.

## 3. Epistemic labels

[T] theorem · [CERT] finite certificate · [M] measurement · [DEV] development · [H] hypothesis · [OPEN] open · [FAIL] failure · [R] retracted · [EXT] external validation · [ARCH] archived model · [A] axiom · [DEF] definition · [METH] method.

Rules: failures are shown first; nothing retracted is resurrected; no identification with a physical object (photon, graviton, Standard Model, ΛCDM…) is admitted in a formal statement before the confrontation book.

## 4. Procedure

1. **Issue** — open an *issue* with the appropriate template ("Attack on an open research problem", "Critique / refutation", "Replication", "Question").
2. **Discussion** — the author and the community examine the approach before the heavy work.
3. **Pull request** — place your files in `contributions/RO-xx_your-name/` (or `contributions/critique_your-name/`). Tick the CLA acceptance box in the description.
4. **Review** — adversarial review, modelled on the tribunal of eight reviewers.
5. **Integration** — the author decides on integration into the corpus and on any change of status. The contributor is listed in [CONTRIBUTORS.md](CONTRIBUTORS.md) and cited in the master that integrates their contribution.

## 5. What will not be accepted

- Direct modification of the original corpus files (masters, books): they are frozen and timestamped. Contributions go in `contributions/`.
- A claim without reproducibility, or the promotion of an analogy to an identity.
- Code submitted under an incompatible licence, or of which you are not the author.
- Any presentation of a contribution as a distinct theory claiming authorship of the Blob Principle.
- **Unverifiable work.** Every contribution must be checkable by a third party: files actually present in the PR, quoted values traceable in the corpus (file and line), and a command that reproduces the result. Batch-generated submissions lacking these elements are closed without review on the merits. Using an AI is welcome, provided you declare it and have checked what you submit yourself.

## 6. Conduct

Criticise ideas, never people. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
