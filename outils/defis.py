#!/usr/bin/env python3
"""Vérifie docs/defis.json et régénère le tableau d'état des défis
dans DEFIS.md (FR) et en/CHALLENGES.md (EN).

Usage :
  python3 outils/defis.py          # vérifie puis réécrit les tableaux
  python3 outils/defis.py --check  # vérifie seulement ; code 1 si un tableau est à régénérer

Seule la zone comprise entre les marqueurs ETAT-DEFIS est réécrite.
"""
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
JSON = RACINE / "docs" / "defis.json"
DEBUT = "<!-- ETAT-DEFIS:DEBUT (généré par outils/defis.py, ne pas modifier à la main) -->"
FIN = "<!-- ETAT-DEFIS:FIN -->"
ETAPES = {"P1", "P2", "P3", "P4", "T"}
ETAT_EN = {
    "ouvert": "open",
    "en cours": "in progress",
    "réplication obtenue": "replicated",
    "clos par une preuve": "closed by a proof",
    "clos par une réfutation": "closed by a refutation",
    "reformulé": "reformulated",
}


def verifier(d):
    erreurs = []
    if set(d.get("states", {})) != set(ETAT_EN):
        erreurs.append("la liste « states » ne correspond pas aux états connus du script")
    vus = set()
    for c in d["challenges"]:
        code = c.get("code", "?")
        if code in vus:
            erreurs.append(f"{code} : code en double")
        vus.add(code)
        if c.get("state") not in ETAT_EN:
            erreurs.append(f"{code} : état inconnu « {c.get('state')} »")
        if c.get("path_step") not in ETAPES:
            erreurs.append(f"{code} : étape du chemin inconnue « {c.get('path_step')} »")
        for h in c.get("history", []):
            for champ in ("date", "result", "effect"):
                if not h.get(champ):
                    erreurs.append(f"{code} : historique incomplet (champ « {champ} » manquant)")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", h.get("date", "")):
                erreurs.append(f"{code} : date d'historique mal formée")
        for x in c.get("derived", []):
            if x not in {k["code"] for k in d["challenges"]}:
                erreurs.append(f"{code} : défi dérivé inconnu {x}")
        if c["state"] != "ouvert" and not c.get("history"):
            erreurs.append(f"{code} : état « {c['state']} » sans historique qui le justifie")
    return erreurs


def tableau(d, langue):
    if langue == "fr":
        lignes = [f"*État au {d['updated']} — défis v{d['version']}.*", "",
                  "| Défi | Étape du chemin de preuve | État | Dernier événement |", "|---|---|---|---|"]
    else:
        lignes = [f"*Status as of {d['updated']} — challenges v{d['version']}.*", "",
                  "| Challenge | Proof-path step | State | Latest event |", "|---|---|---|---|"]
    for c in d["challenges"]:
        etat = c["state"] if langue == "fr" else ETAT_EN[c["state"]]
        h = c.get("history") or []
        if not h:
            dernier = "—"
        elif langue == "fr":
            dernier = f"{h[-1]['date']} : {h[-1]['result']}"
        else:
            dernier = f"{h[-1]['date']}: {h[-1].get('result_en', h[-1]['result'])}"
        lignes.append(f"| {c['code']} | {c['path_step']} | {etat} | {dernier} |")
    return "\n".join(lignes)


def injecter(chemin, contenu):
    texte = chemin.read_text(encoding="utf-8")
    motif = re.compile(re.escape(DEBUT) + r".*?" + re.escape(FIN), re.S)
    if not motif.search(texte):
        raise SystemExit(f"Marqueurs ETAT-DEFIS absents de {chemin}")
    return texte, motif.sub(lambda _: f"{DEBUT}\n{contenu}\n{FIN}", texte)


def main():
    controle = "--check" in sys.argv
    d = json.loads(JSON.read_text(encoding="utf-8"))
    erreurs = verifier(d)
    if erreurs:
        print("defis.json invalide :")
        print("\n".join(f"  - {e}" for e in erreurs))
        sys.exit(1)
    a_jour = True
    for chemin, langue in ((RACINE / "DEFIS.md", "fr"), (RACINE / "en" / "CHALLENGES.md", "en")):
        avant, apres = injecter(chemin, tableau(d, langue))
        if avant != apres:
            a_jour = False
            if not controle:
                chemin.write_text(apres, encoding="utf-8")
                print(f"{chemin.relative_to(RACINE)} : tableau régénéré")
    print(f"defis.json v{d['version']} valide : {len(d['challenges'])} défis.")
    if controle and not a_jour:
        print("Tableaux à régénérer : python3 outils/defis.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
