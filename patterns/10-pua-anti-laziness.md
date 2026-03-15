# Pattern 10: PUA Skill (Anti-Laziness for Complex Agents)

**Problem:** Agents have 5 lazy patterns — brute-force retry, blame user, idle tools, busywork, passive waiting.

**Solution:** [PUA skill](https://github.com/tanweai/pua) (7.3K stars) uses escalating pressure to force exhaustive problem-solving.

**When to use:** Complex problem-solving agents (debugging, research, backtesting).
**When NOT to use:** Simple scan/report agents — adds ~300 lines to context.

**Install:**
```bash
mkdir -p agents/my-agent/skills/pua
curl -s "https://raw.githubusercontent.com/tanweai/pua/main/skills/pua-en/SKILL.md" \
  -o agents/my-agent/skills/pua/SKILL.md
```
