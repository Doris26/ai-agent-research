# Daily Operations Checklist

What to check every morning to make sure your agents are healthy.

---

## 30-Second Health Check

```bash
cd /path/to/openclaw

# 1. Is the gateway alive?
node openclaw.mjs gateway status 2>&1 | grep "RPC probe"
# Should say: "RPC probe: ok"

# 2. Are crons running or erroring?
node openclaw.mjs cron list
# Check Status column: "ok" = good, "error" = investigate, "running" = in progress

# 3. Any crons overdue?
# Check "Next" column — if it says "12h ago" the cron missed its window (gateway was down)
```

## If Gateway Is Down

```bash
# Restart it
node openclaw.mjs gateway --force &

# Missed crons will auto-fire on restart if overdue
```

## If a Cron Shows "error"

```bash
# Check gateway logs for the error
node openclaw.mjs logs | grep -i "error\|fail" | tail -20

# Common fixes:
# - "Discord recipient is required" → cron missing --to flag, recreate it
# - "CLI produced no output for 480s" → agent workspace missing .claude/settings.json
# - "Missing Permissions" → bot not invited to server or missing channel access
# - "Missing Access" → bot token expired or revoked
```

## Check Discord Channels

Open Discord and scan:
- Did Scout post to `#scout-feed` today?
- Did Scholar post to `#scholar-feed` today?
- Did Analyst post to `#daily-briefing` today?
- Any error messages from bots?

## Check Git Commits

```bash
# Did agents commit their updates?
cd /path/to/repo
git log --oneline -5
# Should see recent commits from agents with today's date
```

## Keeping OpenClaw Updated

OpenClaw is actively developed — new features, bug fixes, and security patches ship regularly. Set up a weekly cron to pull and rebuild:

```bash
node openclaw.mjs cron add \
  --name "openclaw-weekly-update" \
  --cron "0 6 * * 0" \
  --session isolated \
  --agent <any-agent> \
  --to "channel:CHANNEL_ID" \
  --message 'Update OpenClaw:
```bash
cd /path/to/openclaw
git pull origin main
pnpm install
pnpm run build
```
Post result: success or error message.'
```

**Schedule:** Every Sunday at 6 AM UTC. Agent pulls latest, rebuilds, reports.

**After update:** Restart the gateway manually to pick up changes:
```bash
node openclaw.mjs gateway stop
node openclaw.mjs gateway --force
```

> **Why not auto-restart?** A bad build could break the gateway. Better to let the agent report success, then you restart manually when convenient.

---

## Weekly Review

Every week:
- [ ] Review RESEARCH_LEDGER.md — mark items ✅ Actioned or 📦 Archived
- [ ] Check agent MEMORY.md files — are they growing too large? (>500 lines = trim old entries)
- [ ] Review Claude API usage — are costs within budget?
- [ ] Update SOUL.md if agent output needs adjustment
- [ ] Pull latest from git on all repos

## Emergency: Agent Posting Nonsense

```bash
# 1. Disable the cron immediately
node openclaw.mjs cron delete CRON_ID

# 2. Check what happened
node openclaw.mjs sessions --agent AGENT_ID

# 3. Read the agent's SOUL.md — did it drift? (check git blame)
git log --oneline agents/AGENT/SOUL.md

# 4. Fix SOUL.md, recreate cron, test with one-shot first
```

## Quick Reference

| Check | Command | Healthy |
|-------|---------|---------|
| Gateway | `gateway status` | "RPC probe: ok" |
| Crons | `cron list` | All show "ok" or "idle" |
| Discord | Open app | Posts from today visible |
| Git | `git log -5` | Recent agent commits |
| EC2 (trading) | `ssh openclaw-ec2-direct 'systemctl is-active freqtrade-paper-daily-ma120.service'` | "active" |
