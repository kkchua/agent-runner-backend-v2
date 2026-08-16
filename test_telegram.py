#!/usr/bin/env python3
"""Test Telegram notification."""
from agent_runner_backend_v2.qwenpaw_client import notify_telegram

# Simple test message
msg = "Test message from backend"
print(f"Sending message: {msg}")
result = notify_telegram(msg)
print(f"Result: {result}")

# Test with the full format
full_msg = """⚠️ *[AGB Events]*
*Status:* AWAITING_INTERVENTION

*Workflow:* test_wf
*Job ID:* TEST-001
*Worker:* chua-worker-01
*Duration:* 5m 30s

*Action Required:* RETRY"""

print(f"\nSending full message...")
result2 = notify_telegram(full_msg)
print(f"Result: {result2}")
