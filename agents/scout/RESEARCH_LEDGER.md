# Research Ledger

## 2026-03-25 — Daily Scan

### Cloud Provider Updates
| Provider | Update | GCP Equivalent? | Gap? |
|----------|--------|-----------------|------|
| AWS | Bedrock AgentCore stateful MCP GA (March 10) — elicitation, sampling, progress notifications, isolated microVM sessions | No equivalent in Vertex AI Agent Builder | GAP — GCP has MCP server management UI (Preview) but no MCP runtime |
| AWS | Bedrock AgentCore Quality Evaluations + Policy Controls — governance layer for trusted agent deployment | Limited eval tooling | GAP — AWS governance tooling more mature |
| Azure | SRE Agent GA (March 10) — 1,300+ agents deployed internally, 35K incidents mitigated, 20K eng-hours saved/month | No equivalent | GAP — GCP has no AI SRE agent product |
| Azure | Microsoft Agent Framework — unified build/observe/govern multi-agent system | ADK | Comparable |
| GCP | No new major announcements found March 24-25 — Agent Engine GA, Agent Designer Preview, Cloud API Registry Preview from earlier in month | — | GCP quiet this week |

### Major Product Launches (March 24-25 window)
- **[Alibaba Wukong](https://www.cnbc.com/2026/03/17/alibaba-wukong-ai-enterprise-tool-restructuring-qwen-exits.html)** — enterprise multi-agent management with Slack/Teams integration. First serious Chinese enterprise agent with Western collaboration integrations.
- **[Manus Desktop App](https://techcrunch.com/2026/03/05/exclusive-luma-launches-creative-ai-agents-powered-by-its-new-unified-intelligence-models/)** — Meta-backed local desktop agent; operates on files/apps directly. Third desktop agent after Azure Copilot Cowork + Claude Computer Use.
- **[AgentDiscuss](https://aitoolly.com/ai-news/article/2026-03-17-agentdiscuss-launches-on-product-hunt-a-new-platform-for-ai-agent-collaboration-and-discussion)** — Garry Tan/YC-backed platform for AI agent collaboration/discussion. ProductHunt March 17.
- **[Siemens Fuse EDA AI Agent](https://news.siemens.com/en-us/siemens-fuse-eda-ai-agent/)** — domain-specific agent for electronic design automation. NVIDIA GTC debut. Vertical agent trend accelerating.
- **[Picsart AI Agent Marketplace](https://www.marketingprofs.com/opinions/2026/54448/ai-update-march-20-2026-ai-news-and-views-from-the-past-week)** — creator-facing marketplace for specialized visual editing agents.
- **[BotBoard](https://www.producthunt.com/leaderboard/daily/2026/3/15)** — task management designed for agent-era workflows. ProductHunt ~March 24.
- **[Google Stitch AI Design Env](https://www.crescendo.ai/news/latest-ai-news-and-updates)** — infinite canvas + design agent that reasons across projects + agent manager for parallel UI prototyping.
- **[Gartner Guardian Agents Market Guide](https://hackernoon.com/ai-in-2026-whats-trending)** — first Gartner guide for agents-supervising-agents. New governance category now official.

### SDK Updates
- **OpenAI Agents SDK v0.13.1** (March 25) — SIP protocol in RealtimeRunner, Python 3.14 compat, WebSocket transport (opt-in), default Realtime model = `gpt-realtime-1.5`, `gpt-5.4` for computer use
- **Anthropic Claude Code** — `--bare` flag for scripted calls, `--channels` permission relay to phone, MCP elicitation hooks, VSCode native MCP server management dialog (`/mcp`)

### Open Source (NEW)
- **[Understand-Anything](https://topaiproduct.com/2026/03/22/understand-anything-scores-2400-github-stars-by-mapping-codebases-with-five-ai-agents/)** — 2,400 stars March 22. 5-agent codebase intelligence pipeline (scan → analyze → architecture → tour → validate). MIT licensed. Claude Code plugin.
- **[Hindsight](https://aitoolly.com/ai-news/article/2026-03-15-hindsight-learning-agent-memory-a-new-project-trending-on-github-by-vectorize-io)** (vectorize-io) — learning agent memory project, trending mid-March
- **[Lightpanda](https://www.shareuhack.com/en/posts/github-trending-weekly-2026-03-18)** — headless browser in Zig for AI agents, CDP-compatible
- **LangChain Deep Agents** — 9.9k stars in 5 hours on major March update; NVIDIA AI-Q Blueprint partnership

### Framework Status (March 25)
| Framework | Status | Trend |
|-----------|--------|-------|
| LangGraph | Production-mature, enterprise default | Strong |
| OpenAI Agents SDK | Rapid releases (v0.13.1), 100+ LLMs | Strong |
| CrewAI | v1.10+ A2A support, fast iteration | Growing |
| AutoGen | Last release Sept 2025 (v0.7.5) | Declining |
| Smolagents | Slowed | Flat |

### Updated GCP Gap Scorecard (March 25)
| Gap | Status |
|-----|--------|
| No MCP runtime (only mgmt UI) | OPEN — AWS Bedrock AgentCore stateful MCP GA, GCP Preview only |
| No desktop agent | OPEN — 3 competitors now (Azure, Claude, Manus) |
| No real-time voice agent | OPEN |
| No AI SRE agent | OPEN — Azure SRE Agent GA with hard production metrics |
| No agent marketplace | OPEN |
| Tool governance maturity | NARROWING — GCP Cloud API Registry, but AWS Policy GA is more mature |
| Agent evaluation/quality | OPEN — AWS AgentCore quality evaluations, no GCP equivalent |

---

## 2026-03-23 — Daily Scan

### Cloud Provider Updates
| Provider | Update | GCP Equivalent? | Gap? |
|----------|--------|-----------------|------|
| AWS | Bedrock AgentCore WebRTC — real-time bidirectional audio/video streaming for voice agents | No equivalent yet | GCP STILL BEHIND on real-time voice agent infra |
| AWS | Bedrock AgentCore Slack integration — agents accessible directly in Slack | No native equivalent | Minor gap |
| AWS | NVIDIA Nemotron 3 Super on Bedrock + Nova Forge SDK | N/A | AWS model breadth expanding |
| Azure | Microsoft Agent Framework public preview — build/observe/govern multi-agent systems | ADK | Comparable |
| Azure | Foundry multi-agent workflows — structured stateful workflow layer | Agent Engine | Comparable |
| GCP | No new major announcements found March 23 | — | GCP quiet this week |

### Major Product Launches (March 23)
- **[Dapr Agents v1.0 GA](https://techrseries.com/hrtechnology/confirm-launches-ai-agents-platform-for-performance-management-at-transform-2026/)** — CNCF-backed, production-grade durable workflows for enterprise agents. Huge for cloud-native stacks.
- **[1Password Unified Access Platform](https://betakit.com/1password-launches-new-platform-to-rein-in-companies-ai-agents/)** — secure credential management for AI agents; orgs can deploy agents without surrendering auth control
- **[Qualys Agent Val](https://www.stocktitan.net/news/QLYS/qualys-debuts-industry-s-first-ai-agent-for-safe-exploit-validation-2s0jernyohzl.html)** — first AI agent for safe exploit validation + autonomous remediation
- **[Alibaba Accio Work](https://letsdatascience.com/news/alibaba-launches-accio-work-enterprise-agents-41532389)** — plug-and-play enterprise agent teams, no code required
- **[Anthropic Claude Computer Use](https://siliconangle.com/2026/03/23/anthropics-claude-gets-computer-use-capabilities-preview/)** — Claude can now click, scroll, navigate web/apps. Research preview for Pro/Max. Second desktop agent after Azure Copilot Cowork.
- **[Claude Code Channels](https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels)** — hook Claude Code to Discord/Telegram for mobile access. Described as "OpenClaw killer"
- **[OpenAI Agents SDK v0.13.0](https://github.com/openai/openai-agents-python/releases)** — released today; gpt-realtime-1.5 voice agent support, 100+ LLM providers, guardrails + handoffs improvements
- **[LangChain Open-SWE](https://aitoolly.com/ai-news/article/2026-03-21-langchain-ai-launches-open-swe-a-new-open-source-asynchronous-coding-agent-for-software-engineering)** — open-source async software engineering coding agent
- **[NVIDIA Agent Toolkit + OpenShell](https://nvidianews.nvidia.com/news/ai-agents)** — open-source runtime with policy-based security guardrails for enterprise agent deployment
- **Product Hunt Orbit Awards** — first-ever PH awards for AI workflow automation tools

### Open Source (NEW)
- **obra/superpowers** — +37,809 stars this month. Agent skill framework going mainstream.
- **gstack** (Garry Tan, YC) — 23,057 stars in first 7 days. Opinionated agent config stack.
- **LangChain Open-SWE** — async coding agent, open source

### Security (CRITICAL)
- **[OpenClaw prompt injection + data exfiltration](https://thehackernews.com/2026/03/openclaw-ai-agent-flaws-could-enable.html)** — confirmed vulnerabilities; China restricting OpenClaw on government systems
- **ClawWorm** — self-propagating attack targeting LLM agent ecosystems via OpenClaw. 40,000+ active instances at risk.

### Updated GCP Gap Scorecard (March 23)
| Gap | Status |
|-----|--------|
| No native MCP support | STILL OPEN |
| No desktop agent | NARROWED — Claude Computer Use adds 2nd competitor (Azure was first) |
| No real-time voice agent | STILL OPEN — AWS now has WebRTC voice agents too |
| Tool governance maturity | NARROWING |
| No agent marketplace | STILL OPEN |
| No AI SRE agent | STILL OPEN |

---

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
