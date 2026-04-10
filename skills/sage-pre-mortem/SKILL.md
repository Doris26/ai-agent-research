---
name: pre-mortem
description: "Anti-overfitting check. Before finalizing a strategy, articulate failure scenarios and invalidation criteria."
---

# Pre-Mortem Analysis

## When to Use
Before proposing ANY new strategy to Forge. Run this AFTER designing the strategy but BEFORE posting it.

## Steps

### 1. Failure Scenarios (list 3)
"If this strategy loses money over the next 6 months, what went wrong?"
- Scenario A: [market condition that kills it]
- Scenario B: [parameter sensitivity that breaks it]
- Scenario C: [regime change that invalidates the thesis]

### 2. Variant View
"My technical signal says X. But macro says Y. The tension is:"
- State what the SMA75/ADX/indicator says
- State what macro conditions (liquidity, volatility) suggest
- Identify the contradiction or confirmation

### 3. Invalidation Criteria
"I would abandon this strategy if:"
- [specific metric drops below X]
- [market condition changes to Y]
- [parameter sensitivity test shows Z]

### 4. Overfitting Check
- How many free parameters? (must be ≤ 4)
- What happens if I change each parameter by ±20%?
- Would this strategy have worked in 2020? 2021? 2023? (not just 1Y + 2022)

## Output Template
```
🔍 **Pre-Mortem: Strategy [N]**
**Failure scenarios:**
1. [scenario A]
2. [scenario B]
3. [scenario C]
**Variant view:** [signal says X, macro says Y, tension is Z]
**Kill criteria:** [when to abandon]
**Overfitting risk:** [LOW/MEDIUM/HIGH] — [N] free params, [sensitivity notes]
```
