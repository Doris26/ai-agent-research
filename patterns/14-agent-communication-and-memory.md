# Pattern 14: How Agents See, Talk, and Remember

This pattern explains exactly how information flows in a multi-agent system — what each agent can see, how they communicate, and how memory works.

---

## How an Agent "Sees" Things

An agent has 4 sources of information, loaded in this order:

```
┌─────────────────────────────────────────────────────┐
│  1. SOUL.md (auto-loaded, every session)            │  WHO am I? What's my mission?
│  2. MEMORY.md (auto-loaded, every session)          │  What do I know from past sessions?
│  3. USER.md (auto-loaded, every session)            │  Who is the human I work for?
│  4. Cron message (injected at session start)        │  What should I do RIGHT NOW?
├─────────────────────────────────────────────────────┤
│  Loaded on-demand (agent must actively read):       │
│  5. Discord messages (API call)                     │  What did other agents post?
│  6. Daily logs (memory/YYYY-MM-DD.md)               │  What did I do yesterday?
│  7. Shared files (RESEARCH_LEDGER.md, etc.)         │  Shared facts across agents
│  8. Web search results                              │  External information
└─────────────────────────────────────────────────────┘
```

**Auto-loaded = costs tokens every session.** Keep these files small.
**On-demand = free until the agent reads them.** Can be large.

---

## How Agents Talk to Each Other

Agents do NOT share memory. They communicate through **Discord messages** — like coworkers in a Slack channel.

### The Flow

```
Scout's session:
  1. Reads SOUL.md + MEMORY.md (auto)
  2. Does web_search for AI products
  3. Posts findings to #scout-feed via Discord API
  4. Session ends

        ↓ (30 min gap)

Analyst's session:
  1. Reads SOUL.md + MEMORY.md (auto)
  2. Reads #scout-feed via Discord API (last 20 msgs)
  3. Reads #scholar-feed via Discord API (last 20 msgs)
  4. Synthesizes → posts briefing to #daily-briefing
  5. Session ends
```

### How an Agent Reads Discord

```python
import urllib.request, json

# This is a FREE Discord API call — no Claude tokens used
req = urllib.request.Request(
    "https://discord.com/api/v10/channels/CHANNEL_ID/messages?limit=20",
    headers={"Authorization": "Bot BOT_TOKEN"}
)
messages = json.loads(urllib.request.urlopen(req).read())

# Agent now sees last 20 messages from that channel
for m in messages:
    print(f"{m['author']['username']}: {m['content']}")
```

**Key:** Reading Discord costs 0 Claude tokens. It's a simple HTTP call. The agent only pays tokens when it processes the messages with Claude.

### How an Agent Posts to Discord

```python
# Agent posts via Discord API — also free, no Claude tokens
curl -X POST "https://discord.com/api/v10/channels/CHANNEL_ID/messages" \
  -H "Authorization: Bot BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "🔍 Found: CrewAI v0.80 released with memory support"}'
```

Or OpenClaw handles delivery automatically via `--to "channel:ID"` in the cron config.

### How @mentions Work (Trigger vs Read)

Two different things:
- **@mention = TRIGGER** — wakes up the agent, creates a new session
- **API read = CONTEXT** — agent reads recent messages to understand what happened

```
Forge @mentions Sage: "@Sage evaluate results"
  → OpenClaw creates new Sage session (TRIGGER)
  → Sage reads Discord API — last 20 messages (CONTEXT)
  → Sage sees Forge's results, proposals, everything
  → Sage does the work
```

**When to @mention:** Only when you need another agent to ACT. Not for status posts.
- `@Forge backtest this` → Forge wakes up, reads channel, backtests
- `@Sage evaluate and continue` → Sage wakes up, reads results, continues

**When NOT to @mention:** Status posts, proposals, results — just post them. Everyone can read the channel via API anytime.

**Config required:** Set `allowBots: "mentions"` in Discord config so bot-to-bot @mentions work. Set `tools.profile: "full"` so agents have tools in @mention sessions.

---

## How an Agent Sees Its Own Markdowns

### Auto-loaded Every Session (OpenClaw injects these)

| File | What Agent Sees | Token Cost |
|------|----------------|------------|
| **SOUL.md** | Its identity, mission, rules, output format | Every session |
| **MEMORY.md** | Curated knowledge from all past sessions | Every session |
| **USER.md** | Who Yujun is, how to tailor output | Every session |
| **AGENTS.md** | Available skills and tools | Every session |
| **CLAUDE.md** | Project rules and constraints | Every session |

