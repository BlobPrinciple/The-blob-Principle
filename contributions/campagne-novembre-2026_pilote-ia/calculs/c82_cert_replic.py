exec(open('c82_cycle.py').read().split('for (k,seed')[0])
from fractions import Fraction
# lignee + : a..e = 1..5 (signe +1), miroir 11..15 (signe -1), sites neutres f=100, q=101
s={**{v:1 for v in range(1,6)},**{v:-1 for v in range(11,16)},100:0,101:0}
m=lambda T:tuple(sorted((x+10 if x<100 else x) for x in T))
A=[(1,2,3,4),(1,2,3,5),(1,2,4,100),(1,2,5,101)]
B=[(1,2,4,100),(1,2,5,101),(1,2,4,5),(1,3,4,5),(2,3,4,5)]   # 2->3 sur [abcd]+[abce] : arete [de] creee
KA=R0(A+[m(t) for t in A],s); KB=R0(B+[m(t) for t in B],s); sites=[100,101]
print('dim ker A,B =',round(np.trace(kern(KA,s,g)[0])),round(np.trace(kern(KB,s,g)[0])))
Mup=transport(KA,s,KB,sites); Mdn=transport(KB,s,KA,sites); C=Mdn@Mup
print('M(2->3)=',np.round(Mup,12).tolist()); print('cycle=',[[str(Fraction(x).limit_denominator(100000)) for x in r] for r in C])
print('spectre=',[str(Fraction(x).limit_denominator(100000)) for x in np.linalg.eigvals(C).real])
