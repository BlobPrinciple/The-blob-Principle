exec(open('c64_defi.py').read().split('K4=[(0,1,2,3)]')[0])
print("--- Une seule lignee (branche jumelle de signe unique) ---")
for g in (0.5,1.5):
    cells=complex_from_max([(0,1,2,3)]); D,G,idx=ops(cells); S=polar(cells,{v:1 for v in range(4)})
    ev=np.linalg.eigvalsh(D+g*S@G); print(f"Tetraedre ++++ g={g}: modes nuls={int(np.sum(abs(ev)<1e-9))}, plus petite |valeur propre|={min(abs(ev)):.3f}")
print("--- Rencontre matiere / antimatiere ---")
m={i:(i+4)%8 for i in range(8)}
s8={**{i:1 for i in range(4)},**{i:-1 for i in range(4,8)}}
analyse("Tetra ++++ et tetra ---- relies par 1 arete",[(0,1,2,3),(4,5,6,7),(0,4)],s8,m)
analyse("Tetra ++++ et tetra ---- relies par 2 aretes",[(0,1,2,3),(4,5,6,7),(0,4),(1,5)],s8,m)
analyse("Tetra ++++ et tetra ---- separes",[(0,1,2,3),(4,5,6,7)],s8,m)
# contact par une face : les 3 porteurs de la face sont fixes par le miroir -> doivent etre neutres
s5={0:0,1:0,2:0,3:1,4:-1}
analyse("Bipyramide : face neutre 000, sommets + et -",[(0,1,2,3),(0,1,2,4)],s5,{0:0,1:1,2:2,3:4,4:3})
s5b={0:1,1:1,2:-1,3:1,4:-1}
analyse("Bipyramide sans porteurs neutres",[(0,1,2,3),(0,1,2,4)],s5b,None)
