#!/usr/bin/env python3
"""
Generate _data/loaf-index.json from loaf.yaml manifests across all Loaf_* repos
in the feastorg GitHub organization.

Usage:
    python3 scripts/generate_loaf_index.py

Environment:
    GITHUB_TOKEN  — required; a token with read access to the feastorg org.
                    GITHUB_TOKEN is available automatically in Actions.

Output:
    _data/loaf-index.json
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
OUTPUT = Path("_data/loaf-index.json")
API = "https://api.github.com"

# Fields to extract from each loaf.yaml (all nullable)
EXTRACT = [
    ("id", lambda m: m.get("id")),
    ("name", lambda m: m.get("name")),
    ("status", lambda m: m.get("status")),
    ("role", lambda m: m.get("role")),
    ("summary", lambda m: m.get("summary")),
    ("slice_slots", lambda m: (m.get("interconnect") or {}).get("slice_slots")),
    ("bus_type", lambda m: ((m.get("interconnect") or {}).get("bus") or {}).get("type")),
    ("hw_version", lambda m: (m.get("version") or {}).get("hardware")),
    ("hw_gen_current", lambda m: (m.get("hardware") or {}).get("hw_gen_current")),
    ("pcb_layers", lambda m: ((m.get("hardware") or {}).get("pcb") or {}).get("layers")),
    ("schema_version", lambda m: m.get("schema_version")),
    ("tags", lambda m: (m.get("metadata") or {}).get("tags", [])),
    ("updated", lambda m: (m.get("metadata") or {}).get("updated")),
]

STATUS_ORDER = ["released", "validated", "prototype", "concept", "deprecated"]
ROLE_ORDER = ["backplane", "hybrid", "controller"]


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


def list_loaf_repos(session: requests.Session) -> list[str]:
    """Return names of all public Loaf_* repos in the org."""
    repos = []
    page = 1
    while True:
        r = session.get(
            f"{API}/orgs/{ORG}/repos",
            params={"type": "public", "per_page": 100, "page": page},
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        repos.extend(repo["name"] for repo in batch if repo["name"].startswith("Loaf_"))
        page += 1
    return sorted(repos)


def fetch_manifest(session: requests.Session, repo: str) -> dict | None:
    """Fetch and parse loaf.yaml from the repo's default branch."""
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/main/loaf.yaml"
    r = session.get(url)
    if r.status_code == 404:
        print(f"  SKIP {repo}: no loaf.yaml", flush=True)
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
        STATUS_ORDER.index(entry["status"]) if entry["status"] in STATUS_ORDER else 99
    )
    role_rank = ROLE_ORDER.index(entry["role"]) if entry["role"] in ROLE_ORDER else 99
    return (status_rank, role_rank, entry.get("id") or "")


def main() -> None:
    session = gh_session()

    print(f"Listing Loaf_* repos in {ORG}...", flush=True)
    repos = list_loaf_repos(session)
    print(f"Found {len(repos)} repos.", flush=True)

    loaves = []
    for repo in repos:
        print(f"  Fetching {repo}...", flush=True)
        manifest = fetch_manifest(session, repo)
        if manifest is None:
            continue
        loaves.append(extract(manifest, repo))

    loaves.sort(key=sort_key)

    summary: dict[str, int] = {}
    for entry in loaves:
        key = entry.get("status") or "unknown"
        summary[key] = summary.get(key, 0) + 1

    output = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(loaves),
        "summary": summary,
        "loaves": loaves,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(loaves)} loaves to {OUTPUT}", flush=True)
    for status, count in sorted(summary.items()):
        print(f"  {status}: {count}", flush=True)


if __name__ == "__main__":
    main()
