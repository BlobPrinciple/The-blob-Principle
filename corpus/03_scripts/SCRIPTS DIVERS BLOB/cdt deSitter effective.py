"""
CDT — DYNAMIQUE EFFECTIVE DES VOLUMES DE TRANCHES (minisuperspace), Python pur.
================================================================================
On simule la "pile de couches" : V_t = volume spatial de la tranche t.
N'EST PAS le plein simplicial (lui demande du C++ ; cf. JorenB/3d-cdt).

Action effective, volume total conserve exactement :
    S_eff = (1/Gamma)*[ sum_t (V_{t+1}-V_t)^2/(V_{t+1}+V_t)   (cinetique : lisse)
                      +  mu * sum_t V_t^alpha ]              (potentiel concave : concentre)

RESULTAT (apres avoir pousse le calcul au maximum)
--------------------------------------------------
1. MECANISME (robuste) : l'univers se condense en un blob de de Sitter sur une
   tige minimale. Profil ⟨V(t)⟩ ajuste cos^p avec R^2 ~ 0.9999-1.0000.

2. EXPOSANT (resolu) : profil classique = cos^q, q = 2/(1-alpha)
   - derivation continue (algebre verifiee) ;
   - CONFIRME numeriquement par le saddle classique (Gamma->0, sans bruit MC),
     extrapole en taille -> infinie :
            alpha=0.20 -> p_inf=2.57 (q=2.50)
            alpha=1/3  -> p_inf=2.99 (q=3.00)  <-- 4D de Sitter = cos^3 OK
            alpha=0.50 -> p_inf=4.01 (q=4.00)
     (valeur extrapolee sensible au bruit du fit cos^p, ~+/-0.1 ; donc
      p_inf(alpha=1/3) = 3.0 +/- 0.1, compatible cos^3 ; c'est la CONVERGENCE
      3.3 -> 3.0 et la relation q=2/(1-alpha) qui sont robustes, pas la 3e decimale.)
   - le "p~3.3" mesure par MC a petite taille etait un EFFET DE TAILLE FINIE
     (coherent avec le classique a largeur~32), pas une anomalie.

LIMITE / STATUT HONNETE
-----------------------
Modele EFFECTIF/REDUIT : le cos^3 SORT de l'action effective, elle-meme DERIVEE
de la CDT. C'est donc une validation de COHERENCE INTERNE du modele reduit, PAS
une derivation non-circulaire depuis la combinatoire nue. Ce dernier test = plein
simplicial (C++). Accroche Blob : le Blob, reduit a ses volumes de tranches,
donne-t-il une action effective du meme type ?
"""
import numpy as np

# ---------- 1) saddle classique : test propre de l'exposant (sans bruit) -------
def Sgrad(V, mu, alpha):
    Vp = np.roll(V, -1); Vm = np.roll(V, 1)
    S = ((V-Vp)**2/(V+Vp)).sum() + mu*(V**alpha).sum()
    db = -(Vm-V)*(3*Vm+V)/(Vm+V)**2          # ek(a,b)=(a-b)^2/(a+b), d/db
    da = (V-Vp)*(V+3*Vp)/(V+Vp)**2           #                        d/da
    return S, db + da + mu*alpha*V**(alpha-1)

def classical_profile(T, Vtot, alpha=1/3, mu=6.0, Vmin=2.0):
    from scipy.optimize import minimize
    base = Vtot - T*Vmin; t = np.arange(T)
    x0 = -((t-T/2)**2)/(2*(0.12*T)**2)        # logits gaussiens -> blob unique
    def fun(x):
        x = x - x.max(); e = np.exp(x); sm = e/e.sum(); V = Vmin + base*sm
        S, gV = Sgrad(V, mu, alpha)
        return S, base*sm*(gV - (gV*sm).sum())
    r = minimize(fun, x0, jac=True, method='L-BFGS-B',
                 options={'maxiter':40000,'maxfun':80000,'ftol':1e-14,'gtol':1e-10})
    x = r.x - r.x.max(); e = np.exp(x); sm = e/e.sum(); return Vmin + base*sm

