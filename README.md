# AI Agent Research Hub

Daily AI agent intelligence — products, engineering, and academic papers. Powered by [OpenClaw](https://openclaw.ai).

## What This Does

Three AI agents run daily to scan, analyze, and synthesize the AI agent ecosystem:

| Agent | Role | Sources |
|-------|------|---------|
| **Scout** 🔍 | Product & platform hunter | ProductHunt, HackerNews, AWS, Azure, GCP, OpenAI, Anthropic, open source |
| **Scholar** 📚 | Academic paper researcher | arXiv, Semantic Scholar, Google Scholar, conference proceedings |
| **Analyst** 📊 | Insights synthesizer | Scout + Scholar outputs → daily report with recommendations |

## Daily Output

Every morning, **Analyst** posts a daily briefing to Discord:

- **New Products & Launches** — what shipped yesterday in AI agents
- **Platform Updates** — AWS Bedrock, Azure AI, Google Cloud Vertex AI, Anthropic API changes
- **Papers Worth Reading** — new arxiv papers on AI agents with summaries
- **Competitive Insights** — how products compare, gaps in the market
- **Recommendations** — specific opportunities for Google Cloud / Vertex AI
- All items include **hyperlinks** to sources

## Architecture

```
OpenClaw Gateway (Yujun's Mac)
├── Scout Agent (claude-cli)
│   ├── Scans ProductHunt, HN, cloud provider blogs
│   ├── Posts findings to #scout-feed
│   └── Cron: daily 8 AM CST
├── Scholar Agent (claude-cli)
│   ├── Searches arxiv, Semantic Scholar
│   ├── Posts papers to #scholar-feed
│   └── Cron: daily 8:30 AM CST
└── Analyst Agent (claude-cli)
    ├── Reads #scout-feed + #scholar-feed
    ├── Synthesizes daily briefing to #daily-briefing
    └── Cron: daily 9:30 AM CST
```

## Setup

> **Use Claude Code to set everything up.** Don't manually edit configs — open `claude` in your terminal and describe what you want. Claude Code creates files, configures OpenClaw, sets up Discord bots, and manages crons. This entire project was built by Claude Code.

See [docs/QUICK_START.md](docs/QUICK_START.md) for a 5-minute setup.

## Documentation

| Doc | Audience | What |
|-----|----------|------|
| [QUICK_START.md](docs/QUICK_START.md) | First-timer | Zero to first agent in 5 min |
| [STEP_BY_STEP_SETUP.md](docs/STEP_BY_STEP_SETUP.md) | Builder | Full setup tutorial with explanations |
| [CLAUDE_CODE_SETUP.md](docs/CLAUDE_CODE_SETUP.md) | Builder | Claude Code install + permissions |
| [DISCORD_BOT_SETUP.md](docs/DISCORD_BOT_SETUP.md) | Builder | Discord bots + OpenClaw config |
| [OPENCLAW_GUIDE.md](docs/OPENCLAW_GUIDE.md) | Team | Architecture + multi-agent communication |
| [**PATTERNS.md**](docs/PATTERNS.md) | **Engineers** | **13 production patterns (for presentations)** |
| [SECURITY.md](docs/SECURITY.md) | Ops | Identity protection + secrets |
| [RESILIENCE.md](docs/RESILIENCE.md) | Ops | Crash recovery + auto-resume |
| [DAILY_OPS.md](docs/DAILY_OPS.md) | Ops | Morning health checklist |

## Patterns (Individual Files)

16 standalone pattern files in [`patterns/`](patterns/) — one per pattern, easy to present individually.
