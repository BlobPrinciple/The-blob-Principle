#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# BLOB-TOE C2-R — PRODUCTION AUTONOME (UN SEUL FICHIER, gel v4).
# ============================================================================
# Tout est DANS ce fichier : germe T3 de Freudenthal (construit et certifié en
# mémoire), moteur de secteur et légalité de Regina, moteur d'échange de
# répliques D8.7 (neuf réparations), génération des quatre banques de départs
# (VÉRIFIÉES contre les empreintes du gel v4 — refus si un octet diffère),
# superviseur blindé (générations tournantes, paliers immuables 100 k, journal
# append-only, restauration automatique), analyse canonique (R-chapeau de rang
# et replié en rangs moyens, ESS masse/queue, MCSE), contrat décisionnel C2-R
# gelé (marges incluses), et rapport G0 déterministe.
# Dépendance unique : numpy.  (L'inverse normal est celui d'Acklam, déclaré ;
# le second moteur refera l'analyse officielle sur les checkpoints renvoyés.)
#
# USAGE COLAB :
#   !python3 blob_c2r_autonome.py --selftest    # certifications avant tout
#   !python3 blob_c2r_autonome.py --all         # production : 4 systèmes
#   !python3 blob_c2r_autonome.py --system 2    # un seul système
#   !python3 blob_c2r_autonome.py --verify      # audit à froid
#   !python3 blob_c2r_autonome.py --finalize    # analyse -> décision -> rapport
# Relancer --all après toute coupure : reprise exacte, validée, automatique.
# INTERDIT en production : définir TEST_TARGET ; modifier ce fichier.
# ============================================================================
import argparse, hashlib, itertools, json, math, os, pickle, shutil
import subprocess, sys, time
import numpy as np

# ------------------------------- CONSTANTES GELÉES --------------------------
DSTAR   = 5.104299312119540
ALPHA, B = 0.4, 0.05
LADDER  = [2.6, 2.8, 3.0, 3.2, 3.4]
K       = 100
TARGET  = int(os.environ.get("TEST_TARGET", "1500000"))
CHUNK   = int(os.environ.get("CHUNK_WALL", "3300"))
MILESTONE = 100_000
GENS    = 3
BURN_STEPS, MEAS_STEPS = 300_000, 1_200_000
OBS     = ("N3", "I2", "Dbar", "S")
MARGINS = {"N3": 0.25, "I2": 0.00020, "Dbar": 0.010, "S": 0.60}
BANK_SHA = {1: "6cde4c16e47b057e232f99ccb5e1b09a3e75f9db9e1fc2e65f4f1e5e2a7e3035",
            2: "10bb282d9d44ac12b1738a1be2d7a2898c3021cb26d91db5f4235091261aaba5",
            3: "20959467cad16052bf45ea2d68daac657f5021069d50e2e29c39f3e9ec03c14b",
            4: "b9236fc6cf2aa7b672d20a3774f8c66aa3235e3cb6aa7122be24d480e8d6bb8d"}

def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b_ in iter(lambda: f.read(1 << 20), b""):
            h.update(b_)
    return h.hexdigest()

# ------------------------------- GERME T3 (Freudenthal, L=3) ----------------
GERM_TETS = [(14, 15, 17, 24), (16, 19, 20, 25), (17, 18, 20, 26), (9, 15, 17, 18), (2, 7, 8, 25), (4, 7, 21, 22), (9, 10, 13, 22), (2, 5, 19, 20), (13, 16, 17, 26), (1, 4, 5, 14), (0, 3, 18, 20), (3, 5, 20, 23), (0, 1, 10, 13), (5, 14, 15, 17), (6, 10, 15, 16), (0, 1, 6, 24), (15, 16, 19, 25), (6, 9, 10, 15), (4, 13, 16, 17), (3, 4, 7, 16), (1, 10, 11, 14), (15, 19, 24, 25), (5, 6, 8, 23), (0, 2, 9, 12), (11, 18, 20, 21), (3, 5, 6, 23), (0, 1, 4, 13), (0, 6, 9, 10), (2, 3, 5, 20), (7, 21, 22, 25), (3, 4, 7, 21), (10, 11, 20, 23), (9, 12, 21, 22), (9, 18, 21, 22), (9, 18, 19, 22), (5, 19, 22, 23), (0, 1, 4, 18), (17, 18, 24, 26), (6, 21, 23, 24), (12, 15, 24, 25), (0, 18, 24, 26), (10, 16, 19, 20), (1, 2, 11, 14), (11, 17, 18, 20), (0, 9, 12, 13), (0, 2, 3, 20), (10, 19, 20, 23), (12, 21, 24, 25), (1, 4, 5, 19), (3, 20, 21, 23), (3, 4, 13, 16), (6, 7, 10, 16), (1, 2, 7, 11), (1, 6, 7, 10), (6, 7, 21, 24), (11, 20, 21, 23), (6, 23, 24, 26), (10, 11, 16, 20), (9, 10, 15, 19), (5, 6, 8, 15), (4, 7, 8, 22), (0, 1, 18, 24), (1, 6, 7, 24), (3, 4, 18, 21), (15, 17, 18, 24), (10, 13, 22, 23), (9, 12, 13, 22), (2, 7, 8, 11), (4, 13, 14, 17), (8, 9, 11, 17), (7, 11, 16, 17), (14, 23, 24, 26), (7, 21, 24, 25), (3, 6, 21, 23), (10, 11, 14, 23), (2, 8, 9, 11), (3, 6, 7, 16), (9, 11, 12, 21), (12, 15, 16, 25), (11, 14, 21, 23), (4, 5, 19, 22), (4, 18, 19, 22), (0, 3, 12, 13), (4, 18, 21, 22), (1, 2, 5, 19), (7, 8, 11, 17), (13, 14, 23, 26), (0, 2, 3, 12), (16, 20, 25, 26), (3, 12, 15, 16), (13, 22, 25, 26), (12, 21, 22, 25), (3, 12, 13, 16), (1, 19, 24, 25), (1, 2, 5, 14), (4, 5, 8, 22), (9, 10, 19, 22), (4, 7, 8, 17), (12, 13, 22, 25), (0, 1, 6, 10), (13, 22, 23, 26), (1, 10, 13, 14), (3, 5, 12, 15), (9, 11, 17, 18), (12, 13, 16, 25), (1, 7, 10, 11), (2, 19, 20, 25), (13, 16, 25, 26), (1, 4, 18, 19), (9, 11, 18, 21), (1, 2, 19, 25), (2, 5, 12, 14), (2, 3, 5, 12), (2, 20, 25, 26), (2, 9, 11, 12), (1, 2, 7, 25), (0, 2, 20, 26), (1, 4, 13, 14), (16, 17, 20, 26), (12, 14, 21, 24), (11, 16, 17, 20), (15, 18, 19, 24), (8, 22, 25, 26), (0, 6, 8, 9), (2, 8, 25, 26), (3, 18, 20, 21), (12, 14, 15, 24), (8, 9, 15, 17), (14, 17, 24, 26), (1, 7, 24, 25), (7, 8, 22, 25), (10, 15, 16, 19), (10, 19, 22, 23), (1, 18, 19, 24), (5, 8, 15, 17), (0, 3, 4, 13), (7, 10, 11, 16), (5, 12, 14, 15), (0, 18, 20, 26), (3, 6, 15, 16), (6, 8, 9, 15), (4, 7, 16, 17), (13, 14, 17, 26), (6, 8, 23, 26), (0, 6, 8, 26), (0, 9, 10, 13), (5, 19, 20, 23), (0, 3, 4, 18), (14, 21, 23, 24), (0, 2, 8, 9), (8, 22, 23, 26), (3, 5, 6, 15), (4, 5, 14, 17), (2, 11, 12, 14), (11, 12, 14, 21), (0, 2, 8, 26), (9, 15, 18, 19), (10, 13, 14, 23), (4, 5, 8, 17), (5, 8, 22, 23), (0, 6, 24, 26), (3, 6, 7, 21)]

