# Wave 4A tests 1-3. usage: python -I m4a.py zl3b|rf1b B
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from m4_common import *
name=sys.argv[1];B=int(sys.argv[2]);rng=np.random.default_rng(1)
L=load(name);P=cont(L)
print('==',name,'lines',len(P))
fin=[l['words'][-1] for l in P]
mid=[w for l in P for w in l['words'][1:-1]]
print('final -m rate %.3f mid -m rate %.4f'%(np.mean([last(w)=='m' for w in fin]),np.mean([last(w)=='m' for w in mid])))
# ---------- TEST 1
def stem(w):
    g=glyphs(w);return ''.join(g[:-1]),g[-1]
pos=C.defaultdict(lambda:[[],[]])
for l in P:
    w=l['words']
    for i,x in enumerate(w):
        s,e=stem(x)
        if i==len(w)-1: pos[s][1].append(e)
        elif i>0: pos[s][0].append(e)
ENDS=['m','l','r','n','s','y','g','o','d','a','e','k','t','i']
def delta(items):
    tot=C.Counter();W=0
    for s,(mi,fi) in items:
        W+=len(fi)
        for e in ENDS:
            tot[e]+=len(fi)*(fi.count(e)/len(fi)-mi.count(e)/len(mi))
    return {e:tot[e]/W for e in ENDS},W
items=[(s,v) for s,v in pos.items() if v[0] and v[1]]
obs,W=delta(items);print('T1 stems seen both mid and final',len(items),'final tokens covered',W)
null={e:[] for e in ENDS}
for b in range(B):
    it=[]
    for s,(mi,fi) in items:
        a=mi+fi;idx=rng.permutation(len(a))
        it.append((s,([a[j] for j in idx[:len(mi)]],[a[j] for j in idx[len(mi):]])))
    d,_=delta(it)
    for e in ENDS:null[e].append(d[e])
print('T1a within-stem position-label permutation: ending, delta(final share - mid share), null sd, z')
for e in ENDS:
    sd=np.std(null[e]);print('  ',e,'%+.3f %.3f %+.1f'%(obs[e],sd,(obs[e]-np.mean(null[e]))/sd))
def sib(stems):
    c=C.Counter()
    for s in stems:
        mi=pos[s][0]
        for e in mi:c[e]+=1/len(mi)
    n=sum(c.values());return {e:c[e]/n for e in ENDS},n
sm=[stem(w)[0] for w in fin if last(w)=='m' and pos[stem(w)[0]][0]]
sr=[stem(w)[0] for w in fin if last(w)!='m' and pos[stem(w)[0]][0]]
dm,nm=sib(sm);dr,nr=sib(sr)
print('T1b mid-line ending distribution of the stem of final-m words (n=%d) vs final-nonm words (n=%d)'%(nm,nr))
nl={e:[] for e in ENDS}
for b in range(B):
    sub=[sr[i] for i in rng.choice(len(sr),len(sm),replace=False)]
    ds,_=sib(sub)
    for e in ENDS:nl[e].append(ds[e])
for e in ENDS[:9]:print('  ',e,'final-m stems %.3f  nonm-final stems %.3f  diff z=%+.1f'%(dm[e],dr[e],(dm[e]-np.mean(nl[e]))/np.std(nl[e])))
# fraction of final-m tokens whose stem is attested mid-line with a given ending (any)
for e in 'lrn':
    print('   share of final-m tokens whose stem occurs mid-line as -%s: %.2f vs final-nonm tokens %.2f'%(e,np.mean([e in pos[s][0] for s in sm]),np.mean([e in pos[s][0] for s in sr])))
print('   share with stem attested mid-line at all: m-final %.2f, nonm-final %.2f'%(len(sm)/sum(last(w)=='m' for w in fin),len(sr)/sum(last(w)!='m' for w in fin)))
for k in (1,2,3,4):
    xs=[l['words'][-k] for l in P if len(l['words'])>=8]
    print('   -m rate k-th from end k=%d: %.3f'%(k,np.mean([last(x)=='m' for x in xs])))
