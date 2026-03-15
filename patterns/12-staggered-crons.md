# Pattern 12: Staggered Cron Scheduling

**Problem:** Multiple agents firing simultaneously compete for resources and conflict on git pushes.

**Solution:** Stagger crons with 15-30 minute gaps. Downstream agents run after upstream.

```
8:00 AM  → Scout (scan products)
8:30 AM  → Scholar (scan papers)
9:30 AM  → Analyst (read Scout + Scholar → synthesize)
10:00 AM → All agents commit to git
```

**Why gaps matter:**
- Prevents CPU/memory contention
- Ensures upstream data is ready before downstream reads
- Avoids git push conflicts (15 min gap between commits)
