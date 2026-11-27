import Enonce
/-! # X-27 — K20 est fausse : la preuve, contrôlée par le noyau de Lean.
Fichier écrit par `genere.py` (26 novembre 2026). Il ne contient que des témoins : le parent et les trois voisins de chaque naissance,
le mot de retournements qui mène du germe à chaque constituant. Lean 4 seul, sans Mathlib, sans `sorry`, sans `native_decide`. -/
namespace X27

/-- Un constituant atteint depuis le germe par un mot de retournements est dans l'empilement. -/
theorem dans_mot (k : Vec) (hk : k ∈ germe) : ∀ m : List (Fin 5), DansEmpilement (applique m k)
  | [] => DansEmpilement.germe hk
  | j :: m => DansEmpilement.retourne j (dans_mot k hk m)

theorem dans_0 : DansEmpilement (1, 0, 0, 0, 0) := by
  have h := dans_mot (1, 0, 0, 0, 0) (by decide) []
  have e : applique [] (1, 0, 0, 0, 0) = (1, 0, 0, 0, 0) := by decide
  rw [e] at h; exact h

theorem dans_1 : DansEmpilement (0, 1, 0, 0, 0) := by
  have h := dans_mot (0, 1, 0, 0, 0) (by decide) []
  have e : applique [] (0, 1, 0, 0, 0) = (0, 1, 0, 0, 0) := by decide
  rw [e] at h; exact h

theorem dans_2 : DansEmpilement (0, 0, 1, 0, 0) := by
  have h := dans_mot (0, 0, 1, 0, 0) (by decide) []
  have e : applique [] (0, 0, 1, 0, 0) = (0, 0, 1, 0, 0) := by decide
  rw [e] at h; exact h

theorem dans_3 : DansEmpilement (0, 0, 0, 1, 0) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) []
  have e : applique [] (0, 0, 0, 1, 0) = (0, 0, 0, 1, 0) := by decide
  rw [e] at h; exact h

theorem dans_4 : DansEmpilement (0, 0, 0, 0, 1) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) []
  have e : applique [] (0, 0, 0, 0, 1) = (0, 0, 0, 0, 1) := by decide
  rw [e] at h; exact h

theorem dans_5 : DansEmpilement (1, 1, 1, 1, -1) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) [4]
  have e : applique [4] (0, 0, 0, 0, 1) = (1, 1, 1, 1, -1) := by decide
  rw [e] at h; exact h

theorem dans_6 : DansEmpilement (2, 0, 2, 2, -1) := by
  have h := dans_mot (0, 1, 0, 0, 0) (by decide) [4, 1]
  have e : applique [4, 1] (0, 1, 0, 0, 0) = (2, 0, 2, 2, -1) := by decide
  rw [e] at h; exact h

theorem dans_7 : DansEmpilement (4, 1, 4, 2, -2) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [4, 1, 3]
  have e : applique [4, 1, 3] (0, 0, 0, 1, 0) = (4, 1, 4, 2, -2) := by decide
  rw [e] at h; exact h

theorem dans_8 : DansEmpilement (4, 2, 4, 1, -2) := by
  have h := dans_mot (0, 1, 0, 0, 0) (by decide) [4, 3, 1]
  have e : applique [4, 3, 1] (0, 1, 0, 0, 0) = (4, 2, 4, 1, -2) := by decide
  rw [e] at h; exact h

theorem dans_9 : DansEmpilement (8, 2, 8, 2, -3) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) [4, 1, 3, 1, 4]
  have e : applique [4, 1, 3, 1, 4] (0, 0, 0, 0, 1) = (8, 2, 8, 2, -3) := by decide
  rw [e] at h; exact h

theorem dans_10 : DansEmpilement (9, 3, 9, 1, -3) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [4, 3, 1, 4, 3]
  have e : applique [4, 3, 1, 4, 3] (0, 0, 0, 1, 0) = (9, 3, 9, 1, -3) := by decide
  rw [e] at h; exact h

theorem dans_11 : DansEmpilement (6, 3, 6, 0, -2) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) [4, 3, 1, 4]
  have e : applique [4, 3, 1, 4] (0, 0, 0, 0, 1) = (6, 3, 6, 0, -2) := by decide
  rw [e] at h; exact h

theorem dans_12 : DansEmpilement (12, 4, 12, 0, -3) := by
  have h := dans_mot (0, 1, 0, 0, 0) (by decide) [4, 3, 1, 4, 3, 1]
  have e : applique [4, 3, 1, 4, 3, 1] (0, 1, 0, 0, 0) = (12, 4, 12, 0, -3) := by decide
  rw [e] at h; exact h

theorem dans_13 : DansEmpilement (10, 4, 10, -1, -2) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [4, 3, 1, 4, 1, 3]
  have e : applique [4, 3, 1, 4, 1, 3] (0, 0, 0, 1, 0) = (10, 4, 10, -1, -2) := by decide
  rw [e] at h; exact h

