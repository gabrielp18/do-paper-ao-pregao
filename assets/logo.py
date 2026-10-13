"""Gera o logo do repositório: uma folha de paper com a ponta dobrada e o Ibovespa de verdade desenhado nela.

  python assets/logo.py  ->  assets/logo.svg

A linha é o fechamento mensal do Ibovespa de jan/2020 a ago/2026, o mesmo arquivo do paper 01. A corda tracejada liga o
primeiro ao último ponto, e a mancha âmbar entre os dois é a área de Lévy: o nível 2 da assinatura do caminho, a parte
que sabe a ordem dos movimentos (o mesmo desenho da cena "A assinatura do caminho" do reel).
"""
from pathlib import Path

import numpy as np
import pandas as pd

INK, FOLD, LINE, CIANO, AMBAR, ROSA = "#07080D", "#2A3142", "#E6E8EF", "#4FB3D9", "#E0A040", "#E0245E"
AQUI = Path(__file__).parent
XLSX = AQUI.parent / "papers" / "01-signature-trading" / "base_ibov.xlsx"


def ibovespa_mensal():
    raw = pd.read_excel(XLSX, header=[0, 1], index_col=0).sort_index()
    ibov = raw["Close"]["^BVSP"].dropna()
    assert len(ibov) == 1657 and f"{ibov.index[0]:%d/%m/%Y}" == "02/01/2020", "base diferente da do notebook"
    return ibov.groupby(ibov.index.to_period("M")).last()


def geometria(x0=38, x1=214, y_baixo=210, y_alto=90):
    """Pontos do caminho na caixa do logo (viewBox 256): tempo no x, pontos do índice no y."""
    m = ibovespa_mensal()
    v = m.to_numpy()
    x = x0 + np.arange(len(v)) / (len(v) - 1) * (x1 - x0)
    y = y_baixo - (v - v.min()) / (v.max() - v.min()) * (y_baixo - y_alto)
    return m, x, y


def area_de_levy(x, y):
    """Área com sinal entre o caminho e a corda (fórmula do laço: caminho de ida, corda de volta)."""
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


if __name__ == "__main__":
    m, x, y = geometria()
    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in zip(x, y))
    folha = "M40 16 H188 L240 68 V216 A24 24 0 0 1 216 240 H40 A24 24 0 0 1 16 216 V40 A24 24 0 0 1 40 16 Z"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-label="Do Paper ao Pregão">
  <path d="{folha}" fill="{INK}" stroke="{FOLD}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M188 16 V56 A12 12 0 0 0 200 68 H240 Z" fill="{FOLD}" stroke="{FOLD}" stroke-width="4" stroke-linejoin="round"/>
  <g stroke="{LINE}" stroke-opacity=".14" stroke-width="5" stroke-linecap="round">
    <path d="M44 50H150M44 68H124"/>
  </g>
  <polygon points="{pts}" fill="{AMBAR}" fill-opacity=".45"/>
  <line x1="{x[0]:.1f}" y1="{y[0]:.1f}" x2="{x[-1]:.1f}" y2="{y[-1]:.1f}" stroke="{CIANO}" stroke-width="5"
        stroke-dasharray="2 9" stroke-linecap="round"/>
  <polyline points="{pts}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{x[-1]:.1f}" cy="{y[-1]:.1f}" r="9" fill="{ROSA}" stroke="{INK}" stroke-width="4"/>
</svg>
"""
    out = AQUI / "logo.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"{out} · {len(m)} meses ({m.index[0]} a {m.index[-1]}) · "
          f"de {m.iloc[0]:,.0f} a {m.iloc[-1]:,.0f} pontos · mínimo {m.min():,.0f} em {m.idxmin()} · "
          f"área de Lévy no desenho {area_de_levy(x, y):+,.0f} px²")
