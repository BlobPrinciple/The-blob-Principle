"""
================================================================================
 BLOB — RE-ANALYSE DU BALAYAGE  (a passer sur les blob_dims_N*.json)
================================================================================
 Relit TOUS les JSON par palier deja produits (pas besoin de relancer le
 balayage) et reconstruit le scaling PROPREMENT :
   - d_w extrait de son PLATEAU (fenetre la plus plate de d_w(t)), pas d'un
     point unique  -> supprime le saut d'echantillonnage qui faisait "sauter"
     d_s/d_w dans le summary d'origine ;
   - d_f extrait de son plateau de croissance de volume ;
   - d_s lu a la meme echelle (plateau de d_w) + valeur cinematique 2 d_f/d_w ;
   - fermeture d'Einstein d_s*d_w/2d_f comme controle.

 Le but : lire la TENDANCE de d_w en montant N.
   d_w -> 2  (et d_s -> 3)  => RECOUVREMENT de variete au profond IR.
   d_w -> ~2.5 stable       => anomalie diffusive douce REELLE (CXVIII dynamique).

 Usage Colab :
   %run blob_reanalyse.py
 (cherche les blob_dims_N*.json dans le dossier courant)
================================================================================
"""
import json, glob, os, re
import numpy as np


def plateau_value(t, y, rt, diam, win=5):
    """Valeur de y sur sa fenetre la plus plate, dans la bande diffusive
       r in [0.10, 0.30]*diam. Renvoie (valeur, t_centre, r_centre, largeur)."""
    lo, hi = 0.08 * diam, 0.22 * diam
    m = (rt >= lo) & (rt <= hi) & np.isfinite(y)
    idx = np.where(m)[0]
    if len(idx) < win:
        if len(idx) == 0:
            return np.nan, np.nan, np.nan, 0
        return float(np.nanmedian(y[idx])), float(np.median(t[idx])), \
               float(np.median(rt[idx])), len(idx)
    best = None
    for k in range(len(idx) - win + 1):
        sub = idx[k:k + win]
        spread = np.nanstd(y[sub])          # plus c'est plat, mieux c'est
        if best is None or spread < best[0]:
            best = (spread, sub)
    sub = best[1]
    return (float(np.nanmedian(y[sub])), float(np.median(t[sub])),
            float(np.median(rt[sub])), float(best[0]))  # best[0] = std (platitude)


def df_plateau(dfr, diam):
    rr = np.arange(len(dfr))
    m = (rr >= 4) & (rr <= 0.30 * diam) & np.isfinite(dfr)
    if m.sum() == 0:
        return np.nan
    # mediane sur la zone la plus plate
    idx = np.where(m)[0]
    if len(idx) >= 4:
        best = None
        for k in range(len(idx) - 3):
            sub = idx[k:k + 4]
            sp = np.nanstd(dfr[sub])
            if best is None or sp < best[0]:
                best = (sp, sub)
        return float(np.nanmedian(dfr[best[1]]))
    return float(np.nanmedian(dfr[idx]))


def load_all(folder="."):
    paths = glob.glob(os.path.join(folder, "blob_dims_N*.json"))
    out = []
    for p in paths:
        try:
            d = json.load(open(p))
        except Exception as e:
            print(f"  (saute {p}: {e})"); continue
        out.append(d)
    out.sort(key=lambda d: d["N"])
    return out


