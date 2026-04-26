# CHANGELOG_REVIEW

This document records the scientific upgrade applied to the paper and the
bibliography on 2026-04-26, prior to OpenReview / HAL submission and before
soliciting AI reviews.

## Files modified

- `paper/main.tex` -- full rewrite (see Section "What changed in main.tex").
- `paper/references.bib` -- full rewrite (see Section "What changed in references.bib").
- `CHANGELOG_REVIEW.md` -- new file (this document).

## What changed in main.tex

### Title and author
- New title: *OpenClaw-Agent: A Constrained, Auditable Architecture for
  LLM-Assisted Crypto Paper Trading*. Reframes the contribution around
  bounded LLM autonomy, safety by design, and auditability.
- Author email corrected to `jeandirel.nzekabeyene@aivancity.education`.
- Affiliation set to *PGE5 -- AI in Finance, Aivancity, Paris-Cachan*.

### Abstract
- Sharper, research-oriented framing.
- Names two prior LLM trading systems (TradingAgents, FinMem) and contrasts
  the LLM-as-veto design with their fully autonomous design.
- Drops the words *term paper* and *small agent*.

### Introduction
- Two failure modes (hallucination, look-ahead bias) are now cited
  directly: `hallucination_survey_zhang2023` and `lookaheadbench`.
- Removes the uncited claim that pure LLM agents are *unstable under
  distribution shift*.
- Removes *free of survivorship bias* (over-claim) -- replaced by a more
  honest framing of universe selection.
- Three contributions are now numbered.
- Explicit honest-reporting commitment in the last paragraph.

### Related Work
- Restructured into six paragraphs: LLM trading agents, RL in financial
  markets, Look-ahead bias, Live forecasting benchmarks (out-of-domain
  context), Reproducibility, Hallucination.
- Contest task name corrected to *Task V: Agentic Trading Using OpenClaw*.
- VCBench, YC Bench, FutureX explicitly flagged as out-of-domain context.

### Problem Formulation
- New section, with formal notation: $\mathcal{U}$, $X_t$, $P_t$,
  $\mathcal{A}$, $a_t$, $q_t$.
- Hard constraints written as four labelled equations
  (per-position, gross, stop-loss, take-profit).

### Methodology
- Introduces the formal decision pipeline
  $(a_t, q_t) = \mathcal{R} \circ \mathcal{V}_{\text{LLM}} \circ \mathcal{S}(X_t, P_t)$.
- LLM veto operator $\mathcal{V}_{\text{LLM}}$ defined as a piecewise
  function that can only return $(\hat{a}_t, \hat{q}_t)$ or
  $(\textsc{hold}, 0)$ -- this is the architectural guarantee against
  hallucinated trades.
- Risk envelope $\mathcal{R}$ formalised as the final gate.
- Logging subsection now cites `pineau_reproducibility2020`.

### Experimental Section
- Renamed *Experimental Protocol and Evaluation Plan*.
- States contest constants explicitly:
  \$100{,}000 initial equity, JSONL+CSV submission format.
- Names primary metric (Cumulative Return) and secondary metrics
  (Sharpe, MD, Daily Volatility, Annualised Volatility) per Task V.
- Adds two diagnostic metrics with explicit formulas: LLM veto rate
  $\rho$ and decision consistency $\kappa$.
- Pre-registers four baselines (B1--B4) and three ablations (A1--A3).
- Adds statistical caveats: bootstrap 95% CI; threshold
  $T_{\min} = 500$ cycles per account.
- Adds an explicit *stop-rule*: rows below $T_{\min}$ are reported
  as "insufficient data" rather than imputed.

### Limitations
- Six labelled paragraphs: no empirical results, selection bias, paper-trading
  idealisations, LLM is not a forecaster, provider sensitivity, bibliographic
  concentration.

### Ethical Considerations
- Six labelled paragraphs: no financial advice, no personal data, credentials
  hygiene, LLM safety envelope, compliance, reproducibility transparency.

### Removed phrases
- "term paper", "we hope", "small agent", "free of survivorship bias",
  "unstable reasoning under distribution shift".

## What changed in references.bib

- `finrl_deepseek` -- unchanged (already verified).
- `uniswap_rl` -- added note about AAAI 2025 workshop acceptance.
- `lookaheadbench` -- unchanged (already verified).
- `vcbench` -- *Rick Chen and others* replaced by the full 10-author list,
  verified against arXiv.
- `ycbench` -- title corrected to *YC Bench* (with a space, as on arXiv);
  added `eprint`, `archivePrefix`, `primaryClass=cs.LG`.
- `futurex` -- author list shortened to *Zhiyuan Zeng and Jiashuo Liu and
  Siyuan Chen and others* (paper has 31 authors; "and others" is acceptable).
- `scaling_open_ended` -- *Nikhil Chandak and others* replaced by the full
  5-author list; year corrected from 2026 to 2025 (v1 was 31 Dec 2025).
- `securefinai2026` -- title now includes the official task name
  *Task V: Agentic Trading Using OpenClaw*; added `note = {Accessed: 2026-04-26}`.
- `alpaca_api` -- URL corrected from `alpaca.markets/docs/` to the canonical
  `docs.alpaca.markets/`; added `note = {Accessed: 2026-04-26}`.
- `tradingagents_xiao2024` -- **NEW**, verified on arXiv.
- `finmem_yu2023` -- **NEW**, verified on arXiv.
- `hallucination_survey_zhang2023` -- **NEW**, verified on arXiv.
- `pineau_reproducibility2020` -- **NEW**, verified on arXiv.

All 13 entries verified against their arXiv abstract pages or the official
SecureFinAI Contest 2026 page on 2026-04-26. No fake or placeholder entries
remain. Bibliographic concentration on a single author drops from 3/9 to
3/13.

## What is still missing

- Live empirical results: the paper-trading run is still accumulating data;
  metrics in `results/metrics_template.json` remain `null` by design.
- AI reviews (ChatGPT, Claude, Grok, Gemini Think): to be solicited using
  `reviews/review_prompt.md` and the upgraded PDF.
- OpenReview / HAL / arXiv submissions: pending the final PDF.
- Optional follow-up: enumerate the 31 FutureX authors in full; replace
  *and others* there as well.

## Verification log

- All 13 references verified directly on arXiv abstract pages
  (https://arxiv.org/abs/<id>) on 2026-04-26.
- SecureFinAI Contest 2026 Task V official name verified on
  https://open-finance-lab.github.io/SecureFinAI_Contest_2026/.
- Alpaca docs canonical URL verified via Google search; subdomain is
  `docs.alpaca.markets`, not `alpaca.markets/docs/`.
