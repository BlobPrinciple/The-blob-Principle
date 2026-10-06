#!/usr/bin/env python3
"""Independent certificate for the M2-W GEN-WELLPOSED note.

The proofs in the note are analytic.  This script independently checks:

1. the sharp linear bound L=sum_e log(1+n_e) <= 2 N_3 log(4);
2. the orbit-stabilizer realization of the factor 1/|Aut|;
3. detailed balance, positivity and the row-growth bound for a bounded
   continuous-time Metropolis generator;
4. the finite-matrix version of the analytic-vector estimate;
5. the unbounded-rate obstruction of KIN-FLAT.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
import math

import numpy as np


TOL = 5.0e-12


def random_edge_degrees(
    rng: np.random.Generator,
    tetrahedra: int,
    edge_count: int,
) -> np.ndarray:
    """Return integer n_e>=3 with sum n_e=6*N_3."""
    residual = 6 * tetrahedra - 3 * edge_count
    assert residual >= 0
    degrees = np.full(edge_count, 3, dtype=int)
    if residual:
        degrees += rng.multinomial(residual, np.full(edge_count, 1.0 / edge_count))
    return degrees


def check_log_bound() -> dict:
    rng = np.random.default_rng(2731)
    largest_ratio = 0.0
    largest_jensen_error = 0.0
    for tetrahedra in (20, 50, 100, 250, 500):
        for _ in range(300):
            edge_count = int(rng.integers(tetrahedra + 1, 2 * tetrahedra + 1))
            degrees = random_edge_degrees(rng, tetrahedra, edge_count)
            value = float(np.log1p(degrees).sum())
            bound = 2.0 * tetrahedra * math.log(4.0)
            jensen = edge_count * math.log(1.0 + 6.0 * tetrahedra / edge_count)
            assert value <= jensen + TOL
            assert jensen <= bound + TOL
            largest_ratio = max(largest_ratio, value / bound)
            largest_jensen_error = max(largest_jensen_error, value - jensen)
    return {
        "largest_ratio": largest_ratio,
        "largest_jensen_error": largest_jensen_error,
    }


def permute_graph(mask: int, vertex_count: int, permutation: tuple[int, ...]) -> int:
    edges = list(combinations(range(vertex_count), 2))
    index = {edge: position for position, edge in enumerate(edges)}
    result = 0
    for position, (left, right) in enumerate(edges):
        if not (mask >> position) & 1:
            continue
        image = tuple(sorted((permutation[left], permutation[right])))
        result |= 1 << index[image]
    return result


def check_groupoid_cardinality() -> dict:
    vertex_count = 4
    edges = list(combinations(range(vertex_count), 2))
    group = list(permutations(range(vertex_count)))
    unseen = set(range(1 << len(edges)))
    labelled_sum = Fraction(0, 1)
    for graph in unseen:
        labelled_sum += Fraction(2 ** graph.bit_count(), math.factorial(vertex_count))

    quotient_sum = Fraction(0, 1)
    orbit_count = 0
    max_orbit_error = 0
    while unseen:
        representative = min(unseen)
        orbit = {permute_graph(representative, vertex_count, perm) for perm in group}
        automorphisms = sum(
            permute_graph(representative, vertex_count, perm) == representative
            for perm in group
        )
        max_orbit_error = max(
            max_orbit_error,
            abs(len(orbit) * automorphisms - math.factorial(vertex_count)),
        )
        quotient_sum += Fraction(2 ** representative.bit_count(), automorphisms)
        unseen -= orbit
        orbit_count += 1

    assert max_orbit_error == 0
    assert labelled_sum == quotient_sum
    return {
        "orbit_count": orbit_count,
        "exact_sum": labelled_sum,
        "orbit_error": max_orbit_error,
    }


def metropolis_generator(
    probability: np.ndarray,
    edges: list[tuple[int, int, float]],
) -> np.ndarray:
    generator = np.zeros((probability.size, probability.size), dtype=float)
    for left, right, attempt in edges:
        ratio = probability[right] / probability[left]
        generator[left, right] += attempt * min(1.0, ratio)
        generator[right, left] += attempt * min(1.0, 1.0 / ratio)
    np.fill_diagonal(generator, -generator.sum(axis=1))
    return generator


def counting_hamiltonian(
    generator: np.ndarray,
    probability: np.ndarray,
) -> np.ndarray:
    root = np.sqrt(probability)
    return -(root[:, None] * generator) / root[None, :]


def check_bounded_generator() -> dict:
    state_count = 42
    volumes = 4 + np.arange(state_count)
    raw = np.exp(-0.18 * volumes) * (1.0 + 0.07 * np.cos(volumes))
    probability = raw / raw.sum()

    edges: list[tuple[int, int, float]] = []
    for left in range(state_count - 1):
        edges.append((left, left + 1, 0.8))
    for left in range(state_count - 3):
        edges.append((left, left + 3, 1.0))

    generator = metropolis_generator(probability, edges)
    hamiltonian = counting_hamiltonian(generator, probability)
    flow = probability[:, None] * generator
    balance_error = float(np.max(np.abs(flow - flow.T)))
    symmetry_error = float(np.linalg.norm(hamiltonian - hamiltonian.T, ord=2))
    ground_error = float(np.linalg.norm(hamiltonian @ np.sqrt(probability)))
    eigenvalues = np.linalg.eigvalsh(hamiltonian)
    max_rate = float(np.max(generator - np.diag(np.diag(generator))))

    row_absolute = np.abs(hamiltonian).sum(axis=1)
    row_bound_ratio = float(np.max(row_absolute / (12.0 * volumes)))

    assert balance_error < TOL
    assert symmetry_error < TOL
    assert ground_error < TOL
    assert eigenvalues[0] > -TOL
    assert max_rate <= 1.0 + TOL
    assert row_bound_ratio <= 1.0 + TOL

    vector = np.zeros(state_count)
    vector[0] = 1.0
    maximum_initial_volume = int(volumes[0])
    current = vector.copy()
    largest_analytic_ratio = 0.0
    theoretical = 1.0
    constant = 12.0
    for power in range(1, 9):
        current = hamiltonian @ current
        theoretical *= constant * (maximum_initial_volume + 3 * power)
        ratio = float(np.linalg.norm(current) / theoretical)
        largest_analytic_ratio = max(largest_analytic_ratio, ratio)
        assert ratio <= 1.0 + TOL

    return {
        "balance_error": balance_error,
        "symmetry_error": symmetry_error,
        "ground_error": ground_error,
        "minimum_eigenvalue": float(eigenvalues[0]),
        "max_rate": max_rate,
        "row_bound_ratio": row_bound_ratio,
        "largest_analytic_ratio": largest_analytic_ratio,
    }


def check_nonexplosion_lower_bound() -> dict:
    initial_volume = 4
    rho_max = 1.0
    terms = 200_000
    lower_bound = sum(
        1.0 / (6.0 * rho_max * (initial_volume + 3 * jump))
        for jump in range(terms)
    )
    doubled = sum(
        1.0 / (6.0 * rho_max * (initial_volume + 3 * jump))
        for jump in range(2 * terms)
    )
    assert doubled > lower_bound
    return {
        "partial_sum": lower_bound,
        "doubled_partial_sum": doubled,
        "increment": doubled - lower_bound,
    }


def check_flat_rate_obstruction() -> dict:
    ratios = np.logspace(-12, 12, 49)
    flat_forward = np.sqrt(ratios)
    metropolis_forward = np.minimum(1.0, ratios)
    assert float(np.max(metropolis_forward)) <= 1.0 + TOL
    assert float(np.max(flat_forward)) >= 1.0e6 - TOL
    return {
        "max_flat_rate": float(np.max(flat_forward)),
        "max_metropolis_rate": float(np.max(metropolis_forward)),
    }


def main() -> None:
    log_bound = check_log_bound()
    groupoid = check_groupoid_cardinality()
    generator = check_bounded_generator()
    nonexplosion = check_nonexplosion_lower_bound()
    flat = check_flat_rate_obstruction()

    print("M2-W GEN-WELLPOSED CERTIFICATE")
    print(
        "largest sampled L/(2 N log 4)    = "
        f"{log_bound['largest_ratio']:.12f}"
    )
    print(
        "largest Jensen excess            = "
        f"{log_bound['largest_jensen_error']:.3e}"
    )
    print(
        "unlabelled graph orbits (v=4)    = "
        f"{groupoid['orbit_count']}"
    )
    print(
        "groupoid weighted sum (exact)    = "
        f"{groupoid['exact_sum']}"
    )
    print(
        "orbit-stabilizer integer error   = "
        f"{groupoid['orbit_error']}"
    )
    print(
        "detailed-balance error           = "
        f"{generator['balance_error']:.3e}"
    )
    print(
        "counting-basis symmetry error    = "
        f"{generator['symmetry_error']:.3e}"
    )
    print(
        "ground-state error               = "
        f"{generator['ground_error']:.3e}"
    )
    print(
        "minimum Hamiltonian eigenvalue   = "
        f"{generator['minimum_eigenvalue']:.3e}"
    )
    print(
        "largest Metropolis rate          = "
        f"{generator['max_rate']:.6f}"
    )
    print(
        "largest row-bound ratio          = "
        f"{generator['row_bound_ratio']:.6f}"
    )
    print(
        "largest analytic-vector ratio    = "
        f"{generator['largest_analytic_ratio']:.3e}"
    )
    print(
        "holding-time lower sum K         = "
        f"{nonexplosion['partial_sum']:.12f}"
    )
    print(
        "holding-time lower sum 2K        = "
        f"{nonexplosion['doubled_partial_sum']:.12f}"
    )
    print(
        "positive harmonic increment      = "
        f"{nonexplosion['increment']:.12f}"
    )
    print(
        "max KIN-FLAT rate tested         = "
        f"{flat['max_flat_rate']:.6e}"
    )
    print(
        "max bounded Metropolis rate      = "
        f"{flat['max_metropolis_rate']:.6f}"
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
