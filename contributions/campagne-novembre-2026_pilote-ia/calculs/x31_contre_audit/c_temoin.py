# Temoins : tissus NON clos par plancher ou T21 / T22 echouent.
import pickle, random, itertools, json
from noyau import *
import b_tissus as bt

d = pickle.load(open("/home/claude/audit_x31/rang3_S6.pkl", "rb"))
palier, tuile_de = d["palier"], d["tuile_de"]
G5 = germe(5); GT = frozenset(G5)
pool = sorted(u for u in palier if 2 <= palier[u] <= 4)

def etudie(born):
    B = set(born)
    adj = {u: {v for v in born if v != u and ip(u, v) == -1} for u in born}
    cells = set()
    for a in born:
        for b, c, e in itertools.combinations(sorted(adj[a]), 3):
            if c in adj[b] and e in adj[b] and e in adj[c]:
                cells.add(frozenset((a, b, c, e)))
    clos = all(bt.parents(u, tuile_de[u]) <= B for u in born)
    Q = set(); sans = []
    for c in cells:
        u, v = cotes(list(c))
        if u not in B and v not in B: sans.append(sorted(c))
        for w in (u, v):
            if w not in B: Q.add(w)
    ent, nonent, libres, dep, quads = bt.places_directes(born, B, adj)
    return clos, ent, Q, sans, libres

rng = random.Random(7)
trouve21 = trouve22 = 0; essais = 0; ex21 = ex22 = None
while (trouve21 < 5 or trouve22 < 5) and essais < 400:
    essais += 1
    born = list(G5) + rng.sample(pool, rng.randint(3, 12))
    clos, ent, Q, sans, libres = etudie(born)
    if clos: continue
    if ent != Q:
        trouve21 += 1
        if ex21 is None: ex21 = {"tissu": born, "places_pas_cote": sorted(ent - Q), "cotes_pas_place": sorted(Q - ent), "places_non_entieres_libres": libres}
    if sans:
        trouve22 += 1
        if ex22 is None: ex22 = {"tissu": born, "cellules_sans_cote_ne": sans}
print("essais", essais, "tissus non clos avec T21 en defaut", trouve21, "avec T22 en defaut", trouve22)
print("exemple T21:", json.dumps(ex21))
print("exemple T22:", json.dumps(ex22))
# verification de l'exemple T21 : la place est liee a un ne et a trois voisins nes, independants, ne chevauche rien, n'est cote d'aucune cellule nee
if ex21 and ex21["places_pas_cote"]:
    x = tuple(ex21["places_pas_cote"][0]); born = [tuple(u) for u in ex21["tissu"]]
    nb = [b for b in born if ip(x, b) == -1]
    print("place", x, "constituant:", appartient(x), "contacts nes:", nb, "chevauche un ne:", any(ip(x, b) > -1 for b in born))
    print("parents de ses contacts nes non nes:", [[list(q) for q in bt.parents(b, tuile_de[b]) if q not in set(born)] for b in nb])
