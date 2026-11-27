/-!
# X-28 — le lemme du pont (T2)

Lecture de contact, rang 3 (laboratoire du Principe du Blob, carnet X-28 du 27 novembre 2026).
Lean 4 seul, sans Mathlib. Écrit à la main (Claude, pilote IA).

Énoncé en clair. Soit {p, a, b, c, d} une tuile (cinq constituants tous liés), x une boule liée à p qui ne chevauche ni a,
ni b, ni c, ni d, et q, r deux boules rondes liées à p et à x. Si le milieu de q et r vu de p, le vecteur q + r + 2p,
est une combinaison à coefficients positifs ou nuls de a, b, c, d (et de p), alors le produit de q et r vaut au moins −2.
Pour deux constituants de l'empilement ce produit est impair : il vaut donc −1, q et r sont liés.

La boule x est donnée par un numérateur entier v et un dénominateur D > 0. Le milieu est pris à un facteur entier N > 0 près,
ce qui autorise des coefficients rationnels. La rondeur de x ne sert pas.
-/

namespace X28

/-- Un vecteur à coordonnées entières dans la base du germe. -/
abbrev Vec := Int × Int × Int × Int × Int

/-- Le produit de la lecture de contact : ⟨a,b⟩ = 2 Σ aᵢbᵢ − (Σ aᵢ)(Σ bᵢ). -/
def prod : Vec → Vec → Int
  | (a₀, a₁, a₂, a₃, a₄), (b₀, b₁, b₂, b₃, b₄) =>
    2 * (a₀ * b₀ + a₁ * b₁ + a₂ * b₂ + a₃ * b₃ + a₄ * b₄) - (a₀ + a₁ + a₂ + a₃ + a₄) * (b₀ + b₁ + b₂ + b₃ + b₄)

/-- Somme de deux vecteurs. -/
def plus : Vec → Vec → Vec
  | (a₀, a₁, a₂, a₃, a₄), (b₀, b₁, b₂, b₃, b₄) => (a₀ + b₀, a₁ + b₁, a₂ + b₂, a₃ + b₃, a₄ + b₄)

/-- k fois un vecteur. -/
def fois (k : Int) : Vec → Vec
  | (a₀, a₁, a₂, a₃, a₄) => (k * a₀, k * a₁, k * a₂, k * a₃, k * a₄)

theorem prod_comm (u w : Vec) : prod u w = prod w u := by
  obtain ⟨u0, u1, u2, u3, u4⟩ := u; obtain ⟨w0, w1, w2, w3, w4⟩ := w
  simp only [prod]; grind

theorem prod_plus (u w z : Vec) : prod (plus u w) z = prod u z + prod w z := by
  obtain ⟨u0, u1, u2, u3, u4⟩ := u; obtain ⟨w0, w1, w2, w3, w4⟩ := w; obtain ⟨z0, z1, z2, z3, z4⟩ := z
  simp only [prod, plus]; grind

theorem prod_fois (k : Int) (u z : Vec) : prod (fois k u) z = k * prod u z := by
  obtain ⟨u0, u1, u2, u3, u4⟩ := u; obtain ⟨z0, z1, z2, z3, z4⟩ := z
  simp only [prod, fois]; grind

/-- Produit du milieu (à N près) avec un vecteur z. -/
theorem pM (N : Int) (q r p z : Vec) :
    prod (fois N (plus (plus q r) (fois 2 p))) z = N * (prod q z + prod r z + 2 * prod p z) := by
  simp only [prod_fois, prod_plus]

/-- Produit d'une combinaison de la tuile avec un vecteur z. -/
theorem pR (π αa αb αc αd : Int) (p a b c d z : Vec) :
    prod (plus (fois π p) (plus (fois αa a) (plus (fois αb b) (plus (fois αc c) (fois αd d))))) z
      = π * prod p z + (αa * prod a z + (αb * prod b z + (αc * prod c z + αd * prod d z))) := by
  simp only [prod_fois, prod_plus]

theorem carre_positif (x : Int) : 0 ≤ x * x := by
  rcases Int.le_total 0 x with h | h
  · exact Int.mul_nonneg h h
  · have h' : 0 ≤ -x := by omega
    have := Int.mul_nonneg h' h'
    have e : -x * -x = x * x := by grind
    omega

