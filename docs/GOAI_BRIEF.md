# GOAI Agent Infra brief → build requirements

Source: <https://www.goaihz.com/en/tracks>

## selected track

**Agent Infra** — multi-agent infrastructure and collaboration systems for complex enterprise tasks.

## extracted hard requirements

| Requirement | Build implication |
|---|---|
| not a single-agent showcase | minimum 3 named agents with clear roles and typed handoffs |
| complete enterprise-oriented closed loop | intake → decomposition → tool/skill execution → verification → audit → receipt/review |
| AgentTeams design baseline | docs map our roles, state, handoffs, and orchestration to AgentTeams concepts; implementation starts framework-neutral until API access is confirmed |
| Skill mandatory | key capabilities packaged as versioned Skill contracts with inputs/outputs/failure handling |
| MCP recommended | tool contracts are MCP-shaped and can be exposed via MCP server later |
| observability recommended | every run emits trace JSON, metrics, receipt hash, and failure reasons |
| preliminary focuses on solution design | repo needs clear architecture, proposal-ready proof ledger, runnable smoke path, and open-source plan |
| later rounds need runnable demo/evaluation | maintain `make verify`, fixtures, traces, metrics, and local deployment path |

## scenario wedge

Enterprise compliance / claims / financial-risk teams need agentic help, but cannot trust opaque agent actions. AgentProof OS turns risky workflows into governed multi-agent receipts with deterministic checks and explicit human approval boundaries.

## preliminary submission assets to prepare

- project intro under 500 Chinese-character equivalent
- proposal deck/PDF: scenario, value, agent roles, Skill/tool integration, context passing, verification, exception branches, safety boundaries, risk control, open-source plan
- repo link and run command, even if runnable code is not required
