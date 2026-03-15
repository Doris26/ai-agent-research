# Pattern 13: Resume & Resilience (Auto-Recovery from Failures)

**Problem:** Gateway crashes, internet drops, Mac sleeps. When things come back, agents need to pick up exactly where they left off — not start over.

## The Resume Pattern (3 Layers)

### Layer 1: Overdue Cron Catch-up (automatic)
Gateway restarts → checks all crons → any past due fire immediately.
- Gateway down 8 hours, missed 2 crons → both run on restart
- No manual intervention needed

### Layer 2: Agent Memory (MEMORY.md + daily logs)
Agent reads MEMORY.md at session start → knows exactly where it left off.
```
MEMORY.md says: "Round 8 proposed, waiting for Forge results"
→ Agent picks up from there
→ Doesn't re-propose Round 8
→ Checks Discord for Forge's results instead
```
**This only works if agents commit MEMORY.md to git after every session.** Uncommitted memory = lost on crash.

### Layer 3: Discord as State (message history)
Agent reads Discord channel → sees what happened while it was down.
```
Agent was offline for 6 hours
→ Reads #yujun-team: "Forge posted Round 8 results: Calmar 1.21"
→ Evaluates results, opens Round 9
→ No human had to tell it what happened
```

## Why This Works

| Component | Survives Crash? | How |
|-----------|----------------|-----|
| MEMORY.md | ✅ Yes | Git-backed, committed after every session |
| Daily logs | ✅ Yes | Git-backed, in memory/YYYY-MM-DD.md |
| Discord messages | ✅ Yes | Stored on Discord servers |
| Cron schedule | ✅ Yes | Stored in ~/.openclaw/cron/jobs.json |
| In-memory state | ❌ No | That's why we don't use it |

**Key insight:** Everything is on disk (git) or Discord (cloud). Zero in-memory state. Agent can crash mid-session, restart, and resume from MEMORY.md + Discord.

## Failure Recovery Table

| Failure | Recovery | Action Needed |
|---------|----------|--------------|
| Gateway dies | Overdue crons fire on restart | Install as LaunchAgent |
| Internet drops | Discord auto-reconnects with backoff | None — auto resumes |
| Failed Discord post | Delivery retry queue | None — auto retries |
| Agent timeout (480s) | Next cron run retries | Fix root cause |
| Mac sleeps | Gateway resumes on wake, crons catch up | Install Amphetamine |
| EC2 stops | systemd Restart=always | None — auto restarts |
| Git push conflict | Pull --rebase on next commit | Stagger cron schedules |

## What Breaks Without Resume

| Missing Piece | What Happens |
|--------------|-------------|
| No MEMORY.md commits | Agent starts fresh every session, re-proposes failed strategies |
| No Discord channel reads | Agent doesn't know Forge posted results, re-spawns Forge |
| No git push | MEMORY.md lost on crash, weeks of learning gone |
| No cron catch-up | Missed sessions never run, research stalls |

## The One Must-Do

Install gateway as LaunchAgent so it auto-starts on reboot:
```bash
node openclaw.mjs gateway install
```
This handles 80% of resilience. Everything else is built-in.

## FAQ: Does the agent read the entire Discord channel?

**No.** The agent reads the **last 20-30 messages** only (one Discord API call, free). This is enough to see:
- Did Forge post backtest results?
- Did Analyst ask a follow-up question?
- Did Nova give a directive?

Old messages beyond 30 are not loaded — that's what MEMORY.md is for (curated persistent knowledge). Discord is for **recent events**, MEMORY.md is for **long-term state**.

```python
# Agent reads last 20 messages — costs 0 tokens (Discord API, not Claude)
messages = read_channel("1480051404683870480", bot_token, limit=20)
```
