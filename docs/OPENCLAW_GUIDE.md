# OpenClaw Team Guide — How to Use OpenClaw for AI Research

## What is OpenClaw?

OpenClaw is a **multi-agent AI gateway** that lets you run AI agents autonomously with:
- **Discord integration** — agents post to Discord channels
- **Cron scheduling** — run agents on recurring schedules
- **Isolated sessions** — each agent run gets its own context
- **Multiple agent backends** — Claude, Gemini, GPT, etc.

---

## Quick Start (5 minutes)

### 1. Install OpenClaw

```bash
# Clone and build
git clone https://github.com/nicobailon/openclaw.git
cd openclaw
npm install -g pnpm
pnpm install
pnpm run build

# First-time setup
node openclaw.mjs onboard --non-interactive --accept-risk
```

### 2. Configure Your Agent

Edit `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "claude-cli": {
          "command": "/path/to/claude"
        }
      }
    },
    "list": [
      {
        "id": "my-agent",
        "workspace": "/path/to/agent/workspace/",
        "model": {
          "primary": "claude-cli/claude-sonnet-4-6"
        }
      }
    ]
  },
  "channels": {
    "discord": {
      "accounts": {
        "my-bot": {
          "token": "YOUR_BOT_TOKEN"
        }
      }
    }
  }
}
```

### 3. Start the Gateway

```bash
cd /path/to/openclaw
node openclaw.mjs gateway --force
```

### 4. Send a Message

```bash
# One-shot task
node openclaw.mjs cron add \
  --name "test" \
  --at "1m" \
  --session isolated \
  --agent my-agent \
  --delete-after-run \
  --to "channel:CHANNEL_ID" \
  --message "Hello! Read your SOUL.md and introduce yourself."
```

---

## Key Concepts

### Agents
An agent is an AI that runs in its own workspace directory. The workspace contains key markdown files that shape the agent's behavior:

### Critical Markdown Files (in order of importance)

