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


---

## v3 (2026-04-26) -- Post external NeurIPS-style review

This revision integrates the actionable feedback from an external NeurIPS-style review of v2. The reviewer's overall recommendation was `Strong Reject for NeurIPS main track in current form`, with the diagnosis that the paper is best read as a system description plus an evaluation plan, not a research paper with findings. We do not contest that diagnosis: no empirical results are reported here either. We do, however, sharpen the architecture-level claims and the protocol-level rigour where possible.

### Changes in `paper/main.tex`

- **Soften the central claim.** Removed the wording that framed the LLM-veto subset property as an "architectural guarantee" / contribution. It is now stated explicitly as a *structural property* (true by construction) and is contrasted with the *empirical* claims tested under the protocol. New subsection `Structural property` (Section 4.6) makes the subset relation `A_exec \subseteq A_S \cup {(HOLD,0)}` explicit and labels it as definitional, not as a finding.
- **Split structural vs. empirical claims.** New paragraph in the Introduction (`Structural vs. empirical claims`) and a rewritten Discussion section that separates the two classes of claim. The Discussion no longer says the LLM "can only reduce risk" -- it now says `V_LLM` cannot increase exposure, and explicitly notes that vetoing a profitable trade is itself an opportunity-cost form of risk.
- **Pre-registered falsifiable hypothesis (H1).** New paragraph in Section 5: H1 = "the LLM-veto layer reduces realised maximum drawdown by at least \(\Delta_{\text{MD}} = 2\) percentage points relative to baseline B3 (rules+risk), at the cost of at most \(\Delta_{\text{CR}} = 1\) percentage point in cumulative return." Rejection criteria are stated in terms of bootstrap 95 % CIs, and the thresholds are pre-registered (no post-hoc tuning).
- **Multiple-comparison correction.** New paragraph specifying Benjamini--Hochberg correction at FDR \(\alpha = 0.10\) over the family of secondary comparisons in the B1--B4 \(\times\) A1--A3 grid. H1 is the only confirmatory test.
- **Justification of \(T_{\min} = 500\).** New paragraph: \(T_{\min} = 500\) at \(\Delta_t = 30\) min is roughly 10--11 calendar days of continuous operation, framed explicitly as a minimum reporting threshold rather than a power-analysed sufficient horizon for asymptotic Sharpe inference. A formal power analysis is deferred to a future revision.
- **A2 ablation caveat.** The A2 ablation (OpenAI vs. Anthropic at fixed temperature, identical prompt) is now labelled exploratory rather than confirmatory, with an explicit acknowledgement that it confounds provider identity with prompt-following behaviour.
- **Reading order of Eq. (5).** The decision pipeline is now described as outer-to-inner (\(\mathcal{S}\) first, then \(\mathcal{V}_{\text{LLM}}\), then \(\mathcal{R}\) last), which matches the standard reading of function composition more clearly.
- **Diagnostic vs. confirmatory metrics.** \(\rho\) and \(\kappa\) are now explicitly described as descriptive diagnostics, not test statistics for H1.
- **Related Work expanded.** New paragraphs covering: (i) LLM agent frameworks (ReAct~\cite{react_yao2022}, Reflexion~\cite{reflexion_shinn2023}); (ii) domain-specific finance LLMs (BloombergGPT~\cite{bloomberggpt_wu2023}, FinGPT~\cite{fingpt_yang2023}); (iii) safe RL and shielded control (Alshiekh et al.~\cite{shielded_rl_alshiekh2018}), with explicit text noting that \(\mathcal{R}\) plays the same logical role as a post-posed shield. Empirical evidence that LLMs extract predictive signal from financial text is acknowledged via Lopez-Lira and Tang~\cite{lopezlira_tang2023}.
- **Bibliographic concentration.** Limitations section updated to acknowledge partial mitigation of the single-author concentration via the new finance-LLM, LLM-agent, and safe-RL references.
- **Off-the-shelf signal layer flagged.** New Limitations paragraph explicitly states that \(\mathcal{S}\) uses a textbook EMA/RSI/momentum aggregation with no walk-forward calibration and no transaction-cost model, and that since \(\mathcal{V}_{\text{LLM}}\) cannot originate trades, the achievable upside of the full system is upper-bounded by the quality of \(\mathcal{S}\).

### Changes in `paper/references.bib`

Six new references added, all verified on arXiv:

- `react_yao2022` (arXiv:2210.03629) -- ReAct: Synergizing Reasoning and Acting in Language Models.
- `reflexion_shinn2023` (arXiv:2303.11366) -- Reflexion: Language Agents with Verbal Reinforcement Learning.
- `shielded_rl_alshiekh2018` (arXiv:1708.08611, AAAI 2018) -- Safe Reinforcement Learning via Shielding.
- `bloomberggpt_wu2023` (arXiv:2303.17564) -- BloombergGPT: A Large Language Model for Finance.
- `fingpt_yang2023` (arXiv:2306.06031) -- FinGPT: Open-Source Financial Large Language Models.
- `lopezlira_tang2023` (arXiv:2304.07619) -- Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models.

No previous references were removed; the v2 bibliography is preserved verbatim and only extended.

### What v3 deliberately does *not* attempt to fix

- **Empirical results.** No empirical numbers are reported. The reviewer correctly identifies this as fatal for NeurIPS main-track submission, and we agree. The honest path is to run the protocol of Section 5 and report the result, not to inflate the present draft. v3 sharpens the protocol but does not claim experimental findings.
- **Anonymisation for double-blind submission.** The current draft remains a *preprint* with author identity on page 1 and a public GitHub link in the Appendix. NeurIPS-style anonymisation (e.g., redirecting the GitHub URL to an anonymous fork) is a packaging step that will only be applied at the moment of an actual NeurIPS submission, not in this PGE5 / preprint version.
- **Theoretical regret bound.** The reviewer suggests adding a regret decomposition (signal regret + veto regret + envelope regret). v3 does not include such a result. We mention it as a future direction but do not invent a theorem we have not proved.

### Honest assessment after v3

v3 does not turn the paper into a NeurIPS main-track submission. With zero empirical results, the reviewer's diagnosis still applies. v3's purpose is narrower: to make the structural claims rigorous, the empirical claims falsifiable, and the literature review credible, so that the same draft can be honestly presented as (a) a SecureFinAI Contest 2026 Task V system + protocol report, (b) a PGE5 term paper at Aivancity, and (c) an arXiv / HAL preprint. Once H1 has been tested on a sufficiently long paper-trading log, the paper can be re-targeted at a NeurIPS workshop or a finance-ML venue (ICAIF, ACM AI in Finance) with a real evaluation section.
