# Claude Code Setup Guide

Claude Code is the CLI tool that powers OpenClaw's agent backend. Every agent session runs through `claude-cli` — so Claude Code must be installed and configured before OpenClaw can work.

---

## Why Claude Code?

> **Claude Code CLI (`claude`) uses your Claude Pro/Team subscription** — flat monthly fee, not per-token API charges. This makes agent runs essentially free within your subscription limits. If you used the Anthropic API directly, each agent run would cost $0.50-2.00 in tokens. With Claude Code, unlimited runs.

---

## Step 1: Install Claude Code

```bash
# Install via npm (recommended)
npm install -g @anthropic-ai/claude-code

# Or download binary directly
# https://docs.anthropic.com/en/docs/claude-code

# Verify installation
claude --version
```

Check where it installed:
```bash
which claude
# Usually: ~/.local/bin/claude or /usr/local/bin/claude
```

> **Important:** Remember this path — you'll need it for OpenClaw config (`cliBackends.claude-cli.command`).

---

## Step 2: Log In

```bash
claude
# Follow the prompts to authenticate with your Anthropic account
# This links Claude Code to your Claude Pro/Team subscription
```

---

## Step 3: Configure Permissions for Autonomous Use

> **Why this is critical:** When agents run via OpenClaw crons, there's nobody to click "approve" on file read/write prompts. Without `bypassPermissions`, the agent **hangs forever** waiting for approval, then times out after 480 seconds. This was a real bug that took hours to debug.

### Global Settings (applies to all Claude Code sessions)

```bash
cat > ~/.claude/settings.json << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
EOF
```

### Per-Agent Workspace Settings (ALSO required)

Each agent workspace needs its own settings file. Without this, agents in that workspace still get permission prompts:

```bash
# For each agent workspace:
mkdir -p /path/to/agent/workspace/.claude

cat > /path/to/agent/workspace/.claude/settings.json << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
EOF
```

> **You need BOTH** — global settings AND per-workspace settings. Global alone is not enough because Claude Code checks workspace-level settings first.

---

## Step 4: Verify It Works

Test that Claude Code runs without prompting:

```bash
cd /path/to/agent/workspace
claude --print "Say hello in one word"
```

Should return immediately with a response. If it hangs or asks for permission, the settings are not applied correctly.

---

## Step 5: Configure OpenClaw to Use Claude Code

In `~/.openclaw/openclaw.json`, set the CLI backend:

```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "claude-cli": {
          "command": "/Users/yujunzou/.local/bin/claude"
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
  }
}
```

**Key fields:**
| Field | Value | Notes |
|-------|-------|-------|
| `command` | Full path to `claude` binary | Use `which claude` to find it |
| `model.primary` | `claude-cli/claude-sonnet-4-6` | Cheapest option (uses subscription) |
| `model.fallbacks` | `["claude-cli/opus-4.6"]` | Optional — falls back if Sonnet times out |

---

## Available Models

| Model | Cost | Speed | Use For |
|-------|------|-------|---------|
| `claude-cli/claude-sonnet-4-6` | Subscription (cheap) | Fast | Daily tasks, scans, reports |
| `claude-cli/opus-4.6` | Subscription (more expensive) | Slower | Complex research, deep analysis |
| `claude-cli/haiku-4-5` | Subscription (cheapest) | Fastest | Simple lookups, status checks |

> **Always default to Sonnet** unless the task specifically needs Opus-level reasoning.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Agent hangs for 480s then times out | Missing `bypassPermissions` | Add settings.json to BOTH `~/.claude/` AND agent workspace `.claude/` |
| `command not found: claude` | Not installed or not in PATH | Run `npm install -g @anthropic-ai/claude-code` or check `which claude` |
| `CLI produced no output` in OpenClaw logs | Permission prompt blocking | Same fix — add bypassPermissions settings |
| Falls back to Opus unexpectedly | Sonnet timed out | Check if workspace has `.claude/settings.json` |
| `Authentication required` | Not logged in | Run `claude` interactively once to authenticate |

---

## Security Notes

- `bypassPermissions` means the agent can read/write ANY file in its workspace without asking
- This is safe because:
  1. Agent only accesses files in its workspace directory
  2. Critical files (SOUL.md, AGENTS.md) are `chmod 444` read-only
  3. Pre-commit hooks block changes to protected files
- **Never** use bypassPermissions on a shared machine where untrusted users have access
- The Claude Code authentication token is stored in `~/.claude/` — keep this directory secure

---

## Quick Reference

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Auth
claude  # follow prompts

# Global permissions
cat > ~/.claude/settings.json << 'EOF'
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "skipDangerousModePermissionPrompt": true
}
EOF

# Per-workspace permissions
mkdir -p /path/to/workspace/.claude
cp ~/.claude/settings.json /path/to/workspace/.claude/settings.json

# Test
cd /path/to/workspace && claude --print "Hello"

# Find binary path (for OpenClaw config)
which claude
```
