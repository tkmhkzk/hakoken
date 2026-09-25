import json,re,datetime
N=json.load(open('raw/notices.json')); K=json.load(open('raw/koukoku.json')); ST=json.load(open('stats.json'))
TODAY=datetime.date(2026,9,25)
HAKO={'土木一式工事':'C','管工事':'C','舗装工事':'C','水道施設工事':'B','とび・土工・コンクリート工事':'○','石工事':'○','鋼構造物工事':'○','しゅんせつ工事':'○','塗装工事':'○'}
OFF={o['g']:o for o in ST['offices']}
def jd(s):
    m=re.search(r'令和(\d+)年(\d+)月(\d+)日',s or ''); return datetime.date(2018+int(m.group(1)),int(m.group(2)),int(m.group(3))).isoformat() if m else None
def office(r):
    k=r['kikan']
    for g in ['小名浜支所','四倉支所','常磐支所','勿来支所']:
        if g in k: return g
    if '水道局' in k: return None
    t=r['title']
    if '下水道' in t: return '下水道関係'
    if re.search('保育所|市営住宅|クリンピー|幼稚園|衛生センター',t): return '住宅営繕課'
    if re.search('道路|橋|河川|線',t): return '建設事業課'
    return None
def fmt(z): return z.translate(str.maketrans('ＡＢＣ','ABC'))
out=[]
for r in N:
    key=f"{'8001' if r['no'].startswith('8') else '0001'}_{r['no']}"
    kk=K.get(key.replace('8001_','0001_'),None) or K.get(r['no']) or next((v for k2,v in K.items() if k2.endswith(r['no'])),None)
    shu=r['shu']; mine=HAKO.get(shu)
    checks=[]; status=None; reason=''
    checks.append(['登録業種',f"{shu}：{'登録あり' if mine else '登録なし'}",bool(mine)])
    teishutsu_closed='終了' in r['teishutsu']
    shinsei_closed='終了' in r['shinsei'] or (jd(r['shinsei']) and jd(r['shinsei'])<TODAY.isoformat())
    req=None
    if r['hoshiki']=='一般競争入札' and kk:
        g=fmt(kk['grade'][0]) if kk['grade'] else None
        req=g
        if g and mine and mine!='○':
            okg = mine in re.findall(r'特A|A|B|C',g) and not (mine=='A' and '特A' in g and 'A' not in g.replace('特A',''))
            okg = mine in re.sub('特A','X',g)
            checks.append(['市の等級',f"条件 {g}／箱建 {mine}",okg])
        elif g and mine=='○':
            checks.append(['市の等級',f"条件 {g}（等級なし業種）",True])
        ch=kk['chiiki'][0] if kk['chiiki'] else ''
        if ch:
            okc=('いわき市内' in ch) or ('小名浜地区' in ch)
            checks.append(['地域の条件',('市内に本店' if 'いわき市内' in ch else ch.replace('本店所在地が、','本店が').replace('にあること。','')), okc])
        if key.endswith('0000000069') or r['no']=='8000000069':
            checks.append(['登録業種（追加）','機械器具設置工事の登録も必要',False])
    elif r['hoshiki']=='指名競争入札':
        checks.append(['入札方式','指名競争（市が業者を選ぶ）',None])
    else:
        checks.append(['入札方式','随意契約',None])
    allok=all(c[2] is not False for c in checks)
    of=office(r); os_=OFF.get(of) if of else None
    score=None; note=''
    if r['hoshiki']=='一般競争入札':
        if allok:
            status='missed' if shinsei_closed else 'ok'
            score=60
            note=('参加資格があります。' + ('ただし参加申請の期限（'+(r['shinsei'] if '令和' in r['shinsei'] else '公告から約1週間')+'）を過ぎています。公告日に通知できていれば申請できた案件です。' if shinsei_closed else '申請期限までに参加申請が必要です。'))
            if '水道局' in r['kikan']: note+=' 水道局の過去の入札結果はまだ集めていないため、狙い目度は仮の値です。'
        else:
            status='ng'; bad=[c for c in checks if c[2] is False]
            reason=bad[0][0]+'：'+bad[0][1]
    elif r['hoshiki']=='指名競争入札':
        if not mine: status='ng'; reason='登録業種：'+shu+'の登録なし'
        else:
            status='shimei'
            base=40+(os_['hi']*0.8 if os_ else 10)-((os_['act']-4)*5 if os_ else 0)
            if '小名浜支所' in r['kikan']:
                score=round(base); note='小名浜支所からは過去1年で7回指名されています（すべて辞退）。今回も指名される可能性が高い案件です。'
            elif r['no']=='0000000632':
                score=85; note='前回（9月9日開札）は箱建を含む指名9社が全社辞退し、落札者なしでした。今回はその再公告です。競争相手が少ない見込みです。'
            elif '水道局' in r['kikan']:
                score=55; note='水道施設はB等級のため、水道局の指名対象になり得ます。水道局の過去結果は未収集のため仮の値です。'
            else:
                score=round(base*0.6); note='この発注課から箱建が指名された記録は、過去1年の結果表にはありません。'
    else:
        status='zuii'; reason='随意契約のため入札の対象外'
    if teishutsu_closed and status not in('ng','zuii'): status='closed'
    out.append(dict(no=r['no'],issuer=r['kikan'],title=r['title'],shu=shu,hoshiki=r['hoshiki'],gaiyo=r['gaiyo'],place=r['place'],
        koukoku=jd(r['koukoku']),shinsei=jd(r['shinsei']),shinsei_raw=r['shinsei'],teishutsu=jd(r['teishutsu']),teishutsu_raw=r['teishutsu'],kaisatsu=jd(r['kaisatsu']),
        req=req,checks=checks,status=status,reason=reason,score=score,note=note,office=of,ostat=os_))
json.dump(out,open('mockdata.json','w'),ensure_ascii=False)
import collections; print(collections.Counter(o['status'] for o in out))
for o in out:
    if o['status'] in('ok','missed','shimei','closed'): print(o['status'],o['no'][-4:],o['score'],o['title'][:26],o['checks'])
