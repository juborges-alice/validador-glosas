import csv,collections
R=list(csv.DictReader(open('d3.csv')))
f=lambda x: float(x) if x not in ('',None) else 0.0
for r in R:
    r['g']=f(r['g']); r['acc']=f(r['acc']); r['rec']=f(r['rec']); r['n']=int(f(r['n_dia'])); r['m']=r['dg'][:7]
    r['acat']=r['st'] in ('Autorizado','Autorizado Parcialmente'); r['pend']=r['st']=='Protocolado'; r['neg']=r['st']=='Negado'
    if r['acat'] and r['acc']==0: r['acc']=r['rec']
acatv=sum(r['acc'] for r in R if r['acat']); taxa=acatv/(acatv+sum(r['rec'] for r in R if r['neg']))
def saving(r): return r['g']-r['acc']-(min(r['rec'],r['g'])*taxa if r['pend'] else 0)
print('taxa acato', round(taxa,3), '| status', collections.Counter(r['st'] or '(sem recurso)' for r in R))
print('\nPerfil por mes/codigo: mes | cod | itens | glosado | recursados | acatado R$ | saving')
pc=collections.defaultdict(lambda:[0,0,0,0,0])
for r in R:
    x=pc[(r['m'],r['cod'])]; x[0]+=1; x[1]+=r['g']; x[2]+=r['rec']>0; x[3]+=r['acc']; x[4]+=saving(r)
for k in sorted(pc): x=pc[k]; print(*k, x[0], round(x[1]/1e3,1), x[2], round(x[3]/1e3,1), round(x[4]/1e3,1))
print('\nPor N: N | itens | glosado | acatados | negados | % acato')
bn=collections.defaultdict(lambda:[0,0,0,0])
for r in R: x=bn[min(r['n'],10)]; x[0]+=1; x[1]+=r['g']; x[2]+=r['acat']; x[3]+=r['neg']
for k in sorted(bn): x=bn[k]; print(k,x[0],round(x[1]/1e3),x[2],x[3], f"{100*x[2]/max(x[2]+x[3],1):.0f}%")
by=collections.defaultdict(list)
for r in R: by[r['proc']].append(r)
T={p:(max([r['n'] for r in rows if r['acat']]) if any(r['acat'] for r in rows) else None) for p,rows in by.items()}
WL=set()
for p,rows in by.items():
    a=sum(r['acc'] for r in rows if r['acat']); ng=sum(r['rec'] for r in rows if r['neg']); n=sum(1 for r in rows if r['acat'] or r['neg'])
    if a+ng>0 and a/(a+ng)>=0.8 and n>=5: WL.add(p)
print('\nprocs', len(by), '| com teto', sum(1 for t in T.values() if t), '| whitelist D', len(WL))
def brk(name, rule):
    print(f"\n=== {name}")
    print('mes | itens deixa glosar | glosado | nao recursado (itens, R$) | acatado devolvido | negado | pendente | SAVING PERDIDO | saving total mes | recursos evitados')
    tot=[0]*9
    for m in ['2026-05','2026-06','2026-07','TOTAL']:
        rows=R if m=='TOTAL' else [r for r in R if r['m']==m]
        ins=[r for r in rows if rule(r)]
        nr=[r for r in ins if r['rec']<=0]
        v=[len(ins), sum(r['g'] for r in ins), len(nr), sum(r['g'] for r in nr), sum(r['acc'] for r in ins if r['acat']),
           sum(r['g'] for r in ins if r['neg']), sum(r['g'] for r in ins if r['pend']), sum(saving(r) for r in ins), sum(saving(r) for r in rows), sum(1 for r in ins if r['rec']>0), sum(1 for r in rows if r['rec']>0)]
        print(m, v[0], f"{v[1]/1e3:.1f}k", f"({v[2]}, {v[3]/1e3:.1f}k)", f"{v[4]/1e3:.1f}k", f"{v[5]/1e3:.1f}k", f"{v[6]/1e3:.1f}k", f"**{v[7]/1e3:.1f}k**", f"{v[8]/1e3:.1f}k ({100*v[7]/v[8]:.0f}%)", f"{v[9]}/{v[10]}")
    ins=[r for r in R if rule(r) and r['rec']<=0]
    gg=collections.defaultdict(float); pp=collections.defaultdict(lambda:[0,0.0,''])
    for r in ins: gg[r['grupo'].strip()]+=r['g']; x=pp[r['proc'].strip()]; x[0]+=1; x[1]+=r['g']; x[2]=r['proc_name'][:40]
    print('  nao recursado por grupo:', {k:round(v/1e3,1) for k,v in sorted(gg.items(), key=lambda z:-z[1])[:5]})
    for k,v in sorted(pp.items(), key=lambda z:-z[1][1])[:8]: print('   ',k,v[2],v[0],round(v[1]/1e3,1))
brk('D) procs com acato>=80% (>=5 analisados) e N>=3', lambda r: r['proc'] in WL and r['n']>=3)
brk('B) teto max por procedimento, N>=3', lambda r: T[r['proc']] is not None and 3<=r['n']<=T[r['proc']])
brk('N>=3 sem teto', lambda r: r['n']>=3)