def build_germ():
    L = 3
    def vid(x, y, z): return (x % L) + L * ((y % L) + L * (z % L))
    tets = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for s in itertools.permutations(range(3)):
                    p = [[x, y, z]]
                    for k_ in s:
                        q = list(p[-1]); q[k_] += 1; p.append(q)
                    tets.add(frozenset(vid(*v) for v in p))
    return tets

def certify_germ(tets):
    assert len(tets) == 162, "germe : N3 != 162"
    V = set().union(*tets); assert len(V) == 27, "germe : N0 != 27"
    from collections import Counter
    qv = Counter(v for t in tets for v in t)
    assert set(qv.values()) == {24}, "germe : valences != 24"
    ne = {}
    for t in tets:
        for e in itertools.combinations(sorted(t), 2):
            ne[e] = ne.get(e, 0) + 1
    hist = Counter(ne.values())
    assert dict(hist) == {4: 81, 6: 108}, "germe : histogramme d'aretes inattendu"
    fc = Counter()
    for t in tets:
        for f in itertools.combinations(sorted(t), 3):
            fc[f] += 1
    assert set(fc.values()) == {2}, "germe : variete non fermee (faces != 2)"
    return True

# ------------------------------- MOTEUR DE SECTEUR (d70, embarqué) ----------
def build_maps(tets):
    faces, ne = {}, {}
    for t in tets:
        for f in itertools.combinations(sorted(t), 3):
            faces.setdefault(f, []).append(t)
        for e in itertools.combinations(sorted(t), 2):
            ne[e] = ne.get(e, 0) + 1
    from collections import Counter
    qv = Counter(v for t in tets for v in t)
    return faces, ne, qv

def legal_moves(tets, faces, ne):
    mv = []
    for f, ts in faces.items():
        if len(ts) != 2: continue
        a = next(iter(set(ts[0]) - set(f))); e = next(iter(set(ts[1]) - set(f)))
        if a == e: continue
        if tuple(sorted((a, e))) in ne: continue
        mv.append(("23", f, ts[0], ts[1], a, e))
    for e, c in ne.items():
        if c != 3: continue
        star = [t for t in tets if set(e) <= set(t)]
        link = set().union(*[set(t) - set(e) for t in star])
        if len(link) != 3: continue
        if tuple(sorted(link)) in faces: continue
        t1 = frozenset({e[0]} | link); t2 = frozenset({e[1]} | link)
        if t1 in tets or t2 in tets: continue
        mv.append(("32", e, tuple(star), t1, t2))
    return mv

def dS_of(kind, info, ne):
    def term(m): return -ALPHA * math.log(1 + m) + B * (m - DSTAR) ** 2
    from collections import Counter
    dS = 0.0
    if kind == "23":
        f, tA, tB, a, e = info
        dS += 3.0
        touched = Counter()
        for t in (tA, tB):
            for ed in itertools.combinations(sorted(t), 2): touched[ed] -= 1
        newt = [frozenset({a, e, x, y}) for x, y in itertools.combinations(sorted(f), 2)]
        for t in newt:
            for ed in itertools.combinations(sorted(t), 2): touched[ed] += 1
        for ed, d in touched.items():
            if d == 0: continue
            m = ne.get(ed, 0)
            dS += term(m + d) - (term(m) if m > 0 else 0.0)
        return dS
    else:
        e, star, t1, t2 = info
        dS -= 3.0
        touched = Counter()
        for t in star:
            for ed in itertools.combinations(sorted(t), 2): touched[ed] -= 1
        for t in (t1, t2):
            for ed in itertools.combinations(sorted(t), 2): touched[ed] += 1
        for ed, d in touched.items():
            if d == 0: continue
            m = ne.get(ed, 0); new = m + d
            dS += (term(new) if new > 0 else 0.0) - term(m)
        return dS

