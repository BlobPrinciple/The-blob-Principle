#!/usr/bin/env python3
"""Independent reconstruction of the reported D2.1 CHART-BLOCK-0 certificate.

Uses only D20 data, the printed TRI2 point, and elementary interval operations.
It deliberately does not import the D20 action/generator/Feshbach modules.
"""

from __future__ import annotations

import json
import csv
import os
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from mpmath import iv


ROOT = Path(
    "/workspace/scratch/9f5447c307d2/tmp/"
    "d20_repro_extract/D20_G0FIX"
)


def edge_degrees(tets: list[list[int]]) -> dict[tuple[int, int], int]:
    out: dict[tuple[int, int], int] = {}
    for tet in tets:
        for edge in combinations(sorted(tet), 2):
            out[edge] = out.get(edge, 0) + 1
    return out


def lower_endpoint(x):
    # Converting the interval endpoint to a decimal string avoids binary float.
    return iv.mpf(x).a


def main() -> None:
    iv.prec = int(os.environ.get("IV_PREC", "80"))
    rows = [json.loads(line) for line in (ROOT / "data/states.jsonl").open()]
    adjacency = sp.load_npz(ROOT / "data/adjacency.npz").tocsr()
    with (ROOT / "data/automorphisms.csv").open(newline="") as handle:
        aut_by_id = {
            int(row["id"]): int(row["aut_order"])
            for row in csv.DictReader(handle)
        }

    mu = iv.mpf("2.3")
    alpha = iv.mpf("0.4")
    half = iv.mpf("0.5")
    shift = iv.mpf("1.5")

    actions = []
    volumes = []
    for row in rows:
        tets = row["tets"]
        volumes.append(len(tets))
        log_term = iv.mpf(0)
        for degree in edge_degrees(tets).values():
            log_term += iv.log(iv.mpf(1 + degree))
        aut = iv.mpf(aut_by_id[int(row["id"])])
        # S = mu*N3 - alpha*sum_e log(1+n_e) + log|Aut|.
        actions.append(mu * len(tets) - alpha * log_term + iv.log(aut))

    q_indices = [i for i, volume in enumerate(volumes) if volume > 20]
    block_indices = q_indices[:40]
    block_pos = {state: pos for pos, state in enumerate(block_indices)}
    n = len(block_indices)

    block = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
    for local_i, state_i in enumerate(block_indices):
        start, stop = adjacency.indptr[state_i : state_i + 2]
        neighbours = adjacency.indices[start:stop]
        diagonal = iv.mpf(0)
        for state_j in neighbours:
            diagonal += iv.exp(-half * (actions[state_j] - actions[state_i]))
            local_j = block_pos.get(int(state_j))
            if local_j is not None:
                block[local_i][local_j] = iv.mpf(-1)
        block[local_i][local_i] = diagonal - shift

    # Elementary interval Cholesky. Positive pivot intervals certify SPD.
    chol = [[iv.mpf(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    for i in range(n):
        pivot = block[i][i]
        for k in range(i):
            pivot -= chol[i][k] * chol[i][k]
        if not (pivot.a > 0):
            raise RuntimeError(f"non-positive or unresolved pivot {i}: {pivot}")
        pivots.append(pivot)
        chol[i][i] = iv.sqrt(pivot)
        for j in range(i + 1, n):
            value = block[j][i]
            for k in range(i):
                value -= chol[j][k] * chol[i][k]
            chol[j][i] = value / chol[i][i]

    # An ordinary eigensolve is diagnostic only; it is not part of the proof.
    midpoint_block = np.array(
        [[float(entry.mid) for entry in row] for row in block]
    )
    eig_min = float(np.linalg.eigvalsh(midpoint_block)[0])
    widths = [
        float(pivot.delta)
        for pivot in pivots
    ]
    print(f"block_size={n}")
    print(f"iv_precision_bits={iv.prec}")
    print(f"q_size={len(q_indices)}")
    print(f"first_q_index={block_indices[0]}")
    print(f"last_block_q_index={block_indices[-1]}")
    print(f"all_interval_pivots_positive=True")
    print(f"min_pivot_lower={min(float(pivot.a) for pivot in pivots):.17e}")
    print(f"max_pivot_width={max(widths):.17e}")
    print(f"diagnostic_lambda_min_B_minus_1p5I={eig_min:.17e}")


if __name__ == "__main__":
    main()
