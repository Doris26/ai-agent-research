---
name: macro-regime
description: "Detect market regime using Fed Net Liquidity and MOVE index. Determines risk-on vs risk-off for BTC strategy sizing."
---

# Macro Regime Detection

## When to Use
Before proposing any new strategy or when evaluating existing T1 portfolio risk.

## Indicators

### 1. Fed Net Liquidity
- **Formula:** Fed Total Assets - Treasury General Account (TGA) - ON RRP
- **Search:** `web_search "Federal Reserve balance sheet total assets"` + `web_search "Treasury General Account balance"` + `web_search "ON RRP overnight reverse repo balance"`
- **Signal:**
  - Rising (>5% in 4 weeks): 🟢 RISK-ON — full conviction on SMA75 signals
  - Flat (±5%): 🟡 NEUTRAL — standard position sizing
  - Falling (>5% decline in 4 weeks): 🔴 RISK-OFF — reduce position size, tighten stops

### 2. MOVE Index (Bond Volatility)
- **Search:** `web_search "MOVE index current value"`
- **Signal:**
  - MOVE < 100: 🟢 Calm — full conviction
  - MOVE 100-130: 🟡 Elevated — standard sizing
  - MOVE > 130: 🔴 Stress — defensive posture (halve position sizes)

### 3. MVRV Ratio (BTC On-Chain)
- **Search:** `web_search "Bitcoin MVRV ratio current"`
- **Signal:**
  - MVRV < 1.0: 🟢 Undervalued — aggressive accumulation bias
  - MVRV 1.0-3.0: 🟡 Fair value — standard signals
  - MVRV > 3.5: 🔴 Overheated — defensive, tighten stops, reduce size

## Composite Score
Count green/red signals:
- 3 green: AGGRESSIVE — full position sizes, wider stops
- 2 green 1 yellow: STANDARD — normal operation
- Any red: DEFENSIVE — halve position sizes, tighten ATR stops to 2.0x (from 2.5x)
- 2+ red: MAXIMUM DEFENSE — quarter position sizes, consider cash

## Output Template
```
📊 **Macro Regime Check — [date]**
- Net Liquidity: $[X]T ([trend] [%] over 4wk) [emoji]
- MOVE Index: [value] [emoji]
- MVRV Ratio: [value] [emoji]
**Regime: [AGGRESSIVE/STANDARD/DEFENSIVE/MAX DEFENSE]**
**Action: [position sizing recommendation]**
```

## When to Run
- Before proposing any new strategy
- Weekly check on existing portfolio
- When any T1 strategy shows unusual drawdown
