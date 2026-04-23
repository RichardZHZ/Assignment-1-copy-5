# Note on AI use

This document describes how Claude Code (Anthropic's CLI for Claude) was used in producing this assignment, what was AI-drafted versus user-reviewed, and how outputs were validated.

## Tool and role

The work was mainly carried out in an interactive Claude Code session. Claude acted as a coding collaborator in supporting the author to propose the folder structure, write the five analysis notebooks, execute them non-interactively, and prepare the generator that assembles `docs/index.html` from the Plotly figure HTMLs (with transcript written by the author manually). In every step of collaboration, Claude paused to surface numerical results before moving on to the next step, which is how the author reviewed intermediate findings.

## Step-by-step split between AI and the author

- **Scoping.** The workflow brief (`CLAUDE_WORKFLOW_PROMPT.md`) was created by the author before the session began. Claude followed it step by step.
- **Environment setup.** Claude proposed a `conda` environment with explicit packages and installed it after the user approved. The user approved each non-trivial install (`pyarrow` was added after the first run failed).
- **Data cleaning (`01_*.ipynb`).** Claude wrote the notebook; the user reviewed coverage dates and the annual totals before proceeding. The user noted the absence of the two top-level sanity-check files, and Claude adjusted (skipped that cross-check).
- **Global discrepancy (`02_*.ipynb`).** Claude wrote the notebook, including a pooled log-linear regression with a series × year interaction term. The user provided the basic formula and reviewed all the numerical findings before moving on.
- **Shift-share decomposition (`03_*.ipynb`).** The author chose the Oaxaca-style shift-share decomposition as the quantitative method, and Claude followed through; the author reviewed the result.
- **Regional robustness (`04_*.ipynb`).** Claude drafted the per-region loop; the author rewrote most proportions of the summary and surfaced the Europe-Central-Asia counter-trend (Ukraine effect) in discussion.
- **Africa long-run (`05_*.ipynb`).** Same pattern. The author reviewed and confirmed that the pre/post-2014 split showed a structural break.
- **Report draft (§ 3.5 of the workflow).** Author drafted the narrative in Word and showed it to Claude for grammar checking before letting Claude render it into HTML. The user approved the draft after reading it; Claude then wrote `code/Z_generate_report.py` and rendered `docs/index.html`.

## Validation

- Each notebook was executed top-to-bottom with `jupyter nbconvert --execute`; cells that raised errors during authoring (a `scipy.linregress` shape mismatch in the regional notebook) were fixed and re-run until execution was clean.
- Numerical claims in the report were cross-checked against the notebooks: annual totals and decomposition shares were recomputed in ad-hoc shell scripts against the saved `acled_clean.parquet` to verify the narrative numbers match the notebook cell outputs.
- All figures in the report are iframed directly from the executed notebooks' saved Plotly HTMLs — the report cannot diverge from the notebook outputs because it re-uses the same files.
- Coverage windows and structural breaks are documented in the narrative and the Discussion & Limitations section.

## What was NOT delegated to AI

- Interpretation of the results (e.g., the measurement-vs-substance framing in §4 and §7) and the draft of text were mainly drafted by the author (yes, the very me) and approved by the author. Claude provided side support in grammar checking and structural refining.
- Decisions about which datasets to commit publicly vs. gitignore, and every push to GitHub, required explicit user approval. Thanks for Kadi's prompt. 
- The scope of the research questions and the overall methodology were set by the user in `CLAUDE_WORKFLOW_PROMPT.md`.

