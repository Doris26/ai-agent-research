# Pattern 17: Gateway Topology — One Gateway, Many Agents

**Problem:** Should each agent get its own gateway, or share one?

**Answer:** One gateway per machine. Always.

---

## Why One Gateway

The gateway is a message router, not an agent runtime. It handles:
- Multiple Discord bot accounts simultaneously
- Multiple agent sessions concurrently
- Multiple cron jobs independently
- Multiple servers/guilds at once

```
ONE Gateway (port 18789)
├── Discord Account: sage (bot token A)
├── Discord Account: forge (bot token B)
├── Discord Account: scout (bot token C)
├── Discord Account: scholar (bot token D)
├── Discord Account: analyst (bot token E)
├── Agent: sage (workspace, SOUL.md, cron jobs)
├── Agent: forge (workspace, SOUL.md, cron jobs)
├── Agent: scout (workspace, SOUL.md, cron jobs)
├── Agent: scholar (workspace, SOUL.md, cron jobs)
└── Agent: analyst (workspace, SOUL.md, cron jobs)
```

Each agent has its own:
- Discord bot account (separate token, separate identity)
- Workspace (separate SOUL.md, MEMORY.md)
- Cron schedule (independent timing)
- Session store (independent conversation history)

But they all run through **one gateway process**.

---

## Why NOT Multiple Gateways

| Problem | What Happens |
|---------|-------------|
| Port conflict | Both try to bind port 18789 |
| WebSocket race | Two gateways receive same Discord event → duplicate responses |
| Split config | Cron jobs, agent definitions scattered across configs |
| Double maintenance | Two processes to monitor, restart, update |
| No benefit | Gateway already handles concurrency internally |

---

## When You DO Need Multiple Gateways

**Only when agents run on different machines:**

```
Machine A (Home Mac)              Machine B (Office Mac)
├── Gateway A (port 18789)        ├── Gateway B (port 18789)
├── sage, forge                   ├── scout, scholar, analyst
└── Trading research              └── AI research
```

Each machine gets its own gateway, its own `openclaw.json`, its own set of agents. They communicate via Discord (shared server) not via gateway-to-gateway.

**Even then, prefer one machine** — simpler ops, one config, one process to monitor.

---

## The Config Structure (One Gateway, 5 Agents)

```json
{
  "agents": {
    "list": [
      { "id": "sage",    "workspace": "/path/to/sage" },
      { "id": "forge",   "workspace": "/path/to/forge" },
      { "id": "scout",   "workspace": "/path/to/scout" },
      { "id": "scholar", "workspace": "/path/to/scholar" },
      { "id": "analyst", "workspace": "/path/to/analyst" }
    ]
  },
  "channels": {
    "discord": {
      "accounts": {
        "sage":             { "token": "BOT_TOKEN_A" },
        "forge":            { "token": "BOT_TOKEN_B" },
        "scout-research":   { "token": "BOT_TOKEN_C" },
        "scholar-research": { "token": "BOT_TOKEN_D" },
        "analyst-research": { "token": "BOT_TOKEN_E" }
      }
    }
  }
}
```

**5 agents, 5 bot accounts, 1 gateway, 1 config file, 1 process.**

---

## Operational Implications

### Restart = all agents restart
When you restart the gateway, ALL agents reconnect. This is usually fine — sessions resume from MEMORY.md. But avoid unnecessary restarts.

### Config change = gateway restart needed
Editing `openclaw.json` (tokens, agents, channels) requires a gateway restart to take effect. The running gateway caches config in memory.

### Token rotation = gateway restart needed
If you regenerate a Discord bot token, update `openclaw.json` AND restart the gateway. The old token in memory won't work for new connections.

### Cron jobs survive restarts
Cron state is stored in `~/.openclaw/cron/jobs.json`. After restart, the gateway reads this file and resumes all scheduled jobs.

### Don't restart to fix a stuck agent
If one agent is stuck, don't restart the whole gateway. Instead:
- @mention the agent in Discord (triggers new session)
- Run `openclaw cron run <job-id>` (manually fire its cron)
- Check logs for the specific agent error

Restarting the gateway kills ALL active sessions for ALL agents.

---

## Summary

| Topology | When | Agents Per Gateway |
|----------|------|--------------------|
| 1 gateway, N agents | Same machine (default) | All of them |
| 2 gateways, split agents | Different machines | Split by machine |
| 1 gateway per agent | Never | Don't do this |
