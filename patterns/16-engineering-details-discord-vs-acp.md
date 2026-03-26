# Pattern 16: Engineering Deep Dive — Discord @mention vs ACP Spawn

What actually happens inside the system when agents communicate. Step-by-step, with context windows, token flow, and session mechanics.

---

## Discord @mention — What's In The Context

### Step-by-Step Execution

```
1. Sage posts to #yujun-team:
   "@Forge backtest S50 ADX+OBV, 1Y window, report Calmar"

2. Discord delivers message to OpenClaw gateway
   (gateway is connected to Discord via WebSocket)

3. Gateway sees @Forge mention → routes to Forge agent

4. Gateway creates NEW isolated session for Forge:
   session key: agent:forge:discord:uuid

5. Forge's session context is loaded:
   ┌─────────────────────────────────────────────┐
   │ SYSTEM CONTEXT (auto-injected by OpenClaw): │
   │  - SOUL.md contents        (~500 tokens)    │
   │  - AGENTS.md contents      (~800 tokens)    │
   │  - USER.md contents        (~200 tokens)    │
   │  - MEMORY.md contents      (~400 tokens)    │
   │  Total auto-loaded: ~1,900 tokens           │
   ├─────────────────────────────────────────────┤
   │ USER MESSAGE (the Discord message):         │
   │  "@Forge backtest S50 ADX+OBV, 1Y window,  │
   │   report Calmar"                            │
   │  + metadata: channel=#yujun-team,           │
   │    author=sage, timestamp=...               │
   │  Total: ~50 tokens                          │
   ├─────────────────────────────────────────────┤
   │ Forge sees: ~1,950 tokens of context        │
   │ Forge does NOT see:                         │
   │  ✗ Sage's reasoning/thinking                │
   │  ✗ Previous Discord messages (must read)    │
   │  ✗ Other agents' MEMORY.md                  │
   │  ✗ GOLDEN_SHEET.md (must read on-demand)    │
   └─────────────────────────────────────────────┘

6. Forge starts executing:
   - Reads GOLDEN_SHEET.md (on-demand, +2,000 tokens)
   - Reads Discord channel for context (FREE API call)
   - Writes backtest script
   - Runs backtest
   - Posts results to #yujun-team via Discord API

7. Session ends. Context is discarded.
```

### Key Engineering Facts — Discord @mention

```
Session isolation:     ✅ Forge gets a FRESH session (no Sage context)
Sage's thinking:       ❌ NOT passed to Forge (only the Discord message)
Context window start:  SOUL.md + AGENTS.md + USER.md + MEMORY.md + the message
Additional context:    Forge must actively READ files/Discord to know more
Token cost (Forge):    ~1,950 (auto) + ~50 (message) + whatever Forge reads
Token cost (Sage):     ~50 (posting the Discord message)
Total:                 ~2,000 input tokens for Forge to start
Sage blocks?:          NO — Sage's session already ended
```

### Sequence Diagram

```
Sage Session              Discord              OpenClaw Gateway         Forge Session
     │                       │                       │                       │
     │──POST message────────→│                       │                       │
     │  "@Forge backtest.."  │                       │                       │
     │                       │──WebSocket event──────→│                       │
     │  (session ends)       │                       │──creates session──────→│
     │                       │                       │  inject SOUL+MEMORY    │
     │                       │                       │  inject Discord msg    │
     │                       │                       │                       │
     │                       │                       │              Forge works...
     │                       │                       │              reads files
     │                       │                       │              runs backtest
     │                       │                       │                       │
     │                       │←─────POST results─────│←──────────results─────│
     │                       │  "S50: Calmar 4.2"    │                       │
     │                       │                       │              (session ends)

Timeline: Sage post ──[minutes/hours gap]──→ Forge starts ──[work]──→ Forge posts
```

---

## ACP Spawn — What's In The Context

### Step-by-Step Execution

```
1. Sage is running in its session. Sage calls:
   sessions_spawn({
     task: "Backtest S50 ADX+OBV, 1Y window, report Calmar",
     agentId: "forge",
     mode: "run"        // oneshot
   })

2. Gateway creates CHILD session for Forge:
   session key: agent:forge:acp:uuid
   parent:      agent:sage:cron:uuid
   spawnDepth:  1

3. Forge's session context is loaded:
   ┌─────────────────────────────────────────────┐
   │ SYSTEM CONTEXT (auto-injected by OpenClaw): │
   │  - SOUL.md contents        (~500 tokens)    │
   │  - AGENTS.md contents      (~800 tokens)    │
   │  - USER.md contents        (~200 tokens)    │
   │  - MEMORY.md contents      (~400 tokens)    │
   │  Total auto-loaded: ~1,900 tokens           │
   ├─────────────────────────────────────────────┤
   │ TASK MESSAGE (from parent, NOT Discord):    │
   │  "Backtest S50 ADX+OBV, 1Y window,         │
   │   report Calmar"                            │
   │  + ACP metadata: parent=sage:cron:uuid,     │
   │    mode=run, spawnDepth=1                   │
   │  Total: ~50 tokens                          │
   ├─────────────────────────────────────────────┤
   │ Forge sees: ~1,950 tokens (SAME as Discord) │
   │ Forge does NOT see:                         │
   │  ✗ Sage's full context/reasoning            │
   │  ✗ Sage's MEMORY.md                         │
   │  ✗ What Sage read before spawning           │
   │  ✗ Other messages in Sage's session         │
   └─────────────────────────────────────────────┘

4. Forge executes (same as Discord path):
   - Reads files on-demand
   - Runs backtest
   - Returns result

5. KEY DIFFERENCE: Result goes BACK TO SAGE, not to Discord.
   Sage's session RESUMES with Forge's output in context.

   ┌─────────────────────────────────────────────┐
   │ Sage's context after Forge returns:         │
   │  - Everything Sage had before spawn         │
   │  - + Forge's result (injected)              │
   │  - Sage continues working with this result  │
   └─────────────────────────────────────────────┘

6. Sage can now use the result immediately:
   "Forge says Calmar 4.2 → promote to Tier 1"
   Posts summary to Discord.
```

