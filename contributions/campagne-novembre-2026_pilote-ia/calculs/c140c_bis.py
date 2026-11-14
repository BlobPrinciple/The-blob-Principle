# C-140c : mesures complementaires sur les memes trajectoires (aucune regle modifiee) : composantes connexes, cadence par tour.
import collections, itertools, c140c
src=open('c140c.py').read()
# on reutilise simulate en recuperant le graphe final par une petite variante : meme code, retour de N en plus
src=src.replace("return dict(marks=marks,renouvellements=renew,","return dict(graph={v:set(s) for v,s in N.items()},marks=marks,renouvellements=renew,").split("if __name__=='__main__':")[0]
ns={}; exec(src,ns); sim=ns['simulate']
def comps(N):
    seen=set(); out=[]
    for s in N:
        if s in seen: continue
        st=[s]; seen.add(s); n=0
        while st:
            u=st.pop(); n+=1
            for v in N[u]:
                if v not in seen: seen.add(v); st.append(v)
        out.append(n)
    return sorted(out,reverse=True)
for name,kw in (('W / F / E0 (file)',dict(rebirth='F')),('W / F / E0 synchrone',dict(rebirth='F',sync=True)),('Wmax / F',dict(rebirth='F',wear='Wmax')),('G0 / F',dict(rebirth='F',seed_graph='K1')),('W / R / E0',dict(rebirth='R')),('T0 / R',dict(rebirth='R',trap=False))):
    r=sim(**kw); c=comps(r['graph']); h=collections.Counter(c)
    print(f'{name:22s}: {len(r["graph"])} porteurs, {len(c)} composantes ; plus grande {c[0]} ; tailles (taille : nombre) {dict(sorted(h.items()))}' if len(h)<=12 else f'{name:22s}: {len(r["graph"])} porteurs, {len(c)} composantes ; plus grande {c[0]} ; médiane {c[len(c)//2]} ; isolés {h[1]}')
# cadence du bras principal par tranche de 128 evenements
r=sim(rebirth='F'); h=r['hist']; prev=(0,4,1)
print('cadence, bras principal (naissances par tentative, par tranche de 128 événements) :',[round((h[i][1]-(h[i-2][1] if i>=2 else 4))/128,2) for i in range(1,len(h),2)])
