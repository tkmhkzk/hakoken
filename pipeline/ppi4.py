import re,html,json,time
exec(open('ppi2.py').read().split("allrecs=[]")[0])
recs=json.load(open('raw/ppi_rows.json'))
out=[]
def flat(d):
    t=re.sub(r'<script.*?</script>','',d,flags=re.S)
    t=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' | ',t))); return re.sub(r'(\|\s*)+','| ',t)
for i in range(0,len(recs),3):
    a,lk=recs[i]; b=recs[i+1][0]; c=recs[i+2][0]
    rec=dict(no=a[0],kikan=a[1],title=a[2],shu=a[3],hoshiki=a[4],shinsei=a[5],teishutsu=b[0] if b else '',place=c[0],shudan=c[1],koukoku=c[2],kaisatsu=c[3])
    t=flat(s.get(B+f'PPUBC00500!kenmeiLink?organizationNumber={lk[0]}&nendo={lk[1]}&keiyakuNo={lk[2]}').text)
    def g(k,nxt):
        m=re.search(re.escape(k)+r'(.*?)\| '+nxt,t); return m.group(1).strip(' |') if m else ''
    rec['gaiyo']=g('| 概要 |','予定価格')
    rec['yotei']=g('| 予定価格 | (消費税を除く) |','最低制限価格')
    rec['saitei']=g('| 最低制限価格 | (消費税を除く) |','調査基準価格')
    rec['shikaku']=g('| 資格要件 |','入札公告日')
    rec['koki']=g('| 工期または履行・納入期限 |','工事または')
    out.append(rec); time.sleep(0.3)
json.dump(out,open('raw/notices.json','w'),ensure_ascii=False,indent=1)
for r in out: print(r['no'][-3:],r['shu'],r['hoshiki'],'|',r['title'][:30],'|',r['yotei'][:25],'|',r['shikaku'][:120])
