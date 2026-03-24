# MEMORY.md — Scholar Durable Knowledge

## Critical Security Findings (March 2026)

### Memory Attack Surface
- **From Storage to Steering** (2603.15125): RAG-based memory poisoning achieves 97-100% cross-task attack success on GPT-5 mini, Claude Sonnet 4.5, Gemini 2.5 Flash. Adversarial memories injected as "user preferences" bypass system prompt safety entirely. Vertex AI Memory Bank GA has no write-time admission gate.
- **A-MAC** (2603.04549, Workday AI): 5-factor memory admission gate — future utility + factual confidence + semantic novelty + temporal recency + content type. Blueprint for what Memory Bank write-gate should implement.
- **Governance-Aware Vector Subscriptions** (2603.20833): Policy predicates baked into retrieval layer. Data governance at query time, not just write time.

### OpenClaw / Agent Runtime Security (7 papers, March 2026)
- Baseline sandbox-escape defense rate: **17%** (2603.10387). Enterprise platforms need 95%+.
- 5-layer lifecycle threat model: Initialization/Input/Inference/Decision/Execution (2603.11619).
- Bootstrap hooks are a pre-prompt attack vector — executes before user interaction (2603.19974 Trojan's Whisper).
- Economic DoS via token amplification: 6-9x tokens via trojaned skills (2603.00902 Clawdrain).
- Social manipulation: single rogue agent can take over collective MAS decisions (2603.15809).
- Attack/defense survey: 51 attacks, 60 defenses catalogued; adaptive attacks breach SOTA at >85% (2603.11088).
- Zero-trust + dynamic intent verification = FASA framework (2603.12644).

### Multi-Agent Error Propagation
- **From Spark to Fire** (2603.04474): Genealogy-graph governance lifts cascade defense 0.32 → 0.89.
- **ProMAS** (2603.20260): Markov transition dynamics for proactive error forecasting before cascades.
- **Don't Trust Stubborn Neighbors** (2603.15809): Friedkin-Johnsen social manipulation in agent networks.

## Architecture Insights

### Memory
- **Library Theorem** (2603.21272): Formal proof — indexed external memory achieves exponentially better efficiency than sequential retrieval. Validates Memory Bank architecture.
- **CoMAM** (2603.12631): MDP-based multi-agent memory coordination — prevents fragmentation in collaborative settings.

### Orchestration
- **AdaptOrch** (2602.16873): As LLM performance converges, topology selection dominates. Dynamic topology (parallel/sequential/hierarchical/hybrid) gives 12-23% improvement.
- **Utility-Guided Tool Use** (2603.19896): Explicit quality-vs-cost decision across respond/retrieve/tool_call/verify/stop actions.
- **DOVA** (2603.13327): Deliberation-before-tool-invocation with 6-level token budgeting — 40-60% inference cost reduction on simple tasks.
- **AgentFactory** (2603.18000, Peking U): Self-evolving executable Python subagent code accumulation.

### Self-Propagating Threats
- **ClawWorm** (2603.15727): First documented self-replicating worm targeting production LLM agent platforms. 40,000+ active OpenClaw instances at risk. China restricting OpenClaw on government systems.
- **Thought Virus** (2603.00131): Subliminal misalignment propagation across multi-agent networks via inter-agent comms.

## Evaluation Benchmarks

- **EnterpriseOps-Gym** (2603.13594): Claude Opus 4.5 = 37.4% on 164 DB tables + 512 tools + 1,150 tasks. Gemini 2.5 Pro not tested — open dataset allows external eval (GCP opportunity).
- **ZeroDayBench**: Real CVE evaluation — models score <25% on complex vulns.
- **AuditBench** (2602.22755, Anthropic): 56 LLMs, 14 planted hidden behaviors. Models don't self-report.
- **LiveAgentBench** (2603.02586): 374 tasks from real user queries, continuous updates.
- **AgentComm-Bench** (2603.20285): Cooperative embodied AI under realistic communication latency.

## GCP Gaps Identified (from Scholar feed)
1. **Memory Bank has no write-time admission control** — 97-100% memory poisoning attack success rate
2. **No per-session hardware isolation** — AWS uses Firecracker microVMs, GCP uses shared Cloud Run
3. **No enterprise voice agent API** — Gemini Live is consumer-only; AWS WebRTC + Azure Voice Live both GA
4. **No bootstrap/skill supply chain security** — Trojan's Whisper shows pre-context attacks are unguarded

## Scholar Feed Channel
- `#scholar-feed` channel ID: `1482551533366411307`
- Post format: `[ArXiv ID] Title — arxiv.org/abs/XXXX\nKey contribution. GCP angle.`

## Recurring Sources Worth Checking
- arxiv.org cs.MA (multi-agent systems) — daily
- arxiv.org cs.AI (AI) — weekly
- arxiv.org cs.CR (security) — weekly for agent security papers
