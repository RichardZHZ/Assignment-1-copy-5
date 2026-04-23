"""Render the final HTML report at docs/index.html.

Assumes the notebooks 01–05 have been run and figure HTMLs exist in docs/figures/.
Run: python code/Z_generate_report.py
"""
from pathlib import Path
from textwrap import dedent

PROJECT = Path(__file__).resolve().parent.parent
DOCS = PROJECT / "docs"
FIGDIR = DOCS / "figures"
OUT = DOCS / "index.html"

REPO_URL = "https://github.com/RichardZHZ/richardzhang-poli3148-acled-discrepancy"


def fig(rel_name: str, height: int = 520, caption: str = "") -> str:
    src = f"figures/{rel_name}"
    cap = f'<figcaption>{caption}</figcaption>' if caption else ""
    return (
        f'<figure class="plotfig">'
        f'<div class="plotfig-frame">'
        f'<iframe src="{src}" width="100%" height="{height}" frameborder="0" loading="lazy" scrolling="no"></iframe>'
        f'</div>{cap}</figure>'
    )


def stat_card(kicker: str, big: str, label: str, accent: str = "ink") -> str:
    return (
        f'<div class="stat stat-{accent}">'
        f'<div class="stat-kicker">{kicker}</div>'
        f'<div class="stat-big">{big}</div>'
        f'<div class="stat-label">{label}</div>'
        f'</div>'
    )


def callout(kicker: str, lines: list[str]) -> str:
    items = "".join(f"<li>{t}</li>" for t in lines)
    return (
        f'<aside class="finding-callout">'
        f'<div class="finding-kicker">{kicker}</div>'
        f'<ul>{items}</ul>'
        f'</aside>'
    )


