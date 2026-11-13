exec(open('c92b.py').read().split("I3=np.eye(3); Ref")[0])
for ngen in (15,25,40):
    a=[chi2(*history(seed,ngen),np.eye(3)) for seed in range(16)]
    print(ngen, f'{np.mean(a):+.3f} ± {np.std(a)/4:.3f}')
