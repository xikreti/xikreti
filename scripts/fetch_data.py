from pathlib import Path
from urllib.request import urlopen, Request
from html.parser import HTMLParser
import json, re, html, os
from datetime import date, timedelta
from PIL import Image, ImageOps, ImageFilter
ROOT=Path(__file__).resolve().parents[1]
def fetch(url):
    return urlopen(Request(url,headers={'User-Agent':'xikreti-profile-art'}),timeout=40).read()
def svg(w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" rx="16" fill="#0d1117"/><style>text{{font-family:monospace}} @keyframes enter{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}} .line{{animation:enter .5s both}} @media(prefers-reduced-motion:reduce){{.line{{animation:none}}}}</style>{body}</svg>'
def text(x,y,s,color='#c9d1d9',size=13,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {extra}>{html.escape(s)}</text>'
class Calendar(HTMLParser):
    def __init__(self): super().__init__(); self.days={}; self.tooltips={}; self.target=None; self.parts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('data-date') and 'data-level' in a:
            self.days[a['data-date']]={'date':a['data-date'],'level':int(a['data-level']),'id':a.get('id'),'count':0}
        if tag=='tool-tip': self.target=a.get('for'); self.parts=[]
    def handle_data(self,data):
        if self.target: self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.target:
            self.tooltips[self.target]=''.join(self.parts); self.target=None

def refresh_data(refresh=False):
    path=ROOT/'data/contributions.json'
    if refresh or not path.exists():
        raw=fetch('https://github.com/users/xikreti/contributions').decode()
        p=Calendar(); p.feed(raw)
        if len(p.days)<300: raise RuntimeError('Calendário incompleto; mantendo os arquivos existentes')
        for d in p.days.values():
            label=p.tooltips.get(d.pop('id'),'')
            m=re.search(r'([\d,]+) contribution',label)
            if not label: raise RuntimeError('Contagem indisponível; mantendo os arquivos existentes')
            d['count']=int(m.group(1).replace(',','')) if m else 0
        days=sorted(p.days.values(),key=lambda d:d['date'])
        path.write_text(json.dumps({'updated':date.today().isoformat(),'days':days},indent=2),encoding='utf-8')
