import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np,collections as C
from h23_common import *
name=sys.argv[1]; B=int(sys.argv[2]) if len(sys.argv)>2 else 300
mode='at' if name=='rf1b' else 'marker'
d=load(name,mode); W=words(d)
rng=np.random.default_rng(2)
pop=[x for x in W if x['ty']=='P' and not x['pf'] and x['n']>=3]
N=len(pop)
A=lambda k:np.array([x[k] for x in pop])
pos=A('pos');n=A('n');start=pos==1;end=pos==n;mid=(pos>1)&(pos<n)
fol=np.unique(A('folio'),return_inverse=True)[1]
w=[x['w'] for x in pop]
IND={'end_m':np.array([s[-1]=='m' for s in w]),'end_g':np.array([s[-1]=='g' for s in w]),
 'init_gal':np.array([s[0] in GAL for s in w]),'init_y':np.array([s[0]=='y' for s in w]),
 'init_d':np.array([s[0]=='d' for s in w]),'init_c':np.array([s[0]=='c' for s in w]),'init_t':np.array([s[0]=='t' for s in w])}
POS={'end_m':end,'end_g':end,'init_gal':start,'init_y':start,'init_d':start,'init_c':start,'init_t':start}
strata=[('ALL',np.ones(N,bool))]
for k,vals in [('L',['A','B']),('H',['1','2','3','4']),('I',['H','S','B','P','C','Z','T','A'])]:
    for v in vals:
        m=A(k)==v
        if m.sum()>300: strata.append((k+'='+v,m))
SM=np.array([s[1] for s in strata]).T.astype(float)
orders=[np.lexsort((rng.random(N),fol)) for _ in range(B)]
print('\n### Strata: rate_at_pos / rate_mid / ratio / z vs within-folio shuffle (%s, B=%d)'%(name,B))
print('| stratum | n_lines | '+' | '.join(IND)+' |')
rows={s[0]:[] for s in strata}
for k,ind in IND.items():
    pm=POS[k]
    def rate(indv): return (SM*(indv&pm)[:,None]).sum(0)/np.maximum((SM*pm[:,None]).sum(0),1)
    ro=rate(ind); rmid=(SM*(ind&mid)[:,None]).sum(0)/(SM*mid[:,None]).sum(0)
    nul=np.array([rate(ind[o]) for o in orders])
    z=(ro-nul.mean(0))/(nul.std(0)+1e-9)
    for i,s in enumerate(strata):
        rows[s[0]].append('%.3f/%.3f/%.1f/%.0f'%(ro[i],rmid[i],ro[i]/max(rmid[i],1e-9),z[i]))
for s in strata: print('| %s | %d | '%(s[0],int(s[1][start].sum()))+' | '.join(rows[s[0]])+' |')
print('\n### Gradient (lines with n>=10): rate by position; baseline = positions 5..n-4')
big=n>=10
base=(pos>=5)&(pos<=n-4)&big
for k,from_end in [('end_m',True),('end_g',True),('init_gal',False),('init_y',False),('init_d',False),('init_c',False)]:
    ind=IND[k]; b=ind[base].mean(); r=[]
    for j in range(1,9):
        m=big&((n-pos+1==j) if from_end else (pos==j)); r.append('%.3f'%ind[m].mean())
    print('| %s | base %.3f | %s | (%s) |'%(k,b,' '.join(r),'from end 1..8' if from_end else 'from start 1..8'))
print('\n### H2b length/fill')
L=np.array([len(s) for s in w])
nul=[]
for o in orders[:200]:
    Lp=L[o]; nul.append((Lp[start].mean(),Lp[end].mean(),Lp[mid].mean()))
nul=np.array(nul)
print('mean word len start/end/mid obs: %.2f %.2f %.2f ; null start %.2f+-%.2f end %.2f+-%.2f'%(L[start].mean(),L[end].mean(),L[mid].mean(),nul[:,0].mean(),nul[:,0].std(),nul[:,1].mean(),nul[:,1].std()))
em=IND['end_m']
print('final-position words: len m-ending %.2f (n=%d) vs non-m %.2f; mid-line m-ending %.2f (n=%d) vs mid non-m %.2f'%(L[end&em].mean(),(end&em).sum(),L[end&~em].mean(),L[mid&em].mean(),(mid&em).sum(),L[mid&~em].mean()))
lines={}
for x in W:
    if x['ty']=='P': lines.setdefault(x['li'],[]).append(x)
Ls=[];pre=[];last=[];lastm=[]
for li,xs in lines.items():
    if d[li]['pend'] or len(xs)<3: continue
    ws=[x['w'] for x in xs]
    Ls.append(sum(map(len,ws))+len(ws)-1);pre.append(sum(map(len,ws[:-1]))+len(ws)-1);last.append(len(ws[-1]));lastm.append(ws[-1][-1]=='m')
