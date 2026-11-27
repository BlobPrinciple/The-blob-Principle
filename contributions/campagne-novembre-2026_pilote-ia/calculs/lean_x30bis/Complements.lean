/-
X-30 (seconde partie), compléments non scellés : ce que TroisQuartsEtCone.lean laissait hors de Lean pour T16 et T17,
et la partie arithmétique de T18. Lean 4 seul, sans Mathlib. Écrit à la main. Claude, 27 novembre 2026.

1. T16, cas d'égalité (trois_quarts_egalite). Sous les hypothèses de trois_quarts, si nu(x, w) = (3/4) nu(c, w), alors
   x = p + c + f_i + f_j − f_k : x est le retourné d'un des trois f. Donc l'inégalité est stricte pour une boule hors de l'empilement.
2. T17 sans hypothèse de signe (somme_positive, cone_paire_complet, cone_triplet_complet). Si q est de genre lumière et de somme
   positive (dans la base d'une tuile contenant p et q, q = (1, 0, 0, 0)), toute boule ronde B liée à p avec nu(q, B) > 0 est de
   somme positive. Les hypothèses sx et sw de cone_paire et cone_triplet en découlent : pour x, nu(q, x) = 1 ; pour w, nu(q, w) > 0.
3. T18, arithmétique. Un entier d'Eisenstein z = z0 + z1 ω (ω² + ω + 1 = 0) a pour norme z0² − z0 z1 + z1². Sous le fait admis (C6),
   c étant à l'infini, deux voisins de p sont en α/β et γ/δ, avec nu(c, ·) = norme(β), norme(δ) et nu entre eux = norme(αδ − βγ).
   norme_mod3 : une norme n'est jamais congrue à 2 modulo 3 ; donc jamais 2 ni 5.
   det_div3   : si 3 divise norme(β) et norme(δ), 3 divise norme(αδ − βγ). Exclut les types (1, 3, 3) et (3, 3, 4).
   det_div4   : si 2 divise norme(β) et norme(δ), 4 divise norme(αδ − βγ). Exclut les types (1, 4, 4) et (3, 4, 4).
   Ce qui reste hors de Lean dans T18 : que les boules tangentes des types (3, 3, 3) et (1, 3, 4) sont posées en des points du réseau.
-/
import TroisQuartsEtCone
open Lean.Grind Std

namespace X30bis

variable {K : Type} [CommRing K] [LE K] [LT K] [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K]

theorem carre_nul (a : K) (h : a * a = 0) : a = 0 := by
  apply Classical.byContradiction
  intro hn
  by_cases hp : 0 < a
  · have := OrderedRing.mul_pos hp hp
    grind
  · have hneg : a < 0 := by grind
    have := OrderedRing.mul_pos_of_neg_of_neg hneg hneg
    grind

theorem facteur_nul (a t : K) (ha : 0 < a) (h : a * t = 0) : t = 0 := by
  apply Classical.byContradiction
  intro hn
  by_cases hp : 0 < t
  · have := OrderedRing.mul_pos ha hp
    grind
  · have hneg : t < 0 := by grind
    have := OrderedRing.mul_neg_of_pos_of_neg ha hneg
    grind

/-! ## T16, cas d'égalité -/

theorem reduit_min3_egalite (c1 c2 c3 w1 w2 w3 : K) (h1 : 0 ≤ c1) (h2 : 0 ≤ c2) (hS : 2 ≤ c1 + c2 + c3)
    (g3 : 0 ≤ w3) (m1 : w3 ≤ w1) (m2 : w3 ≤ w2) (gp : 0 < w1+w2+w3)
    (he : 4 * (w1+w2+w3) * (c1*w1 + c2*w2 + c3*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3) = 0) :
    c1 = 0 ∧ c2 = 0 ∧ w3 = 0 ∧ w1 = w2 := by
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
  have z1 : (w1+w2+w3) * (c1 * (w1-w3)) = 0 := by grind
  have z2 : (w1+w2+w3) * (c2 * (w2-w3)) = 0 := by grind
  have z4 : (w1-w2) * (w1-w2) = 0 := by grind
  have z5 : w3 * w3 = 0 := by grind
  have w30 : w3 = 0 := carre_nul _ z5
  have w12 : w1 - w2 = 0 := carre_nul _ z4
  have w1p : 0 < w1 := by grind
  have w2p : 0 < w2 := by grind
  have y1 : c1 * (w1-w3) = 0 := facteur_nul _ _ gp z1
  have y2 : c2 * (w2-w3) = 0 := facteur_nul _ _ gp z2
  have y1' : (w1-w3) * c1 = 0 := by grind
  have y2' : (w2-w3) * c2 = 0 := by grind
  have c10 : c1 = 0 := facteur_nul (w1-w3) c1 (by grind) y1'
  have c20 : c2 = 0 := facteur_nul (w2-w3) c2 (by grind) y2'
  exact ⟨c10, c20, w30, by grind⟩

/-- Cas d'égalité de l'inégalité réduite : deux des c sont nuls. -/
theorem reduit_egalite (c1 c2 c3 w1 w2 w3 : K) (h1 : 0 ≤ c1) (h2 : 0 ≤ c2) (h3 : 0 ≤ c3) (hS : 2 ≤ c1 + c2 + c3)
    (g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : 0 ≤ w3) (gp : 0 < w1+w2+w3)
    (he : 4 * (w1+w2+w3) * (c1*w1 + c2*w2 + c3*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3) = 0) :
    (c1 = 0 ∧ c2 = 0) ∨ (c1 = 0 ∧ c3 = 0) ∨ (c2 = 0 ∧ c3 = 0) := by
  by_cases m12 : w1 ≤ w2
  · by_cases m13 : w1 ≤ w3
    · have := reduit_min3_egalite c2 c3 c1 w2 w3 w1 h2 h3 (by grind) g1 m12 m13 (by grind) (by grind)
      grind
    · have := reduit_min3_egalite c1 c2 c3 w1 w2 w3 h1 h2 hS g3 (by grind) (by grind) gp he
      grind
  · by_cases m23 : w2 ≤ w3
    · have := reduit_min3_egalite c3 c1 c2 w3 w1 w2 h3 h1 (by grind) g2 m23 (by grind) (by grind) (by grind)
      grind
    · have := reduit_min3_egalite c1 c2 c3 w1 w2 w3 h1 h2 hS g3 (by grind) (by grind) gp he
      grind

/-- T16, cas d'égalité : x est le retourné d'un des trois f. -/
theorem trois_quarts_egalite (xp xc x1 x2 x3 wp wc w1 w2 w3 : K)
    (hxp : 2 * xp - (xp+xc+x1+x2+x3) = -1)
    (hxc : 2 * xc - (xp+xc+x1+x2+x3) = -1)
    (n1 : 2 * x1 - (xp+xc+x1+x2+x3) ≤ -1) (n2 : 2 * x2 - (xp+xc+x1+x2+x3) ≤ -1) (n3 : 2 * x3 - (xp+xc+x1+x2+x3) ≤ -1)
    (hx : 2 * (xp*xp + xc*xc + x1*x1 + x2*x2 + x3*x3) - (xp+xc+x1+x2+x3) * (xp+xc+x1+x2+x3) = 1)
    (hwp : 2 * wp - (wp+wc+w1+w2+w3) = -1)
    (hw : 2 * (wp*wp + wc*wc + w1*w1 + w2*w2 + w3*w3) - (wp+wc+w1+w2+w3) * (wp+wc+w1+w2+w3) = 1)
    (g1 : 0 ≤ w1) (g2 : 0 ≤ w2) (g3 : 0 ≤ w3) (gp : 0 < w1+w2+w3)
    (he : 4 * (2 * (xp*wp + xc*wc + x1*w1 + x2*w2 + x3*w3) - (xp+xc+x1+x2+x3) * (wp+wc+w1+w2+w3))
      = 1 + 3 * (2 * wc - (wp+wc+w1+w2+w3))) :
    xp = 1 ∧ xc = 1 ∧ ((x1 = 1 ∧ x2 = 1 ∧ x3 = -1) ∨ (x1 = 1 ∧ x2 = -1 ∧ x3 = 1) ∨ (x1 = -1 ∧ x2 = 1 ∧ x3 = 1)) := by
  have e1 : xc = xp := by grind
  have e2 : x1 + x2 + x3 = 1 := by grind
  have e3 : 2 * (x1*x1 + x2*x2 + x3*x3) = 4 * xp + 2 := by clear he hw hwp; grind
  have c1 : 0 ≤ xp - x1 := by grind
  have c2 : 0 ≤ xp - x2 := by grind
  have c3 : 0 ≤ xp - x3 := by grind
  have p12 := OrderedRing.mul_nonneg c1 c2
  have p13 := OrderedRing.mul_nonneg c1 c3
  have p23 := OrderedRing.mul_nonneg c2 c3
  have id : 4 * ((xp-x1)*(xp-x2) + (xp-x1)*(xp-x3) + (xp-x2)*(xp-x3)) = 12 * (xp * (xp-1)) := by clear he hw hwp; grind
  have pos : 0 ≤ xp * (xp - 1) := by grind
  have bpos : 0 < xp := by grind
  have b1 : 1 ≤ xp := by
    apply Classical.byContradiction
    intro hn
    have ht : xp - 1 < 0 := by grind
    have := OrderedRing.mul_lt_mul_of_pos_left ht bpos
    grind
  have hS : 2 ≤ (xp-x1) + (xp-x2) + (xp-x3) := by grind
  have f1 : wp = wc + (w1+w2+w3) - 1 := by clear he; grind
  have f2 : 4 * ((w1+w2+w3) * wc) = 2 * (w1*w1 + w2*w2 + w3*w3) - 2 * ((w1+w2+w3) * (w1+w2+w3)) := by clear he; grind
  have cle : (w1+w2+w3) * (1 + 3 * (2 * wc - (wp+wc+w1+w2+w3))
        - 4 * (2 * (xp*wp + xc*wc + x1*w1 + x2*w2 + x3*w3) - (xp+xc+x1+x2+x3) * (wp+wc+w1+w2+w3)))
      = 2 * (4 * (w1+w2+w3) * ((xp-x1)*w1 + (xp-x2)*w2 + (xp-x3)*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3)) := by
    clear he; grind
  have red := reduit (xp-x1) (xp-x2) (xp-x3) w1 w2 w3 c1 c2 c3 hS g1 g2 g3
  have zero : 4 * (w1+w2+w3) * ((xp-x1)*w1 + (xp-x2)*w2 + (xp-x3)*w3) + 2 * (w1*w1 + w2*w2 + w3*w3) - (w1+w2+w3) * (w1+w2+w3) = 0 := by
    have hz : (w1+w2+w3) * (1 + 3 * (2 * wc - (wp+wc+w1+w2+w3))
        - 4 * (2 * (xp*wp + xc*wc + x1*w1 + x2*w2 + x3*w3) - (xp+xc+x1+x2+x3) * (wp+wc+w1+w2+w3))) = 0 := by
      rw [he]; grind
    rw [cle] at hz
    grind
  have cas := reduit_egalite (xp-x1) (xp-x2) (xp-x3) w1 w2 w3 c1 c2 c3 hS g1 g2 g3 gp zero
  -- dans chaque cas, deux des x_k valent xp ; la rondeur donne alors xp (xp − 1) = 0, donc xp = 1
  have fin : ∀ (u v t : K), u + v + t = 1 → 2 * (u*u + v*v + t*t) = 4 * xp + 2 → xp - u = 0 → xp - v = 0 → xp = 1 := by
    intro u v t s q hu hv
    have hu' : u = xp := by grind
    have hv' : v = xp := by grind
    have ht : t = 1 - 2 * xp := by grind
    have k : 12 * (xp * (xp - 1)) = 0 := by rw [hu', hv', ht] at q; grind
    have k' : xp * (xp - 1) = 0 := by
      apply Classical.byContradiction
      intro hn
      have : 0 < xp * (xp - 1) := by grind
      grind
    have k2 := facteur_nul xp (xp - 1) bpos k'
    grind
  rcases cas with ⟨k1, k2⟩ | ⟨k1, k3⟩ | ⟨k2, k3⟩
  · have b := fin x1 x2 x3 e2 e3 k1 k2
    grind
  · have b := fin x1 x3 x2 (by grind) (by grind) k1 k3
    grind
  · have b := fin x2 x3 x1 (by grind) (by grind) k2 k3
    grind

/-! ## T17 sans hypothèse de signe -/

/-- Deux boules de genre lumière de produit nu strictement positif sont dans la même nappe. -/
theorem somme_positive (q1 q2 q3 q4 b1 b2 b3 b4 : K)
    (hq : nu4 q1 q2 q3 q4 q1 q2 q3 q4 = 0) (sq : 0 < q1+q2+q3+q4)
    (hb : nu4 b1 b2 b3 b4 b1 b2 b3 b4 = 0)
    (h : 0 < nu4 q1 q2 q3 q4 b1 b2 b3 b4) : 0 < b1+b2+b3+b4 := by
  unfold nu4 at *
  have cs := cauchy4 q1 q2 q3 q4 b1 b2 b3 b4
  have eq : q1*q1 + q2*q2 + q3*q3 + q4*q4 = (q1+q2+q3+q4) * (q1+q2+q3+q4) := by grind
  have eb : b1*b1 + b2*b2 + b3*b3 + b4*b4 = (b1+b2+b3+b4) * (b1+b2+b3+b4) := by grind
  rw [eq, eb] at cs
  apply Classical.byContradiction
  intro hn
  have h0 : b1+b2+b3+b4 ≤ 0 := by grind
  have h1 : (q1+q2+q3+q4) * (b1+b2+b3+b4) ≤ 0 := by
    have := OrderedRing.mul_le_mul_of_nonneg_left h0 (Preorder.le_of_lt sq)
    grind
  have h2 := carre_croissant (-(q1*b1 + q2*b2 + q3*b3 + q4*b4)) (-((q1+q2+q3+q4) * (b1+b2+b3+b4))) (by grind) (by grind)
  have r1 : (-((q1+q2+q3+q4) * (b1+b2+b3+b4))) * (-((q1+q2+q3+q4) * (b1+b2+b3+b4)))
      = ((q1+q2+q3+q4) * (q1+q2+q3+q4)) * ((b1+b2+b3+b4) * (b1+b2+b3+b4)) := by grind
  have r2 : (-(q1*b1 + q2*b2 + q3*b3 + q4*b4)) * (-(q1*b1 + q2*b2 + q3*b3 + q4*b4))
      = (q1*b1 + q2*b2 + q3*b3 + q4*b4) * (q1*b1 + q2*b2 + q3*b3 + q4*b4) := by grind
  rw [r1, r2] at h2
  grind

omit [LE K] [LT K] [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K] in
theorem nu4_sym (a1 a2 a3 a4 b1 b2 b3 b4 : K) : nu4 a1 a2 a3 a4 b1 b2 b3 b4 = nu4 b1 b2 b3 b4 a1 a2 a3 a4 := by
  unfold nu4; grind

/-- T17 pour une paire, sans hypothèse de signe sur x ni sur w : il suffit que q soit de somme positive et que nu(q, w) > 0. -/
theorem cone_paire_complet (x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 w1 w2 w3 w4 : K)
    (hx : nu4 x1 x2 x3 x4 x1 x2 x3 x4 = 0) (hq : nu4 q1 q2 q3 q4 q1 q2 q3 q4 = 0) (hr : nu4 r1 r2 r3 r4 r1 r2 r3 r4 = 0)
    (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 0)
    (sq : 0 < q1+q2+q3+q4) (hqw : 0 < nu4 q1 q2 q3 q4 w1 w2 w3 w4)
    (tq : nu4 x1 x2 x3 x4 q1 q2 q3 q4 = 1) (tr : nu4 x1 x2 x3 x4 r1 r2 r3 r4 = 1)
    (iq : 3 * nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (ir : 3 * nu4 r1 r2 r3 r4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4) :
    3 * nu4 q1 q2 q3 q4 r1 r2 r3 r4 < 16 := by
  have sx : 0 < x1+x2+x3+x4 := somme_positive q1 q2 q3 q4 x1 x2 x3 x4 hq sq hx (by rw [nu4_sym, tq]; grind)
  have sw : 0 < w1+w2+w3+w4 := somme_positive q1 q2 q3 q4 w1 w2 w3 w4 hq sq hw hqw
  exact cone_paire x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 w1 w2 w3 w4 hx hq hr hw sx sw tq tr iq ir

/-- T17 pour les trois contacts, sans hypothèse de signe sur x ni sur w. -/
theorem cone_triplet_complet (x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 s1 s2 s3 s4 w1 w2 w3 w4 : K)
    (hx : nu4 x1 x2 x3 x4 x1 x2 x3 x4 = 0) (hq : nu4 q1 q2 q3 q4 q1 q2 q3 q4 = 0) (hr : nu4 r1 r2 r3 r4 r1 r2 r3 r4 = 0)
    (hs : nu4 s1 s2 s3 s4 s1 s2 s3 s4 = 0) (hw : nu4 w1 w2 w3 w4 w1 w2 w3 w4 = 0)
    (sq : 0 < q1+q2+q3+q4) (hqw : 0 < nu4 q1 q2 q3 q4 w1 w2 w3 w4)
    (tq : nu4 x1 x2 x3 x4 q1 q2 q3 q4 = 1) (tr : nu4 x1 x2 x3 x4 r1 r2 r3 r4 = 1) (ts : nu4 x1 x2 x3 x4 s1 s2 s3 s4 = 1)
    (iq : 3 * nu4 q1 q2 q3 q4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (ir : 3 * nu4 r1 r2 r3 r4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4)
    (is : 3 * nu4 s1 s2 s3 s4 w1 w2 w3 w4 < 4 * nu4 x1 x2 x3 x4 w1 w2 w3 w4) :
    nu4 q1 q2 q3 q4 r1 r2 r3 r4 + nu4 q1 q2 q3 q4 s1 s2 s3 s4 + nu4 r1 r2 r3 r4 s1 s2 s3 s4 < 12 := by
  have sx : 0 < x1+x2+x3+x4 := somme_positive q1 q2 q3 q4 x1 x2 x3 x4 hq sq hx (by rw [nu4_sym, tq]; grind)
  have sw : 0 < w1+w2+w3+w4 := somme_positive q1 q2 q3 q4 w1 w2 w3 w4 hq sq hw hqw
  exact cone_triplet x1 x2 x3 x4 q1 q2 q3 q4 r1 r2 r3 r4 s1 s2 s3 s4 w1 w2 w3 w4 hx hq hr hs hw sx sw tq tr ts iq ir is

/-! ## T18, arithmétique des entiers d'Eisenstein -/

/-- Norme de z0 + z1 ω. -/
def eN (z0 z1 : Int) : Int := z0*z0 - z0*z1 + z1*z1

/-- αδ − βγ, partie sans ω. -/
def det0 (a0 a1 b0 b1 c0 c1 d0 d1 : Int) : Int := (a0*d0 - a1*d1) - (b0*c0 - b1*c1)
/-- αδ − βγ, coefficient de ω. -/
def det1 (a0 a1 b0 b1 c0 c1 d0 d1 : Int) : Int := (a0*d1 + a1*d0 - a1*d1) - (b0*c1 + b1*c0 - b1*c1)

theorem carre_mod3 (t : Int) : (t*t) % 3 = 0 ∨ (t*t) % 3 = 1 := by
  have h : t % 3 = 0 ∨ t % 3 = 1 ∨ t % 3 = 2 := by omega
  rcases h with h | h | h
  · left
    have e : t = 3 * (t / 3) := by omega
    have e2 : t * t = 3 * (3 * ((t/3) * (t/3))) := by rw [e]; grind
    omega
  · right
    have e : t = 3 * (t / 3) + 1 := by omega
    have e2 : t * t = 3 * (3 * ((t/3) * (t/3)) + 2 * (t/3)) + 1 := by
      generalize t / 3 = k at e
      subst e; grind
    omega
  · right
    have e : t = 3 * (t / 3) + 2 := by omega
    have e2 : t * t = 3 * (3 * ((t/3) * (t/3)) + 4 * (t/3) + 1) + 1 := by
      generalize t / 3 = k at e
      subst e; grind
    omega

/-- Une norme n'est jamais congrue à 2 modulo 3. -/
theorem norme_mod3 (z0 z1 : Int) : eN z0 z1 % 3 ≠ 2 := by
  unfold eN
  have e : z0*z0 - z0*z1 + z1*z1 = (z0+z1)*(z0+z1) - 3 * (z0*z1) := by grind
  have c := carre_mod3 (z0+z1)
  rw [e]
  omega

theorem norme_pas_2 (z0 z1 : Int) : eN z0 z1 ≠ 2 := by
  have := norme_mod3 z0 z1
  omega

theorem norme_pas_5 (z0 z1 : Int) : eN z0 z1 ≠ 5 := by
  have := norme_mod3 z0 z1
  omega

/-- Si 3 divise la norme de z, 3 divise z0 + z1. -/
theorem somme_div3 (z0 z1 : Int) (h : eN z0 z1 % 3 = 0) : (z0 + z1) % 3 = 0 := by
  unfold eN at h
  have e : z0*z0 - z0*z1 + z1*z1 = (z0+z1)*(z0+z1) - 3 * (z0*z1) := by grind
  rw [e] at h
  have hc : ((z0+z1)*(z0+z1)) % 3 = 0 := by omega
  have h3 : (z0+z1) % 3 = 0 ∨ (z0+z1) % 3 = 1 ∨ (z0+z1) % 3 = 2 := by omega
  rcases h3 with h3 | h3 | h3
  · exact h3
  · have e1 : z0+z1 = 3 * ((z0+z1) / 3) + 1 := by omega
    have e2 : (z0+z1) * (z0+z1) = 3 * (3 * (((z0+z1)/3) * ((z0+z1)/3)) + 2 * ((z0+z1)/3)) + 1 := by
      generalize (z0+z1) / 3 = k at e1
      generalize z0+z1 = t at e1
      subst e1; grind
    omega
  · have e1 : z0+z1 = 3 * ((z0+z1) / 3) + 2 := by omega
    have e2 : (z0+z1) * (z0+z1) = 3 * (3 * (((z0+z1)/3) * ((z0+z1)/3)) + 4 * ((z0+z1)/3) + 1) + 1 := by
      generalize (z0+z1) / 3 = k at e1
      generalize z0+z1 = t at e1
      subst e1; grind
    omega

/-- Si 3 divise norme(β) et norme(δ), 3 divise norme(αδ − βγ). -/
theorem det_div3 (a0 a1 b0 b1 c0 c1 d0 d1 : Int) (hb : eN b0 b1 % 3 = 0) (hd : eN d0 d1 % 3 = 0) :
    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 3 = 0 := by
  have sb := somme_div3 b0 b1 hb
  have sd := somme_div3 d0 d1 hd
  have eb : b0 = 3 * ((b0+b1)/3) - b1 := by omega
  have ed : d0 = 3 * ((d0+d1)/3) - d1 := by omega
  generalize (b0+b1)/3 = m at eb
  generalize (d0+d1)/3 = n at ed
  subst eb ed
  unfold eN det0 det1
  have e : ((a0*(3*n - d1) - a1*d1) - ((3*m - b1)*c0 - b1*c1)) * ((a0*(3*n - d1) - a1*d1) - ((3*m - b1)*c0 - b1*c1))
      - ((a0*(3*n - d1) - a1*d1) - ((3*m - b1)*c0 - b1*c1)) * ((a0*d1 + a1*(3*n - d1) - a1*d1) - ((3*m - b1)*c1 + b1*c0 - b1*c1))
      + ((a0*d1 + a1*(3*n - d1) - a1*d1) - ((3*m - b1)*c1 + b1*c0 - b1*c1)) * ((a0*d1 + a1*(3*n - d1) - a1*d1) - ((3*m - b1)*c1 + b1*c0 - b1*c1))
      = 3 * (3 * (((a0+a1)*n - a1*d1 - m*(c0+c1) + b1*c1) * ((a0+a1)*n - a1*d1 - m*(c0+c1) + b1*c1))
          - ((a0*(3*n - d1) - a1*d1) - ((3*m - b1)*c0 - b1*c1)) * ((a0*d1 + a1*(3*n - d1) - a1*d1) - ((3*m - b1)*c1 + b1*c0 - b1*c1))) := by
    grind
  rw [e]
  omega

/-- Si 2 divise la norme de z, 2 divise z0 et z1. -/
theorem pair_de_norme_paire (z0 z1 : Int) (h : eN z0 z1 % 2 = 0) : z0 % 2 = 0 ∧ z1 % 2 = 0 := by
  unfold eN at h
  have h0 : z0 % 2 = 0 ∨ z0 % 2 = 1 := by omega
  have h1 : z1 % 2 = 0 ∨ z1 % 2 = 1 := by omega
  have e0 : z0 = 2 * (z0/2) + z0 % 2 := by omega
  have e1 : z1 = 2 * (z1/2) + z1 % 2 := by omega
  generalize z0 / 2 = i at e0
  generalize z1 / 2 = j at e1
  rcases h0 with h0 | h0 <;> rcases h1 with h1 | h1
  · exact ⟨h0, h1⟩
  · exfalso
    rw [h0] at e0; rw [h1] at e1
    have e : z0*z0 - z0*z1 + z1*z1 = 2 * (2*i*i - 2*i*j - i + 2*j*j + 2*j) + 1 := by subst e0 e1; grind
    omega
  · exfalso
    rw [h0] at e0; rw [h1] at e1
    have e : z0*z0 - z0*z1 + z1*z1 = 2 * (2*i*i + 2*i - 2*i*j - j + 2*j*j) + 1 := by subst e0 e1; grind
    omega
  · exfalso
    rw [h0] at e0; rw [h1] at e1
    have e : z0*z0 - z0*z1 + z1*z1 = 2 * (2*i*i + i - 2*i*j + 2*j*j + j) + 1 := by subst e0 e1; grind
    omega

/-- Si 2 divise norme(β) et norme(δ), 4 divise norme(αδ − βγ). -/
theorem det_div4 (a0 a1 b0 b1 c0 c1 d0 d1 : Int) (hb : eN b0 b1 % 2 = 0) (hd : eN d0 d1 % 2 = 0) :
    eN (det0 a0 a1 b0 b1 c0 c1 d0 d1) (det1 a0 a1 b0 b1 c0 c1 d0 d1) % 4 = 0 := by
  have pb := pair_de_norme_paire b0 b1 hb
  have pd := pair_de_norme_paire d0 d1 hd
  have eb0 : b0 = 2 * (b0/2) := by omega
  have eb1 : b1 = 2 * (b1/2) := by omega
  have ed0 : d0 = 2 * (d0/2) := by omega
  have ed1 : d1 = 2 * (d1/2) := by omega
  generalize b0/2 = i0 at eb0
  generalize b1/2 = i1 at eb1
  generalize d0/2 = j0 at ed0
  generalize d1/2 = j1 at ed1
  subst eb0 eb1 ed0 ed1
  unfold eN det0 det1
  have e : ((a0*(2*j0) - a1*(2*j1)) - ((2*i0)*c0 - (2*i1)*c1)) * ((a0*(2*j0) - a1*(2*j1)) - ((2*i0)*c0 - (2*i1)*c1))
      - ((a0*(2*j0) - a1*(2*j1)) - ((2*i0)*c0 - (2*i1)*c1)) * ((a0*(2*j1) + a1*(2*j0) - a1*(2*j1)) - ((2*i0)*c1 + (2*i1)*c0 - (2*i1)*c1))
      + ((a0*(2*j1) + a1*(2*j0) - a1*(2*j1)) - ((2*i0)*c1 + (2*i1)*c0 - (2*i1)*c1)) * ((a0*(2*j1) + a1*(2*j0) - a1*(2*j1)) - ((2*i0)*c1 + (2*i1)*c0 - (2*i1)*c1))
      = 4 * (((a0*j0 - a1*j1) - (i0*c0 - i1*c1)) * ((a0*j0 - a1*j1) - (i0*c0 - i1*c1))
          - ((a0*j0 - a1*j1) - (i0*c0 - i1*c1)) * ((a0*j1 + a1*j0 - a1*j1) - (i0*c1 + i1*c0 - i1*c1))
          + ((a0*j1 + a1*j0 - a1*j1) - (i0*c1 + i1*c0 - i1*c1)) * ((a0*j1 + a1*j0 - a1*j1) - (i0*c1 + i1*c0 - i1*c1))) := by
    grind
  rw [e]
  omega

end X30bis

#print axioms X30bis.trois_quarts_egalite
#print axioms X30bis.cone_paire_complet
#print axioms X30bis.cone_triplet_complet
#print axioms X30bis.norme_pas_2
#print axioms X30bis.norme_pas_5
#print axioms X30bis.det_div3
#print axioms X30bis.det_div4
