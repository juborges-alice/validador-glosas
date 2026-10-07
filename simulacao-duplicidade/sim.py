import csv,collections,statistics
R=list(csv.DictReader(open('d2.csv')))
f=lambda x: float(x) if x not in ('',None) else 0.0
for r in R:
    r['g']=f(r['g']); r['acc']=f(r['acc']); r['rec']=f(r['rec']); r['n']=int(f(r['n_dia'])); r['m']=r['dg'][:7]
    r['acat']=r['st'] in ('Autorizado','Autorizado Parcialmente'); r['pend']=r['st']=='Protocolado'
    if r['acat'] and r['acc']==0: r['acc']=r['rec']
acatv=sum(r['acc'] for r in R if r['acat']); anv=acatv+sum(r['rec'] for r in R if r['st']=='Negado')
taxa=acatv/anv
print('taxa acato valor', round(taxa,3))
def saving(r, exp=True):
    s=r['g']-r['acc']
    if exp and r['pend']: s-= min(r['rec'],r['g'])*taxa
    return s
G=sum(r['g'] for r in R); S=sum(saving(r) for r in R); Sk=sum(saving(r,False) for r in R)
print(f"glosado {G/1e3:.0f}k | saving conhecido {Sk/1e3:.0f}k | saving esperado (pendentes a {taxa:.0%}) {S/1e3:.0f}k | acatado {acatv/1e3:.0f}k")
by=collections.defaultdict(list)
for r in R: by[r['proc']].append(r)
def thr(rows, mode):
    ns=[r['n'] for r in rows if r['acat']]
    if not ns: return None
    if mode=='max': return max(ns)
    ns=sorted(ns); return ns[int(0.9*(len(ns)-1))]
for mode in ['max','p90']:
    T={p:thr(rows,mode) for p,rows in by.items()}
    inside=[r for r in R if T[r['proc']] is not None and r['n']<=T[r['proc']]]
    Gi=sum(r['g'] for r in inside); Si=sum(saving(r) for r in inside); Ski=sum(saving(r,False) for r in inside)
    reci=sum(1 for r in inside if r['rec']>0); itens=len(inside)
    procs_t=sum(1 for p in T if T[p] is not None)
    print(f"\n[{mode}] procs com teto {procs_t}/{len(T)} | deixa de glosar {itens} itens, R$ {Gi/1e3:.0f}k | saving perdido esperado R$ {Si/1e3:.0f}k (conhecido {Ski/1e3:.0f}k) | recursos evitados {reci} de {sum(1 for r in R if r['rec']>0)}")
    print(f"   novo saving esperado R$ {(S-Si)/1e3:.0f}k vs atual {S/1e3:.0f}k ({100*(S-Si)/S:.0f}% mantido)")
    # by month
    for m in ['2026-07','2026-08','2026-09']:
        rm=[r for r in R if r['m']==m]; im=[r for r in inside if r['m']==m]
        print('  ',m, f"glosa {sum(r['g'] for r in rm)/1e3:.0f}k saving {sum(saving(r) for r in rm)/1e3:.0f}k | dentro do teto {len(im)} itens glosa {sum(r['g'] for r in im)/1e3:.0f}k saving perdido {sum(saving(r) for r in im)/1e3:.0f}k")
# distribution of thresholds
T={p:thr(rows,'max') for p,rows in by.items()}
print('\nteto max dist', collections.Counter(T[p] for p in T if T[p]).most_common(12))
# top procs by glosa
print('\nTop procs: proc | nome | itens | glosa | acatado | teto max | p90 | glosa dentro teto | saving perdido')
agg=[]
for p,rows in by.items():
    t=T[p]; ins=[r for r in rows if t and r['n']<=t]
    agg.append((sum(r['g'] for r in rows),p,rows[0]['proc_name'][:35],len(rows),sum(r['acc'] for r in rows),t,thr(rows,'p90'),sum(r['g'] for r in ins),sum(saving(r) for r in ins), sum(saving(r) for r in rows)))
