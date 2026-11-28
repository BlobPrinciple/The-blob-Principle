# Vérification de pilote (hors dépôt) : classes d'holonomie Z3 d'un tétraèdre.
# a(x,y) antisymétrique mod 3 ; h(u,v,w) = a(u,v)+a(v,w)+a(w,u) mod 3.
import itertools, math, random
V=[0,1,2,3]; E=[(i,j) for i in V for j in V if i<j]
def mk(vals):
    a={}
    for (i,j),v in zip(E,vals):
        a[(i,j)]=v%3; a[(j,i)]=(-v)%3
    return a
def h(a,u,v,w): return (a[(u,v)]+a[(v,w)]+a[(w,u)])%3
def faces_sorted(perm):
    # faces orientées par ordre croissant des étiquettes APRÈS renumérotation perm
    inv={perm[i]:i for i in V}
    out=[]
    for tri in itertools.combinations(V,3):          # étiquettes nouvelles, croissantes
        out.append(tuple(inv[x] for x in tri))       # sommets d'origine, dans cet ordre
    return out
idp=(0,1,2,3)
signed_viol=0; tot_counts=[0,0,0]; coh=0; coh_class=[0,0,0]; noninv=0; noninv_coh=0
perms=list(itertools.permutations(V))
for vals in itertools.product(range(3),repeat=6):
    a=mk(vals)
    f=faces_sorted(idp)                              # (0,1,2),(0,1,3),(0,2,3),(1,2,3)
    hs=[h(a,*t) for t in f]
    signed=(h(a,1,2,3)-h(a,0,2,3)+h(a,0,1,3)-h(a,0,1,2))%3
    signed_viol+= (signed!=0)
    T=sum(hs)%3; tot_counts[T]+=1
    c=all(x==0 for x in hs); coh+=c
    if c: coh_class[T]+=1
    classes={sum(h(a,*t) for t in faces_sorted(p))%3 for p in perms}
    if len(classes)>1:
        noninv+=1
        if c: noninv_coh+=1
print("somme signée non nulle :",signed_viol,"/ 729")
print("classes (somme non signée, étiquettes croissantes) :",tot_counts)
print("tétraèdres à 4 faces triviales :",coh,"répartis par classe :",coh_class)
print("configurations dont la classe change selon la numérotation des sommets :",noninv,"/ 729 ; parmi les cohérentes :",noninv_coh)
# corrélation générique laplacien / fonction sur un graphe aléatoire régulier-ish
random.seed(1)
import statistics as st
def corr(x,y):
    mx,my=st.mean(x),st.mean(y); sx,sy=st.pstdev(x),st.pstdev(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)*sx*sy)
n=2000; deg=6; nb=[set() for _ in range(n)]
while sum(len(s) for s in nb)<n*deg:
    i,j=random.randrange(n),random.randrange(n)
    if i!=j: nb[i].add(j); nb[j].add(i)
x=[random.gauss(0,1) for _ in range(n)]
Lx=[len(nb[i])*x[i]-sum(x[j] for j in nb[i]) for i in range(n)]
print("corr(L x, x) pour un bruit blanc sur graphe aléatoire de degré moyen 6 : %.3f  (attendu ~ %.3f)"%(corr(Lx,x),math.sqrt(deg/(deg+1))))
# valeur moyenne du commutateur [X,L] sur un état réel
xs=[random.random() for _ in range(n)]
psi=[abs(random.gauss(0,1)) for _ in range(n)]
def L(v): return [len(nb[i])*v[i]-sum(v[j] for j in nb[i]) for i in range(n)]
XLpsi=[xs[i]*y for i,y in enumerate(L(psi))]
LXpsi=L([xs[i]*psi[i] for i in range(n)])
print("<psi|[X,L]|psi> (psi réel positif) : %.2e"%sum(psi[i]*(XLpsi[i]-LXpsi[i]) for i in range(n)))
