from __future__ import annotations

from . import *

# Common
ENV = "tests"

# Muffin-Peewee-AIO
PEEWEE_CONNECTION = "aiosqlite:///:memory:"
PEEWEE_CONNECTION_PARAMS = {
    "pragmas": [
        ("foreign_keys", "ON"),
        ("journal_mode", "wal"),
        ("synchronous", "normal"),
    ]
}
PEEWEE_AUTO_CONNECTION = False

# ruff: noqa: F401, F403
