import re,json,sys
def parse(path,out):
    lines=[];pg={};pid=0;inpar=False
    for raw in open(path,encoding='utf8'):
        raw=raw.rstrip('\n')
        if not raw or raw[0]=='#':continue
        m=re.match(r'<(f\w+)>\s+<!(.*)>',raw)
        if m:
            pg={k:v for k,v in re.findall(r'\$(\w)=(\S+)',m.group(2))};pg['folio']=m.group(1);continue
        m=re.match(r'<(f\w+)\.(\d+)[^,]*,(.)(\w*)>\s+(.*)',raw)
        if not m:continue
        fol,ln,lt,pt,t=m.groups()
        start='<%>' in t; end='<$>' in t
        if start: pid+=1
        t=re.sub(r'<[^>]*>','',t)
        t=re.sub(r'\[([^\]:]*):[^\]]*\]',r'\1',t)
        t=t.replace('{','').replace('}','').replace("'",'')
        # tokens: split on . and ,
        toks=re.split(r'[.,]',t)
        words=[w for w in toks if w and not re.search(r'[?@!;0-9\-]',w)]
        if not words:continue
        lines.append(dict(folio=fol,line=int(ln),ltype=pt[:1] if pt else '',lt=lt,pstart=start,pend=end,par=pid if pt.startswith('P') else None,
            I=pg.get('I'),L=pg.get('L'),H=pg.get('H'),Q=pg.get('Q'),words=words))
    json.dump(lines,open(out,'w'));return lines
if __name__=='__main__':
    sc=sys.argv[3]
    L=parse(sys.argv[1],sys.argv[2]);print(len(L),sum(len(l['words']) for l in L))