def apply_move(tets, faces, ne, qv, kind, info):
    if kind == "23":
        f, tA, tB, a, e = info
        rem = [tA, tB]
        add = [frozenset({a, e, x, y}) for x, y in itertools.combinations(sorted(f), 2)]
    else:
        e, star, t1, t2 = info
        rem = list(star); add = [t1, t2]
    for t in rem:
        tets.discard(t)
        for fc in itertools.combinations(sorted(t), 3):
            faces[fc].remove(t)
            if not faces[fc]: del faces[fc]
        for ed in itertools.combinations(sorted(t), 2):
            ne[ed] -= 1
            if ne[ed] == 0: del ne[ed]
        for v in t: qv[v] -= 1
    for t in add:
        tets.add(t)
        for fc in itertools.combinations(sorted(t), 3):
            faces.setdefault(fc, []).append(t)
        for ed in itertools.combinations(sorted(t), 2):
            ne[ed] = ne.get(ed, 0) + 1
        for v in t: qv[v] += 1
    return rem, add

def undo(tets, faces, ne, qv, rem, add):
    for t in add:
        tets.discard(t)
        for fc in itertools.combinations(sorted(t), 3):
            faces[fc].remove(t)
            if not faces[fc]: del faces[fc]
        for ed in itertools.combinations(sorted(t), 2):
            ne[ed] -= 1
            if ne[ed] == 0: del ne[ed]
        for v in t: qv[v] -= 1
    for t in rem:
        tets.add(t)
        for fc in itertools.combinations(sorted(t), 3):
            faces.setdefault(fc, []).append(t)
        for ed in itertools.combinations(sorted(t), 2):
            ne[ed] = ne.get(ed, 0) + 1
        for v in t: qv[v] += 1

# ------------------------------- BANQUES (génération vérifiée) --------------
def make_bank(sysid):
    out = "d87_bank_sys%d.pkl" % sysid
    if os.path.exists(out) and sha_file(out) == BANK_SHA[sysid]:
        return out
    rungs = []
    for r, mu in enumerate(LADDER):
        seed = int.from_bytes(hashlib.sha256(("D87BANK|%d|%d" % (sysid, r)).encode()).digest()[:8], "little")
        rng = np.random.default_rng(seed)
        tets = set(frozenset(x) for x in GERM_TETS)
        faces, ne, qv = build_maps(tets)
        mv = sorted(legal_moves(tets, faces, ne), key=lambda m: str(m))
        for step in range(12000):
            n = len(mv); k_ = rng.integers(n); kind, *info = mv[k_]
            # HISTORIQUE GELÉ : double application du décalage (module + script)
            # -> coefficient de volume effectif 2*mu-3 pour les PRÉ-RUNS seulement.
            dS = dS_of(kind, tuple(info), ne) + 2.0 * (mu - 3.0) * (+1 if kind == "23" else -1)
            rem, add = apply_move(tets, faces, ne, qv, kind, tuple(info))
            mv2 = sorted(legal_moves(tets, faces, ne), key=lambda m: str(m))
            if math.log(max(rng.random(), 1e-300)) < min(0.0, -dS + math.log(n) - math.log(max(len(mv2), 1))):
                mv = mv2
            else:
                undo(tets, faces, ne, qv, rem, add)
        rungs.append(sorted(tuple(sorted(t)) for t in tets))
        print("  banque s=%d r=%d mu=%s : N3 final = %d" % (sysid, r, mu, len(tets)), flush=True)
    pickle.dump({"system_id": sysid, "ladder": LADDER, "rungs": rungs,
                 "provenance": "pré-runs indépendants 12k pas, graine sha256(D87BANK|s|r), état FINAL exact"},
                open(out, "wb"))
    h = sha_file(out)
    if h != BANK_SHA[sysid]:
        sys.exit("REFUS : banque système %d régénérée avec empreinte %s != gel %s" % (sysid, h[:16], BANK_SHA[sysid][:16]))
    print("banque système %d : empreinte CONFORME au gel (%s…)" % (sysid, h[:16]))
    return out

# ------------------------------- MOTEUR D8.7 (échange de répliques) ---------
def _mvkey(m):
    kind = m[0]
    def nz(z):
        if isinstance(z, (frozenset, set)): return ("F", tuple(sorted(z)))
        if isinstance(z, tuple):
            parts = [nz(x) for x in z]
            if parts and all(p[0] == "F" for p in parts):
                return ("C", tuple(sorted(p[1] for p in parts)))
            return ("T", tuple(parts))
        return ("i", z)
    return (kind,) + tuple(nz(x) for x in m[1:])

def LM(tets, faces, ne):
    return sorted(legal_moves(tets, faces, ne), key=lambda m: str(_mvkey(m)))

def obs_of(tets, ne, qv):
    N3 = len(tets); N1 = len(ne)
    I2 = sum(q * q for q in qv.values()) / (16.0 * N3 * N3)
    Dbar = sum((m - DSTAR) ** 2 for m in ne.values()) / N1
    S = 3.0 * N3 - ALPHA * sum(math.log(1 + m) for m in ne.values()) + B * sum((m - DSTAR) ** 2 for m in ne.values())
    return (N3, float(I2), float(Dbar), float(S))

def cfg_of(sysid):
    return {"system_id": sysid, "ladder": LADDER, "K": K, "alpha": ALPHA, "b": B,
            "engine": "d87_replica.py", "seed_scheme": "sha256(D87|sys|ladder)"}

