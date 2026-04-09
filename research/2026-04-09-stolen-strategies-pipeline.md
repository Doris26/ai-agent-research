# Stolen Strategies Pipeline — Fund Manager Operations → QQQR Variants
_Date: 2026-04-09 | Sources: 40+ across WebSearch + Gemini Deep Research_

## Executive Summary

After researching 8 top funds, 5 smart-beta ETFs, and 15+ academic factors, here are the **top 10 stolen strategies** to A/B test as QQQR variants. Each takes a proven fund/ETF operation and adapts it for QQQ constituent selection.

Current QQQR baseline: RPS acceleration + EPS tilt + Guidance + FCF Quality (Sharpe 0.802)

---

## TOP 10 STRATEGIES TO STEAL & TEST

### 1. QGRW Clone — Quality×Growth Composite Score
**Stolen from:** WisdomTree QGRW (beat QQQ by +430bps/yr since 2022)
**Signal:** Composite of ROE (3yr avg) + ROA (3yr avg) + analyst earnings growth forecast + 5yr EBITDA growth + 5yr sales growth. Exclude bottom 30% on quality OR growth.
**Why it works:** QGRW proved that combining quality + growth scoring on QQQ-like universe beats plain QQQ. Our QQQR already has growth (RPS), but lacks the ROE/ROA quality dimension.
**QQQR variant:** Replace EPS tilt with QGRW-style composite (ROE + ROA + earnings growth). Weight by composite score instead of ETF weight × EPS mult.
**Priority: HIGH** — proven live track record beating QQQ.

