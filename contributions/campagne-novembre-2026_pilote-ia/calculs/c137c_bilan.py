import json, ast
res=json.load(open('c137c_phase2.json')); ok=[r for r in res if r['echec'] is None]; ko=[r for r in res if r['echec'] is not None]
print(f'Phase 2 : {len(ok)} règles conformes jusqu\'à la génération 12 sur {len(res)} ; échecs entre 7 et 12 : {sorted(set(tuple(r["echec"]) for r in ko))} ({len(ko)})')
cl={}
for r in ok: cl.setdefault(str(r['signature']),[]).append(r)
print('classes de complexes :',len(cl),'; tailles :',sorted((len(v) for v in cl.values()),reverse=True))
rows=[]
for sig,rs in cl.items():
    r=rs[0]; P=r['pal']; g=lambda k:P[str(k)] if str(k) in P else P[k]
    fd=[g(k)['fondateurs'] for k in (3,6,9,12)]; dm=[g(k)['degmax'] for k in (3,6,9,12)]; nv=[g(k)['comptes'][0] for k in (3,6,9,12)]
    ext=min(fd[3])>=2*min(fd[2])>=4*min(fd[1]) and min(fd[3])>1; etendu=(max(fd[3])>max(fd[0])); borne=(dm[3]==dm[2])
    wit=any(x['rule']==[[3,2,1],[0,1,2,3],[0,1,2,3]] for x in rs)
    Hs=set(str(g(k)['H']) for k in (3,6,9,12))
    rows.append(dict(n=len(rs),mots=sorted(set(''.join(map(str,x['rule'][0])) for x in rs)),fd12=fd[3],fd=[max(f) for f in fd],fdmin=[min(f) for f in fd],dm=dm,nv=nv,borne=borne,etendu=etendu,arc=g(12)['quatre_classes'],meme=g(12)['meme_classe'],temoin=wit,
                     qk=g(12)['qualite']['Kuhn'][0],pl=r['plus_long']['Kuhn'],liensmax=max(k for k,_ in r['liens']),H=Hs))
rows.sort(key=lambda x:(-x['borne'],-x['fdmin'][3],x['dm'][3]))
print('\nnb  mots                      porteurs à g=12  degré max (3,6,9,12)     distance entre fondateurs min–max (3,6,9,12)        degré borné  4 classes  liens/naissance max  qualité min (Kuhn)  part fil le plus long  témoin')
for x in rows:
    print(f"{x['n']:2d}  {','.join(x['mots'])[:24]:24s}  {x['nv'][3]:6d}           {str(x['dm']):24s} {str(list(zip(x['fdmin'],x['fd']))):50s} {str(x['borne']):11s}  {str(x['arc']):9s}  {x['liensmax']:6d}               {x['qk']:.4f}              {x['pl']:.3f}                {x['temoin']}")
print('\nH :',set(h for x in rows for h in x['H']))
b=[x for x in rows if x['borne']]; e=[x for x in rows if x['fdmin'][3]>=8]
print(f"classes à degré maximal stable entre g = 9 et g = 12 : {len(b)} ({sum(x['n'] for x in b)} règles) ; classes où TOUTES les distances entre fondateurs atteignent au moins 8 à g = 12 : {len(e)} ({sum(x['n'] for x in e)} règles)")
both=[x for x in rows if x['borne'] and x['fdmin'][3]>=8]; print('classes conformes, à degré stable ET étendues :',len(both),[ (x['n'],x['mots'],x['temoin']) for x in both])
