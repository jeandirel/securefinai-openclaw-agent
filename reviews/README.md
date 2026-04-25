# AI-Generated Reviews of the OpenClaw-Agent Paper

This folder collects independent NeurIPS-style reviews of `paper/main.tex` produced by major frontier LLMs. The same prompt is sent to each model. Links to the public conversations are recorded below for transparency and reproducibility.

## Review prompt

The exact prompt sent to every model is in [`review_prompt.md`](review_prompt.md). Please send that prompt verbatim, attaching the LaTeX source of `paper/main.tex`.

## Reviews summary

| Model         | Public link                          | Recommendation                | Status   |
|---------------|--------------------------------------|-------------------------------|----------|
| ChatGPT       | *to be added*                        | *to be added*                 | pending  |
| Claude        | *to be added*                        | *to be added*                 | pending  |
| Grok          | *to be added*                        | *to be added*                 | pending  |
| Gemini Think  | *to be added*                        | *to be added*                 | pending  |

Allowed values for **Recommendation**: `Strong Reject`, `Reject`, `Weak Reject`, `Borderline`, `Weak Accept`, `Accept`, `Strong Accept`.

Allowed values for **Status**: `pending`, `received`, `integrated`.

## Iteration log

Use this section to keep a short, dated journal of every revision cycle driven by the AI reviews.

| Date (YYYY-MM-DD) | Revision | Trigger (model)   | Summary of changes |
|-------------------|----------|-------------------|--------------------|
| *to be added*     | v0.1     | initial draft     | first complete draft of `paper/main.tex` |
| *to be added*     | v0.2     | *to be added*     | *to be added* |

## Checklist of corrections

After every review round, tick the items that have been addressed in `paper/main.tex`:

- [ ] Abstract clearly states the contribution
- [ ] Introduction motivates the risk-aware design
- [ ] Related work covers SecureFinAI, FinRL-DeepSeek, look-ahead bias
- [ ] Problem formulation is mathematically explicit
- [ ] System architecture figure or paragraph is present
- [ ] Technical signal layer is fully specified
- [ ] LLM filter is specified as veto-only
- [ ] Risk envelope constants are documented
- [ ] Logging format is described
- [ ] Experimental protocol is reproducible
- [ ] No fabricated experimental numbers
- [ ] Limitations section is honest
- [ ] Ethical considerations section is present
- [ ] References compile and are not fake
- [ ] Repository link is correct

## Notes

- Each review must be obtained from a fresh, public conversation so that the link can be shared in the table above.
- Do not edit the model output; copy it verbatim into a per-model file (e.g. `reviews/chatgpt.md`) when archiving locally.
- If a review contains private or sensitive information, do not commit it; only commit the recommendation summary.
