---
name: monitor-papertests
description: "Check EC2 papertest health, trade activity, and PnL. Use during daily checks."
---

# Monitor EC2 Papertests

## Check All Services
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo systemctl list-units "freqtrade*" --no-pager | grep loaded'
```

## Check Trade Activity for Each Strategy
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'cd /home/ec2-user/trading/freqtrade && for db in tradesv3.paper_*.sqlite; do
  .venv_working/bin/python -c "
import sqlite3
conn = sqlite3.connect(\"$db\")
c = conn.cursor()
c.execute(\"SELECT count(*) FROM trades\")
total = c.fetchone()[0]
c.execute(\"SELECT count(*) FROM trades WHERE is_open=1\")
open_t = c.fetchone()[0]
c.execute(\"SELECT sum(close_profit) FROM trades WHERE close_date IS NOT NULL\")
pnl = c.fetchone()[0] or 0
print(f\"$db: {total} trades, {open_t} open, PnL={round(pnl*100,2)}%\")
conn.close()
" 2>/dev/null
done'
```

## Check Logs for Errors
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'for svc in $(sudo systemctl list-units "freqtrade*" --no-pager | grep loaded | awk "{print \$1}"); do
  echo "=== $svc ==="
  sudo journalctl -u "$svc" -n 5 --no-pager | grep -i "error\|warn\|heartbeat" | tail -2
done'
```

## Restart a Crashed Service
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo systemctl restart freqtrade-paper-daily-STRATEGYNAME.service'
```

## Post Health Report to Discord
After checking, post to #yujun-team:
```
📊 EC2 Papertest Health — [DATE]
- X services running
- X total trades across all strategies
- Any errors: [list]
- CPU load: [uptime]
```
