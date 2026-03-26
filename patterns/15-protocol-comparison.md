# Pattern 15: Protocol Comparison — Discord vs ACP vs File-Based

Side-by-side comparison of the three agent communication protocols. Use this to pick the right one for each interaction.

---

## The Quick Answer

| "I need to..." | Use |
|----------------|-----|
| Post results for the team to see | Discord Bus |
| Wake up another agent | Discord @mention |
| Get a computed result to continue my work | ACP Spawn |
| Share structured data across agents | File (LEDGER.md, GOLDEN_SHEET.md) |
| Remember something for my next session | File (MEMORY.md) |
| Debug a sub-agent's work in real time | ACP Spawn with `thread: true` |

---

## Full Comparison Table

| Dimension | Discord Bus (@mention) | ACP Spawn | File-Based (Markdown) |
|-----------|----------------------|-----------|----------------------|
| **Mechanism** | Bot posts to Discord channel via API | `sessions_spawn()` creates child session | Agent writes .md file, other reads later |
| **Visible in chat?** | Yes — everyone sees it | No (unless `thread: true`) | No — only in git/filesystem |
| **Sync or Async?** | Async — fire and forget | Sync — parent waits for result | Async — next session reads it |
| **Latency** | Minutes to hours (depends on cron schedule) | Seconds to minutes (runs immediately) | Hours to days (next session startup) |
| **Parent blocks?** | No — agent posts and moves on | Yes — waits for child to finish | No — write and forget |
| **Result delivery** | Child posts back to Discord channel | Result returned directly to parent | Reader finds it in file next session |
| **Token cost** | Low — summaries only (~150 words) | High — full context piped to child | Zero — file I/O, no LLM involved |
| **Audit trail** | Yes — Discord history (scrollable, searchable) | Only if `thread: true` (creates Discord thread) | Yes — git history |
| **Human can watch?** | Yes — real time in Discord | Only if threaded | Yes — read the file anytime |
| **Trigger mechanism** | @mention wakes agent via OpenClaw | Parent agent calls spawn function | Cron/heartbeat starts session, agent reads file |
| **Session type** | New independent session | Child session under parent (depth tracked) | No new session — just file read |
| **Failure handling** | Agent doesn't reply? Visible in Discord | Spawn fails → parent gets error | File missing → agent handles gracefully |
| **Recursion risk** | Low — manual @mentions | Medium — max depth limit (default 5) | None — no execution triggered |
| **Concurrency** | Multiple agents read same channel | Parent blocked, but other agents free | Multiple agents read same file |
| **Persistence** | Discord stores messages forever | Session-scoped (gone after completion) | Git-backed, survives restarts |
| **Cross-project** | Yes — any bot in the server | Only within same OpenClaw gateway | Yes — if repos are shared |
| **Setup complexity** | Bot token + channel + guild config | ACP backend + agent config + allowed list | Just write/read files |

---

## Cost Comparison (3 agents, daily cycle)

| Protocol | Tokens Used | What Gets Billed |
|----------|------------|-----------------|
| **Discord Bus** | ~150K/cycle | Only synthesis (reading Discord API = free) |
| **ACP Spawn** | ~500K/cycle | Full context of parent + child |
| **File-Based** | ~0/cycle | File I/O only — billed when agent reads file into context |
| **Discord + File combo** | ~150K/cycle | Best of both: cheap comms + persistent memory |

---

## When Each Protocol Breaks Down

### Discord Bus Limitations
- **No synchronous results** — Sage can't say "wait for Forge's answer then continue"
- **Noisy for internal work** — 50 status messages clutter the channel
- **Rate limits** — Discord API limits: 5 messages/5 seconds per channel
- **Context window** — Agent reads last 20 messages, misses older ones

### ACP Spawn Limitations
- **Expensive** — full context piping burns tokens
- **No audit trail** (without threading) — silent failures are invisible
- **Gateway required** — only works within same OpenClaw instance
- **Depth limits** — max 5 levels deep, can't model complex hierarchies
- **Single gateway** — can't span across machines (without Tailscale/proxy)

### File-Based Limitations
- **No real-time** — reader must start a new session to see updates
- **No triggering** — writing a file doesn't wake anyone up
- **Merge conflicts** — two agents writing same file simultaneously
- **Stale data** — agent reads MEMORY.md from hours ago, world has changed

---

## Hybrid Patterns (What Works Best in Production)

### Pattern A: Discord Trigger + File State (Current Sage/Forge setup)
```
Sage posts to Discord: "@Forge backtest S50"     → Discord (trigger)
Forge reads channel, runs backtest               → Forge's own session
Forge posts results to Discord                   → Discord (results)
Forge updates GOLDEN_SHEET.md                    → File (persistent state)
Sage reads Discord + GOLDEN_SHEET.md next wake   → Both protocols
```
**Best for:** Async research loops where humans want visibility.

### Pattern B: ACP Spawn + File State (Faster, invisible)
```
Sage spawns Forge: sessions_spawn("backtest S50") → ACP (sync)
Forge runs, returns result to Sage                → ACP (result)
Sage updates GOLDEN_SHEET.md                      → File (persistent)
Sage posts summary to Discord                     → Discord (audit)
```
**Best for:** Speed-critical workflows where human doesn't need to watch every step.

### Pattern C: Full Pipeline (Scout → Scholar → Analyst)
```
Scout posts to #scout-feed                        → Discord (async)
Scholar posts to #scholar-feed                    → Discord (async)
Both update RESEARCH_LEDGER.md                    → File (shared state)
Analyst reads both channels + ledger              → Discord + File (input)
Analyst spawns Scholar for deep dive              → ACP (sync sub-task)
Analyst posts briefing to #daily-briefing         → Discord (output)
```
**Best for:** Multi-agent pipeline with both async collection and sync sub-tasks.

---

## Decision Flowchart

```
Need to communicate with another agent?
│
├── Does the OTHER agent need to ACT right now?
│   ├── Yes → Do I need the result to continue MY work?
│   │   ├── Yes → ACP Spawn (sync, get result back)
│   │   └── No  → Discord @mention (trigger, move on)
│   └── No  → Just posting info for later?
│       ├── Structured data → File (LEDGER.md, GOLDEN_SHEET.md)
│       └── Summary/status → Discord channel post
│
├── Do I need to remember this for MY next session?
│   └── Yes → File (MEMORY.md or memory/daily.md)
│
└── Should humans see this?
    ├── Yes → Discord (always)
    └── No  → File or ACP (depending on above)
```

---

## Configuration Summary

| Protocol | Required Config |
|----------|----------------|
| Discord Bus | Bot token, channel ID, guild ID, `groupPolicy` |
| Discord @mention | Above + `allowBots: "mentions"` + `tools.profile: "full"` |
| ACP Spawn | `acp.enabled`, `acp.dispatch.enabled`, `acp.backend: "acpx"`, agent in `allowedAgents` |
| ACP Thread | Above + `threadBindings.enabled`, `spawnAcpSessions: true` |
| File-Based | Shared git repo, agreed file paths |
