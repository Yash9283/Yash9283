import json
import random
import datetime

OUT = "work/graph.svg"
DATA = "work/contributions.json"

LEVELS = ["#161b22", "#1c3a5e", "#1c7ed6", "#4dabf7", "#a5d8ff"]

try:
    with open(DATA) as f:
        data = json.load(f)
    weeks = data["weeks"]  # list of 7-day lists, each cell 0-4
    stats = data.get("stats", {})
except FileNotFoundError:
    # placeholder pattern so the README has something to preview
    # before pull_contributions.py has been run for real
    random.seed(9283)
    weeks = [[random.choices([0, 1, 2, 3, 4], weights=[45, 25, 15, 10, 5])[0]
              for _ in range(7)] for _ in range(52)]
    stats = {"total": sum(sum(w) for w in weeks) * 3, "streak": "—", "longest": "—"}

CELL = 11
GAP = 3
PAD = 20
W = PAD * 2 + len(weeks) * (CELL + GAP)
H = PAD * 2 + 7 * (CELL + GAP) + 34

cells = []
col_stagger = 0.02
for wi, week in enumerate(weeks):
    start = wi * col_stagger
    for di, level in enumerate(week):
        x = PAD + wi * (CELL + GAP)
        y = PAD + di * (CELL + GAP)
        color = LEVELS[level]
        cells.append(f'''
    <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}" opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{start:.3f}s" dur="0.3s" fill="freeze"/>
    </rect>''')

legend_x = PAD
legend_y = H - 20
legend = [f'<text x="{legend_x}" y="{legend_y+5}" font-family="Consolas, monospace" font-size="11" fill="#8b93a7">Less</text>']
lx = legend_x + 38
for lvl in LEVELS:
    legend.append(f'<rect x="{lx}" y="{legend_y-6}" width="10" height="10" rx="2" fill="{lvl}"/>')
    lx += 15
legend.append(f'<text x="{lx+4}" y="{legend_y+5}" font-family="Consolas, monospace" font-size="11" fill="#8b93a7">More</text>')

stats_text = f'{stats.get("total","?")} contributions in the last year · streak {stats.get("streak","?")} · longest {stats.get("longest","?")}'

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="10" fill="#0d1117"/>
  {"".join(cells)}
  {"".join(legend)}
  <text x="{W-PAD}" y="{legend_y+5}" text-anchor="end" font-family="Consolas, monospace" font-size="11" fill="#8b93a7">{stats_text}</text>
</svg>'''

with open(OUT, "w") as f:
    f.write(svg)

print("wrote", OUT, "(placeholder data)" if not __import__("os").path.exists(DATA) else "(real data)")