# ---------- TEST 2
def chars(l,upto): return sum(len(x) for x in l['words'][:upto])+max(upto-1,0)
rows=[]
for l in P:
    w=l['words'];n=len(w)
    rows.append(dict(n=n,pre=chars(l,n-1),m=int(last(w[-1])=='m'),g=int(last(w[-1])=='g'),pend=l['pend'],folio=l['folio']))
fmax=C.defaultdict(float)
for r in rows:fmax[r['folio']]=max(fmax[r['folio']],r['pre'])
for r in rows:r['rel']=r['pre']/fmax[r['folio']]
def logit(X,y,it=50):
    X=np.column_stack([np.ones(len(X)),X]);b=np.zeros(X.shape[1])
    for _ in range(it):
        p=1/(1+np.exp(-X@b));Wt=p*(1-p);H=X.T@(X*Wt[:,None])+1e-6*np.eye(len(b))
        b+=np.linalg.solve(H,X.T@(y-p))
    return b,np.sqrt(np.diag(np.linalg.inv(H)))
y=np.array([r['m'] for r in rows]);pre=np.array([r['pre'] for r in rows],float);nn=np.array([r['n'] for r in rows],float);rel=np.array([r['rel'] for r in rows]);pe=np.array([r['pend'] for r in rows],float)
zs=lambda x:(x-x.mean())/x.std()
b,se=logit(zs(pre)[:,None],y);print('T2 logit -m ~ prefix chars: b=%.2f z=%.1f (per sd)'%(b[1],b[1]/se[1]))
b,se=logit(np.column_stack([zs(pre),zs(nn)]),y);print('   + n words: b_pre=%.2f(z%.1f) b_n=%.2f(z%.1f)'%(b[1],b[1]/se[1],b[2],b[2]/se[2]))
b,se=logit(np.column_stack([zs(pre),zs(nn),zs(rel)]),y);print('   + folio-relative fill: b_pre=%.2f b_n=%.2f b_rel=%.2f (z%.1f)'%(b[1],b[2],b[3],b[3]/se[3]))
if pe.sum()>0:
    b,se=logit(np.column_stack([zs(pre),zs(nn),pe]),y);print('   + para-end flag: b_pend=%.2f z=%.1f'%(b[3],b[3]/se[3]))
print('   -m rate by prefix-char tercile within words-per-line strata (low/mid/high), r and z vs shuffle')
for lo,hi in ((3,5),(6,7),(8,9),(10,20)):
    sel=[r for r in rows if lo<=r['n']<=hi]
    if len(sel)<60:continue
    q=np.quantile([r['pre'] for r in sel],[1/3,2/3])
    t=[[r['m'] for r in sel if r['pre']<=q[0]],[r['m'] for r in sel if q[0]<r['pre']<=q[1]],[r['m'] for r in sel if r['pre']>q[1]]]
    ms=np.array([r['m'] for r in sel]);pr=np.array([r['pre'] for r in sel])
    o=np.corrcoef(pr,ms)[0,1];nl2=[np.corrcoef(pr,rng.permutation(ms))[0,1] for _ in range(B)]
    print('   n=%d-%d lines=%d: %s  r=%.3f z=%.1f'%(lo,hi,len(sel),' / '.join('%.1f%%'%(100*np.mean(x)) for x in t),o,(o-np.mean(nl2))/np.std(nl2)))