CSS = dedent(
    """
    :root {
      --ink: #0f172a;
      --ink-soft: #1e293b;
      --muted: #475569;
      --faint: #94a3b8;
      --bg: #fafaf7;
      --card: #ffffff;
      --rule: #e2e8f0;
      --rule-soft: #eef1f5;
      --accent: #b91c1c;       /* red-700 — data/warning */
      --accent-2: #0f766e;     /* teal-700 — positive/structure */
      --accent-3: #7c3aed;     /* violet-600 — lethality */
      --shadow: 0 1px 2px rgba(15,23,42,.04), 0 4px 16px rgba(15,23,42,.05);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 1rem; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
      font-size: 17.5px;
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
      font-feature-settings: "kern","liga","onum";
    }
    .page {
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
      gap: 3rem;
      max-width: 1240px;
      margin: 0 auto;
      padding: 2.5rem 2rem 4rem;
    }
    /* --- sidebar --- */
    .sidebar {
      position: sticky;
      top: 2rem;
      align-self: start;
      max-height: calc(100vh - 4rem);
      overflow-y: auto;
      padding-right: 0.5rem;
    }
    .sidebar .brand {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-weight: 600;
      font-size: 0.82rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.35rem;
    }
    .sidebar .brand-sub {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.85rem;
      color: var(--muted);
      margin-bottom: 1.5rem;
      line-height: 1.35;
    }
    .toc { list-style: none; margin: 0; padding: 0; border-left: 1px solid var(--rule); }
    .toc li { margin: 0; }
    .toc a {
      display: block;
      padding: 0.38rem 0.9rem;
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.9rem;
      color: var(--muted);
      text-decoration: none;
      border-left: 2px solid transparent;
      margin-left: -1px;
      transition: color .15s, border-color .15s, background .15s;
    }
    .toc a:hover { color: var(--ink); background: var(--rule-soft); }
    .toc a.active {
      color: var(--ink);
      border-left-color: var(--accent);
      font-weight: 600;
      background: var(--rule-soft);
    }
    /* --- main --- */
    main { min-width: 0; }
    .masthead { margin-bottom: 2.5rem; }
    .masthead .eyebrow {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.78rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 600;
      margin-bottom: 0.6rem;
    }
    .masthead h1 {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-weight: 600;
      font-size: 2.35rem;
      line-height: 1.18;
      letter-spacing: -0.015em;
      margin: 0 0 0.9rem;
      color: var(--ink);
    }
    .masthead .deck {
      font-size: 1.15rem;
      line-height: 1.5;
      color: var(--muted);
      max-width: 62ch;
      margin: 0 0 1.4rem;
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      align-items: center;
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.88rem;
      color: var(--muted);
      padding-top: 1rem;
      border-top: 1px solid var(--rule);
    }
    .byline strong { color: var(--ink); font-weight: 600; }
    .badge {
      display: inline-flex; align-items: center; gap: 0.4rem;
      padding: 0.25rem 0.7rem;
      background: var(--ink);
      color: #fff;
      border-radius: 999px;
      font-size: 0.78rem; font-weight: 500;
      text-decoration: none;
      transition: background .15s;
    }
    .badge:hover { background: var(--accent); }
    .badge::before { content: "●"; color: #4ade80; font-size: 0.7rem; }
    /* --- hero stat cards --- */
    .hero-stats {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      margin: 0 0 3rem;
    }
    .stat {
      background: var(--card);
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 1.1rem 1.2rem;
      box-shadow: var(--shadow);
      border-top: 3px solid var(--ink);
    }
    .stat-accent  { border-top-color: var(--accent); }
    .stat-teal    { border-top-color: var(--accent-2); }
    .stat-violet  { border-top-color: var(--accent-3); }
    .stat-kicker {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;
      color: var(--muted); font-weight: 600; margin-bottom: 0.35rem;
    }
    .stat-big {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 1.7rem; font-weight: 600; line-height: 1.15;
      color: var(--ink); letter-spacing: -0.015em;
      font-variant-numeric: tabular-nums;
    }
    .stat-label {
      font-size: 0.92rem; color: var(--muted); margin-top: 0.35rem; line-height: 1.35;
    }
    /* --- section headings --- */
    section { margin-bottom: 3.25rem; scroll-margin-top: 1.5rem; }
    section h2 {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-weight: 600;
      font-size: 1.55rem;
      letter-spacing: -0.01em;
      color: var(--ink);
      margin: 0 0 0.4rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid var(--rule);
    }
    section h3 {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-weight: 600;
      font-size: 1.02rem;
      color: var(--ink-soft);
      letter-spacing: 0.01em;
      margin: 1.6rem 0 0.55rem;
    }
    #appendix p { max-width: 72ch; }
    #appendix mjx-container { font-size: 1.02em !important; }
    section h3 {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-weight: 600;
      font-size: 1.05rem;
      color: var(--ink);
      margin: 1.6rem 0 0.4rem;
    }
    section .section-number {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.75rem; letter-spacing: 0.15em; text-transform: uppercase;
      color: var(--faint); font-weight: 600; display: block; margin-bottom: 0.35rem;
    }
    /* --- finding callouts --- */
    .finding-callout {
      background: var(--card);
      border: 1px solid var(--rule);
      border-left: 3px solid var(--accent);
      border-radius: 4px;
      padding: 1rem 1.25rem;
      margin: 1.25rem 0 1.5rem;
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.95rem;
    }
    .finding-callout .finding-kicker {
      font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase;
      color: var(--accent); font-weight: 600; margin-bottom: 0.5rem;
    }
    .finding-callout ul { margin: 0; padding-left: 1.1rem; color: var(--ink-soft); line-height: 1.55; }
    .finding-callout li + li { margin-top: 0.25rem; }
    /* --- body text --- */
    p { margin: 0 0 1.05rem; max-width: 68ch; }
    p em, p strong { color: var(--ink-soft); }
    section ol, section ul { max-width: 66ch; padding-left: 1.4rem; margin: 0 0 1.2rem; }
    section ol li, section ul li { margin-bottom: 0.35rem; line-height: 1.55; }
    code {
      font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.88em;
      background: var(--rule-soft);
      padding: 0.08em 0.35em;
      border-radius: 3px;
      color: var(--ink-soft);
    }
    /* --- figures --- */
    figure.plotfig { margin: 1.5rem 0 2rem; }
    .plotfig-frame {
      background: var(--card);
      border: 1px solid var(--rule);
      border-radius: 6px;
      overflow: hidden;
      box-shadow: var(--shadow);
    }
    .plotfig-frame iframe { display: block; border: 0; }
    figure.plotfig figcaption {
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.78rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--muted);
      margin-top: 0.6rem;
      padding-left: 0.1rem;
      line-height: 1.5;
    }
    /* --- references --- */
    #references ul { padding-left: 1.1rem; color: var(--muted); }
    #references li { margin-bottom: 0.5rem; line-height: 1.5; }
    /* --- footer --- */
    footer {
      margin-top: 3.5rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--rule);
      color: var(--faint);
      font-family: "IBM Plex Sans", system-ui, sans-serif;
      font-size: 0.82rem;
    }
    footer a { color: var(--muted); }
    /* --- responsive --- */
    @media (max-width: 900px) {
      .page { grid-template-columns: 1fr; gap: 1.5rem; padding: 1.5rem 1.25rem 3rem; }
      .sidebar { position: static; max-height: none; padding: 0; border-bottom: 1px solid var(--rule); padding-bottom: 1rem; }
      .toc { display: flex; flex-wrap: wrap; gap: 0.2rem; border-left: none; }
      .toc a { padding: 0.25rem 0.6rem; border-left: none; border-radius: 4px; font-size: 0.82rem; }
      .toc a.active { background: var(--ink); color: #fff; border-left: none; }
      .hero-stats { grid-template-columns: 1fr; }
      .masthead h1 { font-size: 1.9rem; }
    }
    /* --- print --- */
    @media print {
      body { background: #fff; font-size: 11pt; }
      .page { grid-template-columns: 1fr; max-width: none; padding: 0; gap: 0; }
      .sidebar, .badge, footer { display: none; }
      .plotfig-frame { box-shadow: none; border-color: #ccc; page-break-inside: avoid; }
      section { page-break-inside: avoid; }
      a { color: inherit; text-decoration: none; }
    }
    """
)