for a in sorted(agg,reverse=True)[:20]: print(a[1].strip(),'|',a[2],'|',a[3],'|',round(a[0]),'|',round(a[4]),'|',a[5],'|',a[6],'|',round(a[7]),'|',round(a[8]),'| saving total',round(a[9]))
# by provider
print('\nPor grupo (max): grupo | glosa | saving | dentro glosa | saving perdido')
pg=collections.defaultdict(lambda:[0,0,0,0])
for r in R:
    x=pg[r['grupo'].strip()]; x[0]+=r['g']; x[1]+=saving(r)
    t=T[r['proc']]
    if t and r['n']<=t: x[2]+=r['g']; x[3]+=saving(r)
for g,x in sorted(pg.items(), key=lambda z:-z[1][0])[:6]: print(g,[round(v/1e3) for v in x])
# by n_dia and acato
print('\nPor N no dia: N | itens | glosa | recursados | acatados | % acato (n)')
bn=collections.defaultdict(lambda:[0,0,0,0,0])
for r in R:
    k=min(r['n'],10); x=bn[k]; x[0]+=1; x[1]+=r['g']; x[2]+= r['rec']>0; x[3]+=r['acat']; x[4]+= r['st']=='Negado'
for k in sorted(bn): x=bn[k]; print(k, x[0], round(x[1]/1e3), x[2], x[3], f"{100*x[3]/max(x[3]+x[4],1):.0f}%")

print('\n================ cenarios alternativos')
def run(name, rule, rows=R):
    ins=[r for r in rows if rule(r)]
    S0=sum(saving(r) for r in rows); G0=sum(r['g'] for r in rows)
    Si=sum(saving(r) for r in ins); Gi=sum(r['g'] for r in ins)
    reci=sum(1 for r in ins if r['rec']>0); rect=sum(1 for r in rows if r['rec']>0)
    acc_i=sum(r['acc'] for r in ins); acc_t=sum(r['acc'] for r in rows)
    print(f"{name:42s} deixa de glosar {len(ins):5d} itens R$ {Gi/1e3:4.0f}k | saving perdido {Si/1e3:4.0f}k de {S0/1e3:4.0f}k ({100*Si/S0:3.0f}%) | recursos evitados {reci}/{rect} | acato evitado {acc_i/1e3:.0f}k de {acc_t/1e3:.0f}k")
# per-proc acato stats
st={}
for p,rows in by.items():
    a=sum(r['acc'] for r in rows if r['acat']); ng=sum(r['rec'] for r in rows if r['st']=='Negado')
    na=sum(1 for r in rows if r['acat']); nn=sum(1 for r in rows if r['st']=='Negado')
    st[p]=(a/(a+ng) if a+ng>0 else None, na+nn)
WL={p for p,(t,n) in st.items() if t is not None and t>=0.8 and n>=5}
print('procs whitelist', len(WL))
for rows,lab in [(R,'jul-set'),([r for r in R if r['m']=='2026-07'],'so julho (coorte madura)')]:
    print('---',lab)
    run('A) teto max por procedimento', lambda r: T[r['proc']] is not None and r['n']<=T[r['proc']], rows)
    run('B) teto max, mas sempre glosa N=2', lambda r: T[r['proc']] is not None and 3<=r['n']<=T[r['proc']], rows)
    run('C) tira da regra procs com acato>=80% (>=5)', lambda r: r['proc'] in WL, rows)
    run('D) C + so N>=3', lambda r: r['proc'] in WL and r['n']>=3, rows)
# N=2 vs within-item
print('\nN=2: itens_dia=1 (qtd 2 no mesmo item) vs itens_dia=2 (2 itens)')
for k in ['1','2']:
    rr=[r for r in R if r['n']==2 and r['itens_dia']==k]
    print(k, len(rr), round(sum(r['g'] for r in rr)/1e3), 'rec',sum(1 for r in rr if r['rec']>0),'acat',sum(r['acat'] for r in rr),'neg',sum(r['st']=='Negado' for r in rr))