# does char-length add beyond words (residual: chars per word)? mean chars/word as predictor at fixed n
cpw=np.array([r['pre']/max(r['n']-1,1) for r in rows])
b,se=logit(np.column_stack([zs(nn),zs(cpw)]),y);print('   fixed n, longer words (chars/word): b=%.2f z=%.1f'%(b[2],b[2]/se[2]))
if pe.sum()>0:
    ms=y;pr=pre
    print('T2c para-final lines n=%d: -m %.1f%% -g %.1f%%; wrapped lines -m %.1f%%'%(pe.sum(),100*ms[pe==1].mean(),100*np.mean([r['g'] for r in rows if r['pend']]),100*ms[pe==0].mean()))
    for lab,yy in (('m',ms),('g',np.array([r['g'] for r in rows])),('m|g',np.array([r['m']|r['g'] for r in rows]))):
        e2=[]
        for i in np.where(pe==1)[0]:
            c=np.where((pe==0)&(np.abs(pr-pr[i])<=3)&(nn==nn[i]))[0]
            if len(c)>=5:e2.append((yy[i],yy[c].mean()))
        o=np.array(e2);var=np.sum(o[:,1]*(1-o[:,1]))
        print('   matched on n words and prefix chars (+-3): %s observed %.1f%% expected %.1f%% (n=%d) z=%.1f'%(lab,100*o[:,0].mean(),100*o[:,1].mean(),len(o),(o[:,0].sum()-o[:,1].sum())/np.sqrt(var)))
    print('   mean prefix chars para-final %.1f vs wrapped %.1f ; n words %.1f vs %.1f'%(pre[pe==1].mean(),pre[pe==0].mean(),nn[pe==1].mean(),nn[pe==0].mean()))
# ---------- TEST 3
fl=[l['seps'][-1] for l in P]
print('T3 gap before last word:',dict(C.Counter(fl)))
for v in ('.',',','?'):
    s=[last(l['words'][-1])=='m' for l in P if l['seps'][-1]==v]
    if s:print('   -m rate when gap before last word is %r: %.1f%% n=%d'%(v,100*np.mean(s),len(s)))
tail=[any(x in ',?' for x in l['seps'][-2:]) for l in P];mm=[last(l['words'][-1])=='m' for l in P]
print('   lines with uncertain gap in last two gaps: n=%d -m %.1f%% ; without: n=%d -m %.1f%%'%(sum(tail),100*np.mean([m for m,t in zip(mm,tail) if t]),len(tail)-sum(tail),100*np.mean([m for m,t in zip(mm,tail) if not t])))
mc=[];fc=[]
for l in P:
    w,s=l['words'],l['seps']
    for i in range(1,len(w)-1):
        if s[i] not in ',?' and s[i+1] not in ',?':mc.append(last(w[i])=='m')
    if s[-1] not in ',?':fc.append(last(w[-1])=='m')
print('   clean subset (certain gap before word and, mid-line, after word): final -m %.1f%% (n=%d), mid -m %.2f%% => ratio %.1fx'%(100*np.mean(fc),len(fc),100*np.mean(mc),np.mean(fc)/np.mean(mc)))
ur=np.mean([x!='.' for x in fl]);um=np.mean([x!='.' for l in P for x in l['seps'][1:-1]])
print('   uncertain-gap rate before last word %.1f%% vs mid gaps %.1f%%'%(100*ur,100*um))
for v in ('.',','):
    s=[len(l['words'][-1]) for l in P if l['seps'][-1]==v];print('   last-word len when gap %s: %.2f'%(v,np.mean(s)))
# mid-line: does -m rate depend on adjacent uncertain gap?
a=[last(l['words'][i])=='m' for l in P for i in range(1,len(l['words'])-1) if l['seps'][i+1] in ',?']
bb=[last(l['words'][i])=='m' for l in P for i in range(1,len(l['words'])-1) if l['seps'][i+1]=='.']
print('   mid-line word -m rate when followed by uncertain gap %.2f%% (n=%d) vs certain %.2f%%'%(100*np.mean(a),len(a),100*np.mean(bb)))
# merge/split check: tail words legal alone? last word of the line vs mid-line words: mid-line type frequency
mt=C.Counter(mid)
def attested(w): return mt[w]>0
fm=[w for w in fin if last(w)=='m']
print('   final-m tokens whose exact type occurs mid-line: %.2f ; final-nonm: %.2f'%(np.mean([attested(w) for w in fm]),np.mean([attested(w) for w in fin if last(w)!='m'])))
# split hypothesis: final-m word = X+m where m is a detached tiny word? check mid-line standalone 'm' / 'am' words
print('   standalone mid-line words: m=%d am=%d ; final: m=%d am=%d'%(mt['m'],mt['am'],sum(w=='m' for w in fin),sum(w=='am' for w in fin)))
