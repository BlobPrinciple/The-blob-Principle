#!/usr/bin/env python3
"""D2.3-C-HIT: finite first-passage coarse kernel and true projector.

The script uses the reproduced D20 S^3 Pachner state space, the TRI2 point
(mu, alpha, b) = (2.3, 0.4, 0), and certified clock B.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import scipy.linalg as la
import scipy.sparse as sp


ROOT = Path(
    "/workspace/scratch/9f5447c307d2/tmp/"
    "d20_repro_extract/D20_G0FIX"
)
sys.path.insert(0, str(ROOT / "src"))

from action import observables_vec  # noqa: E402
from generator import build_H  # noqa: E402
from pachner import Tet  # noqa: E402


def load_model():
    states = [
        frozenset(Tet(tet) for tet in json.loads(line)["tets"])
        for line in (ROOT / "data/states.jsonl").open()
    ]
    adjacency = sp.load_npz(ROOT / "data/adjacency.npz").toarray() > 0
    with (ROOT / "data/automorphisms.csv").open(newline="") as handle:
        aut_by_id = {
            int(row["id"]): int(row["aut_order"])
            for row in csv.DictReader(handle)
        }
    automorphisms = np.array(
        [aut_by_id[index] for index in range(len(states))],
        dtype=float,
    )
    volumes = np.array([len(state) for state in states], dtype=int)
    observables = observables_vec(states)
    couplings = np.array([2.3, 0.4, 0.0])
    action = couplings @ observables + np.log(automorphisms)
    hamiltonian, probability = build_H(
        adjacency,
        action,
        "B",
        0.3,
        1.0,
    )
    sqrt_probability = np.sqrt(probability)
    generator = (
        -hamiltonian
        * sqrt_probability[None, :]
        / sqrt_probability[:, None]
    )
    return {
        "states": states,
        "adjacency": adjacency,
        "automorphisms": automorphisms,
        "volumes": volumes,
        "observables": observables,
        "couplings": couplings,
        "action": action,
        "hamiltonian": hamiltonian,
        "probability": probability,
        "generator": generator,
    }


def first_hitting_kernel(generator, boundary):
    """Return C(y|x) for first entry into the boundary set."""
    n = generator.shape[0]
    boundary = np.asarray(boundary, dtype=int)
    boundary_mask = np.zeros(n, dtype=bool)
    boundary_mask[boundary] = True
    interior = np.where(~boundary_mask)[0]
    killed = -generator[np.ix_(interior, interior)]
    entrance = generator[np.ix_(interior, boundary)]
    interior_kernel = la.solve(
        killed,
        entrance,
        assume_a="gen",
        check_finite=False,
    )
    kernel = np.zeros((n, len(boundary)))
    kernel[boundary, np.arange(len(boundary))] = 1.0
    kernel[interior, :] = interior_kernel
    return kernel, interior, killed


def weighted_static_fit(observables, coarse_probability):
    design = np.column_stack(
        [np.ones(observables.shape[1]), observables.T]
    )
    weighted_design = design * np.sqrt(coarse_probability)[:, None]
    return design, weighted_design


def main():
    model = load_model()
    adjacency = model["adjacency"]
    volumes = model["volumes"]
    observables = model["observables"]
    automorphisms = model["automorphisms"]
    hamiltonian = model["hamiltonian"]
    probability = model["probability"]
    generator = model["generator"]
    n = len(volumes)

    graph = nx.from_numpy_array(adjacency.astype(int))
    components = list(nx.connected_components(graph))
    if len(components) != 1:
        raise RuntimeError(f"full Pachner graph is disconnected: {len(components)}")

    p20 = np.where(volumes <= 20)[0]
    p18 = np.where(volumes <= 18)[0]
    c20, q20, killed20 = first_hitting_kernel(generator, p20)
    c18, _, killed18 = first_hitting_kernel(generator, p18)

    # Independent symmetric formulation:
    # C_Q = -D_Q^{-1} H_QQ^{-1} H_QP D_P.
    sqrt_probability = np.sqrt(probability)
    h_qq_coordinate = hamiltonian[np.ix_(q20, q20)]
    h_qp_coordinate = hamiltonian[np.ix_(q20, p20)]
    c20_symmetric_q = (
        -la.solve(
            h_qq_coordinate,
            h_qp_coordinate * sqrt_probability[p20][None, :],
            assume_a="sym",
            check_finite=False,
        )
        / sqrt_probability[q20][:, None]
    )
    hitting_two_formulations_error = float(
        np.max(np.abs(c20[q20, :] - c20_symmetric_q))
    )
    harmonic_residual = float(
        np.max(
            np.abs(
                generator[np.ix_(q20, q20)] @ c20[q20, :]
                + generator[np.ix_(q20, p20)]
            )
        )
    )

    row_sum_error = float(np.max(np.abs(c20.sum(axis=1) - 1.0)))
    negative_min = float(np.min(c20))
    generator_row_error = float(np.max(np.abs(generator.sum(axis=1))))
    stationarity_error = float(np.max(np.abs(probability @ generator)))
    detailed_balance_error = float(
        np.max(
            np.abs(
                probability[:, None] * generator
                - probability[None, :] * generator.T
            )
        )
    )
    semigroup_error = float(
        np.max(np.abs(c20 @ c18[p20, :] - c18))
    )

    coarse_probability = c20.T @ probability
    coarse_probability /= coarse_probability.sum()
    sqrt_coarse = np.sqrt(coarse_probability)
    k_symmetric = (
        sqrt_probability[:, None]
        * c20
        / sqrt_coarse[None, :]
    )
    m_symmetric = k_symmetric.T @ k_symmetric
    m_eigenvalues, m_eigenvectors = np.linalg.eigh(m_symmetric)
    inverse_sqrt_m = (
        m_eigenvectors
        @ np.diag(1.0 / np.sqrt(m_eigenvalues))
        @ m_eigenvectors.T
    )
    j_map = k_symmetric @ inverse_sqrt_m
    isometry_error = float(
        np.linalg.norm(j_map.T @ j_map - np.eye(len(p20)), ord=2)
    )
    fine_ground = sqrt_probability
    coarse_ground = sqrt_coarse
    ground_lift_error = float(
        np.linalg.norm(j_map @ coarse_ground - fine_ground)
    )

    # Complete orthonormal basis: range(J) plus its Euclidean orthogonal
    # complement in the symmetrized Hilbert space.
    orthogonal, _ = la.qr(
        j_map,
        mode="full",
        check_finite=False,
    )
    complement = orthogonal[:, len(p20) :]
    complement_error = float(np.linalg.norm(complement.T @ j_map, ord=2))
    range_projector_error = float(
        np.linalg.norm(
            orthogonal[:, : len(p20)]
            @ orthogonal[:, : len(p20)].T
            - j_map @ j_map.T,
            ord=2,
        )
    )

    h_cc = j_map.T @ hamiltonian @ j_map
    h_cq = j_map.T @ hamiltonian @ complement
    h_qq = complement.T @ hamiltonian @ complement
    hqq_eigenvalues = np.linalg.eigvalsh(h_qq)
    low_h_eigenvalues, low_h_vectors = la.eigh(
        hamiltonian,
        subset_by_index=[0, 2],
        check_finite=False,
    )
    lambda_one = float(low_h_eigenvalues[1])

    feshbach_zero = h_cc - h_cq @ la.solve(
        h_qq,
        h_cq.T,
        assume_a="sym",
        check_finite=False,
    )
    feshbach_zero_eigenvalues = np.linalg.eigvalsh(feshbach_zero)
    feshbach_ground_error = float(
        np.linalg.norm(feshbach_zero @ coarse_ground)
        / np.linalg.norm(coarse_ground)
    )

    hqq_lambda_margin = float(hqq_eigenvalues[0] - lambda_one)
    if hqq_lambda_margin > 0:
        shifted_qq = h_qq - lambda_one * np.eye(len(q20))
        feshbach_lambda = (
            h_cc
            - lambda_one * np.eye(len(p20))
            - h_cq
            @ la.solve(
                shifted_qq,
                h_cq.T,
                assume_a="sym",
                check_finite=False,
            )
        )
        coarse_mode = j_map.T @ low_h_vectors[:, 1]
        feshbach_lambda_residual = float(
            np.linalg.norm(feshbach_lambda @ coarse_mode)
            / np.linalg.norm(coarse_mode)
        )
    else:
        feshbach_lambda_residual = math.nan

    # Exact static push-forward relative to the orbit measure 1/|Aut|.
    coarse_observables = observables[:, p20]
    coarse_aut = automorphisms[p20]
    effective_action = -np.log(coarse_probability * coarse_aut)
    design = np.column_stack(
        [np.ones(len(p20)), coarse_observables.T]
    )
    weighted = np.sqrt(coarse_probability)
    coefficients, *_ = np.linalg.lstsq(
        design * weighted[:, None],
        effective_action * weighted,
        rcond=None,
    )
    fitted = design @ coefficients
    residual = effective_action - fitted
    fit_weighted_rms = float(
        np.sqrt(np.sum(coarse_probability * residual**2))
    )
    fit_max = float(np.max(np.abs(residual)))

    conditional_p20 = probability[p20] / probability[p20].sum()
    push_vs_conditional_l1 = float(
        np.sum(np.abs(coarse_probability - conditional_p20))
    )
    q_mass = float(probability[q20].sum())
    mean_volume_fine = float(probability @ volumes)
    mean_volume_coarse = float(coarse_probability @ volumes[p20])
    ell_effective = float(
        (mean_volume_fine / mean_volume_coarse) ** (1.0 / 3.0)
    )
    conditional_q = probability[q20] / probability[q20].sum()
    shell_pushforward = c20[q20, :].T @ conditional_q
    shell_pushforward /= shell_pushforward.sum()
    shell_mean_fine = float(conditional_q @ volumes[q20])
    shell_mean_coarse = float(shell_pushforward @ volumes[p20])
    shell_ell_effective = float(
        (shell_mean_fine / shell_mean_coarse) ** (1.0 / 3.0)
    )
    shell_output_by_volume = {
        str(int(volume)): float(
            shell_pushforward[volumes[p20] == volume].sum()
        )
        for volume in np.unique(volumes[p20])
        if shell_pushforward[volumes[p20] == volume].sum() > 1e-15
    }

    output = {
        "model": {
            "n_states": n,
            "p20_size": int(len(p20)),
            "q20_size": int(len(q20)),
            "p18_size": int(len(p18)),
            "clock": "B",
            "point": {"mu": 2.3, "alpha": 0.4, "b": 0.0},
        },
        "markov": {
            "generator_row_sum_error": generator_row_error,
            "stationarity_error": stationarity_error,
            "detailed_balance_error": detailed_balance_error,
            "hitting_min_entry": negative_min,
            "hitting_row_sum_error": row_sum_error,
            "hitting_two_formulations_error": hitting_two_formulations_error,
            "hitting_harmonic_residual": harmonic_residual,
            "semigroup_22_20_18_error": semigroup_error,
            "killed20_condition_2": float(np.linalg.cond(killed20)),
            "killed18_condition_2": float(np.linalg.cond(killed18)),
        },
        "polar_identification": {
            "coarse_probability_sum": float(coarse_probability.sum()),
            "coarse_probability_min": float(coarse_probability.min()),
            "M_lambda_min": float(m_eigenvalues[0]),
            "M_lambda_max": float(m_eigenvalues[-1]),
            "M_condition": float(m_eigenvalues[-1] / m_eigenvalues[0]),
            "J_isometry_error_2": isometry_error,
            "J_ground_lift_error_2": ground_lift_error,
            "complement_orthogonality_error_2": complement_error,
            "range_projector_error_2": range_projector_error,
        },
        "true_projector_chart": {
            "lambda_1_H": lambda_one,
            "lambda_min_QHQ": float(hqq_eigenvalues[0]),
            "lambda_max_QHQ": float(hqq_eigenvalues[-1]),
            "margin_QHQ_minus_lambda1": hqq_lambda_margin,
            "F0_lambda_min": float(feshbach_zero_eigenvalues[0]),
            "F0_lambda_1": float(feshbach_zero_eigenvalues[1]),
            "F0_ground_residual": feshbach_ground_error,
            "Flambda1_kernel_residual": feshbach_lambda_residual,
        },
        "static_pushforward": {
            "fine_Q_mass": q_mass,
            "pushforward_vs_conditional_L1": push_vs_conditional_l1,
            "mean_N3_fine": mean_volume_fine,
            "mean_N3_coarse": mean_volume_coarse,
            "ell_effective": ell_effective,
            "shell_mean_N3_fine": shell_mean_fine,
            "shell_mean_N3_coarse": shell_mean_coarse,
            "shell_ell_effective": shell_ell_effective,
            "shell_output_mass_by_N3": shell_output_by_volume,
            "fit_intercept": float(coefficients[0]),
            "fit_mu": float(coefficients[1]),
            "fit_alpha": float(coefficients[2]),
            "fit_b": float(coefficients[3]),
            "fit_weighted_RMS": fit_weighted_rms,
            "fit_max_abs": fit_max,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
