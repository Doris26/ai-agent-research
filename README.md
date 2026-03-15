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

See [docs/QUICK_START.md](docs/QUICK_START.md) for a 5-minute setup, or [docs/SETUP.md](docs/SETUP.md) for the full guide.

## Team Guide

See [docs/OPENCLAW_GUIDE.md](docs/OPENCLAW_GUIDE.md) for how to use OpenClaw for AI research workflows.
