import re,html,json,time,os
exec(open('ppi2.py').read().split("allrecs=[]")[0])
rows=json.load(open('raw/ppi_rows.json'))
links=[rows[i][1] for i in range(0,len(rows),3)]
for org,nendo,no in links:
    d=s.get(B+f'PPUBC00500!kenmeiLink?organizationNumber={org}&nendo={nendo}&keiyakuNo={no}').text
    for rb,fn,fs in re.findall(r"download1\('(\d+)', '([^']*)', '(\d+)'\)",d):
        if '公告' not in fn or not fn.lower().endswith('.pdf'): continue
        hid=dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"',d))
        hid.update(renban=rb,fileName=fn,fileSize=fs)
        r=s.post(B+'PPUBC00600!download',data=hid)
        out=f'raw/koukoku/{org}_{no}.pdf'
        if r.content[:4]==b'%PDF': open(out,'wb').write(r.content); print('ok',no,fn)
        else: print('ng',no,fn,r.headers.get('content-type'))
        break
    time.sleep(0.3)
