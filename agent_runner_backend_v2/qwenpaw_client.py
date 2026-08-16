#!/usr/bin/env python3
"""
qwenpaw_client.py — Client for interacting with the QwenPaw Agent REST API 
and Telegram Bot API.

Provides functions to push updates to:
1. QwenPaw Console (for the agent to monitor).
2. Telegram (for the user to see).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.request
import urllib.error
from typing import Any

# ---------------------------------------------------------------------------
# Load .env into os.environ
# NOTE: pydantic-settings loads .env into the Settings object but NOT into
# os.environ, so qwenpaw_client's os.environ.get() fallbacks never saw it.
# This ensures QWENPAW_* / TELEGRAM_* vars reach the process environment.
# Existing process env vars take precedence (override=False).
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
    if _ENV_PATH.exists():
        load_dotenv(_ENV_PATH, override=True)
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def _resolve_credentials() -> tuple[str, str, str, str, str, str, str]:
    """Resolve QwenPaw and Telegram credentials.

    Returns (qwenpaw_url, agent_id, session_id, user_id, tg_bot_token, tg_chat_id, tg_groupchat_id).
    """
    # QwenPaw Credentials
    base_url = os.environ.get("QWENPAW_BASE_URL", "http://localhost:8088").strip()
    agent_id = os.environ.get("QWENPAW_AGENT_ID", "default").strip()
    session_id = os.environ.get("QWENPAW_SESSION_ID", "telegram:1531706495").strip()
    user_id = os.environ.get("QWENPAW_USER_ID", "agent-runner-backend").strip()
    
    # Telegram Credentials (from env)
    tg_token = os.environ.get("TELEGRAM_KOON01_BOT_TOKEN", "").strip()
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    tg_groupchat = os.environ.get("TELEGRAM_GROUPCHAT_ID", "").strip()
    
    return base_url, agent_id, session_id, user_id, tg_token, tg_chat, tg_groupchat


# ---------------------------------------------------------------------------
# 1. QwenPaw Console Notification
# ---------------------------------------------------------------------------

def notify_qwenpaw_agent(
    message: str,
    session_id: str | None = None,
    agent_id: str | None = None,
    base_url: str | None = None,
    user_id: str | None = None,
    timeout: int = 10
) -> bool:
    """Sends a message to the QwenPaw Console."""
    try:
        def_url, def_agent, def_session, def_user_id, _, _, _ = _resolve_credentials()
        final_url = base_url or def_url
        final_agent = agent_id or def_agent
        final_session = session_id or def_session
        final_user_id = user_id or def_user_id

        if not final_url or not final_agent or not final_session:
            print("[qwenpaw_client] Missing QwenPaw credentials.", flush=True)
            return False

        payload = {
            "input": [{"role": "user", "content": [{"type": "text", "text": message}]}],
            "session_id": final_session,
            "user_id": final_user_id,
            "channel": "console"
        }

        chat_url = f"{final_url}/api/console/chat"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(chat_url, data=data, method="POST", headers={"Content-Type": "application/json", "X-Agent-Id": final_agent})

        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                print(f"[qwenpaw_client] Sent to Console: {final_session}", flush=True)
                return True
    except Exception as exc:
        print(f"[qwenpaw_client] QwenPaw notification failed: {exc}", flush=True)
    return False


# ---------------------------------------------------------------------------
# 2. Telegram Bot Notification
# ---------------------------------------------------------------------------

def notify_telegram(
    message: str,
    bot_token: str | None = None,
    chat_id: str | None = None,
    timeout: int = 10
) -> bool:
    """Sends a message directly to Telegram via Bot API."""
    try:
        _, _, _, _, def_token, def_chat, def_groupchat = _resolve_credentials()
        final_token = bot_token or def_token
        final_chat = def_groupchat

        if not final_token or not final_chat:
            print("[qwenpaw_client] Missing Telegram credentials (TELEGRAM_BOT_TOKEN/CHAT_ID).", flush=True)
            return False

        # Telegram Bot API URL
        url = f"https://api.telegram.org/bot{final_token}/sendMessage"
        payload = {
            "chat_id": final_chat,
            "text": message,
            "parse_mode": "Markdown"
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})

        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                print(f"[qwenpaw_client] Sent to Telegram: chat {final_chat}", flush=True)
                return True
            else:
                print(f"[qwenpaw_client] Telegram API Error: {result.get('description')}", flush=True)
                return False
    except Exception as exc:
        print(f"[qwenpaw_client] Telegram notification failed: {exc}", flush=True)
    return False
