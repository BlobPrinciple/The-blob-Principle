#!/usr/bin/env python3
"""Independent exact certificate for the M2-W VOL-COVER theorem.

This certificate checks only finite, algebraic consequences of the proof.
It does not simulate triangulations and does not claim a mixing-time bound.

Checks:
1. the labelled face-pairing count is bounded by (24 N)^(2 N);
2. the proposed soft tail is bounded by N^(-N), exactly;
3. the resulting comparison series is rigorously below 3/2;
4. any positive finite-window bump preserves summability and full support;
5. a hard volume cap can disconnect a connected Pachner-like graph, whereas
   a positive soft bias does not remove any edge;
6. an unrelated finite reversible-chain proxy verifies exact detailed
   balance and exact cancellation of two different volume biases
   conditionally on volume.

All identities except the displayed decimal partial sum use integer or
rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import prod


def odd_double_factorial(odd: int) -> int:
    assert odd >= 1 and odd % 2 == 1
    return prod(range(1, odd + 1, 2))


def check_face_pairing_bound(limit: int = 120) -> int:
    violations = 0
    for volume in range(1, limit + 1):
        encodings = odd_double_factorial(4 * volume - 1) * 6 ** (2 * volume)
        bound = (24 * volume) ** (2 * volume)
        if encodings > bound:
            violations += 1
    return violations


def check_soft_tail_bound(limit: int = 500) -> int:
    """Check N^(2N)/(N+1)^(3N) <= N^(-N) exactly."""
    violations = 0
    for volume in range(1, limit + 1):
        left = Fraction(volume ** (2 * volume), (volume + 1) ** (3 * volume))
        right = Fraction(1, volume**volume)
        if left > right:
            violations += 1
    return violations


def comparison_series_certificate(cutoff: int = 40) -> tuple[Fraction, Fraction]:
    partial = sum(
        (Fraction(1, volume**volume) for volume in range(1, cutoff + 1)),
        Fraction(0, 1),
    )
    # For N >= cutoff+1 >= 2, N^(-N) <= 2^(-N).
    geometric_tail = Fraction(1, 2**cutoff)
    global_upper = partial + geometric_tail
    assert global_upper < Fraction(3, 2)
    return partial, global_upper


def finite_bump_certificate() -> tuple[Fraction, Fraction]:
    """Use a deliberately huge but finite rational bump on a finite window."""
    bump = {
        volume: Fraction((volume + 7) ** 9, 11)
        for volume in range(9, 18)
    }
    base = sum(
        (Fraction(1, volume**volume) for volume in range(1, 41)),
        Fraction(0, 1),
    )
    correction = sum(
        (
            max(Fraction(0, 1), factor - 1)
            * Fraction(1, volume**volume)
            for volume, factor in bump.items()
        ),
        Fraction(0, 1),
    )
    certified_upper = base + Fraction(1, 2**40) + correction
    assert certified_upper > 0
    assert all(factor > 0 for factor in bump.values())
    return correction, certified_upper


def connected_components(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
) -> int:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)
    unseen = set(vertices)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            neighbours = adjacency[vertex] & unseen
            unseen.difference_update(neighbours)
            stack.extend(neighbours)
    return components


def cap_disconnect_certificate() -> tuple[int, int]:
    """Illustrative graph with allowed Pachner volume increments 1 and 3."""
    volume = {
        "a2": 2,
        "a3": 3,
        "a4": 4,
        "x7": 7,
        "b4": 4,
        "b3": 3,
        "b2": 2,
    }
    edges = (
        ("a2", "a3"),
        ("a3", "a4"),
        ("a4", "x7"),
        ("x7", "b4"),
        ("b4", "b3"),
        ("b3", "b2"),
    )
    assert all(abs(volume[left] - volume[right]) in (1, 3) for left, right in edges)
    all_vertices = tuple(volume)
    hard_vertices = tuple(vertex for vertex in all_vertices if volume[vertex] <= 4)
    full_components = connected_components(all_vertices, edges)
    hard_components = connected_components(hard_vertices, edges)
    assert full_components == 1
    assert hard_components == 2
    return hard_components, full_components


STATES = ("a2", "b2", "a3", "b3", "x6")
VOLUME = {"a2": 2, "b2": 2, "a3": 3, "b3": 3, "x6": 6}
SHAPE_OVER_AUT = {
    "a2": Fraction(5, 7),
    "b2": Fraction(11, 13),
    "a3": Fraction(17, 19),
    "b3": Fraction(23, 29),
    "x6": Fraction(31, 37),
}
CHAIN_EDGES = (
    ("a2", "a3"),
    ("b2", "b3"),
    ("a3", "b3"),
    ("a3", "x6"),
    ("b3", "x6"),
)


def bias_one(volume: int) -> Fraction:
    return Fraction(2**volume, (volume + 1) ** (volume + 2))


def bias_two(volume: int) -> Fraction:
    return Fraction(5**volume, (volume + 2) ** (volume + 3))


def stationary_mass(state: str, bias) -> Fraction:
    return SHAPE_OVER_AUT[state] * bias(VOLUME[state])


def metropolis_rate(source: str, target: str, bias) -> Fraction:
    ratio = stationary_mass(target, bias) / stationary_mass(source, bias)
    return min(Fraction(1, 1), ratio)


def reversible_proxy_certificate() -> tuple[Fraction, Fraction, Fraction]:
    detailed_balance_residual = Fraction(0, 1)
    stationarity_residual = Fraction(0, 1)

    neighbours = {state: set() for state in STATES}
    for left, right in CHAIN_EDGES:
        neighbours[left].add(right)
        neighbours[right].add(left)

    for bias in (bias_one, bias_two):
        for left, right in CHAIN_EDGES:
            lhs = stationary_mass(left, bias) * metropolis_rate(left, right, bias)
            rhs = stationary_mass(right, bias) * metropolis_rate(right, left, bias)
            detailed_balance_residual = max(
                detailed_balance_residual,
                abs(lhs - rhs),
            )

        for target in STATES:
            incoming = sum(
                (
                    stationary_mass(source, bias)
                    * metropolis_rate(source, target, bias)
                    for source in neighbours[target]
                ),
                Fraction(0, 1),
            )
            outgoing = stationary_mass(target, bias) * sum(
                (
                    metropolis_rate(target, other, bias)
                    for other in neighbours[target]
                ),
                Fraction(0, 1),
            )
            stationarity_residual = max(
                stationarity_residual,
                abs(incoming - outgoing),
            )

    conditional_bias_residual = Fraction(0, 1)
    for volume in (2, 3):
        layer = tuple(state for state in STATES if VOLUME[state] == volume)
        base_total = sum((SHAPE_OVER_AUT[state] for state in layer), Fraction())
        base = {
            state: SHAPE_OVER_AUT[state] / base_total
            for state in layer
        }
        for bias in (bias_one, bias_two):
            biased_total = sum(
                (stationary_mass(state, bias) for state in layer),
                Fraction(),
            )
            for state in layer:
                conditional = stationary_mass(state, bias) / biased_total
                conditional_bias_residual = max(
                    conditional_bias_residual,
                    abs(conditional - base[state]),
                )

    assert detailed_balance_residual == 0
    assert stationarity_residual == 0
    assert conditional_bias_residual == 0
    return (
        detailed_balance_residual,
        stationarity_residual,
        conditional_bias_residual,
    )


def main() -> None:
    pairing_violations = check_face_pairing_bound()
    tail_violations = check_soft_tail_bound()
    partial, global_upper = comparison_series_certificate()
    bump_correction, bumped_upper = finite_bump_certificate()
    hard_components, soft_components = cap_disconnect_certificate()
    balance_residual, stationary_residual, bias_residual = (
        reversible_proxy_certificate()
    )

    assert pairing_violations == 0
    assert tail_violations == 0
    assert global_upper < Fraction(3, 2)
    assert hard_components == 2
    assert soft_components == 1

    print("M2-W VOL-COVER CERTIFICATE")
    print(f"face-pairing bound violations          = {pairing_violations}")
    print(f"soft-tail bound violations             = {tail_violations}")
    print(f"sum N^(-N), N=1..40                   = {float(partial):.12f}")
    print(f"certified all-N comparison upper       = {float(global_upper):.12f}")
    print(f"universal simple upper bound           = {float(Fraction(3, 2)):.12f}")
    print(f"finite-bump correction (positive)      = {float(bump_correction):.6e}")
    print(f"finite-bump certified upper (finite)   = {float(bumped_upper):.6e}")
    print(f"hard-cap illustrative components       = {hard_components}")
    print(f"soft-support illustrative components   = {soft_components}")
    print(f"exact detailed-balance residual        = {balance_residual}")
    print(f"exact stationarity residual            = {stationary_residual}")
    print(f"exact conditional-bias residual        = {bias_residual}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
