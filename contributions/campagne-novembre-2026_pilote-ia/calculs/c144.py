# C-144 / PR-1 — LE LIANT PEUT-IL SE DISSOCIER PAR TRANSFERT A SES DEGRES INTERNES, SANS CONVERSION THERMIQUE IMPOSEE ?
# Protocole FIGE par ChatGPT (12 nov. 2026, fil principal, sha256 315399b02ad6f2ecbb9de3cd127ecedfb14caf75aa21ad539ee8df1e69024329, recalculée par Claude).
# Modèle : tétraèdre régulier, 4 masses 1, r0 = 1, D = 1, k = 2, L = sqrt(6D/k) = sqrt 3, r_c = r0 + L, u = (r - r0)/L.
#   U_c : k (r-r0)^2 / 2 (r < r0) ; D (3u^2 - 2u^3) (r0 <= r < r_c) ; D (r >= r_c).   h : r - r0 ; L u (1-u)^2 ; 0.
#   V_e = U_c(r_e) + somme_a (w_a^2 / 2) [y_ea - alpha h(r_e)]^2 ; y'' + nu y' + w_a^2 [y - alpha h] = 0 ; Q_ext' = nu somme y'^2. Aucun amortisseur radial.
#   Source : impulsions de C-142B / C-143 (porteur 0 contre ses trois voisins, travail exact W = P c), aux instants j c T0, j = 0..N-1, N = 24/c ; puis 4 T0 sans choc.
#   Régimes : B0 (alpha 0) ; H1 (m 1, w sqrt2) ; H3 (w 1, sqrt2, 2) ; X1, X3 (idem, nu 0,04) ; DET3 (w 2, 2 sqrt2, 4). P = 0, 1/48, 1/4, 1/2, 1 ; c = 1/2, 4/5, 1, 6/5.
#   120 trajectoires + 24 témoins de perturbation (P 1/4, 1/2 ; c 4/5, 1 ; B0, H3, X3 ; un sommet de base déplacé de +/- 1e-8).
#   Séparation persistante : r_e >= r_c sur toute la fenêtre [24 T0, 28 T0], avec un franchissement sortant antérieur.
#   Solveurs : DOP853 (rtol 1e-10, atol 1e-12), RK4 à T0/512 et T0/1024 ; verdicts différents, ou résidu > 1e-6 (relatif ou absolu) : INDETERMINE.
# PRECISIONS D'EXECUTION (Claude, déclarées avant calcul) :
#  - tous les chocs programmés sont délivrés (aucun lien n'est effacé, donc aucun arrêt d'injection) ; l'impulsion suit les directions actuelles des trois liens du porteur 0 ;
#  - B0 est exécuté sans oscillateur (équivalent, dit le protocole, à des oscillateurs au repos découplés) ;
#  - intégration par segments entre instants de choc et points de contrôle ; RK4 : pas égaux par segment, au plus égaux à la cible ; franchissements RK4 repérés par
#    changement de signe de r - r_c entre deux pas, instant interpolé linéairement ; DOP853 : événements non terminaux ;
#  - statut d'une trajectoire : LIE (aucun franchissement), TRANSITOIRE (franchissement sans séparation persistante), PERSISTANTE (au moins un lien) ; l'accord des
#    solveurs porte sur le statut ET sur l'ensemble des liens séparés ; résidu relatif rapporté à 24 P ;
#  - ECART DECLARE AVANT EXECUTION (voir c144_declaration.txt) : sur un témoin hors grille (H3, P = 0,3), RK4 au pas T0/512 laisse un résidu relatif de 3e-5,
#    au-dessus de la tolérance de 1e-6, alors que DOP853 la respecte (6e-9). Deux lectures sont donc rapportées pour chaque trajectoire : « lettre stricte »
#    (tolérance exigée des trois intégrations) et « référence » (tolérance exigée de DOP853, schéma de référence du protocole ; accord de statut et de liens exigé des trois) ;
#  - témoins de perturbation : sommet 1, axe x, DOP853 seul ; leur désaccord avec la trajectoire nominale rend celle-ci INDETERMINEE, comme l'exige le protocole.
import numpy as np, itertools, math, json, sys, time
from scipy.integrate import solve_ivp
EDGE = np.array(list(itertools.combinations(range(4), 2))); I, J = EDGE[:, 0], EDGE[:, 1]
M = np.zeros((4, 6))
for z, (i, j) in enumerate(EDGE): M[i, z] = 1.0; M[j, z] = -1.0
P0 = np.array([[0, 0, 0], [1, 0, 0], [.5, math.sqrt(3) / 2, 0], [.5, math.sqrt(3) / 6, math.sqrt(2 / 3)]], float)
T0 = 2 * math.pi / math.sqrt(2); KS = 2.0; D = 1.0; R0 = 1.0; LL = math.sqrt(6 * D / KS); RC = R0 + LL
S2 = math.sqrt(2)
REG = {'B0': (0.0, (), 0.0), 'H1': (1.0, (S2,), 0.0), 'H3': (1.0, (1.0, S2, 2.0), 0.0), 'X1': (1.0, (S2,), 0.04), 'X3': (1.0, (1.0, S2, 2.0), 0.04), 'DET3': (1.0, (2.0, 2 * S2, 4.0), 0.0)}
CAD = {'1/2': 0.5, '4/5': 0.8, '1': 1.0, '6/5': 1.2}; NIMP = {'1/2': 48, '4/5': 30, '1': 24, '6/5': 20}
CHECK = (1, 4, 8, 12, 16, 20, 24, 28)

