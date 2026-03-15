# Pattern 11: USER.md (Tailored Output)

**Problem:** Agents produce generic output unless they know who is reading it.

**Solution:** `USER.md` in each workspace tells the agent your role, expertise, and preferences.

```markdown
# User: Yujun
**Role:** SWE at Google Cloud AI team
**Focus:** Agent runtime and infrastructure

## How to Tailor Output
- Be technical — skip marketing fluff
- Compare to Google Cloud / Vertex AI
- Highlight runtime details — memory, orchestration, scaling
- Include code snippets when relevant
```

Place in each agent workspace. OpenClaw injects it into session context automatically.
