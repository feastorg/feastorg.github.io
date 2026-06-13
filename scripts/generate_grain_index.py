#!/usr/bin/env python3
"""
Generate _data/grain-index.json from grain.yaml manifests across all
feastorg repos that contain one.

Discovery uses the GitHub Code Search API to find repos with grain.yaml,
avoiding the need to enumerate all repos.

Usage:
    python3 scripts/generate_grain_index.py

Environment:
    GITHUB_TOKEN  — required; a token with read access to the feastorg org.
                    GITHUB_TOKEN is available automatically in Actions.

Output:
    _data/grain-index.json
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Error: 'requests' not installed. Run: pip install requests")

try:
    import yaml
except ImportError:
    sys.exit("Error: 'pyyaml' not installed. Run: pip install pyyaml")

ORG = "feastorg"
OUTPUT = Path("_data/grain-index.json")
API = "https://api.github.com"

# Fields to extract from each grain.yaml
EXTRACT = [
    ("id",            lambda m: m.get("id")),
    ("name",          lambda m: m.get("name")),
    ("status",        lambda m: m.get("status")),
    ("category",      lambda m: m.get("category")),
    ("summary",       lambda m: m.get("summary")),
    ("hw_version",    lambda m: (m.get("version") or {}).get("hardware")),
    ("form_factor",   lambda m: (m.get("hardware") or {}).get("form_factor")),
    ("license_hw",    lambda m: (m.get("license") or {}).get("hardware")),
    ("compatibility", lambda m: m.get("compatibility")),
    ("related_slices",lambda m: m.get("related_slices")),
    ("tags",          lambda m: (m.get("metadata") or {}).get("tags", [])),
    ("updated",       lambda m: (m.get("metadata") or {}).get("updated")),
]

STATUS_ORDER = ["released", "prototype", "concept", "deprecated"]
CATEGORY_ORDER = ["shield", "card", "adapter", "module"]


def gh_session() -> requests.Session:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        sys.exit("Error: GITHUB_TOKEN environment variable not set.")
    s = requests.Session()
    s.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )
    return s


def find_grain_repos(session: requests.Session) -> list[str]:
    """Return distinct repo names that contain grain.yaml via code search."""
    repos: set[str] = set()
    page = 1
    while True:
        r = session.get(
            f"{API}/search/code",
            params={
                "q": f"filename:grain.yaml org:{ORG}",
                "per_page": 100,
                "page": page,
            },
        )
        r.raise_for_status()
        data = r.json()
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            # Only count grain.yaml at the repo root (path == "grain.yaml")
            if item.get("path") == "grain.yaml":
                repos.add(item["repository"]["name"])
        if len(items) < 100:
            break
        page += 1
    return sorted(repos)


def fetch_manifest(session: requests.Session, repo: str) -> dict | None:
    """Fetch and parse grain.yaml from the repo's main branch."""
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/main/grain.yaml"
    r = session.get(url)
    if r.status_code == 404:
        print(f"  SKIP {repo}: no grain.yaml on main", flush=True)
        return None
    r.raise_for_status()
    try:
        return yaml.safe_load(r.text)
    except yaml.YAMLError as e:
        print(f"  WARN {repo}: YAML parse error — {e}", flush=True)
        return None


def extract(manifest: dict, repo: str) -> dict:
    entry = {"repo": repo}
    for key, fn in EXTRACT:
        try:
            entry[key] = fn(manifest)
        except Exception:
            entry[key] = None
    entry["url"] = f"https://feastorg.github.io/{repo}/"
    return entry


def sort_key(entry: dict) -> tuple:
    status_rank = (
        STATUS_ORDER.index(entry["status"])
        if entry["status"] in STATUS_ORDER
        else 99
    )
    cat_rank = (
        CATEGORY_ORDER.index(entry["category"])
        if entry["category"] in CATEGORY_ORDER
        else 99
    )
    return (status_rank, cat_rank, entry.get("id") or "")


def main() -> None:
    session = gh_session()

    print(f"Searching for grain.yaml in {ORG}...", flush=True)
    repos = find_grain_repos(session)
    print(f"Found {len(repos)} repo(s) with grain.yaml at root: {repos}", flush=True)

    grains = []
    for repo in repos:
        print(f"  Fetching {repo}/grain.yaml...", flush=True)
        manifest = fetch_manifest(session, repo)
        if manifest is None:
            continue
        grains.append(extract(manifest, repo))

    grains.sort(key=sort_key)

    summary: dict[str, int] = {}
    for g in grains:
        key = g.get("status") or "unknown"
        summary[key] = summary.get(key, 0) + 1

    output = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(grains),
        "summary": summary,
        "grains": grains,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(grains)} grain(s) to {OUTPUT}", flush=True)
    for status, count in sorted(summary.items()):
        print(f"  {status}: {count}", flush=True)


if __name__ == "__main__":
    main()
