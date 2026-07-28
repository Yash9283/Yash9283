from PIL import Image
import numpy as np

SRC = "work/photo-ready.png"
OUT = "work/portrait.svg"

GLYPHS = " '.,:;~+*xXO#"   # left = light/empty, right = dense/dark
ACCENT = "#7aa2f7"          # tokyonight blue, matches stats/panel theme
BG = "#0d1117"              # GitHub dark bg so it blends into the profile

COLS = 92
CHAR_ASPECT = 0.52           # monospace glyphs are taller than wide

img = Image.open(SRC).convert("L")
w, h = img.size
rows = int(COLS * (h / w) * CHAR_ASPECT)
small = img.resize((COLS, rows), Image.LANCZOS)
arr = np.array(small).astype(np.float32) / 255.0  # 0=black,1=white

def glyph_for(v):
    # v: 0 (dark) -> dense glyph, 1 (light) -> space
    idx = int((1 - v) * (len(GLYPHS) - 1))
    idx = max(0, min(len(GLYPHS) - 1, idx))
    return GLYPHS[idx]

cell_w = 9.6
cell_h = 16
pad = 20
svg_w = COLS * cell_w + pad * 2
svg_h = rows * cell_h + pad * 2

lines_svg = []
row_stagger = 0.045  # seconds between row starts
row_draw_time = 0.5

for r in range(rows):
    row_chars = "".join(glyph_for(arr[r, c]) for c in range(COLS))
    row_chars_esc = (row_chars
                      .replace("&", "&amp;")
                      .replace("<", "&lt;")
                      .replace(">", "&gt;"))
    y = pad + (r + 1) * cell_h - 4
    clip_id = f"clip{r}"
    start = r * row_stagger
    lines_svg.append(f'''
    <clipPath id="{clip_id}">
      <rect x="{pad}" y="{pad + r*cell_h}" width="0" height="{cell_h}">
        <animate attributeName="width" from="0" to="{COLS*cell_w}"
                 begin="{start:.3f}s" dur="{row_draw_time}s"
                 fill="freeze" calcMode="spline"
                 keySplines="0.25 0.1 0.25 1" />
      </rect>
    </clipPath>
    <text x="{pad}" y="{y}" font-family="Consolas, 'Courier New', monospace"
          font-size="{cell_h*0.85:.1f}" xml:space="preserve"
          fill="{ACCENT}" clip-path="url(#{clip_id})">{row_chars_esc}</text>''')

svg = f'''<svg viewBox="0 0 {svg_w:.0f} {svg_h:.0f}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{BG}" rx="10"/>
  {"".join(lines_svg)}
</svg>'''

with open(OUT, "w") as f:
    f.write(svg)

print("wrote", OUT, "grid", COLS, "x", rows, "total duration ~", rows*row_stagger + row_draw_time, "s")
