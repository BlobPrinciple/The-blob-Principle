/-
X-30, lemme de la fenêtre (T13), pour une boule à coordonnées rationnelles. Lean 4 seul, sans Mathlib. Écrit à la main.

Dans la base d'une tuile {f1, f2, f3, f4, u}, la boule x a pour coordonnées (a1, a2, a3, a4 ; b)/D, avec D > 0.
  x liée à u                     :  b = (a1 + a2 + a3 + a4) - D
  x ne chevauche pas f_j         :  a_j ≤ (a1 + a2 + a3 + a4) - D          (c'est 2 a_j - A - b ≤ -D, avec b = A - D)
  x ronde                        :  a1² + a2² + a3² + a4² = (a1 + a2 + a3 + a4)²   (c'est 2 Σ a_j² + b² - 2 A b - A² = D², avec b = A - D)
Conclusion : A ≥ 2 D, c'est-à-dire b ≥ D, c'est-à-dire <x, n> = 6 b / D ≥ 6 : x est au-delà du mur opposé à u.
-/
namespace X30

theorem ident (a1 a2 a3 a4 D : Int) :
    2 * ((a1+a2+a3+a4-D-a1) * (a1+a2+a3+a4-D-a2) + (a1+a2+a3+a4-D-a1) * (a1+a2+a3+a4-D-a3) + (a1+a2+a3+a4-D-a1) * (a1+a2+a3+a4-D-a4)
       + (a1+a2+a3+a4-D-a2) * (a1+a2+a3+a4-D-a3) + (a1+a2+a3+a4-D-a2) * (a1+a2+a3+a4-D-a4) + (a1+a2+a3+a4-D-a3) * (a1+a2+a3+a4-D-a4))
      + (a1*a1 + a2*a2 + a3*a3 + a4*a4 - (a1+a2+a3+a4) * (a1+a2+a3+a4))
    = 6 * ((a1+a2+a3+a4-D) * (a1+a2+a3+a4-2*D)) := by
  grind

theorem fenetre (a1 a2 a3 a4 D : Int) (hD : 0 < D)
    (h1 : a1 ≤ a1+a2+a3+a4-D) (h2 : a2 ≤ a1+a2+a3+a4-D) (h3 : a3 ≤ a1+a2+a3+a4-D) (h4 : a4 ≤ a1+a2+a3+a4-D)
    (hn : a1*a1 + a2*a2 + a3*a3 + a4*a4 = (a1+a2+a3+a4) * (a1+a2+a3+a4)) :
    2 * D ≤ a1+a2+a3+a4 := by
  have c1 : 0 ≤ a1+a2+a3+a4-D-a1 := by omega
  have c2 : 0 ≤ a1+a2+a3+a4-D-a2 := by omega
  have c3 : 0 ≤ a1+a2+a3+a4-D-a3 := by omega
  have c4 : 0 ≤ a1+a2+a3+a4-D-a4 := by omega
  have p12 := Int.mul_nonneg c1 c2
  have p13 := Int.mul_nonneg c1 c3
  have p14 := Int.mul_nonneg c1 c4
  have p23 := Int.mul_nonneg c2 c3
  have p24 := Int.mul_nonneg c2 c4
  have p34 := Int.mul_nonneg c3 c4
  have e := ident a1 a2 a3 a4 D
  have pos : 0 ≤ (a1+a2+a3+a4-D) * (a1+a2+a3+a4-2*D) := by omega
  have hAD : 0 < a1+a2+a3+a4-D := by omega
  apply Classical.byContradiction
  intro hc
  have hneg : a1+a2+a3+a4-2*D ≤ -1 := by omega
  have m := Int.mul_le_mul_of_nonneg_left hneg (Int.le_of_lt hAD)
  omega

end X30

#print axioms X30.fenetre
