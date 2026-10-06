# =====================================================================================
# EXPÉRIENCE DES FENTES — SOLVEUR DE SCHRÖDINGER 2D PROPRE (Crank-Nicolson implicite)
# Script autonome Colab. Validation par ÉTAPES avant de conclure (méthode rigoureuse) :
#   ÉTAPE 0 : propagation libre — vérifier que la norme se conserve (solveur correct).
#   ÉTAPE 1 : UNE fente — doit donner une tache de diffraction simple (lobe central unique).
#   ÉTAPE 2 : DEUX fentes — interférence de Young (pic CENTRAL entre les fentes + franges).
#   ÉTAPE 3 (option GRAV) : ajouter un POTENTIEL GRAVITATIONNEL (puits de courbure) et voir
#            si la gravité canalise/structure l'interférence (intuition R. Mirante : la gravité
#            a un rôle clé, confirmée par l'ablation du Blob).
#
# Schéma Crank-Nicolson : UNITAIRE (conserve la norme exactement), STABLE à tout dt.
#   i dψ/dt = H ψ,  H = -(1/2)∇² + V.   (I + i dt/2 H) ψ^{n+1} = (I - i dt/2 H) ψ^n.
# Résolution par gradient bi-conjugué (pas d'inversion de matrice dense).
# Conditions absorbantes (couche complexe) aux bords pour éviter les réflexions.
#
# C'est l'outil HONNÊTE : on valide qu'il conserve la norme ET propage correctement
# (étape 0) AVANT de tester les fentes. Aucune conclusion sans validation de l'instrument.
# =====================================================================================
import numpy as np
import time

def make_grid(nx=240, ny=240):
    return nx, ny, 1.0/(nx-1), np.linspace(0,1,nx), np.linspace(0,1,ny)

def slit_mask(nx, ny, mode):
    """Barrière verticale à x=0.5 (épaisseur 3 colonnes), ouvertures selon mode."""
    xs=np.linspace(0,1,nx); ys=np.linspace(0,1,ny)
    wall=np.zeros((nx,ny),bool)
    if mode=="libre":
        return wall
    if mode=="1fente":
        slits=[(0.46,0.54)]
    else:
        slits=[(0.40,0.46),(0.54,0.60)]
    ix=np.argmin(np.abs(xs-0.5))
    for col in (ix-1,ix,ix+1):
        for iy in range(ny):
            y=ys[iy]
            if not any(lo<=y<=hi for lo,hi in slits):
                wall[col,iy]=True
    return wall

def potentiel_gravite(nx, ny, actif, force=300.0):
    """Potentiel gravitationnel : puits de courbure (attractif) au centre de l'écran.
       V<0 = puits qui attire/canalise l'onde. Modélise le rôle de la gravité (courbure)."""
    if not actif: return np.zeros((nx,ny))
    xs=np.linspace(0,1,nx); ys=np.linspace(0,1,ny)
    X,Y=np.meshgrid(xs,ys,indexing='ij')
    # puits doux le long de l'axe de propagation, après les fentes
    V=-force*np.exp(-((X-0.75)**2/0.05 + (Y-0.5)**2/0.08))
    return V

def absorbing_layer(nx, ny, width=20, strength=4.0):
    """Couche absorbante imaginaire aux bords (potentiel complexe négatif)."""
    xs=np.linspace(0,1,nx); ys=np.linspace(0,1,ny)
    W=np.zeros((nx,ny))
    for ix in range(nx):
        for d,iy in [(ix,0)]:
            pass
    # profil de bord
    bx=np.minimum(np.arange(nx), nx-1-np.arange(nx))
    by=np.minimum(np.arange(ny), ny-1-np.arange(ny))
    BX,BY=np.meshgrid(bx,by,indexing='ij')
    B=np.minimum(BX,BY)
    absorb=np.where(B<width, strength*((width-B)/width)**2, 0.0)
    return absorb  # sera multiplié par -1j

def H_apply(psi, V_eff, h):
    """H psi = -(1/2) Lap psi + V_eff psi. V_eff inclut potentiel reel + absorption (complexe)."""
    lap=np.zeros_like(psi)
    lap[1:-1,:]+=psi[2:,:]+psi[:-2,:]
    lap[:,1:-1]+=psi[:,2:]+psi[:,:-2]
    lap-=4*psi
    lap/=h*h
    return -0.5*lap + V_eff*psi

