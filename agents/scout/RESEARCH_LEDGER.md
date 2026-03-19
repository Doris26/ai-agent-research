# Research Ledger

## 2026-03-19 — Daily Scan

### Cloud Provider Updates
| Provider | Update | GCP Equivalent? | Gap? |
|----------|--------|-----------------|------|
| GCP | Vertex AI Agent Engine Code Execution — NOW GA | N/A (native) | GCP STRENGTH — was Preview, now GA |
| GCP | Vertex AI Agent Engine Sessions & Memory Bank — NOW GA | N/A (native) | GCP STRENGTH |
| GCP | Gemini 3.1 Flash-Lite public preview — cost-efficient, low-latency | N/A (native) | GCP STRENGTH |
| GCP | GLM 5 experimental in Model Garden — complex agentic tasks | N/A (native) | GCP STRENGTH |
| GCP | Image generation endpoints deprecated — migrate by March 19 | N/A | ACTION REQUIRED |
| Azure | Foundry Agent Service GA — Durable Agent Orchestration added | Agent Engine Sessions GA | Comparable |
| Azure | Foundry REST API GA — stable /openai/v1/ contract | Vertex AI API | Comparable |

### SDK Updates (NEW)
- **OpenAI Agents SDK v0.12.5** (released March 19!) — WebSocket transport for Responses models, handoff history packaged as single assistant message, tool search with namespaces, configurable MCP tool failure handling
- **Anthropic Claude Code** — /loop command, voice mode, MCP elicitation hooks, startup name flag, sparse worktree paths, PostCompact hook, effort command

### Product Launches (NEW)
- **TestSprite 2.1** — agentic testing for AI-native teams, automates test planning → code gen → execution → debugging (ProductHunt March 7)
- **Ceros AI Trust Layer** (Beyond Identity) — sits on developer machine alongside Claude Code, provides real-time visibility + runtime policy enforcement for AI coding agents
- **Apple Siri Reimagined** — 2026 debut: context-aware, on-screen awareness, cross-app integration (announced)

### Security (NEW)
- **Claude Code security at scale** — running across enterprise eng orgs with full developer permissions, no audit trail visible to existing security infra. Described as operating "entirely outside traditional security controls"
- **Agentic security validation going mainstream** — security validation shifting from manual to agentic approaches

---

## 2026-03-18 Evening — Fresh Scan

### NEW Cloud Provider Updates
| Provider | Update | GCP Equivalent? | Gap? |
|----------|--------|-----------------|------|
| Azure | SRE Agent GA — 1,300 agents deployed internally, 35K incidents mitigated, 20K eng-hours saved/month | No equivalent | GAP — GCP has no AI SRE agent product |
| Azure | Microsoft Agent Framework announced — unified agent building framework | ADK (Agent Development Kit) | Comparable — different ecosystems |
| Azure | Foundry Portal GA at ai.azure.com — unified interface for agents | Vertex AI Console | Comparable |
| Azure | Foundry Agent Service private networking (BYO VNet) | VPC Service Controls | Comparable |
| GCP | Gemini 3 Flash public preview — agentic reasoning + coding | N/A (native) | GCP STRENGTH |
| GCP | Agent Designer low-code visual builder (Preview) | N/A (native) | GCP STRENGTH |
| GCP | Cloud API Registry for MCP server management (Preview) | N/A (native) | Catching up on MCP |

### NEW Product Launches
- **Luma Agents** — creative AI agents with "Unified Intelligence" models for text/image/video/audio generation. API available.
- **NeuralAgent 2.0 Skills** — ProductHunt launch, desktop computer control agent (sees screen, clicks buttons, manages files)
- **OpenAI Codex Security** — AI security agent scanning commits for vulnerabilities (1.2M commits scanned, 10,561 high-severity issues found)
- **Claude Certified Architect (CCA)** — Anthropic's enterprise certification program launched March 12, includes MCP orchestration
- **Samsung Galaxy S26** — Bixby + Gemini + Perplexity agents for device control via conversation

### NEW Security Alerts
- **China CNCERT warning on OpenClaw** — flagged "inherently weak default security configurations" as exploitable
- **Agentic browser phishing** — AI browsers tricked into phishing/scam traps via reasoning manipulation
- **OpenAI Codex Security findings** — 10,561 high-severity issues across 1.2M commits

---

## 2026-03-18 Afternoon — Daily Scan

### Cloud Provider Updates
| Provider | Update | GCP Equivalent? | Gap? |
|----------|--------|-----------------|------|
| AWS | Bedrock AgentCore Policy GA — fine-grained agent-tool controls | Vertex AI Agent Builder Tool Governance (Preview) | GCP has similar via Cloud API Registry but AWS Policy is GA |
| AWS | Bedrock AgentCore stateful MCP support (elicitation, sampling, progress) | No direct equivalent | GAP — GCP has no native MCP support in Agent Builder |
| AWS | Bedrock shell command execution API (InvokeAgentRuntimeCommand) | Agent Engine Code Execution (Preview) | Partial — GCP sandbox execution, not shell commands |
| Azure | Foundry Agent Service GA — Python/JS/Java/.NET SDKs | Vertex AI Agent Engine GA | Comparable |
| Azure | Copilot Cowork — desktop file manipulation agent | No equivalent | GAP — GCP has no desktop agent |
| Azure | Voice Live + Agent Service preview | No equivalent | GAP — GCP has no real-time voice agent integration |

### Major Product Launches
- **Nvidia NemoClaw** — open-source security/privacy layer for AI agents, announced at GTC 2026
- **Galileo Agent Control** — open-source governance layer for AI agent behavior standards
- **Salesforce Agentforce Health** — 6 new autonomous healthcare agents
- **Anthropic Enterprise Marketplace** — third-party apps on Claude for enterprise customers

### Open Source Trending
- **OpenClaw** — 210k+ stars, dominant AI agent framework
- **The Agency** — 61 specialized coding agents, 10k stars in first week
- **Autoresearch** (Karpathy) — automated ML research on single GPU, 23k stars
- **DeerFlow** (ByteDance) — SuperAgent framework with sandbox/memory/sub-agents
- **OpenViking** (Volcengine) — context database for AI agents
- **Superpowers** — agentic skills framework for coding agents

### SDK Updates
- **OpenAI Agents SDK v0.12.3** — WebSocket transport, SIP realtime, gpt-5.4 computer use
- **Anthropic MCP** — elicitation support, native server management, binary content handling

### Security Concerns
- AI agents described as "identity dark matter" — powerful but unmanaged security risks
- 23% of orgs planning agent deployments, 2/3 building in-house
