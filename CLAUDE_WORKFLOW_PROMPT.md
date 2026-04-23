# Workflow: ACLED Discrepancy Analysis (POLI 3148 Assignment 1)

You are assisting with POLI 3148 Assignment 1. The working directory is
`/Users/zhangtingmin/Desktop/PhD/Year_1_Sem_2/POLI_3148/Assignment 1 copy 5/`.
Primary language: **Python 3** (Anaconda at `/Users/zhangtingmin/opt/anaconda3/`).
All analysis code must live in **Jupyter notebooks** under `code/`. Do not use R.

## Research question

Globally, the *number of ACLED events* and the *number of fatalities* may follow
different trends. Test three claims in order:

1. **Discrepancy exists.** The annual trend of events and the annual trend of
   fatalities diverge at the global level (2014–2025, the common window across
   all six ACLED regions).
2. **Event-type composition explains it.** The divergence is driven by shifts
   in the mix of `EVENT_TYPE` / `DISORDER_TYPE` — e.g., the share of
   low-lethality events (Protests, Strategic developments) rises while
   high-lethality events (Battles, Explosions/Remote violence, Violence
   against civilians) change at a different rate, or their per-event
   lethality changes.
3. **Regional robustness.** If (2) holds globally, check whether the same
   compositional story holds within each of the six ACLED regions, or
   whether some regions (e.g., Middle East, Africa) drive the global pattern.

## Data

Inputs (read-only), in `data/`:

- Six regional weekly `.xlsx` files named
  `<Region>_aggregated_data_up_to_week_of-*.xlsx`. Columns: `WEEK, REGION,
  COUNTRY, ADMIN1, EVENT_TYPE, SUB_EVENT_TYPE, EVENTS, FATALITIES,
  POPULATION_EXPOSURE, DISORDER_TYPE, ID, CENTROID_LATITUDE,
  CENTROID_LONGITUDE`. These are the **primary source**.
- `number_of_political_violence_events_by_country-year_as-of-03Apr2026.xlsx`
  and `number_of_reported_fatalities_by_country-year_as-of-03Apr2026.xlsx`
  — use only as a sanity check on global totals.
- `acled-codebook.html` — consult for event-type definitions.

**Time window:** restrict all cross-region analysis to weeks where
`2014-01-01 <= WEEK <= 2025-12-31` so regions with shorter coverage are
comparable (Asia-Pacific, Europe-Central-Asia, LatAm, Middle-East start in
2014; US-Canada in 2019 — flag this caveat in the report).

**Africa long-run extension:** Africa has coverage back to 1996. In addition
to the comparable-window analysis, include a dedicated Africa-only
long-run section (1997–2025) that repeats the RQ1 and RQ2 analyses on the
full Africa series. Present it as a supplementary finding in the report,
clearly labeled as Africa-only and separate from the cross-region
comparison.

## Deliverables (match the assignment rubric)

Create this structure if it does not already exist:

```
project root/
├── README.md
├── data/                 (already populated — do not modify)
├── code/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_global_discrepancy.ipynb
│   ├── 03_event_type_decomposition.ipynb
│   ├── 04_regional_robustness.ipynb
│   ├── 05_africa_long_run.ipynb
│   └── Z_generate_report.py
├── docs/
│   └── index.html        (let me manually input the transcript)
└── note_on_ai_use.md (let me draft the script at the first)
```

Every notebook must run top-to-bottom without errors and have markdown cells
that state the question, method, and takeaway for each section.

## Step-by-step workflow

### Step 0 — Setup

- Confirm Python 3 and install (if missing): `pandas`, `numpy`, `matplotlib`,
  `plotly`, `openpyxl`, `jupyter`, `scipy`, `jinja2`. Do NOT install globally
  without asking; propose a conda env or `pip install --user`.
- Create the folder structure above.

### Step 1 — `01_data_cleaning.ipynb`

- Load and concatenate all six regional `.xlsx` files into one DataFrame
  `df_weekly` (keep a `REGION` column).
- Parse `WEEK` as datetime; add `YEAR`, `MONTH`.
- Filter to `2014-01-01 ≤ WEEK ≤ 2025-12-31`.
- Save a cleaned Parquet/CSV to `data/derived/acled_clean.parquet`.
- Cross-check: annual global `EVENTS` totals should roughly match the
  country-year top-level file for overlapping years. Report any discrepancy.

