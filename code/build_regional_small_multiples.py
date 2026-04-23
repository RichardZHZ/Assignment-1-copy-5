"""Regenerate docs/figures/04_regional_small_multiples.html as a 2x3
small-multiples panel — one region per facet, with annual events on the left
axis (teal) and annual fatalities on the right axis (red). All x-axes lock to
2014-2025 with horizontal labels so the facets read consistently.

Run after 01_data_cleaning.ipynb has produced acled_clean.parquet.
"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJECT = Path(__file__).resolve().parent.parent
CLEAN = PROJECT / "data" / "derived" / "acled_clean.parquet"
OUT = PROJECT / "docs" / "figures" / "04_regional_small_multiples.html"

REGIONS = [
    "Africa",
    "Asia-Pacific",
    "Europe-Central-Asia",
    "Latin-America-Caribbean",
    "Middle-East",
    "US-and-Canada",
]
LABEL = {
    "Africa": "Africa",
    "Asia-Pacific": "Asia-Pacific",
    "Europe-Central-Asia": "Europe & Central Asia",
    "Latin-America-Caribbean": "Latin America & Caribbean",
    "Middle-East": "Middle East",
    "US-and-Canada": "US & Canada",
}

INK = "#0f172a"
GRID = "#e2e8f0"
PAPER = "#fafaf7"
EVENTS_COL = "#0f766e"      # teal-700
FATAL_COL = "#b91c1c"       # red-700

df = pd.read_parquet(CLEAN)
df = df[df["YEAR"].between(2014, 2025)]

fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[f"<b>{LABEL[r]}</b>" for r in REGIONS],
    specs=[[{"secondary_y": True}] * 3] * 2,
    horizontal_spacing=0.09, vertical_spacing=0.22,
)

for i, reg in enumerate(REGIONS):
    r, c = i // 3 + 1, i % 3 + 1
    ann = (df[df["REGION"] == reg]
             .groupby("YEAR")[["EVENTS", "FATALITIES"]].sum().reset_index())

    fig.add_trace(go.Scatter(
        x=ann["YEAR"], y=ann["EVENTS"],
        mode="lines+markers",
        line=dict(color=EVENTS_COL, width=2.2),
        marker=dict(size=5, color=EVENTS_COL, line=dict(color="white", width=1)),
        name="Events",
        legendgroup="events",
        showlegend=(i == 0),
        hovertemplate="<b>Events</b> %{x}: %{y:,}<extra></extra>",
    ), row=r, col=c, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=ann["YEAR"], y=ann["FATALITIES"],
        mode="lines+markers",
        line=dict(color=FATAL_COL, width=2.2),
        marker=dict(size=5, color=FATAL_COL, line=dict(color="white", width=1)),
        name="Fatalities",
        legendgroup="fatalities",
        showlegend=(i == 0),
        hovertemplate="<b>Fatalities</b> %{x}: %{y:,}<extra></extra>",
    ), row=r, col=c, secondary_y=True)

    # X-axis: consistent range, horizontal labels
    fig.update_xaxes(
        dtick=2, tickangle=0, automargin=False,
        range=[2013.5, 2025.5],
        tickfont=dict(size=10, color=INK),
        showgrid=False, zeroline=False,
        linecolor=GRID, linewidth=1, ticks="outside", tickcolor=GRID,
        row=r, col=c,
    )
    # Y-axes: matched styling, left teal / right red tint
    fig.update_yaxes(
        tickfont=dict(size=10, color=EVENTS_COL),
        gridcolor=GRID, gridwidth=1, zeroline=False,
        linecolor=GRID, linewidth=1,
        rangemode="tozero", tickformat="~s",
        row=r, col=c, secondary_y=False,
    )
    fig.update_yaxes(
        tickfont=dict(size=10, color=FATAL_COL),
        showgrid=False, zeroline=False,
        linecolor=GRID, linewidth=1,
        rangemode="tozero", tickformat="~s",
        row=r, col=c, secondary_y=True,
    )

# Subplot titles
for a in fig.layout.annotations[:len(REGIONS)]:
    a.font = dict(size=13, color=INK,
                  family="IBM Plex Sans, system-ui, sans-serif")

fig.update_layout(
    title=dict(
        text="<b>Annual events vs. fatalities by region, 2014–2025</b>"
             "<br><sup><span style='color:#0f766e'>teal</span> = events (left axis) · "
             "<span style='color:#b91c1c'>red</span> = fatalities (right axis)</sup>",
        x=0.5, xanchor="center",
        font=dict(size=17, color=INK,
                  family="IBM Plex Sans, system-ui, sans-serif"),
        pad=dict(t=10, b=6),
    ),
    height=640,
    margin=dict(l=60, r=60, t=100, b=70),
    paper_bgcolor=PAPER,
    plot_bgcolor=PAPER,
    font=dict(family="IBM Plex Sans, system-ui, sans-serif",
              size=12, color=INK),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.06, yanchor="top",
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color=INK),
    ),
)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")
