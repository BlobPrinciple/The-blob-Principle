#!/usr/bin/env python3
"""X-35 : dépouillement de x35_resultats.jsonl. Moyennes et erreurs types (écart-type des graines / racine du nombre de graines)."""
import json, math, collections
PL = (0.6847, 0.2645, 0.0490); BANDES = (0.030, 0.030, 0.012)
G = collections.defaultdict(list)
for l in open('x35_resultats.jsonl'):
    d = json.loads(l); G[(d['bras'], d['kappa'], d['N'])].append(d)
def ms(v):
    n = len(v); m = sum(v) / n
    s = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1)) if n > 1 else float('nan')
    return m, s / math.sqrt(n) if n > 1 else float('nan')
def f(v): m, e = ms(v); return f"{m:.4f}±{e:.4f}"
print("bras kappa N | graines (écartées) | lecture principale theta=0,50 : f_L f_DM f_b | dans les bandes ? | theta=0,338 : f_L f_DM f_b")
for k in sorted(G):
    R = [d for d in G[k] if not d.get('ecartee')]; ne = len(G[k]) - len(R)
    if not R: print(k, f"| 0 ({ne})"); continue
    a = [[d['par_theta']['0.5'][x] for d in R] for x in ('f_L', 'f_DM', 'f_b')]
    b = [[d['par_theta']['0.338'][x] for d in R] for x in ('f_L', 'f_DM', 'f_b')]
    dans = ['oui' if abs(ms(a[i])[0] - PL[i]) <= BANDES[i] else 'NON' for i in range(3)]
    print(k, f"| {len(R)} ({ne}) |", f(a[0]), f(a[1]), f(a[2]), '|', '/'.join(dans), '|', f(b[0]), f(b[1]), f(b[2]))
print("\nComptage brut, sans classeur : sans triangle / triangle hors K4 / dans un K4 ; puis K4 stables (theta 0,5), part au-dessus de la moyenne, triangles et K4 par point, acceptation, stabilité moyenne")
for k in sorted(G):
    R = [d for d in G[k] if not d.get('ecartee')]
    if not R: continue
    print(k, '|', f([d['f_sans_triangle'] for d in R]), f([d['f_triangle_hors_k4'] for d in R]), f([d['f_k4'] for d in R]), '|',
          f([d['par_theta']['0.5']['f_k4_stable'] for d in R]),
          f([d['par_theta']['0.5'].get('p_chi', float('nan')) for d in R]), '|', f([d['tri_par_N'] for d in R]), f([d['k4_par_N'] for d in R]),
          f([d['acceptation'] for d in R]), f([d['stabilite_moyenne'] for d in R]))
print("\nConventions de rechange à theta = 0,50 : (i) résidu en matière noire : f_L f_DM f_b ; (ii) médiane : f_L f_DM f_b")
for k in sorted(G):
    R = [d for d in G[k] if not d.get('ecartee') and 'alt_mediane' in d['par_theta']['0.5']]
    if not R or k[0] != 'blob': continue
    print(k, '|', ' '.join(f([d['par_theta']['0.5']['alt_residu_en_DM'][i] for d in R]) for i in range(3)), '|',
          ' '.join(f([d['par_theta']['0.5']['alt_mediane'][i] for d in R]) for i in range(3)))
print("\nf_b selon theta (bras blob, kappa = 4)")
for k in sorted(G):
    R = [d for d in G[k] if not d.get('ecartee')]
    if not R or k[0] != 'blob' or k[1] != 4.0: continue
    print(k, '|', ' '.join(f"{t}:{ms([d['par_theta'][t]['f_b'] for d in R])[0]:.4f}" for t in ('0.338', '0.4', '0.45', '0.5', '0.55', '0.6')))
