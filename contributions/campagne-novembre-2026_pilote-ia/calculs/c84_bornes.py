# Verification des bornes de Loewner proposees par ChatGPT : (I+2D/g^2)^-1 <= G <= (I+2D/(g^2+k))^-1
exec(open('c81_32.py').read().split('g=1.5; F=')[0])
viol_lo=viol_hi=0; n=0; worst=[]
for g in (0.5,1.5,4.0):
  for k in (1,2,3):
    for seed in range(6):
      for ngen in range(0,6):
        tp,tm,s,mir=grow(k,ngen,seed); F=[100+i for i in range(k)]
        cells=R0(tp+tm,s); P,idx=kern(cells,s,g); V=np.array([P[:,idx[(c,)]] for c in F]).T; G=V.T@V
        d=[sum(1 for c in cells if len(c)==2 and f in c and s[[x for x in c if x!=f][0]]>0) for f in F]
        D=np.diag(d); lo=np.linalg.inv(np.eye(k)+2*D/g**2); hi=np.linalg.inv(np.eye(k)+2*D/(g**2+k))
        e1=np.linalg.eigvalsh(G-lo).min(); e2=np.linalg.eigvalsh(hi-G).min(); n+=1
        viol_lo+=e1<-1e-12; viol_hi+=e2<-1e-12
        if e1<-1e-12 or e2<-1e-12: worst.append((g,k,seed,ngen,d,round(e1,5),round(e2,5)))
print('cas',n,'violations borne inf',viol_lo,'borne sup',viol_hi); print(worst[:8])
