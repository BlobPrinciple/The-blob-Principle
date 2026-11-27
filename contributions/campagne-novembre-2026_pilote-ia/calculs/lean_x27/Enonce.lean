/-!
# X-27 — K20 est fausse : l'énoncé

Lecture de contact, rang 3 (laboratoire du Principe du Blob, carnet X-27 du 23 novembre 2026).
Ce fichier ne contient que des définitions et un énoncé. Il n'importe rien : Lean 4 seul, sans Mathlib.
La preuve est dans `Preuve.lean`. Écrit à la main le 26 novembre 2026 (Claude, pilote IA).

Un constituant est une boule ronde de la sphère S³. On l'écrit par ses cinq coordonnées dans la base du germe
(cinq constituants tous liés). Le produit de deux boules vaut 1 pour une boule avec elle-même, −1 quand elles se
touchent, moins que −1 quand elles sont séparées, plus que −1 quand elles se chevauchent.
-/

namespace X27

/-- Un vecteur à coordonnées entières dans la base du germe. -/
abbrev Vec := Int × Int × Int × Int × Int

/-- Le produit de la lecture de contact : ⟨a,b⟩ = 2 Σ aᵢbᵢ − (Σ aᵢ)(Σ bᵢ). -/
def prod : Vec → Vec → Int
  | (a₀, a₁, a₂, a₃, a₄), (b₀, b₁, b₂, b₃, b₄) =>
    2 * (a₀ * b₀ + a₁ * b₁ + a₂ * b₂ + a₃ * b₃ + a₄ * b₄) - (a₀ + a₁ + a₂ + a₃ + a₄) * (b₀ + b₁ + b₂ + b₃ + b₄)

/-- Le germe : cinq constituants tous liés. -/
def germe : List Vec := [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]

/-- Les cinq retournements du groupe d'Apollonius : la coordonnée j change de signe, les quatre autres la reçoivent. -/
def retourne : Fin 5 → Vec → Vec
  | 0, (a, b, c, d, e) => (-a, b + a, c + a, d + a, e + a)
  | 1, (a, b, c, d, e) => (a + b, -b, c + b, d + b, e + b)
  | 2, (a, b, c, d, e) => (a + c, b + c, -c, d + c, e + c)
  | 3, (a, b, c, d, e) => (a + d, b + d, c + d, -d, e + d)
  | 4, (a, b, c, d, e) => (a + e, b + e, c + e, d + e, -e)

/-- Un mot de retournements appliqué à un vecteur : `applique [j₁, j₂, …] u = retourne j₁ (retourne j₂ (… u))`. -/
def applique : List (Fin 5) → Vec → Vec
  | [], u => u
  | j :: m, u => retourne j (applique m u)

/-- L'EMPILEMENT né du germe : tout ce qu'on atteint depuis le germe par des retournements.
Les retournements ont des coefficients entiers : l'empilement est fait de vecteurs entiers, par construction. -/
inductive DansEmpilement : Vec → Prop
  | germe {u : Vec} : u ∈ germe → DansEmpilement u
  | retourne (j : Fin 5) {u : Vec} : DansEmpilement u → DansEmpilement (retourne j u)

/-- Deux constituants sont LIÉS quand ils se touchent : leur produit vaut −1. -/
abbrev lies (u w : Vec) : Prop := prod u w = -1

/-- Une boule à coordonnées rationnelles : le vecteur `num` divisé par l'entier `den`. -/
structure Boule where
  num : Vec
  den : Int

/-- La boule est ronde : ⟨x,x⟩ = 1. -/
abbrev ronde (x : Boule) : Prop := prod x.num x.num = x.den * x.den
/-- La boule touche le constituant u : ⟨x,u⟩ = −1. -/
abbrev touche (x : Boule) (u : Vec) : Prop := prod x.num u = -x.den
/-- La boule ne chevauche pas le constituant u : ⟨x,u⟩ ≤ −1. -/
abbrev neChevauchePas (x : Boule) (u : Vec) : Prop := prod x.num u ≤ -x.den

/-- La combinaison α·p + β·q + γ·r + δ·s. -/
def comb (α β γ δ : Int) : Vec → Vec → Vec → Vec → Vec
  | (p₀, p₁, p₂, p₃, p₄), (q₀, q₁, q₂, q₃, q₄), (r₀, r₁, r₂, r₃, r₄), (s₀, s₁, s₂, s₃, s₄) =>
    (α * p₀ + β * q₀ + γ * r₀ + δ * s₀, α * p₁ + β * q₁ + γ * r₁ + δ * s₁, α * p₂ + β * q₂ + γ * r₂ + δ * s₂,
     α * p₃ + β * q₃ + γ * r₃ + δ * s₃, α * p₄ + β * q₄ + γ * r₄ + δ * s₄)

