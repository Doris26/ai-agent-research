# How to Build AI Agents with OpenClaw — Step-by-Step Tutorial

This guide teaches you how to set up your own multi-agent AI research system from scratch using OpenClaw + Discord + Claude.

---

## Why This Architecture?

### 🔑 Why separate Discord bots for each agent?
> **Token savings.** If you pipe Agent A's full output directly into Agent B, you pay Claude API tokens for ALL of Agent A's reasoning + output as Agent B's input. With Discord, Agent A posts a **summary** to a channel. Agent B reads only the summary (free Discord API call). **This saves 50-80% of Claude API costs.**

### 🔑 Why Discord instead of piping outputs?
> **Persistence + visibility.** Discord messages are persistent — you can scroll back and see what agents said. Team members can read the feeds without running any code. Agents can @mention each other for follow-ups. It's a human-readable audit trail.

### 🔑 Why `--session isolated`?
> **Clean context.** Without isolation, an agent might reuse stale context from yesterday's run. Isolated sessions start fresh every time — the agent reads its SOUL.md + MEMORY.md and works from current state. **Never skip this for cron jobs.**

### 🔑 Why `--to "channel:ID"`?
> **Silent failure prevention.** Without `--to`, the cron runs but output goes nowhere. The agent does work but nobody sees it. This was a real bug we hit — crons ran for days with no visible output. **Always specify the target channel.**

### 🔑 Why SOUL.md matters so much?
> **It's the agent's job description.** SOUL.md is injected as system context on every run. A vague SOUL.md = vague, rambling output. A specific SOUL.md with exact sources, output format, and rules = focused, useful output. **Spend 80% of your design time on SOUL.md.**

### 🔑 Why agents must commit to git?
> **Knowledge persistence.** MEMORY.md is how agents remember across sessions. If they don't commit, the next session starts from stale knowledge. Also, if the machine reboots, uncommitted work is lost. **Every cron message should end with a git commit instruction.**

### 🔑 Why Message Content Intent must be enabled?
> **Discord security feature.** Discord disabled message reading by default for bots in August 2022. Without this intent enabled, your bot can post messages but **cannot read** other bots' messages. This breaks the whole multi-agent communication pattern. **Enable it in Discord Developer Portal → Bot → Privileged Gateway Intents → Message Content Intent.**
>
> **⚠️ Important:** This is **FREE** for bots in fewer than 100 servers (no subscription or verification needed). Just toggle it ON and save. Discord may show a warning about verification — ignore it unless your bot is in 100+ servers.

### 🔑 Why use claude-cli as the backend?
> **Cost.** Claude Code CLI (`claude-cli`) uses your Claude Pro/Team subscription — you pay a flat monthly fee, not per-token. This makes agent runs essentially **free** after subscription. If you use the Anthropic API directly, each agent run costs $0.50-2.00 in API tokens. With claude-cli, you get unlimited runs within your subscription limits. **Always use `claude-cli/claude-sonnet-4-6` as the model for cost efficiency.**

---

## Step 1: Install OpenClaw

```bash
# Install Node.js (if needed)
brew install node

# Install pnpm
npm install -g pnpm

# Clone and build OpenClaw
git clone https://github.com/nicobailon/openclaw.git
cd openclaw
pnpm install
pnpm run build

# First-time setup
node openclaw.mjs onboard --non-interactive --accept-risk
```

This creates `~/.openclaw/openclaw.json` — the main config file.

---

## Step 2: Install Claude CLI

```bash
# Install Claude Code CLI
# Follow instructions at https://docs.anthropic.com/en/docs/claude-code
# The binary typically installs to ~/.local/bin/claude

# Verify
claude --version

# Set up permissions for autonomous use
cat > ~/.claude/settings.json << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
EOF
```

> **Why bypassPermissions?** Agents run autonomously via crons — there's nobody to click "approve" on file reads/writes. This setting lets the agent work without interactive approval.

---

## Step 3: Create Discord Server & Bots

### Create Server
1. Open Discord → click `+` on left sidebar → "Create My Own"
2. Enable Developer Mode: User Settings (gear icon, bottom left) → Advanced → Developer Mode ON

### Create Bots (one per agent)
For each agent, go to https://discord.com/developers/applications:

1. Click "New Application" → name it (e.g., "Scout")
2. Go to **Bot** tab → click "Reset Token" → **copy and save the token**
3. **⚠️ CRITICAL: Enable "Message Content Intent"** under Privileged Gateway Intents
4. Go to **OAuth2** → **URL Generator**
   - Scopes: check `bot`
   - Bot Permissions: check `Administrator`
5. Copy the generated URL → open in browser → select your server → Authorize

> **Why Administrator?** Simplifies permissions. The bot can create channels, read messages, post — everything it needs. For production, you'd scope this down.

### Get Channel IDs
Right-click each channel → "Copy Channel ID" (requires Developer Mode enabled).

---

## Step 4: Design Your Agents

### Create Workspace
```bash
mkdir -p my-project/agents/my-agent/{skills,.claude}
```

### Write SOUL.md (THE most important file)

```markdown
# MyAgent — Clear Name & Emoji

You are **MyAgent**, a [specific role] that [specific mission].

## Your Mission
[1-2 sentences. Be SPECIFIC. Not "research AI" but "find new AI agent products launched in the last 24 hours on ProductHunt and Hacker News"]

## Sources to Check
1. [Specific source with URL pattern]
2. [Another source]
3. [Another source]

## Output Format
For each finding, include:
- **Title** with hyperlink
- **Summary** (1-2 sentences)
- **Category:** [list categories]
- **Relevance:** High/Medium/Low

## Team @mentions
- **AgentA:** `<@BOT_USER_ID>`
- **AgentB:** `<@BOT_USER_ID>`

## Discord Channels
- `#channel-name` (CHANNEL_ID) — what goes here

## Rules
- [Specific constraint]
- [Another rule]
- Always commit to git after each session
```

> **Good SOUL.md test:** If you gave this to a new hire on day 1, would they know exactly what to do? If not, add more detail.

### Create .claude/settings.json
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
```

### Create MEMORY.md
Start with `# MEMORY.md` — the agent will fill it in as it learns.

---

## Step 5: Configure OpenClaw

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
        "workspace": "/absolute/path/to/agents/my-agent/",
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
          "token": "BOT_TOKEN_HERE"
        }
      }
    }
  }
}
```

> **Important:** Workspace path must be absolute. Model format is `backend/model-name`.

---

## Step 6: Start Gateway

```bash
cd /path/to/openclaw
node openclaw.mjs gateway --force
```

Verify bots connected in the log output — look for "logged in to discord as [ID] (bot-name)".

---

## Step 7: Set Up Crons

```bash
cd /path/to/openclaw

# One-shot test (fires in 1 minute, deletes after)
node openclaw.mjs cron add \
  --name "test-my-agent" \
  --at "1m" \
  --session isolated \
  --agent my-agent \
  --delete-after-run \
  --to "channel:CHANNEL_ID" \
  --message "Read your SOUL.md and introduce yourself."

# Daily recurring
node openclaw.mjs cron add \
  --name "my-agent-daily" \
  --cron "0 14 * * *" \
  --session isolated \
  --agent my-agent \
  --to "channel:CHANNEL_ID" \
  --message "Read your SOUL.md and MEMORY.md. Do your daily task. Commit changes to git."

# Every 4 hours
node openclaw.mjs cron add \
  --name "my-agent-4h" \
  --every "4h" \
  --session isolated \
  --agent my-agent \
  --to "channel:CHANNEL_ID" \
  --message "..."
```

### Cron Management
```bash
node openclaw.mjs cron list              # See all crons
node openclaw.mjs cron delete CRON_ID    # Remove a cron
```

> **Cron time format:** UTC. `0 14 * * *` = 2 PM UTC = 8 AM CST.

---

## Step 8: Multi-Agent Communication

### Pattern: Feed → Synthesize

```
Agent A (Scout) → posts to #scout-feed
Agent B (Scholar) → posts to #scholar-feed
Agent C (Analyst) → reads both feeds → posts to #daily-briefing
```

### Reading Discord in Python (for agents)

```python
import urllib.request, json