def pot(r):
    u = (r - R0) / LL
    U = np.where(r < R0, .5 * KS * (r - R0) ** 2, np.where(r < RC, D * (3 * u * u - 2 * u ** 3), D))
    dU = np.where(r < R0, KS * (r - R0), np.where(r < RC, D * (6 * u - 6 * u * u) / LL, 0.0))
    h = np.where(r < R0, r - R0, np.where(r < RC, LL * u * (1 - u) ** 2, 0.0))
    dh = np.where(r < R0, 1.0, np.where(r < RC, (1 - u) * (1 - 3 * u), 0.0))
    return U, dU, h, dh

class Model:
    def __init__(self, reg):
        self.alpha, w, self.nu = REG[reg]; self.w2 = np.array(w) ** 2; self.m = len(w); self.n = 24 + 12 * self.m + 1
    def unpack(self, s):
        m = self.m; return s[:12].reshape(4, 3), s[12:24].reshape(4, 3), s[24:24 + 6 * m].reshape(6, m), s[24 + 6 * m:24 + 12 * m].reshape(6, m), s[-1]
    def rhs(self, t, s):
        x, v, y, yd, _ = self.unpack(s); d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); U, dU, h, dh = pot(r)
        if self.m:
            dev = y - self.alpha * h[:, None]; dV = dU - self.alpha * (self.w2 * dev).sum(1) * dh; ydd = -self.nu * yd - self.w2 * dev
            return np.concatenate([v.ravel(), (M @ (d * (dV / r)[:, None])).ravel(), yd.ravel(), ydd.ravel(), [self.nu * float((yd * yd).sum())]])
        return np.concatenate([v.ravel(), (M @ (d * (dU / r)[:, None])).ravel(), [0.0]])
    def energies(self, s):
        x, v, y, yd, q = self.unpack(s); d = x[J] - x[I]; r = np.sqrt((d * d).sum(1)); U, dU, h, dh = pot(r)
        ein = (.5 * yd * yd + .5 * self.w2 * (y - self.alpha * h[:, None]) ** 2) if self.m else np.zeros((6, 0))
        return dict(cin=.5 * float((v * v).sum()), coh=float(U.sum()), interne=float(ein.sum()), ext=float(q), interne_lien=[float(k) for k in ein.sum(1)],
                    interne_freq=[float(k) for k in ein.sum(0)], r=[float(k) for k in r])
    def lengths(self, s):
        x = s[:12].reshape(4, 3); d = x[J] - x[I]; return np.sqrt((d * d).sum(1))

