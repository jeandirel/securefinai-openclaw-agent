# Results

This folder collects the empirical metrics of the OpenClaw-Agent paper-trading run. **Metrics must be computed from the actual Alpaca paper-trading logs** produced by `agent/main.py` and helper scripts in `scripts/`. **Do not replace `null` values with invented numbers.**

## Files

- `metrics_template.json` -- canonical schema for the reported metrics. Keep `null` for any metric that has not yet been computed from real logs.

## Expected metrics

| Metric                | Description |
|-----------------------|-------------|
| `cumulative_return`   | Total return of the paper-trading equity curve over the evaluation window, expressed as a decimal (e.g. `0.05` = +5%). |
| `sharpe_ratio`        | Annualised Sharpe ratio computed from the equity curve, using the convention documented in the paper (typically risk-free rate = 0 for paper trading). |
| `max_drawdown`        | Maximum peak-to-trough drawdown of the equity curve, as a non-negative decimal (e.g. `0.12` = 12%). |
| `volatility`          | Annualised realised volatility of the equity curve. |
| `llm_veto_rate`       | Fraction of candidate orders proposed by the rules layer that the LLM filter vetoed (`vetoed / proposed`). `null` when the LLM filter is disabled. |
| `decision_consistency`| Fraction of decision cycles in which the rules layer and the LLM filter agreed. `null` when the LLM filter is disabled. |

## How to compute

1. Run the agent in paper trading and let it generate logs in `logs/`.
2. Use `scripts/export_equity.py` to export the equity curve.
3. Compute each metric from the exported logs using your own analysis script (notebook or standalone Python).
4. Write the resulting numbers into `metrics_template.json`, replacing the corresponding `null` values.
5. Commit the updated JSON together with a short note in the paper's experimental section.

## Honest reporting

If the live paper-trading run is too short or the LLM filter has been disabled, leave the affected fields as `null` and clearly state this in the paper. Do not fabricate, interpolate, or back-fill numbers from synthetic data.