def run_engine(sysid, wall, ck_name=None):
    CFG = cfg_of(sysid)
    CFH = hashlib.sha256(json.dumps(CFG, sort_keys=True).encode()).hexdigest()
    CK = ck_name or ("d87_sys%d.pkl" % sysid)
    seed = int.from_bytes(hashlib.sha256(("D87|%d|" % sysid + ",".join(map(str, LADDER))).encode()).digest()[:8], "little")
    rng = np.random.default_rng(seed)
    nL = len(LADDER)
    if os.path.exists(CK):
        st = pickle.load(open(CK, "rb"))
        if st.get("cfg_hash") != CFH:
            raise RuntimeError("REFUS DE REPRISE : configuration incompatible")
        R = []
        for r in st["reps"]:
            tets = set(frozenset(t) for t in r)
            faces, ne, qv = build_maps(tets)
            R.append([tets, faces, ne, qv, LM(tets, faces, ne)])
        ident, done, samp = st["ident"], st["done"], st["samp"]
        pair, resid, track = st["pair"], st["resid"], st["track"]
        rng.bit_generator.state = st["rng"]
    else:
        bank = pickle.load(open(make_bank(sysid), "rb"))
        R = []
        for i, mu in enumerate(LADDER):
            tets = set(frozenset(t) for t in bank["rungs"][i])
            faces, ne, qv = build_maps(tets)
            R.append([tets, faces, ne, qv, LM(tets, faces, ne)])
        ident = list(range(nL))
        track = [{"pos": i, "phase": ("armed_low" if i == 0 else "idle"), "rt": 0} for i in range(nL)]
        done, samp, pair, resid = 0, [[] for _ in LADDER], np.zeros((nL - 1, 2)), np.zeros((nL, nL))
    t0 = time.time()
    def dump():
        payload = {"cfg": CFG, "cfg_hash": CFH,
                   "reps": [sorted(tuple(sorted(t)) for t in r[0]) for r in R],
                   "ident": ident, "done": done, "samp": samp, "pair": pair,
                   "resid": resid, "track": track, "rng": rng.bit_generator.state}
        tmp = CK + ".tmp"
        with open(tmp, "wb") as f:
            pickle.dump(payload, f); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, CK)
    while done < TARGET and time.time() - t0 < wall:
        for i, mu in enumerate(LADDER):
            tets, faces, ne, qv, mv = R[i]
            for _ in range(K):
                n = len(mv); k_ = rng.integers(n); kind, *info = mv[k_]
                dS = dS_of(kind, tuple(info), ne) + (mu - 3.0) * (+1 if kind == "23" else -1)
                rem, add = apply_move(tets, faces, ne, qv, kind, tuple(info))
                mv2 = LM(tets, faces, ne)
                if math.log(max(rng.random(), 1e-300)) < min(0.0, -dS + math.log(n) - math.log(max(len(mv2), 1))):
                    mv = mv2
                else:
                    undo(tets, faces, ne, qv, rem, add)
                R[i][4] = mv
            samp[i].append(obs_of(tets, ne, qv))
        for pos, idn in enumerate(ident):
            resid[idn, pos] += K
        par = (done // K) % 2
        for i in range(par, nL - 1, 2):
            Ni = len(R[i][0]); Nj = len(R[i + 1][0])
            loga = (LADDER[i] - LADDER[i + 1]) * (Ni - Nj)
            pair[i, 1] += 1
            if math.log(max(rng.random(), 1e-300)) < min(0.0, loga):
                pair[i, 0] += 1
                R[i], R[i + 1] = R[i + 1], R[i]
                ident[i], ident[i + 1] = ident[i + 1], ident[i]
        for pos, idn in enumerate(ident):
            tk = track[idn]; tk["pos"] = pos
            if tk["phase"] == "idle" and pos == 0: tk["phase"] = "armed_low"
            elif tk["phase"] == "armed_low" and pos == nL - 1: tk["phase"] = "went_high"
            elif tk["phase"] == "went_high" and pos == 0:
                tk["rt"] += 1; tk["phase"] = "armed_low"
        done += K
        if done % 4000 == 0: dump()
    dump()
    return done, pair, track

# ------------------------------- SUPERVISEUR BLINDÉ -------------------------
def log(sysid, **kw):
    kw.update(t=time.strftime("%Y-%m-%dT%H:%M:%S"), system=sysid)
    with open("heartbeat.jsonl", "a") as f:
        f.write(json.dumps(kw, sort_keys=True) + "\n")

def valid_ck(path, sysid=None, require_sidecar=False):
    try:
        st = pickle.load(open(path, "rb"))
        need = {"cfg", "cfg_hash", "done", "samp", "pair", "resid", "track", "ident", "reps", "rng"}
        assert need <= set(st)
        assert tuple(st["cfg"]["ladder"]) == tuple(LADDER)
        if sysid is not None:
            assert int(st["cfg"]["system_id"]) == sysid
        if require_sidecar:
            side = path + ".sha256"
            assert os.path.exists(side), "sidecar absent (génération)"
            assert open(side).read().strip() == sha_file(path), "sidecar divergent"
        return int(st["done"])
    except Exception as e:
        print("  checkpoint invalide (%s) : %s" % (path, e)); return None

def rotate(ck):
    open(ck + ".sha256", "w").write(sha_file(ck) + "\n")
    for g in range(GENS, 1, -1):
        a, b_ = ck + ".gen%d" % (g - 1), ck + ".gen%d" % g
        if os.path.exists(a):
            shutil.copy2(a, b_); shutil.copy2(a + ".sha256", b_ + ".sha256")
    shutil.copy2(ck, ck + ".gen1"); shutil.copy2(ck + ".sha256", ck + ".gen1.sha256")

def restore_if_needed(ck, sysid):
    if os.path.exists(ck) and valid_ck(ck, sysid) is not None: return
    for g in range(1, GENS + 1):
        cand = ck + ".gen%d" % g
        if os.path.exists(cand) and valid_ck(cand, sysid, require_sidecar=True) is not None:
            print("  RESTAURATION automatique depuis", cand)
            shutil.copy2(cand, ck); shutil.copy2(cand + ".sha256", ck + ".sha256")
            log(sysid, event="restore", source=cand)
            return
    if os.path.exists(ck):
        sys.exit("checkpoint irrécupérable, aucune génération valide : arrêt de sécurité")

def milestone(ck, done):
    m = (done // MILESTONE) * MILESTONE
    if m == 0: return
    tag = ck.replace(".pkl", "_m%07d.pkl" % m)
    if not os.path.exists(tag):
        shutil.copy2(ck, tag)
        open(tag + ".sha256", "w").write(sha_file(tag) + "\n")
        print("  palier immuable :", tag)

def run_system(sysid):
    ck = "d87_sys%d.pkl" % sysid
    restore_if_needed(ck, sysid)
    while True:
        done = valid_ck(ck, sysid) if os.path.exists(ck) else 0
        if done is None:
            restore_if_needed(ck, sysid); continue
        if done >= TARGET:
            print("système %d : TERMINÉ (%d pas)" % (sysid, done))
            log(sysid, done=done, status="DONE", ck_sha=sha_file(ck)); return
        t0 = time.time()
        try:
            d2, pair, track = run_engine(sysid, CHUNK)
        except Exception as e:
            print("  moteur : exception (%s) — validation puis reprise" % e)
            restore_if_needed(ck, sysid); continue
        restore_if_needed(ck, sysid)
        d2 = valid_ck(ck, sysid) or 0
        rotate(ck); milestone(ck, d2)
        log(sysid, done=d2, dt=round(time.time() - t0, 1),
            swaps=[[int(a), int(b_)] for a, b_ in pair],
            rt=[t["rt"] for t in track], ck_sha=sha_file(ck))
        print("système %d : %d / %d pas (tranche %.0f s)" % (sysid, d2, TARGET, time.time() - t0), flush=True)

# ------------------------------- ANALYSE (d88c, embarquée) ------------------
def _phi_inv(p):
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    bb=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    dd=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    pl=0.02425
    if p<pl:
        q=math.sqrt(-2*math.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1)
    if p>1-pl:
        q=math.sqrt(-2*math.log(1-p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((dd[0]*q+dd[1])*q+dd[2])*q+dd[3])*q+1)
    q=p-0.5; r=q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((bb[0]*r+bb[1])*r+bb[2])*r+bb[3])*r+bb[4])*r+1)

