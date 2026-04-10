---
name: deploy-papertest
description: "Deploy a Tier 1 strategy to EC2 as a Freqtrade papertest. Creates strategy file, config, systemd service. Use after every Tier 1 promotion."
---

# Deploy Strategy to EC2 Papertest

## When to Use
After EVERY Tier 1 promotion (6M or 1Y Calmar > 3).

## Step 1: Create Freqtrade Strategy File on EC2

```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'cat > /home/ec2-user/trading/freqtrade/user_data/strategies/StrategyName.py << "STRATEGY"
from freqtrade.strategy import IStrategy
import pandas as pd
import talib

class StrategyName(IStrategy):
    timeframe = "1d"
    stoploss = -0.99
    can_short = False  # BinanceUS spot only, no futures

    def populate_indicators(self, dataframe, metadata):
        # ADD YOUR INDICATORS HERE
        return dataframe

    def populate_entry_trend(self, dataframe, metadata):
        # ADD ENTRY CONDITIONS HERE
        return dataframe

    def populate_exit_trend(self, dataframe, metadata):
        # ADD EXIT CONDITIONS HERE
        return dataframe
STRATEGY'
```

**IMPORTANT:** `can_short = False` — BinanceUS is spot only, no short selling.

## Step 2: Create Papertest Config on EC2

```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'cat > /home/ec2-user/trading/freqtrade/user_data/papertest_configs/papertest_binanceus_daily_STRATEGYNAME_opt.json << "CONFIG"
{
    "trading_mode": "spot",
    "max_open_trades": 1,
    "stake_currency": "USDT",
    "stake_amount": "unlimited",
    "tradable_balance_ratio": 1.0,
    "dry_run": true,
    "dry_run_wallet": 10000,
    "exchange": {
        "name": "binanceus",
        "key": "",
        "secret": "",
        "pair_whitelist": ["BTC/USDT"]
    },
    "pairlists": [{"method": "StaticPairList"}],
    "bot_name": "paper_binanceus_STRATEGYNAME_opt"
}
CONFIG'
```

## Step 3: Create Systemd Service on EC2

**THIS IS THE CRITICAL STEP — do NOT skip it.**

```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo bash -c "cat > /etc/systemd/system/freqtrade-paper-daily-STRATEGYNAME.service << SERVICE
[Unit]
Description=Freqtrade Papertrade - StrategyName
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/trading/freqtrade
ExecStart=/bin/bash -lc \\\". /home/ec2-user/trading/freqtrade/.venv_working/bin/activate && exec python -m freqtrade trade -c /home/ec2-user/trading/freqtrade/user_data/papertest_configs/papertest_binanceus_daily_STRATEGYNAME_opt.json --strategy StrategyName --strategy-path /home/ec2-user/trading/freqtrade/user_data/strategies --dry-run\\\"
Restart=always
RestartSec=10
KillSignal=SIGINT
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
SERVICE"

sudo systemctl daemon-reload
sudo systemctl enable freqtrade-paper-daily-STRATEGYNAME.service
sudo systemctl start freqtrade-paper-daily-STRATEGYNAME.service'
```

## Step 4: Verify It's Running

```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo systemctl status freqtrade-paper-daily-STRATEGYNAME.service --no-pager | head -10'
```

Must show `Active: active (running)`. If it shows `activating (auto-restart)` or `failed`, check:
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo journalctl -u freqtrade-paper-daily-STRATEGYNAME.service -n 20 --no-pager'
```

## Step 5: Post Confirmation

Post to the strategy's Discord channel:
```
✅ Papertest deployed to EC2
- Service: freqtrade-paper-daily-STRATEGYNAME
- Status: RUNNING
- Config: papertest_binanceus_daily_STRATEGYNAME_opt.json
- Wallet: $10,000 USDT (dry run)
```

## Checklist (ALL must be done)
- [ ] Strategy .py file created on EC2
- [ ] Config .json file created on EC2
- [ ] Systemd service file created
- [ ] `systemctl daemon-reload` run
- [ ] `systemctl enable` run
- [ ] `systemctl start` run
- [ ] Verified `active (running)` status
- [ ] Posted confirmation to Discord channel

## Current EC2 Limits
- t3.small (2 vCPU, 2GB RAM)
- Max 5 freqtrade processes before CPU overloads
- Currently running: 4 strategies
