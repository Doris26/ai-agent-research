# Pattern 13: Resilience (Auto-Recovery from Failures)

**Problem:** Gateway crashes, internet drops, Mac sleeps, Discord goes down.

**Solution:** OpenClaw has built-in recovery for most failures:

| Failure | Recovery | Action Needed |
|---------|----------|--------------|
| Gateway dies | Overdue crons fire on restart | Install as LaunchAgent |
| Internet drops | Discord auto-reconnects with backoff | None — auto resumes |
| Failed Discord post | Delivery retry queue | None — auto retries |
| Agent timeout (480s) | Next cron run retries | Fix root cause |
| Mac sleeps | Gateway resumes on wake, crons catch up | Install Amphetamine |
| EC2 stops | systemd Restart=always | None — auto restarts |
| Git push conflict | Pull --rebase on next commit | Stagger cron schedules |

**When network comes back:** Discord bots auto-reconnect with exponential backoff (1s, 2s, 4s, 8s...). Overdue crons fire immediately. No manual action needed.

**Daily logs help debugging:** When something breaks, read `memory/YYYY-MM-DD.md` to see exactly what the agent was doing when it failed. MEMORY.md is curated (lossy), daily logs are raw (lossless).

**The one manual piece:** Install gateway as LaunchAgent:
```bash
node openclaw.mjs gateway install
```
This handles 80% of resilience. Everything else is built-in.