theorem dans_14 : DansEmpilement (5, 3, 5, -1, -1) := by
  have h := dans_mot (0, 1, 0, 0, 0) (by decide) [3, 4, 3, 1]
  have e : applique [3, 4, 3, 1] (0, 1, 0, 0, 0) = (5, 3, 5, -1, -1) := by decide
  rw [e] at h; exact h

theorem dans_15 : DansEmpilement (1, 1, 1, -1, 1) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [3]
  have e : applique [3] (0, 0, 0, 1, 0) = (1, 1, 1, -1, 1) := by decide
  rw [e] at h; exact h

theorem dans_16 : DansEmpilement (2, 2, 0, -1, 2) := by
  have h := dans_mot (0, 0, 1, 0, 0) (by decide) [3, 2]
  have e : applique [3, 2] (0, 0, 1, 0, 0) = (2, 2, 0, -1, 2) := by decide
  rw [e] at h; exact h

theorem dans_17 : DansEmpilement (4, 4, 1, -2, 2) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) [3, 2, 4]
  have e : applique [3, 2, 4] (0, 0, 0, 0, 1) = (4, 4, 1, -2, 2) := by decide
  rw [e] at h; exact h

theorem dans_18 : DansEmpilement (4, 4, 2, -2, 1) := by
  have h := dans_mot (0, 0, 1, 0, 0) (by decide) [3, 4, 2]
  have e : applique [3, 4, 2] (0, 0, 1, 0, 0) = (4, 4, 2, -2, 1) := by decide
  rw [e] at h; exact h

theorem dans_19 : DansEmpilement (8, 8, 2, -3, 2) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [3, 2, 4, 2, 3]
  have e : applique [3, 2, 4, 2, 3] (0, 0, 0, 1, 0) = (8, 8, 2, -3, 2) := by decide
  rw [e] at h; exact h

theorem dans_20 : DansEmpilement (9, 9, 3, -3, 1) := by
  have h := dans_mot (0, 0, 0, 0, 1) (by decide) [3, 4, 2, 3, 4]
  have e : applique [3, 4, 2, 3, 4] (0, 0, 0, 0, 1) = (9, 9, 3, -3, 1) := by decide
  rw [e] at h; exact h

theorem dans_21 : DansEmpilement (6, 6, 3, -2, 0) := by
  have h := dans_mot (0, 0, 0, 1, 0) (by decide) [3, 4, 2, 3]
  have e : applique [3, 4, 2, 3] (0, 0, 0, 1, 0) = (6, 6, 3, -2, 0) := by decide
  rw [e] at h; exact h

theorem indep_1 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (0, 0, 1, 0, 0) (0, 0, 0, 1, 0) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_1 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)] ⟨(1, 1, 1, 1, -1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_1⟩

theorem indep_2 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (0, 0, 0, 1, 0) (1, 1, 1, 1, -1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_2 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1)] ⟨(2, 0, 2, 2, -1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (1, 1, 1, 1, -1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_2⟩

theorem indep_3 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (1, 1, 1, 1, -1) (2, 0, 2, 2, -1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_3 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1)] ⟨(4, 1, 4, 2, -2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_3⟩

theorem indep_4 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (1, 1, 1, 1, -1) (4, 1, 4, 2, -2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_4 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2)] ⟨(4, 2, 4, 1, -2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (1, 1, 1, 1, -1), (4, 1, 4, 2, -2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_4⟩

theorem indep_5 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (4, 1, 4, 2, -2) (4, 2, 4, 1, -2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_5 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2)] ⟨(8, 2, 8, 2, -3), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_5⟩

theorem indep_6 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (4, 2, 4, 1, -2) (8, 2, 8, 2, -3) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_6 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3)] ⟨(9, 3, 9, 1, -3), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_6⟩

theorem indep_7 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (4, 2, 4, 1, -2) (9, 3, 9, 1, -3) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_7 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3)] ⟨(6, 3, 6, 0, -2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (4, 2, 4, 1, -2), (9, 3, 9, 1, -3),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_7⟩

theorem indep_8 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (9, 3, 9, 1, -3) (6, 3, 6, 0, -2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_8 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2)] ⟨(12, 4, 12, 0, -3), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_8⟩

