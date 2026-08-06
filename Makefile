PYTHON ?= python

.PHONY: verify demo test

verify: test demo
	$(PYTHON) -m agentproof.cli check-skills
	$(PYTHON) -m agentproof.cli verify-receipt --receipt artifacts/receipts/latest.json

test:
	pytest -q

demo:
	$(PYTHON) -m agentproof.cli run --fixture fixtures/cases/vendor_refund_claim.json --out artifacts/runs/latest.json
	$(PYTHON) -m agentproof.cli receipt --run artifacts/runs/latest.json --out artifacts/receipts/latest.json
