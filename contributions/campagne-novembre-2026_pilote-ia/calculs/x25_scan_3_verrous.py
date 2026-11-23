#!/usr/bin/env python3
"""Scan des masters, etape 3 : rangement par verrou. Pour chaque master, nombre de phrases distinctes touchant chaque verrou (mots-cles declares ci-dessous),
dont phrases absentes du master courant. Ecrit, par verrou, les phrases absentes (verrou_Vk_absentes.tsv) et les pages de V346 les plus denses."""
import os, re, json, pickle, collections
ICI = os.path.dirname(os.path.abspath(__file__))
d = pickle.load(open(os.path.join(ICI, 'phrases.pkl'), 'rb')); T, absents = d['T'], d['absents']
V = collections.OrderedDict([
 ('V1', r"lorentz|minkowski|causal|c[oô]ne de lumi|espace-temps|espace–temps|3\s?\+\s?1|signature|dimension spectrale|hausdorff|temps propre|horloge|isotrop|vitesse de la lumi|continuum|limite continue|vari[ée]t[ée]"),
 ('V2', r"einstein|regge|courbure|ricci|newton|gravit|g[ée]od[ée]sique|schwarzschild|constante cosmologique|hubble|[ée]nergie sombre|mati[èe]re noire|friedmann|\bΛ\b|lambda cosmo"),
 ('V3', r"\bborn\b|schr[öo]dinger|hilbert|unitair|interf[ée]rence|intrication|\bbell\b|chsh|mesure quantique|d[ée]coh[ée]rence|ℏ|\bhbar\b|planck|nelson|superposition|amplitude|quantique"),
 ('V4', r"charge|\bspin|fermion|boson|dirac|spineur|photon|[ée]lectron|antimati[èe]re|chiralit|m[ée]diateur|positron"),
 ('V5', r"\bmasses?\b|koide|g[ée]n[ée]rations?\b|familles?\b|lepton|quark|hi[ée]rarchie|ckm|neutrino|muon|\btau\b|proton|1836"),
 ('V6', r"jauge|su\(3\)|su\(2\)|u\(1\)|yang|anomalie|couplage|\balpha\b|137|structure fine|confinement|weinberg|\bα\b"),
 ('V7', r"pr[ée]diction|pr[ée]dit|falsif|observable|observation|desi\b|ligo|exp[ée]rience|mesurable|t[ée]lescope|w\s?=\s?[−-]\s?1|test d[ée]cisif"),
])
RX = {k: re.compile(v, re.I) for k, v in V.items()}
bilan = []
abs_union = {k: {} for k in V}
for nom, ph in T.items():
    dist = {}
    for p, s in ph: dist.setdefault(s, p)
    ab = set(s for p, s in absents[nom])
    ligne = dict(master=nom)
    for k, rx in RX.items():
        tot = [s for s in dist if rx.search(s)]
        a = [s for s in tot if s in ab]
        ligne[k] = len(tot); ligne[k + '_absentes'] = len(a)
        for s in a: abs_union[k].setdefault(s, (nom, dist[s]))
    bilan.append(ligne)
print('%-14s' % 'master' + ''.join('%14s' % (k + ' tot/abs') for k in V))
for l in bilan:
    print('%-14s' % l['master'] + ''.join('%14s' % ('%d/%d' % (l[k], l[k + '_absentes'])) for k in V))
print('phrases absentes distinctes par verrou :', {k: len(v) for k, v in abs_union.items()})
for k, v in abs_union.items():
    with open(os.path.join(ICI, 'verrou_%s_absentes.tsv' % k), 'w') as f:
        for s, (nom, p) in v.items(): f.write('%s\t%d\t%s\n' % (nom, p, s))
# pages de V346 les plus denses par verrou
pages = collections.defaultdict(lambda: collections.Counter())
for p, s in T['V346']:
    for k, rx in RX.items():
        n = len(rx.findall(s))
        if n: pages[k][p] += n
dens = {k: pages[k].most_common(40) for k in V}
json.dump(dict(bilan=bilan, pages_denses_V346=dens), open(os.path.join(ICI, 'verrous_bilan.json'), 'w'), indent=1)
for k in V: print(k, 'pages V346 les plus denses :', ' '.join('%d(%d)' % (p, n) for p, n in sorted(pages[k].most_common(24))))