def rank_normalize(a):
    a=np.asarray(a,float); flat=a.ravel()
    order=np.argsort(flat,kind="mergesort"); r=np.empty(len(flat),float)
    i=0
    while i<len(flat):
        j=i+1
        while j<len(flat) and flat[order[j]]==flat[order[i]]: j+=1
        r[order[i:j]]=(i+j-1)/2.0
        i=j
    p=(r+1.0-3.0/8.0)/(len(flat)+0.25)
    z=np.array([_phi_inv(x) for x in p])
    return z.reshape(a.shape)

def split_chains(a):
    a=np.asarray(a,float); m,n=a.shape; h=n//2
    return np.concatenate([a[:,:h],a[:,n-h:]],axis=0)

def basic_rhat(a):
    x=split_chains(a); m,n=x.shape
    means=x.mean(axis=1); W=float(np.mean(np.var(x,axis=1,ddof=1))); Bv=float(n*np.var(means,ddof=1))
    if W==0: return 1.0 if Bv==0 else float("inf")
    return float(math.sqrt(((n-1)/n*W+Bv/n)/W))

def autocov_fft(x):
    x=np.asarray(x,float); n=len(x); x=x-x.mean()
    size=1<<(2*n-1).bit_length()
    f=np.fft.rfft(x,size); ac=np.fft.irfft(f*np.conjugate(f),size)[:n]
    return ac/np.arange(n,0,-1)

def ess(a):
    x=split_chains(a); m,n=x.shape
    if np.all(x==x.flat[0]): return float(m*n)
    ac=np.array([autocov_fft(c) for c in x])
    W=float(np.mean(np.var(x,axis=1,ddof=1))); Bv=float(n*np.var(x.mean(axis=1),ddof=1))
    var_plus=(n-1)/n*W+Bv/n
    if not np.isfinite(var_plus) or var_plus<=0: return float("nan")
    rho=np.ones(n)
    for t in range(1,n): rho[t]=1.0-(W-float(np.mean(ac[:,t])))/var_plus
    pairs=[]
    for t in range(1,n-1,2):
        p=rho[t]+rho[t+1]
        if p<0: break
        pairs.append(p)
    for i in range(1,len(pairs)):
        if pairs[i]>pairs[i-1]: pairs[i]=pairs[i-1]
    tau=max(-1.0+2.0*(1.0+sum(pairs)),1.0/(m*n))
    return float(min(m*n,m*n/tau))

def diagnostics(a):
    a=np.asarray(a,float)
    rr=basic_rhat(rank_normalize(a))
    med=float(np.median(a))
    fr=basic_rhat(rank_normalize(np.abs(a-med)))
    bulk=ess(rank_normalize(a))
    flat=a.ravel(); q05,q95=np.quantile(flat,[.05,.95])
    tail=min(ess((a<=q05).astype(float)),ess((a<=q95).astype(float)))
    raw=ess(a); sd=float(np.std(flat,ddof=1))
    mcse=sd/math.sqrt(raw) if raw>0 else float("inf")
    return dict(mean=float(np.mean(flat)),sd=sd,rank_Rhat=rr,folded_Rhat=fr,
                bulk_ESS=bulk,tail_ESS=tail,MCSE=mcse)