/-- Identité de polynômes qui porte le calcul de la norme du milieu. -/
theorem ident (N π αa αb αc αd g Aa Ab Ac Ad Ba Bb Bc Bd : Int) :
    N * N * (2 * g - 2) - (2 * (αa * αa + αb * αb + αc * αc + αd * αd) - 2 * ((αa + αb + αc + αd) * (αa + αb + αc + αd)))
    = N * ((N * (1 + g + 2 * -1) - (π * -1 + (αa * Aa + (αb * Ab + (αc * Ac + αd * Ad)))))
         + (N * (g + 1 + 2 * -1) - (π * -1 + (αa * Ba + (αb * Bb + (αc * Bc + αd * Bd))))))
      + αa * (N * (Aa + Ba + 2 * -1) - (π * -1 + (αa * 1 + (αb * -1 + (αc * -1 + αd * -1)))))
      + αb * (N * (Ab + Bb + 2 * -1) - (π * -1 + (αa * -1 + (αb * 1 + (αc * -1 + αd * -1)))))
      + αc * (N * (Ac + Bc + 2 * -1) - (π * -1 + (αa * -1 + (αb * -1 + (αc * 1 + αd * -1)))))
      + αd * (N * (Ad + Bd + 2 * -1) - (π * -1 + (αa * -1 + (αb * -1 + (αc * -1 + αd * 1)))))
      - (π - (αa + αb + αc + αd)) * (2 * N + (αa + αb + αc + αd)) := by grind

/-- La norme du milieu, calculée des deux façons. -/
theorem norme (N π αa αb αc αd g Aa Ab Ac Ad Ba Bb Bc Bd : Int)
    (hπ : π = αa + αb + αc + αd)
    (ea : N * (Aa + Ba + 2 * -1) = π * -1 + (αa * 1 + (αb * -1 + (αc * -1 + αd * -1))))
    (eb : N * (Ab + Bb + 2 * -1) = π * -1 + (αa * -1 + (αb * 1 + (αc * -1 + αd * -1))))
    (ec : N * (Ac + Bc + 2 * -1) = π * -1 + (αa * -1 + (αb * -1 + (αc * 1 + αd * -1))))
    (ed : N * (Ad + Bd + 2 * -1) = π * -1 + (αa * -1 + (αb * -1 + (αc * -1 + αd * 1))))
    (eq : N * (1 + g + 2 * -1) = π * -1 + (αa * Aa + (αb * Ab + (αc * Ac + αd * Ad))))
    (er : N * (g + 1 + 2 * -1) = π * -1 + (αa * Ba + (αb * Bb + (αc * Bc + αd * Bd)))) :
    N * N * (2 * g - 2) = 2 * (αa * αa + αb * αb + αc * αc + αd * αd) - 2 * ((αa + αb + αc + αd) * (αa + αb + αc + αd)) := by
  have h := ident N π αa αb αc αd g Aa Ab Ac Ad Ba Bb Bc Bd
  have da : N * (Aa + Ba + 2 * -1) - (π * -1 + (αa * 1 + (αb * -1 + (αc * -1 + αd * -1)))) = 0 := by omega
  have db : N * (Ab + Bb + 2 * -1) - (π * -1 + (αa * -1 + (αb * 1 + (αc * -1 + αd * -1)))) = 0 := by omega
  have dc : N * (Ac + Bc + 2 * -1) - (π * -1 + (αa * -1 + (αb * -1 + (αc * 1 + αd * -1)))) = 0 := by omega
  have dd : N * (Ad + Bd + 2 * -1) - (π * -1 + (αa * -1 + (αb * -1 + (αc * -1 + αd * 1)))) = 0 := by omega
  have dq : N * (1 + g + 2 * -1) - (π * -1 + (αa * Aa + (αb * Ab + (αc * Ac + αd * Ad)))) = 0 := by omega
  have dr : N * (g + 1 + 2 * -1) - (π * -1 + (αa * Ba + (αb * Bb + (αc * Bc + αd * Bd)))) = 0 := by omega
  have dπ : π - (αa + αb + αc + αd) = 0 := by omega
  rw [da, db, dc, dd, dq, dr, dπ] at h
  simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.sub_zero] at h
  omega

