# Pattern 8: Claude CLI Subscription (75-90% Cost Reduction)

**Problem:** Anthropic API charges per-token. 3 agents daily = $90-240/month.

**Solution:** Use Claude Code CLI which runs on Claude Pro/Team subscription — flat $20-30/month.

| Approach | Per Run | Monthly (3 agents daily) |
|----------|---------|-------------------------|
| Anthropic API | $0.50-2.00 | **$90-240** |
| Claude CLI subscription | ~$0 | **$20-30** |

**This is the single most important cost decision.**

**Config:** `"model": { "primary": "claude-cli/claude-sonnet-4-6" }`

Always default to Sonnet. Only use Opus for tasks that specifically need deeper reasoning.
