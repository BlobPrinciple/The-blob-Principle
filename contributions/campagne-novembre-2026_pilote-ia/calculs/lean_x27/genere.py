#!/usr/bin/env python3
"""X-27 passe au noyau de Lean -- generateur de la preuve.
Ecrit Preuve.lean : pour chacune des 17 naissances et pour la place hors de l'empilement, les temoins (parent, trois voisins du parent, mot de retournements)
que le noyau de Lean controle ensuite. L'enonce (Enonce.lean) est ecrit a la main et ne depend pas de ce programme.
Ce programme ne prouve rien : il cherche des temoins. Si un temoin est faux, Lean refuse la preuve.
Independant des programmes de X-27 (rien n'est importe). Usage : python3 genere.py > Preuve.lean      Claude, 26 novembre 2026."""
import itertools

G = [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
B = [(1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3),
     (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2), (4, 4, 1, -2, 2), (4, 4, 2, -2, 1), (8, 8, 2, -3, 2), (9, 9, 3, -3, 1),
     (6, 6, 3, -2, 0)]
X, D = (18, 18, 16, -6, -3), 7


def prod(a, b):
    return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)


def retourne(j, y):
    t = y[j]
    return tuple(-t if k == j else y[k] + t for k in range(5))


def mot(x):
    """Descente : x = retourne w1 (retourne w2 (... (e_k)))."""
    y, w = tuple(x), []
    while min(y) < 0:
        j = min(range(5), key=lambda k: y[k]); y = retourne(j, y); w.append(j)
        assert sum(y) > 0 and len(w) < 10000
    assert sorted(y) == [0, 0, 0, 0, 1], x
    return w, y.index(1)


def rang(vs):
    """Rang d'une famille de vecteurs entiers (elimination en fractions)."""
    from fractions import Fraction as F
    m = [[F(v) for v in u] for u in vs]; r = 0
    for c in range(5):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None: continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def temoins_cellule(S, b):
    """Parent et trois voisins, les quatre tous lies entre eux (une cellule), tous touches par b."""
    touche = [u for u in S if prod(b, u) == -1]
    for q in itertools.combinations(touche, 4):
        if all(prod(u, w) == -1 for u, w in itertools.combinations(q, 2)) and rang(q) == 4: return q
    raise SystemExit('pas de cellule pour %r' % (b,))


def lv(u): return '(%s)' % ', '.join(str(v) for v in u)
def ll(S): return '[' + ', '.join(lv(u) for u in S) + ']'


out = []
w = out.append
w('''import Enonce
/-! # X-27 — K20 est fausse : la preuve, contrôlée par le noyau de Lean.
Fichier écrit par `genere.py` (26 novembre 2026). Il ne contient que des témoins : le parent et les trois voisins de chaque naissance,
le mot de retournements qui mène du germe à chaque constituant. Lean 4 seul, sans Mathlib, sans `sorry`, sans `native_decide`. -/
namespace X27

/-- Un constituant atteint depuis le germe par un mot de retournements est dans l'empilement. -/
theorem dans_mot (k : Vec) (hk : k ∈ germe) : ∀ m : List (Fin 5), DansEmpilement (applique m k)
  | [] => DansEmpilement.germe hk
  | j :: m => DansEmpilement.retourne j (dans_mot k hk m)
''')

# 1. Les 22 constituants sont dans l'empilement.
tous = G + B
for i, u in enumerate(tous):
    m, k = mot(u)
    w('theorem dans_%d : DansEmpilement %s := by' % (i, lv(u)))
    w('  have h := dans_mot %s (by decide) [%s]' % (lv(G[k]), ', '.join(str(j) for j in m)))
    w('  have e : applique [%s] %s = %s := by decide' % (', '.join(str(j) for j in m), lv(G[k]), lv(u)))
    w('  rw [e] at h; exact h\n')

# 2. Independance des quadruples (un lemme par quadruple, prouve par l'arithmetique lineaire entiere).
def lemme_indep(nom, q):
    w('theorem %s : independants %s %s %s %s := by' % ((nom,) + tuple(lv(u) for u in q)))
    w('  intro α β γ δ h')
    w('  simp only [comb, Prod.mk.injEq] at h')
    w('  omega\n')

# 3. Chaque naissance est une naissance dans la cellule du tissu deja la.
S = list(G)
for i, b in enumerate(B, 1):
    q = temoins_cellule(S, b)
    lemme_indep('indep_%d' % i, q)
    w('theorem naissance_%d : NaissanceDansCellule %s ⟨%s, 1⟩ :=' % (i, ll(S), lv(b)))
    w('  ⟨by decide, by decide, by decide, %s, %s, %s, %s,' % tuple(lv(u) for u in q))
    w('   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,')
    w('   by decide, by decide, by decide, by decide, indep_%d⟩\n' % i)
    S.append(b)

# 4. Le tissu.
w('theorem tissu_de_cellules : TissuDeCellules germe naissances17 :=')
w('  ⟨' + ', '.join('naissance_%d' % i for i in range(1, 18)) + ', trivial⟩\n')
w('theorem tissu : Tissu germe naissances17 :=')
w('  ⟨' + ', '.join('cellule_admissible naissance_%d' % i for i in range(1, 18)) + ', trivial⟩\n')

# 5. Tout le tissu est dans l'empilement.
w('theorem tissu_dans_empilement : ∀ u ∈ tissu22, DansEmpilement u := by')
w('  intro u hu')
w('  simp only [tissu22, germe, naissances17, List.cons_append, List.nil_append, List.mem_cons, List.not_mem_nil, or_false] at hu')
w('  rcases hu with ' + ' | '.join('rfl' for _ in tous))
for i in range(len(tous)):
    w('  · exact dans_%d' % i)
w('')

# 6. La place.
touche = [u for u in S if prod(X, u) == -D]
assert prod(X, X) == D * D and all(prod(X, u) <= -D for u in S) and len(touche) == 4
p = G[0]; vois = [u for u in touche if u != p]
assert p in touche and all(prod(p, u) == -1 for u in vois) and rang([p] + vois) == 4
lemme_indep('indep_place', [p] + vois)
w('theorem place_admissible : PlaceAdmissible tissu22 place :=')
w('  ⟨by decide, by decide, by decide, %s, %s, %s, %s,' % tuple(lv(u) for u in [p] + vois))
w('   by decide, by decide, by decide, by decide, by decide, by decide, by decide,')
w('   by decide, by decide, by decide, by decide, indep_place⟩\n')
w('''theorem place_hors_empilement : ¬ BouleDansEmpilement place := by
  rintro ⟨⟨a, b, c, d, e⟩, _, h⟩
  simp only [place, fois, Prod.mk.injEq] at h
  omega

/-- **K20 est fausse.** L'énoncé est dans `Enonce.lean`. -/
theorem K20_est_fausse : EnonceK20Fausse :=
  ⟨tissu, tissu_de_cellules, tissu_dans_empilement, place_admissible, place_hors_empilement⟩

end X27

#print axioms X27.K20_est_fausse
''')
print('\n'.join(out))
