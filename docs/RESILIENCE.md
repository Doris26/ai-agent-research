# Resilience Guide — Surviving Crashes, Reboots, and Internet Outages

Your agents run 24/7. Things will break. The gateway will crash, your Mac will sleep, WiFi will drop, Discord will have an outage. This guide covers every failure mode and how to recover.

---

## Failure Modes and Recovery

### 1. Gateway Dies (Terminal Closed, Process Killed)

**What happens:** All crons stop. Agents stop posting. Discord bots go offline.

**How to detect:**
```bash
cd /path/to/openclaw
node openclaw.mjs gateway status
# If "RPC probe: ok" → alive. Otherwise → dead.
```

**How to recover:**
```bash
node openclaw.mjs gateway --force &
```

**How to prevent:**
> Install as a **LaunchAgent** (macOS) so it auto-restarts:
> ```bash
> node openclaw.mjs gateway install
> ```
> This creates a macOS LaunchAgent that starts the gateway on login and restarts on crash. **This is the #1 most important resilience pattern.**

> If you can't install LaunchAgent, use **Amphetamine** (free macOS app) to prevent sleep, and run the gateway in a **tmux** or **screen** session:
> ```bash
> tmux new -s openclaw
> node openclaw.mjs gateway --force
> # Ctrl+B then D to detach
> # tmux attach -t openclaw to reattach
> ```

**What about missed crons?**
> When the gateway restarts, it checks for overdue crons and **fires them immediately**. So if the gateway was down for 6 hours and a cron was scheduled during that time, it runs on restart. You may see "12h ago" in the "Next" column — that means it was overdue and will fire now.

---

### 2. Internet Drops (WiFi Outage, ISP Down)

**What happens:**
- Discord bots disconnect
- Agent sessions that need web_search fail
- SSH to EC2 fails
- Git push fails

**How OpenClaw handles it:**
> Discord bots have **auto-reconnect with backoff**. When connection drops, they retry at 1s, 2s, 4s, 8s... intervals. You'll see in logs:
> ```
> discord gateway: Attempting resume with backoff: 1000ms after code 1006
> ```
> When internet returns, bots reconnect automatically. **No action needed.**

**What about in-progress agent sessions?**
> If an agent was mid-session when internet dropped:
> - **web_search calls fail** → agent may fall back to cached knowledge or skip
> - **Discord posting fails** → delivery gets queued for retry
> - **git push fails** → changes are committed locally, push on next session
> The session itself runs locally (claude-cli is local) — it doesn't need internet to think, only to search/post/push.

**How to detect:**
```bash
# Check Discord bot health
node openclaw.mjs status
# Look for "stopped" or "reconnecting" channels
```

---

### 3. Mac Sleeps or Screen Locks

**What happens:** Depends on settings.
- **Screen lock only (Amphetamine running):** Everything keeps running. Gateway alive, crons fire normally.
- **Mac actually sleeps:** Gateway process suspends. Crons don't fire. Discord bots disconnect.

**How to prevent:**
> Install **Amphetamine** from the Mac App Store (free). Set it to "Prevent Sleep" indefinitely. Screen can lock — that's fine. As long as the Mac doesn't sleep, the gateway runs.

**Recovery after sleep:**
> Gateway resumes when Mac wakes. Overdue crons fire immediately. Discord bots auto-reconnect. Usually recovers within 30 seconds.

---

### 4. Mac Reboots

**What happens:** Gateway process dies. All agents stop. tmux sessions lost.

**How to recover:**
```bash
# After reboot, restart gateway
cd /path/to/openclaw
node openclaw.mjs gateway --force &
```

**How to prevent:**
> **LaunchAgent** (best):
> ```bash
> node openclaw.mjs gateway install
> ```
> Gateway auto-starts on login. Overdue crons fire immediately.

> **Login Items** (alternative): Add a script to System Settings → Login Items that runs the gateway on login.

---

### 5. Agent Session Hangs / Times Out

**What happens:** Agent produces no output for 480 seconds → OpenClaw kills it and marks cron as error.

**Common causes:**
| Cause | Fix |
|-------|-----|
| Missing `.claude/settings.json` | Add `bypassPermissions` to agent workspace |
| Claude API overloaded | Auto-retries. Falls back to Opus if Sonnet times out. |
| Agent stuck in a loop | PUA skill prevents this. Check SOUL.md for ambiguous instructions. |

**How to detect:**
```bash
node openclaw.mjs cron list
# Status "error" with "consecutiveErrors: N" means repeated failures
```

**Recovery:** Fix the root cause, then the next cron run will succeed. If cron has too many consecutive errors, delete and recreate it.

---

### 6. Discord Outage

**What happens:** Bots can't post. Agent sessions complete but delivery fails.

**How OpenClaw handles it:**
> Failed deliveries go to a **recovery queue**. When Discord comes back, OpenClaw retries. You'll see in logs:
> ```
> [delivery-recovery] Found 1 pending delivery entries — starting recovery
> ```

**What if delivery recovery also fails?**
> The agent's work is still done (files updated, git committed). Only the Discord announcement was lost. Check the agent's MEMORY.md or git log to see what happened.

---

### 7. EC2 Instance Stops (Paper Trading)

**What happens:** Freqtrade paper tests stop. No trades simulated.

**How to detect:**
```bash
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo systemctl is-active freqtrade-paper-daily-ma120.service'
# "active" = good, timeout/error = instance down
```

**Recovery:**
```bash
# Start the instance
aws ec2 start-instances --instance-ids i-01e93b5394248448f --profile openclaw-papertest --region us-west-2

# Wait 60s, then verify
ssh -o ConnectTimeout=10 openclaw-ec2-direct 'sudo systemctl status freqtrade-paper-daily-ma120.service --no-pager | head -5'
```

> EC2 paper tests use **systemd** with `Restart=always` — they auto-restart when the instance boots. No manual restart needed.

---

### 8. Git Push Conflicts

**What happens:** Multiple agents modify the same repo simultaneously → push rejected.

**How to handle:**
> Agents should always pull before push:
> ```bash
> git pull --rebase origin main && git push origin main
> ```

**Prevention:**
> Stagger cron schedules so agents don't commit simultaneously. Our schedule:
> - Sage daily commit: 9:30 AM
> - Forge daily commit: 9:45 AM (15 min gap)

---

## Resilience Checklist

| Pattern | Status | How |
|---------|--------|-----|
| Gateway auto-restart | Set up LaunchAgent | `node openclaw.mjs gateway install` |
| Prevent Mac sleep | Install Amphetamine | Free from App Store |
| Discord auto-reconnect | Built-in | No action needed |
| Overdue cron catch-up | Built-in | Fires on gateway restart |
| Delivery retry queue | Built-in | Auto-retries failed Discord posts |
| EC2 auto-restart | systemd Restart=always | Built-in for paper tests |
| Git conflict prevention | Staggered cron schedules | 15 min gaps between agents |
| Agent timeout recovery | Auto-retry on next cron | Fix root cause if repeated |

## The One Thing You Must Do

> **Install the gateway as a LaunchAgent.** Everything else has built-in recovery. But if the gateway isn't running, nothing works. LaunchAgent ensures it starts on boot and restarts on crash.
>
> ```bash
> cd /path/to/openclaw
> node openclaw.mjs gateway install
> ```
>
> This single command handles 80% of resilience. Everything else is nice-to-have.
