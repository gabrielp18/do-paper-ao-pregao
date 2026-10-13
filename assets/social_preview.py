"""Gera a prévia social do repositório (1280×640), a imagem que aparece quando o link é compartilhado.

  python assets/social_preview.py  ->  assets/social-preview.png

Suba em Settings → General → Social preview. O desenho da folha é o mesmo do logo (assets/logo.py).
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Polygon

from logo import AMBAR, CIANO, FOLD, INK, LINE, ROSA, geometria

AQUI = Path(__file__).parent
FUNDO, CINZA = "#0D1017", "#8A93A6"
MONO = next((f for f in ("Consolas", "DejaVu Sans Mono") if f in {x.name for x in font_manager.fontManager.ttflist}))


def canto(cx, cy, r, a0, a1, n=12):
    t = np.radians(np.linspace(a0, a1, n))
    return np.column_stack([cx + r * np.cos(t), cy + r * np.sin(t)])


def folha():
    # contorno do logo (coordenadas do SVG, y para baixo): ponta dobrada no canto superior direito
    return np.vstack([[[188, 16], [240, 68]], canto(216, 216, 24, 0, 90), canto(40, 216, 24, 90, 180),
                      canto(40, 40, 24, 180, 270)])


fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor=FUNDO)

ax = fig.add_axes([0.03, 0.11, 0.36, 0.78])
ax.set_xlim(0, 256); ax.set_ylim(256, 0); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Polygon(folha(), closed=True, fc=INK, ec=FOLD, lw=3, joinstyle="round"))
ax.add_patch(Polygon([[188, 16], [188, 56], [200, 68], [240, 68]], closed=True, fc=FOLD, ec=FOLD, lw=3))
for y0, x1 in [(50, 150), (68, 124)]:
    ax.plot([44, x1], [y0, y0], color=LINE, alpha=0.14, lw=5, solid_capstyle="round")
_, x, y = geometria()
ax.add_patch(Polygon(np.column_stack([x, y]), closed=True, fc=AMBAR, alpha=0.45, lw=0))
ax.plot([x[0], x[-1]], [y[0], y[-1]], color=CIANO, lw=3.5, ls=(0, (0.4, 2.2)), dash_capstyle="round")
ax.plot(x, y, color=LINE, lw=4.2, solid_capstyle="round", solid_joinstyle="round")
ax.plot(x[-1], y[-1], "o", ms=14, mfc=ROSA, mec=INK, mew=3)

tx = 0.425
fig.text(tx, 0.81, "Do Paper ao Pregão", color=LINE, fontsize=44, fontweight="bold", family=MONO, va="center")
fig.text(tx, 0.705, "Papers de finanças quant, implementados do zero", color=CINZA, fontsize=16.5, family=MONO)
fig.text(tx, 0.655, "e testados no mercado brasileiro.", color=CINZA, fontsize=16.5, family=MONO)

fichas = [("01", "Signature Trading", "Futter, Horvath & Wiese · arXiv 2023", "a conta fecha, o alfa não"),
          ("02", "Machine learning PE returns", "Tausch & Pietz · JFDS 2024", "a textura fecha, o nível não")]
for k, (n, titulo, ref, veredito) in enumerate(fichas):
    y0 = 0.50 - k * 0.19
    fig.text(tx, y0, n, color=AMBAR, fontsize=24, fontweight="bold", family=MONO, va="center")
    fig.text(tx + 0.055, y0 + 0.025, titulo, color=LINE, fontsize=18, fontweight="bold", family=MONO, va="center")
    fig.text(tx + 0.055, y0 - 0.025, ref, color=CINZA, fontsize=13, family=MONO, va="center")
    fig.text(tx + 0.055, y0 - 0.068, veredito, color=ROSA, fontsize=13, family=MONO, va="center")

fig.text(tx, 0.085, "github.com/gabrielp18/do-paper-ao-pregao  ·  @gabrielp.pires", color=CIANO, fontsize=14,
         family=MONO)

out = AQUI / "social-preview.png"
fig.savefig(out, dpi=100, facecolor=FUNDO)
print(out, "·", MONO)
