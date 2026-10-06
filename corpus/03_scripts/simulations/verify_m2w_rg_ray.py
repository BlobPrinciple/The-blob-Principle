#!/usr/bin/env python3
"""Deterministic certificate for the M2-W operator/ray analysis.

The analytic proof is independent of this program.  The program supplies
explicit reachable witnesses on a periodic Freudenthal triangulation of T^3:
two legal Pachner moves with identical changes of (N3, Delta) but different
changes of X_56.
"""

from __future__ import annotations

from collections import Counter
import math

from verify_m2w_topology_fvector import (
    apply_two_to_three,
    faces_of,
    freudenthal_torus,
    incidence_counts,
    legal_two_to_three_faces,
)


def x56(tetrahedra: set[tuple[int, int, int, int]]) -> int:
    edge_degree, _ = incidence_counts(tetrahedra)
    return sum((degree - 5) * (degree - 6) for degree in edge_degree.values())


def apply_one_to_four(
    tetrahedra: set[tuple[int, int, int, int]],
    tetrahedron: tuple[int, int, int, int],
) -> set[tuple[int, int, int, int]]:
    if tetrahedron not in tetrahedra:
        raise AssertionError("tetrahedron is absent")
    new_vertex = 1 + max(vertex for tet in tetrahedra for vertex in tet)
    result = set(tetrahedra)
    result.remove(tetrahedron)
    for face in faces_of(tetrahedron, 3):
        result.add(tuple(sorted((*face, new_vertex))))
    return result


def move_23_local_sums(
    tetrahedra: set[tuple[int, int, int, int]],
    move: tuple[tuple[int, int, int], int, int],
) -> tuple[int, int]:
    face, u, v = move
    edge_degree, _ = incidence_counts(tetrahedra)
    face_edges = faces_of(face, 2)
    outer_edges = {
        tuple(sorted((vertex, opposite)))
        for vertex in face
        for opposite in (u, v)
    }
    return (
        sum(edge_degree[edge] for edge in face_edges),
        sum(edge_degree[edge] for edge in outer_edges),
    )


def move_14_edge_sum(
    tetrahedra: set[tuple[int, int, int, int]],
    tetrahedron: tuple[int, int, int, int],
) -> int:
    edge_degree, _ = incidence_counts(tetrahedra)
    return sum(edge_degree[edge] for edge in faces_of(tetrahedron, 2))


def edge_degree_histogram(
    tetrahedra: set[tuple[int, int, int, int]],
) -> Counter[int]:
    edge_degree, _ = incidence_counts(tetrahedra)
    return Counter(edge_degree.values())


def tetrahedron_edge_sum_histogram(
    tetrahedra: set[tuple[int, int, int, int]],
) -> Counter[int]:
    edge_degree, _ = incidence_counts(tetrahedra)
    return Counter(
        sum(edge_degree[edge] for edge in faces_of(tetrahedron, 2))
        for tetrahedron in tetrahedra
    )


def tetrahedron_degree_tuple_histogram(
    tetrahedra: set[tuple[int, int, int, int]],
) -> Counter[tuple[int, int, int, int, int, int]]:
    edge_degree, _ = incidence_counts(tetrahedra)
    return Counter(
        tuple(sorted(edge_degree[edge] for edge in faces_of(tetrahedron, 2)))
        for tetrahedron in tetrahedra
    )


def refinement_tangent(
    tetrahedra: set[tuple[int, int, int, int]],
    b: float,
) -> float:
    """Return Y_b = sum_t exp(-2 b sum_{e subset t} n_e).

    Overall factors depending only on mu, b, and d_star are omitted because
    they are identical for the two witness configurations.
    """
    histogram = tetrahedron_edge_sum_histogram(tetrahedra)
    return sum(
        multiplicity * math.exp(-2.0 * b * edge_sum)
        for edge_sum, multiplicity in histogram.items()
    )


