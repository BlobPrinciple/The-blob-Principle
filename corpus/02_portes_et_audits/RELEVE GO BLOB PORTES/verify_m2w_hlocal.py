#!/usr/bin/env python3
"""Independent finite-dimensional certificate for the M2-W H-LOCAL note.

The script verifies three statements used in the formal argument:

1. A nonnegative range-one half-transfer B can give a positive tridiagonal
   transfer T=B^T B whose exact logarithm has nonzero matrix elements at every
   configuration distance.
2. When T is injective, the explicit Neumann-series quasi-locality bound for
   -log(T/lambda_max) holds.
3. A local-transition support condition does not constrain amplitudes to be
   spatially local: a remote controlled amplitude generates an undiminished
   bilocal term in the exact Hamiltonian.

The numerical checks certify signs and implementation.  The proofs in the note
are analytic and do not depend on floating-point output.
"""

from __future__ import annotations

import math

import numpy as np


TOL = 5.0e-11


def symmetric_matrix_function(matrix: np.ndarray, function) -> np.ndarray:
    """Evaluate a real function on a real symmetric matrix."""
    values, vectors = np.linalg.eigh(matrix)
    return (vectors * function(values)) @ vectors.T


def path_adjacency(size: int) -> np.ndarray:
    adjacency = np.zeros((size, size), dtype=float)
    indices = np.arange(size - 1)
    adjacency[indices, indices + 1] = 1.0
    adjacency[indices + 1, indices] = 1.0
    return adjacency


def check_strict_locality_counterexample(size: int, epsilon: float) -> dict:
    """Check T=I+epsilon*A_path and its positive bidiagonal Gram factor."""
    adjacency = path_adjacency(size)
    transfer = np.eye(size) + epsilon * adjacency
    eigenvalues = np.linalg.eigvalsh(transfer)
    assert eigenvalues[0] > 0.0

    # numpy returns L with T=L L^T.  Hence B=L^T gives T=B^T B.
    half_transfer = np.linalg.cholesky(transfer).T
    gram_error = np.linalg.norm(
        transfer - half_transfer.T @ half_transfer, ord=2
    )
    assert gram_error < 100.0 * np.finfo(float).eps
    assert np.min(half_transfer) > -TOL

    allowed = np.eye(size, dtype=bool)
    allowed[np.arange(size - 1), np.arange(1, size)] = True
    assert np.max(np.abs(half_transfer[~allowed])) < TOL

    lambda_min = float(eigenvalues[0])
    lambda_max = float(eigenvalues[-1])
    hamiltonian = symmetric_matrix_function(
        transfer, lambda values: -np.log(values / lambda_max)
    )

    distance = size - 1
    far_element = float(hamiltonian[0, -1])
    analytic_leading_magnitude = epsilon**distance / distance
    expected_sign = 1.0 if distance % 2 == 0 else -1.0
    assert expected_sign * far_element > 0.0
    # Every contributing walk has parity distance, so all logarithmic-series
    # terms have the same sign; the leading shortest path is a lower bound.
    assert abs(far_element) >= analytic_leading_magnitude * (1.0 - 2.0e-6)

    q = 1.0 - lambda_min / lambda_max
    max_bound_ratio = 0.0
    for left in range(size):
        for right in range(left + 1, size):
            graph_distance = right - left
            bound = (
                q**graph_distance
                / (graph_distance * (1.0 - q))
            )
            ratio = abs(hamiltonian[left, right]) / bound
            max_bound_ratio = max(max_bound_ratio, ratio)
            assert ratio <= 1.0 + 2.0e-10

    # Independently reconstruct H from the convergent Neumann series.
    contraction = np.eye(size) - transfer / lambda_max
    series = np.zeros_like(transfer)
    power = np.eye(size)
    for order in range(1, 600):
        power = power @ contraction
        series += power / order
    series_error = np.linalg.norm(series - hamiltonian, ord=2)
    assert series_error < 2.0e-12

    return {
        "size": size,
        "condition_number": lambda_max / lambda_min,
        "far_element": far_element,
        "leading_bound": analytic_leading_magnitude,
        "max_bound_ratio": max_bound_ratio,
        "series_error": series_error,
    }