Ls=np.array(Ls);pre=np.array(pre);last=np.array(last);lastm=np.array(lastm)
cr=np.corrcoef(pre,last)[0,1]
nulc=[np.corrcoef(pre,rng.permutation(last))[0,1] for _ in range(1000)]
print('para non-final lines n=%d: char len mean %.1f sd %.1f; corr(prefix chars, last word len)=%.3f null sd %.3f z=%.1f'%(len(Ls),Ls.mean(),Ls.std(),cr,np.std(nulc),(cr-np.mean(nulc))/np.std(nulc)))
q=np.quantile(pre,[1/3,2/3])
for nm,m in [('short',pre<=q[0]),('mid',(pre>q[0])&(pre<=q[1])),('long',pre>q[1])]:
    print('  prefix-length %s: n=%d final-m rate %.3f  mean last len %.2f'%(nm,m.sum(),lastm[m].mean(),last[m].mean()))
pend_m=[(x['w'][-1]=='m') for x in W if x['ty']=='P' and x['pend'] and x['pos']==x['n'] and x['n']>=3]
print('final-m rate in paragraph-last-line (n=%d): %.3f'%(len(pend_m),np.mean(pend_m)))
allcount=C.Counter(x['w'] for x in W if x['ty']=='P')
midcount=C.Counter(s for s,mm in zip(w,mid) if mm)
endw=[s for s,mm in zip(w,end&em) if mm]
print('line-final m tokens %d, types %d; share of tokens whose exact type appears mid-line: %.3f'%(len(endw),len(set(endw)),np.mean([midcount[s]>0 for s in endw])))
midm=[s for s,mm in zip(w,mid&em) if mm]
es=set(endw)
print('  mid-line m tokens %d; share whose type also occurs line-final: %.3f'%(len(midm),np.mean([s in es for s in midm])))
def alt_dist(tokens):
    stems=set(s[:-1] for s in tokens); D=C.Counter()
    for s in stems:
        for X in ['m','n','in','iin','y','r','l','g','dy','ly','o','s']:
            D[X]+=allcount.get(s+X,0)>0
    return D,len(stems)
D1,n1=alt_dist(endw); D2,n2=alt_dist(midm)
print('  stem(final-m word)+X attested anywhere: frac of %d stems:'%n1,{k:round(v/n1,2) for k,v in D1.items()})
print('  stem(mid-line m word)+X attested: frac of %d stems:'%n2,{k:round(v/n2,2) for k,v in D2.items()})
print('  line-final top words:',C.Counter(endw).most_common(8))
# mid-line (non-final) tokens with the same stem as final-m words: which ending
stems=set(s[:-1] for s in endw)
E=C.Counter()
for s,mm in zip(w,mid):
    if mm:
        for k in range(len(s)):
            pass
midend=C.Counter()
for s,mm in zip(w,mid):
    if mm and s[:-1] in stems and s[-1]!='m': midend[s[-1]]+=1
midendm=sum(1 for s,mm in zip(w,mid) if mm and s[:-1] in stems and s[-1]=='m')
print('  mid-line tokens sharing stem with a final-m word: ending distribution',midend.most_common(6),'m:',midendm)
print('\n### H2c groups (first-word initial rate, last-word final rate), lines with >=2 words')
def grp(sel,label):
    ls=[li for li,l in enumerate(d) if sel(l) and len(l['words'])>=2]
    if not ls: return
    f=[d[li]['words'][0] for li in ls]; e=[d[li]['words'][-1] for li in ls]
    r=lambda xs,cond:np.mean([cond(s) for s in xs])
    print('| %s | %d | gal %.3f | y %.3f | d %.3f | c %.3f | end-m %.3f | end-g %.3f |'%(label,len(ls),r(f,lambda s:s[0] in GAL),r(f,lambda s:s[0]=='y'),r(f,lambda s:s[0]=='d'),r(f,lambda s:s[0]=='c'),r(e,lambda s:s[-1]=='m'),r(e,lambda s:s[-1]=='g')))
grp(lambda l:l['ltype']=='P' and l['pf'],'P first line')
for k in [1,2,3,4]:
    grp(lambda l,k=k:l['ltype']=='P' and not l['pf'] and l['pli']==k,'P line #%d'%(k+1))
grp(lambda l:l['ltype']=='P' and not l['pf'] and l['pli'] is not None and l['pli']>=5,'P line #6+')
grp(lambda l:l['ltype']=='P' and l['pend'],'P last line')
for t in 'LCR': grp(lambda l,t=t:l['ltype']==t,'type '+t)
print('single-word lines:')
for t in 'LCRP':
    ls=[l for l in d if l['ltype']==t and len(l['words'])==1]
    if ls: print('| %s | %d | gal %.3f | y %.3f | m %.3f | g %.3f |'%(t,len(ls),np.mean([l['words'][0][0] in GAL for l in ls]),np.mean([l['words'][0][0]=='y' for l in ls]),np.mean([l['words'][0][-1]=='m' for l in ls]),np.mean([l['words'][0][-1]=='g' for l in ls])))
