#!/usr/bin/env python3
"""Vérification indépendante des scellés du Blob (Ronde n°1, 11 juillet 2026).
Usage : python3 verifier_scelles.py  (dans le dossier contenant les .md)
Recalcule les SHA-256 et les compare aux empreintes du Registre. Aucune dépendance externe."""
import hashlib, sys
ATTENDU = {
 "Blob_Scelles_Ronde1_11juillet.md":
   "8402a49fda0443490bf4d0e2a57683b4857fc2dc704ae150394a64be1a2ae369",
 "Blob_Kit_Brainstorm_MultiIA_11juillet.md":
   "22b936a3837fc60d34ecf02f8e934222ae3835b0d9bbd18d44d9ca5bc985c8b8",
 "Blob_Triage_Ronde_MultiIA_1_11juillet.md":
   "e9feec9075db65bb3c576bbed4c2919f0ac0b42081fed1ae662ecdd2030d23e1",
}
ok = True
for f, h in ATTENDU.items():
    try:
        calc = hashlib.sha256(open(f, "rb").read()).hexdigest()
    except FileNotFoundError:
        print(f"✗ ABSENT   {f}"); ok = False; continue
    if calc == h:
        print(f"✓ CONFORME {f}")
    else:
        print(f"✗ ALTÉRÉ   {f}\n    attendu  {h}\n    calculé  {calc}"); ok = False
sys.exit(0 if ok else 1)
