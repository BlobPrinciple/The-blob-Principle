#!/usr/bin/env python3
"""X-31, RANG 2, VUE DU PARENT : LA DIVISION DU FIL. Programme independant : n'importe rien du laboratoire.
Prediction scellee : x31_cellule_et_arete_prediction.txt (SHA-256 d0bf1d15...912efc), clause B1.
Disques : vecteurs entiers de R^4 dans la base du germe (quatre disques tous lies). Produit <x, y> = 2 somme x_k y_k - (somme x)(somme y) ;
lies : produit -1. Cellule : trois disques tous lies. Ses deux cotes u et u' verifient u + u' = 2 (a + b + c).
 brut n   : regle a la lettre appliquee a la lettre, par force brute (toutes les cellules, tous les cotes), jusqu'au palier n.
 rapide n : la meme regle par les interstices ; comparee a la force brute sur les paliers communs ; puis tous les controles de la clause B1.
 reseau g : decompte des points du reseau triangulaire d'etendue au plus g + 1 (correction de T25), par enumeration et par la regle.
Claude, 27 novembre 2026."""
import itertools, json, sys, time
import numpy as np

GERME = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]

def prod(a, b): return 2 * sum(x * y for x, y in zip(a, b)) - sum(a) * sum(b)

def autre(a, b, c, u): return tuple(2 * (a[k] + b[k] + c[k]) - u[k] for k in range(4))

def brut(nmax):
    """S(n+1) = S(n) plus tous les cotes non nes des cellules nees de S(n). Rend {disque: palier}."""
    S = {u: 0 for u in GERME}
    for n in range(1, nmax + 1):
        L = sorted(S); V = {u: {v for v in L if v != u and prod(u, v) == -1} for u in L}; nouveaux = set()
        for a in L:
            for b in V[a]:
                if b <= a: continue
                for c in V[a] & V[b]:
                    if c <= b: continue
                    cotes = V[a] & V[b] & V[c]
                    assert 1 <= len(cotes) <= 2
                    for u in cotes:
                        u2 = autre(a, b, c, u)
                        if u2 not in S: nouveaux.add(u2)
        for u in nouveaux: S[u] = n
    return S

def rapide(nmax):
    """La meme regle, par les interstices : chaque disque ne dans la cellule {a, b, c} ouvre trois cellules, dont le cote ne est connu."""
    S = {u: 0 for u in GERME}; front = []
    for u in GERME:
        a, b, c = [v for v in GERME if v != u]; front.append((a, b, c, u))
    for n in range(1, nmax + 1):
        suiv = []
        for a, b, c, u in front:
            x = autre(a, b, c, u)
            assert x not in S
            S[x] = n; suiv += [(x, a, b, c), (x, b, c, a), (x, a, c, b)]
        front = suiv
    return S

