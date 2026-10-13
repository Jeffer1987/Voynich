# Wave 4A per-line-state tests (mechanism iii). usage: python -I m4c.py zl3b|rf1b B
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from m4_common import *
name=sys.argv[1];B=int(sys.argv[2]);rng=np.random.default_rng(3)
L=load(name);P=cont(L)
print('==',name)
fol=np.array([l['folio'] for l in P]);m=np.array([last(l['words'][-1])=='m' for l in P],float);g=np.array([last(l['words'][-1])=='g' for l in P],float)
def fperm(x,f):
    x2=x.copy()
    for u in np.unique(f):
        ii=np.where(f==u)[0];x2[ii]=x[ii][rng.permutation(len(ii))]
    return x2
# 1. in-line: mid-line -m words present -> final m?
anym=np.array([any(last(w)=='m' for w in l['words'][1:-1]) for l in P])
o=m[anym].mean()-m[~anym].mean()
nl=[]
for b in range(B):
    m2=fperm(m,fol);nl.append(m2[anym].mean()-m2[~anym].mean())
print('P(final m | mid-line -m present)=%.3f (n=%d) vs absent %.3f ; folio-perm z=%.1f'%(m[anym].mean(),anym.sum(),m[~anym].mean(),(o-np.mean(nl))/np.std(nl)))
# 2. count of -l/-r words earlier in line (candidate source of replaced endings), controlling n words via strata
lr=np.array([sum(last(w) in 'lr' for w in l['words'][:-1])/ (len(l['words'])-1) for l in P]);n=np.array([len(l['words']) for l in P])
r=np.corrcoef(lr,m)[0,1];nl=[np.corrcoef(lr,fperm(m,fol))[0,1] for _ in range(B)]
print('corr(final m, share of -l/-r words earlier in line)=%.3f folio-perm z=%.1f'%(r,(r-np.mean(nl))/np.std(nl)))
# 3. line-to-line persistence of final-m / final-g within folio
for lab,x in (('m',m),('g',g)):
    a=[];b_=[];f2=[]
    for i in range(len(P)-1):
        if fol[i]==fol[i+1] and P[i+1]['line']==P[i]['line']+1:a.append(x[i]);b_.append(x[i+1]);f2.append(fol[i])
    a=np.array(a);b_=np.array(b_);f2=np.array(f2)
    o=np.corrcoef(a,b_)[0,1];nl=[np.corrcoef(a,fperm(b_,f2))[0,1] for _ in range(B)]
    print('lag-1 autocorr of final-%s between consecutive lines r=%.3f within-folio perm z=%.1f (n=%d)'%(lab,o,(o-np.mean(nl))/np.std(nl),len(a)))
# 4. page-level heterogeneity of final-m beyond binomial given section/hand cells
cells=C.defaultdict(list)
for l,x in zip(P,m):cells[(l['I'],l['H'])].append((l['folio'],x))
tot=0;ob=0;nlv=[]
chi=0;df=0
for k,v in cells.items():
    if len(v)<100:continue
    p=np.mean([x for _,x in v]);fs=C.defaultdict(list)
    for f,x in v:fs[f].append(x)
    for f,xs in fs.items():
        if len(xs)>=8:chi+=(sum(xs)-len(xs)*p)**2/(len(xs)*p*(1-p));df+=1
print('page-level overdispersion of final-m within (section,hand) cells: chi2=%.0f on %d pages (ratio %.2f; 1.0 = binomial per-line independence)'%(chi,df,chi/max(df,1)))
# 5. final-m by words-in-line within cell vs overall (does a position-in-line threshold exist?) rate by n
for lo,hi in ((3,4),(5,6),(7,8),(9,10),(11,13),(14,30)):
    s=[(k,x) for k,x,l in zip(range(len(P)),m,P) if lo<=len(l['words'])<=hi]
    print('   n words %d-%d: lines %d final-m %.1f%%'%(lo,hi,len(s),100*np.mean([x for _,x in s])))
