# C-134 (B) — confrontation aux mesures : 31 chronometres cosmiques (ages differentiels, sans modele cosmologique), table verifiee a la source
# (compilation reproduite dans A&A 683, A91, 2024, table 1 : Jimenez 2003, Simon 2005, Stern 2010, Chuang & Wang 2012, Moresco 2012, 2015, 2016, Zhang 2014).
# Erreurs traitees comme independantes (les covariances systematiques ne sont pas incluses : le test est indicatif, pas une analyse de precision).
import numpy as np, math
from scipy.stats import chi2
D=np.array([(0.09,69,12),(0.17,83,8),(0.27,77,14),(0.4,95,17),(0.9,117,23),(1.3,168,17),(1.43,177,18),(1.53,140,14),(1.75,202,40),(0.48,97,62),(0.88,90,40),
 (0.35,82.1,4.9),(0.179,75,4),(0.199,75,5),(0.352,83,14),(0.593,104,13),(0.68,92,8),(0.781,105,12),(0.875,125,17),(1.037,154,20),(0.07,69,19.6),(0.12,68.6,26.2),
 (0.2,72.9,29.6),(0.28,88.8,36.6),(1.363,160,33.6),(1.965,186.5,50.4),(0.3802,83,13.5),(0.4004,77,10.2),(0.4247,87.1,11.2),(0.4497,92.8,12.9),(0.4783,80.9,9)])
z,H,s=D.T; w=1/s**2
Hc=(w*H).sum()/w.sum(); c2=(w*(H-Hc)**2).sum(); n=len(z)
print(f'{n} mesures, z de {z.min()} à {z.max()}')
print(f'Cadence constante (H constant, meilleur ajustement {Hc:.1f} km/s/Mpc) : chi2 = {c2:.1f} pour {n-1} degrés de liberté ; probabilité {chi2.sf(c2,n-1):.1e}')
Hl=lambda z,H0=67.4,Om=0.315:H0*np.sqrt(Om*(1+z)**3+1-Om); c2l=(w*(H-Hl(z))**2).sum()
print(f'Référence ΛCDM (Planck 2018, aucun paramètre ajusté) : chi2 = {c2l:.1f} pour {n} degrés de liberté ; probabilité {chi2.sf(c2l,n):.2f}')
# loi de puissance a ~ t^p : H = p/t, H(z) = H0 (1+z)^(1/p) ; ajustement de H0 et p
best=None
for p in np.arange(0.3,3.01,0.01):
    f=(1+z)**(1/p); H0=(w*H*f).sum()/(w*f*f).sum(); c=(w*(H-H0*f)**2).sum()
    if best is None or c<best[0]: best=(c,p,H0)
print(f'Loi de puissance a ∝ t^p (deux paramètres ajustés) : p = {best[1]:.2f}, H0 = {best[2]:.1f}, chi2 = {best[0]:.1f} pour {n-2} degrés de liberté')
lo=z<0.5; hi=z>1.0
print(f'Moyennes pondérées : z < 0,5 : {(w[lo]*H[lo]).sum()/w[lo].sum():.1f} ± {w[lo].sum()**-.5:.1f} ; z > 1 : {(w[hi]*H[hi]).sum()/w[hi].sum():.1f} ± {w[hi].sum()**-.5:.1f} km/s/Mpc')
print(f'DESI DR2, forêt Lyman-alpha : D_H/r_d = 8,632 ± 0,101 à z = 2,33 → H·r_d = {299792.458/8.632:.0f} km/s ; avec r_d = 147,1 Mpc : H = {299792.458/8.632/147.1:.0f} km/s/Mpc')
# --- Lois de cadence sans coefficient nouveau, puis epreuve d'Alcock-Paczynski (rapport D_M/D_H a z = 2,33, independant de H0 et de r_d).
# DECLARATION : l'ajustement en loi de puissance ci-dessus (p = 0,98) a ete vu AVANT l'enonce de la branche K3 ; K3 n'est donc pas a l'aveugle sur les
# chronometres. L'epreuve d'Alcock-Paczynski, elle, a ete enoncee avant le calcul du rapport.
from scipy.integrate import quad
print('\nLois de cadence (un seul parametre, H0) sur les 31 chronometres :')
for nom,f in (('K1 cadence constante par cellule : a = exp(Ht)',lambda z:np.ones_like(z)),('K2 une naissance a la fois, debit global constant : a ∝ t^(1/3)',lambda z:(1+z)**3),
              ('K3 generations synchronisees a la vitesse de la lumiere : a ∝ t',lambda z:1+z)):
    F=f(z); H0=(w*H*F).sum()/(w*F*F).sum(); c=(w*(H-H0*F)**2).sum(); print(f'  {nom:70s}: H0 = {H0:6.1f} ; chi2 = {c:8.1f} / {n-1} ; probabilité {chi2.sf(c,n-1):.1e}')
zz=2.33; obs=39.32/8.600; sig=0.01*obs
E=lambda x:math.sqrt(0.315*(1+x)**3+0.685); lcdm=quad(lambda x:1/E(x),0,zz)[0]*E(zz)
k3=(1+zz)*math.log(1+zz); milne=(1+zz)*((1+zz)-1/(1+zz))/2; ds=zz*1.0   # de Sitter : D_M = z c/H, D_H = c/H
print(f'\nAlcock-Paczynski à z = 2,33 — mesure DESI DR2 (IV, juillet 2026) : D_M/D_H = 39,32 / 8,600 = {obs:.3f} ± {sig:.3f} (précision annoncée : 1 %)')
for nom,v in (('K1 de Sitter',ds),('K3 plat, a ∝ t',k3),('K3 ouvert (Milne), a ∝ t',milne),('Référence ΛCDM (Planck 2018)',lcdm)):
    print(f'  {nom:30s}: {v:.3f}  écart {(v-obs)/sig:+.1f} sigma')
