---
name: tier1-promotion
description: "When a strategy passes Tier 1: create Discord channel, update Golden Sheet, notify Nova, set up QC Cloud papertest. Follow ALL steps."
---

# Tier 1 Promotion — FOLLOW ALL STEPS

## When to Use
Strategy passes BOTH:
- 1Y Recent: Calmar > 3 OR (Calmar > 2 + Sharpe > 1)
- 2022 Crash: MaxDD < 30% + loss < 15%

## Step 1: Create Discord Channel
**🚨 MUST use parent_id "1483141174532374558" (Yujun Strategy category). If you skip this, channel is invisible.**

Use this EXACT code — do NOT create channels any other way:
```bash
curl -s -X POST "https://discord.com/api/v10/guilds/1475717065049378936/channels" \
  -H "Authorization: Bot DISCORD_BOT_TOKEN_REDACTED" \
  -H "Content-Type: application/json" \
  -d '{"name": "STRATEGYNAME", "type": 0, "parent_id": "1483141174532374558"}'
```
Replace STRATEGYNAME with lowercase strategy name (e.g. s36-adx-sar).

**After creating, VERIFY it's in the right category:**
```bash
curl -s "https://discord.com/api/v10/channels/CHANNEL_ID" \
  -H "Authorization: Bot DISCORD_BOT_TOKEN_REDACTED" | python3 -c "
import json,sys
c = json.loads(sys.stdin.read())
assert c.get('parent_id') == '1483141174532374558', f'WRONG CATEGORY: {c.get(\"parent_id\")}. Fix with PATCH.'
print(f'OK: #{c[\"name\"]} in Yujun Strategy category')
"
```

## Step 2: Post Strategy Details to Channel
Post to the new channel:
```
🎯 **[Strategy Name] — TIER 1**

**1Y Recent:** Calmar X.XX | Sharpe X.XX | ROI +XX% | MaxDD X% | Trades X
**2022 Crash:** Loss X% | MaxDD X% | Trades X

**Signal:** [exact entry/exit rules]
**Parameters:** [final params]

**QC Backtest URLs:**
- 1Y: [url]
- 2022: [url]
```

## Step 3: Commit Strategy Code to BOTH Repos
```bash
# Copy to nova-brain
cp -r /Users/yujunzou/python/python_repo/lean-workspace-v2/StrategyName/ /Users/yujunzou/python/python_repo/nova-brain/strategies/lean/StrategyName/
cd /Users/yujunzou/python/python_repo/nova-brain && git add strategies/lean/ && git commit -m "feat: add StrategyName T1" && git push origin main

# ALSO copy to apexnova (next to Kai's strategies) — DO NOT SKIP
cp -r /Users/yujunzou/python/python_repo/lean-workspace-v2/StrategyName/ /Users/yujunzou/python/python_repo/apexnova/lean/StrategyName/
cd /Users/yujunzou/python/python_repo/apexnova && git add lean/ && git commit -m "feat(forge): add StrategyName T1" && git push origin main 2>&1 || echo "Push failed (branch protection) — committed locally"
```

## Step 4: Update Golden Sheet
Update `/Users/yujunzou/python/python_repo/nova-brain/GOLDEN_SHEET.md` with both windows + Sharpe. Commit.

## Step 4: Notify Nova
Post to #all-hands (1480262938672500848):
`<@1475686344805318787> TIER 1 PROMOTION: [strategy] 1Y Calmar X.XX, Sharpe X.XX. 2022 survived (MaxDD X%, loss X%). Channel created.`

## Step 5: QC Cloud Papertest
```bash
source /Users/yujunzou/python/python_repo/apexnova/.venv/bin/activate
cd /Users/yujunzou/python/python_repo/lean-workspace-v2
lean cloud live deploy StrategyName --brokerage "paper trading" --data-provider-live "quantconnect" --node "NODE_NAME" --auto-restart true --notify-order-events false --notify-insights false
```
Note: Requires QC live node ($20/mo). If no node available, skip this step and note it.

## Step 6: Verify & Confirm
Post to #yujun-team:
```
✅ TIER 1 PROMOTION COMPLETE:
- Discord channel: #strategyname ✅
- Golden Sheet: updated ✅
- Nova notified: ✅
- QC Papertest: [deployed/pending node]
```

## Checklist (ALL must be done)
- [ ] Discord channel created
- [ ] Strategy details posted to channel
- [ ] Golden Sheet updated with both windows + Sharpe
- [ ] Nova notified in #all-hands
- [ ] QC Cloud papertest (if node available)
- [ ] Confirmation posted