/-- Quatre vecteurs entiers sont INDÉPENDANTS : aucune combinaison entière non nulle ne s'annule
(pour des vecteurs entiers, c'est la même chose que l'indépendance sur les rationnels ou sur les réels). -/
abbrev independants (p q r s : Vec) : Prop :=
  ∀ α β γ δ : Int, comb α β γ δ p q r s = (0, 0, 0, 0, 0) → α = 0 ∧ β = 0 ∧ γ = 0 ∧ δ = 0

/-- PLACE ADMISSIBLE du tissu S (naissance héritée et fixée) : une boule ronde x qui touche son parent p et trois
voisins q, r, s de p, les quatre étant indépendants, et qui ne chevauche aucun constituant du tissu. -/
abbrev PlaceAdmissible (S : List Vec) (x : Boule) : Prop :=
  0 < x.den ∧ ronde x ∧ (∀ u ∈ S, neChevauchePas x u) ∧
  ∃ p q r s : Vec, p ∈ S ∧ q ∈ S ∧ r ∈ S ∧ s ∈ S ∧ lies p q ∧ lies p r ∧ lies p s ∧
    touche x p ∧ touche x q ∧ touche x r ∧ touche x s ∧ independants p q r s

/-- NAISSANCE DANS LA CELLULE : la plus stricte des naissances héritées et fixées. Le parent et les trois voisins
sont de plus tous liés entre eux. -/
abbrev NaissanceDansCellule (S : List Vec) (x : Boule) : Prop :=
  0 < x.den ∧ ronde x ∧ (∀ u ∈ S, neChevauchePas x u) ∧
  ∃ p q r s : Vec, p ∈ S ∧ q ∈ S ∧ r ∈ S ∧ s ∈ S ∧ lies p q ∧ lies p r ∧ lies p s ∧ lies q r ∧ lies q s ∧ lies r s ∧
    touche x p ∧ touche x q ∧ touche x r ∧ touche x s ∧ independants p q r s

/-- UN TISSU : à partir de S, les naissances de la liste ont lieu une à une, chacune à une place admissible du tissu déjà là. -/
def Tissu (S : List Vec) : List Vec → Prop
  | [] => True
  | u :: suite => PlaceAdmissible S ⟨u, 1⟩ ∧ Tissu (S ++ [u]) suite

/-- Le même, quand chaque naissance est une naissance dans la cellule. -/
def TissuDeCellules (S : List Vec) : List Vec → Prop
  | [] => True
  | u :: suite => NaissanceDansCellule S ⟨u, 1⟩ ∧ TissuDeCellules (S ++ [u]) suite

/-- d fois un vecteur. -/
def fois (d : Int) : Vec → Vec
  | (a, b, c, d', e) => (d * a, d * b, d * c, d * d', d * e)

/-- La boule x = num/den est un constituant de l'empilement. -/
abbrev BouleDansEmpilement (x : Boule) : Prop := ∃ u : Vec, DansEmpilement u ∧ x.num = fois x.den u

/-! ## Le contre-exemple du carnet X-27 -/

/-- Les 17 naissances, dans l'ordre. -/
def naissances17 : List Vec :=
  [(1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3),
   (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2),
   (4, 4, 1, -2, 2), (4, 4, 2, -2, 1), (8, 8, 2, -3, 2), (9, 9, 3, -3, 1), (6, 6, 3, -2, 0)]

/-- Le tissu de 22 constituants : le germe et ses 17 naissances. -/
def tissu22 : List Vec := germe ++ naissances17

/-- La place : la boule (18, 18, 16, −6, −3)/7. -/
def place : Boule := ⟨(18, 18, 16, -6, -3), 7⟩

/-- **K20 est fausse.** K20 disait : quel que soit l'ordre des naissances, toute place admissible appartient à l'empilement.
Ici : (1) les 17 naissances forment un tissu ; (2) ce sont toutes des naissances dans la cellule ; (3) les 22 constituants
sont dans l'empilement ; (4) la place est une place admissible de ce tissu ; (5) elle n'est pas dans l'empilement. -/
def EnonceK20Fausse : Prop :=
  Tissu germe naissances17 ∧ TissuDeCellules germe naissances17 ∧ (∀ u ∈ tissu22, DansEmpilement u) ∧
  PlaceAdmissible tissu22 place ∧ ¬ BouleDansEmpilement place

/-- Une naissance dans la cellule est une naissance héritée et fixée (on oublie trois liens). -/
theorem cellule_admissible {S : List Vec} {x : Boule} : NaissanceDansCellule S x → PlaceAdmissible S x
  | ⟨h1, h2, h3, p, q, r, s, hp, hq, hr, hs, a, b, c, _, _, _, t1, t2, t3, t4, i⟩ =>
    ⟨h1, h2, h3, p, q, r, s, hp, hq, hr, hs, a, b, c, t1, t2, t3, t4, i⟩

end X27
