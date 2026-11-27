/-
X-30 (seconde partie) : T16 (les trois quarts) et T17 (le cône), les deux inégalités de la démonstration de (G1).
Lean 4 seul, sans Mathlib. Écrit à la main. Claude, 27 novembre 2026.

Les énoncés valent dans tout anneau commutatif totalement ordonné K : les entiers, les rationnels, les réels, un corps
quadratique réel. Les boules à coordonnées irrationnelles sont donc couvertes. Aucune division n'est employée.

Produit dans la base d'une tuile : <u, v> = 2 Σ u_k v_k − (Σ u_k)(Σ v_k). nu(u, v) = (1 − <u, v>)/2. Liés : <u, v> = −1.

T16. Base de la tuile {p, c, f1, f2, f3}. x = (xp, xc ; x1, x2, x3), w = (wp, wc ; w1, w2, w3).
  x liée à p              : 2 xp − s = −1          (s = xp + xc + x1 + x2 + x3)
  x liée à c              : 2 xc − s = −1
  x ne chevauche pas f_k  : 2 x_k − s ≤ −1
  x ronde                 : 2 (xp² + xc² + x1² + x2² + x3²) − s² = 1
  w liée à p              : 2 wp − t = −1          (t = wp + wc + w1 + w2 + w3)
  w ronde                 : 2 (wp² + wc² + w1² + w2² + w3²) − t² = 1
  w dans le secteur       : w1, w2, w3 ≥ 0 ; w1 + w2 + w3 > 0 (cette somme vaut nu(c, w) : w n'est pas dans le faisceau de p et c)
  Conclusion : nu(x, w) ≥ (3/4) nu(c, w), c'est-à-dire 4 <x, w> ≤ 1 + 3 <c, w>, avec <c, w> = 2 wc − t.

T17. Base d'une tuile contenant p. Une boule liée à p est donnée par ses quatre coordonnées hors p ; sa coordonnée sur p
  vaut leur somme moins 1, et nu(A, B) = (Σ A_k)(Σ B_k) − Σ A_k B_k (définition nu4). Ronde : nu(A, A) = 0. La somme des quatre
  coordonnées d'une boule liée à p est strictement positive (hypothèses sx et sw).
  x liée à q, r (et s) ; nu(x, w) > (3/4) nu(c, w) pour c = q, r (et s).
  Conclusions : 3 nu(q, r) < 16 (cone_paire) ; nu(q, r) + nu(q, s) + nu(r, s) < 12 (cone_triplet).
-/
open Lean.Grind Std

namespace X30bis

variable {K : Type} [CommRing K] [LE K] [LT K] [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K]

theorem carre_positif (a : K) : 0 ≤ a * a := by
  have := OrderedRing.sq_nonneg (a := a)
  grind

theorem positif_de_produit (a t : K) (ha : 0 < a) (h : 0 ≤ a * t) : 0 ≤ t := by
  apply Classical.byContradiction
  intro hn
  have ht : t < 0 := by grind
  have := OrderedRing.mul_lt_mul_of_pos_left ht ha
  grind

theorem carre_croissant (u v : K) (hv : 0 ≤ v) (h : v < u) : v * v < u * u := by
  have hu : 0 < u := by grind
  have h1 := OrderedRing.mul_le_mul_of_nonneg_left (Preorder.le_of_lt h) hv
  have h2 := OrderedRing.mul_lt_mul_of_pos_right h hu
  grind

/-! ## T16 -/

/-- L'inégalité réduite, quand w3 est le plus petit des trois. c_k = nu(x, f_k) − 1. -/
theorem reduit_min3 (c1 c2 c3 w1 w2 w3 : K) (h1 : 0 ≤ c1) (h2 : 0 ≤ c2) (hS : 2 ≤ c1 + c2 + c3)
    (g3 : 0 ≤ w3) (m1 : w3 ≤ w1) (m2 : w3 ≤ w2) :
    0 ≤ 4 * (w1+w2+w3) * (c1*w1 + c2*w2 + c3*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3) := by
  have hP : 0 ≤ w1+w2+w3 := by grind
  have d1 : 0 ≤ w1 - w3 := by grind
  have d2 : 0 ≤ w2 - w3 := by grind
  have d3 : 0 ≤ c1 + c2 + c3 - 2 := by grind
  have d4 : 0 ≤ w1 + w2 := by grind
  have a1 : 0 ≤ (w1+w2+w3) * (c1 * (w1-w3)) := OrderedRing.mul_nonneg hP (OrderedRing.mul_nonneg h1 d1)
  have a2 : 0 ≤ (w1+w2+w3) * (c2 * (w2-w3)) := OrderedRing.mul_nonneg hP (OrderedRing.mul_nonneg h2 d2)
  have a3 : 0 ≤ ((w1+w2+w3) * w3) * (c1+c2+c3 - 2) := OrderedRing.mul_nonneg (OrderedRing.mul_nonneg hP g3) d3
  have a4 : 0 ≤ (w1-w2) * (w1-w2) := carre_positif _
  have a5 : 0 ≤ w3 * w3 := carre_positif _
  have a6 : 0 ≤ w3 * (w1+w2) := OrderedRing.mul_nonneg g3 d4
  have e : 4 * (w1+w2+w3) * (c1*w1 + c2*w2 + c3*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3)
      = 4 * ((w1+w2+w3) * (c1 * (w1-w3))) + 4 * ((w1+w2+w3) * (c2 * (w2-w3))) + 4 * (((w1+w2+w3) * w3) * (c1+c2+c3 - 2))
        + (w1-w2) * (w1-w2) + 9 * (w3*w3) + 6 * (w3 * (w1+w2)) := by grind
  grind

theorem reduit (c1 c2 c3 w1 w2 w3 : K) (h1 : 0 ≤ c1) (h2 : 0 ≤ c2) (h3 : 0 ≤ c3) (hS : 2 ≤ c1 + c2 + c3)
    (g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : 0 ≤ w3) :
    0 ≤ 4 * (w1+w2+w3) * (c1*w1 + c2*w2 + c3*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3) := by
  by_cases m12 : w1 ≤ w2
  · by_cases m13 : w1 ≤ w3
    · have := reduit_min3 c2 c3 c1 w2 w3 w1 h2 h3 (by grind) g1 m12 m13
      grind
    · have := reduit_min3 c1 c2 c3 w1 w2 w3 h1 h2 hS g3 (by grind) (by grind)
      grind
  · by_cases m23 : w2 ≤ w3
    · have := reduit_min3 c3 c1 c2 w3 w1 w2 h3 h1 (by grind) g2 m23 (by grind)
      grind
    · have := reduit_min3 c1 c2 c3 w1 w2 w3 h1 h2 hS g3 (by grind) (by grind)
      grind

/-- T16, les trois quarts. -/
theorem trois_quarts (xp xc x1 x2 x3 wp wc w1 w2 w3 : K)
    (hxp : 2 * xp - (xp+xc+x1+x2+x3) = -1)
    (hxc : 2 * xc - (xp+xc+x1+x2+x3) = -1)
    (n1 : 2 * x1 - (xp+xc+x1+x2+x3) ≤ -1) (n2 : 2 * x2 - (xp+xc+x1+x2+x3) ≤ -1) (n3 : 2 * x3 - (xp+xc+x1+x2+x3) ≤ -1)
    (hx : 2 * (xp*xp + xc*xc + x1*x1 + x2*x2 + x3*x3) - (xp+xc+x1+x2+x3) * (xp+xc+x1+x2+x3) = 1)
    (hwp : 2 * wp - (wp+wc+w1+w2+w3) = -1)
    (hw : 2 * (wp*wp + wc*wc + w1*w1 + w2*w2 + w3*w3) - (wp+wc+w1+w2+w3) * (wp+wc+w1+w2+w3) = 1)
    (g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : 0 ≤ w3) (gp : 0 < w1+w2+w3) :
    4 * (2 * (xp*wp + xc*wc + x1*w1 + x2*w2 + x3*w3) - (xp+xc+x1+x2+x3) * (wp+wc+w1+w2+w3))
      ≤ 1 + 3 * (2 * wc - (wp+wc+w1+w2+w3)) := by
  have e1 : xc = xp := by grind
  have e2 : x1 + x2 + x3 = 1 := by grind
  have e3 : 2 * (x1*x1 + x2*x2 + x3*x3) = 4 * xp + 2 := by grind
  have c1 : 0 ≤ xp - x1 := by grind
  have c2 : 0 ≤ xp - x2 := by grind
  have c3 : 0 ≤ xp - x3 := by grind
  have p12 := OrderedRing.mul_nonneg c1 c2
  have p13 := OrderedRing.mul_nonneg c1 c3
  have p23 := OrderedRing.mul_nonneg c2 c3
  have id : 4 * ((xp-x1)*(xp-x2) + (xp-x1)*(xp-x3) + (xp-x2)*(xp-x3)) = 12 * (xp * (xp-1)) := by grind
  have pos : 0 ≤ xp * (xp - 1) := by grind
  have bpos : 0 < xp := by grind
  -- la fenêtre (T13) : la coordonnée de x sur c vaut au moins 1
  have b1 : 1 ≤ xp := by
    apply Classical.byContradiction
    intro hn
    have ht : xp - 1 < 0 := by grind
    have := OrderedRing.mul_lt_mul_of_pos_left ht bpos
    grind
  have hS : 2 ≤ (xp-x1) + (xp-x2) + (xp-x3) := by grind
  have red := reduit (xp-x1) (xp-x2) (xp-x3) w1 w2 w3 c1 c2 c3 hS g1 g2 g3
  have f1 : wp = wc + (w1+w2+w3) - 1 := by grind
  have f2 : 4 * ((w1+w2+w3) * wc) = 2 * (w1*w1 + w2*w2 + w3*w3) - 2 * ((w1+w2+w3) * (w1+w2+w3)) := by grind
  have cle : (w1+w2+w3) * (1 + 3 * (2 * wc - (wp+wc+w1+w2+w3))
        - 4 * (2 * (xp*wp + xc*wc + x1*w1 + x2*w2 + x3*w3) - (xp+xc+x1+x2+x3) * (wp+wc+w1+w2+w3)))
      = 2 * (4 * (w1+w2+w3) * ((xp-x1)*w1 + (xp-x2)*w2 + (xp-x3)*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3)) := by
    grind
  have fin := positif_de_produit (w1+w2+w3) _ gp (by rw [cle]; grind)
  grind

/-! ## T17 -/

/-- Cauchy-Schwarz en dimension 4, sous forme polynomiale. -/
theorem cauchy4 (a1 a2 a3 a4 b1 b2 b3 b4 : K) :
    (a1*b1 + a2*b2 + a3*b3 + a4*b4) * (a1*b1 + a2*b2 + a3*b3 + a4*b4)
      ≤ (a1*a1 + a2*a2 + a3*a3 + a4*a4) * (b1*b1 + b2*b2 + b3*b3 + b4*b4) := by
  have s12 := carre_positif (a1*b2 - a2*b1)
  have s13 := carre_positif (a1*b3 - a3*b1)
  have s14 := carre_positif (a1*b4 - a4*b1)
  have s23 := carre_positif (a2*b3 - a3*b2)
  have s24 := carre_positif (a2*b4 - a4*b2)
  have s34 := carre_positif (a3*b4 - a4*b3)
  have e : (a1*a1 + a2*a2 + a3*a3 + a4*a4) * (b1*b1 + b2*b2 + b3*b3 + b4*b4)
      - (a1*b1 + a2*b2 + a3*b3 + a4*b4) * (a1*b1 + a2*b2 + a3*b3 + a4*b4)
      = (a1*b2 - a2*b1) * (a1*b2 - a2*b1) + (a1*b3 - a3*b1) * (a1*b3 - a3*b1) + (a1*b4 - a4*b1) * (a1*b4 - a4*b1)
        + (a2*b3 - a3*b2) * (a2*b3 - a3*b2) + (a2*b4 - a4*b2) * (a2*b4 - a4*b2) + (a3*b4 - a4*b3) * (a3*b4 - a4*b3) := by grind
  grind

theorem cone_scalaire (SV SX SW PVX PWV NV NX NW : K)
    (hNX : NX = SX * SX) (hNW : NW = SW * SW) (sX : 0 < SX) (sW : 0 < SW)
    (hV : NV ≤ SV * SV)
    (cs1 : PVX * PVX ≤ NV * NX) (cs2 : PWV * PWV ≤ NW * NV)
    (hVX : PVX < SV * SX) : PWV ≤ SW * SV := by
  subst hNX hNW
  have qX : 0 ≤ SX * SX := carre_positif SX
  have qW : 0 ≤ SW * SW := carre_positif SW
  have b1 : NV * (SX * SX) ≤ (SV * SV) * (SX * SX) := OrderedRing.mul_le_mul_of_nonneg_right hV qX
  have b2 : (SW * SW) * NV ≤ (SW * SW) * (SV * SV) := OrderedRing.mul_le_mul_of_nonneg_left hV qW
  have posV : 0 < SV := by
    apply Classical.byContradiction
    intro hn
    have h0 : SV ≤ 0 := by grind
    have h1 : SV * SX ≤ 0 := by
      have := OrderedRing.mul_le_mul_of_nonneg_right h0 (Preorder.le_of_lt sX)
      grind
    have h2 := carre_croissant (-PVX) (-(SV * SX)) (by grind) (by grind)
    have r1 : (-(SV * SX)) * (-(SV * SX)) = (SV * SV) * (SX * SX) := by grind
    have r2 : (-PVX) * (-PVX) = PVX * PVX := by grind
    rw [r1, r2] at h2
    grind
  apply Classical.byContradiction
  intro hn
  have h3 : SW * SV < PWV := by grind
  have h4 : 0 < SW * SV := OrderedRing.mul_pos sW posV
  have h5 := carre_croissant PWV (SW * SV) (Preorder.le_of_lt h4) h3
  have r3 : (SW * SV) * (SW * SV) = (SW * SW) * (SV * SV) := by grind
  rw [r3] at h5
  grind

/-- Le cône. V de genre temps ou lumière ; X et W de genre lumière, de somme positive ; nu(V, X) > 0. Alors nu(W, V) ≥ 0. -/
theorem cone (v1 v2 v3 v4 x1 x2 x3 x4 w1 w2 w3 w4 : K)
    (hX : x1*x1 + x2*x2 + x3*x3 + x4*x4 = (x1+x2+x3+x4) * (x1+x2+x3+x4)) (sX : 0 < x1+x2+x3+x4)
    (hW : w1*w1 + w2*w2 + w3*w3 + w4*w4 = (w1+w2+w3+w4) * (w1+w2+w3+w4)) (sW : 0 < w1+w2+w3+w4)
    (hV : v1*v1 + v2*v2 + v3*v3 + v4*v4 ≤ (v1+v2+v3+v4) * (v1+v2+v3+v4))
    (hVX : v1*x1 + v2*x2 + v3*x3 + v4*x4 < (v1+v2+v3+v4) * (x1+x2+x3+x4)) :
    w1*v1 + w2*v2 + w3*v3 + w4*v4 ≤ (w1+w2+w3+w4) * (v1+v2+v3+v4) :=
  cone_scalaire (v1+v2+v3+v4) (x1+x2+x3+x4) (w1+w2+w3+w4) (v1*x1 + v2*x2 + v3*x3 + v4*x4) (w1*v1 + w2*v2 + w3*v3 + w4*v4)
    (v1*v1 + v2*v2 + v3*v3 + v4*v4) (x1*x1 + x2*x2 + x3*x3 + x4*x4) (w1*w1 + w2*w2 + w3*w3 + w4*w4)
    hX hW sX sW hV (cauchy4 v1 v2 v3 v4 x1 x2 x3 x4) (cauchy4 w1 w2 w3 w4 v1 v2 v3 v4) hVX

/-- nu(A, B) pour deux boules liées à p, données par leurs quatre coordonnées hors p dans la base d'une tuile contenant p. -/
def nu4 (a1 a2 a3 a4 b1 b2 b3 b4 : K) : K := (a1+a2+a3+a4) * (b1+b2+b3+b4) - (a1*b1 + a2*b2 + a3*b3 + a4*b4)

/-- T17, pour une paire de contacts. -/
theorem cone_paire (x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 w1 w2 w3 w4 : K)
    (hx : nu4 x1 x2 x3 x4 x1 x2 x3 x4 = 0) (hq : nu4 q1 q2 q3 q4 q1 q2 q3 q4 = 0) (hr : nu4 r1 r2 r3 r4 r1 r2 r3 r4 = 0)
    (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 0)
    (sx : 0 < x1+x2+x3+x4) (sw : 0 < w1+w2+w3+w4)
    (tq : nu4 x1 x2 x3 x4 q1 q2 q3 q4 = 1) (tr : nu4 x1 x2 x3 x4 r1 r2 r3 r4 = 1)
    (iq : 3 * nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (ir : 3 * nu4 r1 r2 r3 r4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4) :
    3 * nu4 q1 q2 q3 q4 r1 r2 r3 r4 < 16 := by
  unfold nu4 at *
  apply Classical.byContradiction
  intro hn
  have c := cone (3*(q1+r1) - 8*x1) (3*(q2+r2) - 8*x2) (3*(q3+r3) - 8*x3) (3*(q4+r4) - 8*x4) x1 x2 x3 x4 w1 w2 w3 w4
    (by grind) sx (by grind) sw (by grind) (by grind)
  grind

/-- T17, pour les trois contacts. -/
theorem cone_triplet (x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 s1 s2 s3 s4 w1 w2 w3 w4 : K)
    (hx : nu4 x1 x2 x3 x4 x1 x2 x3 x4 = 0) (hq : nu4 q1 q2 q3 q4 q1 q2 q3 q4 = 0) (hr : nu4 r1 r2 r3 r4 r1 r2 r3 r4 = 0)
    (hs : nu4 s1 s2 s3 s4 s1 s2 s3 s4 = 0) (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 0)
    (sx : 0 < x1+x2+x3+x4) (sw : 0 < w1+w2+w3+w4)
    (tq : nu4 x1 x2 x3 x4 q1 q2 q3 q4 = 1) (tr : nu4 x1 x2 x3 x4 r1 r2 r3 r4 = 1) (ts : nu4 x1 x2 x3 x4 s1 s2 s3 s4 = 1)
    (iq : 3 * nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (ir : 3 * nu4 r1 r2 r3 r4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (is : 3 * nu4 s1 s2 s3 s4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4) :
    nu4 q1 q2 q3 q4 r1 r2 r3 r4 + nu4 q1 q2 q3 q4 s1 s2 s3 s4 + nu4 r1 r2 r3 r4 s1 s2 s3 s4 < 12 := by
  unfold nu4 at *
  apply Classical.byContradiction
  intro hn
  have c := cone (3*(q1+r1+s1) - 12*x1) (3*(q2+r2+s2) - 12*x2) (3*(q3+r3+s3) - 12*x3) (3*(q4+r4+s4) - 12*x4)
    x1 x2 x3 x4 w1 w2 w3 w4 (by grind) sx (by grind) sw (by grind) (by grind)
  grind

end X30bis

#print axioms X30bis.trois_quarts
#print axioms X30bis.cone_paire
#print axioms X30bis.cone_triplet
