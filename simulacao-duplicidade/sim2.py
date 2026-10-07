exec(open('sim.py').read().split("print('\\n================ cenarios")[0].replace("print(","(lambda *a,**k:None)("))
st={}
for p,rows in by.items():
    a=sum(r['acc'] for r in rows if r['acat']); ng=sum(r['rec'] for r in rows if r['st']=='Negado')
    st[p]=(a/(a+ng) if a+ng>0 else None, sum(1 for r in rows if r['acat'] or r['st']=='Negado'))
WL={p for p,(t,n) in st.items() if t is not None and t>=0.8 and n>=5}
def brk(name, rule, rows):
    ins=[r for r in rows if rule(r)]
    def s(sel): x=[r for r in ins if sel(r)]; return len(x), sum(r['g'] for r in x), sum(r['acc'] for r in x)
    tot=s(lambda r: True)
    nr=s(lambda r: r['rec']<=0); ac=s(lambda r: r['acat']); ng=s(lambda r: r['st']=='Negado'); pe=s(lambda r: r['pend'])
    pend_keep=sum(min(r['rec'],r['g'])*(1-taxa)+(r['g']-min(r['rec'],r['g'])) for r in ins if r['pend'])
    print(f"\n{name}: {tot[0]} itens, glosado R$ {tot[1]/1e3:.1f}k")
    print(f"  nao recursado (glosa que ficou): {nr[0]} itens R$ {nr[1]/1e3:.1f}k")
    print(f"  recursado e acatado: {ac[0]} itens glosa R$ {ac[1]/1e3:.1f}k, devolvido R$ {ac[2]/1e3:.1f}k -> ficou R$ {(ac[1]-ac[2])/1e3:.1f}k")
    print(f"  recursado e negado: {ng[0]} itens R$ {ng[1]/1e3:.1f}k")
    print(f"  recurso pendente: {pe[0]} itens R$ {pe[1]/1e3:.1f}k (esperado ficar R$ {pend_keep/1e3:.1f}k)")
    lost=nr[1]+(ac[1]-ac[2])+ng[1]+pend_keep
    print(f"  => saving que deixaria de existir: R$ {lost/1e3:.1f}k")
    top=collections.defaultdict(lambda:[0,0,0])
    for r in ins:
        if r['rec']<=0: x=top[(r['proc'].strip(),r['proc_name'][:40])]; x[0]+=1; x[1]+=r['g']
    for k,v in sorted(top.items(), key=lambda z:-z[1][1])[:8]: print('    nao recursado:',k, v[0], round(v[1]))
    gg=collections.defaultdict(float)
    for r in ins:
        if r['rec']<=0: gg[r['grupo'].strip()]+=r['g']
    print('    por grupo (nao recursado):', {k:round(v/1e3,1) for k,v in sorted(gg.items(), key=lambda z:-z[1])[:4]})
J=[r for r in R if r['m']=='2026-07']
print('Julho total 7G4: itens',len(J),'glosado',round(sum(r['g'] for r in J)/1e3,1),'k')
brk('D) procs com acato>=80% e N>=3', lambda r: r['proc'] in WL and r['n']>=3, J)
brk('B) teto max por procedimento, N>=3', lambda r: T[r['proc']] is not None and 3<=r['n']<=T[r['proc']], J)
brk('N>=3 sem teto (tudo)', lambda r: r['n']>=3, J)
