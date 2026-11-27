"""Places admissibles (cotes non nes des cellules nees) dans le tissu de T28, et part occupee a la generation suivante."""
import json
import t28, libre
from commun import GERME
for s in (1, 2, 3):
    t28.TISSUS.clear(); r = t28.run('hasard', s, 9, 'hasard')
    tissus = [{u: 0 for u in GERME}] + t28.TISSUS
    lignes = []
    for g, gen in enumerate(tissus[:-1]):
        _, npl, _ = libre.candidats(gen)
        nes_suivante = len(tissus[g + 1]) - len(gen)
        lignes.append(dict(generation=g, constituants=len(gen), places_admissibles=npl, occupees_a_la_suivante=nes_suivante, part_occupee=round(nes_suivante / npl, 3)))
    print(json.dumps(dict(graine=s, par_generation=lignes)))
