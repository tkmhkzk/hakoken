import requests,re,html,sys
from html.parser import HTMLParser
B='https://iwaki.efftis.jp/PPI/Public/'
s=requests.Session()
s.get(B+'PPUBC00100')
r=s.get(B+'PPUBC00100!link?screenId=PPUBC00400&chotatsu_kbn=00')
class P(HTMLParser):
    def __init__(s):
        super().__init__();s.f=[];s.sel=None;s.opts={};s.first={}
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='input' and a.get('name') and a.get('type') in ('hidden','text'): s.f.append((a['name'],a.get('value','')))
        if t=='select': s.sel=a.get('name'); s.opts[s.sel]=None
        if t=='option' and s.sel:
            if s.sel not in s.first: s.first[s.sel]=a.get('value','')
            if 'selected' in a: s.opts[s.sel]=a.get('value','')
            s.opts.setdefault(s.sel+'#all',[]).append(a.get('value',''))
    def handle_endtag(s,t):
        if t=='select': s.sel=None
p=P();p.feed(r.text)
data=[(k,v) for k,v in p.f]
for k,v in p.opts.items():
    if k.endswith('#all'): continue
    data.append((k, v if v is not None else p.first.get(k,'')))
print(p.opts.get('kensakuJoken.selHyojiKensu#all'), p.opts.get('kensakuJoken.selNendo#all'), file=sys.stderr)
data=[(k,v) for k,v in data if k!='kensakuJoken.selHyojiKensu']+[('kensakuJoken.selHyojiKensu',p.opts['kensakuJoken.selHyojiKensu#all'][-1]),('method:search','検　索')]
r=s.post(B+'PPUBC00400',data=data)
open('raw/ppi_list.html','w').write(r.text)
t=re.sub(r'<script.*?</script>','',r.text,flags=re.S)
t=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' | ',t)))
t=re.sub(r'(\|\s*)+','| ',t)
i=t.find('件名'); print(t[i-300:i+6000])
