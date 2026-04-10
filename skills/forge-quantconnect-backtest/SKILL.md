---
name: quantconnect-backtest
description: "Backtest strategies using QuantConnect Cloud. Cross-validate Freqtrade results. Write LEAN strategy → push to QC Cloud → run backtest → compare."
---

# QuantConnect Cloud Backtest

## Paths
- **Lean workspace:** `/Users/yujunzou/python/python_repo/lean-workspace-v2/`
- **Python venv:** `source /Users/yujunzou/python/python_repo/apexnova/.venv/bin/activate`
- **Lean CLI:** `lean` (in apexnova venv)
- **QC credentials:** ~/.lean/credentials (User ID: 476740)

## Step 1: Write LEAN Strategy

```bash
source /Users/yujunzou/python/python_repo/apexnova/.venv/bin/activate
cd /Users/yujunzou/python/python_repo/lean-workspace-v2

# Create project (skip if exists)
lean create-project --language python StrategyName
```

**QC Account:** User 475829 (lean login already done)
**Workspace:** `/Users/yujunzou/python/python_repo/lean-workspace-v2/`

Save to `StrategyName/main.py`:

```python
from AlgorithmImports import *

class StrategyName(QCAlgorithm):
    def initialize(self):
        # CHANGE DATES FOR EACH TEST WINDOW
        self.set_start_date(2025, 3, 17)  # Window 1: 1Y recent
        self.set_end_date(2026, 3, 17)
        self.set_cash(10000)

        self.btc = self.add_crypto("BTCUSDT", Resolution.DAILY).symbol
        # ADD INDICATORS HERE

    def on_data(self, data):
        if not data.contains_key(self.btc):
            return
        # ADD ENTRY/EXIT LOGIC HERE
```

## Step 1.5: CODE REVIEW (MANDATORY — DO NOT SKIP)

**Before pushing to QC Cloud, run the `strategy-review` skill checklist.**
Read: `/Users/yujunzou/python/python_repo/nova-brain/agents/forge/skills/strategy-review/SKILL.md`

Post the review to Discord with PASS/FAIL for each item:
- Double-order bugs (no liquidate + set_holdings in same bar)
- Look-ahead bias
- Indicator readiness (no neutral fallbacks)
- Position sizing caps
- Exit logic conflicts

**If ANY item FAILS → fix the code FIRST. Do NOT proceed to backtest.**

## Step 2: Push to QC Cloud

```bash
source /Users/yujunzou/python/python_repo/apexnova/.venv/bin/activate
cd /Users/yujunzou/python/python_repo/lean-workspace
lean cloud push --project StrategyName
```

## Step 3: Run Cloud Backtest

```bash
lean cloud backtest StrategyName --name "backtest-name"
```

Output includes: Net Profit %, Drawdown %, Sharpe, Trades, Win Rate.

**Calculate Calmar:** Annual Return % / Max Drawdown %

## Step 4: UPDATE GOLDEN SHEET (IMMEDIATELY — DO NOT SKIP)

```bash
# Read current Golden Sheet
cat /Users/yujunzou/python/python_repo/nova-brain/GOLDEN_SHEET.md

# Add results to the Both-Window Results table or appropriate section
# Include: Strategy name, 1Y Calmar, 1Y Sharpe, 1Y MaxDD, 1Y ROI, 1Y Trades, 2022 Loss, 2022 MaxDD, Pass/Fail

# Commit and push IMMEDIATELY
cd /Users/yujunzou/python/python_repo/nova-brain
git add GOLDEN_SHEET.md
git commit -m "results: StrategyName Calmar X.XX (T1/T2/T3)"
git push origin main
```

**This step is NOT optional. EVERY backtest result goes in Golden Sheet. Pass OR fail. Do this BEFORE posting to Discord.**

## Step 5: Commit Code to BOTH repos

```bash
# Copy strategy to nova-brain
cp -r /Users/yujunzou/python/python_repo/lean-workspace-v2/StrategyName/ /Users/yujunzou/python/python_repo/nova-brain/strategies/lean/StrategyName/

cd /Users/yujunzou/python/python_repo/nova-brain
git add strategies/lean/
git commit -m "feat: add StrategyName QC backtest (Calmar X.XX)"
git push origin main

# ALSO copy to apexnova (next to Kai's strategies)
cp -r /Users/yujunzou/python/python_repo/lean-workspace-v2/StrategyName/ /Users/yujunzou/python/python_repo/apexnova/lean/StrategyName/

cd /Users/yujunzou/python/python_repo/apexnova
git add lean/
git commit -m "feat(forge): add StrategyName QC backtest (Calmar X.XX)"
git push origin main 2>&1 || echo "Push failed (branch protection) — committed locally"
```

**Both repos must have the strategy code. apexnova/lean/ is where Kai's strategies live.**

## Example: Full Run

```bash
source /Users/yujunzou/python/python_repo/apexnova/.venv/bin/activate
cd /Users/yujunzou/python/python_repo/lean-workspace

# Create
lean create-project --language python MyStrategy

# Write main.py (edit the file)

# Push + backtest
lean cloud push --project MyStrategy
lean cloud backtest MyStrategy --name "test-1y"

# Read results from output
# Calculate: Calmar = Annual Return / Max Drawdown
```


## ⚠️ REQUIRED: Test BOTH Windows
Every strategy must show results for BOTH:
1. **1Y Recent** (2025-03-17 to 2026-03-17) — current market
2. **2022 Crash** (2022-01-01 to 2022-12-31) — stress test

**Tier 1 requires BOTH:**
- 1Y Recent: Calmar > 3 OR (Calmar > 2 + Sharpe > 1)
- 2022 Crash: MaxDD < 30% AND loss < 15%

**After EVERY backtest: update Golden Sheet immediately with ALL results.**
**If strategy has a Discord channel: update the channel with new results.**

Change `set_start_date` and `set_end_date` for each window, push, backtest, report both.

## Iteration Rules
- Calmar < 1: REJECT, no iterations
- Calmar 1-2: max 2 iterations then reject
- Calmar > 2 but Sharpe < 1: max 3 iterations to push Sharpe > 1
- Calmar > 3 + 2022 survive: TIER 1 (no Sharpe needed)
- Calmar > 2 + Sharpe > 1 + 2022 survive: TIER 1
- After 3 fails: try completely different approach
