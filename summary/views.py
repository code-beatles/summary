from __future__ import annotations

from summary import app, jinja


@app.route("/")
async def index(request):
    return await jinja.render("index.html")
