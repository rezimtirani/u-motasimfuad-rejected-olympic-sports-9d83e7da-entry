"""Upload this entry's files to its GitHub repository.

Pushes main.py and README.md to the public repo for the
Rejected Olympic Sports bounty, using the stored GitHub PAT
(custom.github) through the surrogate credential helper.

Usage, from the entry folder:
    python3 gh_upload_rejected_olympic_sports.py

The repository must already exist (created with create_repo.py);
this script only creates or updates files inside it.
"""

import base64
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")

from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-motasimfuad-rejected-olympic-sports-9d83e7da-entry"
API = "https://api.github.com"
HERE = Path(__file__).resolve().parent
FILES = ["main.py", "README.md"]


def github_request(method, url, payload=None):
    """Send one authenticated GitHub API request and return its JSON."""
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def existing_sha(path):
    """Return the blob SHA of a file already in the repo, else None."""
    try:
        info = github_request("GET", f"{API}/repos/{OWNER}/{REPO}/contents/{path}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def push_file(path):
    """Create or update one file in the repo from the local copy."""
    local = HERE / path
    encoded = base64.b64encode(local.read_bytes()).decode("ascii")
    payload = {
        "message": f"Add {path} — Rejected Olympic Sports entry",
        "content": encoded,
    }
    sha = existing_sha(path)
    if sha:
        payload["sha"] = sha
    result = github_request(
        "PUT", f"{API}/repos/{OWNER}/{REPO}/contents/{path}", payload
    )
    print(f"{path}: {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in FILES:
        push_file(name)
    print(f"Done: {OWNER}/{REPO}")


if __name__ == "__main__":
    main()
