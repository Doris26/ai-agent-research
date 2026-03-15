# Agent Security Guide — Protecting Identity, Permissions, and Secrets

When running autonomous AI agents 24/7, security is not optional. Agents can modify files, push to git, post to Discord, and SSH to servers. Without guardrails, a single misconfigured agent can overwrite critical files, leak secrets, or drift from its mission.

This guide covers the security patterns we use and **why each one matters**.

---

## 1. Protect Agent Identity Files

### The Problem
> Agents can rewrite their own SOUL.md. If an agent modifies its own identity file, it can gradually drift from its original mission. An agent designed to "scan ProductHunt for AI agent tools" could rewrite itself to "do general AI research" or worse. **This is the #1 risk with autonomous agents.**

### The Solution: Read-Only Identity Files

**Which files to protect:**
| File | Contains | Risk if Modified |
|------|----------|-----------------|
| `SOUL.md` | Agent identity, mission, rules | Agent drifts from mission |
| `AGENTS.md` | Skills, tools, API access | Agent gains unintended capabilities |
| `CLAUDE.md` | Project-wide rules | All agents lose guardrails |
| `RESEARCH_LOOP.md` | Research protocol | Research process breaks |
| `NIGHTLY_SPRINT.md` | Sprint protocol | Sprint behavior changes |

**Which files agents CAN modify:**
| File | Contains | Why Agents Need Write Access |
|------|----------|---------------------------|
| `MEMORY.md` | Learned knowledge | Must update after every session |
| `PATTERNS.md` | Discovered patterns | Captures reusable insights |
| `RESEARCH.md` | Research log | Records findings with dates |
| `skills/` | Skill files | May create new recipes |

### How to Implement

**Step 1: File permissions**
```bash
# Lock identity files (read-only for everyone)
chmod 444 agents/my-agent/SOUL.md
chmod 444 agents/my-agent/AGENTS.md

# When YOU need to edit:
chmod 644 agents/my-agent/SOUL.md   # unlock
vim agents/my-agent/SOUL.md          # edit
chmod 444 agents/my-agent/SOUL.md   # re-lock
```

**Step 2: Pre-commit hook**

Create `.githooks/pre-commit`:
```bash
#!/bin/bash
# Block commits to protected files unless human override
PROTECTED_FILES=(
  "agents/sage/SOUL.md"
  "agents/sage/AGENTS.md"
  "agents/forge/SOUL.md"
  "agents/forge/AGENTS.md"
  "CLAUDE.md"
)

for file in "${PROTECTED_FILES[@]}"; do
  if git diff --cached --name-only | grep -q "^$file$"; then
    if [ -z "$ALLOW_PROTECTED" ]; then
      echo "⛔ BLOCKED: $file is protected."
      echo "   Human override: ALLOW_PROTECTED=1 git commit ..."
      exit 1
    fi
  fi
done
```

Install it:
```bash
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

**Step 3: Agent CLAUDE.md**

Every agent workspace gets a `CLAUDE.md` that explicitly lists what's off-limits:
```markdown
# Agent Rules

## Protected Files (DO NOT MODIFY)
- SOUL.md — only Yujun can change
- AGENTS.md — only Yujun can change

## Files You CAN Modify
- MEMORY.md — update after every session
- PATTERNS.md — add new patterns
- RESEARCH.md — log findings
```

> **Why CLAUDE.md?** Claude Code reads CLAUDE.md as system instructions at the start of every session. This is the most reliable way to tell the agent "don't touch these files" — it's baked into every session context.

---

## 2. API Key Security

### The Problem
> API keys committed to git get leaked. Google, GitHub, and AWS all scan repos for exposed keys and revoke them automatically. We learned this the hard way — our Gemini API key was revoked within hours of being committed to a GitHub repo.

### Rules

| Do | Don't |
|----|-------|
| Store keys in `~/.openclaw/` or `~/.zshrc` | Commit keys to git repos |
| Read keys from files at runtime | Hardcode keys in Python scripts |
| Use `.gitignore` for `.env` files | Put keys in SOUL.md or AGENTS.md |
| Rotate keys if exposed | Reuse revoked keys |

### Pattern: Runtime Key Loading
```python
# ✅ CORRECT — read from secure file at runtime
with open("/Users/yujunzou/.openclaw/gemini_api_key") as f:
    api_key = f.read().strip()

