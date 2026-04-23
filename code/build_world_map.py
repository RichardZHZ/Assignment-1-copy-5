"""Regenerate docs/figures/02_world_map.html as a vertically stacked,
year-animated pair of choropleths (cumulative events on top, cumulative
fatalities on bottom). Driven by a single year slider + play button.

Run after notebook 01 has produced data/derived/acled_clean.parquet.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

PROJECT = Path(__file__).resolve().parent.parent
CLEAN = PROJECT / "data" / "derived" / "acled_clean.parquet"
OUT = PROJECT / "docs" / "figures" / "02_world_map.html"

df = pd.read_parquet(CLEAN)

# Cumulative country totals by year
by_cy = (df.groupby(["YEAR", "COUNTRY"])[["EVENTS", "FATALITIES"]]
           .sum()
           .reset_index()
           .sort_values(["COUNTRY", "YEAR"]))

years = sorted(by_cy["YEAR"].unique().tolist())
countries = sorted(by_cy["COUNTRY"].unique().tolist())

# Reindex to the full (country × year) grid so every frame has the same
# set of locations (fills missing-year gaps with 0) and compute running cumulative totals.
idx = pd.MultiIndex.from_product([countries, years], names=["COUNTRY", "YEAR"])
full = (by_cy.set_index(["COUNTRY", "YEAR"])
             .reindex(idx)
             .fillna(0)
             .reset_index())
full["CUM_EVENTS"] = full.groupby("COUNTRY")["EVENTS"].cumsum()
full["CUM_FATALITIES"] = full.groupby("COUNTRY")["FATALITIES"].cumsum()
full["log_ev"] = np.log10(full["CUM_EVENTS"].clip(lower=1))
full["log_ft"] = np.log10(full["CUM_FATALITIES"].clip(lower=1))

zmax_ev = float(full["log_ev"].max())
zmax_ft = float(full["log_ft"].max())


def trace_events(yr: int) -> go.Choropleth:
    d = full[full["YEAR"] == yr]
    return go.Choropleth(
        locations=d["COUNTRY"],
        locationmode="country names",
        z=d["log_ev"],
        zmin=0,
        zmax=zmax_ev,
        colorscale="Blues",
        marker_line_color="white",
        marker_line_width=0.35,
        colorbar=dict(
            title=dict(text="log₁₀ events", font=dict(size=11)),
            thickness=10, len=0.38,
            x=1.01, xanchor="left",
            y=0.78, yanchor="middle",
            tickfont=dict(size=10),
        ),
        customdata=np.stack([d["COUNTRY"], d["CUM_EVENTS"]], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>"
                      "Cumulative events: %{customdata[1]:,.0f}<extra></extra>",
        geo="geo",
        name="Events",
    )


def trace_fat(yr: int) -> go.Choropleth:
    d = full[full["YEAR"] == yr]
    return go.Choropleth(
        locations=d["COUNTRY"],
        locationmode="country names",
        z=d["log_ft"],
        zmin=0,
        zmax=zmax_ft,
        colorscale="Reds",
        marker_line_color="white",
        marker_line_width=0.35,
        colorbar=dict(
            title=dict(text="log₁₀ fatalities", font=dict(size=11)),
            thickness=10, len=0.38,
            x=1.01, xanchor="left",
            y=0.23, yanchor="middle",
            tickfont=dict(size=10),
        ),
        customdata=np.stack([d["COUNTRY"], d["CUM_FATALITIES"]], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b><br>"
                      "Cumulative fatalities: %{customdata[1]:,.0f}<extra></extra>",
        geo="geo2",
        name="Fatalities",
    )


frames = [
    go.Frame(name=str(yr), data=[trace_events(yr), trace_fat(yr)])
    for yr in years
]

GEO_STYLE = dict(
    projection_type="natural earth",
    showframe=False,
    showcoastlines=True,
    coastlinecolor="#cbd5e1",
    coastlinewidth=0.4,
    showcountries=True,
    countrycolor="#ffffff",
    countrywidth=0.3,
    showland=True,
    landcolor="#f1ede3",
    showocean=True,
    oceancolor="#ffffff",
    lakecolor="#ffffff",
    bgcolor="rgba(0,0,0,0)",
)

fig = go.Figure(
    data=[trace_events(years[-1]), trace_fat(years[-1])],  # default to most recent
    frames=frames,
    layout=go.Layout(
        title=dict(
            text="<b>Cumulative ACLED activity by country</b>"
                 "<br><sup>drag the slider or hit play — log₁₀ colour scale, hover for country totals</sup>",
            x=0.5, xanchor="center",
            font=dict(size=17, color="#0f172a"),
            pad=dict(t=10, b=6),
        ),
        geo={**GEO_STYLE, "domain": dict(x=[0, 0.92], y=[0.56, 1.0])},
        geo2={**GEO_STYLE, "domain": dict(x=[0, 0.92], y=[0.08, 0.52])},
        height=880,
        margin=dict(l=10, r=10, t=90, b=110),
        paper_bgcolor="#fafaf7",
        plot_bgcolor="#fafaf7",
        font=dict(family="IBM Plex Sans, system-ui, sans-serif",
                  size=12, color="#0f172a"),
        annotations=[
            dict(text="<b>Events</b> — cumulative count",
                 x=0.01, y=1.0, xref="paper", yref="paper",
                 xanchor="left", yanchor="top", showarrow=False,
                 font=dict(size=13, color="#1e40af",
                           family="IBM Plex Sans, system-ui, sans-serif")),
            dict(text="<b>Fatalities</b> — cumulative count",
                 x=0.01, y=0.52, xref="paper", yref="paper",
                 xanchor="left", yanchor="top", showarrow=False,
                 font=dict(size=13, color="#b91c1c",
                           family="IBM Plex Sans, system-ui, sans-serif")),
        ],
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.02, y=-0.02,
            xanchor="left", yanchor="top",
            pad=dict(r=8, t=4),
            showactive=False,
            bgcolor="#ffffff",
            bordercolor="#cbd5e1",
            font=dict(family="IBM Plex Sans, system-ui, sans-serif", size=12),
            buttons=[
                dict(label="▶  Play", method="animate",
                     args=[None, dict(frame=dict(duration=900, redraw=True),
                                      transition=dict(duration=300),
                                      fromcurrent=True, mode="immediate")]),
                dict(label="❚❚  Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        transition=dict(duration=0),
                                        mode="immediate")]),
            ],
        )],
        sliders=[dict(
            active=len(years) - 1,
            x=0.14, y=-0.02, len=0.82,
            xanchor="left", yanchor="top",
            pad=dict(t=40, b=10),
            bgcolor="#e2e8f0",
            activebgcolor="#b91c1c",
            bordercolor="#cbd5e1",
            tickcolor="#94a3b8",
            font=dict(family="IBM Plex Sans, system-ui, sans-serif", size=11),
            currentvalue=dict(
                prefix="Year: ",
                visible=True,
                xanchor="left",
                font=dict(size=14, color="#b91c1c",
                          family="IBM Plex Sans, system-ui, sans-serif"),
            ),
            steps=[dict(method="animate", label=str(yr),
                        args=[[str(yr)], dict(mode="immediate",
                                              frame=dict(duration=0, redraw=True),
                                              transition=dict(duration=0))])
                   for yr in years],
        )],
    ),
)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)  ·  {len(years)} frames")