theorem indep_9 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (6, 3, 6, 0, -2) (12, 4, 12, 0, -3) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_9 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3)] ⟨(10, 4, 10, -1, -2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_9⟩

theorem indep_10 : independants (1, 0, 0, 0, 0) (0, 0, 1, 0, 0) (6, 3, 6, 0, -2) (10, 4, 10, -1, -2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_10 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2)] ⟨(5, 3, 5, -1, -1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (6, 3, 6, 0, -2), (10, 4, 10, -1, -2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_10⟩

theorem indep_11 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (0, 0, 1, 0, 0) (0, 0, 0, 0, 1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_11 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1)] ⟨(1, 1, 1, -1, 1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 0, 1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_11⟩

theorem indep_12 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (0, 0, 0, 0, 1) (1, 1, 1, -1, 1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_12 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1)] ⟨(2, 2, 0, -1, 2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 0, 1), (1, 1, 1, -1, 1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_12⟩

theorem indep_13 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (1, 1, 1, -1, 1) (2, 2, 0, -1, 2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_13 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2)] ⟨(4, 4, 1, -2, 2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_13⟩

theorem indep_14 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (1, 1, 1, -1, 1) (4, 4, 1, -2, 2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_14 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2), (4, 4, 1, -2, 2)] ⟨(4, 4, 2, -2, 1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (1, 1, 1, -1, 1), (4, 4, 1, -2, 2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_14⟩

theorem indep_15 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (4, 4, 1, -2, 2) (4, 4, 2, -2, 1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_15 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2), (4, 4, 1, -2, 2), (4, 4, 2, -2, 1)] ⟨(8, 8, 2, -3, 2), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (4, 4, 1, -2, 2), (4, 4, 2, -2, 1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_15⟩

theorem indep_16 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (4, 4, 2, -2, 1) (8, 8, 2, -3, 2) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_16 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2), (4, 4, 1, -2, 2), (4, 4, 2, -2, 1), (8, 8, 2, -3, 2)] ⟨(9, 9, 3, -3, 1), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (4, 4, 2, -2, 1), (8, 8, 2, -3, 2),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_16⟩

theorem indep_17 : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (4, 4, 2, -2, 1) (9, 9, 3, -3, 1) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem naissance_17 : NaissanceDansCellule [(1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, -1), (2, 0, 2, 2, -1), (4, 1, 4, 2, -2), (4, 2, 4, 1, -2), (8, 2, 8, 2, -3), (9, 3, 9, 1, -3), (6, 3, 6, 0, -2), (12, 4, 12, 0, -3), (10, 4, 10, -1, -2), (5, 3, 5, -1, -1), (1, 1, 1, -1, 1), (2, 2, 0, -1, 2), (4, 4, 1, -2, 2), (4, 4, 2, -2, 1), (8, 8, 2, -3, 2), (9, 9, 3, -3, 1)] ⟨(6, 6, 3, -2, 0), 1⟩ :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (4, 4, 2, -2, 1), (9, 9, 3, -3, 1),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_17⟩

theorem tissu_de_cellules : TissuDeCellules germe naissances17 :=
  ⟨naissance_1, naissance_2, naissance_3, naissance_4, naissance_5, naissance_6, naissance_7, naissance_8, naissance_9, naissance_10, naissance_11, naissance_12, naissance_13, naissance_14, naissance_15, naissance_16, naissance_17, trivial⟩

theorem tissu : Tissu germe naissances17 :=
  ⟨cellule_admissible naissance_1, cellule_admissible naissance_2, cellule_admissible naissance_3, cellule_admissible naissance_4, cellule_admissible naissance_5, cellule_admissible naissance_6, cellule_admissible naissance_7, cellule_admissible naissance_8, cellule_admissible naissance_9, cellule_admissible naissance_10, cellule_admissible naissance_11, cellule_admissible naissance_12, cellule_admissible naissance_13, cellule_admissible naissance_14, cellule_admissible naissance_15, cellule_admissible naissance_16, cellule_admissible naissance_17, trivial⟩

theorem tissu_dans_empilement : ∀ u ∈ tissu22, DansEmpilement u := by
  intro u hu
  simp only [tissu22, germe, naissances17, List.cons_append, List.nil_append, List.mem_cons, List.not_mem_nil, or_false] at hu
  rcases hu with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact dans_0
  · exact dans_1
  · exact dans_2
  · exact dans_3
  · exact dans_4
  · exact dans_5
  · exact dans_6
  · exact dans_7
  · exact dans_8
  · exact dans_9
  · exact dans_10
  · exact dans_11
  · exact dans_12
  · exact dans_13
  · exact dans_14
  · exact dans_15
  · exact dans_16
  · exact dans_17
  · exact dans_18
  · exact dans_19
  · exact dans_20
  · exact dans_21

theorem indep_place : independants (1, 0, 0, 0, 0) (0, 1, 0, 0, 0) (5, 3, 5, -1, -1) (6, 6, 3, -2, 0) := by
  intro α β γ δ h
  simp only [comb, Prod.mk.injEq] at h
  omega

theorem place_admissible : PlaceAdmissible tissu22 place :=
  ⟨by decide, by decide, by decide, (1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (5, 3, 5, -1, -1), (6, 6, 3, -2, 0),
   by decide, by decide, by decide, by decide, by decide, by decide, by decide,
   by decide, by decide, by decide, by decide, indep_place⟩

theorem place_hors_empilement : ¬ BouleDansEmpilement place := by
  rintro ⟨⟨a, b, c, d, e⟩, _, h⟩
  simp only [place, fois, Prod.mk.injEq] at h
  omega

/-- **K20 est fausse.** L'énoncé est dans `Enonce.lean`. -/
theorem K20_est_fausse : EnonceK20Fausse :=
  ⟨tissu, tissu_de_cellules, tissu_dans_empilement, place_admissible, place_hors_empilement⟩

end X27

#print axioms X27.K20_est_fausse

