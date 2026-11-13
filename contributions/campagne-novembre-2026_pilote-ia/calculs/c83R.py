# C-83-R : audit deterministe de la reversibilite (demande ChatGPT).
exec(open('c83.py').read().split("#MAIN")[0])
k=2; g=1.5; F=[100,101]
tp,tm,s,mir=init(k); nv=200; rng=random.Random(0)
for _ in range(3):
    m=('B',tp[rng.randrange(len(tp))]); tp,tm,s,mir,nv=apply(m,tp,tm,s,mir,nv)
def adm(tp,tm,s,mir,nv):
    out=[]
    for m in moves(tp,s,F):
        if m[0]=='B': continue
        st=apply(m,tp,tm,s,mir,nv); J=info(st[0],st[1],st[2],g,F)
        ok=J[6]==k and not any(len(c)>1 and pol(c,st[2])==0 for c in J[0])
        out.append((m,ok,st))
    return out
cur=(tp,tm,s,mir,nv); path=[]
rng=random.Random(0)
for step in range(200):
    A=adm(*cur); okm=[x for x in A if x[1]]
    if not okm:
        print('BLOQUE au pas',step,'; mouvements listés:',[(m,ok) for m,ok,_ in A]); 
        pm,prev=path[-1]; print('dernier mouvement:',pm)
        # inverse attendu
        if pm[0]=='23': f,x,y=pm[1]; print('inverse attendu : 32 sur arete',tuple(sorted((x,y))))
        else: print('inverse attendu : 23 recreant les tetras', pm[1])
        tpc=cur[0]; e=pm[1] if pm[0]=='32' else tuple(sorted(pm[1][1:]))
        if pm[0]=='23':
            around=[t for t in tpc if set(e)<=set(t)]; print('tetras autour',around)
        else:
            around=[t for t in tpc if set(e)<=set(t)]; print('tetras contenant l arete supprimee (doit etre 0):',around)
            # chercher la face partagee
            link=None
        break
    m,_,st=okm[rng.randrange(len(okm))]; path.append((m,cur)); cur=st[:5]
prev=path[-1][1][0]; e=(2,204)
around=[t for t in prev if set(e)<=set(t)]; link=sorted(set().union(*map(set,around))-set(e))
print('lien',link,'; tetras contenant deja la face-lien AVANT le 3->2 :',[t for t in prev if set(link)<=set(t)])
print('apres :',[t for t in cur[0] if set(link)<=set(t)])
# frequence de violations sur toute la marche
viol=0;tot=0
for m,c in path:
    if m[0]=='32':
        tot+=1; ar=[t for t in c[0] if set(m[1])<=set(t)]; L=set().union(*map(set,ar))-set(m[1])
        viol+= any(set(L)<=set(t) and not set(m[1])&set(t) for t in c[0])
print('3->2 effectués',tot,'dont non-variétés (face-lien déjà présente)',viol)
