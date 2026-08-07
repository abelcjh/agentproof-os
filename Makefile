PYTHON ?= $(shell if [ -x .venv/bin/python ]; then printf .venv/bin/python; else printf python; fi)

.PHONY: verify demo test

verify: test demo
	$(PYTHON) -m agentproof.cli check-skills
	$(PYTHON) -m agentproof.cli check-tool-lock
	$(PYTHON) -m agentproof.cli verify-receipt --receipt artifacts/receipts/latest.json
	$(PYTHON) -m agentproof.cli trace-summary --run artifacts/runs/latest.json --out artifacts/runs/latest.md
	$(PYTHON) -m agentproof.cli receipt-summary --receipt artifacts/receipts/latest.json --out artifacts/receipts/latest.md
	$(PYTHON) -m agentproof.cli control-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/control/latest.md
	$(PYTHON) -m agentproof.cli health-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/health/latest.md
	$(PYTHON) -m agentproof.cli carrier-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/carrier/latest.md
	$(PYTHON) -m agentproof.cli identity-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/identity/latest.md
	$(PYTHON) -m agentproof.cli proof-index --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/proof/latest.md
	$(PYTHON) -m agentproof.cli readiness-summary --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/readiness/latest.md
	$(PYTHON) -m agentproof.cli gateway-trace --run artifacts/runs/latest.json --receipt artifacts/receipts/latest.json --out artifacts/gateway/latest.md

test:
	$(PYTHON) -m pytest -q

demo:
	AGENTPROOF_FIXED_TIME=2026-08-06T00:00:00+00:00 $(PYTHON) -m agentproof.cli run --fixture fixtures/cases/vendor_refund_claim.json --out artifacts/runs/latest.json
	$(PYTHON) -m agentproof.cli receipt --run artifacts/runs/latest.json --out artifacts/receipts/latest.json
