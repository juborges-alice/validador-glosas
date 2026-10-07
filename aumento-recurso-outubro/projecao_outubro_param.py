import csv, datetime as dt, collections, sys
D=lambda s: dt.date.fromisoformat(s[:10])
A=[(r['grp'].strip(),r['tipo'].strip(),D(r['dg']),int(r['lag']),int(r['itens']),float(r['recursado'] or 0)) for r in csv.DictReader(open(FA))]
B=[(r['grp'].strip(),r['tipo'].strip(),D(r['dg']),int(r['itens']),float(r['glosado'])) for r in csv.DictReader(open(FB))]
MAXL=180
def project(T, E, verbose=False):
    # history known at T
    Bt=[b for b in B if b[2]<=T]; At=[a for a in A if a[2]+dt.timedelta(a[3])<=T]
    gtot=collections.Counter(); 
    for g,t,d,n,v in Bt: gtot[g]+=v
    tipo_of={}
    for g,t,d,n,v in Bt: tipo_of[g]=t
    key=lambda g: g if gtot[g]>=THR else 'POOL_'+tipo_of[g]
    # at-risk denominators by key & age
    den_v=collections.defaultdict(lambda:[0.0]*(MAXL+1)); den_n=collections.defaultdict(lambda:[0.0]*(MAXL+1))
    for g,t,d,n,v in Bt:
        age=min((T-d).days,MAXL); k=key(g)
        for a in range(age+1): den_v[k][a]+=v; den_n[k][a]+=n
    num_v=collections.defaultdict(lambda:[0.0]*(MAXL+1)); num_n=collections.defaultdict(lambda:[0.0]*(MAXL+1))
    for g,t,d,l,n,r in At:
        if l>MAXL: continue
        k=key(g); num_v[k][l]+=r; num_n[k][l]+=n
    F={}
    for k in den_v:
        cv=cn=0; fv=[];fn=[]
        for a in range(MAXL+1):
            if den_v[k][a]>0: cv+=num_v[k][a]/den_v[k][a]
            if den_n[k][a]>0: cn+=num_n[k][a]/den_n[k][a]
            fv.append(cv); fn.append(cn)
        F[k]=(fv,fn)
    f=lambda k,a,i: F[k][i][min(max(a,0),MAXL)]
    # recursed so far per group-cohort-month
    got=collections.defaultdict(lambda:[0.0,0.0])
    for g,t,d,l,n,r in At: got[(g,d.strftime('%Y-%m'))][0]+=r; got[(g,d.strftime('%Y-%m'))][1]+=n
    coh=collections.defaultdict(lambda:[0.0]*6) # G, N, Fnow_v*G, Fend_v*G, Fnow_n*N, Fend_n*N
    for g,t,d,n,v in Bt:
        k=key(g); c=coh[(g,d.strftime('%Y-%m'))]
        an=(T-d).days; ae=(E-d).days
        c[0]+=v;c[1]+=n;c[2]+=v*f(k,an,0);c[3]+=v*f(k,ae,0);c[4]+=n*f(k,an,1);c[5]+=n*f(k,ae,1)
    out=collections.defaultdict(lambda:[0.0,0.0])
    for (g,m),c in coh.items():
        if c[0]<=0: continue
        av=got[(g,m)][0]/c[0]; an_=got[(g,m)][1]/max(c[1],1)
        addv=c[0]*max(0,c[3]/c[0]-max(c[2]/c[0],av)); addn=c[1]*max(0,c[5]/c[1]-max(c[4]/c[1],an_))
        out[(g,tipo_of[g],m)][0]+=addv; out[(g,tipo_of[g],m)][1]+=addn
    # new glosas between T+1 and E, at average daily rate of last 92 days
    s=T-dt.timedelta(92); rate=collections.defaultdict(lambda:[0.0,0.0])
    for g,t,d,n,v in Bt:
        if d>s: rate[g][0]+=v/92; rate[g][1]+=n/92
    for g,(rv,rn) in rate.items():
        k=key(g); days=(E-T).days
        sv=sum(f(k,(E-(T+dt.timedelta(i))).days,0) for i in range(1,days+1))
        sn=sum(f(k,(E-(T+dt.timedelta(i))).days,1) for i in range(1,days+1))
        out[(g,tipo_of[g],'novas')][0]+=rv*sv; out[(g,tipo_of[g],'novas')][1]+=rn*sn
    return out
def actual(T,E):
    o=collections.defaultdict(lambda:[0.0,0.0])
    for g,t,d,l,n,r in A:
        dr=d+dt.timedelta(l)
        if T<dr<=E: o[(g,t)][0]+=r; o[(g,t)][1]+=n
    return o
if __name__=='__main__':
    for T,E in [('2026-07-06','2026-07-31'),('2026-08-06','2026-08-31'),('2026-09-06','2026-09-30'),('2026-10-06','2026-10-31')]:
        T,E=D(T),D(E); p=project(T,E); a=actual(T,E)
        pv=sum(v[0] for v in p.values()); pn=sum(v[1] for v in p.values())
        av=sum(v[0] for v in a.values()); an=sum(v[1] for v in a.values())
        print(T,E,'proj R$%.0fk itens %.0f | real R$%.0fk itens %.0f'%(pv/1e3,pn,av/1e3,an))
