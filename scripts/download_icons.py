from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
import json
root=Path(__file__).resolve().parents[1]; dest=root/'assets/icons'; dest.mkdir(exist_ok=True)
icons={'HTML':'html5/html5-original.svg','CSS':'css3/css3-original.svg','JavaScript':'javascript/javascript-original.svg','TypeScript':'typescript/typescript-original.svg','React':'react/react-original.svg','Next.js':'nextjs/nextjs-original.svg','Tailwind':'tailwindcss/tailwindcss-original.svg','Sass':'sass/sass-original.svg','Node.js':'nodejs/nodejs-original.svg','Python':'python/python-original.svg','Supabase':'supabase/supabase-original.svg','PostgreSQL':'postgresql/postgresql-original.svg','MongoDB':'mongodb/mongodb-original.svg','Prisma':'prisma/prisma-original.svg','Rust':'rust/rust-original.svg','Solidity':'solidity/solidity-original.svg','Bitcoin':'bitcoin/bitcoin-original.svg','Ethereum':'ethereum/ethereum-original.svg','VS Code':'vscode/vscode-original.svg','Git':'git/git-original.svg','GitHub':'github/github-original.svg','Electron':'electron/electron-original.svg','Figma':'figma/figma-original.svg','Linux':'linux/linux-original.svg','Docker':'docker/docker-original.svg','Vite':'vitejs/vitejs-original.svg'}
def get(item):
    label,path=item; filename=path.split('/')[-1]
    try:
        data=urlopen(Request('https://raw.githubusercontent.com/devicons/devicon/master/icons/'+path,headers={'User-Agent':'Xikreti-profile'}),timeout=30).read()
        (dest/filename).write_bytes(data); return label,filename
    except Exception as e: print(label,str(e)); return label,None
results=dict(ThreadPoolExecutor(max_workers=8).map(get,icons.items()))
(dest/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('Icones baixados:',sum(bool(x) for x in results.values()),'/',len(results))
