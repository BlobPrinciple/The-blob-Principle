#!/usr/bin/env python3
"""EXPLORATION (hors protocole) -- 26 novembre 2026, Claude. Les trois places admissibles hors de l'empilement connues (X-27), lues dans le dictionnaire d'Eisenstein.
Algebre exacte : si x = v/d est une boule ronde liee a p, alors q = v + (d-1)p est un vecteur entier rond, lie a p au meme point, et <x,q> = 1 (x contient q, tangente interieure).
Question : ce q est-il un constituant de l'empilement ?"""
import json
from x27bis_ford_eisenstein import prod, dans_l_empilement, pgcd, N
p = (1, 0, 0, 0, 0)
cas = {"x  (toit, 26 naissances)": ((8, 8, 7, -2, -2), 3), "x' (17 naissances)": ((18, 18, 16, -6, -3), 7), "x'' (23 naissances)": ((226, 220, 208, -92, -19), 91)}
for nom, (v, d) in cas.items():
    assert prod(v, v) == d * d and prod(v, p) == -d
    q = tuple(a + (d - 1) * b for a, b in zip(v, p))
    b = q[2] + q[3] + q[4]; g = pgcd((q[3] + q[4], q[4]), (b, 0))
    print(json.dumps({"place": nom, "numerateur": list(v), "denominateur": d, "q": list(q), "q_rond": prod(q, q) == 1, "q_lie_a_p": prod(q, p) == -1,
                      "x_contient_q_tangent": prod(v, q) == d, "courbure_de_q": b, "norme_du_denominateur_d_Eisenstein": b * b // N(g),
                      "q_sphere_de_Ford": N(g) == b, "q_dans_l_empilement": dans_l_empilement(q), "courbure_de_x": "%d/%d" % (b, d)}, ensure_ascii=False))

print("--- la meme lecture depuis chacun des quatre contacts de la place (q_c = v + (d-1)c)")
contacts = {"x  (toit, 26 naissances)": [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, -1, -1), (14, 12, 8, -4, -1)],
            "x' (17 naissances)": [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, -1, -1), (6, 6, 3, -2, 0)]}
for nom, cs in contacts.items():
    v, d = cas[nom]
    for c in cs:
        assert prod(v, c) == -d and dans_l_empilement(c)
        q = tuple(a + (d - 1) * b for a, b in zip(v, c))
        print(json.dumps({"place": nom, "contact": list(c), "q_c": list(q), "q_c_rond": prod(q, q) == 1, "q_c_dans_l_empilement": dans_l_empilement(q)}))
