#!/usr/bin/env python3
"""C-174c bis -- COMPLEMENT DECLARE APRES COUP (Claude, 16 novembre 2026). Le seuil de << plancher actif >> de c174c.py (0,2 + 1e-6) etait faux : la relaxation
sous contrainte de C-155a tient le plancher a 0,2002 Vref, si bien que 27 etats a plancher actif ont ete classes << libres >> a tort. Meme programme, meme protocole,
seul changement : plancher actif si V/Vref < 0,2003. Sorties : c174c_bis_G_<debut>.jsonl, c174c_bis_synthese.json. Usage identique a c174c.py."""
import sys
src = open('c174c.py').read(); assert src.count('0.2 + TOL') == 1
src = src.replace('0.2 + TOL', '0.2003').replace('c174c_G_', 'c174c_bis_G_').replace('c174c_synthese', 'c174c_bis_synthese')
exec(compile(src, 'c174c_bis(c174c.py modifie)', 'exec'))
