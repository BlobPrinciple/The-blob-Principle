# Reprise de la graine 1322 du bras P (C-132 bis), interrompue par la limite de temps du premier lancement. Meme code, meme graine.
import c132_audit as A
def show(r):
    print(f'P graine 1322 n={r["n"]:3d} cellules={r["N3"]:4d} V/V0={r["Vratio"]:8.3f} V/cellule={r["Vcell"]:.3f} diam={r["diam"]:.3f} fondateurs moy×{r["fmoy"]:.3f} max×{r["fmax"]:.3f} E={r["E"]:.4f} E/fil={r["E_par_fil"]:.4f} activation cumulée={r["cum"]:.3f} qmin={r["qmin"]:.4f} q10%={r["q10"]:.3f} qméd={r["qmed"]:.3f} degré max={r["degmax"]} L∈[{r["Lmin"]:.2f},{r["Lmax"]:.2f}] au contact={r["nact"]} V/Vref min={r["ratio"]:.3f} grad max={r["gmax"]:.1e} fil le plus long du patch={100*r["part_long"]:.0f} %',flush=True)
A.HOOK=show
rows,_=A.run('P',1322,127)
if rows and rows[-1]['statut']!='ok': print('P graine 1322 :',rows[-1],flush=True)
