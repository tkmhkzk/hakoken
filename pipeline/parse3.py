import json,re,glob,collections,os
recs=json.load(open('recs.json'))
CO=re.compile(r'([(（]\s*[株有合資]\s*[)）]|株式会社|有限会社|建設|工業|組|興業|産業|設備|土木|工務店|商事)')
def col(fn):
    if not os.path.exists(fn): return []
    L=[l.strip(' |_.-—') for l in open(fn).read().splitlines()]
    out=[];cur=None
    for l in L:
        c=l.replace(' ','')
        if not c: continue
        if '落札者なし' in c: out.append(('__NOWIN__','')); continue
        m=re.match(r'^(.*?)(不参加|辞退|無効|\d[\d.,]{2,}\d)?$',l)
        name=l; val=None
        mm=re.search(r'\s{2,}(\S+)$',l)
        head=l
        if mm: head=l[:mm.start()].strip(); val=mm.group(1)
        if CO.search(head.replace(' ','')) and not head.replace(' ','').startswith(('千円','円','最低制限','落札')):
            cur=dict(name=re.sub(r'\s','',head).lstrip('|').replace('（','(').replace('）',')'),val=None,win=False); out.append(cur)
            if val: cur['val']=val
        elif cur:
            if c.startswith('落札'): cur['win']=True
            if cur['val'] is None:
                v=re.search(r'(不参加|辞退|無効|\d[\d.,]{2,}\d)',c)
                if v and not c.startswith(('千円','円')): cur['val']=v.group(1)
            elif mm and cur['val'] is None: cur['val']=val
    return out
def norm(n):
    n=n.replace('(株','(株').replace('(村)','(株)').replace('〈','(').replace('<','')
    n=re.sub(r'^[^\w(]+','',n)
    return n
agg=[]
for r in recs:
    b=r['file']
    items=col(f'ocr2/{b}_L.txt')+col(f'ocr2/{b}_R.txt')
    bidders=[i for i in items if i!=('__NOWIN__','') and isinstance(i,dict)]
    for i in bidders: i['name']=norm(i['name'])
    nowin=any(i==('__NOWIN__','') for i in items)
    actual=[i for i in bidders if i['val'] and i['val'] not in('不参加','辞退')]
    decl=[i for i in bidders if i['val'] in('不参加','辞退')]
    win=[i['name'] for i in bidders if i['win']]
    m=re.match(r'(?:[a-z]_)?kouji_(\d\d)(\d\d)(\d\d)',b)
    agg.append(dict(k=b,name=r['name'].strip('|」 ,'),method=r['method'],ka=r['ka'].strip('|/ '),date=r['date'],
        pub=(2018+int(m.group(1)),int(m.group(2))),yotei=r['yotei'],saitei=r['saitei'],keiyaku=r['keiyaku'],
        nb=len(bidders),nact=len(actual),ndecl=len(decl),win=win[0] if win else None,nowin=nowin,
        names=[i['name'] for i in bidders],act=[i['name'] for i in actual],hako=r['hako'] or any('箱' in i['name'] for i in bidders),
        hako_val=next((i['val'] for i in bidders if '箱' in i['name'] and 'エンジ' in i['name']),None)))
json.dump(agg,open('agg.json','w'),ensure_ascii=False)
ok=[a for a in agg if a['yotei'] and a['keiyaku'] and a['yotei']>=a['keiyaku']>0.6*a['yotei']]
print('pages',len(agg),'priced',len(ok),'with winner',sum(1 for a in ok if a['win']))
print(collections.Counter(a['win'] for a in ok if a['win']).most_common(20))
print([ (a['k'],a['hako_val']) for a in agg if a['hako']])
