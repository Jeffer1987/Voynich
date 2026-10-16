# Wave 4A tests 1(detail),4,5 + cross-transcription. usage: python -I m4b.py zl3b|rf1b B
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from m4_common import *
name=sys.argv[1];B=int(sys.argv[2]);rng=np.random.default_rng(2)
L=load(name);P=cont(L)
print('==',name)
def stem(w):
    g=glyphs(w);return ''.join(g[:-1]),g[-1]
# ---- T1c: allograph determinism among l/r/m
cnt=C.defaultdict(lambda:C.Counter())
for l in P:
    w=l['words']
    for i,x in enumerate(w):
        s,e=stem(x)
        if e in 'lrm':cnt[(s,'F' if i==len(w)-1 else 'M' if i>0 else 'I')][e]+=1
stems=set(s for s,_ in cnt)
tf=C.Counter();tm=C.Counter()
for (s,p),c in cnt.items():
    if p=='F':tf.update(c)
    if p=='M':tm.update(c)
print('T1c among words ending l/r/m: final share m=%.3f l=%.3f r=%.3f ; mid share m=%.3f l=%.3f r=%.3f'%tuple([tf[e]/sum(tf.values()) for e in 'mlr']+[tm[e]/sum(tm.values()) for e in 'mlr']))
# by penultimate glyph of stem
pg=C.defaultdict(lambda:[0,0,0,0])
for (s,p),c in cnt.items():
    g=glyphs(s);k=g[-1] if g else '^'
    if p=='F':pg[k][0]+=c['m'];pg[k][1]+=sum(c.values())
    if p=='M':pg[k][2]+=c['m'];pg[k][3]+=sum(c.values())
print('   share of -m among l/r/m endings by preceding glyph (final | mid): ')
for k,v in sorted(pg.items(),key=lambda kv:-kv[1][1])[:8]:print('    %s: %.2f (n=%d) | %.3f (n=%d)'%(k,v[0]/max(v[1],1),v[1],v[2]/max(v[3],1),v[3]))
# stem-level overdispersion: stems with >=6 final tokens ending l/r/m
fs=[(s,c['m'],sum(c.values())) for (s,p),c in cnt.items() if p=='F' and sum(c.values())>=6]
pm=sum(a for _,a,_ in fs)/sum(n for _,_,n in fs)
obsv=np.var([a/n for _,a,n in fs]);nulls=[]
for b in range(B):
    nulls.append(np.var([rng.binomial(n,pm)/n for _,_,n in fs]))
print('   stems n=%d: per-stem final m-share variance %.4f vs binomial null %.4f (sd %.4f) z=%.1f ; pooled share %.2f'%(len(fs),obsv,np.mean(nulls),np.std(nulls),(obsv-np.mean(nulls))/np.std(nulls),pm))
print('   histogram of per-stem m-share:',np.histogram([a/n for _,a,n in fs],bins=[0,.01,.2,.4,.6,.8,1.01])[0])
# ---- T4 line-initial
init=[l['words'][0] for l in P];midw=[w for l in P for w in l['words'][1:-1]]
midset=C.Counter(midw)
print('T4 line-initial word strip test (remainder attested as a mid-line word type)')
print('   glyph | init rate | init attested | mid attested (same first glyph, same length) | n_init')
for g in ['y','d','t','p','s','o','q','k','c','l','a']:
    ii=[w for w in init if first(w)==g and len(glyphs(w))>=3]
    mm=[w for w in midw if first(w)==g and len(glyphs(w))>=3]
    rem=lambda w:''.join(glyphs(w)[1:])
    a=np.mean([midset[rem(w)]>0 for w in ii]) if ii else float('nan')
    # null: mid-line words w/ same first glyph and length distribution, excluding self-match
    ml=C.Counter(len(glyphs(w)) for w in ii)
    pool=C.defaultdict(list)
    for w in mm:pool[len(glyphs(w))].append(w)
    nl=[]
    for b in range(min(B,200)):
        xs=[]
        for k,n in ml.items():
            if pool[k]:
                for j in rng.integers(0,len(pool[k]),n):
                    w=pool[k][j];c=midset[rem(w)]
                    xs.append(c>0)
        nl.append(np.mean(xs))
    print('   %s | %.3f | %.3f | %.3f (sd %.3f) z=%+.1f | %d'%(g,np.mean([first(w)==g for w in init]),a,np.mean(nl),np.std(nl),(a-np.mean(nl))/np.std(nl),len(ii)))
# length of line-initial words, excluding prefix glyph
print('   word length (glyphs): init vs mid by first glyph; init remainder after stripping first glyph')
for g in ['y','d','t','p','s','o','q','k','c','l']:
    ii=[len(glyphs(w)) for w in init if first(w)==g];mm=[len(glyphs(w)) for w in midw if first(w)==g]
    print('    %s: init %.2f mid %.2f diff %+.2f z=%.1f (n=%d,%d)'%(g,np.mean(ii),np.mean(mm),np.mean(ii)-np.mean(mm),(np.mean(ii)-np.mean(mm))/np.sqrt(np.var(ii)/len(ii)+np.var(mm)/len(mm)),len(ii),len(mm)))
