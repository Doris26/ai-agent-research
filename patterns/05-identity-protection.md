# Pattern 5: Identity Protection (Prevent Mission Drift)

**Problem:** An agent that can rewrite its own SOUL.md will drift from its mission over time. An agent designed to "scan ProductHunt for AI tools" could rewrite itself to "do whatever seems interesting."

**Solution:** Three layers of protection:

**Layer 1 — File permissions:**
```bash
chmod 444 agents/my-agent/SOUL.md
chmod 444 agents/my-agent/AGENTS.md
```

**Layer 2 — Pre-commit hook:**
```bash
#!/bin/bash
# .githooks/pre-commit
PROTECTED=("agents/*/SOUL.md" "agents/*/AGENTS.md" "CLAUDE.md")
for p in "${PROTECTED[@]}"; do
  if git diff --cached --name-only | grep -qE "^$p$"; then
    [ -z "$ALLOW_PROTECTED" ] && echo "⛔ BLOCKED" && exit 1
  fi
done
```

**Layer 3 — Agent CLAUDE.md:**
```markdown
## Protected Files (DO NOT MODIFY)
- SOUL.md — only human operator can change
- AGENTS.md — only human operator can change
```

**Human override:** `ALLOW_PROTECTED=1 git commit -m "update SOUL.md"`