# ---------- 2) MC "quantique" : ⟨V(t)⟩ a Gamma fini (volume conserve exact) ----
def simulate_mc(expo=1/3, T=80, V_tot=12000.0, V_min=2.0, Gamma=0.5, mu=6.0,
                n_sweeps=100000, burn=35000, meas_every=10, dV=5.0, seed=5):
    rng = np.random.default_rng(seed)
    t = np.arange(T); sb = np.clip(np.cos((t-T/2)*np.pi/(0.5*T))**3, 0, None)
    V = V_min + (V_tot-T*V_min)*sb/sb.sum(); inv = 1.0/Gamma
    def ek(lo, hi): return (lo-hi)**2/(lo+hi)
    prof = np.zeros(T); nc = 0
    for s in range(n_sweeps):
        for _ in range(T):
            i = int(rng.integers(T)); j = int(rng.integers(T))
            if j == i or j == (i+1)%T or j == (i-1)%T: continue
            a = dV*(rng.random()*2-1); ni = V[i]-a; nj = V[j]+a
            if ni < V_min or nj < V_min: continue
            im, ip, jm, jp = (i-1)%T, (i+1)%T, (j-1)%T, (j+1)%T
            old = ek(V[im],V[i])+ek(V[i],V[ip])+ek(V[jm],V[j])+ek(V[j],V[jp])+mu*(V[i]**expo+V[j]**expo)
            new = ek(V[im],ni)+ek(ni,V[ip])+ek(V[jm],nj)+ek(nj,V[jp])+mu*(ni**expo+nj**expo)
            dS = (new-old)*inv
            if dS <= 0 or rng.random() < np.exp(-dS): V[i] = ni; V[j] = nj
        if s >= burn and s % meas_every == 0:
            ang = 2*np.pi*np.arange(T)/T
            c = (np.arctan2((V*np.sin(ang)).sum(), (V*np.cos(ang)).sum())/(2*np.pi))*T
            prof += np.roll(V, int(round(T/2 - c))); nc += 1
    return prof/nc

def fit_cos_power(prof):
    T = len(prof); t = np.arange(T); y = prof - prof.min(); c = (t*y).sum()/y.sum(); best = None
    for W in np.arange(6, T/2, 0.5):
        x = (t-c)*np.pi/(2*W); inb = np.abs(x) < np.pi/2
        for p in np.linspace(1.0, 6.0, 501):
            sh = np.where(inb, np.cos(np.clip(x, -np.pi/2, np.pi/2))**p, 0.0); den = (sh*sh).sum()
            if den <= 0: continue
            A = (y*sh).sum()/den
            R2 = 1 - ((y-A*sh)**2).sum()/((y-y.mean())**2).sum()
            if best is None or R2 > best[1]: best = (p, R2, W)
    return best

if __name__ == "__main__":
    print("Saddle classique, alpha=1/3 (cible cos^3) : convergence en taille\n")
    W = []; P = []
    for Vtot in [1e4, 3e4, 1e5, 3e5, 1e6, 3e6, 1e7]:
        V = classical_profile(400, Vtot, alpha=1/3)
        p, R2, w = fit_cos_power(V); W.append(2*w); P.append(p)
        print(f"  Vtot={Vtot:.0e} | largeur~{2*w:5.0f} | p={p:.3f} | R2={R2:.5f}")
    W = np.array(W); P = np.array(P)
    pinf = np.linalg.lstsq(np.vstack([np.ones_like(W[-4:]), 1/W[-4:]]).T, P[-4:], rcond=None)[0][0]
    print(f"\n  extrapolation p(1/largeur -> 0) = {pinf:.3f}   (cos^3 = 3.000)")