def impulse(s, W):
    x = s[:12].reshape(4, 3); v = s[12:24].reshape(4, 3); g = np.zeros((4, 3))
    for o in (1, 2, 3):
        u = x[o] - x[0]; u = u / np.linalg.norm(u); g[o] += u; g[0] -= u
    aa = (v * g).sum(); bb = (g * g).sum(); al = (-aa + math.sqrt(aa * aa + 2 * bb * W)) / bb; vn = v + al * g
    w = .5 * float((vn * vn).sum() - (v * v).sum()); s[12:24] = vn.ravel(); return w          # travail calculé AVANT d'écrire (v est une vue de s)

def run(reg, P, cad, solver='dop', sub=1, perturb=0.0, sabotage=False):
    md = Model(reg); c = CAD[cad]; N = NIMP[cad]; W = P * c; s = np.zeros(md.n); x0 = P0.copy()
    if perturb: x0[1, 0] += perturb; x0 -= x0.mean(0)
    s[:12] = x0.ravel(); src = 24 * P; E0 = 24 * P
    raw = sorted([(j * c * T0, 'k') for j in range(N)] + [(float(k) * T0, 'c') for k in CHECK]); marks = []; flags = []
    for tm_, f_ in raw:                                   # fusion des instants confondus (un choc et un point de contrôle au même instant)
        if marks and abs(tm_ - marks[-1]) < 1e-9: flags[-1].add(f_)
        else: marks.append(tm_); flags.append({f_})
    out_t = [[] for _ in range(6)]; in_t = [[] for _ in range(6)]; beyond = np.zeros(6); pts = {}; res = 0.0; pmax = 0.0; t = 0.0
    def tot(s): e = md.energies(s); return src + e['cin'] + e['coh'] + e['interne'] + (0.0 if sabotage else e['ext'])
    for k, tm in enumerate(marks):
        if tm > t + 1e-12:                                   # intégrer de t à tm
            if solver == 'dop':
                evs = []
                for z in range(6):
                    f = (lambda tt, ss, z=z: md.lengths(ss)[z] - RC); evs.append(f)
                sol = solve_ivp(md.rhs, (t, tm), s, method='DOP853', rtol=1e-10, atol=1e-12, events=evs, dense_output=True)
                for z in range(6):
                    for te in sol.t_events[z]:
                        dr = md.lengths(sol.sol(min(te + 1e-7, tm)))[z] - md.lengths(sol.sol(max(te - 1e-7, t)))[z]
                        (out_t if dr > 0 else in_t)[z].append(float(te))
                    tt = np.concatenate([[t], sol.t_events[z], [tm]])
                    for a, b in zip(tt[:-1], tt[1:]):
                        if b > a and md.lengths(sol.sol(.5 * (a + b)))[z] >= RC: beyond[z] += b - a
                s = sol.y[:, -1].copy()
            else:
                nst = math.ceil((tm - t) / (T0 / (512 * sub)) - 1e-9); hh = (tm - t) / nst; rp = md.lengths(s)
                for i in range(nst):
                    k1 = md.rhs(0, s); k2 = md.rhs(0, s + .5 * hh * k1); k3 = md.rhs(0, s + .5 * hh * k2); k4 = md.rhs(0, s + hh * k3)
                    s = s + hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4); rn = md.lengths(s); ta = t + i * hh
                    for z in range(6):
                        if (rp[z] - RC) * (rn[z] - RC) < 0:
                            te = ta + hh * (RC - rp[z]) / (rn[z] - rp[z]); (out_t if rn[z] > rp[z] else in_t)[z].append(float(te))
                            beyond[z] += (ta + hh - te) if rn[z] > rp[z] else (te - ta)
                        elif rp[z] >= RC and rn[z] >= RC: beyond[z] += hh
                    rp = rn
            t = tm
        res = max(res, abs(tot(s) - E0))
        if 'c' in flags[k]:
            e = md.energies(s); e['source'] = src; pts[int(round(tm / T0))] = e
        if 'k' in flags[k] and P > 0:
            src -= impulse(s, W); res = max(res, abs(tot(s) - E0))
        v = s[12:24].reshape(4, 3); pmax = max(pmax, float(np.abs(v.sum(0)).max()))
    rf = md.lengths(s); tfin = 24 * T0
    pers = [z for z in range(6) if rf[z] >= RC and out_t[z] and not any(te >= tfin for te in in_t[z]) and not any(te > tfin for te in out_t[z])]
    crossed = any(out_t[z] for z in range(6))
    return dict(statut='PERSISTANTE' if pers else ('TRANSITOIRE' if crossed else 'LIE'), liens=[tuple(int(q) for q in EDGE[z]) for z in pers],
                premier=[(min(o) / T0 if o else None) for o in out_t], sorties=[len(o) for o in out_t], recaptures=[len(o) for o in in_t], au_dela=[float(b / T0) for b in beyond],
                r_fin=[float(q) for q in rf], points=pts, residu_abs=res, residu_rel=res / (E0 if E0 > 0 else 1.0), qmv=pmax)

