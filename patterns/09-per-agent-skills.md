# Pattern 9: Per-Agent Skills (Not Shared Registry)

**Problem:** Community skill registries have 5,400+ skills. Loading even 20 wastes thousands of tokens per session on irrelevant capabilities.

**Solution:** Each agent gets 2-3 custom skills in its own workspace.

| Approach | Tokens/session | When to Use |
|----------|---------------|-------------|
| Per-agent skills | Low | Default. Always. |
| Shared skills | Higher | Only if every agent needs it |
| Community registry | Very high | **Never install directly.** Browse for ideas only. |

**Rule:** Only add a skill if the agent uses it every single session. 2-3 skills per agent is ideal.
