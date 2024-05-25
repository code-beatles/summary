from __future__ import annotations

from summary import app


@app.route("/")
async def index(request):
    return f"{app.cfg.NAME} v{app.cfg.VERSION}"
