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

## 2026-08-06T18:02Z keyword sweep

Queries varied across GOAI Agent Infra, AgentTeams/HiClaw, multi-agent runtime verification, MCP tool gateway, agent observability, Reddit multi-agent framework terms, and LinkedIn/web-indexed AI hackathon winners.

- AgentTeams keeps confirming the most judge-relevant product surface for this track: Manager/Worker orchestration, Matrix-room human visibility, intervention, central gateway credentials, MCP server hosting, controller observability, and coexistence of OpenClaw/QwenPaw/Hermes workers. AgentProof should make its local fallback read like a future room transcript, not only a JSON log. Sources: https://github.com/agentscope-ai/AgentTeams and https://hiclaw.io/
- GOAI press coverage reinforces that Agent Infra is about moving agents from demos to production with task decomposition, context passing, tool invocation, result verification, execution evidence, reusable Skills, plus bonus MCP/RAG/observability/security approval/rollback auditing. Source: https://www.newsfilecorp.com/release/306212/GOAI-Global-OpenSource-AI-Challenge-Four-Tracks-Officially-Launched
- MCP Runtime and agentgateway-style projects make policy-on-the-live-request-path look more production-ready than policy docs: per-tool allow/deny, session/grant identity, audit events, OpenTelemetry, and revocation should eventually appear in AgentProof receipts. Sources: https://docs.mcpruntime.org/ and https://github.com/agentgateway/agentgateway
- Agent Trust Suite and AXIOM MCP show that trust projects are judged by before/during/after proof: declare contracts before execution, observe traces during execution, then export tamper-evident bundles, replay reports, drift/guard scores, or HTML/Markdown receipts after execution. Sources: https://github.com/wharfe/agent-trust-suite and https://github.com/Mr-Brownn/axiom-mcp
- Web-indexed LinkedIn winner posts point to concrete hackathon proof bars: Splunk Agentic Ops winner `kassi` used a state machine and k6 MCP to catch bad deploys, test, and return a fix; a ConductorOne Agent Infra track winner used parallel MCP servers plus guardrails to prevent tool-call spam and keep codebase scanning token-efficient. Sources: https://www.linkedin.com/posts/adamsrahman_aiagents-splunk-devpost-activity-7484952315905527808-O4-k and https://www.linkedin.com/posts/anthony-l103_hackathon-agenticai-golang-activity-7457948322402709504--r1v

Action taken from this sweep: add a generated `artifacts/runs/latest.md` AgentTeams-style trace summary so judges can see ordered worker handoffs, payload contracts, verifier result, blocked refund gate, and SkillLibrarian lesson without opening raw JSON.

## 2026-08-06T20:08Z keyword sweep

Queries varied across GOAI Agent Infra, AgentTeams/HiClaw, multi-agent runtime verification, MCP tool gateway, agent observability, reusable agent skills, Reddit multi-agent framework terms, and LinkedIn/web-indexed AI hackathon winner posts.

- AgentTeams/HiClaw keeps setting the GOAI-native bar: humans should be able to watch Manager/Worker collaboration in Matrix rooms, intervene in real time, and keep real credentials in the Higress gateway rather than inside worker agents. AgentProof should keep turning local handoffs into future room-message artifacts and keep credential boundaries explicit. Sources: https://www.hiclaw.io/ and https://github.com/agentscope-ai/AgentTeams
- The HiClaw Kubernetes-native orchestration doc adds a more precise control-plane metaphor: Worker/Team/Human/Manager resources, declarative communication policies, controller reconcile loops, MinIO shared state, and Higress gateway consumer tokens. AgentProof can stay rule-clean by documenting which local proof artifacts map to those future CRD/control-plane concepts without pretending a live AgentTeams deployment exists. Source: https://github.com/agentscope-ai/HiClaw/blob/main/docs/k8s-native-agent-orch.md
- MCP gateway projects converge on the same judge-visible trust surface: every tool call should pass through auth/RBAC or allowlists, produce an audit record, expose latency/status/denial metrics, support revocation/rate limits/circuit breakers, and avoid trusting spoofable client fields. Sources: https://github.com/Agentgateway/Agentgateway, https://docs.mcpruntime.org/, https://github.com/iamdainwi/AgentGate, and https://github.com/reaatech/mcp-gateway
- Agent observability / trust projects frame proof across before-during-after: declare contracts before execution, observe traces while running, then export tamper-evident bundles or verifier outputs after execution. Source: https://github.com/wharfe/agent-trust-suite
- Web-indexed winner posts show that multi-agent hackathon demos win when the architecture is legible: MCP Atlas focused on MCP request tracing, tool-call observability, and context-bloat reduction; AGNTCity showed supervisor-worker agents, MCP storage, A2A/NATS, and OpenTelemetry/Grafana; ForgeMCU showed Architecture → Code → Test → Quality → Build agents with MCP governance. Sources: https://www.linkedin.com/posts/deepeshkatudia_ai-artificialintelligence-generativeai-activity-7439425959046418432-xhpa, https://www.linkedin.com/posts/jiaying-chen01_my-team-just-won-the-multi-agent-systems-activity-7424216495091748864-7Q0X, and https://www.linkedin.com/posts/jeeva4772_hackathonwin-agenticai-embeddedsystems-activity-7434996618615070720-MA1d

Action taken from this sweep: add a generated `artifacts/control/latest.md` control-surface summary. It makes task identity, actor boundary, requested side effect, evidence inputs, verifier result, policy decision, approval gate, external side-effect state, and rule-clean MCP/observability mapping visible from the deterministic fixture.