def main() -> None:
    initial = freudenthal_torus(3)
    first_move = ((0, 1, 4), 18, 13)
    if first_move not in legal_two_to_three_faces(initial):
        raise AssertionError("declared first move is not legal")
    state = apply_two_to_three(initial, *first_move)

    # Same move type => same Delta N3 and Delta Delta.  Different Delta X56
    # therefore proves operational independence on the reachable T^3 sector.
    witnesses_23 = (
        ((0, 1, 13), 10, 18),
        ((0, 1, 10), 13, 6),
    )
    results_23 = []
    for move in witnesses_23:
        if move not in legal_two_to_three_faces(state):
            raise AssertionError(f"declared 2->3 move is not legal: {move}")
        face_sum, outer_sum = move_23_local_sums(state, move)
        moved = apply_two_to_three(state, *move)
        measured = x56(moved) - x56(state)
        predicted = 2 * (outer_sum - face_sum) - 18
        if measured != predicted:
            raise AssertionError((move, measured, predicted))
        results_23.append((move, face_sum, outer_sum, measured))
    if results_23[0][3] == results_23[1][3]:
        raise AssertionError("2->3 witnesses failed to separate X56")

    witnesses_14 = (
        (0, 1, 6, 10),
        (0, 4, 13, 18),
    )
    results_14 = []
    for tetrahedron in witnesses_14:
        edge_sum = move_14_edge_sum(state, tetrahedron)
        moved = apply_one_to_four(state, tetrahedron)
        measured = x56(moved) - x56(state)
        predicted = 2 * edge_sum - 36
        if measured != predicted:
            raise AssertionError((tetrahedron, measured, predicted))
        results_14.append((tetrahedron, edge_sum, measured))
    if results_14[0][2] == results_14[1][2]:
        raise AssertionError("1->4 witnesses failed to separate X56")

    # Stronger RG witness.  The following two legal 2->3 moves produce
    # configurations with the same complete one-edge histogram, hence the
    # same value of sum_e V(n_e) for every potential V.  Their distributions
    # of the six-edge sum inside a tetrahedron are nevertheless different.
    correlation_moves = (
        ((3, 6, 15), 16, 5),
        ((3, 6, 16), 15, 7),
    )
    correlated_states = []
    for move in correlation_moves:
        if move not in legal_two_to_three_faces(state):
            raise AssertionError(f"declared correlation move is not legal: {move}")
        correlated_states.append(apply_two_to_three(state, *move))
    state_a, state_b = correlated_states

    invariant_a = (
        len(state_a),
        sum(edge_degree_histogram(state_a).values()),
        x56(state_a),
        edge_degree_histogram(state_a),
    )
    invariant_b = (
        len(state_b),
        sum(edge_degree_histogram(state_b).values()),
        x56(state_b),
        edge_degree_histogram(state_b),
    )
    if invariant_a != invariant_b:
        raise AssertionError((invariant_a, invariant_b))

    environment_a = tetrahedron_edge_sum_histogram(state_a)
    environment_b = tetrahedron_edge_sum_histogram(state_b)
    expected_a = Counter({31: 8, 32: 115, 33: 38, 34: 3})
    expected_b = Counter({31: 7, 32: 116, 33: 39, 34: 2})
    if environment_a != expected_a or environment_b != expected_b:
        raise AssertionError((environment_a, environment_b))

    tuple_a = tetrahedron_degree_tuple_histogram(state_a)
    tuple_b = tetrahedron_degree_tuple_histogram(state_b)
    tuple_positive = tuple_a - tuple_b
    tuple_negative = tuple_b - tuple_a
    expected_positive = Counter(
        {
            (4, 4, 5, 6, 6, 6): 1,
            (4, 4, 6, 6, 7, 7): 1,
        }
    )
    expected_negative = Counter(
        {
            (4, 4, 5, 6, 6, 7): 1,
            (4, 4, 6, 6, 6, 7): 1,
        }
    )
    if tuple_positive != expected_positive or tuple_negative != expected_negative:
        raise AssertionError((tuple_positive, tuple_negative))

    # For a general one-edge potential V, put
    # w_n = exp(-(V(n+1)-V(n))).  The difference of the refinement tangents
    # factors exactly as w4^2*w6^2*(w6-w7)*(w5-w7).
    weights = {4: 0.7, 5: 0.8, 6: 1.1, 7: 1.3}
    measured_general = sum(
        multiplicity
        * math.prod(weights[degree] for degree in degree_tuple)
        for degree_tuple, multiplicity in (tuple_a - tuple_b).items()
    ) - sum(
        multiplicity
        * math.prod(weights[degree] for degree in degree_tuple)
        for degree_tuple, multiplicity in (tuple_b - tuple_a).items()
    )
    predicted_general = (
        weights[4] ** 2
        * weights[6] ** 2
        * (weights[6] - weights[7])
        * (weights[5] - weights[7])
    )
    if not math.isclose(
        measured_general,
        predicted_general,
        rel_tol=1e-12,
        abs_tol=1e-15,
    ):
        raise AssertionError((measured_general, predicted_general))

    b_test = 0.1
    tangent_a = refinement_tangent(state_a, b_test)
    tangent_b = refinement_tangent(state_b, b_test)
    q = math.exp(-2.0 * b_test)
    predicted_difference = q**31 * (1.0 - q) * (1.0 - q**2)
    if not math.isclose(
        tangent_a - tangent_b,
        predicted_difference,
        rel_tol=1e-10,
        abs_tol=1e-15,
    ):
        raise AssertionError(
            (tangent_a - tangent_b, predicted_difference)
        )
    if tangent_a == tangent_b:
        raise AssertionError("RG tangent failed to separate correlation witnesses")

    edge_degree, _ = incidence_counts(state)
    print("M2-W RG-RAY / OP-INDEP CERTIFICATE")
    print(f"initial T3 tetrahedra          = {len(initial)}")
    print(f"state after first legal 2->3  = {len(state)} tetrahedra")
    print(f"state X56                     = {x56(state)}")
    print(f"state edge-degree histogram   = {dict(sorted(Counter(edge_degree.values()).items()))}")
    print("2->3: Delta N3=1 and Delta Delta=1-r_star for both witnesses")
    for move, face_sum, outer_sum, delta_x in results_23:
        print(
            f"  {move}: S_face={face_sum}, S_outer={outer_sum}, "
            f"Delta X56={delta_x}"
        )
    print("1->4: Delta N3=3 and Delta Delta=4-3*r_star for both witnesses")
    for tetrahedron, edge_sum, delta_x in results_14:
        print(
            f"  {tetrahedron}: sum_6_edge_degrees={edge_sum}, "
            f"Delta X56={delta_x}"
        )
    print("RG one-cell correlation witnesses:")
    print(
        f"  common (N3,N1,X56)         = "
        f"{invariant_a[0:3]}"
    )
    print(
        f"  common edge histogram      = "
        f"{dict(sorted(invariant_a[3].items()))}"
    )
    print(
        f"  tetra edge-sum histogram A = "
        f"{dict(sorted(environment_a.items()))}"
    )
    print(
        f"  tetra edge-sum histogram B = "
        f"{dict(sorted(environment_b.items()))}"
    )
    print(
        "  tuple difference A-B (+)  = "
        f"{dict(sorted(tuple_positive.items()))}"
    )
    print(
        "  tuple difference A-B (-)  = "
        f"{dict(sorted(tuple_negative.items()))}"
    )
    print(
        "  general-V factorization   = "
        "w4^2*w6^2*(w6-w7)*(w5-w7)"
    )
    print(
        f"  Y_0.1(A)-Y_0.1(B)          = "
        f"{tangent_a - tangent_b:.15e}"
    )
    print(
        f"  exact-form check           = "
        f"q^31(1-q)(1-q^2), q=e^-0.2"
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
