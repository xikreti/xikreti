# Personalizar localmente

- README.md: apresentação, stack, links e citação.
- assets/source-photo.png: foto original do GitHub.
- scripts/make_ascii_svg.py: retrato, contraste e velocidade de digitação.
- scripts/render_stats_svg.py: aparência e textos das estatísticas.
- scripts/generate.py: calendário e tratamento da foto.

Execute `python scripts/generate.py` para regenerar os SVGs usando os dados locais.
Execute `python scripts/generate.py --daily` para atualizar os dados públicos, o calendário e as estatísticas.
A prévia pode ser reconstruída com `python scripts/build_preview.py`.

Para publicar manualmente, envie README.md, assets/, data/, scripts/ e .github/workflows/. A prévia e o backup não são necessários para o perfil.

O retrato e o painel de estatísticas foram adaptados dos scripts públicos de AVIVASHISHTA29/AVIVASHISHTA29. Referência: https://github.com/AVIVASHISHTA29/AVIVASHISHTA29.