def analyse():
    cks=["d87_sys%d.pkl" % s for s in (1,2,3,4)]
    states=[]
    for p in cks:
        st=pickle.load(open(p,"rb"))
        if int(st["done"])<BURN_STEPS+MEAS_STEPS:
            sys.exit("analyse refusée : %s incomplet (done=%d)"%(p,st["done"]))
        states.append(st)
    burn_n,meas_n=BURN_STEPS//K,MEAS_STEPS//K
    res={"schema":"D88C_ANALYSIS_V1","ladder":LADDER,"systems":len(states),
         "burn_steps":BURN_STEPS,"measure_steps":MEAS_STEPS,"sample_stride":K,
         "rungs":{},"exchange":{},"residence":{},"round_trips":{}}
    for ri,mu in enumerate(LADDER):
        rd={}
        for oi,name in enumerate(OBS):
            chains=np.array([[row[oi] for row in s["samp"][ri][burn_n:burn_n+meas_n]] for s in states],float)
            rd[name]=diagnostics(chains)
        res["rungs"][str(mu)]=rd
    for si,s in enumerate(states,1):
        P=np.asarray(s["pair"],float)
        for i in range(len(LADDER)-1):
            res["exchange"]["sys%d:%s-%s"%(si,LADDER[i],LADDER[i+1])]={
                "accepted":int(P[i,0]),"attempted":int(P[i,1]),
                "rate":float(P[i,0]/P[i,1]) if P[i,1] else None}
    for si,s in enumerate(states,1):
        res["residence"][str(si)]=np.asarray(s["resid"]).tolist()
        res["round_trips"][str(si)]=[int(t["rt"]) for t in s["track"]]
    open("d88c_analysis_results.json","w").write(json.dumps(res,indent=2,sort_keys=True)+"\n")
    return res

# ------------------------------- DÉCISION (contrat D8.8D, embarqué) ---------
def decide(res):
    reasons=[]; fail=set()
    Tconv=0.0; Tess=float("inf")
    for mu in map(str,LADDER):
        rd=res["rungs"].get(mu)
        if rd is None or set(rd)!=set(OBS): return "INDECIDABLE",["barreau %s incomplet"%mu]
        for o in OBS:
            d=rd[o]
            Tconv=max(Tconv,d["rank_Rhat"],d["folded_Rhat"])
            Tess=min(Tess,d["bulk_ESS"],d["tail_ESS"])
            if d["rank_Rhat"]>=1.01 or d["folded_Rhat"]>=1.01: fail.add("FAIL_CONVERGENCE")
            if d["bulk_ESS"]<400 or d["tail_ESS"]<400: fail.add("FAIL_ESS")
            if d["MCSE"]>=0.05*d["sd"] or d["MCSE"]>=MARGINS[o]: fail.add("FAIL_MCSE")
    for k_,e in res["exchange"].items():
        if e["rate"] is None or not (0.15<=e["rate"]<=0.80):
            fail.add("FAIL_SANTE"); reasons.append("acceptation hors bande %s"%k_)
    for s,rts in res["round_trips"].items():
        if min(rts)<20: fail.add("FAIL_SANTE"); reasons.append("allers-retours<20 système %s"%s)
    for s,mat in res["residence"].items():
        for i,row in enumerate(mat):
            share=[c/max(sum(row),1) for c in row]
            if min(share)<0.05:
                fail.add("FAIL_SANTE"); reasons.append("résidence<5%% sys %s identité %d"%(s,i)); break
    for i in range(len(LADDER)-1):
        a,b_=LADDER[i],LADDER[i+1]
        Na=res["rungs"][str(a)]["N3"]; Nb=res["rungs"][str(b_)]["N3"]
        fd=(Nb["mean"]-Na["mean"])/(b_-a); vbar=(Na["sd"]**2+Nb["sd"]**2)/2
        tol=max(0.10*vbar,3*(Na["MCSE"]+Nb["MCSE"])/(b_-a))
        if abs(fd+vbar)>tol:
            fail.add("FAIL_SANTE")
            reasons.append("identité thermo violée %s-%s (fd=%.2f, -Var=%.2f, tol=%.2f)"%(a,b_,fd,-vbar,tol))
    reasons.insert(0,"T_conv=%.5f ; T_ess=%.1f"%(Tconv,Tess))
    return ("PASS" if not fail else "FAIL"), (reasons if not fail else sorted(fail)+reasons)

# ------------------------------- RAPPORT G0 (déterministe) ------------------
def report(res,verdict,reasons):
    L_=[]; A=L_.append
    A("# G0_REPORT — campagne C2-R (autonome, déterministe)"); A("")
    A("## Empreintes")
    A("- ce script : %s"%sha_file(__file__))
    A("- résultats : %s"%sha_file("d88c_analysis_results.json"))
    for s in (1,2,3,4):
        A("- d87_sys%d.pkl : %s"%(s,sha_file("d87_sys%d.pkl"%s)))
    A(""); A("## Paramètres gelés")
    A("- échelle %s ; K=%d ; rodage %d ; mesure %d ; marges %s"%(LADDER,K,BURN_STEPS,MEAS_STEPS,json.dumps(MARGINS)))
    A(""); A("## Diagnostics")
    A(""); A("| mu | obs | moyenne | sd | rank-Rhat | folded-Rhat | bulk ESS | tail ESS | MCSE |")
    A("|---|---|---|---|---|---|---|---|---|")
    for mu in map(str,LADDER):
        for o in OBS:
            d=res["rungs"][mu][o]
            A("| %s | %s | %.6g | %.4g | %.5f | %.5f | %.0f | %.0f | %.3g |"
              %(mu,o,d["mean"],d["sd"],d["rank_Rhat"],d["folded_Rhat"],d["bulk_ESS"],d["tail_ESS"],d["MCSE"]))
    A(""); A("## Santé")
    for k_,e in sorted(res["exchange"].items()):
        A("- paire %s : %.3f (%d/%d)"%(k_,e["rate"],e["accepted"],e["attempted"]))
    for s,r in sorted(res["round_trips"].items()):
        A("- système %s : allers-retours %s"%(s,r))
    A(""); A("## VERDICT C2-R : **%s**"%verdict)
    for r in reasons: A("- %s"%r)
    A(""); A("Portes physiques : 0/7 avant lecture ; seule l'application du contrat")
    A("gelé aux données ci-dessus peut faire évoluer C2-R. « TOE démontrée : NON ;")
    A("candidate digne d'étude : OUI. »")
    open("G0_REPORT.md","w",encoding="utf-8").write("\n".join(L_)+"\n")
    print("G0_REPORT.md :",sha_file("G0_REPORT.md"))

