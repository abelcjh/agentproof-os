# Reddit Data API access status

Status: **manual approval requested; self-serve app creation still blocked**.

## What happened

- Reddit `/prefs/apps` app creation form was completed for `agentproof-os-research` as a `script` app.
- Required policy links were opened/read:
  - Responsible Builder Policy
  - Reddit Developer Terms
  - Reddit Data API Terms
- A Reddit Help **Data Access Request** was submitted for non-commercial, low-volume, read-only API access.
- After submission, `/prefs/apps` still rejects app creation with:

```text
In order to create an application or use our API you can read our full policies here: https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
```

Screenshot evidence:

```text
artifacts/screenshots/goai-social-2026-08-06/09-reddit-api-policy-block.png
```

## Current interpretation

This is not a form-field or reCAPTCHA issue. The likely blocker is Reddit's post-2026 manual Data API approval gate: the account can submit a request, but self-serve OAuth app creation remains blocked until Reddit approves or allowlists the account/use case.

## Rule-clean fallback

Until Reddit approves the request:

- Do **not** claim live Reddit API/OAuth integration.
- Continue using logged-in Reddit browser search as read-only social research evidence.
- Keep `scripts/reddit_search.py` ready, but treat it as pending credentials.
- Do not scrape or bypass Reddit limits.
- Do not use Reddit data for model training.

## Approved app draft values

```text
name: agentproof-os-research
type: script
description: Read-only low-volume Reddit search for Abel GOAI AgentProof OS hackathon research. Used to gather public discussion signals for a public open-source hackathon project; no posting, voting, or automation of user actions.
about url: https://github.com/abelcjh/agentproof-os
redirect uri: http://localhost:8080
user-agent: linux:agentproof-os-research:v0.1.0 (by /u/unicornalgorithm)
```

## Activation steps after Reddit approval

1. Create the app at `https://www.reddit.com/prefs/apps`.
2. Save `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT` into the local environment/secrets store.
3. Run a read-only smoke test:

```bash
REDDIT_USER_AGENT='linux:agentproof-os-research:v0.1.0 (by /u/unicornalgorithm)' \
python scripts/reddit_search.py "MCP agents" --subreddit all --limit 3
```

4. Only after that succeeds, claim Reddit API setup is live.