# ❌ WRONG — hardcoded
api_key = "AIzaSy..."  # NEVER do this
```

### Key Locations on This Machine
| Key | Location | NOT in |
|-----|----------|--------|
| Gemini API | `~/.openclaw/gemini_api_key` | Any git repo |
| Discord bot tokens | `~/.openclaw/openclaw.json` | Any git repo |
| BinanceUS API | `~/.zshrc` env vars | Any git repo |
| AWS credentials | `~/.aws/credentials` | Any git repo |

### What to Do If a Key is Leaked
1. **Immediately revoke** the key in the provider's dashboard
2. Generate a **new key**
3. Update the local file (NOT the repo)
4. Search git history: `git log -p --all -S "leaked_key_prefix"` and clean if needed

---

## 3. Discord Permission Security

### The Problem
> Bots with Administrator permission can do anything — create channels, delete messages, kick users. If a bot token is compromised, an attacker has full server control.

### Recommendations

**For development/small teams (current setup):**
- Administrator permission is fine for convenience
- Keep bot tokens in `~/.openclaw/openclaw.json` only (never in git)

**For production/larger teams:**
- Use minimum required permissions per bot:
  - Scout: Send Messages, Read History, Embed Links
  - Scholar: Send Messages, Read History, Embed Links
  - Analyst: Send Messages, Read History, Embed Links, Manage Messages
- Create a `#config` channel that only humans can post in
- Use Discord's channel-level permissions to restrict which bots can post where

### Channel Permission Pattern
```
#scout-feed     → Scout can post, others read-only
#scholar-feed   → Scholar can post, others read-only
#daily-briefing → Analyst can post, others read-only
#config         → Only human operators can post
```

---

## 4. SSH & Server Access Security

### The Problem
> Agents SSH to EC2 to check papertests and update the Golden Sheet. If SSH keys are exposed or permissions are too broad, an agent could accidentally (or through prompt injection) run destructive commands on the server.

### Current Setup
| Item | Value | Security |
|------|-------|----------|
| SSH key | `~/.ssh/openclaw_ec2_codex` | Generated on this machine, ed25519 |
| EC2 access | IPv6 direct + AWS SSM | No password auth |
| Agent SSH scope | Read logs, update Golden Sheet | Limited to specific commands |

### Recommendations
- SSH key is **not** in any git repo
- Agents should only run **specific, known commands** via SSH (not arbitrary bash)
- Consider using SSM Run Command instead of SSH for better audit logging
- Never give agents `sudo` access to production servers

---

## 5. Message Content Intent

### The Problem
> Discord requires bots to explicitly opt-in to reading message content (since August 2022). Without this, your bot can post but **cannot read** other bots' messages. This silently breaks multi-agent communication.

### How to Enable
1. Go to https://discord.com/developers/applications
2. Click your bot → **Bot** tab
3. Scroll to **Privileged Gateway Intents**
4. Toggle **Message Content Intent** → ON
5. Click **Save Changes**

> **Cost:** FREE for bots in fewer than 100 servers. No subscription needed. Discord may show a verification warning — ignore it unless you're in 100+ servers.

### What Breaks Without It
- Analyst cannot read Scout's posts in #scout-feed
- Agents cannot respond to @mentions
- Multi-agent communication completely fails
- OpenClaw logs will show: `"Message Content Intent is disabled"`

---

## 6. Claude CLI Permissions

### The Problem
> Claude CLI prompts for permission before reading/writing files. In an autonomous cron, there's nobody to click "approve." The agent hangs until it times out.

### Solution
Create `.claude/settings.json` in each agent workspace:
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
```

> **Why this is safe:** The agent only has access to files in its workspace directory. Combined with read-only identity files (chmod 444), the agent can freely read/write its knowledge files but cannot modify its own mission.

---

## 7. Git Security

### Rules for Agents
- **Never force push** (`git push --force`)
- **Never push to main directly** in production repos (use branches + PRs)
- **Always pull before push** to avoid conflicts
- **Never commit secrets** — check `git diff --cached` before committing

### Pre-commit Checks
The pre-commit hook should also scan for leaked secrets:
```bash
# Add to .githooks/pre-commit
if git diff --cached | grep -iE "(api_key|secret|token|password)\s*=\s*['\"]?[A-Za-z0-9]" | grep -v "\.md"; then
  echo "⚠️ WARNING: Possible secret detected in commit. Review carefully."
fi
```

---

## Security Checklist

- [ ] Identity files (SOUL.md, AGENTS.md) are chmod 444
- [ ] Pre-commit hook blocks changes to protected files
- [ ] Agent CLAUDE.md lists protected vs editable files
- [ ] API keys stored in `~/` paths, NOT in git repos
- [ ] Discord bots have Message Content Intent enabled
- [ ] Bot tokens only in `~/.openclaw/openclaw.json`
- [ ] SSH keys not in any git repo
- [ ] `.claude/settings.json` in each agent workspace
- [ ] No secrets in git history (`git log -p -S "key_prefix"`)