/-- La somme des coefficients est au plus 2N. -/
theorem somme (N D π αa αb αc αd Xa Xb Xc Xd : Int) (hD : 0 < D)
    (hπ : π = αa + αb + αc + αd)
    (ev : N * (-D + -D + 2 * -D) = π * -D + (αa * Xa + (αb * Xb + (αc * Xc + αd * Xd))))
    (ma : αa * Xa ≤ αa * -D) (mb : αb * Xb ≤ αb * -D) (mc : αc * Xc ≤ αc * -D) (md : αd * Xd ≤ αd * -D) :
    αa + αb + αc + αd ≤ 2 * N := by
  have n1 : N * (-D + -D + 2 * -D) = -(4 * (N * D)) := by grind
  have n2 : π * -D = -(αa * D) - αb * D - αc * D - αd * D := by rw [hπ]; grind
  have n3 : αa * -D = -(αa * D) := by grind
  have n4 : αb * -D = -(αb * D) := by grind
  have n5 : αc * -D = -(αc * D) := by grind
  have n6 : αd * -D = -(αd * D) := by grind
  have n7 : (αa + αb + αc + αd) * D = αa * D + αb * D + αc * D + αd * D := by grind
  have n8 : (2 * N) * D = 2 * (N * D) := by grind
  have hAD : (αa + αb + αc + αd) * D ≤ (2 * N) * D := by omega
  exact Int.le_of_mul_le_mul_right hAD hD

/-- La conclusion, en nombres : des trois relations on tire g ≥ −2. -/
theorem conclusion (N αa αb αc αd g : Int) (hN : 0 < N)
    (h0a : 0 ≤ αa) (h0b : 0 ≤ αb) (h0c : 0 ≤ αc) (h0d : 0 ≤ αd)
    (hA : αa + αb + αc + αd ≤ 2 * N)
    (e3 : N * N * (2 * g - 2) = 2 * (αa * αa + αb * αb + αc * αc + αd * αd) - 2 * ((αa + αb + αc + αd) * (αa + αb + αc + αd))) :
    -2 ≤ g := by
  have s1 := carre_positif (αa - αb); have s2 := carre_positif (αa - αc); have s3 := carre_positif (αa - αd)
  have s4 := carre_positif (αb - αc); have s5 := carre_positif (αb - αd); have s6 := carre_positif (αc - αd)
  have sos : 4 * (αa * αa + αb * αb + αc * αc + αd * αd) - (αa + αb + αc + αd) * (αa + αb + αc + αd)
      = (αa - αb) * (αa - αb) + (αa - αc) * (αa - αc) + (αa - αd) * (αa - αd)
        + (αb - αc) * (αb - αc) + (αb - αd) * (αb - αd) + (αc - αd) * (αc - αd) := by grind
  have hA0 : 0 ≤ αa + αb + αc + αd := by omega
  have hA2 : (αa + αb + αc + αd) * (αa + αb + αc + αd) ≤ (2 * N) * (2 * N) := Int.mul_le_mul hA hA hA0 (by omega)
  have n1 : N * N * (2 * g - 2) = 2 * (N * N * g) - 2 * (N * N) := by grind
  have n2 : (N * N) * (1 - g) = N * N - N * N * g := by grind
  have n3 : (2 * N) * (2 * N) = 4 * (N * N) := by grind
  have n4 : (N * N) * 3 = 3 * (N * N) := by grind
  have clef : (N * N) * (1 - g) ≤ (N * N) * 3 := by omega
  have := Int.le_of_mul_le_mul_left clef (Int.mul_pos hN hN)
  omega

