# Term Paper Submission Checklist

This checklist tracks everything that must be in place before submitting the OpenClaw-Agent term paper to a venue (NeurIPS-style preprint, OpenReview, HAL, arXiv cross-post).

## Repository

- [ ] GitHub repository public: https://github.com/jeandirel/securefinai-openclaw-agent
- [ ] `README.md` complete (project context, install, run, structure, ethics, links)
- [ ] `requirements.txt` present and pinned
- [ ] `.env.example` present, no real secrets in repo
- [ ] `.gitignore` excludes `.env`, `logs/`, `__pycache__/`
- [ ] `LICENSE` present (MIT)
- [ ] `CITATION.cff` present and accurate
- [ ] `SUBMISSION_CHECKLIST.md` (this file) up to date

## Paper

- [ ] `paper/main.tex` complete (Abstract, Introduction, Related Work, Problem Formulation, Methodology, Experimental Protocol, Experimental Plan or Results, Discussion, Limitations, Ethics, Conclusion, Appendix)
- [ ] `paper/references.bib` complete and compiles
- [ ] PDF compiled successfully on Overleaf with `\\usepackage[preprint]{neurips_2024}`
- [ ] No fake / fabricated experimental numbers
- [ ] All references manually verified (no broken or hallucinated citations)
- [ ] All claims in the paper are either cited or supported by the implementation

## AI reviews

- [ ] ChatGPT review obtained and link added to `reviews/README.md`
- [ ] Claude review obtained and link added to `reviews/README.md`
- [ ] Grok review obtained and link added to `reviews/README.md`
- [ ] Gemini Think review obtained and link added to `reviews/README.md`
- [ ] Iteration log updated in `reviews/README.md`
- [ ] Checklist of corrections in `reviews/README.md` resolved or explicitly deferred

## External submissions

- [ ] OpenReview submission completed; link added to `README.md`
- [ ] HAL submission completed; link added to `README.md`
- [ ] arXiv cross-post enabled; link added to `README.md`

## Final sanity checks

- [ ] No API keys, tokens, or personal credentials anywhere in the repo
- [ ] No real-money trading code paths enabled
- [ ] All metrics in `results/metrics_template.json` are either real (computed from Alpaca paper logs) or `null`
- [ ] Final submission package (PDF + bib + repo link) ready

> **Warning.** Do not submit the paper while `results/metrics_template.json` contains fabricated numbers. If the live paper-trading run is too short, keep the values `null` and clearly state the empirical status in the paper.
