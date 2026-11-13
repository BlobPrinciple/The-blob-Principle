# C-127 bis — DEPENDANCE D1 (ChatGPT) : les coordonnees comobiles figees heritent-elles la regularite ? (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Meme regle que C-127 (regle U, etirement impose, naissance des que la division abaisse l'energie), mais seuls les sommets du BORD suivent l'etirement
#   impose ; tous les sommets interieurs sont libres et se relaxent (minimisation de Hooke) apres chaque pas d'etirement et chaque naissance.
# En coordonnees comobiles : ressorts de longueur naturelle 1/s, bord fixe. Pas d'etirement : 0,5 %. Germe de Kuhn. Arret a 512 puis 4 096 cellules.
# Une solution a cellule retournee arrete le bras (INCONCLUSIF).
# CRITERE : part du fil le plus long >= 90 %, qualite minimale >= 0,003, degre maximal <= 40, aucune inversion.
# PREDICTION ENREGISTREE : PASS a 512 cellules avec une trame proche de S1 mais deformee (qualite entre 0,01 et 0,03) ; incertain a 4 096.
import sys, itertools, math, json, numpy as np
from c120 import Mesh, SEEDS, vol6
target=int(sys.argv[1]); m=Mesh(SEEDS['Kuhn'],1.0,'U','X'); s=0.756; step=1.005; nb=0; nlong=0; log=[]
def setrest(s):
    m.l0=1.0/s
    for e in m.rest: m.rest[e]=m.l0
setrest(s)
while len(m.T)<target:
    E=m.inc(); cand=[(m.dE_insert(e,E),e) for e in E]; d,e=min(cand)
    if d<-1e-12*max(1.0,m.energy()):
        l=m.length(e); longall=all(l>=max(m.length(x) for x in itertools.combinations(sorted(t),2))-1e-9 for t in E[e]); nlong+=longall; nb+=1
        m.bisect(e,E=E); r=m.relax()
        if not r.get('ok',True):
            # relance : la convergence stricte peut manquer ; on n'arrete que sur inversion
            if not r.get('valid',True): print('ARRÊT : cellule retournée après la naissance',nb,'à',len(m.T),'cellules'); break
    else:
        s*=step; setrest(s); r=m.relax()
        if not r.get('valid',True): print('ARRÊT : cellule retournée pendant l\'étirement à s =',round(s,3),',',len(m.T),'cellules'); break
    if nb and nb%50==0 and (not log or log[-1][0]!=nb):
        mt=m.metrics(E=None); log.append((nb,len(m.T),s)); print(f'  naissances={nb} cellules={mt["N3"]} s={s:.3f} part du fil le plus long={100*nlong/nb:.1f} % degré max={mt["degmax"]} qmin={mt["qmin"]:.4f} Lmax/Lmin={mt["Lmax"]/mt["Lmin"]:.2f} inversions={mt["inversions"]}',flush=True)
mt=m.metrics(); deg={}
for a,b in m.rest: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
print(f'FINAL : cellules={mt["N3"]} sommets={mt["N0"]} naissances={nb} s={s:.3f} part du fil le plus long={100*nlong/max(1,nb):.1f} % degré max={mt["degmax"]} qmin={mt["qmin"]:.4f} Lmax/Lmin={mt["Lmax"]/mt["Lmin"]:.2f} inversions={mt["inversions"]} auto-intersections={mt["autointersections"]} E/arête (unités physiques)={mt["E"]*s*s/mt["N1"]:.4f}')
print('suite des degrés triée (10 plus grands) :',sorted(deg.values())[-10:],' histogramme :',sorted({d:list(deg.values()).count(d) for d in set(deg.values())}.items()))
