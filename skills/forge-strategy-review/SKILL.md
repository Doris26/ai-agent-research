---
name: strategy-review
description: "Code review every strategy before posting results. Check for execution bugs, double orders, look-ahead bias, and architecture issues. Learned from Nova's reviews."
---

# Strategy Code Review — MANDATORY before posting results

## When to Use
After writing or modifying ANY strategy code, before running backtest.

## Review Checklist (ALL items)

### 1. Double-Order Bug (CRITICAL)
- **NEVER** call `liquidate()` + `set_holdings()` in the same `on_data` for the same symbol
- `set_holdings()` already handles full position transition (short→long, long→short)
- Use `liquidate()` ONLY for exit-to-flat (no new position)
- **Bad:** `if is_short: self.liquidate(); self.set_holdings(long_sz)` = 2x position
- **Good:** `self.set_holdings(long_sz)` directly flips from short to long

### 2. Look-Ahead Bias
- Signal must use data available BEFORE the current bar close
- No same-bar execution: signal at bar N → execute at bar N+1
- QC Cloud's `set_holdings` executes at next bar open (correct)
- But indicators computed from current bar's close ARE look-ahead if used for same-bar entry

### 3. Indicator Readiness
- Never fallback to neutral values (e.g., RSI=50) when indicator not ready
- Always check `.is_ready` and `return` if not ready
- `set_warm_up()` should cover ALL indicators (use max period + buffer)

### 4. Data Source Consistency
- BTCUSD vs BTCUSDT — different data sources, fees, liquidity on QC
- Match what will be used in live trading
- Document which symbol and why

### 5. Position Sizing
- Vol targeting: verify annualization factor (sqrt(365) for crypto, sqrt(252) for equities)
- Short sizing cap: verify shorts are limited (0.5x or less)
- No uncapped leverage: `min(target/realized, 1.0)` not `target/realized`

### 6. Exit Logic
- Force exits (e.g., SMA break) must not conflict with entry logic
- Check: can a force exit and new entry happen in the same bar?
- If yes, which takes priority? Document it.

### 7. Window Parameters
- Backtest window must match what Golden Sheet expects (1Y recent + 2022 crash)
- `set_start_date`/`set_end_date` must be correct for each window

## Output Format
After review, post to Discord:
```
**Code Review: [Strategy Name]**
- Double-order: PASS/FAIL [details]
- Look-ahead: PASS/FAIL
- Indicator readiness: PASS/FAIL
- Data source: [symbol] [reason]
- Position sizing: PASS/FAIL
- Exit conflicts: PASS/FAIL
- Windows: [correct dates]
```

## After Backtest — MANDATORY (do not skip any)
1. **Update Golden Sheet** — add results to GOLDEN_SHEET.md, commit + push. EVERY result, pass or fail.
2. **Commit code** — to both nova-brain/strategies/lean/ AND apexnova/lean/
3. **Update Discord channel** — if strategy has one
4. **Post to #yujun-team** — results summary

## Example: Nova's S16b-v8 Review (learn from this)
Nova caught: `liquidate() + set_holdings()` in same on_data = 2x position.
Fix: `set_holdings()` handles full flip, `liquidate()` only for exit-to-flat.
This bug was in ALL previous S16b variants — all results need re-verification.
