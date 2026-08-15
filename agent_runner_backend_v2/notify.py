#!/usr/bin/env python3
"""
notify.py — Standalone notification script for agent-runner-v2.

Call this from the backend to send notifications to QwenPaw Console
and/or Telegram channels.

Usage:
    python -m agent_runner_backend_v2.notify --step generate_implementation \
        --outcome approved --run-code SDLC50IMP-xxx \
        --workflow sdlc_50_implementation_v1 \
        --job-dir "C:\Users\kengk\.ukbe-runner\jobs\20260814\..." \
        --project "D:\MyProjectSpace\01_Workflows\agent-runner-v2" \
        --tokens 92200 \
        --artifacts '{"TASK_FILE": "TASK-xxx.md", "IMPL_FILE": "IMPL-xxx.md"}'

    # Terminal job notification
    python -m agent_runner_backend_v2.notify --status COMPLETED \
        --run-code SDLC50IMP-xxx --workflow sdlc_50_implementation_v1 \
        --job-dir "..." --project "..." --duration "5m 30s"
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# Load .env into os.environ
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    if _ENV_PATH.exists():
        load_dotenv(_ENV_PATH, override=False)
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Credential resolution
# ---------------------------------------------------------------------------

def _resolve_credentials() -> dict:
    """Resolve all notification credentials from environment."""
    return {
        "qwenpaw_url": os.environ.get("QWENPAW_BASE_URL", "http://localhost:8088").strip(),
        "qwenpaw_agent_id": os.environ.get("QWENPAW_AGENT_ID", "default").strip(),
        "qwenpaw_session_id": os.environ.get("QWENPAW_SESSION_ID", "").strip(),
        "qwenpaw_user_id": os.environ.get("QWENPAW_USER_ID", "default").strip(),
        "tg_bot_token": os.environ.get("TELEGRAM_KOON01_BOT_TOKEN", "").strip(),
        "tg_chat_id": os.environ.get("TELEGRAM_CHAT_ID", "").strip(),
        "tg_groupchat_id": os.environ.get("TELEGRAM_GROUPCHAT_ID", "").strip(),
    }


# ---------------------------------------------------------------------------
# Notification functions
# ---------------------------------------------------------------------------

def notify_qwenpaw(
    message: str,
    creds: dict | None = None,
    timeout: int = 10,
) -> bool:
    """Send a message to QwenPaw Console."""
    creds = creds or _resolve_credentials()
    session_id = creds.get("qwenpaw_session_id", "")
    if not session_id:
        print("[notify] QwenPaw: no session_id configured — skipped", flush=True)
        return False

    payload = {
        "input": [{"role": "user", "content": [{"type": "text", "text": message}]}],
        "session_id": session_id,
        "user_id": creds.get("qwenpaw_user_id", "default"),
        "channel": "console",
    }

    url = f"{creds['qwenpaw_url']}/api/console/chat"
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Agent-Id": creds["qwenpaw_agent_id"],
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ok = resp.status == 200
            print(f"[notify] QwenPaw: {'sent' if ok else 'failed'} (session={session_id})", flush=True)
            return ok
    except Exception as exc:
        print(f"[notify] QwenPaw failed: {exc}", flush=True)
        return False


def notify_telegram(
    message: str,
    chat_id: str | None = None,
    creds: dict | None = None,
    timeout: int = 10,
) -> bool:
    """Send a message to a Telegram chat."""
    creds = creds or _resolve_credentials()
    token = creds.get("tg_bot_token", "")
    target_chat = chat_id or creds.get("tg_chat_id", "")

    if not token or not target_chat:
        print("[notify] Telegram: no token or chat_id configured — skipped", flush=True)
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_chat,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                print(f"[notify] Telegram: sent to {target_chat}", flush=True)
                return True
            else:
                print(f"[notify] Telegram error: {result.get('description')}", flush=True)
                return False
    except Exception as exc:
        print(f"[notify] Telegram failed: {exc}", flush=True)
        return False


# ---------------------------------------------------------------------------
# Message builders
# ---------------------------------------------------------------------------

def build_step_message(
    step_name: str,
    outcome: str,
    run_code: str,
    workflow: str = "",
    project_root: str = "",
    job_dir: str = "",
    tokens: int | None = None,
    artifacts: dict | None = None,
    failure_class: str | None = None,
    error_message: str | None = None,
    next_status: str | None = None,
) -> str:
    """Build step-level notification message."""
    if outcome == "approved":
        emoji = "✅"
    elif outcome == "rejected":
        emoji = "🔄"
    elif outcome == "failed":
        emoji = "❌"
    else:
        emoji = "ℹ️"

    lines = [
        f"{emoji} *[AGB Step]*",
        f"*Workflow:* {workflow}",
        f"*Job ID:* {run_code}",
        f"*Project:* {project_root or 'N/A'}",
        "",
        "━━━ *Step Result* ━━━",
        f"*Step:* {step_name}",
        f"*Outcome:* {outcome.upper()}",
    ]

    if failure_class:
        lines.append(f"*Failure Class:* {failure_class}")
    if error_message:
        lines.append("")
        lines.append("━━━ *Error* ━━━")
        lines.append(f"`{error_message[:300]}`")

    if tokens:
        lines.append("")
        lines.append("━━━ *Usage* ━━━")
        lines.append(f"*Tokens:* {tokens:,}")

    if artifacts:
        lines.append("")
        lines.append("━━━ *Artifacts* ━━━")
        for key, path in artifacts.items():
            fname = path.split("\\")[-1].split("/")[-1] if isinstance(path, str) else str(path)
            lines.append(f"*{key}:* `{fname}`")

    if next_status:
        lines.append("")
        lines.append(f"*Next Status:* {next_status}")

    paths = []
    if job_dir:
        paths.append(f"*Job Dir:* `{job_dir}`")
    if project_root:
        paths.append(f"*Project Root:* `{project_root}`")
    if paths:
        lines.append("")
        lines.append("━━━ *Where to Review* ━━━")
        lines.extend(paths)

    return "\n".join(lines)


def build_job_message(
    status: str,
    run_code: str,
    workflow: str = "",
    project_root: str = "",
    job_dir: str = "",
    duration: str = "",
    current_step: str = "",
    action_requested: str | None = None,
    action_feedback: str | None = None,
    error_message: str | None = None,
    refine_iterations: dict | None = None,
) -> str:
    """Build job-level notification message."""
    if status == "COMPLETED":
        emoji = "✅"
    elif status in ("FAILED", "CANCELLED"):
        emoji = "❌"
    else:
        emoji = "⚠️"

    lines = [
        f"{emoji} *[AGB Events]*",
        f"*Status:* {status}",
        "",
        "━━━ *Job Info* ━━━",
        f"*Workflow:* {workflow}",
        f"*Job ID:* {run_code}",
    ]

    if duration:
        lines.append(f"*Duration:* {duration}")
    if current_step:
        lines.append(f"*Current Step:* {current_step}")

    if status in ("WAITING_FOR_HUMAN_APPROVAL", "AWAITING_INTERVENTION"):
        lines.append("")
        lines.append("━━━ *Action Required* ━━━")
        lines.append(f"*Action:* {action_requested or 'REVIEW'}")
        if action_feedback:
            lines.append(f"*Feedback:* {action_feedback[:200]}")

    if error_message:
        lines.append("")
        lines.append("━━━ *Error* ━━━")
        lines.append(f"`{error_message[:300]}`")

    paths = []
    if project_root:
        paths.append(f"*Project:* `{project_root}`")
    if job_dir:
        paths.append(f"*Job Dir:* `{job_dir}`")
    if paths:
        lines.append("")
        lines.append("━━━ *Paths* ━━━")
        lines.extend(paths)

    if refine_iterations:
        info = ", ".join(f"{step}: {count}x" for step, count in refine_iterations.items())
        if info:
            lines.append("")
            lines.append(f"*Refine Iterations:* {info}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main entry point (CLI)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Send agent-runner notifications")
    parser.add_argument("--step", help="Step name (for step-level notifications)")
    parser.add_argument("--outcome", help="Step outcome: approved, rejected, failed")
    parser.add_argument("--status", help="Job status (for job-level notifications)")
    parser.add_argument("--run-code", dest="run_code", required=True, help="Job run code")
    parser.add_argument("--workflow", default="", help="Workflow name")
    parser.add_argument("--project", default="", dest="project_root", help="Project root path")
    parser.add_argument("--job-dir", default="", dest="job_dir", help="Job directory path")
    parser.add_argument("--tokens", type=int, default=None, help="Token usage")
    parser.add_argument("--artifacts", type=json.loads, default=None, help="Artifacts dict (JSON string)")
    parser.add_argument("--failure-class", dest="failure_class", default=None, help="Failure class")
    parser.add_argument("--error-message", dest="error_message", default=None, help="Error message")
    parser.add_argument("--next-status", dest="next_status", default=None, help="Next run status")
    parser.add_argument("--duration", default="", help="Job duration string")
    parser.add_argument("--current-step", dest="current_step", default="", help="Current step name")
    parser.add_argument("--action", dest="action_requested", default=None, help="Action requested")
    parser.add_argument("--feedback", dest="action_feedback", default=None, help="Action feedback")
    parser.add_argument("--refine", type=json.loads, default=None, dest="refine_iterations", help="Refine iterations (JSON)")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP timeout seconds")
    parser.add_argument("--channels", default="both", choices=["qwenpaw", "telegram", "both"], help="Notification channels")

    args = parser.parse_args()
    creds = _resolve_credentials()

    # Build message
    if args.step and args.outcome:
        message = build_step_message(
            step_name=args.step,
            outcome=args.outcome,
            run_code=args.run_code,
            workflow=args.workflow,
            project_root=args.project_root,
            job_dir=args.job_dir,
            tokens=args.tokens,
            artifacts=args.artifacts,
            failure_class=args.failure_class,
            error_message=args.error_message,
            next_status=args.next_status,
        )
    elif args.status:
        message = build_job_message(
            status=args.status,
            run_code=args.run_code,
            workflow=args.workflow,
            project_root=args.project_root,
            job_dir=args.job_dir,
            duration=args.duration,
            current_step=args.current_step,
            action_requested=args.action_requested,
            action_feedback=args.action_feedback,
            error_message=args.error_message,
            refine_iterations=args.refine,
        )
    else:
        print("Error: provide either --step + --outcome, or --status", file=sys.stderr)
        sys.exit(1)

    # Send
    if args.channels in ("qwenpaw", "both"):
        notify_qwenpaw(message, creds=creds, timeout=args.timeout)
    if args.channels in ("telegram", "both"):
        notify_telegram(message, creds=creds, timeout=args.timeout)


if __name__ == "__main__":
    main()
