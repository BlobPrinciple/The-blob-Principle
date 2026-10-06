#!/usr/bin/env python3
"""First genuinely propagated interval pivot for the D20 shell.

Blocks 0..5 consist only of N3=21 states and have no mutual Pachner edges.
Block 6 contains the final 12 N3=21 states and the first 28 N3=22 states.
It is therefore the first pivot that receives nonzero Schur corrections from
earlier blocks.
"""

from __future__ import annotations

import csv
import json
import os
from itertools import combinations
from pathlib import Path

import scipy.sparse as sp
from mpmath import iv


ROOT = Path(
    os.environ.get(
        "D20_ROOT",
        "/workspace/scratch/9f5447c307d2/tmp/"
        "d20_repro_extract/D20_G0FIX",
    )
)
BLOCK_SIZE = 40
TARGET = 6


def edge_degrees(tets):
    result = {}
    for tet in tets:
        for edge in combinations(sorted(tet), 2):
            result[edge] = result.get(edge, 0) + 1
    return result


def interval_cholesky(matrix):
    n = len(matrix)
    factor = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    for j in range(n):
        pivot = matrix[j][j]
        for k in range(j):
            pivot -= factor[j][k] * factor[j][k]
        if not (pivot.a > 0):
            raise RuntimeError(f"unresolved pivot {j}: {pivot}")
        pivots.append(pivot)
        factor[j][j] = iv.sqrt(pivot)
        for i in range(j + 1, n):
            value = matrix[i][j]
            for k in range(j):
                value -= factor[i][k] * factor[j][k]
            factor[i][j] = value / factor[j][j]
    return factor, pivots


def solve_cholesky(factor, rhs):
    n = len(factor)
    forward = [iv.mpf(0) for _ in range(n)]
    for i in range(n):
        value = rhs[i]
        for k in range(i):
            value -= factor[i][k] * forward[k]
        forward[i] = value / factor[i][i]
    result = [iv.mpf(0) for _ in range(n)]
    for i in reversed(range(n)):
        value = forward[i]
        for k in range(i + 1, n):
            value -= factor[k][i] * result[k]
        result[i] = value / factor[i][i]
    return result


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

    q = [state for state, volume in enumerate(volumes) if volume > 20]
    blocks = [
        q[index * BLOCK_SIZE : (index + 1) * BLOCK_SIZE]
        for index in range(TARGET + 1)
    ]
    positions = [
        {state: local for local, state in enumerate(block)}
        for block in blocks
    ]

    diagonal_cache = {}

    def diagonal(state):
        if state not in diagonal_cache:
            value = iv.mpf(0)
            start, stop = adjacency.indptr[state : state + 2]
            for neighbour in adjacency.indices[start:stop]:
                delta_s = actions[int(neighbour)] - actions[state]
                value += clock(delta_s) * iv.exp(-half * delta_s)
            diagonal_cache[state] = value
        return diagonal_cache[state]

    def diagonal_block(index):
        block = blocks[index]
        position = positions[index]
        n = len(block)
        matrix = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
        for i, state in enumerate(block):
            start, stop = adjacency.indptr[state : state + 2]
            for neighbour in adjacency.indices[start:stop]:
                local = position.get(int(neighbour))
                if local is not None:
                    delta_s = actions[int(neighbour)] - actions[state]
                    matrix[i][local] = -clock(delta_s)
            matrix[i][i] = diagonal(state) - shift
        return matrix

    def cross_block(left_index, right_index):
        left = blocks[left_index]
        right_position = positions[right_index]
        matrix = [
            [iv.mpf(0) for _ in range(len(blocks[right_index]))]
            for _ in range(len(left))
        ]
        nonzero = 0
        for i, state in enumerate(left):
            start, stop = adjacency.indptr[state : state + 2]
            for neighbour in adjacency.indices[start:stop]:
                local = right_position.get(int(neighbour))
                if local is not None:
                    delta_s = actions[int(neighbour)] - actions[state]
                    matrix[i][local] = -clock(delta_s)
                    nonzero += 1
        return matrix, nonzero

    target_matrix = diagonal_block(TARGET)
    source_summaries = []
    for source in range(TARGET):
        source_matrix = diagonal_block(source)
        source_factor, source_pivots = interval_cholesky(source_matrix)
        cross, nonzero = cross_block(TARGET, source)
        source_summaries.append(
            (
                source,
                nonzero,
                min(float(pivot.a) for pivot in source_pivots),
                max(float(pivot.delta) for pivot in source_pivots),
            )
        )
        if nonzero == 0:
            continue
        solved_columns = [
            solve_cholesky(source_factor, cross[row])
            for row in range(len(blocks[TARGET]))
        ]
        for i in range(len(blocks[TARGET])):
            for j in range(len(blocks[TARGET])):
                target_matrix[i][j] -= sum(
                    cross[i][k] * solved_columns[j][k]
                    for k in range(len(blocks[source]))
                )

    _, target_pivots = interval_cholesky(target_matrix)
    print(f"iv_precision_bits={iv.prec}")
    print(f"target_block={TARGET}")
    print(
        "target_volume_counts="
        + json.dumps(
            {
                str(volume): sum(
                    1 for state in blocks[TARGET]
                    if volumes[state] == volume
                )
                for volume in sorted(
                    {volumes[state] for state in blocks[TARGET]}
                )
            },
            sort_keys=True,
        )
    )
    for source, nonzero, lower, width in source_summaries:
        print(
            f"source={source} cross_nnz={nonzero} "
            f"min_pivot_lower={lower:.17e} "
            f"max_pivot_width={width:.17e}"
        )
    print("target_pivots_positive=40/40")
    print(
        "target_min_pivot_lower="
        f"{min(float(pivot.a) for pivot in target_pivots):.17e}"
    )
    print(
        "target_max_pivot_width="
        f"{max(float(pivot.delta) for pivot in target_pivots):.17e}"
    )


if __name__ == "__main__":
    main()
