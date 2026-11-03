# -*- coding: utf-8 -*-
"""DEFI-R6 — mesures (implémentation A) et conditions initiales reconstruites.

Le script producteur de blob_toile_results.json manque au corpus (NOTE R5, E4).
Les conventions de mesure sont reconstruites depuis le fichier lui-même :
- vides : fraction des 20^3 = 8 000 cellules vides (le Poisson archivé suit
  exp(−N/8000) : 0,883 à N = 1 000 ; 0,083 à N = 20 000) ;
- P(k) : |FFT|^2 des comptes sur grille 64^3 (affectation au plus proche), moyenne
  par coquille round(|k|) = 1..31 ; le Poisson archivé vaut ≈ N à tout k.
Les germes (nucléation « K = 8 germes d'âges variés », V346 XXV.2 p. 644) sont un
modèle reconstruit, déclaré comme tel : centres uniformes, âges a_k ~ U(0,2 ; 1),
effectifs ∝ a_k^3, nuages gaussiens d'écart-type s·a_k, ramenés dans [0,1]^3
par np.clip comme le moteur de mobilité archivé.
"""
import numpy as np

NG_VIDE = 20
NG_PK = 64


def vides(pts):
    c = np.clip((pts * NG_VIDE).astype(int), 0, NG_VIDE - 1)
    occ = np.zeros((NG_VIDE,) * 3, bool)
    occ[c[:, 0], c[:, 1], c[:, 2]] = True
    return 1.0 - occ.mean()


_K = None


def _coquilles():
    global _K
    if _K is None:
        f = np.fft.fftfreq(NG_PK) * NG_PK
        kx, ky, kz = np.meshgrid(f, f, f[: NG_PK // 2 + 1], indexing="ij")
        km = np.rint(np.sqrt(kx**2 + ky**2 + kz**2)).astype(int)
        # poids rfft : les plans kz = 0 et kz = Nyquist ne sont pas doublés
        w = np.full(km.shape, 2.0)
        w[:, :, 0] = 1.0
        w[:, :, -1] = 1.0
        _K = (km, w)
    return _K


def pk(pts):
    c = np.clip((pts * NG_PK).astype(int), 0, NG_PK - 1)
    g = np.zeros((NG_PK,) * 3)
    np.add.at(g, (c[:, 0], c[:, 1], c[:, 2]), 1.0)
    p = np.abs(np.fft.rfftn(g)) ** 2
    km, w = _coquilles()
    out = np.empty(31)
    for k in range(1, 32):
        m = km == k
        out[k - 1] = (p[m] * w[m]).sum() / w[m].sum()
    return out


def resume(pts):
    p = pk(pts)
    n = len(pts)
    return {"Pmax_sur_mediane": float(p.max() / np.median(p)),
            "Pmax_sur_N2": float(p.max() / n**2), "kmax": int(np.argmax(p) + 1),
            "mediane_sur_N": float(np.median(p) / n), "vides": float(vides(pts))}


def germes(N, rng, K=8, s=0.06, amin=0.2):
    if K == 1:
        ages = np.array([1.0])
    else:
        ages = rng.uniform(amin, 1.0, K)
    centres = rng.uniform(0, 1, (K, 3))
    poids = ages**3 / (ages**3).sum()
    nk = rng.multinomial(N, poids)
    pts = np.concatenate([centres[k] + rng.normal(0, s * ages[k], (nk[k], 3)) for k in range(K)])
    return np.clip(pts, 0, 1)


def poisson(N, rng):
    return rng.uniform(0, 1, (N, 3))
