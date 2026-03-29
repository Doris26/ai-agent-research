# Patterns & Lessons Learned

## Gateway Operations
- Gateway is persistent — never restart to "wake up" agents
- Only restart when: config changed, crashed, tokens changed, updated
- Trigger agents via @mention or `openclaw cron run <job-id>`
- Pin to commit `ae60094fb5` — latest main has Discord regression
- Start: `node openclaw.mjs gateway run --force --allow-unconfigured`

## Config Pitfalls
- `default` account: `openclaw doctor` auto-creates it. Always remove after doctor.
- `agents.defaults.tools`: invalid key, breaks Discord init
- `allowBots: "mentions"`: required for bot-to-bot triggering
- NEVER `npm install` — use `pnpm install` (pnpm workspace)
- NEVER `openclaw doctor --fix` without checking what it changed

## Discord Bot Connections
- All 5 bots connect simultaneously via Carbon library
- If only 1-2 connect: rate limited from restarts. Wait or regenerate tokens.
- "awaiting gateway readiness" = IDENTIFY never got READY
- `sglang` plugin crash blocks ALL Discord init — check logs
- Lid close = auto-reconnect via RESUME. Do nothing on wake.

## Sequential Research Flow
- One kickoff cron (scout-daily) triggers the chain
- Scout → Scholar → Analyst (each pings next via curl)
- Each agent posts to its own feed channel + #daily-feed
- Scout/Scholar MUST use curl to trigger next agent (bot IDs, not plain text)
- Scout/Scholar NEVER update software — scan + feed only

## Trading Strategy Rules
- Max 4 free parameters per strategy (don't count shared template)
- Shared template: SMA=75, VT=13, RSI=50/50, ATR=14/2.5
- Verify robustness: standardize RSI to 50/50, re-run. If Calmar drops >50%, fragile.
- Golden Sheet is source of truth
- Forge: create Discord channel immediately for T1 (step 3, not step 7)
- Forge: update Golden Sheet after EVERY backtest, pass or fail

## CLI Auth (No Browser)
- `primaryProvider: bedrock` in `~/.claude/settings.json`
- Env vars: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `ANTHROPIC_DISABLE_OAUTH=1`
- "Not logged in" error = missing bedrock config

## Agent @mentions
- Plain text `@forge` does NOT trigger agents — Discord API limitation
- Must use bot ID format: `<@1480084559390441552>`
- Agents should use curl with bot ID to trigger each other
- `dangerouslyAllowNameMatching` doesn't fix this (it's for allowlists, not mentions)

## SSH Remote Access
- Tailscale: `ssh yujunzou@100.82.246.54` (any network)
- Local: `ssh yujunzou@YujuntekiMacBook-Pro.local` (same WiFi)
- Password auth enabled, SSH key from other Mac in authorized_keys
