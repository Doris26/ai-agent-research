# Pattern 14: Agent Communication — Three Protocols, One System

This pattern documents the complete multi-agent communication architecture. Most frameworks support only 1:1 streaming or "transfer to agent." OpenClaw supports three simultaneous communication paths.

---

## The Three Communication Protocols

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway (localhost:18789)            │
│                    WebSocket + JSON-RPC + Token Auth             │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  Scout   │   │  Sage    │   │  Forge   │   │ Analyst  │   │
│  │ (claude) │   │ (claude) │   │ (claude) │   │ (claude) │   │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘   │
│       │              │              │              │           │
│  ─────┴──────────────┴──────────────┴──────────────┴────────── │
│       │              │              │                          │
│   Protocol 1     Protocol 2     Protocol 3                    │
│   Discord Bus    ACP Spawn      File-Based                    │
│   (visible)      (invisible*)   (async)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Protocol 1: Discord as Agent Bus (Visible, Async)

**How:** Each agent has a dedicated Discord bot. Posts summaries to channels. Other agents read via API.

**When to use:** Status updates, results, proposals, audit trail.

```
Scout runs (cron 8:00 AM):
  1. web_search for AI products
  2. Posts findings to #scout-feed via Discord API
  3. Session ends

        ↓ (90 min gap — no tokens burned)

Analyst runs (cron 9:30 AM):
  1. Reads #scout-feed via Discord API (FREE — 0 tokens)
  2. Reads #scholar-feed via Discord API (FREE — 0 tokens)
  3. Synthesizes → posts briefing to #daily-briefing
  4. Session ends
```

**Cost:** Reading Discord = 0 tokens (HTTP call). Only synthesis costs tokens.

**Triggering other agents:** `@mention` wakes them up.
```
Sage posts: "@Forge backtest S50 ADX+OBV strategy"
  → OpenClaw sees @mention → creates new Forge session
  → Forge reads channel for context → does the work
```

**Config required for bot-to-bot @mentions:**
```json
{
  "allowBots": "mentions",
  "tools": { "profile": "full" }
}
```

### Token Savings vs Direct Piping

| Approach | Tokens/cycle | Monthly (3 agents) |
|----------|-------------|-------------------|
| Piped (full context) | ~500K | $90-240 |
| Discord summaries | ~150K | $20-30 |
| **Savings** | **70%** | **75-90%** |

---

## Protocol 2: ACP Spawn (Invisible, Synchronous)

**How:** Agent A spawns Agent B as a sub-session via `sessions_spawn`. B runs, returns result to A.

**When to use:** Agent needs another agent's output to continue its own work.

```python
# Inside Sage's session:
sessions_spawn({
    task: "Backtest RSI strategy on BTC, 1Y window, report Calmar",
    agentId: "forge",
    thread: false,    # invisible — no Discord output
    mode: "run"       # oneshot — run and return
})
# Sage blocks, waits for Forge result, then continues
```

### Visible vs Invisible ACP

| Config | Discord Visible? | Use Case |
|--------|-----------------|----------|
| `thread: true` | Yes — creates Discord thread | Debug, human monitoring |
| `thread: false` | No — runs silently | Speed, batch processing |

### ACP Session Lifecycle

```
1. Parent calls sessions_spawn({agentId, task, thread})
2. Gateway creates session: agent:forge:acp:uuid
3. If thread=true: creates Discord thread, posts intro
4. Child agent runs with full tool access
5. Child completes → result returned to parent
6. If thread=true: posts farewell, thread goes read-only
```

### Spawn Depth Limit

```
Sage (depth 0)
  → spawns Forge (depth 1)
    → Forge spawns sub-agent (depth 2)
      → ... up to maxSpawnDepth: 5
```

Prevents infinite recursion. Configurable per agent.

### ACP vs Discord Bus — When to Use Which

| | Discord Bus | ACP Spawn |
|--|------------|-----------|
| **Visibility** | Everyone sees it | Silent (unless thread: true) |
| **Timing** | Async (minutes/hours gap) | Sync (parent waits) |
| **Cost** | Cheap (summaries only) | Full context (more tokens) |
| **Audit trail** | Yes (Discord history) | Only if threaded |
| **Use case** | Status, results, proposals | "I need X computed now" |

---

## Protocol 3: File-Based (Async, Persistent)

**How:** Agent A writes to shared files. Agent B reads them in its next session.

**When to use:** Long-term knowledge transfer, structured data, shared state.

```
Forge finishes backtest:
  1. Updates GOLDEN_SHEET.md with results
  2. Updates its own MEMORY.md
  3. Commits to git

        ↓ (next session, hours later)

Sage wakes up:
  1. MEMORY.md auto-loaded (sees strategy status)
  2. Reads GOLDEN_SHEET.md (shared across all agents)
  3. Knows which strategies passed/failed without Discord
```

