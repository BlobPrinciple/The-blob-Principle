# AUDIT LOGICIEL exigé par [T-2] : 5 paires D = 1/2 / D = 2 non identiques en RK4, toutes dans la géométrie exactement symétrique. On suit les deux calculs choc par choc.
from c145c import *
def suivi(D, P, src, cad, sub, nmax=40):
    cx = Ctx('K4', D, 0.0, 0.5); c = {'1/2': .5, '1': 1.}[cad]; T0 = cx.T0; s = np.zeros(cx.N); s[:12] = geometrie('K4', 0).ravel(); r = np.empty(6); p = np.empty(6); lensg(s, cx.BI, cx.BJ, r)
    side = np.ones((3, 10), np.int64); side[0, :6] = np.where(r >= R0, 1, -1); side[1, :6] = -1; ev = []; colls = []; st = dict(rmin=np.ones(6), ovl=-1.0, k=0, fprev=None, IFU=0.0); t = 0.0; log = []
    for j in range(int(24 / c)):
        tm = j * c * T0
        if tm > t + 1e-12: s = rk_adv3(cx, s, t, tm, sub, side, ev, st, colls); t = tm
        kick3(s, P * c, 4, v=0) if src == 'S' else kick3(s, P * c, 4, edge=(0, 1))
        lensg(s, cx.BI, cx.BJ, r); log.append((j, len(colls), [float(q) for q in r], [float(q) for q in s[12:24] / math.sqrt(D)]))
        if len(log) >= nmax: break
    return log, [(q[0] / T0, tuple(q[1])) for q in colls]
for P_D, src, cad, sub in ((0.0625, 'S', '1', 1), (0.125, 'S', '1', 2)):
    la, ca = suivi(0.5, P_D * 0.5, src, cad, sub); lb, cb = suivi(2.0, P_D * 2.0, src, cad, sub)
    k = next((i for i, (x, y) in enumerate(zip(ca, cb)) if abs(x[0] - y[0]) > 1e-12 or x[1] != y[1]), None)
    j = next((i for i, (x, y) in enumerate(zip(la, lb)) if x[2] != y[2] or x[3] != y[3]), None)
    print(f'P/D = {P_D}, {src}, cadence {cad}, RK4 T0/{1024*sub} : première collision différente : n° {k}' + (f' — D=1/2 : {ca[k]} ; D=2 : {cb[k]}' if k is not None else '') + f' ; premier choc où les états (positions, vitesses réduites) ne sont plus identiques bit à bit : n° {j}')
    if j is not None: print('     écart maximal à ce choc : positions', max(abs(x - y) for x, y in zip(la[j][2], lb[j][2])), '; vitesses réduites', max(abs(x - y) for x, y in zip(la[j][3], lb[j][3])), '; collisions avant :', la[j][1], lb[j][1])
    if k is not None and k > 0: print('     collision précédente (identique) :', ca[k - 1], '| contacts simultanés à la collision différente : D=1/2', len(ca[k][1]), ', D=2', len(cb[k][1]))
