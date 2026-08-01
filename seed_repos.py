"""Seed repos and workflow assignments from operator-console.json config."""
import json
import sys
from urllib import request, error

BASE = "http://localhost:8200"

REPOS = {
    "agent-runner-v2": [
        ("workflow_builder_v1", "Workflow Builder v1"),
        ("sdlc_00_init_doc_v1", "SDLC-00: INIT Doc"),
        ("sdlc_10_requirement_v1", "SDLC-10: Requirement Intake"),
        ("sdlc_20_planning_v1", "SDLC-20: Planning"),
        ("sdlc_30_backlog_v1", "SDLC-30: Backlog"),
        ("sdlc_40_task_v1", "SDLC-40: Task"),
        ("sdlc_50_implementation_v1", "SDLC-50: Implementation"),
        ("sdlc_60_execution_v1", "SDLC-60: Execution"),
        ("sdlc_70_validation_v1", "SDLC-70: Validation"),
        ("sdlc_80_review_v1", "SDLC-80: Review"),
        ("01_governance_foundation_v1", "Governance Foundation"),
        ("02_agent_runner_platform_v1", "Agent Runner Platform v1"),
        ("sdlc_00_codebase_v1", "Repository Codebase Sync"),
        ("sdlc_00_delivery_scaffold_v1", "Repository Delivery Doc Scaffold"),
    ],
    "Agnes-AI": [
        ("agnes_media_gen_v1", "Agnes Media Generator v1"),
        ("agnes_gen_video_v1", "Agnes Video Generator v1"),
    ],
    "agent-runner-backend": [
        ("sdlc_00_codebase_v1", "REPO Codebase v1"),
    ],
    "WSL-agent-runner-backend": [
        ("sdlc_00_codebase_v1", "REPO Codebase v1"),
    ],
}


def api_get(path):
    req = request.Request(f"{BASE}{path}")
    with request.urlopen(req) as r:
        return json.loads(r.read())


def api_post(path, data):
    body = json.dumps(data).encode()
    req = request.Request(f"{BASE}{path}", data=body, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req) as r:
        return json.loads(r.read())


def main():
    repos = api_get("/api/repos")
    repo_lookup = {r["name"]: r["id"] for r in repos}

    total = 0
    for repo_name, workflows in REPOS.items():
        repo_id = repo_lookup.get(repo_name)
        if not repo_id:
            print(f"SKIP: repo '{repo_name}' not found", flush=True)
            continue
        for wf_name, display in workflows:
            try:
                api_post(f"/api/repos/{repo_id}/workflows", {
                    "workflow_name": wf_name,
                    "display_name": display,
                })
                total += 1
                print(f"  OK: {repo_name} <- {wf_name}", flush=True)
            except error.HTTPError as e:
                if e.code == 409:
                    print(f"  EXISTS: {repo_name} <- {wf_name}", flush=True)
                else:
                    print(f"  FAIL: {repo_name} <- {wf_name}: {e}", flush=True)

    print(f"\nDone: {total} assignments created", flush=True)


if __name__ == "__main__":
    main()
