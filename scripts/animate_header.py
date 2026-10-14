from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import quote
import re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
s=(root/'README.md').read_text(encoding='utf-8')
urls=re.findall(r'<img src="(https://[^"]+)"',s)
selected=[u for u in urls if 'capsule-render' in u or 'readme-typing' in u or 'img.shields.io/badge/Status-' in u or 'img.shields.io/badge/Foco-' in u or 'img.shields.io/badge/Web3-' in u or 'img.shields.io/badge/Caf' in u]
ns='http://www.w3.org/2000/svg'; ET.register_namespace('',ns)
def download(url):
    return ET.fromstring(urlopen(Request(quote(url,safe=':/?=&%+'),headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read())
def wrap(nodes,w,h,delay):
    svg=ET.Element('{'+ns+'}svg',{'width':str(w),'height':str(h),'viewBox':f'0 0 {w} {h}'})
    style=ET.SubElement(svg,'{'+ns+'}style'); style.text=f'@keyframes profileEntrance{{from{{opacity:0;transform:translateY(-18px)}}to{{opacity:1;transform:translateY(0)}}}}.profileEntrance{{animation:profileEntrance .8s cubic-bezier(.16,1,.3,1) {delay}s both}}@media(prefers-reduced-motion:reduce){{.profileEntrance{{animation:none}}}}'
    g=ET.SubElement(svg,'{'+ns+'}g',{'class':'profileEntrance'})
    for node in nodes: g.append(node)
    return ET.tostring(svg,encoding='unicode')
for u in selected[:2]:
    node=download(u); view=node.get('viewBox','').split(); w=float(node.get('width','0').replace('px','')); h=float(node.get('height','0').replace('px',''))
    if view: w,h=float(view[2]),float(view[3])
    name='header.svg' if 'capsule-render' in u else 'typing.svg'
    (root/'assets'/name).write_text(wrap([node],w,h,0 if name=='header.svg' else .18),encoding='utf-8')
badges=[]; x=0
for u in selected[2:]:
    node=download(u); w=float(node.get('width')); node.set('x',str(x)); badges.append(node); x+=w+12
(root/'assets/status.svg').write_text(wrap(badges,x-12,28,.36),encoding='utf-8')
s=s.replace(selected[0],'./assets/header.svg').replace(selected[1],'./assets/typing.svg')
start=s.index('<div align="center">\n  <img src="https://img.shields.io/badge/Status-'); end=s.index('</div>',start)+len('</div>')
s=s[:start]+'<div align="center">\n<img src="./assets/status.svg" width="860" alt="Status: Codando agora · Foco: Full Stack · Web3: Blockchain Dev · Café: Necessário" />\n</div>'+s[end:]
(root/'README.md').write_text(s,encoding='utf-8')
print('Banner, texto digitado e badges com animação de entrada gerados.')

