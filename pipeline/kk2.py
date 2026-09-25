import pymupdf,glob,re,json
TYPES=['土木一式工事','建築一式工事','管工事','舗装工事','水道施設工事','電気工事','機械器具設置工事','解体工事','とび・土工・コンクリート工事','電気通信工事','しゅんせつ工事','塗装工事','防水工事']
res={}
for f in sorted(glob.glob('raw/koukoku/*.pdf')):
    t=''.join(pg.get_text() for pg in pymupdf.open(f)); L=[l.strip().replace('　','') for l in t.splitlines()]
    grade=[l for l in L if re.fullmatch(r'[特ＡＢＣ又は、から以上下のいずれか]+',l) and re.search('[ＡＢＣ]',l)]
    pten=[l for l in L if re.fullmatch(r'(\d{3,4}点以上|要件なし|[０-９\d]+点以上)',l)]
    types=[l for l in L if l in TYPES]
    chiiki=[re.sub(r'\s','',c) for c in re.findall(r'(いわき市内に本店を有する者であること。|本店所在地が、[^。]*にあること。)',t.replace('\n',''))]
    key=f.split('/')[-1][:-4]
    res[key]=dict(types=types,grade=grade,p=pten,chiiki=chiiki[:1])
    print(key[-4:],types[:2],grade,pten,chiiki[:1])
json.dump(res,open('raw/koukoku.json','w'),ensure_ascii=False,indent=1)