# ------------------------------- MODES --------------------------------------
def selftest():
    print("[1/4] germe : construction, certification, égalité au littéral embarqué…")
    G=build_germ(); certify_germ(G)
    assert G == set(frozenset(x) for x in GERM_TETS), "littéral du germe != construction"
    print("      PASS (N3=162, N0=27, q=24, {4:81,6:108}, fermée ; littéral == construction)")
    print("[2/4] banque système 1 : génération et empreinte contre le gel…")
    make_bank(1)
    print("[3/4] moteur : tranche courte + reprise identique…")
    global TARGET; old=TARGET; TARGET=2000
    for f in list(os.listdir(".")):
        if f.startswith("_selftest_"): os.remove(f)
    run_engine(1,600,ck_name="_selftest_cont.pkl"); a=pickle.load(open("_selftest_cont.pkl","rb"))
    TARGET=1000; run_engine(1,600,ck_name="_selftest_split.pkl")
    TARGET=2000; run_engine(1,600,ck_name="_selftest_split.pkl")
    b_=pickle.load(open("_selftest_split.pkl","rb"))
    assert a["reps"]==b_["reps"] and a["samp"]==b_["samp"] and a["ident"]==b_["ident"], "reprise non identique"
    assert (np.asarray(a["pair"])==np.asarray(b_["pair"])).all(), "pair divergent"
    assert (np.asarray(a["resid"])==np.asarray(b_["resid"])).all(), "resid divergent"
    assert a["track"]==b_["track"], "track divergent"
    assert json.dumps(a["rng"],sort_keys=True,default=str)==json.dumps(b_["rng"],sort_keys=True,default=str), "état RNG divergent"
    print("      PASS (états, échantillons, identités, paires, résidence, automate, RNG : identiques)")
    for f in ("_selftest_cont.pkl","_selftest_split.pkl"):
        if os.path.exists(f): os.remove(f)
    TARGET=old
    print("[4/4] décision : trois issues voulues sur cas synthétiques…")
    def mk(rhat=1.003,drop=None):
        means={2.6:152.0,2.8:148.4,3.0:144.8,3.2:141.2,3.4:137.6}
        R={"schema":"D88C_ANALYSIS_V1","ladder":LADDER,"rungs":{},"exchange":{},"residence":{},"round_trips":{}}
        for mu in LADDER:
            rd={}
            for o,(m,sd) in {"N3":(means[mu],18.0**0.5),"I2":(0.048,0.0026),"Dbar":(2.1,0.12),"S":(430.0,7.0)}.items():
                rd[o]={"mean":m,"sd":sd,"rank_Rhat":rhat,"folded_Rhat":rhat,"bulk_ESS":900.0,"tail_ESS":900.0,"MCSE":sd/40}
            R["rungs"][str(mu)]=rd
        for i in range(len(LADDER)-1):
            R["exchange"]["%s-%s"%(LADDER[i],LADDER[i+1])]={"accepted":500,"attempted":1000,"rate":0.5}
        for s in "1234":
            R["round_trips"][s]=[30,41,35,28,33]; R["residence"][s]=[[3000,2400,2400,2400,1800]]*5
        if drop: del R["rungs"][str(drop)]
        return R
    v1,_=decide(mk()); v2,_=decide(mk(rhat=1.024)); v3,_=decide(mk(drop=3.0))
    assert (v1,v2,v3)==("PASS","FAIL","INDECIDABLE"), (v1,v2,v3)
    print("      PASS (PASS / FAIL / INDECIDABLE voulus : 3/3)")
    print("SELFTEST : 4/4 — le fichier est autonome et conforme.")

def verify_all():
    import glob
    for f in sorted(glob.glob("d87_sys*_m*.pkl"))+sorted(glob.glob("d87_sys?.pkl")):
        side=f+".sha256"
        ok=os.path.exists(side) and open(side).read().strip()==sha_file(f)
        print("%-28s : sha %s | done=%s"%(f,"OK" if ok else "ABSENT/KO",valid_ck(f)))

def finalize():
    for s in (1,2,3,4):
        d=valid_ck("d87_sys%d.pkl"%s,s)
        if d is None or d<BURN_STEPS+MEAS_STEPS:
            sys.exit("finalisation refusée : système %d à %s pas"%(s,d))
    res=analyse()
    v,rs=decide(res)
    print("VERDICT C2-R :",v)
    for r in rs: print("  -",r)
    report(res,v,rs)
    for s in (1,2,3,4):
        print("SHA256 d87_sys%d.pkl"%s,sha_file("d87_sys%d.pkl"%s))


