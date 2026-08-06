# Inspiration patterns

Rule-clean note: these are inspiration sources only. AgentProof OS should adapt patterns, not copy implementation.

| Source | Pattern worth adapting | AgentProof OS response |
|---|---|---|
| [FidusGate](https://github.com/SafetyMP/FidusGate) | zero-trust agent operation governance, policy gates, signed receipts, MCP proxy enforcement | add policy-as-code and stronger cryptographic receipt signing beyond SHA-256 hash |
| [fuseraft](https://github.com/fuseraft/fuseraft-cli) | runtime verification of handoffs by checking artifacts and command results, not agent claims | keep `make verify` as the authority and gate agent handoffs on evidence predicates |
| [mcpfusion](https://github.com/vinkius-labs/mcpfusion) | MCP security contract, state-gated tools, behavior digests, capability lockfile | add `mcp_tools.lock.json` and tool behavior digest check |
| [LangSight](https://github.com/langsight/langsight) | “watch the hands”: MCP/tool call health, cost, schema drift, blast radius | expose tool-call metrics and schema-drift report in receipts |
| [AgentTeams](https://github.com/agentscope-ai/AgentTeams) | Manager/Worker/Team/Human roles, Matrix collaboration, controller, Higress/MCP routes | keep architecture mapped to AgentTeams and plan a compatibility adapter |
| [ATLAS LinkedIn post](https://www.linkedin.com/posts/sardor-razikov-569a5327b_atlas-enterprise-multi-agent-system-ai-activity-7462457002317975552-ADGR) | enterprise multi-agent governance pitch with tests, signed audit chain, adversarial blocking demo | make our 10-second demo a visibly blocked risky action plus test count + hash receipt |
| [SONiC Agentic RCA post](https://www.linkedin.com/posts/hugo-tinoco_sonic-networkautomation-ocpsummit-activity-7384988067977199635-vV_q) | hackathon-winning MCP server wrapped with LLM-as-judge / pytest RCA evaluation | add pytest-style fixture evaluations for each scenario and eventual RCA/claims scenario |
| [Cloud.ru Procurement Agent](https://github.com/stavrmoris/hack_mcp_cloud_ru) | award-winning enterprise MCP architecture with external APIs, RAG memory, logistics scenario | later add procurement/claim scenarios as extra vertical fixtures without losing infra focus |

## immediate build implications

1. **policy-as-code** before UI polish: a small `policies/actions.yaml` can make approval gates inspectable.
2. **tool contract lockfile**: hash MCP-style tool definitions so judges see schema drift detection.
3. **receipt metrics**: agent count, handoff count, verdicts, blocked action, hash, and future latency/cost.
4. **AgentTeams bridge note**: show how this local runner migrates to Manager/Worker/Human + Higress/MCP routes.
5. **adversarial fixture**: add a prompt-injection / unsafe-action case and prove it blocks.
