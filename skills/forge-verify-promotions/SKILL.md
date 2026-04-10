---
name: verify-promotions
description: "Check Golden Sheet for any T1 strategy missing a Discord channel. Run after every backtest session."
---

# Verify Promotions — Run at END of every session

## What to check
1. Read Golden Sheet for all T1 strategies
2. List all Discord channels under Yujun Strategy category
3. Any T1 without a channel → create it immediately

## How to run
```bash
# 1. Get all T1 from Golden Sheet
grep -i "YES.*T1\|— T1" /Users/yujunzou/python/python_repo/nova-brain/GOLDEN_SHEET.md | grep -v "~~\|NOT T1\|fake\|DEMOTED"

# 2. Get all channels
curl -s "https://discord.com/api/v10/guilds/1475717065049378936/channels" \
  -H "Authorization: Bot DISCORD_BOT_TOKEN_REDACTED" | python3 -c "
import json, sys
for c in json.loads(sys.stdin.read()):
    if c.get('parent_id') == '1483141174532374558' and c['type'] == 0:
        print(c['name'])
"

# 3. Compare — any T1 missing a channel? Create it:
curl -s -X POST "https://discord.com/api/v10/guilds/1475717065049378936/channels" \
  -H "Authorization: Bot DISCORD_BOT_TOKEN_REDACTED" \
  -H "Content-Type: application/json" \
  -d '{"name": "STRATEGYNAME", "type": 0, "parent_id": "1483141174532374558"}'
```

## Also check
- All strategies (pass AND fail) have Golden Sheet entries
- All T1 channels have strategy details posted
- Code committed to both nova-brain + apexnova

## When to run
- End of every backtest session
- After promoting any T1
- When Yujun asks to verify
