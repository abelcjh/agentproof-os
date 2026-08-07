#!/usr/bin/env python3
"""Read-only Reddit search helper for AgentProof OS research.

Requires environment variables:
  REDDIT_CLIENT_ID
  REDDIT_CLIENT_SECRET
  REDDIT_USER_AGENT

Usage:
  python scripts/reddit_search.py "multi agent governance" --subreddit LocalLLaMA --limit 10
"""
from __future__ import annotations

import argparse
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--subreddit", default="all")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--sort", default="relevance", choices=["relevance", "hot", "top", "new", "comments"])
    args = parser.parse_args()

    missing = [k for k in ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"] if not os.getenv(k)]
    if missing:
        print("missing env: " + ", ".join(missing), file=sys.stderr)
        print("create an approved Reddit app/token first; browser login alone is not enough for API calls", file=sys.stderr)
        return 2

    try:
        import praw
    except ImportError:
        print("missing dependency: praw. run `.venv/bin/python -m pip install praw`", file=sys.stderr)
        return 2

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )
    subreddit = reddit.subreddit(args.subreddit)
    for i, post in enumerate(subreddit.search(args.query, sort=args.sort, limit=args.limit), 1):
        print(f"[{i}] r/{post.subreddit} | score={post.score} | comments={post.num_comments}")
        print(post.title)
        print(f"https://www.reddit.com{post.permalink}")
        if getattr(post, "selftext", ""):
            text = post.selftext.replace("\n", " ")[:300]
            print(text)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
