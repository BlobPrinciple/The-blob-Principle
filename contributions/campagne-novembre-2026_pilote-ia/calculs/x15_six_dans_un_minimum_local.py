#!/usr/bin/env python3
"""X-15 [APRES COUP, non aveugle] -- controle de l'observation de ChatGPT (C-192-U, graine 192009, N = 13) : un minimum LOCAL de Lennard-Jones ou un lien est entoure de SIX tetraedres.
Coordonnees recopiees de son fichier C192U_N13_192009_POSTHOC_COORDS.csv. On verifie avec mes outils : energie, force, valeurs propres du hessien, liens entoures, et on compare a mon
etat de la meme graine (c192uc.json). (Claude, 17 novembre 2026.) Usage : python3 x15_six_dans_un_minimum_local.py"""
import json, itertools
import numpy as np, scipy.optimize as so
from c187c import lj
from c189c import mesure
X = np.array([[-0.047381458466428439,0.073302481643530731,0.29198886276921898],[0.48697286861217309,-0.56794336358514808,-0.34780419011203667],[0.24602731617729071,0.89378333143393374,-0.1687403920145584],
[0.91084047354235509,-0.058459525157299859,0.37445280002006937],[0.87865783901471894,0.27751345229833141,-0.58449376704340428],[-0.12175487991855291,0.1169810447099989,-0.68438515661973276],
[0.47711669150389818,0.76767477910900517,0.77865956862202801],[0.21732799916134285,-0.8207846247837054,0.57836339535081305],[0.36251469967531785,-0.098628625377834719,1.211856202061121],
[-0.4524256233103045,-0.71593802423487996,-0.15869359681763245],[0.24077810138921665,-1.4888178203292024,-0.13757009294336039],[1.1084831495323837,-1.0443246507316821,0.23671483149885542],[1.2092009698170387,0.86367474942936162,0.13095358426948739]])
e, g = lj(X.ravel()); r = so.minimize(lj, X.ravel(), jac=True, method='BFGS', options=dict(gtol=1e-10, maxiter=5000)); Y = r.x.reshape(-1, 3)
h = 1e-5; z = Y.ravel(); H = np.array([(lj(z + h * v)[1] - lj(z - h * v)[1]) / (2 * h) for v in np.eye(39)]); w = np.linalg.eigvalsh((H + H.T) / 2)
m0 = mesure(X, 1.30 + 1e-12); m1 = mesure(Y, 1.30 + 1e-12); D = np.linalg.norm(Y[:, None] - Y[None], axis=2)
moi = json.load(open('c192uc.json'))['LJ'][9]['etats']['13']
out = dict(E_fourni=float(e), force_fournie=float(np.linalg.norm(g)), E_apres_BFGS=float(r.fun), deplacement_max=float(np.abs(Y - X).max()), force_apres=float(np.linalg.norm(lj(z)[1])), modes_nuls=int((abs(w) < 1e-3).sum()), vp_negatives=int((w < -1e-3).sum()),
           plus_petite_vp_positive=float(w[w > 1e-3].min()), mesure_fournie=dict(tetraedres=m0['tetraedres'], distribution=m0['distribution'], surcharges=m0['faces_surchargees']), mesure_apres=dict(tetraedres=m1['tetraedres'], distribution=m1['distribution'], surcharges=m1['faces_surchargees']),
           longueur_lien_0_3=float(D[0, 3]), mon_etat_meme_graine=dict(E=moi['E'], distribution=moi['distribution'], tetraedres=moi['tetraedres']))
json.dump(out, open('x15_six_dans_un_minimum_local.json', 'w'), indent=1); print(json.dumps(out))
