# OpenClaw: Multi-Agent AI Orchestration — A Practical Guide

**TL;DR:** OpenClaw is an open-source multi-agent AI gateway that lets you run autonomous AI agents on a schedule, communicate via Discord, and persist knowledge via git — all for ~$20-30/month instead of $90-240/month on API tokens. This repo demonstrates a production system with 3 agents that daily scan the AI agent ecosystem and deliver a synthesized briefing.

> This summary is intended for Googlers who want to understand and experiment with autonomous multi-agent orchestration using OpenClaw + Claude Code CLI.

---

## What is OpenClaw?

OpenClaw is a Node.js gateway that orchestrates autonomous AI agents. It provides cron scheduling, Discord integration, isolated sessions, and support for multiple AI backends (Claude CLI, Gemini, GPT). Think of it as a lightweight "agent runtime" you run on your laptop or a VM.

**Core idea:** Instead of one monolithic agent, you split work across specialized agents that communicate through Discord channels — like a team of humans with Slack. This architecture cuts token costs by 50-80% because agents exchange short summaries instead of passing full context chains.

- [Full OpenClaw Architecture Guide](https://github.com/Doris26/ai-agent-research/blob/main/docs/OPENCLAW_GUIDE.md)
- [Quick Start (5 minutes)](https://github.com/Doris26/ai-agent-research/blob/main/docs/QUICK_START.md)
- [Step-by-Step Setup Tutorial](https://github.com/Doris26/ai-agent-research/blob/main/docs/STEP_BY_STEP_SETUP.md)

---

## How This System Works

This repo runs **3 autonomous agents** on a daily cron schedule:

| Agent | Role | Schedule (CST) | Discord Channel |
|-------|------|-----------------|-----------------|
| **Scout** | Scans ProductHunt, HN, cloud provider blogs for AI agent products/updates | 8:00 AM | #scout-feed |
| **Scholar** | Searches arXiv, Semantic Scholar, conference proceedings for AI agent papers | 8:30 AM | #scholar-feed |
| **Analyst** | Reads Scout + Scholar feeds, produces a daily competitive briefing | 9:30 AM | #daily-briefing |

Agents share structured facts via a [Research Ledger](https://github.com/Doris26/ai-agent-research/blob/main/RESEARCH_LEDGER.md) (a markdown table all agents append to). Each agent has its own identity file (`SOUL.md`), memory (`MEMORY.md`), and workspace.

- [Scout SOUL.md](https://github.com/Doris26/ai-agent-research/blob/main/agents/scout/SOUL.md)
- [Scholar SOUL.md](https://github.com/Doris26/ai-agent-research/blob/main/agents/scholar/SOUL.md)
- [Analyst SOUL.md](https://github.com/Doris26/ai-agent-research/blob/main/agents/analyst/SOUL.md)
- [Project README](https://github.com/Doris26/ai-agent-research/blob/main/README.md)

---

## 14 Production Patterns

The repo documents 14 battle-tested patterns for running autonomous multi-agent systems. Each pattern addresses a real problem encountered in production.

### Communication & Cost

**Discord as Agent Bus** — Instead of piping full context between agents (500K tokens/day, $90-240/month), agents post summaries to Discord channels and other agents read them via the free Discord API. This yields 50-80% token savings. Each agent gets its own Discord bot for identity and audit trail.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/01-discord-agent-bus.md)

**Claude CLI Subscription Savings** — Using Claude Code CLI on a Pro/Team subscription ($20-30/month flat) instead of per-token API billing is the single biggest cost lever. Config uses `claude-cli/claude-sonnet-4-6` as the model backend.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/08-cli-subscription-savings.md)

**Per-Agent Skills** — Each agent gets only 2-3 custom skills it actually uses, rather than loading from a massive shared registry. This keeps token overhead minimal per session.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/09-per-agent-skills.md)

### Agent Identity & Design

**SOUL.md Design** — An agent's `SOUL.md` is its job description: mission, sources (with URLs), output format (with template), team @mentions, channel IDs, and rules. Spending 80% of design time here determines 80% of output quality. The litmus test: "Would a new hire know exactly what to do from this file alone?"
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/02-soul-md-design.md)

**Identity Protection** — Agents that can rewrite their own SOUL.md will drift from their mission. Three layers prevent this: `chmod 444` on identity files, a pre-commit hook blocking changes, and explicit rules in `CLAUDE.md`.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/05-identity-protection.md)

**USER.md Tailoring** — A `USER.md` file tells the agent who's reading the output (role, expertise, preferences), so it can tailor tone and content. For example: "Be technical, skip marketing fluff, compare to Vertex AI."
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/11-user-md-tailoring.md)

### Memory & Knowledge

**Two-Tier Memory** — Daily raw notes go to `memory/YYYY-MM-DD.md` (cheap, loaded on-demand). Only curated, durable facts get promoted to `MEMORY.md` (expensive, auto-loaded every session). Keep `MEMORY.md` under 200 lines. This prevents unbounded token growth.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/03-two-tier-memory.md)

**Auto Skill Evolution** — Agents update `MEMORY.md` after each session and commit to git. Over time they accumulate knowledge — e.g., "EMA/SMA broken in downtrend, avoid." Identity files stay protected; only knowledge evolves.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/04-auto-skill-evolution.md)

