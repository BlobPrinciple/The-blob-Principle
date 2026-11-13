🇬🇧 English summary · 🇫🇷 [Rapport complet en français](RAPPORT.md) (authoritative)

# November 2026 cross-audit campaign — status on 13 November

> **Mandatory status block**
> TOE demonstrated: **NO**. Gates G0–G5: **open**. G6: **external**. Physical gates: **0/7**.
> This deposit changes **no status** of the programme. It has not been reviewed by any outside person.

**Author of the Blob Principle:** Rudolphe Mirante. **Execution and counter-audit:** the laboratory's AI pilot (Claude, Anthropic). **Frozen protocols and partial recounts:** ChatGPT (OpenAI). This summary is an AI-written translation; the French report prevails.

## What this is

Between 1 and 13 November 2026, the author asked for his cosmogony to be tested branch by branch, without embellishment. Each idea was turned into a computable model and tested under common rules: protocol frozen before computing, SHA-256 fingerprint, predictions written before execution, negative controls, two readings of the results, cross-check by a second program. Laboratories are numbered C-1 to C-146, plus three exact notes (BP-R1, BP-EQ1, BP-IM1).

## Failures first

- Relational closure alone does not select the tetrahedron: it drives every connected graph to a clique (27,475 connected graphs checked).
- In a spring model, mitosis does not sustain itself; three coefficient-free cadence laws are refuted.
- Koide: twelve operators tried, all failed. Born rule: every geometric route tested failed or stalled.
- Edge, triangle and tetrahedron as cosmic fractions by plain counting: 6 failures out of 6.
- A rotating load does not detach a carrier better than a fixed one: 0 configuration out of 120.
- A second tetrahedron does not hold back the least-bonded carrier, and the two tetrahedra pass through each other in 144 runs out of 144: excluding point carriers does not exclude overlapping simplices.

## What holds

- Edge mitosis yields an extended three-dimensional space with N = 2^g and no small-world collapse [CERT].
- A purely genealogical rule generates that regular fabric [CERT].
- Protected modes at matter–antimatter contacts are neutral and spectrally separated [T].
- A classical local Blob cannot reproduce quantum correlations [T].
- Without double inheritance of links nothing closes: the graph stays a tree [T].
- A bond breaks durably only when the source resumes while the structure re-closes, above a power threshold; friction raises that threshold four- to eightfold without removing it [CERT, not cross-checked].

## Morning of 13 November

Three statements by the author opened three leads, formalised by ChatGPT and independently re-computed by the pilot.

- **Equity of exchanges.** Among complete graphs, K4 is the only one whose imbalance modes equal its circulation modes (3 and 3) [T]. But the equality is equivalent to "links = 2 × (elements − 1)", which every wheel graph satisfies: it does not single out the tetrahedron.
- **Nesting in the void.** Exposed edges go 3, 4, 3, 0 as the faces of a tetrahedron are assembled; four equal non-overlapping elements under equal compression form a regular tetrahedron, three dimensions being assumed. The cause of the first encounter remains open.
- **Casimir-type bath.** In a Gaussian bath pinned on the boundaries, two tetrahedra attract, more so face to face. All 96 values reproduced to 4 × 10⁻¹⁵. Caveats: the interaction equals minus the mutual information between the two boundaries, so it is attractive by construction; the orientation preference survives mesh refinement but is about half of what the protocol mesh shows; the well has no bottom at contact; at range the attraction is of the order of thermal agitation, so there is no capture without dissipation.

## Retractions and wrong predictions

Seven statements by the pilot were withdrawn and at least twenty-three recorded predictions turned out wrong on 12 and 13 November; all are listed in the French report and the notebooks.

## Later additions (13 November, after the first deposit)

- **C-147c — a 1/r law from the fabric, under one condition.** On the true plateau fabric of the edge-mitosis tissue, a conserved quantity passed from thread to thread follows u = Q / (4πDr) with D = 4, isotropic within 1 % beyond seven cells. An elastic spring network fails (1/r² and faster); any loss gives a screened profile. ChatGPT found the same coefficient independently. What matter emits that is conserved is not given by the cosmogony: the gravitation lock stays open.
- **C-145 — the disagreement under stop rule A1 is settled.** It came from an unstated convention: the gap below which two contacts are treated as one collision. A multi-contact collision is not the limit of successive collisions. One statement of the pilot is retracted; ChatGPT froze a new protocol (PR-4 bis), not executed.
- **C-148c — the cadence of mitosis against the measured expansion.** "Matter slows mitosis" **fails as a level law** (expansion would have been slower in the past). It passes as a braking law acting on the derivative of the cadence: with dc/dt = −κ·c^(2−n)·ρ, DESI DR2 gives **n = 2.04 ± 0.07**, which is flat ΛCDM rewritten (the cosmological constant is the cadence of empty tissue); this is a dictionary, not a derivation. The expansion history alone cannot tell whether matter brakes; structure growth excludes the pure brake and is compatible with dc/dt = (c∞² − c²)/3 − 4πG·ρ (indicative). Under the condition of C-147c, this brake and the 1/r law are one law by Gauss's theorem. One wrong prediction is declared.

No lock changes. Details: notebook of 12–13 November, sections 69 to 73.

## Limits

714 indeterminate runs out of 3,312 (PR-3) and 632 out of 2,160 (PR-2) are counted as such. PR-3 has not been cross-checked; PR-2 only in part, with one unresolved disagreement. Three-dimensional space, masses, the cohesion potential, the energy reserve and the Gaussian bath are assumed, not derived. ChatGPT's reports and programs are not deposited here; their fingerprints are in `chatgpt/EMPREINTES.md`.

## How to check

```
cd contributions/campagne-novembre-2026_pilote-ia/calculs
python3 bp_r1_eq1_im1_contre_audit.py
python3 c146_contre_audit.py
gunzip -k c145c.json.gz && python3 c145c_analyse.py
```
