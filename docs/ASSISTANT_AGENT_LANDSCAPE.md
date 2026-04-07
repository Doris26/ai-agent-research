# Assistant Agent Landscape — April 2026

Personal & workplace AI assistants that help individual users — not generic developer frameworks.

---

## 1. Personal AI Assistants (Always-On, For YOU)

| Product | Type | Memory | Privacy | Status |
|---|---|---|---|---|
| **OpenClaw** | Self-hosted Mac app | SOUL.md + MEMORY.md (Markdown, git-backed) | Full local | 346K⭐ [GitHub](https://github.com/openclaw/openclaw) |
| **Screenpipe** | Screen + audio capture → AI context | Records everything, local storage | Full local | 16K⭐ [GitHub](https://github.com/mediar-ai/screenpipe) |
| **Apple Intelligence** | On-device NPU + Siri | On-device personal context | Local + Private Cloud Compute | Shipping on all Apple devices |
| **Google Gemini / Astra** | Cloud multimodal assistant | Cloud-based, 1M+ token context | Cloud (Google sees data) | GA, deep Workspace integration |
| **Limitless** | Pendant + always-on audio | Meeting transcripts | Was local | Acquired by Meta (2025) |
| **Rabbit R1** | Hardware LAM device | Cloud-based | Cloud | Pivoted to software |
| **Humane AI Pin** | Wearable projector | Cloud-based | Cloud | Discontinued |

### What Makes an Assistant ≠ Chatbot

A chatbot waits for input and forgets after each conversation. An assistant:
- **Remembers** — knows your preferences, past decisions, ongoing projects
- **Acts** — sends emails, books meetings, manages files (not just suggests)
- **Proactive** — interrupts when something needs attention
- **Always available** — runs 24/7, not just when you open a tab

---

## 2. Workplace Assistant Agents

| Product | Domain | Key Capability | Integration |
|---|---|---|---|
| **Microsoft Copilot** | Office/Enterprise | Copilot Cowork = persistent agents alongside you. Agent 365 = IT governance | Word, Excel, Teams, Outlook, SharePoint |
| **Salesforce Agentforce** | CRM | Autonomous customer service, sales follow-ups, case routing | Salesforce ecosystem, Atlas reasoning engine |
| **Slack AI (Claude-powered)** | Team chat | Summarize channels, answer from workspace history, suggest actions | Slack natively, rebuilt on Claude |
| **ServiceNow AI Agents** | IT service desk | Auto-resolve tickets, provision accounts, handle requests | ServiceNow platform |
| **Notion AI Custom Agents** | Knowledge management | Workspace-aware Q&A scoped to your team's docs/databases | Notion |
| **Dust AI** | Company assistants | Connect Slack + Notion + Drive, manage data sources | 4.4K⭐ [GitHub](https://github.com/dust-tt/dust) |
| **Lindy AI** | No-code assistants | 3000+ integrations, trigger on email/calendar/CRM events | No-code builder |
| **Granola** | Meeting notes | AI meeting assistant with structured note-taking | Calendar, conferencing apps |
| **Otter.ai** | Meeting transcription | Real-time transcription + action item extraction | Zoom, Teams, Google Meet |

---

## 3. Memory Systems — How Assistants Remember You

| System | Approach | Editability | Persistence | Link |
|---|---|---|---|---|
| **OpenClaw** | SOUL.md + MEMORY.md (flat Markdown) | Human-readable, git-backed, editable | Survives restarts | [GitHub](https://github.com/openclaw/openclaw) |
| **Letta/MemGPT** | 3-tier self-editing (core/recall/archival) | Agent edits own memory autonomously | Database-backed | [GitHub](https://github.com/letta-ai/letta) |
| **Zep** | Temporal knowledge graph (facts with validity windows) | Structured, queryable, time-aware | Scores 15pts above Mem0 | [GitHub](https://github.com/getzep/zep) |
| **Mem0** | Embedding-based memory layer | API-driven | Cloud or self-hosted | [GitHub](https://github.com/mem0ai/mem0) |
| **Memsearch** | Extracted from OpenClaw's memory system | Markdown + semantic search | Standalone library | [GitHub](https://github.com/openclaw/memsearch) |
| **Apple** | On-device personal context | Opaque to user | Device-local | Proprietary |
| **Google** | Cloud conversation history + user signals | Google controls | Cloud | Proprietary |
| **AWS Bedrock** | Episodic memory in AgentCore | API-driven | Managed service | [Docs](https://aws.amazon.com/bedrock/agentcore/) |

### Memory Architecture Comparison

```
OpenClaw (file-based):
  SOUL.md (identity, ~500 tokens, auto-loaded every session)
  MEMORY.md (curated facts, auto-loaded)
  memory/YYYY-MM-DD.md (daily raw logs, read on-demand)
  → Simple, transparent, human-editable, git-versioned

Letta (database-based):
  Core Memory (always in context, agent self-edits)
  Recall Memory (conversation search, auto-retrieved)
  Archival Memory (long-term storage, vector search)
  → Sophisticated, autonomous, harder to debug

Zep (graph-based):
  Fact nodes with temporal validity
  Entity relationships
  Auto-expiration of stale facts
  → Best for accuracy over time, enterprise use
```

**The key insight:** Memory is what separates an assistant from a chatbot. Without it, every conversation starts from zero.

---

## 4. How Assistant Agents Connect to Your Stuff

### The Protocol Stack

```
┌─────────────────────────────────────────────────┐
│              YOUR ASSISTANT AGENT                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │   MCP    │  │ OAuth 2.1│  │     A2A      │ │
│  │ (tools)  │  │ (user    │  │ (other       │ │
│  │          │  │  data)   │  │  agents)     │ │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘ │
│       │              │               │         │
├───────┼──────────────┼───────────────┼─────────┤
│       ▼              ▼               ▼         │
│  Files, DBs,    Calendar,      Vendor's        │
│  APIs, Code     Email, Drive   Assistant       │
│  Interpreters   Slack, CRM     Agents          │
└─────────────────────────────────────────────────┘
```

| Protocol | What It Connects | Standard | Status |
|---|---|---|---|
| **MCP** (Anthropic → Linux Foundation) | Agent ↔ Tools (files, databases, APIs) | [Spec](https://modelcontextprotocol.io/specification/2025-11-25) | Standard. 97M+ monthly SDK downloads |
| **OAuth 2.1** | Agent ↔ User's data (calendar, email, drive) | RFC standard | Mature. MCP added OAuth mid-2025 |
| **A2A** (Google → Linux Foundation) | Agent ↔ Other agents | [GitHub](https://github.com/a2aproject/A2A) | Draft. GA planned 2026. 150+ orgs |
| **AG-UI** (CopilotKit) | Agent ↔ Web frontend UI | [GitHub](https://github.com/ag-ui-protocol/ag-ui) | Active. Adopted by Microsoft, Google, AWS |
| **Computer Use** (Anthropic) | Agent ↔ Screen/mouse/keyboard | Anthropic API | Available in Claude |

### How OpenClaw Connects

```
OpenClaw Gateway (localhost:18789)
├── Discord WebSocket ──→ Sage, Forge, Scout (messaging)
├── Claude CLI ──→ LLM reasoning (via OAuth or Bedrock)
├── MCP servers ──→ Tools (file access, web search, etc.)
├── Cron scheduler ──→ Periodic agent wake-ups
└── Heartbeat ──→ Proactive monitoring
```

### Credential Management

| Solution | What It Does |
|---|---|
| **Auth0 Token Vault** | Manages OAuth tokens across services for your agent |
| **Composio** | 1000+ tool integrations with managed OAuth. [GitHub](https://github.com/ComposioHQ/composio) |
| **MCP OAuth** | Built-in OAuth flow added to MCP spec (mid-2025) |

---

## 5. Assistant Agent Runtimes

### How They Stay "Always On"

| Runtime | Architecture | Cost Model | Example |
|---|---|---|---|
| **Local daemon** | Process on your Mac/PC, always running | Electricity only | OpenClaw gateway |
| **On-device NPU** | Neural engine on phone/laptop | Free (built into hardware) | Apple Intelligence |
| **Cloud API** | Calls to Claude/GPT/Gemini per request | Pay per token | Most chatbot assistants |
| **Cron + heartbeat** | Sleeps, wakes periodically to check | Tokens only when active | OpenClaw's approach |
| **Event-driven** | Wakes on trigger (email, calendar, @mention) | Tokens only when triggered | Slack AI, Agentforce |

### OpenClaw's Runtime Model

```
Gateway (always running, ~50MB RAM):
  └── WebSocket to Discord (persistent, free)
  └── Cron scheduler (fires agents on schedule)
  └── Heartbeat (checks every 30 min)

Agent sessions (ephemeral, spawn on demand):
  └── Claude CLI subprocess
  └── Runs for 1-10 minutes
  └── Uses tools, posts to Discord
  └── Dies, context gone
  └── Memory survives in .md files
```

---

## 6. Privacy & Security Spectrum

```
FULL LOCAL ──────────────────────────────────────── FULL CLOUD
    │                    │                    │            │
OpenClaw+Ollama    Apple Private       OpenClaw+Claude    Google Gemini
(nothing leaves    Cloud Compute       (API calls to      (Google processes
 your machine)     (encrypted cloud    Anthropic, they    everything in
                    processing,        see prompts)       their cloud)
                    Apple can't see)
```

| Approach | Data Stays Local? | Model Runs Local? | Who Sees Your Data? |
|---|---|---|---|
| OpenClaw + Ollama | ✅ | ✅ | Nobody |
| OpenClaw + Claude API | ❌ (API calls) | ❌ | Anthropic (with privacy policy) |
| Apple Intelligence | ✅ (mostly) | ✅ (NPU) | Apple (Private Cloud Compute only) |
| Google Gemini | ❌ | ❌ | Google |
| Microsoft Copilot | ❌ | ❌ | Microsoft (enterprise data boundaries) |

---

## 7. Unsolved Problems (The Gaps)

### 1. Always-On Cost
90% of CIOs cite cost as the #1 barrier. Running Claude 24/7 for proactive monitoring is expensive.
**Current mitigation:** Cron schedules (check every 30min/4h, not continuously). But this means delayed responses.

### 2. Proactive vs Reactive
Most assistants wait for you to ask. A true assistant should interrupt: "Your flight is delayed, I rebooked." Very few do this well.
**Who's trying:** Apple (Siri proactive suggestions), OpenClaw (heartbeat checks), Google (Gemini notifications).
**The gap:** Nobody has solved "know WHEN to interrupt vs when to stay quiet."

### 3. Trust & Delegation
Users don't trust agents to send emails or book meetings autonomously. The UX challenge: how much autonomy to grant?
**Approaches:**
- OpenClaw: "Ask first for external actions, act freely for internal" (AGENTS.md rules)
- Microsoft: Agent 365 governance (IT admin controls what agents can do)
- Anthropic: Constitutional AI constraints baked into the model

### 4. Memory Staleness
Agent remembers you like coffee at 9am but you changed jobs 3 months ago. No good solution for memory decay/update.
**Best current approach:** Zep's temporal knowledge graph (facts have expiration dates). OpenClaw relies on human to update MEMORY.md.

### 5. Context Window Limits
Even 1M tokens can't hold a year of emails. RAG helps but adds latency and misses nuance.
**Trend:** Context windows growing (1M → 2M → eventually unlimited?). But cost scales with context size.

### 6. Integration Fragmentation
Despite MCP, most apps still need custom connectors. The "universal assistant" that works with EVERYTHING doesn't exist yet.
**MCP helps but:** Only 8M server downloads. Most enterprise apps don't have MCP servers yet.

### 7. Multi-Device Continuity
Start a task on phone, continue on laptop, finish on desktop. Only Apple has this somewhat solved (Handoff/Continuity).
**OpenClaw limitation:** Runs on one Mac. No cross-device sync built in. Tailscale SSH is a workaround, not a solution.

---

## 8. The Opportunity Map

```
                    SOLVED ──────────────────── UNSOLVED
                    │                              │
Tool Access (MCP)   ████████████████               │
Memory (basic)      ███████████████                │
Messaging Channels  ████████████████               │
                    │                              │
Memory (temporal)   ████████                       │
Proactive Actions   ████                           │
Trust/Delegation    ████                           │
Multi-device        ███                            │
Universal Integr.   ██                             │
Always-on (cheap)   ██                             │
```

**Where to build:**
- Proactive + Trust = the assistant that interrupts smartly and users actually trust
- Temporal Memory = the assistant that knows what's CURRENTLY true, not what WAS true
- Cross-device = the assistant that follows you everywhere

---

## 9. GitHub Repos Worth Following

| Repo | Stars | What | Link |
|---|---|---|---|
| openclaw/openclaw | 346K | Self-hosted personal AI | [GitHub](https://github.com/openclaw/openclaw) |
| mediar-ai/screenpipe | 16K | Always-on screen/audio capture | [GitHub](https://github.com/mediar-ai/screenpipe) |
| letta-ai/letta | 13K | Memory-first agents (MemGPT) | [GitHub](https://github.com/letta-ai/letta) |
| getzep/zep | 3K+ | Temporal memory for agents | [GitHub](https://github.com/getzep/zep) |
| dust-tt/dust | 4.4K | Company assistant platform | [GitHub](https://github.com/dust-tt/dust) |
| mem0ai/mem0 | 25K+ | Memory layer for AI | [GitHub](https://github.com/mem0ai/mem0) |
| ComposioHQ/composio | 15K+ | 1000+ tool integrations | [GitHub](https://github.com/ComposioHQ/composio) |
| modelcontextprotocol | — | MCP spec + SDKs | [GitHub](https://github.com/modelcontextprotocol) |
| a2aproject/A2A | — | Agent-to-Agent protocol | [GitHub](https://github.com/a2aproject/A2A) |

---

## 10. Key Papers

| Paper | Topic | Link |
|---|---|---|
| MAS Orchestration: Architectures, Protocols, Enterprise | Multi-agent system design | [arXiv:2601.13671](https://arxiv.org/abs/2601.13671) |
| A Call for Collaborative Intelligence (Zou et al.) | Human-Agent collaborative systems | [arXiv:2506.09420](https://arxiv.org/abs/2506.09420) |
| Building Effective AI Coding Agents for the Terminal | Agent runtime, tool dispatch, context mgmt | [arXiv:2603.05344](https://arxiv.org/abs/2603.05344) |
| Open Agent Specification (Oracle) | Declarative agent definition format | [arXiv:2510.04173](https://arxiv.org/abs/2510.04173) |

---

*Last updated: 2026-04-07. Sources: GitHub, product docs, arXiv, web research.*