def analyse(folder="."):
    data = load_all(folder)
    if not data:
        print("Aucun blob_dims_N*.json trouve dans", os.path.abspath(folder))
        return
    print(f"{'N':>9} {'diam':>5} {'d_f':>6} {'d_w(plat)':>10} {'std':>6} {'d_s':>6} "
          f"{'2df/dw':>7} {'ferm':>6}  {'plateau?':>9}")
    rows = []
    for d in data:
        N = d["N"]; diam = d["diam"]; gc = d["gc"]
        t = np.array(d["t_axis"], float)
        dw = np.array([np.nan if x is None else x for x in d["d_w_t"]])
        ds = np.array([np.nan if x is None else x for x in d["d_s_t"]])
        dfr = np.array([np.nan if x is None else x for x in d["df_r"]])
        MSD = np.array([np.nan if x is None else x for x in d["MSD"]])
        P = np.array([np.nan if x is None else x for x in d["P_return"]])
        rt = np.sqrt(np.maximum(MSD, 1e-12))
        floor = 8.0 / gc
        ok = P > floor * 1.5
        dw_p, t_p, r_p, std_p = plateau_value(t, np.where(ok, dw, np.nan), rt, diam)
        df_p = df_plateau(dfr, diam)
        sel = (np.abs(t - t_p) <= max(2, 0.4 * t_p)) & ok & np.isfinite(ds)
        ds_p = float(np.nanmedian(ds[sel])) if sel.sum() else np.nan
        ds_kin = 2 * df_p / dw_p if (dw_p and np.isfinite(df_p)) else np.nan
        clos = ds_p * dw_p / (2 * df_p) if np.isfinite(ds_p * dw_p * df_p) else np.nan
        # plateau fiable : plat (std petit) ET diametre assez grand pour
        # separer le regime diffusif de la saturation de bord
        clean = (std_p < 0.04) and (diam >= 35)
        flag = "OUI" if clean else ("petit-N" if diam < 35 else "bruite")
        print(f"{N:>9,} {diam:>5} {df_p:>6.2f} {dw_p:>10.2f} {std_p:>6.3f} "
              f"{ds_p:>6.2f} {ds_kin:>7.2f} {clos:>6.3f}  {flag:>9}")
        rows.append(dict(N=N, d_f=df_p, d_w=dw_p, d_s=ds_p, closure=clos, clean=clean))

    # ---------- tendance de d_w (UNIQUEMENT points a plateau propre) ----------
    Ns = np.array([r["N"] for r in rows], float)
    dws = np.array([r["d_w"] for r in rows])
    dfs = np.array([r["d_f"] for r in rows])
    cln = np.array([r["clean"] for r in rows])
    print("\n--- TENDANCE de d_w (points a PLATEAU PROPRE seulement) ---")
    Nc, dwc = Ns[cln], dws[cln]
    if cln.sum() >= 2:
        order = np.argsort(Nc); Nc, dwc = Nc[order], dwc[order]
        print("  points fiables : " + ", ".join(f"N={int(n):,}:d_w={w:.2f}"
              for n, w in zip(Nc, dwc)))
        direction = "DECROIT" if dwc[-1] < dwc[0] - 0.02 else (
                    "CROIT" if dwc[-1] > dwc[0] + 0.02 else "STABLE")
        print(f"  direction : d_w {direction}  ({dwc[0]:.2f} -> {dwc[-1]:.2f})")
        if cln.sum() >= 4:
            # forme physique : (d_w - 2) decroit-il ? log(d_w-2) vs log N
            ex = (dwc - 2.0) > 0.02
            if ex.sum() >= 4:
                sl = np.polyfit(np.log(Nc[ex]), np.log(dwc[ex] - 2.0), 1)[0]
                if sl < -0.05:
                    print(f"  (d_w-2) decroit en N^{sl:.2f} -> RECOUVREMENT de variete (d_w->2).")
                else:
                    print(f"  (d_w-2) ~ plat -> ANOMALIE douce persistante (d_w->~{dwc[-1]:.2f}).")
        else:
            print(f"  {cln.sum()} point(s) propre(s) : il en faut >=4 (donc N>=100k) "
                  "pour extrapoler. NE PAS conclure encore.")
    else:
        print(f"  seulement {cln.sum()} plateau propre : pousser N (>=25k donne un plateau).")

    # ---------- figure ----------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        ax.plot(Ns, dfs, "ko-", label=r"$d_f$ (volume)")
        ax.plot(Ns, dws, "s-", color="C3", label=r"$d_w$ (plateau)")
        cln_=np.array([r["clean"] for r in rows]); ax.plot(Ns[cln_], dws[cln_], "s", color="C3", ms=11, mfc="none", mew=2, label="plateau propre")
        ax.plot(Ns, [r["d_s"] for r in rows], "^-", color="C0", label=r"$d_s$")
        ax.axhline(3, ls=":", c="g", lw=1, label="3 (variete)")
        ax.axhline(2, ls=":", c="r", lw=1, label="2 (diff. normale)")
        ax.set_xscale("log"); ax.set_xlabel("N"); ax.set_ylabel("dimension")
        ax.set_ylim(1.8, 3.4); ax.grid(alpha=.3); ax.legend()
        ax.set_title("Scaling robuste : d_w descend-il vers 2 (recouvrement) ?")
        plt.tight_layout(); plt.savefig("blob_reanalyse_scaling.png", dpi=120)
        print("\n[fig] blob_reanalyse_scaling.png")
    except Exception as ex:
        print(f"[fig] indisponible ({ex})")


if __name__ == "__main__":
    analyse(".")
