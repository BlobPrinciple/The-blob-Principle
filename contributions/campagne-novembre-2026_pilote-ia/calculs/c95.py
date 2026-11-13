# Audit C-95 (ChatGPT) et C-96 exploratoire : fuites des modes de site, recouvrement au fil des generations.
exec(open('c94c.py').read().split("worst=0")[0])
from fractions import Fraction as Fr
fr=lambda x:Fr(x).limit_denominator(5000)
for g in (1.5,):
  sn=chain(2,0,1,g)
  A,B=sn[0],sn[1]; S=Smat(A,B); G0=A[4].T@A[4]; G1=B[4].T@B[4]
  ev=np.linalg.eigvals(np.linalg.solve(G0,G1)).real
  print('k=2 g=1.5, 1re naissance : facteurs de conservation (valeurs propres généralisées G1/G0) :',[str(fr(x)) for x in sorted(ev,reverse=True)])
  R=S@A[4]-B[4]; ov=R[:,0]@R[:,1]/np.linalg.norm(R[:,0])/np.linalg.norm(R[:,1]); print('  recouvrement des fuites r1,r2 :',str(fr(ov)),round(ov,5))
# C-96 : fuites cumulees r_i(n) = (S_n...S_1 v_i(0)) - v_i(n) ; recouvrement normalise au fil des generations
print('C-96 : recouvrement normalisé des fuites cumulées des deux sites (k=2)')
for g in (0.5,1.5,4.0):
  rows=[]
  for seed in range(8):
    sn=chain(2,seed,8,g); X=sn[0][4].copy(); r=[]
    for n in range(1,len(sn)):
      X=Smat(sn[n-1],sn[n])@X; Rn=X-sn[n][4]
      r.append(abs(Rn[:,0]@Rn[:,1])/np.linalg.norm(Rn[:,0])/np.linalg.norm(Rn[:,1]))
    rows.append(r)
  rows=np.array(rows); print(f'  g={g}: générations 1→8 :',np.round(rows.mean(0),4).tolist(),' max à n=8 :',round(rows[:,-1].max(),4))
