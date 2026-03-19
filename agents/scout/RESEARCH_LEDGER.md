# Research Ledger

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
