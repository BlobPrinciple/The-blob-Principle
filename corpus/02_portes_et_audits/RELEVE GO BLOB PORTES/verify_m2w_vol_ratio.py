#!/usr/bin/env python3
"""Independent exact certificate for the M2-W VOL-RATIO theorem.

The production model uses triangulations and pointed Pachner channels.  This
certificate deliberately uses a different finite groupoid: simple graphs on
five vertices, with edge-addition/removal channels of size 1 and 3.  It checks
with exact rational arithmetic that:

1. groupoid weights 1/|Aut| give the pointed-channel flux identity;
2. the flux quotient reconstructs A_{N+d}/A_N for arbitrary volume bias;
3. two different biases give the same reconstructed ratios;
4. the direct d=3 ratio equals three successive d=1 ratios;
5. deleting 1/|Aut| or collapsing marked channels breaks the identity.

The graph model is not evidence for the physics of M2-W.  It is an independent
implementation certificate for the algebra used in the theorem.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import combinations, permutations
import math


VERTICES = 5
EDGES = tuple(combinations(range(VERTICES), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
PERMUTATIONS = tuple(permutations(range(VERTICES)))
FULL_MASK = (1 << len(EDGES)) - 1
RHO = {1: Fraction(7, 11), 3: Fraction(5, 13)}


def bits(indices: tuple[int, ...]) -> int:
    result = 0
    for index in indices:
        result |= 1 << index
    return result


@lru_cache(maxsize=None)
def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for index, (left, right) in enumerate(EDGES):
        if not ((mask >> index) & 1):
            continue
        image = tuple(sorted((permutation[left], permutation[right])))
        result |= 1 << EDGE_INDEX[image]
    return result


@lru_cache(maxsize=None)
def canonical(mask: int) -> int:
    return min(permute_mask(mask, permutation) for permutation in PERMUTATIONS)


@lru_cache(maxsize=None)
def automorphism_order(mask: int) -> int:
    representative = canonical(mask)
    return sum(
        permute_mask(representative, permutation) == representative
        for permutation in PERMUTATIONS
    )


REPRESENTATIVES = tuple(
    mask for mask in range(FULL_MASK + 1) if canonical(mask) == mask
)


def triangle_count(mask: int) -> int:
    count = 0
    for vertices in combinations(range(VERTICES), 3):
        triangle_edges = tuple(
            EDGE_INDEX[tuple(sorted(edge))]
            for edge in combinations(vertices, 2)
        )
        if all((mask >> index) & 1 for index in triangle_edges):
            count += 1
    return count


def wedge_count(mask: int) -> int:
    degrees = [0] * VERTICES
    for index, (left, right) in enumerate(EDGES):
        if (mask >> index) & 1:
            degrees[left] += 1
            degrees[right] += 1
    return sum(degree * (degree - 1) // 2 for degree in degrees)


@lru_cache(maxsize=None)
def shape_weight(mask: int) -> Fraction:
    """Positive isomorphism-invariant weight with nontrivial shape dependence."""
    representative = canonical(mask)
    triangles = triangle_count(representative)
    wedges = wedge_count(representative)
    return Fraction(2**triangles, 3**wedges)


def bias_a(volume: int) -> Fraction:
    return Fraction(5**volume, 4**volume)


def bias_b(volume: int) -> Fraction:
    return Fraction(7**volume, 9**volume)


def microcanonical_weights(use_automorphisms: bool = True) -> dict[int, Fraction]:
    values = {volume: Fraction(0, 1) for volume in range(len(EDGES) + 1)}
    for representative in REPRESENTATIVES:
        volume = representative.bit_count()
        divisor = automorphism_order(representative) if use_automorphisms else 1
        values[volume] += shape_weight(representative) / divisor
    return values


def metropolis_rate(
    source: int,
    target: int,
    bias,
    delta: int,
) -> Fraction:
    source_volume = source.bit_count()
    target_volume = target.bit_count()
    ratio = (
        shape_weight(target)
        * bias(target_volume)
        / (shape_weight(source) * bias(source_volume))
    )
    return RHO[delta] * min(Fraction(1, 1), ratio)


def fluxes(
    delta: int,
    bias,
    *,
    use_automorphisms: bool = True,
    collapse_target_classes: bool = False,
) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    upward = {volume: Fraction(0, 1) for volume in range(len(EDGES) + 1)}
    downward = {volume: Fraction(0, 1) for volume in range(len(EDGES) + 1)}

    for representative in REPRESENTATIVES:
        volume = representative.bit_count()
        divisor = automorphism_order(representative) if use_automorphisms else 1
        mass = shape_weight(representative) * bias(volume) / divisor
        present = tuple(
            index for index in range(len(EDGES)) if (representative >> index) & 1
        )
        missing = tuple(
            index for index in range(len(EDGES)) if not ((representative >> index) & 1)
        )

        up_channels = []
        if len(missing) >= delta:
            up_channels = [
                representative | bits(choice)
                for choice in combinations(missing, delta)
            ]
        down_channels = []
        if len(present) >= delta:
            down_channels = [
                representative & ~bits(choice)
                for choice in combinations(present, delta)
            ]

        if collapse_target_classes:
            up_channels = list({canonical(target) for target in up_channels})
            down_channels = list({canonical(target) for target in down_channels})

        for target in up_channels:
            upward[volume] += mass * metropolis_rate(
                representative, target, bias, delta
            )
        for target in down_channels:
            downward[volume] += mass * metropolis_rate(
                representative, target, bias, delta
            )

    return upward, downward


def microcanonical_rate_average(
    total_flux: Fraction,
    volume: int,
    bias,
    microcanonical: dict[int, Fraction],
) -> Fraction:
    return total_flux / (microcanonical[volume] * bias(volume))


def reconstructed_ratios(
    delta: int,
    bias,
    microcanonical: dict[int, Fraction],
) -> dict[int, Fraction]:
    upward, downward = fluxes(delta, bias)
    result: dict[int, Fraction] = {}
    for volume in range(len(EDGES) + 1 - delta):
        up_average = microcanonical_rate_average(
            upward[volume], volume, bias, microcanonical
        )
        down_average = microcanonical_rate_average(
            downward[volume + delta],
            volume + delta,
            bias,
            microcanonical,
        )
        assert up_average > 0
        assert down_average > 0
        result[volume] = (
            bias(volume)
            / bias(volume + delta)
            * up_average
            / down_average
        )
    return result


def maximum_relative_flux_error(
    upward: dict[int, Fraction],
    downward: dict[int, Fraction],
    delta: int,
) -> float:
    maximum = Fraction(0, 1)
    for volume in range(len(EDGES) + 1 - delta):
        left = upward[volume]
        right = downward[volume + delta]
        scale = max(abs(left), abs(right), Fraction(1, 10**100))
        maximum = max(maximum, abs(left - right) / scale)
    return float(maximum)


def main() -> None:
    assert len(REPRESENTATIVES) == 34
    microcanonical = microcanonical_weights()
    assert all(value > 0 for value in microcanonical.values())

    exact_flux_residual = Fraction(0, 1)
    exact_ratio_residual = Fraction(0, 1)
    bias_residual = Fraction(0, 1)

    ratios_by_bias: dict[tuple[str, int], dict[int, Fraction]] = {}
    for bias_name, bias in (("A", bias_a), ("B", bias_b)):
        for delta in (1, 3):
            upward, downward = fluxes(delta, bias)
            for volume in range(len(EDGES) + 1 - delta):
                exact_flux_residual = max(
                    exact_flux_residual,
                    abs(upward[volume] - downward[volume + delta]),
                )

            reconstructed = reconstructed_ratios(delta, bias, microcanonical)
            ratios_by_bias[(bias_name, delta)] = reconstructed
            for volume, estimate in reconstructed.items():
                exact = microcanonical[volume + delta] / microcanonical[volume]
                exact_ratio_residual = max(
                    exact_ratio_residual,
                    abs(estimate - exact),
                )

    for delta in (1, 3):
        for volume in ratios_by_bias[("A", delta)]:
            bias_residual = max(
                bias_residual,
                abs(
                    ratios_by_bias[("A", delta)][volume]
                    - ratios_by_bias[("B", delta)][volume]
                ),
            )

    cycle_residual = Fraction(0, 1)
    ratio_1 = ratios_by_bias[("A", 1)]
    ratio_3 = ratios_by_bias[("A", 3)]
    for volume in range(len(EDGES) + 1 - 3):
        indirect = (
            ratio_1[volume]
            * ratio_1[volume + 1]
            * ratio_1[volume + 2]
        )
        cycle_residual = max(cycle_residual, abs(ratio_3[volume] - indirect))

    naive_up, naive_down = fluxes(
        1,
        bias_a,
        use_automorphisms=False,
    )
    naive_error = maximum_relative_flux_error(naive_up, naive_down, 1)

    collapsed_up, collapsed_down = fluxes(
        1,
        bias_a,
        collapse_target_classes=True,
    )
    collapsed_error = maximum_relative_flux_error(
        collapsed_up,
        collapsed_down,
        1,
    )

    assert exact_flux_residual == 0
    assert exact_ratio_residual == 0
    assert bias_residual == 0
    assert cycle_residual == 0
    assert naive_error > 1.0e-3
    assert collapsed_error > 1.0e-3

    nontrivial_automorphisms = sum(
        automorphism_order(representative) > 1
        for representative in REPRESENTATIVES
    )

    print("M2-W VOL-RATIO CERTIFICATE")
    print(f"unlabelled graph classes               = {len(REPRESENTATIVES)}")
    print(f"classes with nontrivial automorphisms  = {nontrivial_automorphisms}")
    print(f"exact pointed-flux residual            = {exact_flux_residual}")
    print(f"exact reconstructed-ratio residual     = {exact_ratio_residual}")
    print(f"two-bias invariance residual           = {bias_residual}")
    print(f"delta-3 cycle residual                 = {cycle_residual}")
    print(f"naive no-|Aut| relative flux error     = {naive_error:.6e}")
    print(f"collapsed-channel relative flux error  = {collapsed_error:.6e}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
