🇫🇷 [Version française](RAPPORT.md) · 🇬🇧 English

*Translation produced with DeepL and corrected by the pilot; the French original prevails.*

# RO-25 / RO-24 — The growth → Gibbs bridge: what mitosis alone cannot carry

*Contribution from the laboratory's AI pilot (Claude, Anthropic), 15 October 2026. Filed like any other contribution, as an `ia-assistee` issue. Checked by the pilot itself (exact computation, plus a cross-check by a second, independent implementation, `networkx`); **no human review at this stage**.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It sharpens one open research question (RO-25) and refutes an option proposed for another (RO-24).

## 1. The question

The V347.1 armature (§ II.0) separates three strata: **A_gen** (genealogical growth by mitosis μ, variable N), **A_Gibbs** [ARCH] (fixed N and |E|, measure π_N ∝ exp(N·S_sim/τ), Metropolis edge exchanges), **B** (triangulations of T³). The bridge A_gen → A_Gibbs is open research question **RO-25**:

> *A joint dynamics at variable N, combining mitosis/closure and relaxation, such that the conditional law at fixed N reproduces, or derives, the measure π_N of A_Gibbs.*

For closure (**RO-24**, § II.5), the armature proposes, as the *"most economical option to test"*, to **interleave the already existing edge dynamics of A_Gibbs between growth events**, rather than inventing a third law.

This report tests these two statements.

## 2. Framework and declared hypothesis

- S_sim(C) = log(1 + n_tri(C)) − β·D(C), where D is the standard deviation of the degrees divided by the mean degree (A3); π_{N,M}(C) ∝ exp(N·S_sim(C)/τ) (A4); β = 0.30, τ = 0.50 (ARCHIVE / PRODUCTION values).
- μ adds a leaf vertex and **one** edge (§ II.3, Theorem 5.2-a); μ⁻¹ is the collapse of a leaf (Theorem 3.4).
- The A_Gibbs edge exchange removes one edge and adds another: it preserves N and |E| = M (§ II.0; historical script, V346 pp. 291–292 printed, pp. 339–340 of the PDF).
- **[H-abs]** The computations concern **abstract** labelled graphs, without the Rips geometric constraint (pool of edges at distance < 1.5 r) of the historical engine. The [T] statements of §§ 3.1 and 3.2 do not depend on it; the exact measurements of §§ 3.3 and 3.4 do.

## 3. Results

### 3.1 Density invariant [T]

**Proposition A.** Under any composition of μ, μ⁻¹ and fixed-|E| exchanges, the quantity **M − N is conserved**.

*Proof.* μ: (N, M) ↦ (N + 1, M + 1); μ⁻¹: (N, M) ↦ (N − 1, M − 1); an exchange: (N, M) ↦ (N, M). ∎

**Corollary A1 [T].** From Ω⁰ (N = 1, M = 0), every trajectory satisfies **M = N − 1**: the mean degree is 2 − 2/N < 2 forever. The production regime of A_Gibbs, where the mean degree is of the order of κ₀ (5.5 to 8 in the scans; 6.6 "canonical"; V346 p. 148 printed, p. 196 of the PDF), is **unreachable**: the conditional law at fixed N of this dynamics lives on the sector M = N − 1, disjoint from that of π_N. The total-variation distance is 1 as soon as the sector of π_N has a number of edges other than N − 1, that is, for any target mean degree greater than 2.

**Corollary A2 [T].** To reach a mean degree κ̄ asymptotically, one must create on average **κ̄/2 − 1 edges per newborn vertex beyond the one mitosis provides** (2.3 for κ̄ = 6.6). These edges can come neither from μ nor from the exchange: a generator that changes M − N is **necessary**.

*Numerical check [M]:* 200 random trajectories of 400 steps (μ, μ⁻¹, exchanges; seed 20261015, N up to 172): 0 violations of M = N − 1.

### 3.2 On the sector M = N − 1, selection fragments [T] + [CERT]

**Lemma B [T].** A graph with N vertices and N − 1 edges has c = 1 + β₁ connected components (β₁: cyclomatic number). A triangle forces β₁ ≥ 1, hence **c ≥ 2**; a tetrahedron K₄ (β₁(K₄) = 3) forces **c ≥ 4**. ∎

In other words, on the only sector the economical option can reach, **every triangle disconnects the graph**. Yet the measure π_{N,N−1} rewards triangles:

| N | graphs (M = N − 1) | π(at least one triangle) | π(connected graph) | E_π[n_tri] |
|---|---|---|---|---|
| 4 | 20 | 0.9757 | 0.0243 | 0.98 |
| 5 | 210 | 0.99688 | 2.9·10⁻³ | 1.00 |
| 6 | 3,003 | 0.99990 | 7.7·10⁻⁵ | 1.84 |
| 7 | 54,264 | 0.9999993 | 4.5·10⁻⁷ | 3.73 |

[CERT] complete enumeration; no exception to Lemma B among the 57,497 graphs. Independently cross-checked (`networkx`) for N = 5 and 6: same probabilities to within 10⁻¹⁵.

**Consequence.** The option "mitosis + interleaved A_Gibbs exchanges" does not produce the cascade in a connected carrier: under the viability weight, it produces **disjoint triangular islands**. This is the opposite of the narrative (Book I, ch. 5). The most economical option proposed for RO-24 is therefore **refuted** for the fixed-|E| engine. This does not refute RO-24: it says that closure must **create edges**.

### 3.3 Genealogical obstruction [T] + [CERT]

