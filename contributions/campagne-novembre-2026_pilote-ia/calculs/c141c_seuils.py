# C-141c / PR-1, section F : mesures aux premiers passages à 1 024 et 8 192 porteurs (bras séquentiels), même moteur que c141c.py
import c141c, json
from statistics import median
out={}
for name,kw in (('C',dict(mode='C')),('A',dict(mode='A')),('T1',dict(mode='C',support='one'))):
    S=c141c.Sim(**kw); todo=[1024,8192]; out[name]={}
    while todo and S.n<65536:
        S.attempt()
        if len(S.N)==todo[0]:
            m=c141c.measure(S.N,S.born,True); m['n']=S.n; out[name][todo.pop(0)]=m
            d=sorted(m['distances'].values())
            print(f"[{name}] premier passage V={m['V']} à la tentative {S.n} : T={m['T']} chi={m['chi']} deg max/med/q95={m['deg_max']}/{m['deg_med']}/{m['deg_q95']} "
                  f"distances={list(m['distances'].values())} médiane={median(d)} entourages={m['entourages']} top3={m['top10'][:3]}",flush=True)
    if len(out[name])==2:
        a,b=out[name][1024],out[name][8192]
        print(f"   {name} : degré maximal {a['deg_max']} -> {b['deg_max']} ; six distances strictement croissantes : {all(b['distances'][k]>a['distances'][k] for k in a['distances'])} ; "
              f"rapport des distances médianes : {b['d_med']/a['d_med']:.3f} (référence 2)")
json.dump(out,open('c141c_seuils.json','w'),default=str)
