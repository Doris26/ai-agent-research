# Pattern 4: Auto Skill Evolution (Agents That Learn)

**Problem:** Without learning, every session starts from scratch. After 30 days, the agent is no smarter than day 1.

**Solution:** Agents update MEMORY.md after each session, commit to git. Next session reads updated knowledge.

```
Session 1: empty MEMORY.md → does work → writes learnings → commits
Session 7: rich MEMORY.md → knows all past failures → expert-level output
```

**Real example (Sage, crypto researcher):**
- Day 1: tried EMA switching strategy. Failed.
- Day 3: tried ATR regime filter. Failed.
- Day 7: MEMORY.md says "EMA/SMA switching fundamentally broken in downtrend." Agent **automatically avoids** this approach.
- No human told it to stop — it learned from its own history.

**What agents update (evolving):** MEMORY.md, PATTERNS.md, RESEARCH.md
**What agents don't touch (protected):** SOUL.md, AGENTS.md, CLAUDE.md

**Key insight:** Let agents evolve their **knowledge** (what they know), but protect their **identity** (who they are).

**Implementation:** Add a daily commit cron that runs after the work cron:
```bash
node openclaw.mjs cron add --name "agent-daily-commit" --cron "30 1 * * *" \
  --session isolated --agent my-agent --to "channel:ID" \
  --message "Update MEMORY.md with today's findings. Commit and push to git."
```

**Anti-pattern: Memory Bloat** — MEMORY.md grows forever. Fix: weekly human review, keep under 200 lines, archive old entries.
