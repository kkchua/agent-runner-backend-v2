#!/usr/bin/env python3
"""Seed an API key directly into the database."""
from agent_runner_backend_v2.auth.api_key_auth import generate_api_key
from agent_runner_backend_v2.database.api_key_repository import create_api_key
from agent_runner_backend_v2.database import SessionLocal

db = SessionLocal()
plain_key, key_hash = generate_api_key()
create_api_key(
    db,
    key_hash=key_hash,
    key_prefix=plain_key[:8],
    name="chua-worker-01",
    role="service-account",
    created_by="seed",
)
db.commit()
print(f"API Key created: {plain_key}")
print("Use this key in your daemon config as X-API-Key header.")
db.close()
