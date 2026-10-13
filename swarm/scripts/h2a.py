import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sys,numpy as np,collections as C
from h23_common import *
name=sys.argv[1]; B=int(sys.argv[2]) if len(sys.argv)>2 else 500
mode='at' if name=='rf1b' else 'marker'
d=load(name,mode); W=words(d)
pop=[x for x in W if x['ty']=='P' and not x['pf'] and x['n']>=3]
pf=[x for x in W if x['ty']=='P' and x['pf'] and x['n']>=3]
print(name,'cont-line words',len(pop),'para-first words',len(pf))
rng=np.random.default_rng(1)
def feats(P):
    f1=[x['w'][0] for x in P]; l1=[x['w'][-1] for x in P]; l2=[x['w'][-2:] for x in P]
    return dict(first1=f1,last1=l1,last2=l2,word=[x['w'] for x in P])
def run(P,label,Bn):
    F=feats(P); N=len(P)
    pos=np.array([x['pos'] for x in P]); n=np.array([x['n'] for x in P])
    start=pos==1; end=pos==n; mid=(pos>1)&(pos<n)
    fol=np.unique([x['folio'] for x in P],return_inverse=True)[1]
    # folios appear in order? ensure contiguity by stable sort key
    out={}
    for fn in ['first1','last1','last2','word']:
        vals=F[fn]; u={v:i for i,v in enumerate(sorted(set(vals)))}; code=np.array([u[v] for v in vals]); K=len(u)
        inv={i:v for v,i in u.items()}
        obs={m:np.bincount(code[msk],minlength=K) for m,msk in [('start',start),('end',end),('mid',mid)]}
        ns=start.sum();ne=end.sum();nm=mid.sum()
        null_s=np.zeros((Bn,K));null_e=np.zeros((Bn,K));null_m=np.zeros((Bn,K))
        for b in range(Bn):
            order=np.lexsort((rng.random(N),fol))
            c=code[order]
            null_s[b]=np.bincount(c[start],minlength=K);null_e[b]=np.bincount(c[end],minlength=K);null_m[b]=np.bincount(c[mid],minlength=K)
        res=[]
        for k in range(K):
            tot=obs['start'][k]+obs['end'][k]+obs['mid'][k]
            if tot<(40 if fn!='word' else 25): continue
            for pn,msk_n,nul in [('start',ns,null_s),('end',ne,null_e)]:
                o=obs[pn][k]; mu=nul[:,k].mean(); sd=nul[:,k].std()+1e-9
                rm=obs['mid'][k]/nm; ro=o/msk_n
                p=(1+np.sum(np.abs(nul[:,k]-mu)>=abs(o-mu)))/(Bn+1)
                res.append((fn,pn,inv[k],int(o),round(float(mu),1),round(float(ro),4),round(float(rm),4),round(float(ro/max(rm,1e-9)),2),round(float((o-mu)/sd),1),round(float(p),4)))
        out[fn]=res
    return out
out=run(pop,'cont',B)
for fn,res in out.items():
    for pn in ['start','end']:
        r=[x for x in res if x[1]==pn]; r.sort(key=lambda x:-abs(x[8]))
        print('\n##',fn,pn,'(feature,pos,val,obs,null_mean,rate_pos,rate_mid,ratio,z,p)')
        for x in r[:10]: print('| '+' | '.join(str(y) for y in x[2:])+' |')
import pickle;pickle.dump(out,open(SP+'/h2a_%s.pkl'%name,'wb'))
