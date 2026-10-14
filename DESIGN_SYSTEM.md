# Design system — Xikreti Green Terminal

A identidade combina terminal escuro, verde esmeralda e destaques verde neon. Os tokens estão em `design-system.json`.

## Cores

| Papel | Cor | Uso |
|---|---|---|
| Fundo | #080F0C | Prévia e contexto escuro |
| Superfície | #0D1913 | Painéis e retrato |
| Elevação | #14271D | Cards e etiquetas |
| Borda | #294B38 | Separação discreta |
| Principal | #22C55E | Barras, badges e ondas |
| Destaque | #4ADE80 | Digitação, números e links |
| Verde profundo | #166534 | Gradientes e acentos secundários |
| Texto | #E8F5EC | Conteúdo principal |
| Texto secundário | #A3B8AB | Legendas e contexto |

Os cinco níveis do calendário mantêm intensidade crescente para representar contribuições. Os três botões das janelas preservam suas cores convencionais para identificar o terminal.

## Tipografia e composição

- Interface e calendário: fontes de sistema, com fallback sem serifa.
- Terminal e etiquetas: ui-monospace, Consolas e monospace.
- Texto principal claro; verde reservado a destaques. Não transmitir informação apenas por cor.
- Painéis pareados: 840 × 880, exibidos com a mesma largura.
- Largura principal do README: 860 px, limitada pelo espaço disponível.
- Escala de espaçamento: 4, 8, 12, 16, 24, 32 e 48 px.
- Raios: painéis 12 px, cards 10 px, etiquetas 4 px.

## Movimento

Entrada: deslocamento suave de cima para baixo e fade, 0,8 s, intervalo de 0,18 s. Retrato: digitação sequencial em aproximadamente 5,8 s. Calendário: aparecimento progressivo com breve brilho. Ondas: movimento contínuo lento.

## Edição

1. Edite as cores em `design-system.json`.
2. Execute `python scripts/apply_theme.py` para aplicar a paleta aos arquivos locais.
3. Execute `python scripts/build_preview.py` e recarregue a prévia.
4. `python scripts/generate.py` gera retrato e estatísticas e reaplica o tema automaticamente.

O GitHub controla a interface externa e o estilo do Markdown. A paleta se aplica aos SVGs; o fundo, os títulos e o bloco de código nativos acompanham o tema do visitante. O widget externo de troféus permanece dependente do serviço original.