Call a growth kernel G **genealogical** if it gives birth to a vertex without rewiring any old edge (the induced subgraph on the old vertices is preserved). This is what a genealogy in the strong sense requires.

**Proposition C [T].** For any genealogical kernel G and any M′:

TV(π_{N,M} G, π_{N+1,M′}) ≥ TV(π_{N,M}, R#π_{N+1,M′}) ≥ 1 − P_{π_{N+1,M′}}(deg(new vertex) = M′ − M) > 0,

where R is the restriction to the N old vertices. *Proof.* R is deterministic and R#(π_{N,M}G) = π_{N,M}; total variation does not increase under a measurable map; the mass whose restriction does not have M edges lies outside the support of π_{N,M}. The last inequality is strict because π_{N+1,M′} charges graphs in which the degree of the new vertex differs (full support, 0 < M′ < N(N+1)/2, N ≥ 2). ∎

**No purely genealogical growth reproduces π exactly.** Exact bounds, minimised over the number k of edges of the new vertex:

| N → N + 1 | M → M′ (best k) | lower bound on TV |
|---|---|---|
| 4 → 5 | 3 → 6 (k = 3) | 0.313 |
| 4 → 5 | 4 → 7 (k = 3) | 0.477 |
| 5 → 6 | 5 → 9 (k = 4) | 0.613 |
| 5 → 6 | 7 → 11 (k = 4) | 0.551 |
| 6 → 7 | 9 → 13 (k = 4) | 0.675 |

[CERT]; the 4 → 5 case is cross-checked with `networkx` (0.31306).

### 3.4 What works: growth with closure, then relaxation [T] + [CERT]

Consider the "mitosis + closure" kernel: the vertex is born linked to k distinct old vertices drawn uniformly (k = 1: μ alone; k ≥ 2: k − 1 closure edges), followed by t Metropolis exchanges at fixed |E| (uniform, hence symmetric, proposal; acceptance min(1, π′/π)).

**[T] (classical result for finite reversible Markov chains, applied here).** The exchange kernel leaves π_{N,M} invariant (symmetric proposal, Metropolis acceptance). On abstract graphs it is irreducible (two sets of M edges are linked by at most M exchanges, each reducing their symmetric difference) and aperiodic (rejections of positive probability as soon as π is not uniform); the law after t exchanges therefore converges to π_{N,M} whatever the initial law. The bridge thus "derives" π_N **in the limit of time-scale separation**, at a finite cost for finite N.

Exact measurements (propagation of the law, no sampling):

| N, M after birth | k | states | TV at t = 0 | t for TV ≤ 0.1 | ≤ 0.01 | ≤ 0.001 | exchanges per edge (TV ≤ 0.01) |
|---|---|---|---|---|---|---|---|
| 5, 7 | 2 | 120 | 0.865 | 9 | 33 | 61 | 4.7 |
| 6, 11 | 3 | 1,365 | 0.787 | 9 | 27 | 50 | 2.5 |
| 7, 14 | 3 | 116,280 | 0.853 | 19 | 61 | 117 | 4.4 |

Checks: stochasticity and π-invariance verified to within 10⁻¹⁴.

**The price [T, from Proposition C].** This convergence goes through the rewiring of old edges: the genealogy of the **vertices** survives, that of the **edges** is erased by relaxation. One must choose between a strict genealogy of the edges and the exact measure π_N; one cannot have both.

## 4. Proposed effect on the programme (no change of status)

- **RO-24:** the option "interleave the A_Gibbs exchanges" is refuted for the fixed-|E| engine (§§ 3.1–3.2). Any viable closure must create edges, at a rate of about κ̄/2 − 1 per birth.
- **RO-25:** exactly "reproducing" π_N by genealogical growth is impossible (§ 3.3); "deriving" π_N by growth-with-closure then relaxation is possible at finite N (§ 3.4), at the cost of the edge genealogy. The research remains **open**: the relaxation cost as N grows is unknown (the three measured points show no law).

## 5. What is established, what remains to be checked, the weakest point

- **Established:** Propositions A and C and Lemma B (elementary proofs above); exact values of §§ 3.2–3.4 on abstract graphs.
- **To be checked:** everything, by a person; the transposition to the geometric Rips engine (hypothesis H-abs), where the edge pool is restricted; the behaviour of the relaxation cost beyond N = 7.
- **Weakest point:** hypothesis H-abs. The corpus also measures a "stepwise" growth (V346 p. 209 printed, p. 257 of the PDF, `etape4_mitose_paliers.py`, node N3) in which each new vertex attaches to an existing structure and which produces tetrahedra in a connected space: that model already contains, in fact, a multi-edge closure rule, which is consistent with Corollary A2 but has not been re-run here.

## 6. Next step on the proof path (P1)

1. **DEFI-M7** — the cost of the bridge: does the number of exchanges per edge needed after a birth stay bounded as N grows, on the Rips engine?
2. **DEFI-M8** — a non-arbitrary closure: derive from S_sim the attachment law of the new vertex (k and targets) that minimises the distance to π from birth, rather than positing it.

## Reproduce

```bash
python3 contributions/RO-25_pilote-ia/pont_croissance_gibbs.py            # 1 to 3 min, writes resultats.json
python3 contributions/RO-25_pilote-ia/pont_croissance_gibbs.py --rapide   # without the N = 7 case of part D
```

Python 3.13, numpy 2.5.3, scipy 1.18.1. SHA-256 fingerprints: see `EMPREINTES_SHA256.txt` at the repository root.