### 2. Earnings Revision Momentum
**Stolen from:** AQR Fundamental Momentum + Mill Street Research
**Signal:** Track analyst EPS estimate changes. Score = (# upgrades - # downgrades) / total analysts. Buy stocks with positive revision breadth AND magnitude. Sell when revisions turn negative.
**Alpha:** Up to 22% annual gross alpha in academic backtests. Revisions breadth + magnitude together outperform either alone.
**QQQR variant:** Add analyst revision score as a multiplier. Stocks with all-upgrades get 1.3x weight, all-downgrades get 0.5x, mixed stay 1.0x. Use QC fundamental data for analyst estimates.
**Priority: HIGH** — strong academic evidence, directly available in QC data.

### 3. PEAD Decay-Weighted Tilt
**Stolen from:** Ball & Brown (1968) + Quantpedia
**Signal:** After earnings release, buy stocks with positive surprise (actual > estimate), hold 60 days. Weight by surprise magnitude. SUE (Standardized Unexpected Earnings) top decile → 5.1% quarterly alpha.
**QQQR variant:** Already partially captured by RPS acceleration, but add explicit PEAD: boost weight by 1.2x in the 60 days after a positive earnings surprise. Reduce weight after negative surprise.
**Priority: MEDIUM** — partially overlaps with existing guidance signal.

### 4. Accruals Quality Filter (Earnings Quality)
**Stolen from:** Sloan (1996) + AQR QMJ
**Signal:** Accruals = (Net Income - Operating Cash Flow) / Total Assets. High accruals = low quality earnings (accounting tricks). Low accruals = cash-backed earnings. Long low-accruals, short high-accruals.
**QQQR variant:** Exclude stocks where accruals ratio > 0.10 (earnings not backed by cash). This is different from FCF quality — accruals specifically catches accounting manipulation.
**Priority: HIGH** — proven anomaly, complements existing FCF filter.

### 5. AQR Quality-Minus-Junk (QMJ) Filter
**Stolen from:** AQR Capital (Sharpe 0.47, 4.7% annual premium since 1964)
**Signal:** Quality = average of (Profitability + Growth + Safety + Payout). Score each QQQ constituent. Long top quality, avoid bottom junk.
**Components:** GP/Assets, ROE, ROA, earnings variability, leverage, beta, payout ratio, equity issuance.
**QQQR variant:** Compute simplified QMJ score (GP/Assets + ROE + low debt/equity). Multiply weight by quality z-score. Junk stocks (bottom 20%) get 0.5x weight.
**Priority: HIGH** — 60 years of data, AQR provides free monthly factor returns for validation.

### 6. Insider Buying Confirmation
**Stolen from:** Lakonishok & Lee (2002) + Cohen/Malloy/Pomorski (2012)
**Signal:** Cluster buying by multiple insiders = strong bullish signal. Opportunistic purchases (not routine) predict 5.2% alpha over 6 months. Focus on open-market buys, not option exercises.
**QQQR variant:** At rebalance, check SEC Form 4 filings. If 2+ insiders bought in last 90 days, boost weight by 1.2x. If heavy insider selling, reduce weight by 0.8x. Use SEC EDGAR API (already have pipeline).
**Priority: MEDIUM** — moderate alpha, but we already have EDGAR pipeline.

### 7. Shareholder Yield (Buyback + Dividend)
**Stolen from:** Cambria SYLD (Meb Faber methodology)
**Signal:** Shareholder yield = dividend yield + net buyback yield + debt paydown yield. Companies returning most cash to shareholders tend to outperform. Top 100 by shareholder yield.
**QQQR variant:** Compute shareholder yield for each QQQ constituent. Overweight stocks with yield > median. This captures the "capital allocation quality" dimension.
**Priority: MEDIUM** — QQQ tech stocks generally have low dividends but high buybacks (AAPL, GOOGL, META).

### 8. Volatility-Adjusted Momentum
**Stolen from:** Man AHL + Renaissance (vol-weighted signals)
**Signal:** Instead of raw price momentum, use risk-adjusted momentum: 12-month return / 12-month volatility. This gives more weight to stocks that went up smoothly vs. stocks that went up violently.
**QQQR variant:** Replace current growth-only signal with vol-adjusted growth: revenue_growth / revenue_growth_volatility. Smooth growers get higher weight than erratic growers.
**Priority: MEDIUM** — reduces whipsaw from volatile growth stocks.

### 9. Multi-Factor Ensemble (Renaissance-Style)
**Stolen from:** Renaissance Technologies approach (combine many weak signals)
**Signal:** Instead of relying on one strong signal, combine 5-7 weak but uncorrelated signals. Each signal votes, majority wins. Signals: RPS acceleration, EPS tilt, FCF quality, accruals quality, insider buying, analyst revisions, shareholder yield.
**QQQR variant:** Score each stock on all available factors (0-1 each). Total score = sum. Only hold stocks scoring > 4/7. Weight proportional to score.
**Priority: HIGH** — this is how the best quant funds actually work.

### 10. ESG Exclusion Alpha (QQMG Clone)
**Stolen from:** Invesco QQMG (beat QQQ by +5.6% since inception)
**Signal:** Simply exclude 10 QQQ stocks involved in: cannabis, alcohol, weapons, gambling, nuclear, tobacco, oil & gas. The remaining 90 stocks outperform the full 100.
**QQQR variant:** Exclude the ~10 QQQ constituents with worst ESG scores (simple negative screen). No complex scoring needed.
**Priority: LOW** — easy to implement but alpha may be period-specific.

---

## IMPLEMENTATION PRIORITY

| Round | Variant | Stolen From | Expected Alpha |
|-------|---------|-------------|----------------|
| 1 | QGRW Quality×Growth Score | WisdomTree QGRW | +430bps/yr proven |
| 1 | Analyst Revision Momentum | AQR + Mill Street | +22% gross alpha |
| 1 | Accruals Quality Filter | Sloan (1996) | +4-6% annual |
| 2 | AQR QMJ Score | AQR Capital | +4.7% annual |
| 2 | Multi-Factor Ensemble | Renaissance approach | +5-10% annual |
| 2 | PEAD Decay Tilt | Ball & Brown | +5.1% quarterly |
| 3 | Insider Buying Confirmation | Form 4 research | +5.2% 6-month |
| 3 | Shareholder Yield | Cambria SYLD | +3-5% annual |
| 3 | Vol-Adjusted Growth | Man AHL | +2-3% Sharpe |
| 3 | ESG Exclusion | QQMG | +2-3% annual |

## Data Sources Needed

| Data | Source | Available? |
|------|--------|-----------|
| ROE, ROA, GP/Assets | QC Fundamentals | YES |
| Analyst estimates/revisions | QC EstimateMultiPeriod | YES |
| Accruals (NI - OCF) | QC Fundamentals | YES |
| Insider transactions | SEC EDGAR Form 4 | YES (have pipeline) |
| Buyback/dividend yield | QC Fundamentals | YES |
| Revenue volatility | QC (compute from history) | YES |
| ESG scores | External (MSCI) | NO - use exclusion list |

**All Round 1 strategies are implementable with existing QC data. No new data sources needed.**
