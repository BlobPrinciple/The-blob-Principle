#!/usr/bin/env python3
"""Global interval certificate for H_QQ - zI using shell bipartiteness.

For Q = {N3=21} union {N3=22}, Pachner moves give no same-volume
off-diagonal entries.  After permutation:

    A(z) = H_QQ-zI = [[D21, C], [C.T, D22]].

If D21,D22 are positive and K=D21^(-1/2)|C|D22^(-1/2) has ||K||_2<1,
then A(z) is positive definite.  The norm is certified by applying the
Collatz-Wielandt upper bound to the nonnegative symmetric dilation
[[0,K],[K.T,0]], component by component.
"""

from __future__ import annotations

import csv
import json
import os
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from mpmath import iv
from scipy.sparse.csgraph import connected_components


ROOT = Path(
    os.environ.get(
        "D20_ROOT",
        "/workspace/scratch/9f5447c307d2/tmp/"
        "d20_repro_extract/D20_G0FIX",
    )
)


def edge_degrees(tets):
    result = {}
    for tet in tets:
        for edge in combinations(sorted(tet), 2):
            result[edge] = result.get(edge, 0) + 1
    return result


def exact_decimal(value):
    # Any strictly positive vector is valid in Collatz-Wielandt.
    # Seventeen decimal digits encode the chosen floating diagnostic vector
    # as an exact decimal interval, not as an uncertain approximation.
    return iv.mpf(format(float(value), ".17e"))


