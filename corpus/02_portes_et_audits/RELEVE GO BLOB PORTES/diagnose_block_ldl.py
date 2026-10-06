#!/usr/bin/env python3
"""Floating-point diagnostic for a 40-state block LDL order (not a proof)."""

from __future__ import annotations

import json
import os
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

from action import aut_order, observables_vec  # noqa: E402
from generator import build_H  # noqa: E402
from pachner import Tet  # noqa: E402


def main() -> None:
    states = [
        frozenset(Tet(tet) for tet in json.loads(line)["tets"])
        for line in (ROOT / "data/states.jsonl").open()
    ]
    adjacency = sp.load_npz(ROOT / "data/adjacency.npz").toarray() > 0
    component = np.array(
        sorted(
            next(
                comp
                for comp in nx.connected_components(
                    nx.from_numpy_array(adjacency.astype(int))
                )
                if 0 in comp
            )
        )
    )
    volumes = np.array([len(state) for state in states])
    observables = observables_vec(states)
    auts = np.array([aut_order(state) for state in states], dtype=float)
    action = np.array([2.3, 0.4, 0.0]) @ observables + np.log(auts)
    hamiltonian, _ = build_H(
        adjacency[np.ix_(component, component)],
        action[component],
        "A",
        0.3,
        1.0,
    )
    q = np.where(volumes[component] > 20)[0]
    shift = float(os.environ.get("LDL_SHIFT", "0.0"))
    work = hamiltonian[np.ix_(q, q)].copy() - shift * np.eye(len(q))

    block_size = 40
    summaries = []
    offset = 0
    block_number = 0
    while offset < len(work):
        width = min(block_size, len(work) - offset)
        pivot = work[offset : offset + width, offset : offset + width]
        eig_min = float(np.linalg.eigvalsh(pivot)[0])
        summaries.append((block_number, offset, width, eig_min))
        if offset + width < len(work):
            cross = work[offset + width :, offset : offset + width]
            factor = la.cho_factor(pivot, lower=True, check_finite=False)
            solved = la.cho_solve(factor, cross.T, check_finite=False)
            work[offset + width :, offset + width :] -= cross @ solved
            work[offset + width :, offset : offset + width] = 0.0
            work[offset : offset + width, offset + width :] = 0.0
        offset += width
        block_number += 1

    for item in summaries:
        print(
            "block=%02d offset=%03d size=%02d lambda_min=%.17e"
            % item
        )
    print(
        "weakest_block=%d weakest_lambda_min=%.17e"
        % min(((b, value) for b, _, _, value in summaries), key=lambda x: x[1])
    )
    print(f"shift={shift:.17e}")


if __name__ == "__main__":
    main()
