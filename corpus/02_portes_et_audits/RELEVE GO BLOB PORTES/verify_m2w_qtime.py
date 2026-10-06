#!/usr/bin/env python3
"""Independent certificate for the M2-W Q-TIME / DYN-UNIQUENESS note.

The analytic note proves that a positive equilibrium measure and a local move
graph do not determine a reversible generator.  This script independently
checks:

1. the exact conductance parametrization of all channelwise reversible rates;
2. the ground state sqrt(pi) and the kinetic off-diagonal matrix elements;
3. a three-state local counterexample whose gap can be made arbitrarily small
   without changing pi or the move graph;
4. the cutoff-uniform comparison between Metropolis and Barker conductances.
5. the potentially unbounded comparison between flat hopping and Metropolis.

Floating-point calculations only certify the implementation and signs.  The
statements in the note are proved algebraically.
"""

from __future__ import annotations

import math

import numpy as np


TOL = 2.0e-13


def generator_from_kinetic_amplitudes(
    probability: np.ndarray,
    edges: list[tuple[int, int, float]],
) -> np.ndarray:
    """Build q_ij=a_ij sqrt(pi_j/pi_i), with a_ij=a_ji."""
    size = probability.size
    generator = np.zeros((size, size), dtype=float)
    for left, right, amplitude in edges:
        generator[left, right] += amplitude * math.sqrt(
            probability[right] / probability[left]
        )
        generator[right, left] += amplitude * math.sqrt(
            probability[left] / probability[right]
        )
    np.fill_diagonal(generator, -generator.sum(axis=1))
    return generator


def counting_basis_hamiltonian(
    generator: np.ndarray,
    probability: np.ndarray,
) -> np.ndarray:
    root = np.sqrt(probability)
    return -(root[:, None] * generator) / root[None, :]


def detailed_balance_error(
    generator: np.ndarray,
    probability: np.ndarray,
) -> float:
    flow = probability[:, None] * generator
    return float(np.max(np.abs(flow - flow.T)))


def spectral_gap(hamiltonian: np.ndarray) -> float:
    values = np.linalg.eigvalsh(hamiltonian)
    assert values[0] > -TOL
    return float(values[1])


def check_exact_parametrization() -> dict:
    probability = np.array([0.07, 0.13, 0.19, 0.23, 0.38], dtype=float)
    probability /= probability.sum()
    edges = [
        (0, 1, 0.7),
        (1, 2, 1.1),
        (2, 3, 0.4),
        (3, 4, 1.7),
        (4, 0, 0.9),
        (1, 4, 0.6),
    ]
    generator = generator_from_kinetic_amplitudes(probability, edges)
    hamiltonian = counting_basis_hamiltonian(generator, probability)

    balance_error = detailed_balance_error(generator, probability)
    symmetry_error = float(np.linalg.norm(hamiltonian - hamiltonian.T, ord=2))
    ground_error = float(np.linalg.norm(hamiltonian @ np.sqrt(probability)))
    assert balance_error < TOL
    assert symmetry_error < TOL
    assert ground_error < TOL

    max_kinetic_error = 0.0
    for left, right, amplitude in edges:
        max_kinetic_error = max(
            max_kinetic_error,
            abs(hamiltonian[left, right] + amplitude),
            abs(hamiltonian[right, left] + amplitude),
        )
    assert max_kinetic_error < TOL

    values = np.linalg.eigvalsh(hamiltonian)
    assert values[0] > -TOL
    assert values[1] > 0.0
    return {
        "balance_error": balance_error,
        "symmetry_error": symmetry_error,
        "ground_error": ground_error,
        "kinetic_error": max_kinetic_error,
        "gap": float(values[1]),
    }


def path_generator(epsilon: float) -> np.ndarray:
    """Uniform-pi generator on 1--2--3 with rates 1 and epsilon."""
    generator = np.array(
        [
            [-1.0, 1.0, 0.0],
            [1.0, -(1.0 + epsilon), epsilon],
            [0.0, epsilon, -epsilon],
        ],
        dtype=float,
    )
    return generator


