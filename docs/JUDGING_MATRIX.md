# GOAI Agent Infra judging matrix

Source: <https://www.goaihz.com/en/tracks> and GOAI FAQ <https://www.goaihz.com/en/faq>.

## selected track

**Agent Infra**. Preliminary submission deadline: **Aug 16**. Semi-final deadline: **Sep 3**. Finals / GOAI DAY: **Sep 22–23, Hangzhou**.

## weighted rubric → build order

| Rubric bucket | Weight | Hard build requirement in AgentProof OS | Current evidence |
|---|---:|---|---|
| Scenario value and industry reusability | 25% | Enterprise compliance / financial-risk workflow with reusable regulated-action receipt pattern | `README.md`, `docs/PROPOSAL_INTRO.md`, `fixtures/cases/vendor_refund_claim.json` |
| Multi-agent collaboration and autonomous closed loop | 25% | 3+ distinct agents, typed handoffs, end-to-end intake → evidence → policy → verification → audit → skill capture | `agentproof/agents.py`, `artifacts/runs/latest.json` |
| Skill engineering system and ecosystem reuse | 25% | reusable Skill specs with inputs/outputs/failure handling, plus AgentTeams-compatible Skill docs | `skills/*.skill.yaml`, `skills/*/SKILL.md` |
| Engineering implementation, runtime verification, security auditability | 20% | deterministic tests, policy-as-code, tool contract lock, receipt hash, blocked side effect demo | `make verify`, `policies/actions.yaml`, `mcp_tools.lock.json`, `artifacts/receipts/latest.json` |
| Open-source / long-term value | 5% | MIT license, public repo, roadmap, AI-agent entrypoint, contributor-ready contracts | `LICENSE`, `AI_Agent.md`, `docs/ROADMAP.md` |

## preliminary assets checklist

- [x] public repo
- [x] project intro draft
- [x] proposal-ready architecture docs
- [x] agent roles and task decomposition
- [x] Skill/tool integration story
- [x] result verification and safety boundary
- [x] executable fixture even though preliminary code is optional
- [ ] PDF/PPT proposal deck
- [ ] official registration/submission form
