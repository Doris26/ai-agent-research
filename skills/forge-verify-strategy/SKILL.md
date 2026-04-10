---
name: verify-strategy
description: "Deep verification of a T1 strategy — check code, re-run QC backtest, compare results, flag overfitting."
---

# Strategy Verification — Run on EVERY T1 candidate

## Red Flags (fix or flag)
- **Double-order bug** → FIX (liquidate + set_holdings same bar)
- **Look-ahead bias** → FIX (using current bar data for same-bar entry)
- **Low trade count** → FLAG (note in results, not auto-reject)
- **High win rate** → FLAG (note in results, check if realistic)
- **Free parameters > 4** → SIMPLIFY (max 4 strategy-specific tuned params)

## Free Parameter Rule (MAX 4)
Count only parameters that **differ from defaults/template**.

**Template (don't count):** SMA=75, VT=13, VT_window=21, short_cap=0.5, RSI 50/50 thresholds
**Textbook defaults (don't count):** RSI_period=14, ADX_period=14, ATR_period=14, ATR_mult=2.5, SAR_step=0.02, ROC_period=14

**DO count (strategy-specific tuned):**
- Non-default indicator periods (EMA=9/21, Aroon=25, HA_smooth=8, CI_period=20)
- Non-default thresholds (ADX>=25 vs default, RSI>40 vs template 50, CI<61.8)
- Non-default SAR params (SAR_start=0.022, SAR_max=0.14 — but SAR_step=0.02 is default)

If > 4, simplify by using defaults or removing filters.

## Verification Steps

### Step 1: Read the actual code
```bash
cat /Users/yujunzou/python/python_repo/nova-brain/strategies/lean/STRATEGY/main.py
```
Check:
- Does it implement what the name says? (SAR, EMA, ADX etc.)
- Is SMA75 asymmetric present? (longs above SMA75 only, shorts always)
- Is VT13 present? (vol targeting tv=13)
- Is there an ATR trailing stop or other exit?
- Any hardcoded dates that aren't backtest windows?

### Step 2: Code review (5 checks)
- Double-order: NO liquidate + set_holdings in same bar path
- Look-ahead: signals use data BEFORE current bar close
- Indicator readiness: NO fallback to neutral (RSI=50, ADX=0) — must gate with is_ready
- Position sizing: long <= 1.0, short <= 0.5
- Exit conflicts: trail-stop exit can't be followed by same-bar re-entry

### Step 3: Re-run QC Cloud backtest
Push code and re-run BOTH windows to verify Golden Sheet numbers match:
```bash
lean cloud push --project STRATEGY
lean cloud backtest STRATEGY --name "verify-1y"
# Change dates to 2022
lean cloud backtest STRATEGY --name "verify-2022"
```
Compare: Calmar, Sharpe, MaxDD, ROI, Trades must match Golden Sheet within ±5%.

### Step 4: Trade count check
- Trades >= 15: GOOD (statistically meaningful)
- Trades 5-14: ACCEPTABLE (note low count)
- Trades < 5: FLAG as low (note in verification, do not auto-reject)

### Step 5: Post verification result
```
**VERIFIED: [Strategy Name]**
- Code: CLEAN / BUG FOUND [details]
- QC re-run: MATCH / MISMATCH [numbers]
- Trade count: [N] trades — OK / LOW / REJECT
- Overfitting risk: LOW / MODERATE / HIGH
```
