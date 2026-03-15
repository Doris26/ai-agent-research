# Auto Skill Evolution — How Agents Learn and Improve Over Time

Agents shouldn't just run tasks — they should **get better** at running tasks. Auto skill evolution is the pattern where agents update their own knowledge and skills after each session, creating a feedback loop of continuous improvement.

---

## The Problem

> Without skill evolution, every agent session starts from scratch. The agent makes the same mistakes, asks the same questions, and produces the same generic output. After 30 days of daily runs, the agent is no smarter than day 1.

## The Solution

> After every session, agents update their knowledge files and commit to git. The next session reads the updated files and builds on previous work. **The agent literally teaches itself.**

---

## How It Works

```
Session 1: Agent reads SOUL.md + empty MEMORY.md
           → does work → learns things
           → updates MEMORY.md with learnings
           → commits to git

Session 2: Agent reads SOUL.md + MEMORY.md (now has Session 1 learnings)
           → does better work (knows what failed before)
           → updates MEMORY.md with new learnings
           → commits to git

Session N: Agent reads SOUL.md + rich MEMORY.md
           → knows all past results, failed strategies, validated patterns
           → produces expert-level output
```

---

## What Agents Update (Auto-Evolving Files)

| File | What Evolves | Example |
|------|-------------|---------|
| **MEMORY.md** | Facts, results, team info, rules learned | "Round 7 EnsembleConsensus: Calmar 0.72, REJECTED" |
| **PATTERNS.md** | Validated patterns backed by evidence | "SMA-based strategies cap at Calmar ~3.0 in bear markets" |
| **RESEARCH.md** | Timestamped research log | "2026-03-14: Tested vol-targeting, improves MaxDD by 39%" |
| **RESEARCH_LEDGER.md** | Shared fact table | New product/paper entries with dates and links |

## What Agents Do NOT Update (Protected Files)

| File | Why Protected |
|------|--------------|
| **SOUL.md** | Agent identity — only human changes this |
| **AGENTS.md** | Agent capabilities — only human changes this |
| **CLAUDE.md** | Project rules — only human changes this |

> **Key insight:** Let agents evolve their **knowledge** (what they know), but protect their **identity** (who they are). An agent that can rewrite its own mission will drift.

---

## Implementation: Daily Commit Cron

We set up a daily cron that tells the agent to review its work, update knowledge files, and push to git:

```bash
node openclaw.mjs cron add \
  --name "agent-daily-commit" \
  --cron "30 1 * * *" \
  --session isolated \
  --agent my-agent \
  --to "channel:CHANNEL_ID" \
  --message 'You are MyAgent. This is your daily knowledge sync.

## Step 1: Read your current knowledge
- Read your MEMORY.md
- Read your PATTERNS.md (if exists)

## Step 2: Update based on recent work
- Add any new findings from today
- Update status of ongoing items
- Add new patterns you discovered
- Remove outdated information

## Step 3: Commit and push
```bash
cd /path/to/repo
git add -A
git commit -m "docs(agent): daily knowledge sync [date]"
git push origin main
```

Post confirmation: "Knowledge sync complete. [X] files updated."'
```

### Timing

Schedule the commit cron **after** the main work cron:

| Time | Cron | Purpose |
|------|------|---------|
| 8:00 AM | scout-daily | Do the work |
| 8:30 AM | scholar-daily | Do the work |
| 9:30 AM | analyst-daily | Synthesize |
| 10:00 AM | all-daily-commit | Update knowledge + git push |

This ensures the commit cron captures all work done in the earlier sessions.

---

## Real Example: Sage's Skill Evolution

Sage (crypto quant researcher) started with an empty MEMORY.md. After 7 rounds of research:

**Day 1 MEMORY.md:**
```
# MEMORY.md
(empty)
```

**Day 7 MEMORY.md (auto-evolved):**
```
## Confirmed Failed Strategies (Tier 3)
- CrossPlatformDonchian: 0/81 positive on BinanceUS 2Y
- CrossPlatformMomentum: Negative all exchanges
- EMA/SMA switching: fundamentally broken in sustained downtrend

## Research Backlog
- Round 1-4: All SMA variants. Best Calmar=1.02. REJECTED.
- Round 5: WeeklyGatedBidirectional. Calmar=2.53. Tier 2.
- Round 6: VolTargeted. Calmar=3.05. BEST EVER.
- Round 7: EnsembleConsensus. Calmar=0.72. REJECTED.

## Key Pattern
SMA-based strategies cap at ~Calmar 3.0 in bear markets.
The SHORT side is the bottleneck.
```

> Sage now **automatically avoids** strategies it already tried and failed. No human had to tell it "don't try EMA switching again" — it learned from its own MEMORY.md.

---

## PATTERNS.md: The Knowledge Base

PATTERNS.md is where agents store **validated, reusable insights**:

```markdown
## Pattern: SMA Ceiling in Bear Markets
**Evidence:** Rounds 1-7, 7 consecutive SMA variants tested
**Finding:** SMA-based crypto strategies cap at Calmar ~3.0 in bearish BTC
**Root cause:** SMA lag forces 15-20% adverse move before exit signal
**Implication:** Need non-SMA signals (momentum, vol regime, order flow) to break Calmar 4.0
**Confidence:** High (7/7 rounds confirmed)
```

This pattern will prevent the agent from wasting time on SMA variants in future sessions.

---

## Anti-Pattern: Memory Bloat

> **Warning:** MEMORY.md grows over time. After 100+ sessions, it can exceed 1000 lines — burning tokens every session just to read context.

### How to Prevent
1. **Weekly review:** Human operator trims old/irrelevant entries
2. **Archival rule:** Tell agent in SOUL.md: "Keep MEMORY.md under 200 lines. Archive old entries to MEMORY_ARCHIVE.md"
3. **Structured format:** Tables are denser than prose. Use tables for results, not paragraphs.

---

## Checklist: Setting Up Auto Skill Evolution

- [ ] Agent SOUL.md says "update MEMORY.md after every session"
- [ ] Agent SOUL.md says "commit to git after every session"
- [ ] Daily commit cron scheduled after work crons
- [ ] MEMORY.md, PATTERNS.md, RESEARCH.md are writable (not chmod 444)
- [ ] SOUL.md, AGENTS.md are read-only (chmod 444)
- [ ] Pre-commit hook blocks changes to protected files
- [ ] Weekly human review of MEMORY.md size and quality
