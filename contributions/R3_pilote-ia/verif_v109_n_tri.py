#!/usr/bin/env python3
"""Contrôle du comptage incrémental des triangles dans le moteur MCMC « V109 »
imprimé dans le master V346 (p. 291–292 imprimées, p. 339–340 du PDF).

Pilote IA du laboratoire (Claude, Anthropic), 15 octobre 2026.

Le script extrait le listage du PDF (pdftotext requis), l'exécute tel quel (seule
l'impression de progression, tronquée par la mise en page, est retirée), puis compare
le n_tri suivi pas à pas au nombre de triangles recompté sur le graphe final.
Usage : python3 verif_v109_n_tri.py
"""
import importlib.util, pathlib, re, subprocess, sys, tempfile
RACINE = pathlib.Path(__file__).resolve().parents[2]
PDF = RACINE / "corpus" / "00_master_courant" / "BLOB_PRINCIPLE_MASTER_V346_complet.pdf"

txt = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], capture_output=True, text=True).stdout
i = txt.find("KAPPA0 = 8\nBETA = 0.30"); j = txt.find("# =============== d_h via BFS", i)
code = re.sub(r"\n\s*\n\s*\d{3}\s*\n", "\n", txt[i:j]).replace("for \\_ in", "for _ in")
a = code.index("        if verbose and"); b = code.index("    return adj, n_tri, n_accept")
code = ("import numpy as np\nfrom scipy.special import gamma as gamma_func\n"
        "from scipy.spatial import distance_matrix\n") + code[:a] + code[b:]
tmp = pathlib.Path(tempfile.mkdtemp()) / "v109_extrait.py"; tmp.write_text(code)
spec = importlib.util.spec_from_file_location("v109", tmp); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for N, steps in ((300, 20000), (500, 50000)):
    for seed in range(3):
        adj, nt, acc = m.run_mcmc_fast(N, 3, seed, steps)
        vrai = m.count_triangles_full(adj)
        print(f"N={N} graine={seed} n_tri suivi={nt} recompté={vrai} écart={nt - vrai:+d} "
              f"({100 * (nt - vrai) / vrai:+.1f} %) acceptés={acc}")
