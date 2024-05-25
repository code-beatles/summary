from __future__ import annotations

from muffin_rest import Api

from summary import app

api = Api(app, prefix="/api/v1")

app.import_submodules()
