# -*- coding: utf-8 -*-
"""DEFI-R6 — analyse de la campagne (parties B et C).

Statistiques par graine et différences appariées (même configuration initiale) :
  nucléation  = figé − poisson ;
  mobilité    = mobile − figé ;
  viabilité   = viab − mobile.
Lit r6_campagne_N*.json (moteur archivé) et r6_second_N*.json (seconde implémentation).
Écrit r6_analyse_sortie.json.
"""
import glob, json, os, re
import numpy as np
from scipy import stats

ICI = os.path.dirname(os.path.abspath(__file__))
OBS = ["Pmax_sur_N2", "vides", "Pmax_sur_mediane"]


def charger(motif):
    par = {}
    for f in sorted(glob.glob(os.path.join(ICI, motif))):
        d = json.load(open(f))
        cle = (d["N"], d["balayages"]) if d.get("init", "germes") == "germes" else (d["N"], d["balayages"], "init_poisson")
        par.setdefault(cle, {}).update(d["graines"])
    return par


def ms(x):
    x = np.asarray(x, float)
    return [float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x)))]


def resumer(par, etiquette):
    out = {}
    for cle, gr in sorted(par.items(), key=lambda t: tuple(str(x) for x in t[0])):
        N, b = cle[0], cle[1]
        suffixe = "_init_poisson" if len(cle) > 2 else ""
        G = sorted(gr, key=int)
        bloc = {"graines": len(G)}
        for o in OBS:
            v = {bras: np.array([gr[g][bras][o] for g in G]) for bras in ("poisson", "fige", "mobile", "viab")}
            bloc[o] = {bras: ms(v[bras]) for bras in v}
            dif = {"nucleation": v["fige"] - v["poisson"], "mobilite": v["mobile"] - v["fige"],
                   "viabilite": v["viab"] - v["mobile"], "viab_moins_fige": v["viab"] - v["fige"]}
            bloc[o]["apparie"] = {}
            for k, x in dif.items():
                t = stats.ttest_1samp(x, 0.0)
                bloc[o]["apparie"][k] = {"moyenne_et": ms(x), "positifs": int((x > 0).sum()),
                                         "p_bilateral": float(t.pvalue)}
            if o == "Pmax_sur_N2":
                tot = v["viab"] - v["poisson"]
                bloc[o]["part_de_la_nucleation"] = ms((v["fige"] - v["poisson"]) / tot)
        bloc["kmax_viab"] = [gr[g]["viab"]["kmax"] for g in G]
        bloc["kmax_fige"] = [gr[g]["fige"]["kmax"] for g in G]
        out[f"N{N}_b{b}{suffixe}"] = bloc
        A = bloc["Pmax_sur_N2"]; V = bloc["vides"]
        print(f"[{etiquette}] N={N} balayages={b}{suffixe} graines={len(G)}")
        print(f"   amplitude Pmax/N^2 : poisson {A['poisson'][0]:.4f} figé {A['fige'][0]:.4f} "
              f"mobile {A['mobile'][0]:.4f} viab {A['viab'][0]:.4f} ; part nucléation {A['part_de_la_nucleation'][0]:.3f}")
        for k in ("mobilite", "viabilite", "viab_moins_fige"):
            a = A["apparie"][k]; w = V["apparie"][k]
            print(f"   {k:16s} Δamp {a['moyenne_et'][0]:+.5f} ± {a['moyenne_et'][1]:.5f} ({a['positifs']}/{len(G)}) | "
                  f"Δvides {w['moyenne_et'][0]:+.5f} ± {w['moyenne_et'][1]:.5f} ({w['positifs']}/{len(G)})")
        print(f"   kmax viab {bloc['kmax_viab']} ; Pmax/médiane viab {bloc['Pmax_sur_mediane']['viab'][0]:.1f} figé {bloc['Pmax_sur_mediane']['fige'][0]:.1f}")
        print(f"   vides : poisson {V['poisson'][0]:.4f} figé {V['fige'][0]:.4f} mobile {V['mobile'][0]:.4f} viab {V['viab'][0]:.4f}")
    return out


def main():
    res = {"moteur_archive": resumer(charger("r6_campagne_N*.json"), "A"),
           "second_moteur": resumer(charger("r6_second_N*.json"), "B")}
    # comparaison A/B : écart des moyennes par bras, en unités d'erreur combinée
    comp = {}
    for cle in res["moteur_archive"]:
        if cle not in res["second_moteur"]:
            continue
        comp[cle] = {}
        for o in ("Pmax_sur_N2", "vides"):
            for k in ("mobilite", "viabilite"):
                a = res["moteur_archive"][cle][o]["apparie"][k]["moyenne_et"]
                b = res["second_moteur"][cle][o]["apparie"][k]["moyenne_et"]
                z = (a[0] - b[0]) / np.hypot(a[1], b[1])
                comp[cle][f"{o}_{k}"] = {"A": a, "B": b, "z": float(z)}
                print(f"[A/B] {cle} {o:12s} {k:10s} A {a[0]:+.5f} B {b[0]:+.5f} z = {z:+.2f}")
    res["comparaison_A_B"] = comp
    json.dump(res, open(os.path.join(ICI, "r6_analyse_sortie.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