### Key Engineering Facts — ACP Spawn

```
Session isolation:     ✅ Forge gets a FRESH session (no Sage context)
Sage's thinking:       ❌ NOT passed to Forge (only the task message)
Context window start:  SOUL.md + AGENTS.md + USER.md + MEMORY.md + task
Additional context:    Forge must actively READ files to know more
Token cost (Forge):    ~1,950 (auto) + ~50 (task) + whatever Forge reads
Token cost (Sage):     Sage PAUSED during Forge execution (0 tokens while waiting)
                       + Forge's result added to Sage's context when it resumes
Total:                 ~2,000 input for Forge + result tokens added to Sage
Sage blocks?:          YES — Sage waits for Forge to finish, then continues
```

### Sequence Diagram

```
Sage Session                    OpenClaw Gateway              Forge Session
     │                                │                            │
     │──sessions_spawn(forge, task)──→│                            │
     │                                │──creates child session────→│
     │  (BLOCKED — waiting)           │  inject SOUL+MEMORY        │
     │                                │  inject task message       │
     │                                │                            │
     │                                │                   Forge works...
     │                                │                   reads files
     │                                │                   runs backtest
     │                                │                            │
     │←───────result injected─────────│←────────result─────────────│
     │  "Calmar 4.2, 12 trades,      │                   (session ends)
     │   MaxDD 8.1%"                  │
     │                                │
     │  Sage CONTINUES with result
     │  in its context window
     │  "Promote to Tier 1..."
     │

Timeline: Sage spawns ──[Forge works]──→ Sage resumes (NO gap)
```

---

## The Critical Difference: Context After Communication

### Discord @mention
```
Sage's context:  [gone — session ended before Forge started]
Forge's context: SOUL + MEMORY + Discord message (50 tokens from Sage)
Result:          Forge posts to Discord. Sage sees it NEXT SESSION.

Sage CANNOT continue working based on Forge's result.
```

### ACP Spawn
```
Sage's context:  [preserved — paused while Forge ran]
Forge's context: SOUL + MEMORY + task message (50 tokens from Sage)
Result:          Injected into Sage's LIVE context. Sage continues immediately.

Sage CAN continue working based on Forge's result.
```

### File-Based (for comparison)
```
Sage's context:  [gone — session ended]
Forge's context: [gone — session ended]
Result:          Written to GOLDEN_SHEET.md. Next agent reads it on next wake.

Nobody continues. Next cron session picks it up.
```

---

## Side-by-Side Summary

| Aspect | Discord @mention | ACP Spawn |
|--------|-----------------|-----------|
| **Forge's input context** | SOUL+MEMORY+Discord msg | SOUL+MEMORY+task msg |
| **Forge sees Sage's reasoning?** | No | No |
| **Forge's context size** | ~2,000 tokens | ~2,000 tokens |
| **Where result goes** | Discord channel (public) | Back to Sage's session (private) |
| **Sage can use result?** | Not in same session | Yes, immediately |
| **Sage's session state** | Ended before Forge starts | Paused, resumes after |
| **Human visibility** | Full (Discord messages) | None (unless `thread: true`) |
| **Time gap** | Minutes to hours | Seconds to minutes |
| **Total token cost** | Lower (no result injection) | Higher (result added to Sage context) |
| **Multi-step chains** | Hard (need multiple cron cycles) | Easy (spawn → result → spawn → result) |

---

## When ACP Spawn Wins

```
Sage needs to:
  1. Research strategy → 2. Spawn Forge to backtest → 3. Evaluate result → 4. Decide next step

With Discord: 4 separate sessions, 4 cron cycles, hours of wall time
With ACP:     1 session, 4 steps, minutes of wall time
```

## When Discord @mention Wins

```
Sage proposes strategy. Forge should backtest it.
But Sage doesn't need the result right now.
Human wants to see the conversation.

Discord: Sage posts proposal, Forge sees it whenever, posts results.
         Human follows along in #yujun-team. Cheap. Auditable.
ACP:     Overkill. Sage burns tokens waiting. Human sees nothing.
```

---

## Engineering Gotchas

1. **ACP spawn does NOT pass parent's full context** — child gets a fresh session with only SOUL+MEMORY+task. If Forge needs to know what Sage discovered, Sage must include it in the task message.

2. **Discord @mention does NOT guarantee order** — if Sage @mentions Forge twice quickly, Forge might get two overlapping sessions.

3. **ACP thread mode creates VISIBLE threads** — useful for debugging but clutters Discord with `🤖 forge` threads.

4. **File-based is the only protocol that survives gateway restarts** — Discord messages persist in Discord, but ACP sessions are lost if gateway crashes mid-execution.

5. **Discord API rate limit: 5 messages/5 seconds per channel** — agents that post too fast get throttled.

6. **ACP max spawn depth: 5** — prevents A spawns B spawns C spawns D loops. Configurable but keep it low.