JS = dedent(
    """
    (function(){
      const links = document.querySelectorAll('.toc a');
      const sections = Array.from(links).map(a => document.querySelector(a.getAttribute('href')));
      if (!('IntersectionObserver' in window)) return;
      const io = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (!e.isIntersecting) return;
          links.forEach(l => l.classList.remove('active'));
          const id = e.target.id;
          const active = document.querySelector('.toc a[href="#' + id + '"]');
          if (active) active.classList.add('active');
        });
      }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });
      sections.forEach(s => s && io.observe(s));
    })();
    """
)

# --- content -------------------------------------------------------------

HERO_STATS = "\n".join([
    stat_card("Headline divergence", "+27.5 % / yr",
              "Global ACLED events outpace fatalities (+12.3 %/yr) — slope difference p = 0.006", "accent"),
    stat_card("Lethality collapse", "−69 %",
              "Fatalities per event fell from 1.91 (2014) to 0.59 (2025)", "violet"),
    stat_card("Regional picture", "5 / 6 conform",
              "Only Europe-Central-Asia reverses the pattern (Ukraine war from 2022)", "teal"),
])

TOC = dedent("""\
    <nav aria-label="Contents">
      <ul class="toc">
        <li><a href="#introduction">1. Introduction</a></li>
        <li><a href="#data-methods">2. Data &amp; Methods</a></li>
        <li><a href="#finding-1">3. Finding 1 — Global divergence</a></li>
        <li><a href="#finding-2">4. Finding 2 — Decomposition</a></li>
        <li><a href="#finding-3">5. Finding 3 — Regional story</a></li>
        <li><a href="#africa">6. Africa, 1997–2025</a></li>
        <li><a href="#discussion">7. Discussion &amp; Limitations</a></li>
        <li><a href="#references">References</a></li>
        <li><a href="#appendix">Appendix — Math</a></li>
      </ul>
    </nav>
""")

FINDING_1 = callout("Finding 1 at a glance", [
    "Pearson <em>r</em> = 0.856, Spearman &rho; = 0.811 — series remain correlated.",
    "Log-linear trends: events +27.5&nbsp;%/yr vs fatalities +12.3&nbsp;%/yr.",
    "Pooled regression with series×year interaction: t = &minus;3.06, <strong>p = 0.006</strong>.",
    "Per-event lethality fell from <strong>1.91</strong> (2014) to <strong>0.59</strong> (2025).",
])