/-- **Le lemme du pont.** -/
theorem pont (p a b c d q r v : Vec) (D N π αa αb αc αd : Int)
    -- la tuile {p, a, b, c, d}
    (hpp : prod p p = 1) (haa : prod a a = 1) (hbb : prod b b = 1) (hcc : prod c c = 1) (hdd : prod d d = 1)
    (hpa : prod p a = -1) (hpb : prod p b = -1) (hpc : prod p c = -1) (hpd : prod p d = -1)
    (hab : prod a b = -1) (hac : prod a c = -1) (had : prod a d = -1)
    (hbc : prod b c = -1) (hbd : prod b d = -1) (hcd : prod c d = -1)
    -- la boule x = v / D : liée à p, ne chevauche ni a, ni b, ni c, ni d
    (hD : 0 < D) (hvp : prod v p = -D)
    (hva : prod v a ≤ -D) (hvb : prod v b ≤ -D) (hvc : prod v c ≤ -D) (hvd : prod v d ≤ -D)
    -- q et r : rondes, liées à p et à x
    (hqq : prod q q = 1) (hrr : prod r r = 1) (hqp : prod q p = -1) (hrp : prod r p = -1)
    (hvq : prod v q = -D) (hvr : prod v r = -D)
    -- le milieu de q et r vu de p est dans la tuile
    (hN : 0 < N) (h0a : 0 ≤ αa) (h0b : 0 ≤ αb) (h0c : 0 ≤ αc) (h0d : 0 ≤ αd)
    (hmil : fois N (plus (plus q r) (fois 2 p))
        = plus (fois π p) (plus (fois αa a) (plus (fois αb b) (plus (fois αc c) (fois αd d))))) :
    -2 ≤ prod q r := by
  -- produits du milieu avec p, v, a, b, c, d, q, r, calculés des deux façons
  have e (z : Vec) : N * (prod q z + prod r z + 2 * prod p z)
      = π * prod p z + (αa * prod a z + (αb * prod b z + (αc * prod c z + αd * prod d z))) := by
    rw [← pM, ← pR, hmil]
  have ep := e p; have ev := e v; have ea := e a; have eb := e b; have ec := e c; have ed := e d
  have eq := e q; have er := e r
  clear e
  -- on ramène tous les produits à ceux des hypothèses
  have hap := (prod_comm a p).trans hpa; have hbp := (prod_comm b p).trans hpb
  have hcp := (prod_comm c p).trans hpc; have hdp := (prod_comm d p).trans hpd
  have hba := (prod_comm b a).trans hab; have hca := (prod_comm c a).trans hac; have hda := (prod_comm d a).trans had
  have hcb := (prod_comm c b).trans hbc; have hdb := (prod_comm d b).trans hbd; have hdc := (prod_comm d c).trans hcd
  have hpq := (prod_comm p q).trans hqp; have hpr := (prod_comm p r).trans hrp
  have hpv := (prod_comm p v).trans hvp; have hqv := (prod_comm q v).trans hvq; have hrv := (prod_comm r v).trans hvr
  rw [hqp, hrp, hpp, hap, hbp, hcp, hdp] at ep
  rw [hqv, hrv, hpv, prod_comm a v, prod_comm b v, prod_comm c v, prod_comm d v] at ev
  rw [hpa, haa, hba, hca, hda] at ea
  rw [hpb, hab, hbb, hcb, hdb] at eb
  rw [hpc, hac, hbc, hcc, hdc] at ec
  rw [hpd, had, hbd, hcd, hdd] at ed
  rw [hqq, hpq, prod_comm r q, prod_comm a q, prod_comm b q, prod_comm c q, prod_comm d q] at eq
  rw [hrr, hpr, prod_comm a r, prod_comm b r, prod_comm c r, prod_comm d r] at er
  -- (1) π est la somme des coefficients
  have hπ : π = αa + αb + αc + αd := by omega
  -- (2) la somme des coefficients est au plus 2N
  have hA : αa + αb + αc + αd ≤ 2 * N :=
    somme N D π αa αb αc αd (prod v a) (prod v b) (prod v c) (prod v d) hD hπ ev
      (Int.mul_le_mul_of_nonneg_left hva h0a) (Int.mul_le_mul_of_nonneg_left hvb h0b)
      (Int.mul_le_mul_of_nonneg_left hvc h0c) (Int.mul_le_mul_of_nonneg_left hvd h0d)
  -- (3) la norme du milieu, puis (4) la conclusion
  exact conclusion N αa αb αc αd (prod q r) hN h0a h0b h0c h0d hA
    (norme N π αa αb αc αd (prod q r) (prod q a) (prod q b) (prod q c) (prod q d) (prod r a) (prod r b) (prod r c) (prod r d)
      hπ ea eb ec ed eq er)

end X28

#print axioms X28.pont
