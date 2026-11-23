#!/usr/bin/env python3
"""Scan des masters, etape 2 : au grain de la phrase. Pour chaque master anterieur, part des phrases presentes dans le master courant (V346 ou armature V347.1),
et phrases absentes (contenu qui n'a pas ete porte). Les phrases absentes sont gardees pour le scan par verrou."""
import os, re, json, pickle, hashlib
ICI = os.path.dirname(os.path.abspath(__file__))
ORDRE = [('V111', 'S087'), ('V139', 'S034'), ('V152a', 'S035'), ('V152b', 'S036'), ('V155', 'S037'), ('PROPRE', 'S030'), ('V223', 'S032'), ('V230', 'S033'),
         ('V311', 'S005'), ('V315', 'S006'), ('V316', 'S007'), ('V319', 'S008'), ('MAITRE_UNIQUE', 'S009'), ('V345s', 'S004'), ('V346', 'S001'), ('V347.1', 'S002')]
def phrases(texte):
    out = []
    for p, page in enumerate(texte.split('\f'), 1):
        page = re.sub(r'-\n\s*', '', page)                       # cesures
        page = re.sub(r'\s+', ' ', page)
        for ph in re.split(r'(?<=[.!?;:])\s+(?=[A-ZÀÂÉÈÊÎÔÛÇ\[(«0-9])', page):
            ph = ph.strip()
            if len(ph) >= 50: out.append((p, ph))
    return out
def cle(ph):
    return hashlib.md5(re.sub(r'[^a-z0-9àâäéèêëîïôöùûüç]+', '', ph.lower()).encode()).digest()[:8]
T = {nom: phrases(open(os.path.join(ICI, 'txt', sid + '.txt'), encoding='utf-8', errors='replace').read()) for nom, sid in ORDRE}
courant = set(cle(ph) for nom in ('V346', 'V347.1') for p, ph in T[nom])
absents = {}; bilan = []
for nom, sid in ORDRE:
    ks = [(p, ph, cle(ph)) for p, ph in T[nom]]
    dist = {}
    for p, ph, k in ks: dist.setdefault(k, (p, ph))
    manq = [(p, ph) for k, (p, ph) in dist.items() if k not in courant]
    absents[nom] = manq
    b = dict(master=nom, phrases=len(ks), phrases_distinctes=len(dist), presentes_dans_le_master_courant=len(dist) - len(manq), absentes=len(manq), part_portee=round(1 - len(manq) / max(1, len(dist)), 4), caracteres_absents=sum(len(ph) for p, ph in manq))
    bilan.append(b)
    print('%-14s | %6d phrases distinctes | %6d portees dans V346/V347.1 (%5.1f %%) | %6d absentes | %8d car absents' % (nom, len(dist), b['presentes_dans_le_master_courant'], 100 * b['part_portee'], len(manq), b['caracteres_absents']))
json.dump(bilan, open(os.path.join(ICI, 'phrases_bilan.json'), 'w'), indent=1)
pickle.dump(dict(T=T, absents=absents), open(os.path.join(ICI, 'phrases.pkl'), 'wb'))
