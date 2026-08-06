PYTHON ?= python

.PHONY: verify demo test

verify: test demo
	$(PYTHON) -m agentproof.cli check-skills
	$(PYTHON) -m agentproof.cli check-tool-lock
	$(PYTHON) -m agentproof.cli verify-receipt --receipt artifacts/receipts/latest.json
	$(PYTHON) -m agentproof.cli receipt-summary --receipt artifacts/receipts/latest.json --out artifacts/receipts/latest.md

test:
	$(PYTHON) -m pytest -q

demo:
	AGENTPROOF_FIXED_TIME=2026-08-06T00:00:00+00:00 $(PYTHON) -m agentproof.cli run --fixture fixtures/cases/vendor_refund_claim.json --out artifacts/runs/latest.json
	$(PYTHON) -m agentproof.cli receipt --run artifacts/runs/latest.json --out artifacts/receipts/latest.json
