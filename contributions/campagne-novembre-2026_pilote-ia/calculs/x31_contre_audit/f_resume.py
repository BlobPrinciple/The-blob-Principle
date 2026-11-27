# Resume des tissus tires (lit b_tissus_1_40.out)
import json
from collections import Counter
L = [json.loads(l) for l in open('/home/claude/audit_x31/b_tissus_1_40.out') if l.startswith('{')]
print("tissus:", len(L), "; constituants min/max:", min(r['constituants'] for r in L), max(r['constituants'] for r in L))
print("modes:", dict(Counter(r['mode'] for r in L)))
print("generation maximale atteinte (nombre de tissus):", dict(sorted(Counter(r['generation_max'] for r in L).items())))
print("tissus clos par plancher:", sum(r['clos_par_plancher'] for r in L))
print("tissus ou places = cotes non nes:", sum(r['T21_places_egal_cotes_non_nes'] for r in L))
print("tissus avec au moins une place a plancher incomplet:", sum(1 for r in L if r['places_plancher_incomplet'] > 0))
print("tissus avec au moins une place creant plus de 4 cellules:", sum(1 for r in L if any(int(k) > 4 for k in r['T23_cellules_creees_par_place'])))