def check_three_state_counterexample() -> dict:
    epsilon = 1.0e-6
    generator = path_generator(epsilon)
    hamiltonian = -generator
    values = np.linalg.eigvalsh(hamiltonian)
    exact = np.array(
        [
            0.0,
            1.0 + epsilon - math.sqrt(1.0 - epsilon + epsilon**2),
            1.0 + epsilon + math.sqrt(1.0 - epsilon + epsilon**2),
        ]
    )
    exact_error = float(np.max(np.abs(values - exact)))
    assert exact_error < TOL
    assert abs(values[1] / epsilon - 1.5) < 2.0e-6

    scaled = 7.25 * generator
    scaled_values = np.linalg.eigvalsh(-scaled)
    scaling_error = float(np.max(np.abs(scaled_values - 7.25 * values)))
    assert scaling_error < TOL
    return {
        "epsilon": epsilon,
        "gap": float(values[1]),
        "gap_over_epsilon": float(values[1] / epsilon),
        "upper_level": float(values[2]),
        "formula_error": exact_error,
        "clock_scaling_error": scaling_error,
    }


def metropolis_and_barker(
    probability: np.ndarray,
    edges: list[tuple[int, int, float]],
) -> tuple[np.ndarray, np.ndarray, list[float]]:
    size = probability.size
    metropolis = np.zeros((size, size), dtype=float)
    barker = np.zeros((size, size), dtype=float)
    ratios: list[float] = []
    for left, right, attempt in edges:
        ratio = probability[right] / probability[left]
        metropolis[left, right] += attempt * min(1.0, ratio)
        metropolis[right, left] += attempt * min(1.0, 1.0 / ratio)
        barker[left, right] += attempt * ratio / (1.0 + ratio)
        barker[right, left] += attempt / (1.0 + ratio)

        c_metropolis = probability[left] * metropolis[left, right]
        c_barker = probability[left] * barker[left, right]
        ratios.append(c_barker / c_metropolis)

    np.fill_diagonal(metropolis, -metropolis.sum(axis=1))
    np.fill_diagonal(barker, -barker.sum(axis=1))
    return metropolis, barker, ratios


def check_uniform_ellipticity_comparison() -> dict:
    probability = np.array([0.03, 0.08, 0.14, 0.21, 0.22, 0.32], dtype=float)
    probability /= probability.sum()
    edges = [
        (0, 1, 0.8),
        (1, 2, 1.3),
        (2, 3, 0.5),
        (3, 4, 1.7),
        (4, 5, 0.9),
        (5, 0, 1.2),
        (1, 4, 0.6),
    ]
    metropolis, barker, ratios = metropolis_and_barker(probability, edges)
    assert detailed_balance_error(metropolis, probability) < TOL
    assert detailed_balance_error(barker, probability) < TOL

    h_metropolis = counting_basis_hamiltonian(metropolis, probability)
    h_barker = counting_basis_hamiltonian(barker, probability)
    gap_metropolis = spectral_gap(h_metropolis)
    gap_barker = spectral_gap(h_barker)

    assert min(ratios) >= 0.5 - TOL
    assert max(ratios) <= 1.0 + TOL
    assert gap_barker >= 0.5 * gap_metropolis - TOL
    assert gap_barker <= gap_metropolis + TOL

    rng = np.random.default_rng(2731)
    min_rayleigh_ratio = math.inf
    max_rayleigh_ratio = 0.0
    conductance_m = probability[:, None] * metropolis
    conductance_b = probability[:, None] * barker
    for _ in range(500):
        function = rng.normal(size=probability.size)
        function -= np.dot(probability, function)
        energy_m = 0.0
        energy_b = 0.0
        for left, right, _ in edges:
            difference = function[right] - function[left]
            energy_m += conductance_m[left, right] * difference**2
            energy_b += conductance_b[left, right] * difference**2
        ratio = energy_b / energy_m
        min_rayleigh_ratio = min(min_rayleigh_ratio, ratio)
        max_rayleigh_ratio = max(max_rayleigh_ratio, ratio)
        assert 0.5 - TOL <= ratio <= 1.0 + TOL

    return {
        "min_edge_ratio": min(ratios),
        "max_edge_ratio": max(ratios),
        "gap_metropolis": gap_metropolis,
        "gap_barker": gap_barker,
        "gap_ratio": gap_barker / gap_metropolis,
        "min_rayleigh_ratio": min_rayleigh_ratio,
        "max_rayleigh_ratio": max_rayleigh_ratio,
    }


