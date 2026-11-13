import random, collections, math
random.seed(7)
# 1) Polya : 1 porteur +, 1 porteur -, chaque porteur se divise au meme taux
N=12; c=collections.Counter()
for _ in range(200000):
    p,n=1,1
    while p+n<N:
        if random.random()<p/(p+n): p+=1
        else: n+=1
    c[p]+=1
print("Polya N=12, P(N+=k) :",[round(c[k]/200000,3) for k in range(1,N)], " attendu 1/11 =",round(1/11,3))
# 2) Naissance sur place dans un tetraedre (subdivision stellaire aleatoire) : distance moyenne vs N
def stacked(N):
    adj=collections.defaultdict(set); tets=[(0,1,2,3)]
    for a in range(4):
        for b in range(a+1,4): adj[a].add(b); adj[b].add(a)
    for v in range(4,N):
        t=tets.pop(random.randrange(len(tets)))
        for u in t: adj[u].add(v); adj[v].add(u)
        for i in range(4): tets.append(tuple(x for j,x in enumerate(t) if j!=i)+(v,))
    return adj
def meandist(adj,n,samples=40):
    tot=cnt=0
    for s in random.sample(range(n),samples):
        d={s:0}; q=[s]
        for x in q:
            for y in adj[x]:
                if y not in d: d[y]=d[x]+1; q.append(y)
        tot+=sum(d.values()); cnt+=len(d)-1
    return tot/cnt
for n in (500,2000,8000,32000):
    print("naissance sur place N=%6d  distance moyenne=%.2f  ln N=%.2f  N^(1/3)=%.1f"%(n,meandist(stacked(n),n),math.log(n),n**(1/3)))
