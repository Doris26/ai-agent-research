# Research Ledger

## 2026-03-18 — Daily Scan

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