def check_flat_hopping_vs_metropolis() -> dict:
    probability_ratios = np.logspace(-12, 12, 49)
    observed = []
    expected = []
    for ratio in probability_ratios:
        probability_left = 1.0
        probability_right = ratio
        flat_conductance = math.sqrt(probability_left * probability_right)
        metropolis_conductance = min(probability_left, probability_right)
        observed.append(flat_conductance / metropolis_conductance)
        expected.append(
            math.sqrt(
                max(probability_left, probability_right)
                / min(probability_left, probability_right)
            )
        )

    observed_array = np.asarray(observed)
    expected_array = np.asarray(expected)
    formula_error = float(np.max(np.abs(observed_array - expected_array)))
    assert formula_error < 1.0e-9
    assert float(np.min(observed_array)) >= 1.0 - TOL
    assert float(np.max(observed_array)) >= 1.0e6 - 1.0e-8
    return {
        "formula_error": formula_error,
        "min_ratio": float(np.min(observed_array)),
        "max_ratio": float(np.max(observed_array)),
    }


def main() -> None:
    parametrization = check_exact_parametrization()
    counterexample = check_three_state_counterexample()
    comparison = check_uniform_ellipticity_comparison()
    flat_comparison = check_flat_hopping_vs_metropolis()

    print("M2-W Q-TIME / DYN-UNIQUENESS CERTIFICATE")
    print(
        "detailed-balance error             = "
        f"{parametrization['balance_error']:.3e}"
    )
    print(
        "counting-basis symmetry error      = "
        f"{parametrization['symmetry_error']:.3e}"
    )
    print(
        "ground-state sqrt(pi) error        = "
        f"{parametrization['ground_error']:.3e}"
    )
    print(
        "off-diagonal kinetic error         = "
        f"{parametrization['kinetic_error']:.3e}"
    )
    print(
        "three-state epsilon                = "
        f"{counterexample['epsilon']:.1e}"
    )
    print(
        "three-state gap                    = "
        f"{counterexample['gap']:.15e}"
    )
    print(
        "gap / epsilon                      = "
        f"{counterexample['gap_over_epsilon']:.12f}"
    )
    print(
        "exact spectrum formula error       = "
        f"{counterexample['formula_error']:.3e}"
    )
    print(
        "global clock scaling error         = "
        f"{counterexample['clock_scaling_error']:.3e}"
    )
    print(
        "Barker/Metropolis edge ratios      = "
        f"{comparison['min_edge_ratio']:.6f}"
        " .. "
        f"{comparison['max_edge_ratio']:.6f}"
    )
    print(
        "Metropolis gap                     = "
        f"{comparison['gap_metropolis']:.12f}"
    )
    print(
        "Barker gap                         = "
        f"{comparison['gap_barker']:.12f}"
    )
    print(
        "Barker/Metropolis gap ratio        = "
        f"{comparison['gap_ratio']:.12f}"
    )
    print(
        "sampled Dirichlet-form ratios      = "
        f"{comparison['min_rayleigh_ratio']:.6f}"
        " .. "
        f"{comparison['max_rayleigh_ratio']:.6f}"
    )
    print(
        "flat/Metropolis conductance ratios = "
        f"{flat_comparison['min_ratio']:.6f}"
        " .. "
        f"{flat_comparison['max_ratio']:.6e}"
    )
    print(
        "flat/Metropolis formula error      = "
        f"{flat_comparison['formula_error']:.3e}"
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
