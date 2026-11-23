#!/usr/bin/env python3
"""Scan des masters, etape 1 : decoupage en pages et en blocs, dedoublonnage entre versions.
Ordre chronologique des masters ; pour chaque master : blocs, blocs deja vus dans une version anterieure, blocs nouveaux."""
import hashlib, json, os, re, sys, collections
ICI = os.path.dirname(os.path.abspath(__file__))
ORDRE = [('V111', 'S087'), ('V139', 'S034'), ('V152a', 'S035'), ('V152b', 'S036'), ('V155', 'S037'), ('PROPRE', 'S030'), ('V223', 'S032'), ('V230', 'S033'),
         ('V311', 'S005'), ('V315', 'S006'), ('V316', 'S007'), ('V319', 'S008'), ('MAITRE_UNIQUE', 'S009'), ('V345s', 'S004'), ('V346', 'S001'), ('V347.1', 'S002')]

def blocs(texte):
    """Rend la liste (page, bloc) ; un bloc = paragraphe separe par une ligne vide ; pages separees par saut de page."""
    out = []
    for p, page in enumerate(texte.split('\f'), 1):
        for b in re.split(r'\n\s*\n', page):
            n = re.sub(r'\s+', ' ', b).strip()
            if len(n) >= 60:
                out.append((p, n))
    return out

def cle(n):
    return hashlib.md5(re.sub(r'[^a-z0-9àâäéèêëîïôöùûüç]+', '', n.lower()).encode()).hexdigest()

vus = {}
bilan = []
nouveaux = {}
for nom, sid in ORDRE:
    t = open(os.path.join(ICI, 'txt', sid + '.txt'), encoding='utf-8', errors='replace').read()
    bl = blocs(t)
    neufs = []; deja = 0; car_neufs = 0; interne = set()
    for p, n in bl:
        k = cle(n)
        if k in vus or k in interne:
            if k in vus: deja += 1
            continue
        interne.add(k); neufs.append((p, n)); car_neufs += len(n)
    for p, n in neufs:
        vus[cle(n)] = nom
    nouveaux[nom] = neufs
    bilan.append(dict(master=nom, source=sid, pages=t.count('\f') + (0 if sid in ('S087',) else 0), caracteres=len(t), blocs=len(bl), deja_vus=deja, blocs_nouveaux=len(neufs), caracteres_nouveaux=car_neufs))
    print('%-14s %s | %8d car | %6d blocs | %6d deja vus | %6d nouveaux | %8d car nouveaux' % (nom, sid, len(t), len(bl), deja, len(neufs), car_neufs))
print('total caracteres nouveaux :', sum(b['caracteres_nouveaux'] for b in bilan))
json.dump(bilan, open(os.path.join(ICI, 'dedoublonnage.json'), 'w'), indent=1)
import pickle; pickle.dump(nouveaux, open(os.path.join(ICI, 'nouveaux.pkl'), 'wb'))