li=[len(glyphs(w)) for w in init];lm=[len(glyphs(w)) for w in midw]
print('   all: init %.2f mid %.2f; init excl y/d/t/p %.2f vs mid excl same %.2f'%(np.mean(li),np.mean(lm),np.mean([len(glyphs(w)) for w in init if first(w) not in 'ydtp']),np.mean([len(glyphs(w)) for w in midw if first(w) not in 'ydtp'])))
# do initial-slot words come from a distinct vocabulary? fraction of init tokens whose type seen mid-line
print('   init tokens whose exact type occurs mid-line: %.2f ; last-word tokens: %.2f ; mid tokens (leave-one-out) : %.2f'%(
    np.mean([midset[w]>0 for w in init]),np.mean([midset[l['words'][-1]]>0 for l in P]),np.mean([midset[w]>1 for w in midw])))
# strip y/d prefix: then normalised init remainder matches the mid distribution? chi-square on first glyph of remainder
rem1=C.Counter(first(''.join(glyphs(w)[1:])) for w in init if first(w) in 'yd' and len(glyphs(w))>1)
rem0=C.Counter(first(w) for w in midw)
ks=sorted(set(rem1)|set(rem0));
obs=np.array([rem1[k] for k in ks],float);exp=np.array([rem0[k] for k in ks],float);exp=exp/exp.sum()*obs.sum()
print('   first glyph of remainder after stripping y/d vs first glyph of mid words: chi2 p (cells>=5)=%.3g'%stats.chisquare(obs[exp>=5],exp[exp>=5]*obs[exp>=5].sum()/exp[exp>=5].sum()).pvalue)
print('   top remainder first glyphs:',[(k,round(rem1[k]/sum(rem1.values()),2),round(rem0[k]/sum(rem0.values()),2)) for k in sorted(ks,key=lambda k:-rem1[k])[:6]])
# ---- co-variation of line-start and line-end
def rates(lines):
    fm=np.mean([last(l['words'][-1])=='m' for l in lines]);iy=np.mean([first(l['words'][0]) in 'yd' for l in lines])
    return fm,iy
byf=C.defaultdict(list)
for l in P:byf[l['folio']].append(l)
fo=[f for f,v in byf.items() if len(v)>=12]
A=np.array([rates(byf[f]) for f in fo])
r,p=stats.spearmanr(A[:,0],A[:,1])
# null: shuffle folio-level initial rate among folios of same I/H stratum
strat=C.defaultdict(list)
for i,f in enumerate(fo):strat[(byf[f][0]['I'],byf[f][0]['H'])].append(i)
nl=[]
for b in range(B):
    y2=A[:,1].copy()
    for idx in strat.values():y2[idx]=A[idx,1][rng.permutation(len(idx))]
    nl.append(stats.spearmanr(A[:,0],y2)[0])
print('T4c per-folio (n=%d, >=12 lines) rho(final -m rate, initial y/d rate)=%.3f raw p=%.3g ; within (section,hand) permutation null %.3f sd %.3f z=%.1f'%(len(fo),r,p,np.mean(nl),np.std(nl),(r-np.mean(nl))/np.std(nl)))
# per-line cross-line dependency: line i ends m -> line i+1 begins y/d ?
pairs=[]
for k in range(len(L)-1):
    a,b_=L[k],L[k+1]
    if a['ty']=='P' and b_['ty']=='P' and a['folio']==b_['folio'] and not b_['pf'] and len(a['words'])>=3 and len(b_['words'])>=3 and not a['pend']:
        pairs.append((last(a['words'][-1])=='m',first(b_['words'][0]) in 'yd',a['folio']))
x=np.array([p[0] for p in pairs]);z=np.array([p[1] for p in pairs])
o=z[x].mean()-z[~x].mean();nl=[]
fol=np.array([p[2] for p in pairs])
for b in range(B):
    x2=x.copy()
    for f in np.unique(fol):
        ii=np.where(fol==f)[0];x2[ii]=x[ii][rng.permutation(len(ii))]
    nl.append(z[x2].mean()-z[~x2].mean())
print('   next-line y/d start after line-final m: %.3f vs after non-m %.3f (diff %+.3f, within-folio perm z=%.1f, n=%d pairs)'%(z[x].mean(),z[~x].mean(),o,(o-np.mean(nl))/np.std(nl),len(x)))
# within-line: first word y/d vs last word m in the SAME line
x=np.array([last(l['words'][-1])=='m' for l in P]);z=np.array([first(l['words'][0]) in 'yd' for l in P]);fol=np.array([l['folio'] for l in P])
o=z[x].mean()-z[~x].mean();nl=[]
for b in range(B):
    x2=x.copy()
    for f in np.unique(fol):
        ii=np.where(fol==f)[0];x2[ii]=x[ii][rng.permutation(len(ii))]
    nl.append(z[x2].mean()-z[~x2].mean())