def traj(a):
    reg, P, cad = a; t0 = time.time(); o = dict(regime=reg, P=P, cadence=cad)
    o['dop'] = run(reg, P, cad, 'dop'); o['rk1'] = run(reg, P, cad, 'rk', 1); o['rk2'] = run(reg, P, cad, 'rk', 2)
    sol = [o['dop'], o['rk1'], o['rk2']]
    same = len(set((s['statut'], tuple(sorted(tuple(l) for l in s['liens']))) for s in sol)) == 1
    okres = all(s['residu_abs'] <= 1e-6 and s['residu_rel'] <= 1e-6 for s in sol)
    o['accord'] = same; o['bilan_ok'] = okres
    if P in (0.25, 0.5) and cad in ('4/5', '1') and reg in ('B0', 'H3', 'X3'):
        o['pert'] = [run(reg, P, cad, 'dop', perturb=e) for e in (1e-8, -1e-8)]
        o['accord_pert'] = all((p['statut'], tuple(sorted(tuple(l) for l in p['liens']))) == (o['dop']['statut'], tuple(sorted(tuple(l) for l in o['dop']['liens']))) for p in o['pert'])
    o['verdict'] = o['dop']['statut'] if (same and okres and o.get('accord_pert', True)) else 'INDETERMINE'            # lettre stricte : tolérance exigée des trois intégrations
    okref = o['dop']['residu_abs'] <= 1e-6 and o['dop']['residu_rel'] <= 1e-6
    o['verdict_ref'] = o['dop']['statut'] if (same and okref and o.get('accord_pert', True)) else 'INDETERMINE'        # lecture de référence : tolérance exigée de DOP853
    o['duree'] = round(time.time() - t0, 1); return o

if __name__ == '__main__':
    from multiprocessing import Pool
    jobs = [(reg, P, c) for P in (0.0, 1 / 48, 0.25, 0.5, 1.0) for c in ('1/2', '4/5', '1', '6/5') for reg in ('B0', 'H1', 'H3', 'X1', 'X3', 'DET3')]
    res = []; t0 = time.time()
    with Pool(2) as pool:
        for o in pool.imap(traj, jobs):
            res.append(o); json.dump(res, open('c144.json', 'w')); d = o['dop']; f = [x for x in d['premier'] if x is not None]
            print(f"P={o['P']:<8.5f} cad={o['cadence']:<4} {o['regime']:<5} -> {o['verdict']:<12} ref={o['verdict_ref']:<12} dop={d['statut']:<12} rk={o['rk1']['statut'][:5]},{o['rk2']['statut'][:5]} liens={d['liens']} "
                  f"1er={round(min(f),3) if f else None} recapt={sum(d['recaptures'])} résidu={max(d['residu_rel'],o['rk1']['residu_rel'],o['rk2']['residu_rel']):.1e} "
                  f"pert={[p['statut'][:5] for p in o['pert']] if 'pert' in o else ''} ({time.time()-t0:.0f} s)", flush=True)
    print('TERMINE', len(res))