### Step 2 — `02_global_discrepancy.ipynb`  (Question 1)

- Aggregate `df_weekly` to annual global `EVENTS` and `FATALITIES`.
- Plot a world map of cumulative events and fatalities by country over the full period
  (Plotly, interactive).
- Plot both as a dual-axis line chart (Plotly, interactive).
- Compute a **lethality ratio** = fatalities / events per year and plot it.
- Quantify divergence: Pearson & Spearman correlation between annual events
  and fatalities; year-over-year growth rates; a simple OLS of `log(events)`
  and `log(fatalities)` on `YEAR` — compare slopes and report whether the
  difference is statistically meaningful.

### Step 3 — `03_event_type_decomposition.ipynb`  (Question 2)

- Aggregate to `YEAR × EVENT_TYPE`: sum `EVENTS` and `FATALITIES`.
- Stacked area / 100%-stacked area charts showing the **share of events by
  type** over time, and separately **share of fatalities by type**.
- Compute per-event lethality (`FATALITIES/EVENTS`) by type-year.
- Decomposition: pick whatever quantitative decomposition method you
  judge most appropriate for separating (a) shifts in the event-type mix
  from (b) within-type changes in lethality. Document your choice of
  method and assumptions clearly in a markdown cell.
- Repeat briefly with `DISORDER_TYPE` as a robustness check.

### Step 4 — `04_regional_robustness.ipynb`  (RQ3)

- Repeat Steps 2–3 separately for each of the six regions.
- Produce a 2×3 small-multiples figure: events vs. fatalities trend per
  region.
- Produce a table: per region, the correlation between annual events and
  fatalities, and the share of the fatality trend explained by compositional
  shifts (reuse the Step 3 decomposition).
- Identify regions where the global story holds vs. regions that deviate.
- **Markdown takeaway:** is the global pattern region-driven or general?

### Step 4b — `05_africa_long_run.ipynb` (Africa supplement)

- Load the Africa regional file only; do NOT apply the 2014 cutoff — use
  the full 1997–2025 range.
- Plot a Africa Map of cumulative events and fatalities by country over the full period (Interactable).
- Repeat the RQ1 analysis (annual events vs. fatalities, lethality ratio,
  correlations, log-trend slopes) and the RQ2 event-type decomposition on
  the full Africa series.
- Highlight any structural breaks visible in the longer window that the
  2014–2025 cut would hide (e.g., pre/post-2011, major shifts around
  conflicts in DRC, Sudan, Somalia, Sahel).

### Step 5 — Report (`docs/index.html`)

- Help me to inpute my transcript into `code/Z_generate_report.py` that renders a standalone HTML report
  embedding the Plotly figures from Steps 2–4 (stop and ask me which section should be put into where).

### Step 6 — GitHub publication

- Initialize a git repo in the project root if one does not exist.
- Add a sensible `.gitignore` (ignore `__pycache__/`, `.ipynb_checkpoints/`,
  `data/derived/` if large, `.DS_Store`).
- **Do not commit raw ACLED `.xlsx` files if they are large or if their
  license restricts redistribution — ask me before committing the `data/`
  folder.** If unsure, commit only a `data/README.md` explaining how to
  obtain the files.
- Ask me for the GitHub username and desired repo name, then:
  1. Create the repo via `gh repo create <user>/<repo> --public --source=.
     --remote=origin --push` (confirm `gh auth status` first).
  2. Ensure `docs/index.html` exists.
  3. Enable GitHub Pages from the `docs/` folder on the `main` branch:
     `gh api -X POST repos/<user>/<repo>/pages -f source[branch]=main
     -f source[path]=/docs`.
  4. Report the public URL (`https://<user>.github.io/<repo>/`) back to me.
- Stop and confirm with me before every push and before enabling Pages.

### Step 7 — README.md and note_on_ai_use.md

- `README.md`: project overview, data sources, methodology summary, key
  findings (one paragraph each for Q1/Q2/Q3), limitations (time-coverage
  caveat; events-vs-fatalities reporting bias), author info placeholder.
- `note_on_ai_use.md`: draft with me.

## Ground rules

- Ask me before installing packages or creating a conda env.
- After each step, pause and show me the key figure/table before moving on.
- Do not fabricate numbers in the report — every figure in the narrative
  must trace back to a notebook cell.
- Respect the time window (2014–2025) in every cross-region comparison.
- When uncertain about interpretation, ask — do not invent causal claims.
