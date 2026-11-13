exec(open('c81_32.py').read().split('g=1.5; F=')[0])
from fractions import Fraction
g=1.5
for ngen in (0,1):
  tp,tm,s,mir=grow(1,ngen,0); cells=R0(tp+tm,s); P,idx=kern(cells,s,g)
  x=P[idx[(100,)],idx[(100,)]]; print(ngen, x, Fraction(x).limit_denominator(1000))
