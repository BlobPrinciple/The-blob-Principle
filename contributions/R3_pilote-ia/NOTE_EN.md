🇫🇷 [Version française](NOTE.md) · 🇬🇧 English

*Translated with DeepL and corrected by the pilot; the French original prevails.*

# DEFI-R3 — Triangle-counting error in the archived "V109" engine

*The laboratory's AI pilot (Claude, Anthropic), 15 October 2026. Found while rewriting the sampler for DEFI-M7. Not reviewed by a person.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. No change of status.

## Finding

The "V109" MCMC engine printed in the V346 master (pp. 291–292 printed, pp. 339–340 of the PDF) updates the triangle count with `n_tri_new = n_tri - common_rm + common_add`, where `common_add` is computed on the graph **before** the edge (u, v) is removed. Nothing prevents the added edge from sharing an endpoint with the removed one.

**[T]** If the added edge is (u, w) and v is adjacent to w, the triangle {u, v, w} is counted in `common_add` although the edge (u, v) has just disappeared. The error is always an excess: the tracked counter drifts upwards, and the Metropolis acceptance relies on this wrong counter, so the chain does not sample π exactly.

**[M]** Listing run as is (N = 300 and 500, 3 seeds each, 20,000 and 50,000 steps): the tracked n_tri exceeds the recount by 1.4% to 2.7%, in all 6 cases.

## Scope

- The current canonical engine (`blob engine.py`) is **not** affected: it excludes candidate pairs that touch u or v.
- Results produced with V109 are already classed [ARCH]; this error adds to the reasons not to carry them over without recomputation.

## Reproduce

`python3 contributions/R3_pilote-ia/verif_v109_n_tri.py` (pdftotext required; a few seconds).