def read_channel(channel_id, bot_token, limit=20):
    req = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}",
        headers={"Authorization": f"Bot {bot_token}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

# Read last 20 messages
messages = read_channel("CHANNEL_ID", "BOT_TOKEN")
for m in messages:
    print(f"[{m['timestamp'][:16]}] {m['author']['username']}: {m['content'][:200]}")
```

### @mentioning Other Agents

Include bot user IDs in SOUL.md so agents can ping each other:
```
Ping Scout: <@1234567890>
Ping Analyst: <@0987654321>
```

---

## Step 9: Skills (Reusable Recipes)

Create `skills/<name>/SKILL.md` in the agent workspace:

```markdown
---
name: my-skill
description: "What this skill does. When to use it."
---

# Skill Name

## When to Use
[Trigger conditions]

## How to Run
[Step-by-step instructions with exact commands]

## Expected Output
[What the agent should produce]
```

Skills prevent agents from reinventing the wheel each session.

---

## Step 10: Monitoring & Debugging

```bash
# Tail live logs
node openclaw.mjs logs

# Check cron status (look for "error" or "ok")
node openclaw.mjs cron list

# View agent sessions
node openclaw.mjs sessions --agent my-agent

# Check Discord directly
curl -s "https://discord.com/api/v10/channels/CHANNEL_ID/messages?limit=5" \
  -H "Authorization: Bot BOT_TOKEN" | python3 -m json.tool
```

### Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Cron runs but no Discord post | Missing `--to` | Add `--to "channel:ID"` |
| Bot can't read messages | Message Content Intent disabled | Enable in Discord Dev Portal |
| Agent hangs / times out | Missing `.claude/settings.json` | Add `bypassPermissions` config |
| "Unknown Guild" error | Bot not invited to server | Re-invite with OAuth2 URL |
| Git push fails | Uncommitted changes conflict | `git pull --rebase` first |

---

## Cost Estimate

| Component | Per Agent Run | Daily (3 agents) |
|-----------|--------------|-------------------|
| Claude Sonnet | $0.50-2.00 | $3-6 |
| Gemini Deep Research | $0.04-0.10 | $0-0.30 |
| Discord | Free | Free |
| OpenClaw | Free | Free |
| **Total** | | **~$3-8/day** |

---

## Security: Protecting Agent Identity Files

Agents can update their own MEMORY.md, PATTERNS.md, RESEARCH.md — but they should **NEVER** modify their own SOUL.md or AGENTS.md. Only the human operator should change an agent's identity and core mission.

### Why This Matters
> If an agent can rewrite its own SOUL.md, it can drift from its original mission over time. An agent that starts as "scan ProductHunt for AI tools" could gradually rewrite itself to "do whatever seems interesting." This is a real risk with autonomous agents running on crons.

### How to Enforce

**1. File permissions (local):**
```bash
# Make identity files read-only
chmod 444 agents/my-agent/SOUL.md
chmod 444 agents/my-agent/AGENTS.md

# To edit as human operator:
chmod 644 agents/my-agent/SOUL.md
# ... make changes ...
chmod 444 agents/my-agent/SOUL.md
```

**2. Pre-commit hook (git):**
```bash
# .githooks/pre-commit
#!/bin/bash
PROTECTED_FILES=("agents/*/SOUL.md" "agents/*/AGENTS.md" "CLAUDE.md")
for pattern in "${PROTECTED_FILES[@]}"; do
  if git diff --cached --name-only | grep -qE "^$pattern$"; then
    if [ -z "$ALLOW_PROTECTED" ]; then
      echo "⛔ BLOCKED: Protected file. Set ALLOW_PROTECTED=1 to override."
      exit 1
    fi
  fi
done

# Install:
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

**3. Agent CLAUDE.md (instructions):**
Create a `CLAUDE.md` in each agent workspace listing which files are protected:
```markdown
## Protected Files (DO NOT MODIFY)
- SOUL.md — only Yujun can change
- AGENTS.md — only Yujun can change

## Files You CAN Modify
- MEMORY.md — update after every session
- PATTERNS.md — add new patterns
- RESEARCH.md — log findings
```

**4. Discord channel permissions (optional):**
Create a `#agent-config` channel where only the human operator can post. Agents read config updates from this channel but cannot modify it.

---

## Checklist: Before Going Live

- [ ] All bots have Message Content Intent enabled
- [ ] All bots invited to Discord server with permissions
- [ ] Each agent has SOUL.md, MEMORY.md, .claude/settings.json
- [ ] OpenClaw config has all agents + Discord accounts
- [ ] Gateway starts without errors
- [ ] Test cron posts to correct channel
- [ ] Agent workspace is a git repo (for commit/push)
- [ ] Crons have `--session isolated` and `--to "channel:ID"`
