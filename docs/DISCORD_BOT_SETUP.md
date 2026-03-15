# Setup Guide — AI Agent Research Hub

## Prerequisites

- macOS with Node.js installed
- OpenClaw built and working (`/Users/yujunzou/python/python_repo/openclaw/`)
- Python 3.9+ with `google-genai` installed
- Discord account
- Gemini API key

---

## Step 1: Create Discord Server

1. Open Discord → click `+` on left sidebar → "Create My Own"
2. Name it: **AI Research Hub**
3. Enable Developer Mode: Settings → Advanced → Developer Mode

## Step 2: Create Discord Bots

Go to https://discord.com/developers/applications for each:

### Bot 1: Scout
1. New Application → name "Scout"
2. Go to Bot tab → click "Reset Token" → copy token
3. **Enable "Message Content Intent"** under Privileged Gateway Intents
4. Go to OAuth2 → URL Generator
   - Scopes: `bot`
   - Permissions: Send Messages, Read Message History, Manage Messages, Embed Links
5. Copy URL → open in browser → select your server

### Bot 2: Scholar
Same steps, name "Scholar"

### Bot 3: Analyst
Same steps, name "Analyst"

**IMPORTANT:** For each bot, you MUST enable **Message Content Intent** in the Bot settings tab. Without this, the bot cannot read message content.

## Step 3: Create Discord Channels

In your Discord server, create these text channels:
- `#scout-feed` — Scout posts product/platform findings here
- `#scholar-feed` — Scholar posts paper summaries here
- `#daily-briefing` — Analyst posts daily intelligence briefing here
- `#general` — general discussion

Copy each channel's ID (right-click → Copy Channel ID).

## Step 4: Configure OpenClaw

The OpenClaw config lives at `~/.openclaw/openclaw.json`. Add the AI Research agents alongside any existing config.

See [OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md) for the exact config to add.

## Step 5: Start Gateway

```bash
cd /Users/yujunzou/python/python_repo/openclaw
node openclaw.mjs gateway --force
```

## Step 6: Add Crons

```bash
cd /Users/yujunzou/python/python_repo/openclaw

# Scout — daily 8 AM CST (UTC 14:00)
node openclaw.mjs cron add \
  --name "scout-daily" \
  --cron "0 14 * * *" \
  --session isolated \
  --agent scout \
  --to "channel:<SCOUT_FEED_CHANNEL_ID>" \
  --message "..."

# Scholar — daily 8:30 AM CST (UTC 14:30)
node openclaw.mjs cron add \
  --name "scholar-daily" \
  --cron "30 14 * * *" \
  --session isolated \
  --agent scholar \
  --to "channel:<SCHOLAR_FEED_CHANNEL_ID>" \
  --message "..."

# Analyst — daily 9:30 AM CST (UTC 15:30)
node openclaw.mjs cron add \
  --name "analyst-daily" \
  --cron "30 15 * * *" \
  --session isolated \
  --agent analyst \
  --to "channel:<DAILY_BRIEFING_CHANNEL_ID>" \
  --message "..."
```

## Step 7: Verify

```bash
node openclaw.mjs cron list
```

Should show 3 crons: scout-daily, scholar-daily, analyst-daily.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Bot can't read messages | Enable "Message Content Intent" in Discord Developer Portal → Bot tab |
| Gateway dies | Restart: `node openclaw.mjs gateway --force` |
| Cron not firing | Check `node openclaw.mjs cron list` for error status |
| Claude CLI hangs | Ensure `.claude/settings.json` has `bypassPermissions` in agent workspace |
