# Control surface summary

Generated from `artifacts/runs/latest.json` and `artifacts/receipts/latest.json`.
It turns the gateway / observability inspiration into concrete, local proof without claiming a live external MCP gateway deployment.

## live-request-path controls in the fixture

| Control surface | Current fixture value | Judge-visible proof |
|---|---|---|
| task identity | CASE-GOAI-001 | stable case/session id emitted in every receipt |
| human / tenant boundary | operations_manager | actor is tracked separately from workers; no worker receives real credentials in fixture mode |
| requested tool/action | refund | side-effect candidate extracted before any execution |
| evidence inputs | invoice-7781, ticket-183 | source ids remain attached to the decision |
| deterministic verifier | PASS | failures=0 |
| policy decision | BLOCK | refund requires explicit human approval; policy gate requires human approval |
| approval gate | required=True; present=False | high-risk actions cannot self-approve |
| external side effect | not executed | fixture-safe replay keeps mutation outside the agent process |

## rule-clean inspiration mapping

| Inspiration pattern | Rule-clean AgentProof adaptation | Artifact |
|---|---|---|
| AgentTeams / HiClaw | maps handoffs to visible Manager → Worker room messages | `artifacts/runs/latest.md` |
| MCP gateway pattern | intercept tool/action before execution; deny risky mutation without approval | this control summary + `agentproof/security.py` |
| observability pattern | emit task id, actor, tool/action, decision, reason, and receipt hash | `artifacts/receipts/latest.json` |
| tamper-evident exit artifact | bind final decision to sha256 receipt | acd2aec115bb16121ecf1633b8012dca58d245f71f830fb16164523d1ac3ca52 |