def _colab_bootstrap():
    try:
        ip = get_ipython()            # n'existe que dans un notebook
    except NameError:
        return False
    try:
        src = ip.history_manager.input_hist_raw[-1]
        if not src.strip().startswith("#!/usr/bin/env"):
            return False              # cellule partielle : laisser la voie CLI
        with open("blob_c2r_autonome.py", "w", encoding="utf-8") as f:
            f.write(src)
        import hashlib, subprocess
        h = hashlib.sha256(open("blob_c2r_autonome.py", "rb").read()).hexdigest()
        print("[COLAB] fichier auto-écrit : blob_c2r_autonome.py")
        print("[COLAB] empreinte sha256   :", h)
        if os.getcwd().startswith("/content") and "/drive/" not in os.getcwd():
            print("[COLAB] AVERTISSEMENT : répertoire éphémère. Pour survivre aux")
            print("        déconnexions : monter le Drive puis recoller la cellule :")
            print("          from google.colab import drive; drive.mount('/content/drive')")
            print("          %cd /content/drive/MyDrive")
        etats = {s: (valid_ck("d87_sys%d.pkl" % s, s) if os.path.exists("d87_sys%d.pkl" % s) else None)
                 for s in (1, 2, 3, 4)}
        deja = {s: d for s, d in etats.items() if d}
        if deja:
            print("[COLAB] REPRISE détectée :", ", ".join("sys%d=%d pas" % (s, d) for s, d in sorted(deja.items())))
            print("[COLAB] autotest sauté (aucun fichier de production n'est jamais touché).")
        else:
            print("[COLAB] première exécution — autotest sandboxé (2 à 4 minutes)…", flush=True)
            r = subprocess.run([sys.executable, "blob_c2r_autonome.py", "--selftest"])
            if r.returncode != 0:
                print("[COLAB] AUTOTEST EN ÉCHEC — production NON lancée ; renvoyer la sortie.")
                return True
        print("[COLAB] PRODUCTION — enchaînement automatique (reprise à chaque relance)…", flush=True)
        r = subprocess.run([sys.executable, "blob_c2r_autonome.py", "--all"])
        fini = all((valid_ck("d87_sys%d.pkl" % s, s) or 0) >= TARGET for s in (1, 2, 3, 4))
        if fini:
            print("[COLAB] quatre systèmes au but — FINALISATION automatique…", flush=True)
            subprocess.run([sys.executable, "blob_c2r_autonome.py", "--finalize"])
            print("")
            print("[COLAB] CAMPAGNE TERMINÉE. Fichiers à renvoyer pour contre-analyse :")
            print("        d87_sys1.pkl … d87_sys4.pkl, d88c_analysis_results.json, G0_REPORT.md")
        else:
            print("[COLAB] session interrompue avant le but — RECOLLER/RELANCER cette cellule :")
            print("        la campagne reprendra exactement où elle en est.")
        return True
    except Exception as e:
        print("[COLAB] bootstrap impossible (%s) — utiliser :  !python3 blob_c2r_autonome.py --selftest" % e)
        return True

def _run_cli():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true"); ap.add_argument("--all",action="store_true")
    ap.add_argument("--system",type=int); ap.add_argument("--verify",action="store_true")
    ap.add_argument("--finalize",action="store_true"); ap.add_argument("--smoke",action="store_true")
    a, _unknown = ap.parse_known_args()
    _unknown = [u for u in _unknown if u != "-f" and not u.endswith(".json")]
    if _unknown:
        print("arguments ignorés :", _unknown)
    try:
        print("blob_c2r_autonome.py — empreinte propre :",sha_file(__file__))
    except Exception:
        print("blob_c2r_autonome.py — collé en cellule : utiliser plutôt  !python3 blob_c2r_autonome.py --selftest")
    if a.selftest: selftest(); sys.exit(0)
    if os.environ.get("TEST_TARGET") and (a.all or a.system):
        sys.exit("REFUS : TEST_TARGET est INTERDIT avec --all/--system (production). Utiliser --smoke.")
    if a.smoke:
        TARGET, CHUNK = 9000, 35
        print("*** MODE SMOKE : cible 9000 pas, tranches 35 s — PAS UNE PRODUCTION ***")
        for f in list(os.listdir(".")):
            if f.startswith("_smoke_"): os.remove(f)
        make_bank(1)
        while True:
            d=valid_ck("_smoke_sys.pkl",1) if os.path.exists("_smoke_sys.pkl") else 0
            if d and d>=TARGET: break
            run_engine(1,CHUNK,ck_name="_smoke_sys.pkl")
            print("smoke :",valid_ck("_smoke_sys.pkl",1),"/",TARGET,"pas")
        st=pickle.load(open("_smoke_sys.pkl","rb"))
        assert st["done"]==9000, "smoke : cible non atteinte (boucle de restauration ?)"
        print("SMOKE : PASS — progression monotone multi-tranches jusqu'à la cible.")
        sys.exit(0)
    if a.verify: verify_all(); sys.exit(0)
    if a.finalize: finalize(); sys.exit(0)
    if a.all:
        for s in (1,2,3,4): make_bank(s)
        for s in (1,2,3,4): run_system(s)
    elif a.system:
        make_bank(a.system); run_system(a.system)
    else:
        print("Aucun mode demandé. Usage (dans une cellule Colab, avec le point")
        print("d'exclamation, le fichier étant sur le Drive ou téléversé) :")
        print("  !python3 blob_c2r_autonome.py --selftest")
        print("  !python3 blob_c2r_autonome.py --all")
        print("  !python3 blob_c2r_autonome.py --system N")
        print("  !python3 blob_c2r_autonome.py --verify")
        print("  !python3 blob_c2r_autonome.py --finalize")
        sys.exit(0)


if __name__=="__main__":
    if _colab_bootstrap():
        pass
    else:
        _run_cli()