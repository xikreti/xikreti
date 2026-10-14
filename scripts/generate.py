from pathlib import Path
import json, subprocess, sys, os, html
from datetime import date,timedelta
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from fetch_data import refresh_data
ROOT=Path(__file__).resolve().parents[1]
def prepare():
    # The original avatar already has a white background. Preserve the photo;
    # suppress texture and enhance edges without an unnecessary model download.
    im=Image.open(ROOT/'assets/source-photo.png').convert('L').filter(ImageFilter.MedianFilter(3))
    im=ImageOps.autocontrast(im,cutoff=1)
    a=np.asarray(im,dtype=float)
    fine=np.asarray(im.filter(ImageFilter.GaussianBlur(1.5)),dtype=float)
    coarse=np.asarray(im.filter(ImageFilter.GaussianBlur(6)),dtype=float)
    a=np.clip(a-.35*np.maximum(coarse-fine,0),0,255)
    Image.fromarray(a.astype('uint8')).save(ROOT/'assets/source-prepped.png')
def enrich():
    p=ROOT/'data/contributions.json'; d=json.loads(p.read_text(encoding='utf-8')); days=d['days']
    active=[x for x in days if x['count']>0]; best=max(days,key=lambda x:x['count'])
    longest={'length':0,'start':None,'end':None}; run=0; begin=None
    for x in days:
        if x['count']:
            if not run: begin=x['date']
            run+=1
            if run>longest['length']: longest={'length':run,'start':begin,'end':x['date']}
        else: run=0
    current=[]; i=len(days)-1
    if days[i]['count']==0 and days[i]['date']==date.today().isoformat(): i-=1
    while i>=0 and days[i]['count']>0: current.append(days[i]); i-=1
    monthly={}
    for x in days: monthly[x['date'][:7]]=monthly.get(x['date'][:7],0)+x['count']
    total=sum(x['count'] for x in days)
    d.update(username='xikreti',total_contributions=total,active_days=len(active),avg_per_active_day=round(total/len(active),1) if active else 0,current_streak={'length':len(current),'start':current[-1]['date'] if current else None,'end':current[0]['date'] if current else None},longest_streak=longest,best_day=best,monthly=[{'month':k,'total':v} for k,v in sorted(monthly.items())],range={'start':days[0]['date'],'end':days[-1]['date']})
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8'); return d

def calendar(d):
    days=d['days']; first=date.fromisoformat(days[0]['date']); start=first-timedelta(days=(first.weekday()+1)%7)
    weeks=((date.fromisoformat(days[-1]['date'])-start).days//7)+1
    w=34+weeks*16+6; h=158; colors=['#161b22','#0e4429','#006d32','#26a641','#39d353']
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif"><style>.lbl{{fill:#7d8590;font-size:13px;font-weight:600}}.c{{transform-box:fill-box;transform-origin:center;animation:pop .55s ease-out both}}.g{{animation:pop .55s ease-out both,flash .7s ease-out both}}@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}60%{{opacity:1;transform:scale(1.1)}}100%{{opacity:1;transform:scale(1)}}}}@keyframes flash{{0%,45%{{filter:brightness(2.4)}}100%{{filter:brightness(1)}}}}@media(prefers-reduced-motion:reduce){{.c,.g{{animation:none}}}}</style>']
    months=['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']; seen=set()
    for x in days:
        dt=date.fromisoformat(x['date']); n=(dt-start).days; col,row=divmod(n,7); delay=(col+row*.55)/(weeks-1+3.3)*3.6
        if (dt.year,dt.month) not in seen and (dt.day<=7 or not seen):
            parts.append(f'<text class="lbl" x="{34+col*16}" y="16">{months[dt.month-1]}</text>'); seen.add((dt.year,dt.month))
        parts.append(f'<rect class="c {"g" if x["level"] else ""}" x="{34+col*16}" y="{24+row*16}" width="13" height="13" rx="2.5" fill="{colors[x["level"]]}" style="animation-delay:{delay:.3f}s"><title>{x["date"]}: {x["count"]} contribuições</title></rect>')
    for name,r in [('Seg',1),('Qua',3),('Sex',5)]: parts.append(f'<text class="lbl" x="2" y="{24+r*16+11}">{name}</text>')
    parts.append(f'<text x="34" y="152" fill="#e6edf3" font-size="15" font-weight="700">{d["total_contributions"]} contribuições no período exibido</text></svg>')
    (ROOT/'assets/contributions.svg').write_text(''.join(parts),encoding='utf-8')
if __name__=='__main__':
    if '--daily' in sys.argv: refresh_data(True)
    d=enrich(); calendar(d)
    subprocess.run([sys.executable,str(ROOT/'scripts/render_stats_svg.py')],check=True,env={**os.environ,'PYTHONUTF8':'1'})
    if '--daily' not in sys.argv:
        prepare(); subprocess.run([sys.executable,str(ROOT/'scripts/make_ascii_svg.py'),str(ROOT/'assets/source-prepped.png'),str(ROOT/'assets/portrait.svg')],check=True,env={**os.environ,'PYTHONUTF8':'1'})


    from apply_theme import apply
    apply()
