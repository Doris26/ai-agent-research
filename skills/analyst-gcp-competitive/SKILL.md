---
name: gcp-competitive-analysis
description: "Daily GCP agent platform competitive analysis. Pull latest features, check public opinions, compare with competitors, post concrete product/API/infra ideas to #insights."
---

# GCP Agent Platform Competitive Analysis

Run this DAILY as part of the briefing cycle.

## Step 1: Pull Latest GCP Agent Features
```
web_search("Vertex AI Agent Engine release notes 2026")
web_search("Google ADK agent development kit latest features")
web_search("Gemini Interactions API new features")
web_search("site:cloud.google.com/vertex-ai/docs release-notes agent")
```

## Step 2: Pull Latest Competitor Features
```
web_search("AWS Bedrock Agents new features 2026")
web_search("Azure AI Agent Service updates 2026")
web_search("Anthropic MCP model context protocol latest")
web_search("OpenAI Agents SDK latest release")
web_search("LangChain CrewAI AutoGen latest release")
```

## Step 3: Check Public Opinions & Developer Sentiment
```
web_search("Vertex AI Agent Builder developer review")
web_search("Google ADK vs LangChain vs CrewAI reddit")
web_search("Google Cloud agent experience feedback twitter")
web_search("site:reddit.com Vertex AI agent")
web_search("site:news.ycombinator.com Google agent AI")
```

## Step 4: Deep Research on Key Gaps
For the biggest gaps found, run Gemini Deep Research:
```bash
/Users/yujunzou/python/python_repo/apexnova/.venv/bin/python3 \
  /Users/yujunzou/python/python_repo/apexnova/bin/deep_research.py \
  "What specific features is Google Cloud missing in its agent platform compared to AWS Bedrock and Azure AI? Focus on: tool authorization, memory persistence, multi-agent orchestration, and developer experience."
```

## Step 5: Post to #insights (channel 1483951839660609678)
Format each idea:
```
💡 **[Product/API/Infra Idea Name]**

**Evidence:** [competitor launched X / paper proved Y / developers complain about Z]
**GCP Today:** [what Agent Engine/ADK/Interactions API already has]
**Gap:** [what's missing specifically]
**Recommendation:** [exact feature/API to build, with technical details]
**Impact:** [developer adoption / revenue / competitive moat]
**Priority:** High / Medium / Low
```

Post 3-5 ideas per day to #insights.

## Step 6: Update RESEARCH_LEDGER.md
Add all findings with links and status.