def main():
    iv.prec = int(os.environ.get("IV_PREC", "80"))
    shift = iv.mpf(os.environ.get("SHIFT", "1.5"))
    rows = [json.loads(line) for line in (ROOT / "data/states.jsonl").open()]
    adjacency = sp.load_npz(ROOT / "data/adjacency.npz").tocsr()
    with (ROOT / "data/automorphisms.csv").open(newline="") as handle:
        aut_by_id = {
            int(row["id"]): int(row["aut_order"])
            for row in csv.DictReader(handle)
        }

    mu = iv.mpf("2.3")
    alpha = iv.mpf("0.4")
    eps = iv.mpf("0.3")
    e0 = iv.mpf("1")
    half = iv.mpf("0.5")
    volumes = [len(row["tets"]) for row in rows]
    actions = []
    for row in rows:
        log_term = iv.mpf(0)
        for degree in edge_degrees(row["tets"]).values():
            log_term += iv.log(iv.mpf(1 + degree))
        actions.append(
            mu * len(row["tets"])
            - alpha * log_term
            + iv.log(iv.mpf(aut_by_id[int(row["id"])]))
        )

    def clock(delta_s):
        magnitude = abs(delta_s)
        return iv.mpf(1) - eps * magnitude / (e0 + magnitude)

    q21 = [state for state, volume in enumerate(volumes) if volume == 21]
    q22 = [state for state, volume in enumerate(volumes) if volume == 22]
    q_other = [
        state
        for state, volume in enumerate(volumes)
        if volume > 20 and volume not in (21, 22)
    ]
    if q_other:
        raise RuntimeError(f"unexpected Q-shell volumes: {q_other[:10]}")
    same_volume_nnz_21 = adjacency[np.ix_(q21, q21)].nnz
    same_volume_nnz_22 = adjacency[np.ix_(q22, q22)].nnz
    if same_volume_nnz_21 or same_volume_nnz_22:
        raise RuntimeError(
            "Q is not bipartite by volume: "
            f"nnz21={same_volume_nnz_21}, nnz22={same_volume_nnz_22}"
        )
    pos21 = {state: i for i, state in enumerate(q21)}
    pos22 = {state: j for j, state in enumerate(q22)}

    diagonal = {}
    for state in q21 + q22:
        value = iv.mpf(0)
        start, stop = adjacency.indptr[state : state + 2]
        for neighbour in adjacency.indices[start:stop]:
            delta_s = actions[int(neighbour)] - actions[state]
            value += clock(delta_s) * iv.exp(-half * delta_s)
        diagonal[state] = value - shift
        if not (diagonal[state].a > 0):
            raise RuntimeError(
                f"non-positive diagonal after shift at state {state}: "
                f"{diagonal[state]}"
            )

    # Store only nonzero normalized cross entries.
    normalized = {}
    cross_rows = []
    cross_cols = []
    for state21 in q21:
        i = pos21[state21]
        start, stop = adjacency.indptr[state21 : state21 + 2]
        for neighbour in adjacency.indices[start:stop]:
            state22 = int(neighbour)
            j = pos22.get(state22)
            if j is None:
                continue
            delta_s = actions[state22] - actions[state21]
            magnitude = clock(delta_s)
            entry = magnitude / iv.sqrt(
                diagonal[state21] * diagonal[state22]
            )
            normalized[(i, j)] = entry
            cross_rows.append(i)
            cross_cols.append(j)

    n21 = len(q21)
    n22 = len(q22)
    graph = sp.bmat(
        [
            [None, sp.csr_matrix(
                (
                    np.ones(len(cross_rows), dtype=int),
                    (cross_rows, cross_cols),
                ),
                shape=(n21, n22),
            )],
            [sp.csr_matrix(
                (
                    np.ones(len(cross_rows), dtype=int),
                    (cross_cols, cross_rows),
                ),
                shape=(n22, n21),
            ), None],
        ],
        format="csr",
    )
    component_count, labels = connected_components(
        graph,
        directed=False,
    )

    component_bounds = []
    component_passes = []
    component_upper_endpoints = []
    component_sizes = []
    for component in range(component_count):
        nodes = np.where(labels == component)[0]
        rows_component = [int(node) for node in nodes if node < n21]
        cols_component = [
            int(node - n21) for node in nodes if node >= n21
        ]
        component_sizes.append((len(rows_component), len(cols_component)))
        if not rows_component or not cols_component:
            component_bounds.append(0.0)
            component_passes.append(True)
            component_upper_endpoints.append(iv.mpf(0))
            continue

        row_local = {row: i for i, row in enumerate(rows_component)}
        col_local = {col: j for j, col in enumerate(cols_component)}
        midpoint = np.zeros(
            (len(rows_component), len(cols_component)),
            dtype=float,
        )
        for (row, col), entry in normalized.items():
            if row in row_local and col in col_local:
                midpoint[row_local[row], col_local[col]] = float(entry.mid)

        left, _, right_t = np.linalg.svd(
            midpoint,
            full_matrices=False,
        )
        left_vector_float = np.abs(left[:, 0])
        right_vector_float = np.abs(right_t[0, :])
        if (
            np.min(left_vector_float) <= 0
            or np.min(right_vector_float) <= 0
        ):
            raise RuntimeError(
                f"non-positive diagnostic Perron vector in component "
                f"{component}"
            )
        left_vector = [exact_decimal(value) for value in left_vector_float]
        right_vector = [exact_decimal(value) for value in right_vector_float]

        ratios = []
        for row in rows_component:
            numerator = iv.mpf(0)
            for col in cols_component:
                entry = normalized.get((row, col))
                if entry is not None:
                    numerator += (
                        entry * right_vector[col_local[col]]
                    )
            ratio = numerator / left_vector[row_local[row]]
            ratios.append(ratio)
        for col in cols_component:
            numerator = iv.mpf(0)
            for row in rows_component:
                entry = normalized.get((row, col))
                if entry is not None:
                    numerator += entry * left_vector[row_local[row]]
            ratio = numerator / right_vector[col_local[col]]
            ratios.append(ratio)
        component_bounds.append(max(float(ratio.b) for ratio in ratios))
        # This comparison is performed on interval endpoints, before any
        # conversion to binary float for display.
        component_passes.append(all(ratio.b < 1 for ratio in ratios))
        component_upper_endpoints.append(
            max((ratio.b for ratio in ratios), key=float)
        )

    global_bound = max(component_bounds)
    min_d21_endpoint = min(
        (diagonal[state].a for state in q21),
        key=float,
    )
    min_d22_endpoint = min(
        (diagonal[state].a for state in q22),
        key=float,
    )
    min_d21 = float(min_d21_endpoint)
    min_d22 = float(min_d22_endpoint)
    global_upper_endpoint = max(component_upper_endpoints, key=float)
    global_diagonal_lower = min(
        min_d21_endpoint,
        min_d22_endpoint,
        key=float,
    )
    certified_gap_lower = (
        global_diagonal_lower
        * (iv.mpf(1) - global_upper_endpoint)
    )
    print(f"iv_precision_bits={iv.prec}")
    print(f"shift={shift}")
    print(f"n21={n21} n22={n22}")
    print(f"same_volume_nnz_21={same_volume_nnz_21}")
    print(f"same_volume_nnz_22={same_volume_nnz_22}")
    print(f"cross_nnz={len(normalized)}")
    print(f"component_sizes={component_sizes}")
    print(f"min_D21_lower={min_d21:.17e}")
    print(f"min_D22_lower={min_d22:.17e}")
    print(
        "component_collatz_upper="
        + json.dumps(
            [format(value, ".17e") for value in component_bounds]
        )
    )
    print(f"global_norm2_upper={global_bound:.17e}")
    global_pass = all(component_passes)
    print(f"global_norm2_upper_lt_1={global_pass}")
    print(
        "certified_lambda_min_lower="
        f"{float(certified_gap_lower.a):.17e}"
    )
    print(
        "verdict="
        + (
            "PASS_INTERVAL_GLOBAL_HQQ_MINUS_SHIFT_SPD"
            if global_pass
            else "FAIL_TO_CERTIFY"
        )
    )


if __name__ == "__main__":
    main()
