# Quick Start — First Agent in 5 Minutes

Get from zero to an AI agent posting to Discord in 5 minutes. No fluff.

---

## Prerequisites
- Node.js installed (`brew install node`)
- Claude Code installed and authenticated (`claude --version`)
- A Discord server with a bot token ([create one](https://discord.com/developers/applications))

## 1. Build OpenClaw (1 min)
```bash
git clone https://github.com/nicobailon/openclaw.git
cd openclaw && npm install -g pnpm && pnpm install && pnpm run build
node openclaw.mjs onboard --non-interactive --accept-risk
```

## 2. Set up Claude Code permissions (30 sec)
```bash
cat > ~/.claude/settings.json << 'EOF'
{
  "permissions": { "defaultMode": "bypassPermissions" },
  "skipDangerousModePermissionPrompt": true
}
EOF
```

## 3. Create your agent (1 min)
```bash
mkdir -p ~/my-agent/.claude
cp ~/.claude/settings.json ~/my-agent/.claude/settings.json

cat > ~/my-agent/SOUL.md << 'EOF'
# MyBot — Hello World Agent
You are MyBot. When asked, say hello and share one interesting AI fact.
EOF
```

## 4. Configure OpenClaw (1 min)

Edit `~/.openclaw/openclaw.json` — add your agent and Discord bot:
```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "claude-cli": { "command": "/path/to/claude" }
      }
    },
    "list": [
      {
        "id": "mybot",
        "workspace": "/absolute/path/to/my-agent/",
        "model": { "primary": "claude-cli/claude-sonnet-4-6" }
      }
    ]
  },
  "channels": {
    "discord": {
      "accounts": {
        "mybot": { "token": "YOUR_BOT_TOKEN" }
      }
    }
  }
}
```

Replace `/path/to/claude` (run `which claude`) and `YOUR_BOT_TOKEN`.

## 5. Start and test (1 min)
```bash
cd /path/to/openclaw
node openclaw.mjs gateway --force &
sleep 5

# Fire a one-shot test
node openclaw.mjs cron add \
  --name "test" \
  --at "1m" \
  --session isolated \
  --agent mybot \
  --delete-after-run \
  --to "channel:YOUR_CHANNEL_ID" \
  --message "Read your SOUL.md and introduce yourself."
```

Check Discord in ~2 minutes. Your agent should post.

## Done!

Next steps:
- [SETUP.md](SETUP.md) — full multi-agent setup
- [HOW_TO_BUILD_AGENTS.md](HOW_TO_BUILD_AGENTS.md) — design patterns and best practices
- [SECURITY.md](SECURITY.md) — protect your agents