| File | Purpose | When to Update |
|------|---------|---------------|
| **SOUL.md** | Agent identity, mission, rules, output format. **This is the most important file** — it defines WHO the agent is and WHAT it does. A well-written SOUL.md = a well-performing agent. | When you want to change the agent's behavior |
| **MEMORY.md** | Persistent knowledge — what the agent knows across sessions. Strategies found, results, team info, rules learned. **Agent should update this after every session.** | After every agent run (auto-updated by agent) |
| **SKILLS/** | Skill files (SKILL.md) teach the agent HOW to do specific tasks. Each skill is a step-by-step recipe. E.g., "how to run a backtest", "how to read Discord", "how to use the deep research API". | When you add new capabilities |
| **.claude/settings.json** | Permissions config. Must have `bypassPermissions` for autonomous agent runs. | Once during setup |
| **PATTERNS.md** | Validated patterns and learnings. Things the agent has confirmed through evidence. | When agent discovers reusable knowledge |
| **RESEARCH.md** | Ongoing research log with dates and findings. | After each research session |

### Why SOUL.md Matters Most

The SOUL.md is injected into every agent session as system context. It's like giving an employee their job description + handbook on day 1. A vague SOUL.md = vague results. A specific SOUL.md = specific, useful results.

**Good SOUL.md includes:**
- Clear mission statement (1-2 sentences)
- Specific sources to check (with URLs/names)
- Exact output format (with examples)
- Rules and constraints
- What NOT to do

### Why Skills Matter

Skills are reusable recipes stored in `skills/<name>/SKILL.md`. They teach agents HOW to do things:

```
agents/scout/skills/
├── product-scan/SKILL.md    — how to scan ProductHunt, HN
├── cloud-monitor/SKILL.md   — how to check AWS/Azure/GCP updates
└── discord-post/SKILL.md    — how to format and post to Discord
```

Without skills, agents figure things out from scratch each run (slow, inconsistent, wastes tokens). With skills, they follow proven recipes (fast, consistent, cheap).

### Why Committing Code is Critical

**Agents MUST commit their changes to git after every session.** This is non-negotiable because:
1. Other agents may need the updated MEMORY.md
2. If the machine reboots, uncommitted work is lost
3. Team members need to see what agents did
4. Git history = audit trail of all agent decisions

**Rule:** Every cron message should end with: "Commit all changes to git after completing your work."

### Why Crons Need `--to` and `--session isolated`

Two mistakes that cause silent failures:

1. **Missing `--to "channel:ID"`** — the cron runs but output goes nowhere. The agent does work but nobody sees it. Always specify the target channel.

2. **Missing `--session isolated`** — without isolation, the agent may reuse stale context from a previous run. Always use `--session isolated` for crons.

### Crons
Crons schedule agent runs. Types:
- `--at "1m"` — run once in 1 minute
- `--every "4h"` — run every 4 hours
- `--cron "0 14 * * *"` — run at specific time (crontab format)

### Sessions
- `--session isolated` — fresh context each run (recommended for crons)
- Sessions preserve tool access (file read/write, bash, web search)

### Delivery
- `--to "channel:ID"` — post results to a Discord channel
- `--delete-after-run` — remove cron after execution (for one-shots)

---

## Common Commands

```bash
# List all crons
node openclaw.mjs cron list

# Delete a cron
node openclaw.mjs cron delete <CRON_ID>

# Check gateway status
node openclaw.mjs gateway status

# View agent sessions
node openclaw.mjs sessions --agent my-agent

# Tail gateway logs
node openclaw.mjs logs
```

---

## Building Your Own Agent

### Step 1: Create Workspace

```bash
mkdir -p my-agent/.claude
```

### Step 2: Write SOUL.md

```markdown
# My Agent — What I Do

You are **MyAgent**, an AI that [does something specific].

## Your Mission
[Clear, specific mission statement]

## Sources
[Where to look for information]

## Output Format
[Exactly how to format results]

## Rules
[Constraints and requirements]
```

### Step 3: Create Settings

```bash
cat > my-agent/.claude/settings.json << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
EOF
```

### Step 4: Add to OpenClaw Config

Add to `~/.openclaw/openclaw.json` under `agents.list`:

```json
{
  "id": "my-agent",
  "workspace": "/absolute/path/to/my-agent/",
  "model": {
    "primary": "claude-cli/claude-sonnet-4-6"
  }
}
```

### Step 5: Create Discord Bot

1. Go to https://discord.com/developers/applications
2. New Application → name your bot
3. Bot tab → Reset Token → copy it
4. **Enable "Message Content Intent"** ← IMPORTANT
5. OAuth2 → URL Generator → scope `bot` → permissions: Send Messages, Read History
6. Invite to your server

### Step 6: Add Bot Token to Config

```json
"channels": {
  "discord": {
    "accounts": {
      "my-bot": {
        "token": "YOUR_BOT_TOKEN_HERE"
      }
    }
  }
}
```

### Step 7: Schedule It

```bash
node openclaw.mjs cron add \
  --name "my-agent-daily" \
  --cron "0 14 * * *" \
  --session isolated \
  --agent my-agent \
  --to "channel:CHANNEL_ID" \
  --message "Read your SOUL.md and MEMORY.md, then do your daily task."
```

---

## Multi-Agent Communication — Why Separate Bots & Servers?

### The Token-Saving Architecture

Each agent gets its own **Discord bot account** and communicates via **@mentions** in Discord channels. This is a critical design choice:

**Why separate bots (not one shared bot)?**
- Each bot has its own identity → agents can `@mention` each other
- Scout posts to `#scout-feed`, Scholar posts to `#scholar-feed`
- Analyst reads both feeds by reading Discord messages (cheap API call)
- **This avoids passing full context between agents** → saves Claude API tokens

**Why Discord as the communication layer?**
- Without Discord: you'd need to pass Agent A's entire output as input to Agent B → costs tokens for both input AND output
- With Discord: Agent A posts a summary to a channel. Agent B reads only what it needs via Discord API (free). Agent B's Claude session only sees the summary, not Agent A's full reasoning chain
- **Token savings: 50-80%** compared to piping full agent outputs

**Why separate servers?**
- Different projects get different Discord servers (e.g., Apexnova trading vs AI research)
- Each server has its own channels, bots, and permissions
- Team members only join servers relevant to them
- Keeps research context isolated — trading agents don't see research noise

### How @mentions Work

```
Scout posts to #scout-feed:
  "🔍 New: CrewAI v0.80 released with memory support [link]"

Analyst reads #scout-feed via Discord API, then posts to #daily-briefing:
  "📊 Daily Briefing: CrewAI added memory — similar to Vertex AI Agent Builder's
   session history. Recommendation: integrate persistent memory into our agent SDK.
   @Scout any pricing changes with this release?"

Scout gets pinged, responds in thread:
  "No pricing changes. CrewAI remains MIT license."
```

### Reading Discord Messages (Python)

```python
import urllib.request, json

def read_channel(channel_id, bot_token, limit=20):
    req = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}",
        headers={"Authorization": f"Bot {bot_token}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

### Cost Comparison

| Approach | Tokens per daily cycle | Cost |
|----------|----------------------|------|
| Piped (A→B→C full context) | ~500K tokens | ~$8-15 |
| Discord @mentions (summaries only) | ~150K tokens | ~$3-5 |
| **Savings** | **~70%** | **~$5-10/day** |

---

## Tips

- **Always use `--session isolated`** for crons — prevents context bleed between runs
- **Always include `--to "channel:ID"`** — without this, crons silently fail
- **SOUL.md is key** — the more specific your SOUL.md, the better the agent performs
- **MEMORY.md persists** — agents should update it after each session
- **Commit to git** — always commit changes after agent runs
- **Monitor logs** — `node openclaw.mjs logs` or check `/tmp/openclaw/`

---

## Architecture

```
┌─────────────────────────────────────────┐
│           OpenClaw Gateway              │
│  (Node.js, runs on your machine)        │
├─────────────────────────────────────────┤
│  Cron Scheduler                         │
│  ├── scout-daily (8 AM)                 │
│  ├── scholar-daily (8:30 AM)            │
│  └── analyst-daily (9:30 AM)            │
├─────────────────────────────────────────┤
│  Agent Runner (claude-cli backend)      │
│  ├── Spawns Claude in agent workspace   │
│  ├── Agent reads SOUL.md, MEMORY.md     │
│  ├── Agent does work (search, analyze)  │
│  └── Posts results to Discord           │
├─────────────────────────────────────────┤
│  Discord Channels                       │
│  ├── #scout-feed                        │
│  ├── #scholar-feed                      │
│  └── #daily-briefing                    │
└─────────────────────────────────────────┘
```

---

## Cost

| Component | Cost |
|-----------|------|
| Claude Sonnet (per agent run) | ~$0.50-2.00 |
| Gemini Deep Research (per query) | ~$0.04-0.10 |
| Discord | Free |
| OpenClaw | Free (open source) |
| **Estimated daily total** | **~$3-8** |
