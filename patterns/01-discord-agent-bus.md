# Pattern 1: Discord as Agent Bus (50-80% Token Savings)

**Problem:** Piping Agent A's full output into Agent B costs tokens for ALL of A's reasoning as B's input.

**Solution:** Agents communicate via Discord channel posts — short summaries only.

| Approach | Tokens/cycle | Monthly Cost (3 agents) |
|----------|-------------|------------------------|
| Piped (full context) | ~500K | $90-240 |
| Discord summaries | ~150K | $20-30 |
| **Savings** | **70%** | **75-90%** |

**How it works:**
```
Scout → posts findings to #scout-feed (summary + links)
Scholar → posts papers to #scholar-feed (summary + links)
Analyst → reads both feeds (free Discord API) → synthesizes daily briefing
```

**Why Discord specifically?**
- Messages persist — scroll back anytime
- Team members can read without running code
- @mentions enable agent-to-agent follow-ups
- Human-readable audit trail
- Free

**Live example — Scout posting its daily scan to #scout-feed:**

![Discord AI Research Hub — Scout agent posting daily scan results to #scout-feed channel](../images/discord-scout-feed.png)
