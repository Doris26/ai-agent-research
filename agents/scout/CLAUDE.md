# Agent Rules

## Memory Management (Official OpenClaw Pattern)
- **Daily log:** Write everything to `memory/YYYY-MM-DD.md` — raw notes, findings, links, messy context. Be liberal.
- **MEMORY.md:** Curated, durable knowledge only — key findings, recurring sources, validated patterns. Keep under 200 lines.
- **Weekly:** Promote important daily log entries to MEMORY.md. Prune old/outdated entries.
- **Why:** MEMORY.md is loaded every session (costs tokens). Daily files are only loaded on-demand. Keeping MEMORY.md small = cheaper sessions.

## Git Rules
- Always commit and push after modifying files
- Never force push
- Use descriptive commit messages
