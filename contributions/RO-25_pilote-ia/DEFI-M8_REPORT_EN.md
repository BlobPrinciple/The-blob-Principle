🇬🇧 English · 🇫🇷 [Version française](DEFI-M8_RAPPORT.md)

# DEFI-M8 — The attachment law derived from S_sim: here, being born right does not make a good bridge

*Contribution by the laboratory's AI pilot (Claude, Anthropic), 20 October 2026. Filed like any contribution, as an `ia-assistee` issue. Checked by the pilot (exact enumeration, cross-checked by a second independent implementation) and reviewed by a second AI agent acting as a hostile reviewer (three corrections accepted, see § 5); **no human review at this stage**. The French version is authoritative.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status. It partially answers DEFI-M8 (RO-24, RO-25), on abstract graphs and for at most 7 vertices.

## 1. The question

DEFI-M8 (docs/defis.json) asks to derive from S_sim, without positing it, the attachment law of a newborn vertex (number of edges and targets) that minimises the gap to π at birth, and to compare it with uniform attachment; or to prove that no local law does better than uniform.

Authoritative sources: V347.1 framework, § II.0 (strata A_gen, A_Gibbs, B, p. 10); RO-25 box (p. 11: "a joint dynamics at variable N […] such that the conditional law at fixed N reproduces, or derives, the measure π_N"; falsifier: "no local Markovian extension simultaneously has the intended genealogy, the announced conditional measure and a non-arbitrary closure rule"; our translation); RO-24 box (§ II.5, p. 15); axioms A3–A4 (p. 18): S_sim(C) = log(1 + n_tri(C)) − β·D(C), β = 0.30; π_N ∝ exp(N·S_sim/τ), τ = 0.50; theorem 4.7-b (p. 13): τ·KL(ν‖π_N) is a Lyapunov functional. Starting point: [REPORT_EN.md](REPORT_EN.md), proposition C (§ 3.3) and the measurements of § 3.4.

## 2. Setting

