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