FINDING_2 = callout("Finding 2 at a glance", [
    "Shift-share decomposition of &Delta;L (2014&rarr;2025):",
    "<strong>Within-type</strong> effect &asymp; <strong>82&nbsp;%</strong> of the lethality decline.",
    "Composition (mix-shift to Protests, Strategic developments) &asymp; 27&nbsp;%.",
    "Every event type lost lethality — Explosions/Remote violence −78&nbsp;%, VAC −61&nbsp;%, Battles −49&nbsp;%.",
    "Robustness with <code>DISORDER_TYPE</code>: within-type share rises to 92&nbsp;%.",
])

FINDING_3 = callout("Finding 3 at a glance", [
    "Africa &amp; Middle East → <em>within-type lethality collapse</em> (81&nbsp;% and 62&nbsp;%).",
    "Latin America → <em>pure composition shift</em> (~102&nbsp;%); per-type lethality unchanged.",
    "<strong>Europe-Central-Asia reverses</strong>: fatalities +183&nbsp;%/yr vs events +66&nbsp;%/yr (Ukraine, 2022+).",
    "US-Canada enters only 2019; &Delta;L &asymp; 0 — not interpretable in this frame.",
])

AFRICA = callout("Supplement at a glance", [
    "Long series (1997–2025): events +12.0&nbsp;%/yr vs fatalities +2.8&nbsp;%/yr.",
    "Lethality: <strong>8.63 (1997) → 1.42 (2025)</strong>; 95&nbsp;% of &Delta;L is within-type.",
    "Pre-2014 regime: events rose, fatalities <em>fell</em> (&minus;7.5&nbsp;%/yr) — a structural break the 2014 cut hides.",
    "1998–99 DRC / Great Lakes spike: lethality peaked at 33.9 fatalities per event.",
])