**Shared Ledger** — Agents share structured facts via a shared `RESEARCH_LEDGER.md` table, not by reading each other's private MEMORY.md. This keeps communication cheap and avoids leaking internal reasoning.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/07-shared-ledger.md)

**Agent Communication & Memory Architecture** — A comprehensive breakdown of what each agent "sees" (4 auto-loaded sources + 4 on-demand sources), how inter-agent communication flows through Discord, and the full information lifecycle.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/14-agent-communication-and-memory.md)

### Safety & Reliability

**No-Recursion Guard** — Without explicit rules, Agent A can trigger Agent B, whose output triggers A again — infinite loop. Each SOUL.md includes a no-recursion matrix: downstream agents never spawn upstream agents.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/06-no-recursion-guard.md)

**PUA Anti-Laziness** — AI agents exhibit 5 lazy patterns (brute-force retry, blame user, idle tools, busywork, passive waiting). The PUA skill uses escalating pressure to force exhaustive problem-solving. Best for complex debugging/research tasks; skip for simple scan-and-report agents.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/10-pua-anti-laziness.md)

**Staggered Cron Scheduling** — Multiple agents firing simultaneously compete for CPU/memory and create git push conflicts. Stagger with 15-30 min gaps and ensure downstream agents run after upstream ones.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/12-staggered-crons.md)

**Resume & Resilience** — Three layers of auto-recovery: (1) overdue cron catch-up on gateway restart, (2) agent reads MEMORY.md to resume from last known state, (3) Discord channel history as external state. Zero in-memory state — everything persists to git or Discord.
[Pattern Details](https://github.com/Doris26/ai-agent-research/blob/main/patterns/13-resume-and-resilience.md)

- [Full Pattern Index](https://github.com/Doris26/ai-agent-research/blob/main/docs/PATTERNS.md)

---

## Operations & Security

**Daily health check takes 30 seconds:** run `gateway status`, check `cron list`, glance at Discord, check `git log`. The repo includes a full operational runbook covering weekly reviews, memory pruning, and OpenClaw updates.

Security follows defense-in-depth: identity files are read-only (`chmod 444`), API keys live in `~/.openclaw/secrets/` (or GCP Secret Manager in production), pre-commit hooks block protected file changes, and Discord bots use scoped permissions.

- [Daily Operations Runbook](https://github.com/Doris26/ai-agent-research/blob/main/docs/DAILY_OPS.md)
- [Resilience & Failure Recovery](https://github.com/Doris26/ai-agent-research/blob/main/docs/RESILIENCE.md)
- [Security Guide](https://github.com/Doris26/ai-agent-research/blob/main/docs/SECURITY.md)
- [Claude Code CLI Setup](https://github.com/Doris26/ai-agent-research/blob/main/docs/CLAUDE_CODE_SETUP.md)
- [Discord Bot Setup](https://github.com/Doris26/ai-agent-research/blob/main/docs/DISCORD_BOT_SETUP.md)

---

## Agent Workspace Structure

Every OpenClaw agent follows this standard layout:

```
my-agent/
├── SOUL.md              # Identity & mission (protected, read-only)
├── MEMORY.md            # Curated knowledge (auto-loaded every session)
├── CLAUDE.md            # Rules & constraints (protected)
├── USER.md              # Who reads the output (auto-loaded)
├── AGENTS.md            # Available skills & tools (protected)
├── memory/
│   └── YYYY-MM-DD.md    # Daily raw notes (loaded on-demand)
├── skills/
│   └── skill-name/SKILL.md
└── .claude/
    └── settings.json    # bypassPermissions for autonomous runs
```

---

## Cost Comparison

| Approach | Monthly Cost | Why |
|----------|-------------|-----|
| Per-token API (piped context) | $90-240 | 500K+ tokens/day across 3 agents |
| Claude CLI + Discord summaries | **$20-30** | Flat subscription + 70% fewer tokens via summaries |

---

## Getting Started

1. **Clone this repo** — `gh repo clone Doris26/ai-agent-research`
2. **Read the [Quick Start](https://github.com/Doris26/ai-agent-research/blob/main/docs/QUICK_START.md)** — 5-minute setup
3. **Study the [SOUL.md files](https://github.com/Doris26/ai-agent-research/tree/main/agents)** — see how agent identities are designed
4. **Browse the [14 patterns](https://github.com/Doris26/ai-agent-research/tree/main/patterns)** — pick what's relevant to your use case
5. **Customize** — swap out agents for your own research domain

---

## Key Takeaways for Googlers

- **Multi-agent > monolithic:** Splitting work across specialized agents with Discord-based communication cuts costs dramatically and improves output quality.
- **SOUL.md is everything:** Agent identity design is the highest-leverage activity. Be specific about mission, sources, output format, and constraints.
- **Memory must be tiered:** Auto-loading everything is a token trap. Use cheap daily logs + curated long-term memory.
- **Protect identity, evolve knowledge:** Lock down who the agent *is*; let it freely update what it *knows*.
- **Resilience = no in-memory state:** Everything important lives in git or Discord. Crashes are non-events.
- **Claude CLI subscription is the cost unlock:** Per-token billing kills multi-agent economics; flat-rate subscription makes it viable.

---

*Source: [Doris26/ai-agent-research](https://github.com/Doris26/ai-agent-research)*
