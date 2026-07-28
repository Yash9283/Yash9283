OUT = "work/sysinfo.svg"

ACCENT = "#7aa2f7"
DIM = "#8b93a7"
BG = "#0d1117"
BORDER = "#232937"

ROWS = [
    ("role",  "Software Engineer"),
    ("focus", "Full Stack Development"),
    ("stack", "Java · C# · .NET · ASP.NET Core/MVC/Web API · React.js"),
    ("data",  "SQL Server"),
    ("tools", "Docker · GitLab"),
]

W = 620
HEADER_H = 46
ROW_H = 44
PAD = 24
H = HEADER_H + len(ROWS) * ROW_H + PAD

rows_svg = []
for i, (label, value) in enumerate(ROWS):
    y = HEADER_H + i * ROW_H + 30
    start = 0.3 + i * 0.18
    label_esc = label
    value_esc = (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    rows_svg.append(f'''
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" begin="{start:.2f}s" dur="0.35s" fill="freeze"/>
      <text x="{PAD}" y="{y}" font-family="Consolas, 'Courier New', monospace" font-size="15" fill="{ACCENT}">{label_esc}</text>
      <text x="{PAD+95}" y="{y}" font-family="Consolas, 'Courier New', monospace" font-size="15" fill="{DIM}">:</text>
      <text x="{PAD+112}" y="{y}" font-family="Consolas, 'Courier New', monospace" font-size="14.5" fill="#e6edf3">{value_esc}</text>
    </g>''')

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="0" y="0" width="100%" height="{HEADER_H}" rx="10" fill="#161b22"/>
  <rect x="0" y="{HEADER_H-10}" width="100%" height="10" fill="#161b22"/>
  <circle cx="24" cy="{HEADER_H/2}" r="6" fill="#ff5f56"/>
  <circle cx="44" cy="{HEADER_H/2}" r="6" fill="#ffbd2e"/>
  <circle cx="64" cy="{HEADER_H/2}" r="6" fill="#27c93f"/>
  <text x="{W/2}" y="{HEADER_H/2+5}" text-anchor="middle" font-family="Consolas, 'Courier New', monospace" font-size="13" fill="{DIM}">sysinfo.sh</text>
  {"".join(rows_svg)}
</svg>'''

with open(OUT, "w") as f:
    f.write(svg)

print("wrote", OUT)
