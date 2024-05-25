from __future__ import annotations

from muffin import Application

# Initialize the application
app = Application(
    # Congiturations
    "env:MUFFIN_CONFIG",
    "summary.config.local",
    "summary.config",
    # Options
    name="summary",
    version="0.1.0",
)
cfg = app.cfg
logger = app.logger

# Setup database
from muffin_peewee import Plugin as DB

db = DB(app)

app.import_submodules("api", "views")

# ruff: noqa: N814,E402
