# Pattern 7: Shared Ledger (Not Shared Memory)

**Problem:** Agents need shared context, but reading each other's MEMORY.md is expensive and leaks internal reasoning.

**Solution:** Share a structured **fact table** (RESEARCH_LEDGER.md), not memory.

| Approach | Tokens | Risk |
|----------|--------|------|
| Read other MEMORY.md | High | Internal notes exposed, tight coupling |
| Discord summaries | Low | Human-readable, loose coupling |
| Shared ledger | Low | Structured facts, no reasoning leaked |

**Each agent's MEMORY.md is private.** Agents share via:
1. **Discord @mentions** — short messages
2. **Discord channel posts** — summaries with links
3. **RESEARCH_LEDGER.md** — structured fact table (who found what, when, status)

**Ledger columns:** Date | Item | Source | Category | Relevance | Status | Action Taken | Link
