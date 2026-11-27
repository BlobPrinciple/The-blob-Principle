import TroisQuartsEtCone
open X30bis
-- Satisfiabilite des hypotheses, dans Z (tuile = germe).
-- trois_quarts : p = e1, c = e2, x = retourne de f3 = (1,1,1,1,-1), w = f1 = e3.
example : 4 * (2 * ((1:Int)*0 + 1*0 + 1*1 + 1*0 + (-1)*0) - (1+1+1+1+(-1)) * (0+0+1+0+0)) ≤ 1 + 3 * (2 * 0 - (0+0+1+0+0)) :=
  trois_quarts (K := Int) 1 1 1 1 (-1) 0 0 1 0 0 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
    (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
-- trois_quarts avec x hors de l'empilement : x = 20000 * (b, b, 1 + e, 1 + e, -1 - 2e), e = 1/100, n'est pas entier ;
-- on ne peut pas le mettre dans Z sans changer les equations (non homogenes). Voir le controle Python.
-- cone_paire : base du germe, p = e1, coordonnees sur (e2, e3, e4, e5) : x = e2, q = e3, r = e4, w = e5.
example : 3 * nu4 (0:Int) 1 0 0 0 0 1 0 < 16 :=
  cone_paire (K := Int) 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
    (by decide) (by decide) (by decide) (by decide)
-- cone_triplet : x = e2, q = e3, r = e4, s = e5, w = retourne de e2 = (-1, 1, 1, 1).
example : nu4 (0:Int) 1 0 0 0 0 1 0 + nu4 (0:Int) 1 0 0 0 0 0 1 + nu4 (0:Int) 0 1 0 0 0 0 1 < 12 :=
  cone_triplet (K := Int) 1 0 0 0  0 1 0 0  0 0 1 0  0 0 0 1  (-1) 1 1 1 (by decide) (by decide) (by decide) (by decide) (by decide)
    (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
