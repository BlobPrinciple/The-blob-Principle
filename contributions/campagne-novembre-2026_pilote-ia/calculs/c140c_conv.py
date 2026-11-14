# C-140c : d'ou vient l'ecart avec l'execution de ChatGPT sur le bras principal (heritage integral, file) ?
# ChatGPT : 407 porteurs, 403 naissances, 621 refus, 150 cellules, degre max 406.  Claude : 592, 588, 436, 61, degre max 7.
# Hypothese : convention d'evaluation des ruptures (point non fixe par le protocole pour les evenements de naissance).
#   A = a la fin de chaque evenement, sur tous les liens (convention declaree de Claude) ;
#   B = seulement aux evenements de refus, sur tous les liens ;
#   C = seulement aux evenements de refus, sur les seuls liens du porteur refuse.
import collections, itertools
src=open('c140c.py').read().split("if __name__=='__main__':")[0]
src=src.replace("def simulate(rebirth='F',","def simulate(conv='A',rebirth='F',")
src=src.replace("    def ruptures(ev):\n        nonlocal phase,frac_id,renew\n        brk=[e for e,x in w.items() if (x>=1 if wear=='Wmax' else x>=max(1,len(N[e[0]]&N[e[1]])))] if wear!='W0' else []",
                "    def ruptures(ev,who=None,blocked_ev=True):\n        nonlocal phase,frac_id,renew\n        if conv in ('B','C') and not blocked_ev: return\n        brk=[e for e,x in w.items() if (x>=1 if wear=='Wmax' else x>=max(1,len(N[e[0]]&N[e[1]]))) and (conv!='C' or who in e)] if wear!='W0' else []")
src=src.replace("""            if trap and incell[p]>0:
                st['blocked']+=1
                if wear!='W0':
                    for q in N[p]: w[key(p,q)]+=1; st['wearcum']+=1
                queue.append(p)
            else:
                z=do_birth(p,ev); queue.append(p)
                if z is None: st['eblocked']+=1
                else: queue.append(z); after_birth(z,ev)
            ruptures(ev)""","""            was_blocked=bool(trap and incell[p]>0)
            if was_blocked:
                st['blocked']+=1
                if wear!='W0':
                    for q in N[p]: w[key(p,q)]+=1; st['wearcum']+=1
                queue.append(p)
            else:
                z=do_birth(p,ev); queue.append(p)
                if z is None: st['eblocked']+=1
                else: queue.append(z); after_birth(z,ev)
            ruptures(ev,who=p,blocked_ev=was_blocked)""")
assert "conv!='C'" in src and "was_blocked" in src
ns={}; exec(src,ns)
for conv in 'ABC':
    r=ns['simulate'](conv=conv,rebirth='F'); s=r['series'][1024]
    print(f"convention {conv} : {s['N']} porteurs, {s['births']} naissances, {s['blocked']} refus, {s['cellules']} cellules, degré max {s['degmax']}, ruptures {s['fract']}, renouvellements {r['renouvellements']}")