> **These files are loaded automatically.** The agent doesn't need to read them — OpenClaw injects them into the session context. That's why keeping them small saves tokens.

### Read On-Demand (agent uses Read tool)

| File | When Agent Reads It | Token Cost |
|------|-------------------|------------|
| `memory/YYYY-MM-DD.md` | When it needs yesterday's raw notes | Only when read |
| `RESEARCH_LEDGER.md` | When checking shared facts | Only when read |
| `PATTERNS.md` | When proposing new strategies | Only when read |
| `RESEARCH.md` | When checking research log | Only when read |
| Other agent's files | **NEVER** — communicate via Discord | N/A |

---

## How Memory Management Works

### The Two-Tier System

```
Session runs:
  ├── Agent does work (search, analyze, etc.)
  ├── Writes EVERYTHING to memory/2026-03-15.md (daily log)
  │     "Searched ProductHunt, found 5 products, 2 relevant..."
  │     "CrewAI v0.80 has memory support, pricing unchanged..."
  │     "Raw search results: [full text]"
  │
  ├── Promotes KEY FACTS to MEMORY.md (1-2 lines)
  │     "CrewAI v0.80: memory support added. Relevant to Vertex AI."
  │
  └── Commits both to git

Next session:
  ├── MEMORY.md auto-loaded (small, curated — 5 tokens)
  ├── memory/2026-03-15.md NOT loaded (saves tokens)
  └── If agent needs yesterday's details → reads daily log on-demand
```

### What Goes Where

| Info Type | Where | Example |
|-----------|-------|---------|
| Raw findings | `memory/YYYY-MM-DD.md` | "Searched arxiv, found 12 papers, 3 relevant..." |
| Key facts | `MEMORY.md` | "Best strategy: Calmar 3.05 (Round 6)" |
| Validated patterns | `PATTERNS.md` | "SMA strategies cap at Calmar ~3.0 in bear markets" |
| Shared facts | `RESEARCH_LEDGER.md` | Table row: date, product, source, status |
| Strategy results | `MEMORY.md` | "Round 8: ADX/DI, Calmar 1.21, REJECTED" |

### What Each Agent Can See of Other Agents

| | Scout's files | Scholar's files | Analyst's files | Shared files |
|--|--------------|----------------|----------------|-------------|
| **Scout** | ✅ All own files | ❌ Cannot see | ❌ Cannot see | ✅ RESEARCH_LEDGER.md |
| **Scholar** | ❌ Cannot see | ✅ All own files | ❌ Cannot see | ✅ RESEARCH_LEDGER.md |
| **Analyst** | ❌ Cannot see | ❌ Cannot see | ✅ All own files | ✅ RESEARCH_LEDGER.md |

**Agents share information via:**
1. **Discord posts** — summaries with links (cheap, auditable)
2. **RESEARCH_LEDGER.md** — shared fact table (structured, no reasoning leaked)
3. **@mentions** — targeted questions (Analyst asks Scout to dig deeper)

**Agents do NOT share:**
- MEMORY.md (private, contains internal reasoning)
- Daily logs (private, contains raw messy notes)
- SOUL.md (protected, only human changes)

---

## Summary: The Information Architecture

```
┌──────────────────────────────────────────────┐
│              Human (Yujun)                    │
│  Can read everything. Can change SOUL.md.     │
│  Reviews RESEARCH_LEDGER.md weekly.           │
├──────────────────────────────────────────────┤
│           RESEARCH_LEDGER.md                  │
│  Shared fact table. All agents read/write.    │
├──────────────────────────────────────────────┤
│         Discord Channels                      │
│  #scout-feed ← Scout posts                   │
│  #scholar-feed ← Scholar posts                │
│  #daily-briefing ← Analyst posts              │
│  Agents read each other's channels (free)     │
├──────┬───────────┬───────────┬───────────────┤
│Scout │  Scholar  │  Analyst  │    (private)   │
│SOUL  │  SOUL     │  SOUL     │  auto-loaded   │
│MEMORY│  MEMORY   │  MEMORY   │  auto-loaded   │
│daily/│  daily/   │  daily/   │  on-demand     │
│PATTERN│ PATTERN  │  PATTERN  │  on-demand     │
└──────┴───────────┴───────────┴───────────────┘
```
