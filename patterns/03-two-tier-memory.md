# Pattern 3: Two-Tier Memory (Official OpenClaw Architecture)

**Problem:** MEMORY.md grows over time. A 500-line MEMORY.md burns 500 lines of tokens before the agent does any work.

**Solution:** Two-tier system — daily logs (free) + curated MEMORY.md (expensive). ([Official docs](https://docs.openclaw.ai/concepts/memory))

| Tier | File | What Goes Here | Loaded |
|------|------|---------------|--------|
| Daily log | `memory/YYYY-MM-DD.md` | Everything — raw notes, findings, links | On-demand only |
| Long-term | `MEMORY.md` | Curated facts, validated patterns | **Every session** |

**Rule:** Write liberally to daily files (free). Curate MEMORY.md carefully (expensive). Keep MEMORY.md under 200 lines.

**How it works in practice:**
```
Session runs → agent writes raw findings to memory/2026-03-15.md
            → agent promotes key facts to MEMORY.md (1-2 lines)
            → commits both to git

Next session → agent loads MEMORY.md (small, curated, cheap)
            → if needed, searches daily files for historical detail
```

**Bonus:** Daily logs also serve as **debugging aid** — when an agent produces bad output, read yesterday's daily log to see exactly what it was thinking. MEMORY.md is curated (lossy), daily logs are raw (lossless).
