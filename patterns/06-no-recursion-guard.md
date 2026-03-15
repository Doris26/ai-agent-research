# Pattern 6: No-Recursion Guard

**Problem:** Agent A asks Agent B → B posts results → A's cron triggers → asks B again → infinite loop. Burns tokens, crashes system.

**Solution:** Each agent's SOUL.md has a `⛔ No-Recursion Rule`:

| Agent | Can Spawn | Cannot Spawn |
|-------|-----------|-------------|
| Scout | Nobody | Scholar, Analyst |
| Analyst | Nobody | Scout, Scholar |
| Sage | Forge (one-shot only) | Itself |
| Forge | Nobody | Any agent |

**Rules:**
- Downstream consumers NEVER spawn upstream agents
- Only designated orchestrators can spawn sub-agents
- Sub-agents use `--delete-after-run` (one-shot, no recurring)
- NEVER self-spawn