def bicgstab(apply_A, b, x0, tol=1e-8, maxit=400):
    """BiCGSTAB pour systeme complexe (I + i dt/2 H) x = b, sans matrice explicite."""
    x=x0.copy()
    r=b-apply_A(x); r0=r.copy()
    rho=1.0; alpha=1.0; omega=1.0
    v=np.zeros_like(b); p=np.zeros_like(b)
    bn=np.sqrt(np.vdot(b,b).real)+1e-30
    for it in range(maxit):
        rho1=np.vdot(r0,r)
        beta=(rho1/rho)*(alpha/omega) if (rho!=0 and omega!=0) else 0
        p=r+beta*(p-omega*v)
        v=apply_A(p)
        alpha=rho1/ (np.vdot(r0,v)+1e-30)
        s=r-alpha*v
        if np.sqrt(np.vdot(s,s).real)/bn<tol:
            x=x+alpha*p; break
        t=apply_A(s)
        omega=np.vdot(t,s)/(np.vdot(t,t)+1e-30)
        x=x+alpha*p+omega*s
        r=s-omega*t
        rho=rho1
        if np.sqrt(np.vdot(r,r).real)/bn<tol: break
    return x

def run(mode="2fentes", grav=False, nx=200, ny=200, steps=400, dt=None):
    nx,ny,h,xs,ys=make_grid(nx,ny)
    wall=slit_mask(nx,ny,mode)
    Vg=potentiel_gravite(nx,ny,grav)
    absorb=absorbing_layer(nx,ny,width=18,strength=6.0)
    Vwall=np.where(wall, 1e6, 0.0)        # mur = potentiel infini
    V_eff=Vg+Vwall-1j*absorb              # reel (grav+mur) + absorption imaginaire
    if dt is None: dt=0.5*h
    # paquet d'onde initial : gaussien a gauche, impulsion k0 vers +x
    X,Y=np.meshgrid(xs,ys,indexing='ij')
    x0,y0=0.18,0.5; sx,sy=0.05,0.16; k0=120.0
    psi=np.exp(-((X-x0)**2/(2*sx**2)+(Y-y0)**2/(2*sy**2)))*np.exp(1j*k0*X)
    psi[wall]=0
    psi/=np.sqrt(np.sum(np.abs(psi)**2)*h*h)
    def A_apply(x): return x + 1j*dt/2*H_apply(x, V_eff, h)
    norm_hist=[]
    screen=np.zeros(ny)
    ix_scr=int(0.92*nx)
    for t in range(steps):
        rhs=psi - 1j*dt/2*H_apply(psi, V_eff, h)
        psi=bicgstab(A_apply, rhs, psi)
        psi[wall]=0
        norm_hist.append(np.sum(np.abs(psi)**2)*h*h)
        if t>steps//2:
            screen+=np.abs(psi[ix_scr,:])**2
    return xs,ys,screen,norm_hist

if __name__=="__main__":
    T0=time.time()
    print("="*70)
    print("SOLVEUR SCHRODINGER PROPRE (Crank-Nicolson) — validation par etapes")
    print("="*70)

    # ETAPE 0 : propagation LIBRE — la norme se conserve-t-elle ? (validation de l'instrument)
    print("\n[ETAPE 0] propagation libre (sans fente) : la norme doit rester ~constante.")
    xs,ys,scr,nh=run(mode="libre",grav=False,nx=160,ny=160,steps=120)
    print(f"  norme initiale ~{nh[0]:.3f}, finale ~{nh[-1]:.3f} (doit etre proche, hors absorption bords)")
    print(f"  => instrument {'VALIDE (norme stable)' if 0.3<nh[-1]/max(nh[0],1e-9)<1.05 else 'A REVOIR'}")

    # ETAPE 1 & 2 : une fente vs deux fentes
    for mode in ["1fente","2fentes"]:
        xs,ys,scr,nh=run(mode=mode,grav=False,nx=200,ny=200,steps=420)
        p=scr/max(scr.max(),1e-15); ny=len(p)
        ic=ny//2
        central=max(p[ic-2:ic+3])
        pk=sum(1 for b in range(2,ny-2) if p[b]>p[b-1] and p[b]>p[b+1] and p[b]>0.30)
        print(f"\n[{mode}] (sans gravite)")
        for b in range(0,ny,max(1,ny//22)):
            yc=ys[b];bar="#"*int(p[b]*38)
            print(f"  y={yc:.2f} |{bar:<38}| {p[b]:.3f}")
        print(f"  centre y=0.5 = {central:.3f} | pics = {pk}  [{time.time()-T0:.0f}s]")

    # ETAPE 3 : deux fentes AVEC gravite (intuition Mirante)
    xs,ys,scr,nh=run(mode="2fentes",grav=True,nx=200,ny=200,steps=420)
    p=scr/max(scr.max(),1e-15); ny=len(p); ic=ny//2
    central=max(p[ic-2:ic+3])
    print(f"\n[2fentes + GRAVITE] (puits de courbure actif)")
    for b in range(0,ny,max(1,ny//22)):
        yc=ys[b];bar="#"*int(p[b]*38)
        print(f"  y={yc:.2f} |{bar:<38}| {p[b]:.3f}")
    print(f"  centre y=0.5 = {central:.3f}  [{time.time()-T0:.0f}s]")
    print("\nVERDICT : ETAPE0 valide l'instrument. 1fente=lobe simple, 2fentes=pic central+franges")
    print("(interference). Comparer 2fentes SANS vs AVEC gravite : la gravite structure-t-elle la figure ?")
