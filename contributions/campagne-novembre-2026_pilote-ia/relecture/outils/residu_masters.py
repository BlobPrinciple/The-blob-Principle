#!/usr/bin/env python3
"""Résidu de lecture d'une suite de documents : pour chaque document, dans l'ordre donné, écrit toutes les phrases
absentes de l'union de ce qui a déjà été lu (index initial + documents précédents), puis ajoute le document à l'union.

Comparaison sur les seuls caractères alphanumériques (insensible à la mise en lignes, aux numéros de page, aux ligatures).
Une phrase d'au moins 40 caractères est dite présente si la moitié au moins de ses fenêtres de 40 caractères (pas de 10)
existent dans l'union ; une phrase de 16 à 39 caractères, si toutes ses fenêtres de 16 caractères y existent ;
une phrase plus courte est neutre (elle n'ouvre pas de bloc, mais reste dans un bloc ouvert).
Les phrases absentes voisines sont regroupées en blocs, précédés de la dernière phrase présente (contexte).
Chaque bloc est classé : « prose » (au moins 55 % de lettres), « formules » (35 à 55 %), « données » (moins de 35 %).

Usage :
  residu_masters.py init  <index.npz> <ref> [<ref> ...]            crée l'index à partir des textes déjà lus
  residu_masters.py lire  <index.npz> <dossier_sortie> <doc> [...]  traite les documents dans l'ordre, met l'index à jour
"""
import re, sys, os, numpy as np
L, L2, B = 40, 16, np.uint64(1099511628211)

def lire(path):
    brut = open(path, encoding='utf-8', errors='replace').read().replace('\x0c', ' ')
    for a, b in (('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬀ', 'ff'), ('ﬃ', 'ffi'), ('ﬄ', 'ffl')):
        brut = brut.replace(a, b)
    return re.sub(r'-\n\s*', '', brut)

_non = re.compile(r'[^0-9a-zà-ÿ]')
def norm(s):
    return _non.sub('', s.lower().replace('÷', '').replace('×', ''))

def hashes(a, n):
    """Hachage polynomial (mod 2^64) de toutes les fenêtres de longueur n du tableau d'octets a."""
    if len(a) < n: return np.zeros(0, dtype=np.uint64)
    with np.errstate(over='ignore'):
        H = {1: a.astype(np.uint64) + np.uint64(1)}
        m = 1
        while 2 * m <= n:
            h = H[m]; H[2 * m] = h[:-m] * (B ** np.uint64(m)) + h[m:]; m *= 2
        res, pos, reste = None, 0, n
        for m in sorted(H, reverse=True):
            while reste >= m:
                h = H[m][pos: pos + len(a) - n + 1] if pos + len(a) - n + 1 <= len(H[m]) else H[m][pos:]
                h = h[: len(a) - n + 1]
                res = h.copy() if res is None else res * (B ** np.uint64(m)) + h
                pos += m; reste -= m
    return res

def octets(s): return np.frombuffer(s.encode('latin-1', errors='ignore'), dtype=np.uint8)

def dans(U, h):
    if len(U) == 0 or len(h) == 0: return np.zeros(len(h), dtype=bool)
    i = np.searchsorted(U, h); i[i >= len(U)] = len(U) - 1
    return U[i] == h

def charger(p):
    if os.path.exists(p):
        z = np.load(p); return z['u40'], z['u16']
    return np.zeros(0, dtype=np.uint64), np.zeros(0, dtype=np.uint64)

def ajouter(U40, U16, n):
    a = octets(n)
    return np.union1d(U40, hashes(a, L)), np.union1d(U16, hashes(a, L2))

def classe(bloc):
    sans = re.sub(r'\s', '', bloc)
    if not sans: return 'données'
    r = len(re.findall(r'[A-Za-zÀ-ÿ]', sans)) / len(sans)
    return 'prose' if r >= 0.55 else ('formules' if r >= 0.35 else 'données')

def traiter(path, U40, U16, sortie):
    brut = lire(path)
    phrases = re.split(r'(?<=[.!?:;])\s+', re.sub(r'\s+', ' ', brut))
    ns = [norm(p) for p in phrases]
    flux = ''.join(ns); a = octets(flux)
    p40 = dans(U40, hashes(a, L)); p16 = dans(U16, hashes(a, L2))
    etat = []; pos = 0
    for n in ns:
        m = len(n)
        if m < L2: etat.append(None)
        elif m < L: etat.append(bool(p16[pos: pos + m - L2 + 1].all()))
        else:
            f = p40[pos: pos + m - L + 1: 10]; etat.append(bool(f.mean() >= 0.5))
        pos += m
    stats = {'prose': [0, 0], 'formules': [0, 0], 'données': [0, 0]}
    out = {k: [] for k in stats}
    i = 0
    while i < len(phrases):
        if etat[i] is False:
            j = i
            while j < len(phrases) and etat[j] is not True: j += 1
            while j > i and etat[j - 1] is None: j -= 1
            k = i - 1
            while k >= 0 and etat[k] is None: k -= 1
            bloc = ' '.join(phrases[i:j]); c = classe(bloc)
            stats[c][0] += 1; stats[c][1] += len(bloc.split())
            out[c].append(f"\n=== bloc (phrases {i}–{j-1}) — après : « {phrases[k][-160:] if k >= 0 else ''} »\n{bloc}\n")
            i = j
        else: i += 1
    base = os.path.join(sortie, os.path.basename(path).rsplit('.', 1)[0])
    for c in out:
        if out[c]:
            open(f"{base}.{c}.txt", 'w', encoding='utf-8').write(''.join(out[c]) + f"\n##### {stats[c][0]} blocs, {stats[c][1]} mots\n")
    U40, U16 = np.union1d(U40, hashes(a, L)), np.union1d(U16, hashes(a, L2))
    tot = len(brut.split())
    print(f"{os.path.basename(path)[:60]:60s} mots {tot:8d} | absents : prose {stats['prose'][1]:7d} ({stats['prose'][0]} blocs) ; "
          f"formules {stats['formules'][1]:6d} ; données {stats['données'][1]:7d} | union {len(U40)/1e6:.1f} M", flush=True)
    return U40, U16

if __name__ == '__main__':
    mode, idx = sys.argv[1], sys.argv[2]
    U40, U16 = charger(idx)
    if mode == 'init':
        for r in sys.argv[3:]:
            U40, U16 = ajouter(U40, U16, norm(lire(r))); print(os.path.basename(r)[:70], '→ union', round(len(U40) / 1e6, 2), 'M', flush=True)
    elif mode == 'lire':
        sortie = sys.argv[3]; os.makedirs(sortie, exist_ok=True)
        for d in sys.argv[4:]:
            U40, U16 = traiter(d, U40, U16, sortie)
    np.savez(idx, u40=U40, u16=U16)
