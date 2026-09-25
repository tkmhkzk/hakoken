import glob,re,json,collections
def num(s):
    s=re.sub(r'[^\d]','',s); return int(s) if s else None
recs=[]
for f in sorted(glob.glob('ocr/*.txt')):
    t=open(f).read()
    if '工' not in t: continue
    L=t.splitlines()
    def grab(keys,after=0):
        for l in L:
            c=l.replace(' ','')
            for k in keys:
                if k in c: return c.split(k,1)[1]
        return ''
    name=grab(['事名'])
    place=grab(['所'])  # weak
    method=grab(['入札方法','札方法'])
    date=grab(['入札の日時及び場所','日時及び場所'])
    ka=grab(['担当課','当課'])
    yotei=grab(['定価格','予定価格'])
    saitei=grab(['制限価格','低制限'])
    keiyaku=grab(['予定金額','定金額'])
    m=re.search(r'令和(\d+)年(\d+)月(\d+)日',date)
    d=(2018+int(m.group(1)),int(m.group(2)),int(m.group(3))) if m else None
    y=num(re.split('円',yotei)[0]) ; k=num(re.split('円',keiyaku)[0]); s=num(re.split('円',saitei)[0])
    page=re.search(r'(\d)\s*枚のうち\s*(\d)\s*枚目',t)
    recs.append(dict(file=f[4:-4],name=name,method=method[:12],date=d,ka=ka,yotei=y,saitei=s,keiyaku=k,
       page=page.groups() if page else None,hako=bool(re.search('箱[建即健達]エンジ',t)),text=t))
ok=[r for r in recs if r['yotei'] and r['keiyaku'] and r['yotei']>=r['keiyaku']>0.6*r['yotei']]
print(len(recs),'pages;',len(ok),'with sane prices')
print(collections.Counter(r['page'] for r in recs).most_common(6))
json.dump(recs,open('recs.json','w'),ensure_ascii=False)
for r in ok[:8]: print(r['file'],r['name'][:25],r['date'],r['ka'][:10],r['yotei'],r['keiyaku'],round(r['keiyaku']/r['yotei']*100,1))
