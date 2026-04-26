# AI-Generated Reviews of the OpenClaw-Agent Paper

This folder collects independent NeurIPS-style reviews of `paper/main.tex` (revision **v3**, commit on 2026-04-26) produced by major frontier LLMs. The same prompt was sent to each model. Links to the public conversations are recorded below for transparency and reproducibility.

## Review prompt

The exact prompt sent to every model is in [`review_prompt.md`](review_prompt.md). The prompt asks each model to write a NeurIPS-level review based on the official NeurIPS [Evaluation Criteria](https://neurips.cc/Conferences/2015/PaperInformation/EvaluationCriteria) and [Reviewer Guidelines](https://neurips.cc/Conferences/2025/ReviewerGuidelines), and to evaluate Summary, Strengths, Weaknesses, Originality, Quality, Clarity, Significance, Reproducibility, Ethics, Missing references, and a final recommendation.

The PDF reviewed is the v3 version of the paper (8 pages, post external NeurIPS-style audit), as recorded in [`../CHANGELOG_REVIEW.md`](../CHANGELOG_REVIEW.md).

## Reviews summary

| Model | Public link | Recommendation | Status |
|-------|-------------|----------------|--------|
| Gemini 2.5 (Google) | [gemini.google.com/share/82e9bb6db1e2](https://gemini.google.com/share/82e9bb6db1e2) | Reject for NeurIPS main track; suitable for a NeurIPS workshop or contest report after empirical results are produced | Completed |
| ChatGPT (OpenAI) | [chatgpt.com/share/69ed70f2-c78c-83eb-b35d-c0835462e3b5](https://chatgpt.com/share/69ed70f2-c78c-83eb-b35d-c0835462e3b5) | Revise before submission; structurally sound, blocked by absence of empirical results | Completed |
| Grok (xAI) | [grok.com/share/c2hhcmQtNQ\_98224744-386f-4792-9a03-cd38375d091c](https://grok.com/share/c2hhcmQtNQ_98224744-386f-4792-9a03-cd38375d091c) | Not ready for NeurIPS main track in current form; redirect to a workshop or finance-ML venue once H1 is tested | Completed |
| Claude (Anthropic) | [claude.ai/share/5a588ab7-b8d5-4083-bf2d-cd63e97220e7](https://claude.ai/share/5a588ab7-b8d5-4083-bf2d-cd63e97220e7) | Strong Reject for NeurIPS main track in current form; constructive path: SecureFinAI contest report, NeurIPS workshop, or position paper | Completed |

## Synthesis

All four reviewers converge on the same diagnosis: the architecture (LLM as bounded Boolean veto, deterministic risk envelope as runtime shield) and the pre-registered evaluation protocol (H1, baselines B1--B4, ablations A1--A3, Benjamini--Hochberg correction, `null`-reporting stop-rule) are sound and intellectually honest, but the absence of empirical results makes the paper not yet ready for NeurIPS main-track submission. None of the reviewers contests the structural claims; all four flag the same actionable next step -- run the protocol, then re-target a workshop or finance-ML venue.

The author concurs with this diagnosis. The current revision (v3) is positioned as (a) a SecureFinAI Contest 2026 Task V system and protocol report, (b) a PGE5 term paper at Aivancity, and (c) an arXiv / HAL preprint, not as a NeurIPS main-track submission.

## Notes on transparency

- Each link points to a public share of the original conversation, hosted by the respective provider. Conversations have not been edited.
- Public share links may expire or be revoked by the provider. Local copies of the review text can be stored alongside this file (e.g., `gemini.md`, `chatgpt.md`, `grok.md`, `claude.md`) if long-term archival is required.
- The author reserves the right to disagree with individual review points, but has incorporated all actionable feedback that does not require fabricating empirical results, as documented in [`../CHANGELOG_REVIEW.md`](../CHANGELOG_REVIEW.md) under the v3 section.