- **[H-abs]** as in REPORT_EN.md: **abstract** labelled simple graphs, without the Rips constraint of the historical engine; D = population standard deviation of degrees / mean degree.
- The newborn vertex v (label N) is born linked to a set A of k old vertices: from sector (N, M) to sector (N + 1, M + k). k = 1 is mitosis alone; k ≥ 2 adds k − 1 closure edges.
- A kernel is **genealogical** if it rewires no old edge (REPORT_EN.md § 3.3). We write π = π_{N,M}, π′ = π_{N+1,M+k}, R the restriction to the N old vertices, B_k(C) = Σ_{|A|=k} π′(C + v_A).
- **Uniform attachment U**: A uniform among the C(N, k) subsets.
- **Gibbs attachment G\*** (heat bath on the newborn's neighbourhood): G\*(A | C) = π′(C + v_A) / B_k(C). It contains no new parameter: it is the conditional law of π′ given the old graph and the newborn's degree k.

## 3. Results

### 3.1 G\* is the best possible genealogical law [T]

**Proposition D.** For every k and every genealogical kernel G attaching the newborn to k old vertices (any G(· | C), local or not):

1. TV(πG, π′) ≥ TV(π, R#π′), with equality if and only if, for every C, the quantities π(C)·G(A | C) − π′(C + v_A) have the same sign (in the wide sense) for all subsets A;
2. **G\* attains equality**: the bound of proposition C (REPORT_EN.md § 3.3, first inequality) is **sharp**;
3. KL(πG ‖ π′) = Σ_C π(C)·log(π(C)/B_k(C)) + Σ_C π(C)·KL(G(· | C) ‖ G\*(· | C)); G\* is therefore the **unique** minimiser of the Kullback-Leibler divergence at birth.

*Proof.* (1) States of π′ where deg(v) ≠ k receive zero mass and contribute 1 − P_{π′}(deg v = k), exactly the mass of R#π′ outside the M-edge sector. For fixed C, with a = π(C) and b_A = π′(C + v_A), the triangle inequality gives Σ_A |a·g_A − b_A| ≥ |a − B_k(C)|, with equality if and only if the terms share a sign. Summing over C gives 2·TV(π, R#π′). (2) For g = b/B_k(C), a·g_A − b_A = b_A·(a/B_k(C) − 1): common sign. (3) Direct expansion; the second term is non-negative and vanishes if and only if G(· | C) = G\*(· | C) for every C (π charges every state). ∎

**Corollary D1 [T].** Uniform attachment is already optimal in total variation as soon as, for each C, π(C)/C(N, k) lies either above or below all the values π′(C + v_A). In that case **no attachment law does better than uniform at birth**: the whole gap comes from the law of the old graph, which no genealogical kernel touches.

**Proposition E (anatomy of G\*) [T].** Let T(C) be the number of triangles, d_u the degrees, Q(C) = Σ_u d_u², e_C(A) the number of edges among the targets and s_A = Σ_{a∈A} d_a. Then

G\*(A | C) ∝ exp( (N + 1)/τ · [ log(1 + T(C) + e_C(A)) − β·D_A ] ),  D_A = √(Q_A/(N + 1) − μ²) / μ,

with μ = 2(M + k)/(N + 1) and Q_A = Q(C) + 2·s_A + k + k². At fixed C, the weight of a subset A varies with A only through **two local statistics**, e_C(A) and s_A (T(C), Q(C), M and N enter as global constants); it increases with e_C(A) (each edge among targets closes a triangle) and decreases with s_A (high-degree targets increase the dispersion D). G\* is thus an **anti-preferential triadic closure**, derived from S_sim and not posited; its exponent (N + 1)/τ grows with N. *Proof.* The newborn creates exactly e_C(A) triangles; degrees become d_a + 1 on A and k at v, hence Q_A; T(C), Q(C) and M are fixed by C. ∎

The normalisation B_k(C) sums over the C(N, k) subsets: the law is not local in the strict sense, but its weights are.

### 3.2 What G\* gains at birth [CERT]

Exact enumeration of all graphs of the sectors concerned (39 transitions: N = 4, 5, 6, four to six values of k per starting sector; up to 352,716 states after birth).

- G\* attains the bound of proposition C in all 39 cases (gap ≤ 2·10⁻¹⁶); its KL is less than or equal to that of U in all 39 cases.
- The condition of corollary D1 holds exactly in **25 cases out of 39** (the 16 cases k = 1 or k = N, and 9 of the 23 intermediate cases): there G\* gains nothing over U. In a 26th case (N = 6, M = 9, k = 2), the gain is 3·10⁻¹².
- At the best k of each starting sector (sectors 4, 5 and 5, 8, where the best k equals N and G\* and U coincide, are omitted):

| N, M → M′ (best k) | TV at birth, U | TV at birth, G\* (= bound) | gain |
|---|---|---|---|
| 4, 3 → 6 (k = 3) | 0.723 | 0.313 | 0.410 |
| 4, 4 → 7 (k = 3) | 0.632 | 0.477 | 0.155 |
| 5, 5 → 9 (k = 4) | 0.744 | 0.613 | 0.131 |
| 5, 7 → 11 (k = 4) | 0.608 | 0.551 | 0.057 |
| 6, 9 → 13 (k = 4) | 0.744 | 0.675 | 0.069 |
| 6, 11 → 16 (k = 5) | 0.614 | 0.606 | 0.008 |

- For 2 ≤ k < N, under G\*, the newborn attaches to a clique (all its targets linked to one another) with probability 0.15 to 0.99 depending on the case (0.04 to 0.83 under U), except in cases (N, M, k) = (5, 5, 4) and (6, 9, 5), where no clique of that size exists in the starting sector.

### 3.3 But, here, the best birth slows the bridge down [CERT]

After birth, t Metropolis swaps at fixed |E| (uniform proposal, acceptance min(1, π′/π)); exact propagation of the law. Number of swaps for TV ≤ 0.01:

| N, M, k | states | U | G\* | first t with TV(G\*) > TV(U) | first t with KL(G\*) > KL(U) |
|---|---|---|---|---|---|
| 4, 5, 2 | 120 | 33 | 33 | 8 | 7 |
| 5, 8, 3 | 1,365 | 27 | 26 | never | never |
| 6, 11, 3 | 116,280 | 61 | 57 | never | (not computed) |
| 4, 3, 3 | 210 | 268 | **387** | 23 | 19 |
| 4, 4, 3 | 120 | 27 | **35** | 3 | 3 |
| 5, 5, 4 | 5,005 | 130 | **163** | 8 | 8 |
| 5, 7, 4 | 1,365 | 26 | **34** | 1 | 2 |
| 6, 9, 4 | 203,490 | 82 | **103** | 6 | (not computed) |

In the **five cases** where G\* gains at birth, it **slows** relaxation by 25 to 44% (t(G\*)/t(U) − 1): its curve rises above U's after 1 to 23 swaps in total variation and, in the four cases where it was computed, also in KL, the Lyapunov functional of theorem 4.7-b. The KL column comes from the second implementation only. The three cases where G\* relaxes as fast or slightly faster (0 to 7%) are those where it gains nothing at birth.

**Tempered family.** G_θ(A | C) ∝ π′(C + v_A)^θ links anti-Gibbs attachment (θ < 0: by proposition E it avoids closing triangles and prefers high-degree targets), U (θ = 0) and G\* (θ = 1). Swaps for TV ≤ 0.01:

| N, M, k | θ = −0.5 | −0.25 | 0 | 0.25 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|---|---|
| 4, 3, 3 | **190** | 218 | 268 | 325 | 363 | 381 | 387 |
| 4, 4, 3 | **21** | 24 | 27 | 30 | 32 | 34 | 35 |
| 5, 5, 4 | **114** | 120 | 130 | 142 | 153 | 159 | 163 |
| 5, 7, 4 | 25 | **24** | 26 | 28 | 31 | 33 | 34 |
| 6, 9, 4 | **68** | 74 | 82 | 90 | 96 | 100 | 103 |
| 6, 11, 3 | 63 | 62 | 61 | 60 | 59 | 58 | **57** |

In five cases out of six, **anti-Gibbs attachment relaxes fastest** (up to 29% fewer swaps than U and 51% fewer than G\*, i.e. 1 − t(θ)/t(reference)), although it is the worst at birth (TV 0.945 against 0.313 for G\* in case 4, 3, 3). Case 6, 11, 3 goes the other way.

### 3.4 Independent cross-check

Second implementation with no shared code (`defi_m8_second_moteur.py`: graphs as edge sets, triangles and degrees via `networkx`, kernel built by set enumeration, dense matrices) on the 27 transitions and 6 relaxations with at most 6 vertices after birth, and on the 4 corresponding tempered cases: maximum gap 1.3·10⁻¹⁵ on TVs, bounds and KLs; same numbers of swaps and same crossing times in total variation. The 7-vertex cases (6, 9, 4 and 6, 11, 3) are computed by the first implementation only. Checks: stochasticity and invariance of π′ to within 4·10⁻¹⁵.

## 4. Reading

- **[T]** The DEFI-M8 deliverable is provided **for the targets, at fixed k**, on abstract graphs: the target law that minimises the gap to π at birth exists, is unique in the KL sense, contains no new parameter (heat bath of S_sim) and has a readable form (anti-preferential triadic closure). At fixed k, no genealogical law, local or not, does better; the bound of proposition C is attained. The number k is not derived from S_sim: it is fixed by the arrival sector (M′ = M + k), and comparing values of k means comparing different targets π_{N+1,M+k}.
- **[CERT]** Its gain is often zero; at the best k it ranges from 0 (sectors 4, 5 and 5, 8) to 0.41 (sector 4, 3), and does not exceed 0.07 in the two N = 6 sectors; three sizes are not enough to establish a trend in N. Most of the gap at birth comes not from attachment but from the law of the old graph: R#π_{N+1} is not π_N.
- **[CERT], against intuition**: in the cases computed, minimising the gap at birth is not the right criterion for the bridge. In five cases out of six of the tempered family, the kernel most faithful at birth is the slowest to reach π′, and the anti-Gibbs kernel (which avoids triangles and prefers high degrees) is the fastest.
- **[H]** Untested explanation: G\* sinks the newborn into a clique, a high-weight configuration that edge swaps take long to undo, while the remaining gap lies in the old graph; a more "neutral" birth lets the chain correct first what matters.
- For the narrative (Book I, cascade of closures) and for RO-24: the closure derived from S_sim does close triangles and cliques at birth. For RO-25: this fidelity is paid for in relaxation time in most of the cases computed; RO-25's falsifier is neither triggered nor ruled out by these computations: proposition C only excludes exact reproduction of π by a strict genealogy, RO-25 also allows π_N to be "derived" (which relaxation does, at the price of rewiring), and "the intended genealogy" is not defined in the framework.

## 5. What is established, what remains to be checked, the weakest point

- **Established:** propositions D and E and corollary D1 (proofs above); exact values of §§ 3.2–3.3 on abstract graphs, for N + 1 ≤ 7.
- **To be checked:** everything, by a person; the trend of the gain with N (three sizes only); hypothesis H-abs (on the Rips engine, targets are restricted to geometric neighbours, which changes B_k(C)); thresholds other than ε = 0.01.
- **Hostile review (second AI agent):** count for corollary D1 corrected (25 cases, not 26), sentence on cliques corrected, deliverable restricted to targets at fixed k; proofs, tables and quotations were replayed and confirmed, including a third independent check on cases (4, 3, 3) and (4, 4, 3).
- **Weakest point:** the scope of the relaxation result. Eight cases, eight sectors, N ≤ 6 before birth, a single swap kernel; case 6, 11, 3 (the denser of the two 7-vertex cases) goes the other way. Nothing says the order "anti-Gibbs < uniform < Gibbs" persists as N grows.

## 6. Next step on the proof path (P1)

**DEFI-M11 — Born right or relaxed fast.** Which attachment law minimises the total cost of the bridge (swaps until TV ≤ ε after birth), and is it derivable from S_sim? Does the order anti-Gibbs < uniform < Gibbs survive beyond N = 6, and on the canonical engine at N ≥ 250?

## Reproduce

```bash
python3 contributions/RO-25_pilote-ia/defi_m8_attachement_gibbs.py   # ≈ 30 s, writes defi_m8_resultats.json
python3 contributions/RO-25_pilote-ia/defi_m8_tempere.py             # ≈ 40 s, writes defi_m8_tempere.json
python3 contributions/RO-25_pilote-ia/defi_m8_second_moteur.py       # ≈ 6 s, cross-check
python3 contributions/RO-25_pilote-ia/defi_m8_second_moteur.py --tempere
```

Python 3, numpy 2.5.3, scipy 1.18.1, networkx 3.7. Screen outputs: `defi_m8_sortie.txt`, `defi_m8_second_moteur_sortie.txt`, `defi_m8_tempere_sortie.txt`. SHA-256 fingerprints: `EMPREINTES_SHA256.txt` at the repository root.
