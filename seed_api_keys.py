#!/usr/bin/env python3
"""Seed multiple API keys for common use cases."""
from agent_runner_backend_v2.auth.api_key_auth import generate_api_key
from agent_runner_backend_v2.database.api_key_repository import create_api_key
from agent_runner_backend_v2.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Clear existing keys (optional - comment out to keep existing)
db.execute(text("DELETE FROM api_keys"))

keys_to_create = [
    {"name": "chua-worker-01", "role": "service-account"},
    {"name": "admin-cli", "role": "admin"},
    {"name": "operator-console", "role": "operator"},
]

print("=" * 60)
print("API Keys Created")
print("=" * 60)

for key_config in keys_to_create:
    plain_key, key_hash = generate_api_key()
    create_api_key(
        db,
        key_hash=key_hash,
        key_prefix=plain_key[:8],
        name=key_config["name"],
        role=key_config["role"],
        created_by="seed",
    )
    print(f"\nName: {key_config['name']}")
    print(f"Role: {key_config['role']}")
    print(f"Key:  {plain_key}")

db.commit()
print("\n" + "=" * 60)
print("Store these keys securely - they cannot be retrieved later!")
print("=" * 60)
db.close()
