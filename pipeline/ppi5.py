import re,json
src=open('ppi2.py').read()
exec(src.split("allrecs=[]")[0])
def crawl(sortv):
    page=s.post(B+'PPUBC00400',data=data).text
    f=F(); f.feed(page); d=f.f+list(f.selv.items())
    d=[(k,v) for k,v in d if k!='selNarabikae']+[('selNarabikae',sortv),('method:redisplay','再表示')]
    page=s.post(B+'PPUBC00500',data=d).text
    got=[]
    for i in range(10):
        got+=rows(page)
        m=re.search(r'全(\d+)件中 (\d+) - (\d+)件目',page)
        if int(m.group(3))>=int(m.group(1)): break
        f=F(); f.feed(page); page=s.post(B+'PPUBC00500!next',data=f.f+list(f.selv.items())).text
    return got
seen={};
for sv in ['1','2','3','4','5','6']:
    g=crawl(sv)
    for i in range(0,len(g),3):
        a,lk=g[i]; seen[tuple(lk)]=[g[i],g[i+1],g[i+2]]
    print(sv,len(seen))
    if len(seen)>=57: break
json.dump([x for v in seen.values() for x in v],open('raw/ppi_rows.json','w'),ensure_ascii=False)
