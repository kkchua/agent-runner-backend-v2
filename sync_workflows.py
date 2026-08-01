"""Sync workflow definitions from agent-runner-v2 to V2 backend."""
import sys
import json
from pathlib import Path
from urllib import request

# Add agent-runner-v2 to path
sys.path.insert(0, r'D:\MyProjectSpace\01_Workflows\agent-runner-v2')

from agent_runner_v2.workflow_packages.loader import load_workflow_package

V2_BACKEND = 'http://localhost:8200'
WORKFLOWS_DIR = Path(r'D:\MyProjectSpace\01_Workflows\agent-runner-v2\workflows')

def sync_workflow(wf_dir: Path) -> bool:
    """Sync a single workflow to V2 backend."""
    try:
        bundle = load_workflow_package(wf_dir)
        sys.stdout.write(f'Syncing {bundle.name}... ')
        sys.stdout.flush()

        # Convert to V2 format
        definition = {
            'job_prefix': bundle.job_prefix,
            'init_step': bundle.init_step,
            'default_max_rejects': bundle.default_max_rejects,
            'steps': {}
        }

        for step_name, step_config in bundle.steps.items():
            step_def = {}
            # Handle step_config attributes safely
            if hasattr(step_config, 'onsuccess') and step_config.onsuccess:
                step_def['onsuccess'] = step_config.onsuccess
            if hasattr(step_config, 'requires_human_approval_after') and step_config.requires_human_approval_after:
                step_def['requires_human_approval_after'] = True
            if hasattr(step_config, 'on_reject_refine') and step_config.on_reject_refine:
                step_def['on_reject_refine'] = step_config.on_reject_refine
            if hasattr(step_config, 'on_exhaust_replan') and step_config.on_exhaust_replan:
                step_def['on_exhaust_replan'] = step_config.on_exhaust_replan
            if hasattr(step_config, 'coder') and step_config.coder:
                step_def['coder'] = step_config.coder
            if hasattr(step_config, 'action') and step_config.action:
                step_def['action'] = step_config.action
            if hasattr(step_config, 'prompt') and step_config.prompt:
                step_def['prompt'] = step_config.prompt
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