print('   same line: y/d start given final m %.3f vs not %.3f (within-folio perm z=%.1f)'%(z[x].mean(),z[~x].mean(),(o-np.mean(nl))/np.std(nl)))
# ---- T5 within-section and folio fixed effects
def logit(X,y,it=40,ridge=1e-3):
    X=np.column_stack([np.ones(len(X)),X]);b=np.zeros(X.shape[1])
    for _ in range(it):
        p=1/(1+np.exp(-X@b));Wt=p*(1-p)+1e-9;H=X.T@(X*Wt[:,None])+ridge*np.eye(len(b))
        b+=np.linalg.solve(H,X.T@(y-p)-ridge*b)
    return b,np.sqrt(np.diag(np.linalg.inv(H)))
rows=[]
for l in P:
    w=l['words'];rows.append((len(w),sum(len(x) for x in w[:-1])+len(w)-2,int(last(w[-1])=='m'),int(l['pend']),l['folio'],l['I'],l['H']))
R_=rows
def zs(x):
    x=np.asarray(x,float);return (x-x.mean())/x.std()
n_=np.array([r[0] for r in R_]);pre_=np.array([r[1] for r in R_]);y_=np.array([r[2] for r in R_]);pe_=np.array([r[3] for r in R_]);fo_=np.array([r[4] for r in R_])
D=np.column_stack([(fo_==f).astype(float) for f in np.unique(fo_)[1:]])
b,se=logit(np.column_stack([zs(pre_),zs(n_),D]),y_)
print('T5 folio-fixed-effects logit -m ~ prefix chars, n words: b_pre=%.2f z=%.1f ; b_n=%.2f z=%.1f'%(b[1],b[1]/se[1],b[2],b[2]/se[2]))
b,se=logit(np.column_stack([zs(pre_),zs(n_),pe_,D]),y_)
print('   + para-end flag (folio FE): b_pend=%.2f z=%.1f'%(b[3],b[3]/se[3]))
# folio-level: is the -m rate heterogeneous across folios beyond binomial?  (line state vs page state)
print('   cell metrics within (section I, hand H): lines, final-m %, mid-m %, ratio, init y/d %, mid y/d %, ratio, r(-m,n words) within-cell, z (within-folio perm)')
cells=C.defaultdict(list)
for l in P:cells[(l['I'],l['H'])].append(l)
for k,v in sorted(cells.items(),key=lambda kv:-len(kv[1])):
    if len(v)<150:continue
    fm=np.mean([last(l['words'][-1])=='m' for l in v]);mm=np.mean([last(w)=='m' for l in v for w in l['words'][1:-1]])
    fy=np.mean([first(l['words'][0]) in 'yd' for l in v]);my=np.mean([first(w) in 'yd' for l in v for w in l['words'][1:-1]])
    nn=np.array([len(l['words']) for l in v]);mx=np.array([last(l['words'][-1])=='m' for l in v],float);fl=np.array([l['folio'] for l in v])
    o=np.corrcoef(nn,mx)[0,1];nl=[]
    for b_ in range(min(B,300)):
        m2=mx.copy()
        for f in np.unique(fl):
            ii=np.where(fl==f)[0];m2[ii]=mx[ii][rng.permutation(len(ii))]
        nl.append(np.corrcoef(nn,m2)[0,1])
    print('    %s: %d, %.1f, %.2f, %.0fx, %.1f, %.1f, %.1fx, r=%.3f z=%.1f'%(k,len(v),100*fm,100*mm,fm/max(mm,1e-9),100*fy,100*my,fy/my,o,(o-np.mean(nl))/np.std(nl)))
# ---- cross-transcription alignment (ZL vs RF), only when run on zl3b
if name=='zl3b':
    RFL=load('rf1b');rfd={(l['folio'],l['line']):l for l in RFL}
    agree=[];dis=[]
    for l in P:
        r=rfd.get((l['folio'],l['line']))
        if r is None or r['ty']!='P':continue
        if ''.join(l['words'])==''.join(r['words']):
            (agree if l['words'][-1]==r['words'][-1] else dis).append((last(l['words'][-1])=='m',last(r['words'][-1])=='m',len(l['words'][-1]),len(r['words'][-1])))
    print('T3b ZL vs RF same-letters lines: last word identical n=%d, differently split n=%d'%(len(agree),len(dis)))
    print('   -m rate ZL: identical %.1f%% / differently-split %.1f%% ; RF differently-split %.1f%%'%(100*np.mean([a[0] for a in agree]),100*np.mean([a[0] for a in dis]),100*np.mean([a[1] for a in dis])))
