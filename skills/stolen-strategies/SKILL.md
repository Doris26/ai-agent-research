---
name: stolen-strategies
description: "Research pipeline that finds fund manager strategies, extracts their signals/factors, implements as QC variants, backtests, and evaluates. Use when asked to find new trading factors, steal strategies from funds/ETFs/papers, or A/B test QQQR variants."
---

# Stolen Strategies Pipeline

## Overview
Systematically discover, extract, implement, and backtest trading strategies from hedge funds, ETFs, academic papers, and GitHub repos.

## Pipeline Steps

### Step 1: Research (use WebSearch + Deep Researcher agent)
Search for strategies from:
- Hedge fund 13F filings (HedgeFollow, WhaleWisdom)
- Smart-beta ETFs that beat QQQ (QGRW, QQMG, SYLD)
- Academic papers (Piotroski, Novy-Marx, Sloan, Fama-French)
- GitHub repos (factor models, backtest frameworks)
- Fund manager interviews and strategy disclosures

### Step 2: Extract Signals
For each strategy found, extract:
- Core signal/factor and how to compute it
- Data source (QC fundamentals, external API, alternative data)
- Reported alpha/returns vs benchmark
- Whether it can be applied to QQQ constituents

### Step 3: Implement as QQQR Variant
- Copy the current champion as base
- Add ONE new factor per variant (isolate the effect)
- Use try/except for all fundamentals access
- Keep file under 50K chars (QC limit is 64K)
- No emoji characters (QC rejects non-ASCII)
- Create config.json alongside main.py

### Step 4: Backtest on QC Cloud
```bash
lean cloud push --project "lean/factors/VARIANT_NAME"
lean cloud backtest "lean/factors/VARIANT_NAME"
```
QC only runs 1 backtest at a time. Queue sequentially.

### Step 5: Evaluate
Compare vs baseline: Sharpe, CAGR, MaxDD, Orders
- Sharpe improvement > 0.01 AND no CAGR drop = WINNER
- MaxDD increase > 3pp without Sharpe gain = REJECT
- Walk-forward validate winners (train 2015-2020, test 2021-2025)

## Key Learnings (from 65+ variants)
- Quality gates (remove bad stocks) work better than new buy signals
- Revenue acceleration on QQQ is already a strong signal
- Factors that work: accruals, FCF, Piotroski, Rule of 40, SBC dilution
- Factors that don't: momentum, PEAD, insider, analyst revisions, sentiment, technical overlays
- QQQ is the optimal universe — broader markets dilute alpha
- Use strategy-review skill BEFORE pushing to QC (prevents runtime errors)

## Data Sources Available on QC
- Fundamentals: income statement, balance sheet, cash flow (quarterly + TTM)
- Valuation: ROE, ROA, P/E, dividend yield
- ETF constituents: QQQ, SPY, IWB, IWM
- News: Tiingo News (free), Brain Sentiment (paid)