# --- assembly -------------------------------------------------------------

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>More Conflicts, More Civilized? — ACLED 2014–2025</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<script>window.MathJax = {{ tex: {{ inlineMath: [['$','$'], ['\\\\(','\\\\)']], displayMath: [['$$','$$'], ['\\\\[','\\\\]']] }}, svg: {{ fontCache: 'global' }} }};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" defer></script>
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <aside class="sidebar">
    <div class="brand">POLI 3148 · Assignment 1</div>
    <div class="brand-sub">ACLED events &amp; fatalities, 2014–2025. Discrepancy, decomposition, regional robustness.</div>
    {TOC}
  </aside>

  <main>
    <header class="masthead">
      <div class="eyebrow">Data report · April 2026</div>
      <h1>More Conflicts, More Civilized?</h1>
      <p class="deck">Global ACLED event counts grew <strong>sixteenfold</strong> between 2014 and 2025. Fatalities grew only <strong>fivefold</strong>. It seems like, while we are having more conflicts, the conflicts are more &ldquo;civilized&rdquo; regarding the unparalleled increasing rate of fatality. Is that true and what may contribute to this discrepancy? This report asks where the gap comes from — a shift in the mix of violence, or a change inside every category — and whether the pattern holds across regions.</p>
      <div class="byline">
        <span><strong>Richard Zhang</strong></span>
        <span>Six ACLED regional weekly files, Mar&nbsp;2026</span>
        <a class="badge" href="{REPO_URL}" target="_blank" rel="noopener">View source &amp; notebooks</a>
      </div>
    </header>

    <div class="hero-stats">{HERO_STATS}</div>

    <section id="introduction">
      <span class="section-number">§ 1</span>
      <h2>Introduction</h2>
      <p>Political violence is commonly tracked through two headline figures: the <em>count</em> of recorded events and the <em>count</em> of fatalities those events produce. Intuitively, the two should share similar trends of dynamics — more conflict, more deaths. However, based on the Armed Conflict Location &amp; Event Data (ACLED) project's weekly regional files from 2014 to 2025, we found that trends between the number of conflicts and fatalities are not statistically identical. The number of recorded events globally rose roughly <strong>sixteenfold</strong> (from 25k to 409k per year), while fatalities grew only <strong>fivefold</strong> (from 47k to 243k). Average per-event lethality collapsed from 1.9 to 0.6. Why is that the case? Does that mean, sarcastically, while we are observing a resurgence of global conflicts, conflicts are turning to a more civilized version, resulting in less lethality?</p>
      <p>Is that true? To discover the real attribution to this discrepancy, we ask three questions in turn:</p>
      <ol>
        <li>Is the divergence real and statistically meaningful?</li>
        <li>Is it explained by a shift toward low-lethality event categories, or by within-category changes?</li>
        <li>Is the pattern global or driven by particular regions?</li>
      </ol>
      <p>A supplementary section extends the analysis to the full Africa series (1997–2025) where coverage is deepest.</p>
    </section>

    <section id="data-methods">
      <span class="section-number">§ 2</span>
      <h2>Data &amp; Methods</h2>
      <p>We use six ACLED regional weekly aggregation files (Africa, Asia-Pacific, Europe &amp; Central Asia, Latin America &amp; the Caribbean, Middle East, US &amp; Canada), dated March 2026. Regional coverage is uneven with regard to the time frame. Taking the most parsimonious converging manner, we restricted the cross-region analyses to 2014–2025. A separate Africa-only frame, loaded before the 2014 filter, is used for the long-run supplement.</p>
      <p>For the first question, we aggregate to annual global totals and compare the two series via Pearson and Spearman correlation, year-over-year growth, and a pooled log-linear regression with a series-by-year interaction that formally tests whether the two trend slopes differ. For the second question, we decompose the change in aggregate lethality into a composition effect, a within-type effect, and an interaction. This is the standard Oaxaca-style shift-share decomposition; because aggregate lethality is exactly a share-weighted average of type lethalities, the decomposition is an identity, not an approximation. For the third question, we repeat both analyses inside each region. All analysis is in Python, with tokens kindly offered by the Anthropic (the antonym of generosity).</p>
    </section>

    <section id="finding-1">
      <span class="section-number">§ 3</span>
      <h2>Finding 1 — The global discrepancy is real</h2>
      {FINDING_1}
      {fig("02_world_map.html", 920, "Cumulative events (top, blue) and fatalities (bottom, red) by country. Drag the year slider or hit <em>Play</em> to watch the panel fill in from 2014 to 2025. Log₁₀ colour scale; hover for country totals.")}
      <p>Across 2014–2025, annual events and fatalities remain strongly positively correlated (Pearson <em>r</em> = 0.856, p &lt; 0.001; Spearman &rho; = 0.811), but grow at sharply different rates. A log-linear fit implies events growing at a rate of <strong>27.5 % per year</strong>, while the fatalities grow at <strong>12.3 %</strong>. In a pooled regression with a series-year interaction, the slope difference is −0.127 log-units (t = −3.06, p = 0.006, thereby standing as a rejection of the null that events and fatalities follow a common trend). The mechanical consequence is that per-event lethality has fallen from <strong>1.91 fatalities per event in 2014 to 0.59 in 2025</strong>, a 69 % decline. The sharpest inflection is between 2017 and 2018, when lethality roughly halves from 1.62 to 0.84.</p>
      {fig("02_dual_axis.html", 470, "Global annual events (blue, left axis) vs. fatalities (red, right axis).")}
      {fig("02_lethality.html", 440, "Global lethality ratio (fatalities per event), 2014–2025.")}
      <p>Two readings are on the table：<br><em>Substantively speaking</em>, the world records more conflict events, but those events are on average smaller.<br><em>Methodologically speaking</em>, ACLED's coverage has expanded, and the added events are disproportionately low-lethality (protests, small clashes) that would previously have gone unrecorded. Both would produce the pattern observed. Finding 2 examines whether this &ldquo;collapse&rdquo; is concentrated in the <em>composition</em> of events or <em>within</em> event types.</p>
    </section>

    <section id="finding-2">
      <span class="section-number">§ 4</span>
      <h2>Finding 2 — Within-type lethality change does most of the work</h2>
      {FINDING_2}
      {fig("03_share_stacked.html", 520, "Shares of events and fatalities by EVENT_TYPE, 2014–2025 (100 %-stacked).")}
      <p>The shift-share decomposition of lethality from 2014 to 2025 attributes <strong>82% to within-type lethality changes, 27% to composition, and −10% to interaction</strong> (shares sum to 100). Both channels operate, but the within-type channel dominates. Composition did shift as expected — the share of events that are Protests rose from 29% to 38%, Strategic developments from 5% to 10%, while Violence-against-civilians fell from 20% to 10% and Battles from 24% to 16%.</p>
      <p>Yet the bigger change is that <em>per-event lethality fell inside every single category</em>:</p>
      <ol>
        <li>Battles from 4.23 to 2.16 (−49%);</li>
        <li>Explosions/Remote violence from 2.58 to 0.58 (−78%);</li>
        <li>Violence-against-civilians from 2.89 to 1.14 (−61%).</li>
      </ol>
      <p>Notably, Explosions/Remote violence actually grew as a share of events (+11%) — compositionally, that would raise lethality — but its own per-event deadliness collapsed so sharply that the net effect is still downward.</p>
      {fig("03_lethality_by_type.html", 500, "Per-event lethality by event type (log scale). All six categories trend downward.")}
      {fig("03_decomposition.html", 500, "Shift-share decomposition: composition vs. within-type contribution to ΔL, by event type.")}
      {fig("03_rolling_decomp.html", 480, "Year-on-year decomposition. Bars sum to the black ΔL line.")}
      <p>Robustness with the coarser disorder type classification gives a stronger within-type share (92%). In other words, it implies that the character of recorded combat has changed — more frequent but smaller engagements, better civilian-protection norms, or more successful remote-violence interception. A measurement reading would say that ACLED is increasingly capturing the long tail of low-casualty incidents within each type. Without an independent ground-truth series, both stories remain on the table and must be treated as joint explanations. We can certainly find other databases for a cross-check or complement the types of casualty, but that will be beyond this study.</p>
    </section>

    <section id="finding-3">
      <span class="section-number">§ 5</span>
      <h2>Finding 3 — The pattern is real but heterogeneous across regions</h2>
      {FINDING_3}
      {fig("04_regional_small_multiples.html", 660, "Annual events (blue) vs. fatalities (red) by region.")}
      <p>Repeating both analyses by region shows the global story is not a single mechanism. In Africa (2014–2025), events grew 13.6% per year against fatalities at 8.4% per year; the decomposition mirrors the global split (25% composition / 81% within). The Middle East shows the same shape, more sharply: events +50% per year, fatalities +26% per year, lethality rate is −1.34, with 78% composition and 62% within (they add to more than 100 because the interaction term is strongly negative).</p>
      <p>Latin America tells a different story: trend slopes barely differ (+38% per year vs +35% per year), and what little lethality decline there is comes almost entirely from composition shift (~102%) — per-type lethality barely moved. This is consistent with a region where the <em>type</em> of unrest has shifted toward protests, not where combat has become less lethal.</p>
      <p>Europe-Central-Asia is the exception that is developing in an &ldquo;uncivilized&rdquo; manner. Fatalities grew 183% per year, against events at 66% per year — per-event lethality <em>rose</em>, driven by the war in Ukraine from 2022. Any global story about &ldquo;declining violence intensity&rdquo; breaks here.</p>
      {fig("04_regional_lethality.html", 700, "Per-event lethality by region, small multiples on linear scale. Dotted grey line = global reference. Europe-Central-Asia rises against the global downward drift; US-and-Canada stays near zero.")}
      {fig("04_regional_decomposition.html", 470, "Share of ΔL explained by composition vs. within-type, by region.")}
      <p>US-and-Canada enters only in 2019 and its &Delta;L is effectively zero — the series is dominated by protests at near-zero lethality and is not interpretable in the same frame. Asia-Pacific looks like a hybrid (66 % composition, 57 % within). The overall conclusion is that the global discrepancy is not a single mechanism. Africa and the Middle East drive the within-type lethality collapse narrative; Latin America is pure composition; Europe-CA is an active-war outlier.</p>
    </section>

    <section id="africa">
      <span class="section-number">§ 6 · Supplement</span>
      <h2>Africa, 1997–2025</h2>
      {AFRICA}
      {fig("05_africa_map.html", 500, "Cumulative events and fatalities by country in Africa, 1997–2025.")}
      <p>Africa's coverage extends back to the late 1990s, allowing a longer view. Over 1997–2025 events grew 12.0% year, while fatalities grew only 2.8% year — a divergence much larger than the post-2014 window shows. Per-event lethality fell from <strong>8.63 to 1.42</strong> (death rate collapsed by −7.21), driven 95% by within-type change.</p>
      <p>Splitting the series reveals two regimes. In <strong>1997–2013</strong>, events grew slowly (+5.5% year) while fatalities actually <em>fell</em> (−7.5% per year) — this is the period that contains the 1998–1999 Second Congo War spike, with lethality peaking at 33.9 fatalities per event in 1999. In <strong>2014–2025</strong>, events grew rapidly (+13.6% every year), and fatalities grew modestly (+8.4% per year) — more recording, moderate lethality. The 2014 cut, therefore, averages across a structural break that is obvious in the long series.</p>
      {fig("05_africa_dual_axis.html", 450, "Africa annual events vs. fatalities, 1997–2025.")}
      {fig("05_africa_lethality.html", 450, "Africa per-event lethality, 1997–2025. Dashed lines mark 2011 and the 2014 cutoff.")}
      {fig("05_africa_rolling_decomp.html", 480, "Year-on-year shift-share decomposition for Africa, 1998–2025.")}
      <p>The long-run view <em>reinforces</em> the cross-region finding: even net of the DRC/Rwanda mass-violence episode and pre-2011 thin coverage, most of the long-run lethality decline is a within-type change, not a mix shift. That said, coverage-expansion bias is mechanically stronger over a 29-year window than a 12-year one, so the real-world vs measurement ambiguity is also larger.</p>
    </section>

    <section id="discussion">
      <span class="section-number">§ 7</span>
      <h2>Discussion &amp; Limitations</h2>
      <p>Three caveats bound these findings. <strong>First</strong>, coverage is not uniform across regions or time: Europe-Central Asia, Latin America, and US-Canada enter the panel late, and pre-2014 coverage (used only for Africa) is thinner than post-2014. Analyses on the common 2014–2025 window mitigate but do not remove this. <strong>Second</strong>, ACLED's sourcing has expanded over the period — an endogenous increase in the event denominator mechanically reduces average per-event lethality without any change in underlying violence. Finding 2's within-type effect is consistent with either a real change in combat character or the within-type equivalent of coverage expansion, and the data cannot distinguish between them. <strong>Third</strong>, the shift-share decomposition is descriptive, not causal: it partitions the change of the lethality rate into algebraic components, not into structural mechanisms. Any claim that "violence has become less deadly" rather than "the recording of violence has broadened" would need an external benchmark this report does not construct.</p>
    </section>

    <section id="references">
      <span class="section-number">§</span>
      <h2>References</h2>
      <ul>
        <li>Raleigh, C., Linke, A., Hegre, H., &amp; Karlsen, J. (2010). <em>Introducing ACLED: An Armed Conflict Location and Event Dataset.</em> Journal of Peace Research, 47(5).</li>
        <li>ACLED Codebook (2024 edition, <code>acled-codebook.html</code>).</li>
        <li>ACLED regional aggregation files, downloaded week-of 21/28 March 2026.</li>
      </ul>
    </section>

    <section id="appendix">
      <span class="section-number">Appendix</span>
      <h2>Mathematical formulation</h2>

      <h3>A.1 Annual aggregation</h3>
      <p>Let $w$ index weeks and $t$ index calendar years. For each region $r$ (or for the global panel) we aggregate weekly cells to annual totals of events $E_t$ and fatalities $F_t$:</p>
      <p>$$E_t \\;=\\; \\sum_{{w \\in t}} \\text{{EVENTS}}_w, \\qquad F_t \\;=\\; \\sum_{{w \\in t}} \\text{{FATALITIES}}_w.$$</p>
      <p>The aggregate per-event lethality and the year-over-year growth rate are</p>
      <p>$$L_t \\;=\\; \\frac{{F_t}}{{E_t}}, \\qquad g^Y_t \\;=\\; \\frac{{Y_t}}{{Y_{{t-1}}}} - 1 \\quad\\text{{for }} Y \\in \\{{E, F\\}}.$$</p>

      <h3>A.2 Correlation and log-linear trend</h3>
      <p>Between annual series $\\{{E_t\\}}$ and $\\{{F_t\\}}$ we report Pearson's $r$ and Spearman's $\\rho$. The log-linear trend for each series is</p>
      <p>$$\\log Y_t \\;=\\; \\alpha_Y + \\beta_Y \\cdot t + \\varepsilon_t, \\qquad \\hat{{g}}_Y \\;=\\; e^{{\\hat\\beta_Y}} - 1,$$</p>
      <p>where $\\hat{{g}}_Y$ is the annualised percentage growth implied by the fitted slope.</p>

      <h3>A.3 Pooled interaction test for slope equality</h3>
      <p>To formally test whether the events and fatalities trends share a common slope, we stack the two log-series and fit</p>
      <p>$$\\log Y_{{t,s}} \\;=\\; \\beta_0 + \\beta_1 \\cdot t + \\beta_2 \\cdot \\mathbb{{1}}[s = F] + \\beta_3 \\cdot \\bigl(t \\cdot \\mathbb{{1}}[s = F]\\bigr) + \\varepsilon_{{t,s}},$$</p>
      <p>where $s \\in \\{{E, F\\}}$ identifies the series. The coefficient $\\beta_3$ is exactly the difference between the fatalities and events log-slopes; the null hypothesis of interest is</p>
      <p>$$H_0: \\beta_3 = 0 \\quad\\text{{vs.}}\\quad H_1: \\beta_3 \\neq 0,$$</p>
      <p>tested by the usual OLS <em>t</em>-statistic $t = \\hat\\beta_3 / \\widehat{{\\text{{SE}}}}(\\hat\\beta_3)$.</p>

      <h3>A.4 Shift-share decomposition</h3>
      <p>Let $k$ index event categories (<code>EVENT_TYPE</code> or <code>DISORDER_TYPE</code>). Define the category share of events and the category per-event lethality as</p>
      <p>$$s_{{k,t}} \\;=\\; \\frac{{E_{{k,t}}}}{{E_t}}, \\qquad l_{{k,t}} \\;=\\; \\frac{{F_{{k,t}}}}{{E_{{k,t}}}}.$$</p>
      <p>Because aggregate lethality is exactly a share-weighted average of category lethalities,</p>
      <p>$$L_t \\;=\\; \\frac{{F_t}}{{E_t}} \\;=\\; \\sum_k \\frac{{E_{{k,t}}}}{{E_t}} \\cdot \\frac{{F_{{k,t}}}}{{E_{{k,t}}}} \\;=\\; \\sum_k s_{{k,t}} \\, l_{{k,t}},$$</p>
      <p>the change $\\Delta L = L_1 - L_0$ between a base period $t=0$ and an end period $t=1$ admits the Oaxaca-style identity</p>
      <p>$$\\Delta L \\;=\\; \\underbrace{{\\sum_k (s_{{k,1}} - s_{{k,0}})\\, l_{{k,0}}}}_{{\\text{{composition}}}} \\;+\\; \\underbrace{{\\sum_k s_{{k,0}}\\, (l_{{k,1}} - l_{{k,0}})}}_{{\\text{{within-type}}}} \\;+\\; \\underbrace{{\\sum_k (s_{{k,1}} - s_{{k,0}})(l_{{k,1}} - l_{{k,0}})}}_{{\\text{{interaction}}}}.$$</p>
      <p>This is an algebraic identity, not a regression-based approximation: the three terms sum exactly to $\\Delta L$. Reported percentages ("27 % composition / 82 % within-type") are each term divided by $\\Delta L$.</p>

      <h3>A.5 Regional and long-run application</h3>
      <p>For RQ3 all of A.1–A.4 are applied to each region independently, using that region's earliest and latest years in the 2014–2025 window as $(t_0, t_1)$ for the decomposition. For the Africa supplement, $t_0$ and $t_1$ are the first and last years of the full 1997–2025 series, and sub-window decompositions use $t_0 = 1997, t_1 = 2013$ and $t_0 = 2014, t_1 = 2025$.</p>
    </section>

    <footer>
      Generated by <code>code/Z_generate_report.py</code> from notebooks <code>01–05</code>.
      Figures are interactive Plotly HTMLs embedded as iframes from <code>docs/figures/</code>.
      · <a href="{REPO_URL}">repository</a>
    </footer>
  </main>
</div>
<script>{JS}</script>
</body>
</html>
"""


def main() -> None:
    if not FIGDIR.exists():
        raise SystemExit(f"Missing figure directory {FIGDIR}; run the notebooks first.")
    OUT.write_text(HTML, encoding="utf-8")
    print(f"Wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
