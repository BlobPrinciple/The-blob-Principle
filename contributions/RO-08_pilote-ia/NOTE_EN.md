🇬🇧 English · 🇫🇷 [Version française](NOTE.md)

# RO-08 — The Blob graph cannot be the 1-skeleton of any connected closed 3-manifold

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. Note by the laboratory's AI pilot (Claude, Anthropic), scheduled session of 13 November 2026, by delegation of Rudolphe Mirante. Not reviewed by a person. The laboratory's first work on the RO-08 bridge. The French note is the reference text.

## Object

RO-08 (armature V347.1, II.0, p. 11) asks to send the Ω³ regime of the historical layer A_Gibbs onto a closed triangulation of controlled topology, or to prove that B is a typical/limit sector of A_Gibbs; falsifier: "typical Ω³ configurations do not form closed 3-manifolds, or their topology is not controllable".

Already established in the corpus, not redone here:
- the Blob **clique complex** is not a 3-pseudomanifold (V346, CXL.2.4, Proposition 2, printed p. 1195, PDF 1243: mean 2-face multiplicity ≈ 9–10, 3.6 to 5 % of faces with exactly 2);
- the **Delaunay ∩ Blob** subcomplex is manifold-like but does not percolate (V346, AD.1–AD.2, tome V279, and CXL.3: 2.5–2.6 % of tetrahedra, 13–15 % vertex coverage).

Open question: **keeping the vertices and edges** of the Blob and choosing triangles and tetrahedra **freely** (not necessarily cliques), can one obtain a closed triangulation? This is the most economical route to B: it changes neither the population nor the bonds.

## Result in brief

