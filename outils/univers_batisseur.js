#!/usr/bin/env node
// Défi du Bâtisseur (DEFI-L5) : reproduit les chiffres publiés sur docs/univers.html et dans l'issue #33.
// Le moteur ci-dessous est identique à celui de la page (même générateur pseudo-aléatoire, mêmes règles).
// Usage :
//   node outils/univers_batisseur.js                 # tableau de réussite (k = 3, 4, 5) et record à k = 3
//   node outils/univers_batisseur.js 5215 3 1 80     # refait naître une graine : graine, fermeture, relaxation, taille
// Durée : quelques minutes pour le tableau complet.
// Moteur jouet du Blob : naissance d'un sommet (mitose + k arêtes de fermeture),
// puis relaxation par échanges d'arêtes à |E| fixé (Metropolis) sous
// pi_N ∝ exp(N·S_sim/τ), S_sim = log(1 + n_tri) − β·D, D = écart-type(deg)/moyenne(deg).
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

class Blob{
  constructor(seed,closure,sweeps,beta=0.30,tau=0.50){
    this.rng=mulberry32(seed>>>0);this.k=closure;this.sweeps=sweeps;this.beta=beta;this.tau=tau;
    this.adj=[new Set()];this.edges=[];this.ntri=0;this.t1=0;this.acc=0;this.prop=0;
  }
  get N(){return this.adj.length}
  get E(){return this.edges.length}
  common(a,b){const A=this.adj[a],B=this.adj[b];const[s,l]=A.size<B.size?[A,B]:[B,A];let c=0;for(const x of s)if(l.has(x))c++;return c}
  has(a,b){return this.adj[a].has(b)}
  addEdge(a,b){this.ntri+=this.common(a,b);this.adj[a].add(b);this.adj[b].add(a);this.edges.push(a<b?[a,b]:[b,a])}
  removeEdgeAt(i){const[a,b]=this.edges[i];this.adj[a].delete(b);this.adj[b].delete(a);this.ntri-=this.common(a,b);const last=this.edges.pop();if(i<this.edges.length)this.edges[i]=last}
  D(){const n=this.N;if(n===0)return NaN;let s=0,s2=0;for(const v of this.adj){s+=v.size;s2+=v.size*v.size}const m=s/n;if(m===0)return NaN;const varr=Math.max(0,s2/n-m*m);return Math.sqrt(varr)/m}
  S(){const d=this.D();return Math.log(1+this.ntri)-this.beta*(isNaN(d)?0:d)}
  // Naissance : mitose (un lien vers un sommet existant u) + jusqu'à k arêtes de fermeture vers des voisins de u.
  birth(){
    const n=this.N;this.adj.push(new Set());this.t1++;
    if(n===0)return; // ne devrait pas arriver
    const u=Math.floor(this.rng()*n);
    this.addEdge(n,u);
    const nb=[...this.adj[u]].filter(x=>x!==n);
    for(let j=0;j<this.k&&nb.length;j++){const i=Math.floor(this.rng()*nb.length);const w=nb.splice(i,1)[0];this.addEdge(n,w)}
  }
  // Un échange : retirer une arête au hasard, en proposer une absente au hasard ; Metropolis.
  swap(){
    const n=this.N;if(n<3||this.E===0)return;const maxE=n*(n-1)/2;if(this.E>=maxE)return;
    this.prop++;
    const i=Math.floor(this.rng()*this.E);const[a,b]=this.edges[i];
    let c,d,tries=0;do{c=Math.floor(this.rng()*n);d=Math.floor(this.rng()*n);tries++}while((c===d||this.has(c,d)||(c===a&&d===b)||(c===b&&d===a))&&tries<200);
    if(tries>=200)return;
    const S0=this.S();
    this.removeEdgeAt(i);this.addEdge(c,d);
    const dS=this.S()-S0;
    if(dS>=0||this.rng()<Math.exp(n*dS/this.tau)){this.acc++;return}
    // rejet : annuler
    const j=this.edges.length-1;this.removeEdgeAt(j);this.addEdge(a,b);
  }
  relax(){const m=Math.round(this.sweeps*this.E);for(let i=0;i<m;i++)this.swap()}
  step(){this.birth();this.relax()}
  components(){const n=this.N,seen=new Uint8Array(n);let c=0,iso=0;for(let s=0;s<n;s++){if(seen[s])continue;c++;if(this.adj[s].size===0)iso++;const st=[s];seen[s]=1;while(st.length){const x=st.pop();for(const y of this.adj[x])if(!seen[y]){seen[y]=1;st.push(y)}}}return{c,iso}}
  tetra(){let t=0;for(const[a,b]of this.edges){const cm=[];for(const x of this.adj[a])if(x>b&&this.adj[b].has(x))cm.push(x);for(let i=0;i<cm.length;i++)for(let j=i+1;j<cm.length;j++)if(this.adj[cm[i]].has(cm[j]))t++}return t}
  bruteTri(){let t=0;for(const[a,b]of this.edges)for(const x of this.adj[a])if(x>b&&this.adj[b].has(x))t++;return t}
}

function run(seed,k,sw,n){const b=new Blob(seed,k,sw);for(let i=1;i<n;i++)b.step();return b}
const a=process.argv.slice(2).map(Number);
if(a.length>=1){
  const [seed,k=2,sw=1,n=80]=a;const b=run(seed,k,sw,n);const c=b.components();
  console.log(`graine ${seed}, fermeture ${k}, relaxation ${sw}, N = ${b.N}`);
  console.log(`arêtes ${b.E} · triangles ${b.ntri} · tétraèdres ${b.tetra()} · morceaux ${c.c} (${c.iso} isolés) · D = ${b.D().toFixed(4)} · S_sim = ${b.S().toFixed(4)}`);
  console.log(c.c===1&&b.D()<0.5?'défi du Bâtisseur : réussi':'défi du Bâtisseur : non réussi');
}else{
  const plan=[[5,1,300,s=>s*13],[4,1,400,s=>s*31+7],[3,0,400,s=>s*31+7],[3,0.5,400,s=>s*31+7],[3,1,400,s=>s*31+7],[3,2,400,s=>s*31+7],[3,3,400,s=>s*31+7],[3,4,400,s=>s*31+7]];
  let best=[9,0,0];
  for(const [k,sw,m,g] of plan){let w=0;for(let s=1;s<=m;s++){const b=run(g(s),k,sw,80);const c=b.components().c,D=b.D();if(c===1&&D<0.5)w++;if(k===3&&c===1&&D<best[0])best=[D,g(s),sw]}
    console.log(`fermeture ${k}, relaxation ${sw} : ${w}/${m} univers d'un seul tenant avec D < 0,50`)}
  console.log(`record à fermeture 3 : D = ${best[0].toFixed(4)}, graine ${best[1]}, relaxation ${best[2]}`);
}
