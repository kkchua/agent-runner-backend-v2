"""Sync workflow definitions from agent-runner-v2 to V2 backend."""
import sys
import json
from pathlib import Path
from urllib import request

# Add agent-runner-v2 to path
sys.path.insert(0, r'D:\MyProjectSpace\01_Workflows\agent-runner-v2')

from agent_runner_v2.workflow_packages.loader import (
    load_workflow_package,
    bundle_to_template_group_dict,
)

V2_BACKEND = 'http://localhost:8200'
WORKFLOWS_DIR = Path(r'D:\MyProjectSpace\01_Workflows\agent-runner-v2\workflows')

def sync_workflow(wf_dir: Path) -> bool:
    """Sync a single workflow to V2 backend."""
    try:
        bundle = load_workflow_package(wf_dir)
        sys.stdout.write(f'Syncing {bundle.name}... ')
        sys.stdout.flush()

        # Use the same adapter as the runner's sync to get the canonical dict
        group_dict = bundle_to_template_group_dict(bundle)

        # Strip non-serializable bundle refs
        for cfg in group_dict.get("step_configs", {}).values():
            cfg.pop("_workflow_bundle", None)

        # Convert TEMPLATE_GROUPS format to V2 backend format
        # V1: {"steps": [...], "step_configs": {"name": {"onsuccess": "..."}}}
        # V2: {"steps": {"name": {"onsuccess": "..."}}}
        step_configs = group_dict.get("step_configs", {})
        steps_order = group_dict.get("steps", [])

        definition = {
            'job_prefix': group_dict.get('job_prefix', 'JOB'),
            'init_step': group_dict.get('job_init_step'),
            'default_max_rejects': group_dict.get('default_max_rejects', 0),
            'steps': {},
        }

        for step_name in steps_order:
            cfg = step_configs.get(step_name, {})
            step_def = {}
            # Copy routing: onsuccess is in extra/passthrough
            if 'onsuccess' in cfg:
                step_def['onsuccess'] = cfg['onsuccess']
            if cfg.get('requires_human_approval_after'):
                step_def['requires_human_approval_after'] = True
            if 'on_reject_refine' in cfg:
                step_def['on_reject_refine'] = cfg['on_reject_refine']
            if 'on_exhaust_replan' in cfg:
                step_def['on_exhaust_replan'] = cfg['on_exhaust_replan']
            if 'coder' in cfg:
                step_def['coder'] = cfg['coder']
            if 'action' in cfg:
                step_def['action'] = cfg['action']
            if 'prompt_file' in cfg:
                step_def['prompt_file'] = cfg['prompt_file']
            definition['steps'][step_name] = step_def

        # Send to backend
        data = json.dumps({
            'workflow_name': bundle.name,
            'definition': definition
        }).encode()

        req = request.Request(
            f'{V2_BACKEND}/api/workflows/sync',
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        r = request.urlopen(req)

        if r.status == 200:
            sys.stdout.write('OK\n')
            sys.stdout.flush()
            return True
        else:
            sys.stdout.write(f'FAILED (status {r.status})\n')
            sys.stdout.flush()
            return False

    except Exception as e:
        import traceback
        sys.stdout.write(f'ERROR: {e}\n')
        traceback.print_exc()
        sys.stdout.flush()
        return False

def main():
    """Sync all workflows."""
    sys.stdout.write(f'Syncing workflows from {WORKFLOWS_DIR} to {V2_BACKEND}\n\n')
    sys.stdout.flush()

    synced = 0
    failed = 0

    for wf_dir in sorted(WORKFLOWS_DIR.iterdir()):
        if wf_dir.is_dir() and (wf_dir / 'workflow.toml').exists():
            if sync_workflow(wf_dir):
                synced += 1
            else:
                failed += 1

    sys.stdout.write(f'\nDone: {synced} synced, {failed} failed\n')
    sys.stdout.flush()

if __name__ == '__main__':
    main()
