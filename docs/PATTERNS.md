# Multi-Agent AI Patterns — OpenClaw Production Playbook

14 patterns from running autonomous AI agents 24/7 in production. Each pattern is a standalone file in the `patterns/` folder.

| # | Pattern | Key Benefit | File |
|---|---------|-------------|------|
| 1 | [Discord as Agent Bus](../patterns/01-discord-agent-bus.md) | 50-80% token savings | `01-discord-agent-bus.md` |
| 2 | [SOUL.md Design](../patterns/02-soul-md-design.md) | 80% of agent quality | `02-soul-md-design.md` |
| 3 | [Two-Tier Memory](../patterns/03-two-tier-memory.md) | Prevents memory bloat | `03-two-tier-memory.md` |
| 4 | [Auto Skill Evolution](../patterns/04-auto-skill-evolution.md) | Agents learn over time | `04-auto-skill-evolution.md` |
| 5 | [Identity Protection](../patterns/05-identity-protection.md) | Prevents mission drift | `05-identity-protection.md` |
| 6 | [No-Recursion Guard](../patterns/06-no-recursion-guard.md) | Prevents infinite loops | `06-no-recursion-guard.md` |
| 7 | [Shared Ledger](../patterns/07-shared-ledger.md) | Facts without leaking memory | `07-shared-ledger.md` |
| 8 | [CLI Subscription](../patterns/08-cli-subscription-savings.md) | 75-90% cost reduction | `08-cli-subscription-savings.md` |
| 9 | [Per-Agent Skills](../patterns/09-per-agent-skills.md) | Minimal token overhead | `09-per-agent-skills.md` |
| 10 | [PUA Skill](../patterns/10-pua-anti-laziness.md) | Prevents agent laziness | `10-pua-anti-laziness.md` |
| 11 | [USER.md](../patterns/11-user-md-tailoring.md) | Tailored output | `11-user-md-tailoring.md` |
| 12 | [Staggered Crons](../patterns/12-staggered-crons.md) | Prevents conflicts | `12-staggered-crons.md` |
| 13 | [Resilience](../patterns/13-resilience.md) | Auto-recovery from failures | `13-resilience.md` |
| 14 | [Agent Communication](../patterns/14-agent-communication-and-memory.md) | 3 protocols: Discord Bus + ACP Spawn + File-Based | `14-agent-communication-and-memory.md` |

*Built with [OpenClaw](https://openclaw.ai) + [Claude Code](https://claude.ai/claude-code). All patterns validated in production with 8 agents across 2 projects.*
