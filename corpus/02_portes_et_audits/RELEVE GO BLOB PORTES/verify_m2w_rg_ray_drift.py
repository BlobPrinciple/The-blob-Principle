#!/usr/bin/env python3
"""Deterministic checks for the M2-W RG-RAY transversality theorem.

The proof is analytic.  This certificate independently checks:
  * the finite tuple-count dimensions at bounded edge coordination;
  * the first-b derivative of the exact R_z tangent by finite differences;
  * its decomposition in the (N3, Delta, X56) basis on several reachable
    triangulations of T^3;
  * the non-zero normal drift away from g_Delta = A g_X.
"""

from __future__ import annotations

import math
from collections import Counter

from verify_m2w_rg_ray import (
    apply_one_to_four,
    tetrahedron_edge_sum_histogram,
    x56,
)
from verify_m2w_topology_fvector import (
    apply_two_to_three,
    freudenthal_torus,
    incidence_counts,
)


def close(a: float, b: float, *, rel: float = 1e-10, abs_: float = 1e-10) -> None:
    if not math.isclose(a, b, rel_tol=rel, abs_tol=abs_):
        raise AssertionError(f"{a!r} != {b!r}")


def n1(tetrahedra: set[tuple[int, int, int, int]]) -> int:
    edge_degree, _ = incidence_counts(tetrahedra)
    return len(edge_degree)


def c1(tetrahedra: set[tuple[int, int, int, int]]) -> int:
    edge_degree, _ = incidence_counts(tetrahedra)
    return sum(degree * degree for degree in edge_degree.values())


def rz_tangent(
    tetrahedra: set[tuple[int, int, int, int]],
    b: float,
    kappa: float,
) -> float:
    """Return dS'_z/dz at z=0, with mu=0."""
    histogram = tetrahedron_edge_sum_histogram(tetrahedra)
    y_b = sum(
        multiplicity * math.exp(-2.0 * b * edge_sum)
        for edge_sum, multiplicity in histogram.items()
    )
    return -math.exp(-b * kappa) * y_b


def tuple_dimension(n_max: int) -> int:
    if n_max < 3:
        raise ValueError("closed 3-manifold edge degrees start at 3")
    number_of_allowed_degrees = n_max - 2
    return math.comb(number_of_allowed_degrees + 5, 6)


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """Solve a small dense system by pivoted Gaussian elimination."""
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    size = len(augmented)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise AssertionError("singular witness matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][index] - factor * augmented[column][index]
                for index in range(size + 1)
            ]
    return [augmented[row][-1] for row in range(size)]


def main() -> None:
    theta = math.acos(1.0 / 3.0)
    d_star = 2.0 * math.pi / theta
    r_star = 6.0 / d_star
    a_ray = d_star * d_star - 30.0
    kappa = 4.0 * d_star * d_star - 36.0 * d_star + 42.0

    expected_dimensions = {
        7: 210,
        8: 462,
        10: 1716,
        12: 5005,
        16: 27132,
    }
    for n_max, expected in expected_dimensions.items():
        measured = tuple_dimension(n_max)
        if measured != expected:
            raise AssertionError((n_max, measured, expected))

    # Reachable, topology-preserving T^3 configurations.
    state_0 = freudenthal_torus(3)
    state_1 = apply_two_to_three(state_0, (0, 1, 4), 18, 13)
    state_a = apply_two_to_three(state_1, (3, 6, 15), 16, 5)
    state_b = apply_two_to_three(state_1, (3, 6, 16), 15, 7)
    state_4 = apply_one_to_four(state_1, (0, 1, 6, 10))
    states = [state_0, state_1, state_a, state_b, state_4]

    beta_delta = -60.0
    beta_x = 2.0
    beta_volume = kappa + 132.0 - 60.0 * r_star
    beta_normal = beta_delta - a_ray * beta_x
    expected_normal = -2.0 * d_star * d_star
    close(beta_normal, expected_normal, rel=1e-13, abs_=1e-13)

    epsilon = 1.0e-6
    maximum_relative_fd_error = 0.0
    witness_matrix = []
    witness_vector = []
    for state in states:
        n3_value = len(state)
        n1_value = n1(state)
        delta_value = n1_value - r_star * n3_value
        x_value = x56(state)
        c1_value = c1(state)

        # Exact incidence reduction:
        # C1 = X56 - 30 Delta + (66-30 r*) N3.
        predicted_c1 = (
            x_value
            - 30.0 * delta_value
            + (66.0 - 30.0 * r_star) * n3_value
        )
        close(c1_value, predicted_c1, rel=1e-13, abs_=1e-10)

        exact_b_derivative = kappa * n3_value + 2.0 * c1_value
        basis_b_derivative = (
            beta_volume * n3_value
            + beta_delta * delta_value
            + beta_x * x_value
        )
        close(exact_b_derivative, basis_b_derivative, rel=1e-13, abs_=1e-9)

        finite_difference = (
            rz_tangent(state, epsilon, kappa)
            - rz_tangent(state, -epsilon, kappa)
        ) / (2.0 * epsilon)
        relative_error = abs(finite_difference - exact_b_derivative) / abs(
            exact_b_derivative
        )
        maximum_relative_fd_error = max(maximum_relative_fd_error, relative_error)
        close(finite_difference, exact_b_derivative, rel=2e-8, abs_=2e-5)
        if len(witness_matrix) < 3 and state in (state_0, state_1, state_4):
            witness_matrix.append([n3_value, delta_value, x_value])
            witness_vector.append(exact_b_derivative)

    fitted_volume, fitted_delta, fitted_x = solve_linear_system(
        witness_matrix,
        witness_vector,
    )
    close(fitted_volume, beta_volume, rel=1e-12, abs_=1e-10)
    close(fitted_delta, beta_delta, rel=1e-12, abs_=1e-10)
    close(fitted_x, beta_x, rel=1e-12, abs_=1e-10)

    print("M2-W RG-RAY TRANSVERSALITY CERTIFICATE")
    print("tuple-count dimensions:")
    for n_max, dimension in expected_dimensions.items():
        print(
            f"  n_max={n_max:2d}: C(n_max+3,6) = "
            f"{tuple_dimension(n_max)}"
        )
    print(f"d_star                         = {d_star:.15f}")
    print(f"A=d_star^2-30                 = {a_ray:+.15f}")
    print(f"kappa                         = {kappa:+.15f}")
    print("first-order R_z coefficients (mu=0):")
    print(f"  beta_Delta / b              = {beta_delta:+.15f}")
    print(f"  beta_X / b                  = {beta_x:+.15f}")
    print(
        "  independently fitted       = "
        f"({fitted_delta:+.12f}, {fitted_x:+.12f})"
    )
    print(f"  (beta_Delta-A beta_X) / b   = {beta_normal:+.15f}")
    print(f"  -2 d_star^2                 = {expected_normal:+.15f}")
    print(f"reachable T3 states checked   = {len(states)}")
    print(f"max central-FD relative error = {maximum_relative_fd_error:.3e}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
