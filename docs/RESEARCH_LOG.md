# Research log

## source query ladder

- official: `site:goaihz.com/en Global Open-source AI Challenge tracks Agent Infra`
- official wording: `"Global Open-source AI Challenge" "Agent Infra" "at least three agents"`
- inspiration: GitHub multi-agent runtime verification, agent skills open source, MCP gateway enterprise agents, AgentTeams Hiclaw Alibaba, hackathon winning agent infra, Reddit multi-agent framework winners, LinkedIn AI agent hackathon winner.

## initial official findings

- GOAI has four tracks: Agent Infra, Boundless Agents, AI for Research, Embodied Future.
- Agent Infra requires at least three agents with distinct roles and an end-to-end enterprise loop.
- AgentTeams/Hiclaw is the design baseline.
- Skill is mandatory; MCP and observability are recommended.
- Preliminary round focuses on direction/technical solution/open-source value/feasibility; later rounds require runnable demos/evaluation/open-source standards.

## adaptation rule

Do not clone inspiration projects. Extract reusable patterns: typed handoffs, explicit verifier, human approval for risky actions, open-source Skill contracts, trace receipts, one-command demo.

## 2026-08-06 keyword sweep

Queries varied across GOAI Agent Infra, AgentTeams/Hiclaw, multi-agent runtime verification, MCP tool gateway, agent observability, reusable agent skills, winning agent hackathon project, Reddit multi-agent framework, and LinkedIn AI hackathon winner.

- GOAI/Agent Infra official material emphasizes AgentTeams as the collaboration design baseline and asks teams to demonstrate task decomposition, context passing, tool invocation, result verification, execution evidence, and reusable Skills. Source: https://www.goaihz.com/en
- Alibaba Cloud's Agent Infra launch article gives the most concrete rubric signal found this sweep: scenario value/copyability 25%, multi-agent collaboration/autonomous loop 25%, Skill engineering/ecosystem reuse 25%, engineering verification/security audit 20%, open-source contribution 5%; it also names AgentTeams and AgentLoop as expected infrastructure references. Source: https://developer.aliyun.com/article/1750732
- HiClaw/AgentTeams positions Matrix-room collaboration as a human-visible, auditable Manager/Worker architecture with centralized gateway credentials; AgentProof should keep making receipts/handoffs visible and avoid agents holding real secrets. Sources: https://hiclaw.io/ and https://github.com/agentscope-ai/AgentTeams
- Popular agent gateway/control-plane projects converge on MCP/A2A routing plus policy, OAuth/RBAC, OpenTelemetry, budget/spend controls, human approvals, and audit trails; useful inspiration is a narrow proof table that shows these controls in one place. Sources: https://github.com/agentgateway/agentgateway, https://github.com/Preloop/Preloop, https://github.com/microsoft/mcp-gateway
- Agent observability/trust projects make the strongest proof surfaces explicit: contracts before execution, trace/telemetry during execution, tamper-evident bundles after execution, plus tool-call latency/status/cost where available. Sources: https://github.com/wharfe/agent-trust-suite, https://github.com/KryptosAI/agent-observability, https://github.com/LangSight/langsight
- Winning or winner-claimed multi-agent hackathon repos tend to ship a one-command/offline deterministic demo, live visualization/control deck, trace/audit ledger, cost meter or observability, and clear human approval gates. Sources: https://github.com/s-k-28/hive, https://github.com/IGiotto12/Lungo_Plus, https://github.com/etisamhaq/aegis-multi-agent-system, https://www.linkedin.com/posts/aditya-jadhav-06484123a_sandhacks2026-multiagentsystems-agenticai-activity-7424527129838612481-NAQn
Action taken from this sweep: add a generated receipt proof-summary table so judges see the current run's agents, handoffs, evidence sources, verification verdict, security gate, approval boundary, side-effect boundary, and receipt hash without reading raw JSON.
