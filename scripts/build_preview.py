from pathlib import Path
import re,html
root=Path(__file__).resolve().parents[1]
s=(root/"README.md").read_text(encoding="utf-8")
# Render all current Markdown sections and embedded HTML into a GitHub-like preview.
lines=s.splitlines(); out=[]; code=False; codebuf=[]; quote=[]
for line in lines:
    if line.startswith('```'):
        if code: out.append('<pre><code>'+html.escape('\n'.join(codebuf))+'</code></pre>'); codebuf=[]
        code=not code; continue
    if code: codebuf.append(line); continue
    if line.startswith('#'):
        m=re.match(r'(#+) (.*)',line); level=len(m[1]); out.append(f'<h{level}>{m[2]}</h{level}>'); continue
    if line.startswith('[!['):
        m=re.match(r'\[!\[([^]]*)\]\((.*?)\)\]\((.*?)\)',line)
        if m: out.append(f'<a href="{html.escape(m[3])}"><img alt="{m[1]}" src="{html.escape(m[2])}" /></a>')
        continue
    if line.startswith('>'):
        text=line[1:].strip(); text=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',text); text=re.sub(r'\*(.*?)\*',r'<em>\1</em>',text); out.append('<p class="quote">'+text+'</p>'); continue
    if line=='---': out.append('<hr>'); continue
    out.append(line)
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Xikreti — prévia do README</title><style>*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#e6edf3;font:16px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.shell{max-width:940px;margin:28px auto;padding:24px;border:1px solid #30363d;border-radius:6px}.label{font-size:12px;color:#8b949e;margin-bottom:32px}h3{font-size:20px;margin:24px 0 16px}code{font-family:ui-monospace,Consolas,monospace;background:#21262d;border-radius:6px;padding:2px 5px;font-size:85%}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;margin:16px 0}td{padding:6px 13px;border:1px solid #30363d;width:50%}pre{background:#161b22;padding:16px;border-radius:6px;overflow:auto;font-size:14px;line-height:1.5}pre code{background:none;padding:0;font-size:100%}p{line-height:1.5}hr{border:0;border-top:1px solid #30363d;margin:24px 0}.quote{color:#8b949e}a{color:#58a6ff}a img{vertical-align:middle;margin:3px 0}@media(max-width:600px){.shell{margin:8px;padding:12px}td{padding:4px}h3{font-size:16px}}</style><article class="shell"><div class="label">xikreti / README.md · Prévia local</div>'''+ '\n'.join(out)+'</article></html>'
import json
colors=json.loads((root/'design-system.json').read_text(encoding='utf-8-sig'))['colors']
for old,key in [('#0d1117','background'),('#161b22','surface'),('#21262d','raised'),('#30363d','border'),('#8b949e','muted'),('#e6edf3','text'),('#58a6ff','highlight')]: page=page.replace(old,colors[key])
(root/'preview.html').write_text(page,encoding='utf-8')
