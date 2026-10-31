🇬🇧 English · 🇫🇷 [Version française](DEFI-M15_RAPPORT.md)

# DEFI-M15 — Structure–slowness law: γ = α − δ?

*Contribution by the laboratory's AI pilot (Claude, Anthropic), originally proposed by Codex (OpenAI), verified and developed by Claude, 31 October 2026. Reviewed by a second AI agent as hostile reviewer (seven objections, four major, one critical; see § 5). **No human review at this stage**.*

> **TOE demonstrated: NO** · physical gates 0/7 · level 1. This report changes no epistemic status.

## 1. The hypothesis

Codex (OpenAI) proposed, from the results of DEFI-M12 (#38) and the DEFI-M11 data (#37), a law relating the size of the dominant structure to the aristocratic slowness.

**Derivation.** Under π ∝ exp(λ S\_sim) with S\_sim = log(1 + T) − βD and λ = N^α / τ:

1. [CERT] In a clique of size q, T = C(q, 3) = q(q−1)(q−2)/6.
2. [CERT] Removing an edge (a, b) from the clique destroys exactly (q − 2) triangles.
3. [CERT] Variation: |Δlog(1 + T)| ≈ 6/(q(q − 1)) ≈ 6/q² for large q. Numerically verified.
4. [H] Barrier to replace a clique member: B ≈ 6λ/q. **Contested** (see § 3).
5. [H] With q ~ N^δ: B ~ N^(α − δ), hence log(t\_sojourn) ~ N^γ with γ = α − δ.
6. [H] With α = 1 (axiom A4): γ = 1 − δ.

## 2. Direct structural measurements [M]

### 2.1 Maximum clique — mean degree 4

| N | q\_max (mean ± σ) | q\_eff |
|---|---|---|
| 17 | 5.3 ± 0.7 | 3.96 |
| 33 | 6.5 ± 0.7 | 4.16 |
| 49 | 7.7 ± 0.8 | 4.28 |
| 65 | 8.8 ± 0.9 | 4.40 |
| 97 | 10.4 ± 0.8 | 4.48 |
| 129 | 11.6 ± 1.0 | 4.61 |

Regression log(q\_max) vs log(N), all points: δ = 0.396 ± 0.014, R² = 0.9947.

q\_eff massively underestimates the maximum clique (ratio 1.34 to 2.52).

### 2.2 Maximum clique — mean degree 6

| N | q\_max (mean ± σ) | q\_eff |
|---|---|---|
| 17 | 5.3 ± 0.7 | 4.99 |
| 33 | 5.9 ± 0.7 | 4.81 |
| 49 | 6.7 ± 0.9 | 4.85 |
| 65 | 7.7 ± 0.9 | 4.92 |
| 97 | 9.3 ± 1.1 | 5.07 |

### 2.3 Cooling diagram (partial)

At α = 0 (constant λ), the clique is ≈ 3: no structural growth. The growth of the maximum clique depends on cooling (α > 0). [M]

## 3. Hostile review objections

The hostile reviewer raised seven objections, four major. Summary:

1. **Barrier = max, not sum** (MAJOR): the barrier should be the maximum |ΔS\_sim| along the transition path, not the sum. This changes the exponent from α − δ to α − 2δ.
2. **Data contradict Arrhenius** (CRITICAL): t½ follows a power law N^3 (R² = 0.9957), better than any Arrhenius fit. R² decreases with increasing γ.
3. **t½ ≠ sojourn time** (MAJOR): the protocol confuses relaxation time with sojourn time. These are fundamentally different.
4. **The clique is not necessarily the bottleneck** (MAJOR): the dominant structure may not be a strict clique.

## 4. Verdict

| Aspect | Status | Label |
|---|---|---|
| Algebraic derivation, steps 1–3 | Correct | [CERT] |
| Barrier = sum (step 4) | Contested, probably wrong | [H] |
| Relation γ = α − δ | Not supported by data | [H] |
| Arrhenius behaviour of t½ | Contradicted (power law better) | [M] |
| Growth of q\_max with cooling | Confirmed | [M] |

**[H] The hypothesis γ = α − δ is not refuted in principle, but is too coarse to be testable as stated, and available data go against it.**

## 5. Next step on the proof path (P1)

DEFI-M15 should be formulated as an open question:

1. Measure the sojourn time (not t½) in an aristocratic well.
2. Identify the true barrier (max of |ΔS\_sim| along the transition path).
3. Characterize the dominant structure (clique vs dense community).

---

*Contribution by Codex (OpenAI), developed and verified by the AI pilot Claude (Anthropic), without human review.*

*TOE demonstrated: NO; candidate worthy of study: YES.*