### What's Shared vs Private

| File | Shared? | Who Writes | Who Reads |
|------|---------|-----------|----------|
| `SOUL.md` | Private | Human only | Own agent |
| `MEMORY.md` | Private | Own agent | Own agent |
| `memory/YYYY-MM-DD.md` | Private | Own agent | Own agent |
| `GOLDEN_SHEET.md` | Shared | Any agent | All agents |
| `RESEARCH_LEDGER.md` | Shared | Any agent | All agents |
| Discord channels | Shared | Posting agent | Any agent (API read) |

---

## How All Three Work Together (Real Example)

```
[8:00 AM] Scout cron fires (Protocol 3: reads SOUL.md, MEMORY.md)
  → web_search for AI products
  → Posts to #scout-feed (Protocol 1: Discord)
  → Updates RESEARCH_LEDGER.md (Protocol 3: File)

[8:30 AM] Scholar cron fires
  → Searches arxiv
  → Posts to #scholar-feed (Protocol 1)
  → Updates RESEARCH_LEDGER.md (Protocol 3)

[9:30 AM] Analyst cron fires
  → Reads #scout-feed + #scholar-feed (Protocol 1: free API call)
  → Reads RESEARCH_LEDGER.md (Protocol 3)
  → If needs deeper analysis: sessions_spawn(scholar, "dig into paper X") (Protocol 2: ACP)
  → Posts daily briefing to #daily-briefing (Protocol 1)
```

---

## Why Three Protocols Instead of One?

| Need | Best Protocol | Why |
|------|--------------|-----|
| "Post results for everyone" | Discord Bus | Visible, auditable, cheap |
| "I need this computed now" | ACP Spawn | Synchronous, returns result |
| "Remember this for next time" | File-Based | Persistent across sessions |
| "Wake up Agent B" | Discord @mention | Triggers new session |
| "Share structured data" | File (LEDGER.md) | All agents read it |

Using only one protocol creates bottlenecks:
- **Only Discord:** Can't do synchronous sub-tasks
- **Only ACP:** Expensive (full context piping), no audit trail
- **Only Files:** No real-time communication, no triggering

The combination gives you **async + sync + persistent** coverage with minimal token waste.

---

## Configuration Reference

### Discord Account (per agent)
```json
{
  "token": "BOT_TOKEN",
  "groupPolicy": "open",
  "streaming": "off",
  "guilds": { "GUILD_ID": {} }
}
```

### ACP Config
```json
{
  "acp": {
    "enabled": true,
    "dispatch": { "enabled": true },
    "backend": "acpx",
    "defaultAgent": "claude",
    "allowedAgents": ["claude", "claude-code", "codex", "gemini"]
  }
}
```

### Thread Binding (for visible ACP)
```json
{
  "channels": {
    "discord": {
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true,
        "spawnAcpSessions": true
      }
    }
  }
}
```

### Cron Job (triggers Protocol 1 or 3)
```json
{
  "agentId": "scout",
  "schedule": { "kind": "cron", "expr": "0 8 * * *" },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "to": "channel:DISCORD_CHANNEL_ID"
  }
}
```

---

## Summary Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Human (Yujun)                           │
│   Reads Discord, reviews GOLDEN_SHEET, changes SOUL.md     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Protocol 1: Discord Bus          Protocol 2: ACP Spawn    │
│  ┌──────────────────────┐        ┌───────────────────┐    │
│  │ #scout-feed    ← Scout│        │ Sage ──spawn──→   │    │
│  │ #scholar-feed  ← Scholar      │    Forge (silent) │    │
│  │ #daily-briefing← Analyst      │    ↓ result back  │    │
│  │ #yujun-team    ← Sage/Forge│  │ Sage continues    │    │
│  │                        │      └───────────────────┘    │
│  │ Agents read each other │                               │
│  │ via API (0 tokens)     │      Protocol 3: Files        │
│  │                        │      ┌───────────────────┐    │
│  │ @mention = trigger     │      │ GOLDEN_SHEET.md   │    │
│  │ new agent session      │      │ RESEARCH_LEDGER.md│    │
│  └──────────────────────┘        │ MEMORY.md (private)│   │
│                                   │ memory/daily.md   │    │
│                                   └───────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Scout    Scholar    Sage    Forge    Analyst               │
│  (own     (own       (own    (own     (own                  │
│   SOUL,    SOUL,      SOUL,   SOUL,    SOUL,               │
│   MEMORY)  MEMORY)    MEMORY) MEMORY)  MEMORY)             │
└─────────────────────────────────────────────────────────────┘
```