def check_dense_null_projector(size: int) -> dict:
    """Use B_{i,i}=B_{i,i+1}=1 to exhibit a dense quotient projector."""
    half_transfer = np.zeros((size - 1, size), dtype=float)
    rows = np.arange(size - 1)
    half_transfer[rows, rows] = 1.0
    half_transfer[rows, rows + 1] = 1.0
    transfer = half_transfer.T @ half_transfer

    alternating = (-1.0) ** np.arange(size)
    alternating /= np.linalg.norm(alternating)
    kernel_error = np.linalg.norm(half_transfer @ alternating)
    assert kernel_error < TOL

    projector = np.eye(size) - np.outer(alternating, alternating)
    far_projector = float(projector[0, -1])
    assert abs(abs(far_projector) - 1.0 / size) < TOL

    eigenvalues, vectors = np.linalg.eigh(transfer)
    positive = eigenvalues > 1.0e-12
    lambda_max = float(eigenvalues[positive][-1])
    physical_hamiltonian = (
        vectors[:, positive]
        * (-np.log(eigenvalues[positive] / lambda_max))
    ) @ vectors[:, positive].T
    far_hamiltonian = float(physical_hamiltonian[0, -1])
    assert abs(far_hamiltonian) > 1.0e-8

    return {
        "size": size,
        "kernel_error": kernel_error,
        "far_projector": far_projector,
        "far_physical_hamiltonian": far_hamiltonian,
    }


def check_remote_controlled_amplitude(epsilon: float) -> dict:
    """A flip at x whose positive amplitude depends on a remote bit y."""
    identity_2 = np.eye(2)
    flip_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    z_y = np.diag([1.0, -1.0])
    amplitude_y = np.diag([1.0, 2.0])

    x_operator = np.kron(flip_x, identity_2)
    xz_operator = np.kron(flip_x, z_y)
    controlled_flip = np.kron(flip_x, amplitude_y)

    half_transfer = np.eye(4) + epsilon * controlled_flip
    assert np.min(half_transfer) >= 0.0
    assert np.linalg.eigvalsh(half_transfer)[0] > 0.0

    transfer = half_transfer.T @ half_transfer
    lambda_max = float(np.linalg.eigvalsh(transfer)[-1])
    hamiltonian = symmetric_matrix_function(
        transfer, lambda values: -np.log(values / lambda_max)
    )

    # Pauli-basis coefficient: Tr(H X_x Z_y)/4.
    numerical_xz = float(np.trace(hamiltonian @ xz_operator) / 4.0)
    analytic_xz = math.atanh(2.0 * epsilon) - math.atanh(epsilon)
    assert abs(numerical_xz - analytic_xz) < 2.0e-14

    # The transition changes x only; y enters solely through its amplitude.
    transition_mask = np.abs(controlled_flip) > 0.0
    for row, col in np.argwhere(transition_mask):
        x_row, y_row = divmod(int(row), 2)
        x_col, y_col = divmod(int(col), 2)
        assert x_row != x_col
        assert y_row == y_col

    return {
        "epsilon": epsilon,
        "bilocal_xz_coefficient": numerical_xz,
        "analytic_xz_coefficient": analytic_xz,
        "unused_local_x_coefficient": float(
            np.trace(hamiltonian @ x_operator) / 4.0
        ),
    }


def main() -> None:
    epsilon = 0.2
    path_results = [
        check_strict_locality_counterexample(size, epsilon)
        for size in range(3, 13)
    ]
    kernel = check_dense_null_projector(12)
    remote = check_remote_controlled_amplitude(epsilon)

    print("M2-W H-LOCAL CERTIFICATE")
    print(f"path family epsilon                 = {epsilon:.6f}")
    print(
        "condition numbers N=3..12          = "
        f"{min(r['condition_number'] for r in path_results):.6f}"
        " .. "
        f"{max(r['condition_number'] for r in path_results):.6f}"
    )
    print(
        "largest certified distance          = "
        f"{path_results[-1]['size'] - 1}"
    )
    print(
        "far H element at that distance       = "
        f"{path_results[-1]['far_element']:+.15e}"
    )
    print(
        "shortest-path analytic lower bound   = "
        f"{path_results[-1]['leading_bound']:.15e}"
    )
    print(
        "max ratio |H_ij| / theorem bound     = "
        f"{max(r['max_bound_ratio'] for r in path_results):.6f}"
    )
    print(
        "max Neumann reconstruction error     = "
        f"{max(r['series_error'] for r in path_results):.3e}"
    )
    print(
        "dense null-projector far magnitude   = "
        f"{abs(kernel['far_projector']):.15f}"
    )
    print(
        "physical pseudolog far element       = "
        f"{kernel['far_physical_hamiltonian']:+.15e}"
    )
    print(
        "remote controlled X_x Z_y coefficient= "
        f"{remote['bilocal_xz_coefficient']:.15f}"
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
