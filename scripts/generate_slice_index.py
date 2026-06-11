#!/usr/bin/env python3
"""
Generate _data/slice-index.json from slice.yaml manifests across all Slice_*
repos in the feastorg GitHub organization.

Usage:
    python3 scripts/generate_slice_index.py

Environment:
    GITHUB_TOKEN  — required; a token with read access to the feastorg org.
                    GITHUB_TOKEN is available automatically in Actions.

Output:
    _data/slice-index.json
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
OUTPUT = Path("_data/slice-index.json")
API = "https://api.github.com"

# Fields to extract from each slice.yaml (all nullable)
EXTRACT = [
    ("id", lambda m: m.get("id")),
    ("name", lambda m: m.get("name")),
    ("status", lambda m: m.get("status")),
    ("category", lambda m: m.get("category")),
    ("summary", lambda m: m.get("summary")),
    ("hw_version", lambda m: (m.get("version") or {}).get("hardware")),
    ("fw_version", lambda m: (m.get("version") or {}).get("firmware")),
    ("hw_gen_current", lambda m: (m.get("hardware") or {}).get("hw_gen_current")),
    ("schema_version", lambda m: m.get("schema_version")),
    ("tags", lambda m: (m.get("metadata") or {}).get("tags", [])),
    ("url", lambda m: (m.get("repository") or {}).get("url")),
    ("updated", lambda m: (m.get("metadata") or {}).get("updated")),
]

STATUS_ORDER = ["released", "validated", "prototype", "concept", "deprecated"]
CATEGORY_ORDER = [
    "actuation",
    "sensing",
    "integrated",
    "power",
    "interface",
    "template",
    "prototype",
]


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


def list_slice_repos(session: requests.Session) -> list[str]:
    """Return names of all public Slice_* repos in the org."""
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
        repos.extend(
            repo["name"] for repo in batch if repo["name"].startswith("Slice_")
        )
        page += 1
    return sorted(repos)


def fetch_manifest(session: requests.Session, repo: str) -> dict | None:
    """Fetch and parse slice.yaml from the repo's default branch."""
    url = f"https://raw.githubusercontent.com/{ORG}/{repo}/main/slice.yaml"
    r = session.get(url)
    if r.status_code == 404:
        print(f"  SKIP {repo}: no slice.yaml", flush=True)
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
    return entry


def sort_key(entry: dict) -> tuple:
    status_rank = (
        STATUS_ORDER.index(entry["status"]) if entry["status"] in STATUS_ORDER else 99
    )
    cat_rank = (
        CATEGORY_ORDER.index(entry["category"])
        if entry["category"] in CATEGORY_ORDER
        else 99
    )
    return (status_rank, cat_rank, entry.get("id") or "")


def main() -> None:
    session = gh_session()

    print(f"Listing Slice_* repos in {ORG}...", flush=True)
    repos = list_slice_repos(session)
    print(f"Found {len(repos)} repos.", flush=True)

    slices = []
    for repo in repos:
        print(f"  Fetching {repo}...", flush=True)
        manifest = fetch_manifest(session, repo)
        if manifest is None:
            continue
        slices.append(extract(manifest, repo))

    slices.sort(key=sort_key)

    # Summary counts
    summary: dict[str, int] = {}
    for s in slices:
        key = s.get("status") or "unknown"
        summary[key] = summary.get(key, 0) + 1

    output = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": len(slices),
        "summary": summary,
        "slices": slices,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(slices)} slices to {OUTPUT}", flush=True)
    for status, count in sorted(summary.items()):
        print(f"  {status}: {count}", flush=True)


if __name__ == "__main__":
    main()
