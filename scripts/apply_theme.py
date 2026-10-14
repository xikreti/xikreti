from pathlib import Path
import json,re,html
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'design-system.json').read_text(encoding='utf-8-sig'))['colors']
def panel(labels,name):
    import xml.etree.ElementTree as ET
    manifest_path=ROOT/'assets/icons/manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    slots=[]; x=12
    for label in labels:
        iconfile=manifest.get(label) if name.startswith('stack-') else None
        has_icon=bool(iconfile)
        w=len(label)*8+24+(28 if has_icon else 0)
        slots.append(f'<rect x="{x}" y="10" width="{w}" height="32" rx="4" fill="{C["raised"]}" stroke="{C["border"]}"/>')
        if has_icon:
            node=ET.fromstring((ROOT/'assets/icons'/iconfile).read_text(encoding='utf-8'))
            node.set('x',str(x+10)); node.set('y','17'); node.set('width','18'); node.set('height','18')
            # Monochrome icons need a light ink on the dark tag background.
            if label in ['Next.js','Prisma','Rust','Solidity','GitHub','Bitcoin','Ethereum']:
                node.set('fill',C['highlight'])
                for child in node.iter():
                    if child.get('fill') and child.get('fill')!='none':
                        if label=='Next.js' and child.get('fill').lower() in ['#fff','#ffffff','white']: continue
                        child.set('fill',C['highlight'])
            slots.append(ET.tostring(node,encoding='unicode'))
        tx=x+(38 if has_icon else 12)
        slots.append(f'<text x="{tx}" y="31" fill="{C["highlight"]}" font-size="13">{html.escape(label)}</text>'); x+=w+8
    (ROOT/'assets'/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x+4} 52" width="{x+4}" height="52" font-family="ui-monospace,Consolas,monospace">'+''.join(slots)+'</svg>',encoding='utf-8')
def apply():
    replacements={'#0d1117':C['surface'],'#111722':C['raised'],'#161b22':C['raised'],'#30363d':C['border'],'#7d8590':C['muted'],'#c9d1d9':C['text'],'#e6edf3':C['text'],'#39d353':C['highlight'],'#26a641':C['primary'],'#a855f7':C['highlight'],'#d38312':C['deep'],'#a83279':C['primary'],'#555':C['raised'],'#7c3aed':C['deep'],'#6d28d9':C['deep'],'#f59e0b':C['primary']}
    for p in (ROOT/'assets').glob('*.svg'):
        s=p.read_text(encoding='utf-8')
        s=re.sub(r'#[0-9a-fA-F]{3,8}\b',lambda m:replacements.get(m[0].lower(),m[0]),s)
        p.write_text(s,encoding='utf-8')
    for labels,name in [(['HTML','CSS','JavaScript','TypeScript','React','Next.js','Tailwind','Sass'],'stack-front.svg'),(['Node.js','Python','Supabase','PostgreSQL','MongoDB','Prisma','Rust'],'stack-back.svg'),(['Solidity','Bitcoin','Ethereum'],'stack-web3.svg'),(['VS Code','Git','GitHub','Electron','Figma','Linux','Docker','Vite'],'stack-tools.svg')]: panel(labels,name)
    for label,name in [('LinkedIn','link-linkedin.svg'),('Instagram','link-instagram.svg'),('TikTok','link-tiktok.svg'),('Spotify','link-spotify.svg')]: panel([label],name)
    footer=f'''<svg xmlns="http://www.w3.org/2000/svg" width="854" height="120" viewBox="0 0 854 120"><defs><linearGradient id="green"><stop stop-color="{C['deep']}"/><stop offset="1" stop-color="{C['primary']}"/></linearGradient></defs><path fill="url(#green)" opacity=".45" d="M0 40 Q210 110 427 60 T854 40 V120 H0Z"><animate attributeName="d" values="M0 40 Q210 110 427 60 T854 40 V120 H0Z;M0 65 Q210 10 427 65 T854 55 V120 H0Z;M0 40 Q210 110 427 60 T854 40 V120 H0Z" dur="9s" repeatCount="indefinite"/></path><path fill="url(#green)" opacity=".8" d="M0 55 Q210 10 427 60 T854 45 V120 H0Z"><animate attributeName="d" values="M0 55 Q210 10 427 60 T854 45 V120 H0Z;M0 35 Q210 100 427 55 T854 65 V120 H0Z;M0 55 Q210 10 427 60 T854 45 V120 H0Z" dur="7s" repeatCount="indefinite"/></path></svg>'''
    (ROOT/'assets/footer.svg').write_text(footer,encoding='utf-8')
if __name__=='__main__': apply()
