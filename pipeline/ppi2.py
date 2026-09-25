import requests,re,html,json
from html.parser import HTMLParser
exec(open('ppi.py').read().split("r=s.post")[0])  # reuse session + search form build
r=s.post(B+'PPUBC00400',data=data)
class F(HTMLParser):
    def __init__(s): super().__init__(); s.f=[]; s.in_form=False; s.sel=None; s.selv={}
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='form' and a.get('id')=='PPUBC00500': s.in_form=True
        if not s.in_form: return
        if t=='input' and a.get('type')=='hidden' and a.get('name'): s.f.append((a['name'],a.get('value','')))
        if t=='select': s.sel=a.get('name')
        if t=='option' and s.sel and 'selected' in a: s.selv[s.sel]=a.get('value','')
    def handle_endtag(s,t):
        if t=='select': s.sel=None
        if t=='form': s.in_form=False
def rows(txt):
    out=[]
    body=txt.split('id="meibo_list"')[1].split('</table>')[0]
    trs=re.findall(r'<tr[^>]*>(.*?)</tr>',body,re.S)
    recs=[]
    for tr in trs:
        if '<th' in tr: continue
        cells=[re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',c))).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)]
        lk=re.search(r"link\('?(\d+)'?,\s*'?(\d+)'?,\s*'?(\d+)'?\)",tr)
        recs.append((cells,lk.groups() if lk else None))
    return recs
allrecs=[]
page=r.text
for i in range(10):
    allrecs+=rows(page)
    m=re.search(r'全(\d+)件中 (\d+) - (\d+)件目',page); print(m.group(0))
    if int(m.group(3))>=int(m.group(1)): break
    f=F(); f.feed(page)
    d=f.f+list(f.selv.items()); print([x for x in d if x[0] in ('offset','selHyojiKensu','pagesize0')])
    page=s.post(B+'PPUBC00500!next',data=d).text
open('raw/ppi_rows.json','w').write(json.dumps(allrecs,ensure_ascii=False,indent=0))
print(len(allrecs)); print(allrecs[:3])
