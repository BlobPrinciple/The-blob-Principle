# C-134 — LA MITOSE COMME MOTEUR : BILAN D'ENERGIE ET CINEMATIQUE (Claude, 12 nov. 2026). PREENREGISTRE AVANT CALCUL.
# Donnee de l'auteur (Rudolphe, 12 nov., 13 h 46 UTC, dans la conversation avec ChatGPT) : "la mitose est ce qui etire" ; elle est premiere, continue,
#   ralentie ou arretee dans les tetraedres et la matiere sous tension. Front complementaire de C-132 (ChatGPT : mecanique a positions libres).
# (A) Bilan d'energie, sans calcul nouveau de trame : temoin homothetique de C-120/PR-1 (mitose reguliere imposee, regle U, 512 cellules).
#     Par generation : energie injectee par les naissances (E_insertion - E_equilibre precedent), energie dissipee par la detente, energie stockee.
#     PREDICTION : energie stockee par naissance entre 0,10 et 0,13 (c'est le residu geometrique de C-23, 0,021 par fil) ; energie injectee par
#     naissance strictement superieure a 0,128 (naissances synchrones, donc loin du seuil) ; la difference est dissipee.
# (B) Cinematique : N_g = 2^g et volume moyen par cellule constant donnent a_g = 2^(g/3) [C-116, C-120]. Si la duree d'une generation est constante
#     dans le temps des observateurs, a(t) = exp(H t), H = ln 2 / (3 tau) : expansion de de Sitter, q = -1, w = -1 (coherent avec F-01).
#     PREDICTION : la cadence constante seule [FAIL] contre l'histoire mesuree de l'expansion (H(z) croit avec z) ; elle ne rend que la limite future.
#     Exigence observationnelle traduite dans le langage du Blob : cadence par cellule = 3 H(z).
import json, math, numpy as np
rows=json.load(open('c120_s1.json'))['UI']; prev=None; tot=dict(inj=0,dis=0,b=0)
print('(A) Témoin homothétique, mitose régulière imposée, règle U')
print('  g  cellules  naissances  injectée  dissipée  stockée   injectée/naissance  facteur d\'échelle (fondateurs)')
for r in rows:
    if prev is not None:
        b=r['N0']-prev['N0']; inj=r['E_insertion']-prev['E']; dis=r['E_insertion']-r['E']; tot['inj']+=inj; tot['dis']+=dis; tot['b']+=b
        print(f"  {r['g']}  {r['N3']:7d}  {b:9d}  {inj:8.4f}  {dis:8.4f}  {r['E']-prev['E']:8.4f}  {inj/b:12.4f}        {np.mean(r['fondateurs'])/np.mean(prev['fondateurs']):.4f}")
    prev=r
sto=rows[-1]['E']-rows[0]['E']
print(f"  total : {tot['b']} naissances ; injectée {tot['inj']:.3f} = {tot['inj']/tot['b']:.4f} par naissance ; dissipée {tot['dis']:.3f} = {tot['dis']/tot['b']:.4f} ; stockée {sto:.3f} = {sto/tot['b']:.4f} par naissance ; {rows[-1]['E']/rows[-1]['N1']:.4f} par fil")
# trois derniers paliers seulement (regime etabli)
r6,r9=rows[6],rows[9]; b=r9['N0']-r6['N0']; inj=sum(rows[g]['E_insertion']-rows[g-1]['E'] for g in (7,8,9))
print(f"  dernier palier (générations 7 à 9) : {b} naissances ; injectée {inj/b:.4f} ; stockée {(r9['E']-r6['E'])/b:.4f} par naissance ; échelle × {np.mean(r9['fondateurs'])/np.mean(r6['fondateurs']):.4f}")
print('\n(B) Cinématique : cadence exigée par l\'observation, par cellule, = 3 H(z). ΛCDM plate de référence (Planck 2018 : H0 = 67,4 ; Ωm = 0,315 ; Ωr = 9,2e-5)')
H0=67.4; Om=0.315; Or=9.2e-5; OL=1-Om-Or; Gyr=977.8/H0   # 1/H0 en milliards d'annees
H=lambda z:H0*math.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)
for z in (0,0.51,1,2.33,1100):
    t2=math.log(2)/3*Gyr*H0/H(z)
    print(f'  z = {z:<6}: H = {H(z):12.1f} km/s/Mpc ; cadence relative {H(z)/H0:10.2f} ; doublement du nombre de cellules en {t2*1e9:.3e} ans')
print(f'  limite future (de Sitter) : H = {H0*math.sqrt(OL):.1f} km/s/Mpc ; doublement en {math.log(2)/3*Gyr/math.sqrt(OL):.2f} milliards d\'années')
print(f'  décélération aujourd\'hui q0 = {Om/2+Or-OL:.3f} (de Sitter : -1) ; transition décélération → accélération à z = {(2*OL/Om)**(1/3)-1:.2f}')
