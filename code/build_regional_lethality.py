"""Regenerate docs/figures/04_regional_lethality.html as a 2x3 small-multiples
panel — one region per facet, each on its own linear y-axis so US-and-Canada's
near-zero lethality reads correctly. A muted global reference line is overlaid
on every facet for cross-region context; endpoint values are annotated.

Run after 01_data_cleaning.ipynb has produced acled_clean.parquet.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT = Path(__file__).resolve().parent.parent
CLEAN = PROJECT / "data" / "derived" / "acled_clean.parquet"
OUT = PROJECT / "docs" / "figures" / "04_regional_lethality.html"

REGIONS = [
    "Africa",
    "Asia-Pacific",
    "Europe-Central-Asia",
    "Latin-America-Caribbean",
    "Middle-East",
    "US-and-Canada",
]
# Nicer display labels
LABEL = {
    "Africa": "Africa",
    "Asia-Pacific": "Asia-Pacific",
    "Europe-Central-Asia": "Europe & Central Asia",
    "Latin-America-Caribbean": "Latin America & Caribbean",
    "Middle-East": "Middle East",
    "US-and-Canada": "US & Canada",
}
# Per-region accent (distinct, muted but legible on paper bg)
COLOR = {
    "Africa": "#b45309",            # amber-700
    "Asia-Pacific": "#0f766e",      # teal-700
    "Europe-Central-Asia": "#7c3aed",  # violet-600
    "Latin-America-Caribbean": "#be185d",  # pink-700
    "Middle-East": "#b91c1c",       # red-700
    "US-and-Canada": "#334155",     # slate-700
}

def hex_to_rgba(h: str, a: float) -> str:
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

INK = "#0f172a"
MUTED = "#94a3b8"
GRID = "#e2e8f0"
PAPER = "#fafaf7"

df = pd.read_parquet(CLEAN)
df = df[df["YEAR"].between(2014, 2025)]

# Global reference: all-region annual lethality
glob = (df.groupby("YEAR")[["EVENTS", "FATALITIES"]].sum().reset_index())
glob["L"] = glob["FATALITIES"] / glob["EVENTS"]

# Per-region annual lethality (only years with events)
reg_data = {}
for reg in REGIONS:
    ann = (df[df["REGION"] == reg]
             .groupby("YEAR")[["EVENTS", "FATALITIES"]].sum().reset_index())
    ann = ann[ann["EVENTS"] > 0].copy()
    ann["L"] = ann["FATALITIES"] / ann["EVENTS"]
    reg_data[reg] = ann

fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[f"<b>{LABEL[r]}</b>" for r in REGIONS],
    horizontal_spacing=0.08, vertical_spacing=0.22,
    shared_xaxes=False,
)

for i, reg in enumerate(REGIONS):
    r, c = i // 3 + 1, i % 3 + 1
    ann = reg_data[reg]
    col = COLOR[reg]

    # Muted global reference first (so regional line sits on top)
    fig.add_trace(go.Scatter(
        x=glob["YEAR"], y=glob["L"],
        mode="lines",
        line=dict(color=MUTED, width=1.3, dash="dot"),
        name="Global (all regions)",
        legendgroup="global",
        showlegend=(i == 0),
        hovertemplate="Global %{x}: %{y:.2f}<extra></extra>",
    ), row=r, col=c)

    # Region line + filled area
    fig.add_trace(go.Scatter(
        x=ann["YEAR"], y=ann["L"],
        mode="lines+markers",
        line=dict(color=col, width=2.4),
        marker=dict(size=6, color=col, line=dict(color="white", width=1)),
        fill="tozeroy",
        fillcolor=hex_to_rgba(col, 0.12),
        name=LABEL[reg],
        showlegend=False,
        hovertemplate=f"<b>{LABEL[reg]}</b> %{{x}}<br>"
                      "Lethality: %{y:.2f}<extra></extra>",
    ), row=r, col=c)

    # Endpoint annotations (first and last observed year)
    if len(ann) >= 2:
        y0v, y1v = ann.iloc[0], ann.iloc[-1]
        for pt, xshift in [(y0v, -4), (y1v, 4)]:
            fig.add_annotation(
                x=pt["YEAR"], y=pt["L"],
                text=f"<b>{pt['L']:.2f}</b>",
                showarrow=False,
                xshift=xshift, yshift=14,
                font=dict(size=10, color=col,
                          family="IBM Plex Sans, system-ui, sans-serif"),
                row=r, col=c,
            )

    # Axes styling per facet
    fig.update_xaxes(
        dtick=2, tickfont=dict(size=10, color=INK),
        tickangle=0, automargin=False,
        showgrid=False, zeroline=False,
        linecolor=GRID, linewidth=1, ticks="outside", tickcolor=GRID,
        range=[2013.5, 2025.5],
        row=r, col=c,
    )
    fig.update_yaxes(
        tickfont=dict(size=10, color=INK),
        gridcolor=GRID, gridwidth=1, zeroline=False,
        linecolor=GRID, linewidth=1,
        rangemode="tozero",
        row=r, col=c,
    )

# Subplot titles — restyle
for a in fig.layout.annotations[:len(REGIONS)]:
    a.font = dict(size=13, color=INK,
                  family="IBM Plex Sans, system-ui, sans-serif")

fig.update_layout(
    title=dict(
        text="<b>Per-event lethality by region, 2014–2025</b>"
             "<br><sup>fatalities ÷ events, linear scale per panel · "
             "<span style='color:#94a3b8'>dotted grey</span> = global reference</sup>",
        x=0.5, xanchor="center",
        font=dict(size=17, color=INK,
                  family="IBM Plex Sans, system-ui, sans-serif"),
        pad=dict(t=10, b=6),
    ),
    height=620,
    margin=dict(l=60, r=30, t=100, b=70),
    paper_bgcolor=PAPER,
    plot_bgcolor=PAPER,
    font=dict(family="IBM Plex Sans, system-ui, sans-serif",
              size=12, color=INK),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.08, yanchor="top",
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=INK),
    ),
    annotations=list(fig.layout.annotations) + [
        dict(
            text="Fatalities per event",
            x=-0.045, y=0.5, xref="paper", yref="paper",
            xanchor="center", yanchor="middle",
            textangle=-90, showarrow=False,
            font=dict(size=12, color=INK,
                      family="IBM Plex Sans, system-ui, sans-serif"),
        ),
        dict(
            text="Year",
            x=0.5, y=-0.02, xref="paper", yref="paper",
            xanchor="center", yanchor="top", showarrow=False,
            font=dict(size=12, color=INK,
                      family="IBM Plex Sans, system-ui, sans-serif"),
        ),
    ],
)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")