1. **[T] No, for every configuration, at the canonical mean degree.** The A_Gibbs engine fixes |E| = round(κN/2) with κ = 6.6 (armature parameter table, κ₀; `blob engine.py`, `KAPPA = 6.6`), and edge exchange preserves |E|. Every simplicial triangulation of a connected closed 3-manifold satisfies f₁ ≥ 4f₀ − 10 (Walkup's lower bound theorem, 1970), i.e. mean degree ≥ 8 − 20/N. f₁ < 4f₀ − 10 as soon as N ≥ 16 (at N = 14 and 15, equality through rounding). No A_Gibbs configuration with N ≥ 16 is the 1-skeleton of a connected closed 3-manifold, whatever faces are chosen and whatever the state of the chain (for k components the bound becomes f₁ ≥ 4f₀ − 10k; the configurations measured here are connected, but the engine does not guarantee it). For T³ the bound is stronger: f₁ ≥ 4f₀ − 10 + 10·β₁ = 4f₀ + 20 (Novik–Swartz, Adv. Math. 222 (2009) 2059–2084, for M orientable over the chosen field; recalled by Lutz–Sulanke–Swartz 2009), mean degree ≥ 8 + 40/N.
2. **[M] Locally, the Blob is further from B than the control without viability.** Three necessary local conditions (below), tested on the canonical engine (N = 500 to 4,000, 4 seeds): 96 to 97.5 % of vertices violate at least one depending on N (92 % for the geometric graph without viability, 100 % for Erdős–Rényi); 65 % of edges have fewer than 3 common neighbours (40 % without viability). In the core of the cube (away from the faces), 96 % of Blob vertices violate a condition. The local deficit (sum of max(0, 3d − 6 − t)) is 6.1 per vertex for the Blob against 3.6 without viability. The link condition (C2) alone is not violated more by the Blob (0.776) than without viability (0.781): the gap comes from C1, C3 and the deficit.
3. **[M] The aristocracy paradox.** The Blob crosses the necessary global threshold n_tri/N ≥ κ − 2 = 4.6 (5.0 to 5.4 on average per N; 4.82 to 6.04 per configuration), which the control without viability does not (3.6 to 3.9). But it concentrates triangles: 31 % of its vertices carry none, 27 % have degree < 4; only the most massive decile (137 triangles and degree 21 on average) satisfies the link condition almost everywhere (97.5 %), and 76 % of its vertices remain in violation, at least 74 % through the edge condition (C3), on their links to poor vertices. Viability creates enough triangles in total but places them opposite to what a manifold requires, where each vertex carries exactly 3d − 6 triangular faces.

**Verdict.** The RO-08 bridge cannot be a mere "choice of faces" on the A_Gibbs graph: it must change the edges (add at least 0.7·N − 10 for Walkup's bound, at least 0.7·N + 20 for T³), or the vertices (coarse-graining), or go through another construction. The RO-08 falsifier is met **for this route only**; RO-08 stays open for the others. No status change.

## Necessary conditions used

Let G = (V, E) be the 1-skeleton of a simplicial triangulation K (a simplicial complex, not a Δ-complex) of a closed 3-manifold; d_v the degree of v, t_v the number of edges of G between neighbours of v (triangles of G at v), c_uv the number of common neighbours of u and v.

- **(C1) d_v ≥ 4 [T].** The link of v is a triangulated 2-sphere, which has at least 4 vertices.
- **(C2) t_v ≥ 3d_v − 6 [T].** The vertices of the link of v are exactly the neighbours of v. A triangulated 2-sphere with d vertices has 3d − 6 edges (Euler); each link edge ab is an edge of K between neighbours of v. Hence G[N(v)] has at least 3d_v − 6 edges. For a flag triangulation (faces = cliques) this is an equality, with d_v ≥ 6.
- **(C3) c_uv ≥ 3 [T].** The link of the edge uv is a triangulated circle (at least 3 vertices) whose vertices are common neighbours of u and v.
- **(Glob) n_tri/N ≥ κ − 2 [T].** Sum of (C2) over v: 3·n_tri ≥ 6|E| − 6N.
- **(W) f₁ ≥ 4f₀ − 10 [T, cited].** D. W. Walkup, "The lower bound conjecture for 3- and 4-manifolds", *Acta Mathematica* 125 (1970), 75–107; stated for connected M. Bound for T³: f₁ − 4f₀ + 10 ≥ 10·β₁ (I. Novik, E. Swartz, "Socles of Buchsbaum modules, complexes and posets", Adv. Math. 222 (2009) 2059–2084, M orientable over the chosen field), recalled in F. H. Lutz, T. Sulanke, E. Swartz, "f-vectors of 3-manifolds", *Electron. J. Combin.* 16(2) (2009), R13; β₁(T³) = 3. (W) alone suffices for point 1.

(C1)–(C3) and (W) are independent (a graph can satisfy (W) and have a vertex of degree 3); at κ = 6.6, (W) suffices, and (C1)–(C3) say **where** the graph fails.

## Measurements

`ro08_squelette.py` (Python sets) and `ro08_second_moteur.py` (sparse matrices: t_v = (A³)_vv/2, c_uv = (A²)_uv); engine `corpus/03_scripts/SCRIPTS DIVERS BLOB/blob engine.py` imported as is (κ 6.6; β 0.30; τ 0.50; pool_fac 1.6; therm_fac 120). Maximal difference between the two implementations: 0 on five quantities, 32 configurations; the hostile reviewer recomputed N = 1,000 seed 0 and N = 4,000 seed 1 independently (networkx), identically. |E| = 3.3·N exactly in all 32 configurations.

**Positive control**: Freudenthal–Kuhn germ of T³ (L = 4 and 5, degree 14): zero violations, n_tri/N = 12 = κ − 2 exactly, flag equality everywhere.

| model | N | vertices in violation | C1 (d < 4) | C2 | edges C3 (c < 3) | n_tri/N (threshold 4.6) | C2 deficit / N |
|---|---|---|---|---|---|---|---|
| Blob | 500 | 0.963 ± 0.009 | 0.302 | 0.737 | 0.608 | 5.29 | 5.46 |
| Blob | 1,000 | 0.972 ± 0.006 | 0.277 | 0.772 | 0.640 | 5.38 | 6.01 |
| Blob | 2,000 | 0.975 ± 0.002 | 0.274 | 0.772 | 0.645 | 5.04 | 6.04 |
| Blob | 4,000 | 0.975 ± 0.003 | 0.273 | 0.776 | 0.649 | 5.23 | 6.11 |
| without viability (RGG) | 4,000 | 0.920 ± 0.004 | 0.127 | 0.781 | 0.397 | 3.60 | 3.59 |
| Erdős–Rényi (|E| within 0.1 %, duplicates) | 4,000 | 1.000 | 0.105 | 0.959 | 1.000 | 0.01 | 13.79 |

(means over 4 seeds, standard deviation between seeds.) Core of the cube (vertices farther than 2r from the faces, ≈ 1,400 vertices at N = 4,000): 0.963 for the Blob, 0.919 without viability. Four times longer relaxation (N = 1,000, 2 seeds): 0.966 and 0.968, unchanged.

Breakdown by triangular-mass decile, Blob, N = 4,000 (rank deciles, 4 seeds): deciles 0–2 mass 0, degree 3.3, C1 0.61–0.65, all in violation; decile 5 mass 1.6, degree 5.1, all in violation; decile 8 mass 9.7, degree 8.8, 0.988; decile 9 mass 137.6, degree 21.4, C2 0.025, 0.764 in violation.

## Limits

- Point 1 concerns the canonical engine (κ = 6.6 imposed). A variant of A_Gibbs with κ ≥ 8 would escape (W); whether it also escapes the local conditions is not tested here. [OPEN]
- The engine lives in a cube with boundary (V346, CXL.8); a closed triangulation has none. The cube core gives the same figures, and (W) does not depend on the boundary.
- A bridge through coarse-graining (R-TRUE, blocks) or through a construction that adds edges is not excluded. The note only says that the graph must change.
- The comparison with the control without viability is at equal |E| but not at a comparable equilibrium law (the RGG is not relaxed).

## Open question

What is the smallest number of edge changes that makes a typical A_Gibbs configuration the 1-skeleton of a triangulation of T³, and does this cost per vertex tend to a limit as N grows? Does a Gibbs measure at κ ≥ 8 keep the aristocracy, which is the local obstacle measured here?

## Reproduce

```
pip install numba scipy
python3 contributions/RO-08_pilote-ia/ro08_squelette.py      # ≈ 1 min; ro08_squelette.json
python3 contributions/RO-08_pilote-ia/ro08_second_moteur.py  # ≈ 1 min; last line ACCORD
```