def controles(S, nmax):
    L = sorted(S, key=lambda u: (S[u], u)); N = len(L); M = np.array(L, dtype=np.int64); s = M.sum(1); pal = np.array([S[u] for u in L])
    V = [None] * N; liens = 0; meme_palier = 0
    for d in range(0, N, 1000):
        G = 2 * M[d:d + 1000] @ M.T - np.outer(s[d:d + 1000], s); I, J = np.nonzero(G == -1)
        assert (G[np.arange(G.shape[0]), np.arange(d, d + G.shape[0])] == 1).all()
        assert ((G <= -1) | (G == 1)).all(), 'deux disques se chevauchent'
        vois = [[] for _ in range(G.shape[0])]
        for i, j in zip(I.tolist(), J.tolist()): vois[i].append(j)
        for i in range(G.shape[0]): V[d + i] = vois[i]
    c = dict(disques_controles=0, ages_controles=0, ecarts_au_doublement=0, nouveaux_voisins=0, nouveau_voisin_sans_fil_divise=0, fils_divises_deux_fois=0,
             fil_divise_en_retard=0, voisins_du_meme_palier_lies=0)
    for i in range(N):
        vi = V[i]; liens += len(vi); n0 = int(pal[i]); pv = pal[vi]
        meme_palier += int(((pv == n0) & (n0 >= 1)).sum())
        c['disques_controles'] += 1
        for g in range(0, nmax - n0 + 1):
            c['ages_controles'] += 1
            if int((pv <= n0 + g).sum()) != 3 * 2 ** g: c['ecarts_au_doublement'] += 1
        ens = set(vi); divises = set()
        for x in vi:
            if pal[x] <= n0: continue
            c['nouveaux_voisins'] += 1
            bouts = [q for q in V[x] if q in ens and pal[q] < pal[x]]
            if len(bouts) != 2 or bouts[1] not in V[bouts[0]]: c['nouveau_voisin_sans_fil_divise'] += 1; continue
            fil = (min(bouts), max(bouts))
            if fil in divises: c['fils_divises_deux_fois'] += 1
            divises.add(fil)
            if pal[x] != max(n0, int(pal[bouts[0]]), int(pal[bouts[1]])) + 1: c['fil_divise_en_retard'] += 1
        # deux voisins de p nes au meme palier, apres p, sont-ils lies ?
        for x in vi:
            if pal[x] <= n0: continue
            c['voisins_du_meme_palier_lies'] += sum(1 for q in V[x] if q in ens and pal[q] == pal[x])
    return dict(liens=liens // 2, liens_entre_disques_du_meme_palier_a_partir_de_1=meme_palier // 2, **c)

def partie_rapide(nmax):
    t0 = time.time(); S = rapide(nmax); nb = [sum(1 for u in S if S[u] <= n) for n in range(nmax + 1)]
    nbrut = min(nmax, 5); Sb = brut(nbrut); accord = all(Sb[u] == S[u] for u in Sb) and sum(1 for u in S if S[u] <= nbrut) == len(Sb)
    r = controles(S, nmax)
    print(json.dumps(dict(partie='B1', paliers=nmax, disques_par_palier=nb, regle_a_la_lettre_par_force_brute_jusqu_au_palier=nbrut,
                          accord_force_brute=accord, **r, duree_s=round(time.time() - t0, 1))), flush=True)

def partie_reseau(gmax):
    """Reseau triangulaire : points (i, j, k) entiers de somme 1. Regle : un point nait des que deux de ses voisins lies entre eux sont nes.
    Depart : (1,0,0), (0,1,0), (0,0,1). Compare le palier a l'etendue (max - min) moins un, et le decompte a (g+1)(g+2), plus un si g est multiple de 3."""
    t0 = time.time(); B = gmax + 3; pts = [(i, j, 1 - i - j) for i in range(-B, B + 1) for j in range(-B, B + 1) if abs(1 - i - j) <= B]
    ens = set(pts); pas = [(1, -1, 0), (-1, 1, 0), (1, 0, -1), (-1, 0, 1), (0, 1, -1), (0, -1, 1)]
    def vois(v): return [w for w in ((v[0] + d[0], v[1] + d[1], v[2] + d[2]) for d in pas) if w in ens]
    tau = {(1, 0, 0): 0, (0, 1, 0): 0, (0, 0, 1): 0}
    for n in range(1, gmax + 1):
        nouveaux = []
        for v in pts:
            if v in tau: continue
            W = [w for w in vois(v) if w in tau]
            if any(sum(abs(a - b) for a, b in zip(w1, w2)) == 2 for w1, w2 in itertools.combinations(W, 2)): nouveaux.append(v)
        for v in nouveaux: tau[v] = n
    ecarts = sum(1 for v in tau if tau[v] != max(v) - min(v) - 1)
    oublies = sum(1 for v in pts if v not in tau and max(v) - min(v) - 1 <= gmax)
    compte = [sum(1 for v in tau if tau[v] <= g) for g in range(gmax + 1)]
    formule = [(g + 1) * (g + 2) + (1 if g % 3 == 0 else 0) for g in range(gmax + 1)]
    print(json.dumps(dict(partie='reseau', gmax=gmax, palier_different_de_l_etendue_moins_un=ecarts, points_oublies=oublies,
                          nombre_de_points_par_palier_cumule=compte[:12], accord_avec_la_formule_jusqu_a_gmax=(compte == formule),
                          duree_s=round(time.time() - t0, 1))), flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'rapide': partie_rapide(int(sys.argv[2]))
    elif sys.argv[1] == 'reseau': partie_reseau(int(sys.argv[2]))
    elif sys.argv[1] == 'brut':
        S = brut(int(sys.argv[2])); print(json.dumps(dict(partie='brut', disques_par_palier=[sum(1 for u in S if S[u] <= n) for n in range(int(sys.argv[2]) + 1)])))
